"""Generate Comprehensive Decision Engine Design, Formulas, and Implementation Blueprint in Indonesian (.docx).
Location: context/to_fathir/TaniAdapt_Desain_Rumus_dan_Skema_Decision_Engine.docx
Revised v2:
- Fully includes all 5 commodities (Padi, Jagung, Kedelai, Cabai Merah & Rawit, Tomat)
- Fixes confusing "SAFE / WARN" labeling for irrigation: clearly separates CROP STATUS from ACTION RECOMMENDATION
- Explicitly differentiates horticulture operations (Cabai & Tomat: wiwil/pruning, periodic harvest, fungal LWD scouting) from field grain crops (Jagung & Kedelai)
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
OUT_DOCX = PROJECT_ROOT / "context" / "to_fathir" / "TaniAdapt_Desain_Rumus_dan_Skema_Decision_Engine_v2.docx"
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
            elif any(k in val_str for k in ["CONVENTION", "Perlu Waspada", "WARN", "Waspada", "UNCALIBRATED", "Belum Perlu"]):
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


def add_formula_box(doc, formula_text: str, label: str = ""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "F8FAFC")
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    left_b = OxmlElement("w:left")
    left_b.set(qn("w:val"), "single")
    left_b.set(qn("w:sz"), "18")
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
    if label:
        r_lab = p.add_run(f"[{label}]\n")
        r_lab.bold = True
        r_lab.font.name = "Aptos"
        r_lab.font.size = Pt(8.5)
        r_lab.font.color.rgb = RGBColor(44, 82, 130)
    r_form = p.add_run(formula_text)
    r_form.bold = True
    r_form.font.name = "Consolas"
    r_form.font.size = Pt(9.2)
    r_form.font.color.rgb = RGBColor(20, 20, 20)
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


def build_design_doc():
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
    r_title = p_title.add_run("TANIADAPT DECISION ENGINE: CETAK BIRU ARSITEKTUR, FORMULA BIOFISIK, & SKEMA IMPLEMENTASI")
    r_title.bold = True
    r_title.font.name = "Aptos Display"
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = RGBColor(27, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("Dokumen Desain Sistem Lengkap: Seluruh Persamaan Fisika FAO-56, Matriks Logika Jam Operasional,\nPembedaan Karakteristik 5 Komoditas (Padi, Jagung, Kedelai, Cabai Merah/Rawit, Tomat), dan Cetak Biru Web Next.js")
    r_sub.font.name = "Aptos"
    r_sub.font.size = Pt(10.5)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(44, 82, 130)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Disusun Khusus Untuk: Fathir Rizki Fadillah | Engine Version: v2.4-verified-params | Kontrak: Draft 2020-12")
    r_meta.font.name = "Aptos"
    r_meta.font.size = Pt(9.0)
    r_meta.bold = True
    r_meta.font.color.rgb = RGBColor(100, 100, 100)

    # =========================================================================
    # BAB 1: FILOSOFI & ARSITEKTUR SISTEM
    # =========================================================================
    add_heading_1(doc, "BAB 1: FILOSOFI & ARSITEKTUR SISTEM (THE BIG PICTURE)")
    
    add_p(doc,
        "Decision Engine TaniAdapt adalah modul komputasi biofisik deterministik yang berfungsi menerjemahkan data agrometeorologi hiperlokal (data cuaca harian dan per jam) menjadi evaluasi kartu tindakan operasional lapangan (Siram, Pupuk, Semprot, Panen, dan Olah Tanah) bagi petani di Jawa Barat.",
        bold_prefix="Definisi Sistem: "
    )

    add_p(doc,
        "Di sektor pertanian pangan, keputusan petani membawa konsekuensi fatal: kegagalan panen, pemborosan solar pompa air, pencemaran racun kimia, atau tanaman hangus terbakar. Sistem ini menolak keras dua jebakan umum dalam aplikasi AI saat ini:\n"
        "1. Menolak Model Prediktif Black-Box (ML Yield Prediction): Riset Phase 9 telah membuktikan secara empiris bahwa model Machine Learning (OLS, Ridge, Lasso, Elastic Net, dan Random Forest) mengalami keruntuhan generalisasi out-of-sample (LOYO CV R² ≈ 0). Data statistik tahunan dinas didominasi oleh noise non-cuaca (subsidi pupuk, mutu benih, hama tikus, manipulasi data birokrasi).\n"
        "2. Menolak LLM sebagai Pengambil Keputusan: Model AI generatif bersifat stokastik (probabilistik) dan rawan mengalami halusinasi numerik. Mengizinkan LLM mengarang dosis fungisida atau menetapkan waktu irigasi adalah tindakan berbahaya.",
        bold_prefix="Mengapa Bukan ML atau LLM Langsung? "
    )

    add_callout(doc,
        "Arsitektur Decoupled TaniAdapt memisahkan secara fisik dan logis antara Otak Keputusan (Decision Engine) dan Lapisan Komunikasi (LLM Explainer). Decision Engine 100% deterministik, berbasis rumus fisika baku FAO-56 dan aturan terdaftar di rules.json, menghasilkan payload JSON yang terkunci kontrak skema. LLM hanya membaca alasan yang sudah diputuskan oleh Engine dan menarasikannya ke dalam bahasa santun tanpa wewenang menambah angka.",
        title="PRINSIP ARSITEKTUR DECOUPLED"
    )

    add_p(doc,
        "Alur pipa data berjalan satu arah tanpa siklus tertutup:\n"
        "Input Petani (Tanaman, Tanggal Tanam, Lokasi) + Live Weather API (Open-Meteo ERA5) \n"
        "    ↓\n"
        "Pure TypeScript Decision Engine (fao56.ts, kc.ts, waterBalance.ts, percentile.ts)\n"
        "    ↓ [Validasi Kontrak Ajv Draft 2020-12]\n"
        "Payload JSON Terverifikasi (actions[], hourly[], status, evidence_refs[])\n"
        "    ↓\n"
        "Antarmuka Web Dua Lapis (Next.js) + Agen Suara LLM (RAG 16 Paper Ilmiah)",
        bold_prefix="Alur Aliran Data: "
    )

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig24_phase11_decision_trace_flowchart.png",
        "FIGUR 1: Diagram Alir Pohon Rekam Jejak Keputusan (Decision Trace Flowchart) — Struktur Penelusuran Logika Deterministik Tanpa Halusinasi."
    )

    # =========================================================================
    # BAB 2: PORTOFOLIO LENGKAP 5 KOMODITAS & PEMBEDAAN KARAKTERISTIK
    # =========================================================================
    add_heading_1(doc, "BAB 2: PORTOFOLIO LENGKAP 5 KOMODITAS & PEMBEDAAN KARAKTERISTIK")
    
    add_p(doc,
        "Decision Engine TaniAdapt secara tegas membedakan sifat biologis, agronomis, dan perlakuan operasional antara tanaman pangan semusim (Padi, Jagung, Kedelai) dan tanaman hortikultura buah berkala (Cabai Merah, Cabai Rawit, Tomat). Sistem tidak menyeragamkan aturan ke dalam satu cetakan kaku.",
        bold_prefix="Pembedaan Agronomis Komoditas: "
    )

    crop_detail_rows = [
        ["1. Padi Sawah (Oryza sativa)", "Pangan Pokok Semusim", "Regim Tergenang (Ponded Wetland)", "30/30/35/25 (120 hari)", "Modul deplesi tanah TIDAK BERLAKU (INSUFFICIENT). Modul semprot, pupuk, dan panen aktif."],
        ["2. Jagung Pipil (Zea mays)", "Pangan / Pakan Semusim", "Lahan Kering (Tanah Tak Jenuh)", "20/35/40/30 (125 hari)", "Modul air AKTIF PENUH (Zr=1.0 m, p=0.55). Panen biji kering lapangan (RH <= 75%)."],
        ["3. Kedelai (Glycine max)", "Pangan Legum Semusim", "Lahan Kering (Tanah Tak Jenuh)", "15/15/40/15 (85 hari)", "Modul air AKTIF PENUH (Zr=0.8 m, p=0.50). Pemanenan polong tua kering."],
        ["4. Cabai Merah Besar (Capsicum annuum)", "Hortikultura Buah Petik Berkala", "Lahan Kering / Bedengan Mulsa", "Siklus panen petik bertahap", "Sangat rentan patek/antraknosa (scouting LWD). Butuh perempelan tunas air (pruning/wiwil)."],
        ["5. Cabai Rawit (Capsicum frutescens)", "Hortikultura Buah Petik Panjang", "Lahan Kering / Bedengan", "Siklus hidup panjang (6-12 bulan)", "Tajuk kompak, rentan rontok bunga saat terik radiasi ekstrem (>500 W/m²). Petik berkala."],
        ["6. Tomat (Solanum lycopersicum)", "Hortikultura Buah Segar", "Lahan Kering / Bedengan", "30/40/45/30 (145 hari)", "Modul air AKTIF (Zr=0.7 m, p=0.40, Kc=0.80). Butuh wiwil tunas air & sanitasi luka pangkas."]
    ]
    add_table_data(doc, ["Komoditas Binaan", "Tipe Tanaman", "Regim Lingkungan Perakaran", "Panjang Siklus Tumbuh", "Perlakuan Khusus di Decision Engine"], crop_detail_rows, [1.4, 1.2, 1.3, 1.1, 2.0])

    add_heading_2(doc, "Mengapa Cabai Merah dan Cabai Rawit Dibedakan?")
    add_p(doc,
        "1. Morfologi Tajuk & Kelembapan Mikro: Cabai Merah Besar memiliki tajuk kanopi yang lebih rimbun dan daun lebih lebar, sehingga kelembapan mikro di dalam kanopi bertahan lebih lama di pagi hari (risiko spora jamur antraknosa Colletotrichum gloeosporioides lebih tinggi). Cabai Rawit memiliki daun lebih kecil dan tajuk lebih terbuka.\n"
        "2. Dinamika Pemanenan: Cabai Merah dipanen serentak per interval 7–10 hari begitu buah matang merah penuh; pemanenan saat hujan dilarang keras karena tangkai buah basah memicu pembusukan di karung pengiriman. Cabai Rawit memiliki interval pemanenan lebih fleksibel (dapat dipetik hijau atau merah) namun sangat sensitif terhadap cekaman air fajar yang menyebabkan kerontokan bunga muda.\n"
        "3. Kerentanan Terik Siang: Cabai rawit di dataran rendah Jawa Barat (seperti Pantura) rentan mengalami gugur bunga jika terpapar radiasi surya > 500 W/m² bersamaan dengan VPD tinggi (> 15 hPa).",
        bold_prefix="Karakteristik Cabai: "
    )

    # =========================================================================
    # BAB 3: FORMULA BIOFISIK MEKANISTIK FAO-56 LENGKAP
    # =========================================================================
    add_heading_1(doc, "BAB 3: FORMULA BIOFISIK MEKANISTIK FAO-56 LENGKAP")
    add_p(doc, "Seluruh formula mekanistik di dalam Decision Engine mengacu secara murni pada dokumen rujukan internasional: FAO Irrigation and Drainage Paper 56 (Allen et al., 1998; URL: https://www.fao.org/4/x0490e).")

    add_heading_2(doc, "A. Komponen 1: Evapotranspirasi Acuan Penman-Monteith Harian (ET0)")
    add_p(doc, "Formula Penman-Monteith menghitung laju penguapan air dari permukaan rumput acuan ideal setinggi 0,12 meter dengan resistensi kanopi 70 s/m dan albedo 0,23:")

    add_formula_box(doc,
        "ET0 = [ 0.408 * Δ * (Rn - G) + γ * (900 / (Tmean + 273)) * u2 * (es - ea) ] / [ Δ + γ * (1 + 0.34 * u2) ]\n\n"
        "Di mana:\n"
        "- ET0  : Evapotranspirasi acuan (mm/hari)\n"
        "- Rn   : Radiasi surya bersih pada permukaan tanaman (MJ m-2 hari-1)\n"
        "- G    : Fluks panas tanah harian (G = 0 untuk perhitungan harian, Eq. 42)\n"
        "- Tmean: Suhu rata-rata harian (Tmax + Tmin) / 2 (°C)\n"
        "- u2   : Kecepatan angin pada ketinggian 2 meter (m/s)\n"
        "- es   : Tekanan uap jenuh rata-rata (kPa)\n"
        "- ea   : Tekanan uap aktual (kPa)\n"
        "- Δ    : Kemiringan kurva tekanan uap jenuh terhadap suhu (kPa °C-1)\n"
        "- γ    : Konstanta psikrometrik atmosfer (kPa °C-1)",
        label="FAO-56 Bab 4, Persamaan 6 (Eq. 6)"
    )

    add_p(doc, "Persamaan pendukung termodinamika atmosfer:")
    add_formula_box(doc,
        "1. Tekanan Uap Jenuh (Eq. 11):\n"
        "   e0(T) = 0.6108 * exp( (17.27 * T) / (T + 237.3) )\n"
        "   es = ( e0(Tmax) + e0(Tmin) ) / 2\n\n"
        "2. Kemiringan Kurva Tekanan Uap (Eq. 13):\n"
        "   Δ = ( 4098 * es ) / (Tmean + 237.3)^2\n\n"
        "3. Tekanan Udara Barometrik & Konstanta Psikrometrik (Eq. 7 & Eq. 8):\n"
        "   P = 101.3 * [ (293 - 0.0065 * z) / 293 ]^5.26  (z = elevasi DEM SRTM, meter)\n"
        "   γ = 0.000665 * P\n\n"
        "4. Konversi Kecepatan Angin 10m ke 2m (Eq. 47):\n"
        "   u2 = u10 * [ 4.87 / ln(67.8 * 10 - 5.42) ] ≈ u10 * 0.7479\n\n"
        "5. Radiasi Surya Bersih (Eq. 38 & Eq. 39):\n"
        "   Rn = Rns - Rnl = 0.77 * Rs - Rnl\n"
        "   Rnl = σ * [ (Tmax_K^4 + Tmin_K^4) / 2 ] * (0.34 - 0.14 * sqrt(ea)) * [ 1.35 * (Rs / Rso) - 0.35 ]",
        label="Persamaan Pendukung Fisika Atmosfer FAO-56"
    )

    add_p(doc,
        "Validasi Independen: Formula di atas telah diuji terhadap Contoh 18 Bab 4 FAO-56 (Brussels/Uccle benchmark). Hasil komputasi TypeScript menghasilkan ET0 = 3,877 mm/hari, cocok sempurna dengan angka standar FAO 3,88 mm/hari (selisih < 0,01 mm/hari, status PASS).",
        bold_prefix="Uji Validasi Benchmark Example 18: "
    )

    add_heading_2(doc, "B. Komponen 2: Koefisien Tanaman Dinamis Kc(t)")
    add_p(doc,
        "Kebutuhan air tanaman riil dihitung dari perkalian evapotranspirasi acuan dengan koefisien tanaman: ETc = Kc * ET0. Nilai Kc berubah secara dinamis mengikuti umur tanaman (Hari Setelah Tanam / HST / DAP) yang terbagi dalam 4 fase fenologi (FAO-56 Bab 6, Tabel 11 & Tabel 12):",
        bold_prefix="Kurva Kc Dinamis: "
    )

    add_formula_box(doc,
        "Kc(t) = \n"
        "  - Kc_ini                          , jika t <= L_ini (Fase Awal)\n"
        "  - Kc_ini + [ (t - L_ini) / L_dev ] * (Kc_mid - Kc_ini) , jika L_ini < t <= L_ini + L_dev (Fase Perkembangan)\n"
        "  - Kc_mid                          , jika L_ini + L_dev < t <= L_ini + L_dev + L_mid (Fase Pertengahan)\n"
        "  - Kc_mid + [ (t - (L_ini+L_dev+L_mid)) / L_late ] * (Kc_end - Kc_mid) , jika t > L_ini + L_dev + L_mid (Fase Akhir)",
        label="Interpolasi Dinamis Kurva Kc FAO-56"
    )

    kc_rows = [
        ["Jagung Pipil (Grain)", "0.30", "1.20", "0.35 (kering) / 0.60 (basah)", "20 / 35 / 40 / 30 (125 hari)", "Tabel 12 Footnote 11: 0.35 panen biji kering di batang, 0.60 panen basah."],
        ["Kedelai", "0.40", "1.15", "0.50", "15 / 15 / 40 / 15 (85 hari)", "Tabel 12: nilai tunggal definitif panen polong kering; Tabel 11 Tropics."],
        ["Tomat", "0.60", "1.15", "0.80 (rentang 0.70–0.90)", "30 / 40 / 45 / 30 (145 hari)", "Tabel 12: 0.70 olahan industri, 0.80 konsumsi segar (titik tengah CONVENTION_PENDING)."],
        ["Cabai Merah & Rawit", "UNVERIFIED", "UNVERIFIED", "UNVERIFIED", "Siklus petik bertahap", "Kc tropis lokal belum terdaftar di FAO-56 (sweet pepper tidak diekstrapolasi)."],
        ["Padi Sawah", "1.05", "1.20", "0.60 (kering) / 0.90 (genang)", "30 / 30 / 35 / 25 (120 hari)", "Tabel 12 mengasumsikan sawah tergenang; deplesi tanah TIDAK BERLAKU (INSUFFICIENT)."]
    ]
    add_table_data(doc, ["Komoditas", "Kc Awal", "Kc Tengah", "Kc Akhir", "Panjang Fase (hari)", "Dasar Bukti & Asumsi Panen"], kc_rows, [1.5, 0.8, 0.8, 1.3, 1.2, 1.6])

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig21_phase10_abiotic_water_risk_calibration.png",
        "FIGUR 2: Model Biofisik Mekanistik FAO-56 — Kurva Koefisien Tanaman Dinamis (Kc) dan Kalibrasi Neraca Air Evapotranspirasi."
    )

    add_heading_2(doc, "C. Komponen 3: Neraca Deplesi Air Tanah Zona Perakaran (Dr vs RAW)")
    add_p(doc,
        "Alih-alih menggunakan ambang tebakan ad-hoc, keputusan irigasi didasarkan pada fisika air tanah tak jenuh FAO-56 Bab 8 (Allen et al., 1998):",
        bold_prefix="Prinsip Deplesi Air Tanah: "
    )

    add_formula_box(doc,
        "1. Total Available Water (TAW, mm) — FAO-56 Bab 8, Persamaan 82 (Eq. 82):\n"
        "   TAW = 1000 * (θ_FC - θ_WP) * Zr\n"
        "   Di mana θ_FC adalah kapasitas lapang, θ_WP adalah titik layu permanen, dan Zr adalah kedalaman akar aktif (meter).\n\n"
        "2. Readily Available Water (RAW, mm) — FAO-56 Bab 8, Persamaan 83 (Eq. 83):\n"
        "   RAW = p * TAW\n"
        "   Di mana p adalah fraksi deplesi air tanah tanpa menimbulkan cekaman air (FAO-56 Bab 8, Tabel 22).\n\n"
        "3. Neraca Deplesi Harian (Dr, mm) — FAO-56 Bab 8, Persamaan 85 (Eq. 85):\n"
        "   Dr(t) = Dr(t-1) - P_eff(t) + ETc(t)\n"
        "   Dengan batasan fisik: 0 <= Dr(t) <= TAW (air hujan melebihi TAW diasumsikan limpasan/perkolasi dalam).\n\n"
        "4. Kriteria Pengambilan Keputusan Irigasi:\n"
        "   - Jika Dr > RAW : Status Tanaman = Cekaman Air (kondisi_stres_abiotik) -> Aksi SIRAM = Sangat Dianjurkan.\n"
        "   - Jika Dr <= RAW: Status Tanaman = Normal (Air Cukup) -> Aksi SIRAM = Belum Perlu (Tahan/Hemat Air).",
        label="Formula Neraca Deplesi Lengas Tanah FAO-56 Bab 8"
    )

    add_p(doc,
        "Konfigurasi Parameter Fisik Tanah & Akar (rules.json v2.4):",
        bold_prefix="Parameter Fisik Terverifikasi: "
    )
    add_p(doc,
        "• Tanah Loam Standar: θ_FC = 0.27 (rentang 0.20–0.30), θ_WP = 0.12 (rentang 0.07–0.17), TAW dasar = 150.0 mm/m (rentang 130–180 mm/m) (FAO-56 Bab 7, Tabel 19).\n"
        "• Kedalaman Akar Zr: Jagung Zr = 1.0 m (rentang 1.0–1.7 m); Kedelai Zr = 0.8 m (rentang 0.6–1.3 m); Tomat Zr = 0.7 m (rentang 0.7–1.5 m) (FAO-56 Bab 8, Tabel 22).\n"
        "• Fraksi Deplesi p: Jagung p = 0.55; Kedelai p = 0.50; Tomat p = 0.40; Padi p = 0.20 (FAO-56 Bab 8, Tabel 22).\n"
        "• Asumsi Awal Deplesi Dr0: Dijadikan input eksplisit (default Dr0 = 0 mm, kondisi kapasitas lapang setelah olah tanah).\n"
        "• Analisis Sensitivitas Tanah: Engine secara otomatis mengevaluasi sensitivitas TAW pada batas bawah (130 mm/m) dan batas atas (180 mm/m). Jika status keputusan siram berubah di antara kedua batas, engine menyalakan flag 'sensitif_terhadap_asumsi_tanah = true' untuk memperingatkan petani."
    )

    add_p(doc,
        "Uji Paritas Independen Example 36: Kode engine telah diuji terhadap Contoh 36 FAO-56 untuk 3 jenis tekstur tanah (Loamy Sand, Silt, Silty Clay). Seluruh hasil TAW dan RAW menghasilkan nilai persis dengan toleransi <= 1 mm (Tomat: 72/29, 136/54, 96/38 mm; Jagung: 108/59, 204/112, 144/79 mm), membuktikan kebenaran implementasi matematika.",
        bold_prefix="Uji Paritas Example 36: "
    )

    # =========================================================================
    # BAB 4: MATRIKS KEPUTUSAN JAM-JAMAN & LOGIKA OPERASIONAL
    # =========================================================================
    add_heading_1(doc, "BAB 4: MATRIKS KEPUTUSAN JAM-JAMAN (06.00–18.00 WIB) & TINDAKAN LAPANGAN")
    
    add_p(doc,
        "PENTING: Di Decision Engine TaniAdapt, kita membedakan secara tegas antara STATUS KONDISI TANAMAN / CUACA dengan REKOMENDASI STATUS TINDAKAN OPERASIONAL PETANI:",
        bold_prefix="Klarifikasi Pelabelan Aksi vs Kondisi Tanaman: "
    )
    add_p(doc,
        "1. Pada Modul Irigasi (Siram):\n"
        "   - Ketika kondisi tanaman Dr > RAW (tanah haus / stres cekaman air), maka status rekomendasi tindakan bagi petani adalah SANGAT AMAN / DIANJURKAN SEGERA MENYIRAM (label: Sangat Aman, lampu hijau pada tombol siram).\n"
        "   - Ketika kondisi tanaman Dr <= RAW (air tanah masih mencukupi), maka status rekomendasi tindakan bagi petani adalah BELUM PERLU MENYIRAM / TAHAN (label: Perlu Waspada, lampu kuning agar hemat air dan solar pompa).\n"
        "   - Ketika terjadi hujan aktif >= 3 mm, status tindakan menjadi HINDARI MENYIRAM (label: Hindari, lampu merah).\n"
        "2. Pada Modul Tindakan Fisik Lainnya (Semprot, Pupuk, Panen, Pangkas):\n"
        "   - Status 'Sangat Aman' berarti kondisi cuaca optimal untuk melakukan pekerjaan fisik tersebut.\n"
        "   - Status 'Perlu Waspada' berarti ada parameter cuaca di zona transisi yang memerlukan penyesuaian teknik.\n"
        "   - Status 'Hindari' berarti kondisi cuaca berbahaya bagi tanaman, lingkungan, atau efektivitas bahan."
    )

    action_matrix_rows = [
        ["1. Siram (Irigasi)", "06.00 - 08.00 WIB", "Dr > RAW (tanah butuh air irigasi)", "Dr <= RAW (air tanah masih cukup)", "Hujan aktif >= 3 mm (air berlebih)", "FAO-56 Bab 8 (VERIFIED_METHOD). Jagung, kedelai, tomat aktif. Padi sawah mengembalikan evidence_insufficient."],
        ["2. Semprot (Pestisida)", "06.00 - 08.00 WIB", "Angin 3–12 km/j, T < 30°C", "Angin < 3 km/j (inversi fajar) atau 12–15 km/j (transisi drift)", "Angin > 15 km/j atau Hujan >= 3 mm", "Menutup celah angin: <3 km/j partikel racun terperangkap, >15 km/j spray drift melayang ke tetangga."],
        ["3. Pupuk (Pemupukan)", "07.00 - 09.00 WIB", "Tanah lembap, hujan 12h < 8 mm", "VPD > 15 hPa atau terik radiasi", "Prakiraan hujan 12h >= 8 mm", "Mencegah pupuk hanyut tererosi limpasan air hujan atau membakar daun saat stomata tertutup."],
        ["4. Panen Pangan (Jagung/Kedelai)", "08.00 - 12.00 WIB", "RH <= 75%, hujan = 0 mm", "RH 75–85% (zona transisi jemur)", "RH > 85% atau Hujan > 5 mm", "Panen biji/polong kering. Menutup celah RH 75-85%: status WARN mengingatkan perlunya penjemuran segera."],
        ["5. Panen Hortikultura (Cabai/Tomat)", "07.00 - 10.00 WIB", "Tanpa hujan, suhu sejuk pagi", "Embun daun masih basah", "Hujan aktif atau buah basah kuyup", "Pemanenan buah segar bertahap. Dilarang petik saat basah kuyup karena memicu busuk buah di wadah simpan."],
        ["6. Rawat / Pangkas (Tomat/Cabai)", "07.00 - 09.00 WIB", "Hujan 8h < 2 mm, cuaca cerah", "Kelembapan malam tinggi", "Prakiraan hujan 8h >= 2 mm", "Perempelan tunas air (wiwil) tomat & cabai. Mencegah luka pangkas basah terinfeksi spora jamur."],
        ["7. Pengamatan OPT (Cabai/Tomat)", "Pagi hari (06.00 WIB)", "RH malam normal < 90%", "Jumlah jam RH >= 90% >= 10 jam", "Kondisi basah terus-menerus", "Indikator Leaf Wetness Duration (LWD Sentelhas 2008, METHOD_UNCALIBRATED). Waspada patek/antraknosa."]
    ]
    add_table_data(doc, ["Tindakan Lapangan", "Window Ideal", "Kondisi Disarankan (Sangat Aman)", "Kondisi Penyesuaian (Perlu Waspada)", "Kondisi Larangan (Hindari)", "Dasar Biofisik & Spesifikasi Tanaman"], action_matrix_rows, [1.4, 1.1, 1.2, 1.2, 1.1, 1.8])

    add_heading_2(doc, "Logika Penggabungan Teraman (Worst-Of Aggregation) per Jam")
    add_p(doc,
        "Pada jadwal per jam (06.00–18.00 WIB), sistem mengevaluasi seluruh aturan cuaca secara independen. Jika terdapat lebih dari satu aturan yang terpicu dalam satu jam yang sama, status akhir jam tersebut ditentukan oleh status paling berisiko:\n"
        "1. Jika salah satu aturan menghasilkan DANGER (Merah) -> Status jam otomatis DANGER (Hindari pelaksanaan).\n"
        "2. Jika tidak ada DANGER tetapi terdapat WARN (Kuning) -> Status jam menjadi WARN (Perlu waspada / sesuaikan teknik).\n"
        "3. Jam hanya berstatus SAFE (Hijau) jika SELURUH aturan cuaca menyatakan aman.",
        bold_prefix="Prinsip Worst-Of: "
    )

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig23_phase11_hourly_advisory_schedule_matrix.png",
        "FIGUR 3: Matriks Rekomendasi Jam Operasional Harian (06.00–18.00 WIB) — Evaluasi Multi-Tindakan Berdasarkan Kecepatan Angin, Hujan, dan Radiasi Surya."
    )

    # =========================================================================
    # BAB 5: KONTRAK SKEMA JSON DRAFT 2020-12
    # =========================================================================
    add_heading_1(doc, "BAB 5: KONTRAK SKEMA JSON DRAFT 2020-12 & INTEGRITAS DATA")
    
    add_p(doc,
        "Untuk menjamin bahwa Decision Engine tidak pernah menghasilkan format yang cacat atau mengarang angka di luar kontrak, keluaran engine diikat oleh JSON Schema Draft 2020-12 (schemas/engine_output.schema.json).",
        bold_prefix="Penerapan Contract-First: "
    )

    add_p(doc,
        "Ketentuan Keras di Level Skema:\n"
        "1. additionalProperties: false ditegakkan di level root dan seluruh nested object (tidak boleh ada properti liar).\n"
        "2. Format Waktu: issue_time wajib mematuhi standar RFC 3339 ISO 8601 date-time.\n"
        "3. Pengetatan Kondisional (if/then Clause):\n"
        "   - Jika status == 'kondisi_stres_abiotik', evidence_refs WAJIB memuat ID aturan pemicu: 'RULE_WATER_FAO56_DEPLETION'.\n"
        "   - Kombinasi ID FAO lain (seperti hanya mencantumkan FAO56_RAW_DEPLETION tanpa ID aturan) otomatis DITOLAK.\n"
        "4. Status 'kondisi_mendukung_OPT' Dihapus dari Enum Level Atas:\n"
        "   - Karena belum ada aturan OPT berstatus VERIFIED_METHOD, status ini dinyatakan tak terjangkau di level atas.\n"
        "   - Aturan kebasahan daun Sentelhas 2008 berstatus METHOD_UNCALIBRATED dan hanya diizinkan muncul pada level kartu tindakan scouting_opt.\n"
        "5. Modul Padi: Wajib mengembalikan status 'evidence_insufficient' karena asumsi sawah tergenang air.",
        bold_prefix="Aturan Validasi Kontrak: "
    )

    # =========================================================================
    # BAB 6: SKEMA PENERAPAN DI WEB NEXT.JS (PHASE 13)
    # =========================================================================
    add_heading_1(doc, "BAB 6: SKEMA PENERAPAN DI WEB NEXT.JS (CETAK BIRU PHASE 13)")

    add_heading_2(doc, "A. Arsitektur Route Handler Server-Side (/api/advisory)")
    add_p(doc,
        "Aplikasi web Next.js di repo taniadapt-web mengakses Decision Engine melalui endpoint API server-side:\n"
        "1. Client mengirimkan request POST ke /api/advisory membawa parameter: crop, latitude, longitude, kabkota, planting_date.\n"
        "2. Input divalidasi menggunakan Zod Schema. Jika parameter tanggal atau koordinat cacat, API mengembalikan HTTP 400 Bad Request.\n"
        "3. Server memanggil Open-Meteo Weather API untuk koordinat lahan petani secara asinkron.\n"
        "4. Pure Decision Engine TypeScript (src/lib/engine/) dieksekusi dalam hitungan milidetik tanpa subprocess Python.\n"
        "5. Payload keluaran divalidasi menggunakan Ajv Draft 2020-12 terhadap engine_output.schema.json. Jika terjadi pelanggaran skema sekecil apa pun, API mengembalikan HTTP 500.\n"
        "6. Client menerima objek JSON yang bersih, terverifikasi, dan siap dirender ke komponen React.",
        bold_prefix="Alur Server API: "
    )

    add_heading_2(doc, "B. Desain Dua Lapis Antarmuka Pengguna (Two-Layer UI)")
    add_p(doc,
        "Komponen antarmuka pengguna (EvaluationCard.tsx) sengaja dirancang memiliki dua lapis visual:\n"
        "• Lapis 1 (Rekomendasi Ringkas untuk Petani):\n"
        "  Menampilkan kartu aksi dengan lampu status visual (Sangat Aman / Perlu Waspada / Hindari), rentang jam kerja terbaik (misal: '06.00 - 08.00 WIB'), dan catatan aksi praktis lapangan yang mudah dipahami.\n"
        "• Lapis 2 (Rincian Bukti & Transparansi Sains):\n"
        "  Menampilkan badge integritas bukti transparan: 'Metode terverifikasi (FAO-56)' berwarna hijau, 'Metode belum dikalibrasi (Sentelhas 2008)' berwarna oranye, 'Konvensi tim' berwarna kuning, atau 'Bukti belum cukup' berwarna abu-abu. Menyertakan ID referensi bukti, asumsi awal deplesi Dr0, dan peringatan sensitivitas tanah loam.",
        bold_prefix="Two-Layer UI: "
    )

    add_heading_2(doc, "C. State Management Buku Kas Air (Water Ledger) & Proyeksi 7 Hari")
    add_p(doc,
        "Untuk menjawab kebutuhan proyeksi masa depan tanpa perlu riset baru dari nol:\n"
        "1. Begitu petani mendaftarkan tanamannya di Hari ke-1 (HST 1), aplikasi web menyimpan status deplesi harian di LocalStorage/Database (Water Ledger).\n"
        "2. Setiap hari rumus Dr(t) = Dr(t-1) - P_eff + ETc diperbarui secara otomatis berdasarkan riwayat cuaca riil dan pencatatan siraman petani di tombol 'Tandai selesai hari ini'.\n"
        "3. Untuk memproyeksikan kondisi 7 hari ke depan, engine cukup mengambil data prakiraan 7-hari Open-Meteo dan menjalankan simulasi maju cepat (forward simulation):\n"
        "   - Jika tidak ada hujan dan petani tidak menyiram, sistem memproyeksikan hari ke berapa Dr akan melampaui RAW.\n"
        "   - Di layar petani muncul kartu peringatan dini: 'Perhatian: Tanaman Anda diproyeksikan mengalami stres kekeringan dalam 3 hari ke depan (Kamis). Siapkan pompa air.'",
        bold_prefix="Buku Kas Air: "
    )

    add_heading_2(doc, "D. Peran Asisten Suara & Chatbot RAG 16 Paper")
    add_p(doc,
        "Asisten percakapan AI di dalam web:\n"
        "1. Dilarang keras menghitung formula sendiri atau mengarang dosis obat kimia.\n"
        "2. Murni membaca payload JSON yang dikeluarkan Decision Engine dan menerjemahkannya ke bahasa Indonesia/Sunda santun.\n"
        "3. Jika petani bertanya tentang teori sains di balik rekomendasi, chatbot mengambil konteks dari basis data RAG 16 Paper Ilmiah terverifikasi yang relevan dengan 5 komoditas binaan TaniAdapt.",
        bold_prefix="Chatbot Penjelas: "
    )

    # =========================================================================
    # BAB 7: BUKTI PENGUJIAN OTOMATIS & INTEGRITAS SISTEM
    # =========================================================================
    add_heading_1(doc, "BAB 7: BUKTI PENGUJIAN OTOMATIS & INTEGRITAS SISTEM")

    test_summary_rows = [
        ["1. Pytest Python", "tests/test_engine_schema_and_rules.py", "11 / 11", "0", "PASS (100%)", "Validasi skema Draft 2020-12, if/then trigger rule, Example 36 parity, RH panen, hash parity."],
        ["2. Vitest TypeScript", "taniadapt-web/tests/engine.test.ts", "17 / 17", "0", "PASS (100%)", "Example 18 Brussels 3.88 mm, golden vectors parity, sensitivitas tanah, Example 36, Ajv contract."],
        ["3. Guardrail Templat", "scripts/test_template_guardrails.py", "10 / 10", "0", "PASS (100%)", "Pengujian batas guardrail templat: anti-obat kimia sintetik, anti-tebak yield, penolakan halusinasi."],
        ["4. Next.js Web Build", "npm run build di taniadapt-web", "8 / 8 routes", "0", "PASS (Exit 0)", "Kompilasi sukses Turbopack & TypeScript (/api/advisory, /sumber-dan-batasan, dashboard)."]
    ]
    add_table_data(doc, ["Test Suite", "Berkas Pengujian", "Jumlah Lulus", "Gagal", "Status Akhir", "Cakupan Pengujian"], test_summary_rows, [1.5, 2.0, 0.8, 0.6, 1.0, 1.9])

    add_image_box(doc,
        PROJECT_ROOT / "reports" / "figures" / "10_cross_dataset_synthesis" / "fig26_phase12_edge_case_robustness_matrix.png",
        "FIGUR 4: Matriks Ketahanan Kasus Batas (Stress-Testing Matrix) — Membuktikan Penanganan Anggun 100% (Graceful Degradation Pass Rate 100%) pada Seluruh Skenario Ekstrem."
    )

    add_callout(doc,
        "Dengan arsitektur decoupled ini, TaniAdapt berhasil membuktikan bahwa sistem kecerdasan agrikultur tidak harus mengorbankan kebenaran ilmiah demi kecanggihan semu. Otak biofisik mekanistik FAO-56 memberikan kepastian hukum fisika yang aman bagi petani, sementara antarmuka modern Next.js dan asisten suara menghadirkan kemudahan teknologi mutakhir yang ramah di lapangan.",
        title="KESIMPULAN AKHIR"
    )

    doc.save(OUT_DOCX)
    print(f"Successfully generated Decision Engine Design Dossier at {OUT_DOCX}")


if __name__ == "__main__":
    build_design_doc()
