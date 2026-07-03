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

DEPTH_STEP_MM = 1
PBP_FIGURE_ENERGIES = (50, 125, 175, 230)
PBP_CTC_CASES = (("3 x bw", 3), ("5 x bw", 5))
FIGURE1_PBP_BEAM_WIDTHS = ("5", "10", "12", "15", "20")
FIGURE2_PBP_BEAM_WIDTHS = ("5", "7", "10", "12", "15", "20")
PBP_BRAGG_PEAK_INDEX = {50: 21, 125: 112, 175: 203, 230: 325}
FIGURE_S5_ENERGY_COLORS = {
    50: "#9DD4E8",
    125: "#00A51A",
    175: "#FF1F2D",
    230: "#FF8C00",
}
FIGURE_S5_PVDR_CASES = [
    {
        "panel": "a",
        "bw_label": "5",
        "bw_mm": 0.5,
        "xmax": 120,
        "profiles": [(50, (1.5, 2.0))],
    },
    {
        "panel": "b",
        "bw_label": "12",
        "bw_mm": 1.2,
        "xmax": 210,
        "profiles": [(125, (4.8, 6.0)), (175, (4.8, 6.0))],
    },
    {
        "panel": "c",
        "bw_label": "7",
        "bw_mm": 0.7,
        "xmax": 120,
        "profiles": [(50, (2.1, 2.8)), (125, (2.8, 3.5))],
    },
    {
        "panel": "d",
        "bw_label": "15",
        "bw_mm": 1.5,
        "xmax": 330,
        "profiles": [(175, (6.0, 7.5)), (230, (6.0, 7.5))],
    },
    {
        "panel": "e",
        "bw_label": "10",
        "bw_mm": 1.0,
        "xmax": 210,
        "profiles": [(125, (4.0, 5.0)), (175, (4.0, 5.0))],
    },
    {
        "panel": "f",
        "bw_label": "20",
        "bw_mm": 2.0,
        "xmax": 330,
        "profiles": [(230, (8.0, 10.0))],
    },
]


def ctc_label(ctc_mm: float) -> str:
    """Return the ctc filename label in tenths of a millimeter."""

    return str(int(round(ctc_mm * 10)))


def output_path(filename: str) -> Path:
    """Return an output path under ``figures`` and create the folder."""

    out_dir = ROOT / "figures"
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


def parse_beam_width(path: Path) -> float:
    """Return the beam width in millimeters from a folder name such as FWHM5."""

    match = re.fullmatch(r"FWHM(\d+)", path.name)
    if not match:
        raise ValueError(f"Unexpected beam-width folder: {path.name}")
    return int(match.group(1)) / 10.0


def parse_zpeak_1d_path(path: Path) -> tuple[float, int, float]:
    """Return beam width, energy, and ctc from a 1D-array peak-profile path."""

    match = re.fullmatch(r"zpeak_1Darray_ctc(\d+)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected peak-profile filename: {path.name}")

    bw_dir = next((parent for parent in path.parents if re.fullmatch(r"FWHM\d+", parent.name)), None)
    if bw_dir is None:
        raise ValueError(f"No FWHM folder found for {path}")

    ctc_mm = int(match.group(1)) / 10.0
    energy = int(match.group(2))
    return parse_beam_width(bw_dir), energy, ctc_mm


def _pbp_ctc_mm(bw_label: str, multiplier: int) -> float:
    """Return the pMBRT PDD ctc value for a beam width label and multiplier."""

    return int(round(float(bw_label) * multiplier)) / 10.0


def _pbp_profile_path(profile_name: str, bw_label: str, energy: int, ctc_mm: float) -> Path:
    """Return the processed PBP profile path for one pMBRT PDD case."""

    ctc = ctc_label(ctc_mm)
    filename = f"{profile_name}_1Darray_ctc{ctc}_{energy}MeV.txt"
    return PROCESSED_DATA_ROOT / f"FWHM{bw_label}" / f"{energy}MeV" / filename


def _pbp_pvdr_profile_path(bw_label: str, energy: int, ctc_mm: float) -> Path:
    """Return the processed PBP PVDR profile path for one pMBRT case."""

    ctc = ctc_label(ctc_mm)
    filename = f"PVDR_1Darray_ctc{ctc}_{energy}MeV.txt"
    return PROCESSED_DATA_ROOT / f"FWHM{bw_label}" / f"{energy}MeV" / filename


def _dedupe_profiles_by_ctc(profiles: list[tuple[float, Path]]) -> list[tuple[float, Path]]:
    """Return one profile per ctc, preferring the shortest matching path."""

    deduped: dict[float, Path] = {}
    for ctc_mm, path in profiles:
        current = deduped.get(ctc_mm)
        if current is None or len(path.parts) < len(current.parts):
            deduped[ctc_mm] = path
    return sorted(deduped.items(), key=lambda item: item[0])


def find_figure1_peak_profiles() -> list[tuple[float, list[tuple[int, str, float, Path]]]]:
    """Return Figure 1 peak profiles for the pMBRT PDD case list."""

    figure_groups: list[tuple[float, list[tuple[int, str, float, Path]]]] = []
    for bw_label in FIGURE1_PBP_BEAM_WIDTHS:
        bw_mm = int(bw_label) / 10.0
        selected: list[tuple[int, str, float, Path]] = []
        for energy in PBP_FIGURE_ENERGIES:
            for ctc_role, multiplier in PBP_CTC_CASES:
                ctc_mm = _pbp_ctc_mm(bw_label, multiplier)
                path = _pbp_profile_path("zpeak", bw_label, energy, ctc_mm)
                require_existing(path)
                selected.append((energy, ctc_role, ctc_mm, path))
        if selected:
            figure_groups.append((bw_mm, selected))
    return figure_groups


def _panel_grid(n_panels: int) -> tuple[int, int]:
    """Return a compact row-column grid for a requested panel count."""

    if n_panels <= 2:
        return 1, n_panels
    return math.ceil(n_panels / 2), 2


def plot_figure1_peak_depth_profiles(*, output: Path | None = None) -> Path:
    """Plot Figure 1 peak depth-dose profiles for the 1D MB geometry."""

    set_publication_style()
    groups = find_figure1_peak_profiles()
    if not groups:
        raise FileNotFoundError("No zpeak_1Darray_ctc*_*.txt files found under data/processed_data")

    energies = sorted({energy for _, profiles in groups for energy, _, _, _ in profiles})
    colors = {energy: paired_color(index) for index, energy in enumerate(energies)}

    n_rows, n_cols = _panel_grid(len(groups))
    fig, axes_array = plt.subplots(
        n_rows,
        n_cols,
        figsize=(5.1 * n_cols, 3.65 * n_rows),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    axes = list(axes_array.ravel())

    max_depth = 0
    for ax, (bw_mm, profiles) in zip(axes, groups):
        for energy, ctc_role, ctc_mm, path in profiles:
            values = np.asarray(read_numeric_series(path), dtype=float)
            profile_max = float(np.nanmax(values))
            if profile_max <= 0:
                continue
            normalized = values / profile_max
            depths_mm = np.arange(values.size) * DEPTH_STEP_MM
            max_depth = max(max_depth, int(depths_mm[-1]))
            linestyle = "-" if ctc_role == "3 x bw" else "--"
            ax.plot(depths_mm, normalized, color=colors[energy], linestyle=linestyle)

        style_axes(
            ax,
            xlabel="Depth z [mm]",
            ylabel="Normalized peak dose",
            title=f"bw = {bw_mm:g} mm",
            grid_axis="y",
        )
        ax.set_ylim(0, 1.05)

    for ax in axes[len(groups):]:
        ax.set_visible(False)
    for ax in axes[: len(groups)]:
        ax.set_xlim(left=0, right=max_depth)

    energy_handles = [Line2D([0], [0], color=colors[energy], linewidth=2.0, label=f"{energy} MeV") for energy in energies]
    style_handles = [
        Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="-", label="ctc = 3 x bw"),
        Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="--", label="ctc = 5 x bw"),
    ]
    fig.legend(handles=energy_handles, title="Energy", loc="upper center", ncol=min(len(energy_handles), 4), frameon=False)
    fig.legend(handles=style_handles, loc="lower center", ncol=2, frameon=False)
    fig.suptitle("Peak depth-dose profiles for the MB configuration", y=0.995)
    fig.tight_layout(rect=(0, 0.08, 1, 0.90))

    output = output or output_path("fig1_peak_depth_profiles.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output


def parse_zvalley_1d_path(path: Path) -> tuple[float, int, float]:
    """Return beam width, energy, and ctc from a 1D-array valley-profile path."""

    match = re.fullmatch(r"zvalley_1Darray_ctc(\d+)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected valley-profile filename: {path.name}")

    bw_dir = next((parent for parent in path.parents if re.fullmatch(r"FWHM\d+", parent.name)), None)
    if bw_dir is None:
        raise ValueError(f"No FWHM folder found for {path}")

    ctc_mm = int(match.group(1)) / 10.0
    energy = int(match.group(2))
    return parse_beam_width(bw_dir), energy, ctc_mm


def matching_peak_profile_path(valley_path: Path) -> Path:
    """Return the peak-profile path used to normalize a Figure 2 valley profile."""

    return valley_path.with_name(valley_path.name.replace("zvalley_", "zpeak_", 1))


def find_figure2_valley_profiles() -> list[tuple[float, list[tuple[int, str, float, Path, Path]]]]:
    """Return Figure 2 valley profiles for the pMBRT PDD case list."""

    figure_groups: list[tuple[float, list[tuple[int, str, float, Path, Path]]]] = []
    for bw_label in FIGURE2_PBP_BEAM_WIDTHS:
        bw_mm = int(bw_label) / 10.0
        selected: list[tuple[int, str, float, Path, Path]] = []
        for energy in PBP_FIGURE_ENERGIES:
            for ctc_role, multiplier in PBP_CTC_CASES:
                ctc_mm = _pbp_ctc_mm(bw_label, multiplier)
                valley_path = _pbp_profile_path("zvalley", bw_label, energy, ctc_mm)
                peak_path = _pbp_profile_path("zpeak", bw_label, energy, ctc_mm)
                require_existing(valley_path)
                if not peak_path.exists():
                    try:
                        display_path = peak_path.relative_to(ROOT)
                    except ValueError:
                        display_path = peak_path
                    raise FileNotFoundError(f"Missing matching peak profile for Figure 2 normalization: {display_path}")
                selected.append((energy, ctc_role, ctc_mm, valley_path, peak_path))
        if selected:
            figure_groups.append((bw_mm, selected))
    return figure_groups


def plot_figure2_valley_depth_profiles(*, output: Path | None = None) -> Path:
    """Plot Figure 2 valley depth-dose profiles for the 1D MB geometry."""

    set_publication_style()
    groups = find_figure2_valley_profiles()
    if not groups:
        raise FileNotFoundError("No zvalley_1Darray_ctc*_*.txt files found under data/processed_data")

    energies = sorted({energy for _, profiles in groups for energy, _, _, _, _ in profiles})
    colors = {energy: paired_color(index) for index, energy in enumerate(energies)}

    n_rows, n_cols = _panel_grid(len(groups))
    fig, axes_array = plt.subplots(
        n_rows,
        n_cols,
        figsize=(5.1 * n_cols, 3.65 * n_rows),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    axes = list(axes_array.ravel())

    max_depth = 0
    for ax, (bw_mm, profiles) in zip(axes, groups):
        for energy, ctc_role, ctc_mm, valley_path, peak_path in profiles:
            valley_values = np.asarray(read_numeric_series(valley_path), dtype=float)
            peak_values = np.asarray(read_numeric_series(peak_path), dtype=float)
            peak_max = float(np.nanmax(peak_values))
            if peak_max <= 0:
                continue
            normalized = valley_values / peak_max
            depths_mm = np.arange(valley_values.size) * DEPTH_STEP_MM
            max_depth = max(max_depth, int(depths_mm[-1]))
            linestyle = "-" if ctc_role == "3 x bw" else "--"
            ax.plot(depths_mm, normalized, color=colors[energy], linestyle=linestyle)

        style_axes(
            ax,
            xlabel="Depth z [mm]",
            ylabel="Normalized valley dose",
            title=f"bw = {bw_mm:g} mm",
            grid_axis="y",
        )
        ax.set_ylim(bottom=0)

    for ax in axes[len(groups):]:
        ax.set_visible(False)
    for ax in axes[: len(groups)]:
        ax.set_xlim(left=0, right=max_depth)

    energy_handles = [Line2D([0], [0], color=colors[energy], linewidth=2.0, label=f"{energy} MeV") for energy in energies]
    style_handles = [
        Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="-", label="ctc = 3 x bw"),
        Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="--", label="ctc = 5 x bw"),
    ]
    fig.legend(handles=energy_handles, title="Energy", loc="upper center", ncol=min(len(energy_handles), 4), frameon=False)
    fig.legend(handles=style_handles, loc="lower center", ncol=2, frameon=False)
    fig.suptitle("Valley depth-dose profiles for the MB configuration", y=0.995)
    fig.tight_layout(rect=(0, 0.08, 1, 0.90))

    output = output or output_path("fig2_valley_depth_profiles.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output


def find_figure_s5_pvdr_profiles() -> list[tuple[dict[str, object], list[tuple[int, str, float, Path]]]]:
    """Return Supplementary Figure S5 PVDR profiles for the public case list."""

    figure_panels: list[tuple[dict[str, object], list[tuple[int, str, float, Path]]]] = []
    for panel in FIGURE_S5_PVDR_CASES:
        selected: list[tuple[int, str, float, Path]] = []
        for energy, ctc_values in panel["profiles"]:
            for role, ctc_mm in zip(("min", "max"), ctc_values):
                path = _pbp_pvdr_profile_path(str(panel["bw_label"]), int(energy), float(ctc_mm))
                require_existing(path)
                selected.append((int(energy), role, float(ctc_mm), path))
        figure_panels.append((panel, selected))
    return figure_panels


def plot_figure_s5_pvdr_depth_profiles(*, output: Path | None = None) -> Path:
    """Plot Supplementary Figure S5 PVDR depth profiles for the 1D MB geometry."""

    set_publication_style()
    panels = find_figure_s5_pvdr_profiles()

    fig, axes_array = plt.subplots(3, 2, figsize=(11.0, 11.8), sharey=True, squeeze=False)
    axes = list(axes_array.ravel())

    for ax, (panel, profiles) in zip(axes, panels):
        line_handles: list[Line2D] = []
        for energy, role, ctc_mm, path in profiles:
            values = np.asarray(read_numeric_series(path), dtype=float)
            stop = min(values.size, PBP_BRAGG_PEAK_INDEX[energy] + 5)
            pvdr = np.where(values[:stop] > 0, values[:stop], np.nan)
            depths_mm = np.arange(stop) * DEPTH_STEP_MM
            linestyle = "-" if role == "min" else "--"
            color = FIGURE_S5_ENERGY_COLORS[energy]
            label = f"{ctc_mm:g} mm"
            ax.plot(depths_mm, pvdr, color=color, linestyle=linestyle)
            line_handles.append(
                Line2D([0], [0], color=color, linestyle=linestyle, linewidth=2.0, label=label)
            )

        ax.set_yscale("log")
        ax.set_ylim(0.75, 2000)
        ax.set_xlim(0, int(panel["xmax"]))
        style_axes(
            ax,
            xlabel="z [mm]" if str(panel["panel"]) in {"e", "f"} else "",
            ylabel="PVDR",
            title=f"FWHM = {panel['bw_mm']:g} mm",
            grid_axis="y",
        )
        ax.text(-0.10, 1.04, str(panel["panel"]), transform=ax.transAxes, fontsize=16, fontweight="bold")
        ax.legend(handles=line_handles, title="ctc", loc="upper right", frameon=False, handlelength=2.4)

    energy_handles = [
        Line2D([0], [0], marker="s", linestyle="None", color=color, markersize=10, label=f"{energy} MeV")
        for energy, color in FIGURE_S5_ENERGY_COLORS.items()
    ]
    fig.legend(handles=energy_handles, loc="lower center", ncol=4, frameon=False)
    fig.tight_layout(rect=(0, 0.055, 1, 1))

    output = output or output_path("figS5_pvdr_depth_profiles.png")
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output
