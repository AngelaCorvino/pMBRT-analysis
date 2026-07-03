"""Plotting utilities for the public pMBRT analysis repository."""

from __future__ import annotations

from pathlib import Path
import math
import re
import sys

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_ROOT = ROOT / "data" / "processed_data" / "PBP_dataset"

DEPTH_STEP_MM = 1
PBP_ENERGIES = (50, 125, 175, 230)
PBP_CTC_CASES = (("3 x bw", 3), ("5 x bw", 5))
PBP_PDD_BEAM_WIDTHS = ("5", "7", "10", "12", "15", "20")
PBP_PVDR_BEAM_WIDTHS = ("5", "7", "10", "12", "15", "20")
PBP_BRAGG_PEAK_INDEX = {50: 21, 125: 112, 175: 203, 230: 325}
PBP_ENERGY_COLORS = {
    50: "#9DD4E8",
    125: "#00A51A",
    175: "#FF1F2D",
    230: "#FF8C00",
}
PBP_PVDR_CASES = [
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


def report_missing_data(missing_paths: list[Path], *, analysis_name: str) -> None:
    """Print a concise message for processed data that are not public."""

    if not missing_paths:
        return

    print(
        f"{analysis_name}: {len(missing_paths)} processed data file(s) are not included in this public repository. "
        "Please contact the authors if you need those data.",
        file=sys.stderr,
    )


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
    """Apply the shared plotting style."""

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


def beam_width_to_label(beam_width: str | float | int) -> str:
    """Return a FWHM folder label from a beam width in millimeters or tenths."""

    raw_value = str(beam_width).strip().lower()
    for token in ("fwhm", "bw", "mm"):
        raw_value = raw_value.replace(token, "")
    raw_value = raw_value.strip()
    if not raw_value:
        raise ValueError("Beam width is empty")

    try:
        numeric_value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"Could not parse beam width: {beam_width}") from exc

    if numeric_value <= 0:
        raise ValueError(f"Beam width must be positive: {beam_width}")
    if numeric_value > 3:
        return str(int(round(numeric_value)))
    return str(int(round(numeric_value * 10)))


def beam_width_mm_from_label(bw_label: str) -> float:
    """Return the beam width in millimeters from a FWHM folder label."""

    return int(bw_label) / 10.0


def format_beam_widths(bw_labels: tuple[str, ...]) -> str:
    """Return a readable list of available beam widths."""

    return ", ".join(f"{beam_width_mm_from_label(label):g}" for label in bw_labels)


def select_beam_width_labels(
    available_labels: tuple[str, ...],
    beam_width: str | float | int | None,
) -> tuple[str, ...]:
    """Return all available beam-width labels or the requested single label."""

    if beam_width is None:
        return available_labels

    selected_label = beam_width_to_label(beam_width)
    if selected_label not in available_labels:
        choices = format_beam_widths(available_labels)
        raise ValueError(f"Beam width {beam_width} is not available. Choose one of: {choices} mm")
    return (selected_label,)


def beam_width_output_token(bw_mm: float) -> str:
    """Return a filename-safe beam-width token."""

    return f"bw{bw_mm:g}mm".replace(".", "p")


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


def find_peak_pdd_profiles(
    *,
    beam_width: str | float | int | None = None,
    missing: list[Path] | None = None,
) -> list[tuple[float, list[tuple[int, str, float, Path]]]]:
    """Return peak PDD profiles for all or one public beam width."""

    profile_groups: list[tuple[float, list[tuple[int, str, float, Path]]]] = []
    for bw_label in select_beam_width_labels(PBP_PDD_BEAM_WIDTHS, beam_width):
        bw_mm = beam_width_mm_from_label(bw_label)
        selected: list[tuple[int, str, float, Path]] = []
        for energy in PBP_ENERGIES:
            for ctc_role, multiplier in PBP_CTC_CASES:
                ctc_mm = _pbp_ctc_mm(bw_label, multiplier)
                path = _pbp_profile_path("zpeak", bw_label, energy, ctc_mm)
                if path.exists():
                    selected.append((energy, ctc_role, ctc_mm, path))
                elif missing is not None:
                    missing.append(path)
        if selected:
            profile_groups.append((bw_mm, selected))
    return profile_groups


def _panel_grid(n_panels: int) -> tuple[int, int]:
    """Return a compact row-column grid for a requested panel count."""

    if n_panels <= 2:
        return 1, n_panels
    return math.ceil(n_panels / 2), 2


def plot_peak_pdd_profiles(
    *,
    beam_width: str | float | int | None = None,
    output: Path | None = None,
) -> Path:
    """Plot peak PDD profiles for the 1D MB geometry."""

    set_publication_style()
    missing: list[Path] = []
    groups = find_peak_pdd_profiles(beam_width=beam_width, missing=missing)
    report_missing_data(missing, analysis_name="Peak PDD")
    if not groups:
        raise FileNotFoundError(
            "No processed peak PDD data are available for the requested beam width. "
            "Please contact the authors for the corresponding data."
        )

    energies = sorted({energy for _, profiles in groups for energy, _, _, _ in profiles})
    colors = {energy: PBP_ENERGY_COLORS[energy] for energy in energies}
    single_panel = beam_width is not None

    if single_panel:
        fig, ax = plt.subplots(figsize=(9.0, 6.0))
        axes = [ax]
    else:
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
    line_handles: list[Line2D] = []
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
            if single_panel:
                line_handles.append(
                    Line2D(
                        [0],
                        [0],
                        color=colors[energy],
                        linestyle=linestyle,
                        linewidth=2.0,
                        label=f"{energy} MeV, ctc {ctc_mm:g} mm",
                    )
                )

        style_axes(
            ax,
            xlabel="z [mm]" if single_panel else "Depth z [mm]",
            ylabel="Normalized peak dose",
            title=f"FWHM = {bw_mm:g} mm" if single_panel else f"bw = {bw_mm:g} mm",
            grid_axis="y",
        )
        ax.set_ylim(0, 1.05)

    if not single_panel:
        for ax in axes[len(groups):]:
            ax.set_visible(False)
    for ax in axes[: len(groups)]:
        ax.set_xlim(left=0, right=max_depth)

    if single_panel:
        axes[0].legend(handles=line_handles, loc="upper right", frameon=True, fontsize=11, title="Energy, ctc")
        fig.tight_layout()
    else:
        energy_handles = [Line2D([0], [0], color=colors[energy], linewidth=2.0, label=f"{energy} MeV") for energy in energies]
        style_handles = [
            Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="-", label="ctc = 3 x bw"),
            Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="--", label="ctc = 5 x bw"),
        ]
        fig.legend(
            handles=energy_handles,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.955),
            ncol=min(len(energy_handles), 4),
            frameon=False,
        )
        fig.legend(handles=style_handles, loc="lower center", ncol=2, frameon=False)
        fig.suptitle("Peak PDD profiles for the MB configuration", y=0.99)
        fig.tight_layout(rect=(0, 0.08, 1, 0.87))

    if output is None:
        filename = "peak_pdd_profiles.png"
        if single_panel:
            filename = f"peak_pdd_profiles_{beam_width_output_token(groups[0][0])}.png"
        output = output_path(filename)
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
    """Return the peak-profile path used to normalize a valley PDD profile."""

    return valley_path.with_name(valley_path.name.replace("zvalley_", "zpeak_", 1))


def find_valley_pdd_profiles(
    *,
    beam_width: str | float | int | None = None,
    missing: list[Path] | None = None,
) -> list[tuple[float, list[tuple[int, str, float, Path, Path]]]]:
    """Return valley PDD profiles for all or one public beam width."""

    profile_groups: list[tuple[float, list[tuple[int, str, float, Path, Path]]]] = []
    for bw_label in select_beam_width_labels(PBP_PDD_BEAM_WIDTHS, beam_width):
        bw_mm = beam_width_mm_from_label(bw_label)
        selected: list[tuple[int, str, float, Path, Path]] = []
        for energy in PBP_ENERGIES:
            for ctc_role, multiplier in PBP_CTC_CASES:
                ctc_mm = _pbp_ctc_mm(bw_label, multiplier)
                valley_path = _pbp_profile_path("zvalley", bw_label, energy, ctc_mm)
                peak_path = _pbp_profile_path("zpeak", bw_label, energy, ctc_mm)
                if valley_path.exists() and peak_path.exists():
                    selected.append((energy, ctc_role, ctc_mm, valley_path, peak_path))
                elif missing is not None:
                    if not valley_path.exists():
                        missing.append(valley_path)
                    if not peak_path.exists():
                        missing.append(peak_path)
        if selected:
            profile_groups.append((bw_mm, selected))
    return profile_groups


def plot_valley_pdd_profiles(
    *,
    beam_width: str | float | int | None = None,
    output: Path | None = None,
) -> Path:
    """Plot valley PDD profiles for the 1D MB geometry."""

    set_publication_style()
    missing: list[Path] = []
    groups = find_valley_pdd_profiles(beam_width=beam_width, missing=missing)
    report_missing_data(missing, analysis_name="Valley PDD")
    if not groups:
        raise FileNotFoundError(
            "No processed valley PDD data are available for the requested beam width. "
            "Please contact the authors for the corresponding data."
        )

    energies = sorted({energy for _, profiles in groups for energy, _, _, _, _ in profiles})
    colors = {energy: PBP_ENERGY_COLORS[energy] for energy in energies}
    single_panel = beam_width is not None

    if single_panel:
        fig, ax = plt.subplots(figsize=(9.0, 6.0))
        axes = [ax]
    else:
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
    line_handles: list[Line2D] = []
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
            if single_panel:
                line_handles.append(
                    Line2D(
                        [0],
                        [0],
                        color=colors[energy],
                        linestyle=linestyle,
                        linewidth=2.0,
                        label=f"{energy} MeV, ctc {ctc_mm:g} mm",
                    )
                )

        style_axes(
            ax,
            xlabel="z [mm]" if single_panel else "Depth z [mm]",
            ylabel="Normalized valley dose",
            title=f"FWHM = {bw_mm:g} mm" if single_panel else f"bw = {bw_mm:g} mm",
            grid_axis="y",
        )
        ax.set_ylim(bottom=0)

    if not single_panel:
        for ax in axes[len(groups):]:
            ax.set_visible(False)
    for ax in axes[: len(groups)]:
        ax.set_xlim(left=0, right=max_depth)

    if single_panel:
        axes[0].legend(handles=line_handles, loc="upper right", frameon=True, fontsize=11, title="Energy, ctc")
        fig.tight_layout()
    else:
        energy_handles = [Line2D([0], [0], color=colors[energy], linewidth=2.0, label=f"{energy} MeV") for energy in energies]
        style_handles = [
            Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="-", label="ctc = 3 x bw"),
            Line2D([0], [0], color="0.2", linewidth=2.0, linestyle="--", label="ctc = 5 x bw"),
        ]
        fig.legend(
            handles=energy_handles,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.955),
            ncol=min(len(energy_handles), 4),
            frameon=False,
        )
        fig.legend(handles=style_handles, loc="lower center", ncol=2, frameon=False)
        fig.suptitle("Valley PDD profiles for the MB configuration", y=0.99)
        fig.tight_layout(rect=(0, 0.08, 1, 0.87))

    if output is None:
        filename = "valley_pdd_profiles.png"
        if single_panel:
            filename = f"valley_pdd_profiles_{beam_width_output_token(groups[0][0])}.png"
        output = output_path(filename)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output


def find_pvdr_profiles(
    *,
    beam_width: str | float | int | None = None,
    missing: list[Path] | None = None,
) -> list[tuple[dict[str, object], list[tuple[int, str, float, Path]]]]:
    """Return PVDR profiles for all or one public beam width."""

    profile_panels: list[tuple[dict[str, object], list[tuple[int, str, float, Path]]]] = []
    selected_labels = select_beam_width_labels(PBP_PVDR_BEAM_WIDTHS, beam_width)
    for panel in PBP_PVDR_CASES:
        if str(panel["bw_label"]) not in selected_labels:
            continue
        selected: list[tuple[int, str, float, Path]] = []
        for energy, ctc_values in panel["profiles"]:
            for role, ctc_mm in zip(("min", "max"), ctc_values):
                path = _pbp_pvdr_profile_path(str(panel["bw_label"]), int(energy), float(ctc_mm))
                if path.exists():
                    selected.append((int(energy), role, float(ctc_mm), path))
                elif missing is not None:
                    missing.append(path)
        if selected:
            profile_panels.append((panel, selected))
    return profile_panels


def plot_pvdr_profiles(
    *,
    beam_width: str | float | int | None = None,
    output: Path | None = None,
) -> Path:
    """Plot PVDR profiles for the 1D MB geometry."""

    set_publication_style()
    missing: list[Path] = []
    panels = find_pvdr_profiles(beam_width=beam_width, missing=missing)
    report_missing_data(missing, analysis_name="PVDR")
    if not panels:
        raise FileNotFoundError(
            "No processed PVDR data are available for the requested beam width. "
            "Please contact the authors for the corresponding data."
        )

    single_panel = beam_width is not None
    if single_panel:
        fig, ax = plt.subplots(figsize=(8.4, 6.0))
        axes = [ax]
    else:
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
            color = PBP_ENERGY_COLORS[energy]
            label = f"{energy} MeV, ctc {ctc_mm:g} mm" if single_panel else f"{ctc_mm:g} mm"
            ax.plot(depths_mm, pvdr, color=color, linestyle=linestyle)
            line_handles.append(
                Line2D([0], [0], color=color, linestyle=linestyle, linewidth=2.0, label=label)
            )

        ax.set_yscale("log")
        ax.set_ylim(0.75, 2000)
        ax.set_xlim(0, int(panel["xmax"]))
        style_axes(
            ax,
            xlabel="z [mm]" if single_panel or str(panel["panel"]) in {"e", "f"} else "",
            ylabel="PVDR",
            title=f"FWHM = {panel['bw_mm']:g} mm",
            grid_axis="y",
        )
        if not single_panel:
            ax.text(-0.10, 1.04, str(panel["panel"]), transform=ax.transAxes, fontsize=16, fontweight="bold")
        ax.legend(
            handles=line_handles,
            title="Energy, ctc" if single_panel else "ctc",
            loc="upper right",
            frameon=single_panel,
            handlelength=2.4,
        )

    if single_panel:
        fig.tight_layout()
    else:
        energy_handles = [
            Line2D([0], [0], marker="s", linestyle="None", color=color, markersize=10, label=f"{energy} MeV")
            for energy, color in PBP_ENERGY_COLORS.items()
        ]
        fig.legend(handles=energy_handles, loc="lower center", ncol=4, frameon=False)
        fig.tight_layout(rect=(0, 0.055, 1, 1))

    if output is None:
        filename = "pvdr_profiles.png"
        if single_panel:
            filename = f"pvdr_profiles_{beam_width_output_token(float(panels[0][0]['bw_mm']))}.png"
        output = output_path(filename)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output
