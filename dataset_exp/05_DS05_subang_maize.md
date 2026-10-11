# 🌽 DS05 — Produktivitas Jagung Jawa Barat & Analisis Tren Kabupaten Subang

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS05_subang_maize_productivity`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18104_produktivitas_jagung_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV & JSON di `data/raw/DS05_subang_maize_productivity/`
* **Ukuran Total:** ~14 KB (216 baris lengkap, 0 missing value)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **27 Kabupaten/Kota Se-Jawa Barat** (dengan audit mendalam pada Kabupaten Subang).
* **Rentang Waktu:** 8 Tahun Penuh (**2015 s.d. 2022**).
* **Frekuensi:** Tahunan agregat.
* **Satuan Ukuran:** **KUINTAL / HEKTAR** ($1\text{ ku} = 100\text{ kg} = 0.1\text{ ton}$).

---

## 3. Kamus Data & Struktur Kolom Aktual

| Nama Kolom Aktual | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer | ID unik record sistem Galura |
| `kode_provinsi` | Integer | `32` (Jawa Barat) |
| `nama_provinsi` | String | `JAWA BARAT` |
| `kode_kabupaten_kota` | Integer | `3213` (Kabupaten Subang), dll. |
| `nama_kabupaten_kota` | String | `KABUPATEN SUBANG`, `KABUPATEN GARUT`, dll. |
| `produktivitas_jagung` | Float | Hasil panen per hektar (Kuintal/Ha) |
| `satuan` | String | `KUINTAL/HEKTAR` |
| `tahun` | Integer | Tahun observasi (2015 s.d. 2022) |

---

## 4. Bedah Kasus Empiris: Anomali Subang & Detrending Jagung (Audit B2)

### A. Runtun Waktu Asli Produktivitas Jagung Subang (2015–2022)
* **2015:** 45,75 ku/ha
* **2016:** 51,53 ku/ha ($+12,6\%$)
* **2017:** 50,64 ku/ha ($-1,7\%$)
* **2018:** 51,38 ku/ha ($+1,5\%$)
* **2019:** 56,41 ku/ha ($+9,8\%$)
* **2020:** 57,23 ku/ha ($+1,5\%$)
* **2021:** **68,20 ku/ha** ($+19,2\%$) $\rightarrow$ lonjakan tajam
* **2022:** **89,49 ku/ha** ($+31,2\%$) $\rightarrow$ lonjakan kedua
* **Total Kenaikan 2 Tahun (2020 ke 2022):** $+56,4\%$!

### B. Posisi Subang sebagai Outlier Lokal (Bukan Fenomena Provinsi)
Audit tren lintas 27 kabupaten membuktikan bahwa lonjakan Subang adalah **anomali lokal idiosinkratik**:
* Slope Subang: **$+4,933\text{ ku/ha/tahun}$** ($R^2 = 0,739$).
* Mayoritas sentra produksi jagung utama Jawa Barat justru memiliki tren **datar atau menurun**:
  * Kab. Cirebon: $-1,25\text{ ku/ha/thn}$ (rata-rata 75,5 ku/ha)
  * Kab. Kuningan: $-1,54\text{ ku/ha/thn}$ (rata-rata 69,4 ku/ha)
  * Kab. Cianjur: $-1,86\text{ ku/ha/thn}$ (rata-rata 71,1 ku/ha)
  * Kab. Indramayu: $-2,03\text{ ku/ha/thn}$ (rata-rata 68,6 ku/ha)
  * Kab. Garut: $-1,20\text{ ku/ha/thn}$

### C. Standardisasi Definisi CV Residual & Atribusi Cuaca
* **Definisi Koefisien Variasi Residual Subang:**
  * Populasi ($\text{ddof}=0$): $\text{CV}_{\text{pop}} = \frac{\sigma_0(e)}{\bar{y}} = \mathbf{11,42\%}$
  * Sampel ($\text{ddof}=1$): $\text{CV}_{\text{sample}} = \frac{\sigma_1(e)}{\bar{y}} = \mathbf{12,21\%}$
  * OLS Degree of Freedom ($N-2$): $\text{CV}_{\text{OLS}} = \frac{\sqrt{\frac{\sum e^2}{N-2}}}{\bar{y}} = \mathbf{13,19\%}$
  * *Standar yang diadopsi proyek*: Menggunakan $\text{CV}_{\text{sample}}$ ($\text{ddof}=1$) sebesar **$12,21\%$**.
* **Batas Atas Sinyal Cuaca**: Variasi residual $\approx 12,2\%$ merupakan **batas atas variasi yang berpotensi dijelaskan oleh cuaca**. Angka ini mencakup derau pengukuran ubinan, fluktuasi serangan hama/penyakit, dinamika harga input/pupuk, dan variasi manajemen petani.
* **Status Atribusi Metodologi BPS KSA Jagung**: Transisi metodologi survei ubinan BPS ke Kerangka Sampel Area (KSA) untuk komoditas jagung berstatus **HIPOTESIS BELUM TERKONFIRMASI** (BPS secara nasional baru mempublikasikan rilis resmi KSA Jagung pada periode pilot 2020–2022).
* **Penjelasan Angka Panel $R^2 = 0,640$ dan $32,74\%$**: Model regresi panel (Kabupaten FE + Tren Linier Provinsi) menyerap variasi cross-sectional level dan tren makro dengan $R^2 = 0,640$, menyisakan residual variasi bersih tingkat provinsi sebesar $32,74\%$ (didominasi variasi unit-unit perkotaan non-sentra).

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
import numpy as np
from pathlib import Path

csv_path = Path("data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv")
df = pd.read_csv(csv_path)

subang = df[df['nama_kabupaten_kota'] == 'KABUPATEN SUBANG'].sort_values('tahun')
x = subang['tahun'].values
y = subang['produktivitas_jagung'].values

# Estimasi Tren Linier OLS
slope, intercept = np.polyfit(x, y, 1)
y_pred = slope * x + intercept
residuals = y - y_pred
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1 - (ss_res / ss_tot)

mean_y = np.mean(y)
cv_ddof0 = (np.std(residuals, ddof=0) / mean_y) * 100
cv_ddof1 = (np.std(residuals, ddof=1) / mean_y) * 100

print(f"Slope Subang    : +{slope:.3f} ku/ha/tahun")
print(f"R² OLS Tren     : {r2:.4f}")
print(f"CV Residual (ddof=0): {cv_ddof0:.2f}%")
print(f"CV Residual (ddof=1): {cv_ddof1:.2f}%")
```
