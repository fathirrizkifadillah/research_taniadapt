"""Generate Comprehensive Mapping Document: Research (Phase 0-12 & Notebooks 01-10) -> Decision Engine & Formulas.
Location: context/to_fathir/TaniAdapt_Pemetaan_Riset_ke_Decision_Engine.docx
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
OUT_DOCX = PROJECT_ROOT / "context" / "to_fathir" / "TaniAdapt_Pemetaan_Riset_ke_Decision_Engine.docx"
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


def build_mapping_doc():
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
    r_title = p_title.add_run("TANIADAPT: PEMETAAN LENGKAP HASIL RISET KE DECISION ENGINE")
    r_title.bold = True
    r_title.font.name = "Aptos Display"
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = RGBColor(27, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("Penelusuran Jejak Ilmiah Lengkap: Bagaimana Setiap Rumus, Aturan, Ambang Batas,\ndan Perlakuan 5 Komoditas Diturunkan Langsung dari Phase 0–12 dan Notebook 01–10")
    r_sub.font.name = "Aptos"
    r_sub.font.size = Pt(10.5)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(44, 82, 130)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Disusun Khusus Untuk: Fathir Rizki Fadillah | Traceability: Phase 0 s/d Phase 13 | Single Source of Truth: rules.json v2.4")
    r_meta.font.name = "Aptos"
    r_meta.font.size = Pt(9.0)
    r_meta.bold = True
    r_meta.font.color.rgb = RGBColor(100, 100, 100)

    # =========================================================================
    # BAB 1: PRINSIP PENELUSURAN ILMIAH (TRACEABILITY MATRIX)
    # =========================================================================
    add_heading_1(doc, "BAB 1: PRINSIP PENELUSURAN ILMIAH (TRACEABILITY MATRIX)")
    
    add_p(doc,
        "Di dalam rekayasa perangkat lunak mission-critical dan riset agrikultur presisi, tidak boleh ada angka 'ajaib' (magic numbers) yang muncul tiba-tiba di dalam kode aplikasi tanpa dasar pengujian. Setiap ambang batas cuaca, rumus fisika air, dan aturan operasional di TaniAdapt memiliki rantai pembuktian yang dapat dilacak (traceable) ke fase riset dan notebook asalnya.",
        bold_prefix="Mengapa Penelusuran Ini Wajib? "
    )

    add_callout(doc,
        "Prinsip TaniAdapt: 'Evidence → Finding → Agricultural Interpretation → Model → Decision Logic → Action'.\n"
        "Jika sebuah parameter tidak memiliki bukti kuat dalam data lokal Jawa Barat atau literatur primer, sistem menolak berpura-pura tahu dan mengunci statusnya pada 'evidence_insufficient' atau 'CONVENTION_PENDING'. Ini adalah pembeda terbesar TaniAdapt dari aplikasi AI generik yang gemar berhalusinasi.",
        title="RANTAI PEMBUKTIAN KANONIK"
    )

    # =========================================================================
    # BAB 2: PEMETAAN 5 KOMODITAS KE FASE RISET & NOTEBOOK
    # =========================================================================
    add_heading_1(doc, "BAB 2: PEMETAAN 5 KOMODITAS KE FASE RISET & NOTEBOOK")
    
    add_p(doc,
        "Berikut adalah tabel komparasi pelacakan asal-usul mengapa kelima komoditas memiliki status dan perlakuan yang berbeda di Decision Engine:",
        bold_prefix="Tabel Pelacakan Asal Komoditas: "
    )

    crop_mapping_rows = [
        ["1. Padi Sawah", "Phase 4 (Blocker A1, B1) & Phase 5\nNotebook 03 & Notebook 10", "Lonjakan data 2019 (+21.8%) adalah artefak pelaporan. Patahan BPS KSA 2018 membatasi panel ke T=3. Padi sawah di Jabar ditanam tergenang air (ponded).", "MODUL AIR: INSUFFICIENT (sawah tergenang, deplesi tanah tak jenuh tidak berlaku).\nMODUL LAIN: Semprot, pupuk, dan panen AKTIF 100%."],
        ["2. Jagung Pipil", "Phase 4 (A3, A4, A5), Phase 8, 9, 10\nNotebook 05 & Notebook 10 (Bagian 10H, 10I, 10J)", "Imputasi dinas 2022 (75.70 ku/ha kembar di 13 kab) dibuang. Uji ML LOYO CV R² ≈ 0 (ML runtuh). MDE ±0.1444.", "MODUL AIR: AKTIF PENUH berbasis FAO-56 (Zr=1.0 m, p=0.55, Kc=0.30->1.20->0.35).\nSELURUH 5 TINDAKAN: Aktif 100%."],
        ["3. Kedelai", "Phase 4 (A5), Phase 5, 8, 10\nNotebook 07 & Notebook 10 (Bagian 10J)", "Imputasi 2022 dibuang. 17 sentra aktif ex-ante di Jabar (17 sel AgERA5 unik, N=112 valid pasca filter MAD-z).", "MODUL AIR: AKTIF PENUH berbasis FAO-56 (Zr=0.8 m, p=0.50, Kc=0.40->1.15->0.50).\nSELURUH 5 TINDAKAN: Aktif 100%."],
        ["4. Cabai Merah & Cabai Rawit", "Phase 4 (A6), Phase 5, Phase 13 (M2)\nNotebook 06 (Hortikultura)", "Ketiadaan data ground truth OPT lokal di Jabar. FAO-56 Tabel 12 tidak memuat cabai tropis (hanya ada sweet pepper/paprika subtropis).", "MODUL AIR: UNVERIFIED (sistem menolak ekstrapolasi liar dari paprika).\nMODUL LAIN: Sangat aktif untuk mitigasi jamur LWD (RH>=90%), semprot, wiwil tunas air, dan panen."],
        ["5. Tomat", "Phase 4 (A6), Phase 5, Phase 10\nNotebook 06 & Notebook 10 (Bagian 10J)", "Koefisien Kc terdaftar di FAO-56 Tabel 12 (0.60->1.15->0.80). Butuh pemangkasan tunas air dan mulsa.", "MODUL AIR: AKTIF PENUH (Zr=0.7 m, p=0.40, Kc=0.80).\nMODUL OPT: Scouting LWD jamur aktif, wiwil aktif."]
    ]
    add_table_data(doc, ["Komoditas", "Asal Riset (Phase & Notebook)", "Temuan Empiris & Alasan Ilmiah", "Implementasi Nyata di Web Engine"], crop_mapping_rows, [1.3, 1.6, 2.0, 1.8])

    add_heading_2(doc, "Penjelasan Mendalam: Mengapa Cabai Tetap Dipakai dan Mengapa Cabai Merah & Rawit Dibedakan?")
    add_p(doc,
        "1. Mengapa Cabai Tetap Dipakai di Web? Meskipun kartu siramnya berstatus 'Bukti Belum Cukup' (karena ketiadaan nilai Kc terverifikasi di buku FAO-56), cabai adalah komoditas dengan nilai ekonomi tertinggi di Jawa Barat yang paling rentan terhadap cuaca harian. Petani cabai sangat membutuhkan Decision Engine untuk: (a) memandu jam semprot aman agar pestisida tidak hanyut hujan, (b) memperingatkan kondisi kondusif spora patek/antraknosa (LWD saat RH >= 90%), (c) memandu waktu perempelan tunas air (wiwil), dan (d) mencegah pemetikan buah saat basah kuyup hujan.\n"
        "2. Pembedaan Cabai Merah Besar vs Cabai Rawit:\n"
        "   - Cabai Merah Besar (Capsicum annuum): Tajuk kanopi rimbun, kelembapan mikro daun bertahan lebih lama di pagi hari (risiko antraknosa Colletotrichum lebih tinggi). Pemanenan serentak per 7–10 hari sekali.\n"
        "   - Cabai Rawit (Capsicum frutescens): Tajuk lebih kompak, daun lebih kecil, siklus hidup panjang (6–12 bulan), petik bertahap hijau/merah. Sangat rentan mengalami kerontokan bunga muda jika terpapar radiasi terik siang > 500 W/m² bersamaan dengan VPD tinggi > 15 hPa.",
        bold_prefix="Cabai di Decision Engine: "
    )

    # =========================================================================
    # BAB 3: PEMETAAN SELURUH FORMULA KE FASE RISET & NOTEBOOK
    # =========================================================================
    add_heading_1(doc, "BAB 3: PEMETAAN SELURUH FORMULA KE FASE RISET & NOTEBOOK")

    add_heading_2(doc, "1. Formula Evapotranspirasi Acuan Penman-Monteith (ET0)")
    add_p(doc,
        "• Asal Riset: Phase 2 (Literature Review) & Phase 10 (Evidence to Risk Model), diuji di Notebook 01 & Notebook 10.\n"
        "• Dasar Literatur: Allen et al. (1998), FAO Irrigation and Drainage Paper 56, Bab 4, Persamaan 6 (Eq. 6, p. 65).\n"
        "• Validasi Independen: Diuji terhadap Contoh 18 Bab 4 FAO-56 (Brussels/Uccle benchmark: target 3.88 mm/hari, hasil komputasi 3.877 mm/hari, status PASS).\n"
        "• Implementasi Kode: Diimplementasikan dalam fungsi murni di `src/lib/engine/fao56.ts`.",
        bold_prefix="Rantai Pembuktian ET0: "
    )
    add_formula_box(doc,
        "ET0 = [ 0.408 * Δ * (Rn - G) + γ * (900 / (Tmean + 273)) * u2 * (es - ea) ] / [ Δ + γ * (1 + 0.34 * u2) ]",
        label="FAO-56 Bab 4 Eq. 6 (Implementasi fao56.ts)"
    )

    add_heading_2(doc, "2. Formula Elevasi DEM SRTM & Tekanan Udara Barometrik")
    add_p(doc,
        "• Asal Riset: Phase 3 (Dataset Discovery) & Phase 4 (Blocker A8 Geospasial), diuji di Notebook 07 (EDA 7.5 Profil Elevasi SRTM).\n"
        "• Temuan Empiris: Centroid 27 kabupaten/kota Jawa Barat memiliki elevasi bervariasi dari 11 meter (pantai Pantura) hingga 1.250 meter (pegunungan Lembang/Garut). Offset jarak centroid ke grid cuaca terdekat rata-rata 5.80 km (Haversine).\n"
        "• Implementasi Kode: Hasil EDA disimpan di `data/processed/lookup_kab_cell_elev.csv`. Angka elevasi z dimasukkan ke rumus tekanan atmosfer FAO-56 Eq. 7 di `fao56.ts`:",
        bold_prefix="Rantai Pembuktian Elevasi: "
    )
    add_formula_box(doc,
        "P = 101.3 * [ (293 - 0.0065 * z) / 293 ]^5.26  (z = elevasi DEM SRTM, meter)\n"
        "γ = 0.000665 * P  (Konstanta psikrometrik atmosfer)",
        label="FAO-56 Bab 3 Eq. 7 & Eq. 8 (Fusi Geospasial Notebook 07)"
    )

    add_heading_2(doc, "3. Formula Koefisien Tanaman Dinamis Kc(t)")
    add_p(doc,
        "• Asal Riset: Phase 5 (Crop Selection) & Phase 10, diuji di Notebook 10 (Bagian 10J).\n"
        "• Dasar Literatur: FAO-56 Bab 6, Tabel 11 (panjang fase fenologi) dan Tabel 12 (Kc awal, tengah, dan akhir).\n"
        "• Implementasi Kode: Diimplementasikan di `src/lib/engine/kc.ts` menggunakan interpolasi linear dinamis berdasarkan Hari Setelah Tanam (HST / DAP).",
        bold_prefix="Rantai Pembuktian Kc(t): "
    )

    add_heading_2(doc, "4. Formula Total Available Water (TAW) & Readily Available Water (RAW)")
    add_p(doc,
        "• Asal Riset: Phase 10 (Risk Model) & Phase 13 Milestone M1/M2.\n"
        "• Dasar Literatur: FAO-56 Bab 8, Persamaan 82 (TAW) dan Persamaan 83 (RAW), terkonfirmasi definitif dari Contoh 36 FAO-56.\n"
        "• Uji Paritas Independen: Teruji lulus pada 3 tekstur tanah (Loamy Sand, Silt, Silty Clay) dengan toleransi <= 1 mm di Vitest (`tests/engine.test.ts`).\n"
        "• Implementasi Kode: Diimplementasikan di `src/lib/engine/waterBalance.ts`.",
        bold_prefix="Rantai Pembuktian TAW & RAW: "
    )
    add_formula_box(doc,
        "TAW = 1000 * (θ_FC - θ_WP) * Zr   [FAO-56 Bab 8, Eq. 82]\n"
        "RAW = p * TAW                      [FAO-56 Bab 8, Eq. 83]",
        label="FAO-56 Bab 8 Eq. 82 & 83 (Implementasi waterBalance.ts)"
    )

    add_heading_2(doc, "5. Formula Neraca Deplesi Air Harian Dr(t)")
    add_p(doc,
        "• Asal Riset: Phase 10 (Risk Model), Notebook 10 (Bagian 10J Cell 62–68).\n"
        "• Dasar Literatur: FAO-56 Bab 8, Persamaan 85 (Eq. 85).\n"
        "• Logika Keputusan: Tanaman hanya mengalami cekaman kekurangan air jika Dr(t) > RAW. Jika Dr(t) <= RAW, air tanah masih mencukupi sehingga petani disarankan hemat air pompa solar.\n"
        "• Implementasi Kode: Diimplementasikan di fungsi `updateDailyDepletion()` dan `evaluateWaterStress()` pada `waterBalance.ts`.",
        bold_prefix="Rantai Pembuktian Dr(t): "
    )
    add_formula_box(doc,
        "Dr(t) = Dr(t-1) - P_eff(t) + ETc(t)   [FAO-56 Bab 8, Eq. 85]\n"
        "Batasan Fisis: 0 <= Dr(t) <= TAW (kelebihan air dianggap perkolasi dalam)",
        label="FAO-56 Bab 8 Eq. 85 (Neraca Deplesi Harian)"
    )

    add_heading_2(doc, "6. Formula Uji Sensitivitas Tanah Loam (130 vs 180 mm/m)")
    add_p(doc,
        "• Asal Riset: Phase 13 Milestone M1 & M2 (Kepatuhan Audit Rigor Claude).\n"
        "• Dasar Ilmiah: FAO-56 Bab 7, Tabel 19 menyatakan kapasitas simpan air tanah loam memiliki rentang 130–180 mm/m. Mengasumsikan nilai tunggal 150 mm/m tanpa uji sensitivitas adalah cacat metodologis.\n"
        "• Implementasi Kode: Engine mengevaluasi status keputusan irigasi pada kedua batas ekstrim (TAW = 130 mm/m dan TAW = 180 mm/m). Jika status berubah (misal: aman di 180 mm/m tapi stres di 130 mm/m), sistem otomatis menyalakan flag `sensitif_terhadap_asumsi_tanah = true` di JSON payload.",
        bold_prefix="Rantai Pembuktian Sensitivitas: "
    )

    # =========================================================================
    # BAB 4: PEMETAAN ATURAN OPERASIONAL & AMBANG BATAS CUACA
    # =========================================================================
    add_heading_1(doc, "BAB 4: PEMETAAN ATURAN OPERASIONAL & AMBANG BATAS CUACA")

    rule_trace_rows = [
        ["RULE_WATER_FAO56_DEPLETION", "Dr > RAW (stres abiotik)", "Irigasi Darurat (Sangat Dianjurkan)", "Phase 10 & 11\nNotebook 10 (10J, 10K)", "Satu-satunya aturan irigasi aktif berstatus VERIFIED_METHOD. Menggantikan aturan empiris lama CWB -25/-50 mm yang dipensiunkan."],
        ["RULE_IRRIG_RAIN_ACTIVE", "Hujan aktif >= 3.0 mm", "Dilarang Siram (Hindari)", "Phase 11\nNotebook 10 (10K)", "Circuit breaker operasional lapangan: membatalkan penyiraman karena kanopi dan tanah sudah basah."],
        ["RULE_IRRIG_SRAD_VPD", "Radiasi > 500 W/m² atau VPD > 15 hPa", "Waspada Siram Siang", "Phase 8 & 11\nNotebook 01 & 10", "Mencegah penguapan kilat air siraman di tengah terik siang dan mencegah efek lensa air membakar daun."],
        ["RULE_SPRAY_WIND_BOUNDS", "< 3 km/j (inversi fajar)\n3–12 km/j (aman ideal)\n12–15 km/j (transisi)\n> 15 km/j (bahaya drift)", "Semprot Pestisida & Fungisida", "Phase 11 & 12\nNotebook 10 (10K, 10L)", "Menutup seluruh celah kecepatan angin. <3 km/j partikel racun terperangkap dekat tanah; >15 km/j spray drift melayang ke pemukiman."],
        ["RULE_FERT_RAIN_12H", "Prakiraan hujan 12h >= 8.0 mm", "Dilarang Pupuk (Hindari)", "Phase 11\nNotebook 10 (10K)", "Mencegah butiran pupuk larut hanyut terbawa aliran permukaan air hujan (surface runoff)."],
        ["RULE_HARVEST_RH_BOUNDS", "<= 75% (Aman kering)\n75–85% (Transisi waspada)\n> 85% (Bahaya pembusukan)", "Pemanenan Pangan (Jagung/Kedelai)", "Phase 11 & Phase 13 (M2)\nNotebook 10", "Memastikan kadar air biji/polong rendah saat panen; kelembapan 75-85% memicu status WARN untuk segera menjemur hasil."],
        ["RULE_PRUNE_RAIN_8H", "Prakiraan hujan 8h >= 2.0 mm", "Dilarang Pangkas (Hindari)", "Phase 11 & Phase 13\nNotebook 10", "Sanitasi perempelan tunas air (wiwil) hortikultura cabai & tomat: luka pangkas basah rawan infeksi jamur."],
        ["RULE_OPT_LWD_HOURLY_RH90", "Jumlah jam per hari dengan RH >= 90% >= 10 jam", "Pengamatan Hama (Scouting OPT)", "Phase 2 & Phase 13 (M2)\nPaper Sentelhas 2008", "Indikator Leaf Wetness Duration (LWD). Berstatus METHOD_UNCALIBRATED: dilarang memicu status level atas."]
    ]
    add_table_data(doc, ["ID Aturan di rules.json", "Ambang Batas Agrometeorologi", "Tindakan & Status", "Asal Riset (Phase & NB)", "Alasan Ilmiah & Catatan Khusus"], rule_trace_rows, [1.5, 1.3, 1.2, 1.1, 1.9])

    # =========================================================================
    # BAB 5: PANDUAN PENGEMBANGAN UNTUK REKAN TIM WEB (FRONTEND GUIDE)
    # =========================================================================
    add_heading_1(doc, "BAB 5: PANDUAN PENGEMBANGAN UNTUK REKAN TIM WEB (FRONTEND GUIDE)")

    add_p(doc,
        "Bagian ini disusun khusus agar rekan tim pengembang antarmuka web (Frontend Developer) memahami bagaimana cara mengintegrasikan hasil riset ke dalam komponen UI Next.js di repositori taniadapt-web:",
        bold_prefix="Tujuan Panduan Tim: "
    )

    add_heading_2(doc, "1. Memanggil Route Handler Backend (/api/advisory)")
    add_p(doc,
        "Frontend cukup mengirimkan request HTTP POST ke `/api/advisory` tanpa perlu mengimpor atau menghitung rumus fisika di client. Contoh payload request:",
        bold_prefix="Payload Request: "
    )
    add_formula_box(doc,
        "POST /api/advisory\n"
        "Content-Type: application/json\n\n"
        "{\n"
        '  "crop": "jagung",\n'
        '  "latitude": -6.4830,\n'
        '  "longitude": 107.7322,\n'
        '  "kabkota": "KABUPATEN SUBANG",\n'
        '  "planting_date": "2026-09-01",\n'
        '  "panen_kering": true,\n'
        '  "initial_depletion_dr0_mm": 0.0\n'
        "}",
        label="Format Request Client ke Route Handler Next.js"
    )

    add_heading_2(doc, "2. Memahami Respons JSON & Merender UI Dua Lapis")
    add_p(doc,
        "Backend mengembalikan objek JSON yang sudah divalidasi ketat oleh Ajv Draft 2020-12. Frontend merender respons ini ke dua lapis visual:\n"
        "• Lapis 1 (Visual Ringkas untuk Petani):\n"
        "  - Ambil array `actions[]`: render 5 kartu aksi dengan lampu indikator warna (SAFE = Hijau, WARN = Kuning, DANGER = Merah, INSUFFICIENT = Abu-abu).\n"
        "  - Tampilkan `bestWindow` (misal: '06.00 - 08.00 WIB') dan `reason` sebagai catatan aksi lapangan praktis.\n"
        "  - Ambil array `hourly[]`: render garis waktu 13 jam (06.00–18.00 WIB).\n"
        "• Lapis 2 (Transparansi Sains & Sumber):\n"
        "  - Tampilkan badge status aturan (`rule_status`): 'Metode terverifikasi (FAO-56)' untuk irigasi, 'Konvensi tim' untuk semprot/pupuk, 'Metode belum dikalibrasi' untuk OPT cabai/tomat, dan 'Bukti belum cukup' untuk air padi/cabai.\n"
        "  - Jika `sensitif_terhadap_asumsi_tanah === true`, tampilkan kotak peringatan kuning: '⚠️ Rekomendasi sensitif terhadap variasi rentang jenis tanah loam'.",
        bold_prefix="Rendering Komponen React: "
    )

    add_heading_2(doc, "3. Menangani Kasus Khusus Komoditas (Padi & Cabai)")
    add_p(doc,
        "• Jika user memilih PADI: Kartu siram otomatis berstatus 'Bukti Belum Cukup' (karena sawah tergenang). Kartu semprot, pupuk, dan panen tetap berfungsi normal.\n"
        "• Jika user memilih CABAI (Merah atau Rawit): Kartu siram otomatis berstatus 'Bukti Belum Cukup' (karena Kc cabai tropis unverified). Namun kartu 'Pengamatan Hama (Scouting OPT)' aktif memantau jamur patek (LWD), kartu semprot aktif memandu angin, kartu 'Pangkas/Wiwil' aktif memandu sanitasi tunas air, dan kartu panen aktif mencegah petik saat basah hujan.",
        bold_prefix="Logika Khusus Komoditas: "
    )

    add_heading_2(doc, "4. State Management Buku Kas Air (Water Ledger) & Logbook")
    add_p(doc,
        "• Di frontend, tombol 'Tandai selesai hari ini' menyimpan catatan aksi petani ke LocalStorage/Database (`lib/storage.ts`).\n"
        "• Ketika petani mencatat telah menyiram hari ini, nilai deplesi tanah Dr0 untuk hari berikutnya direset kembali ke kapasitas lapang (Dr0 = 0 mm).\n"
        "• Jika petani mencatat telah memupuk hari ini, frontend mengunci kartu pupuk selama 14 hari ke depan (*fertilizer lockout*) untuk mencegah overdosis pupuk kimia.",
        bold_prefix="Manajemen Logbook Tani: "
    )

    # Summary Callout
    add_callout(doc,
        "Dokumen ini membuktikan bahwa TaniAdapt adalah karya rekayasa perangkat lunak yang utuh: setiap baris kode di frontend dan backend terikat pada hukum fisika agrometeorologi yang telah diuji secara empiris sepanjang Phase 0 hingga Phase 13. Seluruh tim pengembang kini dapat bekerja sama dengan visi ilmiah yang seragam, jelas, dan dapat dipertanggungjawabkan.",
        title="PENUTUP CETAK BIRU"
    )

    doc.save(OUT_DOCX)
    print(f"Successfully generated Research-to-Engine Mapping Dossier at {OUT_DOCX}")


if __name__ == "__main__":
    build_mapping_doc()
