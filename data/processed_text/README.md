# Processed Text Data

This folder contains small processed text outputs from the curated partial `PBP_paperdataset/FWHM5` subset. The subset represents PBP data with `bw = 0.5 mm`. These files are included to make the published CSV extraction auditable and to provide lightweight processed profiles that can support a future static GitHub Pages/GUI viewer.

These files are not raw Monte Carlo dose volumes. Large `.npy`, `.header`, `.mhd`, `.raw`, and related raw/intermediate simulation outputs are intentionally excluded from the public repository.

## Included File Types

- `FWHM_1Darray_ctc*_*.txt`: processed FWHM depth profiles for 1D minibeam arrays.
- `FWHM_2Darray_ctc*_*.txt`: processed FWHM depth profiles for selected 2D minibeam-array cases.
- `<energy>MeV/FWHM_singlebeam_*MeV.txt`: processed single-beam FWHM depth profiles.
- `<energy>MeV/FWHM_singleslit_*MeV.txt`: processed single-slit FWHM depth profiles where available in the curated subset.
- `<energy>MeV/PVDR_2Darray_*.txt`: processed PVDR depth profiles. These files store PVDR values only; peak and valley dose components are not stored in this text layer.
- `<energy>MeV/zpeak_*.txt`: processed peak-region depth-dose/profile text files saved by the legacy workflow.
- `dose_min_max_*dictionary*.txt`: JSON-style dictionaries of homogeneity and dose-threshold summary metrics.
- `dose_BEDR_1Darray_dictionary*.txt`: JSON-style BEDR-related threshold dictionaries. In the inspected subset these store threshold flags, not numeric BEDR values.
- `dictionaryforSOBP_*.txt`: processed SOBP helper dictionaries present in the curated subset. They are included for provenance, but the current public CSVs focus on the PBP/FWHM5 subset.

## Relationship to CSV Figure-Source Data

The primary public data products remain the tidy CSV files in `data/figure_source_data/`. The processed `.txt` files here are lower-level processed outputs used to audit or rebuild those CSVs. They are small enough for GitHub and suitable for future browser-based visualization, but they are not a complete replacement for the full private raw/intermediate Monte Carlo dataset.

To rebuild the CSVs from this public processed-text layer, run from the repository root:

```bash
python scripts/build_figure_source_data_from_legacy.py data/processed_text
```
