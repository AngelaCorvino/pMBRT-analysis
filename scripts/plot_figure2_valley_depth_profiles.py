"""Generate Figure 2 valley depth-dose profiles from processed .txt data."""

from __future__ import annotations

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
sys.path.insert(0, str(ROOT / "src"))

from plotting import plot_figure2_valley_depth_profiles


def main() -> None:
    output = plot_figure2_valley_depth_profiles()
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
