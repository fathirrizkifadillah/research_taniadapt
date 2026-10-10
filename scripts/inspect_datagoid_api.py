import requests
import re
import json

for slug in ['produktivitas-padi-berdasarkan-kabupaten-kota-di-jawa-barat',
             'produktivitas-padi-sawah-berdasarkan-kabupaten-kota-di-jawa-barat',
             'produktivitas-jagung-menurut-kecamatan-di-kabupaten-subang']:
    url = f'https://data.go.id/dataset/dataset/{slug}'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'=== {slug} ===')
    # search for api urls in the html
    for api_url in set(re.findall(r'https?://[^\s"\'<>]*(?:api|data|resource)[^\s"\'<>]*', r.text)):
        if any(k in api_url.lower() for k in ['distanhor', 'padi', 'jagung', 'subang', 'jabar', 'download']):
            print('  ->', api_url)
