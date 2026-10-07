# Referenzhardware

Bestellt: **Elecrow/Sonocotta Loud-ESP32**, ESP32-WROVER-N8R8 mit 8 MB physischem Flash und 8 MB physischer PSRAM, USB-C und zwei integrierten I²S-Verstärkern. Zwei vorhandene Deckenlautsprecher: je 3 W / 8 Ω. Keine zusätzliche Audio-Platine.

Herstellerquellen: https://www.elecrow.com/loud-esp32.html und https://github.com/sonocotta/esp32-audio-dock . WROVER-Hardwarestände sind unter `hardware/2-loud-esp32/rev-e2` und `rev-e3` dokumentiert; die tatsächlich gelieferte Revision ist noch zu prüfen. ESP32-S3-Varianten benötigen andere Pins und eine eigene Firmwareumgebung.

| Signal | Klassischer ESP32-WROVER |
| --- | --- |
| I²S BCLK / WS / DATA | GPIO 26 / 25 / 22 |
| Verstärkerfreigabe | GPIO 13 |
| Für PSRAM reserviert | GPIO 16 / 17 |

Gehäusekonzept V0.1: 104 × 80 × 32,4 mm außen, zwei rückseitige Schlüssellochaufnahmen mit 60 mm Abstand und 7 mm Einhängeweg. USB-C und Lautsprecherleitungen müssen zugänglich bleiben. Druckdateien und physische Passform werden getrennt geprüft; die Firmware setzt kein Display und keine zusätzliche Bedientaste voraus.

Beide Lautsprecher erhalten jeweils ihr eigenes Plus-/Minus-Paar. Die Brückenausgänge der Verstärker dürfen nicht über eine gemeinsame Minusleitung verbunden werden.
