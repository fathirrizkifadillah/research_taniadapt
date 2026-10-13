"""Sync canonical research rules and schemas to web app engine directory and check SHA256 hashes."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

RESEARCH_ROOT = Path(__file__).resolve().parents[1]
WEB_ENGINE_DIR = Path("/mnt/c/CODING/TaniAdapt/taniadapt-web/src/lib/engine")


def get_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    h.update(filepath.read_bytes())
    return h.hexdigest()


def sync_and_verify():
    WEB_ENGINE_DIR.mkdir(parents=True, exist_ok=True)
    
    files_to_sync = [
        ("rules/rules.json", "rules.json"),
        ("schemas/engine_output.schema.json", "engine_output.schema.json"),
        ("tests/golden_engine_vectors.json", "golden_engine_vectors.json")
    ]
    
    for src_rel, dst_name in files_to_sync:
        src = RESEARCH_ROOT / src_rel
        dst = WEB_ENGINE_DIR / dst_name
        if not src.exists():
            print(f"Warning: {src} not found")
            continue
        shutil.copy2(src, dst)
        src_hash = get_sha256(src)
        dst_hash = get_sha256(dst)
        assert src_hash == dst_hash, f"Hash mismatch for {dst_name}: {src_hash} != {dst_hash}"
        print(f"Synced {dst_name} -> SHA256: {src_hash[:12]}... OK")


if __name__ == "__main__":
    sync_and_verify()
