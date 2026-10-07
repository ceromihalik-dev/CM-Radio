#!/usr/bin/env python3
"""Generate the flash-resident UI. No filesystem upload is required."""
from pathlib import Path
import argparse
ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'firmware/web/index.html'
target = ROOT / 'firmware/src/WebUi.cpp'
generated = '#include "WebUi.h"\nconst char WEB_UI[] PROGMEM = R"CMRADIO(\n' + source.read_text(encoding='utf-8') + ')CMRADIO";\n'
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
if args.check:
    if not target.exists() or target.read_text(encoding='utf-8') != generated:
        raise SystemExit('WebUi.cpp differs. Run python scripts/embed_web.py')
else:
    target.write_text(generated, encoding='utf-8')
