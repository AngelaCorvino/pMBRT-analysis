"""Plotting utilities for the public pMBRT analysis repository."""

from __future__ import annotations

from pathlib import Path
import math
import re

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_ROOT = ROOT / "data" / "processed_data" / "PBP_dataset" / "FWHM5"

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


def paired_color(index: int):
    """Return a color from Matplotlib's Paired palette."""

    return plt.get_cmap("Paired")(index % 12)


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


def parse_pvdr_path(path: Path) -> tuple[int, float]:
    """Return energy and ctc from a processed PVDR filename."""

    match = re.fullmatch(r"PVDR_2Darray_ctc(\d+)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected PVDR filename: {path.name}")
    ctc_mm = int(match.group(1)) / 10.0
    energy = int(match.group(2))
    return energy, ctc_mm


def plot_pvdr_vs_depth(*, energy: int = PREFERRED_PVDR_ENERGY_MEV, output: Path | None = None) -> Path:
    """Plot PVDR versus depth for the selected processed profiles."""

    set_publication_style()
    energy_dir = PROCESSED_DATA_ROOT / f"{energy}MeV"
    paths = sorted(energy_dir.glob(f"PVDR_2Darray_ctc*_{energy}MeV.txt"), key=parse_pvdr_path)

    if not paths:
        all_paths = sorted(PROCESSED_DATA_ROOT.glob("*MeV/PVDR_2Darray_ctc*_*.txt"), key=parse_pvdr_path)
        if not all_paths:
            raise FileNotFoundError("No PVDR_2Darray_ctc*_*.txt files found under data/processed_data")
        energy = parse_pvdr_path(all_paths[0])[0]
        paths = [path for path in all_paths if parse_pvdr_path(path)[0] == energy]

    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    inset = ax.inset_axes([0.53, 0.18, 0.40, 0.35])

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
