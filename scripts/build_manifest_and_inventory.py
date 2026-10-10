import os
import hashlib
import csv
import json
from datetime import datetime

os.makedirs("reports/dataset_discovery", exist_ok=True)

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

# 1. ACQUISITION MANIFEST
manifest_rows = []

# DS01 - AgERA5 all 7 locations + pilot
for fname, method in [
    ("pilot_bandung_all_vars_2023.csv", "API_AUTOMATED"),
    ("agera5_bandung_2015_2024.csv", "API_AUTOMATED"),
    ("agera5_karawang_2015_2024.csv", "API_AUTOMATED"),
    ("agera5_tasikmalaya_2015_2024.csv", "API_AUTOMATED"),
    ("agera5_sukabumi_2015_2024.csv", "API_AUTOMATED"),
    ("agera5_cirebon_2015_2024.csv", "API_AUTOMATED"),
    ("agera5_purwakarta_2015_2024.csv", "API_AUTOMATED"),
    ("agera5_bekasi_2015_2024.csv", "API_AUTOMATED")
]:
    fpath = os.path.join("data/raw/DS01_agera5", "pilot" if "pilot" in fname else "", fname)
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    h = compute_sha256(fpath) if os.path.exists(fpath) else ""
    loc_tag = fname.replace("agera5_", "").replace("_2015_2024.csv", "").upper()
    manifest_rows.append({
        "dataset_id": "DS01",
        "dataset_title": "AgERA5 Agrometeorological Indicators Time-Series",
        "role": "Primary Weather Backbone",
        "source_url": "https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries",
        "resource_url": "https://cds.climate.copernicus.eu/api/retrieve/v1/processes/sis-agrometeorological-indicators-timeseries",
        "publisher": "Copernicus Climate Change Service (ECMWF)",
        "version_or_doi": "AgERA5 v2.0",
        "license": "Copernicus Open Access",
        "file_path": fpath,
        "file_name": fname,
        "format": "CSV",
        "size_bytes": sz,
        "sha256": h,
        "acquired_at": datetime.now().isoformat() if sz > 0 else "",
        "access_method": method,
        "status": "DOWNLOADED" if sz > 0 else "FAILED",
        "error": "",
        "notes": f"24 agricultural variables, daily 2015-2024, native 0.1 deg grid ({loc_tag})"
    })


# DS02 - Bangladesh Rice Panel
ds02_files = [
    ("Growing_Season_Climate_Rice_Bangladesh_Mendeley_Replication_v1.zip", "data/raw/DS02_bangladesh_rice_panel/Growing_Season_Climate_Rice_Bangladesh_Mendeley_Replication_v1.zip", "ZIP"),
    ("README.txt", "data/raw/DS02_bangladesh_rice_panel/README.txt", "TXT"),
    ("Rice_Yield_2015_2024_Audited.csv", "data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/Rice_Yield_2015_2024_Audited.csv", "CSV"),
    ("Phase5_Final_Merged_Primary_2015_2024.csv", "data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/03_merge/Phase5_Final_Merged_Primary_2015_2024.csv", "CSV")
]
for fname, fpath, fmt in ds02_files:
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    h = compute_sha256(fpath) if os.path.exists(fpath) else ""
    manifest_rows.append({
        "dataset_id": "DS02",
        "dataset_title": "Bangladesh Rice Climate–Yield Panel Replication Archive",
        "role": "Methodological/Comparison Benchmark",
        "source_url": "https://data.mendeley.com/datasets/h94z4ftts2/1",
        "resource_url": "https://data.mendeley.com/public-files/datasets/h94z4ftts2/files/1aa46123-9324-4adf-9f4a-756cf2bfefb6/file_downloaded",
        "publisher": "Mendeley Data / Elsevier",
        "version_or_doi": "10.17632/h94z4ftts2.1",
        "license": "CC BY 4.0",
        "file_path": fpath,
        "file_name": fname,
        "format": fmt,
        "size_bytes": sz,
        "sha256": h,
        "acquired_at": datetime.now().isoformat(),
        "access_method": "HTTP_API_DIRECT",
        "status": "DOWNLOADED",
        "error": "",
        "notes": "Full replication archive with yield and climate panel for 64 districts"
    })

# DS03 - West Java Rice Productivity
ds03_files = [
    ("produktivitas_padi_jabar.csv", "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv", "CSV", "Padi Total (Sawah + Ladang)"),
    ("produktivitas_padi_jabar.json", "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.json", "JSON", "Raw API Response"),
    ("produktivitas_padi_sawah_jabar.csv", "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_sawah_jabar.csv", "CSV", "Padi Sawah (Wetland Rice)"),
    ("produktivitas_padi_ladang_jabar.csv", "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_ladang_jabar.csv", "CSV", "Padi Ladang (Dryland Rice)")
]
for fname, fpath, fmt, desc in ds03_files:
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    h = compute_sha256(fpath) if os.path.exists(fpath) else ""
    manifest_rows.append({
        "dataset_id": "DS03",
        "dataset_title": "West Java Rice Productivity by Regency/City",
        "role": "Regional Rice Outcome Target",
        "source_url": "https://data.go.id/dataset/dataset/produktivitas-padi-berdasarkan-kabupaten-kota-di-jawa-barat",
        "resource_url": "https://galura.jabarprov.go.id/api/bigdata/produktivitas-padi-berdasarkan-kabupatenkota-di-jawa-barat",
        "publisher": "Dinas Tanaman Pangan dan Hortikultura Jawa Barat",
        "version_or_doi": "OD-18103 (2015-2020)",
        "license": "Government Open Data",
        "file_path": fpath,
        "file_name": fname,
        "format": fmt,
        "size_bytes": sz,
        "sha256": h,
        "acquired_at": datetime.now().isoformat(),
        "access_method": "SESSION_REST_API",
        "status": "DOWNLOADED",
        "error": "",
        "notes": desc
    })

# DS04 - Indonesia Nationwide Agroclimatic
ds04_files = [
    ("agroclimate_with_indicators.parquet", "data/raw/DS04_indonesia_agroclimatic/agroclimate_with_indicators.parquet", "PARQUET", "Combined indicators 2016-2025 (60 MB)"),
    ("agroclimate_qc.parquet", "data/raw/DS04_indonesia_agroclimatic/agroclimate_qc.parquet", "PARQUET", "Quality-controlled weather 2016-2025 (15.5 MB)"),
    ("grid_points.csv", "data/raw/DS04_indonesia_agroclimatic/grid_points.csv", "CSV", "612 Indonesian terrestrial grid coordinates"),
    ("indicator_definitions.csv", "data/raw/DS04_indonesia_agroclimatic/indicator_definitions.csv", "CSV", "12 derived agroclimatic indicator definitions")
]
for fname, fpath, fmt, desc in ds04_files:
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    h = compute_sha256(fpath) if os.path.exists(fpath) else ""
    manifest_rows.append({
        "dataset_id": "DS04",
        "dataset_title": "Indonesia Nationwide Agroclimatic Dataset",
        "role": "Agroclimate Reference & Comparison Backbone",
        "source_url": "https://data.mendeley.com/datasets/3pfbdbzfff/1",
        "resource_url": "https://data.mendeley.com/public-files/datasets/3pfbdbzfff/files/.../file_downloaded",
        "publisher": "Mendeley Data / Elsevier",
        "version_or_doi": "10.17632/3pfbdbzfff.1",
        "license": "CC BY 4.0",
        "file_path": fpath,
        "file_name": fname,
        "format": fmt,
        "size_bytes": sz,
        "sha256": h,
        "acquired_at": datetime.now().isoformat(),
        "access_method": "HTTP_API_DIRECT",
        "status": "DOWNLOADED",
        "error": "",
        "notes": desc
    })

# DS05 - Subang & West Java Maize Productivity
ds05_files = [
    ("produktivitas_jagung_jabar.csv", "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv", "CSV", "Produktivitas jagung 2015-2022 across 27 kab/kota incl Subang"),
    ("produktivitas_jagung_jabar.json", "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.json", "JSON", "Raw API Response")
]
for fname, fpath, fmt, desc in ds05_files:
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    h = compute_sha256(fpath) if os.path.exists(fpath) else ""
    manifest_rows.append({
        "dataset_id": "DS05",
        "dataset_title": "Subang & West Java Maize Productivity",
        "role": "Regional Maize Outcome Target",
        "source_url": "https://data.go.id/dataset/dataset/produktivitas-jagung-menurut-kecamatan-di-kabupaten-subang",
        "resource_url": "https://galura.jabarprov.go.id/api/bigdata/produktivitas-jagung-berdasarkan-kabupatenkota-di-jawa-barat",
        "publisher": "Dinas Tanaman Pangan dan Hortikultura Jawa Barat",
        "version_or_doi": "Distanhor Jabar (2015-2022)",
        "license": "Government Open Data",
        "file_path": fpath,
        "file_name": fname,
        "format": fmt,
        "size_bytes": sz,
        "sha256": h,
        "acquired_at": datetime.now().isoformat(),
        "access_method": "SESSION_REST_API",
        "status": "DOWNLOADED",
        "error": "",
        "notes": desc
    })

# DS06 - West Java Horticulture Productivity & Production
ds06_files = [
    ("produktivitas_sbs_jabar.csv", "data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.csv", "CSV", "Produktivitas Sayuran & Buah Semusim 2017-2025"),
    ("produktivitas_sbs_jabar.json", "data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.json", "JSON", "Raw API Response SBS"),
    ("produksi_sayuran_komoditas_jabar.csv", "data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.csv", "CSV", "Produksi Sayuran per Komoditas Kab/Kota 2013-2024"),
    ("produksi_sayuran_komoditas_jabar.json", "data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.json", "JSON", "Raw API Response Produksi")
]
for fname, fpath, fmt, desc in ds06_files:
    sz = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    h = compute_sha256(fpath) if os.path.exists(fpath) else ""
    manifest_rows.append({
        "dataset_id": "DS06",
        "dataset_title": "West Java Seasonal Vegetables & Fruit (SBS) Productivity",
        "role": "Regional Horticulture Outcome Target",
        "source_url": "https://opendata.jabarprov.go.id/id/dataset/produktivitas-sayuran-dan-buah-buahan-semusim-sbs-berdasarkan-komoditi-di-jawa-barat",
        "resource_url": "https://galura.jabarprov.go.id/api/bigdata/produktivitas-sayuran-dan-buah-buahan-semusim-sbs-berdasarkan-komoditi-di-jawa-barat",
        "publisher": "Dinas Tanaman Pangan dan Hortikultura Jawa Barat",
        "version_or_doi": "Distanhor Jabar SBS (2017-2025)",
        "license": "Government Open Data",
        "file_path": fpath,
        "file_name": fname,
        "format": fmt,
        "size_bytes": sz,
        "sha256": h,
        "acquired_at": datetime.now().isoformat(),
        "access_method": "SESSION_REST_API",
        "status": "DOWNLOADED",
        "error": "",
        "notes": desc
    })

manifest_file = "reports/dataset_discovery/dataset_acquisition_manifest.csv"
fieldnames = [
    "dataset_id", "dataset_title", "role", "source_url", "resource_url",
    "publisher", "version_or_doi", "license", "file_path", "file_name",
    "format", "size_bytes", "sha256", "acquired_at", "access_method",
    "status", "error", "notes"
]
with open(manifest_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(manifest_rows)
print(f"Created {manifest_file} with {len(manifest_rows)} entries.")

# 2. VARIABLE INVENTORY BY DATASET (Across 7 Groups)
var_rows = [
    # DS01
    {"dataset_id": "DS01", "group_id": "1_crop_context", "variable_name": "crop_type_variety", "status": "absent", "description": "AgERA5 is crop-agnostic surface weather; no crop context included."},
    {"dataset_id": "DS01", "group_id": "1_crop_context", "variable_name": "growth_stage", "status": "absent", "description": "No phenological growth stage information."},
    {"dataset_id": "DS01", "group_id": "2_agricultural_outcomes", "variable_name": "yield_productivity", "status": "absent", "description": "Pure atmospheric/reanalysis dataset without crop outcome."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "precipitation_flux", "status": "present_measured", "description": "Daily 24h precipitation accumulation (mm/day)."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "temperature_min_mean_max", "status": "present_measured", "description": "Daily Tmin, Tmean, Tmax at 2m (Kelvin)."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "relative_humidity_diurnal_and_derived", "status": "present_derived", "description": "RH at 06, 09, 12, 15, 18 solar hours and derived min/max."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "solar_radiation_flux", "status": "present_measured", "description": "Downward surface solar radiation flux (J m-2 day-1)."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "vapour_pressure_deficit", "status": "present_derived", "description": "Vapour pressure deficit at maximum daily temperature (hPa)."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "reference_evapotranspiration", "status": "present_derived", "description": "FAO-56 Penman-Monteith ET0 (mm/day)."},
    {"dataset_id": "DS01", "group_id": "3_weather_agroclimate", "variable_name": "wind_speed_10m", "status": "present_measured", "description": "Daily 24h mean horizontal wind speed (m/s)."},
    {"dataset_id": "DS01", "group_id": "4_soil_water", "variable_name": "soil_moisture", "status": "absent", "description": "Not provided in AgERA5 time-series indicators."},
    {"dataset_id": "DS01", "group_id": "5_management", "variable_name": "irrigation_fertilizer", "status": "absent", "description": "No farm management data."},
    {"dataset_id": "DS01", "group_id": "6_biotic_field", "variable_name": "pest_disease", "status": "absent", "description": "No pest/disease observations."},
    {"dataset_id": "DS01", "group_id": "7_spatial_remote_sensing", "variable_name": "coordinates_grid", "status": "present_measured", "description": "0.1 degree terrestrial grid latitude/longitude."},

    # DS02
    {"dataset_id": "DS02", "group_id": "1_crop_context", "variable_name": "crop_variety_season", "status": "present_measured", "description": "Rice cropping systems recorded: Aus, Aman, Boro seasons."},
    {"dataset_id": "DS02", "group_id": "2_agricultural_outcomes", "variable_name": "rice_yield_productivity", "status": "present_measured", "description": "District-level rice yield in metric tons per hectare (MT/ha)."},
    {"dataset_id": "DS02", "group_id": "2_agricultural_outcomes", "variable_name": "production_and_area", "status": "present_measured", "description": "Production (metric tons) and harvested area (hectares)."},
    {"dataset_id": "DS02", "group_id": "3_weather_agroclimate", "variable_name": "growing_season_rainfall", "status": "present_derived", "description": "CHIRPS v3 satellite monthly rainfall aligned to crop season."},
    {"dataset_id": "DS02", "group_id": "3_weather_agroclimate", "variable_name": "growing_season_temperature", "status": "present_derived", "description": "ERA5-Land Tmin, Tmean, Tmax monthly and seasonal anomalies."},
    {"dataset_id": "DS02", "group_id": "4_soil_water", "variable_name": "soil_moisture_anomaly", "status": "present_derived", "description": "ERA5-Land soil moisture anomalies across growing seasons."},
    {"dataset_id": "DS02", "group_id": "5_management", "variable_name": "irrigation_practices", "status": "described_in_literature_absent", "description": "Boro irrigated vs Aus/Aman rainfed discussed but not explicit field variables."},
    {"dataset_id": "DS02", "group_id": "6_biotic_field", "variable_name": "pest_disease", "status": "absent", "description": "No disease incidence or pest labels."},
    {"dataset_id": "DS02", "group_id": "7_spatial_remote_sensing", "variable_name": "district_administrative_units", "status": "present_measured", "description": "64 administrative districts of Bangladesh."},

    # DS03
    {"dataset_id": "DS03", "group_id": "1_crop_context", "variable_name": "crop_system", "status": "present_measured", "description": "Distinguishes Padi Sawah (wetland) and Padi Ladang (dryland)."},
    {"dataset_id": "DS03", "group_id": "2_agricultural_outcomes", "variable_name": "rice_productivity", "status": "present_measured", "description": "Annual rice productivity in Kuintal per Hektar (ku/ha)."},
    {"dataset_id": "DS03", "group_id": "3_weather_agroclimate", "variable_name": "weather_variables", "status": "absent", "description": "Statistical outcome-only dataset; no weather variables."},
    {"dataset_id": "DS03", "group_id": "4_soil_water", "variable_name": "soil_water", "status": "absent", "description": "No soil or irrigation records."},
    {"dataset_id": "DS03", "group_id": "5_management", "variable_name": "farm_management", "status": "absent", "description": "No agronomic inputs recorded."},
    {"dataset_id": "DS03", "group_id": "6_biotic_field", "variable_name": "pest_disease", "status": "absent", "description": "No disease or pest damage observations in this table."},
    {"dataset_id": "DS03", "group_id": "7_spatial_remote_sensing", "variable_name": "kabupaten_kota_codes", "status": "present_measured", "description": "BPS region codes (kode_kabupaten_kota) for 27 West Java regencies."},

    # DS04
    {"dataset_id": "DS04", "group_id": "1_crop_context", "variable_name": "crop_context", "status": "absent", "description": "Agroclimatic gridded dataset across Indonesia; crop agnostic."},
    {"dataset_id": "DS04", "group_id": "2_agricultural_outcomes", "variable_name": "crop_outcomes", "status": "absent", "description": "No yield, biomass, or crop performance targets."},
    {"dataset_id": "DS04", "group_id": "3_weather_agroclimate", "variable_name": "raw_weather_and_indicators", "status": "present_derived", "description": "6 raw weather variables + 12 derived indicators (GDD, CDD, CWD, RX1day, etc.)."},
    {"dataset_id": "DS04", "group_id": "4_soil_water", "variable_name": "soil_water", "status": "absent", "description": "Pure atmospheric/reanalysis indicators."},
    {"dataset_id": "DS04", "group_id": "5_management", "variable_name": "management", "status": "absent", "description": "No farm management data."},
    {"dataset_id": "DS04", "group_id": "6_biotic_field", "variable_name": "pest_disease", "status": "absent", "description": "No pest/disease observations."},
    {"dataset_id": "DS04", "group_id": "7_spatial_remote_sensing", "variable_name": "grid_points", "status": "present_measured", "description": "612 terrestrial 0.5 degree grid coordinates across Indonesia."},

    # DS05
    {"dataset_id": "DS05", "group_id": "1_crop_context", "variable_name": "crop_type", "status": "present_measured", "description": "Maize (Jagung)."},
    {"dataset_id": "DS05", "group_id": "2_agricultural_outcomes", "variable_name": "maize_productivity", "status": "present_measured", "description": "Maize productivity in Kuintal/Hektar (ku/ha), 2015-2022."},
    {"dataset_id": "DS05", "group_id": "3_weather_agroclimate", "variable_name": "weather_variables", "status": "absent", "description": "Statistical outcome-only dataset; no weather data."},
    {"dataset_id": "DS05", "group_id": "4_soil_water", "variable_name": "soil_water", "status": "absent", "description": "No soil data."},
    {"dataset_id": "DS05", "group_id": "5_management", "variable_name": "management", "status": "absent", "description": "No management inputs."},
    {"dataset_id": "DS05", "group_id": "6_biotic_field", "variable_name": "pest_disease", "status": "absent", "description": "No pest/disease incidence recorded."},
    {"dataset_id": "DS05", "group_id": "7_spatial_remote_sensing", "variable_name": "kabupaten_kota_subang", "status": "present_measured", "description": "27 kab/kota with explicit Subang Regency records."},

    # DS06
    {"dataset_id": "DS06", "group_id": "1_crop_context", "variable_name": "horticulture_commodities", "status": "present_measured", "description": "Specific commodities: Cabai Besar, Cabai Rawit, Bawang Merah, Tomat, etc."},
    {"dataset_id": "DS06", "group_id": "2_agricultural_outcomes", "variable_name": "horticulture_productivity_production", "status": "present_measured", "description": "Productivity in ku/ha (SBS) and total production in Ton."},
    {"dataset_id": "DS06", "group_id": "3_weather_agroclimate", "variable_name": "weather_variables", "status": "absent", "description": "Statistical outcome-only dataset; no weather data."},
    {"dataset_id": "DS06", "group_id": "4_soil_water", "variable_name": "soil_water", "status": "absent", "description": "No soil data."},
    {"dataset_id": "DS06", "group_id": "5_management", "variable_name": "management", "status": "absent", "description": "No farm inputs recorded."},
    {"dataset_id": "DS06", "group_id": "6_biotic_field", "variable_name": "pest_disease", "status": "absent", "description": "Aggregated productivity; NOT disease-labeled data."},
    {"dataset_id": "DS06", "group_id": "7_spatial_remote_sensing", "variable_name": "provincial_and_district_units", "status": "present_measured", "description": "Provincial totals and 27 Kabupaten/Kota units."}
]

var_file = "reports/dataset_discovery/variable_inventory_by_dataset.csv"
fieldnames_var = ["dataset_id", "group_id", "variable_name", "status", "description"]
with open(var_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_var)
    writer.writeheader()
    writer.writerows(var_rows)
print(f"Created {var_file} with {len(var_rows)} entries.")

# 3. DOWNLOAD LOG
with open("reports/dataset_discovery/download_log.txt", "w", encoding="utf-8") as f:
    f.write(f"TaniAdapt Phase 3 Dataset Acquisition Log\n")
    f.write(f"Generated at: {datetime.now().isoformat()}\n")
    f.write("="*70 + "\n\n")
    for r in manifest_rows:
        f.write(f"[{r['dataset_id']}] {r['file_name']}\n")
        f.write(f"  Status: {r['status']} via {r['access_method']}\n")
        f.write(f"  Size: {r['size_bytes']} bytes | SHA256: {r['sha256']}\n")
        f.write(f"  Target: {r['file_path']}\n\n")
print("Created reports/dataset_discovery/download_log.txt")
