"""Join lossless model archives and extract the original STL/STEP files."""
from pathlib import Path
from zipfile import ZipFile
root = Path(__file__).resolve().parent
for folder in [root/'STL', root/'STEP']:
    for first in sorted(folder.glob('*.zip.001')):
        target = first.with_suffix('')
        parts = sorted(folder.glob(target.name+'.[0-9][0-9][0-9]'))
        if [p.suffix for p in parts] != [f'.{i:03d}' for i in range(1, len(parts)+1)]:
            raise SystemExit('Missing archive part: '+target.name)
        target.write_bytes(b''.join(p.read_bytes() for p in parts))
    for archive in sorted(folder.glob('*.zip')):
        with ZipFile(archive) as package:
            bad = package.testzip()
            if bad:
                raise SystemExit('Corrupt model archive: '+bad)
            package.extractall(folder)
        print('Extracted:', archive.name)
