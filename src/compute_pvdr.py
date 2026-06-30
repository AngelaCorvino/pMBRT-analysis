"""PVDR calculations."""

from __future__ import annotations

import numpy as np


def compute_pvdr(peak_dose: np.ndarray, valley_dose: np.ndarray) -> np.ndarray:
    """Compute peak-to-valley dose ratio with legacy zero-division handling."""

    peak = np.asarray(peak_dose, dtype=float)
    valley = np.asarray(valley_dose, dtype=float)
    return np.divide(peak, valley, out=np.zeros_like(peak, dtype=float), where=valley != 0)


def value_at_depth(values: np.ndarray, depth_mm: float, resolution_mm: float) -> float:
    """Return the sampled value nearest a physical depth."""

    index = int(round(depth_mm / resolution_mm))
    values = np.asarray(values)
    if index < 0 or index >= values.size:
        raise IndexError("Requested depth is outside the sampled profile.")
    return float(values[index])
