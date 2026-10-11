"""Append/replace only the enclosure section, preserving the firmware notes."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

tag = sys.argv[1]
repo = os.environ['GITHUB_REPOSITORY']
data = json.loads(subprocess.check_output(
    ['gh','release','view',tag,'--repo',repo,'--json','body'], text=True))
start, end = '<!-- CM-RADIO-ENCLOSURE -->', '<!-- /CM-RADIO-ENCLOSURE -->'
body = data['body'] or ''
if start in body:
    if end not in body:
        raise RuntimeError('Incomplete enclosure section; refusing to replace unrelated release notes')
    before, remainder = body.split(start, 1)
    _, after = remainder.split(end, 1)
    body = before.rstrip()+after
section = '''
### Gehäuse Modell 3 - Retro V0.3 R8

104 × 80 × 36 mm, ohne Display; offene Lüftung, aufgeklebte Front,
Resetmechanik, zwei untere Kabelauslässe und Wandmontage per Schlüsselloch.

- **CM-Radio_Modell_3_Retro_JLC3DP_V03_R8.zip**: fünf STL-Druckteile, STEP-Dateien und CAD-Quellen.
- **CM-Radio_Modell_3_Retro_Fusion_STEP_V03_R8.zip**: STEP-Volumenkörper für Autodesk Fusion, ohne native Modellhistorie.
- Beide ZIPs enthalten aktuelle Explosionszeichnung, Schrauben-/Einsatzliste,
  Montage- und Materialangaben sowie ausführliche USB-Erstinstallationsanleitung.
- PDF, Explosionsbild und Materialliste sind zusätzlich einzeln verfügbar;
  SHA256SUMS_Gehaeuse_R8.txt enthält die Prüfsummen.

CAD- und Dateiprüfungen bestanden. **Physische R8-Abnahme steht aus.**
Nutzerfertigung aus Resin: **Gewindeeinsätze nicht thermisch einsetzen.**
Die unveränderten R8-Pilotbohrungen benötigen für Resin eine Anpassung und
Musterprüfung vor Klebemontage; siehe RESIN_HINWEIS_R8.md. Resin-Sorten/Farben
aller Teile sind nicht bestätigt. Die Firmwaredateien bleiben unverändert.
'''
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)/'release-notes.md'
    path.write_text(body.rstrip()+'\n\n'+start+'\n'+section.strip()+'\n'+end+'\n', encoding='utf-8')
    subprocess.run(['gh','release','edit',tag,'--repo',repo,'--notes-file',str(path)], check=True)
