import json

path = r'C:\Users\FATHIR\.gemini\antigravity-ide\brain\fe57d88d-8084-4839-a409-099e1487b008\.system_generated\logs\transcript_full.jsonl'

with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        for name in ['02_bangladesh', '03_west_java', '04_indonesia', '05_maize', '06_west_java', '07_west_java', '08_west_java']:
            if name in line and 'VIEW_FILE' in line:
                obj = json.loads(line)
                print(f"Line {idx} {name} length: {len(obj.get('content', ''))}")
                # print first few lines of content
                lines = obj.get('content', '').splitlines()[:20]
                for l in lines:
                    print("  ", l)
