"""Generate scenario-driven synthetic RF data in the existing PostgreSQL schema."""

import argparse
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from emitter import generate_transmissions
from noise import observe
from scenario import ScenarioError, load_scenario


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCENARIO = PROJECT_ROOT / "scenarios" / "mixed_emitters.yaml"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, default=DEFAULT_SCENARIO, help="YAML scenario file")
    return parser.parse_args()


def database_config():
    load_dotenv(PROJECT_ROOT / ".env")
    keys = ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD")
    missing = [key for key in keys if not os.getenv(key)]
    if missing:
        raise RuntimeError(f"Missing database settings in .env/environment: {', '.join(missing)}")
    return {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }


def active_transmission(transmissions, band_id, scan_time):
    candidates = [
        tx for tx in transmissions
        if tx["band_id"] == band_id and tx["start_time"] <= scan_time < tx["end_time"]
    ]
    return max(candidates, key=lambda tx: tx["signal_strength_dbm"], default=None)


def emitter_behavior(database_type):
    """Map the existing seed-table labels to engine behavior classes."""
    normalized = " ".join(str(database_type).lower().replace("_", " ").split())
    aliases = {
        "fixed": "fixed",
        "periodic": "periodic",
        "intermittent": "burst",
        "burst": "burst",
        "frequency agile": "hopping",
        "hopping": "hopping",
    }
    if normalized not in aliases:
        raise RuntimeError(f"Unsupported database emitter_type: {database_type!r}")
    return aliases[normalized]


def choose_band(strategy, bands, scan_time, memory, rng):
    if strategy == "Sequential":
        return bands[memory["sequential_index"] % len(bands)][0]
    if strategy == "Random":
        return rng.choice(bands)[0]

    scored = []
    for band_id, priority in bands:
        score = priority + 3.0 * memory["hits"][band_id] - 0.5 * memory["misses"][band_id]
        last = memory["last_detection"][band_id]
        if last is not None:
            elapsed = (scan_time - last).total_seconds()
            score += 5 if elapsed < 5 else (2 if elapsed < 10 else 0)
        scored.append((band_id, score))
    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return scored[0][0] if rng.random() < 0.8 else rng.choice(bands)[0]


def main():
    args = parse_args()
    try:
        scenario = load_scenario(args.scenario)
        config = database_config()
    except (ScenarioError, RuntimeError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    settings = scenario["scenario"]
    start_time = datetime.fromisoformat(str(settings["start_time"]))
    duration = float(settings["duration_seconds"])
    scans_per_strategy = int(settings["scans_per_strategy"])
    dwell_ms = int(settings["dwell_time_ms"])
    strategies = settings.get("strategies", ["Sequential", "Random", "Adaptive"])
    if not strategies or any(s not in {"Sequential", "Random", "Adaptive"} for s in strategies):
        print("Configuration error: strategies must use Sequential, Random, or Adaptive.", file=sys.stderr)
        return 2

    rng = random.Random(int(settings["seed"]))
    try:
        connection = psycopg2.connect(**config)
    except psycopg2.Error as exc:
        print(f"Database connection failed: {exc}", file=sys.stderr)
        return 1

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT band_id, priority FROM frequency_bands ORDER BY band_id;")
            bands = cursor.fetchall()
            cursor.execute("SELECT emitter_id, emitter_name, emitter_type FROM emitters ORDER BY emitter_id;")
            database_emitters = {row[0]: row[1:] for row in cursor.fetchall()}

            if not bands:
                raise RuntimeError("No frequency bands found. Run Database/01_schema.sql and 02_seed_data.sql first.")
            band_ids = {row[0] for row in bands}
            scenario_emitters = {int(spec["id"]): spec for spec in scenario["emitters"]}
            missing_emitters = set(scenario_emitters) - set(database_emitters)
            if missing_emitters:
                raise RuntimeError(
                    "Scenario references emitter IDs absent from the database: "
                    f"{sorted(missing_emitters)}"
                )
            for spec in scenario["emitters"]:
                configured_type = str(spec["type"]).lower()
                seeded_type = emitter_behavior(database_emitters[int(spec["id"])][1])
                if configured_type != seeded_type:
                    raise RuntimeError(
                        f"Emitter {spec['id']} is seeded as {seeded_type!r} but the scenario configures "
                        f"{configured_type!r}. Keep the scenario type aligned with emitters.emitter_type."
                    )
                emitter_type = str(spec["type"]).lower()
                if emitter_type in {"fixed", "periodic", "burst"}:
                    used_bands = [int(spec["band_id"])]
                else:
                    used_bands = [int(value) for value in spec["hop_pattern"]]
                if not set(used_bands).issubset(band_ids):
                    raise RuntimeError(f"Emitter {spec['id']} references a band absent from frequency_bands.")
            if int(settings["dwell_time_ms"]) * scans_per_strategy > duration * 1000:
                raise RuntimeError("scans_per_strategy × dwell_time_ms exceeds scenario duration.")

            transmissions = generate_transmissions(scenario["emitters"], duration, start_time, rng)
            print(f"Connected. Scenario: {settings.get('name', args.scenario.stem)}")
            print(f"Generated {len(transmissions)} ground-truth transmissions.")
            cursor.execute("DELETE FROM intercepts;")
            cursor.execute("DELETE FROM observations;")
            cursor.execute("DELETE FROM scans;")
            cursor.execute("DELETE FROM transmissions;")

            for tx in transmissions:
                cursor.execute(
                    """INSERT INTO transmissions
                       (transmission_id, emitter_id, band_id, start_time, end_time, signal_strength_dbm)
                       VALUES (%s, %s, %s, %s, %s, %s);""",
                    (tx["transmission_id"], tx["emitter_id"], tx["band_id"], tx["start_time"],
                     tx["end_time"], tx["signal_strength_dbm"]),
                )

            scan_id = observation_id = intercept_id = 1
            for strategy in strategies:
                print(f"Running {strategy} strategy...")
                memory = {
                    "sequential_index": 0,
                    "hits": {band_id: 0 for band_id, _ in bands},
                    "misses": {band_id: 0 for band_id, _ in bands},
                    "last_detection": {band_id: None for band_id, _ in bands},
                }
                for scan_number in range(scans_per_strategy):
                    scan_time = start_time + timedelta(milliseconds=scan_number * dwell_ms)
                    band_id = choose_band(strategy, bands, scan_time, memory, rng)
                    if strategy == "Sequential":
                        memory["sequential_index"] += 1
                    tx = active_transmission(transmissions, band_id, scan_time)
                    received_signal, snr_db = observe(tx, scenario.get("noise", {}), rng)
                    actual_signal = tx is not None

                    cursor.execute(
                        "INSERT INTO scans (scan_id, band_id, strategy, scan_time, dwell_time_ms) VALUES (%s, %s, %s, %s, %s);",
                        (scan_id, band_id, strategy, scan_time, dwell_ms),
                    )
                    cursor.execute(
                        "INSERT INTO observations (observation_id, scan_id, band_id, received_signal, actual_signal, snr_db) VALUES (%s, %s, %s, %s, %s, %s);",
                        (observation_id, scan_id, band_id, received_signal, actual_signal, snr_db),
                    )

                    if strategy == "Adaptive":
                        if actual_signal and received_signal:
                            memory["hits"][band_id] += 1
                            memory["last_detection"][band_id] = scan_time
                        elif actual_signal:
                            memory["misses"][band_id] += 1

                    if actual_signal and received_signal:
                        intercept_time = scan_time + timedelta(seconds=rng.uniform(0.02, 0.08))
                        if intercept_time < tx["end_time"]:
                            elapsed_ms = (intercept_time - tx["start_time"]).total_seconds() * 1000
                            cursor.execute(
                                "INSERT INTO intercepts (intercept_id, observation_id, emitter_id, intercept_time, time_error_ms) VALUES (%s, %s, %s, %s, %s);",
                                (intercept_id, observation_id, tx["emitter_id"], intercept_time, round(elapsed_ms, 2)),
                            )
                            intercept_id += 1
                    scan_id += 1
                    observation_id += 1

        connection.commit()
        print("Simulation complete:")
        print(f"  Transmissions: {len(transmissions)}")
        print(f"  Scans/observations: {scan_id - 1}")
        print(f"  Intercepts: {intercept_id - 1}")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (psycopg2.Error, RuntimeError, ValueError) as exc:
        print(f"Simulation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
