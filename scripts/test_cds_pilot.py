import cdsapi
import os
import time

c = cdsapi.Client()

# Pilot request for 1 location (Bandung), 4 pilot core variables, format csv
test_area = [-6.85, 107.55, -6.95, 107.65] # [North, West, South, East] covering (-6.9, 107.6)

test_vars = [
    "2m_temperature_24_hour_mean",
    "2m_temperature_24_hour_maximum",
    "2m_temperature_24_hour_minimum",
    "precipitation_flux"
]

out_dir = "data/raw/DS01_agera5/pilot"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "pilot_bandung.zip")

print("Submitting pilot request to sis-agrometeorological-indicators-timeseries...")
start_t = time.time()
try:
    c.retrieve(
        "sis-agrometeorological-indicators-timeseries",
        {
            "variable": test_vars,
            "data_format": "csv",
            "date": "2024-01-01/2024-01-05",
            "area": test_area
        },
        out_file

    )
    print(f"Pilot request successful! File: {out_file}, size: {os.path.getsize(out_file)} bytes in {time.time()-start_t:.1f}s")
except Exception as e:
    print(f"Pilot request failed with error: {e}")
