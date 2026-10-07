import copy
import importlib.util
import json
from pathlib import Path
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
spec = importlib.util.spec_from_file_location('smoke', Path(__file__).resolve().parents[1] / 'scripts/smoke_test.py')
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.status = dict(name='CM-Radio', version='0.1.0', flashBytes=8388608,
                           psramBytes=4194304, audioReady=True, storageReady=True,
                           wifiConnected=True, setupActive=False, settingsPending=False,
                           volume=5, stationIndex=0, autoplay=True, state='streaming')
        self.stations = [dict(name='Test', url='https://example.org/private-token')]
        self.config = dict(ssid='PRIVATE-SSID', autoplay=True)
    def evaluate(self):
        return smoke.evaluate(self.status, self.stations, self.config, '0.1.0')
    def test_valid_board(self):
        self.assertTrue(all(c['result'] == 'PASS' for c in self.evaluate()))
    def test_faults_and_boolean_indices(self):
        for key, value in [('flashBytes', 4194304), ('audioReady', False), ('volume', True),
                           ('stationIndex', True), ('psramBytes', 0), ('storageReady', False),
                           ('wifiConnected', False), ('version', 'other'), ('settingsPending', True)]:
            with self.subTest(key=key):
                original = copy.deepcopy(self.status)
                self.status[key] = value
                self.assertTrue(any(c['result'] == 'FAIL' for c in self.evaluate()))
                self.status = original
    def test_missing_station_list_and_password(self):
        self.stations = None
        self.config['password'] = 'DO-NOT-RECORD'
        result = self.evaluate()
        self.assertTrue(any(c['result'] == 'FAIL' for c in result))
        self.assertNotIn('DO-NOT-RECORD', json.dumps(result))
    def test_readonly_http_and_redacted_report(self):
        payloads = {'status': self.status, 'stations': {'stations': self.stations}, 'config': self.config}
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(('GET', self.path))
                data = json.dumps(payloads[self.path.rsplit('/', 1)[-1]]).encode()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            report = smoke.run('http://127.0.0.1:' + str(server.server_port))
            self.assertEqual(report['result'], 'PASS')
            self.assertEqual(report['hardwareAcceptance'], 'OPEN')
            self.assertEqual(requests, [('GET', '/api/v1/' + p) for p in ('status', 'stations', 'config')])
            for secret in ('PRIVATE-SSID', 'private-token', '127.0.0.1'):
                self.assertNotIn(secret, json.dumps(report))
            payloads['status'] = []
            self.assertEqual(smoke.run('http://127.0.0.1:' + str(server.server_port))['result'], 'FAIL')
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    def test_offline_board(self):
        self.assertEqual(smoke.run('http://127.0.0.1:1', timeout=.1)['result'], 'FAIL')
    def test_address(self):
        for address in ('https://radio', 'http://user:secret@radio', 'http://radio/path', 'http://radio:bad'):
            with self.assertRaises(Exception):
                smoke.base_address(address)
        self.assertEqual(smoke.base_address('http://cm-radio.local/'), 'http://cm-radio.local')

if __name__ == '__main__':
    unittest.main()
