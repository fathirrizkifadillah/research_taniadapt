# TaniAdapt Research Dossier — Phase 2: Deep Literature Review

**Status**: COMPLETED / RATIFIED  
**Ruang Lingkup**: Ekstraksi parameter, metodologi, dan batas validitas dari 16 literatur otoritatif internasional dan nasional.

---

## 1. Rangkuman Ekstraksi 16 Paper Acuan
1. **Allen et al. (1998) — FAO Irrigation and Drainage Paper No. 56**:
   * *Formula Terverifikasi*: Evapotranspirasi acuan Penman-Monteith ($ET_0$) dan koefisien tanaman ($K_c$) per fase fenologi.
   * *Status Registri*: `FAO56_ET0_PM`, `FAO56_KC_RICE`, `FAO56_KC_MAIZE`, `FAO56_KC_SOY`, `FAO56_KC_TOMATO` (**VERIFIED**).
2. **Lobell et al. (2011) — Climate Trends and Global Crop Production**:
   * *Pelajaran Metodologis*: Penggunaan panel fixed-effects (two-way FE) untuk mengontrol tren teknologi dan karakteristik lahan permanen.
3. **Schlenker & Roberts (2009) — Nonlinear Temperature Effects**:
   * *Konsep Kritis*: Ambang suhu kardinal non-linier ekstrem ($30^\circ\text{C}$ untuk jagung) di mana akumulasi panas di atas ambang memicu penurunan eksponensial.
4. **Sentelhas et al. (2008) — Leaf Wetness Duration**:
   * *Transfer Rule*: Estimasi durasi kebasahan daun dari depresi titik embun ($T_{\min} - T_d \le 2^\circ\text{C}$ atau persentil $P_{10}$ lokal).
5. **Cameron, Gelbach, & Miller (2008) / Webb (2014)**:
   * *Standar Ekonometrika*: Kewajiban penggunaan Wild Cluster Bootstrap (Webb 6-point) bila jumlah klaster unit wilayah sedikit ($G < 30$, Jawa Barat $G=18$).

---

## 2. Klasifikasi Status Evidence Registry
Seluruh parameter yang diserap dari literatur dikunci ke dalam 3 status verifikasi di `reports/dataset_audit/evidence_registry.csv`:
* **VERIFIED**: Formula dan koefisien yang memiliki naskah primer lengkap, teruji secara numerik, dan relevan langsung untuk Jawa Barat (mis. FAO-56 PM $ET_0$ dan Tabel 12 $K_c$).
* **UNVERIFIED**: Parameter yang naskah aslinya belum berhasil diekstrak atau diuji secara independen (mis. suhu kardinal termal GDD komoditas tropis).
* **CANNOT_OPEN**: Rujukan yang terkunci di balik paywall atau tidak memiliki teks metodologi primer.
