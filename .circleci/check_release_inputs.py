"""Check that public release inputs are scoped and readable."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MPLCONFIGDIR = Path(tempfile.gettempdir()) / "pMBRT-analysis-mplconfig"
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))
sys.path.insert(0, str(ROOT / "src"))

from plotting import (  # noqa: E402
    PBP_ENERGY_COLORS,
    PBP_ENERGIES,
    find_peak_pdd_profiles,
    find_pvdr_profiles,
    find_valley_pdd_profiles,
    read_numeric_series,
)


REQUIRED_PUBLIC_FILES = (
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "requirements.txt",
    "src/plotting.py",
    "scripts/plot_peak_pdd.py",
    "scripts/plot_valley_pdd.py",
    "scripts/plot_pvdr.py",
    "data/data_dictionary.md",
    "data/processed_data/README.md",
)
FORBIDDEN_TRACKED_PREFIXES = ("private_legacy_do_not_publish/",)
FORBIDDEN_TRACKED_SUFFIXES = (
    ".bin",
    ".header",
    ".mha",
    ".mhd",
    ".npy",
    ".npz",
    ".raw",
    ".root",
)
EXPECTED_ENERGY_COLORS = {
    50: "#9DD4E8",
    125: "#00A51A",
    175: "#FF1F2D",
    230: "#FF8C00",
}


def display(path: Path) -> str:
    """Return a path relative to the repository root when possible."""

    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check_required_public_files(errors: list[str]) -> None:
    """Check that required public release files are present."""

    for relative_path in REQUIRED_PUBLIC_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"Missing required public file: {relative_path}")


def tracked_files() -> list[str]:
    """Return files tracked by Git."""

    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def check_tracked_file_scope(errors: list[str]) -> None:
    """Check that raw or private-local files are not tracked."""

    for path in tracked_files():
        if path.startswith(FORBIDDEN_TRACKED_PREFIXES):
            errors.append(f"Private-local path is tracked: {path}")
        if path.lower().endswith(FORBIDDEN_TRACKED_SUFFIXES):
            errors.append(f"Raw or volume data file is tracked: {path}")


def check_energy_color_mapping(errors: list[str]) -> None:
    """Check that all public plots use the fixed energy color convention."""

    if PBP_ENERGY_COLORS != EXPECTED_ENERGY_COLORS:
        errors.append(f"Unexpected energy color mapping: {PBP_ENERGY_COLORS}")
    if tuple(PBP_ENERGY_COLORS) != PBP_ENERGIES:
        errors.append(f"Energy color order does not match public plot energies: {tuple(PBP_ENERGY_COLORS)}")


def check_numeric_profile(path: Path, errors: list[str]) -> None:
    """Check that one processed profile can be read as numeric text data."""

    try:
        read_numeric_series(path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Invalid processed profile {display(path)}: {exc}")


def check_peak_pdd_inputs(errors: list[str]) -> None:
    """Check that included peak PDD profiles can be read."""

    try:
        groups = find_peak_pdd_profiles(missing=[])
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Peak PDD input discovery failed: {exc}")
        return

    profile_count = sum(len(profiles) for _, profiles in groups)
    if profile_count == 0:
        errors.append("No included peak PDD profiles were found")
    for _, profiles in groups:
        for _, _, _, path in profiles:
            check_numeric_profile(path, errors)


def check_valley_pdd_inputs(errors: list[str]) -> None:
    """Check that included valley PDD profiles and matching peaks can be read."""

    try:
        groups = find_valley_pdd_profiles(missing=[])
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Valley PDD input discovery failed: {exc}")
        return

    profile_count = sum(len(profiles) for _, profiles in groups)
    if profile_count == 0:
        errors.append("No included valley PDD profiles were found")
    for _, profiles in groups:
        for _, _, _, valley_path, peak_path in profiles:
            check_numeric_profile(valley_path, errors)
            check_numeric_profile(peak_path, errors)


def check_pvdr_inputs(errors: list[str]) -> None:
    """Check that included PVDR profiles can be read."""

    try:
        panels = find_pvdr_profiles(missing=[])
    except Exception as exc:  # noqa: BLE001
        errors.append(f"PVDR input discovery failed: {exc}")
        return

    profile_count = sum(len(profiles) for _, profiles in panels)
    if profile_count == 0:
        errors.append("No included PVDR profiles were found")
    for _, profiles in panels:
        for _, _, _, path in profiles:
            check_numeric_profile(path, errors)


def main() -> None:
    """Run the release input checks."""

    errors: list[str] = []
    check_required_public_files(errors)
    check_tracked_file_scope(errors)
    check_energy_color_mapping(errors)
    check_peak_pdd_inputs(errors)
    check_valley_pdd_inputs(errors)
    check_pvdr_inputs(errors)

    if errors:
        print("Release input check failed:")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
