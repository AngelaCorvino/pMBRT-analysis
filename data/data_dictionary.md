# Data Dictionary

The public numerical data are processed `.txt` files under `data/processed_data/PBP_dataset/FWHM*/150MeV/`. The files are derived processed outputs from the analysis workflow, not raw Monte Carlo dose-volume arrays.

## Folder Pattern

`data/processed_data/PBP_dataset/FWHM*/150MeV/`

The folder name follows the legacy naming convention where `FWHM5` corresponds to `bw = 0.5 mm`, `FWHM7` corresponds to `bw = 0.7 mm`, and so on.

## Public Data Files

| File pattern | Meaning | Notes |
|---|---|---|
| `FWHM*/150MeV/PVDR_2Darray_ctc<ctc>_150MeV.txt` | Processed PVDR values versus depth for E = 150 MeV, grouped by beam width and center-to-center distance. | One numeric value per line. The plotting script uses 1 mm depth spacing. `ctc10` corresponds to `ctc = 1.0 mm`. |

## Currently Included Files

| File | Meaning |
|---|---|
| `FWHM5/150MeV/PVDR_2Darray_ctc10_150MeV.txt` | PVDR profile for `bw = 0.5 mm`, `ctc = 1.0 mm`. |
| `FWHM5/150MeV/PVDR_2Darray_ctc15_150MeV.txt` | PVDR profile for `bw = 0.5 mm`, `ctc = 1.5 mm`. |
| `FWHM5/150MeV/PVDR_2Darray_ctc20_150MeV.txt` | PVDR profile for `bw = 0.5 mm`, `ctc = 2.0 mm`. |

Additional beam-width folders can be added with the same filename pattern.

## Values

The public data files are one-dimensional text profiles. Each non-empty line contains one PVDR value sampled at the corresponding depth index.

For a line index `i`, the plotting script uses:

`depth_mm = i * 1 mm`

## Filename Terms

| Term | Meaning |
|---|---|
| `PVDR` | Peak-to-valley dose ratio. |
| `2Darray` | 2D minibeam-array setup label inherited from the processed output filename. |
| `ctc10`, `ctc15`, `ctc20` | Center-to-center distance labels corresponding to 1.0 mm, 1.5 mm, and 2.0 mm. |
| `150MeV` | Initial proton energy. |
