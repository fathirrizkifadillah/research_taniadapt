# TaniAdapt Research Dossier — Phase 0: Problem Definition & Architectural Scope

**Status**: PENDING_USER_RATIFICATION  
**Cakupan Spasial**: 27 Kabupaten/Kota Jawa Barat (18 Sentra Pangan & Hortikultura)  
**Pengguna Sasaran**: Petani Kecil (*Smallholders*) & Pengelola Kebun Agribisnis (*Farm Managers*)  
**Penanggung Jawab Riset**: Tim Riset Biofisik & Rekayasa Perangkat Lunak TaniAdapt  

---

## 1. Konteks dan Realitas Krisis Iklim di Lahan Jawa Barat
Pertanian tanaman pangan dan hortikultura di Jawa Barat menyumbang porsi vital terhadap ketahanan pangan nasional (lumbung beras Pantura, jagung priangan timur, dan sentra sayuran dataran tinggi Bandung-Garut). Namun, pelaku usaha tani di lapangan menghadapi krisis agrometeorologi yang kian parah akibat perubahan iklim global:

1. **Keruntuhan Kalender Tanam Statis & Pranata Mangsa**:
   * Sistem penanggalan tanam tradisional dan rekomendasi kalender tanam statis (seperti KATAM berbasis kalender) kerap meleset karena variabilitas monsun dan telekoneksi iklim makro (El Niño, La Niña, Dipole Mode Samudera Hindia / IOD).
   * Pergeseran awal musim hujan (awal Oktober yang bergeser ke akhir November atau Desember) menyebabkan petani menanam terlalu dini, berujung pada kematian benih di persemaian akibat kekeringan mendadak, atau sebaliknya terendam banjir rob di awal fase vegetatif.
2. **Ketiadaan Rekomendasi Presisi Skala Harian & Jam (*Diurnal Mismatch*)**:
   * Prakiraan cuaca publik (BMKG umum atau aplikasi komersial cuaca ponsel) hanya memberikan informasi cuaca makro agregat (seperti "Cerah Berawan, 28°C, Hujan Ringan"), tanpa menerjemahkan kondisi tersebut ke dalam implikasi mekanik tanah dan fisiologi tanaman.
   * Petani tidak tahu: Apakah tanah sudah mencapai kapasitas lapang? Kapan jendela jam terbaik untuk menyiram agar air tidak menguap sia-sia karena terik radiasi matahari? Kapan waktu menyemprot fungisida/insektisida agar tidak tercuci hujan dalam 3 jam ke depan dan tidak terhempas angin (*spray drift*)?
3. **Bahaya Fatal Halusinasi Model AI Generatif (LLM)**:
   * Gelombang kecerdasan buatan generatif komersial (ChatGPT, Gemini, Claude) sering dimanfaatkan secara keliru untuk konsultasi pertanian tanpa pembatas ilmiah (*guardrail*).
   * LLM murni bersifat stokastik dan berbasis *next-token prediction*, sehingga sangat rentan mengarang (*hallucinate*) formula, dosis pestisida, batas suhu, atau tanggal tanam palsu yang terdengar meyakinkan namun salah secara biofisika. Dalam dunia agrikultur, kesalahan rekomendasi semacam ini dapat memusnahkan seluruh modal panen petani kecil.

---

## 2. Paradigma Solusi: Arsitektur Sistem Terpisah (*Decoupled Architecture*)
TaniAdapt dibangun dengan mematuhi prinsip pemisahan tegas antara otak keputusan biofisik dan antarmuka komunikasi:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TANIADAPT DECOUPLED ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. DATA LAYER:                                                              │
│    AgERA5 Reanalysis (1991–2024), CHIRPS, DEM SRTM, BPS Panel, BMKG History │
│                                  ↓                                          │
│ 2. DETERMINISTIC DECISION ENGINE (OTAK BIOFISIK MEKANISTIK):                │
│    - Neraca Air Penman-Monteith (FAO-56 ET0) & Koefisien Tanaman Kc         │
│    - Proksi Mikroklimat Spora Fajar P10 (Depresi Titik Embun)               │
│    - Evaluasi Cuaca Diurnal Jam 06.00–18.00 WIB (Angin, Hujan, Radiasi, VPD)│
│    - Kontrak Bukti Ilmiah: Strict "evidence_insufficient" Safeguard       │
│                                  ↓ (Payload JSON Terstruktur)               │
│ 3. COMMUNICATION & EXPLANATION LAYER (LLM & SUARA):                         │
│    - Menerjemahkan Keputusan Menjadi Bahasa Petani Lokal yang Ramah         │
│    - Menguraikan Rekam Jejak Keputusan (Decision Trace)                     │
│    - DILARANG MENGARANG ANGKA, DOSIS RACUN, ATAU AMBANG SENDIRI!            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Matriks Sentra Pertanian dan Profil Geospasial
TaniAdapt mengintegrasikan 27 Kabupaten/Kota Jawa Barat yang dipetakan ke 22 sel cuaca unik berukuran $0.1^\circ 	imes 0.1^\circ$ (~10 km) dengan koreksi orografis topografi dari Digital Elevation Model (SRTM DEM):

| Wilayah Sentra | Elevasi Centroid | Tipe Topografi | Karakteristik Agrometeorologi Utama |
|---|:---:|:---:|---|
| **Pantura (Indramayu, Subang, Karawang)** | 7 – 45 mdpl | Dataran Rendah Pesisir | Suhu tinggi ($27–34^\circ	ext{C}$), radiasi matahari kuat, lumbung padi sawah irigasi, rentan kekeringan MK2 & banjir rob. |
| **Priangan Barat (Cianjur, Sukabumi, Bogor)** | 150 – 580 mdpl | Dataran Sedang Berbukit | Curah hujan orografis tinggi, sentra padi pandanwangi, jagung, dan sayuran semusim. |
| **Priangan Tengah (Bandung, Bandung Barat)** | 680 – 1.341 mdpl | Dataran Tinggi Pegunungan | Suhu sejuk ($16–25^\circ	ext{C}$), kelembapan tinggi, kabut fajar tebal, sentra tomat & hortikultura sayuran daun. |
| **Priangan Timur (Garut, Tasikmalaya, Ciamis)** | 450 – 850 mdpl | Lembah Vulkanik | Sentra utama cabai merah, cabai rawit, jagung pipil, dan kedelai; rentan spora jamur embun fajar. |

---

## 4. Prinsip Integritas Riset TaniAdapt
1. **Evidence First**: Seluruh status agronomi wajib memiliki dasar bukti empiris atau literatur yang terverifikasi di `evidence_registry.csv`.
2. **Anti-P-Hacking**: Seluruh hipotesis dipra-daftarkan sebelum pengujian panel statistik dijalankan.
3. **Kejujuran Terhadap Keterbatasan Bukti**: Apabila data lokal tidak memadai untuk menarik kesimpulan kausal bebas bias, sistem wajib menyatakan **`evidence_insufficient`** dan menolak membuat rekomendasi spekulatif.
4. **Pembersihan Klaim Absolut**: Dilarang menggunakan istilah klaim kausalitas mutlak; seluruh temuan observasional dilaporkan secara proporsional sebagai "mengindikasikan", "menunjukkan", atau "mengonfirmasi secara empiris".
