"""Reproduce the representative homogeneity figure from processed CSV data."""

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

from plotting import finalize_axes, output_path, read_nonempty_csv


def main() -> None:
    csv_path = ROOT / "data" / "figure_source_data" / "fig_homogeneity.csv"
    data = read_nonempty_csv(csv_path, ["energy_MeV", "ctc_mm", "homogeneous_flag"])

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    colors = data["homogeneous_flag"].map({0: "#7F7F7F", 1: "#1B9E77", False: "#7F7F7F", True: "#1B9E77"})
    ax.scatter(data["energy_MeV"], data["ctc_mm"], c=colors, s=36, edgecolor="black", linewidth=0.4)

    finalize_axes(
        ax,
        xlabel="Energy [MeV]",
        ylabel="Center-to-center distance [mm]",
        title="Target homogeneity",
    )
    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#1B9E77", markeredgecolor="black", label="Homogeneous"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#7F7F7F", markeredgecolor="black", label="Not homogeneous"),
    ]
    ax.legend(handles=legend_handles, frameon=False)
    fig.tight_layout()
    output = output_path("fig_homogeneity.png")
    fig.savefig(output, dpi=300)
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
