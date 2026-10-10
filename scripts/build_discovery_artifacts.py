import csv
import json
import os
import hashlib
from datetime import datetime

os.makedirs("reports/dataset_discovery", exist_ok=True)

# 1. Dataset Catalog
catalog_rows = [
    {
        "dataset_id": "DS01",
        "dataset_title": "AgERA5 Agrometeorological Indicators Time-Series (1979–2025)",
        "role": "Primary Weather & Agroclimatic Backbone",
        "crop_focus": "All crops (crop-agnostic baseline)",
        "geography": "West Java (7 Locations: Tasikmalaya, Bandung, Bekasi, Purwakarta, Karawang, Sukabumi, Cirebon)",
        "spatial_resolution": "0.1° grid (~10 km proxy)",
        "temporal_coverage": "1979-01-01 to 2025-12-31",
        "cadence": "Daily",
        "source_type": "Reanalysis-derived (Copernicus Climate Data Store)",
        "publisher": "Copernicus Climate Change Service (ECMWF)",
        "license": "Copernicus Open Access License / Creative Commons",
        "status": "ACQUIRING_VERIFIED"
    },
    {
        "dataset_id": "DS02",
        "dataset_title": "Bangladesh Rice Climate–Yield Panel Replication Archive",
        "role": "Methodological & Comparative Crop–Climate Panel Benchmark",
        "crop_focus": "Rice (Aus, Aman, Boro seasons)",
        "geography": "Bangladesh (64 districts)",
        "spatial_resolution": "District-level administrative units",
        "temporal_coverage": "2015–2024",
        "cadence": "Crop-season / Annual panel with monthly climate history",
        "source_type": "Official statistics + Satellite/Reanalysis (CHIRPS & ERA5-Land)",
        "publisher": "Mendeley Data / Elsevier",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "status": "DOWNLOADED"
    },
    {
        "dataset_id": "DS03",
        "dataset_title": "West Java Rice Productivity by Regency/City (Produktivitas Padi Jabar)",
        "role": "Regional Crop Outcome Target (Rice)",
        "crop_focus": "Rice (Total Padi, Padi Sawah, Padi Ladang)",
        "geography": "West Java, Indonesia (27 Regencies/Cities)",
        "spatial_resolution": "Kabupaten/Kota administrative units",
        "temporal_coverage": "2015–2020",
        "cadence": "Annual",
        "source_type": "Official Agricultural Statistics (BPS / Distanhor Jabar)",
        "publisher": "Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar",
        "license": "Government Open Data (Satu Data Indonesia / Jabar)",
        "status": "DOWNLOADED"
    },
    {
        "dataset_id": "DS04",
        "dataset_title": "Indonesia Nationwide Agroclimatic Dataset (Open-Meteo/ERA5-Seamless)",
        "role": "National Agroclimatic Comparison & Derived Indicator Reference",
        "crop_focus": "All crops (cross-commodity climate indicators)",
        "geography": "Indonesia Nationwide (612 terrestrial grid points)",
        "spatial_resolution": "0.5° grid (~50 km)",
        "temporal_coverage": "2016-01-01 to 2025-12-31",
        "cadence": "Daily",
        "source_type": "Modelled Reanalysis (ERA5-Seamless via Open-Meteo)",
        "publisher": "Mendeley Data / Elsevier",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "status": "DOWNLOADED"
    },
    {
        "dataset_id": "DS05",
        "dataset_title": "Subang & West Java Maize Productivity (Produktivitas Jagung Jabar)",
        "role": "Regional Crop Outcome Target (Maize)",
        "crop_focus": "Maize / Jagung",
        "geography": "West Java (27 Kab/Kota including Kab. Subang)",
        "spatial_resolution": "Kabupaten/Kota level (Subang included)",
        "temporal_coverage": "2015–2022",
        "cadence": "Annual",
        "source_type": "Official Agricultural Statistics (Dinas Pertanian / Pemprov Jabar)",
        "publisher": "Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar",
        "license": "Government Open Data (Satu Data Indonesia / Jabar)",
        "status": "DOWNLOADED"
    },
    {
        "dataset_id": "DS06",
        "dataset_title": "West Java Seasonal Vegetables & Fruit (SBS) Productivity (Chili Focus)",
        "role": "Regional Horticulture Outcome Target (Large Chili & Bird's-Eye Chili)",
        "crop_focus": "Chili (Cabai Besar, Cabai Rawit) and Seasonal Vegetables",
        "geography": "West Java, Indonesia (Provincial and Kab/Kota breakdown)",
        "spatial_resolution": "Provincial and Kabupaten/Kota",
        "temporal_coverage": "2017–2025 (SBS Productivity) & 2013–2024 (Vegetable Production)",
        "cadence": "Annual",
        "source_type": "Official Agricultural Statistics (Distanhor Jabar)",
        "publisher": "Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar",
        "license": "Government Open Data (Satu Data Indonesia / Jabar)",
        "status": "DOWNLOADED"
    }
]

catalog_file = "reports/dataset_discovery/dataset_catalog.csv"
with open(catalog_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(catalog_rows[0].keys()))
    writer.writeheader()
    writer.writerows(catalog_rows)
print(f"Created {catalog_file}")

# 2. Dataset Sources JSON
with open("reports/dataset_discovery/dataset_sources.json", "w", encoding="utf-8") as f:
    json.dump(catalog_rows, f, indent=2)
print("Created reports/dataset_discovery/dataset_sources.json")

# 3. Clean start note for AgERA5
clean_start_md = """# AgERA5 Clean-Start Acquisition Note

## Background
The previous AgERA5 raw downloads were intentionally deleted by the user to perform a complete, clean, and properly structured fresh-start data acquisition. This was a conscious user decision, not an agent failure or data-loss incident.

## Legacy State vs. New Architecture
- **Legacy approach:** The previous notebook (`01_AgERA5.ipynb`) configured the gridded product (`sis-agrometeorological-indicators`) split into 24 jobs across 47 individual annual requests (up to 1,128 requests), which resulted in large multi-gigabyte ZIP archives with individual NetCDF files for the bounding box.
- **New fresh architecture:** We verified and leveraged the official Copernicus AgERA5 time-series endpoint (`sis-agrometeorological-indicators-timeseries`). This endpoint:
  1. Accepts precise point/area proxies for the 7 target locations in West Java.
  2. Directly generates multi-variable combined CSV files.
  3. Returns daily time-series with unified variables (Kelvin temperatures, mm/day precipitation, relative humidity, solar radiation, VPD, and ET0).
  4. Reduces request complexity from 1,128 requests down to location-based batch requests with verifiable responses.

## Target Locations
1. **Tasikmalaya**: Administrative proxy (-7.33, 108.22)
2. **Bandung**: Administrative proxy (-6.91, 107.61)
3. **Bekasi**: Administrative proxy (-6.24, 107.00)
4. **Purwakarta**: Administrative proxy (-6.56, 107.44)
5. **Karawang**: Administrative proxy (-6.30, 107.30)
6. **Sukabumi**: Administrative proxy (-6.92, 106.93)
7. **Cirebon**: Administrative proxy (-6.73, 108.56)

## Verification Status
- CDS API Client configured locally and verified against `https://cds.climate.copernicus.eu/api`.
- Parameter schema verified directly from ECMWF OpenAPI catalogue:
  - Latitude/Longitude bounding box requires grid-covering extent (0.1° AgERA5 native resolution).
  - Date format requires ISO-8601 interval `yyyy-mm-dd/yyyy-mm-dd`.
  - Format: CSV.
- Pilot execution validated: 4 variables pilot and full 24-variable pilot executed successfully on ECMWF CDS infrastructure.
"""

with open("reports/dataset_discovery/agera5_clean_start_note.md", "w", encoding="utf-8") as f:
    f.write(clean_start_md)
print("Created reports/dataset_discovery/agera5_clean_start_note.md")
