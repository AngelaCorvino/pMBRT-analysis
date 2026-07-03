# Data Dictionary

The public numerical data are processed `.txt` files under `data/processed_data/`. These files are processed profile data used by the public plotting scripts, not raw Monte Carlo dose-volume arrays.

## Folder Patterns

`data/processed_data/PBP_dataset/FWHM*/<energy>MeV/`

The folder name follows the dataset naming convention where `FWHM5` corresponds to `bw = 0.5 mm`, `FWHM7` corresponds to `bw = 0.7 mm`, and so on.

## Public Data Files

| File pattern | Meaning | Public workflow |
|---|---|---|
| `PBP_dataset/FWHM*/<energy>MeV/zpeak_1Darray_ctc<ctc>_<energy>MeV.txt` | Processed peak depth-dose values for the PBP 1D MB array geometry. One numeric value per line. | Peak PDD plotting and valley PDD normalization |
| `PBP_dataset/FWHM*/<energy>MeV/zvalley_1Darray_ctc<ctc>_<energy>MeV.txt` | Processed valley depth-dose values for the PBP 1D MB array geometry. One numeric value per line. | Valley PDD plotting |
| `PBP_dataset/FWHM*/<energy>MeV/PVDR_1Darray_ctc<ctc>_<energy>MeV.txt` | Processed peak-to-valley dose ratio for the PBP 1D MB array geometry. One numeric value per line. | PVDR plotting |

## PDD Cases

The public peak-PDD and valley-PDD scripts follow the pMBRT `plot_PDD_MB.py` case convention:

- energies: 50, 125, 175, and 230 MeV
- ctc values: `3 x bw` and `5 x bw`

All public plotting scripts use the same energy color convention: 50 MeV is light blue, 125 MeV is green, 175 MeV is red, and 230 MeV is orange.

The public PDD plotting code can use processed files for `FWHM5`, `FWHM7`, `FWHM10`, `FWHM12`, `FWHM15`, and `FWHM20` when those files are included.

Valley PDD profiles are normalized by the maximum of the matching peak PDD profile. If a requested processed case is not included, the plotting code skips it and prints a message asking the user to contact the authors for those data.

## PVDR Cases

| Case | Energy [MeV] | bw [mm] | ctc [mm] | Folder and ctc label |
|---|---:|---:|---:|---|
| a | 50 | 0.5 | 1.5, 2.0 | `FWHM5`, `ctc15`, `ctc20` |
| b | 125 | 1.2 | 4.8, 6.0 | `FWHM12`, `ctc48`, `ctc60` |
| b | 175 | 1.2 | 4.8, 6.0 | `FWHM12`, `ctc48`, `ctc60` |
| c | 50 | 0.7 | 2.1, 2.8 | `FWHM7`, `ctc21`, `ctc28` |
| c | 125 | 0.7 | 2.8, 3.5 | `FWHM7`, `ctc28`, `ctc35` |
| d | 175 | 1.5 | 6.0, 7.5 | `FWHM15`, `ctc60`, `ctc75` |
| d | 230 | 1.5 | 6.0, 7.5 | `FWHM15`, `ctc60`, `ctc75` |
| e | 125 | 1.0 | 4.0, 5.0 | `FWHM10`, `ctc40`, `ctc50` |
| e | 175 | 1.0 | 4.0, 5.0 | `FWHM10`, `ctc40`, `ctc50` |
| f | 230 | 2.0 | 8.0, 10.0 | `FWHM20`, `ctc80`, `ctc100` |

## Values

Each non-empty line contains one value sampled at the corresponding depth index.

For a line index `i`, the plotting scripts use:

`depth_mm = i * 1 mm`

Peak PDD profiles are normalized by their own maximum. Valley PDD profiles are normalized by the maximum of the matching peak profile. PVDR profiles are plotted directly on a logarithmic y-axis.

## Filename Terms

| Term | Meaning |
|---|---|
| `zpeak` | Peak-region depth-dose profile. |
| `zvalley` | Valley-region depth-dose profile. |
| `PVDR` | Peak-to-valley dose ratio. |
| `1Darray` | 1D MB array geometry. |
| `ctc10`, `ctc15`, `ctc20` | Center-to-center distance labels corresponding to 1.0 mm, 1.5 mm, and 2.0 mm. |
| `<energy>MeV` | Initial proton energy. |
