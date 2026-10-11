"""
Script: update_audit_matrices_a9.py
Purpose: Update cross_dataset_linking_matrix_revised.csv and dataset_audit_summary.csv according to A9 requirements.
"""

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"

# ==============================================================================
# 1. UPDATE CROSS DATASET LINKING MATRIX
# ==============================================================================
linking_rows = [
    {
        "linking_pair_id": "LINK_01",
        "target_engine": "Rice Decision Engine (Padi Sawah)",
        "weather_source": "DS01 (AgERA5 Time-Series 24 Vars, Grid Cell Unik)",
        "outcome_source": "BPS KSA Resmi (2018–2020) & DS03 Area-Weighted Baseline (2015–2017) [Eksklusi Galura 2018–2020]",
        "weather_period": "2015–2024",
        "outcome_period": "2015–2017 (Baseline) / 2018–2020 (KSA Resmi)",
        "overlap_temporal_years": 6,
        "overlap_period": "2015–2020",
        "weather_spatial_grain": "Grid 0.1° (~10 km) Centroid Resmi (-6.4830, 107.7322 Subang)",
        "outcome_spatial_grain": "Kabupaten / Kota (18 Sentra Padi Utama)",
        "overlap_spatial_status": "EXACT_NAME_AND_BPS_CODE_MATCH",
        "effective_n_matched": 108,
        "grain_gap": "Daily-to-Annual Agronomic Window Aggregation (KATAM MH/MK)",
        "join_feasibility": "HIGH",
        "effective_n_independent": 18,
        "expected_signal_power": "MODERATE_LOW (MDE ~28% log points; Panel FE OLS + Wild Cluster Bootstrap)",
        "feature_engineering_strategy": "KATAM Phenology Splitting (MH: Okt-Jan, MK I: Mar-Mei, MK II: Jul-Okt), Solar Radiation MH, CDD MK I",
        "key_risk_factor": "Data 2018–2020 Galura mengandung artefak GKP (+21.8%); wajib diganti BPS KSA atau dibatasi ke analisis konsistensi."
    },
    {
        "linking_pair_id": "LINK_02",
        "target_engine": "Maize Decision Engine (Jagung)",
        "weather_source": "DS01 (AgERA5 Time-Series 24 Vars, Grid Cell Unik)",
        "outcome_source": "DS05 (Produktivitas Jagung 18 Sentra, Ex-Imputasi 2022)",
        "weather_period": "2015–2024",
        "outcome_period": "2015–2022 (Tahun 2022 Ditandai SUSPECT)",
        "overlap_temporal_years": 8,
        "overlap_period": "2015–2022 (7 Tahun Valid Tanpa 2022)",
        "weather_spatial_grain": "Grid 0.1° (~10 km) Centroid Resmi (-6.4830, 107.7322 Subang)",
        "outcome_spatial_grain": "Kabupaten / Kota (18 Sentra Jagung)",
        "overlap_spatial_status": "EXACT_NAME_AND_BPS_CODE_MATCH",
        "effective_n_matched": 144,
        "grain_gap": "Daily-to-Annual Fixed-Weight Aggregation",
        "join_feasibility": "HIGH",
        "effective_n_independent": 18,
        "expected_signal_power": "MODERATE (Detrended Residual CV 12.21% sample / 5.49% ex-2022; Subang diuji terpisah)",
        "feature_engineering_strategy": "Fixed-weight baseline area (2015–2017) WLS, detrending piecewise/linear, VPD & Tmean Apr-Jun",
        "key_risk_factor": "Tahun 2022 suspect (13 unit nilai seragam 75.70 ku/ha); lonjakan produksi Subang 98.4% berasal dari ekspansi luas panen."
    },
    {
        "linking_pair_id": "LINK_03",
        "target_engine": "Horticulture Decision Engine (Cabai & Tomat)",
        "weather_source": "DS01 (AgERA5 Time-Series 24 Vars)",
        "outcome_source": "DS06 (Produktivitas Cabai SBS Tingkat Provinsi Jawa Barat)",
        "weather_period": "2015–2024",
        "outcome_period": "2017–2024",
        "overlap_temporal_years": 8,
        "overlap_period": "2017–2024",
        "weather_spatial_grain": "Grid 0.1° (~10 km)",
        "outcome_spatial_grain": "Provinsi Jawa Barat (Agregat Tunggal)",
        "overlap_spatial_status": "PROVINCIAL_AGGREGATE_ONLY",
        "effective_n_matched": 8,
        "grain_gap": "Daily Microclimate to Annual Provincial Aggregate",
        "join_feasibility": "LOW_MACRO_ONLY",
        "effective_n_independent": 1,
        "expected_signal_power": "UNDERPOWERED_RULE_BASED_ONLY (N=8 tidak dapat diregresi; CV Cabai 4.49% & 5.71%)",
        "feature_engineering_strategy": "IFWC Rule-Based Advisory berbasis P10 depresiasi embun (Tmin - Td) per sel/bulan; dilarang ML penyakit.",
        "key_risk_factor": "Absennya label OPT dan data kab/kota pasca-2014; timing mismatch Tmin harian vs Td 24-jam."
    },
    {
        "linking_pair_id": "LINK_04",
        "target_engine": "Extreme Climate Early Warning Layer",
        "weather_source": "DS04 (Indonesia Nationwide Agroclimatic Grid, ERA5-Derived)",
        "weather_period": "2016–2025",
        "outcome_source": "DS01 (AgERA5 24 Vars Time-Series)",
        "outcome_period": "2015–2024",
        "overlap_temporal_years": 9,
        "overlap_period": "2016–2024",
        "weather_spatial_grain": "Grid 0.5° Terestrial (12 Titik Poligon Resmi Jabar / 14 Titik BBox)",
        "outcome_spatial_grain": "Grid 0.1° AgERA5 (25 Sel Grid Unik Jabar)",
        "overlap_spatial_status": "SPATIAL_INTERSECTION_GRID_OVERLAY",
        "effective_n_matched": 12,
        "grain_gap": "Daily 0.5° to Daily 0.1° Grid Harmonization",
        "join_feasibility": "VERY_HIGH",
        "effective_n_independent": 12,
        "expected_signal_power": "INTERNAL_CONSISTENCY_CHECK (Sirkular ERA5, validasi harmonisasi definisi indeks CDD/GDD)",
        "feature_engineering_strategy": "Harmonisasi definisi indeks ekstrem CDD, CWD, RX1day, GDD tanpa ambang batas absolut hari.",
        "key_risk_factor": "Sirkularitas fisik (keduanya bersumber dari ECMWF ERA5); bukan validasi independen lapangan."
    },
    {
        "linking_pair_id": "LINK_05",
        "target_engine": "Methodological & Panel Benchmark",
        "weather_source": "DS02 Weather Covariates (BRRI Bangladesh)",
        "outcome_source": "DS02 Audited Rice Yield (BRRI Bangladesh Panel 3 Musim)",
        "weather_period": "Historical BRRI",
        "outcome_period": "Historical BRRI",
        "overlap_temporal_years": 10,
        "overlap_period": "Panel Seimbang Lengkap",
        "weather_spatial_grain": "Distrik / Stasiun Meteorologi Bangladesh",
        "outcome_spatial_grain": "Distrik Bangladesh (Aus, Aman, Boro)",
        "overlap_spatial_status": "EXACT_DISTRICT_SEASON_MATCH",
        "effective_n_matched": 1728,
        "grain_gap": "Seasonal Farm Survey to Regional Agroclimate",
        "join_feasibility": "VERY_HIGH",
        "effective_n_independent": 64,
        "expected_signal_power": "HIGH (Daya statistik tinggi untuk kalibrasi arsitektur ekonometrika panel 3 musim)",
        "feature_engineering_strategy": "Two-Way Fixed Effects, Wild Cluster Bootstrap, Uji Non-linearitas Kuadratik Suhu/Hujan",
        "key_risk_factor": "Transferabilitas lintas negara; struktur irigasi Boro vs sawah tadah hujan Jawa Barat."
    }
]

df_link_out = pd.DataFrame(linking_rows)
out_link_path = AUDIT_DIR / "cross_dataset_linking_matrix_revised.csv"
df_link_out.to_csv(out_link_path, index=False)
print(f"Updated linking matrix saved to: {out_link_path}")

# ==============================================================================
# 2. UPDATE DATASET AUDIT SUMMARY (DS01 to DS09)
# ==============================================================================
summary_rows = [
    {
        "dataset_id": "DS01",
        "title": "AgERA5 Agricultural Weather Reanalysis (West Java 27 Kab/Kota)",
        "primary_rows": 98631,
        "primary_cols": 27,
        "date_min": "2015-01-01",
        "date_max": "2024-12-31",
        "disposition": "PASS",
        "effective_n_matched": 25, # 25 unique grid cells across 27 units
        "limitations": "Model reanalisis ECMWF; bias orografis positif terdeteksi di pegunungan Bandung Raya (+33% s.d. +61%) dan bias negatif di Bogor (-34% s.d. -39%).",
        "audit_disposition_status": "PASS",
        "blocking_issue": "NONE (Validasi bias spasial selesai via CHIRPS v2)"
    },
    {
        "dataset_id": "DS02",
        "title": "Bangladesh Rice Research Institute (BRRI) Panel Benchmark",
        "primary_rows": 1728,
        "primary_cols": 18,
        "date_min": "Panel",
        "date_max": "Panel",
        "disposition": "PASS",
        "effective_n_matched": 1728,
        "limitations": "Benchmark metodologis ekonometrika eksternal; bukan data agronomi lokal Jawa Barat.",
        "audit_disposition_status": "PASS",
        "blocking_issue": "NONE"
    },
    {
        "dataset_id": "DS03",
        "title": "West Java Rice Productivity Panel (Distanhor / Galura)",
        "primary_rows": 162,
        "primary_cols": 8,
        "date_min": "2015",
        "date_max": "2020",
        "disposition": "CONDITIONAL",
        "effective_n_matched": 18,
        "limitations": "Artefak konversi GKP/GKG pada data Galura 2019 (+21.8% lonjakan buatan); BPS KSA per kab/kota tidak tersedia publik. Padi 2018–2020 dikeluarkan dari panel utama.",
        "audit_disposition_status": "CONDITIONAL",
        "blocking_issue": "B1 Rice Reconciliation: Seri 2015–2017 valid (area-weighted match BPS), 2018–2020 dibatasi sebagai analisis sensitivitas."
    },
    {
        "dataset_id": "DS04",
        "title": "Indonesia Nationwide Agroclimatic Grid Indicators (ERA5-Derived)",
        "primary_rows": 2235024,
        "primary_cols": 18,
        "date_min": "2016-01-01",
        "date_max": "2025-12-31",
        "disposition": "PASS",
        "effective_n_matched": 12,
        "limitations": "Sirkularitas fisik dengan AgERA5 (keduanya turunan ERA5); berfungsi sebagai pembanding internal definisi indikator ekstrem (12 titik poligon resmi Jabar).",
        "audit_disposition_status": "PASS",
        "blocking_issue": "NONE (Ambang absolut hari dihapus; diubah ke persentil empiris)"
    },
    {
        "dataset_id": "DS05",
        "title": "West Java Maize Productivity (Distanhor / Galura & Subang)",
        "primary_rows": 216,
        "primary_cols": 8,
        "date_min": "2015",
        "date_max": "2022",
        "disposition": "CONDITIONAL",
        "effective_n_matched": 18,
        "limitations": "Tahun 2022 suspect (13 kabupaten memiliki angka identik 75.70 ku/ha); dieksklusikan dari analisis utama; Subang dianalisis terpisah.",
        "audit_disposition_status": "CONDITIONAL",
        "blocking_issue": "Imputasi Seragam 2022: Panel 2015–2021 valid (N=7 tahun); 2022 hanya disertakan dalam uji sensitivitas."
    },
    {
        "dataset_id": "DS06",
        "title": "West Java SBS Horticulture (Chili & Tomato) Productivity",
        "primary_rows": 230,
        "primary_cols": 7,
        "date_min": "2017",
        "date_max": "2024",
        "disposition": "CONDITIONAL",
        "effective_n_matched": 1,
        "limitations": "Agregat provinsi tunggal (N=8); label penyakit OPT absen 100%; dilarang regresi hasil tahunan & ML klasifikasi penyakit.",
        "audit_disposition_status": "CONDITIONAL",
        "blocking_issue": "TIER B ONLY: Diisolasi ke modul advisory mikroklimat rule-based IFWC berbasis P10 depresiasi titik embun."
    },
    {
        "dataset_id": "DS07",
        "title": "West Java Spatial GeoBoundaries & Administrative Centroids",
        "primary_rows": 27,
        "primary_cols": 12,
        "date_min": "2024",
        "date_max": "2024",
        "disposition": "PASS",
        "effective_n_matched": 27,
        "limitations": "25 sel grid AgERA5 unik; duplikasi sel hanya terjadi pada pasangan Kab/Kota Bogor dan Kab/Kota Cirebon. Seluruh 18 kabupaten sentra Tier A memiliki sel 100% independen.",
        "audit_disposition_status": "PASS",
        "blocking_issue": "NONE"
    },
    {
        "dataset_id": "DS08",
        "title": "West Java Production Volume & Harvest Area (Padi, Jagung, Kedelai)",
        "primary_rows": 648,
        "primary_cols": 9,
        "date_min": "2015",
        "date_max": "2022",
        "disposition": "PASS",
        "effective_n_matched": 27,
        "limitations": "Yield dihitung dari Produksi/Luas Panen (identitas akuntansi). Dekomposisi log membuktikan 98.4% fluktuasi produksi Subang didorong ekspansi luas tanam.",
        "audit_disposition_status": "PASS",
        "blocking_issue": "NONE"
    },
    {
        "dataset_id": "DS09",
        "title": "Macro-Climate Covariates (ONI, DMI) & CHIRPS Satellite Validation",
        "primary_rows": 3653,
        "primary_cols": 8,
        "date_min": "2015-01-01",
        "date_max": "2024-12-31",
        "disposition": "PASS",
        "effective_n_matched": 27,
        "limitations": "CHIRPS benchmark 2016, 2020, 2024 (dan runtun 10-thn). Data konsisten dengan bukti bahwa wilayah pegunungan basah (>3.800 mm), namun AgERA5 overestimasi di Bandung Raya.",
        "audit_disposition_status": "PASS",
        "blocking_issue": "NONE (Klaim 4.466 mm Tasikmalaya dikoreksi sebagai rata-rata 3 tahun; kata 'terbukti' diganti 'konsisten dengan')"
    }
]

df_sum_out = pd.DataFrame(summary_rows)
out_sum_path = AUDIT_DIR / "dataset_audit_summary.csv"
df_sum_out.to_csv(out_sum_path, index=False)
print(f"Updated audit summary saved to: {out_sum_path}")
