# CM-Radio

WLAN-Internetradio für das **Loud-ESP32 mit ESP32-WROVER-N8R8**, gesteuert über eine lokale Weboberfläche und eine versionierte API. Zwei vorhandene **3-W-/8-Ω-Deckenlautsprecher** werden direkt an die eingebauten Stereo-Verstärker angeschlossen.

**Stand: V0.1.0, Entwicklung vor der ersten Hardware-Inbetriebnahme.** Die Firmware ist für den konkreten WROVER-Aufbau vorbereitet. Ein erfolgreicher Build ersetzt noch keinen Test von Ton, Stereo, WLAN und Neustart auf dem bestellten Board. Ergebnisse stehen in [docs/BUILDSTATUS.md](docs/BUILDSTATUS.md).

## V0.1

- Erstkonfiguration über ein Setup-WLAN mit zufälligem Passwort im seriellen Monitor.
- Speichern von WLAN, bis zu zehn Sendern, Lautstärke und Autostart im NVS-Speicher.
- MP3-/AAC-Streams, Play/Stop, Titelanzeige, automatischer Wiederverbindungsversuch.
- Start des zuletzt gewählten Senders nach Stromzufuhr; voreingestellte Lautstärke **5 von 21**.
- Handy-Weboberfläche unter `http://cm-radio.local` oder der Geräte-IP, ohne externe Dateien.
- Lokale `/api/v1/...`-API für die spätere Android-App.

Die eigenständige Android-App, Radio-Browser-Sendersuche und OTA-Updates folgen nach den Hardware-Grundtests. Das Handy kann V0.1 bereits im Browser bedienen. Für die Erstinstallation ist USB vorgesehen.

## Sofort starten

Ein kompiliertes Erstinstallationspaket enthält `CM-Radio-V0.1.0-full.bin`, `flash.py`, Prüfsummen und `ERSTSTART.md`. Es ist ausschließlich für **klassischen ESP32-WROVER mit 8 MB Flash** geeignet. Das vollständige Image ersetzt bei der Erstinstallation die Werksfirmware und löscht gespeicherte Einstellungen.

```powershell
py -m pip install esptool==4.8.1
py flash.py --port COM5 --erase
```

`COM5` durch den tatsächlichen Board-Port ersetzen. Danach den seriellen Monitor mit **115200 Baud** öffnen, das angezeigte `CM-Radio-XXXXXX`-WLAN verwenden und `http://192.168.4.1` öffnen. Ausführlich: [Erststart](docs/ERSTSTART.md).

## Entwickeln

Python 3.12 und Git installieren; für die zusätzlichen Host-Prüfungen werden außerdem Node.js und `g++` benötigt. Alternativ PlatformIO in VS Code verwenden und den Ordner `firmware` öffnen.

Die Buildumgebung und CI verwenden deaktivierte PlatformIO-Telemetrie. Lokal unter PowerShell vor den Befehlen `$env:PLATFORMIO_SETTING_ENABLE_TELEMETRY="no"` setzen; unter Linux/macOS `export PLATFORMIO_SETTING_ENABLE_TELEMETRY=no`.

```sh
python -m pip install -r requirements-dev.txt
python scripts/embed_web.py
python -m platformio run -d firmware
python -m platformio run -d firmware -t upload --upload-port COM5
python -m platformio device monitor -b 115200 --port COM5
```

Der erste `upload` über eine fremde Werksfirmware benötigt zuvor `python -m platformio run -d firmware -t erase --upload-port COM5`. Dieser Schritt löscht alle Einstellungen. Bei späteren CM-Radio-USB-Updates mit unverändertem Partitionslayout **nicht erneut löschen**.

```sh
python scripts/check_project.py
python scripts/package_firmware.py
python scripts/smoke_test.py http://cm-radio.local
```

Die Weboberfläche liegt im Firmware-Image; ein separater Dateisystem-Upload entfällt. Wenn `firmware/web/index.html` verändert wird, muss `embed_web.py` erneut ausgeführt werden. CI prüft, dass das eingebettete HTML aktuell ist.

## Projektstruktur

| Pfad | Aufgabe |
| --- | --- |
| `firmware/platformio.ini` | Festgelegte Toolchain und WROVER-Boardprofil |
| `firmware/include/BoardConfig.h` | I²S-Pins und Firmwareversion |
| `firmware/src/main.cpp` | WLAN, Setup-WLAN, Webserver, API, Boot |
| `firmware/src/Player.cpp` | Audio-Task, Befehlsqueue, Wiederverbindung |
| `firmware/src/Settings.cpp` | Validierte Konfiguration im NVS |
| `firmware/web/index.html` | Android-taugliche Webbedienung |
| `docs/` | Firmwarekonzept, API, Erststart, Testplan, Buildstatus |
| `hardware/` | Referenzhardware und Gehäuse mit CM-Radio-Schriftzug, STL/STEP und Wandmontage |
| `scripts/` | UI-Erzeugung, Prüfung, Paketierung, Flashen, Gerätetest |
| `tests/` | Prüfungen ohne Board |
| `.github/workflows/firmware.yml` | Build und Firmwarepaket pro Commit; Release bei Tag |

Öffentliche Entwicklung: [ceromihalik-dev/CM-Radio](https://github.com/ceromihalik-dev/CM-Radio). Zugangsdaten werden auf dem Gerät eingerichtet und gehören nicht in Quelltext, Issues oder Testprotokolle.

## Dokumentation und Lizenz

[Firmwarekonzept V0.1](docs/FIRMWAREKONZEPT_V0.1.md) · [API](docs/API_V0.1.md) · [Testplan](docs/TESTPLAN.md) · [Roadmap](docs/ROADMAP.md)

CM-Radio ist unter **GPL-3.0-or-later** lizenziert. Die eingebundene Audiobibliothek und ihre Codec-Lizenzen sind in [THIRD_PARTY.md](THIRD_PARTY.md) verzeichnet. Hersteller-Hardware ist ein unabhängiges Projekt.
