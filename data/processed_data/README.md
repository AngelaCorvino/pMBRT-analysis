# Processed Text Data

This folder contains processed PVDR text files used by the public plotting script.

These files are not raw Monte Carlo dose volumes. Large `.npy`, `.header`, `.mhd`, `.raw`, and related raw/intermediate simulation outputs are intentionally excluded from the public repository.

## Included File Pattern

`PBP_dataset/FWHM*/150MeV/PVDR_2Darray_ctc<ctc>_150MeV.txt`

The files store PVDR values only; peak and valley dose components are not stored in this text layer.

