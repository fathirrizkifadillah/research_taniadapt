# TaniAdapt Research Dossier — Phase 7: Statistical Analysis & Econometric Panel Inference

**Status**: COMPLETED  
**Ruang Lingkup**: Pengujian Rigor 11 Hipotesis Prapendaftaran pada Panel Jagung, Padi, dan Kedelai Jawa Barat  
**Metodologi**: Two-Way Fixed Effects, Wild Cluster Bootstrap Webb (B=999), Multiple Testing Corrections (Holm & FDR), Minimum Detectable Effect (MDE)

---

## 1. Hasil Lengkap Pengujian Empiris 11 Hipotesis Fenologi

Seluruh 11 hipotesis fenologi diuji menggunakan spesifikasi Two-Way Fixed Effects (Kabupaten FE + Year FE):

| ID Hipotesis | Komoditas | Prediktor Agrometeorologi | Tanda Hipotesis | Estimasi $\hat{\beta}$ | 95% Webb Bootstrap CI | MDE (Power 80%) | Nilai $p$ Mentah | Nilai $p$ (Holm) | Nilai $q$ (FDR) | Kesimpulan Inferensi |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **H_CORN_01** | Jagung | Presipitasi Vegetatif (Feb–Apr) | (+) | $+0.0368$ | $[-0.0521, +0.1300]$ | $\pm 0.1444$ | $0.4745$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_CORN_02** | Jagung | Suhu Rata-rata Tumbuh (Mar–Mei) | (-) | $+0.5647$ | $[-1.0976, +2.1968]$ | $\pm 2.4995$ | $0.6120$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_CORN_03** | Jagung | VPD Maksimum Reproduktif (Apr–Jun) | (-) | $+0.0909$ | $[-0.0707, +0.2474]$ | $\pm 0.2562$ | $0.4800$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_CORN_04** | Jagung | Hari Kering Berurutan CDD (Mei–Jul) | (-) | $+0.0957$ | $[-0.0034, +0.1939]$ | $\pm 0.1821$ | $0.3010$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_RICE_01** | Padi | Presipitasi Musim Hujan (Okt–Jan) | (Cap) | $+0.0129$ | $[-0.0178, +0.0418]$ | $\pm 0.0425$ | $0.3800$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_RICE_02** | Padi | Suhu Maksimum MK1 (Mar–Mei) | (-) | $-0.1600$ | $[-0.4799, +0.1495]$ | $\pm 0.4543$ | $0.3040$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_RICE_03** | Padi | Hari Kering CDD MK1 (Apr–Jun) | (-) | $-0.0021$ | $[-0.0319, +0.0274]$ | $\pm 0.0453$ | $0.8800$ | $1.0000$ | $0.8800$ | `evidence_insufficient` |
| **H_RICE_04** | Padi | Radiasi Surya MH (Des–Feb) | (+) | $-0.0813$ | $[-0.2216, +0.0585]$ | $\pm 0.2079$ | $0.2520$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_SOY_01** | Kedelai | Presipitasi Polong (Jun–Agu) | (+) | $-0.0094$ | $[-0.0822, +0.0553]$ | $\pm 0.1090$ | $0.7800$ | $1.0000$ | $0.8580$ | `evidence_insufficient` |
| **H_SOY_02** | Kedelai | Suhu Malam Tinggi (Jul–Sep) | (-) | $+0.7188$ | $[-0.2631, +1.6834]$ | $\pm 1.4808$ | $0.3340$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |
| **H_SOY_03** | Kedelai | Hujan Lebat Pemasakan (Agu–Okt) | (-) | $+0.0400$ | $[-0.0140, +0.0904]$ | $\pm 0.0755$ | $0.2980$ | $1.0000$ | $0.8037$ | `evidence_insufficient` |

---

## 2. Analisis Sensitivitas Jendela Waktu & Uji Falsifikasi (Lead Placebo)
Untuk memastikan ketahanan hasil estimasi, dilakukan dua uji diagnostik tambahan pada panel jagung:

1. **Sensitivitas Pergeseran Jendela Waktu Kalender**:
   * *Pergeseran -1 Bulan (Jan–Mar)*: $\hat{\beta} = -0.0076$, $95\%\text{ CI} = [-0.0760, +0.0682]$, $\text{MDE} = \pm 0.1064$.
   * *Jendela Terdaftar (Feb–Apr)*: $\hat{\beta} = +0.0368$, $95\%\text{ CI} = [-0.0521, +0.1300]$, $\text{MDE} = \pm 0.1444$.
   * *Pergeseran +1 Bulan (Mar–Mei)*: $\hat{\beta} = +0.0581$, $95\%\text{ CI} = [-0.0221, +0.1431]$, $\text{MDE} = \pm 0.1330$.
   * *Interpretasi*: Seluruh pergeseran jendela tetap mencakup angka nol dan tidak ada efek struktural yang stabil.
2. **Uji Falsifikasi Placebo Cuaca Masa Depan ($t+1$)**:
   * Memasukkan data cuaca tahun depan ($t+1$) sebagai prediktor hasil panen tahun berjalan ($t$).
   * *Hasil*: $\hat{\beta} = +0.1341$, $95\%\text{ CI} = [-0.1017, +0.3628]$, $\text{MDE} = \pm 0.4199$, $p > 0.40$.
   * *Interpretasi*: Uji falsifikasi lolos; tidak terdapat korelasi palsu yang signifikan secara statistik antara cuaca masa depan dan hasil panen saat ini.

---

## 3. Kesimpulan Saintifik Kritis Phase 7: Penegasan `evidence_insufficient`
1. **Tidak Ada Efek Kausal yang Terdeteksi**: 100% dari 11 hipotesis menghasilkan interval kepercayaan yang mencakup angka nol dan nilai p terkoreksi Holm = 1.0000.
2. **Keterbatasan Daya Statistik Panel Agregat**: Ukuran sampel tahunan ($T=7$) pada 18 sentra tidak memiliki daya statistik (*statistical power*) yang memadai untuk mendeteksi efek cuaca kecil di tengah besarnya variasi pupuk, benih, hama lokal, dan kebisingan pelaporan birokrasi.
3. **Kepatuhan Etis TaniAdapt**: TaniAdapt secara jujur menegakkan status **`evidence_insufficient`** untuk peramalan yield statistik, melarang sistem berpura-pura menemukan korelasi yang tidak ada di data nyata.
