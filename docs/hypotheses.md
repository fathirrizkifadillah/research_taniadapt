# Pra-Registrasi Hipotesis Ekonometrika & Fenologi (TaniAdapt Phase 6 EDA)

Dokumen ini mengunci seluruh hipotesis pengujian empiris **SEBELUM** menjalankan Exploratory Data Analysis (EDA) di Phase 6 dan pemodelan regresi di Phase 9. 

> [!IMPORTANT]
> **Aturan Anti-P-Hacking**: Variabel dan jendela waktu yang tercantum di bawah ini bersifat terikat (*pre-registered*). Analis dilarang memilih variabel atau mengubah definisi jendela waktu setelah melihat korelasi data. Seluruh pengujian akan dikoreksi untuk *multiple hypothesis testing* (Holm-Bonferroni & Benjamini-Hochberg FDR).
> **Prinsip Inferensi**: Seluruh klaim wajib menggunakan bahasa asosiasi empiris, bukan klaim kausal mutlak tanpa identifikasi eksperimental.

---

## 1. Kerangka Fenologi & Jendela Kalender Tanam (KATAM)

Karena outcome produktivitas pada data primer dilaporkan dalam agregat tahunan (bukan per musim), pengujian akan menggunakan dua spesifikasi utama disertai uji sensitivitas:
1. **Spesifikasi A (Tahun Kalender)**: Januari s.d. Desember tahun $T$.
2. **Spesifikasi B (Jendela Siklus Pertanian KATAM)**: Oktober tahun $T-1$ s.d. September tahun $T$.
   - **Musim Hujan (MH / Rendengan)**: Tanam Okt/Nov – Panen Jan/Feb.
   - **Musim Kemarau I (MK I / Gadu 1)**: Tanam Mar/Apr – Panen Jun/Jul.
   - **Musim Kemarau II (MK II / Gadu 2 / Palawija)**: Tanam Jul/Agu – Panen Okt/Nov.
3. **Uji Sensitivitas Jendela**: Penggeseran awal jendela tanam sebesar $\pm 1$ bulan untuk mengevaluasi ketahanan estimasi terhadap variasi tanggal tanam petani riil.

---

## 2. Hipotesis Terdaftar per Komoditas (Maksimal 3–4 Variabel Utama)

### A. Padi Sawah (Tier A)
*Panel: 18 Kabupaten sentra, 2015–2020. Catatan: Menggunakan data resmi BPS KSA untuk periode 2018–2020 guna menghindari distorsi artefak satuan GKP/GKG Galura (Audit B1).*

| ID | Variabel Cuaca | Jendela Waktu | Arah Asosiasi Diharapkan | Rasional Agronomis & Sitasi | Uji Statistik & Inferensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H_RICE_01** | Presipitasi Akumulasi MH (`precip_sum_mh`) | Okt – Jan (MH) | **Non-linear cekung ($\cap$)** | Air cukup memacu pertumbuhan, namun kelebihan memicu genangan/kebusukan akar (Paper 12: Hosokawa et al., 2023). | Panel FE Kuadratik, Wild Cluster Bootstrap |
| **H_RICE_02** | Suhu Maksimum Rata-rata (`tmax_mean_mk1`) | Mar – Mei (MK I) | **Negatif ($-$)** | Suhu tinggi saat *anthesis* menginduksi sterilitas serbuk sari bulir padi (Paper 15: Ansari et al., 2021). | Panel FE OLS, Wild Cluster Bootstrap |
| **H_RICE_03** | Consecutive Dry Days (`cdd_mk1`) | Apr – Jun (MK I) | **Negatif ($-$)** | Cekaman kekeringan pada fase pengisian bulir mereduksi bobot 1.000 butir gabah. | Panel FE OLS, Wild Cluster Bootstrap |
| **H_RICE_04** | Radiasi Surya Akumulasi (`solar_rad_mh`) | Des – Feb (MH) | **Positif ($+$)** | Radiasi surya tinggi saat pengisian bulir meningkatkan akumulasi biomassa fotosintesis. | Panel FE OLS, Wild Cluster Bootstrap |

---

### B. Jagung (Tier A)
*Panel: 18 Kabupaten sentra, 2015–2022. Pembobotan regresi wajib menggunakan Fixed Baseline Harvest Area (rata-rata luas panen 2015–2017) untuk mencegah bias endogenitas luas tahun berjalan. Kabupaten Subang diuji terpisah.*

| ID | Variabel Cuaca | Jendela Waktu | Arah Asosiasi Diharapkan | Rasional Agronomis & Sitasi | Uji Statistik & Inferensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H_CORN_01** | Presipitasi Akumulasi Tanam (`precip_veg`) | Feb – Apr | **Positif ($+$)** | Fase vegetatif awal jagung membutuhkan kelembapan tanah yang memadai (Paper 13: Heino et al., 2023). | WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_CORN_02** | Suhu Rata-rata Tumbuh (`tmean_grow`) | Mar – Mei | **Negatif ($-$)** | Peningkatan suhu mempercepat pematangan dini (*forced maturity*) dan mengurangi berat tongkol (Paper 13, 14). | WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_CORN_03** | Vapor Pressure Deficit Maksimum (`vpd_max`) | Apr – Jun | **Negatif ($-$)** | VPD tinggi memicu penutupan stomata dan cekaman transpirasi saat pembentukan tongkol. | WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_CORN_04** | Hari Sangat Kering berturut-turut (`cdd_corn`) | Mei – Jul | **Negatif ($-$)** | Kekeringan parah saat *tasseling* dan *silking* menggagalkan penyerbukan tongkol. | WLS Fixed-Weight FE, Wild Cluster Bootstrap |

---

### C. Kedelai (Tier A)
*Panel: 17 Kabupaten sentra, 2015–2022. Catatan: Tahun 2022 wajib dievaluasi terhadap dugaan imputasi seragam provinsi (Audit 2022: std deviasi mengecil ke 0.19 ku/ha).*

| ID | Variabel Cuaca | Jendela Waktu | Arah Asosiasi Diharapkan | Rasional Agronomis & Sitasi | Uji Statistik & Inferensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H_SOY_01** | Presipitasi Fase Perkandungan (`precip_pod`) | Jun – Agu (MK II) | **Positif ($+$)** | Fase pembentukan dan pengisian polong sensitif terhadap defisit air tanah. | WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_SOY_02** | Suhu Malam Rata-rata (`tmin_night`) | Jul – Sep | **Negatif ($-$)** | Suhu malam tinggi meningkatkan respirasi gelap dan menguras fotosintat. | WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_SOY_03** | Frekuensi Hari Hujan Lebat Panen (`heavy_rain_harvest`) | Agu – Okt | **Negatif ($-$)** | Hujan saat panen memicu pembusukan biji di polong dan rebah batang. | WLS Fixed-Weight FE, Wild Cluster Bootstrap |

---

### D. Cabai & Tomat (Tier B — Modul IFWC Aturan Mikroklimat)
*Pendekatan: Rule-based literatur transfer & persentil relatif lokal. Dilarang menggunakan regresi yield tahunan ataupun supervised ML klasifikasi penyakit.*

| ID | Indikator Mikroklimat | Jendela Waktu | Ambang Respons Relatif | Rasional Agronomis & Sitasi |
| :--- | :--- | :--- | :--- | :--- |
| **H_HORT_01** | Proksi Durasi Kebasahan Daun Malam | Dini hari (00:00–06:00) | **Persentil terendah ($P_{10}$ / $P_{20}$) dari depresiasi embun ($T_{\min} - T_d$)** | Ketika suhu udara mendekati titik embun, lapisan air bebas terbentuk pada permukaan daun, menjadi media perkecambahan spora cendawan (*Colletotrichum*, *Phytophthora*) (Sentelhas et al., 2008; Campbell & Norman, 1998). |
| **H_HORT_02** | Persentil Relatif Curah Hujan Mingguan | Jendela 7-hari kalender berjalan | **Anomali hujan relatif $> P_{85}$ historis grid** | Tanah jenuh air memicu kondisi anaerob perakaran, busuk pangkal batang, dan rontok bunga. |

---

## 3. Protokol Ekonometrika & Mitigasi Klaim Semu (*Spurious Claims*)

Mengingat daya statistik panel tahunan berdurasi pendek ($T=6\text{--}8$) terbatas pada MDE besar ($\pm 35\%$ log points), protokol inferensi berikut wajib dipatuhi:

1. **Wild Cluster Bootstrap & Randomization Inference**:
   Karena jumlah klaster waktu sangat sedikit ($G = 6\text{--}8$ tahun), rumus standard error cluster asimptotik tidak valid. Inferensi signifikansi wajib menggunakan Wild Cluster Bootstrap (Cameron, Gelbach, & Miller, 2008) dengan bobot Webb atau Rademacher.
2. **Leave-One-Year-Out (LOO) Sensitivity Test**:
   Model wajib diestimasi ulang secara iteratif dengan membuang satu tahun per iterasi—khususnya membuang tahun Super El Niño 2015—untuk memastikan hasil regresi tidak didorong secara artifisial oleh satu kejadian bencana ekstrem tunggal.
3. **Uji Falsifikasi Temporal (Lead Weather Placebo)**:
   Memasukkan anomali cuaca masa depan ($W_{i, t+1}$) ke dalam model hasil panen tahun berjalan ($Y_{i, t}$). Koefisien $\beta_{t+1}$ **wajib tidak signifikan ($p > 0.10$)**. Jika cuaca masa depan signifikan memprediksi hasil panen masa lalu, model gugur karena menangkap tren semu.
4. **Pelaporan Effect Size & 95% Confidence Interval**:
   Wajib melaporkan besaran elastisitas ekonomi beserta rentang estimasi ketidakpastian 95% CI, bukan sekadar pelaporan bintang signifikansi $p$-value.
5. **Trade-Off Year Fixed Effects vs Indeks ENSO/IOD**:
   Indeks makro ONI dan DMI bervariasi secara serentak per tahun di seluruh Jawa Barat, sehingga kolinier sempurna dengan Year Fixed Effects. Model utama wajib menggunakan Year Fixed Effects (mengontrol seluruh syok makro bersama); model alternatif mengganti Year FE dengan kovariat eksplisit ONI/DMI secara terpisah.
6. **Posisi Realistis Tier A**:
   Hasil regresi panel empiris 6–8 tahun ini difungsikan sebagai **uji konsistensi agronomis (*consistency check*)**, bukan pembuktian elastisitas kausal mutlak. Jika variasi data tidak mencukupi, status resmi yang dicatat adalah **"Evidence Insufficient"**.
