# Crop and Outcome Selection

**Status:** PENDING_USER_RATIFICATION (Keputusan Kanonik Pasca-Audit, Menunggu Ratifikasi Pengguna Manusia)  
**Tanggal Pengajuan:** 2026-10-13  
**Otoritas Bukti:** Didasarkan pada Audit Kualitas Data Phase 4 (Butir A1–A11) dan Analisis Eksplorasi Data Phase 6.

---

## 1. Kriteria Seleksi Berdasarkan Audit Data Empiris

Komoditas dan outcome diseleksi berdasarkan bukti empiris yang lolos audit integritas data, bukan asumsi teoretis:
1. **Integritas Target Outcome**: Observasi valid setelah penyaringan robust outlier/near-zero flag (`reports/logs/crop_cell_and_outlier_audit.csv`). `N_valid` tidak didefinisikan secara arbitrer dengan aturan `outcome > 0`.
2. **Cakupan Spasial & Resolusi Cuaca**: Pemadanan terhadap 22 sel AgERA5 unik (`reports/dataset_audit/a8_spatial_grid_cells_audit.csv`), di mana seluruh 18 kabupaten sentra pertanian memiliki sel grid cuaca independen (dan 17 sentra aktif kedelai memiliki 17 sel cuaca unik).
3. **Batas Deteksi Statistik (MDE)**: Pengujian daya deteksi panel via Wild Cluster Bootstrap Webb ($B=999$, klaster kabupaten). Jika estimasi berada di bawah MDE, efek dilarang diklaim kausal dan diklasifikasikan sebagai `evidence_insufficient`.
4. **Hierarki Kelas Registry Bukti**: Pembagian ketat antara *mechanistic advisory*, *empirical sensitivity analysis*, dan *Tier B literature-transfer rule*.

---

## 2. Portofolio Komoditas Pengajuan Resmi

| Komoditas | Outcome & Periode Analisis | N Valid (Robust Screen) | Sel Cuaca AgERA5 Unik | Kelas Registry Bukti | Batasan & Safeguard Metodologis |
|---|---|---:|---:|---|---|
| **Padi** | ADM2 produktivitas tahunan, 2015–2017 | 53 | 18 | `mechanistic advisory` | Baseline 2015–2017 berstatus `PENDING_MANUAL_VERIFICATION`; dilarang regresi panel cuaca primer karena $T=3$ ($df=33$) tidak memadai untuk inferensi kausal. Modul penyiraman deplesi tanah berstatus `evidence_insufficient` karena Kc FAO-56 mengasumsikan sawah tergenang. |
| **Jagung** | ADM2 produktivitas tahunan, 2015–2021 | 121 | 18 | `empirical sensitivity analysis + mechanistic advisory` | Tahun 2022 dieksklusikan (`SUSPECT`); estimasi efek presipitasi $\beta = +0.0368$ berada di bawah $\text{MDE} = \pm 0.1444$ (`evidence_insufficient`). |
| **Kedelai** | ADM2 produktivitas tahunan, 2015–2021 | 112 (MAD-z) / 115 (raw non-zero) | 17 | `empirical sensitivity analysis + mechanistic advisory` | Tahun 2022 dieksklusikan (`SUSPECT`); tepat 17 sentra aktif ex-ante ($N \ge 6$ tahun, Kabupaten Bekasi non-aktif dieksklusikan) dengan tepat 17 sel AgERA5 unik dari `a8_spatial_grid_cells_audit.csv`. |
| **Cabai** | Produktivitas tahunan provinsi, 2017–2024 | 8 per target | Agregat provinsi (tidak ada unit sel terdefinisi) | `Tier B literature-transfer rule` | Zero temporal overlap data kab/kota (`od_18096` hanya 2013–2014); 100% tanpa label ground truth OPT; dilarang regresi yield atau klasifikasi ML penyakit. |
| **Tomat** | Produktivitas tahunan provinsi, 2017–2024 | 8 | Agregat provinsi (tidak ada unit sel terdefinisi) | `Tier B literature-transfer rule + mechanistic advisory` | Zero temporal overlap data kab/kota; dilarang regresi yield atau ML penyakit; kebutuhan air menggunakan Kc FAO-56 Tabel 12 terverifikasi. |
| **Bawang Merah** | Tidak ada outcome lokal memenuhi syarat | — | — | `blocked pending new data` | Dieksklusikan dari portfolio operasional awal engine karena ketiadaan data sentra terpercaya. |

*Catatan Pangsa Luas Panen*: Angka pangsa luas panen sengaja tidak dimasukkan dari ingatan (klaim Garut `>60%` resmi dihapus) dan ditangguhkan hingga agregasi DS08 tervalidasi penuh.

---

## 3. Verifikasi Data, Audit, dan Temuan EDA

Pemilihan portofolio di atas didasarkan pada temuan empiris yang telah diperiksa di repositori:
1. **Audit Integritas Padi (Item A1 & B1)**:
   * Rata-rata berbobot luas panen DS03 cocok 100.0% (selisih 0.00%–0.01%) dengan publikasi resmi BPS Jawa Barat 2015–2017 (`reports/dataset_audit/bps_manual_input.csv`).
   * Lonjakan seragam 2019 (+21.8%) merupakan artefak pelaporan administratif konversi GKP Galura, sehingga periode 2018–2020 resmi dieksklusikan dari panel utama.
   * Daya statistik pada $T=3$ menghasilkan $\text{MDE} = \pm 0.0255$ log points ($df=33$), yang mencerminkan sempitnya variasi residual dalam-kabupaten (2.14%), bukan daya deteksi cuaca tinggi.
2. **Audit Jagung Subang & Jabar (Item A3, A4, A5, B1)**:
   * Deteksi imputasi birokrasi 2022: 13 kabupaten memiliki angka identik persis 75.70 ku/ha. Eksklusi titik 2022 menurunkan CV residu detrended Subang ke 5.49%.
   * Dekomposisi log produksi mengindikasikan 98.4% lonjakan produksi Subang disumbang oleh ekspansi luas panen, bukan lompatan produktivitas akibat cuaca.
   * Model regresi panel WLS `H_CORN_01` (presipitasi vegetatif Feb–Apr) menghasilkan $\beta = +0.0368$ dengan 95% Webb CI $[-0.0521, +0.1300]$ dan $\text{MDE} = \pm 0.1444$. Karena CI mencakup nol dan $|\beta| < \text{MDE}$, hubungan cuaca-yield tahunan tidak memenuhi syarat kausalitas (`evidence_insufficient`).
3. **Audit Sentra Kedelai (Item A3, A9, A10)**:
   * Kolapsnya standar deviasi spasial kedelai pada 2022 ke 0.19 ku/ha mengindikasikan imputasi provinsi seragam.
   * Penyaringan ex-ante kabupaten aktif minimal 6 tahun menghasilkan panel 17 sentra pertanian (mengecualikan Kabupaten Bekasi yang hanya aktif 2 tahun). Ke-17 sentra ini memetakan ke tepat **17 sel AgERA5 unik** dengan $\text{MDE} = \pm 0.1250$ log points.
4. **Audit Hortikultura Cabai & Tomat (Item A6 & B4)**:
   * CV empiris produktivitas provinsi sejati adalah 4.49% (Cabai Besar) dan 5.71% (Cabai Rawit).
   * Ketiadaan tumpang tindih waktu cuaca pasca-2014 dan absennya label insidensi OPT membatasi hortikultura ke aturan transfer literatur agrometeorologi.

---

## 4. Jalur Pemodelan yang Diizinkan (Permitted Model Paths)

### A. Padi
Menggunakan **jalur penasihat mekanistik (mechanistic advisory)** murni.
* Formula: Evapotranspirasi referensi FAO-56 Penman-Monteith (`FAO56_ET0_PM`) dan koefisien tanaman padi (`FAO56_KC_RICE`: $K_{c,\text{ini}}=1.05, K_{c,\text{mid}}=1.20, K_{c,\text{end}}=0.75$, FAO-56 Tabel 12 p. 110).
* Batasan: Menghitung referensi $ET_c$ setelah kalender tanam diberikan. Dilarang memprediksi yield atau menetapkan ambang kehilangan hasil. Modul irigasi deplesi tanah berstatus `evidence_insufficient` karena sawah tergenang air.

### B. Jagung dan Kedelai
Menggunakan **analisis sensitivitas empiris + penasihat mekanistik**.
* Formula: Evaluasi sensitivitas cuaca dibatasi pada pelaporan elastisitas terdaftar. Penasihat kebutuhan air menggunakan `FAO56_ET0_PM`, `FAO56_KC_MAIZE` ($K_{c,\text{ini}}=0.30, K_{c,\text{mid}}=1.20, K_{c,\text{end}}=0.48$), `FAO56_KC_SOY` ($K_{c,\text{ini}}=0.40, K_{c,\text{mid}}=1.15, K_{c,\text{end}}=0.50$), dan kriteria deplesi lengas tanah `FAO56_RAW_DEPLETION` ($RAW = p \times TAW$).
* Batasan: Dilarang mengubah estimasi atau CI regresi menjadi aturan risiko yield atau prakiraan produksi. Parameter termal kardinal tetap berstatus unverified.

### C. Cabai dan Tomat
Menggunakan **aturan transfer literatur Tier B (Tier B literature-transfer rule)**.
* Formula: Metrik keluaran dibakukan sebagai **jumlah hari kondusif dalam jendela N hari terakhir** berbasis persentil lokal $P_{10}$ depresiasi titik embun fajar ($T_{\min} - T_d$). Kebutuhan air tomat mengacu pada `FAO56_KC_TOMATO` ($K_{c,\text{ini}}=0.60, K_{c,\text{mid}}=1.15, K_{c,\text{end}}=0.80$).
* Batasan: Dilarang keras menampilkan skor risiko 0–100, probabilitas penyakit numerik, klaim keterjadian penyakit fisik, atau prediksi kehilangan hasil. Ambang suhu/RH literal berstatus `PENDING_LITERATURE`. Jika aturan belum VERIFIED, status wajib `evidence_insufficient`.
