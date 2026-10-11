import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"

# Load Kedelai
df_kedelai = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "produktivitas_kedelai_jabar.csv")
# Load Tomat (from SBS)
df_sbs = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS06_west_java_horticulture" / "produktivitas_sbs_jabar.csv")
df_tomat = df_sbs[df_sbs["komoditi"].str.upper() == "TOMAT"]

# Metrics for Kedelai
ked_total = len(df_kedelai)
ked_pos = (df_kedelai["produktivitas_kedelai"] > 0).sum()
ked_zero = (df_kedelai["produktivitas_kedelai"] == 0).sum()
ked_kab_pos = df_kedelai[df_kedelai["produktivitas_kedelai"] > 0].groupby("nama_kabupaten_kota")["tahun"].count()
ked_kab_ge6 = (ked_kab_pos >= 6).sum()
ked_kab_8 = (ked_kab_pos == 8).sum()

ked_vals = df_kedelai.loc[df_kedelai["produktivitas_kedelai"] > 0, "produktivitas_kedelai"]
ked_cv = (ked_vals.std(ddof=1) / ked_vals.mean()) * 100

# Residual CV of Kedelai across active kabupaten
# linear trend per kabupaten
ked_resids = []
for kab, grp in df_kedelai.groupby("nama_kabupaten_kota"):
    pos_grp = grp[grp["produktivitas_kedelai"] > 0]
    if len(pos_grp) >= 4:
        x = pos_grp["tahun"] - pos_grp["tahun"].min()
        y = pos_grp["produktivitas_kedelai"]
        p = np.polyfit(x, y, 1)
        r = y - np.polyval(p, x)
        ked_resids.extend((r / y.mean()).tolist())
ked_resid_cv = np.std(ked_resids, ddof=1) * 100

# Metrics for Tomat
tom_total = len(df_tomat)
tom_pos = (df_tomat["produktivitas_sayur_buah"] > 0).sum()
tom_vals = df_tomat["produktivitas_sayur_buah"]
tom_cv = (tom_vals.std(ddof=1) / tom_vals.mean()) * 100

# Residual CV of Tomat (provincial trend)
x_t = df_tomat["tahun"] - df_tomat["tahun"].min()
y_t = df_tomat["produktivitas_sayur_buah"]
p_t = np.polyfit(x_t, y_t, 1)
r_t = y_t - np.polyval(p_t, x_t)
tom_resid_cv = (np.std(r_t, ddof=1) / y_t.mean()) * 100

comparison_data = [
    {
        "dimensi": "Resolusi Administratif",
        "kedelai": "Tingkat Kabupaten/Kota (ADM2)",
        "tomat": "Tingkat Provinsi Jawa Barat (ADM1 agregat)",
        "keunggulan_komparatif": "Kedelai memiliki variasi spasial lokal antar-kabupaten"
    },
    {
        "dimensi": "Total Baris Data",
        "kedelai": f"{ked_total} baris",
        "tomat": f"{tom_total} baris",
        "keunggulan_komparatif": f"Kedelai memiliki observasi jauh lebih masif (rasio {ked_total//tom_total}x lipat)"
    },
    {
        "dimensi": "Observasi Positif (> 0)",
        "kedelai": f"{ked_pos} baris ({ked_pos/ked_total*100:.1f}%)",
        "tomat": f"{tom_pos} baris (100.0%)",
        "keunggulan_komparatif": "Tomat lengkap di tingkat provinsi; Kedelai memiliki 156 observasi empiris di kabupaten"
    },
    {
        "dimensi": "Kabupaten Aktif >= 6 Tahun",
        "kedelai": f"{ked_kab_ge6} kabupaten/kota",
        "tomat": "0 (data kabupaten tidak tersedia di DS06)",
        "keunggulan_komparatif": "Kedelai memenuhi syarat pembentukan panel ekonometrika mikro"
    },
    {
        "dimensi": "Sentra Penuh 8 Tahun (2015-2022)",
        "kedelai": f"{ked_kab_8} kabupaten sentra utama",
        "tomat": "N/A (hanya runtun waktu provinsi N=8)",
        "keunggulan_komparatif": "14 sentra kedelai memiliki deret waktu penuh tanpa celah"
    },
    {
        "dimensi": "Koefisien Variasi Mentah (Raw CV)",
        "kedelai": f"{ked_cv:.2f}%",
        "tomat": f"{tom_cv:.2f}%",
        "keunggulan_komparatif": "Kedelai mencerminkan variabilitas riil di lapangan antar-wilayah"
    },
    {
        "dimensi": "Koefisien Variasi Residual (Detrended CV)",
        "kedelai": f"{ked_resid_cv:.2f}%",
        "tomat": f"{tom_resid_cv:.2f}%",
        "keunggulan_komparatif": "Variasi residual kedelai (~22%) memadai untuk pengujian anomali cuaca"
    },
    {
        "dimensi": "Dukungan Literatur di Repositori",
        "kedelai": "Paper 13 (Heino et al., 2023) & Paper 14 (Hu et al., 2024)",
        "tomat": "Tidak ada paper spesifik tomat (diduga keselarasan famili Solanaceae dg cabai)",
        "keunggulan_komparatif": "Kedelai secara eksplisit diteliti dalam Paper 13 & 14"
    },
    {
        "dimensi": "Modul Engine yang Digunakan",
        "kedelai": "Panel Regression Statistical Engine (Tier A)",
        "tomat": "IFWC Rule-Based Microclimate Moisture Engine (Tier B)",
        "keunggulan_komparatif": "Tomat berbagi modul mikroklimat kelembapan dengan Cabai"
    },
    {
        "dimensi": "Rekomendasi Penempatan Tier",
        "kedelai": "TIER A (Uji Empiris di Phase 6 EDA; gugurkan jika sinyal nol)",
        "tomat": "TIER B (Aturan Literatur & Transfer Mikroklimat; tanpa regresi yield)",
        "keunggulan_komparatif": "Memisahkan komoditas berbasis bukti panel vs komoditas berbasis transfer aturan"
    }
]

df_comp = pd.DataFrame(comparison_data)
out_csv = AUDIT_DIR / "soybean_vs_tomato_comparison.csv"
df_comp.to_csv(out_csv, index=False)
print(f"Berhasil membuat tabel perbandingan kedelai vs tomat di {out_csv}!")
print(df_comp[["dimensi", "kedelai", "tomat"]].to_string(index=False))
