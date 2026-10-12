# Log Provenance Sumber Data Resmi (Source Log)

Dokumen ini mencatat seluruh penelusuran asal-usul (*data provenance*) angka resmi Badan Pusat Statistik (BPS) dan instansi pemerintah yang digunakan dalam Proyek TaniAdapt Jawa Barat, sesuai ATURAN KERAS No. 1 & No. 2.

> **Aturan Keras No. 2**: Angka BPS tidak boleh dikarang. Selama belum ada input manual terverifikasi, semua angka BPS berstatus **UNVERIFIED** dan **TIDAK dipakai sebagai pembanding utama**. Seluruh input manual terpusat di `reports/dataset_audit/bps_manual_input.csv`.

---

## 1. Seri Hasil Padi Sawah Provinsi Jawa Barat (2015–2020)

| Tahun | Angka BPS (ku/ha) | Judul Publikasi BPS | Status Verifikasi | Catatan Rekonsiliasi & Resolusi Konflik |
| :---: | :---: | :--- | :---: | :--- |
| **2015** | 61.22 | *Provinsi Jawa Barat Dalam Angka 2016* (Tabel 5.1.1) | **UNVERIFIED (PROVISIONAL)** | Pre-KSA. Rata-rata berbobot luas panen DS03 cocok 100.0% (diff 0.01%). Tercatat di `bps_manual_input.csv`. |
| **2016** | 60.49 | *Provinsi Jawa Barat Dalam Angka 2017* (Tabel 5.1.1) | **UNVERIFIED (PROVISIONAL)** | Pre-KSA. Rata-rata berbobot luas panen DS03 cocok 100.0% (diff 0.00%). Tercatat di `bps_manual_input.csv`. |
| **2017** | 58.87 | *Provinsi Jawa Barat Dalam Angka 2018* (Tabel 5.1.1) | **UNVERIFIED (PROVISIONAL)** | Pre-KSA. Rata-rata berbobot luas panen DS03 cocok 100.0% (diff 0.00%). Tercatat di `bps_manual_input.csv`. |
| **2018** | *Pending* | Menunggu input manual user di `bps_manual_input.csv` | **UNVERIFIED (KOSONG)** | **Inkonsistensi Terdeteksi**: Terdapat konflik sumber antara Berita Resmi Statistik BRS 68/11/32 (56.51 ku/ha) vs Publikasi Nasional KSA (52.01 ku/ha). Ditandai UNVERIFIED dan tidak digunakan sebagai pembanding sampai user memverifikasi. |
| **2019** | *Pending* | Menunggu input manual user di `bps_manual_input.csv` | **UNVERIFIED (KOSONG)** | **Inkonsistensi Terdeteksi**: Konflik angka antara Jabar Dalam Angka 2020 (57.54 ku/ha) vs Publikasi Nasional (52.38 ku/ha). Data Galura DS03 mencatat unweighted 68.55 ku/ha dan weighted 70.09 ku/ha (lonjakan artefak ~+21.8%). |
| **2020** | *Pending* | Menunggu input manual user di `bps_manual_input.csv` | **UNVERIFIED (KOSONG)** | **Inkonsistensi Terdeteksi**: Konflik angka antara BRS 67/10/32 (56.82 ku/ha) vs Publikasi Nasional (54.85 ku/ha). Ditandai UNVERIFIED. |

---

## 2. Seri Hasil Jagung dan Kedelai Jawa Barat (2015–2022)

| Komoditas | Tahun | Angka Lapangan / Galura | Status Verifikasi | Catatan Kritis |
| :--- | :---: | :---: | :---: | :--- |
| **Jagung** | 2015–2021 | 60.1 – 72.8 ku/ha | **PASS (AUDIT DINAS)** | Panel 18 sentra kabupaten variatif secara natural. Subang memiliki tren linear +4.93 ku/ha/tahun. |
| **Jagung** | **2022** | **75.70 ku/ha** | **SUSPECT (ARTEFAK)** | 13 kabupaten memiliki angka identik 75.70 ku/ha. Dieksklusikan dari panel utama regresi; diberi penanda abu-abu/hatch. |
| **Kedelai** | 2015–2021 | 13.5 – 15.8 ku/ha | **PASS (AUDIT DINAS)** | 17 kabupaten sentra aktif memiliki $N \ge 6$ tahun valid. |
| **Kedelai** | **2022** | **14.30 ku/ha** | **SUSPECT (ARTEFAK)** | Standar deviasi 27 unit menyusut ekstrem ke 0.19 ku/ha (indikasi imputasi seragam). Dieksklusikan dari panel utama regresi. |

---

## 3. Seri Hortikultura SBS Cabai dan Sayuran (DS06)

| Komoditas | Level | Periode | File Sumber | Status Verifikasi | Catatan Kritis |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **Cabai Besar & Cabai Rawit** | Provinsi | 2017–2024 | `produktivitas_sbs_jabar.csv` (Galura) | **PASS (PROVINSI ONLY)** | Produktivitas valid 8 tahun (2017–2024). Cabai Besar CV = 4.49%, Cabai Rawit CV = 5.71%. Tahun 2025 adalah data sementara. |
| **Sayuran Komoditas (Cabai, Tomat)** | 26 Kab/Kota | **2013–2014** | `od_18096` | **BLOCKED (ZERO OVERLAP)** | Hanya tersedia tahun 2013–2014 (volume produksi ton, tanpa luas panen). **Zero temporal overlap** dengan AgERA5 (2015–2024). |

---

## 4. Resolusi Kebijakan Penggunaan Data (Go / No-Go Threshold)

1. **Padi Sawah (2018–2020)**: Seluruh angka BPS berstatus UNVERIFIED. Periode 2018–2020 **SECARA EKSPLISIT DIKELUARKAN DARI PANEL REGRESI UTAMA**. Panel regresi padi dibatasi pada $T=3$ (2015–2017) atau ditunda ke pendekatan mekanistik saja.
2. **Jagung dan Kedelai (2022)**: Ditandai sebagai `SUSPECT` di seluruh visualisasi dan analisis utama (dibatasi 2015–2021, $N=7$ tahun).
3. **Hortikultura (Cabai & Tomat)**: Terkunci di **Tier B (Rule-Based IFWC Advisory)**. Tidak ada regresi hasil tahunan dan tidak ada supervised ML penyakit tanaman.
