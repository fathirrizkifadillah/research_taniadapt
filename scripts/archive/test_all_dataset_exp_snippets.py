import re
import traceback
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
EXP_DIR = PROJECT_ROOT / "dataset_exp"

md_files = sorted(EXP_DIR.glob("*.md"))

print(f"Testing Python snippets in {len(md_files)} markdown files in dataset_exp/...")

for mf in md_files:
    if mf.name in ["Dataset_overview.md", "README.md"]:
        continue
    content = mf.read_text(encoding="utf-8")
    
    # Extract python code blocks
    pattern = r"```python\s*(.*?)\s*```"
    code_blocks = re.findall(pattern, content, re.DOTALL)
    
    print(f"\n==========================================")
    print(f"File: {mf.name} ({len(code_blocks)} code blocks)")
    print(f"==========================================")
    
    for i, code in enumerate(code_blocks):
        print(f"--- Block {i+1} ---")
        try:
            # Execute in a clean namespace
            exec_globals = {"__name__": "__main__"}
            exec(code, exec_globals)
            print(f"[STATUS] SUCCESS!")
        except Exception as e:
            print(f"[STATUS] FAILED! Error: {type(e).__name__}: {e}")
