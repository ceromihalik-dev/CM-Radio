# CM-Radio Retro und Wave – V0.3 R2

Parametrische Gehäusevarianten für das gelieferte Loud-ESP32 E3, mit denselben
Platinen- und Anschlusskoordinaten wie V0.2 W4. Die Designbilder sind optische
Referenzen; maßgeblich ist die erzeugte CAD-Geometrie.

Retro: zehn kräftige Rippen mit rundem Querschnitt, breiter separater
Fronteinsatz mit weicher Kante, vier M3-Senkschrauben von vorne,
104 × 80 × 36,0 mm, fünf Druckteile. Wave: zwei breite modellierte Wellen,
Front ohne Schraubenköpfe, vier M3-Senkschrauben von hinten,
104 × 80 × 35,8 mm, vier Druckteile.

R2 setzt die gewählten Designvorlagen stärker um: Retro hat fünf statt drei
Rippen pro Band, 2,15 mm Rippenhöhe und 1,1 mm Kopfradius. Der elfenbeinfarbene
Einsatz ist 80 statt 72 mm breit und hat eine 0,8-mm-Kantenrundung. Wave ersetzt
die flachen R1-Gravuren durch eine echte kubische B-Spline-Oberfläche mit
2 mm Höhenänderung, ungefähr 8,8 mm breiten Übergängen und einem sanft
abfallenden Rand. Die Teilezahl und die inneren Hardwarekoordinaten bleiben
erhalten. Das Radiozeichen schneidet nicht mehr in die Resetöffnung hinein.
Seitlich erhält Retro je drei senkrechte, Wave je neun waagerechte Schlitze,
jeweils mit runden Enden und 2,4 mm Breite, entsprechend der Designvorlage.

Die Designbilder verlegen die Kabel gemeinsam nach unten und den Resetknopf
unter das Logo. Hier bleiben USB, Lautsprecherkabel und Reset an den passenden
Stellen für die gemessene Platine. Ohne versetzte Resetmechanik entspricht die
Anordnung deshalb nicht exakt dem optischen Konzept.

JLC3DP-Auslegung: Nylon SLS/MJF; 2,4-mm-Wände und Rückwand, 2-mm-Führungsrand,
0,6 mm Fügespiel je Seite und 0,6 mm radiales Resetspiel. Kabelöffnungen nominal
3 mm; nach dem Druck am vorhandenen Kabel prüfen/nachreiben. Mikrogewinde sind
nicht mitgedruckt: M3-Vorbohrungen müssen kontrolliert und nachgeschnitten werden.

```sh
python -m pip install cadquery==2.7.0 'trimesh>=4,<5' numpy pillow
python hardware/enclosure/designs/make_designs.py --out output/Gehaeuse_V03
python hardware/enclosure/designs/check_front.py output/Gehaeuse_V03
python hardware/enclosure/designs/render_designs.py output/Gehaeuse_V03
```

Die Erzeugung prüft gültige Ein-Körper-Geometrie, STL-Wasserdichtheit und
Normalenorientierung, STEP-Reimport und Montagekollisionen einschließlich
gedrücktem Resetknopf. Vorschauen werden aus tatsächlicher STEP-Geometrie
gerendert. Die vereinfachte PCB-Referenz bildet nicht jedes Bauteil ab;
Druckpassung und tatsächliche Bauteilabstände sind am ersten Exemplar zu prüfen.

`check_front.py` tastet die tatsächliche STEP-Front senkrecht in einem
2-mm-Raster und zusätzlich am Rand ab. Bei Wave prüft es außerdem mindestens
1,8 mm Höhenunterschied zwischen zwei festgelegten Flächenpunkten. Diese
Prüfung erkennt einen verlorenen Oberflächenschnitt auch bei formal gültigem
STL/STEP. Sie ist keine vollständige Analyse aller Wandstärken. Das Wave-
Parametermaß `lid_thickness=6.0` bezeichnet den CAD-Rohling; seine fertige
Front wird auf maximal Z=35,8 mm getrimmt.

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
