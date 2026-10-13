# TaniAdapt — Direktori Laporan Riset Komprehensif (Phase 0 s/d Phase 12)

Direktori ini memuat seluruh dokumen laporan riset mendalam, berintegritas ilmiah tinggi, dan terbebas dari halusinasi untuk pengembangan platform **TaniAdapt (Precision Agro-Advisory & Agricultural Decision Support System Jawa Barat)**.

---

## Matriks Navigasi Laporan Riset per Fase

| Berkas Laporan | Nama Fase Riset | Status Resmi | Topik Utama & Hasil Penelitian Kunci |
|---|---|:---:|---|
| [`phase_00_problem_definition.md`](./phase_00_problem_definition.md) | **Phase 0: Problem Definition & Scope** | `PENDING_USER_RATIFICATION` | Krisis iklim Jabar, keruntuhan kalender statis, bahaya halusinasi LLM, dan arsitektur *decoupled*. |
| [`phase_01_research_questions_and_hypotheses.md`](./phase_01_research_questions_and_hypotheses.md) | **Phase 1: Research Questions & Hypotheses** | `PENDING_USER_RATIFICATION` | 3 RQ utama & hipotesis didokumentasikan (post-data-access documentation, commit 4629ad9 pada 2026-10-11 vs akses data awal 2026-10-05/06, bukan pra-registrasi sebelum akses data). |
| [`phase_02_deep_literature_review.md`](./phase_02_deep_literature_review.md) | **Phase 2: Deep Literature Review** | `PENDING_USER_RATIFICATION` | Ekstraksi 16 paper otoritatif (FAO-56, Lobell, Schlenker, Webb), benchmark 15 kompetitor DSS, & registri bukti. |
| [`phase_03_dataset_discovery_and_acquisition.md`](./phase_03_dataset_discovery_and_acquisition.md) | **Phase 3: Dataset Discovery & Fusion** | `PENDING_USER_RATIFICATION` | Fusi multi-sumber dari 9 dataset utama (AgERA5 1991–2024, CHIRPS, BPS Padi, Open Data Jabar, DEM SRTM). |
| [`phase_04_dataset_quality_audit.md`](./phase_04_dataset_quality_audit.md) | **Phase 4: Dataset Quality Audit** | `PENDING_USER_RATIFICATION` | Penutupan 11 blocker audit (A1–A11), buang data palsu jagung 2022 (75.70 ku/ha), koreksi CHIRPS N=936. |
| [`phase_05_crop_and_outcome_selection.md`](./phase_05_crop_and_outcome_selection.md) | **Phase 5: Crop & Outcome Selection** | `PENDING_USER_RATIFICATION` | Ratifikasi portofolio 5 komoditas (Padi, Jagung, Kedelai, Cabai, Tomat) & eksklusi Bawang Merah. |
| [`phase_06_exploratory_data_analysis.md`](./phase_06_exploratory_data_analysis.md) | **Phase 6: Exploratory Data Analysis (EDA)** | `COMPLETED` | Arsitektur 10 Notebook (01–09 mandiri, Notebook 10 sintesis) & katalog 68 figur kanonik (150 DPI). |
| [`phase_07_statistical_analysis.md`](./phase_07_statistical_analysis.md) | **Phase 7: Statistical Analysis** | `COMPLETED` | Uji 11 hipotesis via Two-Way FE & Wild Cluster Bootstrap Webb, 100% berstatus jujur `evidence_insufficient`. |
| [`phase_08_feature_engineering.md`](./phase_08_feature_engineering.md) | **Phase 8: Feature Engineering** | `COMPLETED` | Feature store 65k baris cuaca, ekstraksi lag/rolling/CDD/ET0, & temuan multikolinearitas ekstrem VIF > 4.000. |
| [`phase_09_ml_baseline_benchmarking.md`](./phase_09_ml_baseline_benchmarking.md) | **Phase 9: ML Baseline Benchmarking** | `COMPLETED` | Benchmark 6 model via LOYO CV. LOYO CV R2≈0: tidak ada bukti prediktif dalam data ini; catat bahwa year FE tidak bisa diestimasi untuk tahun yang ditahan sehingga R2 negatif sebagian akibat desain evaluasi. |
| [`phase_10_evidence_to_risk_model.md`](./phase_10_evidence_to_risk_model.md) | **Phase 10: Evidence → Risk Model** | `COMPLETED` | Model risiko terkonvensi (belum dikalibrasi terhadap data lapangan): kriteria deplesi FAO-56 (Dr > RAW), genangan air, & spora OPT fajar (P10 konvensi). |
| [`phase_11_risk_to_decision_engine.md`](./phase_11_risk_to_decision_engine.md) | **Phase 11: Risk → Decision Engine** | `COMPLETED` | Perakitan logika keputusan 5 tindakan agronomi, jadwal jam 06.00–18.00 WIB, & kepatuhan skema JSON. |
| [`phase_12_validation.md`](./phase_12_validation.md) | **Phase 12: Preliminary Face-Validity Check (n=3 peristiwa)** | `COMPLETED` | Preliminary face-validity check 3 bencana iklim BMKG (n=3 peristiwa regional) & uji ketahanan 5 edge-case (100% graceful degradation). |
