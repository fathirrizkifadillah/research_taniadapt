import json
import pandas as pd
import os

files_to_convert = [
    ("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.json",
     "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv"),
    ("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_sawah_jabar.json",
     "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_sawah_jabar.csv"),
    ("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_ladang_jabar.json",
     "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_ladang_jabar.csv"),
    ("data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.json",
     "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv"),
    ("data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.json",
     "data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.csv"),
    ("data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.json",
     "data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.csv")
]

for src, dst in files_to_convert:
    if os.path.exists(src):
        with open(src, "r", encoding="utf-8") as f:
            d = json.load(f)
        records = d.get("data", [])
        if records:
            df = pd.DataFrame(records)
            df.to_csv(dst, index=False)
            print(f"Converted {src} -> {dst}: {len(df)} rows, columns: {list(df.columns)}")
        else:
            print(f"No records found in {src}")
    else:
        print(f"File not found: {src}")
