"""Reproduce the representative FWHM figure directly from processed .txt data."""

from __future__ import annotations

from pathlib import Path
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(ROOT / "src"))

from plotting import PROCESSED_TEXT_ROOT, finalize_axes, output_path, read_numeric_series


FWHM_DEPTH_STEP_MM = 3


def parse_energy(path: Path) -> int:
    match = re.fullmatch(r"FWHM_singlebeam_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected FWHM filename: {path.name}")
    return int(match.group(1))


def main() -> None:
    paths = sorted(PROCESSED_TEXT_ROOT.glob("*MeV/FWHM_singlebeam_*MeV.txt"), key=parse_energy)
    if not paths:
        raise FileNotFoundError("No FWHM_singlebeam_*MeV.txt files found under data/processed_text")

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for path in paths:
        energy = parse_energy(path)
        values = read_numeric_series(path)
        depths_mm = [index * FWHM_DEPTH_STEP_MM for index in range(len(values))]
        ax.plot(depths_mm, values, marker="o", linewidth=1.5, label=f"{energy} MeV")

    finalize_axes(
        ax,
        xlabel="Depth [mm]",
        ylabel="FWHM [mm]",
        title="Single-beam FWHM versus depth",
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
