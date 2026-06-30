# pMBRT Analysis

Curated public analysis repository for the manuscript:

**Monte Carlo-based characterization of proton minibeam radiation therapy across clinically relevant beam parameters**

This repository contains analysis scripts for post-processing and figure generation for the pMBRT Monte Carlo study, together with a small curated subset of processed `.txt` data used by those scripts. It is not the full raw Monte Carlo workflow and does not include large raw or intermediate dose arrays.

## Current Data Status

The legacy code was inspected to reconstruct the raw/source data formats and preprocessing workflow. The public data are small processed `.txt` outputs from the partial `PBP_dataset/FWHM5` subset. This subset represents PBP data with `bw = 0.5 mm` and includes processed FWHM text files, processed PVDR text files, processed peak-profile text files, and homogeneity/BEDR-related summary dictionaries.

No second numerical CSV layer is published. The reproduction scripts read the processed `.txt` files directly. Raw and intermediate dose arrays are not copied into this public repository. The reconstructed workflow and extraction decisions are documented in `docs/data_flow.md`.

## Repository Contents

- `data/processed_data/`: curated processed `.txt` arrays and dictionaries from the partial PBP/FWHM5 subset; these are not raw Monte Carlo dose volumes.
- `src/`: cleaned reusable helpers for loading processed text profiles, computing FWHM/PVDR/homogeneity/PDD utilities, and plotting.
- `scripts/`: reproduction scripts that read the processed `.txt` files directly.
- `figures/generated/`: output folder for regenerated figures and text summary tables.
- `topas/example_inputs/`: reserved for a future small non-private example input, if needed.

Large raw Monte Carlo outputs and private legacy workflow files are intentionally excluded. Full raw or intermediate outputs can be made available from the corresponding author upon reasonable request, if appropriate.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduce Figures and Tables

Run these commands from the repository root:

```bash
python scripts/reproduce_fwhm_vs_energy.py
python scripts/reproduce_pvdr_figure.py
python scripts/reproduce_homogeneity_figure.py
python scripts/reproduce_summary_table.py
```

Outputs are written to `figures/generated/`.

The current default figures are representative plots from the available partial processed-text dataset.

## Data Flow

The inspected legacy workflow uses 3D dose grids, usually `.npy` arrays with optional `.header` CSV sidecars. Preprocessing creates derived multi-beam dose grids, peak and valley depth profiles, FWHM text files, PVDR text files, and homogeneity summary dictionaries or `.npy` arrays depending on the script version. This repository publishes only the small processed `.txt` layer from the curated subset, not the raw/intermediate dose-volume layer.

See `docs/data_flow.md` for details.

## Citation

Citation metadata is provided in `CITATION.cff`. The Zenodo DOI is currently a placeholder and should be replaced after the archived release is created.

## License

A final license has not been selected yet. `LICENSE` is currently a placeholder and must be replaced with the chosen license text before publication.

## Manual Checks Before Public Release

- Confirm the included processed `.txt` files are the intended representative subset for public release.
- Replace the Zenodo DOI and release date placeholders in `CITATION.cff`.
- Choose and add a final license.
- Confirm no local paths, private comments, institutional/patient-related data, or large raw dose arrays are included.
- Confirm the reproduction commands generate the expected figures and text summary table.
