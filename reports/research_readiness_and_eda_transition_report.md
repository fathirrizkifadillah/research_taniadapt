# 🌾 TaniAdapt Research Readiness & Audit Transition Report (Revisi Rinci Berbasis Masukan Claude)
**Laporan Kesiapan Riset Portofolio 9 Dataset & Notebook Menuju Phase 6 (Exploratory Data Analysis)**  
**Target Pembaca:** Independent Reviewer / Claude / Research Advisory Board  
**Prinsip Desain:** *Evidence $\rightarrow$ Finding $\rightarrow$ Agronomic Interpretation $\rightarrow$ Model $\rightarrow$ Decision Logic*  
**Status Kesiapan:** **LAYAK MEMASUKI PHASE 6 (EDA) DENGAN MITIGASI METODOLOGIS KETAT & PEMOSISIAN REALISTIS TIER A** (Bukan klaim berlebihan "siap 100%")  
**Lokasi Berkas:** `reports/research_readiness_and_eda_transition_report.md`

---

## 1. Executive Summary & Tanggapan Terhadap Review Independen

Tinjauan independen terhadap portofolio riset TaniAdapt menyoroti empat kelebihan kunci yang telah solid:
1. **Blocker B1 (Padi 2019):** Rasio DS03/BPS yang konstan pada $1,188 \pm 0,004$ di 27 kabupaten membuktikan adanya artefak satuan (GKP vs GKG), bukan fluktuasi cuaca.
2. **Dekomposisi Yield Subang (DS08):** Terbuktinya efek penyusutan luas panen ($113\text{--}765\text{ ha}$) menjelaskan volatilitas angka yield tanpa mengorbankan logika agronomi.
3. **Audit Daya Statistik (M3):** Transparansi batas daya deteksi (MDE) menjadi landasan metodologis yang jujur.
4. **Pembagian Tier A vs Tier B:** Pemisahan antara tanaman pangan beresolusi kabupaten (Tier A) dan hortikultura provinsi tanpa label penyakit (Tier B) diterima secara sains data dan biologi patogen.

Namun, tinjauan independen juga mengidentifikasi **enam kelemahan dan risiko metodologis** yang harus diperbaiki secara komputasional sebelum melangkah ke analisis lanjutan. Laporan ini merinci perbaikan konkret atas keenam poin tersebut berbasis bukti eksekusi kode di `scripts/` dan data di `reports/dataset_audit/`.

---

## 2. Resolusi & Perbaikan Enam Isu Metodologis Kritis

### 2.1 Isu 1: Rekonsiliasi Penuh Padi (2015–2020) & Kewaspadaan Imputasi Jagung/Kedelai

Laporan awal hanya mengevaluasi lonjakan tahun 2019. Audit komputasional menyeluruh terhadap seluruh runtun waktu 2015–2020 (`reports/dataset_audit/b1_rice_full_ratio_audit.csv`) mengungkapkan dinamika berikut:

| Tahun | DS03 Mean (Ku/Ha) | BPS Resmi (Ku/Ha) | Rasio DS03 / BPS | Selisih terhadap BPS (%) | YoY DS03 (%) | YoY BPS (%) | Catatan Metodologi BPS |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2015** | 60,19 | 60,19 | **1,0001** | $+0,01\%$ | — | — | Survei Ubinan Lama |
| **2016** | 59,58 | 59,58 | **0,9999** | $-0,01\%$ | $-1,03\%$ | $-1,01\%$ | Survei Ubinan Lama |
| **2017** | 57,47 | 57,47 | **0,9999** | $-0,01\%$ | $-3,54\%$ | $-3,54\%$ | Survei Ubinan Lama |
| **2018** | 55,39 | 56,51 | **0,9802** | $-1,98\%$ | $-3,61\%$ | $-1,67\%$ | Mulai Transisi KSA BPS |
| **2019** | 68,55 | 57,69 | **1,1882** | $\mathbf{+18,82\%}$ | $\mathbf{+23,75\%}$ | $\mathbf{+2,09\%}$ | Puncak Artefak Satuan (GKP) |
| **2020** | 54,22 | 56,82 | **0,9543** | $\mathbf{-4,57\%}$ | $\mathbf{-20,90\%}$ | $\mathbf{-1,51\%}$ | Penurunan Drastis Pasca-Artefak |

**Temuan & Keputusan Metodologis:**
1. Membagi angka 2019 dengan faktor konstan $1,188$ hanya mengoreksi tahun 2019, namun menyisakan distorsi pada tahun 2018 (DS03 berada $-2,0\%$ di bawah BPS) dan tahun 2020 (DS03 anjlok ke $-4,6\%$ di bawah BPS, dengan penurunan YoY $-20,9\%$ vs BPS hanya $-1,5\%$).
2. **Keputusan:** Data produktivitas padi untuk periode KSA (2018–2020) **diganti langsung dengan angka resmi BPS KSA per kabupaten/kota**, bukan mengandalkan penyesuaian faktor ad-hoc pada data Galura.
3. **Peringatan Imputasi Jagung & Kedelai:** Audit terhadap data jagung dan kedelai Galura (`b2_maize_soybean_imputation_audit.csv`) mendeteksi anomali pelaporan seragam pada tahun 2022:
   - Kedelai 2022: Seluruh 27 kabupaten/kota tiba-tiba terisi nilai dengan standar deviasi yang anjlok drastis ke $0,19\text{ ku/ha}$ (rata-rata $14,31$, median $14,30$).
   - Jagung 2022: Sebanyak 6 wilayah (Bogor, Bekasi, Karawang, Purwakarta, Pangandaran, Kota Bandung) memiliki angka kembar persis $75,70\text{ ku/ha}$.
   - **Tindakan:** Tahun 2022 pada jagung dan kedelai Galura ditandai sebagai *suspected administrative imputation* dan wajib direkonsiliasi dengan publikasi BPS "Jawa Barat Dalam Angka 2023" sebelum dimasukkan ke model panel.

---

### 2.2 Isu 2: Bias Absolut AgERA5 vs CHIRPS & Penggunaan Relatif

Klaim awal bahwa AgERA5 "terbukti valid dan bebas bias fatal" telah direvisi secara jujur. Perbandingan kuantitatif titik-per-titik (`reports/dataset_audit/b3_rainfall_bias_chirps_audit.csv`) antara AgERA5 dan CHIRPS v2 (produk *satellite-gauge blending*) menunjukkan adanya bias absolut yang substansial:

| Stasiun / Wilayah | Tahun Evaluasi | CHIRPS v2 (mm/thn) | AgERA5 (mm/thn) | Bias Absolut (mm) | Bias Relatif (%) | Karakteristik Wilayah |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **TASIKMALAYA** | 2016 (La Niña) | 5.817,8 | 4.541,4 | **-1.276,5** | **-21,9%** | Lereng Selatan Galunggung (AgERA5 lebih kering) |
| **TASIKMALAYA** | 2020 | 4.250,5 | 4.045,6 | -204,9 | -4,8% | AgERA5 mendekati CHIRPS |
| **TASIKMALAYA** | 2024 | 3.328,7 | 2.970,2 | -358,5 | -10,8% | AgERA5 lebih kering |
| **SUBANG** | 2016 / 2020 / 2024 | ~3.030 | ~2.990 | -40,5 | **-1,4%** | Dataran Rendah / Sentra Padi (Sangat Konsisten) |
| **GARUT** | 2016 / 2020 / 2024 | 3.541,7 | 4.425,1 | **+883,4** | **+26,9%** | Pegunungan Selatan (AgERA5 lebih basah) |
| **BANDUNG** | 2016 / 2020 / 2024 | 2.672,3 | 3.821,5 | **+1.149,2** | **+45,3%** | Cekungan Dataran Tinggi (AgERA5 jauh lebih basah) |
| **PURWAKARTA** | 2016 / 2020 / 2024 | 3.680,6 | 2.709,6 | **-970,9** | **-26,0%** | Perbukitan Tengah (AgERA5 lebih kering) |
| **KARAWANG** | 2016 / 2020 / 2024 | 2.586,6 | 2.526,7 | -59,9 | **-2,0%** | Pesisir Pantura (Sangat Konsisten) |
| **SUKABUMI** | 2016 / 2020 / 2024 | 4.358,9 | 4.384,2 | +25,3 | **+2,0%** | Wilayah Selatan Luas (Rata-rata Konsisten) |

**Koreksi Ilmiah & Implikasi Praktis:**
1. **Bias Absolut Substansial:** Meskipun kedua produk sepakat dalam *ranking* spasial (Tasikmalaya, Sukabumi, dan Garut konsisten sebagai 3 wilayah terbasah di Jawa Barat), selisih nilai absolutnya berkisar antara $-26\%$ hingga $+45\%$ (ratusan hingga ribuan milimeter per tahun).
2. **Koreksi Diksi:** Kata "terbukti efek orografis" diubah menjadi **"konsisten dengan hipotesis pengangkatan orografis Priangan Timur"**, dan CHIRPS diperlakukan secara tepat sebagai **produk satelit-gauge terasimilasi**, bukan *ground-truth* stasiun permukaan murni.
3. **Aturan Pemodelan Agroklimat:**
   - **DILARANG** menggunakan ambang batas milimeter absolut kaku (misalnya: "curah hujan $>200\text{ mm/bulan} = \text{optimal}$") yang ditarik dari literatur asing.
   - **WAJIB** mentransformasikan data presipitasi ke dalam bentuk **anomali terstandarisasi ($z$-score spasial-temporal)** atau **persentil historis lokal ($P_{25}, P_{75}$)** spesifik per sel grid/kabupaten.

---

### 2.3 Isu 3: Eliminasi Total Ambang Batas Buatan ($T_{\min} - T_d < 1,0^\circ\text{C}$)

1. **Penghapusan Angka Keras:** Kalimat pada laporan sebelumnya yang memuat batas keras "$T_{\min} - T_d < 1,0^\circ\text{C}$ didukung literatur" telah **dihapus sepenuhnya** karena tidak memiliki sitasi empiris langsung dari lapangan Jawa Barat.
2. **Penggantian ke Skor Relatif:** Modul Indeks Kondisi Cuaca Mendukung (IFWC) hortikultura dialihkan murni ke:
   - **Persentil terendah ($P_{10}$ atau $P_{20}$) dari nilai depresiasi titik embun harian ($T_{\min} - T_d$)** spesifik per wilayah dan per bulan kalender.
   - Rujukan dasar mikrometeorologi tetap mengacu pada literatur durasi kebasahan daun (*leaf wetness duration*) standar (Sentelhas et al., 2008; Campbell & Norman, 1998) tanpa menetapkan ambang derajat absolut buatan.
3. **Koreksi Diksi Komparasi:** Kalimat "tomat vs kedelai membuktikan..." telah diperbaiki menjadi **"analisis komparatif menunjukkan bahwa kedelai memiliki unit observasi yang jauh lebih memadai untuk analisis panel dibanding tomat"**.

---

### 2.4 Isu 4: Reposisi Jujur Tier A Menghadapi Keterbatasan Daya Statistik (M3)

Simulasi daya statistik (`scripts/audit_m3_power_simulation.py`) menghasilkan **Minimum Detectable Effect (MDE) sebesar $\pm 35\%$ log points** pada daya $80\%$ ($\alpha = 0,05$) dengan struktur panel pendek $N = 18\text{--}27$, $T = 6\text{--}8$ tahun, dan korelasi spasial $\rho \approx 0,60$.

**Realitas Agronomis & Konsekuensi Logis:**
* Efek fluktuasi cuaca normal di literatur agronomis (Schlenker & Roberts, 2009; Lobell et al., 2011) berkisar antara **$-1\%$ s.d. $-7,5\%$ per derajat Celsius** atau deviasi hujan moderat.
* Koefisien variasi (CV) hasil panen di kabupaten sentra utama Jawa Barat (Karawang, Subang, Garut) hanya berada di kisaran **$4\% - 10\%$**.
* **Konsekuensi Jujur:** Panel tahunan 6–8 tahun ini **hampir pasti tidak memiliki daya statistik untuk mendeteksi variasi cuaca normal**, dan hanya mampu menangkap syok bencana iklim makro ekstrem (seperti Super El Niño 2015). Sebagian besar variabel cuaca spesifik diprediksi akan berstatus **"Evidence Insufficient"** jika hanya bergantung pada data panel pendek ini.

**Reposisi Arsitektur Tier A:**
Alih-alih mengklaim Tier A sebagai "model penentu elastisitas kausal definitif", Tier A dibingkai ulang secara ilmiah sebagai:
> **"Model agronomis berbasis proses mekanistik (akumulasi GDD fenologi, neraca air FAO-56 Penman-Monteith) di mana data panel empiris 6–8 tahun difungsikan murni sebagai uji konsistensi (*consistency check* / *sanity check* arah tanda koefisien)."**

**Roadmap Jangka Panjang Peningkatan Daya Statistik:**
1. **Perpanjangan Deret Waktu:** Mengakuisisi data produktivitas BPS/Kementan periode panjang (2000-an s.d. 2024, $T \approx 15\text{--}25$) dengan pemodelan struktural pemutus metodologi ubinan lama vs KSA 2018.
2. **Disagregasi Musiman:** Menggunakan data luas dan hasil panen per subround KSA BPS (Subround 1: Jan–Apr, Subround 2: Mei–Agu, Subround 3: Sep–Des).
3. **Integrasi Penginderaan Jauh:** Memanfaatkan proksi vegetasi satelit beresolusi temporal tinggi (MODIS / Sentinel NDVI & EVI 16-harian) untuk menangkap dinamika pertumbuhan intra-musiman.

---

### 2.5 Isu 5: Perbaikan Formulasi Pembobotan Luas Panen (WLS)

* **Masalah Luas Berjalan:** Menggunakan luas panen tahun berjalan sebagai bobot regresi WLS berisiko menimbulkan **bias endogenitas**, karena keputusan luas tanam dan luas panen petani itu sendiri merespons cuaca ekstrem (misalnya kekeringan memicu puso atau pembatalan tanam, sehingga luas panen menyusut drastis).
* **Solusi Diadopsi:** Formulasi pembobotan WLS diubah menjadi **Fixed Baseline Weighting**, yaitu menggunakan **rata-rata luas panen pada periode dasar (baseline 2015–2017)** untuk masing-masing kabupaten. Bobot ini bersifat eksogen terhadap fluktuasi cuaca tahun berjalan namun tetap mencerminkan skala sentra pertanian secara proporsional.

---

### 2.6 Isu 6: Protokol Inferensi Ketat & Mitigasi Klaim Semu (*Spurious Claims*)

1. **Jendela Waktu Agregasi Padi:**
   Karena data hasil panen dilaporkan dalam agregat tahun kalender sedangkan siklus tanam mencakup Musim Hujan (Rendengan) dan Musim Kemarau (Gadu), Phase 6 EDA akan mengevaluasi:
   - Jendela tahun kalender (Jan–Des).
   - Jendela siklus pertanian KATAM (Okt tahun $T-1$ s.d. Sep tahun $T$).
   - Uji sensitivitas pergeseran jendela tanam $\pm 1$ bulan.
2. **Wild Cluster Bootstrap:**
   Karena jumlah klaster waktu sangat sedikit ($G = 6\text{--}8$ tahun), rumus standard error cluster asimptotik tidak valid. Inferensi signifikansi wajib menggunakan **Wild Cluster Bootstrap** (Cameron, Gelbach, & Miller, 2008) dengan pembobotan Webb atau Rademacher.
3. **Leave-One-Year-Out (LOO) Sensitivity Test:**
   Regresi diestimasi ulang secara iteratif dengan membuang satu tahun per putaran—khususnya menyingkirkan tahun Super El Niño 2015—untuk memastikan hasil tidak didikte oleh satu tahun anomali tunggal.
4. **Uji Falsifikasi Temporal (Lead Weather Placebo):**
   Memasukkan variabel cuaca tahun $T+1$ terhadap hasil panen tahun $T$. Koefisien $\beta_{t+1}$ **wajib bernilai mendekati nol dan tidak signifikan ($p > 0,10$)**.
5. **Trade-Off Year Fixed Effects vs Kovariat ENSO/IOD:**
   Indeks ONI dan DMI bervariasi serentak per tahun untuk seluruh kabupaten, sehingga kolinier sempurna dengan Year Fixed Effects. Model utama menggunakan Year Fixed Effects (mengontrol seluruh syok makro); model alternatif mengganti Year FE dengan kovariat ONI/DMI eksplisit secara terpisah.
6. **Larangan Rujukan Akurasi Paper 12 ($R = 0,994$):**
   Korelasi tinggi Elastic Net pada Paper 12 dilarang dijadikan benchmark target akurasi karena berasal dari *cross-country level confounding*.

---

## 3. Matriks Kesiapan 9 Notebook Riset (`notebook/`)

Seluruh 9 notebook telah dieksekusi secara penuh (*in-place pre-rendered*) dengan output tabel data mentah dan visualisasi diagnostik tersimpan di dalamnya:

| Notebook | Komoditas / Fokus | Status Data & Eksekusi | Posisi Metodologis yang Diperbarui |
| :---: | :--- | :--- | :--- |
| **01_AgERA5** | Cuaca Harian 27 Kab/Kota ($N=98.631$) | **Pre-rendered** (Tabel 27 wilayah + Plot iklim) | Backbone cuaca mikro; analisis wajib berbasis anomali/$z$-score, bukan ambang batas milimeter absolut. |
| **02_bangladesh** | Benchmark Replikasi TWFE (64 Distrik) | **Pre-rendered** (Tabel panel + Line chart tren) | Cetak biru spesifikasi ekonometrika (Wild cluster bootstrap, dekomposisi musiman). Dilarang di-pooling. |
| **03_west_java_rice** | Produktivitas Padi Jabar (2015–2020) | **Pre-rendered** (Tabel + Plot lonjakan 2019) | Periode 2018–2020 wajib diganti data BPS KSA resmi; faktor pengali konstan tidak mencukupi. |
| **04_indonesia_agroclim** | Parquet ERA5 Derived 60 MB (12 Titik) | **Pre-rendered** (Head table + Matriks komparasi) | Validasi silang internal ERA5; bukan sumber operasional *live engine*. |
| **05_subang_maize** | Produktivitas Jagung Jabar (2015–2022) | **Pre-rendered** (Tabel + Regresi detrending) | Wajib WLS fixed base weight; data 2022 ditandai untuk rekonsiliasi BPS akibat dugaan imputasi seragam. |
| **06_west_java_hortic** | Hortikultura SBS Cabai & Tomat (Provinsi) | **Pre-rendered** (Tabel + Plot Cabai Rawit/Besar) | Tier B murni; tidak dimodelkan dengan regresi yield ataupun supervised ML penyakit. Bebas ambang keras. |
| **07_soybean_spatial** | Kedelai 27 Kab/Kota & Batas ADM2 | **Pre-rendered** (Tabel sentra + Peta 27 centroid) | 14 sentra penuh 8 tahun; data 2022 ditandai untuk rekonsiliasi BPS; sampel jauh lebih memadai dibanding tomat. |
| **08_production_area** | Produksi & Luas Panen (Padi, Jagung, Kedelai) | **Pre-rendered** (Uji identitas matematika + Subang) | Basis penurunan bobot WLS tetap (baseline area 2015–2017) dan verifikasi dekomposisi yield. |
| **09_climate_chirps** | Iklim Makro (ONI, DMI) & CHIRPS v2 | **Pre-rendered** (Timeseries ONI/DMI + Validasi hujan) | Kovariat kontrol sirkulasi makro; bias AgERA5 vs CHIRPS terdokumentasi lengkap per stasiun. |

---

## 4. Kesimpulan & Vonis Transisi ke Phase 6 EDA

### **VONIS: LAYAK MEMASUKI PHASE 6 EDA (DENGAN PENGAWASAN METODOLOGIS KETAT)**

1. **Eksplorasi EDA Berisiko Rendah:** Phase 6 adalah fase eksplorasi distribusi, korelasi awal, dan visualisasi tanpa estimasi kausal akhir. Proyek aman untuk melangkah ke Phase 6.
2. **Komitmen Anti-P-Hacking:** Seluruh hipotesis telah dikunci di [docs/hypotheses.md](file:///c:/CODING/research_taniAdapt/docs/hypotheses.md) dan ditandai dalam jejak commit Git sebelum kode EDA pertama dijalankan.
3. **Ekspektasi Hasil yang Realistis:** Tim peneliti tidak akan memaksakan hasil regresi panel jangka pendek ($T \le 8$) sebagai pembuktian kausal absolut, melainkan sebagai uji plausibilitas agronomis bagi engine rekomendasi adaptasi presisi.
