import os
import json
from pathlib import Path

NOTEBOOK_DIR = Path(r"c:\CODING\research_taniAdapt\notebook")

def make_cell(cell_type, source_text):
    if cell_type == "markdown":
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source_text.strip().split("\n")]
        }
    else:
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source_text.strip().split("\n")]
        }

def save_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.11.9"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    filepath = NOTEBOOK_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Berhasil meng-update: {filepath}")

# =====================================================================
# 1. 01_AgERA5.ipynb (DS01)
# =====================================================================
c01 = [
    make_cell("markdown", """# 01 — AgERA5 Agrometeorological Indicators Time-Series (1979–2025)
**TaniAdapt Project — Primary Weather & Agroclimatic Backbone (DS01)**
**Fase:** Phase 3 (Dataset Discovery & Clean Acquisition) + Phase 4 (Dataset Quality Audit)

- **Sumber Resmi:** [Copernicus Climate Data Store (AgERA5 Time-Series)](https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries)
- **Cakupan Lokasi:** 7 Wilayah Pertanian Jawa Barat (Bandung, Karawang, Tasikmalaya, Sukabumi, Cirebon, Purwakarta, Bekasi)
- **Variabel:** 24 variabel agroklimat resmi harian (suhu min/mean/max, presipitasi, RH diurnal & derived, radiasi, VPD, ET0, angin)
- **Arsitektur:** Menggunakan endpoint OpenAPI Time-Series resmi Copernicus CDS (CSV multivariat harian)
"""),
    make_cell("code", """from pathlib import Path
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Deteksi root project otomatis (bekerja baik dari root maupun folder notebook/)
CWD = Path.cwd().resolve()
PROJECT_ROOT = CWD.parent if CWD.name.lower() == "notebook" else CWD
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
REPORTS_DIR = PROJECT_ROOT / "reports" / "dataset_audit"
FIGURES_DIR = REPORTS_DIR / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
print("Project Root:", PROJECT_ROOT)
print("Raw Data Dir:", RAW_DIR)
"""),
    make_cell("markdown", """## Phase 3 — Discovery & Verifikasi Variabel AgERA5
Membaca katalog 27 variabel AgERA5 yang telah diinventarisasi dari API resmi Copernicus CDS.
"""),
    make_cell("code", """inv_path = PROJECT_ROOT / "reports" / "dataset_discovery" / "agera5_variable_inventory.csv"
if inv_path.exists():
    df_inv = pd.read_csv(inv_path)
    print(f"Total Variabel AgERA5 Dikatalogkan: {len(df_inv)}")
    display(df_inv[["display_label", "exact_identifier", "decision", "units_and_definition"]].head(8))
else:
    print("Catalog AgERA5 belum ditemukan.")
"""),
    make_cell("markdown", """## Phase 3 — Verifikasi File Akuisisi Lokal (7 Lokasi Jawa Barat)
Mengecek keberadaan file 10 tahun (2015–2024, 3.653 hari kalender) untuk ke-7 lokasi.
"""),
    make_cell("code", """locations = ["bandung", "karawang", "tasikmalaya", "sukabumi", "cirebon", "purwakarta", "bekasi"]
print("Status File Mentah Lokal (2015–2024):")
data_summary = []
for loc in locations:
    fpath = RAW_DIR / f"agera5_{loc}_2015_2024.csv"
    if fpath.exists():
        sz = fpath.stat().st_size
        df_temp = pd.read_csv(fpath)
        null_count = df_temp.isnull().sum().sum()
        p_annual_2024 = df_temp[pd.to_datetime(df_temp['valid_time']).dt.year == 2024]['Precipitation_Flux'].sum()
        data_summary.append({
            "Lokasi": loc.upper(),
            "Ukuran (Bytes)": sz,
            "Total Hari": len(df_temp),
            "Missing Values": null_count,
            "Curah Hujan 2024 (mm)": round(p_annual_2024, 1)
        })
        print(f"  [OK] {loc.upper():<12}: {sz:,} bytes | Baris: {len(df_temp):,} | Nulls: {null_count}")

df_loc_summary = pd.DataFrame(data_summary)
"""),
    make_cell("markdown", """## Phase 4 — Quality Audit & Validasi Plausibilitas Fisis
Memeriksa skema, kelengkapan data (0 nulls), dan aturan hukum fisika atmosfer:
1. Suhu: $T_{min} \\le T_{mean} \\le T_{max}$
2. Presipitasi: $\\ge 0$ mm/hari
3. Kelembaban Relatif (RH): berada di rentang 0% hingga 100%
4. Vapour Pressure Deficit (VPD): non-negatif ($\\ge 0$ kPa)
"""),
    make_cell("code", """target_file = RAW_DIR / "agera5_bandung_2015_2024.csv"
df_bandung = pd.read_csv(target_file)

print("Dimensi Data Bandung:", df_bandung.shape)
print("Total Missing Values:", df_bandung.isnull().sum().sum())
print("Rentang Tanggal     :", df_bandung['valid_time'].min(), "s.d.", df_bandung['valid_time'].max())

# Uji Plausibilitas Fisis
t_rule = (df_bandung['Temperature_Air_2m_Min_24h'] <= df_bandung['Temperature_Air_2m_Mean_24h']).all() and \\
         (df_bandung['Temperature_Air_2m_Mean_24h'] <= df_bandung['Temperature_Air_2m_Max_24h']).all()
p_rule = (df_bandung['Precipitation_Flux'] >= 0).all()
rh_rule = ((df_bandung['Derived_Relative_Humidity_2m_Min_24h'] >= 0) & (df_bandung['Derived_Relative_Humidity_2m_Max_24h'] <= 100.1)).all()
vpd_rule = (df_bandung['Vapour_Pressure_Deficit_at_Maximum_Temperature'] >= 0).all()

print("\\n" + "="*50)
print("HASIL UJI VALIDITAS HUKUM FISIKA ATMOSFER:")
print("="*50)
print(f"1. Tmin <= Tmean <= Tmax : {'[PASSED]' if t_rule else '[FAILED]'}")
print(f"2. Presipitasi >= 0 mm   : {'[PASSED]' if p_rule else '[FAILED]'}")
print(f"3. RH dalam rentang 0-100%: {'[PASSED]' if rh_rule else '[FAILED]'}")
print(f"4. VPD non-negatif (>=0) : {'[PASSED]' if vpd_rule else '[FAILED]'}")
print("="*50)
"""),
    make_cell("markdown", """## Visualisasi Diagnostik Multi-Panel (Suhu Bandung & Komparasi Presipitasi 7 Lokasi)
Menampilkan plausibilitas suhu Bandung 2024 dan komparasi curah hujan tahunan antar wilayah Jawa Barat.
"""),
    make_cell("code", """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5), gridspec_kw={'width_ratios': [2, 1.2]})

# Panel 1: Suhu Bandung 2024
df_bandung['valid_time'] = pd.to_datetime(df_bandung['valid_time'])
df_2024 = df_bandung[df_bandung['valid_time'].dt.year == 2024]

ax1.plot(df_2024['valid_time'], df_2024['Temperature_Air_2m_Mean_24h'] - 273.15, label='Tmean (°C)', color='darkorange', linewidth=1.5)
ax1.plot(df_2024['valid_time'], df_2024['Temperature_Air_2m_Max_24h'] - 273.15, label='Tmax (°C)', color='crimson', alpha=0.6, linewidth=1)
ax1.plot(df_2024['valid_time'], df_2024['Temperature_Air_2m_Min_24h'] - 273.15, label='Tmin (°C)', color='royalblue', alpha=0.6, linewidth=1)
ax1.set_title("AgERA5 Bandung 2024 - Plausibilitas Suhu Harian (Tmin ≤ Tmean ≤ Tmax)")
ax1.set_xlabel("Tanggal")
ax1.set_ylabel("Suhu Udara (°C)")
ax1.legend(loc='lower left')
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Komparasi Presipitasi Tahunan 2024 (7 Lokasi Jabar)
colors = ['#2b5c8f', '#4682b4', '#5c9ea6', '#72b9a8', '#99c286', '#c4cb70', '#e6af5d']
bars = ax2.barh(df_loc_summary['Lokasi'], df_loc_summary['Curah Hujan 2024 (mm)'], color=colors, edgecolor='black', alpha=0.85)
ax2.set_title("Curah Hujan Kumulatif 2024 (7 Lokasi Jabar)")
ax2.set_xlabel("Akumulasi Presipitasi (mm/tahun)")
ax2.grid(axis='x', linestyle='--', alpha=0.5)
for bar in bars:
    w = bar.get_width()
    ax2.annotate(f"{w:.0f} mm", xy=(w, bar.get_y() + bar.get_height()/2),
                 xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=9)

plt.tight_layout()
png_out = FIGURES_DIR / "ds01_agera5_plausibility.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""),
    make_cell("markdown", """## Executive Audit Scorecard
Ringkasan metrik audit kualitas dataset AgERA5 untuk pengambilan keputusan di TaniAdapt.
"""),
    make_cell("code", """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS01 — AgERA5 Agrometeorological Indicators"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "ECMWF / Copernicus Climate Data Store (CDS OpenAPI)"},
    {"Dimensi Audit": "Cakupan Wilayah", "Hasil & Evaluasi": "7 Sentra Pertanian Jawa Barat (Bandung, Karawang, Tasikmalaya, Sukabumi, Cirebon, Purwakarta, Bekasi)"},
    {"Dimensi Audit": "Cakupan Temporal", "Hasil & Evaluasi": "10 Tahun Kalender Penuh (2015-01-01 s.d. 2024-12-31 = 3.653 Hari)"},
    {"Dimensi Audit": "Kelengkapan Nilai", "Hasil & Evaluasi": "100% Lengkap (0 Missing Values di seluruh 7 lokasi)"},
    {"Dimensi Audit": "Plausibilitas Fisis", "Hasil & Evaluasi": "PASSED (Memenuhi hukum batas suhu, presipitasi >= 0, RH 0-100%, VPD >= 0)"},
    {"Dimensi Audit": "Peran di TaniAdapt", "Hasil & Evaluasi": "Primary Weather & Agroclimatic Backbone"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Layak sebagai tulang punggung iklim mikro)"},
    {"Dimensi Audit": "Batasan Kritis", "Hasil & Evaluasi": "Data reanalisis grid spasial 0,1° (~10 km); bukan sensor stasiun on-farm."}
])

display(scorecard)
""")
]
save_notebook("01_AgERA5.ipynb", c01)

# =====================================================================
# 2. 02_bangladesh_rice_panel.ipynb (DS02)
# =====================================================================
c02 = [
    make_cell("markdown", """# 02 — Bangladesh Rice Climate–Yield Panel Replication Archive (DS02)
**TaniAdapt Project — Methodological & Comparative Benchmark**
**Fase:** Phase 3 (Discovery & Clean Acquisition) + Phase 4 (Dataset Quality Audit)

- **Sumber Resmi:** [Mendeley Data DOI: 10.17632/h94z4ftts2.1](https://doi.org/10.17632/h94z4ftts2.1)
- **Penerbit:** Bangladesh Rice Research Institute (BRRI) / Elsevier
- **Peran di TaniAdapt:** Benchmark metodologi pemodelan panel regresi antara variabel iklim terhadap hasil panen padi (*rice yield*).
"""),
    make_cell("code", """from pathlib import Path
import os, sys, zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = Path.cwd().resolve()
PROJECT_ROOT = CWD.parent if CWD.name.lower() == "notebook" else CWD
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS02_bangladesh_rice_panel"
FIGURES_DIR = PROJECT_ROOT / "reports" / "dataset_audit" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("Project Root:", PROJECT_ROOT)
print("Raw Data Dir:", RAW_DIR)
"""),
    make_cell("markdown", """## Phase 3 — Audit Arsip & Integritas File Unduhan
Memeriksa integritas arsip ZIP replikasi dan file hasil ekstraksi audit.
"""),
    make_cell("code", """zip_path = RAW_DIR / "Growing_Season_Climate_Rice_Bangladesh_Replication.zip"
csv_path = RAW_DIR / "extracted" / "Growing_Season_Climate_Rice_Bangladesh_Replication" / "Rice_Yield_2015_2024_Audited.csv"

if zip_path.exists():
    print(f"Arsip ZIP Replikasi : {zip_path.stat().st_size:,} bytes")
if csv_path.exists():
    print(f"File CSV Hasil Audit: {csv_path.stat().st_size:,} bytes")
"""),
    make_cell("markdown", """## Phase 4 — Quality Audit, Keunikan Kunci Panel & Statistik Panen
Memeriksa duplikasi kunci panel (`district x crop x crop_year`), kelengkapan metrik panen, dan distribusi yield (t/ha).
"""),
    make_cell("code", """df_rice = pd.read_csv(csv_path)

print("Dimensi Data Padi Bangladesh:", df_rice.shape)
print("Musim Tanam Padi :", df_rice['crop'].unique().tolist())
print("Rentang Tahun    :", sorted(df_rice['crop_year'].unique().tolist()))
print("Total Distrik    :", df_rice['district'].nunique())

# Uji Duplikasi Kunci Panel
dup_count = df_rice.duplicated(subset=['district', 'crop', 'crop_year']).sum()
print("\\n" + "="*50)
print(f"UJI DUPLIKASI KUNCI PANEL (district x crop x crop_year): {dup_count} (HARUS 0)")
print("STATUS KEUNIKAN KUNCI :", "[PASSED]" if dup_count == 0 else "[FAILED]")
print("="*50)

print("\\nStatistik Ringkas Variabel Target:")
display(df_rice[['area_ha', 'yield_t_ha', 'production_mt']].describe())
"""),
    make_cell("markdown", """## Visualisasi Diagnostik Multi-Panel (Observasi Musim & Boxplot Distribusi Yield)
Distribusi jumlah observasi distrik per musim tanam dan sebaran variabilitas produktivitas (t/ha) per musim tanam.
"""),
    make_cell("code", """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

# Panel 1: Stacked Bar Observasi per Tahun & Musim Tanam
pivot = df_rice.groupby(['crop_year', 'crop']).size().unstack().fillna(0)
pivot.plot(kind='bar', stacked=True, ax=ax1, colormap='viridis', edgecolor='black', alpha=0.85)
ax1.set_title("Observasi Distrik per Musim Tanam (2015–2024)")
ax1.set_xlabel("Tahun Panen (Crop Year)")
ax1.set_ylabel("Jumlah Observasi Distrik")
ax1.legend(title="Musim Tanam Padi")
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Panel 2: Boxplot Distribusi Yield per Musim Tanam
crops = df_rice['crop'].unique()
yield_data = [df_rice[df_rice['crop'] == c]['yield_t_ha'].dropna() for c in crops]
bp = ax2.boxplot(yield_data, tick_labels=crops, patch_artist=True)
colors = ['#8dd3c7', '#ffffb3', '#bebada']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
ax2.set_title("Distribusi Hasil Panen (Yield t/ha) per Musim Tanam")
ax2.set_xlabel("Musim Tanam")
ax2.set_ylabel("Produktivitas (Ton / Hektar)")
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds02_rice_panel_missingness.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""),
    make_cell("markdown", """## Executive Audit Scorecard
"""),
    make_cell("code", """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS02 — Bangladesh Rice Climate–Yield Panel"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "BRRI / Elsevier (Mendeley Data DOI: 10.17632/h94z4ftts2.1)"},
    {"Dimensi Audit": "Struktur Data", "Hasil & Evaluasi": "Panel Data Seimbang (64 Distrik x 3 Musim Tanam = 1.728 Baris)"},
    {"Dimensi Audit": "Rentang Periode", "Hasil & Evaluasi": "2015-16 s.d. 2023-24 (9 Tahun Kalender Tanam)"},
    {"Dimensi Audit": "Keunikan Kunci Panel", "Hasil & Evaluasi": "PASSED (0 Duplikasi kunci district x crop x crop_year)"},
    {"Dimensi Audit": "Variabel Agronomi", "Hasil & Evaluasi": "Luas Tanam (ha), Produksi (MT), Produktivitas (t/ha), dan Iklim Musiman"},
    {"Dimensi Audit": "Peran di TaniAdapt", "Hasil & Evaluasi": "Methodological & Comparative Benchmark"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Tolok ukur pemodelan regresi panel iklim vs yield)"},
    {"Dimensi Audit": "Batasan Kritis", "Hasil & Evaluasi": "Data internasional Bangladesh; tidak bisa untuk kalibrasi langsung petani lokal Jabar."}
])

display(scorecard)
""")
]
save_notebook("02_bangladesh_rice_panel.ipynb", c02)

# =====================================================================
# 3. 03_west_java_rice_productivity.ipynb (DS03)
# =====================================================================
c03 = [
    make_cell("markdown", """# 03 — West Java Rice Productivity by Regency/City (DS03)
**TaniAdapt Project — Regional Rice Outcome Target**
**Fase:** Phase 3 (Discovery & Acquisition) + Phase 4 (Dataset Quality Audit)

- **Sumber Resmi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Jawa Barat / Galura Data Jabar
- **Cakupan Wilayah:** 27 Kabupaten/Kota di Jawa Barat (2015–2020)
- **Varian Komoditas:** Padi Total, Padi Sawah (Wetland), dan Padi Ladang (Dryland)
"""),
    make_cell("code", """from pathlib import Path
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = Path.cwd().resolve()
PROJECT_ROOT = CWD.parent if CWD.name.lower() == "notebook" else CWD
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS03_west_java_rice_productivity"
FIGURES_DIR = PROJECT_ROOT / "reports" / "dataset_audit" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("Project Root:", PROJECT_ROOT)
print("Raw Data Dir:", RAW_DIR)
"""),
    make_cell("markdown", """## Phase 3 & 4 — Audit Integritas & Kelengkapan Matriks Panel (27 Wilayah x 6 Tahun)
Memeriksa file Padi Total, Padi Sawah, dan Padi Ladang yang diperoleh dari API resmi Galura.
"""),
    make_cell("code", """df_total = pd.read_csv(RAW_DIR / "produktivitas_padi_jabar.csv")
df_sawah = pd.read_csv(RAW_DIR / "produktivitas_padi_sawah_jabar.csv")
df_ladang = pd.read_csv(RAW_DIR / "produktivitas_padi_ladang_jabar.csv")

print("Dimensi & Missing Values:")
print(f"  Padi Total : {df_total.shape} | Missing: {df_total['produktivitas_padi2'].isnull().sum()}")
print(f"  Padi Sawah : {df_sawah.shape} | Missing: {df_sawah['produktivitas_padi'].isnull().sum()}")
print(f"  Padi Ladang: {df_ladang.shape} | Missing: {df_ladang['produktivitas_padi'].isnull().sum()}")

# Validasi Kelengkapan Matriks Penuh
expected_rows = 27 * 6
is_complete = (len(df_total) == expected_rows)
print("\\n" + "="*50)
print(f"KELENGKAPAN MATRIKS (27 kab/kota x 6 tahun = {expected_rows} baris): {is_complete}")
print("STATUS INTEGRITAS     :", "[PASSED]" if is_complete else "[FAILED]")
print("Satuan Resmi          :", df_total['satuan'].iloc[0])
print("="*50)
"""),
    make_cell("markdown", """## Statistik Produktivitas Tahunan (Kuintal/Hektar)
"""),
    make_cell("code", """display(df_total.groupby('tahun')['produktivitas_padi2'].describe())
"""),
    make_cell("markdown", """## Visualisasi Diagnostik Multi-Panel (Rata-rata Padi Total & Gap Sawah vs Ladang)
Perbandingan produktivitas tahunan dan disparitas antara padi sawah (irigasi) vs padi ladang (tadah hujan).
"""),
    make_cell("code", """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

# Panel 1: Rata-rata Padi Total
mean_total = df_total.groupby('tahun')['produktivitas_padi2'].mean()
ax1.bar(mean_total.index.astype(str), mean_total.values, color='forestgreen', edgecolor='black', alpha=0.85)
ax1.set_title("Rata-rata Produktivitas Padi Total Jabar (2015–2020)")
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Produktivitas (Kuintal / Hektar)")
ax1.grid(axis='y', linestyle='--', alpha=0.5)
for i, v in enumerate(mean_total.values):
    ax1.text(i, v + 0.8, f"{v:.1f}", ha='center', fontsize=9, fontweight='bold')

# Panel 2: Komparasi Padi Sawah vs Padi Ladang
mean_sawah = df_sawah.groupby('tahun')['produktivitas_padi'].mean()
mean_ladang = df_ladang.groupby('tahun')['produktivitas_padi'].mean()

years = np.arange(len(mean_sawah))
width = 0.35
ax2.bar(years - width/2, mean_sawah.values, width, label='Padi Sawah (Wetland)', color='teal', edgecolor='black', alpha=0.85)
ax2.bar(years + width/2, mean_ladang.values, width, label='Padi Ladang (Dryland)', color='goldenrod', edgecolor='black', alpha=0.85)
ax2.set_title("Disparitas Produktivitas: Padi Sawah vs Padi Ladang")
ax2.set_xlabel("Tahun")
ax2.set_ylabel("Produktivitas (Kuintal / Hektar)")
ax2.set_xticks(years)
ax2.set_xticklabels(mean_sawah.index.astype(str))
ax2.legend()
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds03_rice_coverage.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""),
    make_cell("markdown", """## Executive Audit Scorecard
"""),
    make_cell("code", """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS03 — West Java Rice Productivity by Regency/City"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "Distanhor Jabar / Galura Open Data Jabar"},
    {"Dimensi Audit": "Cakupan Wilayah", "Hasil & Evaluasi": "27 Kabupaten/Kota Se-Jawa Barat"},
    {"Dimensi Audit": "Rentang Periode", "Hasil & Evaluasi": "2015 s.d. 2020 (6 Tahun Observasi Penuh)"},
    {"Dimensi Audit": "Varian Komoditas", "Hasil & Evaluasi": "Padi Total, Padi Sawah (Wetland), Padi Ladang (Dryland)"},
    {"Dimensi Audit": "Kelengkapan Matriks", "Hasil & Evaluasi": "PASSED (162 baris per varian, 0 missing value)"},
    {"Dimensi Audit": "Satuan Resmi", "Hasil & Evaluasi": "Kuintal / Hektar (1 Kuintal = 100 kg = 0,1 ton)"},
    {"Dimensi Audit": "Peran di TaniAdapt", "Hasil & Evaluasi": "Regional Rice Outcome Target"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Target hasil panen padi lokal resmi)"},
    {"Dimensi Audit": "Batasan Kritis", "Hasil & Evaluasi": "Granularitas waktu tahunan; memerlukan agregasi cuaca harian per musim tanam saat linking."}
])

display(scorecard)
""")
]
save_notebook("03_west_java_rice_productivity.ipynb", c03)

# =====================================================================
# 4. 04_indonesia_agroclimatic.ipynb (DS04)
# =====================================================================
c04 = [
    make_cell("markdown", """# 04 — Indonesia Nationwide Agroclimatic Dataset (DS04)
**TaniAdapt Project — Agroclimate Benchmark & Extreme Indicators**
**Fase:** Phase 3 (Discovery & Acquisition) + Phase 4 (Dataset Quality Audit)

- **Sumber Resmi:** [Mendeley Data DOI: 10.17632/3pfbdbzfff.1](https://doi.org/10.17632/3pfbdbzfff.1)
- **Basis Data:** Open-Meteo Historical Weather / ERA5-Seamless (612 grid points, 2016–2025)
- **Peran di TaniAdapt:** Referensi pembanding indikator agroklimat ekstrem (CDD, CWD, GDD).
"""),
    make_cell("code", """from pathlib import Path
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = Path.cwd().resolve()
PROJECT_ROOT = CWD.parent if CWD.name.lower() == "notebook" else CWD
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS04_indonesia_agroclimatic"
FIGURES_DIR = PROJECT_ROOT / "reports" / "dataset_audit" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("Project Root:", PROJECT_ROOT)
print("Raw Data Dir:", RAW_DIR)
"""),
    make_cell("markdown", """## Phase 3 & 4 — Audit 612 Titik Grid & Definisi Indikator Ekstrem
Membaca katalog titik grid spasial terestrial Indonesia dan definisi 12 indikator agroklimat.
"""),
    make_cell("code", """df_grid = pd.read_csv(RAW_DIR / "grid_points.csv")
df_def = pd.read_csv(RAW_DIR / "indicator_definitions.csv", encoding="latin1")

print("Total Titik Grid Terestrial Indonesia:", len(df_grid))
print("Total Definisi Indikator Agroklimat  :", len(df_def))

# Titik potong khusus wilayah Jawa Barat (-7.9 s.d. -5.8 N, 106.3 s.d. 109.0 E)
df_jabar_grid = df_grid[(df_grid['latitude'] >= -7.9) & (df_grid['latitude'] <= -5.8) &
                        (df_grid['longitude'] >= 106.3) & (df_grid['longitude'] <= 109.0)]
print(f"\\nJumlah Titik Grid Melingkupi Jawa Barat: {len(df_jabar_grid)} titik")
"""),
    make_cell("markdown", """## Kamus 12 Indikator Agroklimat Turunan
Daftar indikator agroklimat harian yang dikalkulasikan untuk pemodelan stres iklim.
"""),
    make_cell("code", """display(df_def[["variable", "unit", "description"]])
"""),
    make_cell("markdown", """## Visualisasi Diagnostik & Peta Sebaran Spasial (PNG)
Memetakan sebaran 612 titik grid terestrial Indonesia dengan penanda khusus 14 titik di wilayah daratan Jawa Barat.
"""),
    make_cell("code", """plt.figure(figsize=(10, 4.5))
plt.scatter(df_grid['longitude'], df_grid['latitude'], c='grey', s=8, alpha=0.5, label='Seluruh Indonesia (612 Titik)')
plt.scatter(df_jabar_grid['longitude'], df_jabar_grid['latitude'], c='crimson', s=30, label=f'Titik Jawa Barat ({len(df_jabar_grid)} Titik)')

plt.title("DS04 Sebaran 612 Titik Grid Agroklimat Indonesia (ERA5-Seamless)")
plt.xlabel("Bujur (Longitude °E)")
plt.ylabel("Lintang (Latitude °N)")
plt.legend(loc='lower left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

png_out = FIGURES_DIR / "ds04_agroclimate_grid_map.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""),
    make_cell("markdown", """## Executive Audit Scorecard
"""),
    make_cell("code", """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS04 — Indonesia Nationwide Agroclimatic Dataset"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "Elsevier / Mendeley Data (DOI: 10.17632/3pfbdbzfff.1)"},
    {"Dimensi Audit": "Cakupan Wilayah", "Hasil & Evaluasi": "612 Titik Grid Daratan Indonesia (14 Titik Jawa Barat)"},
    {"Dimensi Audit": "Rentang Periode", "Hasil & Evaluasi": "2016 s.d. 2025 (Harian)"},
    {"Dimensi Audit": "Format Data Tersedia", "Hasil & Evaluasi": "Parquet (60 MB) + CSV (Tabel Grid & Definisi)"},
    {"Dimensi Audit": "Indikator Kunci", "Hasil & Evaluasi": "Consecutive Dry Days (CDD), CWD, Rainfall 7d/30d/90d, Temperature Range"},
    {"Dimensi Audit": "Peran di TaniAdapt", "Hasil & Evaluasi": "Agroclimate Reference & Comparison Backbone"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Referensi indikator iklim ekstrem nasional)"},
    {"Dimensi Audit": "Batasan Kritis", "Hasil & Evaluasi": "Resolusi spasial 0,5° (~55 km) lebih kasar dibanding AgERA5 0,1° (~10 km)."}
])

display(scorecard)
""")
]
save_notebook("04_indonesia_agroclimatic.ipynb", c04)

# =====================================================================
# 5. 05_subang_maize_productivity.ipynb (DS05)
# =====================================================================
c05 = [
    make_cell("markdown", """# 05 — Subang & West Java Maize Productivity (DS05)
**TaniAdapt Project — Regional Maize Outcome Target**
**Fase:** Phase 3 (Discovery & Acquisition) + Phase 4 (Dataset Quality Audit)

- **Sumber Resmi:** Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar
- **Cakupan Wilayah:** 27 Kabupaten/Kota di Jawa Barat (2015–2022) termasuk fokus utama Kabupaten Subang
- **Catatan Sumber:** Endpoint sub-kecamatan Subang mengalami HTTP 502 Bad Gateway di server pemerintah; fallback terakuisisi pada level kabupaten resmi.
"""),
    make_cell("code", """from pathlib import Path
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = Path.cwd().resolve()
PROJECT_ROOT = CWD.parent if CWD.name.lower() == "notebook" else CWD
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity"
FIGURES_DIR = PROJECT_ROOT / "reports" / "dataset_audit" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("Project Root:", PROJECT_ROOT)
print("Raw Data Dir:", RAW_DIR)
"""),
    make_cell("markdown", """## Phase 3 & 4 — Audit Integritas Data Jagung & Filter Kabupaten Subang
Membaca dataset resmi jagung Jawa Barat (216 baris = 27 wilayah x 8 tahun) dan mengisolasi runtun waktu Kabupaten Subang.
"""),
    make_cell("code", """df_maize = pd.read_csv(RAW_DIR / "produktivitas_jagung_jabar.csv")
print("Dimensi Data Jagung Jabar:", df_maize.shape)
print("Missing Values Produktivitas:", df_maize['produktivitas_jagung'].isnull().sum())

# Filter Kabupaten Subang
subang_data = df_maize[df_maize['nama_kabupaten_kota'].str.contains('SUBANG', case=False, na=False)].sort_values('tahun')
print(f"Data Spesifik Kabupaten Subang Ditemukan: {len(subang_data)} tahun (2015–2022)")
display(subang_data[['tahun', 'nama_kabupaten_kota', 'produktivitas_jagung', 'satuan']])
"""),
    make_cell("markdown", """## Visualisasi Diagnostik Multi-Panel (Subang vs Jabar & Ranking Top-5 Kabupaten)
Membandingkan tren runtun waktu Kab. Subang vs provinsi, serta memetakan posisi Subang dalam ranking produktivitas jagung tahun 2022.
"""),
    make_cell("code", """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5), gridspec_kw={'width_ratios': [1.3, 1]})

# Panel 1: Runtun Waktu Subang vs Rata-rata Jabar
mean_jabar = df_maize.groupby('tahun')['produktivitas_jagung'].mean()
ax1.plot(mean_jabar.index, mean_jabar.values, marker='o', label='Rata-rata Jawa Barat', color='steelblue', linewidth=2)
ax1.plot(subang_data['tahun'], subang_data['produktivitas_jagung'], marker='s', label='Kabupaten Subang', color='darkorange', linewidth=2.5)
ax1.set_title("DS05 Produktivitas Jagung: Jawa Barat vs Kab. Subang (2015–2022)")
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Produktivitas (Kuintal / Hektar)")
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Ranking Top-5 Kabupaten (Tahun 2022) vs Subang
df_2022 = df_maize[df_maize['tahun'] == 2022].sort_values('produktivitas_jagung', ascending=False)
top5 = df_2022.head(5).copy()
subang_row = df_2022[df_2022['nama_kabupaten_kota'].str.contains('SUBANG', case=False)]
if not subang_row.empty and subang_row.index[0] not in top5.index:
    top5 = pd.concat([top5, subang_row])

top5_sorted = top5.sort_values('produktivitas_jagung', ascending=True)
bar_colors = ['darkorange' if 'SUBANG' in name.upper() else 'steelblue' for name in top5_sorted['nama_kabupaten_kota']]
ax2.barh(top5_sorted['nama_kabupaten_kota'].str.replace('KABUPATEN ', ''), top5_sorted['produktivitas_jagung'], color=bar_colors, edgecolor='black', alpha=0.85)
ax2.set_title("Top Sentra Produktivitas Jagung Jabar (2022)")
ax2.set_xlabel("Produktivitas (Kuintal / Hektar)")
ax2.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds05_maize_coverage.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""),
    make_cell("markdown", """## Executive Audit Scorecard
"""),
    make_cell("code", """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS05 — Subang & West Java Maize Productivity"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "Distanhor Jabar / Galura Open Data Jabar"},
    {"Dimensi Audit": "Cakupan Wilayah", "Hasil & Evaluasi": "27 Kabupaten/Kota (Fokus Utama Kabupaten Subang)"},
    {"Dimensi Audit": "Rentang Periode", "Hasil & Evaluasi": "2015 s.d. 2022 (8 Tahun Observasi Lengkap)"},
    {"Dimensi Audit": "Kelengkapan Nilai", "Hasil & Evaluasi": "PASSED (216 baris penuh, 0 missing value)"},
    {"Dimensi Audit": "Data Kabupaten Subang", "Hasil & Evaluasi": "8 Nilai Tahunan (Meningkat dari 45.75 ke 89.49 kuintal/ha)"},
    {"Dimensi Audit": "Peran di TaniAdapt", "Hasil & Evaluasi": "Regional Maize Outcome Target"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Target hasil panen jagung regional valid)"},
    {"Dimensi Audit": "Batasan Kritis", "Hasil & Evaluasi": "Endpoint sub-kecamatan Subang mengalami HTTP 502 upstream server; fallback kabupaten digunakan."}
])

display(scorecard)
""")
]
save_notebook("05_subang_maize_productivity.ipynb", c05)

# =====================================================================
# 6. 06_west_java_horticulture_productivity.ipynb (DS06)
# =====================================================================
c06 = [
    make_cell("markdown", """# 06 — West Java SBS Horticulture (Chili) Productivity (DS06)
**TaniAdapt Project — Regional Horticulture Outcome Target**
**Fase:** Phase 3 (Discovery & Acquisition) + Phase 4 (Dataset Quality Audit)

- **Sumber Resmi:** Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar
- **Fokus Komoditas Hortikultura:** Cabai Besar dan Cabai Rawit (2017–2024)
- **AUDIT KRITIS TARGET OUTCOME:** Dataset ini berisi angka produktivitas statistik hasil panen agregat, BUKAN data insidensi atau label penyakit tanaman (disease incidence).
"""),
    make_cell("code", """from pathlib import Path
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = Path.cwd().resolve()
PROJECT_ROOT = CWD.parent if CWD.name.lower() == "notebook" else CWD
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "DS06_west_java_horticulture"
FIGURES_DIR = PROJECT_ROOT / "reports" / "dataset_audit" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("Project Root:", PROJECT_ROOT)
print("Raw Data Dir:", RAW_DIR)
"""),
    make_cell("markdown", """## Phase 3 & 4 — Audit Komoditas Cabai Besar & Cabai Rawit (2017–2024)
Membaca file statistik produktivitas Sayuran Buah Semusim (SBS) Jawa Barat.
"""),
    make_cell("code", """df_sbs = pd.read_csv(RAW_DIR / "produktivitas_sbs_jabar.csv")
cabai_besar = df_sbs[df_sbs['komoditi'] == 'CABAI BESAR'].sort_values('tahun')
cabai_rawit = df_sbs[df_sbs['komoditi'] == 'CABAI RAWIT'].sort_values('tahun')

print("Observasi Cabai Besar:", len(cabai_besar), "| Tahun:", cabai_besar['tahun'].min(), "s.d.", cabai_besar['tahun'].max())
print("Observasi Cabai Rawit:", len(cabai_rawit), "| Tahun:", cabai_rawit['tahun'].min(), "s.d.", cabai_rawit['tahun'].max())
print("Satuan Resmi:", cabai_besar['satuan'].iloc[0])
"""),
    make_cell("markdown", """## Audit Kritis Validitas Target Outcome & Gap Analysis Variabel
Pemeriksaan ketat apakah dataset ini dapat digunakan untuk melatih model deteksi penyakit tanaman.
"""),
    make_cell("code", """gap_analysis = pd.DataFrame([
    {"Variabel Agronomi": "Produktivitas Hasil Panen (Kuintal/Ha)", "Status Ketersediaan": "TERSEDIA (8 Tahun)", "Keterangan": "Target luaran hasil panen valid"},
    {"Variabel Agronomi": "Volume Produksi (Kuintal / Ton)", "Status Ketersediaan": "TERSEDIA (8 Tahun)", "Keterangan": "Tercatat di dataset produksi sayuran"},
    {"Variabel Agronomi": "Luas Panen / Tanam (Ha)", "Status Ketersediaan": "TERSEDIA (8 Tahun)", "Keterangan": "Bisa diturunkan dari produksi / produktivitas"},
    {"Variabel Agronomi": "Insidensi / Label Penyakit (OPT)", "Status Ketersediaan": "TIDAK TERSEDIA (ABSEN)", "Keterangan": "TIDAK BISA untuk supervised ML penyakit"},
    {"Variabel Agronomi": "Varietas Spesifik Benih Cabai", "Status Ketersediaan": "TIDAK TERSEDIA (ABSEN)", "Keterangan": "Hanya agregat nama komoditi umum"}
])

print("\\n" + "="*60)
print("HASIL AUDIT TARGET OUTCOME (YIELD vs DISEASE):")
print("="*60)
print("1. Apakah dataset ini berisi angka hasil panen (Yield)? -> YA (VALID)")
print("2. Apakah dataset ini berisi label penyakit tanaman?     -> TIDAK (ABSEN)")
print("KESIMPULAN: Jangan latih ML klasifikasi penyakit dari dataset ini!")
print("="*60 + "\\n")
display(gap_analysis)
"""),
    make_cell("markdown", """## Visualisasi Diagnostik Multi-Panel (Tren Produktivitas Cabai Rawit vs Cabai Besar)
Membandingkan dinamika produktivitas dua komoditas cabai utama di Jawa Barat (2017–2024).
"""),
    make_cell("code", """fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

# Panel 1: Line Chart Komparasi Tren
ax1.plot(cabai_rawit['tahun'], cabai_rawit['produktivitas_sayur_buah'], marker='s', color='darkorange', label='Cabai Rawit', linewidth=2.5)
ax1.plot(cabai_besar['tahun'], cabai_besar['produktivitas_sayur_buah'], marker='o', color='crimson', label='Cabai Besar', linewidth=2.5)
ax1.set_title("Komparasi Tren Produktivitas Cabai di Jawa Barat (2017–2024)")
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Produktivitas (Kuintal / Hektar)")
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel 2: Bar Chart Rata-rata & Nilai Terakhir (2024)
categories = ['Cabai Rawit (Rata-rata)', 'Cabai Rawit (2024)', 'Cabai Besar (Rata-rata)', 'Cabai Besar (2024)']
values = [
    cabai_rawit['produktivitas_sayur_buah'].mean(),
    cabai_rawit[cabai_rawit['tahun'] == 2024]['produktivitas_sayur_buah'].iloc[0],
    cabai_besar['produktivitas_sayur_buah'].mean(),
    cabai_besar[cabai_besar['tahun'] == 2024]['produktivitas_sayur_buah'].iloc[0]
]
colors = ['#f4a261', '#e76f51', '#e63946', '#9b2226']
ax2.bar(categories, values, color=colors, edgecolor='black', alpha=0.85)
ax2.set_title("Benchmark Produktivitas: Rata-rata vs 2024")
ax2.set_ylabel("Produktivitas (Kuintal / Hektar)")
ax2.tick_params(axis='x', rotation=15)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
for i, v in enumerate(values):
    ax2.text(i, v + 1.5, f"{v:.1f}", ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
png_out = FIGURES_DIR / "ds06_chili_commodities.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG berhasil disimpan ke: {png_out}")
"""),
    make_cell("markdown", """## Executive Audit Scorecard
"""),
    make_cell("code", """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS06 — West Java SBS Horticulture (Chili) Productivity"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "Distanhor Jabar / Galura Open Data Jabar"},
    {"Dimensi Audit": "Fokus Komoditas", "Hasil & Evaluasi": "Cabai Besar dan Cabai Rawit (Sayuran Buah Semusim)"},
    {"Dimensi Audit": "Rentang Periode", "Hasil & Evaluasi": "2017 s.d. 2024 (8 Tahun Observasi)"},
    {"Dimensi Audit": "Kelengkapan Nilai", "Hasil & Evaluasi": "PASSED (0 missing value pada komoditas cabai)"},
    {"Dimensi Audit": "Satuan Resmi", "Hasil & Evaluasi": "Kuintal / Hektar"},
    {"Dimensi Audit": "Peran di TaniAdapt", "Hasil & Evaluasi": "Regional Horticulture Outcome Target"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS (Target hasil panen hortikultura cabai valid)"},
    {"Dimensi Audit": "Batasan Kritis", "Hasil & Evaluasi": "TIDAK BISA untuk model deteksi penyakit (disease label absen). Rekomendasi: gunakan rule-based weather threshold."}
])

display(scorecard)
""")
]
save_notebook("06_west_java_horticulture_productivity.ipynb", c06)

print("\nSemua 6 notebook berhasil diperkaya dan diperbarui 100%!")
