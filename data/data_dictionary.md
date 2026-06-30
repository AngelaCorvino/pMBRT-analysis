# Data Dictionary

The CSV files in `data/figure_source_data/` use long/tidy format. Each row represents one plotted observation or one summary row. The current CSVs were extracted from the available partial `PBP_paperdataset/FWHM5` legacy subset, representing `bw = 0.5 mm` PBP data.

## Common Columns

| Column | Meaning |
|---|---|
| `figure` | Manuscript figure identifier or repository figure identifier. |
| `panel` | Figure panel identifier. |
| `setup` | Beam/setup label, for example PBP/SOBP or 1D/2D minibeam arrangement. |
| `source_type` | Source category, for example single beam, 1D grid, or 2D grid. |
| `energy_MeV` | Proton beam energy in MeV. |
| `bw_mm` | Beam width in millimeters. |
| `ctc_mm` | Center-to-center distance in millimeters. |
| `depth_mm` | Depth in millimeters. |
| `depth_cm` | Depth in centimeters. |
| `target_depth_mm` | Target or Bragg-peak depth in millimeters. |
| `target_depth_cm` | Target or Bragg-peak depth in centimeters. |
| `source_file` | Legacy processed file used to extract the value. Use a relative, non-private provenance label. |
| `source_files` | Semicolon-separated list of source files for summary rows. Use relative, non-private provenance labels. |
| `notes` | Short non-private notes about extraction or filtering. |
| `homogeneity_code` | Original `homogeneity_at_BP` value from the legacy summary dictionaries. |
| `homogeneity_before_target_flag` | Original `homogeneity_before_BP` value from the legacy summary dictionaries. |
| `min_normalized_dose` | Minimum normalized dose in the target region from the legacy summary dictionary. |
| `max_normalized_dose` | Maximum normalized dose in the target region from the legacy summary dictionary. |
| `gamma` | Ratio recorded in the legacy summary dictionary. |
| `dose_threshold_flag` | Original `D_BP>0.4D_entrance` flag from the legacy summary dictionary. |
| `BEDR_threshold_flag` | Original `D_BP>0.6D_entrance` flag from the BEDR-related dictionary, where available. |

## `fig_fwhm_vs_energy.csv`

Processed FWHM values used to replot representative FWHM curves.

| Column | Meaning |
|---|---|
| `figure` | Figure identifier. |
| `panel` | Panel identifier. |
| `setup` | Simulation setup or beam arrangement. |
| `source_type` | Single beam, 1D grid, or 2D grid. |
| `energy_MeV` | Proton energy in MeV. |
| `bw_mm` | Beam width in millimeters. |
| `ctc_mm` | Center-to-center distance in millimeters; blank for single-beam rows if not applicable. |
| `depth_mm` | Depth coordinate corresponding to the fitted lateral profile. |
| `depth_cm` | Same depth coordinate converted to centimeters. |
| `FWHM_mm` | Fitted full width at half maximum in millimeters. |
| `source_file` | Processed FWHM text file used for extraction. |
| `notes` | Non-private extraction notes. |

## `fig_pvdr_vs_depth_or_ctc.csv`

Processed peak/valley and PVDR values used to replot representative PVDR curves.

| Column | Meaning |
|---|---|
| `figure` | Figure identifier. |
| `panel` | Panel identifier. |
| `setup` | Simulation setup or beam arrangement. |
| `energy_MeV` | Proton energy in MeV. |
| `bw_mm` | Beam width in millimeters. |
| `ctc_mm` | Center-to-center distance in millimeters. |
| `depth_mm` | Depth coordinate in millimeters. |
| `depth_cm` | Depth coordinate in centimeters. |
| `peak_dose_Gy` | Dose sampled in the peak region, in Gy if the source grid is calibrated in Gy. |
| `valley_dose_Gy` | Dose sampled in the valley region, in Gy if the source grid is calibrated in Gy. |
| `PVDR` | Peak-to-valley dose ratio, computed as `peak_dose_Gy / valley_dose_Gy` with zero-valley handling. |
| `source_file` | Processed or derived source file used for extraction. |
| `notes` | Non-private extraction notes. |

In the current partial subset, this CSV was populated from processed `PVDR_2Darray_*` text files that contain PVDR values only. Therefore `peak_dose_Gy` and `valley_dose_Gy` are blank in those rows.

## `fig_homogeneity.csv`

Processed homogeneity results used to replot representative homogeneity maps or scatter plots.

| Column | Meaning |
|---|---|
| `figure` | Figure identifier. |
| `panel` | Panel identifier. |
| `setup` | Simulation setup or beam arrangement. |
| `homogeneity_dimension` | `x`, `y`, `xy`, or `std`, depending on the source metric. |
| `energy_MeV` | Proton energy in MeV. |
| `bw_mm` | Beam width in millimeters. |
| `ctc_mm` | Center-to-center distance in millimeters. |
| `target_depth_mm` | Depth used for the pass/fail or standard-deviation metric. |
| `target_depth_cm` | Same depth converted to centimeters. |
| `homogeneous_flag` | `1` if the criterion passed, `0` if it failed. |
| `homogeneity_code` | Original `homogeneity_at_BP` value from the legacy dictionary. `homogeneous_flag` is `1` when this code is greater than zero. |
| `homogeneity_before_target_flag` | Original `homogeneity_before_BP` value from the legacy dictionary. |
| `relative_std_at_target` | Standard deviation divided by mean dose at the target depth, where available. |
| `min_normalized_dose` | Minimum normalized dose in the target region from the legacy dictionary. |
| `max_normalized_dose` | Maximum normalized dose in the target region from the legacy dictionary. |
| `gamma` | Ratio recorded in the legacy dictionary. |
| `criterion` | Text description of the criterion, for example `0.95 < normalized dose < 1.07`. |
| `dose_threshold_flag` | Original `D_BP>0.4D_entrance` flag. |
| `source_file` | Homogeneity dictionary or standard-deviation source file used for extraction. |
| `notes` | Non-private extraction notes. |

## `summary_metrics.csv`

Curated row-level summary metrics for representative setups.

| Column | Meaning |
|---|---|
| `setup` | Simulation setup or beam arrangement. |
| `energy_MeV` | Proton energy in MeV. |
| `bw_mm` | Beam width in millimeters. |
| `ctc_mm` | Center-to-center distance in millimeters. |
| `target_depth_mm` | Target or Bragg-peak depth in millimeters. |
| `target_depth_cm` | Target or Bragg-peak depth in centimeters. |
| `PVDR_target` | PVDR at the target depth. |
| `PVDR_entrance` | Entrance-region PVDR, if defined for the selected summary. |
| `BEDR` | BEDR value after the manuscript formula is supplied. No BEDR formula was found in the inspected scripts. |
| `BEDR_threshold_flag` | Binary `D_BP>0.6D_entrance` flag from the available BEDR-related dictionary; this is not a numeric BEDR value. |
| `FWHM_entrance_mm` | Fitted FWHM near entrance depth in millimeters. |
| `FWHM_target_mm` | Fitted FWHM at target or Bragg-peak depth in millimeters. |
| `target_homogeneity` | Homogeneity pass/fail or summary label at target depth. |
| `homogeneity_code` | Original `homogeneity_at_BP` value from the legacy dictionary. |
| `relative_std_at_target` | Standard deviation divided by mean dose at target depth, where available. |
| `source_files` | Semicolon-separated provenance labels for processed source files. |
| `notes` | Non-private extraction notes. |

## `data/processed_text/`

This folder contains small processed `.txt` files from the curated partial `PBP_paperdataset/FWHM5` subset. These files are included for provenance, auditability, and future static visualization. They are not raw Monte Carlo dose volumes.

| File pattern | Meaning | Notes |
|---|---|---|
| `FWHM_1Darray_ctc*_*.txt` | Processed FWHM values versus depth for 1D minibeam arrays. | One numeric value per line. The CSV extraction uses 3 mm depth spacing to match the legacy plotting workflow. |
| `FWHM_2Darray_ctc*_*.txt` | Processed FWHM values versus depth for selected 2D minibeam-array cases. | One numeric value per line. |
| `<energy>MeV/FWHM_singlebeam_*MeV.txt` | Processed single-beam FWHM values versus depth. | One numeric value per line. |
| `<energy>MeV/FWHM_singleslit_*MeV.txt` | Processed single-slit FWHM values versus depth where available. | Included for provenance; not currently used by the representative reproduction scripts. |
| `<energy>MeV/PVDR_2Darray_*.txt` | Processed PVDR values versus depth for 2D minibeam-array cases. | One numeric value per line. Peak and valley dose values are not stored in these files. The CSV extraction uses 1 mm depth spacing. |
| `<energy>MeV/zpeak_*.txt` | Processed peak-region depth-dose/profile text outputs saved by the legacy workflow. | Included as lightweight derived profiles for auditability and future visualization. |
| `dose_min_max_*dictionary*.txt` | JSON-style dictionaries of homogeneity and dose-threshold metrics. | Used to populate homogeneity and summary CSV files. |
| `dose_BEDR_1Darray_dictionary*.txt` | JSON-style BEDR-related threshold dictionaries. | Stores threshold flags in the inspected subset, not numeric BEDR values. |
| `dictionaryforSOBP_*.txt` | Processed SOBP helper dictionaries present in the curated subset. | Included for provenance; current public CSVs focus on the PBP/FWHM5 subset. |
