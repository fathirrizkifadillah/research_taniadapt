# Phase 4 Dataset Quality Audit Report: DS04 — Indonesia Nationwide Agroclimatic Dataset
**TaniAdapt Project — National Agroclimatic Benchmark & Derived Indicators**

---

## 1. Provenance & License
- **Title:** Indonesia Nationwide Agroclimatic Dataset (2016–2025)
- **Publisher / Repository:** Mendeley Data / Elsevier (DOI: [10.17632/3pfbdbzfff.1](https://doi.org/10.17632/3pfbdbzfff.1))
- **Underlying Source:** Open-Meteo Historical Weather / ERA5-Seamless
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

## 2. File Integrity & Contents
- **Total Files Acquired:** 18 files (Parquet + CSV + Python reproduction code, ~85 MB total, SHA-256 verified)
- **Key Tables:**
  - `grid_points.csv`: 612 terrestrial grid points across Indonesian archipelago
  - `indicator_definitions.csv`: 12 agroclimatic indicator definitions (GDD, CDD, CWD, RX1day, RX5day, R10mm, R20mm, SU, TR, etc.)
  - `agroclimate_qc.parquet` (15.5 MB) & `agroclimate_with_indicators.parquet` (60.0 MB)
- **Encoding Note:** `indicator_definitions.csv` contains Windows-1252 / Latin-1 degree symbols; requires explicit encoding parameter.

## 3. Spatial & Temporal Coverage
- **Spatial Resolution:** 0.5° grid (~50 km at equator)
- **Temporal Coverage:** 2016-01-01 to 2025-12-31 (10 years daily data)
- **West Java Grid Intersect:** 23 grid points fall within the West Java bounding box.

## 4. Audit Disposition & Agricultural Role
- **Audit Disposition:** `PASS (AGROCLIMATE_BENCHMARK)`
- **Key Value:** Provides standardized definitions and benchmark values for extreme climate indices (CDD, CWD, GDD) across Indonesia.
- **Limitations:** Derives from ERA5-Seamless (not an independent station validation of AgERA5). 0.5° resolution is significantly coarser than AgERA5's native 0.1° grid.