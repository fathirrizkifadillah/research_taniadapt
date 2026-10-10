import requests
import json
import re

for name, slug in [('DS03', 'produktivitas-padi-berdasarkan-kabupaten-kota-di-jawa-barat'),
                   ('DS05', 'produktivitas-jagung-menurut-kecamatan-di-kabupaten-subang')]:
    url = f'https://data.go.id/dataset/dataset/{slug}'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'=== {name} ===')
    matches = re.findall(r'https?://[^\s"\'<>]+(?:\.csv|\.xlsx|\.json|download)', r.text, re.IGNORECASE)
    print('Matches:', matches[:5])
    # search for script tags or window.__INITIAL_STATE__
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
    for s in scripts:
        if 'resources' in s or 'distanhor' in s or 'produktivitas' in s:
            # find urls
            u = re.findall(r'https?://[^\s"\'<>\\]+', s)
            for x in set(u):
                if 'download' in x or 'bigdata' in x or 'csv' in x:
                    print('Found URL in script:', x)

