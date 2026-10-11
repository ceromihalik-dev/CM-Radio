# CM-Radio Retro R8 - Fertigung aus Resin

Aktueller Nutzerentscheid vom 11.10.2026: Die fünf Gehäuseteile werden aus
Resin hergestellt. Konkrete Resin-Sorte und Farben sind für alle fünf Teile
nicht bestätigt; maßgeblich ist der tatsächliche JLC3DP-Auftrag.

## Gewindeeinsätze: nicht thermisch in Resin einsetzen

Die unveränderten R8-Dateien besitzen M3-Aufnahmen Ø 4,0 × 6,0 mm und
M2-Aufnahmen Ø 3,2 × 5,0 mm. Diese sind für thermisches Einsetzen in
Thermoplast ausgelegt. Die ruthex-Einsätze sind außen Ø 4,6 bzw. 3,6 mm.
Die Resin-Bohrungen sind daher für ein einfaches Einkleben zu klein.

**In ausgehärtetem SLA-Resin weder mit dem Lötkolben einsetzen noch die
Einsätze mit Gewalt einpressen.** Für Klebemontage müssen die Aufnahmen
an den realen Einsatzaußendurchmesser und den verwendeten Klebstoff
angepasst werden. Keine pauschale Bohrfreigabe: Restwand, Sacklochtiefe,
Resin-Sorte und reale Maße zunächst an einer Probe prüfen. Nacharbeit nur
ohne Elektronik und mit Tiefenanschlag. Klebung vollständig aushärten lassen
und Halt sowie Anzugsmoment am Muster prüfen.

Das Release dokumentiert die aktuelle R8-Geometrie. Es enthält keine
automatisch angepasste oder physisch abgenommene Resin-Gewindeaufnahme.
Thermische Montageanweisungen in der Referenzdokumentation gelten
ausschließlich für geeigneten Thermoplast, insbesondere die bisherige
SLS-Nylon-Auslegung. Die Einsatzprobe hat ebenfalls Thermoplast-Pilotmaße.

## Front, Passung und Oberfläche

Fronteinsatz aufkleben; Klebstoff passend zur tatsächlichen Resin-Sorte
auswählen und Haftung am Reststück testen. Fertige Klebeschicht nominal
0,2 mm. Resetführung kleberfrei halten. Deckel, Knopf und Front trocken
prüfen; physische R8-Passung und Festigkeit stehen noch aus.

Die grauschwarz/weiße CAD-Vorschau zeigt die bisherige Gestaltung. Sie
bestätigt keine bestellte Resin-Farbe. 9600 Resin wird von JLC3DP in
Mattweiß angeboten. Oberfläche ohne zusätzliche Schleif-/Lackierbearbeitung
bestellen, wenn diese im Auftrag nicht gewünscht ist.

## Zollbeschreibung für alle Resin-Teile

3D-printed resin (plastic) enclosure parts. No electronic components included.

Deutsch: 3D-gedruckte Gehäuseteile aus Kunstharz (Kunststoff).
Keine elektronischen Bauteile enthalten.

## Herstellerquellen

- Formlabs: https://formlabs.com/blog/adding-screw-threads-3d-printed-parts/
  Thermoplast: Wärme; SLA-Thermoset: angepasste Aufnahmen und Klebemontage.
- JLC3DP: https://jlc3dp.com/help/article/photosensitive-9600-resin
- Einsatzabmessungen: `JLC3DP_ABGLEICH_R8.json` / `MATERIALLISTE_R8.md`.
