# Future GUI/Data Plan

This repository is currently a curated analysis/data repository, not a finished GUI. The data layout is now chosen so a future static GitHub Pages viewer can be built without exposing raw Monte Carlo dose volumes.

## Public Data Layers

1. `data/figure_source_data/*.csv`

   Tidy, figure-level tables intended for direct reuse in scripts, notebooks, and manuscript figure reproduction. These are the preferred citation/replotting files.

2. `data/processed_text/PBP_paperdataset/FWHM5/`

   Small processed profile arrays and JSON-style dictionaries from the curated partial `bw = 0.5 mm` PBP subset. These can support browser-side visualization of processed FWHM, PVDR, and profile curves.

3. Excluded raw/intermediate simulation data

   `.npy`, `.header`, `.mhd`, `.raw`, `.bin`, `.root`, and raw TOPAS scoring outputs remain outside the public repository. A browser viewer should not depend on these files.

## Static Viewer Approach

A future GitHub Pages viewer should be a static application that reads CSV and processed text files from this repository. Recommended first features:

- filter by energy, beam width, ctc, and setup;
- plot FWHM versus depth or energy from `fig_fwhm_vs_energy.csv`;
- plot PVDR versus depth or ctc from `fig_pvdr_vs_depth_or_ctc.csv`;
- plot homogeneity pass/fail or summary metrics from `fig_homogeneity.csv` and `summary_metrics.csv`;
- optionally expose processed profile curves from `data/processed_text/` for users who want lower-level derived profiles.

## Publication Boundary

The GUI should present these data as processed, representative figure-source data from a partial curated subset. It should not claim to expose the full raw Monte Carlo workflow or complete manuscript simulation archive unless those data are later curated and added explicitly.
