"""Common plotting helpers for processed CSV figure-source data."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def read_nonempty_csv(path: str | Path, required_columns: list[str]) -> pd.DataFrame:
    """Read a processed CSV and validate that it has rows and required columns."""

    csv_path = Path(path)
    try:
        display_path = csv_path.relative_to(Path.cwd())
    except ValueError:
        display_path = Path(csv_path.name)

    if not csv_path.exists():
        raise FileNotFoundError(display_path)

    data = pd.read_csv(csv_path)
    missing = [column for column in required_columns if column not in data.columns]
    if missing:
        raise ValueError(f"{display_path} is missing required columns: {', '.join(missing)}")
    if data.empty:
        raise ValueError(
            f"{display_path} contains headers but no data rows. Populate it from the "
            "legacy processed outputs before reproducing this figure."
        )
    return data


def output_path(filename: str) -> Path:
    """Return an output path under ``figures/generated`` and create the folder."""

    root = Path(__file__).resolve().parents[1]
    out_dir = root / "figures" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename


def grouped_label(row: pd.Series, fields: tuple[str, ...]) -> str:
    """Build a compact label from non-null row fields."""

    parts = []
    for field in fields:
        value = row.get(field)
        if pd.notna(value):
            parts.append(f"{field}={value}")
    return ", ".join(parts)


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
