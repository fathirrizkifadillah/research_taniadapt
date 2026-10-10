import re

with open('data/rice_panel/raw/test_file.bin', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print('Length of html:', len(text))
downloads = set(re.findall(r'https?://[^\s"\'<>]+(?:download|prod-files|content|files)[^\s"\'<>]*', text, re.IGNORECASE))
for d in sorted(downloads):
    print('Found URL:', d)

# Also look for json embedded in script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
for s in scripts:
    if '1aa46123-9324-4adf-9f4a-756cf2bfefb6' in s:
        print('Found file ID in script!')
        for line in s.split('\n'):
            if '1aa46123' in line:
                print('Line:', line[:200])
