"""Common plotting and processed-text helpers for the public pMBRT repository."""

from __future__ import annotations

from pathlib import Path
import json
import math
import re
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_ROOT = ROOT / "data" / "processed_data" / "PBP_dataset" / "FWHM5"

FWHM_DEPTH_STEP_MM = 3
PVDR_DEPTH_STEP_MM = 1
PREFERRED_PVDR_ENERGY_MEV = 150

ENERGY_COLOR_INDEX = {
    50: 3,
    75: 1,
    100: 10,
    125: 5,
    150: 7,
    175: 9,
    200: 8,
    230: 0,
}


def output_path(filename: str) -> Path:
    """Return an output path under ``figures/generated`` and create the folder."""

    out_dir = ROOT / "figures" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename


def require_existing(path: str | Path) -> Path:
    """Return ``path`` as a Path after checking that it exists."""

    data_path = Path(path)
    if not data_path.exists():
        try:
            display_path = data_path.relative_to(ROOT)
        except ValueError:
            display_path = data_path
        raise FileNotFoundError(display_path)
    return data_path


def read_numeric_series(path: str | Path) -> list[float]:
    """Read a one-value-per-line processed text profile."""

    data_path = require_existing(path)
    values: list[float] = []
    with data_path.open(encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                values.append(float(stripped))
    if not values:
        raise ValueError(f"{data_path} does not contain numeric values")
    return values


def read_json_dictionary(path: str | Path) -> dict:
    """Read a JSON-style legacy summary dictionary stored as .txt."""

    data_path = require_existing(path)
    with data_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def iter_metric_dictionary(path: str | Path, *, setup: str, dimension: str):
    """Yield flattened rows from a nested legacy metrics dictionary."""

    data = read_json_dictionary(path)
    for bw_label, by_energy in data.items():
        bw_mm = float(bw_label) / 10.0
        for energy_label, by_ctc in by_energy.items():
            energy = int(energy_label)
            for ctc_label, metrics in by_ctc.items():
                yield {
                    "setup": setup,
                    "homogeneity_dimension": dimension,
                    "energy_MeV": energy,
                    "bw_mm": bw_mm,
                    "ctc_mm": float(ctc_label),
                    "metrics": metrics,
                }


def set_publication_style() -> None:
    """Apply the shared plotting style used by the reproduction scripts."""

    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "font.size": 12,
            "axes.titlesize": 15,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 10,
            "legend.title_fontsize": 11,
            "axes.linewidth": 1.0,
            "lines.linewidth": 2.2,
            "lines.markersize": 5,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.minor.width": 0.8,
            "ytick.minor.width": 0.8,
        }
    )


def set_size(width_pt: float = 455, fraction: float = 1.0) -> tuple[float, float]:
    """Return figure dimensions in inches using the legacy golden-ratio sizing."""

    inches_per_pt = 1 / 72.27
    golden_ratio = (5**0.5 - 1) / 2
    fig_width = width_pt * fraction * inches_per_pt
    return fig_width, fig_width * golden_ratio


def paired_color(index: int):
    """Return a color from Matplotlib's Paired palette."""

    return plt.get_cmap("Paired")(index % 12)


def energy_color(energy: int):
    """Return the legacy-style color assigned to a beam energy."""

    return paired_color(ENERGY_COLOR_INDEX.get(energy, energy // 25))


def style_axes(ax, *, xlabel: str, ylabel: str, title: str | None = None, grid_axis: str = "both") -> None:
    """Apply clean axis styling without changing plotted values."""

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, pad=10)
    ax.grid(True, axis=grid_axis, linestyle=":", linewidth=0.8, color="0.25", alpha=0.18)
    ax.tick_params(axis="both", which="major", direction="out", length=5)
    ax.tick_params(axis="both", which="minor", direction="out", length=3)
    ax.spines["top"].set_visible(False)


def finalize_axes(ax, *, xlabel: str, ylabel: str, title: str | None = None) -> None:
    """Backward-compatible wrapper for older scripts."""

    style_axes(ax, xlabel=xlabel, ylabel=ylabel, title=title)
    handles, _ = ax.get_legend_handles_labels()
    if handles:
        ax.legend(frameon=False)


def _normalise(values: Iterable[float]) -> np.ndarray:
    array = np.asarray(list(values), dtype=float)
    finite = array[np.isfinite(array)]
    if finite.size == 0 or np.nanmax(np.abs(finite)) == 0:
        return array
    return array / np.nanmax(array)


def _parse_energy(path: Path, pattern: str) -> int:
    match = re.fullmatch(pattern, path.name)
    if not match:
        raise ValueError(f"Unexpected filename: {path.name}")
    return int(match.group(1))


def _parse_pvdr_path(path: Path) -> tuple[int, float]:
    match = re.fullmatch(r"PVDR_2Darray_ctc(\d+)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected PVDR filename: {path.name}")
    ctc_mm = int(match.group(1)) / 10.0
    energy = int(match.group(2))
    return energy, ctc_mm


def plot_fwhm_vs_depth(*, output: Path | None = None) -> Path:
    """Plot single-beam FWHM versus depth with normalized dose context."""

    set_publication_style()
    paths = sorted(
        PROCESSED_DATA_ROOT.glob("*MeV/FWHM_singlebeam_*MeV.txt"),
        key=lambda path: _parse_energy(path, r"FWHM_singlebeam_(\d+)MeV\.txt"),
    )
    if not paths:
        raise FileNotFoundError("No FWHM_singlebeam_*MeV.txt files found under data/processed_data")

    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    dose_ax = ax.twinx()

    for path in paths:
        energy = _parse_energy(path, r"FWHM_singlebeam_(\d+)MeV\.txt")
        color = energy_color(energy)
        fwhm = np.asarray(read_numeric_series(path), dtype=float)
        depths_mm = np.arange(fwhm.size) * FWHM_DEPTH_STEP_MM
        ax.plot(depths_mm, fwhm, color=color, label=f"{energy} MeV")

        dose_path = path.parent / f"zpeak_singlebeam_{energy}MeV.txt"
        if dose_path.exists():
            dose = _normalise(read_numeric_series(dose_path))
            dose_depths_mm = np.arange(dose.size)
            dose_ax.plot(dose_depths_mm, dose, color=color, linestyle="--", alpha=0.22, linewidth=2.0)

    style_axes(
        ax,
        xlabel="Depth z [mm]",
        ylabel=r"$FWHM_{fit}$ [mm]",
        title="Single-beam FWHM and normalized depth-dose profiles",
    )
    dose_ax.set_ylabel("Normalized dose [a.u.]", color="0.35")
    dose_ax.set_ylim(0, 1.08)
    dose_ax.tick_params(axis="y", colors="0.35", direction="out", length=5)
    dose_ax.spines["top"].set_visible(False)
    dose_ax.spines["right"].set_color("0.45")

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.minorticks_on()
    ax.legend(title="Energy", loc="upper left", frameon=False, ncol=2, columnspacing=1.2, handlelength=2.2)

    fig.tight_layout()
    output = output or output_path("fig_fwhm_vs_energy.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output


def plot_pvdr_vs_depth(*, energy: int = PREFERRED_PVDR_ENERGY_MEV, output: Path | None = None) -> Path:
    """Plot PVDR versus depth using log scaling and a near-unity inset."""

    set_publication_style()
    energy_dir = PROCESSED_DATA_ROOT / f"{energy}MeV"
    paths = sorted(energy_dir.glob(f"PVDR_2Darray_ctc*_{energy}MeV.txt"), key=_parse_pvdr_path)

    if not paths:
        all_paths = sorted(PROCESSED_DATA_ROOT.glob("*MeV/PVDR_2Darray_ctc*_*.txt"), key=_parse_pvdr_path)
        if not all_paths:
            raise FileNotFoundError("No PVDR_2Darray_ctc*_*.txt files found under data/processed_data")
        energy = _parse_pvdr_path(all_paths[0])[0]
        paths = [path for path in all_paths if _parse_pvdr_path(path)[0] == energy]

    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    inset = ax.inset_axes([0.53, 0.18, 0.40, 0.35])

    max_depth = 0
    finite_positive_max = 1.0
    ctc_handles = []
    for index, path in enumerate(paths):
        _, ctc_mm = _parse_pvdr_path(path)
        color = paired_color(2 * index + 1)
        values = np.asarray(read_numeric_series(path), dtype=float)
        depths_mm = np.arange(values.size) * PVDR_DEPTH_STEP_MM
        max_depth = max(max_depth, int(depths_mm[-1]))
        positive = np.where(values > 0, values, np.nan)
        finite_positive = positive[np.isfinite(positive)]
        if finite_positive.size:
            finite_positive_max = max(finite_positive_max, float(np.nanmax(finite_positive)))

        label = f"ctc = {ctc_mm:g} mm"
        ax.plot(depths_mm, positive, color=color, label=label)
        inset.plot(depths_mm, values, color=color, linewidth=1.8)
        ctc_handles.append(Line2D([0], [0], color=color, linewidth=2.4, label=label))

    ax.set_yscale("log")
    lower = 0.2
    upper = 10 ** math.ceil(math.log10(finite_positive_max))
    ax.set_ylim(lower, upper)
    ax.set_xlim(left=0, right=max_depth)
    ax.axhline(1.05, color="#D95F02", linestyle=":", linewidth=1.8)
    ax.axhline(1.10, color="0.35", linestyle=":", linewidth=1.2)
    style_axes(
        ax,
        xlabel="Depth z [mm]",
        ylabel="PVDR",
        title=f"PVDR versus depth at {energy} MeV",
        grid_axis="y",
    )
    ax.legend(handles=ctc_handles, title="Center-to-center distance", loc="upper right", frameon=False)

    inset.axhline(1.05, color="#D95F02", linestyle=":", linewidth=1.4)
    inset.axhline(1.10, color="0.35", linestyle=":", linewidth=1.0)
    inset.set_xlim(0, max_depth)
    inset.set_ylim(0.2, 1.6)
    inset.set_title("near unity", fontsize=10, pad=3)
    inset.tick_params(axis="both", which="major", labelsize=9, direction="out", length=3)
    inset.grid(True, axis="y", linestyle=":", linewidth=0.7, color="0.25", alpha=0.18)
    for spine in inset.spines.values():
        spine.set_color("0.55")
        spine.set_linewidth(0.8)

    fig.tight_layout()
    output = output or output_path("fig_pvdr_vs_depth_or_ctc.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output


def _homogeneity_rows() -> list[dict[str, object]]:
    sources = [
        ("PBP 1D array", "x", "dose_min_max_1Darray_dictionary.txt"),
        ("PBP 2D array", "xy", "dose_min_max_2Darray_finalversion.txt"),
    ]
    rows: list[dict[str, object]] = []
    for setup, dimension, filename in sources:
        for row in iter_metric_dictionary(PROCESSED_DATA_ROOT / filename, setup=setup, dimension=dimension):
            homogeneity_code = row["metrics"].get("homogeneity_at_BP", 0)
            rows.append({**row, "homogeneous": float(homogeneity_code) > 0})
    return rows


def plot_homogeneity_map(*, output: Path | None = None) -> Path:
    """Plot target homogeneity as compact 1D/2D status maps."""

    set_publication_style()
    rows = _homogeneity_rows()
    if not rows:
        raise ValueError("No homogeneity rows found in processed text dictionaries")

    energies = sorted({int(row["energy_MeV"]) for row in rows})
    ctc_values = sorted({float(row["ctc_mm"]) for row in rows})
    cmap = ListedColormap(["#8A8A8A", "#1B9E77"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5], cmap.N)

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.8), sharex=True, sharey=True)
    for ax, setup in zip(axes, ["PBP 1D array", "PBP 2D array"]):
        matrix = np.full((len(ctc_values), len(energies)), np.nan)
        for row in rows:
            if row["setup"] != setup:
                continue
            y = ctc_values.index(float(row["ctc_mm"]))
            x = energies.index(int(row["energy_MeV"]))
            matrix[y, x] = 1 if row["homogeneous"] else 0

        ax.imshow(matrix, origin="lower", aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")
        ax.set_title(setup)
        ax.set_xticks(range(len(energies)), energies, rotation=45, ha="right")
        major_ctc = [value for value in ctc_values if abs(value - round(value)) < 1e-9]
        ax.set_yticks([ctc_values.index(value) for value in major_ctc], [f"{value:g}" for value in major_ctc])
        ax.set_xlabel("Energy [MeV]")
        ax.tick_params(axis="both", direction="out", length=0)
        ax.set_xticks(np.arange(-0.5, len(energies), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(ctc_values), 1), minor=True)
        ax.grid(which="minor", color="white", linestyle="-", linewidth=1.0)
        for spine in ax.spines.values():
            spine.set_visible(False)

    axes[0].set_ylabel("Center-to-center distance [mm]")
    axes[1].tick_params(axis="y", which="both", left=False, labelleft=False)
    legend_handles = [
        Patch(facecolor="#1B9E77", edgecolor="none", label="homogeneous at target"),
        Patch(facecolor="#8A8A8A", edgecolor="none", label="not homogeneous"),
    ]
    fig.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False)
    fig.suptitle("Target homogeneity", y=1.08, fontsize=15)
    fig.tight_layout()

    output = output or output_path("fig_homogeneity.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output
