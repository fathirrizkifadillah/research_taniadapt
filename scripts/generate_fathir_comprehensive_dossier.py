"""Generate Comprehensive Dossier for Fathir in Indonesian (.docx).
Location: context/to_fathir/TaniAdapt_Laporan_Lengkap_Riset_Phase0_sampai_Phase12_Untuk_Fathir.docx
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT_DOCX = Path("context/to_fathir/TaniAdapt_Laporan_Lengkap_Riset_Phase0_sampai_Phase12_Untuk_Fathir.docx")
OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)

NAVY = "1B365D"
STEEL = "2C5282"
PALE_BG = "F4F6F9"
BORDER_GRAY = "CCCCCC"


def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)


def set_cell_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for s in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{s}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), BORDER_GRAY)
        borders.append(b)
    tcPr.append(borders)


def format_cell(cell, text, bold=False, white=False, size=8.5, center=False, color_override=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.05
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(str(text))
    run.bold = bold
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    if white:
        run.font.color.rgb = RGBColor(255, 255, 255)
    elif color_override:
        r, g, b = int(color_override[0:2], 16), int(color_override[2:4], 16), int(color_override[4:6], 16)
        run.font.color.rgb = RGBColor(r, g, b)
    else:
        run.font.color.rgb = RGBColor(40, 40, 40)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_borders(cell)


def add_table_data(doc, headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_shading(cell, NAVY)
        format_cell(cell, h, bold=True, white=True, size=8.8, center=True)
        cell.width = Inches(widths[i])
    hdr._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for r_idx, r_data in enumerate(rows):
        row = t.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        bg = PALE_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            if bg != "FFFFFF":
                set_cell_shading(cell, bg)
            is_c = (c_idx == 0 or (c_idx == 1 and len(str(val)) <= 15))
            color_override = None
            val_str = str(val)
            if any(k in val_str for k in ["COMPLETED", "PASS", "VERIFIED", "Sangat Aman", "100%", "Detected", "Aktif"]):
                color_override = "1B6E34"
            elif any(k in val_str for k in ["PENDING", "Waspada", "WARN", "88.9%", "sebagian"]):
                color_override = "B45309"
            elif any(k in val_str for k in ["stres", "insufficient", "BLOCKED", "DANGER", "Hindari", "FAIL", "INVALID", "DEPRECATED", "Ditolak"]):
                color_override = "B91C1C"
            format_cell(cell, val, bold=(c_idx == 0), white=False, size=8.3, center=is_c, color_override=color_override)
            cell.width = Inches(widths[c_idx])
    doc.add_paragraph()


def add_image_box(doc, img_path: Path, caption: str, width_inches: float = 6.2):
    if not img_path.exists():
        print(f"Warning: image {img_path} not found.")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(str(img_path), width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = "Aptos"
    run_cap.font.size = Pt(8.0)
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGBColor(90, 90, 90)


def add_heading_1(doc, text: str):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Aptos Display"
        r.font.size = Pt(15)
        r.bold = True
        r.font.color.rgb = RGBColor(27, 54, 93)


def add_heading_2(doc, text: str):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(3)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Aptos"
        r.font.size = Pt(12)
        r.bold = True
        r.font.color.rgb = RGBColor(44, 82, 130)


def add_heading_3(doc, text: str):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.space_before = Pt(6)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Aptos"
        r.font.size = Pt(10.5)
        r.bold = True
        r.font.color.rgb = RGBColor(40, 40, 40)


def add_p(doc, text: str, bold_prefix: str = "", italic: bool = False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Aptos"
        r_pre.font.size = Pt(9.5)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(27, 54, 93)
    r = p.add_run(text)
    r.font.name = "Aptos"
    r.font.size = Pt(9.5)
    r.italic = italic
    r.font.color.rgb = RGBColor(30, 30, 30)
    return p


def add_callout(doc, text: str, title: str = "CATATAN PENTING"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, PALE_BG)
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    left_b = OxmlElement("w:left")
    left_b.set(qn("w:val"), "single")
    left_b.set(qn("w:sz"), "24")
    left_b.set(qn("w:space"), "0")
    left_b.set(qn("w:color"), NAVY)
    borders.append(left_b)
    for s in ("top", "bottom", "right"):
        none_b = OxmlElement(f"w:{s}")
        none_b.set(qn("w:val"), "none")
        borders.append(none_b)
    tcPr.append(borders)
    cell.width = Inches(6.5)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r_tit = p.add_run(f"📌 {title}: ")
    r_tit.bold = True
    r_tit.font.name = "Aptos"
    r_tit.font.size = Pt(9.0)
    r_tit.font.color.rgb = RGBColor(27, 54, 93)
    r_txt = p.add_run(text)
    r_txt.font.name = "Aptos"
    r_txt.font.size = Pt(9.0)
    r_txt.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph()


def build_dossier():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title & Metadata
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("TANIADAPT: LAPORAN LENGKAP RISET & CETAK BIRU SISTEM")
    r_title.bold = True
    r_title.font.name = "Aptos Display"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(27, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("Perjalanan Ilmiah Phase 0 s/d Phase 12, Rekonsiliasi Statistik Lapangan,\nModel Biofisik Mekanistik FAO-56, Status Komoditas, & Panduan Integrasi Aplikasi Web Next.js")
    r_sub.font.name = "Aptos"
    r_sub.font.size = Pt(11)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(44, 82, 130)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Disusun Khusus Untuk: Fathir Rizki Fadillah | Repositori: research_taniAdapt | Git Tag: phase13-gate-ready (Commit deccd9f)")
    r_meta.font.name = "Aptos"
    r_meta.font.size = Pt(9.0)
    r_meta.bold = True
    r_meta.font.color.rgb = RGBColor(100, 100, 100)

    # =========================================================================
    # BAGIAN 1: DUDUK PERKARA
    # =========================================================================
    add_heading_1(doc, "1. DUDUK PERKARA: KITA SEBENARNYA LAGI BIKIN APA & KENAPA?")
    
    add_p(doc, 
        "TaniAdapt adalah platform Agricultural Decision Support System (DSS) dan presisi agroadvisory hiperlokal yang dirancang khusus untuk petani kecil (smallholders) dan pengelola kebun (farm managers) di Jawa Barat. Tujuan proyek ini sangat jelas dan membumi: memberikan rekomendasi tindakan harian di lapangan (kapan harus menyiram, memupuk, menyemprot pestisida, atau memanen) secara tepat waktu, berbasis data cuaca lokal per jam, dan memiliki landasan sains biofisik yang kokoh.",
        bold_prefix="Apa Sebenarnya TaniAdapt? "
    )
    
    add_p(doc,
        "Di lapangan Jawa Barat, petani saat ini menghadapi disrupsi iklim tropis yang masif. Kalender tanam tradisional seperti Pranata Mangsa maupun kalender statis dinas tidak lagi sinkron dengan pergeseran musim hujan dan kemarau ekstrem (La Niña 2016, Kemarau Positif IOD 2019, Super El Niño 2023). Petani sering menyemprot pestisida di pagi hari yang kemudian tersapu hujan siang, atau menyemprot saat angin kencang sehingga terjadi drift (penyimpangan semprot) yang membahayakan kesehatan dan mencemari lingkungan. Sementara itu, prakiraan cuaca umum di aplikasi ponsel pintar hanya memberikan informasi cuaca makro harian (misal: 'Hujan Ringan') tanpa memberi tahu petani apa yang harus dilakukan pada jam 07.00 atau 14.00 WIB.",
        bold_prefix="Masalah Nyata di Lapangan: "
    )

    add_callout(doc,
        "Di dunia AI saat ini, banyak pihak tergiur langsung menghubungkan LLM (seperti ChatGPT atau Claude) dengan petani untuk menanyakan dosis obat atau diagnosis penyakit tanaman. Dalam riset TaniAdapt, ini adalah TINDAKAN ILEGAL DAN BERBAHAYA. LLM memiliki sifat stokastik (probabilistik) dan rawan mengalami halusinasi numerik. Jika LLM mengarang dosis fungisida atau herbisida sintetik, tanaman bisa mati terbakar dan petani kecil terancam bangkrut atau keracunan.",
        title="MENGAPA LLM DILARANG MENGAMBIL KEPUTUSAN?"
    )

    add_p(doc,
        "Untuk memecahkan masalah di atas secara radikal dan aman, TaniAdapt mengadopsi Arsitektur Decoupled (Terpisah). Sistem dibagi menjadi dua lapisan yang terisolasi:",
        bold_prefix="Solusi Arsitektur Decoupled TaniAdapt: "
    )
    
    add_p(doc,
        "1. Lapisan Otak Keputusan (Decision Engine): 100% deterministik, berbasis aturan agrometeorologi terstruktur (rules.json), rumus evapotranspirasi FAO-56 Penman-Monteith, dan neraca deplesi air tanah (Dr > RAW). Lapisan ini tidak menggunakan AI generatif sama sekali. Output-nya adalah objek data terstruktur (JSON) yang terikat kontrak skema ketat.\n"
        "2. Lapisan Komunikasi (LLM / Conversational Layer): Murni sebagai penerjemah dan narator rekam jejak keputusan (decision trace). LLM hanya membaca alasan yang sudah diputuskan oleh Decision Engine dan menerjemahkannya ke dalam bahasa daerah/Indonesia yang santun. LLM dilarang keras mengubah angka, mengarang ambang batas baru, atau merekomendasikan zat kimia aktif."
    )

    # =========================================================================
    # BAGIAN 2: KRONOLOGI PERJALANAN RISET (PHASE 0 S/D PHASE 12)
    # =========================================================================
    add_heading_1(doc, "2. KRONOLOGI LENGKAP PERJALANAN RISET (PHASE 0 S/D PHASE 12)")
    add_p(doc, "Riset ini dijalankan secara disiplin melalui 13 fase berurutan. Berikut cerita lengkap perjalanan, temuan mengejutkan, kegagalan hipotesis, dan keputusan yang diambil:")

    # Phase 0 & 1
    add_heading_2(doc, "Phase 0 & Phase 1: Definisi Masalah, Pertanyaan Riset, & Integritas Hipotesis")
    add_p(doc,
        "Riset diawali dengan merumuskan 3 Pertanyaan Riset Utama (RQ1: Sensitivitas cuaca terhadap hasil panen di Jabar; RQ2: Keterbatasan data historis lokal; RQ3: Perancangan decision engine deterministik). Dari sini diturunkan 11 hipotesis fenologi musiman (H_CORN_01 s/d 04, H_SOY_01 s/d 03, H_RICE_01 s/d 04).",
        bold_prefix="RQ dan Hipotesis: "
    )
    add_p(doc,
        "Dalam audit integritas ilmiah, kami mencatat secara jujur bahwa berkas hipotesis pertama kali di-commit pada 2026-10-11 (commit 4629ad9), sedangkan akses data mentah telah berlangsung sejak 2026-10-05 (commit 0d53072). Oleh karena itu, seluruh hipotesis dilaporkan secara transparan sebagai 'hipotesis eksploratori terdaftar setelah akses data' (post-data-access documentation), bukan pra-registrasi eks-ante murni. Ini adalah standar etika sains tertinggi.",
        bold_prefix="Catatan Integritas Ilmiah: "
    )

    # Phase 2 & 3
    add_heading_2(doc, "Phase 2 & Phase 3: Penelaahan Literatur Mendalam & Fusi Data Geospasial")
    add_p(doc,
        "Kami membedah 16 literatur agrometeorologi internasional (standar irigasi FAO-56 Allen et al. 1998, durasi kebasahan daun Sentelhas et al. 2008, ekonometrika cuaca panel Schlenker & Roberts 2009, Lobell et al. 2011, serta wild bootstrap Webb 2014) dan membandingkan 15 kompetitor DSS global. Seluruh parameter dipilah ke dalam Evidence Registry: parameter berstatus VERIFIED_METHOD (didukung rumus dan tabel buku teks resmi) dan parameter UNVERIFIED/CONVENTION (aturan lapangan praktis).",
        bold_prefix="Tinjauan Pustaka: "
    )
    add_p(doc,
        "Pada Phase 3, kami mengumpulkan 8 dataset aktif: data reanalisis atmosfer harian ECMWF AgERA5 (1991–2024), data produktivitas dinas pertanian Jawa Barat (Padi DS03, Jagung DS05, Kedelai DS07, Hortikultura DS08), serta batas administrasi ADM2 BPS. Kami memetakan seluruh 27 Kabupaten/Kota Jawa Barat ke dalam 22 sel grid AgERA5 unik (resolusi 0.1° x 0.1° atau ~11 km) dan menghubungkannya dengan model elevasi digital SRTM DEM. Jarak offset geospasial rata-rata antara centroid kabupaten ke titik grid cuaca terdekat adalah 5.80 km (formula Haversine).",
        bold_prefix="Fusi Geospasial: "
    )

    add_image_box(doc,
        Path("reports/figures/07_soybean_and_geo/fig04_peta_poligon_centroid_sel_agera5.png"),
        "FIGUR 1: Peta Geospasial Jawa Barat — Pemetaan Batas Administrasi 27 Kabupaten/Kota, Titik Centroid, dan 22 Sel Grid AgERA5 Representatif (Jarak Offset Rata-rata 5.80 km)."
    )

    # Phase 4
    add_heading_2(doc, "Phase 4: Audit Integritas Data & Pembongkaran 11 Blocker (A1–A11)")
    add_p(doc, "Phase 4 adalah titik balik terpenting dalam proyek ini. Ketika kami melakukan audit data forensik secara mendalam terhadap dataset pemerintah daerah, kami menemukan anomali-anomali fatal yang jika diabaikan akan merusak validitas sistem:")
    
    audit_rows = [
        ["A1 & B1", "Padi Jawa Barat (DS03)", "Ditemukan lonjakan produksi seragam +21.8% pada 2019 akibat perubahan konversi GKP Galura. Seri BPS terverifikasi manusia pada 2015 (61.22), 2018 (56.51), dan 2019 (57.54). Patahan metode KSA 2017→2018 menyebabkan data 2018-2019 tidak sebanding dengan 2015.", "SOLVED: Periode 2018-2020 resmi dieksklusikan dari panel utama."],
        ["A2", "Korelasi Spasial Makro", "22 sel cuaca Jabar terkorelasikan sangat tinggi (r=0.727). Analisis PCA membuktikan PC1 menyerap 74.97% varians spasial. Jabar secara agroklimat adalah satu klaster regional besar.", "SOLVED: Menghentikan klaim 54 observasi independen; evaluasi dialihkan ke level regional."],
        ["A3 & A4", "Jagung Subang & Jabar (DS05)", "Ditemukan data imputasi seragam birokrasi pada 2022: 13 kabupaten memiliki angka produktivitas PERSIS SAMA yaitu 75.70 ku/ha. Dekomposisi membuktikan 98.4% lonjakan produksi Subang disumbang ekspansi lahan, bukan cuaca.", "SOLVED: Tahun 2022 DIBUANG BERSIH dari seluruh model sensitivitas."],
        ["A5 & B1", "Kedelai Jawa Barat (DS07)", "Sebanyak 13 kabupaten memiliki angka imputasi kembar 75.70 ku/ha pada 2022. Dari 18 kabupaten, Kab. Bekasi hanya aktif 2 tahun, menyisakan 17 sentra aktif ex-ante (17 sel cuaca unik, N=112 baris valid pasca filter MAD-z).", "SOLVED: Tahun 2022 dieksklusi total; baseline dikunci pada 17 sentra aktif."],
        ["A6", "Hortikultura (Cabai & Tomat)", "Data serangan hama dan penyakit (OPT) ground truth lokal sama sekali TIDAK TERSEDIA di Jabar. Data dinas mengalami diskontinuitas pasca-2014.", "SOLVED: Mengunci hortikultura pada Tier B Literature Transfer; dilarang keras membuat model ML OPT."],
        ["A7", "Denominator CHIRPS (DS04)", "Klaim awal menyebut 3.000 observasi bulanan. Koreksi audit: 26 kab x 36 bulan = 936 unit-bulan.", "SOLVED: Denominator distandardisasi menjadi 936."],
        ["A8 s/d A11", "Geospasial & Duplikasi", "Duplikasi sel spasial, ambang baseline 30-tahun CDS vs 10-tahun lokal.", "SOLVED: Seluruh 11 blocker audit resmi DITUTUP LENGKAP."]
    ]
    add_table_data(doc, ["Kode", "Dataset", "Temuan Forensik Audit", "Tindakan Penyelesaian"], audit_rows, [0.8, 1.5, 3.0, 1.2])

    # Phase 5
    add_heading_2(doc, "Phase 5: Pemilihan & Penguncian Portofolio 5 Komoditas")
    add_p(doc,
        "Berdasarkan hasil audit Phase 4, kami mengambil Keputusan Portofolio Resmi (docs/crop_outcome_decision.md):",
        bold_prefix="Seleksi Komoditas: "
    )
    add_p(doc,
        "1. Padi Sawah: Jalur penasihat mekanistik murni. Dilarang membuat model regresi yield cuaca. Modul penyiraman air tanah dinyatakan 'evidence_insufficient' karena sawah di Jabar berregim tergenang (ponded).\n"
        "2. Jagung: Jalur sensitivitas empiris + penasihat mekanistik FAO-56 (N=121 valid, 2015–2021).\n"
        "3. Kedelai: Jalur sensitivitas empiris + penasihat mekanistik FAO-56 (N=112 valid, 17 sentra aktif, 2015–2021).\n"
        "4. Cabai (Merah & Rawit): Jalur transfer literatur Tier B. Dilarang memprediksi penyakit numerik.\n"
        "5. Tomat: Jalur transfer literatur Tier B + penasihat kebutuhan air FAO-56 (Kc terverifikasi).\n"
        "6. Bawang Merah: DIBLOKIR TOTAL (blocked pending new data) karena data dinas tidak representatif."
    )

    # Phase 6 & 7
    add_heading_2(doc, "Phase 6 & Phase 7: Analisis Statistik Ekonometrika & Mengapa 100% Hipotesis Insufficient")
    add_p(doc,
        "Di Phase 7, kami menguji ke-11 hipotesis fenologi menggunakan model ekonometrika panel Two-Way Fixed Effects (Kabupaten FE + Year FE) dengan koreksi klaster kecil Wild Cluster Bootstrap Webb (B=999 ulangan) serta koreksi pengujian ganda Holm-Bonferroni.",
        bold_prefix="Metodologi Ekonometrika: "
    )
    add_p(doc,
        "Hasilnya sangat mengejutkan: 100% hipotesis menghasilkan status EVIDENCE_INSUFFICIENT! Mengapa demikian? Karena nilai estimasi efek cuaca (koefisien beta) jauh lebih kecil daripada Batas Deteksi Minimum (Minimum Detectable Effect / MDE). Sebagai contoh, pada model utama Jagung (H_CORN_01), estimasi koefisien presipitasi vegetatif adalah beta = +0.0368 (p_raw = 0.4745, p_Holm = 1.0000), sedangkan MDE panel jagung adalah +/-0.1444 log points. Artinya, variasi cuaca tahunan yang terekam terlalu lemah untuk dibedakan dari noise residual produksi dinas.",
        bold_prefix="Hasil Pengujian: "
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig11_mde_per_panel_final_formula_sigma.png"),
        "FIGUR 2: Analisis Minimum Detectable Effect (MDE) — Perbandingan Daya Deteksi Statistik Panel Jagung, Kedelai, dan Padi terhadap Variasi Cuaca Antar-Tahun."
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig16_phase7_full_hypotheses_forest_plot_mde.png"),
        "FIGUR 3: Forest Plot Pengujian 11 Hipotesis Fenologi Cuaca — Estimasi Titik Beta, 95% Webb Bootstrap CI, dan Garis Batas MDE (Membuktikan 100% Hipotesis Berada di Bawah Batas Deteksi)."
    )

    # Phase 8 & 9
    add_heading_2(doc, "Phase 8 & Phase 9: Keruntuhan Generalisasi Machine Learning (Mengapa ML Gagal)")
    add_p(doc,
        "Di Phase 8, kami mengekstraksi 65.754 baris data cuaca harian AgERA5 menjadi fitur agroklimat canggih (lag, rolling sum 14 hari, CDD, CWD, DTR, VPD, dan neraca air biofisik P - ET0). Kami menemukan fenomena multikolinearitas ekstrem: korelasi antara presipitasi musiman dan defisit air mencapai r = +0.996 dengan Variance Inflation Factor (VIF) sebesar 4.312,9! Ini membuktikan bahwa memasukkan banyak variabel cuaca sekaligus ke dalam regresi linier akan merusak kestabilan estimasi.",
        bold_prefix="Feature Store & Multikolinearitas: "
    )
    add_p(doc,
        "Di Phase 9, kami melatih 6 model prediktif pada panel jagung 18 sentra (2015–2021, N=124): Pooled OLS, WLS Area, Ridge, Lasso, Elastic Net, dan Random Forest Regressor. Kami mengevaluasi model menggunakan protokol validasi silang paling ketat untuk data panel waktu: Leave-One-Year-Out (LOYO) Cross-Validation.",
        bold_prefix="Benchmarking 6 Model ML: "
    )

    ml_rows = [
        ["Pooled OLS (TWFE)", "0.158", "-0.113", "0.614", "R2 LOYO negatif; estimasi year FE hilang pada tahun ditahan."],
        ["WLS (Bobot Luas Lahan)", "0.158", "-0.113", "0.614", "Identik OLS; penimbangan luas tidak memperbaiki generalisasi."],
        ["Ridge Regressor (L2)", "0.150", "-0.041", "0.594", "Penalti L2 meredam koefisien namun R2 out-of-sample tetap negatif."],
        ["Lasso Regressor (L1)", "0.091", "-0.024", "0.589", "Menyeleksi fitur menjadi nol; performa mendekati baseline mean."],
        ["Elastic Net (L1+L2)", "0.126", "-0.032", "0.591", "Kombinasi regulerisasi gagal memprediksi anomali tahunan."],
        ["Random Forest Regressor", "0.389", "+0.034", "0.572", "Overfit di data latih (R2=0.389) runtuh total saat LOYO CV (R2=+0.034)."]
    ]
    add_table_data(doc, ["Model Algoritma", "R² Data Latih", "R² LOYO CV", "RMSE Out-Sample", "Diagnostik & Temuan Ilmiah"], ml_rows, [1.5, 1.0, 1.0, 1.0, 2.0])

    add_callout(doc,
        "Perhatikan tabel di atas: Random Forest tampak hebat di data latih dengan R² = 0.389 (mampu menjelaskan 39% variasi data). Namun begitu diuji pada tahun yang belum pernah dilihat (LOYO CV), performanya RUNTUH MENJADI HAMPIR NOL (R² = +0.034)! Seluruh model linier bahkan menghasilkan R² negatif. Ini bukan karena algoritmanya jelek, melainkan karena data produktivitas tahunan dinas didominasi oleh faktor non-cuaca (teknologi benih, pupuk subsidi, hama tikus, ekspansi lahan). Oleh karena itu, KAMI MEMUTUSKAN SECARA MUTLAK: TaniAdapt dilarang menggunakan Machine Learning untuk menebak hasil panen!",
        title="MENGAPA MACHINE LEARNING GAGAL & DITINGGALKAN?"
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig19_phase9_ml_baseline_performance_comparison.png"),
        "FIGUR 4: Perbandingan Performa 6 Model Machine Learning — Keruntuhan R² Generalisasi Out-of-Sample (LOYO CV) Dibandingkan Data Latih In-Sample."
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig20_phase9_loyo_actual_vs_predicted_falsification.png"),
        "FIGUR 5: Scatter Plot Aktual vs Prediksi LOYO CV & Uji Falsifikasi Lead Placebo (Membuktikan Tidak Adanya Daya Prediksi Cuaca terhadap Produktivitas Tahunan Dinas)."
    )

    # Phase 10 & 11
    add_heading_2(doc, "Phase 10 & Phase 11: Peralihan ke Biofisik FAO-56 & Desain Decision Engine")
    add_p(doc,
        "Karena model statistik dan ML tidak mampu mengekstrak sinyal cuaca kausal, riset beralih ke fondasi biofisik mekanistik standar dunia: FAO Irrigation and Drainage Paper 56 (Allen et al. 1998). Kami mengimplementasikan perhitungan Evapotranspirasi Acuan Penman-Monteith (ET0) dan neraca deplesi air harian zona perakaran (Dr).",
        bold_prefix="Peralihan ke Mekanistik FAO-56: "
    )
    add_p(doc,
        "Alih-alih menggunakan ambang batas ad-hoc (seperti CWB -25 mm atau kadar lengas 0.70 m³/m³ yang secara fisis salah karena melebihi porositas tanah), kami menerapkan kriteria ilmiah resmi FAO-56 Bab 8: Tanaman hanya mengalami stres kekurangan air jika deplesi air tanah melampaui Readily Available Water: Dr > RAW = p * TAW. Di mana TAW dihitung dari kapasitas lapang dan titik layu permanen tekstur tanah (Tabel 19), kedalaman perakaran Zr, dan fraksi deplesi p (Tabel 22).",
        bold_prefix="Kriteria Deplesi Lengas Tanah: "
    )
    add_p(doc,
        "Di Phase 11, kami menyusun Decision Engine yang mengevaluasi 5 tindakan operasional nyata petani: Siram (Irigasi), Semprot (Pestisida), Pupuk, Panen, dan Olah Tanah pada 13 jam operasional lapangan (06.00–18.00 WIB). Mesin ini memetakan kondisi cuaca jam-jaman menjadi 3 status tegas: SAFE (Sangat Aman / Hijau), WARN (Perlu Waspada / Kuning), dan DANGER (Hindari / Merah). Celah kecepatan angin ditutup secara presisi: <3 km/j (WARN, bahaya inversi suhu udara), 3–12 km/j (SAFE, rentang semprot ideal), 12–15 km/j (WARN, transisi drift nosel kasar), dan >15 km/j (DANGER, bahaya drift tinggi).",
        bold_prefix="Matriks Jadwal Jam-Jaman: "
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig21_phase10_abiotic_water_risk_calibration.png"),
        "FIGUR 6: Model Risiko Biofisik Mekanistik FAO-56 — Kurva Koefisien Tanaman (Kc) Sepanjang Fase Fenologi dan Kalibrasi Neraca Air Evapotranspirasi."
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig23_phase11_hourly_advisory_schedule_matrix.png"),
        "FIGUR 7: Matriks Rekomendasi Jam Operasional Harian (06.00–18.00 WIB) — Evaluasi 5 Tindakan Nyata Petani Berdasarkan Kecepatan Angin, Hujan, dan Radiasi Surya."
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig24_phase11_decision_trace_flowchart.png"),
        "FIGUR 8: Diagram Alir Pohon Keputusan (Decision Trace Flowchart) — Struktur Penelusuran Rekam Jejak Logika Deterministik Tanpa Halusinasi."
    )

    # Phase 12
    add_heading_2(doc, "Phase 12: Validasi Hindcast Bencana BMKG & Stress-Testing Kasus Batas")
    add_p(doc,
        "Untuk menguji apakah Decision Engine bekerja secara masuk akal sebelum dipakai petani, kami melakukan dua pengujian validasi independen di Phase 12:",
        bold_prefix="Dua Uji Validasi: "
    )
    add_p(doc,
        "1. Uji Validasi Hindcast Sejarah (Preliminary Face-Validity Check): Kami menguji mesin terhadap 3 peristiwa iklim ekstrem regional BMKG: La Niña Basah 2016 (terdeteksi 18/18 sentra = 100%), Kemarau Positif IOD 2019 (terdeteksi 18/18 sentra = 100%), dan Super El Niño 2023 (terdeteksi 16/18 sentra = 88.9%). Dua sentra yang tidak memicu alarm 2023 adalah Kab. Indramayu dan Kab. Tasikmalaya karena rata-rata presipitasi 14-harinya tidak menembus batas konjungsi P25 (objektif reported). Pada tahun kontrol normal (2017 dan 2021), alarm kemarau palsu adalah 0/18 (Spesifisitas Kering = 100.0%).\n"
        "2. Uji Ketahanan Kasus Batas (Stress-Testing): Kami menguji 5 skenario ekstrem (sensor suhu rusak 45°C, data masukan NULL/hilang, badai angin 35 km/j, musim pancaroba ekstrem, anomali hujan lebat). Hasilnya: 100% kasus batas berhasil ditangani secara anggun (graceful degradation pass rate 100%) dengan status jujur 'evidence_insufficient', tanpa ada sistem yang crash."
    )

    add_image_box(doc,
        Path("reports/figures/10_cross_dataset_synthesis/fig25_phase12_hindcast_extreme_events_validation.png"),
        "FIGUR 9: Validasi Hindcast Non-Yield Terhadap 3 Peristiwa Bencana Iklim Historis BMKG dan Tahun Kontrol pada 18 Sentra Pertanian Jawa Barat."
    )

    # =========================================================================
    # BAGIAN 3: BAGAIMANA MODEL DECISION ENGINE BEKERJA SEKARANG?
    # =========================================================================
    add_heading_1(doc, "3. BAGAIMANA MODEL DECISION ENGINE BEKERJA SEKARANG?")
    add_p(doc,
        "Model pengambil keputusan TaniAdapt saat ini telah distandardisasi menjadi mesin deterministik murni yang dikendalikan oleh satu berkas konfigurasi resmi: rules/rules.json (versi v2.3-phase13-gate). Tidak ada lagi hardcode angka sembarangan di dalam kode frontend maupun backend.",
        bold_prefix="Single Source of Truth: "
    )

    add_p(doc,
        "Setiap aturan di dalam rules.json memiliki klasifikasi integritas bukti yang tegas:\n"
        "1. VERIFIED_METHOD: Aturan yang didukung penuh oleh metode ilmiah baku berstandar internasional dengan rumus dan tabel tercetak. Saat ini, satu-satunya aturan irigasi aktif berstatus ini adalah deplesi air FAO-56 (RULE_WATER_FAO56_DEPLETION).\n"
        "2. CONVENTION_PENDING: Aturan praktis agrometeorologi lapangan yang ditetapkan oleh tim ahli agronomi namun belum dikalibrasi terhadap data sensor in-situ lokal (misal: batas angin semprot 12 km/j, hujan lebat 3 hari > 100 mm, radiasi surya > 500 W/m²).\n"
        "3. INSUFFICIENT: Aturan yang tidak memiliki sumber referensi ilmiah valid sehingga dinonaktifkan (misal: aturan saturasi tanah 0.70 m³/m³).\n"
        "4. DEPRECATED: Aturan lama yang resmi dipensiunkan agar tidak terjadi konflik ganda (misal: aturan defisit air empiris CWB -25 mm dan -50 mm).",
        bold_prefix="Tiga Kelas Status Aturan: "
    )

    add_heading_2(doc, "Langkah Demi Langkah Perhitungan Deplesi Air Tanah FAO-56")
    add_p(doc,
        "Agar lu paham persis bagaimana sistem menghitung apakah tanaman butuh disiram atau tidak, berikut rumus fisika yang dijalankan Decision Engine:\n"
        "1. Menghitung Total Available Water (TAW, mm):\n"
        "   TAW = 1000 * (theta_FC - theta_WP) * Zr\n"
        "   Di mana theta_FC adalah kapasitas lapang tanah (m³/m³), theta_WP adalah titik layu permanen tanah (m³/m³), dan Zr adalah kedalaman perakaran aktif (m). Pada tanah lempung (loam) standar FAO-56 Tabel 19, theta_FC = 0.27 dan theta_WP = 0.12, sehingga kapasitas simpan air tanah adalah 150 mm per meter kedalaman tanah.\n"
        "2. Menghitung Readily Available Water (RAW, mm):\n"
        "   RAW = p * TAW\n"
        "   Di mana p adalah fraksi deplesi air yang dapat diserap tanaman tanpa mengalami stres (FAO-56 Tabel 22). Untuk jagung p = 0.55, kedelai p = 0.50, dan tomat p = 0.40.\n"
        "3. Menghitung Neraca Deplesi Lengas Harian (Dr, mm):\n"
        "   Dr(t) = Dr(t-1) - P_eff(t) + ETc(t)\n"
        "   Di mana P_eff adalah hujan efektif dan ETc = Kc * ET0 adalah kebutuhan air tanaman riil.\n"
        "4. Pengambilan Keputusan Irigasi:\n"
        "   - Jika Dr > RAW: Status TANAMAN STRES KEKURANGAN AIR (kondisi_stres_abiotik), tindakan 'Siram' berlabel SAFE (Sangat Dianjurkan Segera Disiram).\n"
        "   - Jika Dr <= RAW: Status AIR TANAH MENCUKUPI (normal), tindakan 'Siram' berlabel WARN (Belum Perlu Disiram, Hemat Air)."
    )

    add_callout(doc,
        "Dalam skema kontrak JSON (schemas/engine_output.schema.json Draft 2020-12), kami memasang validasi IF/THEN otomatis: Engine DITOLAK KERAS mengeluarkan status 'kondisi_stres_abiotik' atau 'kondisi_mendukung_OPT' jika tidak menyertakan evidence_refs yang berstatus VERIFIED_METHOD. Seluruh 7 unit test pengujian skema telah LULUS 100% via Pytest.",
        title="PENEGAKAN VALIDASI SKEMA KONTRAK"
    )

    # =========================================================================
    # BAGIAN 4: BAGAIMANA NASIB KELIMA TANAMAN KITA?
    # =========================================================================
    add_heading_1(doc, "4. BAGAIMANA NASIB KELIMA TANAMAN KITA? (STATUS KOMODITAS)")
    add_p(doc, "Berikut peta jalan status dan perlakuan ilmiah terhadap masing-masing komoditas:")

    crop_rows = [
        ["Padi Sawah (Oryza sativa)", "Jalur Penasihat Mekanistik Parsial", "N=54 mentah / 53 robust (2015–2017). Baseline BPS terverifikasi manusia pada 2015 (61.22), 2018 (56.51), dan 2019 (57.54). Patahan KSA 2017→2018 dicatat transparan.", "MODUL AIR: Dinyatakan 'evidence_insufficient' (ponded wetland regime) karena rumus deplesi tanah tidak berlaku pada sawah tergenang. MODUL LAIN: Rekomendasi semprot, pupuk, dan panen AKTIF."],
        ["Jagung Pipil (Zea mays)", "Sensitivitas Empiris + Mekanistik Penuh", "N=121 observasi valid (2015–2021, 18 sentra). Imputasi dinas 2022 dibuang. Uji ekonometrika membuktikan efek cuaca < MDE (evidence_insufficient).", "MODUL AIR: AKTIF PENUH berbasis FAO-56 (Kc: 0.30 -> 1.20 -> 0.35 kering di batang; p=0.55; Zr=1.0 m). MODUL TINDAKAN: Aktif 100%."],
        ["Kedelai (Glycine max)", "Sensitivitas Empiris + Mekanistik Penuh", "N=112 observasi valid pasca filter outlier MAD-z pada 17 sentra aktif ex-ante (17 sel AgERA5 unik, 2015–2021).", "MODUL AIR: AKTIF PENUH berbasis FAO-56 (Kc: 0.40 -> 1.15 -> 0.50; p=0.50; Zr=1.0 m). MODUL TINDAKAN: Aktif 100%."],
        ["Cabai Merah & Rawit (Capsicum spp.)", "Tier B Literature Transfer", "N=8 observasi target provinsi (2017–2024). Ketiadaan data ground truth serangan OPT historis di Jabar.", "MODUL OPT: DITAHAN PADA 'evidence_insufficient' karena formula Sentelhas 2008 membutuhkan data per jam, bukan harian. MODUL AIR: evidence_insufficient sampai Kc lokal diverifikasi."],
        ["Tomat (Solanum lycopersicum)", "Tier B Transfer + Mekanistik Air", "N=8 observasi target provinsi (2017–2024). Koefisien tanaman terverifikasi FAO-56 Tabel 12.", "MODUL AIR: AKTIF PENUH (Kc: 0.60 -> 1.15 -> 0.80 segar konsumsi; p=0.40; Zr=0.7 m). MODUL OPT: evidence_insufficient menunggu data jam-jaman."],
        ["Bawang Merah (Allium cepa)", "BLOCKED (Dibekukan)", "Data dinas tidak representatif dan sentra terfragmentasi.", "STATUS DIBLOKIR TOTAL sampai tersedia dataset agroklimat baru."]
    ]
    add_table_data(doc, ["Komoditas", "Status Pendekatan", "Status Bukti & Ukuran Sampel", "Implementasi Nyata di Sistem"], crop_rows, [1.3, 1.3, 2.0, 1.9])

    # =========================================================================
    # BAGIAN 5: BAGAIMANA KONSEP DIPAKAI DI WEB NEXT.JS? (PHASE 13)
    # =========================================================================
    add_heading_1(doc, "5. BAGAIMANA KONSEP DIPAKAI DI WEB NEXT.JS? (CETAK BIRU PHASE 13)")
    add_p(doc,
        "Di Phase 13, seluruh hasil riset di atas akan diintegrasikan ke dalam antarmuka web modern Next.js di repositori taniadapt-web (/mnt/c/CODING/TaniAdapt/taniadapt-web). Berikut arsitektur implementasinya:",
        bold_prefix="Integrasi Frontend: "
    )

    add_heading_2(doc, "A. Dua Lapis Antarmuka Pengguna (Two-Layer UI)")
    add_p(doc,
        "Antarmuka web TaniAdapt sengaja dipisahkan menjadi dua lapisan visual agar petani dan penyuluh tidak bingung:\n"
        "1. Lapis 1: Fakta Cuaca Terkini (Weather Facts Layer)\n"
        "   Menampilkan kondisi fisik atmosfer riil dari API cuaca Open-Meteo: Suhu udara (°C), Kecepatan & arah angin (km/j), Curah hujan harian & per jam (mm), Kelembapan relatif RH (%), Radiasi surya (W/m²), serta Peringkat Persentil Relatif (misal: 'Hujan 14-hari berada di Persentil 85 — Tergolong Sangat Basah') yang dihitung terhadap baseline klimatologi 21 tahun Open-Meteo ERA5 (2000–2020).\n"
        "2. Lapis 2: Rekomendasi Tindakan Operasional (Advisory Actions Layer)\n"
        "   Menampilkan kartu rekomendasi 5 tindakan nyata lapangan (Siram, Pupuk, Semprot, Panen, Rawat) yang dilengkapi dengan Badge Status Bukti Transparan:\n"
        "   - Badge Hijau / Biru: 'Terverifikasi Ilmiah (FAO-56)' untuk aturan deplesi air.\n"
        "   - Badge Kuning / Netral: 'Aturan Praktis Lapangan — Belum Dikalibrasi Sensor' untuk aturan konvensi angin, radiasi, dan hujan.\n"
        "   - Badge Abu-abu: 'Bukti Belum Cukup (evidence_insufficient)' disertai penjelasan jujur (misal: pada modul air padi atau modul jamur cabai)."
    )

    add_heading_2(doc, "B. Jadwal Jam Operasional (06.00–18.00 WIB) & Logika Worst-Of")
    add_p(doc,
        "Pada jadwal jam operasional harian di web, sistem mengevaluasi prakiraan cuaca per jam (live hourly forecast). Jika dalam satu jam tertentu terdapat beberapa aturan yang aktif bersamaan, Decision Engine menerapkan prinsip penggabungan teraman yaitu Worst-Of Aggregation:\n"
        "- Jika salah satu aturan menghasilkan DANGER (Merah), maka status jam tersebut otomatis DANGER (Hindari).\n"
        "- Jika tidak ada DANGER tetapi ada WARN (Kuning), maka status jam tersebut menjadi WARN (Waspada).\n"
        "- Jam tersebut hanya berstatus SAFE (Hijau) jika SELURUH aturan agrometeorologi menyatakan aman.\n"
        "Field 'reason' di UI akan mencantumkan seluruh aturan yang terpicu beserta status buktinya."
    )

    add_heading_2(doc, "C. Baseline Klimatologi 21 Tahun Open-Meteo ERA5 (2000–2020)")
    add_p(doc,
        "Untuk menghitung peringkat persentil di web secara konsisten di seluruh 27 Kabupaten/Kota Jawa Barat, kami telah mengekspor baseline klimatologi 21 tahun penuh (2000–2020, N=7.671 hari per kabupaten) ke data/export/openmeteo_era5_2000_2020_*.json. Web app akan membaca file ini sehingga peringkat persentil dijamin seragam, adil, dan bebas dari distorsi data campuran."
    )

    add_heading_2(doc, "D. Peran Asisten Percakapan LLM (Voice & Text Assistant)")
    add_p(doc,
        "Asisten AI di dalam aplikasi web (fitur tanya-jawab petani): \n"
        "1. DILARANG menghitung formula sendiri di dalam prompt.\n"
        "2. HANYA membaca payload JSON yang dikeluarkan oleh Decision Engine TypeScript.\n"
        "3. Berfungsi menjelaskan arti kartu tindakan ke bahasa Sunda atau bahasa Indonesia yang santun dan akrab bagi petani.\n"
        "4. Jika status bernilai 'evidence_insufficient', asisten suara akan jujur berkata: 'Mohon maaf Kang/Pak, data kelembapan mikro di lahan kita belum cukup untuk mendeteksi jamur secara pasti. Sangat disarankan untuk berkonsultasi langsung dengan Petugas Penyuluh Lapangan (PPL) setempat.'"
    )

    # Summary Callout
    add_callout(doc,
        "Dengan selesainya Phase 0 hingga Phase 12 dan penutupan seluruh audit integritas ilmiah (git tag: phase13-gate-ready), repositori research_taniAdapt telah berhasil bertransformasi dari sekadar eksperimen data menjadi CETAK BIRU KEPUTUSAN AGRO-BIOFISIK YANG SOLID, JUJUR, DAN ANTI-HALUSINASI. Kita sekarang 100% siap membuka Phase 13 untuk membangun aplikasi web Next.js!",
        title="KESIMPULAN AKHIR & KESIAPAN PHASE 13"
    )

    doc.save(OUT_DOCX)
    print(f"Successfully generated Master Dossier for Fathir at {OUT_DOCX}")


if __name__ == "__main__":
    build_dossier()
