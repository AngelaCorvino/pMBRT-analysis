"""Percentage-depth-dose and depth-profile utilities."""

from __future__ import annotations

import numpy as np


def normalize_to_bragg_peak(profile: np.ndarray, bragg_peak_start_index: int = 0) -> np.ndarray:
    """Normalize a depth-dose profile to the maximum after a BP start index."""

    profile = np.asarray(profile, dtype=float)
    if bragg_peak_start_index < 0 or bragg_peak_start_index >= profile.size:
        raise IndexError("bragg_peak_start_index is outside the profile.")
    denominator = profile[bragg_peak_start_index:].max()
    if denominator == 0:
        return np.zeros_like(profile, dtype=float)
    return profile / denominator


def depth_axis_mm(n_samples: int, resolution_mm: float) -> np.ndarray:
    """Create a depth axis in millimeters."""

    return np.arange(0, n_samples) * resolution_mm
