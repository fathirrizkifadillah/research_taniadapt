# TaniAdapt Research Dossier — Phase 7: Statistical Analysis

**Status**: COMPLETED  
**Metodologi**: Two-Way Fixed Effects (Kabupaten FE + Year FE), Wild Cluster Bootstrap Webb (B=999), Koreksi Holm-Bonferroni & Benjamini-Hochberg FDR, dan Power Analysis Minimum Detectable Effect (MDE).

---

## 1. Hasil Pengujian 11 Hipotesis Fenologi
Seluruh 11 hipotesis terdaftar diuji secara transparan pada panel data empiris:

| ID Hipotesis | Komoditas | Prediktor Agrometeorologi | Tanda Hipotesis | Estimasi $\hat{\beta}$ | 95% Webb Bootstrap CI | MDE (Power 80%) | Nilai $p$ (Holm) | Kesimpulan Statistik |
|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **H_CORN_01** | Jagung | Presipitasi Vegetatif (Feb–Apr) | (+) | $+0.0368$ | $[-0.0521, +0.1300]$ | $\pm 0.1444$ | $1.0000$ | `evidence_insufficient` |
| **H_CORN_02** | Jagung | Suhu Rata-rata Tumbuh (Mar–Mei) | (-) | $+0.5647$ | $[-1.0976, +2.1968]$ | $\pm 2.4995$ | $1.0000$ | `evidence_insufficient` |
| **H_CORN_03** | Jagung | VPD Maksimum Reproduktif (Apr–Jun) | (-) | $+0.0909$ | $[-0.0707, +0.2474]$ | $\pm 0.2562$ | $1.0000$ | `evidence_insufficient` |
| **H_CORN_04** | Jagung | Hari Kering Berurutan CDD (Mei–Jul) | (-) | $+0.0957$ | $[-0.0034, +0.1939]$ | $\pm 0.1821$ | $1.0000$ | `evidence_insufficient` |
| **H_RICE_01** | Padi | Presipitasi Musim Hujan (Okt–Jan) | (Cap) | $+0.0129$ | $[-0.0178, +0.0418]$ | $\pm 0.0425$ | $1.0000$ | `evidence_insufficient` |
| **H_RICE_02** | Padi | Suhu Maksimum MK1 (Mar–Mei) | (-) | $-0.1600$ | $[-0.4799, +0.1495]$ | $\pm 0.4543$ | $1.0000$ | `evidence_insufficient` |
| **H_RICE_03** | Padi | Hari Kering CDD MK1 (Apr–Jun) | (-) | $-0.0021$ | $[-0.0319, +0.0274]$ | $\pm 0.0453$ | $1.0000$ | `evidence_insufficient` |
| **H_RICE_04** | Padi | Radiasi Surya MH (Des–Feb) | (+) | $-0.0813$ | $[-0.2216, +0.0585]$ | $\pm 0.2079$ | $1.0000$ | `evidence_insufficient` |
| **H_SOY_01** | Kedelai | Presipitasi Polong (Jun–Agu) | (+) | $-0.0094$ | $[-0.0822, +0.0553]$ | $\pm 0.1090$ | $1.0000$ | `evidence_insufficient` |
| **H_SOY_02** | Kedelai | Suhu Malam Tinggi (Jul–Sep) | (-) | $+0.7188$ | $[-0.2631, +1.6834]$ | $\pm 1.4808$ | $1.0000$ | `evidence_insufficient` |
| **H_SOY_03** | Kedelai | Hujan Lebat Pemasakan (Agu–Okt) | (-) | $+0.0400$ | $[-0.0140, +0.0904]$ | $\pm 0.0755$ | $1.0000$ | `evidence_insufficient` |

---

## 2. Temuan Utama Phase 7
1. **100% Hipotesis Berstatus `evidence_insufficient`**: Seluruh interval kepercayaan 95% mencakup angka nol dan nilai estimasi $\hat{\beta}$ berada jauh di bawah batas deteksi statistik (MDE).
2. **Keterbatasan Daya Statistik**: Sampel panel tahunan di tingkat kabupaten memiliki variabilitas cuaca antar-tahun yang terlalu sempit dibanding *noise* non-cuaca (manajemen petani dan pelaporan birokrasi), sehingga regresi statistik tidak mampu membuktikan kausalitas cuaca terhadap hasil panen.
