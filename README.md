# pMBRT Analysis

Curated public analysis repository for the manuscript:

**Monte Carlo-based characterization of proton minibeam radiation therapy across clinically relevant beam parameters**

This repository contains analysis scripts for post-processing and figure generation for the pMBRT Monte Carlo study, together with curated processed `.txt` data used by those scripts. It is not the full raw Monte Carlo workflow and does not include large raw or intermediate dose arrays.

## Data

The public data are processed PVDR `.txt` profiles under `data/processed_data/PBP_dataset/FWHM*/150MeV/`.

No second numerical CSV layer is published. The plotting script reads the processed `.txt` files directly. Raw and intermediate dose arrays are not copied into this public repository. The reconstructed data flow is documented in `docs/data_flow.md`.

## Repository Contents

- `data/processed_data/`: processed PVDR `.txt` profiles used by the public plotting script; these are not raw Monte Carlo dose volumes.
- `src/plotting.py`: plotting and processed-text loading utilities used by the public figure script.
- `scripts/`: public figure-generation entry points.
- `figures/generated/`: output folder for generated figures.

Large raw Monte Carlo outputs and private legacy workflow files are intentionally excluded. Full raw or intermediate outputs can be made available from the corresponding author upon reasonable request, if appropriate.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate Figures

Run this command from the repository root:

```bash
python scripts/plot_pvdr_depth_profiles.py
```

Output is written to `figures/generated/`.

## Citation

Citation metadata is provided in `CITATION.cff`. The Zenodo DOI is currently a placeholder and should be replaced after the archived release is created.

## License

A final license has not been selected yet. `LICENSE` is currently a placeholder and must be replaced with the chosen license text before publication.

## Manual Checks Before Public Release

- Confirm the included processed `.txt` files are intended for public release.
- Replace the Zenodo DOI and release date placeholders in `CITATION.cff`.
- Choose and add a final license.
- Confirm no local paths, private comments, institutional/patient-related data, or large raw dose arrays are included.
- Confirm the public figure-generation command creates the expected figure.
