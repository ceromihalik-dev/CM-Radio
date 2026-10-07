#!/usr/bin/env python3
"""Read-only checks after flashing; makes no changes to volume or stations."""
import argparse
import json
from urllib.request import urlopen
parser = argparse.ArgumentParser()
parser.add_argument('address', help='http://cm-radio.local or http://192.168.x.x')
args = parser.parse_args()
def get(path):
    with urlopen(args.address.rstrip('/')+'/api/v1/'+path, timeout=10) as response:
        assert response.status == 200
        return json.load(response)
status = get('status')
stations = get('stations')['stations']
config = get('config')
assert status['name'] == 'CM-Radio'
assert status['version'] == '0.1.0'
assert status['flashBytes'] == 8*1024*1024
assert status['psramBytes'] >= 2*1024*1024
assert status['audioReady'] is True
assert status['storageReady'] is True
assert 0 <= status['volume'] <= 21
assert 1 <= len(stations) <= 10
assert 0 <= status['stationIndex'] < len(stations)
assert 'password' not in config
assert status['wifiConnected'] is True
print('API / Wi-Fi / Flash / PSRAM / Audio initialization: PASS')
print('Playback state:', status['state'], '| volume:', status['volume'])
print('Physical stereo and restart tests remain manual; see docs/TESTPLAN.md.')
