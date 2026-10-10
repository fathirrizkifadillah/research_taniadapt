import requests
import json

# Cek API galura untuk keyword 'opt' atau 'hama' atau 'penyakit'
keywords = ["opt", "hama", "penyakit", "kedelai"]
headers = {"User-Agent": "Mozilla/5.0"}

for kw in keywords:
    url = f"https://galura.jabarprov.go.id/api/bigdata/dataset?search={kw}&per_page=10"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status search '{kw}': {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            items = data.get('data', [])
            print(f"Ditemukan {len(items)} item untuk '{kw}':")
            for it in items[:3]:
                print(f"  - Title: {it.get('title', it.get('name'))}")
                print(f"    Slug: {it.get('slug', it.get('url'))}")
    except Exception as e:
        print(f"Error search '{kw}': {e}")
