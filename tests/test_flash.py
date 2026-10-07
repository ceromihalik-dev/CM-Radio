"""Verify that first flashing cannot mutate the wrong target or bad bytes."""
import contextlib
import hashlib
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1]/'scripts/flash.py'
class FlashTests(unittest.TestCase):
    def invoke(self, output='Detected flash size: 8MB', erase=True, corrupt=False):
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory)/'CM-Radio-V0.1.0-full.bin'
            image.write_bytes(b'checked-test-fixture')
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            (image.parent/'SHA256SUMS').write_text(digest+'  '+image.name+'\n')
            if corrupt:
                image.write_bytes(b'wrong-bytes')
            def run(command, **kwargs):
                calls.append(command)
                return subprocess.CompletedProcess(command, 0, stdout=output)
            argv = [str(SCRIPT), '--port', 'TESTPORT', '--image', str(image)]
            if erase:
                argv.append('--erase')
            exit_code = 0
            with patch.object(sys, 'argv', argv), patch('subprocess.run', side_effect=run), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                try:
                    runpy.run_path(str(SCRIPT), run_name='__main__')
                except SystemExit as e:
                    exit_code = e.code
        return exit_code, calls

    def test_requires_explicit_first_installation(self):
        code, calls = self.invoke(erase=False)
        self.assertEqual(code, 2)
        self.assertEqual(calls, [])
    def test_corrupt_image_never_probes_or_writes(self):
        code, calls = self.invoke(corrupt=True)
        self.assertEqual(code, 2)
        self.assertEqual(calls, [])
    def test_wrong_capacity_never_erases_or_writes(self):
        code, calls = self.invoke(output='Detected flash size: 4MB')
        self.assertEqual(code, 2)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][-1], 'flash_id')
    def test_valid_target_probe_erase_write_order(self):
        code, calls = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][-1], 'flash_id')
        self.assertEqual(calls[1][-1], 'erase_flash')
        self.assertIn('write_flash', calls[2])
        self.assertEqual(calls[2][-2], '0x0')
        self.assertIn('8MB', calls[2])

if __name__ == '__main__':
    unittest.main()
