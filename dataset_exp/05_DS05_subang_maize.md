# 🌽 DS05 — Produktivitas Jagung Jabar & Analisis Kabupaten Subang

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS05_subang_maize_productivity`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18104_produktivitas_jagung_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV & JSON di `data/raw/DS05_subang_maize_productivity/`
* **Ukuran Total:** ~16 KB (216 baris lengkap, 0 missing value)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **27 Kabupaten/Kota Se-Jawa Barat** (dengan fokus investigasi mendalam pada Kabupaten Subang).
* **Rentang Waktu:** 8 Tahun Penuh (**2015 s.d. 2022**).
* **Frekuensi:** Tahunan agregat.
* **Satuan Ukuran:** **KUINTAL / HEKTAR** (1 Kuintal = 100 kg = 0.1 Ton).

---

## 3. Kamus Data & Struktur Kolom

| Nama Kolom | Tipe Data | Deskripsi & Nilai Contoh |
| :--- | :--- | :--- |
| `id` | Integer | ID unik record sistem. |
| `kode_provinsi` | Integer | `32` (Jawa Barat). |
| `nama_provinsi` | String | `JAWA BARAT`. |
| `kode_kabupaten_kota` | Integer | `3213` (Kabupaten Subang), dll. |
| `nama_kabupaten_kota` | String | `KABUPATEN SUBANG`, `KABUPATEN GARUT`, dll. |
| `produktivitas_jagung` | Float | Angka hasil panen per hektar (Kuintal/Ha). |
| `satuan` | String | `KUINTAL/HEKTAR`. |
| `tahun` | Integer | Tahun observasi (2015 s.d. 2022). |

---

## 4. Bedah Kasus Empiris: Anomali & Detrending Jagung Subang

Kabupaten Subang dipilih sebagai fokus utama komoditas jagung karena merupakan salah satu sentra jagung pantura. Namun, audit empiris menemukan dinamika khusus yang wajib dipahami:

### A. Runtun Waktu Asli Produktivitas Jagung Subang (2015–2022)
* **2015:** 45.75 Ku/Ha
* **2016:** 51.53 Ku/Ha ($+12.6\%$)
* **2017:** 50.64 Ku/Ha ($-1.7\%$)
* **2018:** 51.38 Ku/Ha ($+1.5\%$)
* **2019:** 56.41 Ku/Ha ($+9.8\%$)
* **2020:** 57.23 Ku/Ha ($+1.5\%$)
* **2021:** **68.20 Ku/Ha** ($\mathbf{+19.2\%}$) $\rightarrow$ Awal lonjakan tajam
* **2022:** **89.49 Ku/Ha** ($\mathbf{+31.2\%}$) $\rightarrow$ Lonjakan ekstrem kedua
* **Total Kenaikan 2 Tahun (2020 ke 2022):** Melonjak **$+56.4\%$**!

### B. Resolusi Bug Formula OLS ($R^2 = 1.000 \rightarrow 0.739$)
* **Penyebab Bug Sebelumnya:** Script audit awal menulis `ss_res = np.sum((y - y_pred)) ** 2`. Tanda kuadrat di luar `sum` menyebabkan $(\sum e_i)^2 = 0^2 = 0$ (karena jumlah residual OLS selalu 0), sehingga $R^2 = 1 - 0 = 1.000$.
* **Angka OLS Sebenarnya yang Benar:**
  * **$R^2 = 0.7387 \approx 0.739$**
  * **Slope Kenaikan Linier:** $+4.933\text{ ku/ha/tahun}$ (rata-rata 27 kabupaten Jabar hanya $+1.633\text{ ku/ha/tahun}$). Kenaikan Subang **3x lebih cepat** dari provinsi.
  * **CV Mentah (Sebelum Detrending):** $22.35\%$
  * **CV Residual (Setelah Detrending):** **$11.42\%$**

### C. Makna Agronomis & Metodologis bagi TaniAdapt
1. **Sinyal Cuaca Berada di Residu:** Variasi sebesar $11.42\%$ residual itulah yang sesungguhnya dipengaruhi fluktuasi cuaca tahunan (hujan, radiasi, suhu). Kenaikan masif sisanya adalah faktor non-cuaca (teknologi benih hibrida, perluasan lahan program pemerintah, dan perubahan metodologi survei BPS KSA Jagung yang dimulai tahun 2020).
2. **Kewajiban Detrending:** Model prediksi TaniAdapt **tidak boleh melatih data mentah tanpa detrending**, karena model akan salah mengatribusikan kenaikan teknologi sebagai pengaruh cuaca.
3. **Metode Detrending Terpilih:** Metode **Kabupaten Fixed Effects + Provincial Linear Trend** menghasilkan $R^2 = 0.640$ dan menyisakan residual variasi bersih $32.74\%$ di tingkat panel provinsi.

---

## 5. Cuplikan Kode Python

```python
import pandas as pd
import numpy as np
from pathlib import Path

csv_path = Path("data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv")
df = pd.read_csv(csv_path)

subang = df[df['nama_kabupaten_kota'] == 'KABUPATEN SUBANG'].sort_values('tahun')
x = subang['tahun'].values
y = subang['produktivitas_jagung'].values

# OLS Fit
slope, intercept = np.polyfit(x, y, 1)
y_pred = slope * x + intercept
residuals = y - y_pred
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1 - (ss_res / ss_tot)

print(f"Slope Subang : +{slope:.3f} ku/ha/thn")
print(f"R² OLS       : {r2:.4f}")
print(f"CV Residual  : {np.std(residuals)/np.mean(y)*100:.2f}%")
```
