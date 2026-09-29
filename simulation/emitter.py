"""Ground-truth transmission schedules for the supported emitter behaviors."""

from datetime import timedelta


class Emitter:
    def __init__(self, spec):
        self.spec = spec
        self.emitter_id = int(spec["id"])

    def events(self, duration_seconds, start_time, rng):
        raise NotImplementedError

    def transmission(self, band_id, offset, duration, start_time, rng):
        begin = start_time + timedelta(seconds=offset)
        end = begin + timedelta(seconds=duration)
        power = float(self.spec["power_dbm"]) + rng.gauss(0, float(self.spec.get("power_std_db", 3)))
        return {
            "emitter_id": self.emitter_id,
            "band_id": int(band_id),
            "start_time": begin,
            "end_time": end,
            "signal_strength_dbm": round(power, 2),
        }


class FixedEmitter(Emitter):
    """Transmits on one fixed band using a configurable repeat interval."""

    def events(self, duration_seconds, start_time, rng):
        period = float(self.spec.get("period_seconds", 4))
        pulse = float(self.spec.get("duration_seconds", 0.8))
        phase = float(self.spec.get("phase_seconds", 0))
        if period <= 0 or pulse <= 0:
            raise ValueError(f"Emitter {self.emitter_id}: period and duration must be positive.")
        offset = phase
        while offset < duration_seconds:
            yield self.transmission(self.spec["band_id"], offset, min(pulse, duration_seconds - offset), start_time, rng)
            offset += period


class PeriodicEmitter(Emitter):
    def events(self, duration_seconds, start_time, rng):
        period = float(self.spec["period_seconds"])
        pulse = float(self.spec["duration_seconds"])
        phase = float(self.spec.get("phase_seconds", 0))
        if period <= 0 or pulse <= 0:
            raise ValueError(f"Emitter {self.emitter_id}: period and duration must be positive.")
        offset = phase
        while offset < duration_seconds:
            yield self.transmission(self.spec["band_id"], offset, min(pulse, duration_seconds - offset), start_time, rng)
            offset += period


class BurstEmitter(Emitter):
    def events(self, duration_seconds, start_time, rng):
        probability = float(self.spec["burst_probability"])
        if not 0 <= probability <= 1:
            raise ValueError(f"Emitter {self.emitter_id}: burst_probability must be between 0 and 1.")
        pulse = float(self.spec["duration_seconds"])
        if pulse <= 0:
            raise ValueError(f"Emitter {self.emitter_id}: duration must be positive.")
        for slot in range(int(duration_seconds)):
            if rng.random() < probability:
                offset = slot + rng.random() * min(1, duration_seconds - slot)
                yield self.transmission(self.spec["band_id"], offset, min(pulse, duration_seconds - offset), start_time, rng)


class HoppingEmitter(Emitter):
    def events(self, duration_seconds, start_time, rng):
        pattern = [int(band) for band in self.spec["hop_pattern"]]
        interval = float(self.spec["hop_interval_seconds"])
        pulse = float(self.spec["duration_seconds"])
        if interval <= 0 or pulse <= 0:
            raise ValueError(f"Emitter {self.emitter_id}: hop interval and duration must be positive.")
        offset = float(self.spec.get("phase_seconds", 0))
        hop = 0
        while offset < duration_seconds:
            yield self.transmission(pattern[hop % len(pattern)], offset, min(pulse, duration_seconds - offset), start_time, rng)
            offset += interval
            hop += 1


EMITTER_CLASSES = {
    "fixed": FixedEmitter,
    "periodic": PeriodicEmitter,
    "burst": BurstEmitter,
    "hopping": HoppingEmitter,
}


def generate_transmissions(specs, duration_seconds, start_time, rng):
    events = []
    for spec in specs:
        emitter_type = str(spec["type"]).lower()
        cls = EMITTER_CLASSES[emitter_type]
        events.extend(cls(spec).events(duration_seconds, start_time, rng))
    events.sort(key=lambda item: (item["start_time"], item["emitter_id"]))
    for transmission_id, event in enumerate(events, start=1):
        event["transmission_id"] = transmission_id
    return events
