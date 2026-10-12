# Hindcast plan: non-yield climate indicator check

**Status:** preregistered before executing the hindcast indicators.  
**Purpose:** check whether a local, historical-percentile implementation flags documented climate events. This is not a yield-validation exercise and will not be used to infer crop loss, disease incidence, or causal effects.

## Fixed data and scoring design

- **Weather source:** daily AgERA5 for the 22 unique cells in `reports/dataset_audit/a8_spatial_grid_cells_audit.csv`.
- **Reference distribution:** 1991--2020 daily climatology, once acquired and quality checked. The same reference distribution will be used for all event years.
- **Event observation period:** calendar months stated below. No dates, indicator definitions, percentile cut-offs, or event list will be changed after results are inspected.
- **Indicators:** (1) consecutive dry days (CDD), (2) rolling 14-day precipitation total, (3) climatic water balance proxy `P - ET0`, (4) growing degree day accumulation only when a crop-specific base temperature has a VERIFIED evidence record, and (5) count of days meeting literature-defined conducive-weather conditions only when the relevant paper is VERIFIED. An unavailable evidence parameter yields `evidence_insufficient`, rather than a substituted threshold.
- **Extreme reporting convention:** an indicator is called locally high/low only from its historical percentile rank. This is a reporting convention, not an agronomic damage threshold. Each result must record `rank_basis_n`.

## Prespecified events and expected signal

| Event ID | Period assessed | Documented event | Primary source opened before execution | Expected indicator pattern | What counts as a check result |
|---|---|---|---|---|---|
| HC_2016_WET | Oct--Dec 2016 | Weak La Nina with negative IOD; BMKG reported high rainfall potential around western Java and its food-security bulletin notes above-normal rain in Java during prior La Nina periods. | BMKG, [atmospheric analysis, late Nov 2016](https://www.bmkg.go.id/iklim/1650); BMKG, [food-security bulletin Aug 2016](https://www.bmkg.go.id/iklim/buletin-pemantauan-ketahanan-pangan-vol-3-agustus-2016) | Relatively high 14-day precipitation and `P - ET0`; relatively low CDD. | **Hit** if the stated wet indicators are in the direction expected in a documented local cell; otherwise **miss**. Spatial heterogeneity is reported. |
| HC_2019_DRY | Jun--Oct 2019 | Dry season with agricultural drought impacts; BMKG attributes contribution to El Nino active through Jul 2019 and positive IOD. | BMKG, [2019 climate and weather reflection](https://www.bmkg.go.id/siaran-pers/refleksi-2019-kejadian-bencana-terkait-cuaca-iklim-dan-gempabumi-yang-signifikan) | Relatively low rolling precipitation and `P - ET0`; relatively high CDD. | Same directional rule; no tuning of windows after the result. |
| HC_2023_DRY | Jun--Nov 2023 | El Nino and positive IOD; BMKG documented prolonged meteorological drought and extreme long dry spells in West Java. | BMKG, [Q3 seasonal monitoring](https://www.bmkg.go.id/iklim/pemantauan-musiman-april-september-q3-2023); BMKG, [Nov 2023 dry-season impact release](https://www.bmkg.go.id/siaran-pers/dampak-lanjutan-kemarau-kering-bmkg-sebut-sektor-ini-akan-sangat-terpukul) | Relatively low rolling precipitation and `P - ET0`; relatively high CDD. | Same directional rule; no tuning of windows after the result. |

## Interpretation safeguards

1. A hit means that the *weather indicator* reflects the documented climate event at the relevant local percentile. It does not validate a crop-loss prediction or a management action.
2. A miss remains a miss. It is not grounds to alter the reference period, percentile convention, window, or indicator definition.
3. Results are reported per cell and as a count/proportion across the 22 cells. Province-level event descriptions do not imply that every cell must have the same signal.
4. The plan deliberately has no crop calendar assumption. Crop-phase, GDD, disease-conducive-day, and action claims remain `evidence_insufficient` until the associated evidence registry entry is VERIFIED.
