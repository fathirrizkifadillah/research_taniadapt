import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
CENTROIDS_FILE = PROJECT_ROOT / "reports" / "dataset_audit" / "jabar_27_kabkota_centroids.csv"
AGERA5_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"

df_c = pd.read_csv(CENTROIDS_FILE)

# DEM elevation lookup established from GLO-30 Copernicus DEM
elev_map = {
    "KABUPATEN BANDUNG": 1247.0,
    "KABUPATEN BANDUNG BARAT": 663.0,
    "KABUPATEN BEKASI": 13.0,
    "KABUPATEN BOGOR": 196.0,
    "KABUPATEN CIAMIS": 167.0,
    "KABUPATEN CIANJUR": 726.0,
    "KABUPATEN CIREBON": 13.0,
    "KABUPATEN GARUT": 1252.0,
    "KABUPATEN INDRAMAYU": 8.0,
    "KABUPATEN KARAWANG": 9.0,
    "KABUPATEN KUNINGAN": 207.0,
    "KABUPATEN MAJALENGKA": 107.0,
    "KABUPATEN PANGANDARAN": 121.0,
    "KABUPATEN PURWAKARTA": 217.0,
    "KABUPATEN SUBANG": 49.0,
    "KABUPATEN SUKABUMI": 711.0,
    "KABUPATEN SUMEDANG": 482.0,
    "KABUPATEN TASIKMALAYA": 221.0,
    "KOTA BANDUNG": 703.0,
    "KOTA BANJAR": 37.0,
    "KOTA BEKASI": 19.0,
    "KOTA BOGOR": 238.0,
    "KOTA CIMAHI": 747.0,
    "KOTA CIREBON": 7.0,
    "KOTA DEPOK": 84.0,
    "KOTA SUKABUMI": 574.0,
    "KOTA TASIKMALAYA": 355.0,
}

# Slugs mapping to AgERA5 file
def get_agera5_info(name):
    clean = name.lower().replace("kabupaten ", "kab_").replace("kota ", "kota_").replace(" ", "_")
    f = AGERA5_DIR / f"agera5_{clean}_2015_2024.csv"
    if not f.exists():
        clean_alt = clean.replace("kab_", "").replace("kota_", "")
        f = AGERA5_DIR / f"agera5_{clean_alt}_2015_2024.csv"
    if f.exists():
        df_head = pd.read_csv(f, nrows=1)
        lat = round(float(df_head["latitude"].iloc[0]), 2)
        lon = round(float(df_head["longitude"].iloc[0]), 2)
        precip = round(pd.read_csv(f)["Precipitation_Flux"].sum(), 1)
        tmean_c = round(pd.read_csv(f)["Temperature_Air_2m_Mean_24h"].mean() - 273.15, 2)
        return lat, lon, f.name, precip, tmean_c
    return np.nan, np.nan, "MISSING", np.nan, np.nan

rows = []
for _, r in df_c.iterrows():
    name = r["nama_kabupaten_kota"]
    tipe = r["tipe_wilayah"]
    c_lat = r["true_centroid_lat"]
    c_lon = r["true_centroid_lon"]
    elev = elev_map.get(name, np.nan)
    ag_lat, ag_lon, fname, tot_p, tmean = get_agera5_info(name)
    grid_cell_id = f"CELL_({ag_lat:.1f},_{ag_lon:.1f})"
    
    # 18 Tier A sentra kabupaten flag (Kabupaten only, excluding Kota)
    is_tier_a_candidate = (tipe == "KABUPATEN")
    
    rows.append({
        "nama_kabupaten_kota": name,
        "tipe_wilayah": tipe,
        "centroid_lat": c_lat,
        "centroid_lon": c_lon,
        "dem_elevation_m": elev,
        "agera5_grid_lat": ag_lat,
        "agera5_grid_lon": ag_lon,
        "agera5_cell_id": grid_cell_id,
        "agera5_file": fname,
        "total_precip_10yr_mm": tot_p,
        "mean_temp_c": tmean,
        "is_tier_a_candidate": is_tier_a_candidate
    })

df_grid_audit = pd.DataFrame(rows)

# Check shared grid cells
cell_counts = df_grid_audit["agera5_cell_id"].value_counts()
df_grid_audit["units_sharing_this_cell"] = df_grid_audit["agera5_cell_id"].map(cell_counts)

# List sharing partners
sharing_map = df_grid_audit.groupby("agera5_cell_id")["nama_kabupaten_kota"].apply(lambda s: ", ".join(s)).to_dict()
df_grid_audit["sharing_partners"] = df_grid_audit["agera5_cell_id"].map(sharing_map)

out_file = AUDIT_DIR / "a8_spatial_grid_cells_audit.csv"
df_grid_audit.to_csv(out_file, index=False)

print("=== HASIL AUDIT DUPLIKASI SEL GRID AGERA5 (27 WILAYAH) ===")
print(f"Total Unit Wilayah Administrasi: {len(df_grid_audit)}")
print(f"Total Sel Grid AgERA5 Unik (0.1 deg): {df_grid_audit['agera5_cell_id'].nunique()}")
print(f"\nPasangan Wilayah yang Berbagi Sel Grid Sama:")
shared = df_grid_audit[df_grid_audit["units_sharing_this_cell"] > 1][["agera5_cell_id", "nama_kabupaten_kota", "total_precip_10yr_mm", "mean_temp_c"]]
print(shared.to_string(index=False))

# Check Tier A Kabupaten (18 Kab)
tier_a_kab = df_grid_audit[df_grid_audit["tipe_wilayah"] == "KABUPATEN"]
print(f"\nEvaluasi 18 Kabupaten Tier A:")
print(f"Jumlah Kabupaten: {len(tier_a_kab)}")
print(f"Jumlah Sel Grid Unik di 18 Kabupaten: {tier_a_kab['agera5_cell_id'].nunique()}")

# Are there any duplicates among the 18 Kab themselves?
kab_sharing = tier_a_kab[tier_a_kab.duplicated(subset=['agera5_cell_id'], keep=False)]
if len(kab_sharing) == 0:
    print("KESIMPULAN TIER A: SEMUA 18 KABUPATEN MEMILIKI SEL GRID AGERA5 UNIK! Tidak ada kabupaten Tier A yang saling berbagi sel!")
else:
    print("PERINGATAN: Ada kabupaten Tier A yang berbagi sel:", kab_sharing['nama_kabupaten_kota'].tolist())

# Subang coordinates unification
subang_row = df_grid_audit[df_grid_audit["nama_kabupaten_kota"] == "KABUPATEN SUBANG"].iloc[0]
print(f"\nKOORDINAT STANDAR SUBANG TERUNIFIKASI:")
print(f"  Centroid Resmi: Lat {subang_row['centroid_lat']}, Lon {subang_row['centroid_lon']}")
print(f"  Sel AgERA5 (0.1 deg): Lat {subang_row['agera5_grid_lat']}, Lon {subang_row['agera5_grid_lon']}")
print(f"  Elevasi DEM: {subang_row['dem_elevation_m']} m")
