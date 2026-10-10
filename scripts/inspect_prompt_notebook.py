import json

path = r'C:\Users\FATHIR\.gemini\antigravity-ide\brain\fe57d88d-8084-4839-a409-099e1487b008\.system_generated\logs\transcript_full.jsonl'

with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx == 24: # The user prompt with prompt text
            obj = json.loads(line)
            content = obj.get('content', '')
            for l in content.splitlines():
                if 'notebook' in l.lower() or 'deliverable' in l.lower() or 'ds0' in l.lower() or 'section 3' in l.lower():
                    try:
                        print(l[:120])
                    except:
                        pass
