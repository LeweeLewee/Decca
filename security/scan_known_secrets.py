"""Search local Git objects and nonignored files for known installation passwords.

Only counts and field names are printed, never secret values or matching text.
This is exact-match coverage, not a general secret detector.
"""
import ast
from pathlib import Path
import re
import subprocess
import json

root = Path(__file__).resolve().parents[1]
source = (root / 'src/secrets.h').read_text()
needles = {}
for name, literal in re.findall(r'^\s*#define\s+(DECCA_(?:WIFI|OTA)_PASSWORD)\s+("[^"\r\n]*")', source, re.M):
    value = ast.literal_eval(literal).encode()
    if len(value) < 8:
        raise SystemExit('Password missing or too short for this scan; no values printed')
    needles[name] = value
if len(needles) != 2:
    raise SystemExit('Expected two password definitions; no values printed')

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

objects = [line.split(b' ', 1)[0] for line in git('rev-list', '--objects', '--all').splitlines()]
process = subprocess.Popen(['git', '-C', str(root), 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
hits = {name: 0 for name in needles}
max_length = max(map(len, needles.values()))
for oid in objects:
    process.stdin.write(oid + b'\n'); process.stdin.flush()
    header = process.stdout.readline().split()
    if len(header) != 3: raise RuntimeError('Unexpected Git object header')
    remaining = int(header[2]); tail = b''; found = set()
    while remaining:
        block = process.stdout.read(min(65536, remaining))
        if not block: raise RuntimeError('Truncated Git object')
        remaining -= len(block)
        data = tail + block
        found.update(name for name, value in needles.items() if value in data)
        tail = data[-max_length:]
    if process.stdout.read(1) != b'\n': raise RuntimeError('Invalid Git object delimiter')
    for name in found: hits[name] += 1
process.stdin.close()
if process.wait() != 0: raise RuntimeError('Git object scan failed')
paths = set(git('ls-files', '-z', '--cached', '--others', '--exclude-standard').split(b'\0')) - {b''}
file_hits = {name: 0 for name in needles}
for raw in paths:
    path = root / raw.decode('utf-8')
    if path.is_file():
        data = path.read_bytes()
        for name, value in needles.items():
            if value in data: file_hits[name] += 1
print(json.dumps({'git_objects_scanned': len(objects), 'nonignored_files_scanned': len(paths), 'history_matches': hits, 'file_matches': file_hits}))
raise SystemExit(1 if any(hits.values()) or any(file_hits.values()) else 0)
