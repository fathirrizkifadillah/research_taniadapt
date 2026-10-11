# 🌾 DS03 — Produktivitas Padi Jawa Barat (Open Data Jabar)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS03_west_java_rice_productivity`
* **Nama Sumber:** Satu Data Jawa Barat (Open Data Jabar / Galura API)
* **Dataset ID:**
  * Padi Total: `od_18103_produktivitas_padi_berdasarkan_kabupatenkota`
  * Padi Sawah: `od_18099_produktivitas_padi_sawah_berdasarkan_kabupatenkota`
  * Padi Ladang: `od_18102_produktivitas_padi_ladang_berdasarkan_kabupatenkota`
* **Penerbit:** Dinas Tanaman Pangan dan Hortikultura Provinsi Jawa Barat
* **Lisensi:** Open Data Pemerintah Provinsi Jawa Barat
* **Format File Lokal:** CSV dan JSON di `data/raw/DS03_west_java_rice_productivity/`
* **Ukuran Total:** ~11 KB per file

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** 27 Kabupaten/Kota di Provinsi Jawa Barat.
* **Rentang Waktu:** 6 Tahun (**2015 s.d. 2020**).
* **Frekuensi:** Tahunan (*annual aggregate*).
* **Jumlah Observasi:** 162 baris panel seimbang ($27 \text{ kab/kota} \times 6 \text{ tahun}$).

---

## 3. Kamus Data & Nama Kolom Aktual

| Nama Kolom Aktual | Tipe Data | Deskripsi | Catatan Kritis |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Kunci unik baris | Identitas sistem Galura |
| `kode_provinsi` | Integer | Kode BPS Jawa Barat (`32`) | Standar kemendagri/BPS |
| `nama_provinsi` | String | Nama Provinsi (`JAWA BARAT`) | Entitas ADM1 |
| `kode_kabupaten_kota`| Integer | Kode wilayah 27 Kab/Kota | Identitas ADM2 |
| `nama_kabupaten_kota`| String | Nama administratif Kab/Kota | Termasuk 18 Kabupaten & 9 Kota |
| `produktivitas_padi2` | Float | **Produktivitas Padi Total** | **Perhatian: Nama kolom berakhiran '2' di file total**; satuan kuintal/ha |
| `produktivitas_padi`  | Float | Produktivitas Padi Sawah / Ladang | Kolom di file sawah & ladang |
| `satuan` | String | Satuan pengukuran | `KUINTAL/HEKTAR` ($1\text{ ku} = 100\text{ kg} = 0.1\text{ ton}$) |
| `tahun` | Integer | Tahun pencatatan | 2015 s.d. 2020 |

---

## 4. Hasil Audit Kualitas Data (Blocker B1: Artefak Seri 2019/2020)

> [!CAUTION]
> **TEMUAN ARTEFAK SERI DATA (BLOCKER B1)**: 
> Data DS03 mencatat lonjakan produktivitas rata-rata provinsi dari **55,39 ku/ha (2018)** melonjak drastis ke **68,55 ku/ha (2019)** (+23,7% / log-diff +21,3%), lalu anjlok kembali ke **54,22 ku/ha (2020)** (-20,9%). Lonjakan ini terjadi **serentak di 27 dari 27 Kabupaten/Kota (100%)**.

### Bukti Pembuktian Artefak:
1. **Perbandingan dengan BPS Resmi KSA**: Data resmi BPS Jawa Barat (Berita Resmi Statistik No. 27/04/32/Th.XXIII dan No. 16/03/32/Th.XXIV) mencatat produktivitas padi riil:
   * **2018:** $56,51\text{ ku/ha}$
   * **2019:** $57,69\text{ ku/ha}$ (hanya naik $+2,09\%$, bukan $+23,7\%$)
   * **2020:** $56,82\text{ ku/ha}$ (hanya turun $-1,51\%$, bukan $-20,9\%$)
2. **Uji Rasio Konversi GKP vs GKG**: Rasio rata-rata DS03 terhadap BPS pada 2019 adalah **1,1882** (median 1,2196; std 0,0691) secara konstan lintas kabupaten. Rasio ~1,19 ini identik dengan faktor konversi Gabah Kering Panen (GKP) ke Gabah Kering Giling (GKG).
3. **Kesimpulan**: Seri tahun 2019 pada DS03 adalah **ARTEFAK DATA** (diduga pengisian data mentah GKP atau survei ubinan belum terkonversi pada portal Open Data Jabar).
4. **Koreksi Klaim $R^2$**: Klaim lama bahwa "$R^2 < 0.1$ membuktikan cuaca tidak memengaruhi hasil padi" dikoreksi. Nilai $R^2 = 0.054$ tersebut **hanya $R^2$ regresi tren waktu sederhana** terhadap tahun, bukan regresi cuaca terhadap hasil.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

fpath = Path("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv")
df = pd.read_csv(fpath)

print(f"Dimensi Data Padi: {df.shape}")
print(f"Kolom Aktual: {df.columns.tolist()}")
print(f"Kabupaten Terdaftar: {df['nama_kabupaten_kota'].nunique()}")

# Rata-rata produktivitas per tahun (menunjukkan anomali 2019)
annual = df.groupby('tahun')['produktivitas_padi2'].agg(['count', 'mean', 'std']).reset_index()
print("\nTrayektori Produktivitas Padi Total Jabar (ku/ha):")
print(annual)
```
