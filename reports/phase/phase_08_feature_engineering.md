# TaniAdapt Research Dossier — Phase 8: Feature Engineering

**Status**: COMPLETED  
**Ruang Lingkup**: Transformasi data cuaca harian 65.754 baris (2015–2024) menjadi feature store agrometeorologi terstruktur.

---

## 1. Rekayasa Fitur Waktu & Indeks Ekstrem
1. **Fitur Lag & Rolling Window**: Perhitungan lag temporal harian (1 s/d 14 hari) dan jendela bergerak kumulatif (7, 14, 21, dan 30 hari).
2. **Indeks Iklim Ekstrem**:
   * *Consecutive Dry Days (CDD)*: Hari kering berturut-turut ($P < 1.0\text{ mm}$).
   * *Consecutive Wet Days (CWD)*: Hari basah berturut-turut ($P \ge 1.0\text{ mm}$).
   * *Diurnal Temperature Range (DTR)*: $T_{\max} - T_{\min}$.
3. **Indikator Biofisik Terintegrasi**:
   * *Vapor Pressure Deficit (VPD)*: Defisit tekanan uap jenuh udara.
   * *Neraca Air Biofisik ($P - ET_0$)*: Keseimbangan antara suplai hujan dengan penguapan acuan Penman-Monteith.

---

## 2. Temuan Multikolinearitas Ekstrem (VIF)
Analisis diagnostik kolinearitas menemukan masalah serius pada data agrometeorologi tropis:
* Korelasi antara total curah hujan dengan defisit lengas air mencapai **$r = +0.996$**.
* Nilai Variance Inflation Factor (VIF) untuk defisit air mencapai **$4.312,9$** dan curah hujan musiman mencapai **$3.704,6$** (jauh melampaui batas aman VIF $< 10$).
* **Implikasi Metodologis**: Melarang penggunaan model regresi multivariat tanpa regularisasi (L1/L2), karena multikolinearitas ekstrem akan memicu koefisien meledak dan bertanda tidak masuk akal.
