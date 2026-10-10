from bs4 import BeautifulSoup
import re
import json

with open('scripts/mendeley_main.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
for s in soup.find_all('script'):
    if s.string and '10.17632/h94z4ftts2.1' in s.string:
        print('Found script!')
        # find json
        match = re.search(r'(\{.*"doi":\s*"10\.17632/h94z4ftts2\.1".*\})', s.string)
        if match:
            # try to parse json or print substring
            data_str = match.group(1)
            print('String length:', len(data_str))
            # print snippet around "files"
            idx = data_str.find('"files"')
            if idx != -1:
                print('Snippet around files:', data_str[idx:idx+1500])
