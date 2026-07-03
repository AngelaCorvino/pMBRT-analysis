# pMBRT Analysis

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/AngelaCorvino/pMBRT-analysis/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/AngelaCorvino/pMBRT-analysis/tree/main)

Analysis code and processed figure data for the manuscript:

**Monte Carlo-based characterization of proton minibeam radiation therapy across clinically relevant beam parameters**

This repository reproduces manuscript Figures 1 and 2, plus Supplementary Figure S5, from the included processed text profiles.

## Install

Use Python 3.9 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate Figures 1, 2, and S5

Run these commands from the repository root:

```bash
python scripts/plot_figure1_peak_depth_profiles.py
python scripts/plot_figure2_valley_depth_profiles.py
python scripts/plot_figure_s5_pvdr_depth_profiles.py
```

Output is written to `figures/`.

## Data

The data needed by the figure scripts are included under `data/processed_data/`.

- `PBP_dataset/`: processed pristine Bragg peak profiles for Figures 1 and 2, plus processed PVDR profiles for Supplementary Figure S5.

The text files contain one numeric value per line. See `data/data_dictionary.md` for the figure cases and filename conventions.

Raw Monte Carlo dose arrays are not included.

## Citation

Citation metadata is provided in `CITATION.cff`.

## License

This repository is licensed under the MIT License. See `LICENSE` for details.
