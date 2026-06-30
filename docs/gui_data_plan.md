# Future GUI/Data Plan

This repository is currently a curated analysis/data repository, not a finished GUI. The data layout is chosen so a future static GitHub Pages viewer can be built without exposing raw Monte Carlo dose volumes or adding an additional derived CSV layer.

## Public Data Layer

`data/processed_data/PBP_dataset/FWHM5/`

This folder contains the public processed profile arrays and JSON-style dictionaries from the curated partial `bw = 0.5 mm` PBP subset. These files can support browser-side visualization of processed FWHM, PVDR, homogeneity, and profile curves.

## Excluded Data

`.npy`, `.header`, `.mhd`, `.raw`, `.bin`, `.root`, and raw TOPAS scoring outputs remain outside the public repository. A browser viewer should not depend on these files.

## Static Viewer Approach

A future GitHub Pages viewer should be a static application that reads the processed text files from this repository. Recommended first features:

- filter by energy, beam width, ctc, and setup;
- plot FWHM versus depth from `FWHM_singlebeam_*`, `FWHM_1Darray_ctc*`, and `FWHM_2Darray_ctc*` files;
- plot PVDR versus depth or ctc from `PVDR_2Darray_*` files;
- plot homogeneity pass/fail from `dose_min_max_*dictionary*.txt` files;
- expose processed peak profiles from `zpeak_*.txt` files where useful.

## Publication Boundary

The GUI should present these data as processed, representative text outputs from a partial curated subset. It should not claim to expose the full raw Monte Carlo workflow or complete manuscript simulation archive unless those data are later curated and added explicitly.
