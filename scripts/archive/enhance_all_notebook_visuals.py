"""
Script to enhance notebook visualizations according to data-scientist skill standards:
- 01_AgERA5: Distinct labels for all 27 Kab/Kota, proper legend, data value annotations, taller figure.
- 05_subang_maize: Broaden to Seluruh Jawa Barat 27 Kab/Kota as primary, Subang as structural break case study.
- 07_soybean: Real polygon boundary of West Java from GeoJSON + 27 centroids overlay.
- 09_climate: Real calendar dates/years on x-axis (no raw index 0,20,40), El Nino / La Nina color shading.
"""
import json
from pathlib import Path

# ==========================================
# 1. UPDATE NOTEBOOK 01 (AgERA5 Visuals)
# ==========================================
nb01_path = Path("notebook/01_AgERA5.ipynb")
with open(nb01_path, "r", encoding="utf-8") as f:
    nb01 = json.load(f)

cell7_source_01 = """import matplotlib.patches as mpatches

# Setting ukuran gambar yang proporsional untuk seluruh 27 Kabupaten/Kota
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 12))

# Format nama yang membedakan Kabupaten dan Kota secara eksplisit agar tidak ada tabrakan nama
def format_wilayah_label(row):
    nama_clean = row['Nama Wilayah'].replace('KABUPATEN ', '').replace('KOTA ', '').title()
    prefix = 'Kab.' if row['Tipe'] == 'KABUPATEN' else 'Kota'
    return f"{prefix} {nama_clean}"

df_summary_all['Label_Peta'] = df_summary_all.apply(format_wilayah_label, axis=1)

# --- PANEL 1: PERINGKAT CURAH HUJAN TAHUNAN (27 WILAYAH LENGKAP) ---
df_sorted_rain = df_summary_all.sort_values("Curah Hujan Rata-rata (mm/thn)", ascending=True).reset_index(drop=True)
colors_rain = ['#2a9d8f' if t == 'KABUPATEN' else '#e76f51' for t in df_sorted_rain['Tipe']]

bars1 = ax1.barh(range(len(df_sorted_rain)), df_sorted_rain['Curah Hujan Rata-rata (mm/thn)'], 
                 color=colors_rain, alpha=0.85, edgecolor='black', height=0.7)
ax1.set_yticks(range(len(df_sorted_rain)))
ax1.set_yticklabels(df_sorted_rain['Label_Peta'], fontsize=9.5)
ax1.set_title("Peringkat Curah Hujan Tahunan AgERA5 (mm/tahun, 2015–2024)\\n(27 Kabupaten/Kota Se-Jawa Barat)", fontsize=11, fontweight='bold')
ax1.set_xlabel("Akumulasi Curah Hujan Rata-rata (mm / tahun)", fontsize=10)
ax1.grid(axis='x', linestyle='--', alpha=0.5)
ax1.set_xlim(0, df_sorted_rain['Curah Hujan Rata-rata (mm/thn)'].max() * 1.15)

# Label angka nilai di ujung setiap bar
for bar, val in zip(bars1, df_sorted_rain['Curah Hujan Rata-rata (mm/thn)']):
    ax1.text(val + 35, bar.get_y() + bar.get_height()/2, f"{val:,.0f} mm", 
             va='center', ha='left', fontsize=8.5, fontweight='bold', color='#1d3557')

# --- PANEL 2: PERINGKAT SUHU RATA-RATA 24 JAM (27 WILAYAH LENGKAP) ---
df_sorted_temp = df_summary_all.sort_values("T_Mean (°C)", ascending=True).reset_index(drop=True)
colors_temp = ['#457b9d' if t == 'KABUPATEN' else '#e63946' for t in df_sorted_temp['Tipe']]

bars2 = ax2.barh(range(len(df_sorted_temp)), df_sorted_temp['T_Mean (°C)'], 
                 color=colors_temp, alpha=0.85, edgecolor='black', height=0.7)
ax2.set_yticks(range(len(df_sorted_temp)))
ax2.set_yticklabels(df_sorted_temp['Label_Peta'], fontsize=9.5)
ax2.set_title("Peringkat Suhu Rata-rata 24 Jam AgERA5 (°C, 2015–2024)\\n(27 Kabupaten/Kota Se-Jawa Barat)", fontsize=11, fontweight='bold')
ax2.set_xlabel("Suhu Udara Rata-rata (°C)", fontsize=10)
ax2.grid(axis='x', linestyle='--', alpha=0.5)
ax2.set_xlim(0, df_sorted_temp['T_Mean (°C)'].max() * 1.18)

# Label angka nilai di ujung setiap bar
for bar, val in zip(bars2, df_sorted_temp['T_Mean (°C)']):
    ax2.text(val + 0.35, bar.get_y() + bar.get_height()/2, f"{val:.1f} °C", 
             va='center', ha='left', fontsize=8.5, fontweight='bold', color='#1d3557')

# --- LEGEND KETERANGAN WARNA EKSPLISIT ---
patch_kab = mpatches.Patch(facecolor='#2a9d8f', edgecolor='black', label='Kabupaten (18 Wilayah Sentra Pertanian)')
patch_kota = mpatches.Patch(facecolor='#e76f51', edgecolor='black', label='Kota (9 Wilayah Urban / Konsumsi)')
ax1.legend(handles=[patch_kab, patch_kota], loc='lower right', framealpha=0.9, fontsize=9.5)

patch_kab_t = mpatches.Patch(facecolor='#457b9d', edgecolor='black', label='Kabupaten (Sentra Pertanian Dataran Rendah/Tinggi)')
patch_kota_t = mpatches.Patch(facecolor='#e63946', edgecolor='black', label='Kota (Entitas Urban Panas/Sedang)')
ax2.legend(handles=[patch_kab_t, patch_kota_t], loc='lower right', framealpha=0.9, fontsize=9.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds01_all_27_kabkota_climate.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik iklim 27 Kab/Kota berhasil disimpan ke: {png_out}")
"""

nb01['cells'][7]['source'] = [line + "\n" for line in cell7_source_01.strip().split("\n")]
with open(nb01_path, "w", encoding="utf-8") as f:
    json.dump(nb01, f, indent=1)
print("Updated notebook 01 visual code successfully!")


# ==========================================
# 2. UPDATE NOTEBOOK 05 (Maize Visuals & Scope)
# ==========================================
nb05_path = Path("notebook/05_subang_maize_productivity.ipynb")
with open(nb05_path, "r", encoding="utf-8") as f:
    nb05 = json.load(f)

# Update Title and intro
nb05['cells'][0]['source'] = [
    "# 05 — Produktivitas Jagung 27 Kabupaten/Kota Jawa Barat (2015–2022)\n",
    "**TaniAdapt Project — Secondary Cereal Crop & Yield Stability Model (DS05)**\n",
    "**Fase:** Phase 3 (Acquisition) + Phase 4 (Quality Audit & Structural Break Analysis)\n",
    "\n",
    "- **Sumber Resmi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Jawa Barat / Open Data Jabar\n",
    "- **Cakupan Spasial Lengkap:** **27 Kabupaten/Kota Se-Jawa Barat** (Bukan hanya Subang; mencakup seluruh sentra Garut, Majalengka, Cianjur, Tasikmalaya, dll.)\n",
    "- **Periode Observasi:** 2015 s.d. 2022 ($N = 216$ observasi penuh, 8 tahun berturut-turut)\n",
    "- **Studi Kasus Khusus:** Dekomposisi detrending & investigasi lonjakan Kabupaten Subang (+56.4% pada 2021-2022) sebagai anomali metodologis/benih hibrida.\n"
]

cell5_source_05 = """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5.5), gridspec_kw={'width_ratios': [1.1, 1.2]})

# Panel 1: Runtun Waktu Sentra Utama vs Rata-rata Jawa Barat
mean_jabar = df_maize.groupby('tahun')['produktivitas_jagung'].mean()
garut_data = df_maize[df_maize['nama_kabupaten_kota'].str.contains('GARUT')].sort_values('tahun')

ax1.plot(mean_jabar.index, mean_jabar.values, marker='o', label='Rata-rata Jawa Barat', color='black', linewidth=2.5)
ax1.plot(garut_data['tahun'], garut_data['produktivitas_jagung'], marker='^', label='Kab. Garut (Sentra Terbesar)', color='forestgreen', linewidth=2)
ax1.plot(subang_data['tahun'], subang_data['produktivitas_jagung'], marker='s', label='Kab. Subang (Realisasi Melonjak)', color='darkorange', linewidth=2.5)
ax1.plot(x_sub, y_pred_sub, linestyle='--', color='red', alpha=0.7, label=f'Tren Linier Subang (+{p_sub[0]:.2f} ku/ha/thn)')

# Anotasi Structural Break
ax1.annotate('Lonjakan Subang\\n(+56.4% dlm 2 thn)', xy=(2022, 89.49), xytext=(2018.5, 78),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.6))

ax1.set_title("Dinamika Produktivitas Jagung Jawa Barat (2015–2022)", fontsize=11, fontweight='bold')
ax1.set_xlabel("Tahun Observasi", fontsize=10)
ax1.set_ylabel("Produktivitas (Kuintal / Hektar)", fontsize=10)
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Ranking Produktivitas Jagung Rata-rata 27 Kabupaten/Kota Se-Jawa Barat
jabar_ranking = df_maize.groupby('nama_kabupaten_kota')['produktivitas_jagung'].mean().sort_values(ascending=True)
jabar_ranking.index = [n.replace('KABUPATEN ', 'Kab. ').replace('KOTA ', 'Kota ').title() for n in jabar_ranking.index]

bar_colors = ['darkorange' if 'Subang' in name else ('forestgreen' if 'Garut' in name else '#457b9d') for name in jabar_ranking.index]
bars_j = ax2.barh(range(len(jabar_ranking)), jabar_ranking.values, color=bar_colors, edgecolor='black', alpha=0.85, height=0.7)
ax2.set_yticks(range(len(jabar_ranking)))
ax2.set_yticklabels(jabar_ranking.index, fontsize=8)
ax2.set_title("Peringkat Rata-rata Produktivitas Jagung (2015–2022)\\nSeluruh 27 Kabupaten/Kota Se-Jawa Barat", fontsize=11, fontweight='bold')
ax2.set_xlabel("Rata-rata Produktivitas (Kuintal / Hektar)", fontsize=10)
ax2.grid(axis='x', linestyle='--', alpha=0.5)

# Legend penjelasan warna
patch_std = mpatches.Patch(facecolor='#457b9d', edgecolor='black', label='Kabupaten/Kota Lain di Jabar')
patch_garut = mpatches.Patch(facecolor='forestgreen', edgecolor='black', label='Kab. Garut (Sentra Terbesar)')
patch_subang = mpatches.Patch(facecolor='darkorange', edgecolor='black', label='Kab. Subang (Kasus Anomali Lonjakan)')
ax2.legend(handles=[patch_garut, patch_subang, patch_std], loc='lower right', fontsize=8.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds05_maize_coverage.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""

nb05['cells'][5]['source'] = [line + "\n" for line in cell5_source_05.strip().split("\n")]
with open(nb05_path, "w", encoding="utf-8") as f:
    json.dump(nb05, f, indent=1)
print("Updated notebook 05 visual code successfully!")


# ==========================================
# 3. UPDATE NOTEBOOK 07 (Soybean & GeoJSON Map)
# ==========================================
nb07_path = Path("notebook/07_soybean_and_spatial_geoboundaries.ipynb")
with open(nb07_path, "r", encoding="utf-8") as f:
    nb07 = json.load(f)

cell11_source_07 = """import geopandas as gpd

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5), gridspec_kw={'width_ratios': [1, 1.3]})

# Panel 1: Tren Produktivitas Kedelai Sentra Utama
top_sentra = ["KABUPATEN GARUT", "KABUPATEN SUKABUMI", "KABUPATEN MAJALENGKA", "KABUPATEN CIANJUR", "KABUPATEN CIAMIS"]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for kab, c in zip(top_sentra, colors):
    sub = df_ked[df_ked['nama_kabupaten_kota'] == kab].sort_values('tahun')
    ax1.plot(sub['tahun'], sub['produktivitas_kedelai'], marker='o', label=kab.replace('KABUPATEN ', ''), color=c, linewidth=2)

ax1.set_title("Tren Produktivitas Kedelai Sentra Utama Jawa Barat (2015–2022)", fontsize=11, fontweight='bold')
ax1.set_xlabel("Tahun", fontsize=10)
ax1.set_ylabel("Produktivitas (Kuintal / Hektar)", fontsize=10)
ax1.legend(loc='upper right', fontsize=8.5)
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Peta Geospasial Berbentuk Poligon Batas Provinsi Jawa Barat + Centroid 27 Kab/Kota
path_jabar_geojson = RAW_DIR / "jawa_barat_provinsi.geojson"

if path_jabar_geojson.exists():
    gdf_jabar = gpd.read_file(path_jabar_geojson)
    gdf_jabar.plot(ax=ax2, color='#f8f9fa', edgecolor='#212529', linewidth=1.5, alpha=0.9, zorder=1)
    ax2.set_facecolor('#e9ecef') # Latar belakang laut/wilayah sekitar
else:
    ax2.grid(True, linestyle='--', alpha=0.5)

# Overlay titik-titik centroid 27 Kabupaten/Kota
if 'df_centroids' in locals() and df_centroids is not None:
    # Pisahkan Kabupaten dan Kota
    kab_pts = df_centroids[df_centroids['tipe_wilayah'] == 'KABUPATEN']
    kota_pts = df_centroids[df_centroids['tipe_wilayah'] == 'KOTA']
    
    # Plot Kabupaten dengan ukuran sebanding sel AgERA5
    sc1 = ax2.scatter(kab_pts['true_centroid_lon'], kab_pts['true_centroid_lat'], 
                      s=kab_pts['n_sel_agera5_0_1deg'] * 12 + 40, c='#2a9d8f', edgecolors='black', 
                      alpha=0.85, label='Kabupaten (Area Sel AgERA5)', zorder=3)
    
    # Plot Kota sebagai penanda oranye
    sc2 = ax2.scatter(kota_pts['true_centroid_lon'], kota_pts['true_centroid_lat'], 
                      s=50, c='#e76f51', marker='s', edgecolors='black', 
                      alpha=0.9, label='Kota (Centroid Urban)', zorder=3)
    
    # Label nama sentra utama kedelai dan wilayah besar
    key_labels = ['BANDUNG', 'GARUT', 'SUKABUMI', 'CIANJUR', 'INDRAMAYU', 'SUBANG', 'CIREBON', 'MAJALENGKA', 'CIAMIS', 'BOGOR']
    for _, row in df_centroids.iterrows():
        clean_n = row['nama_kabupaten_kota'].replace('KABUPATEN ', '').replace('KOTA ', '')
        if clean_n in key_labels:
            ax2.annotate(clean_n.title(), (row['true_centroid_lon'], row['true_centroid_lat']),
                         textcoords="offset points", xytext=(0, 6), ha='center', fontsize=7.5, fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7), zorder=4)

ax2.set_title("Peta Batas Geospasial Jawa Barat & Sebaran Centroid 27 Kab/Kota", fontsize=11, fontweight='bold')
ax2.set_xlabel("Bujur Geografis (Longitude °E)", fontsize=10)
ax2.set_ylabel("Lintang Geografis (Latitude °S)", fontsize=10)
ax2.set_xlim(106.2, 109.0)
ax2.set_ylim(-7.9, -5.8)
ax2.legend(loc='lower left', framealpha=0.9, fontsize=9)

plt.tight_layout()
png_out = FIGURES_DIR / "ds07_soybean_and_spatial.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik geospasial Jawa Barat berhasil disimpan ke: {png_out}")
"""

nb07['cells'][11]['source'] = [line + "\n" for line in cell11_source_07.strip().split("\n")]
with open(nb07_path, "w", encoding="utf-8") as f:
    json.dump(nb07, f, indent=1)
print("Updated notebook 07 visual code successfully!")


# ==========================================
# 4. UPDATE NOTEBOOK 09 (Climate ONI X-Axis)
# ==========================================
nb09_path = Path("notebook/09_climate_covariates_and_chirps.ipynb")
with open(nb09_path, "r", encoding="utf-8") as f:
    nb09 = json.load(f)

cell7_source_09 = """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5.5))

# --- PANEL 1: RUN TUN WAKTU ONI DENGAN TAHUN KALENDER INFORMATIF (BUKAN INDEKS 0-20-40) ---
df_oni_plot = df_oni_recent.reset_index(drop=True)
n_obs = len(df_oni_plot)

# Buat sumbu x berbasis tahun desimal kalender yang akurat
# Tiap tahun memiliki 12 observasi musim (DJF, JFM, FMA, dst.)
x_years = [df_oni_plot['YR'].iloc[i] + (i % 12) / 12.0 for i in range(n_obs)]
anom_vals = df_oni_plot['ANOM'].values

ax1.plot(x_years, anom_vals, color='#1d3557', linewidth=2, label='NOAA ONI (Niño 3.4 SST Anom)', zorder=4)
ax1.axhline(0.5, color='crimson', linestyle='--', linewidth=1.2, alpha=0.8, label='Ambang El Niño (+0.5°C)')
ax1.axhline(-0.5, color='royalblue', linestyle='--', linewidth=1.2, alpha=0.8, label='Ambang La Niña (-0.5°C)')
ax1.axhline(0.0, color='gray', linestyle='-', alpha=0.5)

# Shading warna informatif untuk fase El Nino (merah muda) dan La Nina (biru muda)
ax1.fill_between(x_years, anom_vals, 0.5, where=(anom_vals >= 0.5), color='crimson', alpha=0.25, label='Fase El Niño (Kering)')
ax1.fill_between(x_years, anom_vals, -0.5, where=(anom_vals <= -0.5), color='royalblue', alpha=0.25, label='Fase La Niña (Basah)')

# Anotasi peristiwa iklim ekstrem riil
ax1.annotate('Super El Niño\\n2015/2016 (+2.6°C)', xy=(2015.8, 2.5), xytext=(2016.2, 2.3),
             arrowprops=dict(facecolor='crimson', shrink=0.08, width=1, headwidth=5),
             fontsize=8.5, fontweight='bold', color='darkred')

ax1.annotate('Triple-Dip La Niña\\n2020–2022', xy=(2021.5, -1.0), xytext=(2019.5, -1.3),
             arrowprops=dict(facecolor='royalblue', shrink=0.08, width=1, headwidth=5),
             fontsize=8.5, fontweight='bold', color='darkblue')

ax1.annotate('El Niño 2023/2024\\n(+2.0°C)', xy=(2023.9, 1.9), xytext=(2022.0, 1.8),
             arrowprops=dict(facecolor='crimson', shrink=0.08, width=1, headwidth=5),
             fontsize=8.5, fontweight='bold', color='darkred')

# Format sumbu x agar menampilkan tahun kalender jelas (2015 s.d. 2024)
unique_years = sorted(df_oni_plot['YR'].unique())
ax1.set_xticks(unique_years)
ax1.set_xticklabels([str(y) for y in unique_years], rotation=0, fontsize=9.5)
ax1.set_title("Dinamika Iklim Makro Pasifik: Oceanic Niño Index (2015–2024)\\n(Kalender Waktu Nyata, Shading Fase El Niño / La Niña)", fontsize=11, fontweight='bold')
ax1.set_ylabel("Anomali Suhu Muka Laut Niño 3.4 (°C)", fontsize=10)
ax1.set_xlabel("Tahun Kalender Observasi", fontsize=10)
ax1.legend(loc='lower left', fontsize=8, framealpha=0.9)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlim(2015, 2025)

# --- PANEL 2: VALIDASI SILANG HUJAN TASIKMALAYA AGERA5 VS CHIRPS V2 ---
tasik_ch = pd.read_csv(chirps_dir / "chirps_tasikmalaya_2015_2024.csv", skiprows=[1])
tasik_ch['year'] = pd.to_datetime(tasik_ch['time']).dt.year
ch_ann = tasik_ch.groupby('year')['precip'].sum()

f_tasik_ag = agera5_dir / "agera5_kab_tasikmalaya_2015_2024.csv"
if not f_tasik_ag.exists():
    f_tasik_ag = agera5_dir / "agera5_tasikmalaya_2015_2024.csv"
tasik_ag = pd.read_csv(f_tasik_ag)
tasik_ag['year'] = pd.to_datetime(tasik_ag['valid_time']).dt.year
ag_ann = tasik_ag.groupby('year')['Precipitation_Flux'].sum()

years = sorted(list(set(ch_ann.index).intersection(set(ag_ann.index))))
x = np.arange(len(years))
width = 0.38

bars_ag = ax2.bar(x - width/2, [ag_ann[y] for y in years], width, label='AgERA5 (ECMWF Reanalysis)', color='#264653', alpha=0.9, edgecolor='black')
bars_ch = ax2.bar(x + width/2, [ch_ann[y] for y in years], width, label='CHIRPS v2 (Satelit + Stasiun Gauge)', color='#2a9d8f', alpha=0.9, edgecolor='black')

ax2.set_title("Validasi Silang Hujan Tasikmalaya: AgERA5 vs CHIRPS v2\\n(Konfirmasi Efek Orografis Nyata >4.000 mm/tahun)", fontsize=11, fontweight='bold')
ax2.set_xlabel("Tahun Kalender", fontsize=10)
ax2.set_ylabel("Akumulasi Curah Hujan (mm / tahun)", fontsize=10)
ax2.set_xticks(x)
ax2.set_xticklabels(years, rotation=0, fontsize=9.5)
ax2.legend(loc='upper right', fontsize=8.5, framealpha=0.9)
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds09_macro_climate_and_chirps.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik iklim makro & CHIRPS berhasil disimpan ke: {png_out}")
"""

nb09['cells'][7]['source'] = [line + "\n" for line in cell7_source_09.strip().split("\n")]
with open(nb09_path, "w", encoding="utf-8") as f:
    json.dump(nb09, f, indent=1)
print("Updated notebook 09 visual code successfully!")
