# 07 — Cross-Dataset Linking & Spatial-Temporal Overlap Feasibility Audit
**TaniAdapt Project — Synthesis Report & Bridge to Phase 5**
**Fase:** Phase 4 (Dataset Quality Audit Synthesis)

---

## 1. Eksekutif Ringkasan (Executive Summary)

Audit komprehensif ini mengevaluasi kelayakan ilmiah dan teknis dalam menggabungkan (*linking*) dataset cuaca beresolusi tinggi harian (**DS01 AgERA5** & **DS04 Indonesia Agroclimatic**) dengan dataset target luaran hasil panen regional Jawa Barat (**DS03 Padi**, **DS05 Jagung Subang**, dan **DS06 Hortikultura Cabai**).

Tantangan utama dalam pemodelan agro-advisory adalah **Kesenjangan Granularitas (Grain Gap)**:
- Data cuaca tersedia pada resolusi **Harian (*Daily*)** dan spasial **Grid 0,1° (~10 km)**.
- Data luaran hasil panen tersedia pada resolusi **Tahunan (*Annual*)** dan spasial **Kabupaten/Kota**.

Laporan ini membuktikan bahwa penggabungan antar-dataset ini **SANGAT LAYAK (HIGH FEASIBILITY)** dengan menerapkan strategi agregasi berbasis jendela fenologi (*phenological growth stage aggregation*) yang didukung oleh bukti literatur ilmiah.

---

## 2. Matriks Kelayakan Penggabungan Antar-Dataset (Cross-Dataset Linking Matrix)

| Pasangan Linking | Target Engine | Sumber Cuaca | Sumber Hasil Panen | Irisan Temporal | Irisan Spasial | Status Kelayakan |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **LINK_01** | **Rice Engine (Padi)** | DS01 AgERA5 (24 Vars) | DS03 Produktivitas Padi | **2015–2020** (6 Tahun) | 27 Kab/Kota Jawa Barat | 🟢 **HIGH** |
| **LINK_02** | **Maize Engine (Jagung)** | DS01 AgERA5 (24 Vars) | DS05 Produktivitas Jagung | **2015–2022** (8 Tahun) | Kab. Subang & 27 Kab/Kota | 🟢 **HIGH** |
| **LINK_03** | **Chili Engine (Cabai)** | DS01 AgERA5 (24 Vars) | DS06 Produktivitas SBS Cabai | **2017–2024** (8 Tahun) | Jawa Barat (Rawit & Besar) | 🟡 **MODERATE TO HIGH** |
| **LINK_04** | **Extreme Climate Alert** | DS04 Indonesia Agroclimate | DS01 AgERA5 Time-Series | **2016–2024** (9 Tahun) | 14 Titik Jawa Barat | 🟢 **VERY HIGH** |
| **LINK_05** | **Panel Benchmark** | DS02 Climate Covariates | DS02 Audited Yield | **2015–2024** (9 Tahun) | 64 Distrik Bangladesh | 🟢 **VERY HIGH** |

---

## 3. Analisis Irisan Temporal & Spasial Rinci

### A. Komoditas Padi (LINK_01 — Rice Engine)
- **Irisan Waktu:** 6 tahun kalender penuh (2015–2020).
- **Irisan Wilayah:** 27 Kabupaten/Kota di Jawa Barat memiliki data Padi Total, Padi Sawah, dan Padi Ladang tanpa nilai kosong (162 baris utuh).
- **Strategi Agregasi Cuaca (Phase 8):**
  Cuaca harian AgERA5 diakumulasikan ke dalam dua musim tanam utama Jawa Barat:
  1. *Musim Hujan (MH / Rendengan):* Oktober – Maret (~120 hari).
  2. *Musim Kemarau (MK / Gadu):* April – September (~120 hari).
  Fitur turunan yang dibentuk: Akumulasi presipitasi fase vegetatif, rata-rata VPD fase bunting (*booting*), dan suhu minimum malam hari saat pengisian bulir.

### B. Komoditas Jagung (LINK_02 — Maize Engine)
- **Irisan Waktu:** 8 tahun kalender penuh (2015–2022).
- **Irisan Wilayah:** Kabupaten Subang terisolasi penuh selama 8 tahun berturut-turut (produktivitas meningkat dari 45,75 ke 89,49 kuintal/ha).
- **Strategi Agregasi Cuaca (Phase 8):**
  Siklus hidup jagung berdurasi 90–110 hari. Fitur agroklimat yang relevan:
  1. *Growing Degree Days (GDD)* akumulatif dari tanam hingga masa keluar malai (*tasseling*).
  2. *Water Stress Index (WSI)* dan hari kering berturut-turut (*Consecutive Dry Days / CDD*) pada fase silking dan pengisian biji.

### C. Komoditas Hortikultura Cabai (LINK_03 — Chili Engine)
- **Irisan Waktu:** 8 tahun kalender penuh (2017–2024).
- **Irisan Wilayah:** Sentra hortikultura sayuran buah semusim Jawa Barat (Bandung, Garut, Tasikmalaya, Sukabumi).
- **Penyelarasan Target Luaran Kritis (Yield vs Disease):**
  - **Untuk Prediksi Hasil Panen (*Yield*):** Layak dimodelkan dengan cuaca harian yang diagregasikan ke fase panen multi-petik.
  - **Untuk Peringatan Risiko Penyakit (*Disease Risk Warning*):** Karena DS06 tidak memuat label penyakit lapangan, TaniAdapt **tidak akan memaksakan model klasifikasi ML supervised**. Sebagai gantinya, modul risiko penyakit cabai menggunakan **Ambang Batas Cuaca Mekanistik (*Rule-Based Weather Threshold*)** berbasis literatur fitopatologi (Paper 3 & Paper 6):
    $$	ext{Alert Antraknosa (Patek)} = \mathbb{I}\left(	ext{RH}_{mean} > 88\% \land 	ext{Rainfall}_{daily} \in [2, 20]	ext{ mm} \land 	ext{Durasi} \ge 3	ext{ hari}ight)$$

---

## 4. Rekomendasi Transisi Menuju Phase 5 (Crop & Outcome Selection)

Berdasarkan hasil audit kelayakan linking ini, rekomendasi resmi untuk **Phase 5** adalah:
1. **Padi (Rice):** Direkomendasikan penuh (*Primary Food Security Crop*). Target luaran: Produktivitas Padi Sawah vs Ladang.
2. **Jagung (Maize):** Direkomendasikan penuh (*Secondary Cereal Crop*). Target luaran: Produktivitas Jagung Kabupaten Subang & Jawa Barat.
3. **Cabai (Chili - Rawit & Besar):** Direkomendasikan penuh (*High-Value Cash Crop*). Target luaran: Produktivitas Panen SBS (kuintal/ha) + Layer Peringatan Dini Stres Agroklimat / Risiko Hama Penyakit berbasis Rule-Based Threshold.

---
**Status Audit Disposisi Linking:** **APPROVED (PASSED)** — Seluruh pasangan dataset siap diintegrasikan pada tahap Feature Engineering (Phase 8).
