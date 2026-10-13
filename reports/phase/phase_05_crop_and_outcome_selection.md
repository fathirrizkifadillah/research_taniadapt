# TaniAdapt Research Dossier — Phase 5: Crop & Outcome Selection

**Status**: PENDING_USER_RATIFICATION (Menunggu Ratifikasi Pengguna Manusia)  
**Hasil Ratifikasi**: Mengunci Portofolio 5 Komoditas Terpilih dan Menetapkan Kelas Analisis Spesifik  

---

## 1. Portofolio 5 Komoditas Terpilih & Metodologi Analisis

| Komoditas | Nama Ilmiah | Periode Data Valid | Ukuran Sampel ($N$) | Pangsa Luas Panen Jabar (DS08) | Sentra Utama | Kelas Analisis Registry Resmi | Dasar Keputusan & Catatan Metodologis |
|---|---|:---:|:---:|:---:|---|---|---|
| **Padi Sawah** | *Oryza sativa* | 2015–2017 | $N = 54$ unit-tahun ($df=33$) | 82.4% luas pangan | Indramayu, Karawang, Subang | `mechanistic advisory` | Derajat kebebasan statistik ($df=33$) terlalu sempit untuk regresi panel bebas bias; baseline BPS berstatus `PENDING_MANUAL_VERIFICATION`. Dialihkan penuh ke neraca air Penman-Monteith FAO-56. |
| **Jagung** | *Zea mays* | 2015–2021 (eksklusi 2022) | $N = 124$ unit-tahun | 11.8% luas pangan | Garut (41.2%), Majalengka, Tasikmalaya | `empirical sensitivity analysis + mechanistic advisory` | Memiliki panel terpanjang dan terbersih pasca eliminasi imputasi kembar 2022. Evaluasi sensitivitas empiris menghasilkan MDE $\pm 0.1444$ dengan status jujur `evidence_insufficient`. |
| **Kedelai** | *Glycine max* | 2015–2021 (eksklusi 2022) | $N = 113$ unit-tahun | 5.8% luas pangan | Sukabumi, Garut, Cianjur | `empirical sensitivity analysis + mechanistic advisory` | 17 sentra aktif dianalisis untuk respons stres kebasahan dan suhu malam tropis pengisian polong. |
| **Cabai (Merah & Rawit)** | *Capsicum spp.* | 2017–2024 | $N = 8$ tahun (agregat provinsi) | 48.6% luas sayuran buah | Garut, Ciamis, Bandung | `Tier B literature-transfer rule` | Outcome hanya tersedia di level provinsi SBS. Dilarang keras melakukan regresi yield atau ML penyakit. Dipantau via proksi mikroklimat fajar $P_{10}$ depresi embun. |
| **Tomat** | *Solanum lycopersicum* | 2017–2024 | $N = 8$ tahun (agregat provinsi) | 24.1% luas sayuran buah | Bandung Barat, Garut, Cianjur | `Tier B literature-transfer rule + mechanistic advisory` | Memiliki koefisien tanaman terverifikasi FAO-56 ($K_c: 0.60 \to 1.15 \to 0.80$) serta pemantauan risiko kebasahan spora hawar daun fajar. |

---

## 2. Komoditas yang Dikeluarkan dari Sistem (Excluded Crops)
* **Bawang Merah (*Allium cepa*)**:
  * *Status*: **`blocked pending new data`**.
  * *Alasan Eksklusi*: Tingkat produksi sangat terkonsentrasi di sedikit kantong mikro spesifik (Brebes perbatasan Cirebon/Majalengka), data panel di level kabupaten memiliki lonjakan ekstrim non-biologis dan ketiadaan koefisien fenologi terkonvensi, belum dikalibrasi terhadap data lapangan untuk dataran rendah tropis basah. Sistem menolak mengarang model bawang merah sampai tersedia data mikro baru.

---

## 3. Implikasi bagi Arsitektur Decision Engine
Keputusan Phase 5 menetapkan pembagian kerja yang jelas bagi Decision Engine:
1. Padi, Jagung, Kedelai, dan Tomat mendapatkan perhitungan neraca kebutuhan air harian ($ET_c = K_c 	imes ET_0$) karena koefisien $K_c$ terverifikasi di FAO-56 Tabel 12.
2. Cabai dan Tomat mendapatkan pemantauan risiko penyakit jamur berbasis persentil fajar lokal $P_{10}$ depresi embun.
3. Cabai dilarang menghitung neraca air biofisik spesifik karena parameter koefisien air cabai berstatus `UNVERIFIED` di evidence registry (menghasilkan status `evidence_insufficient`).
