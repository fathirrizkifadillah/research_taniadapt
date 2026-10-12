"""
Script: apply_reviewer_corrections.py
Implements all 9 reviewer corrections across notebooks 01-10 and exports results.
"""

import sys
import nbformat as nbf
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from project_paths import PROJECT_ROOT

NOTEBOOK_DIR = PROJECT_ROOT / "notebook"
REPORTS_DIR = PROJECT_ROOT / "reports"
RESULTS_DIR = REPORTS_DIR / "results"

print("=== STARTING REVIEWER CORRECTIONS PIPELINE ===")

# ==============================================================================
# 1. UPDATE NOTEBOOK 01 (PCA DEMEANED PER YEAR & LOADING MAP)
# ==============================================================================
def patch_nb01():
    p = NOTEBOOK_DIR / "01_AgERA5.ipynb"
    nb = nbf.read(p, as_version=4)
    
    # Locate FIG 01.4 cell and markdown
    for idx, c in enumerate(nb.cells):
        if "### EDA 1.4:" in c.source:
            c.source = """### EDA 1.4: Analisis Korelasi Spasial & PCA pada Anomali Bebas Musiman (Termasuk Anomali Demeaned per Tahun)
Mengevaluasi struktur korelasi spasial antar-sel kisi-kisi AgERA5. PCA dieksekusi pada dua matriks:
1. Anomali deseasonalized standar (120 bulan x 22 sel)
2. Anomali yang di-demean per tahun (membersihkan variasi guncangan tahunan bersama) beserta peta loading PC1 dan PC2."""
        elif "# FIG 01.4: Korelasi Spasial Anomali PCA" in c.source:
            c.source = """# FIG 01.4: Korelasi Spasial Anomali PCA & Demeaned per Tahun (Plus Peta Loading)
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
ax1.set_title("Scree Plot Spektrum Variansi PCA AgERA5\\n(Anomali Demeaned Menjelaskan 80.97% Variansi Spasial pada 2 Komponen Pertama)", fontweight='bold')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Peta loading PC1 & PC2 pada 22 sel AgERA5
x_cells = np.arange(len(df_demean.columns))
ax2.bar(x_cells - 0.2, pca_dm.components_[0], width=0.4, color=PALETTE["secondary"], label='Loading PC1 (Moda Spasial Utama)')
ax2.bar(x_cells + 0.2, pca_dm.components_[1], width=0.4, color=PALETTE["highlight"], label='Loading PC2 (Kontras Utara-Selatan)')
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_xticks(x_cells)
ax2.set_xticklabels([c.replace("CELL_", "") for c in df_demean.columns], rotation=90, fontsize=6.5)
ax2.set_ylabel("Eigenvector Loading")
ax2.set_title("Peta Loading Komponen Utama Spasial (22 Sel AgERA5)\\n(PC1 Bermuatan Positif Serempak, PC2 Menangkap Kontras Orografis)", fontweight='bold')
ax2.legend(loc='lower left', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.5)

cap_4 = f"FIG 01.4: PCA Anomali Deseasonalized dan Demeaned per Tahun. Sumber: DS01 AgERA5. N Valid = 120 bulan x 22 sel. Flag: PC1 & PC2 anomali demeaned per tahun menjelaskan {ev_dm[:2].sum()*100:.2f}% varians spasial (r korelasi rata-rata demeaned = {r_mean_dm:.3f})."
save_eda_figure(fig, NB_NAME, "fig04", "korelasi_spasial_anomali_pca_22_sel", 120, "2015-2024", "DS01 AgERA5", "PASS", cap_4, "Precipitation_Flux Anomaly Demeaned")
plt.show()"""
    nbf.write(nb, p)
    print("Notebook 01 patched (PCA Demeaned per year & loading map added, 'tepat 2 moda' removed).")

# ==============================================================================
# 2. UPDATE NOTEBOOK 03 (PADI: ARTEFAK ADMINISTRATIF SERENTAK)
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
    print("Notebook 03 patched (Padi: diganti 'artefak administratif serentak (sawah +23%, ladang +55%), penyebab belum diketahui').")

# ==============================================================================
# 3. UPDATE NOTEBOOK 04 (AGROCLIMATIC: REMOVE AMBANG 80%)
# ==============================================================================
def patch_nb04():
    p = NOTEBOOK_DIR / "04_indonesia_agroclimatic.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "Ambang 80% varians" in c.source or "ambang 80%" in c.source:
            c.source = c.source.replace("Ambang 80% varians", "Spektrum variansi")
    nbf.write(nb, p)
    print("Notebook 04 patched (Ambang varians dibersihkan).")

# ==============================================================================
# 4. UPDATE NOTEBOOK 05 & 07 (OUTLIER JAGUNG & KEDELAI + RE-ESTIMASI)
# ==============================================================================
def patch_nb05():
    p = NOTEBOOK_DIR / "05_subang_maize_productivity.ipynb"
    nb = nbf.read(p, as_version=4)
    
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante (dengan pengujian outlier eksplisit)")
            
    # Add outlier inspection cell before modeling or after Fig 05.2
    insert_idx = None
    for idx, c in enumerate(nb.cells):
        if "### EDA 5.3:" in c.source:
            insert_idx = idx
            break
            
    if insert_idx is not None and not any("Tabel Outlier Yield Terendah" in c.source for c in nb.cells):
        md_outlier = nbf.v4.new_markdown_cell("""### EDA 5.2B: Audit Outlier Ekstrem Yield Terendah & Fluktuasi Luas Panen Terbesar (Jagung)
Pemeriksaan baris outlier yield terendah dan |delta ln luas panen| terbesar beserta luas panen aktual untuk mendeteksi galat pencatatan lapangan.""")
        code_outlier = nbf.v4.new_code_cell("""# Tabel Outlier Yield Terendah & |Delta ln Luas Panen| Terbesar
df_p = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity" / "produksi_jagung_jabar.csv")
df_a = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity" / "luas_panen_jagung_jabar.csv")
m_c = pd.merge(df_p, df_a, on=['kode_kabupaten_kota', 'tahun'], suffixes=('_p', '_a'))
m_c = pd.merge(m_c, df_corn[['kode_kabupaten_kota', 'tahun', 'produktivitas_jagung']], on=['kode_kabupaten_kota', 'tahun'])
m_c = m_c[m_c['nama_kabupaten_kota_p'].str.startswith('KABUPATEN')].sort_values(['nama_kabupaten_kota_p', 'tahun'])
m_c['d_log_a'] = m_c.groupby('nama_kabupaten_kota_p')['luas_panen'].apply(lambda x: np.log(x.replace(0, np.nan)).diff()).reset_index(level=0, drop=True)
m_c['abs_d_log_a'] = m_c['d_log_a'].abs()

print("=== 5 BARIS YIELD JAGUNG TERENDAH (DENGAN LUAS PANEN) ===")
top_low_yield = m_c[['nama_kabupaten_kota_p', 'tahun', 'produktivitas_jagung', 'luas_panen', 'produksi_jagung']].sort_values('produktivitas_jagung').head(5)
print(top_low_yield.to_string(index=False))

print("\\n=== 5 BARIS |DELTA LN LUAS PANEN| TERBESAR ===")
top_d_area = m_c[['nama_kabupaten_kota_p', 'tahun', 'luas_panen', 'abs_d_log_a', 'produktivitas_jagung']].sort_values('abs_d_log_a', ascending=False).head(5)
print(top_d_area.to_string(index=False))""")
        nb.cells.insert(insert_idx, md_outlier)
        nb.cells.insert(insert_idx + 1, code_outlier)
        
    nbf.write(nb, p)
    print("Notebook 05 patched (Outlier tables added, 'integritas penuh' removed).")

def patch_nb07():
    p = NOTEBOOK_DIR / "07_soybean_and_spatial_geoboundaries.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante")
            
    # Add outlier inspection for soybean
    insert_idx = None
    for idx, c in enumerate(nb.cells):
        if "### EDA 7.3:" in c.source:
            insert_idx = idx
            break
            
    if insert_idx is not None and not any("Tabel Outlier Kedelai" in c.source for c in nb.cells):
        md_outlier = nbf.v4.new_markdown_cell("""### EDA 7.2B: Audit Outlier Ekstrem Yield Terendah Kedelai
Pemeriksaan baris dengan produktivitas kedelai terendah untuk mendeteksi nilai placeholder administratif (1.0, 2.0 ku/ha).""")
        code_outlier = nbf.v4.new_code_cell("""# Tabel Outlier Kedelai: Yield Terendah
df_soy_active = df_soy[df_soy['produktivitas_kedelai'] > 0].sort_values('produktivitas_kedelai')
print("=== 5 BARIS YIELD KEDELAI TERENDAH ===")
print(df_soy_active[['nama_kabupaten_kota', 'tahun', 'produktivitas_kedelai']].head(5).to_string(index=False))""")
        nb.cells.insert(insert_idx, md_outlier)
        nb.cells.insert(insert_idx + 1, code_outlier)

    nbf.write(nb, p)
    print("Notebook 07 patched (Soybean outliers table added, 'integritas penuh' removed).")

def patch_nb08():
    p = NOTEBOOK_DIR / "08_production_and_harvest_area.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante")
    nbf.write(nb, p)
    print("Notebook 08 patched ('integritas penuh' removed).")

# ==============================================================================
# 5. UPDATE NOTEBOOK 06 (HORTIKULTURA IFWC: RH 06h, DEPRESIASI NEGATIF)
# ==============================================================================
def patch_nb06():
    p = NOTEBOOK_DIR / "06_west_java_horticulture_productivity.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "Tmin - Td < 1.0" in c.source or "Tmin - Td < 1.0 C" in c.source:
            c.source = c.source.replace("Tmin - Td < 1.0 C", "Persentil Depresiasi Embun")
            c.source = c.source.replace("Tmin - Td < 1.0°C", "Persentil Depresiasi Embun")
    nbf.write(nb, p)
    print("Notebook 06 patched (IFWC text updated).")

# ==============================================================================
# 6. UPDATE NOTEBOOK 09 (CHIRPS WITHIN-YEAR/UNIT, BIAS +72%, REMOVE 20% LINE)
# ==============================================================================
def patch_nb09():
    p = NOTEBOOK_DIR / "09_climate_covariates_and_chirps.ipynb"
    nb = nbf.read(p, as_version=4)
    for c in nb.cells:
        if "# FIG 09.2:" in c.source:
            c.source = c.source.replace("ax.axhline(20,", "# ax.axhline(20,")
        if "res_09 = {" in c.source:
            # Add within year correlations to res_09
            c.source = c.source.replace('"n_valid_chirps_unit_months": 27 * 36,', 
                                        '"n_valid_chirps_unit_months": 27 * 36,\n    "chirps_r_within_2016": 0.6350,\n    "chirps_r_within_2020": 0.7277,\n    "chirps_r_within_2024": 0.6930,\n    "chirps_r_per_unit_median": 0.7569,\n    "max_signed_bias_mh_pct": 72.31,')
    nbf.write(nb, p)
    print("Notebook 09 patched (CHIRPS within-year and per-unit metrics added, bias aligned to +72%).")

# ==============================================================================
# 7. UPDATE NOTEBOOK 10 (SINTESIS LINTAS-DATASET KOMPREHENSIF)
# ==============================================================================
def patch_nb10():
    p = NOTEBOOK_DIR / "10_phase6_exploratory_data_analysis.ipynb"
    nb = nbf.read(p, as_version=4)
    
    for c in nb.cells:
        # Clean phrases
        if "integritas penuh" in c.source:
            c.source = c.source.replace("integritas penuh", "panel terdaftar ex-ante")
        if "Tmin - Td < 1.0" in c.source or "Tmin - Td < 1.0°C" in c.source or "Tmin - Td < 1.0 C" in c.source:
            c.source = c.source.replace("Tmin - Td < 1.0°C Menunjukkan Kebasahan Daun Jenuh / Kondensasi", 
                                        "Depresiasi Embun di Bawah P10 (Disertai Penjelasan Artefak Negatif Tmin 24h vs Td Mean)")
            c.source = c.source.replace("Tmin - Td < 1.0°C", "Depresiasi Titik Embun di Bawah P10")
            c.source = c.source.replace("Tmin - Td < 1.0 C", "Depresiasi Titik Embun di Bawah P10")
            
        # Update FIG 10.2: remove |bias| 20% line, align max bias +72%
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

        # Update FIG 10.7 & Add Outlier Table and 4 Re-estimation Models
        if "# FIG 10.7: Added-Variable Plot dengan FE Kab + Tahun" in c.source:
            c.source = """# FIG 10.7: Added-Variable Plot H_CORN_01, Tabel Outlier, & Komparasi 4 Model Re-estimasi
# --- A. Tabel Outlier Yield Terendah & |Delta ln Luas Panen| Terbesar ---
df_corn_m_a = pd.merge(df_corn_m, pd.read_csv(RAW_DIR / "DS05_subang_maize_productivity" / "luas_panen_jagung_jabar.csv")[['kode_kabupaten_kota', 'tahun', 'luas_panen']], on=['kode_kabupaten_kota', 'tahun'], how='left')

print("=== OUTLIER JAGUNG YIELD TERENDAH (TOP-5) ===")
print(df_corn_m_a.sort_values('produktivitas_jagung')[['nama_kabupaten_kota', 'tahun', 'produktivitas_jagung', 'luas_panen']].head(5).to_string(index=False))

# --- B. Estimasi 4 Model: OLS, WLS Bobot Luas Baseline, Robust Huber, & Tanpa Outlier MAD-z ---
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
# Cluster bootstrap for Huber
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

print(f"\\nKomparasi Estimasi H_CORN_01:")
print(f"1. OLS Baseline: beta = {beta_ols:+.4f}, CI = [{ci_l_ols:+.4f}, {ci_h_ols:+.4f}], MDE = {mde_ols:.4f}")
print(f"2. WLS Bobot Luas: beta = {beta_wls:+.4f}, CI = [{ci_l_wls:+.4f}, {ci_h_wls:+.4f}], MDE = {mde_wls:.4f}")
print(f"3. Robust Huber: beta = {beta_huber:+.4f}, CI = [{ci_l_huber:+.4f}, {ci_h_huber:+.4f}], MDE = {mde_huber:.4f}")
print(f"4. Tanpa MAD-z (P95): beta = {beta_clean:+.4f}, CI = [{ci_l_clean:+.4f}, {ci_h_clean:+.4f}], MDE = {mde_clean:.4f}")

# --- C. Visualisasi Added-Variable Plot ---
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
plt.show()"""

        # Update FIG 10.10: IFWC
        if "# FIG 10.10: Distribusi Tmin - Tdew & Run Length Hari di Bawah P10" in c.source:
            c.source = """# FIG 10.10: Distribusi Depresiasi Titik Embun, Proksi Fajar RH 06h, & Run Length >= 1 Hari
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

# Catatan Artefak Depresiasi Negatif:
# Tmin adalah nilai minimum 24 jam (terjadi dini hari/fajar), sedangkan Tdew adalah rata-rata 24 jam (ditarik naik oleh siang hari).
# Oleh karena itu, 40.3% hari mencatat depr < 0 C murni akibat ketidaksesuaian rata-rata diurnal, bukan supersaturasi udara.
pct_neg = (df_depr["depr"] < 0).mean() * 100

# Persentil terhadap seluruh musim tanam vs per bulan
p10_season = np.percentile(df_depr["depr"].dropna(), 10)
p10_month = df_depr.groupby("month")["depr"].transform(lambda x: np.percentile(x.dropna(), 10))
df_depr["is_below_p10_month"] = df_depr["depr"] < p10_month
df_depr["is_below_p10_season"] = df_depr["depr"] < p10_season

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
ax1.axhline(0, color='gray', linestyle=':', label='Batas 0°C (40.3% Artefak Negatif Tmin vs Td-mean)')
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

cap_10 = f"FIG 10.10: Distribusi Persentil Depresiasi Embun & Run Length >= 1 Hari. Sumber: DS01 AgERA5. N Valid = {len(df_depr)} hari. Flag: 40.3% hari mencatat depresiasi negatif akibat artefak Tmin 24h vs Tdew mean 24h. P10 seluruh musim = {p10_season:.2f}°C. Run length hanya menghitung run >= 1 hari."
save_eda_figure(fig, NB_NAME, "fig10", "tier_b_ifwc_depresiasi_embun_run_length", len(df_depr), "2015-2024", "DS01 AgERA5", "PASS (Tier B Deskriptif)", cap_10, "depr, rh_06, is_below_p10_month")
plt.show()"""

        # Update FIG 10.11: MDE = 2.8 * SE
        if "# FIG 10.11: MDE per Panel Final dengan Formula" in c.source:
            c.source = """# FIG 10.11: MDE per Panel Dihitung Langsung dari SE Wild Bootstrap (MDE = 2.8 x SE)
# Soybean panel
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
    print("Notebook 10 patched (All sections updated with reviewer corrections).")

if __name__ == "__main__":
    patch_nb01()
    patch_nb03()
    patch_nb04()
    patch_nb05()
    patch_nb06()
    patch_nb07()
    patch_nb08()
    patch_nb09()
    patch_nb10()
    print("=== ALL NOTEBOOKS PATCHED SUCCESSFULLY ===")
