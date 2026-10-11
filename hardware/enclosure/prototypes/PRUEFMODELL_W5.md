# CM-Radio – Prüfmodell V0.2 W5

Dieses Modell dient dem erneuten Passungstest am vorhandenen Loud-ESP32 E3.
Es verwendet die bewährte W4-Grundform mit 104 × 80 × 32,4 mm Außenmaßen.
Die dekorative Retro-Front ist noch kein Bestandteil dieses Prüfmodells.
Alle Maße und Dateieinheiten sind Millimeter. Keine sichtbare Versionsnummer.

## Änderungen und bestätigte Maße

- Platinen-Lochraster weiterhin **58 × 49 mm**, von Lochmitte zu Lochmitte.
- Beide Lautsprecher-Kabelauslässe **Ø 4,5 mm** an der nach unten gerichteten
  USB-Kante bei Wandmontage. Die bisherigen gegenüberliegenden Öffnungen
  sind geschlossen. Die Deckelzungen schließen die neuen Ausschnitte.
- Trichterförmige IR-Öffnung auf der USB-Seite: **Ø 8 mm außen / Ø 6 mm innen**
  über die 2,4-mm-Wand. Diese beiden Durchmesser sind vorläufig gewählt;
  die tatsächliche schwarze Empfangsfläche ist noch nicht vermessen.
- IR-Mitte: **10 mm rechts vom rechten Metallrand der 9 mm breiten USB-Buchse**,
  entsprechend 14,5 mm rechts von USB-Mitte; **5 mm über Platinenoberseite**.
  CAD-Mitte X=34,7 / Z=16,1 mm. Nach der gemessenen Höhe liegt die IR-Mitte
  14 mm unterhalb der Unterteiloberkante, im CAD 13,9 mm.
- USB-Öffnung unverändert: nominal 18 mm breit, Unterkante Z=8,4 mm,
  Oberkante bei geschlossenem Deckel Z=18,6 mm. Buchse 9 × 3 mm,
  verwendetes Steckergehäuse **12 × 8 mm**. Tatsächlich gemessener
  Freiraum unter dem Stecker: **1 mm**.
- PCB-Unterseite Z=9,4 mm, Oberseite Z=11,1 mm; Abstand zum Unterteilrand
  18,9 mm im CAD, gemessen 19 mm. Platinenstärke 1,7 mm.
- Platinenhalter, Wand-Schlüssellöcher, Resetknopf und Halteplatte behalten
  ihre W4-Maße. Die vorhandenen Kabelbinderhalter bleiben an ihren Positionen;
  die Kabel von den neuen unteren Auslässen innen zu diesen Haltern führen.

## Dateien und Druck

`STL_DRUCK`: Unterteil, Deckel, Resetknopf, Reset-Halteplatte und optionale
Lochrasterprobe. Alle fünf Dateien sind separate geschlossene Volumenkörper
und auf Z=0 gesetzt. Die Baugruppe ist ausschließlich zur Ansicht bestimmt.

Im Slicer **100 % Skalierung** einstellen; keine automatische Größenanpassung.
Bei deinem W4-Ausdruck wurden 58 × 50 mm statt 58 × 49 mm gemessen. Die
CAD-Abstände bleiben 58 × 49 mm; zunächst die kleine Lochrasterprobe drucken
und am Board vergleichen. Bei abweichendem Druck zuerst die Achsenskalierung
und den Messbezug prüfen, bevor das komplette Gehäuse gedruckt wird.

Für einen FDM-Passungstest: 0,2 mm Schichthöhe, 3–4 Wände, 25–35 % Füllung;
dies sind Ausgangswerte, die an deinen Drucker anzupassen sind. PETG eignet
sich für den Gehäusetest. Unterteil mit Rückwand auf dem Druckbett, Deckel
mit Außenfläche nach unten, Halteplatte flach. Diese Orientierung ist in den
STL-Dateien vorbereitet. Kleine Druckhilfen abhängig von der Bettanhaftung.

Resetknopf steht in der Datei auf seiner 2,5-mm-Kontaktspitze. Brim verwenden,
Stützen unter Schaftabsatz und Kragen, anschließend die Gleitflächen glätten.
Ein vorhandener W4-Knopf und die W4-Halteplatte können wiederverwendet werden.
Unterteil und Deckel müssen für W5 beide neu gedruckt werden.

Die IR-Öffnung ist ein horizontaler Trichter; bei eingeschalteter automatischer
Stützgenerierung prüfen, ob Stützen in den optischen Kanal gesetzt werden.
Nach dem Druck alle Stützreste und Grate entfernen, ohne den Empfänger zu
berühren. Kabelöffnungen entgraten; das Kabel darf nicht am Mantel scheuern.

## Montage und Prüfung am Board

1. Stromversorgung trennen. Board spannungsfrei auf die vorhandenen Halter
   setzen. Alle vier Bohrungen müssen passen; Platine nicht verbiegen.
   Die bisherigen M2,5-Platinenschrauben verwenden und die Länge prüfen.
2. USB-Stecker vollständig einstecken. Freiraum links, rechts, oben und unten
   prüfen; die Buchse darf beim Einstecken nicht seitlich belastet werden.
3. Ohne Deckel durch den IR-Trichter schauen: Die Empfangsfläche muss mittig
   und frei sichtbar sein. Bei Verdeckung Durchmesser und tatsächliche Mitte
   messen; die 8/6-mm-Öffnung ist ein Prüfmaß.
4. Lautsprecherkabel durch die unteren Öffnungen führen. Den Verlauf innen
   so wählen, dass kein Kabel über den Resetmechanismus geführt wird und
   Deckelzungen nichts quetschen. An den vorhandenen Haltern zugentlasten.
5. Resetknopf von innen in die Führung stecken. Halteplatte mit den bisherigen
   zwei M2 × 6 mm Kunststoff-/Blechschrauben in den 1,6-mm-Pilotlöchern
   montieren; keine M2-Maschinenschrauben ohne vorbereitetes Gewinde verwenden.
6. Deckel zunächst ohne Strom vorsichtig auflegen. Der Knopf muss auf IO0
   ausgerichtet sein, 0,3 mm nominalen Ruheabstand haben, frei gleiten und nach
   Loslassen zurückkehren. Bei Klemmen entgraten; den Taster nicht vorspannen.
   Der bisherige maximale Knopfweg von 0,6 mm bleibt erhalten; der tatsächliche
   Schalterhub wurde noch nicht gemessen.
7. Deckel mit den vorhandenen M3-Schrauben schließen; Schraubenlänge prüfen.
   Prüfen, dass IR-Kanal und beide runden Kabelöffnungen frei bleiben.
8. Strom anschließen, ohne den Resetknopf gedrückt zu halten: IO0 beim Start
   aktiviert den Flashmodus. USB, Ton und IR-Empfang gerade von vorne sowie
   schräg von links/rechts prüfen. Die IR-Empfangsfunktion muss durch die
   verwendete Firmware/Fernbedienung unterstützt sein.
9. Wandaufnahme prüfen: 60 mm waagerechter Schraubenabstand, Schaft 3,5–4 mm,
   Kopf maximal Ø 8 mm und 3 mm hoch. Kopfunterseite zunächst ca. 3,5 mm
   von der Wand. Über die Köpfe setzen und nach unten schieben. Die Seite
   mit USB, IR und beiden Kabelöffnungen zeigt dabei nach unten.

Bitte die Ergebnisse als PASS oder mit dem abweichenden Maß zurückmelden:
Lochraster; USB-Passung; IR-Ausrichtung; Kabelführung; Deckelpassung;
Reset-Ausrichtung/Rückstellung; Wandmontage.

## Autodesk Fusion

Die STEP-Dateien enthalten echte CAD-Volumenkörper. Für die montierte Ansicht
`BAUGRUPPE_NICHT_DRUCKEN.step` importieren. Die fünf Einzeldateien stehen im
Ordner `STEP_EINZELTEILE` und haben dieselbe Orientierung wie die Druck-STLs.

In Fusion die STEP-Datei über die Datenverwaltung hochladen und nach der
Konvertierung öffnen. Projekt-/Dokumenteinheiten auf mm prüfen. Danach kann
das importierte Modell weiterbearbeitet und als Fusion-Entwurf gespeichert
werden. STEP enthält die Geometrie, aber nicht die ursprünglichen CadQuery-
Parameter oder eine native Fusion-Konstruktionshistorie. Die CAD-Parameter
stehen zusätzlich in `parameter_W5.json` und im Quelltext.

Autodesk-Dokumentation:
https://www.autodesk.com/de/support/technical/article/caas/sfdcarticles/sfdcarticles/DEU/File-formats-supported-by-Fusion-360.html
https://www.autodesk.com/products/fusion-360/blog/import-step-file-into-fusion-360/

## Technische Prüfung und Grenzen

Geprüft werden gültige Ein-Körper-Geometrie, geschlossene STL-Netze mit
konsistenter Orientierung, STEP-Reimport, Montagekollisionen einschließlich
gedrücktem Resetknopf, der IR-Trichterquerschnitt, die neuen Kabelöffnungen
und das Verschließen der alten oberen Kabelöffnungen. Die vereinfachte
Platinenreferenz bildet nicht alle elektronischen Bauteile ab. Diese Prüfungen
ersetzen die tatsächliche Montage-, Druckpassungs- und Empfangsprüfung nicht.
Dieses Paket ist ein Passungsprototyp, keine Freigabe des finalen Retro-Gehäuses.

## Quelltext erneut erzeugen

Aus dem Repository:
`python hardware/enclosure/prototypes/make_w5.py --out output/W5`

Aus dem entpackten Paket im Ordner `QUELLTEXT`:
`python -m pip install -r requirements.txt`
`python make_w5.py --out ../NEU_ERZEUGT`

Die Basisparameter liegen in `parameter.json`; W5-Änderungen werden in
`make_w5.py` ergänzt. Die Vorschau kann danach mit
`python render_w5.py ../NEU_ERZEUGT` aus dem STEP-Modell erzeugt werden.
