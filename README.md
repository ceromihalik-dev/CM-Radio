# CM-Radio

WLAN-Internetradio für das **Loud-ESP32 mit ESP32-WROVER-N8R8**, gesteuert über eine lokale Weboberfläche und eine versionierte API. Zwei vorhandene **3-W-/8-Ω-Deckenlautsprecher** werden direkt an die eingebauten Stereo-Verstärker angeschlossen.

**Stand: v0.1.3 · Build 06.** Sleep-Timer, sanfter Start und Lautstärkegrenze sind implementiert; Build 0a04 wurde vom Nutzer als PASS bestätigt. Radiosendersuche wurde in Build 0a03 vom Nutzer abgenommen. Neue Weboberfläche und grafische WLAN-Anzeige wurden in Build 0a02 vom Nutzer abgenommen. Die grundlegende Inbetriebnahme am gelieferten E3-Board ist bestätigt: WLAN-Suche, Ton aus beiden Lautsprechern, Lautstärke/Stop/Play und automatischer Start nach Stromunterbrechung. Getrennte Stereo-Kanäle, Dauerbetrieb und weitere Abnahmekriterien bleiben offen. Ergebnisse stehen im [Testplan](docs/TESTPLAN.md) und [Buildstatus](docs/BUILDSTATUS.md).

Projektstand: [Roadmap](docs/ROADMAP.md) · [Bugliste](docs/BUGLISTE.md).

## V0.1

- Erstkonfiguration über ein Setup-WLAN mit zufälligem Passwort im seriellen Monitor.
- Speichern von WLAN, bis zu zehn Sendern, Lautstärke und Autostart im NVS-Speicher.
- MP3-/AAC-Streams, Play/Stop, Titelanzeige, automatischer Wiederverbindungsversuch.
- Start des zuletzt gewählten Senders nach Stromzufuhr; voreingestellte Lautstärke **5 von 21**.
- Handy-Weboberfläche unter `http://cm-radio.local` oder der Geräte-IP, ohne externe Dateien.
- Lokale `/api/v1/...`-API für die spätere Android-App.

Neue GUI und grafische WLAN-Stärke sind integriert; internationale/nationale/lokale Sendersuche ist als erster Stand umgesetzt. Geplant bleiben Klangregler, Browser-Updates, Erstellerinfos mit Unterstützungslink, integrierter Changelog und weitere Komfortfunktionen. Die Android-App folgt nach Integration und Prüfung dieser Funktionen. Das Handy kann V0.1 bereits im Browser bedienen. Für die Erstinstallation ist USB vorgesehen.

## Sofort starten

Ein kompiliertes Erstinstallationspaket enthält `CM-Radio-V0.1.2-full.bin`, `flash.py`, Prüfsummen und `ERSTSTART.md`. Es ist ausschließlich für **klassischen ESP32-WROVER mit 8 MB Flash** geeignet. Das vollständige Image ersetzt bei der Erstinstallation die Werksfirmware und löscht gespeicherte Einstellungen.

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
python scripts/smoke_test.py http://cm-radio.local --report CM-Radio_Boardtest.json
```

Die Weboberfläche liegt im Firmware-Image; ein separater Dateisystem-Upload entfällt. Wenn `firmware/web/index.html` verändert wird, muss `embed_web.py` erneut ausgeführt werden. CI prüft, dass das eingebettete HTML aktuell ist.

Der automatische Erststarttest prüft 19 Kriterien ausschließlich lesend und schreibt einen Bericht ohne WLAN- oder Senderdaten. Er verändert keine Wiedergabe oder Einstellungen. Die physische Abnahme bleibt separat offen.

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

[Firmwarekonzept V0.1](docs/FIRMWAREKONZEPT_V0.1.md) · [API](docs/API_V0.1.md) · [Testplan](docs/TESTPLAN.md) · [Roadmap](docs/ROADMAP.md) · [Bugliste](docs/BUGLISTE.md)

CM-Radio ist unter **GPL-3.0-or-later** lizenziert. Die eingebundene Audiobibliothek und ihre Codec-Lizenzen sind in [THIRD_PARTY.md](THIRD_PARTY.md) verzeichnet. Hersteller-Hardware ist ein unabhängiges Projekt.

### Neuer Stand 0a05

Unter **Gerät** stehen Einstellungssicherung, geprüfte Wiederherstellung und Ersatzsender zur Verfügung. Die Sicherung enthält die derzeit implementierten Sender- und Wiedergabefunktionen; Klang wurde später ergänzt; Wecker und Zeitpläne entfallen. Build 0a04 wurde vom Nutzer als PASS bestätigt; Build 0a05 wurde am 09.10.2026 vom Nutzer als PASS bestätigt.

### Neuer Stand 0a06

Die Radioansicht bietet große Schnellwahlkacheln für alle gespeicherten Sender. Unter Sender lässt sich deren Reihenfolge mit Nach oben/Nach unten ändern; erst Änderungen speichern übernimmt sie dauerhaft. Der tatsächlich laufende Sender ist markiert, einschließlich Ersatzsender. Unter Gerät ist der bisherige Projekt-Changelog direkt auf dem Radio verfügbar. Build/Hosttests geprüft; Gerätetest 0a06 offen.

Build 0a07 korrigiert den seit 0a05 gemeldeten periodischen Stream-Neustart (CMR-004) durch Entfernen des Audiozeit-Stillstandswächters. Bestätigung am betroffenen Sender steht aus.

### Neuer Stand 0a08

Firmwareupdate unter Gerät: passende manifest.json und firmware.bin auswählen, Paket prüfen und Installation bestätigen. Ab 0a08 sind passende Paketmetadaten enthalten. Einmalig muss 0a08 noch per USB installiert werden. Anschließend sind lokale Paketupdates im Browser möglich. Ausstehende Einstellungen werden gesichert, Audio/Timer gestoppt; das Radio prüft Größe, ESP32-Header und SHA-256 vor Aktivierung des freien Firmware-Slots. Bei Erfolg startet es neu. Nach Verbindung Seite mit Strg+F5 neu laden. CMR-004 wurde in 0a07 vom Nutzer als PASS bestätigt. Nutzer bestätigt Build 0a08 und den angefragten Browserupdate-/Neustarttest am 09.10.2026 um 18:39 Uhr als PASS.

### Neuer Stand 0a09

Unter Gerät lassen sich Bässe/Höhen (−12 bis +6 dB) und Balance (−16 links bis +16 rechts) einstellen und speichern. Neutral erzeugt einen Entwurf mit allen Werten 0; Klang speichern wendet ihn an. Klang wird dauerhaft und in Sicherungen übernommen. Alte Daten laden neutral. Installation über den in 0a08 bestätigten Browserupdate; Hörprobe 0a09 offen. Loudness folgt separat.

### Neuer Stand 0a0a

Klangregler wirken als Vorschau direkt, ohne NVS-Schreibvorgang. Klang dauerhaft speichern erhält die Werte über Neustarts; Gespeicherte Werte wiederherstellen verwirft die Vorschau. Neutral hören ist vorübergehend. Sicherungen enthalten gespeicherten Klang, keine Vorschau. Vorschau bleibt bis Zurücksetzen, Speichern, Wiederherstellung oder Neustart bestehen, auch bei Senderwechsel und Stop/Play. Nutzer bestätigt 0a09 als PASS; 0a0a-Gerätetest offen.

Nutzerabnahme Build 0a0a am 09.10.2026 um 18:59 Uhr (Europe/Berlin): PASS nach angefragtem Test von direkter Klangvorschau, Zurücksetzen und Neustart ohne Speichern. Keine gesonderten Messwerte übermittelt; vollständige Hardwareabnahme bleibt separat.

### v0.1.3 · Build 01

Loudness lässt sich unter Gerät direkt vorhören und dauerhaft speichern. Die Zusatzanhebung nimmt mit der tatsächlichen Lautstärke ab und ist ab Stufe 15 ausgeschaltet; Bass/Höhen bleiben auf insgesamt +6 dB begrenzt. Alte Einstellungen laden Loudness aus. Jedes Firmware-ZIP enthält die ausführliche USB_ERSTINSTALLATION.txt mit automatisch passenden Paketdaten. Browserupdate nutzt manifest.json und firmware.bin. Gerätetest dieses neuen Stands offen.

Nutzerabnahme v0.1.3 Build 01 am 09.10.2026 um 19:10 Uhr (Europe/Berlin): PASS nach angefragtem Loudness-Hörtest und Prüfung gespeicherter Werte nach Neustart. Keine gesonderten Messwerte übermittelt. USB-Erstinstallation dieses Pakets und vollständige Hardwareabnahme nicht gesondert bestätigt.

### v0.1.3 · Build 02

Senderlogos aus der Radiosendersuche oder eigener HTTPS-Adresse unter Sender werden gespeichert und in Sicherungen übernommen. Browser lädt Logos; ohne Bild bleibt ein Platzhalter. Titel/Interpret aus üblichen Streammetadaten erscheinen getrennt; bei fehlenden Daten bleibt eine klare Ersatzanzeige. Wecker/Zeitpläne wurden auf Nutzerwunsch gestrichen. USB_ERSTINSTALLATION.txt bleibt in jedem Paket enthalten. Gerätetest Build 02 offen.

Nutzerabnahme v0.1.3 Build 02 am 09.10.2026 um 19:38 Uhr (Europe/Berlin): PASS nach angefragtem Test von Logos, Titelanzeige und Senderwechsel. Keine gesonderten Einzelnachweise übermittelt; vollständige Hardwareabnahme bleibt separat.

### v0.1.3 · Build 03

Unter Gerät zeigt der Infobereich den Ersteller C. Mihalik, den öffentlichen GitHub-Projektlink und den freiwilligen PayPal-Unterstützungslink aus CM IR Viewer. Externe Seiten werden erst beim Anklicken geöffnet. USB_ERSTINSTALLATION.txt ist weiterhin in jedem ZIP enthalten. Gerätetest Build 03 offen.

### v0.1.3 · Build 04

Gerät ist in sieben kompakte aufklappbare Bereiche gegliedert. Desktop: zwei Spalten; Smartphone: eine Spalte. Version, WLAN und Speicherzustand stehen oben. Build 03 wurde vom Nutzer als PASS bestätigt; Passwortschutz ist vorerst zurückgestellt. Gerätetest Build 04 offen.

### v0.1.3 · Build 05

50 Lautstärkestufen (0 stumm), unveränderte maximale Verstärkung. Alte Lautstärke und Grenze werden abgerundet auf die neue Skala übertragen. Neue Einstellungen und Sicherungen nutzen Schema 2; Schema 1 kann importiert werden. Ältere Firmware kann Schema 2 nicht laden. Netzwerk steht als aufklappbarer Bereich unter Gerät; WLAN-Knopf öffnet ihn direkt. Gerätetest offen.

Nutzerabnahme v0.1.3 Build 05 am 09.10.2026 um 20:04 Uhr (Europe/Berlin): PASS nach angefragter Prüfung von Lautstärke, Obergrenze, Neustart und WLAN-Suche. Keine gesonderten Messwerte oder Bestätigung eines Sicherungsimports übermittelt; vollständige Hardwareabnahme bleibt separat.

### v0.1.3 · Build 06

Erstpasswort des CM-Radio-WLANs ist passwort, erster Aufruf verlangt Änderung. Eigenes Passwort bleibt dauerhaft für Fallback gespeichert. Spätere Änderung unter Gerät → Netzwerk → Fallback-Zugang mit altem Passwort. USB-Befehl reset-ap-password hilft bei vergessenem Passwort, ohne Heimnetz/Sender zu löschen. Auch beim Upgrade von Build 05 einmalig ein eigenes Setup-Passwort festlegen. Gerätetest offen.

Passwortreset per Taste ab Build 06: Bei laufendem Radio BOOT/IO0 10 Sekunden halten und loslassen. Nur Setup-/Fallback-Passwort wird auf passwort zurückgesetzt; verpflichtender Wechsel beim nächsten Browseraufruf. Nicht mit BOOT beim Einschalten verwechseln (Flashmodus). Während eines Firmwareupdates wird der Reset ignoriert; anschließend neu halten. Prüfen: kurzer Druck bewirkt nichts, ein langer Druck löst einmal aus, Heimnetz/Sender/Klang bleiben erhalten.
