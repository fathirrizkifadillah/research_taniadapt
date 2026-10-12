import nbformat as nbf
from pathlib import Path

p = Path("notebook/09_climate_covariates_and_chirps.ipynb")
nb = nbf.read(p, as_version=4)

cell_7_code = """fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5), gridspec_kw={'width_ratios': [1.1, 1, 1]})

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

# --- PANEL 2: VALIDASI SILANG PRESIPITASI BENCHMARK TASIKMALAYA ---
years_bench = [2016, 2020, 2024]
df_chirps_val_temp = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "chirps_agera5_validation.csv")
tasik_val = df_chirps_val_temp[df_chirps_val_temp["nama_kabupaten_kota"] == "KABUPATEN TASIKMALAYA"].groupby("year")[["Precipitation_Flux", "precip"]].sum()
ag_tasik_vals = [tasik_val.loc[y, "Precipitation_Flux"] for y in years_bench]
ch_tasik_vals = [tasik_val.loc[y, "precip"] for y in years_bench]

w_b = 0.35
x_bench = np.arange(len(years_bench))
ax2.bar(x_bench - w_b/2, ag_tasik_vals, width=w_b, label='AgERA5 (ECMWF)', color='#1d3557', edgecolor='black', alpha=0.85)
ax2.bar(x_bench + w_b/2, ch_tasik_vals, width=w_b, label='CHIRPS v2', color='#2a9d8f', edgecolor='black', alpha=0.85)
ax2.set_xticks(x_bench)
ax2.set_xticklabels(years_bench, fontsize=9.5)
ax2.set_title("Presipitasi Tasikmalaya: 3 Tahun Benchmark\\n(Validasi Silang AgERA5 vs CHIRPS v2)", fontsize=10.5, fontweight='bold')
ax2.set_ylabel("Presipitasi Tahunan (mm)", fontsize=10)
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)
for i in range(len(years_bench)):
    diff_pct = (ag_tasik_vals[i] - ch_tasik_vals[i]) / ch_tasik_vals[i] * 100.0
    ax2.text(x_bench[i], max(ag_tasik_vals[i], ch_tasik_vals[i]) + 80, f"{diff_pct:+.1f}%", ha='center', fontsize=8.5, fontweight='bold')

# --- PANEL 3: POLA BIAS SIGNED VS ELEVASI DEM (27 UNIT) ---
df_cells_temp = pd.read_csv(PROJECT_ROOT / "reports" / "dataset_audit" / "a8_spatial_grid_cells_audit.csv")
df_b3_merged = pd.merge(df_b3_audit, df_cells_temp[["nama_kabupaten_kota", "dem_elevation_m"]], on="nama_kabupaten_kota", how="left")

sc = ax3.scatter(df_b3_merged["dem_elevation_m"], df_b3_merged["signed_bias_overall_pct"], 
                 c=df_b3_merged["bias_mh_wet_pct"], cmap='coolwarm', s=80, edgecolors='black', alpha=0.85, zorder=4)
cbar = plt.colorbar(sc, ax=ax3)
cbar.set_label("Bias MH (%)", fontsize=8.5)
ax3.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.6)
ax3.set_title("Bias Relatif AgERA5 vs CHIRPS vs Elevasi\\n(Gradien Orografis: Overestimasi Tinggi di Dataran Tinggi)", fontsize=10.5, fontweight='bold')
ax3.set_xlabel("Elevasi DEM (meter dpl)", fontsize=10)
ax3.set_ylabel("Signed Bias Tahunan Mean (%)", fontsize=10)
ax3.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
png_out = FIGURES_DIR / "ds09_macro_climate_and_chirps.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik iklim makro dan validasi CHIRPS berhasil disimpan ke: {png_out}")
"""

nb.cells[7].source = cell_7_code
nbf.write(nb, p)
print("Updated cell 7 in nb09 successfully!")
