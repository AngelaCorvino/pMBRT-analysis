"""Build public figure-source CSVs from a curated legacy data subset.

This script is optional and is not required for readers who only want to
reproduce figures from the published CSV files. It is included to document how
the CSVs in this repository were extracted from a small legacy data subset.

Usage:
    python scripts/build_figure_source_data_from_legacy.py /path/to/pMBRTData
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re


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

FWHM_HEADER = [
    "figure",
    "panel",
    "setup",
    "source_type",
    "energy_MeV",
    "bw_mm",
    "ctc_mm",
    "depth_mm",
    "depth_cm",
    "FWHM_mm",
    "source_file",
    "notes",
]

PVDR_HEADER = [
    "figure",
    "panel",
    "setup",
    "energy_MeV",
    "bw_mm",
    "ctc_mm",
    "depth_mm",
    "depth_cm",
    "peak_dose_Gy",
    "valley_dose_Gy",
    "PVDR",
    "source_file",
    "notes",
]

HOMOGENEITY_HEADER = [
    "figure",
    "panel",
    "setup",
    "homogeneity_dimension",
    "energy_MeV",
    "bw_mm",
    "ctc_mm",
    "target_depth_mm",
    "target_depth_cm",
    "homogeneous_flag",
    "homogeneity_code",
    "homogeneity_before_target_flag",
    "relative_std_at_target",
    "min_normalized_dose",
    "max_normalized_dose",
    "gamma",
    "criterion",
    "dose_threshold_flag",
    "source_file",
    "notes",
]

SUMMARY_HEADER = [
    "setup",
    "energy_MeV",
    "bw_mm",
    "ctc_mm",
    "target_depth_mm",
    "target_depth_cm",
    "PVDR_target",
    "PVDR_entrance",
    "BEDR",
    "BEDR_threshold_flag",
    "FWHM_entrance_mm",
    "FWHM_target_mm",
    "target_homogeneity",
    "homogeneity_code",
    "relative_std_at_target",
    "source_files",
    "notes",
]


def read_series(path: Path) -> list[float]:
    values: list[float] = []
    with path.open() as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                values.append(float(stripped))
    return values


def write_csv(path: Path, header: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fwhm_dir_to_bw_mm(path: Path) -> float:
    match = re.fullmatch(r"FWHM(\d+)", path.name)
    if not match:
        raise ValueError(f"Cannot infer beam width from {path}")
    return int(match.group(1)) / 10.0


def find_fwhm_dirs(legacy_root: Path) -> list[Path]:
    if legacy_root.name.startswith("FWHM"):
        return [legacy_root]

    candidates = sorted(legacy_root.glob("FWHM*"))
    if candidates:
        return [path for path in candidates if path.is_dir()]

    paper_subset = legacy_root / "PBP_paperdataset"
    if paper_subset.exists():
        return [path for path in sorted(paper_subset.glob("FWHM*")) if path.is_dir()]

    raise FileNotFoundError("No FWHM* data directories found under the legacy root.")


def relative_source(path: Path, legacy_root: Path) -> str:
    try:
        return str(path.relative_to(legacy_root))
    except ValueError:
        return path.name


def parse_array_fwhm_name(path: Path) -> tuple[str, float, int]:
    match = re.fullmatch(r"FWHM_(1Darray|2Darray)_ctc(\d+)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected FWHM filename: {path.name}")
    source_type = match.group(1)
    ctc_mm = int(match.group(2)) / 10.0
    energy = int(match.group(3))
    return source_type, ctc_mm, energy


def parse_pvdr_name(path: Path) -> tuple[float, int, int]:
    match = re.fullmatch(r"PVDR_2Darray_(ctc\d+|\d+(?:\.\d+)?)_(\d+)MeV\.txt", path.name)
    if not match:
        raise ValueError(f"Unexpected PVDR filename: {path.name}")

    token = match.group(1)
    if token.startswith("ctc"):
        ctc_mm = int(token[3:]) / 10.0
        priority = 0
    elif "." in token:
        ctc_mm = float(token)
        priority = 1
    else:
        value = int(token)
        ctc_mm = value / 10.0 if value >= 10 else float(value)
        priority = 2

    return ctc_mm, int(match.group(2)), priority


def append_fwhm_rows(
    legacy_root: Path,
    fwhm_dirs: list[Path],
) -> tuple[list[dict[str, object]], dict[tuple[str, float, int, float | None], tuple[list[float], str]]]:
    rows: list[dict[str, object]] = []
    index: dict[tuple[str, float, int, float | None], tuple[list[float], str]] = {}

    for fwhm_dir in fwhm_dirs:
        bw_mm = fwhm_dir_to_bw_mm(fwhm_dir)

        for path in sorted(fwhm_dir.glob("*MeV/FWHM_singlebeam_*MeV.txt")):
            match = re.fullmatch(r"FWHM_singlebeam_(\d+)MeV\.txt", path.name)
            if not match:
                continue
            energy = int(match.group(1))
            values = read_series(path)
            source = relative_source(path, legacy_root)
            index[("single_beam", bw_mm, energy, None)] = (values, source)
            for sample_index, fwhm_mm in enumerate(values):
                depth_mm = sample_index * 3
                rows.append(
                    {
                        "figure": "fig_fwhm_vs_energy",
                        "panel": "single_beam",
                        "setup": "PBP",
                        "source_type": "single_beam",
                        "energy_MeV": energy,
                        "bw_mm": bw_mm,
                        "ctc_mm": "",
                        "depth_mm": depth_mm,
                        "depth_cm": depth_mm / 10.0,
                        "FWHM_mm": fwhm_mm,
                        "source_file": source,
                        "notes": "processed FWHM text file; depth spacing follows legacy plotting script",
                    }
                )

        for path in sorted(fwhm_dir.glob("FWHM_*array_ctc*_*MeV.txt")):
            source_type, ctc_mm, energy = parse_array_fwhm_name(path)
            values = read_series(path)
            source = relative_source(path, legacy_root)
            setup = "PBP_1D_array" if source_type == "1Darray" else "PBP_2D_array"
            index[(setup, bw_mm, energy, ctc_mm)] = (values, source)
            for sample_index, fwhm_mm in enumerate(values):
                depth_mm = sample_index * 3
                rows.append(
                    {
                        "figure": "fig_fwhm_vs_energy",
                        "panel": source_type,
                        "setup": setup,
                        "source_type": source_type,
                        "energy_MeV": energy,
                        "bw_mm": bw_mm,
                        "ctc_mm": ctc_mm,
                        "depth_mm": depth_mm,
                        "depth_cm": depth_mm / 10.0,
                        "FWHM_mm": fwhm_mm,
                        "source_file": source,
                        "notes": "processed FWHM text file; depth spacing follows legacy plotting script",
                    }
                )

    return rows, index


def append_pvdr_rows(
    legacy_root: Path,
    fwhm_dirs: list[Path],
) -> tuple[list[dict[str, object]], dict[tuple[float, int, float], tuple[list[float], str]]]:
    rows: list[dict[str, object]] = []
    selected: dict[tuple[float, int, float], tuple[int, Path]] = {}

    for fwhm_dir in fwhm_dirs:
        bw_mm = fwhm_dir_to_bw_mm(fwhm_dir)
        for path in sorted(fwhm_dir.glob("*MeV/PVDR_2Darray_*.txt")):
            ctc_mm, energy, priority = parse_pvdr_name(path)
            key = (bw_mm, energy, ctc_mm)
            if key not in selected or priority < selected[key][0]:
                selected[key] = (priority, path)

    index: dict[tuple[float, int, float], tuple[list[float], str]] = {}
    for (bw_mm, energy, ctc_mm), (_, path) in sorted(selected.items()):
        values = read_series(path)
        source = relative_source(path, legacy_root)
        parent_energy = path.parent.name.removesuffix("MeV")
        note_parts = ["processed PVDR text file; peak and valley dose values not stored in this source"]
        if parent_energy != str(energy):
            note_parts.append("filename energy differs from parent folder; filename energy used")
        notes = "; ".join(note_parts)
        index[(bw_mm, energy, ctc_mm)] = (values, source)

        for sample_index, pvdr in enumerate(values):
            depth_mm = sample_index
            rows.append(
                {
                    "figure": "fig_pvdr_vs_depth_or_ctc",
                    "panel": "2D_array_depth_profile",
                    "setup": "PBP_2D_array",
                    "energy_MeV": energy,
                    "bw_mm": bw_mm,
                    "ctc_mm": ctc_mm,
                    "depth_mm": depth_mm,
                    "depth_cm": depth_mm / 10.0,
                    "peak_dose_Gy": "",
                    "valley_dose_Gy": "",
                    "PVDR": pvdr,
                    "source_file": source,
                    "notes": notes,
                }
            )

    return rows, index


def iter_nested_metrics(path: Path):
    data = json.load(path.open())
    for bw_label, by_energy in data.items():
        bw_mm = float(bw_label) / 10.0
        for energy_label, by_ctc in by_energy.items():
            for ctc_label, metrics in by_ctc.items():
                yield bw_mm, int(energy_label), float(ctc_label), metrics


def build_homogeneity_rows(
    legacy_root: Path,
    fwhm_dirs: list[Path],
) -> tuple[list[dict[str, object]], dict[tuple[str, float, int, float], tuple[dict[str, object], str]]]:
    rows: list[dict[str, object]] = []
    index: dict[tuple[str, float, int, float], tuple[dict[str, object], str]] = {}
    sources = [
        ("PBP_1D_array", "x", "dose_min_max_1Darray_dictionary.txt"),
        ("PBP_2D_array", "xy", "dose_min_max_2Darray_finalversion.txt"),
    ]

    for fwhm_dir in fwhm_dirs:
        for setup, dimension, filename in sources:
            path = fwhm_dir / filename
            if not path.exists():
                continue
            source = relative_source(path, legacy_root)
            for bw_mm, energy, ctc_mm, metrics in iter_nested_metrics(path):
                target_depth_mm = BP_DEPTH_MM.get(energy, "")
                homogeneity_code = metrics.get("homogeneity_at_BP", "")
                homogeneous_flag = int(float(homogeneity_code) > 0) if homogeneity_code != "" else ""
                index[(setup, bw_mm, energy, ctc_mm)] = (metrics, source)
                rows.append(
                    {
                        "figure": "fig_homogeneity",
                        "panel": dimension,
                        "setup": setup,
                        "homogeneity_dimension": dimension,
                        "energy_MeV": energy,
                        "bw_mm": bw_mm,
                        "ctc_mm": ctc_mm,
                        "target_depth_mm": target_depth_mm,
                        "target_depth_cm": target_depth_mm / 10.0 if target_depth_mm != "" else "",
                        "homogeneous_flag": homogeneous_flag,
                        "homogeneity_code": homogeneity_code,
                        "homogeneity_before_target_flag": metrics.get("homogeneity_before_BP", ""),
                        "relative_std_at_target": "",
                        "min_normalized_dose": metrics.get("min_dose", ""),
                        "max_normalized_dose": metrics.get("max_dose", ""),
                        "gamma": metrics.get("gamma", ""),
                        "criterion": "legacy dictionary fields homogeneity_at_BP and homogeneity_before_BP",
                        "dose_threshold_flag": metrics.get("D_BP>0.4D_entrance", ""),
                        "source_file": source,
                        "notes": "homogeneity_code preserves the original dictionary value; homogeneous_flag is 1 when code > 0",
                    }
                )

    return rows, index


def build_bedr_threshold_index(
    legacy_root: Path,
    fwhm_dirs: list[Path],
) -> dict[tuple[str, float, int, float], tuple[object, str]]:
    index: dict[tuple[str, float, int, float], tuple[object, str]] = {}
    for fwhm_dir in fwhm_dirs:
        path = fwhm_dir / "dose_BEDR_1Darray_dictionary.txt"
        if not path.exists():
            continue
        source = relative_source(path, legacy_root)
        for bw_mm, energy, ctc_mm, metrics in iter_nested_metrics(path):
            index[("PBP_1D_array", bw_mm, energy, ctc_mm)] = (
                metrics.get("D_BP>0.6D_entrance", ""),
                source,
            )
    return index


def nearest_fwhm_at_depth(values: list[float], target_depth_mm: int) -> float | str:
    if not values:
        return ""
    nearest_index = min(range(len(values)), key=lambda idx: abs(idx * 3 - target_depth_mm))
    return values[nearest_index]


def build_summary_rows(
    homogeneity_index: dict[tuple[str, float, int, float], tuple[dict[str, object], str]],
    fwhm_index: dict[tuple[str, float, int, float | None], tuple[list[float], str]],
    pvdr_index: dict[tuple[float, int, float], tuple[list[float], str]],
    bedr_index: dict[tuple[str, float, int, float], tuple[object, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, (metrics, homogeneity_source) in sorted(homogeneity_index.items()):
        setup, bw_mm, energy, ctc_mm = key
        target_depth_mm = BP_DEPTH_MM.get(energy, "")
        source_files = [homogeneity_source]

        fwhm_values, fwhm_source = fwhm_index.get(key, ([], ""))
        if fwhm_source:
            source_files.append(fwhm_source)

        pvdr_target = ""
        pvdr_entrance = ""
        if setup == "PBP_2D_array":
            pvdr_values, pvdr_source = pvdr_index.get((bw_mm, energy, ctc_mm), ([], ""))
        else:
            pvdr_values, pvdr_source = ([], "")
        if pvdr_source:
            source_files.append(pvdr_source)
            if pvdr_values:
                pvdr_entrance = pvdr_values[0]
                if target_depth_mm != "" and target_depth_mm < len(pvdr_values):
                    pvdr_target = pvdr_values[target_depth_mm]

        bedr_threshold_flag, bedr_source = bedr_index.get(key, ("", ""))
        if bedr_source:
            source_files.append(bedr_source)

        homogeneity_code = metrics.get("homogeneity_at_BP", "")
        target_homogeneity = int(float(homogeneity_code) > 0) if homogeneity_code != "" else ""
        notes = []
        if setup == "PBP_1D_array" and not pvdr_source:
            notes.append("PVDR source files in this subset are labeled 2Darray")
        if bedr_threshold_flag != "":
            notes.append("BEDR source provides threshold flag only, not numeric BEDR")
        if pvdr_source and pvdr_target == "":
            notes.append("target depth exceeds available PVDR depth profile")

        rows.append(
            {
                "setup": setup,
                "energy_MeV": energy,
                "bw_mm": bw_mm,
                "ctc_mm": ctc_mm,
                "target_depth_mm": target_depth_mm,
                "target_depth_cm": target_depth_mm / 10.0 if target_depth_mm != "" else "",
                "PVDR_target": pvdr_target,
                "PVDR_entrance": pvdr_entrance,
                "BEDR": "",
                "BEDR_threshold_flag": bedr_threshold_flag,
                "FWHM_entrance_mm": fwhm_values[0] if fwhm_values else "",
                "FWHM_target_mm": nearest_fwhm_at_depth(fwhm_values, target_depth_mm) if target_depth_mm != "" else "",
                "target_homogeneity": target_homogeneity,
                "homogeneity_code": homogeneity_code,
                "relative_std_at_target": "",
                "source_files": ";".join(dict.fromkeys(source_files)),
                "notes": "; ".join(notes),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("legacy_root", type=Path, help="Path to pMBRTData, PBP_paperdataset, or an FWHM* subset.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "figure_source_data",
        help="Directory where public CSVs will be written.",
    )
    args = parser.parse_args()

    legacy_root = args.legacy_root.resolve()
    fwhm_dirs = find_fwhm_dirs(legacy_root)

    fwhm_rows, fwhm_index = append_fwhm_rows(legacy_root, fwhm_dirs)
    pvdr_rows, pvdr_index = append_pvdr_rows(legacy_root, fwhm_dirs)
    homogeneity_rows, homogeneity_index = build_homogeneity_rows(legacy_root, fwhm_dirs)
    bedr_index = build_bedr_threshold_index(legacy_root, fwhm_dirs)
    summary_rows = build_summary_rows(homogeneity_index, fwhm_index, pvdr_index, bedr_index)

    write_csv(args.output_dir / "fig_fwhm_vs_energy.csv", FWHM_HEADER, fwhm_rows)
    write_csv(args.output_dir / "fig_pvdr_vs_depth_or_ctc.csv", PVDR_HEADER, pvdr_rows)
    write_csv(args.output_dir / "fig_homogeneity.csv", HOMOGENEITY_HEADER, homogeneity_rows)
    write_csv(args.output_dir / "summary_metrics.csv", SUMMARY_HEADER, summary_rows)

    print(f"Wrote {len(fwhm_rows)} FWHM rows")
    print(f"Wrote {len(pvdr_rows)} PVDR rows")
    print(f"Wrote {len(homogeneity_rows)} homogeneity rows")
    print(f"Wrote {len(summary_rows)} summary rows")


if __name__ == "__main__":
    main()
