import cdsapi
import os
import time

c = cdsapi.Client()

# Bandung box covering (-6.9, 107.6)
test_area = [-6.85, 107.55, -6.95, 107.65]

# All agriculturally relevant variables
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

out_dir = "data/raw/DS01_agera5/pilot"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "pilot_bandung_all_vars_2023.csv")

print(f"Requesting 1 full year (2023) with ALL {len(all_ag_vars)} variables...")
t0 = time.time()
try:
    c.retrieve(
        "sis-agrometeorological-indicators-timeseries",
        {
            "variable": all_ag_vars,
            "data_format": "csv",
            "date": "2023-01-01/2023-12-31",
            "area": test_area
        },
        out_file
    )
    print(f"Success! {out_file} size: {os.path.getsize(out_file)} bytes in {time.time()-t0:.1f}s")
except Exception as e:
    print("Failed:", e)
