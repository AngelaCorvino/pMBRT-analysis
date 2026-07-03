# Processed Text Data

This folder contains curated processed text files used by the public plotting scripts.

For Figure 1, the required files are peak depth-dose profiles for the PBP 1D MB array geometry:

`PBP_dataset/FWHM*/<energy>MeV/zpeak_1Darray_ctc<ctc>_<energy>MeV.txt`

For Figure 2, the required files are valley depth-dose profiles and matching peak profiles for the PBP 1D MB array geometry:

`PBP_dataset/FWHM*/<energy>MeV/zvalley_1Darray_ctc<ctc>_<energy>MeV.txt`

`PBP_dataset/FWHM*/<energy>MeV/zpeak_1Darray_ctc<ctc>_<energy>MeV.txt`

For Supplementary Figure S5, the required files are processed PVDR profiles for the PBP 1D MB array geometry:

`PBP_dataset/FWHM*/<energy>MeV/PVDR_1Darray_ctc<ctc>_<energy>MeV.txt`

Each profile file stores one numeric value per line.

These files are not raw Monte Carlo dose volumes.
