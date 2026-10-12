# TaniAdapt Research Dossier — Phase 9: ML Baseline Benchmarking

**Status**: COMPLETED  
**Ruang Lingkup**: Pelatihan dan evaluasi 6 model prediktif pada panel jagung 18 sentra ($N=124$) menggunakan validasi temporal out-of-sample Leave-One-Year-Out (LOYO) dan uji falsifikasi placebo.

---

## 1. Komparasi Performa Model Prediktif

| Arsitektur Model | In-Sample Fit ($R^2_{\text{train}}$) | Out-of-Sample ($R^2_{\text{LOYO}}$) | Galat Prediksi (LOYO RMSE) | Galat Prediksi (LOYO MAE) | Evaluasi Ilmiah |
|---|:---:|:---:|:---:|:---:|---|
| **1. Pooled OLS (Two-Way FE)** | $0.158$ | **$-0.113$** | $0.614$ | $0.334$ | Gagal generalisasi; lebih buruk dari prediksi rata-rata konstan. |
| **2. WLS (Bobot Luas Panen)** | $0.158$ | **$-0.113$** | $0.614$ | $0.334$ | Pembobotan luas panen tidak memperbaiki akurasi out-of-sample. |
| **3. Ridge Regression ($L_2$)** | $0.150$ | **$-0.041$** | $0.594$ | $0.306$ | Meredam varians ekstrim, namun $R^2$ out-of-sample tetap negatif. |
| **4. Lasso Regression ($L_1$)** | $0.091$ | **$-0.024$** | $0.589$ | $0.263$ | Menghasilkan MAE terendah dengan seleksi fitur sparse. |
| **5. Elastic Net ($L_1+L_2$)** | $0.126$ | **$-0.032$** | $0.591$ | $0.284$ | Meredam multikolinearitas VIF, namun sinyal cuaca tetap tidak prediktif. |
| **6. Random Forest (Shallow)** | **$0.389$** | **$+0.034$** | **$0.572$** | **$0.261$** | Overfitting tajam ($R^2$ anjlok dari $0.389 \to 0.034$); daya prediksi nol. |

---

## 2. Kesimpulan Ilmiah Phase 9
* Seluruh model mengalami keruntuhan performa saat diuji pada tahun baru ($R^2_{\text{LOYO}} \approx 0$).
* Uji falsifikasi placebo cuaca masa depan ($t+1$) menunjukkan korelasi tidak signifikan ($p > 0.40$).
* Temuan ini membuktikan secara ilmiah bahwa model Machine Learning tidak mampu memprediksi yield tahunan dari data cuaca musiman, memvalidasi keputusan arsitektur TaniAdapt untuk beralih total ke **Decision Engine Biofisik Mekanistik FAO-56**.
