# Hindcast Plan v2: Preliminary Face-Validity Check (n=3 Peristiwa)

**Status:** PENDING_USER_RATIFICATION  
**Klasifikasi Evaluasi:** Preliminary Face-Validity Check (Bukan uji kausal yield, bukan validasi kehilangan panen, bukan inferensi statistik independen).  
**Tujuan:** Menguji secara awal apakah indikator agrometeorologi lokal mencerminkan sinyal cuaca pada peristiwa anomali iklim ekstrem historis yang terdokumentasi oleh BMKG di Jawa Barat.

---

## 1. Desain Evaluasi & Pembatasan Metodologis

1. **Struktur Klaster Spasial Regional ($n=3$ Peristiwa)**:
   * Sesuai audit PCA spasial (Item A3), 22 sel cuaca Jawa Barat sangat berkorelasi ($r = 0.727$) di mana Komponen Utama 1 (PC1) menyerap 74.97% varians spasial.
   * Oleh karena itu, 18 sentra pangan Jawa Barat membentuk **satu klaster spasial regional bersama** yang dipengaruhi oleh monsun dan telekoneksi makro (ENSO/IOD).
   * Laporan keberhasilan dihitung pada **level peristiwa ($n=3$)**, bukan diklaim sebagai $N = 54$ sampel independen.
2. **Kriteria Konvensi Pelaporan (Bukan Ambang Kerusakan Agronomi)**:
   * Seluruh ambang batas yang digunakan dalam evaluasi ini berstatus **konvensi pelaporan heuristik** berbasis peringkat persentil lokal, bukan ambang kerusakan biofisik tanaman yang tervalidasi di lahan.

---

## 2. Kriteria Evaluasi Tertulis & Periode Uji

### A. Tiga Peristiwa Ekstrem BMKG yang Diuji ($n=3$)

| ID Peristiwa | Periode Observasi | Peristiwa Terdokumentasi (Sumber Primer BMKG) | Kriteria Deteksi (Konvensi Tertulis) | Hasil Evaluasi Level Sentra | Status Peristiwa |
|---|---|---|---|:---:|:---:|
| **HC_2016_WET** | Okt–Des 2016 | La Niña lemah & IOD negatif; BMKG mencatat potensi hujan ekstrem di Jawa Barat (Buletin Ketahanan Pangan BMKG Vol. 3, 2016). | Rata-rata presipitasi 14-hari $> P_{75}$ ATAU rata-rata water balance $> P_{75}$ ATAU rata-rata CDD $< P_{25}$. | 18 / 18 Sentra Memenuhi | **DETECTED** |
| **HC_2019_DRY** | Jun–Okt 2019 | Kemarau ekstrem; BMKG mencatat dampak El Niño aktif s.d. Juli 2019 dan IOD positif kuat memicu kemarau panjang terparah dekade 2010-an (Refleksi Bencana Iklim BMKG 2019). | **Syarat Konjungsi**: Maksimum CDD $> P_{75}$ **DAN** Rata-rata presipitasi 14-hari $< P_{25}$. | 18 / 18 Sentra Memenuhi | **DETECTED** |
| **HC_2023_DRY** | Jun–Nov 2023 | Super El Niño & IOD positif; BMKG mendokumentasikan kekeringan meteorologis panjang dan deret hari kering ekstrem di Jawa Barat (Siaran Pers BMKG Nov 2023). | **Syarat Konjungsi**: Maksimum CDD $> P_{75}$ **DAN** Rata-rata presipitasi 14-hari $< P_{25}$. | 16 / 18 Sentra Memenuhi (2 Miss) | **DETECTED (Sebagian Sentra)** |

---

## 3. Dokumentasi Obyektif 2 MISS pada Peristiwa HC_2023_DRY

Pada peristiwa kemarau 2023, sistem mencatat 2 sentra yang tidak memenuhi syarat konjungsi ganda:

1. **Kabupaten Indramayu**:
   * *Maksimum CDD*: 87 hari (Memenuhi syarat CDD: $87 > P_{75} = 5.0\text{ hari}$).
   * *Rata-rata Presipitasi 14-Hari*: $9.09\text{ mm}$.
   * *Ambang $P_{25}$ Presipitasi*: $8.28\text{ mm}$.
   * *Jarak ke Kriteria*: $+0.81\text{ mm}$ di atas ambang batas $P_{25}$.
   * *Status*: **MISS**. Gagal karena curah hujan rata-rata sedikit melampaui batas persentil ke-25 sebesar 0.81 mm.
2. **Kabupaten Tasikmalaya**:
   * *Maksimum CDD*: 17 hari (Memenuhi syarat CDD: $17 > P_{75} = 0.0\text{ hari}$).
   * *Rata-rata Presipitasi 14-Hari*: $41.46\text{ mm}$.
   * *Ambang $P_{25}$ Presipitasi*: $38.77\text{ mm}$.
   * *Jarak ke Kriteria*: $+2.69\text{ mm}$ di atas ambang batas $P_{25}$.
   * *Status*: **MISS**. Gagal karena hujan lokal di Tasikmalaya mempertahankan rata-rata 14-hari 2.69 mm di atas $P_{25}$.

*Catatan Integritas*: Kedua miss dilaporkan apa adanya berdasarkan data terhitung, tanpa rasionalisasi pasca-fakta (*no post-hoc rationalization*).

---

## 4. Evaluasi Tahun Kontrol, Penjelasan Aturan Jendela, & Batasan Baseline

### A. Aturan Jendela HIT Berbasis P25 & P75
Kriteria deteksi peristiwa kekeringan (HC_2019_DRY dan HC_2023_DRY) menerapkan **aturan konjungsi ganda (conjunctive rule)**:
1. `max(CDD)` dalam jendela musiman $> P_{75}$ historis deret CDD lokal sel.
2. `mean(rolling_14d_precip)` dalam jendela musiman $< P_{25}$ historis presipitasi 14-hari lokal sel.
Kedua syarat wajib terpenuhi bersamaan agar dapat dinyatakan sebagai **HIT**.

### B. Baseline yang Dipakai & Keterlibatan Tahun Peristiwa
- **Distribusi Referensi**: Karena data klimatologi 30 tahun (1991–2020) dari CDS API saat ini baru terunduh untuk 6 sel unik, ambang persentil $P_{25}$ dan $P_{75}$ pada skrip evaluasi saat ini dihitung dari data 10 tahun AgERA5 (2015–2024) per sel.
- **Keterlibatan Tahun Peristiwa**: Tahun peristiwa (2016, 2019, 2023) **termasuk di dalam baseline 10 tahun** tersebut. 
- **Implikasi Metodologis**: Menyertakan tahun ekstrem ke dalam perhitungan baseline menaikkan ambang $P_{75}$ dan menurunkan ambang $P_{25}$, sehingga kriteria menjadi lebih ketat (*conservative bias*). Pada revisi mendatang dengan basis murni 1991–2020, tahun peristiwa akan sepenuhnya berada di luar (*out-of-sample*) dari baseline.

### C. Evaluasi Tahun Kontrol (False-Alarm Rate)
Pengujian pada tahun kontrol tanpa anomali ekstrem makro:
1. **Tahun Kontrol 2017 (Tahun Netral Tipikal BMKG)**:
   * *Alarm Kering Palsu (Dry False Alarm)*: **0 / 18 Sentra (0.0% False Alarm Rate, Spesifisitas Kering = 100.0%)**. Tidak ada sentra yang memicu alarm kemarau.
   * *Alarm Basah (Wet Alarm)*: **1 / 18 Sentra (5.6% False Alarm Rate, Spesifisitas Basah = 94.4%)**.
2. **Tahun Kontrol 2021 (Tahun Normal / La Niña Lemah Terlokalisir)**:
   * *Alarm Kering Palsu (Dry False Alarm)*: **0 / 18 Sentra (0.0% False Alarm Rate, Spesifisitas Kering = 100.0%)**.
   * *Alarm Basah (Wet Alarm)*: **7 / 18 Sentra (38.9%)** (mencerminkan anomali basah regional di Jawa bagian barat pada akhir 2021).

---

## 5. Kesimpulan Face-Validity Check
Pengujian hindcast non-yield ini hanya berfungsi sebagai **preliminary face-validity check**: menunjukkan bahwa indikator iklim terkonvensi mampu membedakan tahun ekstrem dan tahun kontrol tanpa menghasilkan false alarm kemarau pada tahun normal. Pengujian ini tidak memvalidasi model hasil panen ataupun diagnosis penyakit tanaman.
