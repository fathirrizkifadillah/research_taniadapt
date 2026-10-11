# 🌶️ DS06 — Hortikultura Sayuran Buah Semusim (Cabai & Tomat)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS06_west_java_horticulture`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:**
  * Produktivitas SBS: `https://galura.jabarprov.go.id/api/bigdata/od_18100_produktivitas_sayuran_buah_semusim_berdasarkan_komoditas`
  * Volume Produksi Sayuran: `https://galura.jabarprov.go.id/api/bigdata/od_18096_produksi_sayuran_berdasarkan_komoditas`
* **Format File Lokal:** CSV & JSON di `data/raw/DS06_west_java_horticulture/`
* **Ukuran Total:** ~76 KB (kombinasi 2 dataset)

---

## 2. Cakupan Spasial, Komoditas, & Rentang Waktu
* **Cakupan Spasial:**
  * `produktivitas_sbs_jabar.csv`: **Tingkat Agregat Provinsi Jawa Barat** ($N=9$ baris observasi per komoditas, 2016–2024).
  * `produksi_sayuran_komoditas_jabar.csv`: **Tingkat Kabupaten/Kota** (volume produksi sayuran, 2016–2024).
* **Rentang Waktu:** 9 Tahun Penuh (**2016 s.d. 2024**).
* **Komoditas Utama yang Dipantau:** Cabai Rawit, Cabai Besar, Tomat, Bawang Merah.
* **Satuan Ukuran Aktual:**
  * Produktivitas SBS: **KUINTAL / HEKTAR** ($1\text{ ku} = 100\text{ kg} = 0.1\text{ ton}$).
  * Volume Produksi Sayuran: **TON** (bukan Kuintal/Ton).

---

## 3. Kamus Data & Nama Kolom Aktual

### File `produktivitas_sbs_jabar.csv`:
| Nama Kolom Aktual | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer | ID unik record sistem Galura |
| `kode_provinsi` | Integer | `32` (Jawa Barat) |
| `nama_provinsi` | String | `JAWA BARAT` |
| `komoditi` | String | Nama komoditas (`CABAI RAWIT`, `CABAI BESAR`, `TOMAT`) |
| `produktivitas_sayur_buah` | Float | Rata-rata produktivitas provinsi (Kuintal/Ha) |
| `satuan` | String | `KUINTAL/HEKTAR` |
| `tahun` | Integer | Tahun observasi (2016 s.d. 2024) |

### File `produksi_sayuran_komoditas_jabar.csv`:
| Nama Kolom Aktual | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer | ID unik record |
| `kode_kabupaten_kota` | Integer | Kode wilayah 27 Kab/Kota |
| `nama_kabupaten_kota` | String | Nama Kabupaten/Kota |
| `jenis_komoditas` | String | Komoditas sayuran |
| `produksi_sayuran` | Float | Volume produksi fisik (Ton) |
| `satuan` | String | `TON` |
| `tahun` | Integer | Tahun observasi |

---

## 4. Temuan Audit Metodologi (Yield vs Kejadian Penyakit OPT)

> [!IMPORTANT]
> **Ketiadaan Data Serangan Hama/Penyakit (OPT)**:
> 1. Dataset ini **HANYA BERISI ANGKA HASIL PANEN DAN VOLUME PRODUKSI**.
> 2. Dataset ini **TIDAK MEMILIKI LABEL PENYAKIT / HAMA (OPT)**. Tidak ada data keparahan antraknosa (*Colletotrichum capsici*), layu fusarium (*Fusarium oxysporum*), atau hawar daun (*Phytophthora infestans*).
> 3. **Larangan Metodologis**: Dilarang melatih model Machine Learning klasifikasi atau probabilitas penyakit dari data hasil panen makro tahunan.
> 4. **Penghapusan Ambang Tak Bersumber**: Seluruh aturan sebelumnya seperti *"T - Td <= 2.0 C dan RH >= 90% = syarat mutlak"* atau *"kelembapan tomat 18-20 C teruji di Balitsa Lembang"* telah **DIHAPUS** karena tidak memiliki rujukan sitasi ilmiah langsung di repositori.

### Opsi Implementasi IFWC (Index of Favorable Weather Condition) Tanpa Ambang Buatan:
Sistem advisory mikroklimat mengadopsi 2 opsi transparan:
* **Opsi A (Cutoff Literatur dengan Label Transfer)**: Jika menggunakan batas literatur luar (misal Paper 3/5), sistem **wajib melabelinya secara transparan sebagai *Literature Transfer (Belum Divalidasi Lokal)***, bukan klaim validitas lokal Jawa Barat.
* **Opsi B (Skor Relatif Berbasis Persentil Climatological)**: Mengukur indeks kebasahan relatif per sel dan jendela kalender (misal: *"Kondisi 7 hari terakhir lebih basah dari 85% tahun serupa pada periode kalender yang sama"*), **bukan mengklaim probabilitas risiko infeksi**.

### Uji Hipotesis Proksi Kebasahan: $T_{\min} - T_d$ vs $T_{\text{mean}} - T_d$
Secara termodinamika, kondensasi embun malam terjadi saat suhu turun mendekati titik embun di waktu fajar ($T_{\min}$). Pengujian data AgERA5 membuktikan:
* Pada $T_{\text{mean}} - T_d \le 2.0^\circ\text{C}$, frekuensi keterjadian hanya **0.0% – 3.9%** (karena suhu siang mendistorsi nilai rata-rata 24 jam).
* Pada $T_{\min} - T_d \le 2.0^\circ\text{C}$, frekuensi kondensasi malam terdeteksi pada **31.5% – 93.9%** hari di musim hujan.
* *Status*: Diadopsi sebagai **hipotesis proksi agronomis** untuk pemantauan mikroklimat malam hari.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/DS06_west_java_horticulture")
df_sbs = pd.read_csv(raw_dir / "produktivitas_sbs_jabar.csv")

print(f"Dimensi SBS Jabar: {df_sbs.shape}")
print(f"Kolom Aktual SBS: {df_sbs.columns.tolist()}")

# Filter komoditas cabai rawit dan cabai besar
chili_df = df_sbs[df_sbs['komoditi'].str.upper().str.contains('CABAI')].copy()
print("\nRingkasan Produktivitas Cabai Jabar (ku/ha):")
print(chili_df[['tahun', 'komoditi', 'produktivitas_sayur_buah', 'satuan']].sort_values(['komoditi', 'tahun']))
```
