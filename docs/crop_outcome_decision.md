# 🌾 Dokumen Keputusan Seleksi Komoditas & Target Luaran (Phase 5: Crop + Outcome Selection)
**TaniAdapt Project — West Java Precision Advisory Architecture**
**Status Dokumen**: FINAL RESMI (Pasca Audit Blocker Phase 4 & EDA Phase 6)

---

## 1. Kriteria Seleksi Eks-Ante (Ditetapkan Sebelum Penilaian)

Seluruh kandidat komoditas dinilai berdasarkan 7 kriteria kuantitatif objektif berikut tanpa menggunakan kata sifat subjektif:

1. **Jumlah Observasi Valid ($N_{\text{valid}}$)**: Total baris data panel aktual dengan produktivitas $> 0$ ku/ha.
2. **Panjang Deret Waktu ($T$)**: Jumlah tahun kalender observasi yang bebas artefak pelaporan atau imputasi.
3. **Unit Spasial Independen ($S_{\text{eff}}$)**: Jumlah sel grid AgERA5 unik yang memayungi sentra komoditas (maksimal 22 sel unik di Jawa Barat).
4. **Integritas & Kualitas Outcome**: Bebas dari lonjakan artefak pelaporan (seperti artefak GKP 2019 pada padi) atau imputasi seragam rata-rata dinas (seperti titik identik 2022 pada jagung dan kedelai).
5. **Daya Statistik & Minimum Detectable Effect ($\text{MDE}$)**: Batas deteksi minimum perubahan produktivitas (dalam log points per 1 SD cuaca) pada $\alpha = 0,05$ dan $\text{Power} = 0,80$, dihitung dari residu Two-Way Fixed Effects.
6. **Dukungan Literatur Agronomis**: Ketersediaan model respons biofisik atau estimasi empiris sejenis dalam literatur (ditandai `[Published Model]` atau `[Literature Transfer]`).
7. **Relevansi Ekonomi Petani Jawa Barat**: Luas panen riil dan kontribusi terhadap ketahanan pangan / pendapatan petani kecil di Jawa Barat.

---

## 2. Matriks Penilaian Kuantitatif per Kandidat Komoditas

Angka-angka di bawah ini bersumber langsung dari hasil olah kode di `reports/results/*.json`:

| Kriteria Evaluasi | Padi Sawah (DS03) | Jagung (DS05) | Kedelai (DS07) | Cabai Besar & Rawit (DS06) | Tomat (DS06) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$N_{\text{valid}}$ Aktual** | 54 obs ($T=3$) / 162 total | 124 obs (2015–2021) | 108 obs (2015–2021) | 16 obs (8 thn x 2 jenis) | 8 obs (provinsi) |
| **Tahun Efektif ($T$)** | **$T = 3$** (2015–2017) | **$T = 7$** (2015–2021) | **$T = 7$** (2015–2021) | **$T = 8$** (2017–2024) | **$T = 8$** (2017–2024) |
| **Sel Grid Unik ($S_{\text{eff}}$)** | 18 kabupaten sentra | 18 kabupaten sentra | 17 kabupaten sentra | 1 unit agregat provinsi | 1 unit agregat provinsi |
| **Status Artefak / Imputasi** | 2019 Artefak (+21.8%), 2018–2020 BPS UNVERIFIED | 2022 Imputasi identik 75.70 ku/ha (13 kab) | 2022 Imputasi identik 14.30 ku/ha (SD = 0.19) | Tidak ada label kab/kota pasca-2014 | Tidak ada label kab/kota pasca-2014 |
| **Analytical MDE** | $\pm 0,0329$ ($df = 33$ semu) | $\pm 0,2306$ ($df = 99$) | $\pm 0,1842$ ($df = 84$) | *Tidak Dihitung* (N=16) | *Tidak Dihitung* (N=8) |
| **Literatur Pendukung** | IRRI Oryza / Paper 12 & 15 | Paper 13 & 14 (Global) | Paper 13 & 14 (Global) | IFWC / Microclimate Disease | IFWC / Microclimate Disease |
| **Pangsa Luas Panen Jabar** | 1.580.000 ha (Utama) | ~75.000 ha (Sekunder) | ~15.000 ha (Tersier) | ~25.000 ha (Hortikultura) | ~10.000 ha (Hortikultura) |

---

## 3. Keputusan Resmi per Komoditas

### A. Padi Sawah (`padi_sawah`)
- **Keputusan Arsitektur**: **TIER A — MEKANISTIK SAJA (TIDAK MASUK REGRESI PANEL CUACA)**.
- **Rasionalisasi Ketat Deret Waktu ($T=3$)**:
  - Periode 2018–2020 resmi berstatus **UNVERIFIED** di `reports/dataset_audit/bps_manual_input.csv` dan tahun 2019 terbukti memuat artefak pelaporan administratif (+21.8% lonjakan serempak).
  - Dengan hanya $T=3$ tahun valid (2015–2017, $N=54$), derajat bebas residual ($df = 54 - 18 - 3 = 33$) menyerap variasi dalam-kabupaten secara artifisial ($\text{Within-CV} = 2,14\%$). Residual yang kecil dan MDE sempit ($\pm 0,0329$) terjadi murni karena sedikitnya derajat bebas (*degrees-of-freedom depletion*), **BUKAN KARENA DAYA STATISTIK TINGGI**.
  - **Keputusan Eksplisit**: Padi sawah **TIDAK DIMASUKKAN KE REGRESI PANEL EMPIRIS**. Advisory padi dibangun murni di atas **Model Mekanistik Biofisik (Crop Calendar + Derajat Hari Pertumbuhan GDD + Neraca Air Evapotranspirasi ET0)**. Opsi regresi panel ditunda sampai data BPS resmi KSA tingkat kabupaten/kota 2018–2024 terverifikasi di `bps_manual_input.csv`.
- **Target Luaran Model**: Tanggal jendela tanam optimal (dekad kalender), akumulasi GDD, dan defisit air irigasi kumulatif.

### B. Jagung Pipilan Kering (`jagung`)
- **Keputusan Arsitektur**: **TIER A — EMPIRICAL PANEL REGRESSION (SENSITIVITY ONLY) + MEKANISTIK FENOLOGI**.
- **Target Luaran**: `produktivitas_jagung` (Kuintal/Hektar, level tahunan kabupaten).
- **Periode Analisis Utama**: **2015 s.d. 2021** ($T=7$ tahun penuh, $N=124$ observasi aktif).
- **Tahun Dikecualikan**: **Tahun 2022 SECARA RESMI DIEKSKLUSIKAN DARI REGRESI UTAMA** karena terbukti memuat imputasi dinas identik 75.70 ku/ha di 13 kabupaten. Tahun 2022 hanya dipakai dalam uji sensitivitas ekstrem.
- **Unit Analisis**: 18 Kabupaten Sentra Jagung (Kab. Garut sebagai sentra utama pembobot $>60\%$ luas panen).
- **Status Inferensi**: **Evidence Insufficient** (95% CI Wild Cluster Bootstrap Webb $[-0,0521, +0,1300]$ mencakup efek agronomis relevan $\pm 0,065$ dan efek nol).

### C. Kedelai (`kedelai`)
- **Keputusan Arsitektur**: **TIER A — PANEL SECONDARY BENCHMARK + MEKANISTIK**.
- **Target Luaran**: `produktivitas_kedelai` (Kuintal/Hektar, level tahunan kabupaten).
- **Periode Analisis Utama**: **2015 s.d. 2021** ($T=7$ tahun penuh, $N=108$ observasi).
- **Tahun Dikecualikan**: **Tahun 2022 SECARA RESMI DIEKSKLUSIKAN** (standar deviasi spasial runtuh menjadi $0,19\text{ ku/ha}$ akibat imputasi rata-rata provinsi 14.30 ku/ha).
- **Unit Analisis**: 17 Kabupaten Sentra Ex-Ante ($N \ge 6$ tahun valid).

### D. Hortikultura Cabai Rawit & Cabai Besar (`cabai_rawit`, `cabai_besar`)
- **Keputusan Arsitektur**: **TIER B — RULE-BASED MIKROKLIMAT IFWC (INDEX FOR WEATHER-FAVORABLE CONDITIONS)**.
- **Larangan Keras**: **Dilarang melakukan regresi yield tahunan dan dilarang melatih model Machine Learning penyakit tanaman (OPT)**.
- **Alasan**: Data produksi kab/kota (od_18096) hanya tersedia 2013–2014 (**zero temporal overlap** dengan AgERA5 2015–2024), dan dataset tidak memuat label serangan hama/penyakit.
- **Target Luaran**: Skor Indeks Risiko Harian (0–100) berbasis persistensi kebasahan daun malam ($T_{\min} - T_d < 1,0^\circ\text{C}$) dan anomali kelembapan relatif diurnal.

### E. Tomat (`tomat`)
- **Keputusan Arsitektur**: **TIER B — RULE-BASED ADVISORY BERSAMA CABAI**.
- Berbagi modul mikroklimat kelembapan dan depresiasi titik embun malam bersama cabai.

---

## 4. Daftar Keterbatasan yang Diterima & Implikasi untuk Engine

| Modul Decision Engine | Klasifikasi Tier Evidence | Metodologi yang Digunakan | Batasan Operasional yang Diterima |
| :--- | :---: | :--- | :--- |
| **Fenologi & Kalender Tanam Padi** | `[Published Model]` | Akumulasi Derajat Hari (GDD) & Neraca Air FAO-56 | Tanggal panen riil petani tidak tercatat harian; divalidasi silang ke kalender tanam Katam Balitbangtan |
| **Identifikasi Panel Cuaca Jagung** | `[Evidence Insufficient]` | Fixed Effects OLS + Wild Cluster Bootstrap Webb | Data tahunan makro tidak cukup mendeteksi koefisien halus ($\text{MDE} = \pm 0,2306$); advisory cuaca jagung tidak mengklaim dampak kausal mutlak |
| **Peringatan Dini Kebasahan Cabai** | `[Literature Transfer]` | Persistensi Depresiasi Titik Embun Malam ($T_{\min} - T_d$) | Engine tidak memprediksi kemunculan spora jamur fisik, melainkan hanya menghitung durasi kondisi atmosfer kondusif |
| **Baseline Normalitas Cuaca** | `[Data Learned]` | Klimatologi Persentil AgERA5 2015–2024 (P10–P90) | Menggantikan seluruh ambang batas absolut buatan dengan distribusi persentil lokal per sel grid |

---

## 5. Kandidat Komoditas Tambahan

- **Evaluasi Lapangan**: Telah dilakukan audit pencarian dataset komoditas lain (bawang merah, ubi jalar, kacang tanah) di portal Galura Satu Data Jawa Barat dan BPS.
- **Hasil Audit Overlap**: **TIDAK ADA**. Tidak ditemukan dataset produktivitas komoditas tanaman pangan atau hortikultura tingkat kabupaten/kota lain yang memiliki runtun waktu bertumpang tindih dengan periode AgERA5 (2015–2024).
- **Keputusan**: Portofolio komoditas TaniAdapt resmi dikunci pada 5 komoditas di atas (Padi, Jagung, Kedelai, Cabai, Tomat).
