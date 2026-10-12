# TaniAdapt Research Dossier — Phase 1: Research Questions & Hypotheses

**Status**: COMPLETED / RATIFIED  
**Prinsip Utama**: Pre-registration, anti-p-hacking, pencegahan manipulasi hipotesis eks-post.

---

## 1. Pertanyaan Riset Utama (Research Questions)
1. **RQ1 (Sensitivitas Cuaca Hasil Panen)**: Sejauh mana anomali agrometeorologi musiman (suhu rata-rata, curah hujan vegetatif, VPD maksimum, hari kering berurutan) secara empiris memengaruhi fluktuasi produktivitas tahunan tanaman pangan di tingkat kabupaten Jawa Barat?
2. **RQ2 (Daya Prediksi Out-of-Sample)**: Apakah model regresi linier maupun machine learning non-linier memiliki daya generalisasi temporal (*out-of-sample*) untuk memprediksi hasil panen dari data cuaca tahunan, ataukah variasi tersebut didominasi oleh faktor non-cuaca (manajemen & pelaporan)?
3. **RQ3 (Keunggulan Pendekatan Mekanistik)**: Apakah neraca air biofisik harian berbasis FAO-56 Penman-Monteith dan proksi mikroklimat fajar $P_{10}$ lebih andal sebagai dasar pemodelan risiko keputusan operasional petani dibanding regresi statistik hasil panen?

---

## 2. Prapendaftaran 11 Hipotesis Ekonometrika (Pre-registered Hypotheses)
Sebelum analisis statistik dijalankan, 11 hipotesis fenologi didaftarkan secara transparan di `docs/hypotheses.md`:
* **Jagung**:
  * `H_CORN_01`: Efek curah hujan vegetatif (Feb–Apr) terhadap yield jagung bertanda positif (+).
  * `H_CORN_02`: Efek suhu rata-rata fase tumbuh (Mar–Mei) bertanda negatif (-).
  * `H_CORN_03`: Efek VPD maksimum fase reproduktif (Apr–Jun) bertanda negatif (-).
  * `H_CORN_04`: Efek hari kering berturut-turut CDD (Mei–Jul) bertanda negatif (-).
* **Padi**:
  * `H_RICE_01`: Curah hujan Musim Hujan (Okt–Jan) memiliki efek batas atas (*saturation threshold*).
  * `H_RICE_02`: Suhu maksimum MK1 (Mar–Mei) menurunkan yield gabah (-).
  * `H_RICE_03`: Kekeringan CDD MK1 (Apr–Jun) menurunkan yield gabah (-).
  * `H_RICE_04`: Radiasi surya MH (Des–Feb) meningkatkan fotosintesis dan yield (+).
* **Kedelai**:
  * `H_SOY_01`: Curah hujan pengisian polong (Jun–Agu) meningkatkan hasil (+).
  * `H_SOY_02`: Suhu malam tinggi (Jul–Sep) meningkatkan respirasi dan menurunkan hasil (-).
  * `H_SOY_03`: Hujan lebat saat pemasakan (Agu–Okt) merusak biji dan menurunkan hasil (-).
