# Processed Text Data

This folder contains processed text outputs from `PBP_dataset/FWHM5`. The folder represents PBP data with `bw = 0.5 mm`. These files are the public numerical data layer for the repository and can support the public plotting script and future visualization tools.

These files are not raw Monte Carlo dose volumes. Large `.npy`, `.header`, `.mhd`, `.raw`, and related raw/intermediate simulation outputs are intentionally excluded from the public repository.

## Included File Types

- `FWHM_1Darray_ctc*_*.txt`: processed FWHM depth profiles for 1D minibeam arrays.
- `FWHM_2Darray_ctc*_*.txt`: processed FWHM depth profiles for selected 2D minibeam-array cases.
- `<energy>MeV/FWHM_singlebeam_*MeV.txt`: processed single-beam FWHM depth profiles.
- `<energy>MeV/FWHM_singleslit_*MeV.txt`: processed single-slit FWHM depth profiles where available in the curated folder.
- `<energy>MeV/PVDR_2Darray_*.txt`: processed PVDR depth profiles. These files store PVDR values only; peak and valley dose components are not stored in this text layer.
- `<energy>MeV/zpeak_*.txt`: processed peak-region depth-dose/profile text files.
- `dose_min_max_*dictionary*.txt`: JSON-style dictionaries of homogeneity and dose-threshold summary metrics.
- `dose_BEDR_1Darray_dictionary*.txt`: JSON-style BEDR-related threshold dictionaries. In the inspected folder these store threshold flags, not numeric BEDR values.
- `dictionaryforSOBP_*.txt`: processed SOBP helper dictionaries present in the curated folder.

## Relationship to Public Plotting Code

The public plotting script reads processed text files directly. There is no published CSV conversion layer.
