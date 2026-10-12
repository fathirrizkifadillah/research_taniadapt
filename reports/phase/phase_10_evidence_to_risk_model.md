# TaniAdapt Research Dossier — Phase 10: Evidence → Risk Model

**Status**: COMPLETED  
**Ruang Lingkup**: Penerjemahan Bukti Ilmiah Terverifikasi Menjadi Model Risiko Agronomi Terkalibrasi  
**Prinsip Desain**: Zonasi Risiko Berbasis Neraca Lengas Tanah FAO-56, Proksi Mikroklimat Spora Fajar $P_{10}$, & Safeguard Ketidakcukupan Bukti

---

## 1. Landasan Bukti Ilmiah Model Risiko
Phase 10 bertanggung jawab menjembatani temuan analitik (Phase 7–9) menjadi model risiko fisis yang deterministik. Sesuai kontrak bukti TaniAdapt, status risiko **BUKAN** skor tebakan 0–100 atau probabilitas palsu, melainkan dipetakan ke 3 domain fisis terkalibrasi:

---

## 2. Tiga Domain Model Risiko Agronomi Terkalibrasi

### A. Domain 1: Risiko Cekaman Kekeringan Abiotik (Abiotic Water Deficit Stress)
* **Dasar Bukti Ilmiah**: `FAO56_ET0_PM` (Allen et al. 1998 Eq. 6) dan `FAO56_KC_*` (Tabel 12 halaman 110, status: **`VERIFIED`**).
* **Indikator Kunci**: Neraca Lengas Tanah Kumulatif 14-Hari:
  $$\text{CWB}_{14\text{d}} = \sum_{i=1}^{14} (P_i - ET_{c,i}), \quad \text{di mana } ET_{c} = K_c \times ET_0$$
* **Profil Koefisien Tanaman ($K_c$) Terverifikasi**:
  * Padi Sawah: $K_c = 1.05$ (awal) $	o 1.20$ (tengah/bunting) $	o 0.75$ (akhir/pemasakan).
  * Jagung: $K_c = 0.30$ (awal) $	o 1.20$ (tengah/silking) $	o 0.48$ (akhir).
  * Kedelai: $K_c = 0.40$ (awal) $	o 1.15$ (tengah/polong) $	o 0.50$ (akhir).
  * Tomat: $K_c = 0.60$ (awal) $	o 1.15$ (tengah/berbuah) $	o 0.80$ (akhir).
* **Ambang Kalibrasi Risiko Neraca Lengas 14-Hari**:
  * **`normal`**: $\text{CWB}_{14\text{d}} \ge -25.0\text{ mm}$ (suplai hujan dan lengas tanah mencukupi).
  * **`waspada_defisit_ringan`**: $-50.0\text{ mm} \le \text{CWB}_{14\text{d}} < -25.0\text{ mm}$ (evaporasi melebihi curah hujan).
  * **`kondisi_stres_abiotik`**: $\text{CWB}_{14\text{d}} < -50.0\text{ mm}$ (defisit parah, memicu penutupan stomata dan stres hasil $\to$ pemicu irigasi *replenishment*).

### B. Domain 2: Risiko Genangan Air Abiotik (Anaerobic Waterlogging Stress)
* **Dasar Bukti Ilmiah**: Indikator Iklim Ekstrem Presipitasi AgERA5.
* **Indikator Kunci**: Presipitasi Akumulasi 3-Hari ($\sum P_{3\text{d}}$) dan Consecutive Wet Days ($CWD$).
* **Ambang Kalibrasi**:
  * Jika $\sum P_{3\text{d}} \ge 100.0\text{ mm}$ ATAU $CWD \ge 5\text{ hari}$ berturut-turut dengan hujan lebat $\to$ Status: **`kondisi_stres_abiotik`** (Pemicu alert pemeriksaan parit drainase untuk mencegah anoksia akar).

### C. Domain 3: Risiko Mikroklimat Biotik OPT (Fungal Spore Condensation Risk)
* **Dasar Bukti Ilmiah**: Tier B Agrometeorology Relative Percentile Rule (Sentelhas et al. 2008).
* **Indikator Kunci**: Depresi Titik Embun Fajar:
  $$\Delta T_{\text{embun}} = T_{\min} - T_d$$
* **Ambang Kalibrasi**:
  * Hari basah kondensasi terpicu jika $\Delta T_{\text{embun}} \le P_{10}$ (persentil ke-10 historis sel cuaca per bulan kalender).
  * Jika dalam jendela 7 hari terakhir terdapat **$\ge 3$ hari kondusif** $\to$ Status: **`kondisi_mendukung_OPT`** (Pemicu panduan *field scouting* gejala penyakit antraknosa/hawar daun sebelum infeksi meledak).
  * *Aturan Pelaporan*: Sistem wajib melaporkan **jumlah hari kondusif dalam jendela N hari terakhir**, DILARANG mengarang angka persentase risiko penyakit.

### D. Domain 4: Safeguard Ketidakcukupan Bukti (Insufficient Evidence Handling)
* Jika tanaman belum memiliki koefisien $K_c$ terverifikasi (mis. cabai rawit/merah `CHILI_WATER: UNVERIFIED`) atau parameter suhu kardinal thermal GDD belum terverifikasi $\to$ Status Wajib: **`evidence_insufficient`**.
* Sistem menolak mengarang ambang racun atau dosis kimia, dan memicu aksi default: `ACT_AWAIT_EVIDENCE`.

---

## 3. Hasil Validasi Empiris pada Data Jawa Barat (2015–2024)
* **Sentra Jagung Subang**: Status `kondisi_stres_abiotik` terpicu pada **24.2% hari** (883 hari), terkonsentrasi tajam pada musim kemarau (Mei–Oktober) dengan puncak saat El Niño 2015, 2019, dan 2023.
* **Sentra Hortikultura Garut**: Ambang relatif $P_{10}$ depresi embun mendeteksi klaster kebasahan daun pada **9.0% hari pengamatan** (66 hari/tahun), memicu status `kondisi_mendukung_OPT` secara proporsional tanpa menghasilkan peringatan palsu (*false alarm*).
