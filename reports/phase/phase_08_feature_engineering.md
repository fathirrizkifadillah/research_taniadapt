# TaniAdapt Research Dossier — Phase 8: Feature Engineering & Multicollinearity Diagnostics

**Status**: COMPLETED  
**Ruang Lingkup**: Pembangunan Feature Store Agrometeorologi 65.754 Baris (2015–2024) dan Analisis Diagnostik Kolinearitas VIF  
**Tujuan**: Menyiapkan Fitur Prediktif Berbasis Waktu Sekaligus Mengidentifikasi Bahaya Kolinearitas Data Tropis

---

## 1. Pembangunan Feature Store Agrometeorologi
Data harian AgERA5 (65.754 rekaman) diolah menjadi serangkaian fitur prediktif berorientasi agronomi:

### A. Fitur Temporal Lag & Jendela Bergerak (Rolling Window)
* **Lag Temporal (1 s/d 14 Hari)**: Menangkap memori lengas tanah dan dampak cuaca beberapa hari sebelumnya ($Lag_1, Lag_3, Lag_7, Lag_{14}$).
* **Jendela Bergerak Kumulatif (Rolling Sum & Mean)**:
  * Rolling 7-hari ($P_{7\text{d}}, T_{\text{mean}, 7\text{d}}$): Dinamika cuaca jangka pendek.
  * Rolling 14-hari ($P_{14\text{d}}, \text{CWB}_{14\text{d}}$): Jendela kritis kebutuhan air tanaman dan evapotranspirasi kumulatif.
  * Rolling 30-hari ($P_{30\text{d}}, ET_{0, 30\text{d}}$): Dinamika neraca air bulanan.

### B. Indeks Iklim Ekstrem & Ambang Biologis
* **Consecutive Dry Days (CDD)**: Akumulasi hari kering berturut-turut dengan curah hujan harian $< 1.0\text{ mm}$.
* **Consecutive Wet Days (CWD)**: Akumulasi hari basah berturut-turut dengan curah hujan harian $\ge 1.0\text{ mm}$.
* **Diurnal Temperature Range (DTR)**: Selisih suhu harian ($T_{\max} - T_{\min}$), indikator radiasi cerah dan pelepasan panas malam hari.
* **Vapor Pressure Deficit (VPD)**:
  $$VPD = e_s(T) - e_a = 0.6108 \exp\left(\frac{17.27 T}{T + 237.3}\right) - e_a$$
  Indikator daya hisap transpirasi atmosfer terhadap stomata daun.
* **Neraca Lengas Biofisik ($P - ET_0$)**: Surplus atau defisit air antara presipitasi harian dengan penguapan acuan Penman-Monteith.

---

## 2. Temuan Kritis Multikolinearitas Ekstrem (Variance Inflation Factor / VIF)

Pengujian diagnostik kolinearitas matriks fitur cuaca musiman menemukan multikolinearitas ekstrem yang sangat berbahaya bagi pemodelan machine learning:

| Variabel Fitur Agrometeorologi | Nilai VIF (*Variance Inflation Factor*) | Korelasi Tertinggi ($r$) | Implikasi bagi Pemodelan Machine Learning |
|---|:---:|---|---|
| **Defisit Lengas Air ($P - ET_0$)** | **4.312,9** (Ekstrem) | **$r = +0.996$** terhadap Total Curah Hujan | Variasi neraca air 99.6% didikte oleh hujan; koefisien regresi akan saling membatalkan secara liar bila dimasukkan bersama. |
| **Total Curah Hujan Musiman** | **3.704,6** (Ekstrem) | **$r = +0.929$** terhadap Hari Hujan Lebat | Volume curah hujan musiman terkonsentrasi pada kejadian badai konvektif lebat ($\ge 20\text{ mm/hari}$). |
| **Suhu Rata-rata Tumbuh** | **20,0** (Tinggi) | **$r = +0.697$** terhadap VPD Maksimum | Kenaikan suhu memperlebar defisit tekanan uap udara, memicu stres transpirasi serentak. |
| **Radiasi Surya Kumulatif** | **14,1** (Tinggi) | **$r = -0.713$** terhadap Neraca Air | Hujan lebat selalu beriringan dengan tutupan awan tebal dan reduksi radiasi fotosintesis aktif. |
| **Frekuensi Hari Hujan Lebat** | **8,5** (Moderat) | **$r = +0.925$** terhadap Neraca Air | Indikator frekuensi lebih tahan terhadap outlier ekstrem dibanding volume total. |

---

## 3. Implikasi Metodologis Phase 8
1. **Larangan Regresi OLS Multivariat Tanpa Kontrol**: Penggunaan seluruh fitur cuaca secara simultan dalam model linier biasa akan memicu *severe multicollinearity*, mengakibatkan koefisien meledak dengan tanda acak (*wrong sign paradox*).
2. **Kewajiban Regularisasi L1/L2**: Model prediktif yang dibangun di Phase 9 wajib menggunakan regularisasi penyusutan parameter (Ridge $L_2$, Lasso $L_1$, atau Elastic Net) untuk meredam inflasi varians koefisien.
