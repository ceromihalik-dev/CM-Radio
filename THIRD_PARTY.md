# Abhängigkeiten und Herkunft

CM-Radio-eigener Quelltext: GPL-3.0-or-later, Lizenztext in `LICENSE`.

| Bestandteil | Festgelegter Stand | Herkunft / Lizenz |
| --- | --- | --- |
| ESP32-audioI2S | Git-Tag 3.0.12 | https://github.com/schreibfaul1/ESP32-audioI2S/tree/3.0.12 ; Bibliotheksmanifest GPL-3.0. Eingebundene Decoder behalten ihre jeweiligen Copyright-/Lizenzhinweise. |
| ArduinoJson | 6.21.5 | https://github.com/bblanchon/ArduinoJson ; MIT |
| Arduino-ESP32 | 2.0.17, Paket 3.20017.241212+sha.dcc1105b | https://github.com/espressif/arduino-esp32 ; LGPL-2.1 und zugehörige Drittkomponenten |
| Espressif32 PlatformIO-Plattform | 6.9.0 | https://github.com/platformio/platform-espressif32/tree/v6.9.0 ; Apache-2.0 |
| esptool | 4.8.1 für Flashpaket-Skripte | https://github.com/espressif/esptool ; GPL-2.0-or-later |

Abhängigkeiten werden beim Build von ihren Quellen bezogen, nicht als eigener CM-Radio-Quelltext ausgegeben. Der öffentliche Projektquelltext mit festgelegtem Buildverfahren gehört zu veröffentlichten Firmware-Binärdateien. Bestehende Lizenzhinweise der Bibliothek und der Decoder dürfen beim Weiterverteilen nicht entfernt werden.

Sonocotta-Boarddateien sind ein separates Herstellerprojekt (Apache-2.0 laut Herstellerrepository). CM-Radio kopiert hier keine Hersteller-CAD-Dateien. Der mitgelieferte Radio-Paradise-Stream ist eine externe, veränderliche Beispieladresse; CM-Radio hostet oder verteilt keine Senderinhalte.
