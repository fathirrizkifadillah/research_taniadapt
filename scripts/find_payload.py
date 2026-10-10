import json
import re

with open(r'C:\Users\FATHIR\.gemini\antigravity-ide\brain\fe57d88d-8084-4839-a409-099e1487b008\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '"data":[' in line or '"data": [' in line:
            print(f'Line {i} matches data array! Line length: {len(line)}')
            obj = json.loads(line)
            content = str(obj.get('content', ''))
            print('Content preview:', content[:200])
            m = re.search(r'(\{[\s\S]*"data"[\s\S]*\})', content)
            if m:
                payload = m.group(1)
                print('Found payload length:', len(payload))
                with open('data/raw/DS03_west_java_rice_productivity/od_18103_produktivitas_padi_jabar.json', 'w', encoding='utf-8') as out:
                    out.write(payload)
                print('Saved payload to JSON!')
                break
