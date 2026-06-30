"""Common plotting and processed-text helpers for the public pMBRT repository."""

from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_TEXT_ROOT = ROOT / "data" / "processed_text" / "PBP_paperdataset" / "FWHM5"


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


def finalize_axes(ax, *, xlabel: str, ylabel: str, title: str | None = None) -> None:
    """Apply simple, publication-neutral axis styling."""

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, axis="both", linestyle=":", alpha=0.3)
    handles, _ = ax.get_legend_handles_labels()
    if handles:
        ax.legend(frameon=False, fontsize=8)
