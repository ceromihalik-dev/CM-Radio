## Aktualisierung 11.10.2026 – R5 Display-Prototyp

Deckel mit Fenster, U-Halter und Kabelraum ist umgesetzt. Elecrow-Flexkabel:
ca. 50 mm **freie Kabellänge ab Modul**, vom Anwender bestätigt. Konstruktion
und Prüfung siehe `RETRO_R5_DISPLAY_MONTAGE.md`, `make_retro_display.py` und
`check_retro_display_step.py`. Die neu verlinkte SparkFun-Zeichnung liefert
Panel 34,5×23×1,4 mm, gehört aber zur **0,7-mm-FPC-Variante**; Elecrow/E3
verwendet 0,5 mm. Panelmaßgleichheit und echte Passung bleiben zu prüfen.
Die nachfolgende ursprüngliche Vorprüfung bleibt als historische Referenz.

# CM-Radio Retro – Prüfung SH1106-Display

Stand 11.10.2026; Gehäusebasis V0.3 R4. Ergebnis: elektrisch grundsätzlich
geeignet, mechanischer Einbau einschließlich Flachbandkabel noch nicht freigegeben.
Die R4-Druckdateien enthalten ausschließlich die Kabelauslasskorrektur, kein Display.

## Bestätigte Produktdaten und Anschluss

Elecrow/Sonocotta SKU PIAOLED: weißes SH1106-OLED, 128×64 Pixel, 3,3 V,
30-poliger Flexanschluss, 0,5-mm-Kontaktraster; für SPI auf Sonocotta-Audioboards
vorgesehen. Loud-ESP32 ist ausdrücklich in der Kompatibilitätsliste enthalten.
Nicht aus der Pinzahl allein auf die Kompatibilität anderer Displays schließen.

Die Herstellerunterlagen nennen beim klassischen ESP32 CLK GPIO18, MOSI GPIO23,
CS GPIO15, DC GPIO4 und Reset GPIO32; SPI-MISO GPIO19 gehört zur dokumentierten
Buskonfiguration. Diese GPIOs überschneiden sich nicht mit den aktuell im
CM-Radio verwendeten Audioleitungen 26/25/22, Verstärkerfreigabe 13 und IO0-Taste.
Die CM-Radio-Firmware enthält noch keinen OLED-Treiber und keine Bildschirmausgabe.
Die Squeezelite-Konfigurationsbefehle der Produktseite lassen sich nicht direkt
auf diese eigene Firmware übertragen.

## Tatsächlicher Platz im aktuellen Gehäuse

- Außen 104×80×36 mm; separater Fronteinsatz 80×32×3 mm.
- PCB-Unterseite Z=9,4 mm, Oberseite Z=11,1 mm, Deckel-Innenfläche Z=30 mm.
  Damit nominal 18,9 mm zwischen PCB-Oberseite und Deckel, aber vorhandene
  Komponenten beanspruchen davon bis zu 11 mm; kein durchgängig freier Hohlraum.
- IO0-Knopf X=43,486 / Y=48,201 mm, inklusive Führung, Halteplatte und Säulen.
  Die Halteplatte belegt ungefähr X=30,49..56,49, Y=41,20..55,20,
  Z=22,6..24,6 mm. Das Flexkabel darf dort weder geklemmt noch vom Knopf erfasst werden.
- Die E3-Gerberdaten enthalten die OLED-Kontaktreihe mit 30 Pads im 0,5-mm-Raster:
  Padreihenmitte lokal auf PCB X≈17,646 / Y≈47,324 mm; im Gehäuse
  X≈26,646 / Y≈50,524 mm. Dies ist die Lötpadreihe, NICHT die genaue
  Einsteckkante oder Höhe des bestückten Steckverbinders. Der Anschluss liegt
  links vom IO0-Bereich, an der oberen Platinenkante.

## Vorgeschlagene Integration

Eine neue Front mit Sichtfenster und rückseitigem Displayhalter ist sinnvoll.
Das Panel wird an seinem Rand mit Montagespiel gehalten; nicht auf Glas oder
Flexansatz klemmen. Schrift/Logo müssen dafür neu angeordnet werden. Das
Flachbandkabel führt vom Frontpanel zum oben links liegenden Boardanschluss,
mit weichem Bogen und einer Service-Schlaufe. Keine scharfen 180°-Falten, kein
Zug auf Stecker oder Flexansatz. Beim Deckelöffnen muss das Kabel erreichbar
bleiben. Den Verlauf neben der Resetmechanik prüfen; Display und Kabel dürfen
auch bei gedrückter Taste nicht in deren Bewegungsraum ragen.

Keine notwendige Kabellänge oder zulässigen Biegeradius aus Fotos schätzen.
Eine Verlängerung nur mit bestätigter 30-poliger 0,5-mm-Kontaktbelegung,
Kontaktseite und passender Orientierung wählen; ein beliebiges FFC-Kabel reicht nicht.

## Noch benötigte Daten für verbindliche CAD-Prüfung

1. Panel-Außenbreite, -höhe, -dicke und aktive Fläche mit deren Randversatz.
2. Flexlänge ab Panel bis Kontaktende, Breite, Ansatzposition und zulässiger Biegeradius.
3. Kontaktseite am Flex und passende Einsteckrichtung am tatsächlichen E3-Board;
   Einsteckkante und Steckerhöhe ebenfalls prüfen.

Die verlinkte Produktbeschreibung nennt keine verbindlichen Panel- und
Flexabmessungen. Der dort verlinkte SH1106-Chip-Datensatz ist keine
maßliche Zeichnung dieses Panels. Eine endgültige Einbauposition und ein
Druckfenster können deshalb noch nicht verlässlich festgelegt werden.

## Quellen

- https://www.elecrow.com/ssh1106-30-pin-oled-module.html
  Produktbeschreibung und Galerie am 11.10.2026 geprüft.
- https://github.com/sonocotta/esp32-audio-dock
  README, Abschnitte „Optional peripheral“ und „OLED screen“.
- E3-Gerber TopLayer und BoardOutline, bereits für das CM-Radio-Gehäuse
  verwendete Herstellerdaten; 30 rechteckige 0,3×1,25-mm-Pads ausgewertet.
- Lokale CM-Radio BoardConfig.h, platformio.ini und Retro-R4-Parameter.
