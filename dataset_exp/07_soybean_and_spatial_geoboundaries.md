# 🧬 Data Ekstensi — Kedelai Jawa Barat & Geospasial ADM2 Centroids

## 1. Produktivitas Kedelai Jawa Barat (`produktivitas_kedelai_jabar.csv`)

### A. Identitas Dataset & Sumber Resmi
* **Penerbit / Sumber:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Jawa Barat / Galura Open Data Jabar
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18105_produktivitas_kedelai_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV di `data/raw/produktivitas_kedelai_jabar.csv`
* **Ukuran:** ~15 KB (216 baris lengkap, 27 kabupaten/kota $\times$ 8 tahun: 2015 s.d. 2022)

### B. Distribusi Nilai & Fakta Empiris
Audit langsung terhadap dataset kedelai menghasilkan angka-angka statistik pasti:
* **Total Baris:** 216 baris.
* **Baris Bernilai Positif ($>0$ Ku/Ha):** **156 baris ($72.2\%$)**.
* **Baris Bernilai Nol ($=0$ Ku/Ha):** **60 baris ($27.8\%$)**.
* **Missing Value (NaN / Null):** **0 baris ($0.0\%$)**.
* **Analisis Kelayakan Spasial:**
  * Sebanyak **18 dari 27 kabupaten/kota** memiliki aktivitas tanam kedelai aktif $\ge 6$ tahun dari 8 tahun.
  * Seluruh **14 kabupaten sentra tanaman pangan utama** (Ciamis, Garut, Kuningan, Majalengka, Cianjur, Sukabumi, dll.) memiliki data positif **8 tahun berturut-turut lengkap**.
  * Nilai nol ($=0$) terkonsentrasi $100\%$ pada wilayah perkotaan (KOTA) yang tidak memiliki hamparan sawah/ladang kedelai (seperti Kota Bandung, Kota Cimahi, Kota Cirebon, Kota Sukabumi).

### C. Keputusan Seleksi Portofolio Tanaman ke-4
Meskipun kedelai memiliki kelayakan data yang memadai, portofolio tanaman ke-4 TaniAdapt mengunci **Tomat** (Tier B) dengan pertimbangan:
1. **Sinergi Taksonomi Solanaceae:** Tomat satu famili dengan Cabai (Solanaceae), sehingga struktur fenologi dan fisiologi daun selaras.
2. **Reusabilitas Modul Mikroklimat:** Parameter mikroklimat kebasahan daun ($T - T_d$, $\text{RH}_{\max}$) dapat langsung dipakai bersama ambang batas penyakit hawar daun tomat (*Phytophthora infestans*) $18\text{--}20^\circ\text{C}$ yang telah teruji di Balitsa Lembang.

---

## 2. Batas Geospasial Poligon ADM2 & Centroid Sejati

### A. Sumber Data Geospasial
* **Sumber:** **geoBoundaries (USAID / William & Mary)** — open administrative boundary database.
* **Tingkat Administrasi:** ADM2 (Level Kabupaten/Kota Indonesia).
* **Script Ekstraksi:** [scripts/compute_true_centroids_and_cells.py](file:///c:/CODING/research_taniAdapt/scripts/compute_true_centroids_and_cells.py).
* **File Output:**
  * `reports/dataset_audit/jabar_27_kabkota_spatial_audit.csv`
  * `reports/dataset_audit/jabar_27_kabkota_centroids.csv`

### B. Hasil Audit Spasial & Sel Grid AgERA5 0.1°
Resolusi spasial AgERA5 adalah $0.1^\circ \times 0.1^\circ$ (sekitar $10\text{ km} \times 10\text{ km}$ per sel). Penghitungan poligon resmi menemukan jumlah sel cuaca independen di dalam tiap kabupaten:

| Nama Wilayah | Tipe | Centroid Sejati (Lat, Lon) | Luas Estimasi ($km^2$) | Jumlah Sel AgERA5 (0.1°) |
| :--- | :--- | :--- | :--- | :--- |
| **KABUPATEN SUKABUMI** | Kabupaten | -7.1264, 106.7196 | 4.145 km² | **36 sel grid** |
| **KABUPATEN CIANJUR** | Kabupaten | -7.1472, 107.1738 | 3.501 km² | **30 sel grid** |
| **KABUPATEN GARUT** | Kabupaten | -7.4069, 107.7852 | 3.074 km² | **25 sel grid** |
| **KABUPATEN SUBANG** | Kabupaten | -6.5518, 107.6841 | 2.051 km² | **18 sel grid** |
| **KABUPATEN KARAWANG**| Kabupaten | -6.2415, 107.4243 | 1.753 km² | **16 sel grid** |
| **KABUPATEN INDRAMAYU**| Kabupaten | -6.4529, 108.1633 | 2.040 km² | **18 sel grid** |
| **KOTA BANDUNG** | Kota | -6.9175, 107.6191 | 167 km² | **2 sel grid** |

### C. Manfaat bagi Tahap Modeling TaniAdapt
* Menghindari bias koordinat perkotaan (seperti titik Bandung pilot lama yang berada di pusat kota).
* Memberikan koordinat titik berat pertanian (*true geographic centroid*) untuk mengekstrak data cuaca AgERA5 pada seluruh 27 kabupaten/kota di Jawa Barat.
