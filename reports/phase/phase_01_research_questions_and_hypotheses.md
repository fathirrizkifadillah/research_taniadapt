# TaniAdapt Research Dossier — Phase 1: Research Questions & Documented Hypotheses

**Status**: PENDING_USER_RATIFICATION  
**Dokumen Induk**: `docs/hypotheses.md`  
**Catatan Integritas Prapendaftaran**: Hipotesis didokumentasikan (*post-data-access documentation*). Commit pertama `docs/hypotheses.md` tercatat pada commit `4629ad9` (2026-10-11 14:25:00 +0700), sedangkan penelusuran dan akses dataset awal di repositori telah berlangsung lebih awal sejak commit `0d53072` (2026-10-05 21:35:12) hingga `9c600fe` (2026-10-06 01:10:34). Oleh karena itu, dokumen ini secara jujur diposisikan sebagai dokumentasi hipotesis eksploratori terdaftar, bukan pra-registrasi sebelum akses data.

---

## 1. Tiga Pertanyaan Riset Utama (Research Questions)

### RQ1: Sensitivitas Agrometeorologis Hasil Panen
*Apakah fluktuasi anomali cuaca musiman (suhu rata-rata, presipitasi fenologi, VPD, dan hari kering) memiliki dampak statistik yang terukur secara signifikan terhadap produktivitas tahunan tanaman pangan di Jawa Barat pada skala kabupaten?*

### RQ2: Daya Generalisasi Out-of-Sample Model Prediktif
*Apakah model ekonometrika linier teratur maupun model machine learning non-linier memiliki daya prediksi out-of-sample (antar-tahun) yang memadai untuk meramalkan hasil panen, ataukah variabilitas data tahunan BPS/Dinas didominasi oleh faktor kebisingan administratif dan variasi agronomi mikro di luar cuaca makro?*

### RQ3: Validitas Operasional Pendekatan Mekanistik vs Regresi Hasil
*Dapatkah model neraca air biofisik Penman-Monteith (FAO-56) dan proksi mikroklimat kondensasi daun fajar ($P_{10}$) memberikan sinyal risiko operasional harian yang lebih dapat dipertanggungjawabkan bagi petani kecil dibanding model peramalan hasil panen?*

---

## 2. Prapendaftaran 11 Hipotesis Ekonometrika Fenologi (Pre-registered Hypotheses)

Untuk mencegah bias seleksi model (*p-hacking*), seluruh hipotesis fenologis didaftarkan secara transparan sebelum estimasi dilakukan:

| ID Hipotesis | Komoditas | Jendela Fenologi Kritis | Prediktor Agrometeorologi | Tanda Hipotesis | Mekanisme Fisiologis Tanaman |
|---|---|---|---|:---:|---|
| **H_CORN_01** | Jagung | Vegetatif Awal (Feb–Apr) | Presipitasi Terakumulasi ($P_{\text{veg}}$) | **(+)** | Air yang cukup memicu pembentukan daun dan biomassa fotosintesis awal. |
| **H_CORN_02** | Jagung | Pertumbuhan Aktif (Mar–Mei) | Suhu Rata-rata ($T_{\text{mean}}$) | **(-)** | Suhu di atas batas optimum meningkatkan laju respirasi pemeliharaan dan memperpendek fase pengisian biji. |
| **H_CORN_03** | Jagung | Pembungaan/Silking (Apr–Jun) | VPD Maksimum ($VPD_{\text{max}}$) | **(-)** | Tekanan uap jenuh tinggi mengeringkan rambut tongkol (*silk drying*) dan menurunkan viabilitas serbuk sari. |
| **H_CORN_04** | Jagung | Pemasakan/Ripening (Mei–Jul) | Consecutive Dry Days ($CDD$) | **(-)** | Hari kering berkepanjangan selama pengisian biji memicu aborsi bulir (*kernel abortion*). |
| **H_RICE_01** | Padi | Musim Hujan Awal (Okt–Jan) | Presipitasi Musim Hujan ($P_{\text{mh}}$) | **(Cap)** | Kebutuhan air sawah tergenang; memiliki batas saturasi di mana kelebihan hujan memicu banjir/rebah. |
| **H_RICE_02** | Padi | Musim Kemarau I (Mar–Mei) | Suhu Maksimum ($T_{\text{max}}$) | **(-)** | Suhu $> 35^\circ\text{C}$ saat pembungaan pagi memicu sterilitas bulir gabah hampa (*spikelet sterility*). |
| **H_RICE_03** | Padi | Akhir MK1 (Apr–Jun) | Hari Kering Berurutan ($CDD_{\text{mk1}}$) | **(-)** | Ketiadaan hujan saat pengisian malai menyebabkan retakan tanah sawah dan gagal panen (*puso*). |
| **H_RICE_04** | Padi | Puncak Musim Hujan (Des–Feb) | Radiasi Surya ($Rad_{\text{mh}}$) | **(+)** | Tutupan awan tebal mengurangi radiasi aktif fotosintesis (PAR), menurunkan pembentukan anakan produktif. |
| **H_SOY_01** | Kedelai | Pengisian Polong (Jun–Agu) | Presipitasi Polong ($P_{\text{pod}}$) | **(+)** | Kekurangan air pada fase R3–R5 menyebabkan polong hampa dan ukuran biji kerdil. |
| **H_SOY_02** | Kedelai | Pemasakan Biji (Jul–Sep) | Suhu Malam Tropis ($T_{\text{min}}$) | **(-)** | Suhu malam hangat meningkatkan konsumsi respirasi malam hari dan mengurangi akumulasi minyak/protein. |
| **H_SOY_03** | Kedelai | Panen Fisiologis (Agu–Okt) | Frekuensi Hujan Lebat ($R20$) | **(-)** | Hujan saat polong kering memicu kebusukan polong, pembusukan jamur, dan perkecambahan di polong. |

---

## 3. Protokol Inferensi Ekonometrika yang Ditetapkan
1. **Spesifikasi Model Utama**:
   $$\ln(Y_{it}) = lpha_i + \gamma_t + eta \cdot W_{it} + arepsilon_{it}$$
   Di mana $lpha_i$ adalah *Kabupaten Fixed Effects* (mengontrol kualitas tanah, topografi, dan budaya lokal permanen), dan $\gamma_t$ adalah *Year Fixed Effects* (mengontrol guncangan makro nasional, subsidi pupuk, dan tren varietas).
2. **Koreksi Galat Standar Klaster Kecil**:
   * Jumlah klaster kabupaten di Jawa Barat adalah $G = 18$ (kurang dari batas asimtotik $G=30$–$50$).
   * Standar *Cluster-Robust Standard Errors* (CRSE) standar akan menghasilkan *downward bias* (nilai p terlalu optimis palsu).
   * Ditetapkan secara wajib: **Wild Cluster Bootstrap Webb 6-point ($B=999$ pengulangan)** untuk menghitung interval kepercayaan 95% yang valid.
3. **Analisis Daya Statistik Minimum Detectable Effect (MDE)**:
   $$	ext{MDE} = (t_{lpha/2} + t_{1-\kappa}) 	imes 	ext{SE}_{	ext{bootstrap}} pprox 2.80 	imes 	ext{SE}$$
   Jika nilai estimasi $|\hat{eta}| < 	ext{MDE}$, peneliti **DILARANG** mengklaim bahwa "cuaca tidak berpengaruh", melainkan wajib menyimpulkan bahwa data tidak memiliki daya statistik yang cukup (**`evidence_insufficient`**).
