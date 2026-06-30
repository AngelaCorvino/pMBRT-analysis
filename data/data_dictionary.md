# Data Dictionary

The public numerical data are processed `.txt` files under `data/processed_data/PBP_dataset/FWHM5/`. The files are derived processed outputs from the inspected analysis workflow, not raw Monte Carlo dose-volume arrays.

## Folder

`data/processed_data/PBP_dataset/FWHM5/`

The folder name `FWHM5` follows the legacy naming convention where `5` corresponds to `bw = 0.5 mm`.

## Files Used by the Public Plotting Script

| File pattern | Meaning | Notes |
|---|---|---|
| `<energy>MeV/PVDR_2Darray_ctc<ctc>_<energy>MeV.txt` | Processed PVDR values versus depth for 2D minibeam-array cases. | One numeric value per line. The script uses 1 mm depth spacing. `ctc10` corresponds to `ctc = 1.0 mm`. |

## Other Processed Text Files in the Curated Data Folder

| File pattern | Meaning |
|---|---|
| `FWHM_1Darray_ctc*_*.txt` | Processed FWHM values versus depth for 1D minibeam arrays. |
| `FWHM_2Darray_ctc*_*.txt` | Processed FWHM values versus depth for selected 2D minibeam-array cases. |
| `<energy>MeV/FWHM_singlebeam_*MeV.txt` | Processed single-beam FWHM values versus depth. |
| `<energy>MeV/FWHM_singleslit_*MeV.txt` | Processed single-slit FWHM values versus depth where available. |
| `<energy>MeV/PVDR_2Darray_*.txt` | Processed PVDR values versus depth. |
| `<energy>MeV/zpeak_*.txt` | Processed peak-region depth-dose/profile text outputs. |
| `dose_min_max_*dictionary*.txt` | JSON-style dictionaries of homogeneity and dose-threshold summary metrics. |
| `dose_BEDR_1Darray_dictionary*.txt` | JSON-style BEDR-related threshold dictionaries. In the inspected subset these store threshold flags, not numeric BEDR values. |
| `dictionaryforSOBP_*.txt` | Processed SOBP helper dictionaries present in the curated folder. |

## Dictionary Metric Fields

| Field | Meaning |
|---|---|
| `gamma` | Ratio recorded in the processed dictionary. |
| `min_dose` | Minimum normalized dose in the target region from the summary dictionary. |
| `max_dose` | Maximum normalized dose in the target region from the summary dictionary. |
| `D_BP>0.4D_entrance` | Binary dose-threshold flag from the homogeneity dictionaries. |
| `D_BP>0.6D_entrance` | Binary BEDR-related threshold flag from the BEDR dictionary. This is not a numeric BEDR value. |
| `homogeneity_at_BP` | Homogeneity code at the Bragg-peak/target depth. |
| `homogeneity_before_BP` | Homogeneity-before-target flag. |
