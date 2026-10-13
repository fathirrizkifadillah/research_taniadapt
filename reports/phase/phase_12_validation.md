# TaniAdapt Research Dossier — Phase 12: Preliminary Face-Validity Check (n=3 Peristiwa) & System Stress-Testing

**Status**: PENDING_USER_RATIFICATION  
**Klasifikasi Evaluasi**: Preliminary Face-Validity Check (Bukan uji kausal yield, bukan validasi kehilangan panen)  
**Dokumen Induk Rencana**: `docs/hindcast_plan.md` (v2)  
**Cakupan Spasial**: 18 Sentra Pangan Jawa Barat sebagai Satu Klaster Spasial Regional ($n=3$ Peristiwa)

---

## 1. Evaluasi Face-Validity Peristiwa Ekstrem Historis BMKG ($n=3$)

Evaluasi dijalankan pada level peristiwa ($n=3$) untuk menguji apakah indikator iklim terkonvensi mencerminkan anomali yang terdokumentasi oleh BMKG:

| Peristiwa Iklim Ekstrem BMKG | Karakteristik Agrometeorologis | Indikator Konvensi yang Diuji | Hasil Evaluasi Sentra | Evaluasi Level Peristiwa ($n=3$) |
|---|---|---|:---:|:---:|
| **1. Kemarau Basah La Niña 2016** | Hujan anomali persisten sepanjang musim kemarau (Mei–Oktober 2016), anomali presipitasi $> +50\%$. | Rata-rata presipitasi 14-hari $> P_{75}$ ATAU water balance $> P_{75}$ ATAU CDD $< P_{25}$. | 18 / 18 Sentra Memenuhi | **DETECTED** |
| **2. Kemarau Ekstrem IOD(+) 2019** | Kemarau terpanjang dekade 2010-an; kombinasi IOD positif kuat dan El Niño lemah. | **Syarat Konjungsi**: Max CDD $> P_{75}$ **DAN** Rata-rata presipitasi 14-hari $< P_{25}$. | 18 / 18 Sentra Memenuhi | **DETECTED** |
| **3. Super El Niño 2023** | Anomali SST Pasifik $> +2.0^\circ\text{C}$, kekeringan parah meluas di Pantura dan Priangan Timur. | **Syarat Konjungsi**: Max CDD $> P_{75}$ **DAN** Rata-rata presipitasi 14-hari $< P_{25}$. | 16 / 18 Sentra Memenuhi (2 Miss) | **DETECTED (Sebagian Sentra)** |

---

## 2. Dokumentasi Data Obyektif 2 MISS pada Peristiwa 2023

Pada peristiwa kemarau 2023, sistem mencatat 2 sentra yang tidak memenuhi syarat konjungsi ganda:
1. **Kabupaten Indramayu**:
   * *Maksimum CDD*: 87 hari ($> P_{75} = 5.0\text{ hari}$).
   * *Rata-rata Presipitasi 14-Hari*: $9.09\text{ mm}$ (Ambang $P_{25} = 8.28\text{ mm}$).
   * *Selisih Jarak*: $+0.81\text{ mm}$ di atas $P_{25}$.
   * *Status*: **MISS**. Gagal karena syarat `mean_precip < P25` tidak terpenuhi.
2. **Kabupaten Tasikmalaya**:
   * *Maksimum CDD*: 17 hari ($> P_{75} = 0.0\text{ hari}$).
   * *Rata-rata Presipitasi 14-Hari*: $41.46\text{ mm}$ (Ambang $P_{25} = 38.77\text{ mm}$).
   * *Selisih Jarak*: $+2.69\text{ mm}$ di atas $P_{25}$.
   * *Status*: **MISS**. Gagal karena syarat `mean_precip < P25` tidak terpenuhi.

*Catatan Integritas*: Kedua kasus miss dilaporkan murni berdasarkan data, tanpa rasionalisasi pasca-fakta.

---

## 3. Evaluasi Tahun Kontrol & False-Alarm Rate

Pengujian pada tahun kontrol tanpa anomali ekstrem makro:
1. **Tahun Kontrol 2017 (Netral/Normal BMKG)**:
   * False-alarm kemarau ekstrem: **0 / 18 Sentra (0.0%)**.
   * Alarm basah: **1 / 18 Sentra (5.6%)** (Spesifisitas 94.4%).
2. **Tahun Kontrol 2021 (Normal / La Niña Lemah)**:
   * False-alarm kemarau ekstrem: **0 / 18 Sentra (0.0%)**.

---

## 4. Uji Ketahanan Sistem (Stress-Testing & Edge Cases)

Decision Engine diuji terhadap 5 skenario ekstrem:

| Skenario Uji Ketahanan | Kondisi Input Ekstrem | Respons Decision Engine yang Terverifikasi | Tingkat Lulus Uji |
|---|---|---|:---:|
| **EC1: Data Sensor Cuaca Hilang / Kosong** | Input cuaca harian bernilai `NaN`, null, atau rekaman terputus $> 3$ hari. | Sistem mengembalikan status resmi **`evidence_insufficient`**, menolak membuat tebakan tanpa data lokal. | **PASS (100%)** |
| **EC2: Badai Hujan Konvektif Ekstrem** | Presipitasi mendadak $> 150\text{ mm/hari}$ (kejadian badai tropis lokal). | Sistem mengaktifkan status **`kondisi_stres_abiotik`** (genangan air), memicu status **HINDARI/MERAH** untuk penyemprotan dan pemupukan, serta menyarankan inspeksi drainase. | **PASS (100%)** |
| **EC3: Lonjakan Angin Kencang Ekstrem** | Kecepatan angin mendadak naik $> 25\text{ km/j}$ pada siang hari. | Sistem secara deterministik mengubah status jadwal semprot menjadi **HINDARI/MERAH** (*Bahaya spray drift*) dan memperingatkan risiko kerusakan kanopi. | **PASS (100%)** |
| **EC4: Permintaan Komoditas / Aturan Unverified** | Pengguna memilih komoditas cabai rawit untuk rekomendasi air presisi atau status OPT. | Sistem mengembalikan **`evidence_insufficient`** untuk neraca air karena $K_c$ cabai belum terverifikasi (`CHILI_WATER: UNVERIFIED`), dan mengembalikan **`evidence_insufficient`** untuk status OPT jika aturan belum VERIFIED (hanya menampilkan indikator observasi tanpa diagnosis spekulatif). | **PASS (100%)** |
| **EC5: Permintaan Dosis Racun Kimia Spesifik** | Pengguna menanyakan dosis fungisida kimia tertentu melalui antarmuka asisten. | Decision Engine mengembalikan **`claim_forbidden`** dan memicu aksi `ACT_REFER_PPL_CHEMICAL`, mengarahkan pengguna ke PPL setempat tanpa dosis sintetis dari sistem. | **PASS (100%)** |

---

## 5. Integritas Arsitektur & Kepatuhan Skema
* **Graceful Degradation Pass Rate**: **100%** (Seluruh kasus batas tertangani secara aman tanpa runtime exception).
* **Kepatuhan Validasi Skema**: **100%** (Seluruh payload JSON tervalidasi terhadap `schemas/engine_output.schema.json` Draft 2020-12 dan lulus suite pengujian `pytest tests/test_engine_schema_and_rules.py`).
