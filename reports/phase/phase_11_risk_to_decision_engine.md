# TaniAdapt Research Dossier — Phase 11: Risk → Decision Engine

**Status**: COMPLETED  
**Ruang Lingkup**: Perakitan logika keputusan operasional 5 tindakan agronomi (Siram, Pupuk, Semprot, Panen, Rawat), jadwal per jam (06.00–18.00 WIB), dan penegakan kontrak JSON output.

---

## 1. Logika Evaluasi 5 Tindakan Agronomi
1. **Siram (Irrigation)**:
   * *Kondisi Optimal*: Pagi (06.00–08.00) dan sore (15.00–18.00) saat radiasi rendah dan transpirasi tenang.
   * *Peringatan (WARN)*: Siang terik (11.00–14.00) saat radiasi $> 500\text{ W/m}^2$ atau VPD tinggi (air cepat menguap sebelum meresap).
   * *Bahaya (DANGER)*: Tanah sudah jenuh air (lengas tanah $\ge 70\%$) atau sedang terjadi hujan.
2. **Semprot (Spraying)**:
   * *Kondisi Optimal*: Pagi/sore dengan angin tenang $3–12\text{ km/j}$ dan suhu $< 30^\circ\text{C}$.
   * *Bahaya (DANGER)*: Kecepatan angin $> 15\text{ km/j}$ (*spray drift*) atau ada risiko hujan dalam 3 jam ke depan (*washoff*).
3. **Pupuk (Fertilizing)**:
   * *Kondisi Optimal*: Tanah dalam kelembapan kapasitas lapang yang cukup untuk melarutkan granul pupuk.
   * *Bahaya (DANGER)*: Prakiraan hujan lebat $\ge 8.0\text{ mm}$ dalam 12 jam ke depan (risiko pupuk tercuci/hanyut).
4. **Panen (Harvesting)**:
   * *Kondisi Optimal*: Siang hari kering (08.00–16.00) dengan kelembapan udara $\text{RH} \le 75\%$ dan nihil presipitasi.
   * *Bahaya (DANGER)*: Hujan aktif atau $\text{RH} > 85\%$ (risiko pembusukan hasil panen).
5. **Rawat (Pruning)**:
   * *Kondisi Optimal*: Cuaca cerah dan kering agar jaringan luka pangkas segera membentuk kalus kering.
   * *Bahaya (DANGER)*: Prakiraan hujan $\ge 2.0\text{ mm}$ dalam 8 jam ke depan (luka basah rentan infeksi jamur).

---

## 2. Kepatuhan Skema Kontrak Output Engine (`docs/engine_output_schema.md`)
Decision Engine mengekspor payload JSON terstandarisasi yang memuat:
* Indikator biofisik terhitung lengkap dengan peringkat relatif persentil lokal (`relative_rank`: low/typical/high).
* Status risiko terkalibrasi (`normal`, `kondisi_stres_abiotik`, `kondisi_mendukung_OPT`, atau `evidence_insufficient`).
* Sitasi bukti ilmiah pengesah (`evidence_refs`).
* Batasan klaim yang diizinkan (`claim_allowed`) dan klaim yang dilarang keras (`claim_forbidden`).
