import subprocess
import os
import hashlib
import json

DEST_DIR = "data/raw/DS04_indonesia_agroclimatic"
os.makedirs(DEST_DIR, exist_ok=True)

# Fetch files list from Mendeley API
cmd = [
    "curl.exe", "-s",
    "-H", "Accept: application/json",
    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "https://data.mendeley.com/api/datasets/3pfbdbzfff/files"
]
res = subprocess.run(cmd, capture_output=True, text=True)
files = json.loads(res.stdout)

print(f"Total files in DS04: {len(files)}")

results = []
for f in files:
    fname = f["filename"]
    fsize = f["size"]
    sha256_exp = f["content_details"]["sha256_hash"]
    download_url = f["content_details"]["download_url"]
    
    out_path = os.path.join(DEST_DIR, fname)
    
    # check if already exists and hash matches
    if os.path.exists(out_path) and os.path.getsize(out_path) == fsize:
        with open(out_path, "rb") as fp:
            if hashlib.sha256(fp.read()).hexdigest() == sha256_exp:
                print(f"Already exists & verified: {fname}")
                results.append((fname, fsize, sha256_exp, True))
                continue
                
    print(f"Downloading: {fname} ({fsize} bytes)...")
    sub_cmd = ["curl.exe", "-s", "-L", download_url, "-o", out_path]
    subprocess.run(sub_cmd)
    
    # verify
    if os.path.exists(out_path):
        actual_size = os.path.getsize(out_path)
        with open(out_path, "rb") as fp:
            actual_hash = hashlib.sha256(fp.read()).hexdigest()
        match = (actual_size == fsize) and (actual_hash == sha256_exp)
        print(f"  -> Done {fname}: size={actual_size}, match={match}")
        results.append((fname, actual_size, actual_hash, match))
    else:
        print(f"  -> FAILED to download {fname}")
        results.append((fname, 0, "", False))

print(f"\nAll files processed: {sum(1 for r in results if r[3])}/{len(results)} verified.")
