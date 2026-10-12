# TaniAdapt Research Dossier — Phase 9: ML Baseline Benchmarking & LOYO Out-of-Sample Evaluation

**Status**: COMPLETED  
**Ruang Lingkup**: Benchmarking 6 Arsitektur Model Prediktif pada Panel Jagung 18 Sentra ($N=124$, 2015–2021)  
**Skema Validasi**: Leave-One-Year-Out (LOYO) Temporal Cross-Validation & Uji Falsifikasi Lead Cuaca ($t+1$)  
**Tujuan Ilmiah**: Menguji Apakah Kompleksitas Machine Learning Mampu Menghasilkan Daya Prediksi Out-of-Sample Bebas Kebocoran

---

## 1. Desain Eksperimen & 6 Model Prediktif yang Diuji
Untuk memastikan tidak terjadi kebocoran informasi temporal (*data leakage*), validasi silang acak (*random k-fold*) dilarang keras. Evaluasi diwajibkan menggunakan **Leave-One-Year-Out (LOYO) CV**: melatih model pada $T-1$ tahun dan menguji prediksi pada 1 tahun penuh yang belum pernah dilihat model:

1. **Pooled OLS (Two-Way FE Baseline)**: Model linier kuadrat terkecil standar.
2. **Weighted Least Squares (WLS)**: Model linier dengan pembobotan berdasarkan luas panen rata-rata kabupaten (2015–2017).
3. **Ridge Regression ($L_2$)**: Model linier dengan penalti kuadrat norma koefisien untuk meredam multikolinearitas ($lpha = 1.0$).
4. **Lasso Regression ($L_1$)**: Model linier dengan penalti nilai absolut norma koefisien untuk seleksi fitur sparse ($lpha = 0.05$).
5. **Elastic Net ($L_1 + L_2$)**: Model linier kombinasi penalti $L_1$ dan $L_2$ ($lpha = 0.05$, $l_1	ext{-ratio} = 0.5$).
6. **Random Forest Regressor**: Model ensemble non-linier berbasis pohon keputusan ($	ext{n\_estimators}=100$, $	ext{max\_depth}=3$, $	ext{min\_samples\_split}=5$, $	ext{random\_state}=42$).

---

## 2. Tabel Hasil Komparasi Performa Empiris (Phase 9 Benchmark)

| Arsitektur Model | In-Sample Fit ($R^2_{\text{train}}$) | Out-of-Sample ($R^2_{\text{LOYO}}$) | Galat Prediksi (LOYO RMSE) | Galat Prediksi (LOYO MAE) | Evaluasi Ilmiah & Karakteristik Model |
|---|:---:|:---:|:---:|:---:|---|
| **1. Pooled OLS (Two-Way FE)** | $0.158$ | **$-0.113$** | $0.614$ | $0.334$ | Gagal generalisasi total; nilai $R^2 < 0$ menunjukkan prediksi model lebih buruk dibanding menebak nilai rata-rata historis konstan. |
| **2. WLS (Bobot Luas Panen)** | $0.158$ | **$-0.113$** | $0.614$ | $0.334$ | Pembobotan luas panen tidak memberikan keuntungan prediksi out-of-sample; residual tetap didominasi variasi acak. |
| **3. Ridge Regression ($L_2$)** | $0.150$ | **$-0.041$** | $0.594$ | $0.306$ | Meredam varians ekstrim koefisien, namun daya prediksi out-of-sample tetap di bawah batas nol. |
| **4. Lasso Regression ($L_1$)** | $0.091$ | **$-0.024$** | $0.589$ | **$0.263$** | Memangkas fitur kolinear dan menghasilkan MAE terendah ($0.263$), namun $R^2$ mendekati nol. |
| **5. Elastic Net ($L_1 + L_2$)** | $0.126$ | **$-0.032$** | $0.591$ | $0.284$ | Kompromi L1/L2 meredam multikolinearitas VIF, namun sinyal cuaca tetap tidak mampu memprediksi yield tahun baru. |
| **6. Random Forest (Shallow)** | **$0.389$** | **$+0.034$** | **$0.572$** | $0.261$ | **Overfitting tajam di data latih ($R^2 = 0.389 	o 0.034$)**; model non-linier hanya menghafal noise sampel lokal. |

---

## 3. Uji Falsifikasi Placebo Cuaca Masa Depan ($t+1$)
Untuk memvalidasi apakah model ML menangkap sinyal kausal fisis nyata ataukah sekadar regresi ke nilai rata-rata:
* Dijalankan pengujian falsifikasi dengan mengganti fitur cuaca aktual dengan data cuaca $t+1$ (cuaca 1 tahun di masa depan).
* *Hasil*: Random Forest pada fitur placebo menghasilkan $R^2_{\text{LOYO}} = -0.052$ dengan $p > 0.40$ (tidak ada perbedaan kinerja signifikan secara statistik antara data cuaca nyata dan data cuaca acak masa depan).

---

## 4. Kesimpulan Saintifik & Justifikasi Arsitektur TaniAdapt
Temuan empiris Phase 9 memberikan konfirmasi ilmiah paling kuat bagi arah proyek TaniAdapt:
1. **Kegagalan Paradigma Prediksi Hasil Panen Berbasis Cuaca**: Tidak ada algoritma Machine Learning—baik linier, teratur, maupun pohon non-linier—yang mampu memprediksi variabilitas yield tahunan secara handal dari data cuaca musiman di Jawa Barat ($R^2_{\text{LOYO}} pprox 0$).
2. **Mengapa Petani Tidak Boleh Diberi Model ML Tebak-Hasil**: Fluktuasi hasil panen tahunan di lapangan didominasi oleh faktor bibit, dosis pupuk riil, serangan hama mikro, dan pencatatan administratif dinas, bukan oleh anomali cuaca makro.
3. **Peralihan Mutlak ke Decision Engine Mekanistik FAO-56**: Karena yield tidak dapat diprediksi secara statistik, TaniAdapt mengalihkan seluruh otak pengambil keputusan ke **hukum-hukum biofisik mekanistik deterministik (FAO-56 Penman-Monteith dan neraca lengas tanah harian)** untuk memandu keputusan operasional petani.
