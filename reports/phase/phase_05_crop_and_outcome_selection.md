# TaniAdapt Research Dossier — Phase 5: Crop & Outcome Selection

**Status**: COMPLETED / RATIFIED (Terkunci di `docs/crop_outcome_decision.md`)  
**Keputusan Portofolio**: Mengunci 5 komoditas resmi dan menetapkan metodologi inferensi spesifik untuk tiap komoditas.

---

## 1. Portofolio Komoditas Ratifikasi
1. **Padi Sawah (Oryza sativa)**:
   * *Status Analisis*: `mechanistic advisory` (FAO-56 Penman-Monteith $ET_0$ dan $K_c$ per fase).
   * *Justifikasi*: Data statistik panen BPS hanya tersedia 3 tahun (2015–2017, $N=53$), derajat kebebasan statistik ($df=33$) tidak memadai untuk regresi empiris cuaca bebas bias.
2. **Jagung (Zea mays)**:
   * *Status Analisis*: `empirical sensitivity analysis + mechanistic advisory`.
   * *Justifikasi*: Memiliki sampel panel terbesar (18 sentra, 2015–2021 eksklusi 2022, $N=124$). Minimum Detectable Effect $\text{MDE} = \pm 0.1444$, estimasi efek cuaca $\beta = +0.0368$ (berstatus jujur `evidence_insufficient`).
3. **Kedelai (Glycine max)**:
   * *Status Analisis*: `empirical sensitivity analysis + mechanistic advisory`.
   * *Justifikasi*: 17 sentra aktif (2015–2021 eksklusi 2022, $N=113$), dianalisis untuk respons stres kebasahan pengisian polong.
4. **Cabai Rawit & Cabai Merah (Capsicum spp.)**:
   * *Status Analisis*: `Tier B literature-transfer rule` ($P_{10}$ depresi titik embun fajar).
   * *Justifikasi*: Data hasil panen hanya di tingkat provinsi (SBS $N=8$, 2017–2024), dilarang regresi hasil atau pemodelan ML penyakit.
5. **Tomat (Solanum lycopersicum)**:
   * *Status Analisis*: `Tier B literature-transfer rule + mechanistic advisory`.
   * *Justifikasi*: Memiliki koefisien tanaman terverifikasi FAO-56 ($K_c: 0.60\to 1.15\to 0.80$) serta pemantauan risiko hawar daun berbasis kelembapan fajar.
6. **Bawang Merah**: Berstatus resmi `blocked pending new data` (dikeluarkan dari sistem aktif karena ketiadaan data sentra terpercaya).
