# Kontrak Antarmuka Pengguna TaniAdapt (UI Contract) Phase 13 Milestone 3 (M3)

> **Sasaran Pembaca:** Rekan Tim Pengembang Frontend & Fullstack Web (`taniadapt-web`)  
> **Status Dokumen:** `PENDING_HUMAN` (Menunggu pengesahan pengguna; dilarang mencantumkan status RATIFIED)  
> **Versi Kontrak:** `v2.4-m3-additive` | **Skema:** `JSON Schema Draft 2020-12`  
> **Prinsip Utama:** 100% Aditif & Opsional — Komponen UI lama (`src/components/`, `src/app/**/*.tsx`) **TIDAK DIUBAH SECARA DESTRUKTIF**. Seluruh field baru bersifat opsional pada payload respons.

---

## 1. Ringkasan Perubahan untuk Tim Frontend

Halo Rekan Tim Frontend! 

Pada Milestone 3 (M3) ini, Decision Engine TaniAdapt memperluas kapabilitas saintifik bio-mekanistiknya tanpa mematahkan (*zero-breaking-change*) tampilan yang telah kalian bangun. Seluruh penambahan data di level API (`POST /api/advisory`) bersifat **aditif** (field opsional baru yang melengkapi data sebelumnya).

### Yang Perlu Kalian Ketahui:
1. **Komponen UI Eksisting Tetap Berfungsi Normal**: Kode kalian di `Dashboard.tsx`, `EvaluationCard.tsx`, `HourlyTimeline.tsx`, dan `WeatherInfo.tsx` tidak akan rusak karena skema tetap mempertahankan semua field wajib versi sebelumnya.
2. **Tidak Ada Tebak Dosis / Racun Kimia**: Engine tetap 100% menolak merek dagang pestisida sintetis dan dosis mililiter/sendok makan. Semua peringatan hama/penyakit tetap diarahkan ke pemeriksaan lapangan (*scouting*) dan konsultasi Petugas Penyuluh Lapangan (PPL).
3. **Penyediaan Fitur Baru di Lapis 1 & Lapis 2**:
   - Simulasi proyeksi deplesi air 7 hari ke depan (`proyeksi_7hari`).
   - Penanganan ketidakpastian air tanah awal (*cold-start water ledger*) (`dr_awal_status`, `dr_interval_mm`).
   - Uji sensitivitas curah hujan efektif 80% vs 100% (`sensitif_terhadap_asumsi_hujan_efektif`).
   - Pencegahan perbandingan persentil beda sumber data cuaca (`relative_rank: null`).

---

## 2. Rincian Field Aditif Baru pada Payload Engine

Respons dari endpoint `POST /api/advisory` kini dapat memuat field-field opsional berikut:

### A. Proyeksi Neraca Air 7 Hari (`proyeksi_7hari`)
Engine kini menyimulasikan dinamika deplesi air tanah $D_r$ ke depan selama 7 hari berdasarkan prakiraan cuaca harian Open-Meteo.

- **Tipe Data**: `Array<ProyeksiHariItem>` (panjang 7 elemen)
- **Struktur Tiap Elemen**:
  ```typescript
  interface ProyeksiHariItem {
    hari: number;              // Hari ke-1 s.d. 7 (integer)
    tanggal: string;           // Format ISO: YYYY-MM-DD
    dr_prakiraan_mm: number;   // Deplesi air jika terjadi hujan sesuai prakiraan API (mm)
    dr_tanpa_hujan_mm: number; // Skenario terburuk (worst-case): jika tidak turun hujan sama sekali (mm)
    raw_mm: number;            // Ambang batas air siap serap (Readily Available Water) pada hari tersebut (mm)
  }
  ```
- **Field Pendukung**:
  - `hari_pertama_melewati_raw_prakiraan`: `string | null`  
    Tanggal pertama kali deplesi melampaui $RAW$ pada skenario prakiraan hujan. Bernilai `null` jika tidak terjadi stres air dalam 7 hari.
  - `hari_pertama_melewati_raw_tanpa_hujan`: `string | null`  
    Tanggal pertama kali deplesi melampaui $RAW$ jika sama sekali tidak ada hujan. Bernilai `null` jika air tanah tetap aman.
- **Batasan Biofisik (Penting untuk UI)**:
  Simulasi maju berhenti menambah akumulasi deplesi begitu deplesi melampaui $RAW$, karena koefisien cekaman air ($K_s$) belum dimodelkan secara dinamis. Tampilkan ini sebagai indikator peringatan dini (misal: *"Stres air diproyeksikan terjadi pada tanggal 2026-10-18 jika tidak ada hujan"*).

---

### B. Status & Interval Ledger Air Awal (*Cold-Start*)
Ketika petani baru mendaftarkan tanamannya di tengah musim tanam tanpa data kadar air tanah awal yang pasti, engine menjalankan dua lintasan ekstrem ($D_{r0} = 0\text{ mm}$ atau kapasitas lapang, dan $D_{r0} = TAW$ atau titik layu permanen).

- **`dr_awal_status`**: `'pasti' | 'interval'`
  - `'pasti'`: Kedua lintasan telah bertemu/konvergen (misal karena diguyur hujan lebat $\ge TAW$ atau riwayat siram jenuh).
  - `'interval'`: Kedua lintasan belum konvergen, sehingga nilai deplesi berada dalam rentang ketidakpastian.
- **`dr_interval_mm`**: `[number, number] | undefined`
  - Contoh: `[70.0, 95.0]`. Nilai indeks 0 adalah batas deplesi rendah, indeks 1 batas deplesi tinggi.
- **`konvergen_pada`**: `string | null`
  - Tanggal ketika kedua lintasan deplesi mencapai titik temu yang sama.
- **Perilaku Engine Saat Interval Melintasi $RAW$**:
  Jika interval deplesi merentang melintasi batas $RAW$ (sebagian rentang aman, sebagian rentang stres):
  1. Aksi irigasi (`irrigation`) diberikan status `rule_status = 'INSUFFICIENT'`.
  2. Label status: `'Perlu Waspada'`.
  3. Alasan teks: *"Keadaan air tanah belum pasti; tanyakan kapan terakhir disiram atau hujan deras."*
  4. Status top-level engine dijamin **TIDAK BOLEH bernilai `kondisi_stres_abiotik`** (prinsip defensive programming & anti-false alarm).
- **Rekomendasi Tampilan UI**:
  Jika `dr_awal_status === 'interval'`, tampilkan kotak dialog atau saran interaktif:  
  *"Kapan terakhir kali kebun Anda disiram atau diguyur hujan lebat? Masukkan tanggal siram terakhir agar perhitungan air tanah menjadi pasti."*

---

### C. Sensitivitas Asumsi Curah Hujan Efektif (`sensitif_terhadap_asumsi_hujan_efektif`)
Engine menguji ulang neraca air dengan asumsi hujan efektif konservatif ($P_{\text{eff}} = 0.8 \times P$) dibandingkan asumsi standar ($P_{\text{eff}} = 1.0 \times P$).

- **Tipe Data**: `boolean`
- **Makna**:
  - `true`: Kesimpulan cekaman air berubah jika hanya 80% air hujan yang meresap ke zona perakaran.
  - `false`: Kesimpulan stabil terhadap variasi asumsi peresapan air hujan.
- **Rekomendasi Tampilan UI (Lapis 2)**:
  Tampilkan badge peringatan kuning di bawah kartu irigasi (mirip dengan `sensitif_terhadap_asumsi_tanah`):  
  *"⚠️ Rekomendasi sensitif terhadap asumsi peresapan hujan efektif (80% vs 100%)."*

---

### D. Penanganan Null pada Perbandingan Persentil Cuaca (Kelompok C1)
Sesuai aturan audit paritas klimatologi, data **Prakiraan Terkini (Forecast API)** tidak boleh dibandingkan langsung dengan **Arsip Reanalysis 21 Tahun (ERA5 Archive)** karena perbedaan resolusi kisi dan formulasi model numerik.

- **Nilai yang Dikembalikan Engine**:
  ```json
  {
    "id": "air_temperature_2m",
    "value": 28.5,
    "unit": "°C",
    "relative_rank": null,
    "rank_basis": "beda sumber, tidak dibandingkan",
    "rank_basis_n": null,
    "status": "evidence_insufficient",
    "reason": "Sumber data cuaca (OpenMeteo_Forecast_API) tidak sepadan dengan baseline klimatologi (OpenMeteo_ERA5_Archive); perbandingan persentil dibatalkan demi integritas data."
  }
  ```
- **Instruksi Khusus untuk Komponen UI**:
  - Jangan biarkan komponen merender `NaN`, `undefined`, atau progress bar 0% yang rusak!
  - Jika `indicator.relative_rank === null`, sembunyikan progress bar persentil atau tampilkan label abu-abu netral: *"Nilai Prakiraan Terkini (Tanpa Peringkat Historis)"*.

---

## 3. Contoh Lengkap Payload JSON Respons Engine (`POST /api/advisory`)

Berikut adalah contoh payload utuh yang valid terhadap skema `schemas/engine_output.schema.json` (Draft 2020-12):

```json
{
  "crop": "jagung",
  "location": {
    "kabkota": "KABUPATEN SUBANG",
    "cell_id": "CELL_(-6.5, 107.7)",
    "weather_source": "OpenMeteo_ERA5"
  },
  "as_of": "2026-10-14",
  "issue_time": "2026-10-14T06:00:00+07:00",
  "timezone": "Asia/Jakarta",
  "rules_version": "v2.4-verified-params",
  "data_version": "v2.4-verified-params",
  "data_freshness_days": 0,
  "layer": "daily",
  "source_data": "forecast",
  "indicators": [
    {
      "id": "soil_water_depletion_Dr",
      "rule_id": "RULE_WATER_FAO56_DEPLETION",
      "value": 85.0,
      "unit": "mm",
      "relative_rank": null,
      "rank_basis": "beda sumber, tidak dibandingkan",
      "rank_basis_n": null
    }
  ],
  "actions": [
    {
      "action": "irrigation",
      "window": "06.00 - 08.00 WIB",
      "status_label": "Sangat Aman",
      "rule_ids": ["RULE_WATER_FAO56_DEPLETION"],
      "rule_status": "VERIFIED_METHOD",
      "evidence_refs": ["RULE_WATER_FAO56_DEPLETION", "FAO56_RAW_DEPLETION"],
      "reason": "Deplesi air tanah (Dr = 85.0 mm) melampaui air siap serap (RAW = 82.5 mm). Dianjurkan segera melakukan penyiraman."
    },
    {
      "action": "spraying",
      "window": "06.00 - 08.00 WIB",
      "status_label": "Perlu Waspada",
      "rule_ids": ["RULE_SPRAY_WIND_SAFE"],
      "rule_status": "CONVENTION_PENDING",
      "evidence_refs": [],
      "reason": "Kecepatan angin tenang (< 3 km/j), waspadai potensi inversi suhu di permukaan tajuk."
    }
  ],
  "hourly": [
    { "hour": "06.00", "status": "WARN", "reason": "Angin tenang < 3 km/j" },
    { "hour": "07.00", "status": "SAFE", "reason": "Kondisi operasional optimal" },
    { "hour": "12.00", "status": "WARN", "reason": "Radiasi surya terik > 500 W/m²" }
  ],
  "status": "kondisi_stres_abiotik",
  "evidence_tier": "published_model",
  "evidence_refs": ["RULE_WATER_FAO56_DEPLETION", "FAO56_RAW_DEPLETION"],
  "claim_allowed": "Terdeteksi indikasi cekaman air perakaran (Dr > RAW); tindakan siram dianjurkan.",
  "claim_forbidden": ["prediksi hasil panen kuantitatif", "rekomendasi dosis bahan kimia sintetis"],
  "limitations": [
    "Model deplesi air menggunakan asumsi evapotranspirasi standar FAO-56 Penman-Monteith.",
    "Nilai Kc belum dikoreksi kelembapan relatif minimum dan kecepatan angin harian lokal."
  ],
  "action_ids": ["irrigation", "spraying"],
  "sensitif_terhadap_asumsi_tanah": false,
  "sensitif_terhadap_asumsi_hujan_efektif": true,
  "asumsi_deplesi_awal_dr0": 80.0,
  "dr_awal_status": "pasti",
  "konvergen_pada": "2026-10-10",
  "proyeksi_7hari": [
    { "hari": 1, "tanggal": "2026-10-15", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 },
    { "hari": 2, "tanggal": "2026-10-16", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 },
    { "hari": 3, "tanggal": "2026-10-17", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 },
    { "hari": 4, "tanggal": "2026-10-18", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 },
    { "hari": 5, "tanggal": "2026-10-19", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 },
    { "hari": 6, "tanggal": "2026-10-20", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 },
    { "hari": 7, "tanggal": "2026-10-21", "dr_prakiraan_mm": 85.0, "dr_tanpa_hujan_mm": 85.0, "raw_mm": 82.5 }
  ],
  "hari_pertama_melewati_raw_prakiraan": "2026-10-15",
  "hari_pertama_melewati_raw_tanpa_hujan": "2026-10-15"
}
```

---

## 4. Panduan Higienitas Kalimat & Pelindung Teks (Guardrails)

Bagi pengembang yang mengintegrasikan fitur narasi suara atau kartu penjelas:

### A. Kata Terlarang vs Kata yang Dianjurkan
| Kata Terlarang (DILARANG KERAS) | Frasa Aman yang Dianjurkan | Alasan Ilmiah |
|---|---|---|
| "Membuktikan" / "Terbukti" | "Menunjukkan" / "Mengindikasikan" | Analisis observasional tidak membuktikan kausalitas deterministik. |
| "0% Halusinasi" / "100% Akurat" | "Penanganan degradasi terdefinisi" / "Deterministik berbasis aturan" | Mencegah klaim berlebihan (*over-claim*) di hadapan juri dan akademisi. |
| "Tervalidasi sempurna" | "Sesuai tolok ukur benchmark FAO-56" | Kejujuran batas kalibrasi in-situ. |
| Merek racun (Antracol, Daconil, Regent, Roundup, dll.) | "Konsultasikan bahan pengendali dengan Petugas Penyuluh Lapangan (PPL)" | Tanggung jawab keselamatan agronomis & hukum. |
| Dosis takaran ("2 ml/liter", "1 kg/ha", "3 sdm") | "Lakukan pemantauan gejala fisik di lapangan (scouting)" | Dosis bergantung pada tingkat keparahan serangan dan formulasi resmi terdaftar. |

### B. Templat Jawaban Topik di Luar Lingkup (Out-of-Scope)
Jika antarmuka menerima pertanyaan di luar domain agrometeorologi biofisik:
- **Tebak Hasil Panen (Yield Prediction)**:  
  *"TaniAdapt tidak menyediakan estimasi tonase hasil panen kuantitatif. Model cuaca murni tidak memiliki daya prediktif out-of-sample untuk hasil panen tahunan. Konsultasikan potensi hasil dengan Petugas Penyuluh Lapangan (PPL) setempat."*
- **Prediksi Harga Pasar**:  
  *"TaniAdapt berfokus pada panduan agrometeorologi biofisik dan tidak memprediksi harga komoditas pasar. Pantau Pusat Informasi Harga Pangan Strategis (PIHPS) atau hubungi PPL setempat."*
- **Keracunan / Bahaya Kimia**:  
  *"Peringatan keselamatan medis: TaniAdapt bukan layanan medis darurat. Segera bawa korban keracunan ke Puskesmas atau rumah sakit terdekat beserta label/wadah kemasan bahan kimia."*
- **Sengketa Lahan / Agraria**:  
  *"Pertanyaan hukum agraria dan sengketa lahan berada di luar lingkup TaniAdapt. Silakan berkonsultasi dengan kantor dinas pertanian atau penyuluh setempat (PPL)."*

### C. Normalisasi Teks untuk Suara (Text-to-Speech)
Gunakan fungsi pembantu `normalizeForSpeech` dari `@/lib/narration` untuk mengubah singkatan teknis menjadi ucapan alami sebelum dikirim ke mesin sintesis suara (Web Speech API / TTS):
- `"06.00 - 08.00 WIB"` $\to$ `"pukul enam sampai delapan Waktu Indonesia Barat"`
- `"km/j"` atau `"km/jam"` $\to$ `"kilometer per jam"`
- `"mm"` $\to$ `"milimeter"`
- `"°C"` $\to$ `"derajat Celsius"`
- `"RH"` $\to$ `"kelembapan udara"`

---

## 5. Ringkasan Tindakan untuk Tim Frontend
- [x] Pastikan build aplikasi tetap hijau (`npm test` dan `npm run build` lulus).
- [ ] Opsional: Tambahkan komponen visual mini untuk menampilkan grafik garis/bar `proyeksi_7hari` di bawah kartu irigasi.
- [ ] Opsional: Render badge `sensitif_terhadap_asumsi_hujan_efektif` di Lapis 2 kartu irigasi.
- [ ] Pastikan penanganan `relative_rank: null` tidak merusak bar indikator cuaca.
