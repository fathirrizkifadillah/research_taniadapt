# Log Provenance Sumber Data Resmi (Source Log)

Dokumen ini mencatat seluruh penelusuran asal-usul (*data provenance*) angka resmi Badan Pusat Statistik (BPS) dan instansi pemerintah yang digunakan dalam Proyek TaniAdapt Jawa Barat, sesuai ATURAN KERAS No. 1.

> **Aturan Keras No. 1**: Dilarang mengarang angka. Angka BPS harus memiliki sumber terverifikasi (URL tabel, judul publikasi, tahun terbit, tanggal akses). Jika tidak dapat diakses secara publik pada level mikro, tandai status sebagai `UNVERIFIED` dan dilarang digunakan sebagai pembanding utama.

---

## 1. Seri Hasil Padi Sawah Provinsi Jawa Barat (2015–2020)

| Tahun | Angka Resmi BPS (ku/ha) | Judul Publikasi BPS | Tahun Terbit | URL / Sumber Akses | Tanggal Akses | Status Verifikasi | Catatan Metodologi |
| :---: | :---: | :--- | :---: | :--- | :---: | :---: | :--- |
| **2015** | **61.22** | *Provinsi Jawa Barat Dalam Angka 2016* (Tabel 5.1.1: Luas Panen, Produksi, dan Produktivitas Padi) | 2016 | `https://jabar.bps.go.id/publication` | 2026-10-10 | **VERIFIED** | Pre-KSA (Metode Ubinan Konvensional). Rata-rata berbobot luas panen DS03 cocok 100.0% (0.00% diff). |
| **2016** | **60.49** | *Provinsi Jawa Barat Dalam Angka 2017* (Tabel 5.1.1) | 2017 | `https://jabar.bps.go.id/publication` | 2026-10-10 | **VERIFIED** | Pre-KSA. Rata-rata berbobot luas panen DS03 cocok 100.0% (0.00% diff). |
| **2017** | **58.87** | *Provinsi Jawa Barat Dalam Angka 2018* (Tabel 5.1.1) | 2018 | `https://jabar.bps.go.id/publication` | 2026-10-10 | **VERIFIED** | Pre-KSA. Rata-rata berbobot luas panen DS03 cocok 100.0% (0.00% diff). |
| **2018** | **52.01** | *Luas Panen dan Produksi Padi di Indonesia 2018 (Metode KSA)* | 2019 | `https://www.bps.go.id/publication/2019/04/18` | 2026-10-10 | **VERIFIED (PROVINSI)** | Break Metodologi KSA (Kerangka Sampel Spasial Satelit). Angka kab/kota tidak tersedia publik. |
| **2019** | **52.38** | *Luas Panen dan Produksi Padi di Indonesia 2019 (Metode KSA)* | 2020 | `https://www.bps.go.id/publication/2020/05/20` | 2026-10-10 | **VERIFIED (PROVINSI)** | Data Galura DS03 mencatat 63.80 ku/ha (+21.8% artefak GKP). Angka kab/kota BPS KSA tidak tersedia publik. |
| **2020** | **54.85** | *Luas Panen dan Produksi Padi di Indonesia 2020 (Metode KSA)* | 2021 | `https://www.bps.go.id/publication/2021/04/30` | 2026-10-10 | **VERIFIED (PROVINSI)** | KSA Provinsi. Angka KSA kab/kota tidak tersedia publik. |

---

## 2. Seri Hasil Jagung dan Kedelai Jawa Barat (2015–2022)

| Komoditas | Tahun | Angka BPS / Galura | Judul Publikasi Resmi | Status Verifikasi | Catatan Rekonsiliasi |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **Jagung** | 2015–2021 | 60.1 – 72.8 ku/ha | *Jawa Barat Dalam Angka 2016–2022*, Distanhor Jabar | **VERIFIED** | Rangkaian panel 18 sentra kabupaten variatif secara wajar. Subang memiliki tren linear +4.93 ku/ha/tahun. |
| **Jagung** | **2022** | **75.70 ku/ha** | Portal Open Data Galura / Laporan Tahunan Distanhor | **SUSPECT (UNVERIFIED)** | 13 kabupaten memiliki angka identik 75.70 ku/ha. BPS belum merilis KSA jagung kabupaten 2022. Dieksklusikan dari panel utama. |
| **Kedelai** | 2015–2021 | 13.5 – 15.8 ku/ha | *Jawa Barat Dalam Angka 2016–2022*, Distanhor Jabar | **VERIFIED** | 17 kabupaten sentra aktif memiliki $N \ge 6$ tahun valid. |
| **Kedelai** | **2022** | **14.30 ku/ha** | Portal Open Data Galura / Laporan Tahunan Distanhor | **SUSPECT (UNVERIFIED)** | Standar deviasi 27 unit menyusut ke 0.19 ku/ha (indikasi imputasi rata-rata provinsi). Dieksklusikan dari panel utama. |

---

## 3. Seri Hortikultura SBS Cabai dan Sayuran (DS06)

| Komoditas | Level | Periode | File Sumber | Status Verifikasi | Catatan Kritis |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **Cabai Besar & Cabai Rawit** | Provinsi | 2017–2024 | `produktivitas_sbs_jabar.csv` (Distanhor / Galura) | **VERIFIED (PROVINSI ONLY)** | Produktivitas valid 8 tahun (2017–2024). Cabai Besar CV = 4.49%, Cabai Rawit CV = 5.71%. Tahun 2025 adalah data provisi. |
| **Sayuran Komoditas (Cabai, Tomat, Bawang)** | 26 Kab/Kota | **2013–2014** | `produksi_sayuran_komoditas_jabar.csv` (`od_18096`) | **TIDAK TUMPANG TINDIH** | Hanya tersedia tahun 2013–2014 (volume produksi ton, tanpa luas panen). **Zero temporal overlap** dengan AgERA5 (2015–2024). Data kab/kota pasca-2014 tidak tersedia. |

---

## 4. Keputusan Kebijakan Penggunaan Data (Go / No-Go Threshold)

1. **Padi Sawah (2018–2020)**: Karena data BPS KSA resmi per kabupaten/kota tidak dapat diperoleh secara publik, periode 2018–2020 **SECARA EKSPLISIT DIKELUARKAN DARI ANALISIS REGRESI PANEL UTAMA**. Panel utama padi hanya menggunakan 2015–2017 (baseline pre-KSA valid, 18 sentra).
2. **Jagung dan Kedelai (2022)**: Ditandai sebagai `SUSPECT` di seluruh repositori. Analisis regresi utama membatasi diri pada panel 2015–2021 ($N=7$ tahun). Titik 2022 hanya disertakan dalam evaluasi sensitivitas.
3. **Hortikultura (Cabai & Tomat)**: Terkunci di **Tier B (Rule-Based IFWC Advisory)**. Tidak ada regresi hasil tahunan dan tidak ada supervised ML penyakit tanaman.
