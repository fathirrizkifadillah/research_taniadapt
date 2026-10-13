# Pra-Registrasi Hipotesis Ekonometrika & Fenologi (TaniAdapt Phase 6 EDA — Audit Revision v2)

Dokumen ini mengunci seluruh hipotesis pengujian empiris, jendela fenologi, strategi koreksi *multiple testing*, dan batas deteksi statistik (**MDE**) **SEBELUM** menjalankan Exploratory Data Analysis (EDA) di Phase 6 dan regresi panel di Phase 9.

> [!IMPORTANT]
> **Aturan Metodologis & Anti-P-Hacking**:
> - **Git Commit Hash**: `8f69dcb` | **Git Tag**: `v2-audit-closure`
> 1. **Pre-Registered Variables**: Seluruh variabel cuaca dan jendela waktu yang tercantum di bawah ini bersifat terikat. Dilarang menambah variabel atau menggeser jendela waktu secara ad-hoc setelah melihat data eksplorasi.
> 2. **Keluarga Uji & Koreksi *Multiple Testing***:
>    - **Keluarga Primer**: **Holm-Bonferroni** (mengontrol *Family-Wise Error Rate* / FWER secara ketat).
>    - **Keluarga Sekunder**: **Benjamini-Hochberg** (mengontrol *False Discovery Rate* / FDR).
> 3. **Jendela Tumpang Tindih**: Variasi jendela waktu yang saling tumpang-tindih (misalnya Mar–Mei vs Apr–Jun) diklasifikasikan sebagai **uji sensitivitas**, BUKAN hipotesis independen terpisah.
> 4. **Bahasa Inferensi**: Wajib menggunakan terminologi "berasosiasi dengan" atau "konsisten dengan hipotesis agronomis". Dilarang menggunakan klaim kausalitas mutlak ("menyebabkan", "menunjukkan").

---

## 1. Kerangka Fenologi & Jendela Kalender Tanam (KATAM)

Outcome produktivitas resmi dilaporkan dalam agregat tahunan per kabupaten/kota. Oleh karena itu, pengujian menggunakan spesifikasi fenologi siklus pertanian:
1. **Spesifikasi Musim Hujan (MH / Rendengan)**: Tanam Okt/Nov tahun $T-1$ s.d. Panen Jan/Feb tahun $T$.
2. **Spesifikasi Musim Kemarau I (MK I / Gadu 1)**: Tanam Mar/Apr s.d. Panen Jun/Jul tahun $T$.
3. **Spesifikasi Musim Kemarau II (MK II / Palawija)**: Tanam Jul/Agu s.d. Panen Okt/Nov tahun $T$.
4. **Uji Sensitivitas Jendela**: Penggeseran seragam $\pm 1$ bulan untuk mengevaluasi stabilitas koefisien terhadap variabilitas penanggalan tanam riil petani.

---

## 2. Hipotesis Terdaftar per Komoditas

### A. Padi Sawah (Tier A)
*Panel: 18 Kabupaten sentra, 2015–2017 (Baseline pre-KSA valid, area-weighted mean cocok 100% dengan BPS Provinsi). Periode 2018–2020 Galura dieksklusikan dari panel utama karena terdeteksi artefak GKP (+21.8%) dan hanya digunakan sebagai uji sensitivitas jika data BPS KSA per kabupaten tersedia.*

| ID | Variabel Cuaca | Jendela Waktu | Arah Asosiasi | Rasional Agronomis & Sitasi Resmi | Status Sitasi & Inferensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H_RICE_01** | Presipitasi Akumulasi MH (`precip_sum_mh`) | Okt – Jan (MH) | **Non-linear cekung ($\cap$)** | Air cukup memacu anakan produktif; kelebihan presipitasi memicu genangan anaerob dan busuk akar (Hosokawa et al., 2023). | Transfer Regional (Asia Tenggara); Panel FE Kuadratik, Wild Cluster Bootstrap |
| **H_RICE_02** | Suhu Maksimum Rata-rata (`tmax_mean_mk1`) | Mar – Mei (MK I) | **Negatif ($-$)** | Suhu tinggi (>35°C) saat *anthesis* memicu dehisiensi antera dan sterilitas serbuk sari (Prasad et al., 2006; Jagadish et al., 2007; *Catatan: Paper 15 Ansari et al. 2021 adalah simulasi CropSyst Wonogiri, bukan bukti sterilitas anthesis*). | Transfer Biologis; Panel FE OLS, Wild Cluster Bootstrap |
| **H_RICE_03** | Consecutive Dry Days (`cdd_mk1`) | Apr – Jun (MK I) | **Negatif ($-$)** | Cekaman kekeringan pada fase pengisian bulir mereduksi konduktansi stomata dan bobot 1.000 butir gabah (Boonjung & Fukai, 1996; Hosokawa et al., 2023). | Transfer Fisiologis; Panel FE OLS, Sensitivitas terhadap H_RICE_02 |
| **H_RICE_04** | Radiasi Surya Akumulasi (`solar_rad_mh`) | Des – Feb (MH) | **Positif ($+$)** | Radiasi surya tinggi saat pengisian bulir meningkatkan akumulasi biomassa fotosintesis dan indeks panen (Yoshida, 1981; Evans, 1993). | Transfer Fisiologis Padi; Panel FE OLS, Wild Cluster Bootstrap |

---

### B. Jagung (Tier A)
*Panel: 18 Kabupaten sentra, 2015–2021 (Tahun 2022 SUSPECT dieksklusikan dari panel utama karena 13 kabupaten memiliki angka imputasi identik 75.70 ku/ha). Regresi WLS menggunakan Fixed Baseline Harvest Area (rata-rata luas panen 2015–2017). Kabupaten Subang dianalisis terpisah.*

| ID | Variabel Cuaca | Jendela Waktu | Arah Asosiasi | Rasional Agronomis & Sitasi Resmi | Status Sitasi & Inferensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H_CORN_01** | Presipitasi Akumulasi Vegetatif (`precip_veg`) | Feb – Apr | **Positif ($+$)** | Fase vegetatif awal membutuhkan kelembapan tanah yang cukup untuk kanopi dan inisiasi tongkol (Heino et al., 2023 [Paper 13]). | Transfer Global Tempered; WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_CORN_02** | Suhu Rata-rata Tumbuh (`tmean_grow`) | Mar – Mei | **Negatif ($-$)** | Peningkatan suhu mempercepat kematangan dini (*forced maturity*) dan mengurangi durasi pengisian biji (Schlenker & Roberts, 2009; Heino et al., 2023). | Transfer Literatur; WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_CORN_03** | Vapor Pressure Deficit Maksimum (`vpd_max`) | Apr – Jun | **Negatif ($-$)** | Defisit tekanan uap tinggi memicu penutupan stomata dan stres transpirasi ekstrem saat pembentukan tongkol (Lobell et al., 2014). | Transfer Literatur (US Corn Belt); Sensitivitas terhadap H_CORN_02 |
| **H_CORN_04** | Hari Kering Berurutan (`cdd_corn`) | Mei – Jul | **Negatif ($-$)** | Kekeringan parah saat *tasseling* dan *silking* memperpanjang *anthesis-silking interval* (ASI) sehingga menggagalkan penyerbukan tongkol (Grant et al., 1989; Bänziger et al., 2000). | Transfer Fisiologis Jagung; WLS Fixed-Weight FE, Wild Cluster Bootstrap |

---

### C. Kedelai (Tier A)
*Panel: 17 Kabupaten sentra (Kriteria ex ante: Kabupaten dengan catatan produktivitas > 0 minimal 6 dari 8 tahun kalender), periode 2015–2021 (Tahun 2022 SUSPECT dieksklusikan karena standar deviasi menyusut ekstrem ke 0.19 ku/ha).*

| ID | Variabel Cuaca | Jendela Waktu | Arah Asosiasi | Rasional Agronomis & Sitasi Resmi | Status Sitasi & Inferensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H_SOY_01** | Presipitasi Pembentukan Polong (`precip_pod`) | Jun – Agu (MK II) | **Positif ($+$)** | Fase pembentukan dan pengisian biji polong sangat rentan terhadap defisit lengas tanah (Desclaux et al., 2000; Board & Kahlon, 2011). | Transfer Literatur Agronomi; WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_SOY_02** | Suhu Malam Rata-rata (`tmin_night`) | Jul – Sep | **Negatif ($-$)** | Suhu malam tinggi meningkatkan laju respirasi gelap dan menguras asimilat fotosintesis yang disimpan untuk pembesaran biji (Hatfield et al., 2011; Heinemann et al., 2006). | Transfer Fisiologis Kedelai; WLS Fixed-Weight FE, Wild Cluster Bootstrap |
| **H_SOY_03** | Frekuensi Hari Hujan Lebat Panen (`heavy_rain_harvest`) | Agu – Okt | **Negatif ($-$)** | Hujan lebat saat matang fisiologis memicu pembusukan biji dalam polong, kerontokan, dan infeksi cendawan tular tanah (Ray et al., 2015; Board & Kahlon, 2011). | Transfer Literatur; WLS Fixed-Weight FE, Wild Cluster Bootstrap |

---

### D. Cabai & Tomat (Tier B — Modul IFWC Aturan Mikroklimat)
*Pendekatan: Rule-based literatur transfer & persentil relatif lokal per sel per bulan kalender. DILARANG menggunakan regresi yield tahunan (N=8 tidak mencukupi) ataupun supervised ML klasifikasi penyakit (karena label insidensi penyakit 100% absen).*

| ID | Indikator Mikroklimat | Jendela Waktu | Ambang Respons Relatif Pre-Registered | Rasional Agronomis & Keterbatasan |
| :--- | :--- | :--- | :--- | :--- |
| **H_HORT_01** | Proksi Kondensasi Titik Embun Malam Hari | Dini hari (Fajar) | **Persentil ke-10 ($P_{10}$) dari depresiasi embun ($T_{\min} - T_d$) per sel per bulan kalender** | Lapisan air bebas pada permukaan daun menjadi media perkecambahan spora cendawan antraknosa (*Colletotrichum capsici*) dan busuk daun (*Phytophthora*) (Sentelhas et al., 2008). *Keterbatasan: T_min harian dibandingkan dengan T_d rata-rata 24-jam (timing mismatch); tanpa sensor leaf wetness, ini adalah proksi heuristik, bukan bukti validasi fisik.* |
| **H_HORT_02** | Anomali Kejenuhan Air Mingguan | Jendela bergerak 7-hari | **Persentil ke-90 ($P_{90}$) akumulasi presipitasi mingguan historis sel** | Kelebihan air tanah memicu kondisi hipoksia/anaerob akar, memicu layu bakteri (*Ralstonia*) dan kerontokan bunga cabai. |

---

## 3. Desain Inferensi Ekonometrika & Minimum Detectable Effect (MDE)

### A. Desain Inferensi & Clustering
1. **Unit Klaster Utama**: Standard error diklaster pada level **Kabupaten ($G pprox 18$)**.
2. **Wild Cluster Bootstrap**: Karena jumlah klaster terbatas ($G = 17	ext{--}18$), rumus asimptotik cluster-robust SE dapat *understate* ketidakpastian. Inferensi utama menggunakan **Wild Cluster Bootstrap** (Cameron, Gelbach, & Miller, 2008) dengan bobot Webb (karena $G < 20$) atau Rademacher.
3. **Uji Sensitivitas Spasial**: Koreksi korelasi spasial lintas unit (Conley spatial HAC) diestimasi sebagai uji ketahanan (*robustness check*). Randomization inference digunakan sebagai alternatif non-parametrik.
4. **Anti-Overfitting Constraint**: Dilarang mengestimasi tren linear waktu spesifik per kabupaten (*district-specific linear time trends*) bersamaan dengan FE Kabupaten dan FE Tahun pada panel pendek ($T = 6	ext{--}8$). Spesifikasi tersebut mengonsumsi $2 	imes G + T$ derajat bebas dan mengikis hampir seluruh variasi sinyal cuaca.
5. **Uji Falsifikasi Temporal (Lead Weather Placebo)**: Menambahkan cuaca masa depan ($W_{i, t+1}$) sebagai plasebo. 
   > [!WARNING]
   > **Catatan Interpretasi Plasebo**: Non-signifikansi ($p > 0.10$) pada uji plasebo adalah syarat perlu (*necessary condition*), namun **BUKAN bukti ketiadaan pembaur (*proof of absence of confounding*)** pada desain panel berdaya statistik rendah (*low power*).

### B. Hasil Perhitungan Empiris Minimum Detectable Effect (MDE)
Dihitung secara empiris dari varians residual fixed-effects panel 18 sentra kabupaten Jawa Barat ($lpha = 0.05$, Power = $80\%$, $t_{	ext{multiplier}} pprox 2.97	ext{--}2.99$):

| Komoditas | Klaster ($G$) | Tahun ($T$) | Total Obs ($N$) | Residual SD ($\sigma_\epsilon$) | MDE (Log Points) | MDE Persentase (%) | Implikasi Penafsiran |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Padi Sawah (2015–2017 Pre-KSA)** | 18 | 3 | 54 | 0.0456 | **0.0233** | **2.35%** | Variasi hasil padi sangat homogen; mampu mendeteksi syok cuaca $\ge 2.35\%$, namun rentang waktu sangat pendek ($T=3$). |
| **Jagung (2015–2021 Ex-2022 WLS)** | 18 | 7 | 124 | 0.7724 | **0.2296** | **25.81%** | Heterogenitas hasil jagung antar-kabupaten tinggi; anomali cuaca harus mengubah hasil $\ge 25.8\%$ agar terdeteksi secara reliabel. |
| **Kedelai (2015–2021 Ex-2022 Sentra)** | 17 | 7 | 115 | 0.3160 | **0.0983** | **10.33%** | Panel kedelai mampu mendeteksi fluktuasi cuaca berskala $\ge 10.3\%$. |

*Catatan: Seluruh estimasi regresi di Phase 6 dan Phase 9 wajib menyertakan MDE di samping effect size dan 95% Confidence Interval.*
