# CM-Radio Modell 3 Retro – V0.3 R6 ohne Display

Stand: 11.10.2026. Alle Maße in **mm**, Druck **1:1 / 100 %**.
Außenmaße **104 × 80 × 36 mm**, fünf montierte Druckteile. Zehn abgerundete
Retro-Rippen, separater Fronteinsatz mit CM-Radio-Gravur, vier Deckelschrauben,
Resetmechanik und Wand-Schlüssellöcher. Keine sichtbare Versionsnummer.

## Änderung und bisherige Abnahme

R6 basiert auf dem displayfreien R4. Die zwei Kabelauslässe wurden vom
Anwender bereits mit **PASS** bestätigt. R5 bleibt ein separater, vorerst
zurückgestellter Display-Prototyp; seine Front und der Displayhalter werden
für dieses Paket nicht verwendet.

Geometrisch geändert werden **Unterteil und Deckel**:

- Platinen-Kernlöcher von Ø 2,1 auf **Ø 2,0 mm**, weiterhin 5 mm tief.
- Reset-Kernlöcher **Ø 2,0 mm**, jetzt **5 statt 3 mm** tief.
  Die bisher angegebenen 2,5 × 6-mm-Schrauben durch eine 2-mm-Halteplatte
  reichen 4 mm in den Deckel. Der alte 3-mm-Pilot hätte die Schraubenspitze
  1 mm zu früh gestoppt. Jetzt bleiben nominal 1 mm zum Lochgrund.
- M3-Deckel-Kernlöcher **Ø 2,5 × 6 mm** bleiben erhalten. Das ist ein
  Vorloch zum anschließenden Schneiden von **M3 × 0,5**, kein Druckgewinde.

Fronteinsatz, Resetknopf und Halteplatte aus dem displayfreien R4 können
weiterverwendet werden. USB, IR, Kabelwege, Zugentlastung und Lochraster
entsprechen R4. Der neue komplette R6-Druck ist noch nicht physisch abgenommen.

## Schrauben und Kernlochmaße

| Befestigung | Anzahl / Referenzschraube | Kernloch Ø / Tiefe | Axiales Eindringen / Rest zum Lochgrund |
|---|---|---|---|
| Platine | 4 × 2,5 × 6 mm, gewindeformend für Kunststoff, Linsenkopf ≤ Ø 4,5 mm | 2,0 / 5,0 mm | 4,3 / 0,7 mm |
| Reset-Halteplatte | 2 × 2,5 × 6 mm, gewindeformend für Kunststoff, Linsenkopf ≤ Ø 5 mm | 2,0 / 5,0 mm | 4,0 / 1,0 mm |
| Deckel | 4 × M3 × 8 mm, 90° Senkkopf ≤ Ø 5,6 mm | 2,5 / 6,0 mm; M3 nachschneiden | nominal 4,7 / 1,3 mm |

Die 2,5-mm-Schrauben benötigen ein **Kunststoffgewinde, z. B. PT-Bauart**.
Eine metrische M2,5-Schraube oder eine beliebige Blech-/Holzschraube ist kein
gleichwertiger Ersatz. Die Kernlochwahl Ø 2,0 entspricht 0,8 × Schrauben-Ø;
EJOT nennt für PT eine materialabhängige Spanne 0,7–0,8 × Ø. Dies ist eine
Auslegung für eine Passprobe in gedrucktem Nylon, keine Festigkeitsfreigabe.
Die axiale Eintauchtiefe enthält eine etwaige Schraubenspitze; die wirksame
Gewindetraglänge hängt von der tatsächlich gewählten Schraube ab. Die
vergleichsweise kurzen Schrauben werden beibehalten, damit sie nicht unten
durch die Halter austreten. Klemmung und Haltekraft am Muster prüfen.

Die Senkung am Deckel ist Ø 6,2 mm oben, Ø 3,4 mm unten und 1,4 mm tief.
Ein idealer Ø-5,6-mm-Senkkopf sitzt ca. 0,3 mm unter der Oberfläche; daraus
folgen die 4,7 mm Eintauchtiefe. Der Kopf muss auf der Senkung tragen.
Keine längeren Schrauben einsetzen. Die Durchgangslöcher sind Ø 3,4 mm im
Deckel und Ø 2,9 mm in der Reset-Halteplatte. Platinenhalter außen Ø 5,8 mm,
Resetbossen Ø 6,8 mm, Deckelbossen Ø 7,2 mm. Hinter den neuen Reset-Piloten
bleiben bis zur äußeren Deckelfläche **4,0 mm** Material.

## Drucktoleranzen, Nacharbeit und optionale Kernlochprobe

Die Maße oben sind CAD-Nennmaße. JLC3DP nennt für Nylonbohrungen ±0,3 mm
und weist darauf hin, dass kleine Bohrungen schrumpfen können. Vor Montage
Späne/Pulver entfernen und tatsächliche Bohrungen prüfen. Ø-2,0-mm-Piloten
bei Bedarf mit einem 2,0-mm-Bohrer vorsichtig auf Nennmaß bringen, Tiefenanschlag
**5 mm**. Nur am leeren Teil arbeiten. Eine zu große Bohrung lässt sich dadurch
nicht korrigieren; dann Schrauben-/Materialwahl beziehungsweise CAD anpassen.

M3-Piloten auf Ø 2,5 mm kontrollieren und mit einem Grundloch-Gewindebohrer
mit kurzem Anschnitt schneiden. **Mindestens 4,7 mm nutzbares Vollgewinde**
werden benötigt; höchstens 6 mm Bohrtiefe. Ein langer Anschnitt erreicht bei
dieser Tiefe möglicherweise kein ausreichendes Gewinde. Mit Tiefenanschlag
arbeiten, nicht gewaltsam am Lochgrund drehen. Gewindefunktion zunächst
am Muster prüfen; Schraube darf nicht am Grund fest werden, bevor sie klemmt.

Unter `OPTIONAL_KERNLOCHPROBE` liegt eine separate Probe **52 × 16 × 9,4 mm**.
Sie gehört nicht zum montierten Gehäuse und muss nicht mitbestellt werden.
Die abgeschrägte Ecke kennzeichnet das linke Ende. Von links nach rechts:
**Ø 2,0 / 2,1 / 2,2 / 2,5 mm**, letzte Bohrung 6 mm tief, übrige 5 mm.
Gleiches Material und gleicher Druckprozess wie das Gehäuse verwenden.
Die größeren Vergleichspiloten erlauben eine Prüfung der Druckabweichung;
sie sind keine pauschale Empfehlung für größere Kunststoff-Kernlöcher.
Vor dem Schraubentest die Ist-Durchmesser messen. Für den Kunststofftest
die tatsächliche 1,7-mm-Platine beziehungsweise eine 2-mm-Zwischenlage
simulieren, damit die 6-mm-Schraube die richtige Länge im Boss hat.
Den Ø-2,5-mm-Piloten zunächst auf M3 schneiden und mit einer Zwischenlage
eine Eintauchtiefe ≤ 4,7 mm herstellen. Von Hand anziehen, nicht überdrehen.
Passprobe beurteilen: klemmt sicher, kein Aufplatzen, keine lose Schraube,
keine Verformung der Platine und kein Anschlagen der Spitze.

## Anschluss- und Wandmaße

- Platinen-Lochraster **58 × 49 mm**, Board 85 × 56 × 1,7 mm.
  Platinenunterseite Z=9,4 mm, Oberseite Z=11,1 mm; Unterteilrand Z=30 mm.
- Zwei runde Kabelbohrungen **Ø 4,5 mm** an der unteren USB-Kante,
  X=78/87, Z=6,2 mm. Oberkante 0,95 mm unter der Platinenunterseite.
  Voller gerader Ø-4,5-mm-Kabelweg bis Y=23 mm ist frei; Mindestabstand
  zu allen Platinenhaltern 2,35 mm.
- Kabelbinderösen X=73/92, Y=14 mm, Oberkante Z=6,4 mm;
  Tunnel 3,2 mm breit × 2 mm hoch. **Kabel neben den Ösen am Boden führen**,
  nicht über deren Dach. Dünnen Kabelbinder durch den Tunnel und um den
  Kabelmantel führen, Kopf niedrig seitlich, Mantel nicht quetschen.
- USB-Ausschnitt **18 × 10,2 mm**, Eckradius 2 mm, vollständig im Unterteil.
  Buchse gemessen 9 × 3 mm, Stecker 12 × 8 mm.
- IR-Trichter **Ø 8 mm außen / Ø 6 mm innen**, Mitte X=34,7 / Z=16,1 mm.
  Position gemessen, Durchmesser weiterhin Prüfmaße für Empfang/Sichtfeld.
- Wand-Schlüssellöcher: **60 mm Abstand**, 7 mm Absenkweg, Schaft 3,5–4 mm,
  Kopf bis Ø 8 × 3 mm; Kopfunterseite etwa 3,5 mm vor der Wand. Nominal
  mindestens 2,9 mm zwischen höchstem Schraubenkopf und Platinenunterseite.
  Geeignete Dübel für die Wand verwenden. USB/IR/Kabel zeigen nach unten.

## JLC3DP, Material und Farben

Je ein Teil aus `STL_DRUCK` bestellen: **Unterteil, Deckel, Fronteinsatz,
Resetknopf, Reset-Halteplatte**. Alternativ dieselben Einzel-STEPs verwenden;
beide Formate nicht doppelt bestellen. `BAUGRUPPE_NICHT_DRUCKEN.step` ist
eine Ansichtsbaugruppe. Die optionale Probe ist separat gekennzeichnet.

Auslegungsbasis: **3301PA Nylon SLS**, weiß, alternativ Nylon MJF nach
Anbieterprüfung. Wände/Boden 2,4 mm, Führungsrand 2 mm, seitliches Deckelspiel
0,6 mm, radiales Resetspiel 0,6 mm. Zielgestaltung: Gehäuse **Salbeigrün matt
(RAL 6021)**, Fronteinsatz **Elfenbein matt (RAL 1015)**, Knopf dunkelgrau.
Diese Lackfarben sind ein Gestaltungsvorschlag; Verfügbarkeit beim Anbieter
vor Bestellung klären. Gravur dunkel auslegen. Bohrungen, Führungen,
Gewindepiloten und Klebesitz nicht lackieren.

FDM-Probedruck nicht skalieren. Unterteil, Fronteinsatz und Halteplatte mit
flacher Unterseite auf das Bett. Deckel mit Front nach oben, im Slicer Brim
und nötige Stützen unter der Frontplatte/Innenkonturen vorsehen; die gerippte
Front ist keine flache Bettauflage. Resetknopf braucht Stützen unter den
Absätzen oder eine passende Umorientierung. Optionales Probeteil flach
auflegen. Alle Dateien beginnen bei Z=0. Ausgangswerte für den FDM-Test:
0,2-mm-Schichten, 3–4 Wände, 25–35 % Füllung.

## Montage und Abnahme

1. Ohne Elektronik alle Druckteile entgraten, Piloten kontrollieren und
   Schraubenprobe durchführen. M3 schneiden, Pulver und Späne entfernen.
2. Lautsprecherkabel durch die beiden unteren Bohrungen führen und neben
   den niedrigen Ösen zugentlasten. Reale Unterseitenbauteile freihalten.
3. Platine mit vier gewindeformenden 2,5 × 6-mm-Schrauben befestigen,
   leicht anziehen, Board nicht verspannen. Köpfe von Leiterbahnen und
   Bauteilen fernhalten; nicht alle Bauteile sind im CAD dargestellt.
4. USB-Stecker vollständig einsetzen und IR-Sichtfeld/Empfang prüfen.
5. Resetknopf von innen in den Deckel einsetzen, Halteplatte mit zwei
   gewindeformenden 2,5 × 6-mm-Schrauben befestigen. Freier Hub/Rückstellung
   prüfen. Auch den Freiraum der inneren Schraubenköpfe zu echten Bauteilen
   kontrollieren. Tastspitze nominal 0,3 mm über dem IO0-Taster,
   Mechanikweg 0,6 mm; tatsächlichen Schalterhub am Board prüfen.
6. Deckel probeweise aufsetzen, Reset muss mittig treffen und zurückkehren.
   Fronteinsatz danach mit geeigneter dünner Klebefolie/Nylon-Kleber befestigen;
   seitlich 0,6 mm Spiel, unter dem Einsatz 0,2 mm nomineller Kleberspalt.
7. Deckel mit vier M3 × 8-mm-Senkschrauben befestigen. Wenn eine Schraube
   schon vor Klemmung hart stoppt, Länge/Loch/Anschnitt prüfen, nicht forcieren.
8. USB anschließen, ohne IO0 gedrückt zu halten. Audio, IR, Reset, Zugentlastung,
   Deckelsitz und Wandmontage prüfen. Keine neue physische PASS-Abnahme ist
   aus der CAD-Prüfung abgeleitet. Das belüftete Gehäuse hat keine IP-Freigabe.

## Fusion, Quelltext und Prüfberichte

STEPs enthalten editierbare Volumenkörper, keine native Fusion-Zeitleiste.
Einzelteile beziehungsweise Ansichtsbaugruppe importieren, Einheiten mm
prüfen, danach als Fusion-Entwurf speichern. Es wird keine F3D-Datei behauptet.

Im Repository oder mitgelieferten `QUELLTEXT`-Verzeichnis:

```sh
python -m pip install -r requirements.txt
python designs/make_designs.py --design Retro --revision R6 --out ../NEU_EXPORT
python designs/check_retro_r4.py ../NEU_EXPORT
python designs/check_retro_r6_screws.py ../NEU_EXPORT
python designs/check_front.py ../NEU_EXPORT --design Retro
python designs/make_retro_r6_probe.py ../NEU_EXPORT
python designs/render_retro_r6.py ../NEU_EXPORT
```

Prüfung: fünf gültige Einzelkörper, wasserdichte STL-Netze, STEP-Reimport,
alle zehn Druckteil-Paarungen, Reset im gedrückten Zustand, vollständige
Kabelwege und Anschlussgeometrie. **Alle zehn Kernlöcher wurden am
reimportierten Baugruppen-STEP radial und axial vermessen**, Schraubenlängen
und nominale Resttiefe berechnet. Frontflächen-Stichprobe ist keine vollständige
Wandstärkenanalyse. Reale Schraubengeometrie, Drucktoleranz und Festigkeit
erfordern eine Musterprüfung.

## Mögliche nächste Aufwertung (noch nicht eingebaut)

1. Zweifarbige matte Oberfläche, kontrastreich ausgelegte CM-Radio-Gravur
   und farblich passende Senkköpfe: größter optischer Effekt ohne neue CAD-Teile.
2. Austauschbarer, mechanisch befestigter Fronteinsatz statt Klebung:
   einfacher Farbwechsel und Wartung; verdeckte Befestigung neu konstruieren.
3. M3-Metallgewindeeinsätze für häufiges Öffnen: konkrete Einsatzabmessungen
   auswählen, dann Bossen/Bohrung/Tiefen sowie Einbauverfahren passend ändern.
4. Weiche Wandauflagen gegen Klappern und Kratzer; Abstand und Schlüsselloch-
   Eingriff gemeinsam auslegen, damit die Köpfe weiter sicher tragen.
5. Für den Badeinsatz: nach unten geschützte Lüftung mit Tropfkante oder
   Labyrinth. Thermik und Entwässerung prüfen; dies allein ergibt keine IP-Klasse.

Herstellerquellen, abgerufen 11.10.2026:

- EJOT PT-Auslegung: https://www.ejot.com/medias/sys_master/Industry_Flyer/Industry_Flyer/h54/h3c/9331729760286/EJOT-PT-Flyer-08.23-en.pdf
- M3-Kernlochbereich: https://guhring.com/ProductsServices/SizeDetails?EDP=9046380030000
- JLC3DP: https://jlc3dp.com/help/article/3d-printing-design-guideline
- Nylon: https://jlc3dp.com/help/article/3301pa-nylon
