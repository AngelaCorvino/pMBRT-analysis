"""FWHM fitting utilities extracted from the legacy pMBRT scripts."""

from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, savgol_filter


def gaussian_with_offset(x: np.ndarray, height: float, mean: float, sigma: float, offset: float) -> np.ndarray:
    """Legacy Gaussian-with-offset model."""

    return height * np.exp(-((x - mean) ** 2) / (2 * sigma * sigma)) / (
        sigma * np.sqrt(2 * np.pi)
    ) + offset


def fit_multibeam_fwhm(
    profile_1d: np.ndarray,
    resolution_mm: float,
    ctc_mm: float,
    input_fwhm_tenth_mm: float,
    *,
    window_smoothing_pixel: int = 10,
    plotprofile: bool = False,
) -> float:
    """Fit the central profile of a 1D or 2D minibeam array.

    This follows the active ``fit_FWHM.py`` calculation: Savitzky-Golay
    smoothing, peak counting, Gaussian fitting, and ``FWHM = abs(sigma)*2.355``.
    Plotting is intentionally not implemented here; public reproduction scripts
    plot already processed text values.
    """

    if plotprofile:
        raise NotImplementedError("Diagnostic profile plotting is not part of the cleaned helper.")

    profile_1d = np.asarray(profile_1d, dtype=float)
    n_points = profile_1d.size
    dx = int(ctc_mm / (2 * resolution_mm))
    smoothed = savgol_filter(profile_1d, window_smoothing_pixel, 3)
    peaks, _ = find_peaks(smoothed, height=0.8 * profile_1d)

    x_fit = None
    y_fit = None
    guess: list[float] = []

    if len(peaks) <= 2:
        guess = [float(smoothed.max()), int(len(smoothed) * resolution_mm / 2), 0.8 * input_fwhm_tenth_mm, 0]
        x_fit = np.arange(0, n_points) * resolution_mm
        y_fit = smoothed
    else:
        a0, a1, a2 = peaks[len(peaks) // 2 - 1 : len(peaks) // 2 + 2]
        peak_distance = max(abs(a0 - a1), abs(a0 - a2))
        if peak_distance < dx:
            guess = [float(smoothed.max()), int(len(smoothed) * resolution_mm / 2), 0.8 * input_fwhm_tenth_mm, 0]
            x_fit = np.arange(0, n_points) * resolution_mm
            y_fit = smoothed
        else:
            x_profile = np.arange(0, n_points) * resolution_mm
            center_index = n_points // 2
            peak_index = np.argmax(profile_1d[center_index - dx : center_index + dx]) + (center_index - dx)
            guess = [float(profile_1d[peak_index]), float(x_profile[peak_index]), 1, 0]
            x_fit = x_profile[center_index - dx : center_index + dx]
            y_fit = smoothed[center_index - dx : center_index + dx]

    if x_fit is None or y_fit is None or len(x_fit) == 0:
        return 0.0

    try:
        popt, _ = curve_fit(gaussian_with_offset, x_fit, y_fit, p0=guess)
    except RuntimeError:
        return 0.0

    return float(abs(popt[2]) * 2.355)


def fit_singlebeam_fwhm(
    profile_1d: np.ndarray,
    resolution_mm: float,
    fwhm_sim_tenth_mm: float,
    *,
    window_smoothing_pixel: int = 10,
    z_coordinate: float | None = None,
) -> float:
    """Fit a single-beam lateral profile using the legacy retry windows."""

    profile_1d = np.asarray(profile_1d, dtype=float)
    n_points = profile_1d.size
    smoothed = savgol_filter(profile_1d, window_smoothing_pixel, 3)
    x_profile = np.arange(0, n_points) * resolution_mm

    def fit_window(dx_factor: float) -> float:
        scaling_factor = 0.1
        if z_coordinate is not None:
            dx = int(dx_factor * fwhm_sim_tenth_mm / resolution_mm + scaling_factor * z_coordinate)
        else:
            dx = int(dx_factor * fwhm_sim_tenth_mm / resolution_mm)
        dx = min(dx, n_points // 2)

        x_fit = x_profile[n_points // 2 - dx : n_points // 2 + dx]
        y_fit = smoothed[n_points // 2 - dx : n_points // 2 + dx]
        guess = [smoothed[n_points // 2], x_profile[n_points // 2], 1, 0]
        popt, _ = curve_fit(gaussian_with_offset, x_fit, y_fit, p0=guess)
        return float(abs(popt[2]) * 2.355)

    fwhm = 0.0
    for dx_factor in [0.5, 1, 2, 3]:
        try:
            fwhm = fit_window(dx_factor)
            if fwhm < 2 * fwhm_sim_tenth_mm:
                break
        except RuntimeError:
            fwhm = 0.0

    return fwhm
