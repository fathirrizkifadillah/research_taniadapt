# Phase 4 Dataset Quality Audit Report: DS05 — Subang & West Java Maize Productivity
**TaniAdapt Project — Regional Maize Outcome Target**

---

## 1. Provenance & License
- **Title:** Produktivitas Jagung Berdasarkan Kabupaten/Kota di Jawa Barat (incl. Kab. Subang)
- **Publisher:** Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar
- **Portal:** [data.go.id](https://data.go.id) & [Galura Data Jabar](https://galura.jabarprov.go.id)
- **License:** Government Open Data (Satu Data Indonesia)

## 2. File Integrity & Coverage
- **Acquired Files:** `produktivitas_jagung_jabar.csv` / `.json` (216 rows)
- **Spatial Coverage:** 27 Kabupaten/Kota in Jawa Barat (includes Kabupaten Subang)
- **Temporal Coverage:** 2015 to 2022 (8 calendar years)
- **Completeness:** 27 regions × 8 years = 216 records (100% complete matrix)

## 3. Subang Regency Specifics
- **Subang Records:** 8 annual observations (2015–2022).
- **Subang Productivity Range:** 41.20 Ku/Ha to 68.80 Ku/Ha (Mean: 53.4 Ku/Ha ≈ 5.34 Ton/Ha).
- **Subdistrict (Kecamatan) Blocker:** The upstream subdistrict-level resource on data.go.id / Galura (`produktivitas-jagung-menurut-kecamatan-di-kabupaten-subang`) returned HTTP 502 Bad Gateway from the provincial server; regency-level published series was successfully acquired and verified.

## 4. Audit Disposition & Role
- **Audit Disposition:** `PASS (REGIONAL_OUTCOME)`
- **Role:** Serves as the empirical maize productivity target for West Java / Subang.
- **Limitation:** Available at regency level; annual frequency requires temporal aggregation when merging with weather features.