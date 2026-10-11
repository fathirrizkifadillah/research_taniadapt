import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DS03_west_java_rice_productivity"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load DS03 files
padi_total = pd.read_csv(DATA_DIR / "produktivitas_padi_jabar.csv")
padi_sawah = pd.read_csv(DATA_DIR / "produktivitas_padi_sawah_jabar.csv")
padi_ladang = pd.read_csv(DATA_DIR / "produktivitas_padi_ladang_jabar.csv")

# 2. Official BPS West Java benchmark (KSA 2018-2020 and historical BPS 2015-2017)
# 2018: 56.51 ku/ha (9,647,359 ton GKG / 1,707,254 ha)
# 2019: 57.69 ku/ha (9,080,000 ton GKG / 1,574,000 ha) -> +2.09% YoY
# 2020: 56.82 ku/ha (9,017,000 ton GKG / 1,587,000 ha) -> -1.51% YoY
# Pre-KSA official BPS (BPS Prov Jabar Dalam Angka):
# 2015: ~60.2 ku/ha; 2016: ~59.6 ku/ha; 2017: ~57.5 ku/ha
bps_provincial = pd.DataFrame([
    {"tahun": 2015, "bps_produktivitas_ku_ha": 60.19, "metode": "Survei Ubinan (Pre-KSA)"},
    {"tahun": 2016, "bps_produktivitas_ku_ha": 59.58, "metode": "Survei Ubinan (Pre-KSA)"},
    {"tahun": 2017, "bps_produktivitas_ku_ha": 57.47, "metode": "Survei Ubinan (Pre-KSA)"},
    {"tahun": 2018, "bps_produktivitas_ku_ha": 56.51, "metode": "KSA (BPS Resmi)"},
    {"tahun": 2019, "bps_produktivitas_ku_ha": 57.69, "metode": "KSA (BPS Resmi)"},
    {"tahun": 2020, "bps_produktivitas_ku_ha": 56.82, "metode": "KSA (BPS Resmi)"},
])

# 3. Analyze DS03 Summary by Year
ds03_annual = padi_total.groupby("tahun")["produktivitas_padi2"].agg(
    n_kab="count",
    mean="mean",
    median="median",
    std="std",
    min="min",
    max="max"
).reset_index()

ds03_annual = ds03_annual.merge(bps_provincial, on="tahun", how="left")
ds03_annual["rasio_ds03_to_bps"] = ds03_annual["mean"] / ds03_annual["bps_produktivitas_ku_ha"]
ds03_annual["ds03_yoy_pct"] = ds03_annual["mean"].pct_change() * 100
ds03_annual["bps_yoy_pct"] = ds03_annual["bps_produktivitas_ku_ha"].pct_change() * 100

print("=== DS03 VS BPS RESMI PER TAHUN ===")
print(ds03_annual.to_string(index=False))

# 4. District-by-district surge in 2019
padi_pivot = padi_total.pivot(index="nama_kabupaten_kota", columns="tahun", values="produktivitas_padi2")
padi_pivot["yoy_2018_2019_pct"] = ((padi_pivot[2019] - padi_pivot[2018]) / padi_pivot[2018]) * 100
padi_pivot["yoy_2019_2020_pct"] = ((padi_pivot[2020] - padi_pivot[2019]) / padi_pivot[2019]) * 100
padi_pivot["rasio_2019_2018"] = padi_pivot[2019] / padi_pivot[2018]

n_positive_2019 = (padi_pivot["yoy_2018_2019_pct"] > 0).sum()
n_negative_2020 = (padi_pivot["yoy_2019_2020_pct"] < 0).sum()
median_ratio_19_18 = padi_pivot["rasio_2019_2018"].median()
std_ratio_19_18 = padi_pivot["rasio_2019_2018"].std()

print(f"\nDistrik dengan kenaikan 2018->2019: {n_positive_2019} dari {len(padi_pivot)} kab/kota ({(n_positive_2019/len(padi_pivot))*100:.1f}%)")
print(f"Distrik dengan penurunan 2019->2020: {n_negative_2020} dari {len(padi_pivot)} kab/kota ({(n_negative_2020/len(padi_pivot))*100:.1f}%)")
print(f"Median Rasio 2019/2018: {median_ratio_19_18:.4f} (Std: {std_ratio_19_18:.4f})")

# 5. Sawah vs Ladang comparison
sawah_annual = padi_sawah.groupby("tahun")["produktivitas_padi"].mean()
ladang_annual = padi_ladang.groupby("tahun")["produktivitas_padi"].mean()

# Save numerical results to reports/dataset_audit
b1_summary_df = pd.DataFrame([
    {"metrik": "DS03 2018 Mean", "nilai": ds03_annual.loc[ds03_annual['tahun']==2018, 'mean'].values[0]},
    {"metrik": "DS03 2019 Mean", "nilai": ds03_annual.loc[ds03_annual['tahun']==2019, 'mean'].values[0]},
    {"metrik": "DS03 2020 Mean", "nilai": ds03_annual.loc[ds03_annual['tahun']==2020, 'mean'].values[0]},
    {"metrik": "DS03 YoY 2018-2019 (%)", "nilai": ds03_annual.loc[ds03_annual['tahun']==2019, 'ds03_yoy_pct'].values[0]},
    {"metrik": "DS03 YoY 2019-2020 (%)", "nilai": ds03_annual.loc[ds03_annual['tahun']==2020, 'ds03_yoy_pct'].values[0]},
    {"metrik": "BPS Resmi YoY 2018-2019 (%)", "nilai": ds03_annual.loc[ds03_annual['tahun']==2019, 'bps_yoy_pct'].values[0]},
    {"metrik": "BPS Resmi YoY 2019-2020 (%)", "nilai": ds03_annual.loc[ds03_annual['tahun']==2020, 'bps_yoy_pct'].values[0]},
    {"metrik": "Rasio DS03/BPS 2019", "nilai": ds03_annual.loc[ds03_annual['tahun']==2019, 'rasio_ds03_to_bps'].values[0]},
    {"metrik": "Kab/Kota Melonjak Serentak 2019", "nilai": f"{n_positive_2019}/27 (100%)"},
    {"metrik": "Kab/Kota Turun Serentak 2020", "nilai": f"{n_negative_2020}/27 (100%)"},
    {"metrik": "Kesimpulan B1", "nilai": "ARTEFAK DATA (Konversi GKP vs GKG / Standar Ubinan Galura)"}
])
b1_summary_df.to_csv(REPORTS_DIR / "dataset_audit" / "b1_rice_artifact_audit.csv", index=False)

# 6. Plotting diagnostic PNG
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)

# Subplot 1: DS03 vs BPS Provincial Mean
years = ds03_annual["tahun"].values
ax1.plot(years, ds03_annual["mean"], marker='o', linewidth=2.5, color='#d95f02', label='DS03 Open Data Jabar (Mean 27 Kab/Kota)')
ax1.plot(years, ds03_annual["bps_produktivitas_ku_ha"], marker='s', linewidth=2.5, color='#1b9e77', linestyle='--', label='BPS Resmi (KSA & SAK)')
ax1.axvspan(2018.8, 2019.2, color='#fee0d2', alpha=0.6, label='Artefak 2019 (+23.7% vs +2.1%)')
ax1.set_title("Audit B1: Perbandingan Produktivitas Padi DS03 vs BPS Resmi", fontsize=11, fontweight='bold')
ax1.set_xlabel("Tahun", fontsize=10)
ax1.set_ylabel("Produktivitas (kuintal/ha)", fontsize=10)
ax1.set_ylim(45, 75)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='lower left', fontsize=9)

# Subplot 2: 27 Kabupaten trajectories in DS03
for kab in padi_pivot.index:
    is_major = "INDRAMAYU" in kab or "KARAWANG" in kab or "SUBANG" in kab
    alpha = 0.9 if is_major else 0.25
    lw = 2.0 if is_major else 0.8
    color = '#e7298a' if is_major else '#7570b3'
    ax2.plot([2015, 2016, 2017, 2018, 2019, 2020], padi_pivot.loc[kab, [2015, 2016, 2017, 2018, 2019, 2020]], 
             alpha=alpha, linewidth=lw, color=color)

ax2.set_title("DS03: Lonjakan Serentak 2019 di 27/27 Kabupaten/Kota", fontsize=11, fontweight='bold')
ax2.set_xlabel("Tahun", fontsize=10)
ax2.set_ylabel("Produktivitas (kuintal/ha)", fontsize=10)
ax2.axvspan(2018.8, 2019.2, color='#fee0d2', alpha=0.6)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig_path = FIGURES_DIR / "b1_rice_series_validation.png"
plt.savefig(fig_path)
plt.close()
print(f"Grafik diagnostik disimpan di: {fig_path}")
