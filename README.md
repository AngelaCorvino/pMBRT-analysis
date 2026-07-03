# pMBRT Analysis

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/AngelaCorvino/pMBRT-analysis/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/AngelaCorvino/pMBRT-analysis/tree/main)

Analysis code and processed profile data for the manuscript:

**Monte Carlo-based characterization of proton minibeam radiation therapy across clinically relevant beam parameters**

This repository provides organized plotting code for the processed pMBRT profiles used in the study. The public workflows plot peak PDD, valley PDD, and PVDR profiles from included processed text files.

## Install

Use Python 3.9 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate Plots

Run these commands from the repository root:

```bash
python scripts/plot_peak_pdd.py
python scripts/plot_valley_pdd.py
python scripts/plot_pvdr.py
```

Output is written to `figures/`.

To plot one beam width only, pass `--bw` in millimeters:

```bash
python scripts/plot_peak_pdd.py --bw 0.7
python scripts/plot_valley_pdd.py --bw 0.7
python scripts/plot_pvdr.py --bw 0.7
```

## Data

The processed data included in this public repository are under `data/processed_data/`.

- `PBP_dataset/`: processed pristine Bragg peak peak PDD, valley PDD, and PVDR profiles for the public plotting workflows.

The text files contain one numeric value per line. See `data/data_dictionary.md` for the available cases and filename conventions.

Raw Monte Carlo dose arrays are not included. If a processed case is not included in the public repository, the plotting code skips it and prints a message asking the user to contact the authors for those data.

## Citation

Citation metadata is provided in `CITATION.cff`.

## License

This repository is licensed under the MIT License. See `LICENSE` for details.
