import urllib.request, json
import pandas as pd

df = pd.read_csv('reports/dataset_audit/jabar_27_kabkota_centroids.csv')
lats = ','.join([f"{lat:.4f}" for lat in df['true_centroid_lat']])
lons = ','.join([f"{lon:.4f}" for lon in df['true_centroid_lon']])

url = f"https://api.open-meteo.com/v1/elevation?latitude={lats}&longitude={lons}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

elevations = data['elevation']
df['elevation_dem_m'] = elevations
for _, r in df.iterrows():
    print(f"{r['nama_kabupaten_kota']}: lat={r['true_centroid_lat']:.4f}, lon={r['true_centroid_lon']:.4f}, elev={r['elevation_dem_m']} m")
