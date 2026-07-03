"""Generate Supplementary Figure S5 PVDR depth profiles from processed .txt data."""

from __future__ import annotations

from pathlib import Path
import os
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MPLCONFIGDIR = Path(tempfile.gettempdir()) / "pMBRT-analysis-mplconfig"
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib

matplotlib.use("Agg")
sys.path.insert(0, str(ROOT / "src"))

from plotting import plot_figure_s5_pvdr_depth_profiles


def main() -> None:
    """Generate Supplementary Figure S5 and print the written output path."""

    output = plot_figure_s5_pvdr_depth_profiles()
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
