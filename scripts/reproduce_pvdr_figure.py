"""Reproduce the representative PVDR figure from processed CSV data."""

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
    csv_path = ROOT / "data" / "figure_source_data" / "fig_pvdr_vs_depth_or_ctc.csv"
    data = read_nonempty_csv(csv_path, ["energy_MeV", "ctc_mm", "depth_mm", "PVDR"])

    if 150 in set(data["energy_MeV"]):
        data = data[data["energy_MeV"] == 150].copy()
        title = "PVDR versus depth at 150 MeV"
    else:
        energy = sorted(data["energy_MeV"].dropna().unique())[0]
        data = data[data["energy_MeV"] == energy].copy()
        title = f"PVDR versus depth at {energy} MeV"

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    group_columns = ["ctc_mm"]

    for key, group in data.sort_values("depth_mm").groupby(group_columns, dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        label = ", ".join(f"ctc={value} mm" for value in key)
        ax.plot(group["depth_mm"], group["PVDR"], marker="o", linewidth=1.5, label=label)

    ax.axhline(1.1, color="0.35", linestyle=":", linewidth=1.0)
    finalize_axes(
        ax,
        xlabel="Depth [mm]",
        ylabel="PVDR",
        title=title,
    )
    fig.tight_layout()
    output = output_path("fig_pvdr_vs_depth_or_ctc.png")
    fig.savefig(output, dpi=300)
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
