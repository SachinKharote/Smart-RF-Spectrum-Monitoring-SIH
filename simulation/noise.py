"""Noise, fading, and SNR-based receiver detection model."""

def observe(transmission, noise_config, rng):
    """Return (detected, measured_snr_db); SNR drives every detection decision."""
    noise_floor = float(noise_config["noise_floor_dbm"])
    noise_std = float(noise_config.get("noise_std_db", 3.0))
    threshold = float(noise_config["detection_threshold_db"])
    threshold_jitter = float(noise_config.get("threshold_jitter_db", 1.5))
    noise_power = rng.gauss(noise_floor, noise_std)

    if transmission is None:
        # Noise-only excursions can trigger a false alarm above the same threshold.
        snr_db = noise_power - noise_floor
    else:
        path_loss = rng.uniform(
            float(noise_config.get("path_loss_min_db", 5)),
            float(noise_config.get("path_loss_max_db", 35)),
        )
        fading = rng.gauss(0, float(noise_config.get("fading_std_db", 3)))
        received_power = transmission["signal_strength_dbm"] - path_loss + fading
        snr_db = received_power - noise_power

    decision_threshold = threshold + rng.gauss(0, threshold_jitter)
    detected = snr_db >= decision_threshold
    return detected, round(snr_db, 2)
