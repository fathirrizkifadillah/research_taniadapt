"""Build Master Comprehensive Guidebook for Fathir & Web Development Team (.docx).
Location: context/to_fathir/TaniAdapt_Buku_Panduan_Master_Riset_Rumus_dan_Implementasi_Web.docx

Rules strictly enforced:
- NO raw LaTeX syntax (no \\theta, \\Delta, \\gamma, \\frac, etc.). Clean Unicode typography throughout!
- Complete walkthrough of Research (Phase 0-12, 16 Papers, Notebooks 01-10).
- Complete explanation of Decision Engine models, rules, and worst-of logic.
- Input mapping: manual user input vs live weather API vs static knowledge base.
- Complete breakdown of all 5 crops (Padi, Jagung, Kedelai, Cabai Merah & Rawit, Tomat).
- Concrete web implementation guide for frontend and backend developers.
"""
from __future__ import annotations

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DOCX = PROJECT_ROOT / "context" / "to_fathir" / "TaniAdapt_Buku_Panduan_Master_Riset_Rumus_dan_Implementasi_Web.docx"
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
            if any(k in val_str for k in ["VERIFIED", "Sangat Dianjurkan", "Sangat Aman", "SAFE", "PASS", "100%", "Aktif", "Lulus"]):
                color_override = "1B6E34"
            elif any(k in val_str for k in ["CONVENTION", "Perlu Waspada", "WARN", "Waspada", "UNCALIBRATED", "Belum Perlu", "Tahan"]):
                color_override = "B45309"
            elif any(k in val_str for k in ["INSUFFICIENT", "Hindari", "DANGER", "DEPRECATED", "Ditolak", "Gagal", "Cekaman"]):
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


def add_clean_formula_box(doc, formula_lines: list[str], label: str = ""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "F8FAFC")
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    left_b = OxmlElement("w:left")
    left_b.set(qn("w:val"), "single")
    left_b.set(qn("w:sz"), "20")
    left_b.set(qn("w:space"), "0")
    left_b.set(qn("w:color"), STEEL)
    borders.append(left_b)
    for s in ("top", "bottom", "right"):
        none_b = OxmlElement(f"w:{s}")
        none_b.set(qn("w:val"), "none")
        borders.append(none_b)
    tcPr.append(borders)
    cell.width = Inches(6.5)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if label:
        r_lab = p.add_run(f"[{label}]\n")
        r_lab.bold = True
        r_lab.font.name = "Aptos"
        r_lab.font.size = Pt(8.5)
        r_lab.font.color.rgb = RGBColor(44, 82, 130)
    
    for idx, line in enumerate(formula_lines):
        r_line = p.add_run(line + ("\n" if idx < len(formula_lines) - 1 else ""))
        r_line.font.name = "Consolas"
        r_line.font.size = Pt(9.0)
        r_line.bold = (idx == 0 and not label) or ("=" in line and len(line) < 60)
        r_line.font.color.rgb = RGBColor(20, 20, 20)
    doc.add_paragraph()


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


def build_master_guide():
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
    r_title = p_title.add_run("TANIADAPT: BUKU PANDUAN MASTER RISET, FORMULA, DAN IMPLEMENTASI WEB")
    r_title.bold = True
    r_title.font.name = "Aptos Display"
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = RGBColor(27, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("Dokumen Lengkap untuk Fathir & Rekan Tim Pengembang: Pemetaan Riset Phase 0–12, Formula Fisika Bersih (Bebas LaTeX),\nMatriks Decision Engine, Input Pengguna vs API Cuaca, dan Cetak Biru Next.js")
    r_sub.font.name = "Aptos"
    r_sub.font.size = Pt(10.5)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(44, 82, 130)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Penulis & Lead Researcher: Fathir Rizki Fadillah | Tim: TaniAdapt Engineering | Versi Engine: v2.4-verified-params | Kontrak: Draft 2020-12")
    r_meta.font.name = "Aptos"
    r_meta.font.size = Pt(9.0)
    r_meta.bold = True
    r_meta.font.color.rgb = RGBColor(100, 100, 100)

    # =========================================================================
    # BAB 1: DUDUK PERKARA & ARSITEKTUR BESAR
    # =========================================================================
    add_heading_1(doc, "BAB 1: DUDUK PERKARA & ARSITEKTUR BESAR SISTEM")
    
    add_p(doc,
        "TaniAdapt adalah platform Agricultural Decision Support System (DSS) dan presisi agroadvisory hiperlokal yang dibangun khusus untuk petani kecil (smallholders) dan pengelola kebun di Jawa Barat. Aplikasi ini menjawab masalah nyata di lapangan yang selama ini gagal diselesaikan oleh aplikasi cuaca konvensional:",
        bold_prefix="Definisi Sistem & Masalah Lapangan: "
    )
    add_p(doc,
        "1. Masalah Ketiadaan Panduan Jam Kerja (Diurnal Mismatch): Ramalan cuaca di smartphone umumnya hanya menyajikan informasi makro harian seperti 'Hari ini hujan ringan'. Petani di sawah tidak bisa mengambil keputusan dari informasi pasif tersebut. Petani butuh jawaban konkrit: 'Jam 07.00 pagi ini anginnya aman nggak untuk nyemprot pestisida?', 'Jam 11.00 siang terik matahari bahaya nggak untuk menyebar pupuk?', atau 'Apakah air di dalam tanah sudah habis sehingga wajib menyalakan pompa solar hari ini?'\n"
        "2. Masalah Halusinasi AI Generatif: Banyak aplikasi pertanian baru tergoda menghubungkan LLM (seperti ChatGPT) langsung ke petani untuk diagnosis penyakit dan dosis racun. Di sektor pangan, ini tindakan berbahaya. AI generatif rawan berhalusinasi mengarang takaran kimia sintetis yang bisa membakar tanaman atau meracuni lingkungan.\n"
        "3. Masalah Ilusi Machine Learning: Menghubungkan data cuaca untuk menebak tonase hasil panen (yield prediction) terbukti secara ilmiah mengalami keruntuhan generalisasi out-of-sample karena data produktivitas dinas tahunan didominasi faktor non-cuaca (benih, pupuk subsidi, tikus)."
    )

    add_callout(doc,
        "Solusi Arsitektur Decoupled TaniAdapt:\n"
        "• Otak Keputusan (Decision Engine): 100% deterministik, berbasis rumus fisika baku FAO-56 Penman-Monteith, neraca air deplesi tanah zona perakaran (Dr > RAW), dan aturan agrometeorologi terstruktur (rules.json v2.4). Mesin ini menghasilkan payload JSON murni yang divalidasi skema ketat.\n"
        "• Lapisan Komunikasi (LLM / Conversational Layer): Murni sebagai narator penerjemah JSON ke bahasa santun (Indonesia / Sunda) dan edukasi sains berbasis RAG 16 Paper Ilmiah. LLM dilarang keras mengubah angka atau mendiagnosis obat.",
        title="ARSIKTEKTUR TERPISAH (DECOUPLED)"
    )

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig24_phase11_decision_trace_flowchart.png",
        "FIGUR 1: Diagram Alir Pohon Rekam Jejak Keputusan (Decision Trace Flowchart) — Struktur Penelusuran Logika Deterministik Tanpa Halusinasi."
    )

    # =========================================================================
    # BAB 2: REKAP LENGKAP TEMUAN RISET PHASE 0–12 & 16 PAPER
    # =========================================================================
    add_heading_1(doc, "BAB 2: REKAP LENGKAP TEMUAN RISET PHASE 0–12 & 16 PAPER ILMIAH")
    
    add_p(doc,
        "Decision Engine TaniAdapt bukan hasil imajinasi koding semalam, melainkan produk turunan langsung dari 13 fase riset disiplin dan sintesis 16 paper ilmiah bereputasi internasional:",
        bold_prefix="Perjalanan Riset Berkelanjutan: "
    )

    phase_summary_rows = [
        ["Phase 0 & 1", "Definisi Masalah & Hipotesis", "Merumuskan 3 RQ dan 11 hipotesis fenologi musiman. Dicatat transparan sebagai hipotesis eksploratori terdaftar post-data-access."],
        ["Phase 2", "Deep Literature Review", "Membedah 16 paper ilmiah & 15 kompetitor DSS global. Paper 9 & 5 mendasari arsitektur rantai keputusan kartu aksi; Paper FAO-56 mendasari fisika air; Paper Sentelhas 2008 mendasari durasi basah daun LWD; Paper 6 mendasari mitigasi genangan 3-hari."],
        ["Phase 3 & 4", "Dataset & Audit Kualitas Data", "Mengumpulkan 8 dataset aktif. Memetakan 27 kab/kota ke 22 sel AgERA5 unik dengan elevasi SRTM DEM (jarak offset rata-rata 5.80 km). Membongkar 11 blocker audit: skandal imputasi kembar dinas 75.70 ku/ha di 2022, patahan metode KSA BPS 2018 pada padi, dan ketiadaan label OPT lokal."],
        ["Phase 5", "Penguncian 5 Komoditas", "Mengunci portofolio 5 komoditas: Padi Sawah, Jagung Pipil, Kedelai, Cabai Merah & Rawit, dan Tomat. Memblokir total Bawang Merah karena data dinas tidak representatif."],
        ["Phase 6 & 7", "Analisis Ekonometrika Panel", "Menguji 11 hipotesis via Two-Way Fixed Effects + Wild Cluster Bootstrap Webb 6-titik. Menemukan 100% hipotesis berstatus evidence_insufficient karena efek cuaca berada di bawah batas deteksi statistik (MDE ±0.1444)."],
        ["Phase 8 & 9", "Feature Store & Uji Machine Learning", "Mengekstrak 65.754 baris cuaca AgERA5. Menemukan multikolinearitas ekstrem r = +0.996 (VIF = 4.312,9). Melatih 6 model ML pada panel jagung 18 sentra; membuktikan Random Forest runtuh dari Train R² = 0.389 menjadi Out-of-Sample LOYO CV R² = +0.034 (0%). Keputusan resmi: ML dilarang dipakai menebak hasil panen."],
        ["Phase 10 & 11", "Mekanistik FAO-56 & Decision Engine", "Beralih total ke fisika air FAO-56 Bab 8: TAW, RAW = p * TAW, dan deplesi Dr. Menyusun jadwal jam 06.00–18.00 WIB untuk 5 tindakan operasional lapangan."],
        ["Phase 12", "Validasi Hindcast BMKG & Kasus Batas", "Uji sejarah terhadap 3 bencana iklim BMKG: La Niña 2016 (100% terdeteksi), Kemarau 2019 (100% terdeteksi), Super El Niño 2023 (88.9% terdeteksi). Tahun kontrol normal menghasilkan 0% false alarm kemarau (spesifisitas kering 100%). Uji 5 skenario ekstrem menghasilkan 100% graceful degradation pass rate."]
    ]
    add_table_data(doc, ["Tahapan Riset", "Fokus Utama", "Temuan Empiris & Dampak ke Sistem"], phase_summary_rows, [1.3, 1.8, 3.4])

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig19_phase9_ml_baseline_performance_comparison.png",
        "FIGUR 2: Keruntuhan Performa 6 Model Machine Learning pada Validasi Out-of-Sample LOYO CV (Phase 9) — Justifikasi Ilmiah Peralihan ke Biofisik FAO-56."
    )

    # =========================================================================
    # BAB 3: PEMETAAN LENGKAP INPUT KE DECISION ENGINE
    # =========================================================================
    add_heading_1(doc, "BAB 3: PEMETAAN LENGKAP INPUT KE DECISION ENGINE")
    
    add_p(doc,
        "Agar seluruh tim pengembang paham dari mana setiap data berasal, berikut adalah rincian 3 kelompok input yang masuk ke Decision Engine:",
        bold_prefix="Tiga Kategori Input Sistem: "
    )

    input_mapping_rows = [
        ["1. Komoditas Tanaman (crop)", "Input Manual Petani (UI)", "Dropdown pilihan: padi, jagung, kedelai, cabai, tomat.", "Menentukan koefisien Kc, fraksi deplesi p, kedalaman akar Zr, dan aturan tindakan khusus."],
        ["2. Tanggal Tanam (planting_date)", "Input Manual Petani (UI)", "Format tanggal kalender YYYY-MM-DD.", "Menghitung Hari Setelah Tanam (HST / DAP) = Tanggal Hari Ini - Tanggal Tanam untuk menentukan fase fenologi."],
        ["3. Lokasi / GPS (latitude, longitude, kabkota)", "Input Manual / Sensor GPS HP", "Koordinat lintang bujur desimal dan nama kabupaten.", "Menentukan elevasi DEM SRTM, sel grid cuaca terdekat, dan baseline klimatologi 21 tahun."],
        ["4. Tekstur Tanah (soil_texture)", "Input Manual Petani (Opsional)", "Pilihan: loam (default), pasir, liat, lempung liat.", "Menentukan kapasitas simpan air tanah (TAW dasar: loam = 150 mm/m)."],
        ["5. Asumsi Deplesi Awal (Dr0)", "Input Eksplisit Sistem / Petani", "Nilai numerik deplesi awal (default = 0.0 mm).", "Kondisi air tanah saat hari pertama tanam (Dr0 = 0 mm diasumsikan kapasitas lapang)."],
        ["6. Suhu Udara (Tmax, Tmin, Tmean)", "Otomatis dari Open-Meteo API", "Nilai derajat Celsius (°C) harian dan per jam.", "Menghitung tekanan uap jenuh es, kemiringan Δ, batas aman semprot (< 30°C)."],
        ["7. Kecepatan Angin (wind_speed_10m)", "Otomatis dari Open-Meteo API", "Nilai km/jam per jam (dikonversi ke m/s ketinggian 2m).", "Evaluasi semprot kanopi: < 3 km/j inversi, 3–12 km/j aman, 12–15 km/j transisi, > 15 km/j drift bahaya."],
        ["8. Curah Hujan (precipitation)", "Otomatis dari Open-Meteo API", "Akumulasi hujan per jam, harian, dan 3-hari (mm).", "Penambah air tanah Peff pada deplesi Dr; circuit breaker pembatal siram/semprot (hujan >= 3 mm); pupuk (>= 8 mm)."],
        ["9. Peluang Hujan (precipitation_probability)", "Otomatis dari Open-Meteo API", "Persentase probabilitas hujan model cuaca (%).", "Mengisi field forecast_uncertainty di UI untuk transparansi ketidakpastian prakiraan."],
        ["10. Radiasi Surya & VPD (shortwave_radiation, vpd)", "Otomatis dari Open-Meteo API", "Radiasi (W/m²) dan VPD (hPa) per jam.", "Evaluasi terik siang: radiasi > 500 W/m² dan VPD > 15 hPa mempercepat penguapan siraman dan membakar stomata pupuk."],
        ["11. Titik Embun & Kelembapan (dewpoint_2m, RH)", "Otomatis dari Open-Meteo API", "Titik embun (°C) dan kelembapan relatif (%) per jam.", "Menghitung tekanan uap aktual ea; akumulasi jam RH >= 90% untuk deteksi durasi basah daun (LWD jamur patek cabai/tomat)."],
        ["12. Basis Aturan & Kontrak (rules.json, schema)", "Statis di Kode Program", "Berkas JSON aturan kanonik v2.4 dan Schema Draft 2020-12.", "Single Source of Truth logika keputusan agrometeorologi dan penjaminan struktur data bebas halusinasi."]
    ]
    add_table_data(doc, ["Nama Variabel Input", "Sumber Perolehan Data", "Format & Satuan", "Fungsi Nyata di Decision Engine"], input_mapping_rows, [1.5, 1.4, 1.5, 2.1])

    # =========================================================================
    # BAB 4: FORMULA MATEMATIKA & BIOFISIK MEKANISTIK BERSIH
    # =========================================================================
    add_heading_1(doc, "BAB 4: FORMULA MATEMATIKA & BIOFISIK MEKANISTIK BERSIH (BEBAS LATEX)")
    add_p(doc, "Seluruh persamaan di bawah ini ditulis dalam format tipografi bersih tanpa sintaks kode LaTeX yang berantakan, mengacu pada FAO Irrigation and Drainage Paper 56 (Allen et al., 1998; fao.org/4/x0490e):")

    add_heading_2(doc, "1. Evapotranspirasi Acuan Penman-Monteith Harian (ET0)")
    add_p(doc, "Menghitung laju penguapan air harian dari permukaan rumput standar acuan setinggi 0,12 meter:")
    add_clean_formula_box(doc, [
        "Persamaan Utama FAO-56 Penman-Monteith (Bab 4, Persamaan 6):",
        "",
        "ET0 = [ 0.408 * Δ * (Rn - G) + γ * (900 / (Tmean + 273)) * u2 * (es - ea) ]",
        "      ---------------------------------------------------------------------",
        "                           [ Δ + γ * (1 + 0.34 * u2) ]",
        "",
        "Keterangan Variabel Fisika:",
        "• ET0   = Evapotranspirasi acuan (mm/hari)",
        "• Rn    = Radiasi surya bersih pada permukaan tanaman (MJ/m²/hari)",
        "• G     = Fluks panas tanah harian (G = 0 untuk langkah harian, Eq. 42)",
        "• Tmean = Suhu udara rata-rata harian = (Tmax + Tmin) / 2 (°C)",
        "• u2    = Kecepatan angin pada ketinggian 2 meter di atas tanah (m/s)",
        "• es    = Tekanan uap jenuh rata-rata atmosfer (kPa)",
        "• ea    = Tekanan uap aktual atmosfer (kPa)",
        "• Δ     = Kemiringan kurva tekanan uap jenuh terhadap suhu (kPa/°C)",
        "• γ     = Konstanta psikrometrik atmosfer (kPa/°C)"
    ], label="FAO-56 Bab 4, Persamaan 6 (fao56.ts)")

    add_p(doc, "Persamaan Turunan Termodinamika Udara Pendukung:")
    add_clean_formula_box(doc, [
        "a. Tekanan Uap Jenuh (FAO-56 Persamaan 11 & 12):",
        "   e0(T) = 0.6108 * exp[ (17.27 * T) / (T + 237.3) ]",
        "   es    = [ e0(Tmax) + e0(Tmin) ] / 2",
        "   ea    = e0(Tdew)  [menggunakan titik embun rata-rata]",
        "",
        "b. Kemiringan Kurva Tekanan Uap (FAO-56 Persamaan 13):",
        "   Δ = ( 4098 * es ) / [ (Tmean + 237.3)² ]",
        "",
        "c. Tekanan Udara Barometrik & Psikrometrik (FAO-56 Persamaan 7 & 8):",
        "   P = 101.3 * [ (293 - 0.0065 * z) / 293 ]^5.26   (z = elevasi DEM SRTM, meter)",
        "   γ = 0.000665 * P",
        "",
        "d. Konversi Angin 10 Meter ke 2 Meter (FAO-56 Persamaan 47):",
        "   u2 = u10 * [ 4.87 / ln(67.8 * 10 - 5.42) ] ≈ u10 * 0.7479",
        "",
        "e. Radiasi Bersih Permukaan (FAO-56 Persamaan 38 & 39):",
        "   Rn  = Rns - Rnl = 0.77 * Rs - Rnl   (albedo rumput = 0.23)",
        "   Rnl = σ * [ (Tmax_K⁴ + Tmin_K⁴) / 2 ] * [ 0.34 - 0.14 * sqrt(ea) ] * [ 1.35 * (Rs / Rso) - 0.35 ]"
    ], label="Persamaan Termodinamika Atmosfer Pendukung")

    add_heading_2(doc, "2. Koefisien Tanaman Dinamis Kc(t)")
    add_p(doc, "Kebutuhan air tanaman riil (ETc) dihitung dari perkalian ETc = Kc * ET0. Nilai Kc bergerak dinamis mengikuti umur tanaman (Hari Setelah Tanam / HST) sepanjang 4 fase pertumbuhan:")
    add_clean_formula_box(doc, [
        "Interpolasi Dinamis Kurva Kc (FAO-56 Bab 6, Tabel 11 & 12):",
        "",
        "• Fase Awal (t <= L_ini)                 : Kc(t) = Kc_ini",
        "• Fase Perkembangan (L_ini < t <= L_dev) : Kc(t) = Kc_ini + [ (t - L_ini) / L_dev ] * (Kc_mid - Kc_ini)",
        "• Fase Pertengahan (L_dev < t <= L_mid)  : Kc(t) = Kc_mid",
        "• Fase Akhir (L_mid < t <= L_total)      : Kc(t) = Kc_mid + [ (t - L_mid) / L_late ] * (Kc_end - Kc_mid)",
        "• Pasca Panen (t > L_total)              : Kc(t) = Kc_end"
    ], label="Interpolasi Kurva Kc Dinamis (kc.ts)")

    add_heading_2(doc, "3. Kapasitas Air Tanah (TAW) & Air Siap Serap (RAW)")
    add_p(doc, "Menghitung batas kapasitas simpan air tanah perakaran tanpa menimbulkan cekaman pada tanaman:")
    add_clean_formula_box(doc, [
        "a. Total Available Water (TAW, mm) — FAO-56 Bab 8, Persamaan 82 (Eq. 82):",
        "   TAW = 1000 * (θ_FC - θ_WP) * Zr",
        "",
        "   Di mana:",
        "   • θ_FC = Kadar air tanah pada kapasitas lapang (m³/m³; loam = 0.27, rentang 0.20–0.30)",
        "   • θ_WP = Kadar air tanah pada titik layu permanen (m³/m³; loam = 0.12, rentang 0.07–0.17)",
        "   • Zr   = Kedalaman perakaran aktif tanaman (meter)",
        "   • Kapasitas simpan tanah loam standar = 1000 * (0.27 - 0.12) = 150.0 mm air per meter tanah",
        "",
        "b. Readily Available Water (RAW, mm) — FAO-56 Bab 8, Persamaan 83 (Eq. 83):",
        "   RAW = p * TAW",
        "",
        "   Di mana:",
        "   • p = Fraksi deplesi air yang dapat diserap tanaman tanpa mengalami stres:",
        "     - Jagung  : p = 0.55  (FAO-56 Bab 8, Tabel 22)",
        "     - Kedelai : p = 0.50  (FAO-56 Bab 8, Tabel 22)",
        "     - Tomat   : p = 0.40  (FAO-56 Bab 8, Tabel 22)",
        "     - Padi    : p = 0.20  (Tabel 22; modul deplesi tanah tidak berlaku karena sawah tergenang)"
    ], label="FAO-56 Bab 8 Eq. 82 & Eq. 83 (waterBalance.ts)")

    add_heading_2(doc, "4. Neraca Deplesi Air Tanah Harian Dr(t)")
    add_clean_formula_box(doc, [
        "Neraca Deplesi Air Harian (FAO-56 Bab 8, Persamaan 85):",
        "",
        "Dr(t) = Dr(t-1) - Peff(t) + ETc(t)",
        "",
        "Batasan Fisis: 0 <= Dr(t) <= TAW",
        "",
        "Kriteria Keputusan Status Tanaman vs Rekomendasi Tindakan Siram:",
        "• Jika Dr(t) > RAW : Status Tanaman = Cekaman Air (kondisi_stres_abiotik)",
        "                     Aksi Siram     = Sangat Dianjurkan Segera Menyiram (Lampu Hijau Tombol Siram)",
        "• Jika Dr(t) <= RAW: Status Tanaman = Normal (Air Tanah Masih Cukup)",
        "                     Aksi Siram     = Belum Perlu Menyiram / Tahan (Lampu Kuning, Hemat Air Pompa)",
        "• Jika Hujan >= 3mm: Aksi Siram     = Hindari Menyiram (Lampu Merah, Air Berlebih)"
    ], label="FAO-56 Bab 8 Eq. 85 & Aturan Siram TaniAdapt")

    add_heading_2(doc, "5. Uji Sensitivitas Variasi Tanah Loam (130 vs 180 mm/m)")
    add_clean_formula_box(doc, [
        "Evaluasi Sensitivitas Tanah di Engine:",
        "",
        "1. Hitung status deplesi pada batas bawah tekstur loam : TAW_rendah = 130 mm/m * Zr",
        "2. Hitung status deplesi pada batas atas tekstur loam   : TAW_tinggi = 180 mm/m * Zr",
        "3. Evaluasi kondisi stres pada kedua batas:",
        "   - Stres_Rendah = (Dr > p * TAW_rendah)",
        "   - Stres_Tinggi = (Dr > p * TAW_tinggi)",
        "4. Logika Flag Sensitivitas:",
        "   Jika (Stres_Rendah !== Stres_Tinggi) -> sensitif_terhadap_asumsi_tanah = TRUE",
        "   Jika (Stres_Rendah === Stres_Tinggi) -> sensitif_terhadap_asumsi_tanah = FALSE"
    ], label="Uji Sensitivitas Tanah Loam (waterBalance.ts)")

    # =========================================================================
    # BAB 5: CARA KERJA DECISION ENGINE & MATRIKS OPERASIONAL
    # =========================================================================
    add_heading_1(doc, "BAB 5: CARA KERJA DECISION ENGINE & MATRIKS OPERASIONAL")
    
    add_p(doc,
        "Untuk menghilangkan kerancuan penamaan, Decision Engine memisahkan secara tegas antara STATUS KONDISI TANAMAN dengan REKOMENDASI STATUS TINDAKAN PETANI.",
        bold_prefix="Pemisahan Tegas Kondisi vs Tindakan: "
    )

    action_matrix_clean_rows = [
        ["1. Siram (Irigasi)", "06.00 - 08.00 WIB", "Dr > RAW (tanah butuh air irigasi)", "Dr <= RAW (air tanah masih cukup)", "Hujan aktif >= 3 mm (air berlebih)", "FAO-56 Bab 8 (VERIFIED_METHOD). Jagung, kedelai, tomat aktif. Padi sawah mengembalikan evidence_insufficient."],
        ["2. Semprot (Pestisida)", "06.00 - 08.00 WIB", "Angin 3–12 km/j, Suhu < 30°C", "Angin < 3 km/j (inversi fajar) atau 12–15 km/j (transisi drift)", "Angin > 15 km/j atau Hujan >= 3 mm", "Menutup celah angin: < 3 km/j racun terperangkap dekat tanah; > 15 km/j spray drift melayang ke pemukiman."],
        ["3. Pupuk (Pemupukan)", "07.00 - 09.00 WIB", "Tanah lembap, hujan 12h < 8 mm", "VPD > 15 hPa atau terik siang", "Prakiraan hujan 12h >= 8 mm", "Mencegah pupuk hanyut tererosi limpasan air hujan atau membakar stomata daun saat cuaca terik."],
        ["4. Panen Pangan (Jagung/Kedelai)", "08.00 - 12.00 WIB", "RH <= 75%, hujan = 0 mm", "RH 75–85% (zona transisi jemur)", "RH > 85% atau Hujan > 5 mm", "Panen biji/polong kering. Menutup celah RH 75-85%: status WARN mengingatkan perlunya penjemuran segera."],
        ["5. Panen Hortikultura (Cabai/Tomat)", "07.00 - 10.00 WIB", "Tanpa hujan, suhu sejuk pagi", "Embun daun masih basah", "Hujan aktif atau buah basah kuyup", "Pemanenan buah segar bertahap. Dilarang petik saat basah kuyup karena memicu pembusukan di karung pengiriman."],
        ["6. Rawat / Pangkas (Tomat/Cabai)", "07.00 - 09.00 WIB", "Hujan 8h < 2 mm, cuaca cerah", "Kelembapan malam tinggi", "Prakiraan hujan 8h >= 2 mm", "Perempelan tunas air (wiwil) tomat & cabai. Mencegah luka pangkas basah terinfeksi spora jamur atau bakteri layu."],
        ["7. Pengamatan OPT (Cabai/Tomat)", "Pagi hari (06.00 WIB)", "RH malam normal < 90%", "Jumlah jam RH >= 90% >= 10 jam", "Kondisi basah terus-menerus", "Indikator Leaf Wetness Duration (LWD Sentelhas 2008, METHOD_UNCALIBRATED). Waspada patek/antraknosa."]
    ]
    add_table_data(doc, ["Tindakan Lapangan", "Window Ideal", "Kondisi Sangat Dianjurkan (SAFE)", "Kondisi Penyesuaian (WARN)", "Kondisi Larangan (DANGER)", "Dasar Biofisik & Spesifikasi Tanaman"], action_matrix_clean_rows, [1.4, 1.1, 1.2, 1.2, 1.1, 1.8])

    add_heading_2(doc, "Prinsip Penggabungan Teraman (Worst-Of Aggregation) per Jam")
    add_p(doc,
        "Pada jadwal per jam (06.00–18.00 WIB), sistem mengevaluasi seluruh aturan cuaca secara independen. Status akhir setiap jam ditentukan oleh risiko tertinggi:\n"
        "• Jika salah satu aturan menghasilkan DANGER (Merah) -> Status jam otomatis DANGER (Hindari pelaksanaan).\n"
        "• Jika tidak ada DANGER tetapi ada WARN (Kuning) -> Status jam menjadi WARN (Waspada / sesuaikan teknik).\n"
        "• Jam hanya berstatus SAFE (Hijau) jika SELURUH aturan cuaca menyatakan aman.",
        bold_prefix="Worst-Of Aggregation: "
    )

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig23_phase11_hourly_advisory_schedule_matrix.png",
        "FIGUR 3: Matriks Rekomendasi Jam Operasional Harian (06.00–18.00 WIB) — Evaluasi Multi-Tindakan Berdasarkan Kecepatan Angin, Hujan, dan Radiasi Surya."
    )

    # =========================================================================
    # BAB 6: PETA LENGKAP 5 KOMODITAS & PERLAKUAN KHUSUS
    # =========================================================================
    add_heading_1(doc, "BAB 6: PETA LENGKAP 5 KOMODITAS & PERLAKUAN KHUSUS (PADI & CABAI)")
    
    add_p(doc,
        "Berikut ringkasan perlakuan khusus kelima komoditas di dalam sistem TaniAdapt:",
        bold_prefix="Perlakuan Komoditas di Engine: "
    )

    crop_action_guide_rows = [
        ["1. Padi Sawah", "Modul air INSUFFICIENT (sawah tergenang). Semprot, pupuk, dan panen AKTIF PENUH.", "Muncul badge abu-abu: 'Bukti belum cukup (sawah tergenang)'. Jadwal semprot angin aman dan pupuk tetap memandu petani."],
        ["2. Jagung Pipil", "Semua 5 tindakan operasional AKTIF 100% (Irigasi FAO-56, Semprot, Pupuk, Panen Kering, Rawat).", "Lampu hijau siram menyala jika Dr > RAW (82.5 mm pada tanah loam). Panen biji kering di batang (Kc_end = 0.35)."],
        ["3. Kedelai", "Semua 5 tindakan operasional AKTIF 100% (Irigasi FAO-56, Semprot, Pupuk, Panen Kering, Rawat).", "Siklus tumbuh cepat (85 hari). Panen polong tua kering saat RH <= 75%."],
        ["4. Cabai Merah & Rawit", "Modul air INSUFFICIENT (karena FAO-56 tidak memuat cabai tropis). Modul jamur patek LWD, semprot, wiwil, dan panen SANGAT AKTIF.", "CABAI TETAP DIPAKAI PENUH! Petani cabai sangat terbantu oleh peringatan jamur patek saat fajar lembap, panduan semprot angin aman, panduan wiwil tunas air, dan larangan petik saat basah hujan."],
        ["5. Tomat", "Semua modul AKTIF PENUH (Irigasi FAO-56 Kc=0.80, Semprot, Pupuk, Wiwil tunas air, Panen segar, LWD jamur).", "Rentan busuk daun fajar jika RH >= 90%. Perempelan tunas air (wiwil) dipandu cuaca cerah tanpa hujan 8 jam ke depan."]
    ]
    add_table_data(doc, ["Komoditas", "Status Tindakan di Decision Engine", "Tampilan Nyata di Antarmuka Web Petani"], crop_action_guide_rows, [1.4, 2.5, 2.6])

    # =========================================================================
    # BAB 7: PANDUAN PENGEMBANGAN WEB UNTUK TIM DEVELOPER
    # =========================================================================
    add_heading_1(doc, "BAB 7: PANDUAN PENGEMBANGAN WEB UNTUK TIM DEVELOPER")

    add_heading_2(doc, "1. Memanggil Route Handler Backend (POST /api/advisory)")
    add_p(doc, "Frontend cukup melakukan request HTTP POST ke endpoint server tanpa perlu menghitung rumus fisika:")
    add_clean_formula_box(doc, [
        "Request Client ke Route Handler Next.js:",
        "",
        "POST /api/advisory",
        "Content-Type: application/json",
        "",
        "{",
        '  "crop": "jagung",                    // padi | jagung | kedelai | cabai | tomat',
        '  "latitude": -6.4830,                 // Koordinat lahan',
        '  "longitude": 107.7322,',
        '  "kabkota": "KABUPATEN SUBANG",       // Nama wilayah',
        '  "planting_date": "2026-09-01",       // Format YYYY-MM-DD (menentukan HST / umur tanaman)',
        '  "panen_kering": true,                // Opsional, default true (panen biji kering)',
        '  "initial_depletion_dr0_mm": 0.0      // Opsional, default 0 mm (kapasitas lapang)',
        "}"
    ], label="Endpoint API Advisory (route.ts)")

    add_heading_2(doc, "2. Format Response JSON yang Diterima Frontend")
    add_clean_formula_box(doc, [
        "Respons JSON Terverifikasi (Patuh Draft 2020-12):",
        "",
        "{",
        '  "crop": "jagung",',
        '  "as_of": "2026-10-13",',
        '  "status": "kondisi_stres_abiotik",',
        '  "actions": [',
        '    {',
        '      "action": "irrigation",',
        '      "window": "06.00 - 08.00 WIB",',
        '      "status_label": "Sangat Aman",',
        '      "rule_status": "VERIFIED_METHOD",',
        '      "evidence_refs": ["RULE_WATER_FAO56_DEPLETION", "FAO56_RAW_DEPLETION"],',
        '      "reason": "Deplesi air tanah (Dr = 90 mm) melampaui air siap serap (RAW = 82.5 mm). Sangat dianjurkan segera menyiram."',
        '    }',
        '  ],',
        '  "hourly": [',
        '    { "hour": "06.00", "status": "SAFE", "reason": "Kondisi operasional optimal" },',
        '    { "hour": "12.00", "status": "WARN", "reason": "Terik radiasi surya > 500 W/m²" }',
        '  ],',
        '  "sensitif_terhadap_asumsi_tanah": false,',
        '  "asumsi_deplesi_awal_dr0": 0.0',
        "}"
    ], label="Contoh Response JSON Kontrak Skema")

    add_heading_2(doc, "3. Konsep Antarmuka Dua Lapis (Two-Layer UI)")
    add_p(doc,
        "• Lapis 1 (Farmer-Friendly): Kartu aksi dengan lampu indikator warna (Hijau/Kuning/Merah/Abu-abu), rentang jam terbaik (misal: '06.00 - 08.00 WIB'), dan panduan aksi praktis lapangan.\n"
        "• Lapis 2 (Scientifically Grounded): Badge status rujukan ilmiah ('Metode terverifikasi FAO-56', 'Konvensi tim', 'Metode belum dikalibrasi', 'Bukti belum cukup'), ID referensi bukti, kotak peringatan sensitivitas tanah jika aktif, dan tautan ke halaman transparansi '/sumber-dan-batasan'.",
        bold_prefix="Two-Layer UI: "
    )

    add_heading_2(doc, "4. State Management Water Ledger & Proyeksi 7 Hari")
    add_p(doc,
        "• Begitu petani mendaftarkan tanamannya di Hari ke-1 (HST 1), web menyimpan status harian di LocalStorage/Database (Water Ledger).\n"
        "• Setiap hari nilai Dr diperbarui otomatis mengikuti cuaca riil dan pencatatan siraman di tombol 'Tandai selesai hari ini' (mereset Dr0 kembali ke 0 mm).\n"
        "• Menggunakan prakiraan 7 hari Open-Meteo, engine dapat menjalankan simulasi maju cepat (forward simulation) untuk memproyeksikan hari ke berapa Dr akan menembus RAW, memunculkan kartu peringatan dini: 'Perhatian: Tanaman Anda diproyeksikan stres kekeringan dalam 3 hari ke depan (Kamis). Siapkan pompa air.'",
        bold_prefix="Buku Kas Air: "
    )

    # Summary Callout
    add_callout(doc,
        "Dengan buku panduan master ini, seluruh anggota tim pengembang memiliki pemahaman ilmiah dan teknis yang seragam. TaniAdapt membuktikan perpaduan sejati antara integritas sains agrometeorologi dunia dan kecanggihan rekayasa perangkat lunak modern.",
        title="PENUTUP BUKU PANDUAN MASTER"
    )

    doc.save(OUT_DOCX)
    print(f"Successfully generated Master Guidebook at {OUT_DOCX}")


if __name__ == "__main__":
    build_master_guide()
