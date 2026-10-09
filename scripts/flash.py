#!/usr/bin/env python3
"""First installation for the specific 8 MB ESP32-WROVER target."""
from pathlib import Path
import argparse
import hashlib
import subprocess
import sys
parser = argparse.ArgumentParser(description='CM-Radio V0.1: Loud-ESP32 WROVER-N8R8, 8 MB Flash')
parser.add_argument('--port', required=True, help='e.g. COM5 or /dev/ttyUSB0')
parser.add_argument('--image', type=Path, default=Path(__file__).resolve().parent/'CM-Radio-V0.1.1-full.bin')
parser.add_argument('--erase', action='store_true', help='First installation: erase factory firmware and NVS; deletes stored settings')
args = parser.parse_args()
if not args.erase:
    parser.error('The full image is for first installation. Use --erase; it deletes existing firmware and settings. For CM-Radio updates use PlatformIO upload.')
image = args.image.resolve()
if not image.is_file():
    parser.error('Firmware image not found: '+str(image))
checksum_file = image.parent/'SHA256SUMS'
if checksum_file.is_file():
    expected = dict(line.split('  ', 1)[::-1] for line in checksum_file.read_text().splitlines())
    if image.name not in expected or hashlib.sha256(image.read_bytes()).hexdigest() != expected[image.name]:
        parser.error('Firmware checksum mismatch')
base = [sys.executable, '-m', 'esptool', '--chip', 'esp32', '--port', args.port, '--baud', '460800']
# Read before mutation: a wrong flash capacity must not receive this layout.
probe = subprocess.run(base+['flash_id'], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(probe.stdout)
if 'Detected flash size: 8MB' not in probe.stdout:
    parser.error('This image requires detected 8MB flash; flashing aborted')
if args.erase:
    subprocess.run(base+['erase_flash'], check=True)
subprocess.run(base+['write_flash', '--flash_mode','dio','--flash_freq','40m','--flash_size','8MB','0x0',str(image)], check=True)
print('Done. Open serial monitor at 115200 baud for setup SSID and password.')
