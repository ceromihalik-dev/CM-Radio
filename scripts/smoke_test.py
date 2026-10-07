#!/usr/bin/env python3
"""Read-only board checks with a redacted acceptance report."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, ProxyHandler

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def base_address(value):
    parsed = urlsplit(value)
    if (parsed.scheme != 'http' or not parsed.hostname or parsed.username
            or parsed.password or parsed.path not in ('', '/') or parsed.query or parsed.fragment):
        raise argparse.ArgumentTypeError('Adresse als http://GERAETE-IP ohne Pfad oder Zugangsdaten angeben')
    try:
        parsed.port
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Ungueltiger Port') from exc
    return value.rstrip('/')

def evaluate(status, stations, config, expected_version):
    checks = []
    def check(label, ok):
        checks.append({'check': label, 'result': 'PASS' if ok else 'FAIL'})
    def integer(value):
        return type(value) is int
    check('Projektname', status.get('name') == 'CM-Radio')
    check('Firmwareversion', status.get('version') == expected_version)
    check('Flash 8 MB', status.get('flashBytes') == 8388608)
    psram = status.get('psramBytes')
    check('PSRAM mindestens 2 MB nutzbar', integer(psram) and psram >= 2097152)
    check('Audio initialisiert', status.get('audioReady') is True)
    check('Einstellungsspeicher bereit', status.get('storageReady') is True)
    check('Heim-WLAN verbunden', status.get('wifiConnected') is True)
    check('Setup-WLAN beendet', status.get('setupActive') is False)
    check('Einstellungen gespeichert', status.get('settingsPending') is False)
    volume = status.get('volume')
    check('Lautstaerke 0 bis 21', integer(volume) and 0 <= volume <= 21)
    valid_list = isinstance(stations, list) and 1 <= len(stations) <= 10
    check('Senderliste 1 bis 10', valid_list)
    index = status.get('stationIndex')
    check('Senderauswahl gueltig', valid_list and integer(index) and 0 <= index < len(stations))
    check('Sender besitzen Name und URL', valid_list and all(
        isinstance(s, dict) and isinstance(s.get('name'), str) and bool(s['name'].strip())
        and isinstance(s.get('url'), str) and s['url'].startswith(('http://', 'https://')) for s in stations))
    check('Kein WLAN-Passwort in API', all(
        not any('password' in key.lower() or 'passwort' in key.lower() for key in obj)
        for obj in (status, config)))
    check('Autostart-Konfiguration gueltig', type(config.get('autoplay')) is bool
          and status.get('autoplay') is config.get('autoplay'))
    check('Playerzustand gueltig', status.get('state') in ('stopped', 'connecting', 'streaming', 'error'))
    return checks

def run(address, expected_version='0.1.0', timeout=10):
    # Local radio requests bypass proxies; redirects and unbounded replies are rejected.
    opener = build_opener(ProxyHandler({}), NoRedirect())
    payloads, checks = {}, []
    for endpoint in ('status', 'stations', 'config'):
        try:
            with opener.open(address + '/api/v1/' + endpoint, timeout=timeout) as response:
                if response.status != 200:
                    raise ValueError('HTTP status')
                data = response.read(32769)
                if len(data) > 32768:
                    raise ValueError('Response too large')
                payload = json.loads(data)
                if not isinstance(payload, dict):
                    raise ValueError('JSON object required')
                payloads[endpoint] = payload
            checks.append({'check': 'API ' + endpoint, 'result': 'PASS'})
        except Exception:
            # Never retain raw replies or exception text containing device secrets.
            checks.append({'check': 'API ' + endpoint, 'result': 'FAIL'})
    if len(payloads) == 3:
        checks.extend(evaluate(payloads['status'], payloads['stations'].get('stations'),
                               payloads['config'], expected_version))
    return {'project': 'CM-Radio', 'expectedFirmware': expected_version,
            'testedAtUtc': datetime.now(timezone.utc).isoformat(),
            'result': 'PASS' if all(c['result'] == 'PASS' for c in checks) else 'FAIL',
            'hardwareAcceptance': 'OPEN', 'checks': checks,
            'manualTests': ['Stereo-Hoerprobe', 'Stromneustart und Autostart',
                            'WLAN-Ausfall und Wiederanlauf', '60-Minuten-Dauertest',
                            'Gehaeusepassung und Temperatur']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('address', type=base_address, help='http://cm-radio.local oder http://GERAETE-IP')
    parser.add_argument('--expected-version', default='0.1.0')
    parser.add_argument('--report', type=Path, help='JSON-Ergebnisbericht ohne WLAN- und Senderdaten')
    args = parser.parse_args()
    report = run(args.address, args.expected_version)
    for item in report['checks']:
        print(item['result'] + '  ' + item['check'])
    print('Gesamt: ' + report['result'] + '; physische Hardware-Abnahme bleibt OFFEN.')
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('Ergebnisbericht gespeichert.')
    return 0 if report['result'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
