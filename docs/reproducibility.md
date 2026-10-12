# Reproducibility: Phase 4 Canonical Pipeline

This project is executed from the repository root. Paths are defined in
`scripts/project_paths.py`, so a clone can live in any directory.

## Environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`cdsapi` requires a valid CDS API configuration only when AgERA5 must be
downloaded again. The registered local data are sufficient to reproduce the
current audit outputs.

## Canonical Phase 4 refresh

```powershell
python scripts/run_phase4_pipeline.py
```

The command refreshes A2 (CHIRPS versus AgERA5), A3 (spatial effective sample
size and PCA), and A4 (panel inference and minimum detectable effect). It does
not run the legacy audit or notebook-rewriting scripts.

To regenerate the ten executed EDA notebooks after the canonical computations:

```powershell
python scripts/run_phase4_pipeline.py --include-notebooks
```

Before using outputs for Phase 5, consult
`reports/dataset_audit/final_dataset_registry.csv` and
`docs/phase4_final_dataset_evidence_registry.md`. They specify the authoritative
artifact, valid period, evidence tier, and known restriction for each dataset.
