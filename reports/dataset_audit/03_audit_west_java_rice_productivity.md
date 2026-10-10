# Phase 4 Dataset Quality Audit Report: DS03 — West Java Rice Productivity
**TaniAdapt Project — Regional Rice Outcome Target**

---

## 1. Provenance & License
- **Authoritative Title:** Produktivitas Padi Berdasarkan Kabupaten/Kota di Jawa Barat
- **Publisher:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
- **Official Portals:** [data.go.id](https://data.go.id) & [Galura Data Jabar](https://galura.jabarprov.go.id)
- **API Endpoint:** `https://galura.jabarprov.go.id/api/bigdata/produktivitas-padi-berdasarkan-kabupatenkota-di-jawa-barat`
- **License:** Government Open Data (Satu Data Indonesia)

## 2. File Integrity & Coverage
- **Acquired Files:**
  - `produktivitas_padi_jabar.csv` / `.json`: Padi Total (162 rows)
  - `produktivitas_padi_sawah_jabar.csv` / `.json`: Padi Sawah (162 rows)
  - `produktivitas_padi_ladang_jabar.csv` / `.json`: Padi Ladang (162 rows)
- **Spatial Coverage:** All 27 Kabupaten/Kota in Jawa Barat
- **Temporal Coverage:** 2015 to 2020 (6 calendar years)
- **Completeness:** 27 regions × 6 years = exactly 162 records (100% complete matrix)

## 3. Schema & Outcome Definition
- **Columns:** `id`, `kode_provinsi`, `nama_provinsi`, `kode_kabupaten_kota`, `nama_kabupaten_kota`, `produktivitas_padi2`, `satuan`, `tahun`
- **Metric & Unit:** Productivity in `KUINTAL PER HEKTAR` (1 Ku/Ha = 0.1 Ton/Ha)
- **Outcome Distinctions:** Total paddy, wetland paddy (sawah), and upland paddy (ladang) are distinctly documented in separate datasets.

## 4. Value Plausibility
- **Padi Total Range:** 41.51 Ku/Ha to 75.83 Ku/Ha (Mean: 59.2 Ku/Ha ≈ 5.92 Ton/Ha). Plausible for Indonesian irrigated rice yields.
- **Null Values:** 0 null values.

## 5. Data-Fusion Feasibility & Limitations
- **Audit Disposition:** `PASS (REGIONAL_OUTCOME)`
- **Feasibility:** Can be matched to AgERA5 reanalysis by aggregating weather metrics over corresponding cropping years and administrative boundaries.
- **Limitation:** Annual temporal cadence is coarse. It cannot directly supervise daily operational decision rules without season-specific crop calendar disaggregation.