# CM-Radio Retro R8 - Schrauben und Einschmelzmuttern

Für **ein Gehäuse V0.3 R8 ohne Display**, ohne Reserveteile / optionale Probe.
Die Bildpositionen beziehen sich auf `CM-Radio_Retro_R8_Explosionszeichnung.png`.

**Resin-Fertigung:** Diese Hardwareliste beschreibt die R8-Referenz.
Keine thermische Montage in Resin. Die unveränderten Pilotbohrungen sind
für Klebemontage zu klein; Anpassung und Musterprüfung erforderlich.
Siehe `RESIN_HINWEIS_R8.md`. Physische Resin-Abnahme steht aus.

| Bild | Menge | Teil | Ausführung / Maße | Verwendung |
|---|---:|---|---|---|
| A | 4 | M3 × 8 mm Schraube | 90° Senkkopf, Kopf Ø höchstens 5,6 mm; Länge einschließlich Kopf | Deckel |
| B | 4 | M2 × 6 mm Schraube | Linsen-/Flachrundkopf, Kopf Ø höchstens 3,8 mm; Länge unter Kopf | Platine |
| C | 2 | M2 × 6 mm Schraube | Linsen-/Flachrundkopf, Kopf Ø höchstens 3,8 mm, Kopfhöhe höchstens 1,5 mm | Reset-Halteplatte |
| D | 4 | ruthex RX-M3Sx4.0 SHORT | Messing; M3, Länge 4,0 mm, maximal außen Ø 4,6 mm | Deckelgewinde im Unterteil |
| E | 4 | ruthex RX-M2x4 | Messing; M2, Länge 4,0 mm, maximal außen Ø 3,6 mm | Platinengewinde im Unterteil |
| F | 2 | ruthex RX-M2x4 | Messing; M2, Länge 4,0 mm, maximal außen Ø 3,6 mm | Resetgewinde im Deckel |

**Zusammengefasster Einkauf:** 4 × M3-Senkschraube 8 mm, 6 × M2-Schraube
6 mm (alle mit Kopfhöhe ≤1,5 mm möglich), 4 × M3-SHORT- und 6 × M2-Einsatz.
Damit **10 Schrauben und 10 Einschmelzmuttern**. Keine Frontschrauben.
Einsatzlänge 4 mm für beide Typen; Standard-M3-Einsätze mit anderer Länge
oder anderem Außendurchmesser passen nicht ohne neue Auslegung.

Aufnahmebohrungen: M3 Ø **4,0 × 6,0 mm**, M2 Ø **3,2 × 5,0 mm**.
Nur in Thermoplast nachträglich thermisch und bündig einsetzen; JLC-Standard-Einsatzservice
wird für diese kompakten ruthex-Aufnahmen nicht beauftragt. Erst an der
optionalen Einsatzprobe Material / Maß / Einsetzprozess prüfen.

Zusätzlich: geeigneter Nylon-Kleber (fertige Schicht nominal **0,2 mm**),
zwei Kabelbinder passend zu den **3,2 × 2,0-mm-Ösentunneln**, zwei
Wandschrauben und zum Wandaufbau passende Dübel. Wandschrauben-Schaft
3,5-4,0 mm, Kopf Ø höchstens 8,0 mm und Höhe höchstens 3,0 mm;
Länge / Dübel entsprechend Wand und notwendiger Verankerung wählen.
Diese Wandschrauben sind nicht in den zehn Montageschrauben enthalten.

Optionaler Prüfkörper: zusätzlich 2 × M2- und 2 × M3-SHORT-Einsatz.
Anweisung und Montagekoordinaten: `RETRO_R8_MONTAGE.md`.
Hardware in der Explosionsansicht ist vereinfacht; Explosionsabstände sind
Darstellungsabstände, keine Einbaumaße. R8-Druckpassung und Einsatzhalt
sind noch nicht physisch abgenommen.

Herstellerabmessungen geprüft am 11.10.2026, siehe `JLC3DP_ABGLEICH_R8.json`:

- M3 SHORT: https://www.ruthex.de/products/ruthex-gewindeeinsatz-m3s-100stuck-rx-m3x4-0-short-messing-gewindebuchsen-fur-3d-druck
- M2: https://www.ruthex.de/collections/gewindeeinsatze/products/ruthex-gewindeeinsatz-m2-70-stuck-rx-m2x4-messing-gewindebuchsen
