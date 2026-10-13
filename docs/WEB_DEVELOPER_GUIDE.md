# 🌾 Panduan Lengkap Pengembangan Aplikasi TaniAdapt (Web Developer Guide)

> **Untuk Rekan Tim Pengembang Frontend & Fullstack Web TaniAdapt**  
> Repositori: `taniadapt-web` (Next.js 16 + React 19 + TypeScript + Tailwind CSS)  
> Versi Engine: `v2.4-verified-params` | Kontrak Skema: `Draft 2020-12`

---

## 1. Halo Tim Web! Apa Sebenarnya yang Kita Bangun?

Selamat datang di arsitektur **TaniAdapt**! 

TaniAdapt adalah platform **Agricultural Decision Support System (DSS) dan presisi agroadvisory hiperlokal** yang dirancang khusus untuk petani kecil (*smallholders*) dan pengelola kebun di Jawa Barat (Subang, Garut, Indramayu, Lembang, dll.).

### Masalah Nyata yang Kita Selesaikan
Aplikasi cuaca di HP petani saat ini cuma menampilkan ramalan cuaca makro harian (misal: *"Hari ini hujan ringan"*). Informasi itu **tidak memberi tahu petani tindakan apa yang harus diambil jam ini di kebun**:
- *Apakah jam 07.00 pagi ini anginnya aman untuk menyemprot pestisida tanpa racunnya melayang ke tetangga?*
- *Apakah jam 12.00 siang terik matahari aman untuk menabur pupuk atau menyiram tanaman?*
- *Apakah air di dalam tanah sudah habis sampai wajib menyalakan pompa solar irigasi hari ini?*

TaniAdapt hadir untuk menerjemahkan data cuaca per jam menjadi **kartu tindakan operasional lapangan harian** yang ramah dan mudah dipahami petani: **Siram, Semprot, Pupuk, Panen, dan Rawat/Pangkas**.

---

## 2. Prinsip Arsitektur Decoupled (Kenapa Nggak Pakai AI/LLM Langsung?)

Banyak aplikasi pertanian di hackathon terjebak bikin chatbot ChatGPT atau model Machine Learning tebak-tebakan hasil panen (*yield prediction*). **Di TaniAdapt, kita melarang keras hal itu!**

### Mengapa?
1. **Machine Learning Terbukti Gagal Out-of-Sample**: Riset Phase 9 kita telah menguji 6 model ML (termasuk Random Forest). Di data latih model tampak pintar ($R^2 = 0.389$), tapi pas diuji di tahun baru (*Leave-One-Year-Out* CV), performanya **runtuh ke nol ($R^2 = +0.034$)**. Data dinas tahunan didominasi faktor non-cuaca (benih, pupuk subsidi, tikus).
2. **LLM Rawan Halusinasi Numerik**: Pertanian taruhannya modal hidup petani. Kalau chatbot AI mengarang dosis fungisida kimia sintetis, tanaman bisa hangus terbakar atau meracuni lingkungan.

### Arsitektur Decoupled TaniAdapt:
```text
[Input Petani: Tanaman + Tgl Tanam + Lokasi] + [Open-Meteo Weather API per Jam]
                                ↓
┌────────────────────────────────────────────────────────────────────────┐
│ DECISION ENGINE BACKEND (100% Deterministik, Pure TypeScript)           │
│ - Rumus Fisika Air Tanah FAO-56 Penman-Monteith (fao56.ts)            │
│ - Kurva Koefisien Tanaman Dinamis Kc (kc.ts)                          │
│ - Neraca Deplesi Air Tanah Dr vs RAW (waterBalance.ts)                 │
│ - Matriks Jam Operasional 06.00–18.00 WIB (engine.ts)                  │
│ - Terikat Kontrak JSON Schema Draft 2020-12 (engine_output.schema.json)│
└────────────────────────────────────────────────────────────────────────┘
                                ↓
        [Payload JSON Bersih, Aman, & Teruji via Vitest]
                                ↓
┌───────────────────────────────────────┬────────────────────────────────┐
│ LAPIS 1: REKOMENDASI PETANI (UI)      │ LAPIS 2: BUKTI SAINS (UI)      │
│ - Kartu Aksi Visual (Hijau/Kuning)    │ - Badge Rujukan Ilmiah (FAO-56)│
│ - Rekomendasi Jam Terbaik             │ - Flag Sensitivitas Tanah Loam │
│ - Catatan Aksi Praktis Lapangan       │ - Transparansi Bukti Belum Ckp │
└───────────────────────────────────────┴────────────────────────────────┘
                                ↓
[AGEN SUARA / CHATBOT RAG 16 PAPER ILMIAH (Murni Menerjemahkan JSON ke Bahasa Sunda/Indonesia)]
```

---

## 3. Peta 5 Komoditas Terdaftar & Aturan Khususnya

Sistem kita membina **5 komoditas resmi** di Jawa Barat. Perlakuan untuk tiap tanaman **berbeda nyata** sesuai sifat biologisnya:

| Komoditas | Tipe Tanaman | Modul Irigasi (Siram) | Modul Lain (Semprot, Pupuk, Panen, Pangkas) | Catatan Khusus Frontend |
|---|---|:---:|---|---|
| **1. Padi Sawah** (*Oryza sativa*) | Pangan Semusim | **`evidence_insufficient`** (Abu-abu) | **Aktif 100%** (Semprot angin aman, pupuk tanpa hujan lebat, panen kering) | Di sawah Jabar, padi ditanam tergenang air (*ponded*). Rumus deplesi tanah tak jenuh tidak berlaku. Tampilkan badge abu-abu: *"Bukti belum cukup (sawah tergenang)"*. |
| **2. Jagung Pipil** (*Zea mays*) | Pangan Semusim | **Aktif Penuh** (FAO-56 $Z_r=1.0\text{ m}, p=0.55$) | **Aktif 100%** | Panen biji kering lapangan ($RH \le 75\%$). Opsi panen biji kering di batang ($K_c = 0.35$). |
| **3. Kedelai** (*Glycine max*) | Legum Semusim | **Aktif Penuh** (FAO-56 $Z_r=0.8\text{ m}, p=0.50$) | **Aktif 100%** | Siklus tumbuh cepat (85 hari di tropis). Panen polong tua kering ($RH \le 75\%$). |
| **4. Cabai Merah & Cabai Rawit** (*Capsicum spp.*) | Hortikultura Buah Berkala | **`evidence_insufficient`** (Abu-abu) | **Sangat Aktif** (Mitigasi jamur antraknosa LWD, semprot, wiwil tunas air, petik buah) | **CABAI TETAP DIPAKAI PENUH!** Hanya modul siram yang insufficient (karena FAO-56 hanya punya paprika subtropis). Modul jamur fajar, wiwil tunas air, dan panen segar sangat dibutuhkan petani cabai. |
| **5. Tomat** (*Solanum lycopersicum*) | Hortikultura Buah Segar | **Aktif Penuh** (FAO-56 $Z_r=0.7\text{ m}, p=0.40, K_c=0.80$) | **Sangat Aktif** (Mitigasi jamur LWD, wiwil tunas air, panen segar) | Rentan jamur busuk daun fajar jika malam basah ($RH \ge 90\%$). Butuh perempelan tunas air (*pruning*) saat cuaca cerah. |

---

## 4. Struktur Folder & Modul di `taniadapt-web`

```text
taniadapt-web/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── advisory/
│   │   │       └── route.ts          <-- [BACKEND ROUTE] Endpoint utama penilai keputusan
│   │   ├── sumber-dan-batasan/
│   │   │   └── page.tsx              <-- [HALAMAN STATIS] Transparansi lisensi & sumber sains
│   │   ├── layout.tsx
│   │   └── page.tsx                  <-- Dashboard utama aplikasi
│   │
│   ├── components/                   <-- [KOMPONEN UI FRONTEND] Tempat kalian berkreasi!
│   │   ├── Dashboard.tsx             <-- Wadah utama tampilan
│   │   ├── EvaluationCard.tsx        <-- Kartu 5 Aksi (Lapis 1 & Lapis 2)
│   │   ├── HourlyTimeline.tsx        <-- Garis waktu jam operasional 06.00-18.00 WIB
│   │   ├── ActionSelector.tsx        <-- Pilihan tab aksi (Siram, Semprot, Pupuk, dll.)
│   │   ├── WeatherInfo.tsx           <-- Tampilan widget cuaca
│   │   └── VoiceButton.tsx           <-- Tombol mikrofon asisten suara
│   │
│   └── lib/
│       ├── engine/                   <-- [OTAK KEPUTUSAN SAINS] Pure TypeScript (Jangan ubah rumus)
│       │   ├── fao56.ts              <-- Rumus Evapotranspirasi Penman-Monteith (ET0 Eq. 6)
│       │   ├── kc.ts                 <-- Kurva koefisien tanaman dinamis per umur HST
│       │   ├── waterBalance.ts       <-- Neraca deplesi air tanah (Dr vs RAW = p * TAW)
│       │   ├── percentile.ts         <-- Peringkat persentil iklim 21 tahun (P10, P50, P90)
│       │   ├── rules.ts              <-- Pemuat rules.json
│       │   ├── rules.json            <-- Single Source of Truth 21 aturan agrometeorologi
│       │   ├── engine.ts             <-- Orkestrator penilai 5 tindakan & jadwal jam
│       │   └── types.ts              <-- Definisi TypeScript tipe kontrak engine
│       │
│       ├── weather-api.ts            <-- Fetcher Open-Meteo API (Gratis, tanpa API Key)
│       └── storage.ts                <-- LocalStorage logbook & riwayat Water Ledger
│
└── tests/
    └── engine.test.ts                <-- 17 Automated Unit Tests Vitest (Wajib 100% PASS)
```

---

## 5. Cara Frontend Mengambil Data dari Decision Engine

Tim Frontend **TIDAK PERLU** menghitung rumus fisika di komponen React. Cukup lakukan `fetch` ke endpoint Route Handler server kita:

### Request (POST `/api/advisory`)
```typescript
const response = await fetch('/api/advisory', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    crop: 'jagung',                    // 'padi' | 'jagung' | 'kedelai' | 'cabai' | 'tomat'
    latitude: -6.4830,                 // Koordinat lahan
    longitude: 107.7322,
    kabkota: 'KABUPATEN SUBANG',       // Nama wilayah
    planting_date: '2026-09-01',       // Format YYYY-MM-DD (menentukan HST / umur tanaman)
    panen_kering: true,                // Opsional, default true (panen biji kering)
    initial_depletion_dr0_mm: 0.0      // Opsional, default 0 mm (kapasitas lapang)
  }),
});

const data: TaniAdaptEngineOutput = await response.json();
```

### Response JSON yang Diterima Frontend
Payload respons dijamin patuh 100% pada kontrak **JSON Schema Draft 2020-12**:
```json
{
  "crop": "jagung",
  "as_of": "2026-10-13",
  "status": "kondisi_stres_abiotik",
  "actions": [
    {
      "action": "irrigation",
      "window": "06.00 - 08.00 WIB",
      "status_label": "Sangat Aman",
      "rule_status": "VERIFIED_METHOD",
      "evidence_refs": ["RULE_WATER_FAO56_DEPLETION", "FAO56_RAW_DEPLETION"],
      "reason": "Deplesi air tanah (Dr = 90 mm) melampaui air siap serap (RAW = 82.5 mm). Sangat dianjurkan segera menyiram."
    },
    {
      "action": "spraying",
      "window": "06.00 - 08.00 WIB",
      "status_label": "Perlu Waspada",
      "rule_status": "CONVENTION_PENDING",
      "reason": "Kecepatan angin pagi hari tenang (< 3 km/j), waspada inversi termal fajar."
    }
  ],
  "hourly": [
    { "hour": "06.00", "status": "WARN", "reason": "Angin tenang < 3 km/j" },
    { "hour": "07.00", "status": "SAFE", "reason": "Kondisi operasional optimal" },
    { "hour": "12.00", "status": "WARN", "reason": "Radiasi surya terik > 500 W/m²" }
  ],
  "sensitif_terhadap_asumsi_tanah": false,
  "asumsi_deplesi_awal_dr0": 0.0
}
```

---

## 6. Desain Antarmuka Dua Lapis (Two-Layer UI)

Agar petani tidak bingung dan juri/akademisi puas, setiap kartu tindakan di komponen `EvaluationCard.tsx` memiliki **Dua Lapis Visual**:

### Lapis 1: Rekomendasi Ringkas Petani (Farmer-Friendly)
- **Lampu Status Warna**:
  - 🟢 **Sangat Aman (SAFE)**: Kondisi optimal untuk bekerja / tindakan sangat dianjurkan.
  - 🟡 **Perlu Waspada (WARN)**: Zona transisi, sesuaikan teknik semprot/panen atau tunda siram jika air masih cukup.
  - 🔴 **Hindari (DANGER)**: Bahaya angin kencang $>15\text{ km/j}$, hujan lebat $\ge 3\text{ mm}$, atau terik radiasi ekstrem.
  - ⚪ **Bukti Belum Cukup (INSUFFICIENT)**: Untuk air padi atau air cabai.
- **Rentang Waktu Terbaik (`bestWindow`)**: Misal `06.00 - 08.00 WIB`.
- **Panduan Aksi (`reason`)**: Kalimat praktis berbahasa Indonesia lugas.

### Lapis 2: Dasar & Transparansi Bukti Sains (Scientifically Grounded)
- **Badge Status Aturan**:
  - *Badge Hijau*: `✓ Metode terverifikasi (FAO-56)`
  - *Badge Oranye*: `⚠️ Metode belum dikalibrasi (Sentelhas 2008)`
  - *Badge Kuning*: `⏱️ Konvensi tim (aturan praktis)`
  - *Badge Abu-abu*: `ℹ️ Bukti belum cukup`
- **Peringatan Sensitivitas Tanah**:
  - Jika `sensitif_terhadap_asumsi_tanah === true`, tampilkan boks kuning:  
    *"⚠️ Rekomendasi sensitif terhadap variasi rentang jenis tanah loam (TAW 130–180 mm/m)."*
- **Tautan Transparansi**: Arahkan ke `/sumber-dan-batasan` untuk membaca lisensi Open-Meteo CC BY 4.0 dan sitasi FAO-56.

---

## 7. State Management Logbook Petani & Proyeksi 7 Hari

Sistem kita memiliki fitur buku catatan digital di `src/lib/storage.ts`:

1. **Tombol "Tandai Selesai Hari Ini"**:
   - Begitu petani mengklik tombol ini pada kartu Siram, deplesi air tanah $D_{r,0}$ hari berikutnya otomatis direset kembali ke $0\text{ mm}$ (kapasitas lapang).
   - Jika petani menandai kartu Pupuk selesai, frontend otomatis mengunci kartu pupuk selama 14 hari ke depan (*fertilizer lockout*) agar tanah tidak overdosis bahan kimia.
2. **Proyeksi Masa Depan 7 Hari (Forward Simulation)**:
   - Data Open-Meteo menyediakan prakiraan 7 hari ke depan.
   - Tanpa perlu riset baru, engine kita bisa memproyeksikan kapan deplesi air $D_r$ akan menembus batas kritis $RAW$, sehingga web bisa memunculkan kartu peringatan dini:  
     *"Perhatian: Tanaman Anda diproyeksikan mengalami stres kekeringan dalam 3 hari ke depan (hari Kamis). Siapkan pasokan air irigasi."*

---

## 8. Panduan Menjalankan, Menguji, dan Membangun Aplikasi

Pastikan kalian menjalankan perintah-perintah berikut di terminal:

```bash
# 1. Masuk ke direktori web
cd /mnt/c/CODING/TaniAdapt/taniadapt-web

# 2. Menjalankan Development Server (Port 3000)
npm run dev

# 3. Menjalankan Automated Test Suite Vitest (Wajib 17/17 Lulus)
npm test

# 4. Memverifikasi Production Build Next.js (Wajib 0 Error)
npm run build
```

---

## 9. Aturan Integritas Bersama (Zero-Tolerance Rules)

Sebagai tim pengembang TaniAdapt, kita terikat pada etika ilmiah yang ketat:
1. **Dilarang Menambah Angka Magic di Kode UI**: Semua ambang batas cuaca harus berasal dari respons backend engine (`rules.json`), bukan angka tebakan yang diketik manual di komponen React.
2. **Dilarang Merekomendasikan Merk Kimia / Dosis Obat**: Aplikasi dilarang keras menyebut merk dagang pestisida sintetis atau dosis takaran kimia (misal: "campur 2 sendok"). Rujuk selalu petani ke Petugas Penyuluh Lapangan (PPL).
3. **Dilarang Menghilangkan Label "Bukti Belum Cukup"**: Jangan pernah malu menampilkan status abu-abu pada padi atau cabai. Kejujuran sains ini adalah nilai tawar termahal TaniAdapt di depan dewan juri dan akademisi!

Selamat berkarya tim! Desain UI yang cakep, fungsional, dan ramah petani, maka TaniAdapt akan jadi produk juara! 🚀
