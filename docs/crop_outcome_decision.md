# Crop and Outcome Selection

**Status:** DRAFT - pending user ratification

## Selection criteria written after the data audit

Selection considers valid observations after the same robust outlier / near-zero flag used in `reports/logs/crop_cell_and_outlier_audit.csv`, time coverage, unique AgERA5 cells, outcome integrity, statistical resolution, and a documented evidence tier. `N_valid` is not defined by the rule `outcome > 0`.

## Candidate portfolio

| Crop | Outcome and valid period | N after robust flag | Unique AgERA5 cells | Registry class | Constraint |
|---|---|---:|---:|---|---|
| Padi | ADM2 annual productivity, 2015-2017 | 53 | 18 | mechanistic advisory | BPS baseline is `PENDING_MANUAL_VERIFICATION`; no primary weather-yield panel. |
| Jagung | ADM2 annual productivity, 2015-2021 | 121 | 18 | empirical sensitivity analysis + mechanistic advisory | 2022 excluded as suspect; effect estimate is evidence_insufficient. |
| Kedelai | ADM2 annual productivity, 2015-2021 | 113 | 18 | empirical sensitivity analysis + mechanistic advisory | 2022 excluded as suspect; secondary benchmark only. |
| Cabai | Provincial annual productivity, 2017-2024 | 8 per crop target | Outcome provinsi tidak punya unit sel yang terdefinisi | Tier B literature-transfer rule | No ADM2 outcome-weather overlap and no OPT labels. |
| Tomat | Provincial annual productivity, 2017-2024 | 8 | Outcome provinsi tidak punya unit sel yang terdefinisi | Tier B literature-transfer rule | No ADM2 outcome-weather overlap and no OPT labels. |
| Bawang merah | No eligible local outcome | - | - | blocked pending new data | Not in the current engine crop enum. |

Harvest-area shares are intentionally omitted because this decision document does not yet contain a reproducible DS08 aggregation for every crop. It must not use remembered values. The prior Garut `>60%` statement is removed.

## Statistical interpretation

- Rice MDE is **+/-0.0255 log points** from the recorded bootstrap SE. This does not establish high power because the validated series has T=3.
- Maize H_CORN_01 has beta +0.0368 and 95% Webb CI [-0.0521, +0.1300]. The result is evidence_insufficient for a yield-effect claim.
- Soybean remains a secondary sensitivity benchmark; it is not a calibrated yield model.

## Permitted model paths

### Padi

Use a mechanistic advisory only after the relevant published model and input rules are verified. DS03 is limited to 2015-2017 and the BPS manual baseline remains pending human verification.

### Jagung and kedelai

Use empirical sensitivity analysis plus mechanistic advisory. Do not turn estimates or confidence intervals into causal statements, yield forecasts, or risk thresholds.

### Cabai and tomat

Use a Tier B literature-transfer rule only. The output is **jumlah hari kondusif dalam jendela N hari terakhir**. It must not report a 0-100 score, disease probability, disease occurrence, or yield loss.
