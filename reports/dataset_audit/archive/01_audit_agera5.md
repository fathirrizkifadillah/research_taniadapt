# Phase 4 Dataset Quality Audit Report: DS01 — AgERA5 Time-Series
**TaniAdapt Project — Primary Weather & Agroclimatic Backbone**

---

## 1. Provenance & License
- **Authoritative Title:** Agrometeorological indicators time-series from 1979 to present derived from reanalysis (AgERA5 v2.0)
- **Publisher:** Copernicus Climate Change Service (C3S) / ECMWF
- **Product Landing Page:** [Copernicus CDS AgERA5 Time-Series](https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries)
- **API Endpoint:** `https://cds.climate.copernicus.eu/api/retrieve/v1/processes/sis-agrometeorological-indicators-timeseries`
- **License / Terms:** Copernicus Open Access Licence (free for commercial and research use with attribution)
- **Methodology:** Atmospheric reanalysis (ERA5 surface variables downscaled and bias-adjusted to 0.1° grid using agrometeorological corrections)

## 2. File Integrity & Format
- **Acquired Locations (West Java):** 7 Locations — Bandung, Karawang, Tasikmalaya, Sukabumi, Cirebon, Purwakarta, Bekasi
- **Primary Period Acquired:** 2015-01-01 to 2024-12-31 (10 consecutive calendar years, 3,653 daily timestamps per location)
- **Pilot Test:** 2023 calendar year (365 days) and 2024 pilot
- **Format:** Native CSV format returned directly by CDS OpenAPI process
- **File Integrity:** Valid parsing across all 7 CSV files; non-zero file sizes (~1.0 MB per location); no corrupted or truncated lines.

## 3. Schema & Variables (24 Agricultural Variables)
All 24 agriculturally relevant variables cataloged in `reports/dataset_discovery/agera5_variable_inventory.csv` are present:
- **Thermal:** `Temperature_Air_2m_Mean_24h`, `Max_24h`, `Min_24h`, `Max_Day_Time`, `Mean_Day_Time`, `Mean_Night_Time`, `Min_Night_Time`, `Dew_Point_Temperature_2m_Mean_24h`
- **Hydrological:** `Precipitation_Flux` (mm/day), `Precipitation_Duration_Fraction`, `Precipitation_Rain_Duration_Fraction`
- **Humidity & Pressure:** `Derived_Relative_Humidity_2m_Max_24h`, `Min_24h`, `Relative_Humidity_2m_06h`, `09h`, `12h`, `15h`, `18h`, `Vapour_Pressure_Mean_24h`, `Vapour_Pressure_Deficit_at_Maximum_Temperature`
- **Radiation & Evapotranspiration:** `Solar_Radiation_Flux` (J/m²/day), `Cloud_Cover_Mean_24h`, `ReferenceET_PenmanMonteith_FAO56` (mm/day)
- **Wind:** `Wind_Speed_10m_Mean_24h` (m/s)

## 4. Completeness & Missing Values
- **Missing Value Count:** 0 null values across all 3,653 days and 24 variables for all 7 locations.
- **Completeness:** 100.0% temporal continuity with daily granularity.

## 5. Value Plausibility & Physical Bounds
- **Tmin ≤ Tmean ≤ Tmax:** Verified 100% valid.
- **Precipitation Non-negativity:** Minimum precipitation = 0.00 mm; no negative fluxes.
- **Relative Humidity Bounds:** Min RH ≥ 0.0%, Max RH ≤ 100.0%.
- **Vapour Pressure Deficit (VPD):** Values non-negative; ranges from 0 to ~25 hPa during dry spells.
- **Wind Speed:** All values non-negative (0.2 m/s to 6.8 m/s).

## 6. Spatial Alignment & Proxy Handling
- The requested coordinates represent administrative centroid proxies for West Java regencies/cities.
- AgERA5 maps these proxies to the nearest 0.1° terrestrial grid cell center (e.g. Bandung proxy (-6.91, 107.61) mapped to (-6.90, 107.60)).
- Note: Coordinates are administrative proxies, not field-verified farm points.

## 7. Data-Fusion Feasibility & Role
- **Fit for TaniAdapt:** Ideal primary daily weather backbone for linking with crop calendars, calculating lag windows (1–14 days), rolling rainfall, consecutive wet/dry days, and thermal time (GDD).
- **Audit Disposition:** `PASS`
- **Limitation:** Reanalysis-derived data, not ground-truth station observations.