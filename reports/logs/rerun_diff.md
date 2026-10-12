# Phase 4 Rerun Difference Log

**Date:** 2026-10-12  
**Command:** `scripts/run_phase4_pipeline.py`  
**Credential handling:** No credential file, token, or API key was read, printed, or stored.

## Reproduction environment

| Check | Result |
|---|---|
| Fresh `.venv_phase4_clean` created from `requirements.txt` | TIDAK BISA selesai; first installation was interrupted before packages were written. |
| Clean-environment rerun | TIDAK BISA; the incomplete environment raised `ModuleNotFoundError: numpy`. |
| Local project Python 3.11 rerun | DONE; A2, A3, A4, and canonical result refresh completed. |
| Raw data | Not committed or modified. |

The failed clean-environment installation is retained as a reproducibility issue. The successful local rerun does not substitute for a successful clean-environment reproduction.

## Result differences versus the previous canonical record

| Artifact / metric | Previous record | Rerun / current record | Disposition |
|---|---:|---:|---|
| DS09 matched CHIRPS unit-months | 972 | 936 | Corrected from raw matched data. Indramayu has 24 months (two benchmark years) and Depok has 12 months (one benchmark year). |
| CHIRPS N by benchmark year | not stated | 2016=312; 2020=312; 2024=312 | Added. |
| CHIRPS units with valid per-unit r | not stated | 26 | Added. |
| CHIRPS pooled anomaly r | 0.7102 | 0.7102, N=936 | Estimate unchanged; denominator corrected. |
| CHIRPS within-year r | 0.6350 / 0.7277 / 0.6930 | unchanged, N=312 each | Denominators added. |
| Main maize Webb SE / MDE | 0.0516 / 0.1444 in cross result; older audit MDE 0.2306 | 0.0516 / 0.1444 | Current MDE consistently uses `2.8 x bootstrap SE`. |
| Rice Webb SE / MDE | 0.0091 / 0.0255 in cross result; older audit MDE 0.0329 | 0.0091 / 0.0255 | Current MDE consistently uses `2.8 x bootstrap SE`. |
| Huber CI / MDE | [-0.0292, 0.0709] / 0.0765 | [-0.0282, 0.0704] / 0.0725 | Re-estimated with Webb cluster bootstrap, cluster=kabupaten, B=999. |
| WLS and MAD-z sensitivity models | point/CI/MDE had no method field | point/CI/MDE plus bootstrap SE and explicit method field | Recomputed / documented with Webb bootstrap, B=999. |
| Polygon sampling claim | fixed 15% or 28% reduction calculation | `PENDING` | Removed because raw polygon-area extraction is absent; no empirical reduction is claimed. |

## Registry reconciliation

| Registry item | Result evidence | Current status |
|---|---|---|
| DS01 22 unique AgERA5 cells | A3 rerun reports 22 cells | MATCH |
| DS03 2015-2017 rice baseline | BPS source rows are all `sumber_halaman_verified=false` | Registry changed to `PENDING_MANUAL_VERIFICATION` |
| DS05 main period 2015-2021 | A4 rerun N=124 before robust screen | MATCH; crop-selection N uses its separately documented robust flag. |
| DS06 2017-2024 Tier B | No rerun script changes this source restriction | MATCH |
| DS07 2015-2021 secondary benchmark | No rerun script changes this source restriction | MATCH |
| DS09 936 unit-months | Raw matched file and rerun | Registry corrected from 972 to 936. |

## Unresolved reproduction and data issues

1. A clean environment still requires a successful `pip install -r requirements.txt` followed by a rerun. The dependency installation did not persist packages in the generated environment.
2. The polygon-versus-centroid comparison cannot report before/after bias or a range until actual polygon-area CHIRPS and AgERA5 extraction is available.
3. BPS 2015-2017 pages require human inspection of the cited PDFs before their values can be treated as verified.
