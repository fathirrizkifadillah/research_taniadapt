from bs4 import BeautifulSoup
import re
import json

with open('scripts/mendeley_main.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
print('Title:', soup.title.string if soup.title else 'No title')

for a in soup.find_all('a', href=True):
    href = a['href']
    if any(k in href.lower() for k in ['download', 'file', 'zip', 'csv']):
        print('Link:', a.text.strip()[:30], '->', href)

for btn in soup.find_all(['button', 'a']):
    if 'download' in btn.text.lower():
        print('Download element:', btn)

# Search scripts for initial data or state
for s in soup.find_all('script'):
    if s.string and ('window.__' in s.string or 'dataset' in s.string or 'files' in s.string):
        for line in s.string.split(';'):
            if any(k in line for k in ['files', 'downloadUrl', 'directDownload', 'contentUrl']):
                print('Found in script:', line[:200])
