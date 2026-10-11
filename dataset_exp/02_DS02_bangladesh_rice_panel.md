# 🌾 DS02 — Bangladesh Rice Panel Dataset (Metodologi Replikasi)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS02_bangladesh_rice_panel`
* **Nama Resmi:** Replication Data for: Growing season climate and rice yield in Bangladesh (2015–2024 Audited Panel)
* **Penerbit / Institusi:** Mendeley Data / Audited Replication Panel
* **DOI Terverifikasi:** `10.17632/h94z4ftts2.1`
* **URL Resmi:** [Mendeley Data — Dataset h94z4ftts2](https://data.mendeley.com/datasets/h94z4ftts2/1)
* **Lisensi:** CC BY 4.0
* **Format File Lokal:** CSV hasil ekstraksi arsip ZIP resmi (`data/raw/DS02_bangladesh_rice_panel/extracted/...`)
* **Ukuran Total:** ~2.1 MB

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** 64 Distrik di seluruh Bangladesh.
* **Rentang Waktu:** 10 Tahun (**2015 s.d. 2024**).
* **Frekuensi:** Panel tahunan per musim tanam (*season-specific panel*: Aus, Aman, Boro).

---

## 3. Kamus Data & Variabel Kunci

Dataset memisahkan hasil panen dan indikator iklim muson menurut tiga musim fenologi padi tropis:
* **Aus**: Pra-Muson / Hujan Awal (April s.d. Juli).
* **Aman**: Muson Utama (Juli s.d. November/Desember).
* **Boro**: Musim Kemarau Beririgasi (Desember s.d. Mei).

### Kolom-Kolom Utama di File `Rice_Yield_2015_2024_Audited.csv`:
* `district_id` / `adm2_code`: ID administratif distrik.
* `district`: Nama distrik (64 entitas).
* `crop`: Varietas/musim padi (`Aus`, `Aman`, `Boro`).
* `crop_year`: Tahun panen (2015–2024).
* `yield_t_ha`: Produktivitas panen padi (Ton/Hektar).
* `area_ha`: Luas panen (Hektar).
* `production_mt`: Total produksi padi (Metrik Ton).
* `flag_neighbor_spike`: Bendera audit anomali lokal.

---

## 4. Status Audit Metodologi & Batasan Peran di TaniAdapt

> [!IMPORTANT]
> **BUKAN DATASET KEPUTUSAN JAWA BARAT**: Dataset ini tidak membuktikan performa model di Jawa Barat. Perannya terbatas sebagai **demonstrasi metodologis replikasi** atas arsitektur regresi panel ber-resolusi musim.

### Pembelajaran Metodologis:
1. **Pendekatan Panel Regression**: Menunjukkan pendekatan yang dipakai pada dataset ini, di mana kontrol terhadap heterogenitas spasial (*District Fixed Effects*) dan tren waktu (*Year Fixed Effects*) memisahkan variasi cuaca dari heterogenitas tanah dan manajemen.
2. **Pentingnya Resolusi Musiman**: Menunjukkan bahwa agregasi tahunan mentah (seperti pada data dinas lokal) menghapus variasi cuaca musiman yang berlawanan antara musim hujan dan musim kemarau.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

fpath = Path("data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/Rice_Yield_2015_2024_Audited.csv")
df = pd.read_csv(fpath)

# Filter musim panen Aman (muson utama)
df_aman = df[df['crop'] == 'Aman'].copy()

summary = df_aman.groupby('crop_year')['yield_t_ha'].agg(['count', 'mean', 'std']).reset_index()
print("Ringkasan Musim Aman Bangladesh (2015-2024):")
print(summary.head())
```
