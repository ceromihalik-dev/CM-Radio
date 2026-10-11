# CM-Radio Modell 3 Retro – V0.3 R3

Stand: 11.10.2026. Einheiten **mm**, Maßstab **1:1 / 100 %**.
Dies ist die Weiterentwicklung des Retro-Gehäuses V0.3 R2 mit den jetzt
bestätigten Anschluss- und Kabelmaßen. Fünf Druckteile, Außenmaße
**104 × 80 × 36 mm**. Zehn runde Rippen, separater Fronteinsatz, vier sichtbare
Deckelschrauben, IO0-Resetmechanik und Wand-Schlüssellöcher bleiben erhalten.
Keine sichtbare Versionsnummer am Gehäuse.

## Änderungen gegenüber R2 und Prüfmodell W5

- Zwei **einfache, vollständig runde Ø-4,5-mm-Bohrungen** im Unterteil an der
  nach unten gerichteten USB-Kante. Keine Schlitze bis zum Rand und keine
  Deckelzungen für die Kabel mehr. Alte obere Kabelauslässe geschlossen.
- Bohrungsmitten X=68 und 87 mm, Z=6,2 mm über der äußeren Rückwand.
  Oberkante Z=8,45 mm, **0,95 mm unter der Platinenunterseite Z=9,4 mm**.
  Unterkante Z=3,95 mm; Abstand zur inneren Bodenfläche Z=2,4 mm: 1,55 mm.
- Zwei neue niedrige Kabelbinderösen neben den Kabelwegen: Mittelpunkte
  X=73/92 mm, Y=14 mm. Oberkante Z=6,4 mm. Tunnel quer zur Kabelrichtung,
  3,2 mm breit × 2 mm hoch, 5 mm lang; Dachstärke 1,7 mm, Seitenwände 1,6 mm.
  Die alten hohen Brücken im gegenüberliegenden Gehäusebereich entfallen.
- **USB-Ausschnitt komplett im Unterteil:** 18 × 10,2 mm, Radius 2 mm;
  Z=8,4 bis 18,6 mm. Über dem Ausschnitt bleibt die Gehäusewand geschlossen.
  Kein USB-Verschlusssteg am Deckel. Buchse 9 × 3 mm, Stecker 12 × 8 mm;
  am W4-Druck gemessener Freiraum unter dem Stecker 1 mm.
- IR-Trichter: **Ø 8 mm außen / Ø 6 mm innen**, durch die 2,4-mm-Wand.
  Mitte X=34,7 / Z=16,1 mm, also 10 mm rechts vom rechten Metallrand der
  USB-Buchse und 5 mm über Platinenoberseite. Durchmesser bleiben vorläufige
  Prüfmaße, bis Sichtfeld und Empfang am tatsächlichen Empfänger geprüft sind.
- Platinen-Lochraster weiterhin **58 × 49 mm**, Platinenstärke 1,7 mm,
  Unterteilhöhe 30 mm. Die gemessenen 19 mm Platinenoberseite bis Rand
  entsprechen den 18,9 mm der CAD-Konstruktion.

## Bestellen / drucken

Je **ein Teil** aus `STL_DRUCK` bestellen: Unterteil, Deckel, Fronteinsatz,
Resetknopf und Reset-Halteplatte. Alternativ dieselben Teile aus
`STEP_EINZELTEILE` verwenden; STL und STEP nicht doppelt bestellen.
`BAUGRUPPE_NICHT_DRUCKEN.step` dient ausschließlich der Ansicht.

Für JLC3DP weiterhin Nylon SLS/MJF als Auslegungsbasis: 2,4-mm-Wände und Boden,
2-mm-Führungsrand, 0,6 mm Deckelspiel je Seite und 0,6 mm radiales Resetspiel.
Die Fertigung und der konkrete Material-/Lackauftrag sind vom Anbieter zu prüfen.
Als bisheriges Materialziel: 3301PA Nylon SLS weiß, anschließend außen
Salbeigrün matt (RAL 6021), Fronteinsatz Elfenbein matt (RAL 1015).
Führung, Bohrungen, Gewindepiloten und Klebesitz nicht lackieren.
Schrift/Radiozeichen sind graviert; Farbe entsteht erst durch Farbauslegung.

FDM-Passungstest: nicht skalieren. Unterteil mit Rückwand auf dem Bett,
Fronteinsatz und Halteplatte mit flacher Unterseite auf dem Bett. Die Dateien
sind jeweils auf Z=0 gesetzt. Deckel in Montageorientierung mit Front oben:
im Slicer Brim und Stützen für die freitragende Frontplatte/Innenkonturen
vorsehen. Wegen Rippen und Tasche hat die Retro-Außenfläche keine vollständig
ebene Auflagefläche. Der Resetknopf benötigt Stützen unter dem Schaftabsatz
und Kragen; gegebenenfalls im Slicer umorientieren. Für einen Passungstest
können 0,2-mm-Schichten, 3–4 Wände und 25–35 % Füllung als Ausgangswerte dienen.
Alle Stützreste aus IR-Kanal, Kabelbohrungen und Kabelbinderösen entfernen.

## Zugentlastung und Verdrahtung

**Die Kabel liegen neben den Ösen auf dem Boden, nicht auf deren Dach.**
Ein dünner Kabelbinder (etwa 2,5 mm breit, passend zum 3,2 × 2-mm-Tunnel)
läuft durch den seitlich offenen Tunnel und um den Kabelmantel neben der Öse.
Den Kopf niedrig seitlich am Kabel platzieren; Kabelbinder nicht über die
Platine oder unter Bauteile zwingen. Nur so weit anziehen, dass der Mantel
gehalten und nicht gequetscht wird. Das Kabel darf nicht am Boardanschluss
ziehen. Vor Boardmontage probeweise einfädeln und die Rückhaltewirkung prüfen.

Die bisher gemessenen Lautsprecherkabel haben ca. Ø 3 mm; die Ø-4,5-mm-Bohrungen
bieten Montagespiel. Kabel von der Bohrungsmitte Z=6,2 mm nach innen sanft
auf den Boden führen. Freiraum zu Unterseitenbauteilen an der realen Platine
prüfen; diese Bauteile sind nicht vollständig im CAD modelliert.
Ist ein Stecker größer als Ø 4,5 mm, erst das unkonfektionierte Ende durch
die Bohrung führen und innen anschließen. Deckelöffnungen dafür sind nicht nötig.

## Montage

1. Strom trennen. Zunächst alle Teile entgraten und ohne Elektronik trocken
   zusammenbauen. Bohrungen, Führungen und Schraubenlängen prüfen.
2. Lautsprecherkabel durch die unteren runden Bohrungen führen, seitlich an
   den neuen Ösen zugentlasten. Kabel entlang des Bodens verlegen.
3. Board im 58 × 49-mm-Raster befestigen. Referenz: vier 2,5 × 6 mm
   Kunststoffschrauben, Kopf bis 4,5 mm; Länge und tatsächliche Lochpassung
   prüfen. Board nicht verspannen. Kabel und Binder dürfen keine Bauteile berühren.
4. USB vollständig einstecken: Stecker darf nicht an der Öffnung hebeln.
   Prüfen, dass die IR-Empfangsfläche durch den Trichter frei sichtbar ist.
5. Resetknopf von innen in den Deckel führen; Tastspitze zeigt zum IO0-Taster.
   Halteplatte mit zwei 2,5 × 6 mm Kunststoffschrauben, Kopf bis 5 mm,
   befestigen. Die 2-mm-Pilotlöcher vorher ohne Elektronik kontrollieren und
   gegebenenfalls nacharbeiten. Tastspitze nominal 0,3 mm über unbetätigtem
   IO0-Taster; maximaler Mechanikweg 0,6 mm, tatsächlicher Schalterhub ungeprüft.
6. Deckel auflegen: Knopf muss IO0 mittig treffen, frei gleiten und zurückkehren.
   Fronteinsatz erst nach erfolgreicher Passprobe befestigen: 0,6 mm seitliches
   Spiel und 0,2 mm nomineller Kleberspalt; geeignete dünne Klebefolie oder
   Nylon-Kleber. Führung frei halten. Tasterfläche ca. 0,3 mm versenkt.
7. Vier M3 × 8 mm Senkkopfschrauben (90°, Kopf bis 5,6 mm) für den Deckel.
   Die 2,5-mm-Piloten im Unterteil vorher auf M3 nachschneiden, maximal 6 mm
   tief. Schraubenlänge am Druck prüfen, nicht mit Gewalt festziehen.
8. Strom anschließen, ohne IO0 gedrückt zu halten (sonst Flashmodus).
   USB, Ton, IR gerade und schräg, Deckelsitz und Reset-Rückstellung prüfen.

Wandmontage unverändert: 60 mm Schraubenabstand; Schaft 3,5–4 mm, Kopf
maximal Ø 8 mm und 3 mm hoch, geeignete Dübel. Kopfunterseite zunächst
ca. 3,5 mm vor der Wand; Gehäuse über Köpfe setzen und 7 mm absenken.
Die Seite mit USB, IR und beiden Kabelbohrungen zeigt nach unten.

## Autodesk Fusion und Quelltext

STEP-Einzelteile und montierte Baugruppe können in Fusion importiert werden.
Die Dateien enthalten CAD-Volumenkörper; STEP überträgt keine native
Fusion-Konstruktionshistorie. Einheiten auf mm prüfen und danach als
Fusion-Entwurf speichern. Im separaten Fusion-Paket stehen dieselben STEP-Dateien.

Im Repository beziehungsweise im mitgelieferten `QUELLTEXT`-Verzeichnis:

```sh
python -m pip install -r requirements.txt
python designs/make_designs.py --design Retro --revision R3 --out ../NEU_EXPORT
python designs/check_retro_r3.py ../NEU_EXPORT
python designs/check_front.py ../NEU_EXPORT --design Retro
python designs/render_designs.py ../NEU_EXPORT --design Retro
```

## Prüfergebnisse und Abnahme

Die Berichte unter `PRUEFUNG` prüfen geschlossene Ein-Körper-STLs, STEP-Reimport,
Montagekollisionen einschließlich gedrücktem Reset, tatsächliche Rundbohrungen
unter der PCB-Ebene, USB-Ausschnitt ohne Deckelzunge, IR-Trichter und Ösenkanäle.
Die Frontflächenstichprobe ist keine vollständige Wandstärkenanalyse.
Bitte anschließend am Board prüfen: Lochraster, USB, Kabelführung/Zugentlastung,
IR-Sichtfeld/Empfang, Deckel, Reset und Wandmontage.

Herstellerreferenzen:
https://jlc3dp.com/help/article/3d-printing-design-guideline (abgerufen 11.10.2026)
https://jlc3dp.com/help/article/3301pa-nylon
https://www.autodesk.com/products/fusion-360/blog/import-step-file-into-fusion-360/
