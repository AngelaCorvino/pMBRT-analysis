"""Reproduce the representative PVDR figure directly from processed .txt data."""

from __future__ import annotations

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
sys.path.insert(0, str(ROOT / "src"))

from plotting import plot_pvdr_vs_depth


def main() -> None:
    output = plot_pvdr_vs_depth()
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
