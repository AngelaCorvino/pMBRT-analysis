# Future GUI/Data Plan

This repository is currently a curated analysis/data repository, not a finished GUI. The data layout is chosen so a future static GitHub Pages viewer can be built without exposing raw Monte Carlo dose volumes or adding an additional derived CSV layer.

## Public Data Layer

`data/processed_data/PBP_dataset/FWHM*/150MeV/`

These folders contain the processed PVDR text profiles used by the public plotting script.

## Excluded Data

`.npy`, `.header`, `.mhd`, `.raw`, `.bin`, `.root`, raw TOPAS scoring outputs, and processed files not used by the public plotting script remain outside the public repository. A browser viewer should not depend on raw dose-volume files.

## Static Viewer Approach

A future GitHub Pages viewer can begin as a static application that reads the public PVDR text profiles and plots PVDR versus depth by beam width and ctc.

Additional processed profiles can be added later if they are selected for public release and documented in `data/data_dictionary.md`.
