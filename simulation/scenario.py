"""Scenario loading and validation for the synthetic RF simulator."""

from pathlib import Path

import yaml


class ScenarioError(ValueError):
    """Raised when a scenario file is missing required or valid values."""


def load_scenario(path):
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScenarioError(f"Scenario file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise ScenarioError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("scenario"), dict):
        raise ScenarioError("Scenario file must contain a 'scenario' mapping.")
    if not isinstance(data.get("emitters"), list) or not data["emitters"]:
        raise ScenarioError("Scenario file must contain a non-empty 'emitters' list.")

    settings = data["scenario"]
    for key in ("duration_seconds", "scans_per_strategy", "dwell_time_ms", "seed", "start_time"):
        if key not in settings:
            raise ScenarioError(f"Missing scenario setting: {key}")
    if settings["duration_seconds"] <= 0 or settings["scans_per_strategy"] <= 0 or settings["dwell_time_ms"] <= 0:
        raise ScenarioError("Duration, scans per strategy, and dwell time must be positive.")

    ids = set()
    allowed_types = {"fixed", "periodic", "burst", "hopping"}
    for emitter in data["emitters"]:
        if not isinstance(emitter, dict):
            raise ScenarioError("Each emitter must be a mapping.")
        for key in ("id", "name", "type", "power_dbm"):
            if key not in emitter:
                raise ScenarioError(f"Emitter is missing required field '{key}'.")
        emitter_type = str(emitter["type"]).lower()
        if emitter_type not in allowed_types:
            raise ScenarioError(f"Unsupported emitter type '{emitter['type']}'.")
        if emitter["id"] in ids:
            raise ScenarioError(f"Duplicate emitter id: {emitter['id']}")
        ids.add(emitter["id"])
        if emitter_type in {"fixed", "periodic", "burst"} and "band_id" not in emitter:
            raise ScenarioError(f"{emitter_type} emitter {emitter['id']} requires band_id.")
        required = {
            "periodic": ("period_seconds", "duration_seconds"),
            "burst": ("burst_probability", "duration_seconds"),
            "hopping": ("hop_interval_seconds", "duration_seconds"),
        }.get(emitter_type, ())
        missing = [key for key in required if key not in emitter]
        if missing:
            raise ScenarioError(f"Emitter {emitter['id']} is missing: {', '.join(missing)}")
        if emitter_type == "hopping" and not emitter.get("hop_pattern"):
            raise ScenarioError(f"Hopping emitter {emitter['id']} requires a non-empty hop_pattern.")
        if "duration_seconds" in emitter and float(emitter["duration_seconds"]) <= 0:
            raise ScenarioError(f"Emitter {emitter['id']} duration_seconds must be positive.")
        if "period_seconds" in emitter and float(emitter["period_seconds"]) <= 0:
            raise ScenarioError(f"Emitter {emitter['id']} period_seconds must be positive.")
        if "hop_interval_seconds" in emitter and float(emitter["hop_interval_seconds"]) <= 0:
            raise ScenarioError(f"Emitter {emitter['id']} hop_interval_seconds must be positive.")
        if "burst_probability" in emitter and not 0 <= float(emitter["burst_probability"]) <= 1:
            raise ScenarioError(f"Emitter {emitter['id']} burst_probability must be from 0 to 1.")
    return data
