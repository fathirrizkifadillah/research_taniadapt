import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df_padi = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS03_west_java_rice_productivity" / "produktivitas_padi_jabar.csv")
df_jagung = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity" / "produktivitas_jagung_jabar.csv")
df_kedelai = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "produktivitas_kedelai_jabar.csv")

def evaluate_crop_units(df, val_col, crop_name, max_years):
    records = []
    for kab, grp in df.groupby("nama_kabupaten_kota"):
        is_kota = "KOTA" in kab.upper()
        n_obs = len(grp)
        n_pos = (grp[val_col] > 0).sum()
        n_zero = (grp[val_col] == 0).sum()
        mean_val = grp.loc[grp[val_col] > 0, val_col].mean() if n_pos > 0 else 0
        std_val = grp.loc[grp[val_col] > 0, val_col].std(ddof=1) if n_pos > 1 else 0
        cv_val = (std_val / mean_val) * 100 if mean_val > 0 else 0
        
        # Criteria:
        # 1. Active years >= 6 (or all years if max_years <= 6)
        # 2. If Kota: must have n_pos >= 6 AND cv_val <= 30.0%
        # 3. Non-zero rate >= 75%
        included = False
        alasan = ""
        
        if n_pos < (max_years - 2):
            included = False
            alasan = f"Eksklusi: Tahun aktif kurang ({n_pos}/{max_years} tahun)"
        elif is_kota and cv_val > 30.0:
            included = False
            alasan = f"Eksklusi: Unit perkotaan dengan variabilitas ekstrem (CV={cv_val:.1f}% > 30%)"
        elif is_kota and n_zero > 0:
            included = False
            alasan = f"Eksklusi: Unit perkotaan dengan data hilang/nol ({n_zero} tahun)"
        else:
            included = True
            alasan = f"Inklusi: Data runtun waktu konsisten ({n_pos}/{max_years} tahun, CV={cv_val:.1f}%)"
            
        records.append({
            "tanaman": crop_name,
            "nama_kabupaten_kota": kab,
            "tipe_wilayah": "KOTA" if is_kota else "KABUPATEN",
            "total_tahun": n_obs,
            "tahun_positif": n_pos,
            "tahun_nol": n_zero,
            "mean_produktivitas": mean_val,
            "cv_produktivitas_pct": cv_val,
            "status_panel": "MASUK (INCLUDED)" if included else "KELUAR (EXCLUDED)",
            "alasan_kriteria": alasan
        })
    return pd.DataFrame(records)

df_u_padi = evaluate_crop_units(df_padi, "produktivitas_padi2", "Padi", 6)
df_u_jagung = evaluate_crop_units(df_jagung, "produktivitas_jagung", "Jagung", 8)
df_u_kedelai = evaluate_crop_units(df_kedelai, "produktivitas_kedelai", "Kedelai", 8)

df_all_units = pd.concat([df_u_padi, df_u_jagung, df_u_kedelai], ignore_index=True)
out_path = AUDIT_DIR / "panel_units_per_crop.csv"
df_all_units.to_csv(out_path, index=False)

print(f"Berhasil membuat tabel unit panel di {out_path}!")
print("\n=== REKAP UNIT PANEL PER TANAMAN ===")
print(df_all_units.groupby(["tanaman", "status_panel"])["nama_kabupaten_kota"].count())
