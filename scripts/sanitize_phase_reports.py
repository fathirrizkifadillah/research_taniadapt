"""Script to sanitize all phase reports and master documents according to strict honest-status rules.

Enforces:
1. Replaces 'RATIFIED' with 'PENDING_USER_RATIFICATION'.
2. Removes/replaces '0% halusinasi', 'bebas halusinasi'.
3. Replaces 'terkalibrasi' with 'terkonvensi, belum dikalibrasi terhadap data lapangan'.
4. Removes 'tanpa celah'.
5. Replaces 'konfirmasi kuat' / 'mengonfirmasi secara kuat'.
6. Updates Phase 12 description to 'preliminary face-validity check (n=3 peristiwa)'.
7. Updates Phase 9 description to 'LOYO CV R2≈0: tidak ada bukti prediktif dalam data ini; catat bahwa year FE tidak bisa diestimasi untuk tahun yang ditahan sehingga R2 negatif sebagian akibat desain evaluasi'.
8. Updates Phase 1 to 'hipotesis didokumentasikan (post-data-access documentation, commit 4629ad9 pada 2026-10-11 vs akses data 2026-10-05/06)'.
9. Removes 'BPS Padi KSA 2018–2024' from used datasets.
10. Standardizes spatial offset to '5.80 km (formula Haversine)'.
"""
from __future__ import annotations

import re
from pathlib import Path

PHASE_DIR = Path("reports/phase")
DOCS_DIR = Path("docs")

def sanitize_text(text: str) -> str:
    # 1. Status replacement
    text = text.replace("Status: RATIFIED", "Status: PENDING_USER_RATIFICATION")
    text = text.replace("**Status**: RATIFIED", "**Status**: PENDING_USER_RATIFICATION")
    text = text.replace("`RATIFIED`", "`PENDING_USER_RATIFICATION`")
    text = text.replace("RATIFIED (Locked post-audit canonical decision)", "PENDING_USER_RATIFICATION (Menunggu Ratifikasi Pengguna Manusia)")

    # 2. Hallucination claims
    text = text.replace("0% halusinasi", "penanganan kasus batas terdefinisi (graceful degradation)")
    text = text.replace("0.0% halusinasi", "penanganan kasus batas terdefinisi")
    text = text.replace("0.0% tingkat halusinasi", "penanganan kasus batas terdefinisi")
    text = text.replace("0.0% Hallucination Rate", "Graceful Degradation Pass Rate 100%")
    text = text.replace("bebas halusinasi", "tanpa mengarang (grounded)")
    text = text.replace("Bebas Halusinasi", "Grounded")
    text = text.replace("tanpa celah", "secara terstruktur")

    # 3. Terkalibrasi -> terkonvensi, belum dikalibrasi terhadap data lapangan
    # Only replace when referring to the heuristic rules/thresholds, not verified FAO56
    text = text.replace("model risiko terkalibrasi", "model risiko terkonvensi (belum dikalibrasi terhadap data lapangan)")
    text = text.replace("Model Risiko Terkalibrasi", "Model Risiko Terkonvensi (Belum Dikalibrasi Terhadap Data Lapangan)")
    text = text.replace("Ambang Terkalibrasi", "Ambang Terkonvensi (Belum Dikalibrasi Terhadap Data Lapangan)")
    text = text.replace("ambang terkalibrasi", "ambang terkonvensi (belum dikalibrasi terhadap data lapangan)")
    text = text.replace("terkalibrasi", "terkonvensi, belum dikalibrasi terhadap data lapangan")

    # 4. Confirmation / proof phrases
    text = text.replace("mengonfirmasi secara kuat", "menunjukkan secara empiris")
    text = text.replace("mengonfirmasi secara mutlak", "menunjukkan secara konsisten")
    text = text.replace("konfirmasi kuat", "indikasi empiris")

    # 5. Phase 12 description
    text = text.replace("Phase 12: Validation & Stress-Testing", "Phase 12: Preliminary Face-Validity Check (n=3 peristiwa)")
    text = text.replace("Phase 12: Validation", "Phase 12: Preliminary Face-Validity Check (n=3 peristiwa)")
    text = text.replace("Phase 12 — Validation", "Phase 12 — Preliminary Face-Validity Check (n=3 peristiwa)")

    # 6. Phase 9 description
    phase9_honest = "LOYO CV R2≈0: tidak ada bukti prediktif dalam data ini; catat bahwa year FE tidak bisa diestimasi untuk tahun yang ditahan sehingga R2 negatif sebagian akibat desain evaluasi"
    if "Phase 9: ML Baseline Benchmarking" in text:
        text = text.replace("Benchmark 6 model via LOYO CV, konfirmasi keruntuhan generalisasi ML out-of-sample.", f"Benchmark 6 model via LOYO CV. {phase9_honest}.")
        text = text.replace("Benchmark 6 model via LOYO CV membuktikan keruntuhan generalisasi ML out-of-sample ($R^2 \\approx 0$).", f"Benchmark 6 model via LOYO CV. {phase9_honest}.")

    # 7. Phase 1 description
    phase1_honest = "hipotesis didokumentasikan (post-data-access documentation, commit 4629ad9 pada 2026-10-11 vs akses data awal 2026-10-05/06, bukan pra-registrasi sebelum akses data)"
    text = text.replace("prapendaftaran transparan 11 hipotesis fenologi (*anti-p-hacking*)", f"{phase1_honest}")
    text = text.replace("prapendaftaran transparan 11 hipotesis fenologi (anti-p-hacking)", f"{phase1_honest}")
    text = text.replace("prapendaftaran transparan 11 hipotesis fenologis anti-p-hacking", f"{phase1_honest}")

    # 8. Remove BPS Padi KSA 2018-2024 from used datasets
    text = text.replace(", BPS Padi KSA 2018–2024", "")
    text = text.replace("BPS Padi KSA 2018–2024, ", "")
    text = text.replace("BPS Padi KSA (2018–2024), ", "")
    text = text.replace("BPS Padi KSA 2018–2024", "BPS Padi KSA (tidak tersedia / tidak dipakai)")

    # 9. Spatial offset 5.2 vs 5.80 km
    text = text.replace("5.2 km", "5.80 km (formula Haversine)")
    text = text.replace("5.8 km", "5.80 km (formula Haversine)")

    return text


def main() -> None:
    for f in list(PHASE_DIR.glob("*.md")) + list(DOCS_DIR.glob("*.md")):
        orig = f.read_text(encoding="utf-8")
        sanitized = sanitize_text(orig)
        if orig != sanitized:
            f.write_text(sanitized, encoding="utf-8")
            print(f"Sanitized: {f.as_posix()}")

    print("Sanitization pass complete.")


if __name__ == "__main__":
    main()
