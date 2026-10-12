# TaniAdapt Research Dossier — Phase 11: Risk → Decision Engine

**Status**: COMPLETED  
**Ruang Lingkup**: Perakitan Logika Decision Engine Operasional untuk 5 Tindakan Agronomi & Jadwal Jam 06.00–18.00 WIB  
**Dokumen Induk Kontrak**: `docs/engine_output_schema.md` (Schema v2.1)  
**Tujuan Operasional**: Menerjemahkan Status Risiko dan Cuaca Diurnal Menjadi Rekomendasi Lahan Presisi bagi Aplikasi Web Next.js

---

## 1. Arsitektur Inti Decision Engine
Decision Engine beroperasi secara terpisah (*decoupled*) dari model bahasa (LLM). Mesin menerima 4 vektor input:
1. **Konteks Lahan**: Lokasi (27 Kab/Kota $\to$ 22 Sel AgERA5), Komoditas, Umur Tanaman (HST), Luas Lahan.
2. **Kondisi Cuaca Hari Ini & Jam Berjalan**: Suhu ($T$), Kelembapan ($RH$), Angin ($Wind$), Hujan ($P$), Radiasi ($Srad$), Tekanan Uap ($VPD$).
3. **Riwayat Cuaca Kumulatif**: Neraca lengas 14-hari ($\text{CWB}_{14\text{d}}$), Hari basah kondensasi fajar 7-hari ($N_{\text{kondusif}}$).
4. **Gerbang Kontrak Bukti (Evidence Gate)**: Verifikasi status bukti; jika tidak terverifikasi $\to$ return `evidence_insufficient`.

---

## 2. Matriks Aturan Logika Keputusan untuk 5 Tindakan Agronomi Utama

| Tindakan Agronomi | Status Sangat Aman (Hijau) | Status Waspada (Kuning/Oranye) | Status Hindari / Bahaya (Merah) | Jendela Waktu Lapangan Terbaik (WIB) |
|---|---|---|---|:---:|
| **1. Siram (Irrigation)** | Tanah membutuhkan air ($\text{CWB}_{14\text{d}} < -25\text{ mm}$), kelembapan tanah rendah, radiasi dan evaporasi tenang. | Radiasi matahari puncak ($Srad > 500\text{ W/m}^2$) & $VPD > 15\text{ hPa}$ jam 11.00–14.00 (*Air cepat menguap sebelum meresap*). | Tanah sudah jenuh air (kelembapan tanah $\ge 70\%$) atau sedang terjadi hujan $\ge 3.0\text{ mm}$ (*Tanah sudah jenuh air*). | **06.00–08.00** & **15.00–17.00** |
| **2. Pupuk (Fertilizing)** | Tanah memiliki kelembapan kapasitas lapang yang cukup untuk melarutkan granul pupuk tanpa genangan. | Tanah sangat kering; pupuk tidak akan larut optimal tanpa bantuan irigasi penyiraman. | Prakiraan hujan lebat $\ge 8.0\text{ mm}$ dalam 12 jam ke depan (*Risiko pupuk hanyut / tercuci limpasan permukaan*). | **06.00–10.00** & **15.00–17.00** |
| **3. Semprot (Spraying)** | Kecepatan angin tenang ($3–12\text{ km/j}$) dan suhu udara sejuk ($< 30^\circ\text{C}$). | Suhu mulai terik ($\ge 30^\circ\text{C}$) atau angin sangat tenang ($< 3\text{ km/j}$, risiko inversi termal). | Kecepatan angin $> 15\text{ km/j}$ (*Bahaya spray drift*) ATAU ada probabilitas hujan $> 30\%$ dalam 3 jam (*Risiko obat terbilas*). | **06.00–09.00** & **15.30–17.30** |
| **4. Panen (Harvesting)** | Siang hari kering (08.00–16.00), kelembapan udara $RH \le 75\%$, dan nihil presipitasi. | Embun pagi belum mengering sempurna ($RH > 75\%$, bulir gabah/buah basah). | Terjadi hujan aktif atau udara sangat basah ($RH > 85\%$, risiko pembusukan hasil panen di karung). | **09.00–15.00** |
| **5. Rawat (Pruning)** | Cuaca cerah dan berangin kering; luka pangkas segera membentuk lapisan kalus kering. | Cuaca berawan mendung tanpa kepastian hujan. | Ada potensi hujan $\ge 2.0\text{ mm}$ dalam 8 jam ke depan (*Jaringan luka basah rentan infeksi spora cendawan*). | **07.00–11.00** |

---

## 3. Evaluasi Dinamika Cuaca Diurnal Per Jam (06.00 s/d 18.00 WIB)
Engine mengevaluasi setiap jam secara deterministik untuk mencocokkan tampilan UI website TaniAdapt:
* **Pagi Hari (06.00–08.00 WIB)**: Jendela emas penyiraman dan pemupukan. Suhu sejuk ($22–25^\circ	ext{C}$), angin sepoi ($4–6	ext{ km/j}$), dan transpirasi stomata terbuka stabil.
* **Siang Terik (11.00–14.00 WIB)**: Lonjakan radiasi surya ($>600	ext{ W/m}^2$) dan VPD tinggi ($>18	ext{ hPa}$). Penyiraman diberi status **WASPADA/ORANYE** karena air irigasi akan menguap langsung sebelum diserap akar. Namun, jendela ini menjadi **AMAN/HIJAU** untuk panen gabah/jagung/cabai.
* **Sore Hari (15.00–18.00 WIB)**: Radiasi surya mereda ($<300	ext{ W/m}^2$), membuka kembali jendela irigasi replenishment dan penyemprotan sore sebelum malam.

---

## 4. Kepatuhan Penuh terhadap Skema Kontrak JSON (`docs/engine_output_schema.md`)
Output Decision Engine adalah JSON valid yang memuat:
1. `indicators`: Nilai numerik fisis beserta peringkat relatif persentil lokal (`low`, `typical`, `high`) berbasis AgERA5 1991–2020.
2. `status`: `normal`, `kondisi_stres_abiotik`, `kondisi_mendukung_OPT`, atau `evidence_insufficient`.
3. `evidence_refs`: Daftar ID bukti terverifikasi dari evidence registry (`FAO56_ET0_PM`, `FAO56_KC_*`).
4. `claim_allowed`: Narasi operasional lahan yang diizinkan secara ilmiah.
5. `claim_forbidden`: Batasan klaim terlarang (dilarang meramal angka ton/ha yield, dilarang diagnosis racun kimia spesifik).
