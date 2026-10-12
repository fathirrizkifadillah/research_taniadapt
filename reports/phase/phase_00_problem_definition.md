# TaniAdapt Research Dossier — Phase 0: Problem Definition

**Status**: COMPLETED / RATIFIED  
**Konteks Wilayah**: Provinsi Jawa Barat (27 Kabupaten/Kota, 18 Sentra Pangan & Hortikultura)  
**Target Pengguna**: Petani kecil (*smallholders*) dan pengelola kebun (*farm managers*)  

---

## 1. Latar Belakang Masalah Riil di Lahan
Petani dan pengelola usaha tani di Jawa Barat menghadapi tantangan agrometeorologis yang semakin tidak menentu akibat anomali iklim tropis (fenomena El Niño, La Niña, IOD positif, serta pergeseran musim hujan/kemarau). Permasalahan utama yang diidentifikasi di lapangan mencakup:
1. **Kegagalan Prediksi Kalender Tanam Tradisional**: Pranata Mangsa dan kalender tanam statis tidak lagi dapat diandalkan karena distribusi curah hujan bulanan mengalami variabilitas ekstrem dan pergeseran awal musim basah.
2. **Ketiadaan Rekomendasi Presisi Skala Harian & Jam**: Informasi cuaca publik dari stasiun meteorologi bersifat makro dan tidak memberikan panduan operasional praktis (kapan tepatnya harus menyiram, memupuk agar tidak tercuci hujan, atau menyemprot agar tidak mengalami *spray drift*).
3. **Bahaya Halusinasi AI Generatif (LLM)**: Model bahasa komersial (ChatGPT, Claude, Gemini) sering kali mengarang (*hallucinate*) anjuran dosis kimia, tanggal tanam, atau diagnosis OPT palsu yang dapat memicu kerugian finansial fatal bagi petani.

---

## 2. Paradigma Solusi TaniAdapt: Decoupled Decision Engine
Untuk mengatasi masalah tersebut secara bertanggung jawab, TaniAdapt merumuskan arsitektur sistem terpisah (*decoupled architecture*):
* **Otak Keputusan (Decision Engine)**: Murni deterministik, biofisik mekanistik (FAO-56 Penman-Monteith, neraca lengas tanah $ET_c = K_c \times ET_0$, proksi mikroklimat fajar $P_{10}$), dan ekonometrika terdaftar. Mesin ini tidak memiliki toleransi halusinasi dan memiliki kewajiban etis menjawab `evidence_insufficient` bila data tidak memadai.
* **Lapisan Bahasa (LLM / Voice Agent)**: Murni bertindak sebagai agen penerjemah dan komunikator ramah petani (*explanation layer* / *decision trace narrator*), dilarang mengarang formula atau angka threshold sendiri.

---

## 3. Batasan Wilayah & Portofolio Sasaran
* **Cakupan Wilayah**: 27 Kabupaten/Kota di Jawa Barat yang dipetakan ke 22 sel cuaca AgERA5 unik dengan koreksi elevasi topografi SRTM DEM (rentang 7 mdpl di Indramayu hingga 1.341 mdpl di Bandung/Garut).
* **Komoditas Fokus**: Padi Sawah, Jagung, Kedelai, Cabai Rawit/Merah, dan Tomat.
