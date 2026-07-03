# Processed Text Data

This folder contains curated processed text files used by the public plotting scripts.

Peak PDD profiles for the PBP 1D MB array geometry use this pattern:

`PBP_dataset/FWHM*/<energy>MeV/zpeak_1Darray_ctc<ctc>_<energy>MeV.txt`

Valley PDD profiles for the PBP 1D MB array geometry use this pattern:

`PBP_dataset/FWHM*/<energy>MeV/zvalley_1Darray_ctc<ctc>_<energy>MeV.txt`

PVDR profiles for the PBP 1D MB array geometry use this pattern:

`PBP_dataset/FWHM*/<energy>MeV/PVDR_1Darray_ctc<ctc>_<energy>MeV.txt`

Each profile file stores one numeric value per line.

These files are not raw Monte Carlo dose volumes. If a requested processed profile is not included here, the plotting code skips that case and prints a message asking the user to contact the authors for those data.
