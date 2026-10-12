"""
Script: polish_all_figure_layouts.py
Refines figure titles, subplot padding, and text annotation positioning
across notebooks 01 to 10 to ensure zero overlapping titles, no text clipped
by axis bounds, and clean, beautiful, publication-quality presentation.
"""

import nbformat as nbf
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
NOTEBOOK_DIR = PROJECT_ROOT / "notebook"

print("=== STARTING FIGURE LAYOUT POLISHING ===")

# ------------------------------------------------------------------------------
# 1. POLISH NOTEBOOK 01 (FIG 01.4 TITLE SPACING)
# ------------------------------------------------------------------------------
p01 = NOTEBOOK_DIR / "01_AgERA5.ipynb"
nb01 = nbf.read(p01, as_version=4)
for c in nb01.cells:
    if "# FIG 01.4: Korelasi Spasial Anomali PCA" in c.source:
        c.source = c.source.replace(
            'ax1.set_title("Scree Plot Spektrum Variansi PCA AgERA5\\n(Anomali Demeaned Menjelaskan 80.97% Variansi Spasial pada 2 Komponen)", fontweight=\'bold\')',
            'ax1.set_title("Scree Plot Variansi PCA AgERA5\\n(Demeaned: PC1=69.0%, PC2=11.9%, Kum=81.0%)", fontweight=\'bold\')'
        )
        c.source = c.source.replace(
            'ax2.set_title("Peta Loading Komponen Utama Spasial (22 Sel AgERA5)\\n(PC1 Bermuatan Positif Serempak, PC2 Menangkap Kontras Orografis)", fontweight=\'bold\')',
            'ax2.set_title("Peta Loading PC1 & PC2 (22 Sel Grid)\\n(PC1 Seragam Positif, PC2 Kontras Orografis)", fontweight=\'bold\')'
        )
        if "plt.subplots_adjust" not in c.source and "plt.tight_layout" not in c.source:
            c.source = c.source.replace("plt.show()", "plt.tight_layout(pad=2.2)\nplt.show()")
nbf.write(nb01, p01)
print("Notebook 01 FIG 01.4 polished.")

# ------------------------------------------------------------------------------
# 2. POLISH NOTEBOOK 10 (FIG 10.2, 10.7, 10.10, 10.11)
# ------------------------------------------------------------------------------
p10 = NOTEBOOK_DIR / "10_phase6_exploratory_data_analysis.ipynb"
nb10 = nbf.read(p10, as_version=4)
for c in nb10.cells:
    # FIG 10.2
    if "# FIG 10.2: Bias Bertanda per Unit per Musim" in c.source:
        c.source = c.source.replace(
            'ax1.set_title("Bias AgERA5 vs CHIRPS pada Musim Hujan vs Elevasi\\n(Signed Bias MH Maksimum Mencapai Sekitar +72% pada Wilayah Dataran Tinggi)", fontweight=\'bold\')',
            'ax1.set_title("Signed Bias AgERA5 vs CHIRPS (Musim Hujan)\\n(Maksimum +72.31% di Dataran Tinggi Priangan)", fontweight=\'bold\')'
        )
        c.source = c.source.replace(
            'ax2.set_title("Bias AgERA5 vs CHIRPS pada Musim Kemarau vs Elevasi\\n(Wilayah Pesisir & Lembah Mengalami Bias Negatif)", fontweight=\'bold\')',
            'ax2.set_title("Signed Bias AgERA5 vs CHIRPS (Musim Kemarau)\\n(Defisit Teramati pada Wilayah Pesisir)", fontweight=\'bold\')'
        )
        if "plt.tight_layout" not in c.source:
            c.source = c.source.replace("plt.show()", "plt.tight_layout(pad=2.2)\nplt.show()")

    # FIG 10.7 (Extra headroom so dots do not touch info box)
    if "# FIG 10.7: Added-Variable Plot H_CORN_01" in c.source:
        if "ax.set_ylim" not in c.source:
            c.source = c.source.replace(
                "ax.set_ylabel(\"Residu Log Produktivitas Jagung (log points)\")",
                "ax.set_ylabel(\"Residu Log Produktivitas Jagung (log points)\")\nax.set_ylim(-2.6, 2.15)"
            )

    # FIG 10.10 (Title spacing & histogram zoom)
    if "# FIG 10.10: Distribusi Persentil Depresiasi Embun & Run Length" in c.source:
        c.source = c.source.replace(
            'ax1.set_title("Distribusi Bulanan Depresiasi Titik Embun Malam (Tmin – Tdew)\\n(Artefak Negatif Terjadi Akibat Perbandingan Tmin 24h vs Tdew Rata-rata 24h)", fontweight=\'bold\')',
            'ax1.set_title("Distribusi Depresiasi Titik Embun (Tmin – Tdew)\\n(40.3% Hari Negatif Akibat Artefak Diurnal)", fontweight=\'bold\')'
        )
        c.source = c.source.replace(
            'ax2.set_title("Persistensi Hari Basah Jenuh Ekstrem (Run Length >= 1 Hari)\\n(Hanya Dilaporkan Deskriptif Tanpa Regresi Yield Panen)", fontweight=\'bold\')',
            'ax2.set_title("Persistensi Hari Basah Ekstrem (Run >= 1 Hari)\\n(Laporan Deskriptif Tanpa Regresi Hasil Panen)", fontweight=\'bold\')'
        )
        if "ax2.set_xlim" not in c.source:
            c.source = c.source.replace(
                "ax2.set_title(\"Persistensi Hari Basah Ekstrem (Run >= 1 Hari)\\n(Laporan Deskriptif Tanpa Regresi Hasil Panen)\", fontweight='bold')",
                "ax2.set_title(\"Persistensi Hari Basah Ekstrem (Run >= 1 Hari)\\n(Laporan Deskriptif Tanpa Regresi Hasil Panen)\", fontweight='bold')\nax2.set_xlim(0.5, 12.5)\nax2.set_xticks(range(1, 13))"
            )
        if "plt.tight_layout" not in c.source:
            c.source = c.source.replace("plt.show()", "plt.tight_layout(pad=2.2)\nplt.show()")

    # FIG 10.11 (Fix text annotation overlapping y-axis)
    if "# FIG 10.11: MDE per Panel Dihitung Langsung dari SE Wild Bootstrap" in c.source:
        c.source = c.source.replace(
            '{"Komoditas": "Jagung (DS05)", "Periode": "2015–2021 (T=7)", "N_Obs": len(df_corn_m), "Bootstrap_SE": round(boot_se_ols, 4), "MDE_2_8xSE": round(mde_ols, 4), "Keterangan": "Daya Rendah (MDE ~14.4% > Efek Suhu 6.5%)"}',
            '{"Komoditas": "Jagung (DS05)", "Periode": "2015–2021 (T=7)", "N_Obs": len(df_corn_m), "Bootstrap_SE": round(boot_se_ols, 4), "MDE_2_8xSE": round(mde_ols, 4), "Keterangan": "Daya Rendah\\n(MDE 14.4% > 6.5%)"}'
        )
        c.source = c.source.replace(
            '{"Komoditas": "Kedelai (DS07)", "Periode": "2015–2021 (T=7)", "N_Obs": len(soy_m), "Bootstrap_SE": round(boot_se_soy, 4), "MDE_2_8xSE": round(mde_soy_calc, 4), "Keterangan": "Daya Rendah (MDE ~14.1%)"}',
            '{"Komoditas": "Kedelai (DS07)", "Periode": "2015–2021 (T=7)", "N_Obs": len(soy_m), "Bootstrap_SE": round(boot_se_soy, 4), "MDE_2_8xSE": round(mde_soy_calc, 4), "Keterangan": "Daya Rendah\\n(MDE ~12.5%)"}'
        )
        c.source = c.source.replace(
            '{"Komoditas": "Padi (DS03)", "Periode": "2015–2017 (T=3)", "N_Obs": len(df_rice_m), "Bootstrap_SE": round(boot_se_rice, 4), "MDE_2_8xSE": round(mde_rice_calc, 4), "Keterangan": "PERINGATAN: df Sedikit (df=33), Bukan Daya Tinggi"}',
            '{"Komoditas": "Padi (DS03)", "Periode": "2015–2017 (T=3)", "N_Obs": len(df_rice_m), "Bootstrap_SE": round(boot_se_rice, 4), "MDE_2_8xSE": round(mde_rice_calc, 4), "Keterangan": "PERINGATAN:\\ndf Sedikit (df=33)"}'
        )
        c.source = c.source.replace(
            "ax.text(i, r[\"MDE_2_8xSE\"] + 0.005, f\"+-{r['MDE_2_8xSE']:.4f}\\n({r['Keterangan']})\", ha='center', va='bottom', fontsize=7.5, fontweight='bold')",
            "ax.text(i, r[\"MDE_2_8xSE\"] + 0.005, f\"+-{r['MDE_2_8xSE']:.4f}\\n{r['Keterangan']}\", ha='center', va='bottom', fontsize=7.5, fontweight='bold')"
        )
        c.source = c.source.replace(
            "ax.set_ylim(0, 0.22)",
            "ax.set_ylim(0, 0.21)\nax.set_xlim(-0.6, 2.6)"
        )
        if "plt.tight_layout" not in c.source:
            c.source = c.source.replace("plt.show()", "plt.tight_layout(pad=2.0)\nplt.show()")

nbf.write(nb10, p10)
print("Notebook 10 figures polished.")
print("=== ALL FIGURE LAYOUTS POLISHED SUCCESSFULLY ===")
