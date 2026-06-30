# Data Dictionary

The public numerical data are the processed `.txt` files under `data/processed_data/PBP_dataset/FWHM5/`. The subset represents PBP data with `bw = 0.5 mm`. The files are derived processed outputs from the inspected legacy workflow, not raw Monte Carlo dose-volume arrays.

## Folder

`data/processed_data/PBP_dataset/FWHM5/`

The folder name `FWHM5` follows the legacy naming convention where `5` corresponds to `bw = 0.5 mm`.

## Processed Profile Files

| File pattern | Meaning | Notes |
|---|---|---|
| `FWHM_1Darray_ctc*_*.txt` | Processed FWHM values versus depth for 1D minibeam arrays. | One numeric value per line. Reproduction scripts use the legacy 3 mm depth spacing. `ctc10` corresponds to `ctc = 1.0 mm`. |
| `FWHM_2Darray_ctc*_*.txt` | Processed FWHM values versus depth for selected 2D minibeam-array cases. | One numeric value per line. Reproduction scripts use the legacy 3 mm depth spacing. |
| `<energy>MeV/FWHM_singlebeam_*MeV.txt` | Processed single-beam FWHM values versus depth. | One numeric value per line. Reproduction scripts use the legacy 3 mm depth spacing. |
| `<energy>MeV/FWHM_singleslit_*MeV.txt` | Processed single-slit FWHM values versus depth where available. | Included for provenance; not currently used by the representative reproduction scripts. |
| `<energy>MeV/PVDR_2Darray_*.txt` | Processed PVDR values versus depth for 2D minibeam-array cases. | One numeric value per line. Peak and valley dose values are not stored in these files. Reproduction scripts use 1 mm depth spacing. |
| `<energy>MeV/zpeak_*.txt` | Processed peak-region depth-dose/profile text outputs saved by the legacy workflow. | Included as lightweight derived profiles for auditability and future visualization. |

## Summary Dictionary Files

The dictionary files are JSON-style text files with nested keys. The top-level key is the legacy beam-width label, the second-level key is energy in MeV, and the third-level key is ctc in millimeters.

| File pattern | Meaning | Notes |
|---|---|---|
| `dose_min_max_1Darray_dictionary.txt` | Homogeneity and dose-threshold metrics for 1D minibeam arrays. | Used by `scripts/reproduce_homogeneity_figure.py` and `scripts/reproduce_summary_table.py`. |
| `dose_min_max_2Darray_finalversion.txt` | Homogeneity and dose-threshold metrics for 2D minibeam arrays. | Used by `scripts/reproduce_homogeneity_figure.py`. |
| `dose_min_max_2Darray_dictionary.txt` | Earlier/alternate 2D homogeneity dictionary. | Included for provenance. |
| `dose_min_max_2Darray_dictionary_alongx.txt` | 2D-array homogeneity dictionary along x. | Included for provenance. |
| `dose_BEDR_1Darray_dictionary.txt` | BEDR-related threshold dictionary for 1D arrays. | Stores `D_BP>0.6D_entrance` flags in the inspected subset, not numeric BEDR values. |
| `dose_BEDR_1Darray_dictionary_filtered.txt` | Filtered BEDR-related threshold dictionary. | Included for provenance. |
| `dictionaryforSOBP_1Darray.txt` | Processed SOBP helper dictionary for 1D arrays. | Included for provenance. |
| `dictionaryforSOBP_2Darray.txt` | Processed SOBP helper dictionary for 2D arrays. | Included for provenance. |

## Dictionary Metric Fields

| Field | Meaning |
|---|---|
| `gamma` | Ratio recorded in the legacy dictionary. |
| `min_dose` | Minimum normalized dose in the target region from the legacy summary dictionary. |
| `max_dose` | Maximum normalized dose in the target region from the legacy summary dictionary. |
| `D_BP>0.4D_entrance` | Binary dose-threshold flag from the legacy homogeneity dictionaries. |
| `D_BP>0.6D_entrance` | Binary BEDR-related threshold flag from the legacy BEDR dictionary. This is not a numeric BEDR value. |
| `homogeneity_at_BP` | Legacy homogeneity code at the Bragg-peak/target depth. |
| `homogeneity_before_BP` | Legacy homogeneity-before-target flag. |
