# pMBRT Analysis

Curated public analysis scaffold for the manuscript:

**Monte Carlo-based characterization of proton minibeam radiation therapy across clinically relevant beam parameters**

This repository is intended to contain processed figure-source data and lightweight analysis scripts that allow readers to replot representative manuscript figures and tables. It is not the full raw Monte Carlo workflow and does not include large raw or intermediate dose arrays.

## Current Data Status

The legacy code was inspected to reconstruct the raw/source data formats and preprocessing workflow. The CSV files in `data/figure_source_data/` have been populated from a small partial legacy dataset: the `PBP_paperdataset/FWHM5` subset. This subset represents `bw = 0.5 mm` and includes processed FWHM text files, processed PVDR text files, processed peak-profile text files, and homogeneity/BEDR-related summary dictionaries.

Small processed `.txt` outputs from this curated subset are included under `data/processed_text/` so the CSV extraction is auditable and the data can support a future static GitHub Pages/GUI viewer. Raw and intermediate dose arrays are not copied into this public repository. The reconstructed workflow and extraction decisions are documented in `docs/data_flow.md`.

## Repository Contents

- `data/figure_source_data/`: tidy CSV files for representative FWHM, PVDR, homogeneity, and summary metrics.
- `data/processed_text/`: small processed `.txt` arrays and dictionaries from the curated partial subset; these are not raw Monte Carlo dose volumes.
- `src/`: cleaned reusable helpers for loading profiles, computing FWHM, PVDR, homogeneity, PDD utilities, and plotting.
- `scripts/`: reproduction scripts that read only the processed CSV files.
- `scripts/build_figure_source_data_from_legacy.py`: optional extraction script for rebuilding the CSVs from `data/processed_text/` or from a private legacy subset supplied as a command-line argument.
- `figures/generated/`: output folder for regenerated figures and tables.
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

The figure-source CSVs can also be rebuilt from the included processed text layer:

```bash
python scripts/build_figure_source_data_from_legacy.py data/processed_text
```

If a CSV has only headers, the corresponding script stops with a clear message rather than generating a placeholder figure.

The current default figures are representative plots from the available partial dataset. The CSVs contain more rows than the default plots use.

## Data Flow

The inspected legacy workflow uses 3D dose grids, usually `.npy` arrays with optional `.header` CSV sidecars. Preprocessing creates derived multi-beam dose grids, peak and valley depth profiles, FWHM text files, PVDR text files, and homogeneity summary dictionaries or `.npy` arrays depending on the script version. The public repository publishes the processed CSV layer and a small processed-text provenance layer, not the full raw/intermediate dose-volume layer.

See `docs/data_flow.md` for details.

## Citation

Citation metadata is provided in `CITATION.cff`. The Zenodo DOI is currently a placeholder and should be replaced after the archived release is created.

## License

A final license has not been selected yet. Replace `LICENSE_PLACEHOLDER.txt` with the chosen license before publication.

## Manual Checks Before Public Release

- Confirm the partial processed CSV values and included processed `.txt` files are the intended representative subset for public release.
- Replace the Zenodo DOI and repository URL placeholders in `CITATION.cff`.
- Choose and add a final license.
- Confirm no local paths, private comments, institutional/patient-related data, or large raw dose arrays are included.
- Confirm the reproduction commands generate the expected figures and table.
