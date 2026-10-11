"""
Script: clean_notebook_06.py
Purpose: Clean notebook 06 from arbitrary thresholds (2.0 C), spurious DITERIMA/DITOLAK labels,
         and hallucinated chili CVs (28%/31% -> true 4.49%/5.71%).
"""

import json
from pathlib import Path

nb_path = Path("notebook/06_west_java_horticulture_productivity.ipynb")
nb = json.load(open(nb_path, "r", encoding="utf-8"))

# Cell 0 update: clear period establishment
nb['cells'][0]['source'] = [
    "# 06 — West Java SBS Horticulture (Chili) Productivity (DS06)\n",
    "**TaniAdapt Project — Regional Horticulture Outcome Target**\n",
    "**Fase:** Phase 3 (Discovery & Acquisition) + Phase 4 (Dataset Quality Audit)\n",
    "\n",
    "- **Sumber Data Resmi:**\n",
    "  1. Dinas Tanaman Pangan dan Hortikultura Jawa Barat / Galura Open Data: `produktivitas_sbs_jabar.csv` (Tingkat Provinsi, 2017–2024, N=8 tahun valid; tahun 2025 merupakan data provisi/berubah nomenklatur).\n",
    "  2. Galura Open Data `od_18096_produksi_sayuran_berdasarkan_komoditas` (`produksi_sayuran_komoditas_jabar.csv`): 26 kab/kota hanya tahun 2013–2014 (volume produksi saja, tanpa luas panen dan tanpa tumpang-tindih temporal dengan AgERA5 2015–2024).\n",
    "- **Fokus Komoditas Hortikultura:** Cabai Besar dan Cabai Rawit (Provinsi Jawa Barat, 2017–2024).\n",
    "- **AUDIT KRITIS & PEMBATASAN METODOLOGI (A6)**:\n",
    "  * Ambang absolut 2.0°C dan label 'DITERIMA/DITOLAK' dihapus karena tidak ada sensor leaf wetness sebagai ground truth.\n",
    "  * Ketidakcocokan waktu: T_min (fajar) vs T_d (rata-rata 24 jam) diakui sebagai keterbatasan data harian.\n",
    "  * Proksi kebasahan daun diregistrasi ex ante menggunakan **Persentil ke-10 (P10)** per sel per bulan kalender.\n",
    "  * Koreksi CV Produktivitas Cabai: Label lama (CV ~28% dan ~31%) dikoreksi ke angka empiris sebenarnya: **Cabai Besar CV = 4,49%**, **Cabai Rawit CV = 5,71%**.\n"
]

# Cell 7 update
cell_7_code = """fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

# --- PANEL 1: SKOR KETERSEDIAAN VARIABEL AGRONOMI (OUTCOME GAP ANALYSIS) ---
vars_names = ['Produktivitas (Ku/Ha)', 'Volume Produksi (Ton)', 'Luas Panen (Ha)', 'Insidensi OPT/Penyakit', 'Varietas Spesifik Benih']
avail_scores = [100, 100, 100, 0, 0]
colors_avail = ['#2a9d8f', '#2a9d8f', '#2a9d8f', '#e76f51', '#e76f51']
bars1 = ax1.barh(vars_names, avail_scores, color=colors_avail, edgecolor='black', alpha=0.85, height=0.6)
ax1.set_xlim(0, 130)
ax1.set_title("Audit Ketersediaan Variabel (Outcome Gap Analysis)\\n(Bukti Absennya Label Penyakit Tanaman OPT)", fontsize=10.5, fontweight='bold')
ax1.set_xlabel("Persentase Ketersediaan Data (%)", fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.5)
for bar, score in zip(bars1, avail_scores):
    status = "TERSEDIA (100%)" if score == 100 else "ABSEN (0%)"
    ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2., status, ha='left', va='center', fontsize=8, fontweight='bold',
             color='#1b5e20' if score == 100 else '#b71c1c')
ax1.annotate('KESIMPULAN METODOLOGIS AUDIT:\\nSupervised ML Penyakit DILARANG\\n(Target Label OPT 100% Absen)\\nGunakan Advisory IFWC Mikroklimat', 
             xy=(10, 0.8), fontsize=8.2, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="#ffebee", ec="#c62828", alpha=0.95))

# --- PANEL 2: PROKSI DEPRESIASI TITIK EMBUN (PERSENTIL RELATIF LOKAL P10) ---
# Mengganti ambang absolut 2.0°C dan label DITERIMA/DITOLAK dengan evaluasi persentil empiris
persentil_labels = ['P05 (Sangat Ketat)', 'P10 (Pra-Registrasi H_HORT_01)', 'P20 (Moderat)', 'Ambang Absolut Lama (<=2°C)']
freq_vals = [5.0, 10.0, 20.0, 62.7] 
colors_proxy = ['#457b9d', '#2a9d8f', '#e9c46a', '#e76f51']
bars2 = ax2.bar(persentil_labels, freq_vals, color=colors_proxy, edgecolor='black', alpha=0.85, width=0.5)
ax2.set_ylim(0, 100)
ax2.set_title("Distribusi Frekuensi Proksi Cekaman Kelembapan\\n(Pre-Registrasi P10 per Sel per Bulan; Hapus Ambang Absolut)", fontsize=10.5, fontweight='bold')
ax2.set_ylabel("Persentase Hari Teridentifikasi (%)", fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.5)
plt.setp(ax2.get_xticklabels(), rotation=15, ha='right', fontsize=8)
for bar, val in zip(bars2, freq_vals):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2, f"{val:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
ax2.annotate('CATATAN VALIDITAS:\\nTanpa ground truth kebasahan daun,\\nproksi tidak dapat di-claim valid.\\nP10 dipilih ex-ante untuk deteksi anomali.',
             xy=(0.5, 65), fontsize=7.5, bbox=dict(boxstyle="round,pad=0.3", fc="#fff9c4", ec="#fbc02d", alpha=0.95))

# --- PANEL 3: TREN PRODUKTIVITAS CABAI JAWA BARAT (2017–2024 REKONSILIASI) ---
# Menghitung CV empiris sejati: SD / Mean * 100%
cv_rawit = cabai_rawit['produktivitas_sayur_buah'].std(ddof=1) / cabai_rawit['produktivitas_sayur_buah'].mean() * 100.0
cv_besar = cabai_besar['produktivitas_sayur_buah'].std(ddof=1) / cabai_besar['produktivitas_sayur_buah'].mean() * 100.0

ax3.plot(cabai_rawit['tahun'], cabai_rawit['produktivitas_sayur_buah'], marker='s', color='darkorange', 
         label=f'Cabai Rawit (Empiris CV = {cv_rawit:.2f}%)', linewidth=2.5)
ax3.plot(cabai_besar['tahun'], cabai_besar['produktivitas_sayur_buah'], marker='o', color='crimson', 
         label=f'Cabai Besar (Empiris CV = {cv_besar:.2f}%)', linewidth=2.5)
ax3.set_title("Dinamika Produktivitas Cabai Jabar (2017–2024)\\n(Koreksi Label CV: 4,49% & 5,71%, Bukan 28% / 31%)", fontsize=10.5, fontweight='bold')
ax3.set_xlabel("Tahun Kalender", fontsize=10)
ax3.set_ylabel("Produktivitas (ku/ha)", fontsize=10)
ax3.legend(loc='lower left', fontsize=8.5)
ax3.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
png_out = FIGURES_DIR / "ds06_chili_commodities.png"
plt.savefig(png_out, dpi=150)
plt.show()
print(f"Gambar PNG diagnostik hortikultura cabai Jawa Barat berhasil disimpan ke: {png_out}")
"""
nb['cells'][7]['source'] = [line + "\n" for line in cell_7_code.splitlines()]

# Cell 9 update (Scorecard)
cell_9_code = """scorecard = pd.DataFrame([
    {"Dimensi Audit": "Dataset Identifier", "Hasil & Evaluasi": "DS06 — West Java SBS Horticulture (Chili) Productivity"},
    {"Dimensi Audit": "Penerbit & Sumber", "Hasil & Evaluasi": "Distanhor Jabar & Galura Open Data (produktivitas_sbs_jabar.csv)"},
    {"Dimensi Audit": "Cakupan Temporal Valid", "Hasil & Evaluasi": "2017 s.d. 2024 (8 Tahun Tingkat Provinsi; Tahun 2025 provisi; Od_18096 hanya 2013–2014)"},
    {"Dimensi Audit": "Variabilitas Hasil (CV)", "Hasil & Evaluasi": "Cabai Besar CV = 4,49% (Mean 136,99 ku/ha), Cabai Rawit CV = 5,71% (Mean 126,13 ku/ha)"},
    {"Dimensi Audit": "Status Label Ambang 2.0°C", "Hasil & Evaluasi": "DIHAPUS (Digantikan oleh pra-registrasi P10 per sel/bulan; timing mismatch harian diakui)"},
    {"Dimensi Audit": "Alokasi Portofolio", "Hasil & Evaluasi": "Tier B — Modul IFWC mikroklimat rule-based (Dilarang regresi hasil tahunan & ML penyakit)"},
    {"Dimensi Audit": "Status Disposisi", "Hasil & Evaluasi": "PASS WITH CONSTRAINTS (Terkunci sebagai Tier B)"}
])
display(scorecard)
"""
nb['cells'][9]['source'] = [line + "\n" for line in cell_9_code.splitlines()]

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook 06 updated successfully: {nb_path}")
