import cdsapi
import os
import time
import pandas as pd
from project_paths import PROJECT_ROOT

OUT_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
OUT_DIR.mkdir(parents=True, exist_ok=True)

c = cdsapi.Client()

all_ag_vars = [
    "10m_wind_speed_24_hour_mean",
    "2m_dewpoint_temperature_24_hour_mean",
    "2m_relative_humidity_at_06_00",
    "2m_relative_humidity_at_09_00",
    "2m_relative_humidity_at_12_00",
    "2m_relative_humidity_at_15_00",
    "2m_relative_humidity_at_18_00",
    "2m_temperature_24_hour_maximum",
    "2m_temperature_24_hour_mean",
    "2m_temperature_24_hour_minimum",
    "2m_temperature_day_time_maximum",
    "2m_temperature_day_time_mean",
    "2m_temperature_night_time_mean",
    "2m_temperature_night_time_minimum",
    "cloud_cover_24_hour_mean",
    "derived_2m_relative_humidity_24_hour_maximum",
    "derived_2m_relative_humidity_24_hour_minimum",
    "liquid_precipitation_duration_fraction",
    "precipitation_duration_fraction",
    "precipitation_flux",
    "reference_evapotranspiration",
    "solar_radiation_flux",
    "vapour_pressure_24_hour_mean",
    "vapour_pressure_deficit_at_maximum_temperature"
]

# Mapping 27 Kabupaten/Kota in West Java to coordinates and standardized slug
kabkota_list = [
    # 18 Kabupaten
    {"slug": "kab_bandung", "nama": "KABUPATEN BANDUNG", "lat": -7.1000, "lon": 107.6108},
    {"slug": "kab_bandung_barat", "nama": "KABUPATEN BANDUNG BARAT", "lat": -6.8971, "lon": 107.4150},
    {"slug": "kab_bekasi", "nama": "KABUPATEN BEKASI", "lat": -6.2154, "lon": 107.1207},
    {"slug": "kab_bogor", "nama": "KABUPATEN BOGOR", "lat": -6.5600, "lon": 106.7675},
    {"slug": "kab_ciamis", "nama": "KABUPATEN CIAMIS", "lat": -7.2905, "lon": 108.4286},
    {"slug": "kab_cianjur", "nama": "KABUPATEN CIANJUR", "lat": -7.1337, "lon": 107.1578},
    {"slug": "kab_cirebon", "nama": "KABUPATEN CIREBON", "lat": -6.7456, "lon": 108.5516},
    {"slug": "kab_garut", "nama": "KABUPATEN GARUT", "lat": -7.3596, "lon": 107.7889, "alias": "agera5_garut_centroid_2015_2024.csv"},
    {"slug": "kab_indramayu", "nama": "KABUPATEN INDRAMAYU", "lat": -6.4488, "lon": 108.1686},
    {"slug": "kab_karawang", "nama": "KABUPATEN KARAWANG", "lat": -6.2520, "lon": 107.3542, "alias": "agera5_karawang_2015_2024.csv"},
    {"slug": "kab_kuningan", "nama": "KABUPATEN KUNINGAN", "lat": -7.0042, "lon": 108.5603},
    {"slug": "kab_majalengka", "nama": "KABUPATEN MAJALENGKA", "lat": -6.8159, "lon": 108.2578},
    {"slug": "kab_pangandaran", "nama": "KABUPATEN PANGANDARAN", "lat": -7.6356, "lon": 108.5188},
    {"slug": "kab_purwakarta", "nama": "KABUPATEN PURWAKARTA", "lat": -6.5950, "lon": 107.4322, "alias": "agera5_purwakarta_2015_2024.csv"},
    {"slug": "kab_subang", "nama": "KABUPATEN SUBANG", "lat": -6.4830, "lon": 107.7322, "alias": "agera5_subang_centroid_2015_2024.csv"},
    {"slug": "kab_sukabumi", "nama": "KABUPATEN SUKABUMI", "lat": -7.0762, "lon": 106.7073, "alias": "agera5_sukabumi_kab_centroid_2015_2024.csv"},
    {"slug": "kab_sumedang", "nama": "KABUPATEN SUMEDANG", "lat": -6.8251, "lon": 107.9809},
    {"slug": "kab_tasikmalaya", "nama": "KABUPATEN TASIKMALAYA", "lat": -7.4967, "lon": 108.1413},
    # 9 Kota
    {"slug": "kota_bandung", "nama": "KOTA BANDUNG", "lat": -6.9175, "lon": 107.6191, "alias": "agera5_bandung_2015_2024.csv"},
    {"slug": "kota_banjar", "nama": "KOTA BANJAR", "lat": -7.3683, "lon": 108.5336},
    {"slug": "kota_bekasi", "nama": "KOTA BEKASI", "lat": -6.2383, "lon": 106.9756, "alias": "agera5_bekasi_2015_2024.csv"},
    {"slug": "kota_bogor", "nama": "KOTA BOGOR", "lat": -6.5950, "lon": 106.8167},
    {"slug": "kota_cimahi", "nama": "KOTA CIMAHI", "lat": -6.8865, "lon": 107.5436},
    {"slug": "kota_cirebon", "nama": "KOTA CIREBON", "lat": -6.7320, "lon": 108.5523, "alias": "agera5_cirebon_2015_2024.csv"},
    {"slug": "kota_depok", "nama": "KOTA DEPOK", "lat": -6.3961, "lon": 106.8168},
    {"slug": "kota_sukabumi", "nama": "KOTA SUKABUMI", "lat": -6.9278, "lon": 106.9297, "alias": "agera5_sukabumi_2015_2024.csv"},
    {"slug": "kota_tasikmalaya", "nama": "KOTA TASIKMALAYA", "lat": -7.3274, "lon": 108.2207, "alias": "agera5_tasikmalaya_2015_2024.csv"}
]

print("=== ACQUISITION OF AGERA5 FOR ALL 27 KABUPATEN/KOTA (2015-2024) ===")

for item in kabkota_list:
    slug = item["slug"]
    target_file = OUT_DIR / f"agera5_{slug}_2015_2024.csv"
    
    # Check if alias exists and copy/symlink or use it
    if "alias" in item:
        alias_file = OUT_DIR / item["alias"]
        if alias_file.exists() and alias_file.stat().st_size > 500000:
            if not target_file.exists():
                import shutil
                shutil.copyfile(alias_file, target_file)
                print(f"[{item['nama']}] Linked from existing alias {item['alias']} -> {target_file.name}")
            else:
                print(f"[{item['nama']}] Already exists: {target_file.name}")
            continue

    if target_file.exists() and target_file.stat().st_size > 500000:
        print(f"[{item['nama']}] Already acquired: {target_file.name} ({target_file.stat().st_size} bytes)")
        continue

    lat = item["lat"]
    lon = item["lon"]
    box = [round(lat + 0.05, 4), round(lon - 0.05, 4), round(lat - 0.05, 4), round(lon + 0.05, 4)]
    
    print(f"\n[Acquiring AgERA5] {item['nama']} ({slug}) Box: {box}...")
    t0 = time.time()
    try:
        c.retrieve(
            "sis-agrometeorological-indicators-timeseries",
            {
                "variable": all_ag_vars,
                "data_format": "csv",
                "date": "2015-01-01/2024-12-31",
                "area": box
            },
            str(target_file)
        )
        print(f"  -> SUCCESS! {item['nama']}: {target_file.stat().st_size} bytes in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"  -> Failed {item['nama']}: {e}")
    time.sleep(2)

print("\nSeluruh 27 Kabupaten/Kota AgERA5 selesai diproses!")
