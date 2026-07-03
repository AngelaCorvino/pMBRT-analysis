# Data Dictionary

The public numerical data are processed `.txt` files under `data/processed_data/`. These files are the figure-source data used by the public plotting scripts, not raw Monte Carlo dose-volume arrays.

## Folder Patterns

`data/processed_data/PBP_dataset/FWHM*/<energy>MeV/`

The folder name follows the dataset naming convention where `FWHM5` corresponds to `bw = 0.5 mm`, `FWHM7` corresponds to `bw = 0.7 mm`, and so on.

## Public Data Files

| File pattern | Meaning | Figure |
|---|---|---|
| `PBP_dataset/FWHM*/<energy>MeV/zpeak_1Darray_ctc<ctc>_<energy>MeV.txt` | Processed peak depth-dose values for the PBP 1D MB array geometry. One numeric value per line. | Figure 1 and Figure 2 normalization |
| `PBP_dataset/FWHM*/<energy>MeV/zvalley_1Darray_ctc<ctc>_<energy>MeV.txt` | Processed valley depth-dose values for the PBP 1D MB array geometry. One numeric value per line. | Figure 2 |
| `PBP_dataset/FWHM*/<energy>MeV/PVDR_1Darray_ctc<ctc>_<energy>MeV.txt` | Processed peak-to-valley dose ratio for the PBP 1D MB array geometry. One numeric value per line. | Supplementary Figure S5 |

## Figure 1 and Figure 2 PBP Cases

The public Figure 1 and Figure 2 scripts follow the pMBRT `plot_PDD_MB.py` case convention:

- energies: 50, 125, 175, and 230 MeV
- ctc values: `3 x bw` and `5 x bw`

Figure 1 uses peak PDD cases for `FWHM5`, `FWHM10`, `FWHM12`, `FWHM15`, and `FWHM20`.

Figure 2 uses valley PDD cases for `FWHM5`, `FWHM7`, `FWHM10`, `FWHM12`, `FWHM15`, and `FWHM20`, plus matching peak profiles for normalization.

## Supplementary Figure S5 PVDR Cases

| Panel | Energy [MeV] | bw [mm] | ctc [mm] | Folder and ctc label |
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

Figure 1 normalizes each peak profile by its own maximum. Figure 2 normalizes each valley profile by the maximum of the matching peak profile. Supplementary Figure S5 plots the supplied PVDR values directly on a logarithmic y-axis.

## Filename Terms

| Term | Meaning |
|---|---|
| `zpeak` | Peak-region depth-dose profile. |
| `zvalley` | Valley-region depth-dose profile. |
| `PVDR` | Peak-to-valley dose ratio. |
| `1Darray` | 1D MB array geometry. |
| `ctc10`, `ctc15`, `ctc20` | Center-to-center distance labels corresponding to 1.0 mm, 1.5 mm, and 2.0 mm. |
| `<energy>MeV` | Initial proton energy. |
