# 07 — Cross-Dataset Linking & Spatial-Temporal Overlap Feasibility Audit (Revised)
**TaniAdapt Project — Synthesis Report & Bridge to Phase 5**
**Fase:** Phase 4 (Dataset Quality Audit Synthesis) — *Revisi Pasca-Audit Empiris*

---

## 1. Eksekutif Ringkasan (Executive Summary)

Audit komprehensif ini mengevaluasi kelayakan ilmiah dan teknis dalam menggabungkan (*linking*) dataset cuaca beresolusi tinggi harian (**DS01 AgERA5** & **DS04 Indonesia Agroclimatic**) dengan dataset target luaran hasil panen regional Jawa Barat (**DS03 Padi**, **DS05 Jagung Subang**, dan **DS06 Hortikultura Cabai**).

Tantangan utama dalam pemodelan agro-advisory adalah **Kesenjangan Granularitas (Grain Gap)**:
- Data cuaca tersedia pada resolusi **Harian (*Daily*)** dan spasial **Grid 0,1° (~10 km)**.
- Data luaran hasil panen tersedia pada resolusi **Tahunan (*Annual*)** dan spasial **Kabupaten/Kota atau Provinsi**.

Berdasarkan audit verifikasi empiris yang ketat:
1. **Padi (DS03):** Seluruh 27 Kabupaten/Kota Jawa Barat kini **100% MATCHED** dengan AgERA5 ($N = 162$ baris observasi, atau $N_{	ext{eff}} = 108$ baris untuk 18 sentra kabupaten pertanian).
2. **Jagung Subang (DS05):** Kabupaten Subang kini **100% MATCHED** dengan AgERA5 (`agera5_kab_subang_2015_2024.csv`, centroid $-6.4830^\circ	ext{S}, 107.7322^\circ	ext{E}$, 18 sel grid). Kenaikan produktivitas Subang pada 2020–2022 (+56,4%) mencerminkan **Patahan Struktural (Structural Break)** akibat BPS KSA/benih hibrida; sinyal cuaca dievaluasi pada residu detrending ($CV_{	ext{resid}} = 11,42\%$).
3. **Target Musiman MH/MK:** Kolom target produktivitas di DS03 dan DS05 bersifat **tahunan murni**. Tidak ada data pemisahan MH/MK di publikasi resmi. Regresi terpisah MH vs MK terhadap angka tahunan resmi dibatalkan; strategi yang valid adalah agregasi kalender tahunan atau indikator kumulatif 2 musim.
4. **Hortikultura Cabai (DS06):** Granularitas geografis adalah **Tingkat Provinsi Jawa Barat ($N=8$ baris)** tanpa rincian kabupaten, dan **TIDAK MEMILIKI LABEL PENYAKIT/OPT**. Ambang batas buatan ("RH > 88%") resmi dinyatakan **EVIDENCE INSUFFICIENT**. Modul penyakit cabai dialihkan menjadi **Index of Favorable Weather Condition (IFWC)** berbasis proksi fisika kebasahan daun ($T_{\min} - T_d$ dan RH maksimum).
5. **Validasi Cuaca:** Korelasi harian AgERA5 vs Open-Meteo di Bandung ($r_{	ext{precip}}=0,851$, $r_{	ext{temp}}=0,764$) membuktikan **konsistensi sesama turunan ECMWF ERA5**, bukan pembuktian stasiun darat BMKG (ground truth).

---

## 2. Matriks Kelayakan Penggabungan Antar-Dataset (Cross-Dataset Linking Matrix Revised)

| Pasangan Linking | Target Engine | Sumber Cuaca | Sumber Hasil Panen | Irisan Temporal | Sampel Efektif ($N_{	ext{eff}}$) | Status Spasial & Kelayakan |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **LINK_01** | **Rice Engine (Padi)** | DS01 AgERA5 (24 Vars) | DS03 Produktivitas Padi | **2015–2020** (6 Thn) | **162 baris** (27 Kab/Kota) <br> *(108 baris di 18 sentra)* | 🟢 **HIGH** (100% matched cuaca 27 Kab/Kota; WLS Fixed Baseline Area) |
| **LINK_02** | **Maize Engine (Jagung)** | DS01 AgERA5 (24 Vars) | DS05 Produktivitas Jagung | **2015–2022** (8 Thn) | **216 baris** (27 Kab/Kota) <br> *(Subang direct match)* | 🟢 **HIGH-MODERATE** (Subang Matched; detrending linier diterapkan) |
| **LINK_03** | **Chili Engine (Cabai)** | DS01 AgERA5 (24 Vars) | DS06 Produktivitas SBS Cabai | **2017–2024** (8 Thn) | **8 baris** (Provinsi Jabar) | 🟡 **MODERATE** (Yield makro N=8; Modul Penyakit wajib Rule-Based IFWC) |
| **LINK_04** | **Extreme Climate Alert** | DS04 Indonesia Agroclimate | DS01 AgERA5 Time-Series | **2016–2024** (9 Thn) | **3.653 hari** (10 Thn) | 🟢 **VERY HIGH** (Konsistensi ERA5 r=0.85; Tasikmalaya ekstrem >4.000 mm) |
| **LINK_05** | **Panel Benchmark** | DS02 Climate Covariates | DS02 Audited Yield | **2015–2024** (9 Thn) | **1.728 baris** (Balanced) | 🟢 **VERY HIGH** (Benchmark metodologi regresi panel BRRI) |

---

## 3. Analisis Irisan & Strategi Pemodelan Berbasis Bukti (Phase 8 & Phase 10)

### A. Komoditas Padi (LINK_01 — Rice Engine)
- **Sampel Saat Ini:** Seluruh 27 Kabupaten/Kota AgERA5 $	imes$ 6 tahun = $N_{	ext{eff}} = 162$ baris (108 baris di 18 sentra pertanian utama).
- **Status Integrasi:** 100% matched secara spasial dan temporal (2015–2020).
- **Resolusi Grain Gap:** Karena data target adalah produktivitas tahunan (bukan per musim MH/MK), fitur cuaca diagregasikan secara tahunan atau menggunakan indikator kumulatif dua musim secara simultan dalam model yang sama.

### B. Komoditas Jagung (LINK_02 — Maize Engine)
- **Status Subang:** 100% Matched langsung dengan `agera5_kab_subang_2015_2024.csv` ($-6.4830^\circ	ext{S}, 107.7322^\circ	ext{E}$, 18 sel grid AgERA5, 3.653 hari kalender).
- **Structural Break Handling:** Produktivitas jagung Subang memiliki tren linier tajam $+4,93	ext{ ku/ha/tahun}$ ($R^2=1,000$). Lonjakan dari 57,23 ke 89,49 ku/ha pada 2020–2022 harus didetrending terlebih dahulu. Variasi cuaca diekstraksi dari residu ($CV_{	ext{resid}} = 11,42\%$).

### C. Komoditas Hortikultura Cabai (LINK_03 — Chili Engine)
- **Granularitas:** Murni tingkat provinsi Jawa Barat ($N=8$ baris untuk Cabai Besar, $N=8$ baris untuk Cabai Rawit).
- **Disposisi Modul Penyakit:** DS06 **tidak memiliki data kejadian penyakit**. TaniAdapt **tidak boleh melatih supervised ML klasifikasi penyakit**.
- **Ambang Batas Ilmiah:** Ambang batas sembarangan ("RH > 88%") resmi **DITOLAK**. Modul penyakit diimplementasikan sebagai **Index of Favorable Weather Condition (IFWC)** berbasis proksi mikroklimat kebasahan daun: depresi titik embun ($T - T_d$) dan kelembaban relatif maksimum harian (`Derived_Relative_Humidity_2m_Max_24h`).

---

## 4. Rekomendasi Resmi untuk Phase 5 (Crop & Outcome Selection)

1. **Padi (Rice):** Komoditas Utama Ketahanan Pangan. Target: Produktivitas Padi Sawah vs Ladang ($N_{\text{eff}}=42$, siap diperluas ke 162).
2. **Jagung (Maize):** Komoditas Serealia Sekunder. Target: Produktivitas Jagung Subang ($N=8$ detrended) & Panel Jawa Barat ($N=56$, siap diperluas ke 216).
3. **Cabai (Chili - Rawit & Besar):** Komoditas Hortikultura Nilai Tinggi. Target: Produktivitas Tahunan Makro Provinsi ($N=8$) + Layer IFWC Mikroklimat Berbasis Fisika Atmosfer.
4. **Bawang Merah (Shallot):** Komoditas Keempat Potensial pengganti Kedelai (Kedelai ditolak karena data nihil/missing parah di Jabar). Sentra Cirebon & Majalengka berpasangan langsung dengan titik AgERA5 Cirebon.

---
**Status Audit Disposisi Linking:** **APPROVED WITH SCIENTIFIC CONDITIONS** — Seluruh batasan data dan strategi mitigasi telah terdokumentasi secara transparan.
