import os
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
AUDIT_DIR = REPORTS_DIR / "dataset_audit"

# 1. Load Jagung & Kedelai data
jagung_path = PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity" / "produktivitas_jagung_jabar.csv"
kedelai_path = PROJECT_ROOT / "data" / "raw" / "produktivitas_kedelai_jabar.csv"

df_jagung = pd.read_csv(jagung_path)
df_kedelai = pd.read_csv(kedelai_path)

print("Jagung columns:", df_jagung.columns.tolist())
print("Kedelai columns:", df_kedelai.columns.tolist())

# Function to compute YoY log diff panel
def analyze_crop_panel(df, val_col, crop_name):
    df_clean = df.copy()
    # Ensure positive values for log
    df_clean = df_clean[df_clean[val_col] > 0].copy()
    df_clean["ln_yield"] = np.log(df_clean[val_col])
    
    # Sort and compute log diff
    df_clean = df_clean.sort_values(["nama_kabupaten_kota", "tahun"])
    df_clean["prev_year"] = df_clean.groupby("nama_kabupaten_kota")["tahun"].shift(1)
    df_clean["prev_ln_yield"] = df_clean.groupby("nama_kabupaten_kota")["ln_yield"].shift(1)
    
    # Only keep strict 1-year differences
    df_diff = df_clean[df_clean["tahun"] - df_clean["prev_year"] == 1].copy()
    df_diff["log_diff"] = df_diff["ln_yield"] - df_diff["prev_ln_yield"]
    df_diff["pct_change"] = (np.exp(df_diff["log_diff"]) - 1) * 100
    
    # Summary per year
    yearly_summary = df_diff.groupby("tahun").agg(
        n_obs=("log_diff", "count"),
        median_log_diff=("log_diff", "median"),
        mean_log_diff=("log_diff", "mean"),
        std_log_diff=("log_diff", "std"),
        n_up=("log_diff", lambda x: (x > 0).sum()),
        n_down=("log_diff", lambda x: (x < 0).sum())
    ).reset_index()
    yearly_summary["crop"] = crop_name
    
    # Check Subang specifically
    subang_diff = df_diff[df_diff["nama_kabupaten_kota"].str.upper().str.contains("SUBANG")]
    
    return df_clean, df_diff, yearly_summary, subang_diff

df_jagung_clean, jagung_diff, jagung_yearly, jagung_subang = analyze_crop_panel(df_jagung, "produktivitas_jagung", "Jagung")
df_kedelai_clean, kedelai_diff, kedelai_yearly, kedelai_subang = analyze_crop_panel(df_kedelai, "produktivitas_kedelai", "Kedelai")

print("=== YOY LOG DIFF SUMMARY JAGUNG ===")
print(jagung_yearly.to_string(index=False))

print("\n=== SUBANG YOY LOG DIFF JAGUNG ===")
print(jagung_subang[["tahun", "log_diff", "pct_change"]].to_string(index=False))

print("\n=== YOY LOG DIFF SUMMARY KEDELAI ===")
print(kedelai_yearly.to_string(index=False))

# 2. Linear Trends per Kabupaten for Jagung
kab_trends = []
for kab, grp in df_jagung.groupby("nama_kabupaten_kota"):
    if len(grp) >= 4 and (grp["produktivitas_jagung"] > 0).sum() >= 4:
        valid_grp = grp[grp["produktivitas_jagung"] > 0]
        x = valid_grp["tahun"] - valid_grp["tahun"].min()
        y = valid_grp["produktivitas_jagung"]
        slope, intercept = np.polyfit(x, y, 1)
        mean_y = y.mean()
        std_y = y.std(ddof=1)
        cv_y = (std_y / mean_y) * 100
        
        # Residuals
        y_pred = intercept + slope * x
        resid = y - y_pred
        std_resid = resid.std(ddof=1)
        cv_resid = (std_resid / mean_y) * 100
        
        kab_trends.append({
            "kabupaten": kab,
            "n_years": len(valid_grp),
            "mean_yield": mean_y,
            "slope_ku_ha_per_year": slope,
            "raw_cv_pct": cv_y,
            "residual_cv_pct": cv_resid
        })

df_trends = pd.DataFrame(kab_trends).sort_values("slope_ku_ha_per_year", ascending=False)
print("\n=== TOP & BOTTOM JAGUNG TRENDS PER KABUPATEN ===")
print(pd.concat([df_trends.head(5), df_trends.tail(5)]).to_string(index=False))

# 3. Three Detrending Methods Comparison on Maize Panel
# We evaluate on full panel where yield > 0
# Method 1: Separate linear trend per kabupaten
residuals_m1 = []
for kab, grp in df_jagung_clean.groupby("nama_kabupaten_kota"):
    if len(grp) >= 3:
        x = grp["tahun"] - grp["tahun"].min()
        res = sm.OLS(grp["ln_yield"], sm.add_constant(x)).fit()
        residuals_m1.extend(res.resid.tolist())
var_m1 = np.var(residuals_m1, ddof=1)
cv_m1 = np.std(residuals_m1, ddof=1) * 100 # approximate log residual CV

# Method 2: Kabupaten FE + Provincial Linear Trend
model_m2 = smf.ols("ln_yield ~ C(nama_kabupaten_kota) + tahun", data=df_jagung_clean).fit()
residuals_m2 = model_m2.resid
var_m2 = np.var(residuals_m2, ddof=1)
cv_m2 = np.std(residuals_m2, ddof=1) * 100

# Method 3: Kabupaten FE + Year FE (Two-way Fixed Effects)
model_m3 = smf.ols("ln_yield ~ C(nama_kabupaten_kota) + C(tahun)", data=df_jagung_clean).fit()
residuals_m3 = model_m3.resid
var_m3 = np.var(residuals_m3, ddof=1)
cv_m3 = np.std(residuals_m3, ddof=1) * 100

detrending_comp = pd.DataFrame([
    {
        "metode": "1. Tren Linier per Kabupaten",
        "rumus": "ln(Y_it) = alpha_i + beta_i * t + eps_it",
        "dof_residual": len(df_jagung_clean) - 2 * df_jagung_clean["nama_kabupaten_kota"].nunique(),
        "std_residual_log": np.std(residuals_m1, ddof=1),
        "cv_residual_pct": cv_m1,
        "variasi_cuaca_yang_tersisa": "Variasi temporal non-linier spesifik kabupaten (menyisakan variasi cuaca bersama & lokal)"
    },
    {
        "metode": "2. Kabupaten FE + Tren Linier Provinsi",
        "rumus": "ln(Y_it) = alpha_i + beta_prov * t + eps_it",
        "dof_residual": model_m2.df_resid,
        "std_residual_log": np.std(residuals_m2, ddof=1),
        "cv_residual_pct": cv_m2,
        "variasi_cuaca_yang_tersisa": "Variasi temporal lintas tahun (baik bersama maupun deviasi antar-kabupaten)"
    },
    {
        "metode": "3. Two-Way FE (Kabupaten FE + Year FE)",
        "rumus": "ln(Y_it) = alpha_i + gamma_t + eps_it",
        "dof_residual": model_m3.df_resid,
        "std_residual_log": np.std(residuals_m3, ddof=1),
        "cv_residual_pct": cv_m3,
        "variasi_cuaca_yang_tersisa": "HANYA deviasi cuaca lokal antar-kabupaten dalam tahun yang sama; menghapus 100% variasi cuaca bersama tahunan (misal El Nino / La Nina)"
    }
])

print("\n=== PERBANDINGAN TIGA METODE DETRENDING (JAGUNG) ===")
print(detrending_comp[["metode", "std_residual_log", "cv_residual_pct", "variasi_cuaca_yang_tersisa"]].to_string(index=False))

# Save outputs
detrending_comp.to_csv(AUDIT_DIR / "b2_maize_detrending_comparison.csv", index=False)
df_trends.to_csv(AUDIT_DIR / "b2_maize_kabupaten_trends.csv", index=False)
jagung_yearly.to_csv(AUDIT_DIR / "b2_maize_yoy_summary.csv", index=False)
kedelai_yearly.to_csv(AUDIT_DIR / "b2_soybean_yoy_summary.csv", index=False)

# 4. Diagnostic PNG Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)

# Subplot 1: Distribution of YoY log diffs
ax1 = axes[0]
years = jagung_yearly["tahun"].values
bar_w = 0.35
ax1.bar(years - bar_w/2, jagung_yearly["n_up"], width=bar_w, label='Kabupaten Naik', color='#2ca25f')
ax1.bar(years + bar_w/2, jagung_yearly["n_down"], width=bar_w, label='Kabupaten Turun', color='#e34a33')
ax1.set_title("Audit B2: Proporsi Kabupaten Naik vs Turun Tiap Tahun (Jagung)", fontsize=11, fontweight='bold')
ax1.set_xlabel("Tahun", fontsize=10)
ax1.set_ylabel("Jumlah Kabupaten", fontsize=10)
ax1.set_xticks(years)
ax1.legend()
ax1.grid(True, linestyle=':', alpha=0.6)

# Subplot 2: Subang vs Key Production Centers (Garut, Indramayu, Cianjur, Majalengka)
ax2 = axes[1]
centers = ["KABUPATEN SUBANG", "KABUPATEN GARUT", "KABUPATEN INDRAMAYU", "KABUPATEN CIANJUR", "KABUPATEN MAJALENGKA"]
palette = {"KABUPATEN SUBANG": '#d95f02', "KABUPATEN GARUT": '#7570b3', "KABUPATEN INDRAMAYU": '#1b9e77', 
           "KABUPATEN CIANJUR": '#e7298a', "KABUPATEN MAJALENGKA": '#66a61e'}

for kab in centers:
    sub = df_jagung[df_jagung["nama_kabupaten_kota"].str.upper() == kab].sort_values("tahun")
    if len(sub) > 0:
        lw = 2.8 if kab == "KABUPATEN SUBANG" else 1.5
        ls = '-' if kab == "KABUPATEN SUBANG" else '--'
        ax2.plot(sub["tahun"], sub["produktivitas_jagung"], marker='o', linewidth=lw, linestyle=ls,
                 color=palette[kab], label=kab.replace("KABUPATEN ", ""))

ax2.set_title("Trayektori Jagung: Subang (Outlier) vs Sentra Lain", fontsize=11, fontweight='bold')
ax2.set_xlabel("Tahun", fontsize=10)
ax2.set_ylabel("Produktivitas (ku/ha)", fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(fontsize=9)

plt.tight_layout()
fig_path = FIGURES_DIR / "b2_maize_soybean_trends.png"
plt.savefig(fig_path)
plt.close()
print(f"Grafik diagnostik disimpan di: {fig_path}")
