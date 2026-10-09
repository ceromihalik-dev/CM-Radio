#!/usr/bin/env python3
"""Generate the flash-resident UI. No filesystem upload is required."""
from pathlib import Path
import argparse
import html
import re
ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'firmware/web/index.html'
target = ROOT / 'firmware/src/WebUi.cpp'
def changelog_html():
    parts = []
    opened = False
    for line in (ROOT/'docs/CHANGELOG.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            if opened: parts.append('</ul></details>')
            parts.append('<details class="change-entry"><summary>'+html.escape(line[3:])+'</summary><ul>')
            opened = True
        elif opened and line.strip():
            text = line[2:] if line.startswith('- ') else line
            parts.append('<li>'+html.escape(text)+'</li>')
    if opened: parts.append('</ul></details>')
    return '\n'.join(parts)
text = source.read_text(encoding='utf-8')
if text.count('<!-- CHANGELOG_START -->') != 1 or text.count('<!-- CHANGELOG_END -->') != 1:
    raise SystemExit('Exactly one changelog block is required')
expected = re.sub(r'<!-- CHANGELOG_START -->.*?<!-- CHANGELOG_END -->', lambda _: '<!-- CHANGELOG_START -->\n'+changelog_html()+'\n<!-- CHANGELOG_END -->', text, flags=re.S)
generated = '#include "WebUi.h"\nconst char WEB_UI[] PROGMEM = R"CMRADIO(\n' + expected + ')CMRADIO";\n'
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
if args.check:
    if text != expected: raise SystemExit('Changelog differs. Run python scripts/embed_web.py')
    if not target.exists() or target.read_text(encoding='utf-8') != generated:
        raise SystemExit('WebUi.cpp differs. Run python scripts/embed_web.py')
else:
    source.write_text(expected, encoding='utf-8')
    target.write_text(generated, encoding='utf-8')
