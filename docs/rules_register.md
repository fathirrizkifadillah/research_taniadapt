# Registri Aturan Operasional Decision Engine (Rules Register)

**Versi Aturan:** `v2.3-phase13-gate`  
**Status Audit:** Mengikat (*Contractual*)  
**Prinsip Desain:** Bebas Ambang Buatan Sendiri, Transparansi Status Bukti, dan Penegakan Batasan Ilmiah  

Dokumen ini mencatat seluruh aturan keputusan operasional yang dijalankan oleh Decision Engine TaniAdapt. Setiap aturan wajib memiliki `id`, `action`, kondisi terstruktur, `unit`, `evidence_id`, `status` bukti, `crop_scope`, dan `source_data`.

---

## 1. Definisi Status Bukti Aturan

1. **`VERIFIED_METHOD`**:
   * Aturan yang diturunkan secara langsung dari literatur primer terakreditasi internasional yang naskah aslinya telah diverifikasi secara numerik dan independen: formula Penman-Monteith FAO-56 Eq. 6 (p. 65) dan kriteria deplesi lengas tanah $D_r > RAW = p \times TAW$ dari FAO-56 Bab 8 (Tabel 19 p. 165 dan Tabel 22 pp. 167–168).
   * Menjadi **satu-satunya metode biofisik aktif** untuk evaluasi kebutuhan air dan stres kekeringan tanaman di Decision Engine.
2. **`CONVENTION_PENDING`**:
   * Aturan operasional heuristik lapangan yang berstatus: **"aturan praktis ditetapkan tim, tanpa sumber"**.
   * Belum dikalibrasi terhadap data pengukuran sensor tanah/in-situ lokal Jawa Barat.
   * Pada antarmuka pengguna (UI), aturan berstatus ini **wajib diberi badge netral / kuning: "Aturan umum — belum diverifikasi sumber resmi"** dan dilarang mengklaim dirinya sebagai ambang biofisik yang terkalibrasi.
3. **`INSUFFICIENT` / `DEPRECATED`**:
   * `INSUFFICIENT`: Aturan yang memiliki keterbatasan parameter fundamental (misalnya modul penyiraman padi sawah yang mengasumsikan sawah tergenang, atau ambang saturasi tanah yang melebihi batas fisik porositas).
   * `DEPRECATED`: Aturan lama yang dinonaktifkan demi ketaatan arsitektur (misalnya aturan empiris CWB -25/-50 mm yang digantikan oleh FAO-56 depletion).
   * Engine **wajib mengembalikan status `evidence_insufficient`** jika input atau model tidak memadai.

---

## 2. Tabel Registri Aturan Lengkap (`rules/rules.json`)

| ID Aturan | Tindakan | Kondisi Metrik Terstruktur | Satuan | Status Bukti | Evidence ID | Cakupan Komoditas | Sumber Data | Status Aksi & Keterangan |
|---|---|---|:---:|:---:|:---:|---|:---:|:---:|
| `RULE_WATER_FAO56_DEPLETION` | `irrigation` | `Dr > RAW = p * TAW` | mm | **`VERIFIED_METHOD`** | `FAO56_RAW_DEPLETION` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | `DANGER` (Satu-satunya aturan deplesi air aktif) |
| `RULE_WATER_CWB_DROUGHT` | `irrigation` | `cwb_14d < -50.0` | mm | `DEPRECATED` | `null` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | Dinonaktifkan; digantikan oleh FAO-56 RAW. |
| `RULE_WATER_CWB_WARN` | `irrigation` | `-50.0 <= cwb_14d < -25.0` | mm | `DEPRECATED` | `null` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | Dinonaktifkan; digantikan oleh FAO-56 RAW. |
| `RULE_WATER_CWB_NORMAL` | `irrigation` | `cwb_14d >= -25.0` | mm | `DEPRECATED` | `null` | Jagung, Kedelai, Tomat | Reanalysis / Forecast | Dinonaktifkan; digantikan oleh FAO-56 RAW. |
| `RULE_WATER_PADI_INSUFFICIENT` | `irrigation` | `ponded_water_depth is null` | mm | **`INSUFFICIENT`** | `null` | Padi Sawah | Forecast | `WARN` (`evidence_insufficient` sawah tergenang) |
| `RULE_IRRIG_RAIN_ACTIVE` | `irrigation` | `precip_current >= 3.0` | mm | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_IRRIG_VPD_HIGH` | `irrigation` | `vpd > 15.0` | hPa | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `WARN` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_IRRIG_SRAD_HIGH` | `irrigation` | `solar_radiation > 500.0` | W/m² | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `WARN` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_IRRIG_SOIL_SATURATED` | `irrigation` | `soil_moisture_relative_to_fc >= 1.0` | fraction | **`INSUFFICIENT`** | `null` | Semua Komoditas | Forecast | `DANGER` (Dinonaktifkan; 0.70 m³/m³ melebihi porositas tanah) |
| `RULE_WATERLOGGING_3D` | `drainage_inspection` | `precip_3d_sum >= 100.0` | mm | `CONVENTION_PENDING` | `null` | Semua Komoditas | Reanalysis / Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_WATERLOGGING_CWD` | `drainage_inspection` | `consecutive_wet_days >= 5` | hari | `CONVENTION_PENDING` | `null` | Semua Komoditas | Reanalysis / Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_OPT_DAWN_P10_7D` | `scouting_opt` | `dew_dep_p10_days_7d >= 3` | hari | `CONVENTION_PENDING` | `null` | Cabai, Tomat | Reanalysis / Forecast | `WARN` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_SPRAY_WIND_SAFE` | `spraying` | `3.0 <= wind_speed <= 12.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `SAFE` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_SPRAY_WIND_CALM_INVERSION` | `spraying` | `wind_speed < 3.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `WARN` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_SPRAY_WIND_WARN_TRANSITION` | `spraying` | `12.0 <= wind_speed <= 15.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `WARN` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_SPRAY_WIND_DANGER` | `spraying` | `wind_speed > 15.0` | km/j | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_SPRAY_TEMP_SAFE` | `spraying` | `temperature < 30.0` | °C | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `SAFE` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_FERT_RAIN_12H` | `fertilizing` | `precip_12h_forecast >= 8.0` | mm | `CONVENTION_PENDING` | `null` | Semua Komoditas | Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_HARVEST_RH_SAFE` | `harvesting` | `relative_humidity <= 75.0` | % | `CONVENTION_PENDING` | `null` | Padi, Jagung, Kedelai | Forecast | `SAFE` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_HARVEST_RH_DANGER` | `harvesting` | `relative_humidity > 85.0` | % | `CONVENTION_PENDING` | `null` | Padi, Jagung, Kedelai | Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |
| `RULE_PRUNE_RAIN_8H` | `pruning` | `precip_8h_forecast >= 2.0` | mm | `CONVENTION_PENDING` | `null` | Tomat, Cabai | Forecast | `DANGER` (aturan praktis ditetapkan tim, tanpa sumber) |

---

## 3. Catatan Implementasi Kritis

### A. Konfigurasi Parameter FAO-56 Depletion (`RULE_WATER_FAO56_DEPLETION`)
Mengikuti Bab 8 FAO-56 (pp. 161–168), stres lengas tanah terjadi ketika deplesi zona perakaran $D_r$ melampaui $RAW = p \times TAW$:
- $TAW = 1000 \times (\theta_{FC} - \theta_{WP}) \times Z_r$ (Eq. 82 p. 162).
- Default tekstur tanah: *loam* ($\theta_{FC} = 0.27, \theta_{WP} = 0.12, TAW = 150.0\text{ mm/m}$, Tabel 19 p. 165).
- Kedalaman akar efektif $Z_r$: jagung $1.0\text{ m}$, kedelai $1.0\text{ m}$, tomat $1.0\text{ m}$ (Tabel 22 pp. 167–168).
- Fraksi deplesi tanpa stres $p$: jagung $0.55$, kedelai $0.50$, tomat $0.40$ (Tabel 22 pp. 167–168).
- Istilah heuristik "0.7 RAW" secara resmi **DIHAPUS DARI SELURUH DOKUMEN** karena tidak memiliki dasar di FAO-56.

### B. Penutupan Celah Kecepatan Angin (12–15 km/j & Inversi < 3 km/j)
- Angin $< 3.0\text{ km/j}$: `RULE_SPRAY_WIND_CALM_INVERSION` (`WARN`, risiko inversi termal di mana droplet halus melayang).
- Angin $3.0$ s.d. $12.0\text{ km/j}$: `RULE_SPRAY_WIND_SAFE` (`SAFE`, angin tenang dan ideal).
- Angin $12.0$ s.d. $15.0\text{ km/j}$: `RULE_SPRAY_WIND_WARN_TRANSITION` (`WARN`, kecepatan transisi, risiko drift mulai meningkat, gunakan nosel droplet kasar).
- Angin $> 15.0\text{ km/j}$: `RULE_SPRAY_WIND_DANGER` (`DANGER`, bahaya drift tinggi).
Seluruh aturan ini diberi catatan: *"aturan praktis ditetapkan tim, tanpa sumber"*.

### C. Penonaktifan Ambang Tanah Jenuh 0.70 m³/m³
Ambang absolut `0.70 m³/m³` dinonaktifkan (`INSUFFICIENT`) karena nilai tersebut secara fisik melampaui porositas total tanah mineral ($\theta_{\text{sat}} \sim 0.45\text{--}0.55\text{ m}^3/\text{m}^3$). Aturan ini ditangguhkan sampai kurva retensi tanah lokal yang terkalibrasi tersedia.

### D. Penegakan Etis Rujukan PPL Kimiawi
Seluruh rekomendasi tindakan kimiawi dilarang menyebut merek dagang atau takaran dosis. Engine secara otomatis memicu aksi `ACT_REFER_PPL_CHEMICAL`: *"Konsultasikan pilihan bahan aktif dan takaran resmi dengan Petugas Penyuluh Lapangan (PPL) setempat."*
