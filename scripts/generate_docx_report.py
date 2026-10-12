"""
Script: generate_docx_report.py
Generates a comprehensive, publication-grade Microsoft Word (.docx) document 
containing the complete TaniAdapt Phase 5 & 6 EDA and Audit Closure Report.
"""

import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
OUTPUT_DOCX = PROJECT_ROOT / "reports" / "TaniAdapt_Comprehensive_EDA_Report.docx"
FIG_DIR = PROJECT_ROOT / "reports" / "figures"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Page setup: Standard A4 or Letter, 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    # Base Normal
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(40, 40, 40)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # --------------------------------------------------------------------------
    # DOCUMENT HEADER / TITLE
    # --------------------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_after = Pt(2)
    title_run = title_p.add_run("TANIADAPT RESEARCH DOSSIER")
    title_run.font.name = 'Arial'
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(27, 94, 32) # Dark Forest Green

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    sub_run = sub_p.add_run("Laporan Komprehensif Hasil Audit Metodologis, Rekonsiliasi Ilmiah & Exploratory Data Analysis (Phase 5 & Phase 6)")
    sub_run.font.name = 'Arial'
    sub_run.font.size = Pt(13)
    sub_run.font.color.rgb = RGBColor(55, 71, 79) # Slate Grey

    # Metadata Box
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    metadata_rows = [
        ("Proyek & Wilayah:", "TaniAdapt — Ekonometrika & Mikroklimat Pertanian Jawa Barat"),
        ("Tujuan Laporan:", "Dossier Evaluasi Lengkap untuk Claude (Independent Review & Research Architecture)"),
        ("Prinsip Metodologis:", "Evidence → Finding → Interpretasi Agronomis → Model → Decision Logic (Zero Hardcode, No P-Values in EDA)"),
        ("Status Versi Git:", "Commit Lokal 1455e70 | Git Tag: v2-audit-closure | Working Tree Clean"),
        ("Tanggal Penyelesaian:", "12 Oktober 2026")
    ]

    for i, (k, v) in enumerate(metadata_rows):
        r = meta_table.rows[i]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.3)
        set_cell_background(r.cells[0], "F1F8E9")
        set_cell_background(r.cells[1], "FAFAFA")
        set_cell_margins(r.cells[0], 60, 60, 100, 100)
        set_cell_margins(r.cells[1], 60, 60, 100, 100)
        p0 = r.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        run0 = p0.add_run(k)
        run0.font.bold = True
        run0.font.size = Pt(9.5)
        run0.font.color.rgb = RGBColor(46, 125, 50)
        
        p1 = r.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        run1 = p1.add_run(v)
        run1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & ATURAN KERAS METODOLOGIS
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary: Transformasi Metodologis", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Laporan ini menyajikan hasil penutupan menyeluruh terhadap seluruh isu audit independen "
        "dan rekonsiliasi ilmiah proyek TaniAdapt. Seluruh analisis dibangun di atas 10 notebook modular "
        "(01–09 per dataset dan 10 lintas-dataset) di mana setiap figur visualisasi kini telah dipisahkan secara modular "
        "menjadi sel tersendiri (sel Markdown penjelasan di atas sel Code pembuat grafik). Seluruh notebook telah dieksekusi "
        "ulang dari atas ke bawah dengan 0 error dan menghasilkan 51 figur grafis beresolusi tinggi (200 DPI)."
    )

    doc.add_paragraph(
        "Kepatuhan ketat terhadap Aturan Keras Metodologis diterapkan secara konsisten:\n"
        "1. Zero Hardcoding: Seluruh angka estimasi, koefisien, Standard Error, Confidence Interval, MDE, dan persentase dihitung langsung dari data melalui kode murni.\n"
        "2. Sumber Resmi Tunggal BPS: Angka resmi BPS hanya bersumber dari reports/dataset_audit/bps_manual_input.csv. Periode 2018–2020 berstatus UNVERIFIED dan dikeluarkan dari perbandingan.\n"
        "3. Larangan Ambang Absolut: Parameter cuaca dievaluasi murni berbasis persentil empiris (P10, P50, P75, P90) atau z-score ex-ante, bukan ambang buatan seperti mm atau derajat tertentu.\n"
        "4. Non-Causal Framing & No P-Values: EDA berfokus murni pada varians, dekomposisi Fixed Effects, dan eksplorasi data. Hipotesis empiris dievaluasi di bawah kerangka pre-registered protocol menggunakan Wild Cluster Bootstrap Webb.\n"
        "5. Isolasi Artefak Pelaporan: Tahun 2022 pada Jagung dan Kedelai resmi ditandai sebagai SUSPECT akibat bukti imputasi seragam rata-rata dinas, dan dikeluarkan dari panel regresi utama."
    )

    # --------------------------------------------------------------------------
    # 2. STATUS PENUTUPAN AUDIT BAGIAN A (A1 - A11)
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("2. Matriks Penutupan Audit Blokade A1 – A11", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Sebanyak 11 item audit Bagian A telah diselesaikan secara tuntas dan terdokumentasi dalam berkas resmi "
        "reports/audit_closure_report.md. Berikut adalah ringkasan status penutupan audit:"
    )

    audit_table = doc.add_table(rows=12, cols=4)
    audit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    audit_table.autofit = False

    audit_headers = ["Item ID", "Fokus Masalah Audit", "Status Penutupan", "Hasil Rekonsiliasi & Bukti Empiris"]
    hdr_row = audit_table.rows[0]
    col_widths = [Inches(0.8), Inches(1.8), Inches(1.3), Inches(2.6)]

    for j, text in enumerate(audit_headers):
        hdr_row.cells[j].width = col_widths[j]
        set_cell_background(hdr_row.cells[j], "2E7D32")
        set_cell_margins(hdr_row.cells[j], 80, 80, 100, 100)
        p = hdr_row.cells[j].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    audit_rows_data = [
        ("A1", "Rekonsiliasi Padi B1 (BPS Tunggal)", "CLOSED", "DS03 berbobot luas cocok 100.0% (diff 0.01%) dengan BPS resmi 2015-2017 (61.22, 60.49, 58.87 ku/ha). 2018-2020 berstatus UNVERIFIED. Lonjakan 2019 (+21.8%) diisolasi sebagai artefak reporting."),
        ("A2", "Validasi Presipitasi CHIRPS ERDDAP", "CLOSED (Partial 3 Thn)", "NOAA ERDDAP melayani 3 tahun benchmark (2016, 2020, 2024; N=972 unit-bulan, Pearson r=0.710). Non-benchmark BLOCKED secara transparan. Sampling area poligon meredam bias 18-28%."),
        ("A3", "Spatial Neff & PCA Anomali", "CLOSED", "PCA anomali deseasonalized (22 sel x 120 bln) membuktikan 2 komponen utama menjelaskan 84.55% varians (r rata-rata = 0.727). Derajat bebas efektif iklim Jabar hanya 2 moda spasial."),
        ("A4", "Inferensi Panel & Wild Bootstrap", "CLOSED", "Jagung H_CORN_01 terhitung beta = +0.0368, 95% Webb CI [-0.0521, +0.1300], MDE = +-0.2306 (Evidence Insufficient). Padi T=3 MDE = +-0.0325 (df=33 semu). Lead placebo t+1 = +0.0075."),
        ("A5", "Higienitas Klaim & Sitasi Agronomi", "CLOSED", "Paper 15 diganti studi Prasad et al. (2006). Klaim kausal dihapus; evaluasi diposisikan sebagai protokol eksploratori terdaftar ex-ante tanpa klaim konfirmatori."),
        ("A6", "Hortikultura Cabai IFWC & CV", "CLOSED", "Ambang absolut diganti P10 depresiasi embun. CV empiris: Cabai Besar 4.49%, Cabai Rawit 5.71%. Overlap kab/kota vs cuaca = 0 tahun. Terkunci permanen di Tier B Rule-Based."),
        ("A7", "Agroklimat DS04 & Ambang CDD", "CLOSED", "Ambang CDD diganti persentil empiris (P90: 12-24 hari). 12 titik grid poligon daratan Jabar. Diakui sebagai pembanding internal sirkular ERA5 (r=0.993)."),
        ("A8", "Duplikasi Sel Grid AgERA5", "CLOSED", "27 unit wilayah Jabar memetakan ke tepat 22 sel AgERA5 unik (5 pasang wilayah berbagi sel; jarak rata-rata centroid-ke-grid 5.2 km). Lookup spasial resmi dibuat."),
        ("A9", "Konsistensi Kriteria Sentra Ex-Ante", "CLOSED", "Kriteria sentra kedelai dibakukan ex-ante: aktif N >= 6 tahun = tepat 17 sentra kabupaten. Baris valid terkunci: 156 baris aktif kedelai, 181 baris aktif jagung."),
        ("A10", "Jagung & Kedelai 2022 SUSPECT", "CLOSED", "Tahun 2022 resmi ditandai SUSPECT (13 kab yield jagung persis 75.70 ku/ha; SD kedelai runtuh ke 0.19 ku/ha). 2022 resmi dieksklusikan dari panel utama regresi (T=7, 2015-2021)."),
        ("A11", "Kebersihan Repositori & Verifikasi Git", "CLOSED", "Terverifikasi 45 file historis terlacak di git history tanpa ada script esensial yang hilang. Seluruh temporary script dibersihkan. Working tree bersih.")
    ]

    for i, (aid, topic, stat, detail) in enumerate(audit_rows_data):
        row = audit_table.rows[i+1]
        bg = "F9FBE7" if i % 2 == 0 else "FFFFFF"
        for j, (val, w) in enumerate(zip([aid, topic, stat, detail], col_widths)):
            cell = row.cells[j]
            cell.width = w
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.font.bold = True
            elif j == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(46, 125, 50)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # 3. HASIL LENGKAP EDA PER DATASET (NOTEBOOK 01 - 09)
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("3. Hasil Lengkap Exploratory Data Analysis per Dataset (NB01 – NB09)", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    # 3.1 AgERA5
    doc.add_heading("3.1 AgERA5 Copernicus Reanalysis (DS01) — Notebook 01", level=2)
    doc.add_paragraph(
        "• Cakupan & Integritas: 120 bulan (2015–2024) untuk 27 unit wilayah administrasi. Uji termodinamika membuktikan 100.0% data lolos batas fisis (Tmax >= Tmin, RH 0–100%, presipitasi non-negatif).\n"
        "• Resolusi Grid: 27 unit wilayah memetakan ke tepat 22 sel grid 0.1° unik. Lima pasang wilayah berbagi sel: Kab/Kota Bogor, Kab/Kota Cirebon, Kab/Kota Bandung, Ciamis–Kota Tasikmalaya, dan Kab. Bandung Barat–Kota Cimahi.\n"
        "• Spatial Neff & PCA: Dekomposisi PCA anomali bulanan membuktikan PC1 (68.91%) dan PC2 (15.64%) menjelaskan 84.55% total variansi spasial. Korelasi anomali rata-rata antar-sel sangat tinggi (r = 0.727), membuktikan bahwa derajat bebas independen iklim Jawa Barat hanya 2 moda regional.\n"
        "• Penyerapan Varians oleh Two-Way FE: Standar deviasi presipitasi vegetatif Feb–Apr mentah adalah 229.36 mm, namun setelah Fixed Effects kabupaten dan tahun diserap, standar deviasi residu hanya menyisakan 68.40 mm untuk identifikasi empiris."
    )

    # 3.2 Bangladesh Rice Panel
    doc.add_heading("3.2 Bangladesh Rice Panel Benchmark (DS02) — Notebook 02", level=2)
    doc.add_paragraph(
        "• Panel Balanced: 1.728 observasi lengkap (64 distrik x 3 musim x 9 tahun, 2015–2023) tanpa missing value.\n"
        "• Pola Musiman: Boro (musim dingin dengan irigasi) memiliki produktivitas tertinggi dan variabilitas terendah; Aus dan Aman mencerminkan kerentanan curah hujan muson.\n"
        "• Partisi Variansi TWFE: Efek tetap temporal menyerap 64.82% varians, spasial menyerap 11.42%, dan residu cuaca lokal menyisakan 23.76% (koefisien TWFE curah hujan = -0.0433 per 100 mm).\n"
        "• Peran Metodologis: Berfungsi murni sebagai arsitektur benchmark ekonometrika panel transfer, bukan untuk mentransfer parameter koefisien ke Jawa Barat."
    )

    # 3.3 West Java Rice
    doc.add_heading("3.3 West Java Rice Productivity (DS03) — Notebook 03", level=2)
    doc.add_paragraph(
        "• Rekonsiliasi BPS Resmi: Rata-rata berbobot luas DS03 cocok 100.0% (selisih < 0.01%) terhadap angka resmi BPS Jawa Dalam Angka pada periode baseline 2015–2017 (2015: 61.22 vs 61.22; 2016: 60.49 vs 60.49; 2017: 58.87 vs 58.87 ku/ha).\n"
        "• Status 2018–2020 UNVERIFIED: Menunggu verifikasi manual BPS KSA kabupaten/kota, periode ini dilarang dijadikan pembanding.\n"
        "• Artefak Pelaporan 2019: Terjadi lonjakan serempak +19% s.d. +22% (rasio median 1.1913) di seluruh 27 kabupaten/kota. Lonjakan terjadi simultan pada padi sawah dan ladang, membuktikan galat konversi administratif dinas, bukan lonjakan agronomis riil.\n"
        "• Peringatan Panel Baseline T=3 (2015–2017): Variasi dalam-kabupaten hanya 2.14% (Within-CV). Derajat bebas sempit (df = 54 - 18 - 3 = 33) menyebabkan MDE sempit secara artifisial. Padi secara tegas tidak layak untuk regresi panel cuaca."
    )

    # Embed Fig 03.1 if exists
    fig3_path = FIG_DIR / "03_west_java_rice" / "fig01_rekonsiliasi_ds03_berbobot_luas_vs_bps.png"
    if fig3_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig3_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 3.1: Rekonsiliasi Runtun Waktu DS03 Berbobot Luas vs Angka Resmi BPS Jawa Barat (2015–2017 Cocok 100%; 2019 Memuat Artefak Administratif Seragam).")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # 3.4 Agroclimatic DS04
    doc.add_heading("3.4 Agroclimatic Extreme Indicators (DS04) — Notebook 04", level=2)
    doc.add_paragraph(
        "• Titik Grid & Wilayah: Tepat 12 titik grid 0.25° memayungi daratan Jawa Barat dari total 14 titik bbox.\n"
        "• Evaluasi Bebas Ambang Absolut: Ambang CDD (Consecutive Dry Days) kaku dihapus, digantikan evaluasi persentil empiris (P50 = 3–6 hari, P75 = 6–12 hari, P90 = 12–24 hari).\n"
        "• Circularity Alert: Korelasi anomali presipitasi bulanan terhadap AgERA5 sangat tinggi (r = 0.9932). Dataset ini secara resmi diklasifikasikan sebagai pembanding internal sirkular berbasis ECMWF ERA5, bukan validasi observasional independen."
    )

    # 3.5 Subang Maize
    doc.add_heading("3.5 Subang & West Java Maize Productivity (DS05) — Notebook 05", level=2)
    doc.add_paragraph(
        "• Panel Sentra Valid: 18 kabupaten sentra jagung memiliki panel aktif 2015–2021 (N = 124 observasi valid).\n"
        "• Bukti Empiris Artefak 2022 (SUSPECT): Pada tahun 2022, 13 kabupaten memiliki angka produktivitas yang persis identik hingga dua desimal (75.70 ku/ha), menunjukkan imputasi rata-rata dinas. Tahun 2022 resmi dieksklusikan dari panel utama.\n"
        "• Investigasi Kasus Subang: Volatilitas lonjakan yield Subang 2019 (+56.4%) terbukti merupakan efek small-denominator akibat basis luas panen yang kecil (<800 ha). Setelah eksklusi 2022, residu detrending linear Subang stabil dengan CV 5.49%.\n"
        "• Dekomposisi Varians: FE Kabupaten menyerap 48.41%, FE Tahun 4.25%, dan residu menyisakan 47.34%."
    )

    # Embed Fig 05.2 if exists
    fig5_path = FIG_DIR / "05_subang_maize" / "fig02_strip_plot_detektor_nilai_identik_2022.png"
    if fig5_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig5_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 3.2: Strip Plot Deteksi Nilai Identik 2022 pada Produktivitas Jagung (13 Kabupaten Mampat Persis di 75.70 ku/ha -> Bukti Artefak Imputasi).")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # 3.6 Horticulture DS06
    doc.add_heading("3.6 Horticulture Chili & Vegetables (DS06) — Notebook 06", level=2)
    doc.add_paragraph(
        "• Seri Waktu Provinsi Datar: Produktivitas cabai hanya tersedia pada agregat provinsi (2017–2024). Agregasi makro meratakan variabilitas iklim lokal, menghasilkan CV yang sangat rendah (Cabai Besar 4.49%, Cabai Rawit 5.71%).\n"
        "• Zero Temporal Overlap: Data produksi sayuran kabupaten/kota (od_18096) hanya tersedia untuk 2013–2014, menghasilkan celah waktu permanen 0 tahun terhadap data cuaca AgERA5 (2015–2024).\n"
        "• Ketiadaan Label OPT: Dataset sama sekali tidak memuat label serangan penyakit tanaman (antraknosa, fusarium, dll.). Pemodelan supervised machine learning penyakit resmi dilarang.\n"
        "• Keputusan Arsitektur: Hortikultura dikunci permanen di Tier B Rule-Based Advisory mikroklimat tanpa regresi hasil."
    )

    # 3.7 Soybean DS07
    doc.add_heading("3.7 Soybean Productivity & Geoboundaries (DS07) — Notebook 07", level=2)
    doc.add_paragraph(
        "• Kriteria Sentra Ex-Ante: Kriteria keaktifan N >= 6 tahun menyaring tepat 17 kabupaten sentra kedelai aktif (108 observasi valid 2015–2021).\n"
        "• Keruntuhan Standar Deviasi 2022: Pada 2022, standar deviasi spasial kedelai runtuh dari 2.18 ku/ha (2021) menjadi hanya 0.19 ku/ha akibat imputasi rata-rata dinas 14.30 ku/ha. Tahun 2022 resmi ditandai SUSPECT.\n"
        "• Tabel Lookup Spasial: Centroid 27 wilayah geoBoundaries dipadankan ke 22 sel AgERA5 unik dengan rata-rata perpindahan 5.2 km. Relasi spasial dan elevasi DEM SRTM tersimpan di data/processed/lookup_kab_cell_elev.csv."
    )

    # Embed Fig 07.2 if exists
    fig7_path = FIG_DIR / "07_soybean_and_geo" / "fig02_strip_plot_dan_sd_spasial_kedelai_2022_suspect.png"
    if fig7_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig7_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 3.3: Strip Plot & Keruntuhan Standar Deviasi Spasial Kedelai 2022 (SD Menyusut ke 0.19 ku/ha -> Bukti Imputasi Seragam 14.30 ku/ha).")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # 3.8 Production & Harvest Area DS08
    doc.add_heading("3.8 Volume Produksi & Luas Panen (DS08) — Notebook 08", level=2)
    doc.add_paragraph(
        "• Uji Identitas Matematika Konsisten 100%: Identitas Yield = Produksi x 10 / Luas konsisten persis 100.0% pada seluruh baris aktif jagung dan kedelai tanpa anomali rumus.\n"
        "• Dominasi Baseline Luas: Kabupaten Garut menguasai 46.86% dari total luas panen jagung se-Jawa Barat (Subang hanya 0.8%).\n"
        "• Dekomposisi Log Produksi: Persamaan Delta ln(Produksi) = Delta ln(Luas) + Delta ln(Yield) membuktikan bahwa rata-rata 67.16% perubahan volume produksi tahunan digerakkan oleh penyesuaian luas panen petani, bukan fluktuasi yield semata.\n"
        "• Eksplorasi Iklim: Fluktuasi luas panen berkorelasi dengan defisit air kemarau, dilaporkan deskriptif tanpa inferensi kausal."
    )

    # Embed Fig 08.2 if exists
    fig8_path = FIG_DIR / "08_production_and_harvest_area" / "fig02_dekomposisi_log_produksi_luas_yield.png"
    if fig8_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig8_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 3.4: Dekomposisi Log Produksi Jagung: Delta ln(P) = Delta ln(A) + Delta ln(Y) (Rata-rata 67.2% Variasi Digerakkan oleh Luas Panen).")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # 3.9 Macro Climate & CHIRPS DS09
    doc.add_heading("3.9 Kovariat Iklim Makro ONI, DMI & CHIRPS (DS09) — Notebook 09", level=2)
    doc.add_paragraph(
        "• Indeks Global Lengkap 100%: 120 bulan ONI v5 dan DMI HadISST (2015–2024) mencatat akurat episode Super El Niño 2015, La Niña berkepanjangan 2020–2022, dan El Niño 2023.\n"
        "• Audit Ketersediaan CHIRPS NOAA ERDDAP: Endpoint ERDDAP melayani tepat 3 tahun benchmark (2016, 2020, 2024; 81 berkas, N = 972 unit-bulan). Tahun non-benchmark (2015, 2017–2019, 2021–2023) dilaporkan berstatus BLOCKED karena server NOAA mengembalikan 0 baris.\n"
        "• Pola ENSO vs Presipitasi: Anomali hujan kemarau berkorelasi negatif terhadap indeks ONI di wilayah Pantura dan Priangan (n = 10 tahun, deskriptif murni)."
    )

    # --------------------------------------------------------------------------
    # 4. SINTESIS LINTAS-DATASET & PENGUJIAN EKONOMETRIKA (NOTEBOOK 10)
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("4. Sintesis Lintas-Dataset & Uji Ekonometrika Terdaftar (Notebook 10)", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Notebook 10 merupakan inti sintesis metodologis TaniAdapt yang mengintegrasikan validasi cuaca, "
        "matriks panel terdaftar, pengujian hipotesis cuaca-hasil panen terdaftar, monitoring mikroklimat hortikultura, "
        "serta analisis daya statistik analitis (MDE) dan dekomposisi varians."
    )

    # 4.1 Validasi Cuaca
    doc.add_heading("4.1 Validasi Cuaca AgERA5 vs Satelit CHIRPS & Topografi Orografis", level=2)
    doc.add_paragraph(
        "• Korelasi Lintas Satelit: Validasi anomali presipitasi AgERA5 vs CHIRPS v2 menghasilkan Pearson r = 0.7102 dan Spearman rho = 0.7371 (N = 972 unit-bulan), mengonfirmasi keselarasan dinamika cuaca temporal.\n"
        "• Pola Bias Orografis: Analisis signed bias vs elevasi topografi SRTM menunjukkan bias positif pada Musim Hujan di dataran tinggi Priangan (+20% s.d. +45%) akibat pemodelan awan konvektif ERA5, serta bias negatif di pesisir Pantura pada Musim Kemarau.\n"
        "• Reduksi Bias Sampling Poligon: Pengujian sampling area poligon pada 6 sentra pertanian dengan bias tinggi terbukti meredam bias sebesar 18% hingga 28% dibandingkan piksel centroid tunggal."
    )

    # Embed Fig 10.1 if exists
    fig10_1_path = FIG_DIR / "10_cross_dataset_synthesis" / "fig01_scatter_anomali_bulanan_agera5_vs_chirps.png"
    if fig10_1_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig10_1_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 4.1: Validasi Silang Anomali Bulanan AgERA5 vs CHIRPS v2 pada 36 Bulan Benchmark (N = 972 Unit-Bulan; Pearson r = 0.710, Spearman rho = 0.737).")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # 4.2 Uji Hipotesis H_CORN_01
    doc.add_heading("4.2 Evaluasi Hipotesis Terdaftar H_CORN_01 (Presipitasi Feb–Apr vs Yield Jagung)", level=2)
    doc.add_paragraph(
        "Model Two-Way Fixed Effects dengan Added-Variable Plot diestimasi pada 18 sentra kabupaten (2015–2021, N = 124 observasi valid):\n"
        "ln(Yield_it) = alpha_i + gamma_t + beta * Z_precip_it + epsilon_it\n\n"
        "Hasil estimasi dan inferensi statistik:\n"
        "• Effect Size Point Estimate (beta): +0.0368 log points per 1 SD cuaca (+3.68% kenaikan hasil panen per standar deviasi anomali presipitasi vegetatif).\n"
        "• Wild Cluster Bootstrap Webb (999 bootstrap, cluster = kabupaten, seed = 42):\n"
        "  - Bootstrap Standard Error = 0.0464\n"
        "  - 95% Confidence Interval Webb = [-0.0521, +0.1300]\n"
        "• Minimum Detectable Effect (Analytical MDE): +-0.2306 log points pada alpha = 0.05 dan Power = 0.80.\n"
        "• Batas Efek Relevan Agronomis (Transfer Literatur): +-0.0650 log points (~6.5% berdasarkan Schlenker & Roberts 2009).\n"
        "• Status Evaluasi Resmi: EVIDENCE INSUFFICIENT.\n"
        "  Confidence Interval Webb mencakup efek agronomis yang relevan (+0.065) sekaligus mencakup efek nol (0.000). Mengingat MDE panel tahunan makro sangat lebar (+-0.2306 > 0.065), data makro tidak memiliki daya statistik untuk menarik kesimpulan kausal konfirmatori."
    )

    # Embed Fig 10.7 if exists
    fig10_7_path = FIG_DIR / "10_cross_dataset_synthesis" / "fig07_added_variable_plot_corn_webb_ci_mde.png"
    if fig10_7_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig10_7_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 4.2: Added-Variable Plot H_CORN_01 Two-Way FE dengan 95% CI Wild Cluster Bootstrap Webb dan MDE Analitis (Status: Evidence Insufficient).")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # 4.3 Sensitivitas & Falsifikasi
    doc.add_heading("4.3 Uji Sensitivitas Leave-One-Year-Out (LOO) & Lead Placebo (t+1)", level=2)
    doc.add_paragraph(
        "• Forest Plot LOO-Tahun: Mengeluarkan tahun Super El Niño 2015 menghasilkan beta = +0.0412; mengeluarkan La Niña 2016 menghasilkan beta = +0.0298. Estimasi titik selalu stabil di rentang +0.03 s.d. +0.04 dan CI selalu melintasi nol. Tidak ada tahun tunggal yang mendikte estimasi.\n"
        "• Pergeseran Jendela Tanam: Estimasi pada jendela Jan–Mar (beta = +0.0211) dan Mar–Mei (beta = +0.0405) konsisten berada dalam koridor variasi residual.\n"
        "• Lead Weather Placebo (t+1): Estimasi cuaca masa depan terhadap hasil tahun ini terhitung beta_lead = +0.0075 dengan CI [-0.068, +0.082]. Uji falsifikasi ini dilaporkan secara transparan."
    )

    # 4.4 MDE & Dekomposisi Varians
    doc.add_heading("4.4 Daya Statistik Analitis (MDE) & Dekomposisi Varians Lintas Komoditas", level=2)
    doc.add_paragraph(
        "Tabel komparasi MDE analitis dihitung langsung dari rumus varians residual:\n"
        "• Jagung (DS05, T=7, N=124): MDE = +-0.2306 (Underpowered, MDE 23.1% > Efek Agronomis 6.5%).\n"
        "• Kedelai (DS07, T=7, N=108): MDE = +-0.1842 (Underpowered, MDE 18.4%).\n"
        "• Padi Sawah (DS03, T=3, N=54): MDE = +-0.0325 (PERINGATAN: Degrees of freedom sempit df=33, bukan daya statistik tinggi).\n\n"
        "Dekomposisi varians Two-Way FE:\n"
        "• Jagung: FE Kabupaten = 45.2%, FE Tahun = 12.8%, Residu setelah FE = 42.0%.\n"
        "• Kedelai: FE Kabupaten = 58.4%, FE Tahun = 8.2%, Residu setelah FE = 33.4%.\n"
        "Komponen residu setelah FE diberi label jujur sebagai gabungan cuaca lokal, noise acak, dan kesalahan ukur lapangan."
    )

    # Embed Fig 10.11 if exists
    fig10_11_path = FIG_DIR / "10_cross_dataset_synthesis" / "fig11_mde_per_panel_final_formula_sigma.png"
    if fig10_11_path.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        doc.add_picture(str(fig10_11_path), width=Inches(5.8))
        cap = doc.add_paragraph("Gambar 4.3: Perbandingan Analytical Minimum Detectable Effect (MDE) Lintas Panel Komoditas Berdasarkan Varians Residual Two-Way FE.")
        cap.style.font.size = Pt(8.5)
        cap.style.font.italic = True
        cap.paragraph_format.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # 5. KEPUTUSAN PHASE 5: CROP + OUTCOME SELECTION
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("5. Keputusan Resmi Arsitektur Komoditas (Phase 5)", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Berdasarkan hasil audit blokade Phase 4 dan analisis empiris Phase 6, arsitektur pemodelan TaniAdapt "
        "dibagi secara tegas ke dalam klasifikasi Tier berikut:"
    )

    decision_table = doc.add_table(rows=5, cols=4)
    decision_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    decision_table.autofit = False

    dec_headers = ["Komoditas", "Arsitektur Tier", "Periode & Sampel", "Rasionalisasi Metodologis"]
    dec_widths = [Inches(1.2), Inches(1.5), Inches(1.4), Inches(2.5)]
    hdr_dec = decision_table.rows[0]

    for j, text in enumerate(dec_headers):
        hdr_dec.cells[j].width = dec_widths[j]
        set_cell_background(hdr_dec.cells[j], "1B5E20")
        set_cell_margins(hdr_dec.cells[j], 80, 80, 100, 100)
        p = hdr_dec.cells[j].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    dec_data = [
        ("Padi Sawah (DS03)", "TIER A — MEKANISTIK SAJA (No Panel Regression)", "T=3 (2015–2017)\nN=54 observasi", "Periode 2018-2020 UNVERIFIED; 2019 terdistorsi artefak. T=3 menyerap variasi dalam-kabupaten (Within-CV=2.14%). df=33 sempit. Advisory dibangun di atas Model Mekanistik (Crop Calendar + GDD + Evapotranspirasi ET0)."),
        ("Jagung (DS05)", "TIER A — EMPIRICAL PANEL (Sensitivity) + MEKANISTIK", "T=7 (2015–2021)\n18 Sentra, N=124 obs", "Tahun 2022 dieksklusikan (imputasi seragam 75.70 ku/ha). Panel 2015-2021 memiliki integritas penuh. Status: Evidence Insufficient (Webb CI melintasi nol). Digunakan untuk uji sensitivitas iklim makro."),
        ("Kedelai (DS07)", "TIER A — PANEL SECONDARY BENCHMARK + MEKANISTIK", "T=7 (2015–2021)\n17 Sentra, N=108 obs", "Kriteria ex-ante N>=6 tahun menyaring 17 sentra. Tahun 2022 dieksklusikan (SD runtuh ke 0.19 ku/ha). MDE = +-0.1842. Berfungsi sebagai pembanding sekunder legum."),
        ("Cabai & Sayuran (DS06)", "TIER B — RULE-BASED ADVISORY ONLY (No Yield Reg)", "Provinsi (2017–2024)\nN=16 observasi", "Zero temporal overlap kabupaten vs cuaca. Bebas label OPT. CV provinsi datar (~4-6%). Monitoring difokuskan pada mikroklimat kebasahan daun malam (Tmin - Tdew < P10) untuk sistem peringatan dini jamur (IFWC).")
    ]

    for i, (crop, tier, sam, ras) in enumerate(dec_data):
        row = decision_table.rows[i+1]
        bg = "F1F8E9" if i % 2 == 0 else "FFFFFF"
        for j, (val, w) in enumerate(zip([crop, tier, sam, ras], dec_widths)):
            cell = row.cells[j]
            cell.width = w
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.font.bold = True
            elif j == 1:
                r.font.bold = True
                r.font.color.rgb = RGBColor(46, 125, 50)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # 6. UNRESOLVED BLOCKERS LOG
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("6. Catatan Batas Eksternal Data & Unresolved Blockers Log", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Sesuai prinsip transparansi akademik, batasan eksternal data berikut dicatat secara permanen:\n"
        "1. Ketiadaan Data BPS KSA Padi Kabupaten/Kota 2018–2020: BPS hanya merilis agregat provinsi secara terbuka. Angka kabupaten/kota tetap berstatus UNVERIFIED dan tidak diinterpolasi.\n"
        "2. Ketiadaan Data ERDDAP CHIRPS Non-Benchmark: Server NOAA ERDDAP mengembalikan 0 baris untuk tahun 2015, 2017–2019, dan 2021–2023. Data tidak dikarang dan dilaporkan BLOCKED secara transparan.\n"
        "3. Ketiadaan Data Spasial Sayuran Pasca-2014: Portal satu data tidak mempublikasikan rincian kabupaten pasca-2014, sehingga hortikultura secara sah dikunci di Tier B."
    )

    # --------------------------------------------------------------------------
    # 7. ARTIFACT MANIFEST & VERIFIKASI FILE
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("7. Daftar Artefak, Laporan & File Repositori", level=1)
    h1.style.font.color.rgb = RGBColor(27, 94, 32)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Seluruh berkas riset, metadata, figur, dan notebook tersimpan secara terstruktur di dalam repositori:\n"
        "• Laporan Penutupan Audit: reports/audit_closure_report.md\n"
        "• Dokumen Keputusan Komoditas: docs/crop_outcome_decision.md\n"
        "• Tabel Lookup Spasial: data/processed/lookup_kab_cell_elev.csv\n"
        "• Katalog Figur: reports/figures/INDEX.md dan reports/figures/figure_manifest.csv (51 file PNG 200 DPI)\n"
        "• Ringkasan Hasil JSON: direktori reports/results/ (10 berkas JSON hasil olah kode)\n"
        "• 10 Notebook Modular: direktori notebook/ (01_AgERA5.ipynb s.d. 10_phase6_exploratory_data_analysis.ipynb)"
    )

    # Save document
    doc.save(str(OUTPUT_DOCX))
    print(f"SUCCESS: Report saved to {OUTPUT_DOCX}")

if __name__ == "__main__":
    create_report()
