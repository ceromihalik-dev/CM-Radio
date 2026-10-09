#!/usr/bin/env python3
"""Host checks: validate inputs, partition bounds and the generated UI."""
from pathlib import Path
import csv
import re
import subprocess
import tempfile
import sys
ROOT = Path(__file__).resolve().parents[1]
subprocess.run(['python3', str(ROOT/'scripts/embed_web.py'), '--check'], check=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT/'tests'), '-p', 'test_*.py'], check=True)
with tempfile.TemporaryDirectory() as directory:
    binary = str(Path(directory)/'validation')
    subprocess.run(['g++', '-std=c++11', '-Wall', '-Wextra', '-Werror', '-I'+str(ROOT/'firmware/include'), str(ROOT/'tests/test_validation.cpp'), '-o', binary], check=True)
    subprocess.run([binary], check=True)
    scan_binary = str(Path(directory)/'wifi_scan')
    subprocess.run(['g++', '-std=c++11', '-Wall', '-Wextra', '-Werror', '-I'+str(ROOT/'firmware/include'), str(ROOT/'tests/test_wifi_scan.cpp'), '-o', scan_binary], check=True)
    subprocess.run([scan_binary], check=True)
    control_binary = str(Path(directory)/'playback_controls')
    subprocess.run(['g++', '-std=c++11', '-Wall', '-Wextra', '-Werror', '-I'+str(ROOT/'firmware/include'), str(ROOT/'tests/test_playback_controls.cpp'), '-o', control_binary], check=True)
    subprocess.run([control_binary], check=True)
    html = (ROOT/'firmware/web/index.html').read_text()
    script = re.search(r'<script>(.*?)</script>', html, re.S).group(1)
    js = Path(directory)/'web.js'
    js.write_text(script)
    subprocess.run(['node', '--check', str(js)], check=True)
subprocess.run(['node', str(ROOT/'tests/test_web.js')], cwd=ROOT, check=True)
rows = list(csv.reader(line for line in (ROOT/'firmware/partitions.csv').read_text().splitlines() if line.strip() and not line.startswith('#')))
previous_end = 0x9000
apps = []
for row in rows:
    name, kind, subtype, raw_offset, raw_size = [part.strip() for part in row[:5]]
    offset, size = int(raw_offset, 0), int(raw_size, 0)
    assert offset >= previous_end, f'{name}: overlapping partition'
    assert offset+size <= 8*1024*1024, f'{name}: exceeds 8 MB'
    if kind == 'app':
        assert offset % 0x10000 == 0
        apps.append((offset, size))
    previous_end = offset+size
assert apps == [(0x10000, 0x300000), (0x310000, 0x300000)]
assert previous_end == 8*1024*1024
print('8 MB partition layout and JavaScript syntax: PASS')
