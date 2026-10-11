# CM-Radio Retro – V0.3 R8 ohne Display

Stand: 11.10.2026. Maße in **mm**, Druck **1:1 / 100 %**.
Fünf Druckteile, zehn Messinggewindeeinsätze. Außenmaß **104 × 80 × 36 mm**.
Keine sichtbare Versionsnummer am Gehäuse.

## Änderung gegenüber R7

Seitliche Schutzhauben und innere Prallwand entfernt. Die drei Schlitze je
Seite und die drei unteren Lüftungsschlitze sind wieder direkt offen.
Fronteinsatz zum Aufkleben: glatte Rückseite, keine Laschen, Haltebügel,
Frontgewinde, Frontschrauben oder Silikon-Zwischenlagen. Die früheren
Laschendurchbrüche im Deckel sind geschlossen. Metallgewinde für Deckel,
Platine und Reset-Halteplatte bleiben erhalten. R5 mit Display bleibt zurückgestellt.

## Druckteile, Material und Farbe

| Teil | Anzahl | JLC3DP-Material / dokumentierte Materialfarbe |
|---|---:|---|
| Unterteil | 1 | 3201PA-F Nylon SLS / Grayish Black (Grauschwarz) |
| Deckel | 1 | 3201PA-F Nylon SLS / Grauschwarz |
| Fronteinsatz | 1 | 3301PA Nylon SLS / White (Weiß) |
| Resetknopf | 1 | 3201PA-F Nylon SLS / Grauschwarz |
| Reset-Halteplatte | 1 | 3201PA-F Nylon SLS / Grauschwarz |

Keine Lackierung erforderlich. Jeder STL aus `STL_DRUCK` einmal, alternativ
die fünf Einzel-STEPs bestellen. Baugruppen und Hardware-Referenzen sind
keine Druckteile. Die optionale Einsatzprobe gehört nicht zu den fünf Teilen.
Vorschaufarben sind eine Annäherung, kein verbindliches Farbmuster / RAL-Abgleich.

## Klebefront

Fronteinsatz **80 × 32 × 3 mm**, montiert X=12…92, Y=25…57, Z=33…36.
Deckeltasche 81,2 × 33,2 mm, Boden Z=32,8; umlaufend nominal 0,6 mm Spiel,
**0,2 mm Abstand unter der Front für die Klebeschicht**. Radiozeichen und
Schrift sind graviert; Rückseite bleibt glatt. Zehn Retro-Rippen bleiben erhalten.

1. Einsatz trocken prüfen und auf der Tasche zentrieren. Resetöffnung
   deckungsgleich ausrichten; Rückseite und Tasche säubern, vollständig trocknen.
2. Für das tatsächliche Nylon geeigneten Klebstoff wählen und am Reststück
   Haftung sowie Materialverträglichkeit prüfen. Keine Haftfestigkeit zugesichert.
3. Dünn auftragen; fertige Klebeschicht nominal 0,2 mm. Kein dickes
   Schaumklebeband: Es würde die Front über Z=36 anheben.
4. Rund um die Resetöffnung frei lassen. Kleber darf weder in Führung noch
   auf den beweglichen Knopf gelangen. Front während der Aushärtung eben halten.
5. Nach vollständiger Aushärtung Reset auf freien Lauf und Rückstellung prüfen.

Die Front ist danach verklebt; ein Wechsel erfordert das Lösen der Klebung.
Die Deckelbefestigung am Unterteil bleibt verschraubt.

## Metallgewindeeinsätze und Schrauben

Einsätze separat beschaffen und **nach dem Druck thermisch einsetzen**.
Druckdateien enthalten Bohrungen, kein Metall. Keine Gewinde in die
Kunststoffbohrungen schneiden; sie sind für die folgenden Einsätze ausgelegt.

| Verwendung | Einsatz / Anzahl | Aufnahme Ø × Tiefe | Schraube |
|---|---|---|---|
| Deckel, im Unterteil | 4 × ruthex RX-M3Sx4.0 SHORT; M3, Länge 4, außen Ø 4,6 | 4,0 × 6,0 | 4 × M3 × 8, 90° Senkkopf ≤ Ø 5,6 |
| Platine, im Unterteil | 4 × ruthex RX-M2x4; M2, Länge 4, außen Ø 3,6 | 3,2 × 5,0 | 4 × M2 × 6, Kopf ≤ Ø 3,8 |
| Reset-Halteplatte, im Deckel | 2 × ruthex RX-M2x4 | 3,2 × 5,0 | 2 × M2 × 6, Kopf ≤ Ø 3,8 × 1,5 Höhe |

Summe **4 M3-SHORT + 6 M2**. M3-Senkkopflänge einschließlich Kopf;
M2-Länge unter dem Kopf. Keine längeren Schrauben verwenden.
Nominales Eindringen Deckel / PCB / Reset: 4,7 / 4,3 / 4,0 mm.
Resttiefe bis Lochgrund: 1,3 / 0,7 / 1,0 mm. Einsatzlänge höchstens 4 mm.
Bossaußendurchmesser 7,8 / 6,8 mm; radiale Wand zum Einsatzaußendurchmesser
je 1,6 mm. Im Deckel Durchgang Ø 3,4; Reset-Halteplatte Ø 2,4 mm.

| Funktion | Mittelpunkte XY in der montierten Baugruppe | Offene Einsetzfläche Z | Richtung |
|---|---|---:|---|
| M3 Deckel | (5;5), (99;5), (5;75), (99;75) | 30,0 | nach -Z |
| M2 PCB | (12,5;6,7), (70,5;6,7), (12,5;55,7), (70,5;55,7) | 9,4 | nach -Z |
| M2 Reset | (33,48635;48,2011), (53,48635;48,2011) | 24,6 | nach +Z |

USB-Kante Y=0; Z=0 äußerer Rückwandboden. In Wandlage zeigt -Y nach unten,
+Z von der Wand zur Front. Einzelteile sind für den Druck auf Minimum X/Y/Z=0
gesetzt; Montageachsen in `BAUGRUPPE_NICHT_DRUCKEN.step` abgleichen.
Einsetzplan: `Gewindeeinsaetze_Einsetzplan_R8.png`.

Die kompakte Konstruktion ist **nicht für JLC3DPs Standard-Einsatzservice**
ausgelegt: Dieser hat andere Einsätze und Mindestmontageflächen, unterstützt
keine M2. Eigene Montage der konkret angegebenen ruthex-Einsätze einplanen.

## Einsatzprobe und Einsetzen

Optionaler Prüfkörper 52 × 16 × 9,4 mm; abgeschrägte Ecke links.
Bohrungen von links nach rechts Ø 3,2 / 3,3 / 4,0 / 4,1 mm, erste zwei M2,
letzte zwei M3 SHORT. Vergleichslöcher dienen der Druckkalibrierung.
Probe mit gleichem Material / Verfahren drucken.

Ohne Elektronik arbeiten. Bohrungen von Pulverresten befreien, Durchmesser
und Tiefe messen. Nacharbeit nur mit Tiefenanschlag. Am Muster mit geregeltem
Lötkolben und passender Einsetzspitze testen; Prozess auf tatsächliches Nylon
abstimmen. Einsatz senkrecht und **bündig** einsetzen, vollständig abkühlen
lassen. Schraube mit 1,7-mm-PCB- oder 2-mm-Halteplatten-Zwischenlage prüfen;
kein Mitdrehen, Herausziehen oder Anschlagen am Grund. Erst nach erfolgreicher
Probe die zehn Gehäuseeinsätze montieren. Material-Festigkeit nicht physisch geprüft.

## Geometrie und Montage

Platine 85 × 56 × 1,7, Lochraster **58 × 49**. Unterseite Z=9,4,
Oberseite Z=11,1. Befestigung mit vier M2 × 6; Leiterbahnen und Bauteile von
Köpfen und Einsätzen freihalten. Board nicht verspannen.

Zwei untere Kabelbohrungen Ø 4,5, Mittelpunkte X=78/87, Z=6,2.
Oberkante 0,95 mm unter PCB-Unterseite. Kabel neben den Ösen am Boden führen,
mit Kabelbindern zugentlasten; nicht auf Ösendächer legen. Minimaler freier
Abstand des vollen Ø-4,5-Kabelwegs zu den jetzt Ø-6,8-PCB-Bossen: **1,85 mm**.
R4-Kabelauslässe sind Anwender-PASS; größere Insert-Bosse nochmals am Muster prüfen.

USB-Ausschnitt vollständig im Unterteil: 18 × 10,2, für gemessenen 12 × 8-Stecker.
IR-Trichter Ø 8 außen / Ø 6 innen; Mittelpunkt X=34,7, Z=16,1.
Durchmesser und Empfangswinkel bleiben am tatsächlichen Empfänger zu prüfen.

Erst Gehäuse und Einsätze trocken prüfen, dann Kabel und Platine montieren.
Front kleben und vollständig aushärten lassen, Resetknopf und Halteplatte
mit zwei M2 × 6 montieren. Knopf: 0,3 mm Ruheluft, 0,6 mm Mechanikweg.
Echte Bauteilabstände der Reset-Schraubenköpfe kontrollieren.
Deckel mit vier M3 × 8 befestigen. Reset, USB, IR, Audio, Kabelhalt und
Klebehaftung am fertigen Exemplar prüfen.

Wandmontage: Schlüssellöcher mit 60 mm Schraubenabstand / 7 mm Absenkweg.
Schraubenschaft 3,5–4, Kopf bis Ø 8 × 3, Kopfunterseite etwa 3,5 vor der Wand.
Höchster Schraubenkopf nominal 2,9 unter PCB-Unterseite. USB-/Kabelkante nach unten.

R7-Resetknopf und R7-Reset-Halteplatte sind unverändert verwendbar.
Unterteil, Deckel und Fronteinsatz für die vollständige R8-Ausführung neu drucken.
Firmware unverändert. Für FDM: Unterteil auf Rückwand, Fronteinsatz auf glatte
Rückseite; Deckel und Resetknopf passend orientieren und erforderliche Stützen
im Slicer prüfen. Wand / Boden 2,4; Deckelführung 2; Fügespiel 0,6 je Seite.

## Fusion und Prüfnachweis

STEP-Dateien enthalten editierbare Volumenkörper, keine native Fusion-Historie.
Die Hardware-Baugruppe enthält glatte Einsatz-Umhüllungen und die PCB-Referenz;
kleinere Aufnahmebohrungen werden beim thermischen Einsetzen absichtlich aufgeweitet.

```sh
python -m pip install -r requirements.txt
python designs/make_retro_r8.py ../NEU_EXPORT
python designs/check_retro_r4.py ../NEU_EXPORT
python designs/check_retro_r8.py ../NEU_EXPORT
python designs/check_front.py ../NEU_EXPORT --design Retro
python designs/make_retro_r8_probe.py ../NEU_EXPORT
python designs/render_retro_r8.py ../NEU_EXPORT
```

Geprüft: fünf gültige Einzelkörper, geschlossene STL-Netze, STEP-Reimport,
zehn Druckteil-Paarungen, PCB-Referenz und gedrückter Reset; zehn Kernlöcher
radial / axial am exportierten STEP vermessen. Anschluss- und Kabelwege,
entfernte Hauben / Prallwand, offene Luftwege, geschlossene Laschenlöcher und
0,2-mm-Klebefuge überprüft. Frontflächenprüfung ist eine Stichprobe.
CAD-PASS ersetzt keine physische Druckpassung, Klebe-/Einsatzfestigkeit oder
vollständige reale Bauteilprüfung. R8-Musterabnahme steht aus.

## Herstellerquellen (abgerufen 11.10.2026)

- Grauschwarz: https://jlc3dp.com/help/article/3201pa-f-nylon
- Weiß: https://jlc3dp.com/help/article/3301pa-nylon
- Einsatzservice: https://jlc3dp.com/help/article/threaded-insert-service
- Druckauslegung: https://jlc3dp.com/help/article/3d-printing-design-guideline
- M3 SHORT: https://www.ruthex.de/products/ruthex-gewindeeinsatz-m3s-100stuck-rx-m3x4-0-short-messing-gewindebuchsen-fur-3d-druck
- M2: https://www.ruthex.de/collections/gewindeeinsatze/products/ruthex-gewindeeinsatz-m2-70-stuck-rx-m2x4-messing-gewindebuchsen
