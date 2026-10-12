# TaniAdapt Research Dossier — Phase 10: Evidence → Risk Model

**Status**: COMPLETED  
**Ruang Lingkup**: Penerjemahan bukti ilmiah terverifikasi menjadi model risiko agronomis terkalibrasi dan penetapan safeguard ketidakcukupan bukti.

---

## 1. Tiga Domain Model Risiko Terkalibrasi
1. **Risiko Cekaman Air Abiotik (Water Deficit & Waterlogging)**:
   * *Formula*: Neraca lengas kumulatif 14-hari $\text{CWB}_{14\text{d}} = \sum_{i=1}^{14} (P_i - ET_{c,i})$, di mana $ET_c = K_c \times ET_0$.
   * *Ambang Terkalibrasi*:
     * $\text{CWB}_{14\text{d}} \ge -25.0\text{ mm} \to$ `normal`
     * $-50.0\text{ mm} \le \text{CWB}_{14\text{d}} < -25.0\text{ mm} \to$ `waspada_defisit_ringan`
     * $\text{CWB}_{14\text{d}} < -50.0\text{ mm} \to$ `kondisi_stres_abiotik` (Irigasi replenishment)
   * *Risiko Genangan*: $\sum P_{3\text{d}} \ge 100\text{ mm}$ atau $\text{CWD} \ge 5\text{ hari} \to$ `kondisi_stres_abiotik` (Inspeksi drainase).
2. **Risiko Mikroklimat Biotik OPT (Penyakit Fajar Hortikultura)**:
   * *Formula*: Depresi embun fajar $\Delta T = T_{\min} - T_d$.
   * *Ambang Terkalibrasi*: Hari kondusif terjadi saat $\Delta T \le P_{10}$ lokal. Jika $\ge 3$ hari kondusif dalam 7 hari terakhir $\to$ `kondisi_mendukung_OPT` (Pemicu inspeksi lapangan / *scouting*).
3. **Safeguard Ketidakcukupan Bukti (*Insufficient Evidence*)**:
   * Jika parameter fenologi atau koefisien belum terverifikasi di evidence registry (mis. suhu kardinal GDD atau air cabai) $\to$ Wajib merespon `evidence_insufficient`.
