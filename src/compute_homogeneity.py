"""Homogeneity metrics used by the legacy pMBRT analysis scripts."""

from __future__ import annotations

import numpy as np

from load_profiles import rectangular_mask_1d


def normalized_profile_is_homogeneous(
    profile: np.ndarray,
    *,
    lower: float = 0.95,
    upper: float = 1.07,
) -> bool:
    """Check whether a profile normalized by its mean falls within limits."""

    profile = np.asarray(profile, dtype=float)
    mean = np.mean(profile)
    if mean == 0:
        return False
    normalized = profile / mean
    return bool(normalized.min() > lower and normalized.max() < upper)


def relative_stddev(profile: np.ndarray) -> float:
    """Return standard deviation divided by mean for a 1D profile."""

    profile = np.asarray(profile, dtype=float)
    mean = np.mean(profile)
    if mean == 0:
        return float("nan")
    return float(np.std(profile) / mean)


def homogeneity_profile_1d(
    z_lateral_profile: np.ndarray,
    *,
    resolution_mm: float,
    ctc_mm: float,
    fwhm_tenth_mm: float,
    bragg_peak_index: int,
    lower: float = 0.95,
    upper: float = 1.07,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute per-depth homogeneity flags and relative standard deviations.

    The depth-dependent mask width follows the active legacy scripts.
    """

    profiles = np.asarray(z_lateral_profile, dtype=float)
    if profiles.ndim != 2:
        raise ValueError("z_lateral_profile must be a 2D array ordered as z, lateral coordinate.")

    nz, n_lateral = profiles.shape
    fwhm_mm = float(fwhm_tenth_mm) / 10.0
    flags = np.zeros(nz, dtype=bool)
    rel_std = np.full(nz, np.nan)

    for z_index in range(nz):
        exp_term = 1 / (1 + np.exp(-(z_index - bragg_peak_index)))
        mask_width = int((ctc_mm / resolution_mm) * (1 - (exp_term * (2 * fwhm_mm / ctc_mm**2))))
        mask = rectangular_mask_1d(n_lateral, mask_width)
        masked_profile = profiles[z_index, mask]
        flags[z_index] = normalized_profile_is_homogeneous(masked_profile, lower=lower, upper=upper)
        rel_std[z_index] = relative_stddev(masked_profile)

    return flags, rel_std


def homogeneous_at_bragg_peak(flags: np.ndarray, bragg_peak_index: int) -> bool:
    """Legacy mono-beam pass/fail check at and near the Bragg peak."""

    flags = np.asarray(flags, dtype=bool)
    candidate_indices = [bragg_peak_index, bragg_peak_index + 1, bragg_peak_index - 1, bragg_peak_index + 2]
    return any(0 <= idx < flags.size and flags[idx] for idx in candidate_indices)


def homogeneous_over_sobp(flags: np.ndarray, bragg_peak_index: int, resolution_mm: float) -> bool:
    """Legacy SOBP-style pass/fail check over the 25%-to-BP interval."""

    flags = np.asarray(flags, dtype=bool)
    twenty_five_percent_index = int((0.25 * bragg_peak_index) / resolution_mm)
    start = max(0, bragg_peak_index - twenty_five_percent_index)
    stop = min(flags.size, bragg_peak_index)
    if start >= stop:
        return False
    return bool(np.all(flags[start:stop]))
