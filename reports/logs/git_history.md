# Git History

## 2026-10-12 Phase 4 close candidate

- Added reproducibility and rerun reconciliation records (`reports/logs/rerun_diff.md`).
- Corrected CHIRPS matched denominator from 972 to 936 unit-months; recorded N for each correlation (pooled N=936, within-year N=312 each, per-unit N=26 units).
- Recomputed maize robust sensitivity models (WLS, Huber, MAD-z) with Webb wild cluster bootstrap (cluster=kabupaten, B=999) and analytical MDE (`2.8 x SE bootstrap`).
- Marked the rice BPS baseline `PENDING_MANUAL_VERIFICATION` and set `diisi_oleh: BELUM DIVERIFIKASI MANUSIA` with `sumber_halaman_verified: false`.
- Updated `docs/crop_outcome_decision.md` to DRAFT status with consistent rice MDE (+/-0.0255), 18 unique sentra cells, robust z-flag, and explicit registry classes.
- Standardized `docs/engine_output_schema.md` with evidence-bounded placeholders, percentile reporting conventions, rank_basis_n, synced action table, and removed unverified thresholds.
- Created tag `phase4-close-candidate` at commit `365214cb2394f9f1ec4340be5bdf665c8a702227`.

## 2026-10-12 Non-Yield Validation & Decision Engine Setup

- Preregistered non-yield hindcast plan (`docs/hindcast_plan.md`) in commit `c515e27`.
- Evaluated hindcast indicators across all 22 cells for 2016 wet, 2019 dry, and 2023 dry (`scripts/evaluate_hindcast.py` -> `reports/results/13_hindcast_validation.json`).
- Built auditable literature evidence registry (`scripts/build_evidence_registry.py` -> `reports/dataset_audit/evidence_registry.csv` and `docs/evidence_registry_literature.md`).
- Implemented and validated FAO-56 Penman-Monteith reference ET0 and verified Kc coefficients (`scripts/mechanistic/` -> `reports/results/12_mechanistic_params.json`).
- Computed climatology baseline percentiles for downloaded 1991-2020 AgERA5 cells (`scripts/compute_11_climatology_baseline.py` -> `reports/results/11_climatology_baseline.json` & `reports/figures/11_climatology_baseline.png`).
- Removed all occurrences of forbidden claim words ("membuktikan") across documentation and results.
