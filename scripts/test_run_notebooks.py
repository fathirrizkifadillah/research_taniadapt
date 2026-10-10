import json
import sys
import traceback
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Non-blocking backend for headless CLI verification

NOTEBOOK_DIR = Path(r"c:\CODING\research_taniAdapt\notebook")

def display(*args):
    for a in args:
        print(a)

for nb_file in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
    print(f"\n==========================================")
    print(f"Testing execution: {nb_file.name}")
    print(f"==========================================")
    with open(nb_file, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    ns = {"display": display, "__name__": "__main__"}
    for idx, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            try:
                exec(code, ns)
            except Exception as e:
                print(f"[ERROR] Cell {idx} in {nb_file.name} failed:")
                traceback.print_exc()
                sys.exit(1)
    print(f"[SUCCESS] {nb_file.name} executed cleanly!")
