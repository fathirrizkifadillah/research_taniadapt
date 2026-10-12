"""Run the canonical Phase 4 computations from any checkout location.

The pipeline deliberately excludes legacy audit scripts and notebook patchers.
It refreshes only the cross-dataset evidence that is registered as canonical in
``reports/dataset_audit/final_dataset_registry.csv``.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from project_paths import PROJECT_ROOT


CANONICAL_STEPS = (
    "compute_a2_chirps_agera5_validation.py",
    "compute_a3_spatial_neff_pca.py",
    "compute_a4_panel_inference_mde.py",
    "refresh_phase4_canonical_results.py",
)


def run_script(script_name: str) -> None:
    script = PROJECT_ROOT / "scripts" / script_name
    print(f"\n>>> {script_name}")
    subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh canonical Phase 4 evidence.")
    parser.add_argument(
        "--include-notebooks",
        action="store_true",
        help="Also execute the ten EDA notebooks after the canonical computations.",
    )
    args = parser.parse_args()

    for step in CANONICAL_STEPS:
        run_script(step)

    if args.include_notebooks:
        run_script("run_all_10_notebooks.py")


if __name__ == "__main__":
    main()
