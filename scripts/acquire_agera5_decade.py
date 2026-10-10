import cdsapi
import os
import time

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

locations = {
    "Bandung": [-6.85, 107.55, -6.95, 107.65],
    "Karawang": [-6.25, 107.25, -6.35, 107.35],
    "Tasikmalaya": [-7.28, 108.17, -7.38, 108.27],
    "Sukabumi": [-6.87, 106.88, -6.97, 106.98],
    "Cirebon": [-6.68, 108.51, -6.78, 108.61],
    "Purwakarta": [-6.51, 107.39, -6.61, 107.49],
    "Bekasi": [-6.19, 106.95, -6.29, 107.05]
}

out_dir = "data/raw/DS01_agera5"
os.makedirs(out_dir, exist_ok=True)

# Test decade 2015-2024 for Bandung (overlaps with rice/maize/chili data)
out_file = os.path.join(out_dir, "agera5_bandung_2015_2024.csv")
print("Requesting 10-year span (2015-2024) for Bandung with all 24 vars...")
t0 = time.time()
try:
    c.retrieve(
        "sis-agrometeorological-indicators-timeseries",
        {
            "variable": all_ag_vars,
            "data_format": "csv",
            "date": "2015-01-01/2024-12-31",
            "area": locations["Bandung"]
        },
        out_file
    )
    print(f"Done! {out_file} size: {os.path.getsize(out_file)} bytes in {time.time()-t0:.1f}s")
except Exception as e:
    print("Error:", e)
