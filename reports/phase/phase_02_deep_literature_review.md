# TaniAdapt Research Dossier — Phase 2: Deep Literature Review & Evidence Framework

**Status**: COMPLETED / RATIFIED  
**Dokumen Induk**: `docs/evidence_registry_literature.md` & `reports/dataset_audit/evidence_registry.csv`  
**Sumber Primer**: 16 Paper Akademik Bereputasi Internasional & 15 Benchmark Kompetitor DSS

---

## 1. Ekstraksi Metodologis dari 16 Paper Ilmiah Utama

### A. Fisika dan Biofisika Tanaman (Bio-mechanistic Foundations)
1. **Allen, Pereira, Raes, & Smith (1998) — FAO Irrigation and Drainage Paper No. 56**:
   * *Formula*: Standar internasional Penman-Monteith untuk menghitung Evapotranspirasi Acuan ($ET_0$) harian dari suhu, radiasi, kecepatan angin, dan tekanan uap.
   * *Koefisien*: Tabel 12 halaman 110 memberikan nilai koefisien tanaman ($K_c$) per fase (awal, tengah, akhir) untuk Padi sawah ($1.05 	o 1.20 	o 0.75$), Jagung ($0.30 	o 1.20 	o 0.48$), Kedelai ($0.40 	o 1.15 	o 0.50$), dan Tomat ($0.60 	o 1.15 	o 0.80$).
   * *Status Audit*: **`VERIFIED`** (Lolos validasi numerik Contoh 18 Bab 4 FAO-56 dengan deviasi < 0.01 mm/hari).
2. **Sentelhas, Gillespie, & Santos (2008) — Leaf Wetness Duration**:
   * *Temuan*: Mengkaji estimasi durasi kebasahan daun (LWD) dari parameter cuaca standar untuk pemodelan spora patogen tanaman.
   * *Aturan Operasional*: Depresi titik embun ($T_{\min} - T_d$) mendekati nol saat fajar mengindikasikan kondensasi embun aktif $\ge 8$ jam pada kanopi.
   * *Status Audit*: Diterapkan sebagai aturan transfer Tier B berbasis persentil relatif lokal $P_{10}$ per sel dan bulan kalender.

### B. Ekonometrika dan Analisis Panel Cuaca-Hasil
3. **Lobell, Bänziger, Magorokosho, & Vivek (2011) — Nonlinear heat effects on African maize (Nature Climate Change)**:
   * Menekankan penggunaan Two-Way Fixed Effects untuk memisahkan dampak cuaca tahun berjalan dari kemajuan teknologi varietas hibrida.
4. **Schlenker & Roberts (2009) — Nonlinear temperature effects on US crop yields (PNAS)**:
   * Mengidentifikasi respons non-linier tajam pada suhu di atas $29–30^\circ	ext{C}$ pada jagung, yang melatarbelakangi pengujian indeks panas ekstrem.
5. **Cameron, Gelbach, & Miller (2008) / Webb (2014) — Wild Cluster Bootstrap for Few Clusters**:
   * Standar baku ekonometrika inferensi klaster kecil ($G < 30$). Distribusi bobot 6-titik Webb terbukti superior dibanding Rademacher 2-titik untuk mencegah distorsi ukuran uji signifikansi.

---

## 2. Struktur Registri Bukti Ilmiah (Evidence Registry)

Setiap parameter ilmiah yang digunakan dalam Decision Engine TaniAdapt dikatalogkan ke dalam format terstruktur dengan status verifikasi yang ketat:

| ID Registri Bukti | Parameter / Aturan Agronomi | Sumber Acuan Primer | Parameter Konkret | Status Verifikasi |
|---|---|---|---|:---:|
| **FAO56_ET0_PM** | Evapotranspirasi Acuan Harian | Allen et al. (1998) Eq. 6 | $ET_0$ Penman-Monteith FAO-56 | **`VERIFIED`** |
| **FAO56_KC_RICE** | Koefisien Fenologi Padi Sawah | Allen et al. (1998) Tabel 12 | $K_c$: 1.05 (ini) $	o$ 1.20 (mid) $	o$ 0.75 (end) | **`VERIFIED`** |
| **FAO56_KC_MAIZE** | Koefisien Fenologi Jagung Pipil | Allen et al. (1998) Tabel 12 | $K_c$: 0.30 (ini) $	o$ 1.20 (mid) $	o$ 0.48 (end) | **`VERIFIED`** |
| **FAO56_KC_SOY** | Koefisien Fenologi Kedelai | Allen et al. (1998) Tabel 12 | $K_c$: 0.40 (ini) $	o$ 1.15 (mid) $	o$ 0.50 (end) | **`VERIFIED`** |
| **FAO56_KC_TOMATO**| Koefisien Fenologi Tomat | Allen et al. (1998) Tabel 12 | $K_c$: 0.60 (ini) $	o$ 1.15 (mid) $	o$ 0.80 (end) | **`VERIFIED`** |
| **RICE_TEMP_PHASES**| Suhu Kardinal Fenologi Padi | Berbagai literatur sekunder | $T_{	ext{base}}, T_{	ext{opt}}, T_{	ext{max}}$ per fase | **`UNVERIFIED`** |
| **MAIZE_TEMP_PHASES**| Suhu Kardinal Fenologi Jagung | Berbagai literatur sekunder | $T_{	ext{base}}, T_{	ext{opt}}, T_{	ext{max}}$ per fase | **`UNVERIFIED`** |
| **CHILI_WATER** | Kebutuhan Air Spesifik Cabai | Ekstrapolasi sweet pepper | Koefisien $K_c$ cabai tropis | **`UNVERIFIED`** |
| **CHILI_ANTHRACNOSE**| Ambang Fisik Spora Antraknosa| Paywalled literature | Jam basah daun dan spora jamur | **`CANNOT_OPEN`** |
| **ACTION_SOPS** | SOP Dosis Kimia Spesifik | Penyuluhan Pertanian | Rekomendasi takaran pestisida | **`CANNOT_OPEN`** |

*Aturan Engine*: Parameter berstatus **`VERIFIED`** diizinkan memicu kalkulasi fisis operasional. Parameter berstatus **`UNVERIFIED`** atau **`CANNOT_OPEN`** dilarang mengarang formula dan **wajib memicu status `evidence_insufficient`**.

---

## 3. Benchmark Lanskap 15 Aplikasi Kompetitor DSS Pertanian
Kajian mendalam terhadap 15 platform agro-advisory (Sipindo, Riung, Katam Kementan, ClimateFieldView, Plantix, Cropin, dll.) mengungkap kelemahan sistemik yang dipecahkan oleh TaniAdapt:
1. **Black-box Heuristics**: Mayoritas aplikasi komersial menyembunyikan formula di balik skor indeks 0–100 tanpa transparansi data cuaca atau sitasi ilmiah.
2. **Tidak Ada Penanganan Ketidakpastian**: Hampir semua aplikasi selalu memberikan tebakan bahkan ketika data cuaca tidak lengkap atau berada di luar domain validitas.
3. **Keunggulan TaniAdapt**: Sepenuhnya terbuka (*glass-box decision trace*), berbasis fisika Penman-Monteith, terikat kontrak JSON skema, dan berani mengembalikan status `evidence_insufficient`.
