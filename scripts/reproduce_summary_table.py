"""Reproduce the representative summary table from processed CSV data."""

from __future__ import annotations

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))
sys.path.insert(0, str(ROOT / "src"))

from plotting import output_path, read_nonempty_csv


REQUIRED_COLUMNS = [
    "setup",
    "energy_MeV",
    "bw_mm",
    "ctc_mm",
    "target_depth_mm",
    "PVDR_target",
    "FWHM_target_mm",
    "target_homogeneity",
]


def dataframe_to_markdown(data) -> str:
    headers = list(data.columns)
    rows = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in data.iterrows():
        rows.append("| " + " | ".join("" if row[col] != row[col] else str(row[col]) for col in headers) + " |")
    return "\n".join(rows) + "\n"


def main() -> None:
    csv_path = ROOT / "data" / "figure_source_data" / "summary_metrics.csv"
    data = read_nonempty_csv(csv_path, REQUIRED_COLUMNS)

    csv_output = output_path("summary_metrics_table.csv")
    md_output = output_path("summary_metrics_table.md")
    data.to_csv(csv_output, index=False)
    md_output.write_text(dataframe_to_markdown(data), encoding="utf-8")
    print(f"Wrote {csv_output}")
    print(f"Wrote {md_output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
