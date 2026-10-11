import nbformat
from pathlib import Path

NOTEBOOK_DIR = Path("notebook")

# ==============================================================================
# 6. NOTEBOOK 07: 07_soybean_and_spatial_geoboundaries.ipynb
# ==============================================================================
def update_nb07():
    p = NOTEBOOK_DIR / "07_soybean_and_spatial_geoboundaries.ipynb"
    nb = nbformat.read(p, as_version=4)
    
    code_nb07_plot = '''import geopandas as gpd

path_jabar_geo = RAW_DIR / "jawa_barat_provinsi.geojson"
if not path_jabar_geo.exists():
    path_jabar_geo = PROJECT_ROOT / "data" / "raw" / "DS07_spatial_geoboundaries" / "jawa_barat_provinsi.geojson"
if path_jabar_geo.exists():
    gdf_jabar = gpd.read_file(path_jabar_geo)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [1, 1.2, 1]})

# --- PANEL 1: VALIDASI AUDIT 0.4: KEDELAI (TIER A) VS TOMAT (TIER B) ---
metrics_eval = ['Observasi N', 'Unit Spasial', 'Sentra 8-Thn']
ked_scores = [216, 27, 14]
tom_scores = [9, 1, 0]
x_eval = np.arange(len(metrics_eval))
w = 0.35
ax1.bar(x_eval - w/2, ked_scores, width=w, label='Kedelai (DS07 - Tier A)', color='#2a9d8f', edgecolor='black', alpha=0.85)
ax1.bar(x_eval + w/2, tom_scores, width=w, label='Tomat (DS06 - Tier B)', color='#e76f51', edgecolor='black', alpha=0.85)
ax1.set_xticks(x_eval)
ax1.set_xticklabels(['Sampel N\\n(216 vs 9)', 'Wilayah Spasial\\n(27 vs 1)', 'Sentra Runtun\\n(14 vs 0)'], fontsize=8.5)
ax1.set_title("Audit 0.4: Komparasi Empiris Sampel\\n(Kedelai Tier A vs Tomat Tier B)", fontsize=10.5, fontweight='bold')
ax1.set_ylabel("Jumlah / Skala Metrik", fontsize=10)
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.annotate('Kedelai memiliki sampel 24x lipat\\n& variasi spasial lokal riil\\n-> Terverifikasi TIER A', 
             xy=(0.5, 120), fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="#e8f5e9", ec="#2e7d32", alpha=0.9))

# --- PANEL 2: PETA BATAS GEOSPASIAL ADM1 JAWA BARAT & SEBARAN CENTROID 27 KAB/KOTA ---
if path_jabar_geo.exists():
    gdf_jabar.boundary.plot(ax=ax2, color='#1d3557', linewidth=1.5, label='Batas Wilayah ADM1 (BPS)')
    gdf_jabar.plot(ax=ax2, color='#e9ecef', alpha=0.6)
ax2.scatter(df_centroids['longitude'], df_centroids['latitude'], color='#e76f51', s=35, edgecolor='black', zorder=5, label='Centroid 27 Kab/Kota')
ax2.set_title("Peta Batas Geospasial Jawa Barat & ADM2 Centroids\\n(Batas Resmi ADM1 & 27 Titik Koordinat Kabupaten/Kota)", fontsize=10.5, fontweight='bold')
ax2.set_xlabel("Bujur (Longitude °E)", fontsize=10)
ax2.set_ylabel("Lintang (Latitude °N)", fontsize=10)
ax2.legend(loc='lower left', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)

# --- PANEL 3: TREN PRODUKTIVITAS KEDELAI SENTRA UTAMA (2015–2022) ---
top_sentra = ["KABUPATEN GARUT", "KABUPATEN SUKABUMI", "KABUPATEN MAJALENGKA", "KABUPATEN CIANJUR", "KABUPATEN CIAMIS"]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
for kab, c in zip(top_sentra, colors):
    sub = df_ked[df_ked['nama_kabupaten_kota'] == kab].sort_values('tahun')
    ax3.plot(sub['tahun'], sub['produktivitas_kedelai'], marker='o', label=kab.replace('KABUPATEN ', '').title(), color=c, linewidth=2)
ax3.set_title("Tren Produktivitas Kedelai Sentra Utama (2015–2022)\\n(Variasi Spasial Nyata Antar-Kabupaten)", fontsize=10.5, fontweight='bold')
ax3.set_xlabel("Tahun Kalender", fontsize=10)
ax3.set_ylabel("Produktivitas (ku/ha)", fontsize=10)
ax3.legend(loc='upper right', fontsize=7.5)
ax3.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds07_soybean_and_spatial.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik kedelai dan spasial Jawa Barat berhasil disimpan ke: {png_out}")
'''
    nb.cells[11].source = code_nb07_plot
    nbformat.write(nb, p)
    print("Updated 07_soybean_and_spatial_geoboundaries.ipynb with fixed 3-panel audit figure!")

# ==============================================================================
# 8. NOTEBOOK 09: 09_climate_covariates_and_chirps.ipynb
# ==============================================================================
def update_nb09():
    p = NOTEBOOK_DIR / "09_climate_covariates_and_chirps.ipynb"
    nb = nbformat.read(p, as_version=4)
    
    code_nb09_plot = '''fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [1.1, 1, 1]})

# --- PANEL 1: RUNTUN WAKTU ONI KALENDER WAKTU RIIL ---
df_oni_plot = df_oni_recent.reset_index(drop=True)
n_obs = len(df_oni_plot)
x_years = [df_oni_plot['YR'].iloc[i] + (i % 12) / 12.0 for i in range(n_obs)]
anom_vals = df_oni_plot['ANOM'].values

ax1.plot(x_years, anom_vals, color='#1d3557', linewidth=2, label='NOAA ONI (SST Anomaly)', zorder=4)
ax1.axhline(0.5, color='crimson', linestyle='--', linewidth=1.2, alpha=0.8, label='Ambang El Niño (+0.5°C)')
ax1.axhline(-0.5, color='royalblue', linestyle='--', linewidth=1.2, alpha=0.8, label='Ambang La Niña (-0.5°C)')
ax1.axhline(0.0, color='gray', linestyle='-', alpha=0.5)

ax1.fill_between(x_years, 0.5, anom_vals, where=(anom_vals >= 0.5), color='crimson', alpha=0.25, label='Fase El Niño (Kering)')
ax1.fill_between(x_years, -0.5, anom_vals, where=(anom_vals <= -0.5), color='royalblue', alpha=0.25, label='Fase La Niña (Basah)')

ax1.set_title("Dinamika Iklim Makro Pasifik: Oceanic Niño Index\\n(2015–2024 Kalender Riil, Shading El Niño/La Niña)", fontsize=10.5, fontweight='bold')
ax1.set_xlabel("Tahun Kalender", fontsize=10)
ax1.set_ylabel("Anomali Suhu Muka Laut (°C)", fontsize=10)
ax1.legend(loc='lower left', fontsize=7.5)
ax1.grid(True, linestyle='--', alpha=0.5)

# --- PANEL 2: VALIDASI SILANG HUJAN TASIKMALAYA: AGERA5 VS CHIRPS V2 ---
ch_file_tasik = chirps_dir / "chirps_tasikmalaya_2015_2024.csv"
ag_file_tasik = agera5_dir / "agera5_kab_tasikmalaya_2015_2024.csv"
if ch_file_tasik.exists() and ag_file_tasik.exists():
    df_ch_t = pd.read_csv(ch_file_tasik, skiprows=[1])
    df_ch_t['year'] = pd.to_datetime(df_ch_t['time']).dt.year
    ch_tasik_ann = df_ch_t.groupby('year')['precip'].sum()
    
    df_ag_t = pd.read_csv(ag_file_tasik)
    df_ag_t['year'] = pd.to_datetime(df_ag_t['valid_time']).dt.year
    ag_tasik_ann = df_ag_t.groupby('year')['Precipitation_Flux'].sum()
    
    ax2.plot(ag_tasik_ann.index, ag_tasik_ann.values, marker='o', color='#1d3557', linewidth=2.2, label='AgERA5 (ECMWF Model)')
    ax2.plot(ch_tasik_ann.index, ch_tasik_ann.values, marker='s', color='#2a9d8f', linestyle='--', linewidth=2.2, label='CHIRPS v2 (Satelit+Stasiun)')
    ax2.axhline(4000, color='purple', linestyle=':', label='Batas Orografis Ekstrem (4.000 mm)')

ax2.set_title("Validasi Hujan Orografis Tasikmalaya (2015–2024)\\n(Konfirmasi Efek Orografis Nyata >4.000 mm/tahun)", fontsize=10.5, fontweight='bold')
ax2.set_xlabel("Tahun", fontsize=10)
ax2.set_ylabel("Presipitasi Tahunan (mm/tahun)", fontsize=10)
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.annotate('Bukan Anomali Sensor!\\nKedua satelit mengonfirmasi\\nhujan ekstrem nyata di lereng Galunggung', 
             xy=(2016, 4200), fontsize=8, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="#f3e5f5", ec="#7b1fa2", alpha=0.9))

# --- PANEL 3: VALIDASI SILANG MULTI-STASIUN BLOCKER B3 (TASIKMALAYA, SUBANG, GARUT) ---
st_names = [f"{row['Wilayah / Stasiun'].title()}" for _, row in df_comp_rf.iterrows()]
ag_means = df_comp_rf['AgERA5 Rata-rata (mm/thn)'].tolist()
ch_means = df_comp_rf['CHIRPS Rata-rata (mm/thn)'].tolist()

x_st = np.arange(len(st_names))
w = 0.35
ax3.bar(x_st - w/2, ag_means, width=w, label='AgERA5 (ECMWF)', color='#1d3557', edgecolor='black', alpha=0.85)
ax3.bar(x_st + w/2, ch_means, width=w, label='CHIRPS v2', color='#2a9d8f', edgecolor='black', alpha=0.85)
ax3.set_xticks(x_st)
ax3.set_xticklabels(st_names, fontsize=8.5)
ax3.set_title("Validasi Silang Multi-Stasiun Blocker B3\\n(AgERA5 vs CHIRPS v2 di 3 Zona Agroklimat Jabar)", fontsize=10.5, fontweight='bold')
ax3.set_ylabel("Presipitasi Rata-rata Tahunan (mm)", fontsize=10)
ax3.legend(loc='upper right', fontsize=8)
ax3.grid(True, linestyle='--', alpha=0.5)
for i in range(len(st_names)):
    ratio_st = ag_means[i] / ch_means[i] if ch_means[i] > 0 else 1.0
    ax3.text(x_st[i], max(ag_means[i], ch_means[i]) + 80, f"Rasio: {ratio_st:.2f}", ha='center', fontsize=8.5, fontweight='bold')

plt.tight_layout()
png_out = FIGURES_DIR / "ds09_macro_climate_and_chirps.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik iklim makro dan validasi CHIRPS berhasil disimpan ke: {png_out}")
'''
    nb.cells[7].source = code_nb09_plot
    nbformat.write(nb, p)
    print("Updated 09_climate_covariates_and_chirps.ipynb with fixed 3-panel audit figure!")

if __name__ == "__main__":
    update_nb07()
    update_nb09()
