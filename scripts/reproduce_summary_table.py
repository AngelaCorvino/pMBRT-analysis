"""Create a representative text summary table directly from processed .txt data."""

from __future__ import annotations

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))
sys.path.insert(0, str(ROOT / "src"))

from plotting import PROCESSED_TEXT_ROOT, iter_metric_dictionary, output_path, read_json_dictionary


BP_DEPTH_MM = {
    50: 21,
    75: 45,
    100: 75,
    125: 112,
    150: 155,
    175: 203,
    200: 256,
    230: 325,
}


def load_bedr_flags() -> dict[tuple[float, int, float], object]:
    path = PROCESSED_TEXT_ROOT / "dose_BEDR_1Darray_dictionary.txt"
    data = read_json_dictionary(path)
    flags = {}
    for bw_label, by_energy in data.items():
        bw_mm = float(bw_label) / 10.0
        for energy_label, by_ctc in by_energy.items():
            energy = int(energy_label)
            for ctc_label, metrics in by_ctc.items():
                flags[(bw_mm, energy, float(ctc_label))] = metrics.get("D_BP>0.6D_entrance", "")
    return flags


def format_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    string_rows = [[str(row.get(column, "")) for column in columns] for row in rows]
    widths = [len(column) for column in columns]
    for row in string_rows:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]

    def line(values: list[str]) -> str:
        return "  ".join(value.ljust(width) for value, width in zip(values, widths)).rstrip()

    output = [line(columns), line(["-" * width for width in widths])]
    output.extend(line(row) for row in string_rows)
    return "\n".join(output) + "\n"


def main() -> None:
    bedr_flags = load_bedr_flags()
    rows = []
    for row in iter_metric_dictionary(
        PROCESSED_TEXT_ROOT / "dose_min_max_1Darray_dictionary.txt",
        setup="PBP 1D array",
        dimension="x",
    ):
        metrics = row["metrics"]
        homogeneity_code = metrics.get("homogeneity_at_BP", "")
        rows.append(
            {
                "setup": row["setup"],
                "energy_MeV": row["energy_MeV"],
                "bw_mm": row["bw_mm"],
                "ctc_mm": row["ctc_mm"],
                "target_depth_mm": BP_DEPTH_MM.get(row["energy_MeV"], ""),
                "target_homogeneity": int(float(homogeneity_code) > 0) if homogeneity_code != "" else "",
                "homogeneity_code": homogeneity_code,
                "min_normalized_dose": metrics.get("min_dose", ""),
                "max_normalized_dose": metrics.get("max_dose", ""),
                "BEDR_threshold_flag": bedr_flags.get((row["bw_mm"], row["energy_MeV"], row["ctc_mm"]), ""),
            }
        )

    if not rows:
        raise ValueError("No summary rows found in processed text dictionaries")

    rows = sorted(rows, key=lambda item: (item["energy_MeV"], item["ctc_mm"]))
    columns = [
        "setup",
        "energy_MeV",
        "bw_mm",
        "ctc_mm",
        "target_depth_mm",
        "target_homogeneity",
        "homogeneity_code",
        "min_normalized_dose",
        "max_normalized_dose",
        "BEDR_threshold_flag",
    ]
    output = output_path("summary_metrics_table.txt")
    output.write_text(format_table(rows, columns), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
