# TaniAdapt Research Dossier — Phase 7: Statistical Analysis & Econometric Panel Inference

**Status**: PENDING_USER_RATIFICATION  
**Ruang Lingkup**: Pengujian Rigor Hipotesis Fenologi pada Panel Jagung dan Kedelai Jawa Barat  
**Metodologi**: Two-Way Fixed Effects, Wild Cluster Bootstrap Webb (B=999), Multiple Testing Corrections (Holm & FDR), Minimum Detectable Effect (MDE)

---

## 1. Hasil Pengujian Empiris Hipotesis Panel Utama (Jagung & Kedelai)

Panel utama diestimasi menggunakan spesifikasi Two-Way Fixed Effects (Kabupaten FE + Year FE) dengan koreksi klaster kecil Wild Cluster Bootstrap Webb ($B=999$ pengulangan):

| ID Hipotesis | Komoditas | Prediktor Fenologi | Tanda | Estimasi $\hat{\beta}$ | 95% Webb Bootstrap CI | MDE (Power 80%) | Nilai $p$ Mentah | Nilai $p$ (Holm) | Nilai $q$ (FDR) | Kesimpulan Inferensi |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **H_CORN_01** | Jagung | Presipitasi Vegetatif (Feb–Apr) | (+) | $+0.0368$ | $[-0.0521, +0.1300]$ | $\pm 0.1444$ | $0.4745$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_CORN_02** | Jagung | Suhu Rata-rata Tumbuh (Mar–Mei) | (-) | $+0.5647$ | $[-1.0976, +2.1968]$ | $\pm 2.4995$ | $0.6120$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_CORN_03** | Jagung | VPD Maksimum Reproduktif (Apr–Jun) | (-) | $+0.0909$ | $[-0.0707, +0.2474]$ | $\pm 0.2562$ | $0.4800$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_CORN_04** | Jagung | Hari Kering Berurutan CDD (Mei–Jul) | (-) | $+0.0957$ | $[-0.0034, +0.1939]$ | $\pm 0.1821$ | $0.3010$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_SOY_01** | Kedelai | Presipitasi Polong (Jun–Agu) | (+) | $-0.0094$ | $[-0.0822, +0.0553]$ | $\pm 0.1090$ | $0.7800$ | $1.0000$ | $0.8580$ | `evidence_insufficient` |
| **H_SOY_02** | Kedelai | Suhu Malam Tinggi (Jul–Sep) | (-) | $+0.7188$ | $[-0.2631, +1.6834]$ | $\pm 1.4808$ | $0.3340$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_SOY_03** | Kedelai | Hujan Lebat Pemasakan (Agu–Okt) | (-) | $+0.0400$ | $[-0.0140, +0.0904]$ | $\pm 0.0755$ | $0.2980$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |

*Catatan Sampel Panel Utama*:
- **Jagung (DS05)**: 18 kabupaten sentra, periode 2015–2021 (eksklusi 2022 SUSPECT), $N = 124$ observasi valid, 18 sel AgERA5 unik.
- **Kedelai (DS07)**: 17 kabupaten sentra aktif ex-ante ($N \ge 6$ tahun non-zero, mengecualikan Kabupaten Bekasi), $N = 112$ observasi (setelah penyaringan robust MAD-z outlier) / $N = 115$ (raw non-zero), tepat 17 sel AgERA5 unik dari `a8_spatial_grid_cells_audit.csv`.

---

## 2. Penjelasan Khusus Prosedur Holm & H_CORN_04

Pada hipotesis `H_CORN_04` (CDD Jagung Mei–Juli):
- Estimasi titik adalah $\hat{\beta} = +0.0957$ dengan galat standar bootstrap $\text{SE} = 0.0504$ dan interval kepercayaan 95% Webb Bootstrap $[-0.0034, +0.1939]$.
- Karena batas bawah interval kepercayaan bernilai negatif ($-0.0034 \le 0$), hipotesis nol $\beta = 0$ secara formal tidak dapat ditolak pada tingkat signifikansi 5%.
- **Prosedur Holm-Bonferroni**:
  * Nilai $p$ mentah adalah $p_{\text{raw}} = 0.3010$.
  * Dalam keluarga 11 hipotesis ($m = 11$), nilai $p$ diurutkan secara menaik. `H_CORN_04` menempati urutan ke-3, sehingga pengali Holm adalah $m - \text{rank} + 1 = 11 - 3 + 1 = 9$.
  * Perkalian langsung: $0.3010 \times 9 = 2.709$.
  * Karena nilai hasil kali melampaui 1.0, nilai $p$ terkoreksi Holm dijepit (*clamped*) tepat pada **$p_{\text{holm}} = 1.0000$**.
- Terlebih lagi, nilai estimasi $|\hat{\beta}| = 0.0957$ berada jauh di bawah batas deteksi minimum $\text{MDE} = \pm 0.1821$, sehingga status inferensi yang jujur adalah **`evidence_insufficient`**.

---

## 3. Lampiran Metodologis: Status INVALID Panel Padi (H_RICE_01 s/d H_RICE_04)

Hipotesis padi sawah `H_RICE_01` s/d `H_RICE_04` **DIKELUARKAN DARI TABEL BUKTI UTAMA** dan diberi penanda **`INVALID`** berdasarkan audit dataset:

| ID Hipotesis | Komoditas | Periode Sampel | Ukuran Sampel ($N$) | Derajat Bebas ($df$) | Status Metodologis | Alasan Penandaan INVALID |
|---|---|:---:|:---:|:---:|:---:|---|
| **H_RICE_01** | Padi | 2015–2017 | $N = 54$ | $df = 33$ | **`INVALID`** | Melanggar batasan registri DS03; $df=33$ sangat underpowered; BPS baseline berstatus `PENDING_MANUAL_VERIFICATION`. |
| **H_RICE_02** | Padi | 2015–2017 | $N = 54$ | $df = 33$ | **`INVALID`** | $T=3$ terlalu pendek; variasi within-kabupaten hanya 2.14%; dilarang inferensi regresi kausal. |
| **H_RICE_03** | Padi | 2015–2017 | $N = 54$ | $df = 33$ | **`INVALID`** | Tidak memenuhi syarat daya statistik; dialihkan penuh ke penasihat mekanistik FAO-56. |
| **H_RICE_04** | Padi | 2015–2017 | $N = 54$ | $df = 33$ | **`INVALID`** | Padi dialihkan ke status `mechanistic advisory` murni sesuai ratifikasi `docs/crop_outcome_decision.md`. |

*Catatan Keras*: Sesuai keputusan resmi Phase 5 dan registri bukti DS03 (`reports/dataset_audit/final_dataset_registry.csv`), data padi BPS pre-KSA (2015–2017) hanya diizinkan untuk penyusunan baseline rasio dan penasihat mekanistik, dan secara tegas dilarang digunakan untuk regresi panel cuaca kausal. Data KSA 2018–2024 tidak tersedia di tingkat kabupaten.

---

## 4. Analisis Sensitivitas Jendela Waktu & Uji Falsifikasi (Lead Placebo)

Pada panel jagung 18 sentra ($N=124$):
1. **Sensitivitas Jendela Kalender**:
   * *Jan–Mar (-1 bulan)*: $\hat{\beta} = -0.0076$, $95\%\text{ CI} = [-0.0760, +0.0682]$, $\text{MDE} = \pm 0.1064$.
   * *Feb–Apr (Jendela Utama)*: $\hat{\beta} = +0.0368$, $95\%\text{ CI} = [-0.0521, +0.1300]$, $\text{MDE} = \pm 0.1444$.
   * *Mar–Mei (+1 bulan)*: $\hat{\beta} = +0.0581$, $95\%\text{ CI} = [-0.0221, +0.1431]$, $\text{MDE} = \pm 0.1330$.
2. **Uji Falsifikasi Placebo Cuaca Masa Depan ($t+1$)**:
   * $\hat{\beta} = +0.1341$, $95\%\text{ CI} = [-0.1017, +0.3628]$, $\text{MDE} = \pm 0.4199$, $p > 0.40$.
   * Lolos uji falsifikasi: tidak terdeteksi korelasi palsu yang signifikan antara cuaca masa depan dan hasil panen saat ini.

---

## 5. Kesimpulan Saintifik Kritis
Hasil ekonometrika menunjukkan secara transparan bahwa data panel tahunan agregat BPS/Dinas tidak memiliki daya statistik untuk membedakan sinyal cuaca dari kebisingan pelaporan. Oleh karena itu, TaniAdapt secara bertanggung jawab menetapkan status **`evidence_insufficient`** untuk pemodelan yield statistik dan mengalihkan otak keputusan ke hukum biofisik mekanistik FAO-56 Penman-Monteith.
