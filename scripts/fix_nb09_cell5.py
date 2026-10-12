import nbformat as nbf
from pathlib import Path

p = Path("notebook/09_climate_covariates_and_chirps.ipynb")
nb = nbf.read(p, as_version=4)
for i, c in enumerate(nb.cells):
    if 'cols_display' in c.source:
        c.source = """# Memuat hasil audit komprehensif 27 unit dari b3_rainfall_bias_chirps_audit_v2.csv
audit_file = PROJECT_ROOT / "reports" / "dataset_audit" / "b3_rainfall_bias_chirps_audit_v2.csv"
df_b3_audit = pd.read_csv(audit_file)

cols_display = [c for c in [
    "nama_kabupaten_kota", "n_months_valid", "years_available", 
    "mean_annual_chirps_mm", "mean_annual_agera5_mm", 
    "signed_bias_overall_pct", "bias_mh_wet_pct", "bias_mk_dry_pct", 
    "pearson_anom_r"
] if c in df_b3_audit.columns]

print("="*95)
print("[TABEL AUDIT REKONSILIASI A2] EVALUASI BIAS AGERA5 VS SATELIT CHIRPS v2 (27 UNIT JAWA BARAT):")
print("="*95)
display(df_b3_audit[cols_display].head(10))
"""
nbf.write(nb, p)
print("Updated cell 5 in nb09 successfully!")
