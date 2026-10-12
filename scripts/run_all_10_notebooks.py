"""
Script: run_all_10_notebooks.py
Executes all 10 notebooks top-to-bottom using NotebookClient,
rendering inline outputs, saving figures to reports/figures/,
and saving JSON results to reports/results/.
"""

import sys
import nbformat as nbf
from nbclient import NotebookClient
from project_paths import PROJECT_ROOT

NOTEBOOK_DIR = PROJECT_ROOT / "notebook"

notebook_files = [
    "01_AgERA5.ipynb",
    "02_bangladesh_rice_panel.ipynb",
    "03_west_java_rice_productivity.ipynb",
    "04_indonesia_agroclimatic.ipynb",
    "05_subang_maize_productivity.ipynb",
    "06_west_java_horticulture_productivity.ipynb",
    "07_soybean_and_spatial_geoboundaries.ipynb",
    "08_production_and_harvest_area.ipynb",
    "09_climate_covariates_and_chirps.ipynb",
    "10_phase6_exploratory_data_analysis.ipynb"
]

print("=== STARTING EXECUTION OF ALL 10 NOTEBOOKS ===")
for nb_name in notebook_files:
    nb_path = NOTEBOOK_DIR / nb_name
    print(f"\n>>> Executing {nb_name}...")
    nb = nbf.read(nb_path, as_version=4)
    client = NotebookClient(
        nb, 
        timeout=600, 
        kernel_name="python3", 
        resources={"metadata": {"path": str(nb_path.parent)}}
    )
    try:
        client.execute()
        nbf.write(nb, nb_path)
        print(f"SUCCESS: {nb_name} executed cleanly!")
    except Exception as e:
        print(f"ERROR executing {nb_name}: {e}")
        nbf.write(nb, nb_path)
        sys.exit(1)

print("\n=== ALL 10 NOTEBOOKS EXECUTED CLEANLY WITH INLINE OUTPUTS! ===")
