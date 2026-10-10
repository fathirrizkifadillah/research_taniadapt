# TaniAdapt — Unified Decision Engine Output Schema Specification
**Dokumen Desain Sistem & Kontrak Data Antar-Modul**
**Versi:** 2.0 (Phase 5 Evidence-Compliant)
**Prinsip Desain:** *Evidence → Finding → Agronomic Interpretation → Model → Risk → Decision Logic → Structured Output*

---

## 1. Prinsip Desain & Batasan Kritis (Design Philosophy)

1. **Anti-Hallucination & Zero-Guessing:** Decision engine dilarang menebak atau membuat angka ambang batas (*threshold*) sendiri. Apabila bukti ilmiah atau data pendukung lokal tidak memadai, sistem **wajib** mengembalikan status `"evidence_insufficient"`.
2. **Peran LLM + RAG:** LLM dan RAG **hanya berfungsi sebagai generator narasi penjelas** atas objek JSON terstruktur yang dihasilkan oleh deterministic decision engine. LLM dilarang mengubah status, memodifikasi nilai numerik, atau menambahkan klaim probabilitas.
3. **Pemisahan Layer Operasional:**
   - **Layer Musiman (*Seasonal Layer*):** Untuk tanaman pangan (Padi & Jagung) yang berorientasi pada hasil panen (*yield anomaly*), water balance, dan mitigasi risiko fase kritis. Indikator dinyatakan dalam **peringkat relatif / persentil historis** terhadap klimatologi setempat, bukan probabilitas terkalibrasi.
   - **Layer Harian (*Daily Layer*):** Untuk hortikultura (Cabai & Tomat) yang berorientasi pada dinamika harian iklim mikro pendukung penyakit (*favorable weather condition*). Indikator dinyatakan sebagai **jumlah hari akumulatif kondisi kondusif dalam jendela $N$ hari terakhir**.
4. **Larangan Klaim Keras (*Strictly Forbidden Claims*):**
   - DILARANG menyebut keluaran engine sebagai "Probabilitas Serangan Terkalibrasi" untuk penyakit hortikultura (karena tidak ada ground truth label penyakit lapangan).
   - DILARANG mengklaim kehilangan kuantitatif hasil panen (*yield loss kg/ha*) akibat penyakit dari dataset ini.
   - DILARANG mengklaim prediksi hasil panen per musim tanam (MH/MK) dari dataset produktivitas tahunan tanpa pemisahan resmi.

---

## 2. Spesifikasi Skema JSON Tunggal (Unified JSON Schema)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TaniAdaptEngineOutput",
  "type": "object",
  "required": [
    "crop",
    "location",
    "as_of",
    "layer",
    "indicators",
    "status",
    "evidence_tier",
    "evidence_refs",
    "claim_allowed",
    "claim_forbidden",
    "limitations",
    "action_ids"
  ],
  "properties": {
    "crop": {
      "type": "string",
      "enum": ["padi", "jagung", "cabai", "tomat", "bawang_merah", "kedelai"],
      "description": "Komoditas target agro-advisory"
    },
    "location": {
      "type": "object",
      "required": ["kabkota", "cell_id", "weather_source"],
      "properties": {
        "kabkota": { "type": "string", "description": "Nama resmi Kabupaten/Kota di Jawa Barat" },
        "cell_id": { "type": "string", "description": "Identifier grid spasial (contoh: GRID_0.1DEG_-06.57_107.76)" },
        "weather_source": { "type": "string", "description": "Sumber data cuaca yang dikonsumsi (AgERA5_v2, OpenMeteo_ERA5, BMKG_Station)" }
      }
    },
    "as_of": {
      "type": "string",
      "format": "date",
      "description": "Tanggal referensi data pengamatan (YYYY-MM-DD)"
    },
    "layer": {
      "type": "string",
      "enum": ["seasonal", "daily"],
      "description": "Skala temporal operasional advisory"
    },
    "indicators": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "value", "unit", "relative_rank", "rank_basis"],
        "properties": {
          "id": { "type": "string" },
          "value": { "type": ["number", "null"] },
          "unit": { "type": "string" },
          "relative_rank": { 
            "type": ["string", "null"],
            "description": "Peringkat relatif terhadap distribusi klimatologi, contoh: p85, p20, median" 
          },
          "rank_basis": { 
            "type": "string", 
            "description": "Dasar perhitungan persentil, contoh: AgERA5_1981_2020_calendar_window_14d" 
          },
          "sensitivity_estimate": {
            "type": "object",
            "properties": {
              "point_estimate": { "type": "number" },
              "ci_95_lower": { "type": "number" },
              "ci_95_upper": { "type": "number" },
              "unit": { "type": "string" }
            }
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["kondisi_mendukung_OPT", "kondisi_stres_abiotik", "normal", "evidence_insufficient"],
      "description": "Kategori level evaluasi status agroklimat (merupakan konvensi pelaporan relatif, bukan ambang batas bukti mutlak)"
    },
    "evidence_tier": {
      "type": "string",
      "enum": ["data_learned", "published_model", "literature_transfer", "insufficient"],
      "description": "Tingkat pembuktian ilmiah yang mendasari aturan keputusan"
    },
    "evidence_refs": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Daftar referensi literatur atau dataset empiris terverifikasi di repo"
    },
    "claim_allowed": {
      "type": "string",
      "description": "Pernyataan naratif presisi yang diizinkan untuk disampaikan ke pengguna"
    },
    "claim_forbidden": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Daftar klaim yang secara keras dilarang diucapkan oleh sistem/LLM"
    },
    "limitations": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Keterbatasan ilmiah dan data yang harus disertakan dalam transparansi"
    },
    "action_ids": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Rekomendasi tindakan agronomi baku yang dapat dipicu (contoh: ACT_DRAINAGE_CHECK, ACT_WATER_CONSERVATION)"
    }
  }
}
```

---

## 3. Penanganan Ketidaksesuaian Sumber Cuaca (*Live Lag vs Climatology*)

Dalam operasional aplikasi nyata:
1. **Latency AgERA5:** Data resmi Copernicus AgERA5 memiliki jeda rilis berkisar antara 2 s.d. 5 hari di belakang waktu *real-time*.
2. **Kebutuhan Live Advisory:** Aplikasi memerlukan data harian berjalan (*today / live*).
3. **Aturan Baku TaniAdapt:**
   - **Prinsip Konsistensi Distribusi:** Persentil anomali relatif **wajib dihitung terhadap sumber data yang sama**. Jika live advisory mengonsumsi Open-Meteo atau data stasiun BMKG, persentil harus dihitung terhadap kurva klimatologi dari sumber yang sama, atau dilakukan pengukuran *systematic bias/offset* secara periodik.
   - **Pengukuran Offset Otomatis:** Sistem mendokumentasikan bias rata-rata harian (sebagaimana terukur pada Bandung: bias suhu AgERA5 vs Open-Meteo adalah $-0,305^\circ\text{C}$ dan presipitasi $-0,732\text{ mm/hari}$).
   - **Label Transparansi Sumber:** Objek JSON selalu memuat field `weather_source` yang menyatakan secara jujur apakah data bersumber dari reanalisis AgERA5, seamless live API, atau observasi stasiun.

---

## 4. Contoh Konkret per Komoditas (Ground Truth Examples)

### Contoh 1: Padi (Rice) — Layer Musiman (*Seasonal Layer*)
```json
{
  "crop": "padi",
  "location": {
    "kabkota": "KABUPATEN KARAWANG",
    "cell_id": "GRID_0.1DEG_-06.30_107.30",
    "weather_source": "AgERA5_v2"
  },
  "as_of": "2024-03-31",
  "layer": "seasonal",
  "indicators": [
    {
      "id": "cdd_seasonal_days",
      "value": 4.0,
      "unit": "hari",
      "relative_rank": "p25 (relatif basah)",
      "rank_basis": "AgERA5_2015_2024_MH_window_Oct_Mar",
      "sensitivity_estimate": {
        "point_estimate": -0.14,
        "ci_95_lower": -0.42,
        "ci_95_upper": 0.14,
        "unit": "ku/ha_per_hari_kering"
      }
    },
    {
      "id": "cumulative_rainfall_sowing_window",
      "value": 842.5,
      "unit": "mm",
      "relative_rank": "p78 (curah hujan tinggi)",
      "rank_basis": "AgERA5_2015_2024_MH_window_Oct_Mar"
    }
  ],
  "status": "normal",
  "evidence_tier": "data_learned",
  "evidence_refs": [
    "DS01 (AgERA5 Karawang 2015–2024)",
    "DS03 (Distanhor Padi Jabar 2015–2020)",
    "Paper 12 (Hosokawa et al., 2023 Sci Rep)"
  ],
  "claim_allowed": "Akumulasi hujan fase awal tanam berada pada persentil 78 (di atas rata-rata historis Karawang). Indikator kekeringan musiman terpantau rendah. Sinyal cuaca terhadap fluktuasi panen tahunan berstatus lemah (R2 < 0.10).",
  "claim_forbidden": [
    "Memprediksi angka ton panen musim hujan (MH) secara terpisah",
    "Mengklaim model memiliki akurasi prediksi hasil panen tinggi"
  ],
  "limitations": [
    "Target produktivitas resmi Distanhor berskala tahunan; tidak ada rincian target hasil per musim (MH/MK).",
    "Data cuaca merupakan reanalisis grid 0,1 derajat, bukan sensor mikroklimat petak sawah."
  ],
  "action_ids": [
    "ACT_MAINTAIN_STANDARD_IRRIGATION",
    "ACT_MONITOR_DRAINAGE_OUTLET"
  ]
}
```

---

### Contoh 2: Jagung (Maize) — Layer Musiman (*Seasonal Layer*)
```json
{
  "crop": "jagung",
  "location": {
    "kabkota": "KABUPATEN SUBANG",
    "cell_id": "CENTROID_KAB_SUBANG_-06.57_107.76",
    "weather_source": "AgERA5_v2_extracted_centroid"
  },
  "as_of": "2024-06-30",
  "layer": "seasonal",
  "indicators": [
    {
      "id": "gdd_accumulated_90d",
      "value": 1420.5,
      "unit": "degree_days",
      "relative_rank": "p62 (mendekati normal historis)",
      "rank_basis": "AgERA5_2015_2022_calendar_window_Apr_Jun",
      "sensitivity_estimate": {
        "point_estimate": -1.25,
        "ci_95_lower": -2.80,
        "ci_95_upper": 0.30,
        "unit": "ku/ha_per_100_GDD_anomaly"
      }
    },
    {
      "id": "vpd_flowering_window_mean",
      "value": 1.45,
      "unit": "kPa",
      "relative_rank": "p88 (stres evaporatif tinggi)",
      "rank_basis": "AgERA5_2015_2022_calendar_window_Apr_Jun"
    }
  ],
  "status": "kondisi_stres_abiotik",
  "evidence_tier": "data_learned",
  "evidence_refs": [
    "DS05 (Distanhor Jagung Subang 2015–2022 detrended)",
    "Paper 13 (Heino et al., 2023 Sci Rep - compound hot/dry impact)",
    "Paper 14 (Hu et al., 2024 Env Mod Softw)"
  ],
  "claim_allowed": "Defisit tekanan uap (VPD) fase pembungaan berada di persentil 88 historis Subang (kondisi kering dan evaporasi tinggi). Variasi cuaca dievaluasi dari residu detrending (CV sisa 11,4%).",
  "claim_forbidden": [
    "Mengklaim kenaikan hasil panen Subang 2021-2022 murni dipicu cuaca",
    "Memprediksi hasil panen tanpa memperhitungkan tren teknologi/intensifikasi benih"
  ],
  "limitations": [
    "Produktivitas jagung Subang mengalami patahan struktural tajam 2021-2022 (+56,4%); variasi cuaca hanya menjelaskan porsi residu.",
    "Data cuaca berbasis centroid administratif kabupaten."
  ],
  "action_ids": [
    "ACT_SCHEDULE_SUPPLEMENTAL_IRRIGATION",
    "ACT_REDUCE_EVAPORATION_MULCHING"
  ]
}
```

---

### Contoh 3: Cabai (Chili) — Layer Harian (*Daily Layer*)
```json
{
  "crop": "cabai",
  "location": {
    "kabkota": "KABUPATEN BANDUNG",
    "cell_id": "GRID_0.1DEG_-06.91_107.61",
    "weather_source": "AgERA5_v2"
  },
  "as_of": "2024-11-15",
  "layer": "daily",
  "indicators": [
    {
      "id": "favorable_dew_point_depression_days_7d",
      "value": 5,
      "unit": "hari_dalam_7_hari_terakhir",
      "relative_rank": "p92 (sangat sering basah)",
      "rank_basis": "AgERA5_2015_2024_Nov_window_14d"
    },
    {
      "id": "rh_max_daily_mean_7d",
      "value": 98.2,
      "unit": "%",
      "relative_rank": "p85 (kelembaban jenuh tinggi)",
      "rank_basis": "AgERA5_2015_2024_Nov_window_14d"
    }
  ],
  "status": "kondisi_mendukung_OPT",
  "evidence_tier": "published_model",
  "evidence_refs": [
    "DS01 (AgERA5 Bandung 2015–2024)",
    "Paper 7 (Handhayani et al., 2026 Sci Rep - weather to yield insufficient on annual scale)",
    "Fisika Mikroklimat: Proksi kebasahan daun berbasis Depresi Titik Embun (T - Td <= 2.0 C)"
  ],
  "claim_allowed": "Dalam 7 hari terakhir, terdapat 5 hari dengan kondisi mikroklimat lembap jenuh (T - Td rendah) yang berada pada persentil 92 klimatologi November. Kondisi fisik atmosfer ini kondusif bagi spora jamur daun.",
  "claim_forbidden": [
    "Menyebut sebagai 'Probabilitas Serangan Antraknosa 80%' atau probabilitas terkalibrasi",
    "Mengklaim estimasi kehilangan kilogram cabai",
    "Menggunakan ambang batas sewenang-wenang tanpa atribusi fisika"
  ],
  "limitations": [
    "DS06 tidak memuat label insidensi atau keparahan penyakit lapangan; supervised ML penyakit tidak dapat dilatih.",
    "Depresi titik embun harian adalah proksi kasar atas kebasahan daun malam hari.",
    "Status merupakan konvensi pelaporan atas peringkat relatif kondisi cuaca, bukan bukti serangan aktual di kebun."
  ],
  "action_ids": [
    "ACT_INSPECT_CANOPY_VENTILATION",
    "ACT_CHECK_DRAINAGE_BEDS",
    "ACT_SCOUT_FIELD_SYMPTOMS"
  ]
}
```

---

### Contoh 4: Tomat (Tomato) — Layer Harian (*Daily Layer*)
```json
{
  "crop": "tomat",
  "location": {
    "kabkota": "KABUPATEN BANDUNG BARAT",
    "cell_id": "CENTROID_KAB_BANDUNG_BARAT_-06.84_107.52",
    "weather_source": "AgERA5_v2_extracted_centroid"
  },
  "as_of": "2024-12-05",
  "layer": "daily",
  "indicators": [
    {
      "id": "late_blight_conducive_days_7d",
      "value": 4,
      "unit": "hari_dalam_7_hari_terakhir",
      "relative_rank": "p80 (di atas normal basah)",
      "rank_basis": "AgERA5_2015_2024_Dec_window_14d"
    },
    {
      "id": "mean_temp_conducive_window",
      "value": 19.4,
      "unit": "°C",
      "relative_rank": "optimal_pathogen_range (18-20°C)",
      "rank_basis": "Balitsa Lembang Field Study Literature"
    }
  ],
  "status": "kondisi_mendukung_OPT",
  "evidence_tier": "published_model",
  "evidence_refs": [
    "DS01 (AgERA5 Lembang/KBB 2015–2024)",
    "Balitsa Lembang (Sastrahidayat & Djauhari, 2014 - Epidemiologi P. infestans)",
    "Paper 5 (Fenu & Malloci, 2021 - Review SimCast model for Solanaceae)"
  ],
  "claim_allowed": "Suhu harian rata-rata 19,4°C dan kelembaban tinggi dalam 4 hari terakhir berada pada rentang optimal perkembangan sporangia hawar daun menurut studi lapangan Balitsa Lembang.",
  "claim_forbidden": [
    "Mengklaim tanaman dipastikan terserang hawar daun",
    "Menyebut persentase risiko terkalibrasi tanpa verifikasi sensor on-farm"
  ],
  "limitations": [
    "Data produktivitas tomat di repo berskala provinsi (N=8); modul penyakit menggunakan transfer mekanistik keluarga Solanaceae.",
    "Mikroklimat kanopi mikro di dataran tinggi Lembang dapat bervariasi signifikan dibanding data kisi 0,1 derajat."
  ],
  "action_ids": [
    "ACT_SCOUT_LATE_BLIGHT_WATER_SOAKED_LESIONS",
    "ACT_IMPROVE_PLANT_SPACING_AIRFLOW",
    "ACT_PREVENTIVE_ORGANIC_OR_RECOMMENDED_FUNGICIDE"
  ]
}
```

---

## 5. Ringkasan Kategori Tindakan Agronomi Baku (`action_ids`)

| Action ID | Nama Tindakan | Sasaran Komoditas | Pemicu Status Engine |
| :--- | :--- | :--- | :--- |
| `ACT_DRAINAGE_CHECK` | Pemeriksaan dan pembersihan parit drainase bedengan | Padi, Cabai, Bawang Merah, Tomat | Curah hujan ekstrem (RX1day / CWD tinggi) |
| `ACT_WATER_CONSERVATION` | Aplikasi mulsa / irigasi suplemen hemat air | Jagung, Kedelai | Hari kering beruntun (CDD p85+) / VPD tinggi |
| `ACT_CANOPY_VENTILATION` | Pemangkasan daun tua & perbaikan sirkulasi udara | Cabai, Tomat | Hari kondusif penyakit ($T - T_d$ rendah $\ge 3$ hari) |
| `ACT_SCOUT_FIELD_SYMPTOMS`| Pengamatan intensif gejala awal di lapangan | Cabai, Tomat, Bawang Merah | Status `kondisi_mendukung_OPT` |
| `ACT_MAINTAIN_STANDARD` | Pemeliharaan rutin standar tanpa intervensi darurat | Seluruh komoditas | Status `normal` |
| `ACT_AWAIT_EVIDENCE` | Menunda rekomendasi spesifik hingga bukti memadai | Seluruh komoditas | Status `evidence_insufficient` |
