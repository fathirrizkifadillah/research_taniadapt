"""Shared, repository-relative paths for TaniAdapt scripts.

This module keeps runnable scripts independent from a particular Windows user
directory. Scripts should import ``PROJECT_ROOT`` from here instead of
embedding an absolute local path.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
DATASET_AUDIT_DIR = REPORTS_DIR / "dataset_audit"
FIGURES_DIR = REPORTS_DIR / "figures"
RESULTS_DIR = REPORTS_DIR / "results"
