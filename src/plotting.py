"""Plotting utilities for the public pMBRT analysis repository."""

from __future__ import annotations

from pathlib import Path
import math
import re

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_ROOT = ROOT / "data" / "processed_data" / "PBP_dataset"

PVDR_DEPTH_STEP_MM = 1
PREFERRED_PVDR_ENERGY_MEV = 150


def output_path(filename: str) -> Path:
    """Return an output path under ``figures/generated`` and create the folder."""

    out_dir = ROOT / "figures" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename


def require_existing(path: str | Path) -> Path:
    """Return ``path`` after checking that it exists."""

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


def set_publication_style() -> None:
    """Apply the shared figure style."""

    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "font.size": 12,
            "axes.titlesize": 14,
            "axes.labelsize": 13,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 9,
            "legend.title_fontsize": 10,
            "axes.linewidth": 1.0,
            "lines.linewidth": 2.0,
            "lines.markersize": 5,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.minor.width": 0.8,
            "ytick.minor.width": 0.8,
        }
    )


def paired_color(index: int):
    """Return a color from Matplotlib's Paired palette."""

    return plt.get_cmap("Paired")(index % 12)


def style_axes(ax, *, xlabel: str, ylabel: str, title: str | None = None, grid_axis: str = "both") -> None:
    """Apply clean axis styling without changing plotted values."""

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, pad=8)
    ax.grid(True, axis=grid_axis, linestyle=":", linewidth=0.8, color="0.25", alpha=0.18)
    ax.tick_params(axis="both", which="major", direction="out", length=5)
    ax.tick_params(axis="both", which="minor", direction="out", length=3)
    ax.spines["top"].set_visible(False)


def parse_pvdr_path(path: Path) -> tuple[int, float]:
    """Return energy and ctc from a processed PVDR filename."""

    match = re.fullmatch(r"PVDR_2Darray_ctc(\d+)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected PVDR filename: {path.name}")
    ctc_mm = int(match.group(1)) / 10.0
    energy = int(match.group(2))
    return energy, ctc_mm


def parse_beam_width(path: Path) -> float:
    """Return the beam width in millimeters from a folder name such as FWHM5."""

    match = re.fullmatch(r"FWHM(\d+)", path.name)
    if not match:
        raise ValueError(f"Unexpected beam-width folder: {path.name}")
    return int(match.group(1)) / 10.0


def find_pvdr_profile_groups(*, energy: int) -> list[tuple[float, list[Path]]]:
    """Find public PVDR profile files grouped by beam-width folder."""

    groups: list[tuple[float, list[Path]]] = []
    for bw_dir in sorted(PROCESSED_DATA_ROOT.glob("FWHM*"), key=parse_beam_width):
        energy_dir = bw_dir / f"{energy}MeV"
        paths = sorted(energy_dir.glob(f"PVDR_2Darray_ctc*_{energy}MeV.txt"), key=parse_pvdr_path)
        if paths:
            groups.append((parse_beam_width(bw_dir), paths))
    return groups


def _plot_pvdr_group(ax, paths: list[Path]) -> tuple[int, float, list[Line2D]]:
    """Plot one beam-width group and return axis bounds plus legend handles."""

    max_depth = 0
    finite_positive_max = 1.0
    ctc_handles = []
    for index, path in enumerate(paths):
        _, ctc_mm = parse_pvdr_path(path)
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
        ctc_handles.append(Line2D([0], [0], color=color, linewidth=2.4, label=label))
    return max_depth, finite_positive_max, ctc_handles


def plot_pvdr_vs_depth(*, energy: int = PREFERRED_PVDR_ENERGY_MEV, output: Path | None = None) -> Path:
    """Plot PVDR versus depth for all public beam-width folders."""

    set_publication_style()
    groups = find_pvdr_profile_groups(energy=energy)
    if not groups:
        raise FileNotFoundError("No PVDR_2Darray_ctc*_*.txt files found under data/processed_data")

    n_groups = len(groups)
    if n_groups == 1:
        fig, axes = plt.subplots(figsize=(8.8, 5.4))
        axes = [axes]
    else:
        fig, axes_array = plt.subplots(n_groups, 1, figsize=(8.8, 3.6 * n_groups), sharex=True)
        axes = list(np.atleast_1d(axes_array))

    shared_handles: list[Line2D] = []
    global_max_depth = 0
    global_positive_max = 1.0
    for ax, (bw_mm, paths) in zip(axes, groups):
        max_depth, finite_positive_max, ctc_handles = _plot_pvdr_group(ax, paths)
        global_max_depth = max(global_max_depth, max_depth)
        global_positive_max = max(global_positive_max, finite_positive_max)
        shared_handles = ctc_handles
        ax.axhline(1.05, color="#D95F02", linestyle=":", linewidth=1.6)
        ax.axhline(1.10, color="0.35", linestyle=":", linewidth=1.1)
        style_axes(
            ax,
            xlabel="Depth z [mm]" if ax is axes[-1] else "",
            ylabel="PVDR",
            title=f"bw = {bw_mm:g} mm",
            grid_axis="y",
        )
        ax.set_yscale("log")

    lower = 0.2
    upper = 10 ** math.ceil(math.log10(global_positive_max))
    for ax in axes:
        ax.set_ylim(lower, upper)
        ax.set_xlim(left=0, right=global_max_depth)

    fig.suptitle(f"PVDR versus depth at {energy} MeV", y=0.995)
    if shared_handles:
        fig.legend(
            handles=shared_handles,
            title="Center-to-center distance",
            loc="upper right",
            bbox_to_anchor=(0.98, 0.94),
            frameon=False,
        )
    fig.tight_layout(rect=(0, 0, 0.86, 0.96))
    output = output or output_path("fig_pvdr_depth_profiles.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output
