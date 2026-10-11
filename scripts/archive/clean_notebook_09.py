"""
Script: clean_notebook_09.py
Purpose: Clean notebook 09 from outdated claims and integrate 27-unit CHIRPS audit v2.
"""

import json
from pathlib import Path

nb_path = Path("notebook/09_climate_covariates_and_chirps.ipynb")
nb = json.load(open(nb_path, "r", encoding="utf-8"))

# Cell 4: Markdown header
nb['cells'][4]['source'] = [
    "## Phase 4 — Validasi Presipitasi Independen AgERA5 vs CHIRPS v2 (Resolusi Audit A2 / B3)\n",
    "Melakukan evaluasi bias presipitasi dan korelasi anomali bulanan antara AgERA5 (reanalisis model ECMWF) dan CHIRPS v2 (sensor satelit inframerah terkalibrasi stasiun) pada 27 unit kabupaten/kota di Jawa Barat.\n",
    "\n",
    "> [!IMPORTANT]\n",
    "> **Catatan Rekonsiliasi Audit A2**:\n",
    "> 1. **Definisi Lokasi**: CHIRPS adalah produk kisi satelit beresolusi 0.05°, bukan stasiun tunggal. Label kolom dibakukan menjadi `Lokasi`.\n",
    "> 2. **Koreksi Tasikmalaya**: Rata-rata 4.465,7 mm adalah rata-rata **3 tahun benchmark** (2016, 2020, 2024), bukan rata-rata 10 tahun.\n",
    "> 3. **Bias Orografis Bandung Raya**: AgERA5 memiliki bias positif tajam di Bandung Raya (+33% s.d. +61%) terutama pada Musim Hujan (+72%), sehingga menempati peringkat terbasah di AgERA5. Sebaliknya, CHIRPS menempatkan Bogor dan Pangandaran sebagai wilayah terbasah.\n",
    "> 4. **Korelasi Anomali Deseasonalized**: Korelasi Pearson anomali bulanan (z-score kalender) berada di kisaran r = 0.50 s.d. 0.80 (median ~0.73), bukan r = 0.91 (yang sebelumnya terdistorsi siklus musiman mentah).\n"
]

# Cell 5: Code table
cell_5_code = """# Memuat hasil audit komprehensif 27 unit dari b3_rainfall_bias_chirps_audit_v2.csv
audit_file = PROJECT_ROOT / "reports" / "dataset_audit" / "b3_rainfall_bias_chirps_audit_v2.csv"
df_b3_audit = pd.read_csv(audit_file)

# Tampilkan ringkasan 27 unit kabupaten/kota (Kolom Lokasi resmi)
cols_display = [
    "lokasi", "elevasi_dem_m", "n_tahun_overlap", 
    "mean_tahunan_chirps_mm", "mean_tahunan_agera5_mm", 
    "bias_persen_signed_mean", "bias_musim_hujan_mh_pct", "bias_musim_kemarau_mk_pct", 
    "korelasi_pearson_anomali"
]

print("="*95)
print("📋 [TABEL AUDIT REKONSILIASI A2] EVALUASI BIAS AGERA5 VS SATELIT CHIRPS v2 (27 UNIT JAWA BARAT):")
print("="*95)
display(df_b3_audit[cols_display])
"""
nb['cells'][5]['source'] = [line + "\n" for line in cell_5_code.splitlines()]

# Cell 7: Multi-panel plot
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

# --- PANEL 2: VALIDASI SILANG PRESIFITASI BENCHMARK TASIKMALAYA ---
years_bench = [2016, 2020, 2024]
r_tasik = df_b3_audit[df_b3_audit["lokasi"] == "KABUPATEN TASIKMALAYA"].iloc[0]
ag_tasik_vals = [r_tasik["agera5_2016_mm"], r_tasik["agera5_2020_mm"], r_tasik["agera5_2024_mm"]]
ch_tasik_vals = [r_tasik["chirps_2016_mm"], r_tasik["chirps_2020_mm"], r_tasik["chirps_2024_mm"]]

w_b = 0.35
x_bench = np.arange(len(years_bench))
ax2.bar(x_bench - w_b/2, ag_tasik_vals, width=w_b, label='AgERA5 (ECMWF)', color='#1d3557', edgecolor='black', alpha=0.85)
ax2.bar(x_bench + w_b/2, ch_tasik_vals, width=w_b, label='CHIRPS v2', color='#2a9d8f', edgecolor='black', alpha=0.85)
ax2.set_xticks(x_bench)
ax2.set_xticklabels(years_bench, fontsize=9.5)
ax2.set_title("Presipitasi Tasikmalaya: 3 Tahun Benchmark\\n(Rata-rata CHIRPS 3-Thn: 4.465,7 mm; AgERA5: 3.852,4 mm)", fontsize=10.5, fontweight='bold')
ax2.set_ylabel("Presipitasi Tahunan (mm)", fontsize=10)
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)
for i in range(len(years_bench)):
    diff_pct = (ag_tasik_vals[i] - ch_tasik_vals[i]) / ch_tasik_vals[i] * 100.0
    ax2.text(x_bench[i], max(ag_tasik_vals[i], ch_tasik_vals[i]) + 80, f"{diff_pct:+.1f}%", ha='center', fontsize=8.5, fontweight='bold')

# --- PANEL 3: POLA BIAS SIGNED VS ELEVASI DEM (27 UNIT) ---
sc = ax3.scatter(df_b3_audit["elevasi_dem_m"], df_b3_audit["bias_persen_signed_mean"], 
                 c=df_b3_audit["bias_musim_hujan_mh_pct"], cmap='coolwarm', s=80, edgecolors='black', alpha=0.85, zorder=4)
cbar = plt.colorbar(sc, ax=ax3)
cbar.set_label("Bias MH (%)", fontsize=8.5)
ax3.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.6)
ax3.set_title("Bias Relatif AgERA5 vs CHIRPS vs Elevasi\\n(Gradien Orografis: Overestimasi Tinggi di Dataran Tinggi)", fontsize=10.5, fontweight='bold')
ax3.set_xlabel("Elevasi DEM (meter dpl)", fontsize=10)
ax3.set_ylabel("Signed Bias Tahunan Mean (%)", fontsize=10)
ax3.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds09_macro_climate_and_chirps.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik iklim makro dan validasi CHIRPS berhasil disimpan ke: {png_out}")
"""
nb['cells'][7]['source'] = [line + "\n" for line in cell_7_code.splitlines()]

# Cell 9: Scorecard
cell_9_code = """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS09 — Macro-Climate Covariates (ONI, DMI) & CHIRPS Satellite Validation"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "NOAA CPC (ONI), NOAA PSL (DMI), NOAA CoastWatch (CHIRPS v2)"},
    {"Dimensi Audit": "Cakupan Temporal", "Hasil & Evaluasi": "2015 s.d. 2024 (10 Tahun Penuh ONI/DMI; Benchmark CHIRPS 2016, 2020, 2024)"},
    {"Dimensi Audit": "Resolusi", "Hasil & Evaluasi": "Bulanan (ONI, DMI) & Harian 0.05° (CHIRPS v2)"},
    {"Dimensi Audit": "Status Rekonsiliasi A2/B3", "Hasil & Evaluasi": "CLOSED (Klaim 4.466 mm Tasikmalaya dikoreksi sebagai rata-rata 3 tahun; bias orografis Bandung Raya teridentifikasi +33% s.d. +61%)"},
    {"Dimensi Audit": "Interpretasi Bukti", "Hasil & Evaluasi": "Konsisten dengan pola spasial satelit bahwa dataran tinggi Jawa Barat basah, namun reanalisis AgERA5 cenderung overestimasi di pegunungan dan underestimasi di Bogor"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Digunakan sebagai kontrol makro dan validasi bias spasial)"}
])
display(scorecard)
"""
nb['cells'][9]['source'] = [line + "\n" for line in cell_9_code.splitlines()]

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook 09 updated successfully: {nb_path}")
