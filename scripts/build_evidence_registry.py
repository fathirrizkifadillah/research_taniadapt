"""Build the auditable literature and extension evidence registry.

Rows marked VERIFIED were checked by opening the linked primary/official source.
Rows with a missing, inaccessible, or insufficiently specific source retain no
operational parameter and are deliberately excluded from engine rules.
"""
from __future__ import annotations

import csv
from pathlib import Path

from project_paths import PROJECT_ROOT

OUT = PROJECT_ROOT / "reports" / "dataset_audit" / "evidence_registry.csv"
FIELDS = ["id", "komoditas", "mekanisme", "variabel", "jendela_fase", "arah_efek",
          "parameter/ambang (jika ada)", "sitasi_lengkap", "DOI/URL", "lokasi_studi",
          "kesesuaian_ke_Jabar", "kekuatan_bukti", "status_verifikasi", "kutipan_halaman"]
FAO = "Allen, R.G., Pereira, L.S., Raes, D. & Smith, M. (1998). Crop evapotranspiration—Guidelines for computing crop water requirements. FAO Irrigation and Drainage Paper 56."
FAO_URL = "https://www.fao.org/4/X0490E/x0490e0b.htm"

ROWS = [
    ["FAO56_ET0_PM", "all", "reference evapotranspiration", "ET0", "daily", "reference only", "FAO-56 Penman–Monteith equation; implementation validation required", FAO, "https://www.fao.org/4/X0490E/X0490E00.htm", "FAO standard", "method transferable; inputs and assumptions must be checked", "authoritative method", "VERIFIED", "FAO-56, Chapter 2/Equation 6; full document p. 65"],
    ["FAO56_KC_RICE", "padi", "crop water requirement", "Kc", "initial/mid/end", "ETc = Kc × ET0", "Kc_ini=1.05; Kc_mid=1.20; Kc_end=0.90–0.60", FAO, FAO_URL, "standard non-stressed, well-managed subhumid condition", "transferable only as reference; local water management may differ", "authoritative reference table", "VERIFIED", "Table 12, full document p. 110"],
    ["FAO56_KC_MAIZE", "jagung", "crop water requirement", "Kc", "initial/mid/end", "ETc = Kc × ET0", "field maize: Kc_ini=0.30; Kc_mid=1.20; Kc_end=0.60–0.35", FAO, FAO_URL, "standard non-stressed, well-managed subhumid condition", "transferable only as reference; crop type and management must match", "authoritative reference table", "VERIFIED", "Table 12, full document p. 110"],
    ["FAO56_KC_TOMATO", "tomat", "crop water requirement", "Kc", "initial/mid/end", "ETc = Kc × ET0", "Kc_ini=0.60; Kc_mid=1.15; Kc_end=0.70–0.90", FAO, FAO_URL, "standard non-stressed, well-managed subhumid condition", "transferable only as reference; local management may differ", "authoritative reference table", "VERIFIED", "Table 12, full document p. 110"],
    ["FAO56_KC_SOY", "kedelai", "crop water requirement", "Kc", "initial/mid/end", "ETc = Kc × ET0", "soybeans: Kc_ini=0.40; Kc_mid=1.15; Kc_end=0.50", FAO, FAO_URL, "standard non-stressed, well-managed subhumid condition", "transferable only as reference; crop type and management must match", "authoritative reference table", "VERIFIED", "Table 12, full document p. 110"],
    ["RICE_TEMP_PHASES", "padi", "thermal development/stress", "base/optimum/maximum temperature", "per growth phase", "PENDING", "", "No accessible, crop- and phase-specific primary source verified in this pass.", "", "", "not established", "none usable", "UNVERIFIED", ""],
    ["MAIZE_TEMP_PHASES", "jagung", "thermal development/stress", "base/optimum/maximum temperature", "per growth phase", "PENDING", "", "No accessible, crop- and phase-specific primary source verified in this pass.", "", "", "not established", "none usable", "UNVERIFIED", ""],
    ["SOY_TEMP_PHASES", "kedelai", "thermal development/stress", "base/optimum/maximum temperature", "per growth phase", "PENDING", "", "No accessible, crop- and phase-specific primary source verified in this pass.", "", "", "not established", "none usable", "UNVERIFIED", ""],
    ["CHILI_WATER", "cabai", "crop water requirement", "Kc / water requirement", "per phase", "PENDING", "", "Bell pepper is not automatically treated as Indonesian cabai; crop-specific source still required.", FAO_URL, "FAO standard", "not established", "none usable", "UNVERIFIED", "Table 12 was opened but does not establish a cabai rule here"],
    ["CHILI_ANTHRACNOSE_WEATHER", "cabai", "antraknosa", "leaf-wetness/RH/temperature proxy", "daily window", "PENDING", "", "No accessible paper defining a verified weather proxy for this engine in this pass.", "", "", "not established", "none usable", "CANNOT_OPEN", ""],
    ["TOMATO_LATE_BLIGHT_WEATHER", "tomat", "hawar daun / Phytophthora infestans", "leaf-wetness/RH/temperature proxy", "daily window", "PENDING", "", "No accessible paper defining a verified weather proxy for this engine in this pass.", "", "", "not established", "none usable", "CANNOT_OPEN", ""],
    ["ACT_DRAINAGE_CHECK_SOURCE", "all", "agronomic action", "ACT_DRAINAGE_CHECK", "event response", "PENDING", "", "Official extension source must be selected and opened before activation.", "", "Indonesia/Jabar required", "not established", "none usable", "CANNOT_OPEN", ""],
    ["ACT_WATER_CONSERVATION_SOURCE", "all", "agronomic action", "ACT_WATER_CONSERVATION", "event response", "PENDING", "", "Official extension source must be selected and opened before activation.", "", "Indonesia/Jabar required", "not established", "none usable", "CANNOT_OPEN", ""],
    ["ACT_CANOPY_VENTILATION_SOURCE", "cabai|tomat", "agronomic action", "ACT_CANOPY_VENTILATION", "event response", "PENDING", "", "Official extension source must be selected and opened before activation.", "", "Indonesia/Jabar required", "not established", "none usable", "CANNOT_OPEN", ""],
    ["ACT_SCOUT_FIELD_SYMPTOMS_SOURCE", "cabai|tomat", "agronomic action", "ACT_SCOUT_FIELD_SYMPTOMS", "event response", "PENDING", "", "Official extension source must be selected and opened before activation.", "", "Indonesia/Jabar required", "not established", "none usable", "CANNOT_OPEN", ""],
    ["ACT_FUNGICIDE_REVIEW_SOURCE", "cabai|tomat", "agronomic action", "ACT_FUNGICIDE_REVIEW", "event response", "PENDING", "", "Official extension source must be selected and opened before activation.", "", "Indonesia/Jabar required", "not established", "none usable", "CANNOT_OPEN", ""],
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        writer.writerows(ROWS)
    print(f"Wrote {len(ROWS)} evidence records to {OUT}")


if __name__ == "__main__":
    main()
