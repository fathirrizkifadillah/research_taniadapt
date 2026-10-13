# Registri Aturan Operasional Decision Engine (Rules Register)

**Versi Aturan:** `v2.2-honest-status`  
**Status Audit:** Mengikat (*Contractual*)  
**Prinsip Desain:** Bebas Ambang Buatan Sendiri, Transparansi Status Bukti, dan Penegakan Batasan Ilmiah  

Dokumen ini mencatat seluruh aturan keputusan operasional yang dijalankan oleh Decision Engine TaniAdapt. Setiap aturan wajib memiliki `id`, `action`, kondisi terstruktur, `unit`, `evidence_id`, `status` bukti, `crop_scope`, dan `source_data`.

---

## 1. Definisi Tiga Status Bukti Aturan

1. **`VERIFIED`**:
   * Aturan yang diturunkan secara langsung dari literatur primer terakreditasi internasional yang naskah aslinya telah diverifikasi secara numerik dan independen (misalnya formula Penman-Monteith FAO-56 Eq. 6 dan kriteria deplesi lengas tanah $D_r > RAW = p \times TAW$ dari FAO-56 Bab 8 Tabel 19 & 22).
   * Diizinkan memicu status operasional dan peringatan stres biofisik.
2. **`CONVENTION_PENDING`**:
   * Aturan heuristik atau konvensi agrometeorologi lapangan yang umum dipakai dalam praktik penyuluhan/lapangan namun **belum dikalibrasi terhadap data pengukuran tanah/lapangan lokal in-situ di Jawa Barat** (misalnya batas angin semprot 12–15 km/j, batas hujan pupuk 8 mm/12 jam, ambang CWB -25/-50 mm, atau proksi embun fajar $P_{10}$).
   * Pada antarmuka pengguna (UI), aturan berstatus ini **wajib diberi badge netral / kuning: "Aturan umum — belum diverifikasi sumber resmi"** dan dilarang mengklaim dirinya sebagai ambang biofisik yang terkonvensi, belum dikalibrasi terhadap data lapangan.
3. **`INSUFFICIENT`**:
   * Aturan yang memiliki keterbatasan parameter fundamental atau ketiadaan model dasar lokal (misalnya modul penyiraman padi sawah yang mengasumsikan sawah tergenang, atau komoditas tanpa nilai $K_c$ terverifikasi).
   * Engine **wajib mengembalikan status `evidence_insufficient`** dan melarang keluarnya rekomendasi tindakan sembarangan.

---

## 2. Tabel Registri Aturan Lengkap (`rules/rules.json`)

| ID Aturan | Tindakan | Kondisi Metrik Terstruktur | Satuan | Status Bukti | Evidence ID | Cakupan Komoditas | Sumber Data | Status Aksi |
|---|---|---|:---:|:---:|:---:|---|:---:|:---:|
| `RULE_WATER_CWB_DROUGHT` | `irrigation` | `cwb_14d < -50.0` | mm | `CONVENTION_PENDING` | `null` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | `DANGER` (Cekaman Defisit) |
| `RULE_WATER_CWB_WARN` | `irrigation` | `-50.0 <= cwb_14d < -25.0` | mm | `CONVENTION_PENDING` | `null` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | `WARN` (Waspada Defisit) |
| `RULE_WATER_CWB_NORMAL` | `irrigation` | `cwb_14d >= -25.0` | mm | `CONVENTION_PENDING` | `null` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | `SAFE` (Lengas Cukup) |
| `RULE_WATER_FAO56_DEPLETION` | `irrigation` | `Dr > RAW = p * TAW` | mm | **`VERIFIED`** | `FAO56_RAW_DEPLETION` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | `DANGER` (Stres Lengas) |
| `RULE_WATER_PADI_INSUFFICIENT` | `irrigation` | `ponded_water_depth is null` | mm | **`INSUFFICIENT`** | `null` | Padi Sawah | Forecast | `WARN` (`evidence_insufficient`) |
| `RULE_WATERLOGGING_3D` | `drainage_inspection` | `precip_3d_sum >= 100.0` | mm | `CONVENTION_PENDING` | `null` | Semua Komoditas | Reanalysis / Forecast | `DANGER` (Alert Genangan) |
| `RULE_WATERLOGGING_CWD` | `drainage_inspection` | `consecutive_wet_days >= 5` | hari | `CONVENTION_PENDING` | `null` | Semua Komoditas | Reanalysis / Forecast | `DANGER` (Alert Genangan) |
| `RULE_OPT_DAWN_P10_7D` | `scouting_opt` | `dew_dep_p10_days_7d >= 3` | hari | `CONVENTION_PENDING` | `null` | Cabai, Tomat | Reanalysis / Forecast | `WARN` (Scouting Lapangan) |
| `RULE_SPRAY_WIND_SAFE` | `spraying` | `wind_speed < 12.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `SAFE` (Angin Tenang) |
| `RULE_SPRAY_WIND_WARN_TRANSITION` | `spraying` | `12.0 <= wind_speed <= 15.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `WARN` (Transisi / Waspada Drift) |
| `RULE_SPRAY_WIND_DANGER` | `spraying` | `wind_speed > 15.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `DANGER` (Bahaya Drift) |
| `RULE_FERT_RAIN_12H` | `fertilizing` | `precip_12h_forecast >= 8.0` | mm | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `DANGER` (Bahaya Hanyut) |
| `RULE_HARVEST_RH_SAFE` | `harvesting` | `relative_humidity <= 75.0` | % | `CONVENTION_PENDING` | `null` | Padi, Jagung, Kedelai | Forecast | `SAFE` (Kering) |
| `RULE_HARVEST_RH_DANGER` | `harvesting` | `relative_humidity > 85.0` | % | `CONVENTION_PENDING` | `null` | Padi, Jagung, Kedelai | Forecast | `DANGER` (Bahaya Busuk) |
| `RULE_IRRIG_SRAD_HIGH` | `irrigation` | `solar_radiation > 500.0` | W/m² | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `WARN` (Penguapan Cepat) |
| `RULE_IRRIG_SOIL_SATURATED` | `irrigation` | `soil_moisture >= 0.70` | m³/m³ | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `DANGER` (Tanah Jenuh Air) |
| `RULE_SPRAY_TEMP_SAFE` | `spraying` | `temperature < 30.0` | °C | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `SAFE` (Suhu Sejuk) |
| `RULE_PRUNE_RAIN_8H` | `pruning` | `precip_8h_forecast >= 2.0` | mm | `CONVENTION_PENDING` | `null` | Tomat, Cabai | Forecast | `DANGER` (Luka Basah Jamur) |

---

## 3. Catatan Implementasi Kritis

### A. Penutupan Celah Kecepatan Angin (12–15 km/j)
Sebelumnya terdapat celah ambang antara batas aman ($< 12\text{ km/j}$) dan batas bahaya ($> 15\text{ km/j}$).
Aturan `RULE_SPRAY_WIND_WARN_TRANSITION` secara tegas menetapkan rentang $12.0 \le \text{wind} \le 15.0\text{ km/j}$ sebagai status **`WARN` (Perlu Waspada)**: kecepatan angin transisi di mana droplet halus mulai terhempas, sehingga operator wajib merendahkan boom semprot dan menggunakan nosel berbutir kasar (*coarse droplets*). Aturan ini berstatus `CONVENTION_PENDING`.

### B. Penanganan Satuan Lengas Tanah (Soil Moisture)
Model cuaca Open-Meteo mengeluarkan variabel lengas tanah (`soil_moisture_0_to_7cm`) dalam satuan **volumetrik fraksi $m^3/m^3$** (rentang 0.0 s.d. ~0.80), BUKAN persen. Nilai ambang `0.70 m³/m³` merefleksikan kondisi mendekati saturasi air pori tanah. Kode evaluator dilarang membandingkan angka desimal Open-Meteo dengan persen (0–100) tanpa konversi satuan eksplisit.

### C. Modul Air Padi Sawah: Penegakan `evidence_insufficient`
Koefisien tanaman $K_c$ padi sawah dari FAO-56 Tabel 12 ($1.05 \to 1.20 \to 0.75$) mengasumsikan sawah berair tergenang (*standing water layer* 5–10 cm) atau jenuh. Rumus neraca air deplesi tanah tak jenuh ($D_r$) tidak berlaku untuk padi sawah irigasi. Oleh karena itu, modul rekomendasi penyiraman untuk padi sawah **diberi status `evidence_insufficient`** sampai tersedia modul ketinggian genangan air dan perkolasi lokal yang tervalidasi.

### D. Penanganan Bahan Kimia & Dosis Pestisida
Decision Engine **dilarang keras mengeluarkan rekomendasi nama merek dagang, takaran ml/liter, atau dosis racun kimia sintetis**. Untuk seluruh peringatan penyakit tanaman atau sanitasi kanopi, engine hanya memberikan panduan inspeksi fisik (*field scouting*) dan secara otomatis mengeluarkan rekomendasi: *"Konsultasikan pilihan bahan aktif dan dosis resmi dengan Petugas Penyuluh Lapangan (PPL) / Balai Proteksi Tanaman setempat."*
