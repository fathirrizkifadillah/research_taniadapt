import subprocess

out = subprocess.check_output(['git', 'log', '--diff-filter=D', '--summary'], encoding='utf-8')
deleted_files = []
current_commit = None
for line in out.splitlines():
    if line.startswith('commit '):
        current_commit = line.split()[1]
    elif 'delete mode' in line:
        filepath = line.split('delete mode 100644 ')[-1].strip()
        deleted_files.append({'commit': current_commit, 'filepath': filepath})

print(f"Total deleted files found: {len(deleted_files)}")
for d in deleted_files:
    print(f"{d['commit'][:7]}: {d['filepath']}")
