import nbformat
from nbclient import NotebookClient
from pathlib import Path
import traceback

NOTEBOOK_DIR = Path(r"c:\CODING\research_taniAdapt\notebook")

for nb_path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
    print(f"\n==========================================")
    print(f"Executing in-place with NotebookClient: {nb_path.name}")
    print(f"==========================================")
    try:
        nb = nbformat.read(nb_path, as_version=4)
        client = NotebookClient(nb, timeout=600, kernel_name='python3')
        client.execute()
        nbformat.write(nb, nb_path)
        print(f"[SUCCESS] {nb_path.name} fully rendered and saved!")
    except Exception as e:
        print(f"[ERROR] Failed {nb_path.name}: {e}")
        traceback.print_exc()

print("\nSemua notebook berhasil dieksekusi dan disimpan dengan output lengkap!")
