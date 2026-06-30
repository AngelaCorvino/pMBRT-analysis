"""Profile-loading utilities for curated pMBRT analysis data.

The legacy analysis scripts read dose grids from ``.npy`` or ``.mhd`` files,
then derive peak, valley, and masked lateral profiles. This module keeps that
logic reusable without hard-coded local paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

import numpy as np


@dataclass(frozen=True)
class SpacingMM:
    """Voxel spacing in millimeters for arrays ordered as z, y, x."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class DoseGrid:
    """Dose grid and metadata.

    ``data`` is expected to be ordered as ``(z, y, x)`` after loading.
    """

    data: np.ndarray
    spacing_mm: SpacingMM
    source_path: Path


@dataclass(frozen=True)
class ProfileSet:
    """Peak, valley, and masked lateral profiles derived from a dose grid."""

    zprofile_peak: np.ndarray
    zprofile_valley: np.ndarray
    zxprofile_masky: np.ndarray
    zyprofile_maskx: np.ndarray
    peak_mask_2d: np.ndarray
    valley_mask_2d: np.ndarray


def read_header_spacing_mm(header_path: str | Path, values_are_cm: bool = True) -> SpacingMM:
    """Read legacy ``.header`` spacing columns and return millimeter spacing.

    Legacy scripts multiply ``res_x``, ``res_y``, and ``res_z`` by 10, so the
    default assumes those header values are stored in centimeters.
    """

    header_path = Path(header_path)
    with header_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        row = next(reader)

    factor = 10.0 if values_are_cm else 1.0
    return SpacingMM(
        x=float(row["res_x"]) * factor,
        y=float(row["res_y"]) * factor,
        z=float(row["res_z"]) * factor,
    )


def load_dose_grid(
    path: str | Path,
    *,
    transpose: bool = False,
    header_path: str | Path | None = None,
    default_spacing_mm: SpacingMM = SpacingMM(0.05, 0.1, 1.0),
) -> DoseGrid:
    """Load a ``.npy`` or ``.mhd`` dose grid.

    Parameters
    ----------
    path:
        Source dose-grid path.
    transpose:
        Apply the legacy ``data.transpose(2, 1, 0)`` operation after loading.
        This was used when the input array was stored as x, y, z but downstream
        profile code expected z, y, x.
    header_path:
        Optional sidecar CSV with ``res_x,res_y,res_z`` columns. If omitted for
        a ``.npy`` file, ``<path without .npy>.header`` is used when present.
    default_spacing_mm:
        Spacing used for ``.npy`` files without a readable header, matching the
        active legacy profile loader defaults.
    """

    source_path = Path(path)
    suffix = source_path.suffix.lower()

    if suffix == ".npy":
        data = np.load(source_path)
        sidecar = Path(header_path) if header_path else source_path.with_suffix(".header")
        spacing = read_header_spacing_mm(sidecar) if sidecar.exists() else default_spacing_mm
    elif suffix == ".mhd":
        try:
            import SimpleITK as sitk
        except ImportError as exc:
            raise ImportError("Reading .mhd files requires SimpleITK.") from exc

        image = sitk.ReadImage(str(source_path))
        spacing = SpacingMM(*map(float, image.GetSpacing()))
        data = sitk.GetArrayFromImage(image)
    else:
        raise ValueError(f"Unsupported dose-grid format: {source_path.suffix}")

    if transpose:
        data = data.transpose(2, 1, 0)

    return DoseGrid(data=np.asarray(data), spacing_mm=spacing, source_path=source_path)


def rectangular_mask_2d(
    height: int,
    width: int,
    delta_y_px: float,
    delta_x_px: float,
    center: tuple[int, int] | None = None,
) -> np.ndarray:
    """Create the rectangular y/x mask used by the legacy profile code."""

    if center is None:
        center = (height // 2, width // 2)

    yy, xx = np.ogrid[:height, :width]
    return (np.abs(yy - center[0]) <= delta_y_px) & (np.abs(xx - center[1]) <= delta_x_px)


def rectangular_mask_1d(length: int, delta_px: float, center: int | None = None) -> np.ndarray:
    """Create a centered 1D rectangular mask."""

    if center is None:
        center = length // 2

    axis = np.ogrid[:length]
    return np.abs(axis - center) <= delta_px


def extract_profiles(
    grid: DoseGrid,
    *,
    deltax_px: float,
    deltay_px: float,
    ctc_mm: float,
    planar_array: bool,
) -> ProfileSet:
    """Extract peak/valley depth profiles and masked lateral profiles.

    ``planar_array=True`` corresponds to the legacy PA=True branch used for
    1D/planar minibeam arrays.
    """

    data = np.asarray(grid.data)
    if data.ndim != 3:
        raise ValueError("Dose grid must be a 3D array ordered as z, y, x.")

    nz, ny, nx = data.shape
    half_ctc_px = int((ctc_mm / 2.0) / grid.spacing_mm.x)

    if planar_array:
        peak_mask = rectangular_mask_2d(ny, nx, ny / 15.0, deltax_px)
        valley_mask = rectangular_mask_2d(
            ny,
            nx,
            ny / 15.0,
            deltax_px,
            center=(ny // 2, nx // 2 + half_ctc_px),
        )
    else:
        peak_mask = rectangular_mask_2d(ny, nx, deltay_px, deltax_px)
        valley_mask = rectangular_mask_2d(
            ny,
            nx,
            deltay_px,
            deltax_px,
            center=(ny // 2 + half_ctc_px, nx // 2 + half_ctc_px),
        )

    zprofile_peak = np.zeros(nz)
    zprofile_valley = np.zeros(nz)
    for z_index in range(nz):
        plane = data[z_index, :, :]
        zprofile_peak[z_index] = np.mean(plane[peak_mask])
        zprofile_valley[z_index] = np.mean(plane[valley_mask])

    y_mask = rectangular_mask_1d(ny, deltay_px)
    x_mask = rectangular_mask_1d(nx, deltax_px)
    zxprofile_masky = np.mean(data[:, y_mask, :], axis=1)
    zyprofile_maskx = np.mean(data[:, :, x_mask], axis=2)

    return ProfileSet(
        zprofile_peak=zprofile_peak,
        zprofile_valley=zprofile_valley,
        zxprofile_masky=zxprofile_masky,
        zyprofile_maskx=zyprofile_maskx,
        peak_mask_2d=peak_mask,
        valley_mask_2d=valley_mask,
    )


def legacy_output_path(
    base_dir: str | Path,
    *,
    setup: str,
    fwhm_tenth_mm: str | int,
    energy_MeV: str | int,
    ctc_mm: float | None = None,
    single_beam: bool = False,
    planar_array: bool = True,
) -> Path:
    """Build a legacy-style path from an explicit base directory.

    This helper does not know any private machine path. The caller must provide
    ``base_dir``.
    """

    folder = Path(base_dir) / setup / f"FWHM{fwhm_tenth_mm}" / f"{energy_MeV}MeV"
    if single_beam:
        return folder / "protonsinglebeam-Dose.npy"

    if ctc_mm is None:
        raise ValueError("ctc_mm is required for multi-beam dose paths.")

    ctc_label = int(round(ctc_mm * 10))
    dose_name = "protonmultibeam-Dose.npy" if planar_array else "protonGRID-Dose.npy"
    return folder / f"ctc{ctc_label}" / dose_name
