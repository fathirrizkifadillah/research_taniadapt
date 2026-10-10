# 🌾 DS02 — Bangladesh Rice Panel Dataset

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS02_bangladesh_rice_panel`
* **Nama Resmi:** Growing Season Climate and Rice Yield Panel for Bangladesh Districts
* **Penerbit / Institusi:** Mendeley Data / Bangladesh Rice Research Institute (BRRI) & Bangladesh Meteorological Department (BMD)
* **DOI:** `10.17632/m44r329k8h.1`
* **Lisensi:** CC BY 4.0
* **Format File Lokal:** CSV hasil ekstraksi arsip ZIP resmi (`data/raw/DS02_bangladesh_rice_panel/`)
* **Ukuran Total:** ~84 KB

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** 64 Distrik di seluruh Bangladesh.
* **Rentang Waktu:** 10 Tahun (**2015 s.d. 2024**).
* **Frekuensi:** Panel tahunan per musim tanam (*season-specific panel*).

---

## 3. Kamus Data & Dekomposisi 3 Musim Tanam Padi

Dataset ini memisahkan hasil panen dan indikator cuaca menurut tiga musim fenologi padi tropis:

| Musim Tanam | Karakteristik Agroklimat | Periode Tanam - Panen | Variabel Utama |
| :--- | :--- | :--- | :--- |
| **Aus** | Pra-Muson / Hujan Awal | April s.d. Juli / Agustus | Curah hujan awal, suhu tinggi, variasi hasil moderat. |
| **Aman** | Muson Utama (Rainfed Wetland) | Juli / Agustus s.d. November / Desember | Curah hujan lebat muson, genangan air, sensitif thd kekeringan akhir fase bunting. |
| **Boro** | Musim Kemarau (Dry Season Irrigated) | Desember / Januari s.d. April / Mei | Suhu dingin saat bibit, radiasi tinggi, ketergantungan 100% pada irigasi sumur. |

### Kolom-Kolom Utama di Tabel:
* `district_name` / `district_id`: Kunci entitas spasial (64 distrik).
* `year`: Tahun panen (2015–2024).
* `season`: Kategori musim (`Aus`, `Aman`, `Boro`).
* `rice_yield`: Produktivitas panen padi (Metrik Ton per Hektar).
* `season_rainfall_sum`: Total curah hujan kumulatif selama musim tanam berlangsung (mm).
* `season_tmean`: Suhu udara rata-rata selama musim tanam (°C).
* `season_tmax_extreme_days`: Jumlah hari dengan suhu ekstrem panas di atas batas kritis pembungaan (>35°C).

---

## 4. Status Audit Metodologi & Peran di TaniAdapt

> [!IMPORTANT]
> **BUKAN DATA LOKAL JAWA BARAT:** Dataset ini tidak digunakan untuk melatih model prediksi hasil panen Jawa Barat karena geografi dan varietas padi lokal yang berbeda.

### Peran Kunci di TaniAdapt:
1. **Benchmark Model Ekonometrik Panel:** Menjadi acuan pembuktian matematis bahwa regresi panel cuaca-tanaman wajib menggunakan **Two-Way Fixed Effects (Entity FE + Time FE)**:
   $$\text{Yield}_{it} = \alpha_i + \lambda_t + \beta \cdot \text{Weather}_{it} + \epsilon_{it}$$
   * Entity FE ($\alpha_i$) menyerap karakteristik tanah, topografi, dan tradisi lokal distrik.
   * Time FE ($\lambda_t$) menyerap shock makro nasional (seperti El Niño/La Niña nasional atau inflasi harga pupuk).
2. **Pelajaran Dekomposisi Musiman:** Membuktikan bahwa menggabungkan data hasil panen menjadi 1 angka tahunan (seperti yang terjadi di DS03 Padi Jabar) menghilangkan sinyal cuaca musiman.

---

## 5. Cuplikan Kode Python

```python
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/DS02_bangladesh_rice_panel/extracted")
# Membaca data panel distrik
csv_files = list(raw_dir.glob("*.csv"))
if csv_files:
    df = pd.read_csv(csv_files[0])
    print("Dimensi Data:", df.shape)
    print("Kolom:", df.columns.tolist()[:8])
    display(df.head())
```
