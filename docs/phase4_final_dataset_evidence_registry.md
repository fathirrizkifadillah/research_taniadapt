# Phase 4 Final Dataset and Evidence Registry

**Status:** Phase 4 closure candidate  
**Canonical date:** 2026-10-12  
**Purpose:** This document is the authoritative gate between dataset audit and later analysis. It specifies each dataset's valid grain, admissible period, permitted use, and forbidden inference.

## Canonical artifacts

- Machine-readable registry: `reports/dataset_audit/final_dataset_registry.csv`
- Canonical single-dataset results: `reports/results/01_AgERA5.json` through `reports/results/09_climate_covariates_and_chirps.json`
- Canonical cross-dataset result: `reports/results/10_cross_dataset_synthesis.json`
- Canonical spatial mapping: `reports/dataset_audit/a8_spatial_grid_cells_audit.csv`
- Canonical BPS provenance record: `reports/dataset_audit/bps_manual_input.csv`

The registry governs later phases. A later notebook, report, figure, or engine rule may not widen a dataset's approved use without a documented audit update.

## Binding Phase 4 decisions

| Dataset / topic | Final decision | Implication for later phases |
|---|---|---|
| DS01 AgERA5 | 27 administrative units map to 22 unique weather cells. | Cluster and spatial dependence must be handled; do not regard 27 ADM2 series as independent climate samples. |
| DS03 rice | The 2015-2017 outcome baseline is `PENDING_MANUAL_VERIFICATION`. | Use a mechanistic rice path only after human verification; defer primary panel inference until reliable post-2017 ADM2 outcome data exists. |
| DS05 maize | 2022 is `SUSPECT`; main panel is 2015-2021. | Use only as registered sensitivity evidence plus a mechanistic advisory layer. |
| DS06 horticulture | No post-2014 ADM2 outcome overlap and no OPT labels. | Keep cabai and tomat in Tier B IFWC; no yield regression, disease classifier, or calibrated disease probability. |
| DS07 soybean | 2022 is `SUSPECT`; select 17 active regencies ex ante. | Use 2015-2021 for the secondary panel benchmark. |
| DS04 | Shares an ERA5 lineage with DS01. | Use as an internal indicator-definition check, not independent weather validation. |
| DS09 / CHIRPS | Independent precipitation benchmark covers 2016, 2020, and 2024 only. | State the three-year scope every time CHIRPS validation is cited. |

## Canonical statistical figures

The current cross-dataset result file is authoritative for the Phase 4 closure snapshot:

| Quantity | Canonical value | Meaning |
|---|---:|---|
| H_CORN_01 estimate | +0.0368 log points per SD | Rainfall-window association, not a causal estimate. |
| H_CORN_01 95% Webb CI | [-0.0521, +0.1300] | Includes zero and an agronomically relevant small effect. |
| H_CORN_01 MDE | +/-0.1444 log points | Uses the documented `2.8 x bootstrap SE` rule. |
| Soybean MDE | +/-0.1250 log points | Uses the same `2.8 x bootstrap SE` rule. |
| Rice MDE | +/-0.0255 log points | Not evidence of high power because the panel has only T=3. |
| AgERA5-CHIRPS pooled anomaly correlation | 0.7102, N=936 | 312 unit-months in each benchmark year (2016, 2020, 2024); 26 units have a valid per-unit correlation. |
| Maximum wet-season signed precipitation bias | +72.31% | Requires bias-aware interpretation in high-bias regions. |

## Deprecation policy

The following values are historical artifacts and may be retained only to explain audit evolution. They must not appear as current results, dashboard values, or engine parameters.

| Deprecated item | Replace with |
|---|---|
| 25 unique AgERA5 grid cells | 22 unique cells |
| 14 DS04 West Java grid points as the official sample | 12 points within the official province polygon |
| 10-year CHIRPS validation, 972 unit-months, or raw-seasonal `r = 0.91` | Three-year benchmark, 936 unit-months, and deseasonalized anomaly metrics from the canonical results |
| Maize MDE +/-0.2306 and soybean MDE +/-0.0983 / 10.33% | The canonical `2.8 x bootstrap SE` metrics above |
| Horticulture period 2016-2024 for the analytical target | 2017-2024, N=8 per provincial crop target |

## Phase 4 exit criteria

Phase 4 is complete when all downstream artifacts use this registry, the maintained pipeline runs from a declared environment, and deprecated numbers are labeled as historical wherever they are retained. The unresolved data limitations remain explicit; they do not block a constrained Phase 5 decision.

## Phase 5 handoff

The Phase 5 selection document must cite this registry and classify every chosen crop as one of:

1. mechanistic advisory;
2. empirical sensitivity analysis plus mechanistic advisory;
3. Tier B literature-transfer rule; or
4. blocked pending new data.
