"""Check that the public release inputs are complete and scoped."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "figures" / "generated" / ".mplconfig"))
sys.path.insert(0, str(ROOT / "src"))

from plotting import (  # noqa: E402
    FIGURE5_CASES,
    figure5_profile_paths,
    find_figure1_peak_profiles,
    find_figure2_valley_profiles,
    read_numeric_series,
)


REQUIRED_PUBLIC_FILES = (
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "requirements.txt",
    "src/plotting.py",
    "scripts/plot_figure1_peak_depth_profiles.py",
    "scripts/plot_figure2_valley_depth_profiles.py",
    "scripts/plot_figure5_sobp_depth_profiles.py",
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


def check_numeric_profile(path: Path, errors: list[str]) -> None:
    """Check that one processed profile can be read as numeric text data."""

    try:
        read_numeric_series(path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Invalid processed profile {display(path)}: {exc}")


def check_figure1_inputs(errors: list[str]) -> None:
    """Check that Figure 1 peak profiles are available."""

    try:
        groups = find_figure1_peak_profiles()
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Figure 1 input discovery failed: {exc}")
        return

    profile_count = sum(len(profiles) for _, profiles in groups)
    if len(groups) != 5 or profile_count != 40:
        errors.append(f"Figure 1 expected 5 beam-width groups and 40 profiles, found {len(groups)} groups and {profile_count} profiles")
    for _, profiles in groups:
        for _, _, _, path in profiles:
            check_numeric_profile(path, errors)


def check_figure2_inputs(errors: list[str]) -> None:
    """Check that Figure 2 valley profiles and matching peaks are available."""

    try:
        groups = find_figure2_valley_profiles()
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Figure 2 input discovery failed: {exc}")
        return

    profile_count = sum(len(profiles) for _, profiles in groups)
    if len(groups) != 6 or profile_count != 48:
        errors.append(f"Figure 2 expected 6 beam-width groups and 48 profiles, found {len(groups)} groups and {profile_count} profiles")
    for _, profiles in groups:
        for _, _, _, valley_path, peak_path in profiles:
            check_numeric_profile(valley_path, errors)
            check_numeric_profile(peak_path, errors)


def check_figure5_inputs(errors: list[str]) -> None:
    """Check that Figure 5 SOBP panel profiles are available."""

    if len(FIGURE5_CASES) != 10:
        errors.append(f"Figure 5 expected 10 panel cases, found {len(FIGURE5_CASES)}")

    for case in FIGURE5_CASES:
        try:
            paths = figure5_profile_paths(case)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Figure 5 panel {case.get('panel', '?')} input discovery failed: {exc}")
            continue
        for path in paths.values():
            check_numeric_profile(path, errors)


def main() -> None:
    """Run the release input checks."""

    errors: list[str] = []
    check_required_public_files(errors)
    check_tracked_file_scope(errors)
    check_figure1_inputs(errors)
    check_figure2_inputs(errors)
    check_figure5_inputs(errors)

    if errors:
        print("Release input check failed:")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
