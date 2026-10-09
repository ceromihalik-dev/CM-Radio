#!/usr/bin/env python3
"""Bundle compiled images with a flash manifest, checksums and build inputs."""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=ROOT/'dist/CM-Radio-V0.1.3-07')
args = parser.parse_args()
build = ROOT/'firmware/.pio/build/loud_wrover'
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
files = [('bootloader.bin', 0x1000), ('partitions.bin', 0x8000), ('firmware.bin', 0x10000)]
for filename, _ in files:
    shutil.copy2(build/filename, out/filename)
core = Path(os.environ.get('PLATFORMIO_CORE_DIR', str(Path.home()/'.platformio')))
shutil.copy2(core/'packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin', out/'boot_app0.bin')
files.insert(2, ('boot_app0.bin', 0xe000))
subprocess.run([sys.executable, '-m', 'esptool', '--chip', 'esp32', 'merge_bin', '-o', str(out/'CM-Radio-V0.1.3-full.bin'), '--flash_mode', 'dio', '--flash_freq', '40m', '--flash_size', '8MB', *[part for name, address in files for part in (hex(address), str(out/name))]], check=True)
shutil.copy2(ROOT/'firmware/platformio.ini', out/'build-platformio.ini')
shutil.copy2(ROOT/'firmware/partitions.csv', out/'build-partitions.csv')
shutil.copy2(ROOT/'scripts/flash.py', out/'flash.py')
shutil.copy2(ROOT/'scripts/smoke_test.py', out/'smoke_test.py')
shutil.copy2(ROOT/'LICENSE', out/'LICENSE')
shutil.copy2(ROOT/'THIRD_PARTY.md', out/'THIRD_PARTY.md')
shutil.copy2(ROOT/'docs/ERSTSTART.md', out/'ERSTSTART.md')
manifest = {'name':'CM-Radio','version':'0.1.3','build':'07','target':'Loud-ESP32 ESP32-WROVER-N8R8','chip':'esp32','flashSize':8388608,'flashOffset':0,'firmwareFile':'CM-Radio-V0.1.3-full.bin','partitions':{name:hex(offset) for name,offset in files},'hardwareTested':False}
guide=(ROOT/'docs/USB_ERSTINSTALLATION.txt').read_text().replace('{VERSION}',manifest['version']).replace('{BUILD}',manifest['build']).replace('{FULL_IMAGE}',manifest['firmwareFile'])
(out/'USB_ERSTINSTALLATION.txt').write_text(guide,encoding='utf-8')
manifest['update'] = {'file':'firmware.bin','size':(out/'firmware.bin').stat().st_size,'sha256':hashlib.sha256((out/'firmware.bin').read_bytes()).hexdigest(),'target':'CM-Radio-WROVER-N8R8'}
try:
    manifest['sourceCommit'] = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    manifest['sourceDirty'] = bool(subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True).strip())
except subprocess.CalledProcessError:
    manifest['sourceCommit'] = 'uncommitted'
manifest['platformioCore'] = importlib.metadata.version('platformio')
(out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
checksums = []
for file in sorted(out.iterdir()):
    if file.is_file() and file.name != 'SHA256SUMS':
        checksums.append(hashlib.sha256(file.read_bytes()).hexdigest()+'  '+file.name)
(out/'SHA256SUMS').write_text('\n'.join(checksums)+'\n')
print('Flash package:', out)
