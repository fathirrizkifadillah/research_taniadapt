# Log Rekonsiliasi & Resolusi Inkonsistensi Internal (TaniAdapt Audit v2)

Dokumen ini mencatat seluruh inkonsistensi numerik, kontradiksi naratif, dan artefak data yang ditemukan oleh review independen di seluruh repositori TaniAdapt, beserta resolusi matematis yang dihitung ulang langsung dari data mentah (*raw source extracts*).

> **Aturan Keras No. 7**: Jika dua dokumen atau notebook menyebut angka berbeda, jangan pilih salah satu secara diam-diam. Catat di `log_inkonsistensi.md` lalu selesaikan dengan menghitung ulang dari data mentah menggunakan script di `scripts/`.

---

## 1. Item A1 — Rekonsiliasi Padi B1: Dua Versi Angka BPS & Artefak GKP 2019

### A. Inkonsistensi Ditemukan
1. **Angka BPS 2015–2017 Berbeda di Notebook vs Laporan**:
   - Notebook 03 memplot angka BPS: `~56.20, 56.40, 56.60 ku/ha` (rasio Galura/BPS 1.071, 1.056, 1.015).
   - Tabel laporan dan `b1_rice_full_ratio_audit.csv` memakai: `60.19, 59.58, 57.47 ku/ha` (rasio tepat 1.000, terindikasi sirkular karena sama persis dengan rata-rata tanpa bobot DS03).
2. **Lonjakan Padi Sawah 2019**:
   - Angka Galura DS03 2019 tercatat `63.80 ku/ha`, sedangkan BPS KSA resmi adalah `52.38 ku/ha` (rasio melonjak drastis ke 1.2181 / +21.8%).
3. **Anomali Padi Ladang 2019**:
   - Hasil padi ladang melonjak +55.1% (dari 41.51 ku/ha menjadi 64.39 ku/ha), jauh melampaui faktor konversi kadar air ubinan (1.188).

### B. Investigasi & Bukti Data Mentah
- **Script**: `scripts/audit_b1_rice_reconciliation_v2.py`
- **Output**: `reports/dataset_audit/b1_rice_reconciliation_v2.csv`
- **Temuan**:
  1. Angka `56.20, 56.40, 56.60 ku/ha` di notebook adalah *placeholder* tidak berdasar sumber resmi.
  2. Angka `60.19, 59.58, 57.47 ku/ha` adalah rata-rata aritmatika tanpa bobot dari 27 unit DS03.
  3. Angka resmi BPS Jawa Barat dalam publikasi *Provinsi Jawa Barat Dalam Angka 2016–2018* adalah: **61.22 ku/ha (2015), 60.49 ku/ha (2016), dan 58.87 ku/ha (2017)**.
  4. Ketika data mentah DS03 dihitung menggunakan **rata-rata berbobot luas panen (area-weighted mean)**:
     - 2015: $61.22\text{ ku/ha}$ (Selisih ke BPS: **0.00%**)
     - 2016: $60.49\text{ ku/ha}$ (Selisih ke BPS: **0.00%**)
     - 2017: $58.87\text{ ku/ha}$ (Selisih ke BPS: **0.00%**)
     - **Resolusi**: DS03 2015–2017 cocok 100.0% dengan BPS resmi pre-KSA jika dan hanya jika dibobotkan dengan luas panen.
  5. Lonjakan padi ladang (+55.1%) pada 2019 terbukti akibat pencampuran pelaporan administratif (*reporting error*), bukan faktor biologis atau kadar air.
  6. Karena angka BPS KSA per kabupaten/kota 2018–2020 tidak tersedia publik, padi 2018–2020 **dikeluarkan dari panel regresi utama**.

---

## 2. Item A2 — Rekonsiliasi Presipitasi B3: Narasi AgERA5 vs CHIRPS

### A. Inkonsistensi Ditemukan
1. Notebook 09 mengklaim rasio AgERA5/CHIRPS `0.92–1.08` dan korelasi $r = 0.91$ untuk Tasikmalaya/Subang/Garut. Namun tabel audit menunjukkan bias Garut $+16\%\text{ s.d. }+38\%$ dan Tasikmalaya $-5\%\text{ s.d. }-22\%$.
2. Narasi menyebut "Rata-rata CHIRPS 10 tahun Tasikmalaya 4.466 mm", padahal file hanya mencakup 3 tahun (2016, 2020, 2024).
3. Peringkat wilayah terbasah bertentangan: AgERA5 menempatkan Garut (4.425 mm) dan Cimahi/Bandung Barat (4.357 mm) di puncak, sementara narasi menyebut "Tasikmalaya, Sukabumi, Garut".

### B. Investigasi & Bukti Data Mentah
- **Script**: `scripts/audit_b3_rainfall_bias_chirps_v2.py`
- **Output**: `reports/dataset_audit/b3_rainfall_bias_chirps_audit_v2.csv` (27 unit)
- **Temuan**:
  1. Angka 4.465,7 mm ($\approx 4.466\text{ mm}$) Tasikmalaya adalah **rata-rata 3 tahun benchmark (2016, 2020, 2024)**, bukan 10 tahun. Label diperbaiki resmi.
  2. Nilai $r = 0.91$ muncul dari korelasi presipitasi bulanan mentah yang terdistorsi oleh siklus tahunan bersama (musim hujan vs kemarau). Ketika dievaluasi menggunakan **anomali bulanan bebas musim (*deseasonalized z-score*)**, korelasi Pearson berada di kisaran **$r = 0.50\text{ s.d. }0.80$ (median 0.73)**.
  3. AgERA5 mengalami **bias overestimasi orografis tajam di Bandung Raya**:
     - Kota Cimahi: $+61.56\%$ bias tahunan ($+67.15\%$ di Musim Hujan)
     - Kab. Bandung: $+45.28\%$ bias tahunan ($+72.31\%$ di Musim Hujan)
     - Kab. Bandung Barat: $+33.48\%$ bias tahunan.
  4. Sebaliknya, CHIRPS menempatkan Kab. Bogor (5.176,8 mm) dan Kota Bogor (4.778,2 mm) sebagai wilayah terbasah di Jawa Barat, di mana AgERA5 mengalami underestimasi sebesar $-34\%\text{ s.d. }-39\%$.
  5. Korelasi elevasi DEM dengan signed bias tahunan bernilai positif kuat ($r = +0.631$), membuktikan model numerik ECMWF melebih-lebihkan hujan di dataran tinggi Jawa Barat.
  6. Nama kolom `stasiun` dibakukan menjadi `lokasi`.

---

## 3. Item A3 — Tahun 2022 Jagung dan Kedelai: Dugaan Imputasi Seragam

### A. Inkonsistensi Ditemukan
- Pada tahun 2022, 13 kabupaten/kota memiliki nilai yield jagung yang persis identik: **75.70 ku/ha**.
- Pada tahun 2022, standar deviasi spasial yield kedelai di seluruh 27 unit menyusut drastis ke **0.19 ku/ha** (nilai median 14.30 ku/ha).

### B. Investigasi & Keputusan
- Fenomena identitas absolut ini tidak mungkin merupakan hasil observasi lapangan independen dan mencerminkan imputasi rata-rata provinsi oleh dinas.
- Karena BPS belum menerbitkan data KSA per kabupaten yang memverifikasi angka ini, **tahun 2022 resmi ditandai sebagai `SUSPECT` di seluruh repositori**.
- Tahun 2022 dieksklusikan dari panel utama jagung dan kedelai (hanya disertakan dalam analisis sensitivitas).

---

## 4. Item A4 — Subang Jagung: Perbedaan Angka CV Residu

### A. Inkonsistensi Ditemukan
- Beredar dua angka CV residu: **11.42%** (di matriks linking dan audit summary) vs **12.21%** (di grafik dan laporan).
- Muncul klaim bahwa "anomali cuaca tidak bisa menjelaskan >12.2% fluktuasi produksi jagung".

### B. Resolusi Teknis
- **Script**: `scripts/audit_a4_subang_detrending_sensitivity.py`
- **Output**: `reports/dataset_audit/a4_subang_detrending_sensitivity.csv`
- **Definisi Dibakukan**:
  - $\text{CV}_{\text{ddof}=0} = \mathbf{11.42\%}$ (Standar deviasi populasi, pembagi $N=8$).
  - $\text{CV}_{\text{ddof}=1} = \mathbf{12.21\%}$ (Standar deviasi sampel, pembagi $N-1=7$).
  - $\text{CV}_{\text{OLS}} = \mathbf{13.19\%}$ (Root Mean Squared Error regresi tren linear OLS, pembagi $N-2=6$).
- Titik outlier 2022 menyumbang **49.8%** dari total kuadrat residual. Tanpa tahun 2022, CV residu menyusut tajam menjadi **5.49%** (linear) dan **2.65%** (piecewise structural break).
- Klaim "cuaca tidak bisa menjelaskan >12.2%" dihapus permanen karena cacat logika (residu mencakup cuaca, noise pengukuran, perubahan metode, dan non-linearitas). Diganti: *"residu detrended, bukan batas atas efek cuaca"*.

---

## 5. Item A5 — Hubungan DS08 vs DS05 (Subang): Yield vs Luas Panen

### A. Inkonsistensi Ditemukan
- DS08 menyatakan hasil panen Subang stagnan dan lonjakan produksi 98.4% didorong oleh luas panen. Namun narasi DS05 menyebut yield Subang melompat dari 45.7 ke 89.5 ku/ha.

### B. Resolusi Dekomposisi Log
- Menggunakan identitas multiplikatif exact: $\ln(\text{Produksi}) = \ln(\text{Luas}) + \ln(\text{Yield})$ $\rightarrow$ $\Delta \ln(\text{Prod}) = \Delta \ln(\text{Area}) + \Delta \ln(\text{Yield})$.
- Pada lonjakan produksi 2018 (+144.9% log-diff) dan 2020 (+109.1% log-diff), komponen luas panen menyumbang **98.4% s.d. 98.7%** dari total perubahan produksi logaritmik.
- Dikonfirmasi bahwa seri yield di DS05 dihitung langsung dari $\text{Produksi} \times 10 / \text{Luas}$, sehingga "uji identitas produksi" adalah **tautologi akuntansi (*accounting identity*)**, bukan temuan independen.

---

## 6. Item A6 — Hortikultura IFWC & Koreksi Label CV Cabai

### A. Inkonsistensi Ditemukan
1. Penggunaan ambang absolut $T_{\min} - T_d \le 2.0^\circ\text{C}$ dengan label "DITERIMA / DITOLAK".
2. Label grafik cabai menuliskan `Cabai Rawit (CV ~ 28%)` dan `Cabai Besar (CV ~ 31%)`, padahal seri yang diplot berkisar antara 117–146 ku/ha.
3. Periode DS06 disebut 2016, 2017, dan 2025 di dokumen yang berbeda.

### B. Resolusi Empiris
- **Script**: `scripts/clean_notebook_06.py`
- Ambang absolut 2.0°C dan label DITERIMA/DITOLAK dihapus. Digantikan oleh **Persentil ke-10 ($P_{10}$)** depresiasi titik embun per sel per bulan kalender.
- Keterbatasan ketidakcocokan waktu (*timing mismatch*) antara $T_{\min}$ fajar vs $T_d$ rata-rata harian 24-jam dicatat secara jujur.
- Perhitungan CV empiris sejati ($SD / Mean \times 100\%$):
  - **Cabai Besar (2017–2024, N=8)**: Mean 136.99 ku/ha, SD 6.15 ku/ha $\rightarrow$ **CV = 4.49%** (bukan 31%).
  - **Cabai Rawit (2017–2024, N=8)**: Mean 126.13 ku/ha, SD 7.20 ku/ha $\rightarrow$ **CV = 5.71%** (bukan 28%).
- Periode valid DS06 tingkat provinsi ditetapkan: **2017–2024 ($N = 8$)**. Data `od_18096` hanya tersedia untuk 2013–2014 (zero overlap dengan AgERA5).

---

## 7. Item A7 — DS04 Titik Grid & Ambang CDD

### A. Inkonsistensi Ditemukan
- Jumlah titik Jawa Barat disebut berbeda: 14 titik vs 12 titik.
- Grafik memakai ambang hari kering absolut `CDD > 30` dan `CDD > 60 hari`.

### B. Resolusi Spasial
- **Script**: `scripts/clean_notebook_04.py`
- Tepat **12 titik grid** berada secara ketat di dalam poligon resmi batas wilayah Jawa Barat (`jawa_barat_provinsi.geojson`). Angka 14 titik muncul dari rectangular bounding box kasar `[-8.0, -5.8] x [106.3, 109.0]`, di mana 2 titik di bujur 109.0°E jatuh di Jawa Tengah. Standar yang dibakukan adalah **12 titik poligon resmi**.
- Ambang absolut 30 dan 60 hari dihapus; diganti persentil empiris $P_{50}, P_{75}, P_{90}$.
- Sirkularitas fisik dengan AgERA5 (keduanya turunan ERA5) dicatat secara eksplisit.

---

## 8. Item A8 — Duplikasi Sel Grid AgERA5 & Koordinat Subang

### A. Inkonsistensi Ditemukan
- Pasangan kota/kabupaten berbagi sel cuaca yang sama. Koordinat Subang berbeda antar dokumen.

### B. Resolusi
- **Script**: `scripts/audit_a8_spatial_grid_cells.py`
- Dari 27 unit administratif, terdapat tepat **25 sel grid AgERA5 unik**.
- Duplikasi sel HANYA terjadi pada:
  1. Kab. Bogor dan Kota Bogor (sel $-6.60^\circ, 106.80^\circ$)
  2. Kab. Cirebon dan Kota Cirebon (sel $-6.70^\circ, 108.60^\circ$).
- Seluruh 18 kabupaten sentra Tier A memiliki sel grid 100% independen ($N_{\text{eff}} = 18$).
- Koordinat Subang dibakukan tunggal:
  - **Centroid Poligon Resmi**: Lintang $-6.4830^\circ$, Bujur $107.7322^\circ$
  - **Sel Grid AgERA5**: $-6.50^\circ, 107.70^\circ$
  - **Elevasi DEM**: $49.0\text{ meter dpl}$.

---

## 9. Item A9 — Definisi Sentra Kedelai & Baris Panel

### A. Inkonsistensi Ditemukan
- Jumlah sentra kedelai disebut 14 (di Notebook 07) vs 17 (di `hypotheses.md`).
- Disebut "216 baris", padahal banyak nilai 0 atau NaN di wilayah perkotaan.

### B. Resolusi Kriteria Ex Ante
- Total baris teoretis adalah 216 ($27 \times 8$). Baris observasi valid (yield $> 0$) adalah **156 baris untuk kedelai** dan **181 baris untuk jagung**.
- Kriteria Ex Ante Sentra Kedelai: Unit berstatus KABUPATEN yang memiliki catatan produktivitas $> 0$ minimal 6 dari 8 tahun ($N \ge 6$).
- Di bawah kriteria ini, terdapat tepat **17 kabupaten sentra kedelai** (13 kabupaten memiliki $N=8$, 4 kabupaten memiliki $N=6\text{--}7$). Definisi panel seimbang ketat ($N=8$, mencakup kota) menghasilkan 14 unit.
