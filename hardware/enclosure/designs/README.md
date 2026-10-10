# CM-Radio Retro und Wave – V0.3 R1

Parametrische Gehäusevarianten für das gelieferte Loud-ESP32 E3, mit denselben
Platinen- und Anschlusskoordinaten wie V0.2 W4. Die Designbilder sind optische
Referenzen; maßgeblich ist die erzeugte CAD-Geometrie.

Retro: gerippte Front, separater Fronteinsatz, vier M3-Senkschrauben von vorne,
104 × 80 × 35,8 mm, fünf Druckteile. Wave: zwei breite gekrümmte Vertiefungen,
Front ohne Schraubenköpfe, vier M3-Senkschrauben von hinten,
104 × 80 × 34,2 mm, vier Druckteile.

JLC3DP-Auslegung: Nylon SLS/MJF; 2,4-mm-Wände und Rückwand, 2-mm-Führungsrand,
0,6 mm Fügespiel je Seite und 0,6 mm radiales Resetspiel. Kabelöffnungen nominal
3 mm; nach dem Druck am vorhandenen Kabel prüfen/nachreiben. Mikrogewinde sind
nicht mitgedruckt: M3-Vorbohrungen müssen kontrolliert und nachgeschnitten werden.

```sh
python -m pip install cadquery==2.7.0 'trimesh>=4,<5' numpy pillow
python hardware/enclosure/designs/make_designs.py --out output/Gehaeuse_V03
python hardware/enclosure/designs/render_designs.py output/Gehaeuse_V03
```

Die Erzeugung prüft gültige Ein-Körper-Geometrie, STL-Wasserdichtheit und
Normalenorientierung, STEP-Reimport und Montagekollisionen einschließlich
gedrücktem Resetknopf. Vorschauen werden aus tatsächlicher STEP-Geometrie
gerendert. Die vereinfachte PCB-Referenz bildet nicht jedes Bauteil ab;
Druckpassung und tatsächliche Bauteilabstände sind am ersten Exemplar zu prüfen.

Retro-Materialempfehlung: 3301PA Nylon SLS, weiß, außen salbeigrün/elfenbein
lackiert. Wave: PA12S-HP Nylon MJF, Unterteil schwarz, Deckel grau mit
petrolfarbener Außenlackierung. Wunschlackierung vor Auftrag vom Anbieter
bestätigen lassen; Passflächen und Resetführung nicht lackieren.

Herstellerquellen, Stand 10.10.2026:

- https://jlc3dp.com/help/article/3d-printing-design-guideline
- https://jlc3dp.com/help/article/3301pa-nylon
- https://jlc3dp.com/help/article/pa12s-hp-nylon
- https://jlc3dp.com/capabilities/3d-printing-service

Die Druckpakete enthalten Einzel-STLs und Einzel-STEPs, getrennte
Ansichtsbaugruppe, Prüfdaten, CAD-Vorschau, Quelltext und konkrete
Bestell-/Montagehinweise. Nur Einzelteile bestellen, keine Baugruppe als ein
Teil. Keine IP-/Spritzwasserschutz-Zertifizierung.
