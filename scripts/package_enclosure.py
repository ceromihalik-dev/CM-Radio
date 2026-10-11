#!/usr/bin/env python3
"""Build verified enclosure assets for the same release as the firmware.

No firmware image is compiled or changed. Never label the CAD check as a
physical print or resin insert mounting acceptance.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT/'hardware/enclosure/designs'
PRINT_ZIP = 'CM-Radio_Modell_3_Retro_JLC3DP_V03_R8.zip'
FUSION_ZIP = 'CM-Radio_Modell_3_Retro_Fusion_STEP_V03_R8.zip'
PDF_NAME = 'CM-Radio_Retro_R8_Explosion_Materialliste.pdf'


def firmware_release():
    tree = ast.parse((ROOT/'scripts/package_firmware.py').read_text())
    assignments = [n for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'manifest' for t in n.targets)]
    value = assignments[0].value
    assert isinstance(value, ast.Dict)
    manifest = {ast.literal_eval(k):ast.literal_eval(v) for k,v in zip(value.keys,value.values)
                if isinstance(k, ast.Constant) and k.value in ('version','build')}
    return manifest['version'], manifest['build']


def run(name, root, *extra):
    subprocess.run([sys.executable, str(DESIGNS/name), str(root), *extra], check=True, cwd=ROOT)


def checksums(root):
    lines = [hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix()
             for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'SHA256SUMS.txt']
    (root/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')


def archive(root, output):
    checksums(root)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(root).as_posix())
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        names = set(z.namelist())
        for required in [PDF_NAME, 'USB_ERSTINSTALLATION.txt', 'RESIN_HINWEIS_R8.md',
                         'MATERIALLISTE_R8.md', 'DRUCKMATERIALIEN_R8.md', 'QUELLSTAND.json']:
            assert required in names, (output.name, required)
        for line in z.read('SHA256SUMS.txt').decode().splitlines():
            digest, name = line.split('  ', 1)
            assert hashlib.sha256(z.read(name)).hexdigest() == digest, name


def build(output, reuse=None):
    from enclosure_pdf import create
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    work = output/'CAD_BUILD'
    if reuse:
        shutil.copytree(Path(reuse)/'Retro', work/'Retro', dirs_exist_ok=True)
    else:
        run('make_retro_r8.py', work)
        run('check_retro_r4.py', work)
        run('check_retro_r8.py', work)
        run('check_front.py', work, '--design', 'Retro')
        run('make_retro_r8_probe.py', work)
        run('render_retro_r8.py', work)
        run('render_retro_r8_exploded.py', work)
    root = work/'Retro'
    assert len(list((root/'STL_DRUCK').glob('*.stl'))) == 5
    assert len(list((root/'STEP_EINZELTEILE').glob('*.step'))) == 5
    geometry = json.loads((root/'PRUEFUNG/Geometrie_R8.json').read_text())
    assert len(geometry['parts']) == 5
    assert all(p['stl_watertight'] and p['step_roundtrip'] for p in geometry['parts'].values())
    assert json.loads((root/'PRUEFUNG/Integration_R8.json').read_text())['result'] == 'PASS'
    for name in ['RETRO_R8_MONTAGE.md','MATERIALLISTE_R8.md','DRUCKMATERIALIEN_R8.md','RESIN_HINWEIS_R8.md']:
        shutil.copy2(DESIGNS/name, root/name)
    shutil.copy2(DESIGNS/'JLC3DP_ABGLEICH_R8.json', root/'PRUEFUNG/Herstellerabgleich_R8.json')
    shutil.copy2(ROOT/'LICENSE', root/'LICENSE')
    shutil.copy2(ROOT/'docs/ERSTSTART.md', root/'ERSTSTART.md')
    version, build_number = firmware_release()
    guide = (ROOT/'docs/USB_ERSTINSTALLATION.txt').read_text(encoding='utf-8')
    guide = guide.replace('{VERSION}', version).replace('{BUILD}', build_number)
    guide = guide.replace('{FULL_IMAGE}', f'CM-Radio-V{version}-full.bin')
    prefix = ('Hinweis zum Gehäusepaket V0.3 R8\n\n'
              'Dieses ZIP enthält Gehäuse-CAD, keine Firmware-Binärdateien.\n'
              'Ein Gehäusewechsel erfordert keine Neuinstallation des eingerichteten Radios.\n'
              'Für ein neues Board das separate Firmware-ZIP aus demselben Release herunterladen.\n'
              'Alle Flashbefehle im vollständig entpackten Firmware-Ordner ausführen.\n'
              f'https://github.com/ceromihalik-dev/CM-Radio/releases/tag/v{version}-build{build_number}\n\n')
    (root/'USB_ERSTINSTALLATION.txt').write_text(prefix+guide, encoding='utf-8')
    source = root/'QUELLTEXT'
    source.mkdir(exist_ok=True)
    for name in ['CM-Radio_Gehaeuse.py','parameter.json','requirements.txt']:
        shutil.copy2(ROOT/'hardware/enclosure'/name, source/name)
    shutil.copytree(DESIGNS, source/'designs', dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copytree(ROOT/'hardware/enclosure/measurements', root/'MESSWERTE', dirs_exist_ok=True)
    commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True).strip())
    status = {'source_commit':commit, 'source_dirty':dirty, 'enclosure':'V0.3 R8',
              'firmware_release':f'v{version}-build{build_number}', 'firmware_modified':False,
              'cad_checked':True, 'physical_fit_R8':'PENDING', 'resin_mounting_adaptation':'PENDING',
              'manufacturing_choice':'SLA resin; exact grades and colors not confirmed',
              'geometry_changed_for_resin':False}
    (root/'QUELLSTAND.json').write_text(json.dumps(status, indent=2)+'\n')
    (root/'STUECKLISTE_BESTELLUNG.json').write_text(json.dumps({
        'printed_parts':[{'file':p.name,'quantity':1,'material':'SLA Resin (per actual order)',
                          'color':'Per actual order'} for p in sorted((root/'STL_DRUCK').glob('*.stl'))],
        'hardware_reference':[{'name':'ruthex RX-M3Sx4.0 SHORT','quantity':4},
                              {'name':'ruthex RX-M2x4','quantity':6},
                              {'name':'M3x8 countersunk head <=5.6 mm','quantity':4},
                              {'name':'M2x6 pan head <=3.8 mm, height <=1.5 mm','quantity':6}],
        'insert_installation':'Resin: no heat; existing pilot holes require adaptation and sample test before glue installation',
        'resin_ready_insert_holes':False,
        'customs_description':'3D-printed resin (plastic) enclosure parts. No electronic components included.'},
        indent=2)+'\n')
    (root/'AENDERUNGEN_R8.txt').write_text(
        'V0.3 R8: offene Lüftung; Klebefront; 5 Druckteile; kein Display.\n'
        'Release-Paket: aktuelle Explosion, Materialliste, USB-Anleitung und CAD-Quellen.\n'
        'Resin-Fertigung laut Nutzerentscheid; konkrete Sorte/Farbe nicht bestätigt.\n'
        'R8-Geometrie unverändert; Resin-Gewindeaufnahmen nicht automatisch angepasst.\n'
        'RESIN_HINWEIS_R8.md vor Fertigung/Montage lesen.\n', encoding='utf-8')
    pdf = create(root)
    fusion = output/'FUSION_BUILD'
    shutil.copytree(root, fusion, dirs_exist_ok=True)
    shutil.rmtree(fusion/'STL_DRUCK')
    for p in fusion.rglob('*.stl'):
        p.unlink()
    archive(root, output/PRINT_ZIP)
    archive(fusion, output/FUSION_ZIP)
    shutil.copy2(pdf, output/PDF_NAME)
    shutil.copy2(root/'CM-Radio_Retro_R8_Explosionszeichnung.png', output/'CM-Radio_Retro_R8_Explosionszeichnung.png')
    shutil.copy2(root/'CM-Radio_Retro_R8_Materialliste.csv', output/'CM-Radio_Retro_R8_Materialliste.csv')
    files = [PRINT_ZIP,FUSION_ZIP,PDF_NAME,'CM-Radio_Retro_R8_Explosionszeichnung.png','CM-Radio_Retro_R8_Materialliste.csv']
    (output/'SHA256SUMS_Gehaeuse_R8.txt').write_text(''.join(
        hashlib.sha256((output/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in files))
    print(json.dumps({'release':status['firmware_release'],'output':str(output),'assets':files,
                      'ZIP_integrity':'PASS','physical_R8':'PENDING'}, indent=2), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=ROOT/'dist/enclosure-release')
    p.add_argument('--reuse-cad', type=Path, help='Use previously validated local CAD exports; never used in CI')
    args = p.parse_args()
    build(args.output, args.reuse_cad)
