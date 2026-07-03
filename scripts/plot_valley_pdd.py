"""Generate valley PDD profiles from processed .txt data."""

from __future__ import annotations

import argparse
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

from plotting import plot_valley_pdd_profiles


def parse_args() -> argparse.Namespace:
    """Return command-line arguments for valley PDD plotting."""

    parser = argparse.ArgumentParser(description="Plot processed valley PDD profiles.")
    parser.add_argument("--bw", "--beam-width", dest="beam_width", help="Optional beam width in mm, for example 0.7 or 1.2.")
    parser.add_argument("--output", type=Path, help="Optional output image path.")
    return parser.parse_args()


def main() -> None:
    """Generate valley PDD output and print the written output path."""

    args = parse_args()
    output = plot_valley_pdd_profiles(beam_width=args.beam_width, output=args.output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
