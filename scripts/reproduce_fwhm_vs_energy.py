"""Reproduce the representative FWHM figure from processed CSV data."""

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
    csv_path = ROOT / "data" / "figure_source_data" / "fig_fwhm_vs_energy.csv"
    data = read_nonempty_csv(csv_path, ["energy_MeV", "depth_mm", "FWHM_mm"])

    if "source_type" in data.columns and (data["source_type"] == "single_beam").any():
        data = data[data["source_type"] == "single_beam"].copy()
        title = "Single-beam FWHM versus depth"
    else:
        title = "FWHM versus depth"

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    group_columns = ["energy_MeV"] if "energy_MeV" in data.columns else []

    for key, group in data.sort_values("depth_mm").groupby(group_columns, dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        label = ", ".join(f"{value} MeV" if col == "energy_MeV" else f"{col}={value}" for col, value in zip(group_columns, key))
        ax.plot(group["depth_mm"], group["FWHM_mm"], marker="o", linewidth=1.5, label=label)

    finalize_axes(
        ax,
        xlabel="Depth [mm]",
        ylabel="FWHM [mm]",
        title=title,
    )
    fig.tight_layout()
    output = output_path("fig_fwhm_vs_energy.png")
    fig.savefig(output, dpi=300)
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
