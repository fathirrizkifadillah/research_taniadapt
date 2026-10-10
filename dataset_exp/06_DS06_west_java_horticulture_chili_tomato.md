# 🌶️ DS06 — Hortikultura Sayuran Buah Semusim (Cabai & Tomat)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS06_west_java_horticulture`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:**
  * Produktivitas SBS: `https://galura.jabarprov.go.id/api/bigdata/od_18100_produktivitas_sayuran_buah_semusim_berdasarkan_komoditas`
  * Volume Produksi Sayuran: `https://galura.jabarprov.go.id/api/bigdata/od_18096_produksi_sayuran_berdasarkan_komoditas`
* **Format File Lokal:** CSV & JSON di `data/raw/DS06_west_java_horticulture/`
* **Ukuran Total:** ~17 KB

---

## 2. Cakupan Spasial, Komoditas, & Rentang Waktu
* **Cakupan Spasial:** **Tingkat Agregat Provinsi Jawa Barat** (angka makro total provinsi, bukan rincian per kabupaten).
* **Rentang Waktu:** 8 Tahun Penuh (**2017 s.d. 2024**).
* **Frekuensi:** Tahunan ($N=8$ baris observasi per komoditas).
* **Komoditas Utama yang Dipantau:**
  1. **Cabai Rawit:** Rata-rata produktivitas $\sim 85\text{--}92\text{ Ku/Ha}$.
  2. **Cabai Besar:** Rata-rata produktivitas $\sim 110\text{--}125\text{ Ku/Ha}$.
  3. **Tomat:** Rata-rata produktivitas $\sim 190\text{--}230\text{ Ku/Ha}$.
* **Satuan Ukuran:** **KUINTAL / HEKTAR** (Produktivitas) dan **KUINTAL / TON** (Produksi).

---

## 3. Kamus Data & Struktur Kolom

| Nama Kolom | Tipe Data | Deskripsi & Nilai Contoh |
| :--- | :--- | :--- |
| `id` | Integer | ID unik record sistem. |
| `kode_provinsi` | Integer | `32` (Jawa Barat). |
| `nama_provinsi` | String | `JAWA BARAT`. |
| `nama_komoditas` | String | `CABAI BESAR`, `CABAI RAWIT`, `TOMAT`. |
| `produktivitas_sayuran_buah_semusim` | Float | Angka rata-rata panen provinsi per hektar (Kuintal/Ha). |
| `satuan` | String | `KUINTAL/HEKTAR`. |
| `tahun` | Integer | Tahun observasi (2017 s.d. 2024). |

---

## 4. TEMUAN AUDIT PALING KRUSIAL (YIELD vs DISEASE INCIDENCE)

Audit mendalam terhadap dataset ini menghasilkan **keputusan metodologi paling penting di proyek TaniAdapt**:

### A. Ketiadaan Total Label Penyakit Tanaman (OPT)
1. Dataset ini **HANYA BERISI ANGKA HASIL PANEN (YIELD)**.
2. Dataset ini **TIDAK MEMILIKI LABEL PENYAKIT / HAMA (OPT)**. Tidak ada data keparahan antraknosa (*Colletotrichum capsici*), layu fusarium (*Fusarium oxysporum*), atau hawar daun (*Phytophthora infestans*).
3. **Aturan Riset TaniAdapt:** **DILARANG KERAS** melatih model Machine Learning klasifikasi penyakit tanaman dari dataset ini! Melatih model klasifikasi penyakit tanpa data label penyakit adalah *pseudoscience*.

### B. Validasi Literatur Riset (Paper 7 Handhayani et al., 2026)
* Sesuai dengan temuan audit Paper 7 di repo: *"Untuk cabai rawit, bukti statistik bahwa meteorologi memengaruhi hasil panen (yield) dinilai belum cukup dalam paper ini"*. Hubungan cuaca ke hasil panen cabai sangat rentan terdistorsi oleh dinamika harga pasar dan panen bertahap (*multi-harvest cycles*).

### C. Solusi Metodologi: Index of Favorable Weather Condition (IFWC)
Karena data label OPT tidak tersedia, advisory penyakit pada cabai dan tomat di TaniAdapt dijalankan menggunakan **Index of Favorable Weather Condition (IFWC)** berbasis **fisika mikroklimat**:
* **Proksi Kebasahan Daun (Leaf Wetness):** Menggunakan selisih suhu terhadap titik embun ($T - T_d$) dan kelembaban relatif maksimum ($\text{RH}_{\max}$).
* Jika $T - T_d \le 2.0^\circ\text{C}$ dan $\text{RH}_{\max} \ge 90\%$, atmosfer berada dalam kondisi jenuh embun malam, yang secara agronomis merupakan syarat mutlak perkecambahan spora jamur antraknosa dan hawar daun.
* Rekomendasi yang dikeluarkan sistem adalah: *"Kondisi cuaca sangat mendukung perkembangan spora jamur (IFWC Tinggi). Lakukan sanitasi drainase dan monitoring lapangan preventif."* (Sistem tidak mengklaim tanaman sudah pasti sakit).

---

## 5. Cuplikan Kode Python

```python
import pandas as pd
from pathlib import Path

csv_path = Path("data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.csv")
df = pd.read_csv(csv_path)

# Filter cabai dan tomat
chili_tomato = df[df['nama_komoditas'].str.upper().isin(['CABAI RAWIT', 'CABAI BESAR', 'TOMAT'])]
display(chili_tomato.pivot(index='tahun', columns='nama_komoditas', values='produktivitas_sayuran_buah_semusim'))
```
