# Log Eksplorasi & Mitigasi Percabangan Jalur Peneliti (Exploration Log)

Dokumen ini melacak seluruh variabel cuaca, definisi jendela fenologi, dan model spesifikasi yang dicoba selama Phase 6 Exploratory Data Analysis (EDA) TaniAdapt Jawa Barat, sebagai perlindungan metodologis terhadap *forking paths* (Gelman & Loken, 2014) dan *p-hacking*.

> **Aturan B5**: Setiap variabel, jendela waktu, atau pengujian yang dicoba dalam analisis wajib tercatat di `exploration_log.md`. Dilarang memilih variabel atau jendela berdasarkan signifikansi korelasi dengan outcome.

---

## 1. Register Percobaan Variabel & Jendela Waktu (Forking Paths Tracking)

| ID Uji | Komoditas | Variabel Cuaca | Jendela Waktu | Status di hypotheses.md | Alasan Pengujian | Temuan / Hasil Diagnostik |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **EXP_01** | Jagung | Presipitasi Akumulasi Vegetatif (`precip_veg`) | Feb – Apr | **Terdaftar Utama (H_CORN_01)** | Pengujian hipotesis primer kebutuhan air fase vegetatif awal. | Effect size $\beta = +0.0182$ log points / SD, $95\%\text{ CI } [-0.038, +0.074]$. Di bawah batas deteksi $\text{MDE} = \pm 0.2296$. Status: Evidence Insufficient. |
| **EXP_02** | Jagung | Presipitasi Vegetatif (Shift -1 Bulan) | Jan – Mar | **Uji Sensitivitas (Pre-Registered)** | Evaluasi pergeseran tanggal tanam lebih dini pada tahun basah. | $\beta = +0.0062$, $95\%\text{ CI } [-0.053, +0.065]$. Hasil stabil berada di dalam selang ketidakpastian EXP_01. |
| **EXP_03** | Jagung | Presipitasi Vegetatif (Shift +1 Bulan) | Mar – Mei | **Uji Sensitivitas (Pre-Registered)** | Evaluasi pergeseran tanam mundur akibat keterlambatan hujan. | $\beta = +0.0262$, $95\%\text{ CI } [-0.033, +0.085]$. Hasil stabil berada di dalam selang ketidakpastian EXP_01. |
| **EXP_04** | Jagung | Lead Weather Placebo ($t+1$) | Feb – Apr tahun $t+1$ | **Diagnostik Falsifikasi (Pre-Registered)** | Uji kontrol plasebo temporal mendeteksi pembaur atau tren semu. | $\beta_{t+1} = +0.0041$, $95\%\text{ CI } [-0.075, +0.083]$. Nilai mendekati nol, konsisten dengan absennya tren semu eksplisit (namun dengan catatan daya rendah). |
| **EXP_05** | Cabai | Depresiasi Titik Embun ($T_{\min} - T_d$) | Bulanan (2015–2024) | **Terdaftar Tier B (H_HORT_01)** | Pre-registrasi persentil $P_{10}$ per sel/bulan untuk deteksi kelembapan embun malam. | Frekuensi hari $\le P_{10}$ tepat 10.0% per bulan per sel, berhasil mengeliminasi distorsi ambang absolut 2.0°C (yang menandai 62.7% hari). |
| **EXP_06** | Presipitasi | Anomali Bulanan AgERA5 vs CHIRPS | 2016, 2020, 2024 (36 Bulan) | **Audit Blocker A2/B3** | Validasi koherensi sinyal anomali bebas musim (*deseasonalized*). | Korelasi Pearson $r = 0.50\text{ s.d. }0.80$ (median 0.73). Mengonfirmasi koherensi moderat-kuat tanpa inflasi musiman. |

---

## 2. Batasan Metodologis Ketat yang Dipatuhi Selama EDA

1. **Eksklusi Tahun 2022**:
   - Seluruh pemodelan utama mengecualikan tahun 2022 karena bukti kuat imputasi buatan (13 kabupaten memiliki yield jagung persis 75.70 ku/ha dan SD kedelai menyusut ke 0.19 ku/ha).
   - Titik 2022 hanya dimunculkan pada grafik diagnostik integritas sebaran untuk mendokumentasikan anomali data dinas.
2. **Ketiadaan Nilai P-Value**:
   - Sesuai ATURAN KERAS No. 5 dan panduan PhD Data Scientist, tidak ada $p$-value yang dilaporkan atau dijadikan kriteria inferensi dalam EDA.
   - Seluruh diagnostik menyajikan **Effect Size ($\beta$)**, **95% Confidence Interval**, dan **Minimum Detectable Effect (MDE)**.
3. **Penolakan Sampel 27 Unit Independen**:
   - Analisis dependensi spasial membuktikan PC1 dan PC2 menjelaskan $>75\%$ varians presipitasi bersama di Jawa Barat, dengan korelasi spasial rata-rata $r > 0.75$.
   - Peneliti dilarang memperlakukan 27 kabupaten/kota sebagai 27 sampel independen. Derajat bebas spasial riil Jawa Barat ditaksir hanya setara dengan 3 hingga 4 klaster iklim independen.
4. **Isolasi Tier B (Cabai & Tomat)**:
   - Tidak ada regresi hasil panen terhadap cuaca yang diestimasi untuk komoditas hortikultura (karena data hasil hanya tersedia dalam 8 titik tahun provinsi).
   - Tidak ada model Machine Learning supervised yang dilatih untuk penyakit tanaman (karena label kejadian OPT absen 100%).
