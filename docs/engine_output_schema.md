# TaniAdapt Engine Output Schema

**Status:** DRAFT - pending research ratification

## Evidence contract

The engine follows `Evidence -> Finding -> Interpretation -> Model -> Decision Logic`. It must not invent thresholds, calibrated probabilities, yield losses, or causal effects. If evidence is absent or a required input is stale, it returns `evidence_insufficient`.

`relative_rank` is a reporting convention, not an evidentiary threshold. With a populated local percentile basis, `low` means below p20, `typical` p20 to p80, and `unusually high` above p80. These labels describe relative position only; they do not establish crop damage, disease presence, or intervention efficacy.

## Output contract

```json
{
  "crop": "padi | jagung | kedelai | cabai | tomat",
  "location": {"kabkota": "<official ADM2>", "cell_id": "<AgERA5 cell>", "weather_source": "<source>"},
  "as_of": "YYYY-MM-DD",
  "issue_time": "YYYY-MM-DDTHH:MM:SS+07:00",
  "timezone": "Asia/Jakarta",
  "rule_version": "<version>",
  "data_version": "<version>",
  "data_freshness_days": null,
  "layer": "seasonal | daily",
  "indicators": [{"id": "<indicator>", "value": null, "unit": "<unit>", "relative_rank": null, "rank_basis": "<dataset and calendar window actually available>", "rank_basis_n": null}],
  "status": "normal | kondisi_mendukung_OPT | kondisi_stres_abiotik | evidence_insufficient",
  "evidence_tier": "data_learned | published_model | literature_transfer | insufficient",
  "evidence_refs": ["<verified dataset or literature reference>"],
  "claim_allowed": "<dari hasil engine>",
  "claim_forbidden": ["<forbidden claim>"],
  "limitations": ["<limitation>"],
  "action_ids": ["<action table ID>"]
}
```

`rank_basis` may name only a climatology that actually exists. It must not claim `AgERA5_1981_2020` until that climatology is available.

## Status mapping

1. Missing evidence, missing verified threshold, absent rank basis, or stale source beyond the rule freshness policy -> `evidence_insufficient`.
2. Valid percentile labels below p20, p20 to p80, and above p80 are reporting conventions only.
3. `kondisi_stres_abiotik` or `kondisi_mendukung_OPT` requires a registered VERIFIED source in `evidence_refs`. Otherwise use `evidence_insufficient`.

## Examples

### Rice

```json
{"crop":"padi","as_of":"YYYY-MM-DD","issue_time":"YYYY-MM-DDTHH:MM:SS+07:00","timezone":"Asia/Jakarta","rule_version":"<version>","data_version":"<version>","data_freshness_days":null,"layer":"seasonal","indicators":[{"id":"water_balance_indicator","value":null,"unit":"<unit>","relative_rank":null,"rank_basis":"<available local basis>","rank_basis_n":null}],"status":"evidence_insufficient","evidence_tier":"published_model","evidence_refs":["DS03 rice outcome baseline, 2015-2017 only","<verified published crop model>"],"claim_allowed":"<dari hasil engine>","claim_forbidden":["season-specific yield prediction","empirical yield effect claim from DS03"],"action_ids":["ACT_AWAIT_EVIDENCE"]}
```

### Maize

```json
{"crop":"jagung","as_of":"YYYY-MM-DD","issue_time":"YYYY-MM-DDTHH:MM:SS+07:00","timezone":"Asia/Jakarta","rule_version":"<version>","data_version":"<version>","data_freshness_days":null,"layer":"seasonal","indicators":[{"id":"phenology_weather_indicator","value":null,"unit":"<unit>","relative_rank":null,"rank_basis":"AgERA5 2015-2021 only when built","rank_basis_n":null}],"status":"evidence_insufficient","evidence_tier":"insufficient","evidence_refs":["DS05 2015-2021 sensitivity analysis","<verified mechanistic reference>"],"claim_allowed":"<dari hasil engine>","claim_forbidden":["yield stress conclusion from a confidence interval containing zero","calibrated yield forecast"],"action_ids":["ACT_AWAIT_EVIDENCE"]}
```

### Chili and tomato

Both crops report `jumlah_hari_kondusif_dalam_jendela_N_hari_terakhir`. They use `evidence_tier: literature_transfer` and `status: evidence_insufficient` until a VERIFIED literature source supplies the rule. Use `ambang: PENDING_LITERATURE`; literal temperature, humidity, and dew-point thresholds are forbidden.

```json
{"crop":"cabai | tomat","layer":"daily","indicators":[{"id":"jumlah_hari_kondusif","value":null,"unit":"hari","relative_rank":null,"rank_basis":"<available local basis>","rank_basis_n":null}],"status":"evidence_insufficient","evidence_tier":"literature_transfer","evidence_refs":["ambang: PENDING_LITERATURE"],"claim_allowed":"<dari hasil engine>","claim_forbidden":["calibrated disease probability","disease occurrence claim","yield loss estimate"],"action_ids":["ACT_AWAIT_EVIDENCE"]}
```

## Action table

| Action ID | Action | Evidence source | Status |
|---|---|---|---|
| `ACT_AWAIT_EVIDENCE` | Defer specific advice until evidence is sufficient. | Engine evidence contract | ACTIVE |
| `ACT_DRAINAGE_CHECK` | Inspect drainage. | PENDING_EXTENSION_SOURCE | PENDING_EXTENSION_SOURCE |
| `ACT_WATER_CONSERVATION` | Consider water conservation. | PENDING_EXTENSION_SOURCE | PENDING_EXTENSION_SOURCE |
| `ACT_CANOPY_VENTILATION` | Inspect canopy ventilation. | PENDING_EXTENSION_SOURCE | PENDING_EXTENSION_SOURCE |
| `ACT_SCOUT_FIELD_SYMPTOMS` | Scout field symptoms. | PENDING_EXTENSION_SOURCE | PENDING_EXTENSION_SOURCE |
| `ACT_FUNGICIDE_REVIEW` | Review fungicide use with official extension guidance. | PENDING_EXTENSION_SOURCE | PENDING_EXTENSION_SOURCE |
| `ACT_MAINTAIN_STANDARD` | Continue routine management. | PENDING_EXTENSION_SOURCE | PENDING_EXTENSION_SOURCE |
