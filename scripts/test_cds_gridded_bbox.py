import os
from pathlib import Path
import cdsapi

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
OUT_DIR = PROJECT_ROOT / "data/raw/DS01_agera5/gridded_jabar"
OUT_DIR.mkdir(parents=True, exist_ok=True)

c = cdsapi.Client()

# Test 1 priority request: Precipitation flux year 2022 for West Java Bbox
# Bbox: North -5.8, West 106.3, South -7.9, East 109.0
target_file = OUT_DIR / "agera5_jabar_precipitation_flux_2022.zip"

if target_file.exists() and target_file.stat().st_size > 1000:
    print(f"File already exists: {target_file} ({target_file.stat().st_size} bytes)")
else:
    print("Testing CDS request for sis-agrometeorological-indicators (gridded)...")
    try:
        c.retrieve(
            "sis-agrometeorological-indicators",
            {
                "variable": "precipitation_flux",
                "year": "2022",
                "month": [f"{m:02d}" for m in range(1, 13)],
                "day": [f"{d:02d}" for d in range(1, 32)],
                "area": [-5.8, 106.3, -7.9, 109.0],
                "format": "zip"
            },
            str(target_file)
        )
        print(f"Success! Downloaded {target_file} ({target_file.stat().st_size} bytes)")
    except Exception as e:
        print(f"CDS API Request failed or queue note: {type(e).__name__}: {e}")
