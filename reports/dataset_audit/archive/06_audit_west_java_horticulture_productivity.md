# Phase 4 Dataset Quality Audit Report: DS06 — West Java Horticulture (Chili Focus)
**TaniAdapt Project — Regional Horticulture Outcome Target**

---

## 1. Provenance & License
- **Title:** Produktivitas Sayuran dan Buah-Buahan Semusim (SBS) Berdasarkan Komoditi di Jawa Barat
- **Related Product:** Produksi Sayuran Berdasarkan Komoditas per Kabupaten/Kota di Jawa Barat
- **Publisher:** Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Data Jabar
- **License:** Government Open Data (Satu Data Indonesia)

## 2. File Integrity & Coverage
- **Acquired Files:**
  - `produktivitas_sbs_jabar.csv` / `.json`: 230 rows (Provincial level across seasonal commodities, 2017–2025)
  - `produksi_sayuran_komoditas_jabar.csv` / `.json`: 1,000 rows (Kabupaten/Kota level across commodities, 2013–2024)
- **Key Target Commodities:**
  - `CABAI BESAR` (Large Chili): 2017–2025 series available
  - `CABAI RAWIT` (Bird's-Eye Chili / Cayenne): 2017–2025 series available

## 3. Value Plausibility & Units
- **SBS Productivity Unit:** `KUINTAL PER HEKTAR` (Ku/Ha)
- **Large Chili Productivity:** 79.2 Ku/Ha to 138.5 Ku/Ha (Mean: 106.8 Ku/Ha)
- **Bird's-Eye Chili Productivity:** 58.1 Ku/Ha to 112.4 Ku/Ha (Mean: 86.3 Ku/Ha)
- **Production Unit:** `TON` (at Kabupaten/Kota level)

## 4. Critical Outcome Validity Audit
- **PENTING:** Does this dataset provide disease incidence or pest severity labels?
- **Finding:** **NO.** This dataset provides aggregated economic crop productivity and production statistics. It does NOT contain field-level disease incidence, pathogen presence, or severity scoring.
- **Agricultural Interpretation:** Suitable as an agricultural outcome target for chili yield response modeling; disease-risk rules cannot be trained directly on this target without epidemiological assumptions or field-level disease datasets.

## 5. Audit Disposition
- **Audit Disposition:** `PASS (REGIONAL_HORTICULTURE_OUTCOME)`
- **Caveat:** Must not be misrepresented as a disease incidence dataset.