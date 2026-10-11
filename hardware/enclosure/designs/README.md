Aktueller Druckstand für Modell 3: **V0.3 R6 ohne Display**.
R4-Anschlussgeometrie mit bestätigten Kabelauslässen; Platinen-Piloten jetzt
Ø 2,0 × 5 mm, Reset-Piloten Ø 2,0 × 5 mm statt nur 3 mm tief.
M3-Piloten Ø 2,5 × 6 mm, nachzuschneidendes Gewinde. Alle zehn Kernlöcher
am reimportierten STEP vermessen; CAD-Prüfung ersetzt keine Schrauben-Passprobe.
Siehe [RETRO_R6_MONTAGE.md](RETRO_R6_MONTAGE.md).

```sh
python hardware/enclosure/designs/make_designs.py --design Retro --revision R6 --out output/Retro_R6
python hardware/enclosure/designs/check_retro_r4.py output/Retro_R6
python hardware/enclosure/designs/check_retro_r6_screws.py output/Retro_R6
python hardware/enclosure/designs/check_front.py output/Retro_R6 --design Retro
python hardware/enclosure/designs/make_retro_r6_probe.py output/Retro_R6
python hardware/enclosure/designs/render_retro_r6.py output/Retro_R6
```

**V0.3 R5 Display** ist als separater Prototyp zurückgestellt.
Neuer Deckel, Fronteinsatz und U-Displayhalter; R4-Unterteil unverändert.
Elecrow-Flex: ca. 50 mm freie Kabellänge vom Anwender bestätigt. Panelmaß
nach verlinkter Zeichnung; 0,7-mm-Zeichnungsvariante nicht mit dem 0,5-mm-Board
verwechseln. Siehe [RETRO_R5_DISPLAY_MONTAGE.md](RETRO_R5_DISPLAY_MONTAGE.md).

Displayfreie Referenz: **V0.3 R4** – linker Kabelauslass um 10 mm
nach rechts versetzt, Kabel rechts an der linken Öse vorbei; kompletter Kabelweg kollisionsgeprüft.
Siehe [RETRO_R4_MONTAGE.md](RETRO_R4_MONTAGE.md). R3 ist durch R4 ersetzt.

# CM-Radio – Retro V0.3 R3 und Wave V0.3 R2

Retro R3 setzt die am 11.10.2026 bestätigten Anschlussmaße um: zwei komplette
Ø-4,5-mm-Kabelbohrungen in der unteren USB-Kante, Oberkante 0,95 mm unter der
PCB-Unterseite; USB als geschlossener Ausschnitt vollständig im Unterteil,
ohne Deckelzungen. Neue niedrige seitliche Kabelbinderösen liegen nahe den
Kabelbohrungen. Die Kabel werden daneben auf dem Boden geführt. IR erhält
einen vorläufigen 8/6-mm-Trichter an der gemessenen Position. Ausführliche
Maße und Montagehinweise: [RETRO_R3_MONTAGE.md](RETRO_R3_MONTAGE.md).

```sh
python hardware/enclosure/designs/make_designs.py --design Retro --revision R3 --out output/Retro_R3
python hardware/enclosure/designs/check_retro_r3.py output/Retro_R3
python hardware/enclosure/designs/check_front.py output/Retro_R3 --design Retro
python hardware/enclosure/designs/render_designs.py output/Retro_R3 --design Retro
```

Ohne `--revision R3` bleibt die bisherige R2-Geometrie reproduzierbar.
Wave R2 wird durch die Retro-R3-Anschlussänderungen nicht verändert.

## Bestehende R2-Referenz

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
