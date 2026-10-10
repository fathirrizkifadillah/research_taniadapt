import os
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"

url = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/IDN/ADM2/geoBoundaries-IDN-ADM2.geojson"
gdf = gpd.read_file(url)

# Target 27 nama resmi Distanhor
df_dist = pd.read_csv(PROJECT_ROOT / "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv")
target_names = sorted(df_dist['nama_kabupaten_kota'].unique().tolist())

# Buat grid AgERA5 0.1 derajat melingkupi Jawa Barat [-5.8 to -7.9 lat, 106.3 to 109.0 lon]
lats = np.arange(-7.9, -5.75, 0.1)
lons = np.arange(106.3, 109.05, 0.1)
grid_points = [Point(lon, lat) for lat in lats for lon in lons]
gdf_grid = gpd.GeoDataFrame(geometry=grid_points, crs="EPSG:4326")

results = []
for name in target_names:
    clean = name.replace('KABUPATEN ', '').replace('KOTA ', '').strip().lower()
    is_kota = 'KOTA' in name
    
    sub = gdf[gdf['shapeName'].str.lower() == clean]
    if len(sub) == 0:
        sub = gdf[gdf['shapeName'].str.lower().str.contains(clean)]
    
    if len(sub) > 1:
        sub_k = sub[sub['shapeType'].str.lower().str.contains('city' if is_kota else 'regency|county')]
        match_row = sub_k.iloc[0] if len(sub_k) > 0 else sub.iloc[0]
    else:
        match_row = sub.iloc[0]
        
    geom = match_row.geometry
    centroid = geom.centroid
    
    # Hitung jumlah sel AgERA5 0.1 derajat yang berada di dalam poligon
    cells_inside = gdf_grid[gdf_grid.geometry.within(geom)]
    n_cells = len(cells_inside)
    
    # Periksa apakah titik AgERA5 pilot/lama beririsan
    results.append({
        'nama_kabupaten_kota': name,
        'tipe_wilayah': 'KOTA' if is_kota else 'KABUPATEN',
        'true_centroid_lat': round(centroid.y, 4),
        'true_centroid_lon': round(centroid.x, 4),
        'luas_approx_km2': round(geom.area * (111**2), 1),
        'n_sel_agera5_0_1deg': n_cells,
        'shape_name_geoboundaries': match_row['shapeName'],
        'shape_type': match_row['shapeType']
    })

df_spatial = pd.DataFrame(results)
out_csv = AUDIT_DIR / "jabar_27_kabkota_spatial_audit.csv"
df_spatial.to_csv(out_csv, index=False)
print(f"Berhasil menyimpan audit spasial: {out_csv}")
print(df_spatial[['nama_kabupaten_kota', 'tipe_wilayah', 'true_centroid_lat', 'true_centroid_lon', 'n_sel_agera5_0_1deg']].head(10).to_string(index=False))

# Update canonical centroids file
df_canonical_centroids = df_spatial[['nama_kabupaten_kota', 'tipe_wilayah', 'true_centroid_lat', 'true_centroid_lon', 'n_sel_agera5_0_1deg']].copy()
df_canonical_centroids.rename(columns={
    'nama_kabupaten_kota': 'nama',
    'true_centroid_lat': 'lat',
    'true_centroid_lon': 'lon'
}, inplace=True)
df_canonical_centroids.to_csv(AUDIT_DIR / "jabar_27_kabkota_centroids.csv", index=False)
print(f"Berhasil memperbarui: {AUDIT_DIR / 'jabar_27_kabkota_centroids.csv'}")
