import cdsapi
import os
import time
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
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

# Additional key agricultural centers for M2 and Subang deep dive
targets = {
    "subang_centroid": [-6.43, 107.68, -6.53, 107.78],   # True centroid Kab. Subang (-6.483, 107.732)
    "garut_centroid": [-7.31, 107.74, -7.41, 107.84],    # True centroid Kab. Garut (-7.360, 107.789)
    "sukabumi_kab_centroid": [-7.02, 106.65, -7.12, 106.75] # True centroid Kab. Sukabumi (-7.076, 106.707)
}

print("Memulai penarikan AgERA5 untuk sentra pertanian tambahan (Subang, Garut, Sukabumi Kabupaten)...")

for name, box in targets.items():
    out_file = OUT_DIR / f"agera5_{name}_2015_2024.csv"
    if out_file.exists() and out_file.stat().st_size > 500000:
        print(f"Skipping {name}, already exists ({out_file.stat().st_size} bytes)")
        continue
    
    print(f"\n[Acquiring AgERA5] {name.upper()} (Box: {box})...")
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
            str(out_file)
        )
        print(f"  -> SUCCESS! Acquired {name}: {out_file.stat().st_size} bytes in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"  -> Failed {name}: {e}")
    time.sleep(2)

print("\nPenarikan selesai!")
