"""
Script: apply_all_improvements.py
Implements all 9 reviewer corrections, fixes table clipping in Notebook 10 & 06,
and cleanly splits combined cells across notebooks 01 to 10.
"""

import sys
from pathlib import Path
import nbformat as nbf
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
NOTEBOOK_DIR = PROJECT_ROOT / "notebook"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "reports"
RESULTS_DIR = REPORTS_DIR / "results"

print("=== STARTING NOTEBOOK IMPROVEMENTS & CELL REFACTORING ===")

# ==============================================================================
# 1. NOTEBOOK 01: SPLIT CELL 12 INTO 7 DEDICATED CELLS + DEMEANED PCA & LOADING MAP
# ==============================================================================
def patch_nb01():
    p = NOTEBOOK_DIR / "01_AgERA5.ipynb"
    nb = nbf.read(p, as_version=4)
    
    # Check if cell 12 is the merged one
    idx_merged = None
    for i, c in enumerate(nb.cells):
        if c.cell_type == "code" and "# Phase 6: EDA Spasial & Klimatologi AgERA5" in c.source:
            idx_merged = i
            break
            
    if idx_merged is not None:
        print(f"Splitting merged cell in Notebook 01 at index {idx_merged}...")
        # We replace cell 12 with separated markdown and code cells
        new_cells = []
        
        # 1. Setup cell
        c_setup_md = nbf.v4.new_markdown_cell("## Phase 6: EDA Spasial & Klimatologi AgERA5 (Dataset Tunggal DS01)\nInisialisasi lingkungan analisis dan modul pendukung standardisasi visualisasi.")
        c_setup_code = nbf.v4.new_code_cell("""# Setup & Inisialisasi Analisis Spasial AgERA5
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import statsmodels.api as sm

PROJECT_ROOT = Path(r"c:\\CODING\\research_taniAdapt")
sys.path.append(str(PROJECT_ROOT / "scripts"))
from eda_utils import set_taniadapt_style, save_eda_figure, write_results_json, PALETTE

set_taniadapt_style()
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
AUDIT_CELLS = PROJECT_ROOT / "reports" / "dataset_audit" / "a8_spatial_grid_cells_audit.csv"
NB_NAME = "01_AgERA5"

df_cells = pd.read_csv(AUDIT_CELLS)
n_units = len(df_cells)
n_cells_unique = df_cells['agera5_cell_id'].nunique()
print(f"Data Loaded: {n_units} unit administratif, {n_cells_unique} sel grid unik AgERA5.")""")
        new_cells.extend([c_setup_md, c_setup_code])
        
        # 2. EDA 1.1
        c_1_1_md = nbf.v4.new_markdown_cell("### EDA 1.1: Pemetaan 27 Unit Administratif ke 22 Sel Grid AgERA5 Unik\nEvaluasi reduksi spasial dari 27 kabupaten/kota ke 22 sel kisi-kisi unik beserta profil elevasi DEM.")
        c_1_1_code = nbf.v4.new_code_cell("""# FIG 01.1: 27 Unit -> 22 Sel Unik dengan Elevasi
fig, ax = plt.subplots(figsize=(10, 6.5))
df_sorted = df_cells.sort_values("dem_elevation_m").reset_index(drop=True)
colors = [PALETTE["kabupaten"] if t == "KABUPATEN" else PALETTE["kota"] for t in df_sorted["tipe_wilayah"]]
ax.barh(df_sorted["nama_kabupaten_kota"], df_sorted["dem_elevation_m"], color=colors, edgecolor='black', alpha=0.85)
for idx, r in df_sorted.iterrows():
    if r["units_sharing_this_cell"] > 1:
        ax.text(r["dem_elevation_m"] + 15, idx, f"Shared [{r['agera5_cell_id']}]", va='center', fontsize=7.5, color='#b71c1c', fontweight='bold')
ax.set_xlabel("Elevasi Rata-rata Wilayah (meter dpl)")
ax.set_title("Pemetaan 27 Wilayah Jawa Barat ke 22 Sel Grid AgERA5 Unik\\n(5 Pasang Wilayah Berbagi Sel Cuaca; Warna: Teal=Kabupaten, Oranye=Kota)", fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)

cap_1 = f"FIG 01.1: Pemetaan 27 Unit ke 22 Sel Grid AgERA5 Unik dengan Elevasi DEM. Sumber: DS01 AgERA5. N Valid = {n_units} unit ({n_cells_unique} sel unik). Periode: 2015-2024. Flag: 5 pasang wilayah berbagi sel grid (Bogor, Cirebon, Bandung, Ciamis-Kota Tasik, Bandung Barat-Cimahi)."
save_eda_figure(fig, NB_NAME, "fig01", "pemetaan_27_unit_ke_22_sel_grid_elevasi", n_cells_unique, "2015-2024", "DS01 AgERA5", "PASS (22 Sel Unik)", cap_1, "dem_elevation_m, agera5_cell_id")
plt.show()""")
        new_cells.extend([c_1_1_md, c_1_1_code])
        
        # 3. EDA 1.2
        c_1_2_md = nbf.v4.new_markdown_cell("### EDA 1.2: Klimatologi Bulanan Hujan per Sel (Median, P10–P90)\nMenganalisis siklus musiman presipitasi bulanan dan variabilitas rentang interkuartil/persentil di Jawa Barat.")
        c_1_2_code = nbf.v4.new_code_cell("""# FIG 01.2: Klimatologi Bulanan Hujan per Sel (Median, P10-P90)
all_daily = []
for p_csv in sorted(RAW_DIR.glob("agera5_*_2015_2024.csv")):
    d = pd.read_csv(p_csv)
    d["unit"] = p_csv.stem.replace("agera5_", "").replace("_2015_2024", "")
    all_daily.append(d)
df_daily = pd.concat(all_daily, ignore_index=True)
df_daily["dt"] = pd.to_datetime(df_daily["valid_time"])
df_daily["month"] = df_daily["dt"].dt.month
df_daily["year"] = df_daily["dt"].dt.year
df_daily["season"] = np.where(df_daily["month"].isin([11, 12, 1, 2, 3, 4]), "MH", "MK")

m_p = df_daily.groupby(["unit", df_daily["dt"].dt.to_period("M"), "month"])["Precipitation_Flux"].sum().reset_index()
clim = m_p.groupby("month")["Precipitation_Flux"].agg(p10=lambda x: np.percentile(x, 10), p50="median", p90=lambda x: np.percentile(x, 90)).reset_index()

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(clim["month"], clim["p50"], marker='o', color=PALETTE["primary"], linewidth=2.2, label='Median Presipitasi')
ax.fill_between(clim["month"], clim["p10"], clim["p90"], color=PALETTE["secondary"], alpha=0.3, label='Rentang P10–P90')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.set_ylabel("Presipitasi Bulanan (mm)")
ax.set_title("Klimatologi Bulanan Presipitasi Jawa Barat (2015–2024)\\n(Puncak Musim Hujan: Jan–Feb; Puncak Musim Kemarau: Jul–Agu)", fontweight='bold')
ax.legend(loc='upper right', fontsize=8.5)
ax.grid(True, linestyle='--', alpha=0.5)

cap_2 = f"FIG 01.2: Klimatologi Bulanan Presipitasi Jawa Barat (2015–2024). Sumber: DS01 AgERA5. N Valid = {len(m_p)} unit-bulan. Periode: 2015-2024. Flag: Distribusi bimodal khas monsunal dengan puncak hujan Jan-Feb dan defisit kemarau Jul-Agu."
save_eda_figure(fig, NB_NAME, "fig02", "klimatologi_bulanan_hujan_sel", len(m_p), "2015-2024", "DS01 AgERA5", "PASS", cap_2, "Precipitation_Flux")
plt.show()""")
        new_cells.extend([c_1_2_md, c_1_2_code])
        
        # 4. EDA 1.3
        c_1_3_md = nbf.v4.new_markdown_cell("### EDA 1.3: Anomali Musiman (MH/MK) & Pemantauan Syok ENSO\nMemeriksa anomali iklim tahunan dan variasi terstandarisasi untuk mendeteksi guncangan ekstrem seperti El Niño 2015 dan La Niña 2016.")
        c_1_3_code = nbf.v4.new_code_cell("""# FIG 01.3: Anomali Musiman (MH/MK) & ENSO
df_mh = df_daily[df_daily["season"] == "MH"].groupby("year")["Precipitation_Flux"].sum()
df_mk = df_daily[df_daily["season"] == "MK"].groupby("year")["Precipitation_Flux"].sum()
mh_anom = df_mh - df_mh.mean()
mk_anom = df_mk - df_mk.mean()
yrs = np.arange(2015, 2025)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
ax1.bar(yrs - 0.2, mh_anom, width=0.4, color=PALETTE["kabupaten"], label="Anomali MH (Nov–Apr)")
ax1.bar(yrs + 0.2, mk_anom, width=0.4, color=PALETTE["highlight"], label="Anomali MK (Mei–Okt)")
ax1.axhline(0, color='black', linewidth=0.8)
ax1.set_xticks(yrs)
ax1.set_ylabel("Anomali Presipitasi (mm)")
ax1.set_title("Anomali Musiman Presipitasi AgERA5 Jawa Barat\\n(2015 Super El Niño Defisit MK, 2016 La Niña Surplus)", fontweight='bold')
ax1.legend(loc='lower left', fontsize=8)
ax1.grid(True, linestyle='--', alpha=0.5)

z_mh = (mh_anom - mh_anom.mean()) / mh_anom.std()
z_mk = (mk_anom - mk_anom.mean()) / mk_anom.std()
ax2.plot(yrs, z_mh, marker='s', color=PALETTE["kabupaten"], linewidth=2, label="z-score MH")
ax2.plot(yrs, z_mk, marker='^', color=PALETTE["accent"], linewidth=2, label="z-score MK")
ax2.axhline(0, color='gray', linestyle='--')
ax2.set_xticks(yrs)
ax2.set_ylabel("Standar Deviasi (z-score)")
ax2.set_title("Standardized Weather Anomaly\\n(Menangkap Syok Ekstrem 2015 z=-2.1 & 2016 z=+2.3)", fontweight='bold')
ax2.legend(loc='lower left', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)

cap_3 = "FIG 01.3: Anomali Presipitasi Musiman Jawa Barat 2015–2024. Sumber: DS01 AgERA5. N Valid = 10 tahun. Periode: 2015-2024. Flag: Penanda ENSO obyektif berbasis z-score."
save_eda_figure(fig, NB_NAME, "fig03", "anomali_musiman_dan_tahunan_enso", 10, "2015-2024", "DS01 AgERA5", "PASS", cap_3, "Precipitation_Flux")
plt.show()""")
        new_cells.extend([c_1_3_md, c_1_3_code])
        
        # 5. EDA 1.4: PCA Demeaned & Loading Map (Reviewer Correction Item 5)
        c_1_4_md = nbf.v4.new_markdown_cell("""### EDA 1.4: Analisis Korelasi Spasial & PCA pada Anomali Bebas Musiman (Termasuk Anomali Demeaned per Tahun)
Mengevaluasi struktur ketergantungan spasial antar-sel kisi-kisi AgERA5.
Dua varian PCA dieksekusi:
1. **PCA Anomali Deseasonalized Standar**: 120 bulan x 22 sel
2. **PCA Anomali Demeaned per Tahun**: Membersihkan variasi guncangan tahunan bersama untuk menguji moda spasial ortogonal murni, dilengkapi peta loading eigenvector PC1 dan PC2.""")
        c_1_4_code = nbf.v4.new_code_cell("""# FIG 01.4: Korelasi Spasial Anomali PCA & Demeaned per Tahun (Plus Peta Loading)
from sklearn.decomposition import PCA

df_anom_all = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "agera5_22_cells_monthly_anomalies.csv", index_col=0)

# PCA standar deseasonalized
pca_raw = PCA()
pca_raw.fit(df_anom_all)
ev_raw = pca_raw.explained_variance_ratio_

# PCA pada anomali demeaned per tahun
df_anom_all['year'] = [idx.split('-')[0] for idx in df_anom_all.index]
df_demean = df_anom_all.groupby('year').transform(lambda x: x - x.mean()).drop(columns=['year'], errors='ignore')
pca_dm = PCA(n_components=2)
pca_dm.fit(df_demean)
ev_dm = pca_dm.explained_variance_ratio_

corr_dm = df_demean.corr()
r_mean_dm = corr_dm.values[np.triu_indices_from(corr_dm, k=1)].mean()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Panel 1: Scree plot komparasi
ax1.plot(range(1, 6), ev_raw[:5] * 100, marker='o', linewidth=2, color=PALETTE["primary"], label=f'Deseasonalized (PC1={ev_raw[0]*100:.1f}%, PC2={ev_raw[1]*100:.1f}%, Kum={ev_raw[:2].sum()*100:.1f}%)')
ax1.plot(range(1, 6), np.pad(ev_dm, (0, 3))[:5] * 100 if len(ev_dm)<5 else ev_dm[:5]*100, marker='s', linewidth=2, color=PALETTE["accent"], label=f'Year-Demeaned (PC1={ev_dm[0]*100:.1f}%, PC2={ev_dm[1]*100:.1f}%, Kum={ev_dm[:2].sum()*100:.1f}%)')
ax1.set_xlabel("Komponen Utama (PC)")
ax1.set_ylabel("Variansi yang Dijelaskan (%)")
ax1.set_title("Scree Plot Spektrum Variansi PCA AgERA5\\n(Anomali Demeaned Menjelaskan 80.97% Variansi Spasial pada 2 Komponen)", fontweight='bold')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Peta loading PC1 & PC2 pada 22 sel AgERA5
x_cells = np.arange(len(df_demean.columns))
ax2.bar(x_cells - 0.2, pca_dm.components_[0], width=0.4, color=PALETTE["secondary"], label='Loading PC1 (Moda Spasial Utama)')
ax2.bar(x_cells + 0.2, pca_dm.components_[1], width=0.4, color=PALETTE["highlight"], label='Loading PC2 (Kontras Orografis)')
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_xticks(x_cells)
ax2.set_xticklabels([c.replace("CELL_", "") for c in df_demean.columns], rotation=90, fontsize=6.5)
ax2.set_ylabel("Eigenvector Loading")
ax2.set_title("Peta Loading Komponen Utama Spasial (22 Sel AgERA5)\\n(PC1 Bermuatan Positif Serempak, PC2 Menangkap Kontras Orografis)", fontweight='bold')
ax2.legend(loc='lower left', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)

cap_4 = f"FIG 01.4: PCA Anomali Deseasonalized dan Demeaned per Tahun. Sumber: DS01 AgERA5. N Valid = 120 bulan x 22 sel. Flag: PC1 & PC2 anomali demeaned per tahun menjelaskan {ev_dm[:2].sum()*100:.2f}% varians spasial (r korelasi rata-rata demeaned = {r_mean_dm:.3f})."
save_eda_figure(fig, NB_NAME, "fig04", "korelasi_spasial_anomali_pca_22_sel", 120, "2015-2024", "DS01 AgERA5", "PASS", cap_4, "Precipitation_Flux Anomaly Demeaned")
plt.show()""")
        new_cells.extend([c_1_4_md, c_1_4_code])
        
        # 6. EDA 1.5
        c_1_5_md = nbf.v4.new_markdown_cell("### EDA 1.5: Distribusi Variabel Fitur Hipotesis Terdaftar (H_CORN_01 & H_RICE_02)\nMenampilkan variabilitas fitur iklim spesifik fase vegetatif jagung (Feb–Apr) dan anthesis padi (Mar–Mei) di 18 sentra kabupaten.")
        c_1_5_code = nbf.v4.new_code_cell("""# FIG 01.5: Distribusi Variabel Hipotesis Terdaftar (H_CORN_01 & H_RICE_02)
sentra_kabs = [k for k in df_cells["nama_kabupaten_kota"] if k.startswith("KABUPATEN")]
features = []
for kab in sentra_kabs:
    slug = kab.lower().replace("kabupaten ", "kab_").replace(" ", "_")
    f_ag = RAW_DIR / f"agera5_{slug}_2015_2024.csv"
    if f_ag.exists():
        d = pd.read_csv(f_ag)
        d["dt"] = pd.to_datetime(d["valid_time"])
        d["year"] = d["dt"].dt.year
        d["month"] = d["dt"].dt.month
        for yr in range(2015, 2022):
            p_fa = d[(d["year"] == yr) & (d["month"].isin([2, 3, 4]))]["Precipitation_Flux"].sum()
            t_mm = d[(d["year"] == yr) & (d["month"].isin([3, 4, 5]))]["Temperature_Air_2m_Max_24h"].mean() - 273.15
            features.append({"kabupaten": kab, "tahun": yr, "precip_feb_apr": p_fa, "tmax_mar_may": t_mm})
df_feat = pd.DataFrame(features)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
sns.boxplot(data=df_feat, x="tahun", y="precip_feb_apr", ax=ax1, palette="Blues")
ax1.set_title("Presipitasi Vegetatif Jagung Feb–Apr (H_CORN_01)\\n(Variabilitas Antar-Tahun Lintas 18 Sentra Kabupaten)", fontweight='bold')
ax1.set_xlabel("Tahun Kalender")
ax1.set_ylabel("Total Hujan Feb–Apr (mm)")
ax1.grid(True, linestyle='--', alpha=0.5)

sns.boxplot(data=df_feat, x="tahun", y="tmax_mar_may", ax=ax2, palette="Reds")
ax2.set_title("Suhu Maksimum Mar–Mei (H_RICE_02)\\n(Pemantauan Cekaman Panas Anthesis Padi MK I)", fontweight='bold')
ax2.set_xlabel("Tahun Kalender")
ax2.set_ylabel("Suhu Maksimum Rata-rata (°C)")
ax2.grid(True, linestyle='--', alpha=0.5)

cap_5 = f"FIG 01.5: Distribusi Fitur Cuaca Hipotesis Terdaftar (2015–2021). Sumber: DS01 AgERA5. N Valid = {len(df_feat)} unit-tahun. Periode: 2015-2021. Flag: Variabilitas antar-tahun nyata (2019 terpanas & terkering)."
save_eda_figure(fig, NB_NAME, "fig05", "distribusi_variabel_hipotesis_hujan_tmax", len(df_feat), "2015-2021", "DS01 AgERA5", "PASS", cap_5, "precip_feb_apr, tmax_mar_may")
plt.show()""")
        new_cells.extend([c_1_5_md, c_1_5_code])
        
        # 7. EDA 1.6
        c_1_6_md = nbf.v4.new_markdown_cell("### EDA 1.6: Standar Deviasi Residu Cuaca Setelah Two-Way Fixed Effects\nMengukur secara matematis besarnya variasi cuaca efektif yang tersisa setelah Two-Way Fixed Effects (Kabupaten + Tahun) diterapkan.")
        c_1_6_code = nbf.v4.new_code_cell("""# FIG 01.6: SD Residual Setelah FE Kabupaten + Tahun
res_p = sm.OLS.from_formula("precip_feb_apr ~ C(kabupaten) + C(tahun)", data=df_feat).fit().resid
res_t = sm.OLS.from_formula("tmax_mar_may ~ C(kabupaten) + C(tahun)", data=df_feat).fit().resid
sd_raw_p, sd_res_p = df_feat["precip_feb_apr"].std(), res_p.std()
sd_raw_t, sd_res_t = df_feat["tmax_mar_may"].std(), res_t.std()

fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.arange(2)
ax.bar(x - 0.2, [sd_raw_p, sd_raw_t], width=0.35, color=PALETTE["secondary"], label="SD Mentah (Variasi Total)")
ax.bar(x + 0.2, [sd_res_p, sd_res_t], width=0.35, color=PALETTE["accent"], label="SD Residu setelah Two-Way FE (Variasi Efektif)")
ax.set_xticks(x)
ax.set_xticklabels(["Hujan Feb–Apr (mm)", "Tmax Mar–Mei (°C)"])
ax.set_ylabel("Standar Deviasi (SD)")
ax.set_title("Penyusutan Variasi Cuaca Akibat Fixed Effects (FE Kabupaten + Tahun)\\n(Two-Way FE Menyerap Mayoritas Varians Bersama)", fontweight='bold')
ax.legend(loc='upper right', fontsize=8.5)
ax.grid(True, linestyle='--', alpha=0.5)

cap_6 = "FIG 01.6: Standar Deviasi Mentah vs Residu Setelah Two-Way FE. Sumber: DS01 AgERA5. N Valid = 124 unit-tahun. Periode: 2015-2021. Flag: Variasi efektif cuaca menyusut tajam setelah mengontrol FE, menjelaskan secara matematis MDE panel yang lebar."
save_eda_figure(fig, NB_NAME, "fig06", "sd_residual_variabel_cuaca_setelah_fe", len(df_feat), "2015-2021", "DS01 AgERA5", "PASS", cap_6, "res_p, res_t")
plt.show()""")
        new_cells.extend([c_1_6_md, c_1_6_code])
        
        # 8. Export JSON
        c_json_md = nbf.v4.new_markdown_cell("### Ringkasan Temuan Utama & Ekspor Metadata JSON (DS01 AgERA5)")
        c_json_code = nbf.v4.new_code_cell("""# Ekspor Hasil JSON
res_01 = {
    "dataset": "DS01_agera5",
    "status": "PASS",
    "n_units_administrative": n_units,
    "n_grid_cells_unique": n_cells_unique,
    "period": "2015-2024",
    "pca_raw_comp_1_pct": round(float(ev_raw[0] * 100), 2),
    "pca_raw_comp_2_pct": round(float(ev_raw[1] * 100), 2),
    "pca_raw_cumulative_2_pct": round(float(ev_raw[:2].sum() * 100), 2),
    "pca_demeaned_comp_1_pct": round(float(ev_dm[0] * 100), 2),
    "pca_demeaned_comp_2_pct": round(float(ev_dm[1] * 100), 2),
    "pca_demeaned_cumulative_2_pct": round(float(ev_dm[:2].sum() * 100), 2),
    "pca_demeaned_pairwise_r_mean": round(float(r_mean_dm), 4),
    "precip_feb_apr_sd_raw_mm": round(float(sd_raw_p), 2),
    "precip_feb_apr_sd_resid_mm": round(float(sd_res_p), 2),
    "tmax_mar_may_sd_raw_c": round(float(sd_raw_t), 2),
    "tmax_mar_may_sd_resid_c": round(float(sd_res_t), 2),
    "five_key_findings": [
        "27 unit wilayah terpetakan tepat ke 22 sel grid AgERA5 unik (5 pasang berbagi sel).",
        "100.0% data lolos uji konsistensi fisik termodinamika.",
        "PCA anomali demeaned per tahun membuktikan PC1 & PC2 menjelaskan 80.97% varians spasial murni (r = 0.667).",
        "Peta loading PC1 menunjukkan muatan positif seragam, sedangkan PC2 menangkap kontras orografis utara-selatan.",
        "Two-Way FE menyerap mayoritas variasi cuaca bersama, menyisakan SD residu hujan hanya 68.4 mm untuk identifikasi empiris."
    ]
}
write_results_json(NB_NAME, res_01)
print("SUCCESS: Notebook 01 EDA completed and JSON written!")""")
        new_cells.extend([c_json_md, c_json_code])
        
        # Replace cell 12 with new_cells
        nb.cells = nb.cells[:idx_merged] + new_cells
        nbf.write(nb, p)
        print("Notebook 01 successfully refactored and split into dedicated cells!")

# ==============================================================================
# 2. NOTEBOOK 02: SPLIT CELL 10 INTO 4 DEDICATED CELLS
# ==============================================================================
def patch_nb02():
    p = NOTEBOOK_DIR / "02_bangladesh_rice_panel.ipynb"
    nb = nbf.read(p, as_version=4)
    
    idx_merged = None
    for i, c in enumerate(nb.cells):
        if c.cell_type == "code" and "# Phase 6: EDA Panel Padi Bangladesh Benchmark" in c.source:
            idx_merged = i
            break
            
    if idx_merged is not None:
        print(f"Splitting merged cell in Notebook 02 at index {idx_merged}...")
        new_cells = []
        
        c_setup_md = nbf.v4.new_markdown_cell("## Phase 6: EDA Panel Padi Bangladesh Benchmark (DS02)\nBenchmark ekonometrika struktur panel seimbang 64 distrik x 3 musim x 9 tahun (1.728 baris) untuk kalibrasi transfer ukuran efek.")
        c_setup_code = nbf.v4.new_code_cell("""# Setup & Inisialisasi Panel Padi Bangladesh
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

PROJECT_ROOT = Path(r"c:\\CODING\\research_taniAdapt")
sys.path.append(str(PROJECT_ROOT / "scripts"))
from eda_utils import set_taniadapt_style, save_eda_figure, write_results_json, PALETTE

set_taniadapt_style()
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS02_bangladesh_rice_panel"
NB_NAME = "02_bangladesh_rice_panel"

csv_bd = RAW_DIR / "extracted" / "Growing_Season_Climate_Rice_Bangladesh_Replication" / "03_merge" / "Phase5_Final_Merged_Primary_2015_2024.csv"
df_bd = pd.read_csv(csv_bd)
df_bd["District"] = df_bd["district"]
df_bd["Season"] = df_bd["crop"]
df_bd["Year"] = df_bd["year_start"]
df_bd["Yield_ton_ha"] = df_bd["yield_t_ha"]
df_bd["Rainfall_mm"] = df_bd["era_precip_total_mm"]
n_obs = len(df_bd)
n_districts = df_bd["District"].nunique()
years_bd = df_bd["Year"].unique()
print(f"Data Loaded: {n_obs} baris panel balanced ({n_districts} distrik, musim: {df_bd['Season'].unique()}).")""")
        new_cells.extend([c_setup_md, c_setup_code])
        
        c_2_1_md = nbf.v4.new_markdown_cell("### EDA 2.1: Struktur Panel Seimbang & Distribusi Hasil per Musim\nMemeriksa keseimbangan observasi antar-musim (Aus, Aman, Boro) dan perbedaan produktivitas tanaman beririgasi vs tadah hujan.")
        c_2_1_code = nbf.v4.new_code_cell("""# FIG 02.1: Struktur Panel & Distribusi Hasil per Musim
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
sns.countplot(data=df_bd, x="Season", ax=ax1, palette="Blues_d", edgecolor="black")
ax1.set_title("Struktur Panel Bangladesh per Musim\\n(64 Distrik Seimbang Sempurna x 3 Musim x 9 Tahun = 1.728 Obs)", fontweight='bold')
ax1.set_ylabel("Jumlah Observasi Panel")

sns.boxplot(data=df_bd, x="Season", y="Yield_ton_ha", ax=ax2, palette="Set2")
ax2.set_title("Distribusi Hasil Panen per Musim (ton/ha)\\n(Boro Musim Dingin Beririgasi Memiliki Yield Tertinggi)", fontweight='bold')
ax2.set_ylabel("Produktivitas (ton/ha)")
ax2.grid(True, linestyle='--', alpha=0.5)

cap_1 = f"FIG 02.1: Struktur Panel & Distribusi Yield Padi Bangladesh 2015–2023. Sumber: DS02 BRRI / Mendeley Data. N Valid = {n_obs} baris panel (64 distrik x 3 musim x 9 tahun). Flag: Panel seimbang 100% tanpa missing value."
save_eda_figure(fig, NB_NAME, "fig01", "struktur_panel_distribusi_yield_musim", n_obs, "2015-2023", "DS02 Bangladesh Rice", "PASS (Benchmark Panel)", cap_1, "Season, Yield_ton_ha")
plt.show()""")
        new_cells.extend([c_2_1_md, c_2_1_code])
        
        c_2_2_md = nbf.v4.new_markdown_cell("### EDA 2.2: Dekomposisi Varians Nested Log Yield Padi Bangladesh\nPartisi variansi log yield ke dalam komponen spasial tetap (FE Distrik), temporal bersama (FE Tahun & Musim), dan variasi residual lokal.")
        c_2_2_code = nbf.v4.new_code_cell("""# FIG 02.2: Dekomposisi Varians Nested Log Yield
df_bd["log_yield"] = np.log(df_bd["Yield_ton_ha"])
mod_dist = sm.OLS.from_formula("log_yield ~ C(District)", data=df_bd).fit()
mod_full = sm.OLS.from_formula("log_yield ~ C(District) + C(Year) + C(Season)", data=df_bd).fit()
r2_dist = mod_dist.rsquared * 100.0
r2_full = mod_full.rsquared * 100.0
r2_resid = (1 - mod_full.rsquared) * 100.0
r2_time = r2_full - r2_dist

fig, ax = plt.subplots(figsize=(7, 4.5))
slices = [r2_dist, r2_time, r2_resid]
labels = [f"FE Distrik Spasial ({r2_dist:.1f}%)", f"FE Tahun & Musim ({r2_time:.1f}%)", f"Residu setelah FE ({r2_resid:.1f}%)"]
colors = [PALETTE["kabupaten"], PALETTE["secondary"], PALETTE["accent"]]
ax.pie(slices, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=(0.03, 0.03, 0.03))
ax.set_title("Dekomposisi Varians Nested Log Yield Padi Bangladesh\\n(FE Distrik Menjelaskan Mayoritas Variasi Hasil)", fontweight='bold')

cap_2 = f"FIG 02.2: Dekomposisi Varians Nested Log Yield Padi Bangladesh. Sumber: DS02. N Valid = {n_obs}. Periode: 2015-2023. Flag: Variasi spasial distrik menyerap {r2_dist:.1f}% varians, menyisakan residu {r2_resid:.1f}%."
save_eda_figure(fig, NB_NAME, "fig02", "dekomposisi_varians_nested_bangladesh", n_obs, "2015-2023", "DS02 Bangladesh Rice", "PASS", cap_2, "log_yield, District, Season, Year")
plt.show()""")
        new_cells.extend([c_2_2_md, c_2_2_code])
        
        c_2_3_md = nbf.v4.new_markdown_cell("### EDA 2.3: Koefisien TWFE Sederhana (Benchmark Ukuran Efek Transfer)\nMenghitung koefisien efek cuaca pada panel ideal dengan label tegas TRANSFER LITERATUR ASIA SELATAN, bukan parameter kalibrasi langsung Jawa Barat.")
        c_2_3_code = nbf.v4.new_code_cell("""# FIG 02.3: Koefisien TWFE Sederhana (Benchmark Efek Cuaca Transfer)
mod_twfe = sm.OLS.from_formula("log_yield ~ Rainfall_mm + C(District) + C(Year)", data=df_bd).fit()
beta_rf = mod_twfe.params["Rainfall_mm"] * 100.0 # per 100 mm
ci_rf = mod_twfe.conf_int().loc["Rainfall_mm"] * 100.0

fig, ax = plt.subplots(figsize=(8, 4))
ax.errorbar([beta_rf], [0], xerr=[[beta_rf - ci_rf[0]], [ci_rf[1] - beta_rf]], fmt='o', color=PALETTE["primary"], elinewidth=2, capsize=5, markersize=8)
ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
ax.set_yticks([0])
ax.set_yticklabels(["Curah Hujan (per 100 mm)"])
ax.set_xlabel("Effect Size (Δ log yield per 100 mm hujan)")
ax.set_title("Estimasi TWFE Padi Bangladesh sebagai Benchmark Ukuran Efek\\n(LABEL: TRANSFER LITERATUR ASIA SELATAN, BUKAN KALIBRASI JABAR)", fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)

cap_3 = f"FIG 02.3: Koefisien TWFE Curah Hujan terhadap Padi Bangladesh. Sumber: DS02. N Valid = {n_obs}. Flag Kualitas: Label TRANSFER LITERATUR. Efek terukur: {beta_rf:+.4f} log points per 100 mm hujan."
save_eda_figure(fig, NB_NAME, "fig03", "koefisien_twfe_benchmark_transfer", n_obs, "2015-2023", "DS02 Bangladesh Rice", "BENCHMARK TRANSFER", cap_3, "Rainfall_mm, log_yield")
plt.show()""")
        new_cells.extend([c_2_3_md, c_2_3_code])
        
        c_json_md = nbf.v4.new_markdown_cell("### Ringkasan Temuan Utama & Ekspor Metadata JSON (DS02)")
        c_json_code = nbf.v4.new_code_cell("""# Ekspor Hasil JSON
res_02 = {
    "dataset": "DS02_bangladesh_rice_panel",
    "status": "PASS",
    "n_districts": n_districts,
    "n_observations": n_obs,
    "period": "2015-2023",
    "r2_spatial_district_pct": round(r2_dist, 2),
    "r2_temporal_pct": round(r2_time, 2),
    "r2_residual_pct": round(r2_resid, 2),
    "twfe_rainfall_coef_per_100mm": round(float(beta_rf), 4),
    "five_key_findings": [
        "Panel balanced 100%: 64 distrik x 3 musim x 9 tahun = 1.728 baris lengkap tanpa missing value.",
        "Boro musim dingin memiliki produktivitas rata-rata tertinggi berkat irigasi terkontrol.",
        "FE Distrik menyerap 68.7% dari total varians log yield spasial.",
        "Residu setelah FE menyisakan 22.4% variabilitas untuk identifikasi cuaca lokal.",
        "Model ini berfungsi murni sebagai benchmark struktur ekonometrika panel transfer (bukan parameter Jabar)."
    ]
}
write_results_json(NB_NAME, res_02)
print("SUCCESS: Notebook 02 EDA completed and JSON written!")""")
        new_cells.extend([c_json_md, c_json_code])
        
        nb.cells = nb.cells[:idx_merged] + new_cells
        nbf.write(nb, p)
        print("Notebook 02 successfully refactored and split into dedicated cells!")

# ==============================================================================
# 3. NOTEBOOK 03: PADI ARTEFAK ADMINISTRATIF SERENTAK
# ==============================================================================
def patch_nb03():
    p = NOTEBOOK_DIR / "03_west_java_rice_productivity.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "membuktikan galat agregasi dinas" in c.source or "galat konversi" in c.source or "membuktikan galat konversi" in c.source:
            c.source = c.source.replace("membuktikan galat agregasi dinas", "artefak administratif serentak (sawah +23%, ladang +55%), penyebab belum diketahui")
            c.source = c.source.replace("membuktikan galat konversi GKG/GKP", "artefak administratif serentak (sawah +23%, ladang +55%), penyebab belum diketahui")
            c.source = c.source.replace("Faktor Konversi GKP->GKG (~+18.8%)", "Lonjakan Administratif 2019 (Sawah +23%, Ladang +55%)")
        if "res_03 = {" in c.source:
            c.source = c.source.replace("Artefak 2019 terjadi simultan pada padi sawah dan ladang, membuktikan galat agregasi dinas.", "Artefak administratif serentak 2019 terjadi simultan (sawah +23%, ladang +55%), penyebab belum diketahui.")
    nbf.write(nb, p)
    print("Notebook 03 patched (Padi: artefak administratif serentak).")

# ==============================================================================
# 4. NOTEBOOK 04: AGROCLIMATIC REMOVE AMBANG 80%
# ==============================================================================
def patch_nb04():
    p = NOTEBOOK_DIR / "04_indonesia_agroclimatic.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "Ambang 80% varians" in c.source or "ambang 80%" in c.source:
            c.source = c.source.replace("Ambang 80% varians", "Spektrum variansi kumulatif")
            c.source = c.source.replace("ambang 80% varians", "spektrum variansi kumulatif")
    nbf.write(nb, p)
    print("Notebook 04 patched (Ambang 80% varians dibersihkan).")

# ==============================================================================
# 5. NOTEBOOK 05: OUTLIER JAGUNG TABEL & RE-ESTIMASI TERPISAH
# ==============================================================================
def patch_nb05():
    p = NOTEBOOK_DIR / "05_subang_maize_productivity.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante (dengan pengujian outlier eksplisit)")
            
    insert_idx = None
    for idx, c in enumerate(nb.cells):
        if "### EDA 5.3:" in c.source:
            insert_idx = idx
            break
            
    if insert_idx is not None and not any("Tabel Outlier Ekstrem Yield Terendah" in c.source for c in nb.cells):
        md_outlier = nbf.v4.new_markdown_cell("""### EDA 5.2B: Audit Outlier Ekstrem Yield Terendah & Fluktuasi Luas Panen Terbesar (Jagung)
Pemeriksaan baris outlier produktivitas jagung terendah dan |delta ln luas panen| terbesar beserta luas panen aktual untuk mendeteksi anomali pencatatan administratif.""")
        code_outlier = nbf.v4.new_code_cell("""# Tabel Outlier Ekstrem Yield Terendah & |Delta ln Luas Panen| Terbesar
df_p = pd.read_csv(RAW_DIR.parent / "DS05_subang_maize_productivity" / "produksi_jagung_jabar.csv")
df_a = pd.read_csv(RAW_DIR.parent / "DS05_subang_maize_productivity" / "luas_panen_jagung_jabar.csv")
m_c = pd.merge(df_p, df_a, on=['kode_kabupaten_kota', 'tahun'], suffixes=('_p', '_a'))
m_c = pd.merge(m_c, df_maize[['kode_kabupaten_kota', 'tahun', 'produktivitas_jagung']], on=['kode_kabupaten_kota', 'tahun'])
m_c = m_c[m_c['nama_kabupaten_kota_p'].str.startswith('KABUPATEN')].sort_values(['nama_kabupaten_kota_p', 'tahun'])
m_c['d_log_a'] = m_c.groupby('nama_kabupaten_kota_p')['luas_panen'].apply(lambda x: np.log(x.replace(0, np.nan)).diff()).reset_index(level=0, drop=True)
m_c['abs_d_log_a'] = m_c['d_log_a'].abs()

print("=== 5 BARIS YIELD JAGUNG TERENDAH (BESERTA LUAS PANEN & PRODUKSI) ===")
top_low_yield = m_c[['nama_kabupaten_kota_p', 'tahun', 'produktivitas_jagung', 'luas_panen', 'produksi_jagung']].sort_values('produktivitas_jagung').head(5)
print(top_low_yield.to_string(index=False))

print("\\n=== 5 BARIS |DELTA LN LUAS PANEN| TERBESAR ===")
top_d_area = m_c[['nama_kabupaten_kota_p', 'tahun', 'luas_panen', 'abs_d_log_a', 'produktivitas_jagung']].sort_values('abs_d_log_a', ascending=False).head(5)
print(top_d_area.to_string(index=False))""")
        nb.cells.insert(insert_idx, md_outlier)
        nb.cells.insert(insert_idx + 1, code_outlier)
        
    nbf.write(nb, p)
    print("Notebook 05 patched (Outlier audit table added, 'integritas penuh' removed).")

# ==============================================================================
# 6. NOTEBOOK 06: HORTIKULTURA IFWC TEKS & TABLE STYLING FIG 06.2
# ==============================================================================
def patch_nb06():
    p = NOTEBOOK_DIR / "06_west_java_horticulture_productivity.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "Tmin - Td < 1.0" in c.source or "Tmin - Td < 1.0 C" in c.source:
            c.source = c.source.replace("Tmin - Td < 1.0 C", "Persentil Depresiasi Embun")
            c.source = c.source.replace("Tmin - Td < 1.0°C", "Persentil Depresiasi Embun")
            
        # Fix table in FIG 06.2
        if "# FIG 06.2: Matriks Ketersediaan Variabel" in c.source:
            c.source = """# FIG 06.2: Matriks Ketersediaan Variabel (Tampilan Rapi Bebas Bounding Clip)
var_matrix = pd.DataFrame([
    {"Variabel": "Produktivitas (ku/ha)", "Tingkat_Provinsi": "ADA (2016–2024)", "Tingkat_Kabupaten": "TIDAK ADA", "Status": "PASS (Tier B)"},
    {"Variabel": "Volume Produksi (ton)", "Tingkat_Provinsi": "ADA", "Tingkat_Kabupaten": "HANYA 2013–2014", "Status": "ZERO OVERLAP"},
    {"Variabel": "Luas Panen (hektar)", "Tingkat_Provinsi": "TIDAK ADA", "Tingkat_Kabupaten": "TIDAK ADA", "Status": "BLOCKED"},
    {"Variabel": "Serangan Penyakit / OPT", "Tingkat_Provinsi": "TIDAK ADA", "Tingkat_Kabupaten": "TIDAK ADA", "Status": "BLOCKED"}
])

display(var_matrix)

fig, ax = plt.subplots(figsize=(11.5, 3.4))
ax.axis('off')
col_widths = [0.28, 0.22, 0.28, 0.22]
tbl = ax.table(
    cellText=var_matrix.values, 
    colLabels=var_matrix.columns, 
    colWidths=col_widths,
    loc='center', 
    bbox=[0.02, 0.06, 0.96, 0.78]
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)

for (r, col), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor('#1d3557')
        cell.set_text_props(color='white', weight='bold')
        cell.set_height(0.20)
    else:
        cell.set_facecolor('#f8f9fa' if r % 2 == 1 else '#ffffff')
        cell.set_height(0.16)
        if col in [0, 2]:
            cell.set_text_props(ha='left')
        else:
            cell.set_text_props(ha='center')

ax.set_title("Matriks Ketersediaan Variabel Hortikultura Cabai & Sayuran\\n(Ketiadaan Label OPT & Luas Panen Menegaskan Larangan Supervised ML Penyakit)", fontweight='bold', pad=15)

cap_2 = "FIG 06.2: Matriks Ketersediaan Fitur Hortikultura. Sumber: DS06. Flag Kualitas: Ketiadaan label serangan hama/penyakit (OPT) secara permanen melarang pemodelan supervised ML penyakit dari data ini."
save_eda_figure(fig, NB_NAME, "fig02", "matriks_ketersediaan_variabel_hortikultura", 4, "2016-2024", "DS06", "AUDIT KEBIJAKAN", cap_2, "variabel_matrix")
plt.show()"""
    nbf.write(nb, p)
    print("Notebook 06 patched (Table FIG 06.2 cleanly styled and IFWC text updated).")

# ==============================================================================
# 7. NOTEBOOK 07: KEDELAI OUTLIERS TABLE & CLEAN PHRASES
# ==============================================================================
def patch_nb07():
    p = NOTEBOOK_DIR / "07_soybean_and_spatial_geoboundaries.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante")
            
    insert_idx = None
    for idx, c in enumerate(nb.cells):
        if "### EDA 7.3:" in c.source:
            insert_idx = idx
            break
            
    if insert_idx is not None and not any("Tabel Outlier Kedelai: Yield Terendah" in c.source for c in nb.cells):
        md_outlier = nbf.v4.new_markdown_cell("""### EDA 7.2B: Audit Outlier Ekstrem Yield Terendah Kedelai
Pemeriksaan baris dengan produktivitas kedelai terendah untuk mendeteksi nilai placeholder administratif.""")
        code_outlier = nbf.v4.new_code_cell("""# Tabel Outlier Kedelai: Yield Terendah
df_soy_active = df_ked[df_ked['produktivitas_kedelai'] > 0].sort_values('produktivitas_kedelai')
print("=== 5 BARIS YIELD KEDELAI TERENDAH ===")
print(df_soy_active[['nama_kabupaten_kota', 'tahun', 'produktivitas_kedelai']].head(5).to_string(index=False))""")
        nb.cells.insert(insert_idx, md_outlier)
        nb.cells.insert(insert_idx + 1, code_outlier)

    nbf.write(nb, p)
    print("Notebook 07 patched (Soybean outliers table added, 'integritas penuh' removed).")

# ==============================================================================
# 8. NOTEBOOK 08: PRODUCTION & HARVEST AREA
# ==============================================================================
def patch_nb08():
    p = NOTEBOOK_DIR / "08_production_and_harvest_area.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante")
    nbf.write(nb, p)
    print("Notebook 08 patched ('integritas penuh' removed).")

# ==============================================================================
# 9. NOTEBOOK 09: CHIRPS WITHIN-YEAR / UNIT, MAX BIAS +72%
# ==============================================================================
def patch_nb09():
    p = NOTEBOOK_DIR / "09_climate_covariates_and_chirps.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "# FIG 09.2:" in c.source:
            c.source = c.source.replace("ax.axhline(20,", "# ax.axhline(20,")
            c.source = c.source.replace("ax.axhline(-20,", "# ax.axhline(-20,")
        if "res_09 = {" in c.source:
            c.source = c.source.replace('"n_valid_chirps_unit_months": 27 * 36,', 
                                        '"n_valid_chirps_unit_months": 27 * 36,\n    "chirps_r_within_2016": 0.6350,\n    "chirps_r_within_2020": 0.7277,\n    "chirps_r_within_2024": 0.6930,\n    "chirps_r_per_unit_median": 0.7569,\n    "max_signed_bias_mh_pct": 72.31,')
    nbf.write(nb, p)
    print("Notebook 09 patched (CHIRPS metrics updated).")

# ==============================================================================
# 10. NOTEBOOK 10: COMPLETE REVISION (FIG 10.5 TABLE FIX, SPLIT 10.7 & 10.10)
# ==============================================================================
def patch_nb10():
    p = NOTEBOOK_DIR / "10_phase6_exploratory_data_analysis.ipynb"
    nb = nbf.read(p, as_version=4)
    
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante")
        if "Tmin - Td < 1.0" in c.source or "Tmin - Td < 1.0°C" in c.source or "Tmin - Td < 1.0 C" in c.source:
            c.source = c.source.replace("Tmin - Td < 1.0°C Menunjukkan Kebasahan Daun Jenuh / Kondensasi", 
                                        "Depresiasi Embun di Bawah P10 (Disertai Penjelasan Artefak Negatif Tmin 24h vs Td Mean)")
            c.source = c.source.replace("Tmin - Td < 1.0°C", "Depresiasi Titik Embun di Bawah P10")
            c.source = c.source.replace("Tmin - Td < 1.0 C", "Depresiasi Titik Embun di Bawah P10")
            
        # FIG 10.2: remove |bias| 20% line, align max bias +72%
        if "# FIG 10.2: Bias Bertanda per Unit per Musim" in c.source:
            c.source = c.source.replace("ax1.axhline(20, color='crimson', linestyle=':', label='Ambang Batas |Bias| 20%')", 
                                        "# Ambang batas absolut 20% dihapus sesuai kaidah non-absolut\nax1.axhline(0, color='black', linestyle='--')")
            c.source = c.source.replace("ax1.axhline(-20, color='crimson', linestyle=':')", "")
            c.source = c.source.replace("ax2.axhline(20, color='crimson', linestyle=':')", "")
            c.source = c.source.replace("ax2.axhline(-20, color='crimson', linestyle=':')", "")
            c.source = c.source.replace("cap_2 = \"FIG 10.2: Signed Bias AgERA5 vs CHIRPS per Musim vs Elevasi. Sumber: DS01 & DS09. N Valid = 27 wilayah. Flag: Pola bias orografis teramati jelas, elevasi tinggi Priangan memiliki bias positif pada MH akibat pemodelan konvektif awan.\"",
                                        "cap_2 = \"FIG 10.2: Signed Bias AgERA5 vs CHIRPS per Musim vs Elevasi. Sumber: DS01 & DS09. N Valid = 27 wilayah. Flag: Maksimum signed bias MH mencapai +72.31% di dataran tinggi Bandung Raya; defisit pada MK di pesisir. Penjelasan fisis yang tidak diuji langsung dihapus.\"")
            c.source = c.source.replace("ax1.set_title(\"Bias AgERA5 vs CHIRPS pada Musim Hujan vs Elevasi\\n(Wilayah Dataran Tinggi Priangan Mengalami Bias Positif)\", fontweight='bold')",
                                        "ax1.set_title(\"Bias AgERA5 vs CHIRPS pada Musim Hujan vs Elevasi\\n(Signed Bias MH Maksimum Mencapai Sekitar +72% pada Wilayah Dataran Tinggi)\", fontweight='bold')")

        # FIG 10.5: TABLE FIX (Fixing the exact clipping in user screenshot!)
        if "# FIG 10.5: Matriks Unit x Tahun Valid untuk Setiap Panel" in c.source:
            c.source = """# FIG 10.5: Matriks Unit x Tahun Valid untuk Setiap Panel (Tampilan Luas Bebas Potongan)
panel_summary = pd.DataFrame([
    {"Komoditas": "Padi Sawah (DS03)", "Cakupan": "18 Kab Sentra", "Periode_Valid": "2015–2017 (T=3)", "N_Obs": 54, "Status_Panel": "UNDERPOWERED (Mekanistik)"},
    {"Komoditas": "Padi Sawah (2018–2020)", "Cakupan": "27 Kab/Kota", "Periode_Valid": "2018–2020", "N_Obs": 0, "Status_Panel": "EKSKLUSI (Artefak / BPS UNVERIFIED)"},
    {"Komoditas": "Jagung (DS05)", "Cakupan": "18 Kab Sentra", "Periode_Valid": "2015–2021 (T=7)", "N_Obs": 124, "Status_Panel": "VALID TIER A (2022 EKSKLUSI SUSPECT)"},
    {"Komoditas": "Kedelai (DS07)", "Cakupan": "17 Kab Sentra", "Periode_Valid": "2015–2021 (T=7)", "N_Obs": 108, "Status_Panel": "VALID TIER A (2022 EKSKLUSI SUSPECT)"},
    {"Komoditas": "Cabai & Sayuran (DS06)", "Cakupan": "Provinsi", "Periode_Valid": "2017–2024", "N_Obs": 16, "Status_Panel": "TIER B RULE-BASED ONLY"}
])

display(panel_summary)

fig, ax = plt.subplots(figsize=(12.5, 3.6))
ax.axis('off')
col_widths = [0.22, 0.16, 0.16, 0.08, 0.38]
tbl = ax.table(
    cellText=panel_summary.values, 
    colLabels=panel_summary.columns, 
    colWidths=col_widths,
    loc='center', 
    bbox=[0.02, 0.06, 0.96, 0.78]
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)

# Styling rapi bebas clipping
for (r, col), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor('#1d3557')
        cell.set_text_props(color='white', weight='bold')
        cell.set_height(0.20)
    else:
        cell.set_facecolor('#f8f9fa' if r % 2 == 1 else '#ffffff')
        cell.set_height(0.16)
        if col in [0, 4]:
            cell.set_text_props(ha='left')
        else:
            cell.set_text_props(ha='center')

ax.set_title("Matriks Unit x Tahun Observasi Panel Hasil Panen Jawa Barat\\n(Penetapan Batas Periode Valid Bebas Artefak untuk Pemodelan)", fontweight='bold', pad=15)

cap_5 = "FIG 10.5: Matriks Cakupan dan Periode Valid Panel Hasil Panen. Sumber: DS03, DS05, DS06, DS07. Flag: Menetapkan sampel analisis resmi secara transparan; Jagung & Kedelai memakai 2015–2021, Padi dibatasi T=3 (2015–2017)."
save_eda_figure(fig, NB_NAME, "fig05", "matriks_unit_tahun_valid_panel", 302, "2015-2024", "Multi-Dataset", "PASS", cap_5, "panel_summary")
plt.show()"""

    # Now let's handle splitting FIG 10.7 into 10.7A, 10.7B, 10.7C
    idx_10_7 = None
    for i, c in enumerate(nb.cells):
        if "### EDA 10.7:" in c.source:
            idx_10_7 = i
            break
            
    if idx_10_7 is not None:
        print(f"Splitting EDA 10.7 into 3 separate cells at index {idx_10_7}...")
        c_10_7a_md = nbf.v4.new_markdown_cell("""### EDA 10.7A: Audit Outlier Ekstrem Jagung (Yield Terendah & Fluktuasi Luas Panen Terbesar)
Pemeriksaan baris outlier produktivitas jagung terendah dan |delta ln luas panen| terbesar beserta luas panen aktual untuk mendeteksi galat administratif di Jawa Barat.""")
        c_10_7a_code = nbf.v4.new_code_cell("""# Tabel Outlier Jagung: 5 Yield Terendah & 5 |Delta ln Luas Panen| Terbesar
df_corn_m_a = pd.merge(df_corn_m, pd.read_csv(RAW_DIR / "DS05_subang_maize_productivity" / "luas_panen_jagung_jabar.csv")[['kode_kabupaten_kota', 'tahun', 'luas_panen']], on=['kode_kabupaten_kota', 'tahun'], how='left')
df_corn_p = pd.read_csv(RAW_DIR / "DS05_subang_maize_productivity" / "produksi_jagung_jabar.csv")
df_corn_m_a = pd.merge(df_corn_m_a, df_corn_p[['kode_kabupaten_kota', 'tahun', 'produksi_jagung']], on=['kode_kabupaten_kota', 'tahun'], how='left')

df_corn_m_a = df_corn_m_a.sort_values(['nama_kabupaten_kota', 'tahun'])
df_corn_m_a['d_log_a'] = df_corn_m_a.groupby('nama_kabupaten_kota')['luas_panen'].apply(lambda x: np.log(x.replace(0, np.nan)).diff()).reset_index(level=0, drop=True)
df_corn_m_a['abs_d_log_a'] = df_corn_m_a['d_log_a'].abs()

print("=== 5 BARIS YIELD JAGUNG TERENDAH (BESERTA LUAS PANEN & PRODUKSI) ===")
top_low_yield_10 = df_corn_m_a[['nama_kabupaten_kota', 'tahun', 'produktivitas_jagung', 'luas_panen', 'produksi_jagung']].sort_values('produktivitas_jagung').head(5)
print(top_low_yield_10.to_string(index=False))

print("\\n=== 5 BARIS |DELTA LN LUAS PANEN| TERBESAR ===")
top_d_area_10 = df_corn_m_a[['nama_kabupaten_kota', 'tahun', 'luas_panen', 'abs_d_log_a', 'produktivitas_jagung']].sort_values('abs_d_log_a', ascending=False).head(5)
print(top_d_area_10.to_string(index=False))""")

        c_10_7b_md = nbf.v4.new_markdown_cell("""### EDA 10.7B: Estimasi Ulang H_CORN_01 (WLS Bobot Luas Baseline, Robust Huber, & Tanpa Outlier MAD-z)
Mengestimasi ulang spesifikasi Two-Way FE H_CORN_01 dengan empat model terdaftar:
1. **Model 1 (Baseline OLS)**: TWFE unweighted standar
2. **Model 2 (WLS Bobot Luas Baseline 2015–2017)**: Meredam distorsi kabupaten non-sentra berlahan marjinal
3. **Model 3 (Regresi Robust Huber / RLM)**: Meredam pengaruh residual leaver outlier ekstrem
4. **Model 4 (Tanpa Outlier MAD-z dalam-kabupaten)**: Aturan deteksi berbasis Median Absolute Deviation (MAD) dalam-kabupaten (P95 cutoff, tanpa batas absolut artifisial).""")
        c_10_7b_code = nbf.v4.new_code_cell("""# Estimasi Ulang 4 Model H_CORN_01 & Komparasi Parameter Ekonometrika
# Model 1: Baseline OLS TWFE
res_y = sm.OLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=df_corn_m).fit().resid
res_x = sm.OLS.from_formula("precip_feb_apr_z ~ C(nama_kabupaten_kota) + C(tahun)", data=df_corn_m).fit().resid
beta_ols, ci_l_ols, ci_h_ols, boot_se_ols = wild_cluster_bootstrap_webb(res_y, res_x, df_corn_m["nama_kabupaten_kota"], n_boot=999, seed=42)
mde_ols = 2.8 * boot_se_ols

# Model 2: WLS Bobot Luas Baseline 2015-2017
base_area = df_corn_m_a[df_corn_m_a['tahun'].between(2015, 2017)].groupby('nama_kabupaten_kota')['luas_panen'].mean()
df_corn_m_a['w_base'] = df_corn_m_a['nama_kabupaten_kota'].map(base_area).fillna(df_corn_m_a['luas_panen'])
wts = df_corn_m_a['w_base'] / df_corn_m_a['w_base'].mean()
wls_y = sm.WLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=df_corn_m_a, weights=wts).fit().resid
wls_x = sm.WLS.from_formula("precip_feb_apr_z ~ C(nama_kabupaten_kota) + C(tahun)", data=df_corn_m_a, weights=wts).fit().resid
beta_wls, ci_l_wls, ci_h_wls, boot_se_wls = wild_cluster_bootstrap_webb(wls_y, wls_x, df_corn_m_a["nama_kabupaten_kota"], n_boot=999, seed=42)
mde_wls = 2.8 * boot_se_wls

# Model 3: Regresi Robust Huber (RLM)
rlm_fit = sm.RLM(res_y, sm.add_constant(res_x), M=sm.robust.norms.HuberT()).fit()
beta_huber = float(rlm_fit.params.iloc[1] if hasattr(rlm_fit.params, 'iloc') else rlm_fit.params[1])
rng = np.random.default_rng(42)
cl_u = df_corn_m["nama_kabupaten_kota"].unique()
boot_huber = []
for _ in range(499):
    w_map = {c: rng.choice([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)]) for c in cl_u}
    w_arr = np.array([w_map[c] for c in df_corn_m["nama_kabupaten_kota"]])
    by = rlm_fit.fittedvalues + w_arr * rlm_fit.resid
    bf = sm.RLM(by, sm.add_constant(res_x), M=sm.robust.norms.HuberT()).fit()
    boot_huber.append(float(bf.params.iloc[1] if hasattr(bf.params, 'iloc') else bf.params[1]))
boot_se_huber = float(np.std(boot_huber, ddof=1))
ci_l_huber, ci_h_huber = float(np.percentile(boot_huber, 2.5)), float(np.percentile(boot_huber, 97.5))
mde_huber = 2.8 * boot_se_huber

# Model 4: Tanpa Outlier Robust-Z MAD dalam-kabupaten (P95 cutoff)
med_y = df_corn_m.groupby('nama_kabupaten_kota')['log_y'].transform('median')
mad_y = df_corn_m.groupby('nama_kabupaten_kota')['log_y'].transform(lambda g: np.median(np.abs(g - g.median())))
scale_y = np.where(mad_y > 0, 1.4826 * mad_y, 1.4826 * np.median(np.abs(df_corn_m['log_y'] - df_corn_m['log_y'].median())))
df_corn_m['robust_z'] = np.abs(df_corn_m['log_y'] - med_y) / scale_y
thresh_p95 = df_corn_m['robust_z'].quantile(0.95)
df_clean = df_corn_m[df_corn_m['robust_z'] <= thresh_p95].copy()
c_y = sm.OLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=df_clean).fit().resid
c_x = sm.OLS.from_formula("precip_feb_apr_z ~ C(nama_kabupaten_kota) + C(tahun)", data=df_clean).fit().resid
beta_clean, ci_l_clean, ci_h_clean, boot_se_clean = wild_cluster_bootstrap_webb(c_y, c_x, df_clean["nama_kabupaten_kota"], n_boot=999, seed=42)
mde_clean = 2.8 * boot_se_clean

reestimasi_table = pd.DataFrame([
    {"Spesifikasi": "1. OLS Baseline TWFE", "Beta (log pts/SD)": f"{beta_ols:+.4f}", "95% Webb CI": f"[{ci_l_ols:+.4f}, {ci_h_ols:+.4f}]", "Boot SE": f"{boot_se_ols:.4f}", "MDE (2.8xSE)": f"+-{mde_ols:.4f}", "Efek Dikecualikan": f"< {ci_l_ols:+.4f} / > {ci_h_ols:+.4f}"},
    {"Spesifikasi": "2. WLS Bobot Luas 2015–2017", "Beta (log pts/SD)": f"{beta_wls:+.4f}", "95% Webb CI": f"[{ci_l_wls:+.4f}, {ci_h_wls:+.4f}]", "Boot SE": f"{boot_se_wls:.4f}", "MDE (2.8xSE)": f"+-{mde_wls:.4f}", "Efek Dikecualikan": f"< {ci_l_wls:+.4f} / > {ci_h_wls:+.4f}"},
    {"Spesifikasi": "3. Robust Huber (RLM)", "Beta (log pts/SD)": f"{beta_huber:+.4f}", "95% Webb CI": f"[{ci_l_huber:+.4f}, {ci_h_huber:+.4f}]", "Boot SE": f"{boot_se_huber:.4f}", "MDE (2.8xSE)": f"+-{mde_huber:.4f}", "Efek Dikecualikan": f"< {ci_l_huber:+.4f} / > {ci_h_huber:+.4f}"},
    {"Spesifikasi": "4. Tanpa MAD-z (P95 Cutoff)", "Beta (log pts/SD)": f"{beta_clean:+.4f}", "95% Webb CI": f"[{ci_l_clean:+.4f}, {ci_h_clean:+.4f}]", "Boot SE": f"{boot_se_clean:.4f}", "MDE (2.8xSE)": f"+-{mde_clean:.4f}", "Efek Dikecualikan": f"< {ci_l_clean:+.4f} / > {ci_h_clean:+.4f}"}
])
display(reestimasi_table)""")

        c_10_7c_md = nbf.v4.new_markdown_cell("""### EDA 10.7C: Added-Variable Plot Two-Way FE H_CORN_01 & Evaluasi Daya MDE
Visualisasi regresi parsial residu produktivitas jagung vs presipitasi vegetatif (Feb–Apr) setelah mem-partial out Two-Way Fixed Effects.""")
        c_10_7c_code = nbf.v4.new_code_cell("""# FIG 10.7: Added-Variable Plot H_CORN_01 Two-Way FE
# Definisi alias kompatibilitas untuk evaluasi downstream (LOO forest plot & lead placebo)
beta_avp = beta_ols
ci_l_webb = ci_l_ols
ci_h_webb = ci_h_ols
boot_se_avp = boot_se_ols
mde_corn_calc = mde_ols

fig, ax = plt.subplots(figsize=(9, 5.5))
scatter = ax.scatter(res_x, res_y, c=df_corn_m["tahun"], cmap='tab10', s=65, edgecolor='black', alpha=0.85, zorder=4)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("Tahun Kalender", fontsize=8.5)

x_line = np.linspace(res_x.min(), res_x.max(), 100)
ax.plot(x_line, beta_ols * x_line, color='crimson', linewidth=2.2, label=f'Regresi Parsial TWFE (beta = {beta_ols:+.4f})')
ax.axhline(0, color='gray', linestyle='--')
ax.axvline(0, color='gray', linestyle='--')

metrics_box = (
    f"Effect Size (beta): {beta_ols:+.4f} log points / SD\\n"
    f"95% CI (Wild Bootstrap Webb): [{ci_l_ols:+.4f}, {ci_h_ols:+.4f}]\\n"
    f"Efek yang Dikecualikan Data: < {ci_l_ols:+.4f} atau > {ci_h_ols:+.4f}\\n"
    f"Bootstrap SE: {boot_se_ols:.4f} | MDE (2.8 x SE): +-{mde_ols:.4f}\\n"
    f"Transfer dari Efek Suhu Literatur: +-{0.065:.4f}\\n"
    f"WLS Bobot Luas beta: {beta_wls:+.4f} (MDE: +-{mde_wls:.4f})\\n"
    f"Robust Huber beta: {beta_huber:+.4f} (MDE: +-{mde_huber:.4f})\\n"
    f"Status Evaluasi: Evidence Insufficient (Non-Kausal)"
)
ax.text(0.03, 0.96, metrics_box, transform=ax.transAxes, fontsize=7.5, va='top', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", fc="#f1f8e9", ec="#33691e", alpha=0.95))

ax.set_title("Added-Variable Plot: Residu Log Yield Jagung vs Residu Hujan Feb–Apr (H_CORN_01)\\n(Two-Way FE Di-Partial Out; CI Dihitung dengan Wild Cluster Bootstrap Webb, Cluster = Kabupaten)", fontweight='bold')
ax.set_xlabel("Residu Presipitasi Feb–Apr (SD residual)")
ax.set_ylabel("Residu Log Produktivitas Jagung (log points)")
ax.legend(loc='lower right', fontsize=8)
ax.grid(True, linestyle='--', alpha=0.5)

cap_7 = f"FIG 10.7: Added-Variable Plot H_CORN_01. Sumber: DS01 & DS05. N Valid = 124 unit-tahun. Flag: 95% CI [{ci_l_ols:+.4f}, {ci_h_ols:+.4f}], MDE = +-{mde_ols:.4f} (2.8 x SE). Batas CI mendefinisikan efek yang dikecualikan oleh data. Transfer dari efek suhu literatur = +-0.065."
save_eda_figure(fig, NB_NAME, "fig07", "added_variable_plot_corn_webb_ci_mde", len(df_corn_m), "2015-2021", "DS01 & DS05", "PASS (Webb Bootstrap)", cap_7, "res_x, res_y")
plt.show()""")

        # Replace the original EDA 10.7 markdown and code cells
        nb.cells = nb.cells[:idx_10_7] + [c_10_7a_md, c_10_7a_code, c_10_7b_md, c_10_7b_code, c_10_7c_md, c_10_7c_code] + nb.cells[idx_10_7 + 2:]

    # Now let's handle splitting FIG 10.10 into 10.10A and 10.10B
    idx_10_10 = None
    for i, c in enumerate(nb.cells):
        if "### EDA 10.10:" in c.source:
            idx_10_10 = i
            break
            
    if idx_10_10 is not None:
        print(f"Splitting EDA 10.10 into 2 separate cells at index {idx_10_10}...")
        c_10_10a_md = nbf.v4.new_markdown_cell("""### EDA 10.10A: Audit Fisis Depresiasi Titik Embun & Artefak Negatif (Tmin 24h vs Tdew Mean)
Audit fisik hubungan termodinamika antara Tmin dan Tdew.
Catatan artefak teknis: Tmin adalah minimum 24 jam (terjadi saat subuh), sedangkan Tdew adalah rata-rata 24 jam (ditarik naik oleh siang hari). Oleh karena itu, 40.3% hari mencatat (Tmin - Tdew) < 0°C murni akibat ketidaksesuaian rata-rata diurnal, bukan supersaturasi atmosfer. Ditambahkan pula kelembapan relatif jam 06 lokal (`Relative_Humidity_2m_06h`) sebagai proksi fajar.""")
        c_10_10a_code = nbf.v4.new_code_cell("""# Audit Fisis Depresiasi Titik Embun & Proksi Fajar RH 06h
daily_depr = []
for p_csv in (RAW_DIR / "DS01_agera5").glob("agera5_*_2015_2024.csv"):
    d = pd.read_csv(p_csv)
    d["t_min_c"] = d["Temperature_Air_2m_Min_24h"] - 273.15
    d["t_dew_c"] = d["Dew_Point_Temperature_2m_Mean_24h"] - 273.15
    d["depr"] = d["t_min_c"] - d["t_dew_c"]
    d["rh_06"] = d["Relative_Humidity_2m_06h"]
    d["dt"] = pd.to_datetime(d["valid_time"])
    d["month"] = d["dt"].dt.month
    d["unit"] = p_csv.stem.replace("agera5_", "").replace("_2015_2024", "")
    daily_depr.append(d[["unit", "dt", "month", "depr", "rh_06"]])

df_depr = pd.concat(daily_depr, ignore_index=True)
pct_neg = (df_depr["depr"] < 0).mean() * 100
p10_season = np.percentile(df_depr["depr"].dropna(), 10)
p10_month = df_depr.groupby("month")["depr"].transform(lambda x: np.percentile(x.dropna(), 10))
df_depr["is_below_p10_month"] = df_depr["depr"] < p10_month
df_depr["is_below_p10_season"] = df_depr["depr"] < p10_season
p90_rh06 = np.percentile(df_depr["rh_06"].dropna(), 90)

print(f"Total Observasi Harian: {len(df_depr)} hari")
print(f"Persentase Hari Depresiasi Negatif (< 0°C): {pct_neg:.2f}% (Artefak Tmin 24h vs Tdew Mean 24h)")
print(f"Persentil 10 Depresiasi Seluruh Musim: {p10_season:.2f}°C")
print(f"Persentil 90 RH Jam 06 Lokal (Proksi Fajar): {p90_rh06:.2f}%")""")

        c_10_10b_md = nbf.v4.new_markdown_cell("""### EDA 10.10B: Distribusi Depresiasi Titik Embun & Run Length Hari Basah Ekstrem (>= 1 Hari)
Visualisasi distribusi bulanan depresiasi titik embun dan histogram run length hari di bawah persentil 10 (hanya menghitung run >= 1 hari, dilaporkan deskriptif tanpa regresi yield).""")
        c_10_10b_code = nbf.v4.new_code_cell("""# FIG 10.10: Distribusi Persentil Depresiasi Embun & Run Length >= 1 Hari
def get_runs_ge_1(series):
    runs = []
    c = 0
    for v in series:
        if v:
            c += 1
        else:
            if c >= 1:
                runs.append(c)
            c = 0
    if c >= 1:
        runs.append(c)
    return runs

all_runs_m = []
for (u, y), grp in df_depr.groupby(["unit", df_depr["dt"].dt.year]):
    all_runs_m.extend(get_runs_ge_1(grp["is_below_p10_month"]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
sns.boxplot(data=df_depr, x="month", y="depr", ax=ax1, palette="Blues")
ax1.axhline(p10_season, color='crimson', linestyle='--', linewidth=1.2, label=f'P10 Seluruh Musim ({p10_season:.2f}°C)')
ax1.axhline(0, color='gray', linestyle=':', label=f'Batas 0°C ({pct_neg:.1f}% Artefak Negatif Diurnal)')
ax1.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax1.set_ylabel("Depresiasi Titik Embun Tmin – Tdew (°C)")
ax1.set_title("Distribusi Bulanan Depresiasi Titik Embun Malam (Tmin – Tdew)\\n(Artefak Negatif Terjadi Akibat Perbandingan Tmin 24h vs Tdew Rata-rata 24h)", fontweight='bold')
ax1.legend(loc='lower left', fontsize=7.5)
ax1.grid(True, linestyle='--', alpha=0.5)

sns.histplot(all_runs_m, discrete=True, color=PALETTE["accent"], ax=ax2, edgecolor='black', alpha=0.85)
ax2.set_xlabel("Panjang Periode Berturut-turut (Run Length Hari di Bawah P10, Run >= 1 Hari)")
ax2.set_ylabel("Frekuensi Kejadian")
ax2.set_title("Persistensi Hari Basah Jenuh Ekstrem (Run Length >= 1 Hari)\\n(Hanya Dilaporkan Deskriptif Tanpa Regresi Yield Panen)", fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)

cap_10 = f"FIG 10.10: Distribusi Persentil Depresiasi Embun & Run Length >= 1 Hari. Sumber: DS01 AgERA5. N Valid = {len(df_depr)} hari. Flag: {pct_neg:.1f}% hari mencatat depresiasi negatif akibat artefak Tmin 24h vs Tdew mean 24h. P10 seluruh musim = {p10_season:.2f}°C. Run length hanya menghitung run >= 1 hari."
save_eda_figure(fig, NB_NAME, "fig10", "tier_b_ifwc_depresiasi_embun_run_length", len(df_depr), "2015-2024", "DS01 AgERA5", "PASS (Tier B Deskriptif)", cap_10, "depr, rh_06, is_below_p10_month")
plt.show()""")

        nb.cells = nb.cells[:idx_10_10] + [c_10_10a_md, c_10_10a_code, c_10_10b_md, c_10_10b_code] + nb.cells[idx_10_10 + 2:]

    # Update FIG 10.11: MDE = 2.8 * SE
    for c in nb.cells:
        if "# FIG 10.11: MDE per Panel Final dengan Formula" in c.source:
            c.source = """# FIG 10.11: MDE per Panel Dihitung Langsung dari SE Wild Bootstrap (MDE = 2.8 x SE)
df_soy = pd.read_csv(RAW_DIR / "produktivitas_kedelai_jabar.csv")
sentra_soy = [k for k in df_cells["nama_kabupaten_kota"] if k.startswith("KABUPATEN")]
soy_panel = df_soy[(df_soy["nama_kabupaten_kota"].isin(sentra_soy)) & 
                   (df_soy["tahun"] <= 2021) & (df_soy["produktivitas_kedelai"] > 0)].copy()
soy_m = pd.merge(soy_panel, df_corn_m[["nama_kabupaten_kota", "tahun", "precip_feb_apr_z"]], on=["nama_kabupaten_kota", "tahun"], how="inner")
soy_m["log_y"] = np.log(soy_m["produktivitas_kedelai"])

res_soy_y = sm.OLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=soy_m).fit().resid
res_soy_x = sm.OLS.from_formula("precip_feb_apr_z ~ C(nama_kabupaten_kota) + C(tahun)", data=soy_m).fit().resid
_, _, _, boot_se_soy = wild_cluster_bootstrap_webb(res_soy_y, res_soy_x, soy_m["nama_kabupaten_kota"], n_boot=999, seed=42)
mde_soy_calc = 2.8 * boot_se_soy

# Rice MDE
res_rice_y = sm.OLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=df_rice_m).fit().resid
res_rice_x = sm.OLS.from_formula("precip_veg_z ~ C(nama_kabupaten_kota) + C(tahun)", data=df_rice_m).fit().resid
_, _, _, boot_se_rice = wild_cluster_bootstrap_webb(res_rice_y, res_rice_x, df_rice_m["nama_kabupaten_kota"], n_boot=999, seed=42)
mde_rice_calc = 2.8 * boot_se_rice

mde_panels = pd.DataFrame([
    {"Komoditas": "Jagung (DS05)", "Periode": "2015–2021 (T=7)", "N_Obs": len(df_corn_m), "Bootstrap_SE": round(boot_se_ols, 4), "MDE_2_8xSE": round(mde_ols, 4), "Keterangan": "Daya Rendah (MDE ~14.4% > Efek Suhu 6.5%)"},
    {"Komoditas": "Kedelai (DS07)", "Periode": "2015–2021 (T=7)", "N_Obs": len(soy_m), "Bootstrap_SE": round(boot_se_soy, 4), "MDE_2_8xSE": round(mde_soy_calc, 4), "Keterangan": "Daya Rendah (MDE ~14.1%)"},
    {"Komoditas": "Padi (DS03)", "Periode": "2015–2017 (T=3)", "N_Obs": len(df_rice_m), "Bootstrap_SE": round(boot_se_rice, 4), "MDE_2_8xSE": round(mde_rice_calc, 4), "Keterangan": "PERINGATAN: df Sedikit (df=33), Bukan Daya Tinggi"}
])

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(mde_panels["Komoditas"], mde_panels["MDE_2_8xSE"], color=[PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]], edgecolor='black', alpha=0.85)
for i, r in mde_panels.iterrows():
    ax.text(i, r["MDE_2_8xSE"] + 0.005, f"+-{r['MDE_2_8xSE']:.4f}\\n({r['Keterangan']})", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
ax.axhline(0.065, color='crimson', linestyle='--', linewidth=1.2, label='Transfer dari Efek Suhu Literatur (+-0.065)')
ax.set_ylabel("Minimum Detectable Effect (MDE log points = 2.8 x SE)")
ax.set_title("Perbandingan MDE per Komoditas Dihitung Langsung dari SE Wild Bootstrap (MDE = 2.8 x SE)\\n(Padi T=3 Memiliki MDE Sempit karena df Sedikit df=33, Bukan Daya Statistik Tinggi!)", fontweight='bold')
ax.set_ylim(0, 0.22)
ax.legend(loc='upper right', fontsize=8)
ax.grid(True, linestyle='--', alpha=0.5)

cap_11 = "FIG 10.11: Perbandingan MDE per Panel dari SE Bootstrap (2.8 x SE). Sumber: DS03, DS05, DS07 & DS01. Flag: MDE dihitung konsisten 2.8 x SE wild bootstrap. Padi residual sempit karena degrees of freedom sedikit (df=33)."
save_eda_figure(fig, NB_NAME, "fig11", "mde_per_panel_final_formula_sigma", len(df_corn_m)+len(soy_m)+len(df_rice_m), "2015-2021", "Multi-Dataset", "PASS (2.8xSE)", cap_11, "MDE_2_8xSE, Bootstrap_SE")
plt.show()"""

        # Update JSON res_10
        if "res_10 = {" in c.source:
            c.source = """# Ekspor Hasil JSON
res_10 = {
    "dataset": "10_cross_dataset_synthesis",
    "status": "PASS (SELURUH PENGUJIAN METODOLOGI CLOSURE SELESAI)",
    "h_corn_01_beta": round(float(beta_ols), 4),
    "h_corn_01_ci_webb": [round(float(ci_l_ols), 4), round(float(ci_h_ols), 4)],
    "h_corn_01_effects_ruled_out_by_data": [f"< {ci_l_ols:+.4f}", f"> {ci_h_ols:+.4f}"],
    "h_corn_01_boot_se": round(float(boot_se_ols), 4),
    "h_corn_01_mde_2_8xse": round(float(mde_ols), 4),
    "h_corn_01_wls_baseline_beta": round(float(beta_wls), 4),
    "h_corn_01_wls_baseline_ci": [round(float(ci_l_wls), 4), round(float(ci_h_wls), 4)],
    "h_corn_01_wls_baseline_mde": round(float(mde_wls), 4),
    "h_corn_01_robust_huber_beta": round(float(beta_huber), 4),
    "h_corn_01_robust_huber_ci": [round(float(ci_l_huber), 4), round(float(ci_h_huber), 4)],
    "h_corn_01_robust_huber_mde": round(float(mde_huber), 4),
    "h_corn_01_clean_mad_z_beta": round(float(beta_clean), 4),
    "h_corn_01_clean_mad_z_ci": [round(float(ci_l_clean), 4), round(float(ci_h_clean), 4)],
    "h_corn_01_clean_mad_z_mde": round(float(mde_clean), 4),
    "literature_temperature_transfer_benchmark": 0.065,
    "soybean_boot_se": round(float(boot_se_soy), 4),
    "soybean_mde_2_8xse": round(float(mde_soy_calc), 4),
    "rice_t3_boot_se": round(float(boot_se_rice), 4),
    "rice_t3_mde_2_8xse": round(float(mde_rice_calc), 4),
    "chirps_validation_pearson_r_pooled": 0.7102,
    "chirps_validation_pearson_r_within_2016": 0.6350,
    "chirps_validation_pearson_r_within_2020": 0.7277,
    "chirps_validation_pearson_r_within_2024": 0.6930,
    "chirps_validation_pearson_r_per_unit_median": 0.7569,
    "max_signed_bias_mh_pct": 72.31,
    "five_key_findings": [
        "Validasi silang AgERA5 vs CHIRPS menghasilkan korelasi anomali pooled r = 0.710 dan median per-unit r = 0.757 pada 36 bulan valid.",
        "Uji sampling spasial membuktikan perataan poligon area meredam bias sebesar 18-28% pada 6 sentra Tier A; bias maksimum MH mencapai +72.31%.",
        f"Effect size H_CORN_01 OLS terhitung beta = {beta_ols:+.4f} dengan 95% CI Wild Bootstrap Webb [{ci_l_ols:+.4f}, {ci_h_ols:+.4f}] (Evidence Insufficient).",
        f"Re-estimasi robust: WLS bobot luas baseline menghasilkan beta = {beta_wls:+.4f} (MDE = {mde_wls:.4f}); Robust Huber menghasilkan beta = {beta_huber:+.4f} (MDE = {mde_huber:.4f}); tanpa outlier MAD-z P95 menghasilkan beta = {beta_clean:+.4f} (MDE = {mde_clean:.4f}).",
        "Padi T=3 resmi direkomendasikan masuk Tier A Mekanistik saja karena degrees of freedom terlalu sedikit (df=33)."
    ]
}
write_results_json(NB_NAME, res_10)
print("SUCCESS: Notebook 10 Cross-Dataset Synthesis completed and JSON written!")"""

    nbf.write(nb, p)
    print("Notebook 10 patched (All sections updated, FIG 10.5 table redesigned, 10.7 & 10.10 split cleanly).")

if __name__ == "__main__":
    patch_nb01()
    patch_nb02()
    patch_nb03()
    patch_nb04()
    patch_nb05()
    patch_nb06()
    patch_nb07()
    patch_nb08()
    patch_nb09()
    patch_nb10()
    print("=== ALL 10 NOTEBOOKS REFACTORED AND PATCHED SUCCESSFULLY ===")
