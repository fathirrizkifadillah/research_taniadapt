import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
MANIFEST_FILE = PROJECT_ROOT / "reports" / "figures" / "figure_manifest.csv"
INDEX_FILE = PROJECT_ROOT / "reports" / "figures" / "INDEX.md"

df = pd.read_csv(MANIFEST_FILE)

nb_titles = {
    "01_AgERA5": "Notebook 01 — AgERA5 Reanalysis Weather (DS01)",
    "02_bangladesh_rice_panel": "Notebook 02 — Bangladesh Rice Panel Literature Transfer Benchmark (DS02)",
    "03_west_java_rice": "Notebook 03 — West Java Rice Productivity & BPS Reconciliation (DS03)",
    "04_indonesia_agroclimatic": "Notebook 04 — Indonesia Agroclimatic Extreme Indicators & Circularity Check (DS04)",
    "05_subang_maize": "Notebook 05 — Maize Productivity, Detrending & 2022 Suspect Flag (DS05)",
    "06_west_java_horticulture": "Notebook 06 — West Java Chili Horticulture & Zero Overlap Audit (DS06)",
    "07_soybean_and_geo": "Notebook 07 — Soybean Productivity & ADM2 geoBoundaries Spatial Relations (DS07)",
    "08_production_and_harvest_area": "Notebook 08 — Harvest Area, Production Volume & Log Decomposition (DS08)",
    "09_climate_covariates_and_chirps": "Notebook 09 — Macro Climate Covariates (ONI, DMI) & CHIRPS Satellite Audit (DS09)",
    "10_cross_dataset_synthesis": "Notebook 10 — Cross-Dataset Synthesis, Panel Inference & Analytical MDE"
}

md_lines = [
    "# Index Visualisasi & Manifest Grafik EDA TaniAdapt (Phase 6)",
    "",
    "Dokumen ini memuat indeks lengkap seluruh **51 visualisasi grafis** yang dihasilkan secara mandiri dan komputasional (tanpa hardcode) dari 10 notebook analitis proyek TaniAdapt Jawa Barat. Seluruh grafik diekspor dalam resolusi tinggi 200 DPI dan tercatat pada [`figure_manifest.csv`](file:///c:/CODING/research_taniAdapt/reports/figures/figure_manifest.csv).",
    "",
    "---",
    ""
]

for nb_name, group in df.groupby("notebook", sort=False):
    title = nb_titles.get(nb_name, nb_name)
    md_lines.append(f"## {title}")
    md_lines.append("")
    md_lines.append("| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |")
    md_lines.append("|---|---|---|---|---|---|---|")
    
    for _, r in group.iterrows():
        rel_path = r["file"].replace("\\", "/")
        file_name = Path(rel_path).name
        fig_id = file_name.split("_")[0].upper()
        clean_cap = str(r["caption"]).replace("\n", " ").replace("|", "/")
        finding = clean_cap.split("Flag: ")[-1] if "Flag: " in clean_cap else clean_cap
        finding = finding.split(".")[0].strip() + "."
        
        md_lines.append(
            f"| **{fig_id}** | [`{file_name}`](file:///{PROJECT_ROOT.as_posix()}/{rel_path}) | {r['periode']} | {r['N_valid']} | {r['dataset']} | `{r['flag_kualitas']}` | {finding} |"
        )
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

INDEX_FILE.write_text("\n".join(md_lines), encoding="utf-8")
print(f"SUCCESS: Generated {INDEX_FILE} with {len(df)} figures registered!")
