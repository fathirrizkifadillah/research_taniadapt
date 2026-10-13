# TaniAdapt Engine Output Schema (v2.2-honest-status)

**Status:** PENDING_USER_RATIFICATION  
**Skema Validasi JSON:** `schemas/engine_output.schema.json` (Draft 2020-12)  

---

## 1. Evidence Contract (Kontrak Ilmiah)

Decision Engine mematuhi alur ketat: `Evidence -> Finding -> Interpretation -> Model -> Decision Logic`. 
1. Dilarang mengarang ambang batas buatan sendiri (*no ad-hoc thresholds*).
2. Dilarang mengarang probabilitas numerik terkonvensi, belum dikalibrasi terhadap data lapangan atau estimasi ton/ha kehilangan hasil tanpa model bersertifikasi.
3. Jika bukti tidak memadai atau parameter input bernilai null/stale $\to$ **Wajib mengembalikan `evidence_insufficient`**.
4. Peringkat `relative_rank` (`low`, `typical`, `unusually_high`) adalah **konvensi pelaporan heuristik** terhadap baseline historis lokal, bukan ambang kerusakan agronomis mutlak.
5. `rank_basis` hanya boleh menyebut sumber data dasar yang benar-benar tersedia secara lokal (misal: `AgERA5_1991_2020` untuk sel yang telah terunduh, atau `AgERA5_2015_2024_10yr`).

---

## 2. Struktur Payload JSON Output Kontrak

```json
{
  "crop": "padi | jagung | kedelai | cabai | tomat",
  "location": {
    "kabkota": "<official ADM2>",
    "cell_id": "<AgERA5 cell>",
    "weather_source": "<source>"
  },
  "as_of": "YYYY-MM-DD",
  "issue_time": "YYYY-MM-DDTHH:MM:SS+07:00",
  "timezone": "Asia/Jakarta",
  "rules_version": "v2.2-honest-status",
  "data_version": "<version>",
  "data_freshness_days": null,
  "layer": "seasonal | daily | hourly",
  "source_data": "forecast | reanalysis | reanalysis_forecast",
  "forecast_uncertainty": null,
  "indicators": [
    {
      "id": "<indicator>",
      "rule_id": "<ID dari rules/rules.json>",
      "value": null,
      "unit": "<unit>",
      "relative_rank": null,
      "rank_basis": "<dataset dan calendar window>",
      "rank_basis_n": null
    }
  ],
  "status": "normal | kondisi_mendukung_OPT | kondisi_stres_abiotik | waspada_defisit_ringan | evidence_insufficient",
  "evidence_tier": "published_model | literature_transfer | convention_pending | insufficient",
  "evidence_refs": ["<VERIFIED evidence_registry ID only>"],
  "claim_allowed": "<narasi operasional yang diperbolehkan>",
  "claim_forbidden": ["<klaim terlarang>"],
  "limitations": ["<keterbatasan ilmiah>"],
  "action_ids": ["<action table ID>"]
}
```

---

## 3. Pemetaan Status & Aturan Validasi Keras

1. **Status Stres / OPT Wajib Didukung Bukti Terverifikasi**:
   * Status `kondisi_stres_abiotik` hanya diizinkan keluar jika didukung oleh `evidence_refs` yang berstatus **`VERIFIED`** (misalnya `FAO56_RAW_DEPLETION`).
   * Status `kondisi_mendukung_OPT` hanya diizinkan keluar jika aturan didukung oleh referensi **`VERIFIED`**. Jika aturan berstatus `CONVENTION_PENDING` (misalnya proksi $P_{10}$), statusnya **wajib diturunkan menjadi `evidence_insufficient`** atau berstatus konvensi terbuka tanpa mengklaim diagnosis OPT.
2. **Layer Hourly**:
   * Menambahkan layer `"hourly"` untuk mendukung rekomendasi per jam (06.00 s/d 18.00 WIB) di antarmuka web, memuat variabel `rule_id`, `source_data`, dan `forecast_uncertainty` (probabilitas hujan % bila ada).

---

## 4. Tabel Aksi Resmi (Action Table)

| Action ID | Tindakan Lapangan | Sumber Bukti Otoritatif | Status Verifikasi |
|---|---|---|:---:|
| `ACT_AWAIT_EVIDENCE` | Tunda saran spesifik; tunggu data/bukti memadai. | Engine Evidence Contract | **ACTIVE** |
| `ACT_IRRIG_REPLENISHMENT` | Lakukan penyiraman replenishment (Dr > RAW). | FAO-56 Chapter 8, Eq. 82–83 | **VERIFIED** |
| `ACT_IRRIG_DEFER_RAIN_SAT` | Tunda penyiraman karena tanah jenuh air / hujan. | Konvensi Operasional Irigasi | `PENDING_EXTENSION_SOURCE` |
| `ACT_FERT_APPLY_MOIST` | Lakukan pemupukan pada tanah lembap terlarut. | Konvensi Standar Agronomi | `PENDING_EXTENSION_SOURCE` |
| `ACT_FERT_DEFER_LEACHING`| Tunda pemupukan; risiko hujan lebat hanyut. | Konvensi Pencegahan Leaching | `PENDING_EXTENSION_SOURCE` |
| `ACT_SPRAY_OPTIMAL` | Waktu ideal penyemprotan (angin tenang, suhu sejuk). | Konvensi Standar Perlindungan Tanaman | `PENDING_EXTENSION_SOURCE` |
| `ACT_SPRAY_DEFER_DRIFT_RAIN`| Tunda penyemprotan; bahaya drift / hujan bilas. | Standar Keselamatan Drift Lapangan | `PENDING_EXTENSION_SOURCE` |
| `ACT_HARVEST_DRY` | Lakukan pemanenan pada cuaca siang kering. | Standar Pascapanen Biji/Gabah | `PENDING_EXTENSION_SOURCE` |
| `ACT_HARVEST_DEFER_WET` | Tunda panen; kelembapan tinggi / risiko busuk. | Standar Pascapanen Biji/Gabah | `PENDING_EXTENSION_SOURCE` |
| `ACT_PRUNE_SANITATION` | Lakukan pemangkasan sanitasi cuaca kering. | Standar Budidaya Hortikultura | `PENDING_EXTENSION_SOURCE` |
| `ACT_PRUNE_DEFER_WET` | Tunda pemangkasan; luka basah rentan infeksi. | Standar Budidaya Hortikultura | `PENDING_EXTENSION_SOURCE` |
| `ACT_DRAINAGE_CHECK` | Periksa dan bersihkan saluran drainase parit. | Manajemen Risiko Genangan | `PENDING_EXTENSION_SOURCE` |
| `ACT_REFER_PPL_CHEMICAL` | **Konsultasikan bahan aktif & dosis resmi ke PPL.** | Regulasi Etis Pestisida Kementan | **ACTIVE (STRICT)** |

*Aturan Larangan Mutlak*: Engine dilarang mengeluarkan nama merek pestisida sintetis, formulasi konsentrat, ataupun takaran kimia (misal ml/liter air). Aksi yang berkaitan dengan bahan kimia wajib memicu `ACT_REFER_PPL_CHEMICAL`.
