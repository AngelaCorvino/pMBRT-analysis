# Processed Text Data

This folder contains small processed text outputs from the curated partial `PBP_dataset/FWHM5` subset. The subset represents PBP data with `bw = 0.5 mm`. These files are the public numerical data layer for the repository and can support both the current reproduction scripts and a future static GitHub Pages/GUI viewer.

These files are not raw Monte Carlo dose volumes. Large `.npy`, `.header`, `.mhd`, `.raw`, and related raw/intermediate simulation outputs are intentionally excluded from the public repository.

## Included File Types

- `FWHM_1Darray_ctc*_*.txt`: processed FWHM depth profiles for 1D minibeam arrays.
- `FWHM_2Darray_ctc*_*.txt`: processed FWHM depth profiles for selected 2D minibeam-array cases.
- `<energy>MeV/FWHM_singlebeam_*MeV.txt`: processed single-beam FWHM depth profiles.
- `<energy>MeV/FWHM_singleslit_*MeV.txt`: processed single-slit FWHM depth profiles where available in the curated subset.
- `<energy>MeV/PVDR_2Darray_*.txt`: processed PVDR depth profiles. These files store PVDR values only; peak and valley dose components are not stored in this text layer.
- `<energy>MeV/zpeak_*.txt`: processed peak-region depth-dose/profile text files saved by the legacy workflow.
- `dose_min_max_*dictionary*.txt`: JSON-style dictionaries of homogeneity and dose-threshold summary metrics.
- `dose_BEDR_1Darray_dictionary*.txt`: JSON-style BEDR-related threshold dictionaries. In the inspected subset these store threshold flags, not numeric BEDR values.
- `dictionaryforSOBP_*.txt`: processed SOBP helper dictionaries present in the curated subset. They are included for provenance, but the current reproduction scripts focus on the PBP/FWHM5 subset.

## Relationship to Reproduction Scripts

The reproduction scripts read these processed text files directly. There is no published CSV conversion layer. This keeps the public numerical data aligned with the processed outputs from the legacy workflow and reduces the amount of derived data that must be manually checked before publication.
