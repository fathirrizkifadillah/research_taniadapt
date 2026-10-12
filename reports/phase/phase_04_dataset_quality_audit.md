# TaniAdapt Research Dossier — Phase 4: Dataset Quality Audit

**Status**: COMPLETED / RATIFIED  
**Penutupan Blocker**: 11 Blocker Data Audit (A1 s/d A11) berhasil diselesaikan tanpa fabrikasi data.

---

## 1. Temuan Kritis Kualitas Data Lapangan
Audit data Phase 4 mengungkap anomali dan kelemahan serius dalam data sekunder yang wajib dimitigasi:
1. **Ketiadaan Data Ground Truth Serangan Hama & Penyakit (OPT)**: Di Jawa Barat tidak tersedia basis data resmi geospasial harian untuk intensitas serangan OPT lokal tingkat kabupaten. Hal ini melarang penggunaan model klasifikasi ML untuk memprediksi serangan penyakit secara langsung.
2. **Artefak Imputasi Birokrasi Jagung & Kedelai 2022**: Pada data Dinas Pertanian tahun 2022, ditemukan angka kembar persis 75.70 ku/ha di 13 kabupaten. Seluruh data jagung dan kedelai tahun 2022 **DIKELUARKAN SECARA TOTAL** dari panel analisis sensitivitas.
3. **Koreksi Denominator CHIRPS vs AgERA5**: Unit evaluasi bulanan dikoreksi secara akurat menjadi $N = 936$ unit-bulan (karena anomali kekosongan data Indramayu dan Depok).
4. **Baseline Padi 2015–2017**: Diberi penanda transparan `PENDING_MANUAL_VERIFICATION` sampai pengguna memverifikasi manual terhadap buku cetak BPS Jabar Dalam Angka.
5. **Koreksi Oragrafis SRTM DEM**: Ditemukan jarak pergeseran rata-rata 5.8 km antara centroid kabupaten dengan pusat sel AgERA5, dengan koreksi elevasi orografis untuk wilayah pegunungan (Garut, Cianjur, Bandung).
