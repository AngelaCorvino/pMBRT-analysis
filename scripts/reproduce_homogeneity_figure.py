"""Reproduce the representative homogeneity figure directly from processed .txt data."""

from __future__ import annotations

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(ROOT / "src"))

from plotting import PROCESSED_TEXT_ROOT, finalize_axes, iter_metric_dictionary, output_path


SOURCES = [
    ("PBP 1D array", "x", "dose_min_max_1Darray_dictionary.txt", "o"),
    ("PBP 2D array", "xy", "dose_min_max_2Darray_finalversion.txt", "s"),
]


def main() -> None:
    rows = []
    for setup, dimension, filename, marker in SOURCES:
        path = PROCESSED_TEXT_ROOT / filename
        for row in iter_metric_dictionary(path, setup=setup, dimension=dimension):
            metrics = row["metrics"]
            homogeneity_code = metrics.get("homogeneity_at_BP", 0)
            rows.append({**row, "homogeneous": float(homogeneity_code) > 0, "marker": marker})

    if not rows:
        raise ValueError("No homogeneity rows found in processed text dictionaries")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for setup, _, _, marker in SOURCES:
        setup_rows = [row for row in rows if row["setup"] == setup]
        for homogeneous, color, label_suffix in [
            (True, "#1B9E77", "homogeneous"),
            (False, "#7F7F7F", "not homogeneous"),
        ]:
            filtered = [row for row in setup_rows if row["homogeneous"] is homogeneous]
            if not filtered:
                continue
            ax.scatter(
                [row["energy_MeV"] for row in filtered],
                [row["ctc_mm"] for row in filtered],
                c=color,
                marker=marker,
                s=36,
                edgecolor="black",
                linewidth=0.4,
                label=f"{setup}, {label_suffix}",
            )

    finalize_axes(
        ax,
        xlabel="Energy [MeV]",
        ylabel="Center-to-center distance [mm]",
        title="Target homogeneity",
    )
    fig.tight_layout()
    output = output_path("fig_homogeneity.png")
    fig.savefig(output, dpi=300)
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
