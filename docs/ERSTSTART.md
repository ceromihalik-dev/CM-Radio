# CM-Radio V0.1 – Flashen und erster Test

## Vorbereiten

Das Firmwarepaket gilt für **Loud-ESP32 / ESP32-WROVER-N8R8, 8 MB Flash**. Modulaufdruck beim Eintreffen prüfen. Bei ESP32-S3 oder einer abweichenden Flashgröße dieses Image nicht verwenden. Das Flashskript prüft Chipfamilie und Flashkapazität vor dem Schreiben.

USB-C-Datenkabel, stabiles 5-V-Netzteil bzw. geeigneten USB-Anschluss, 2,4-GHz-WLAN und einen PC bereitlegen. Für Lautsprechertests eine ausreichende Stromversorgung verwenden; ein schwacher PC-USB-Port kann bei höherer Lautstärke einen Neustart auslösen.

Lautsprecher bei ausgeschaltetem Board jeweils an den eigenen Zweipol-Ausgang anschließen. Die Ausgänge der Class-D-Verstärker besitzen **keine gemeinsame Lautsprechermasse**: Lautsprecher-Minus weder miteinander noch mit GND verbinden. Zunächst frei auf dem Tisch testen; erst nach erfolgreicher Abnahme in das Wandgehäuse setzen.

## A. Kompiliertes Erstinstallationspaket

1. ZIP entpacken. Terminal im Ordner mit `flash.py` und `CM-Radio-V0.1.2-full.bin` öffnen.
2. Python installieren, anschließend unter Windows:

```powershell
py -m pip install esptool==4.8.1
py -m serial.tools.list_ports
py flash.py --port COM5 --erase
```

`COM5` ist ein Beispiel. Unter Linux/macOS `python3` und den tatsächlichen Port verwenden. `--erase` gehört nur zur Erstinstallation: Es löscht die Werksfirmware und alle gespeicherten Einstellungen. Das vollständige Image eignet sich nicht für ein Update mit Erhalt der Einstellungen.

3. Seriellen Monitor öffnen:

```powershell
py -m serial.tools.miniterm COM5 115200
```

Monitor nach Bedarf mit Strg+] verlassen. Für Eingabebefehle Enter verwenden. Nach dem Öffnen die Reset-/EN-Taste kurz drücken, damit der Starttext sichtbar wird. Während des Flashens darf kein anderer serieller Monitor den Port belegen.

## B. Direkt aus dem Quellprojekt

Vom Projekt-Hauptordner aus:

```powershell
py -m pip install -r requirements-dev.txt
py scripts/embed_web.py
py -m platformio run -d firmware
py -m platformio device list
py -m platformio run -d firmware -t erase --upload-port COM5
py -m platformio run -d firmware -t upload --upload-port COM5
py -m platformio device monitor -b 115200 --port COM5
```

`erase` nur beim Wechsel von der Werksfirmware oder bei einem bewusst gewünschten vollständigen Reset ausführen. Bei späteren CM-Radio-Updates denselben `upload` ohne `erase` nutzen. Der Browser ist eingebettet; `uploadfs` ist nicht nötig.

## WLAN und Radio

1. Im Starttext müssen `Flash: 8388608 Bytes` und eine verfügbare PSRAM stehen. `PSRAM fehlt` ist ein Fehler, vor dem Audiotest beheben.
2. Auf dem Handy mit dem angezeigten `CM-Radio-XXXXXX`-WLAN verbinden. Das zufällige Passwort steht im seriellen Monitor. Androids Hinweis „Kein Internet“ akzeptieren und im Setup-WLAN bleiben.
3. `http://192.168.4.1` im Browser öffnen, Heimnetz-SSID und Passwort speichern.
4. Handy wieder mit dem Heimnetz verbinden. `http://cm-radio.local` öffnen; falls die Namensauflösung nicht funktioniert, Geräte-IP aus Router oder serieller Ausgabe verwenden.
5. Der MP3-Teststream startet bei aktivem Autostart selbstständig. Lautstärke zunächst bei 5/21 belassen. Beide Lautsprecher und Play/Stop testen.
6. Eigene direkte MP3-/AAC-Stream-URLs unter „Sender verwalten“ speichern, gewünschten Sender abspielen.
7. Nach Lautstärkeänderungen mindestens zwei Sekunden bis zum Ausschalten warten; im Status muss „Gespeichert“ stehen.

## Diagnose und Rückweg

| Symptom | Prüfung / Aktion |
| --- | --- |
| Kein COM-Port | Anderes Datenkabel, USB-Port, Treiber für den tatsächlich verbauten USB-UART-Chip prüfen |
| Flash-Verbindung scheitert | Monitor schließen; BOOT gedrückt halten, EN kurz drücken, Flash erneut starten, BOOT nach Verbindungsaufbau loslassen |
| Falsche Flashgröße | Abbrechen, Modul/Boardvariante klären |
| Kein Ton trotz aktivem Stream | Beide Lautsprecherklemmen, GPIO-13-Freigabe/Revision und Lautstärke prüfen; „Stream aktiv“ ist kein akustischer Nachweis |
| Nur ein Kanal | Verkabelung und echte Stereo-Testdatei prüfen; ein Sender kann Mono senden |
| WLAN verbindet nicht | 2,4 GHz, SSID, Passwort, Signal; nach 30 s erscheint Setup-WLAN |
| Kein Zugriff auf `.local` | Geräte-IP statt mDNS verwenden |
| Wiederholte Neustarts | 5-V-Versorgung, Kabel, serielles Reset-Protokoll, Heap/PSRAM prüfen |

Seriell `status` gibt Hardware/IP aus, `setup` öffnet erneut das Setup-WLAN, `reset-wifi` löscht nur das gespeicherte WLAN und startet die Einrichtung neu. Vollständiges erneutes Löschen ist über das Erstinstallationsskript möglich.

## Automatischer Erststarttest

Nach der Verbindung mit dem Heim-WLAN im entpackten Firmwarepaket ausführen:

```powershell
py smoke_test.py http://cm-radio.local --report CM-Radio_Boardtest.json
```

Im Quellprojekt lautet der Befehl:

```powershell
py scripts/smoke_test.py http://cm-radio.local --report CM-Radio_Boardtest.json
```

Falls `.local` nicht aufgelöst wird, `http://cm-radio.local` durch `http://GERAETE-IP` ersetzen. Der PC muss im gleichen Heimnetz sein. Python genügt; das Prüfprogramm benötigt keine zusätzlichen Pakete.

Der Test liest ausschließlich Status, Senderliste und Konfiguration. Er prüft 19 Kriterien, unter anderem Firmwareversion, Flash, nutzbare PSRAM, WLAN, Audioinitialisierung, gespeicherte Einstellungen und gültige Senderauswahl. Lautstärke, Wiedergabe und Einstellungen werden nicht verändert. Bei einem Fehler endet das Programm mit Exitcode 1; bei Erfolg mit 0. Wenn alle API-Abfragen fehlschlagen, zuerst Adresse, WLAN und Erreichbarkeit im Browser prüfen.

Der JSON-Bericht enthält keine SSID, Geräte-IP, Sender-URLs oder WLAN-Passwörter. **PASS bestätigt die automatischen Prüfungen; die physische Hardware-Abnahme bleibt offen.** Hörprobe, Stereo, Stromneustart, Netzausfall und Dauertest anschließend nach `docs/TESTPLAN.md` durchführen.

## V0.1.2 – Diagnose am gelieferten Board

Die Weboberfläche versucht die Verbindung automatisch erneut. Bei einem fehlgeschlagenen ersten Laden werden auch Sender und WLAN-Konfiguration nachgeladen. Unter Gerätestatus lässt sich ein Diagnosebericht herunterladen; er enthält keine SSID, IP-Adresse, Sender-URL, Titel oder WLAN-Zugangsdaten. Der Bericht enthält unter anderem Firmwarestand, Speicherwerte, WLAN-Signal und den numerischen ESP32-Neustartgrund. Physische Abnahme bleibt offen.

## WLAN-Netzwerke suchen

Unter „WLAN einrichten“ auf „WLAN-Netzwerke suchen“ tippen. Das gewünschte Netzwerk aus der Liste auswählen, Passwort eingeben und speichern. Die Suche zeigt ausschließlich 2,4-GHz-Netzwerke. Versteckte SSIDs lassen sich weiter manuell eingeben. Während der Suche kann die Setup-Verbindung kurz verzögert reagieren.

## Update von V0.1.1 auf V0.1.2 (Einstellungen erhalten)

Seriellen Monitor schließen (Ctrl+]). Neues ZIP entpacken und PowerShell im neuen Paketordner öffnen. Nur die Anwendung schreiben; nicht `--erase` verwenden:

```powershell
py -3.13 -m esptool --chip esp32 --port COM5 --baud 460800 write_flash --flash_mode dio --flash_freq 40m --flash_size 8MB 0x10000 firmware.bin
```

Diese Update-Anweisung gilt für das bereits mit CM-Radio V0.1.1 installierte Loud-ESP32 mit unverändertem 8-MB-Partitionslayout. Danach Einrichtungsseite neu laden; bei Bedarf Browserseite vollständig schließen und neu öffnen.

Build 0a01 behebt abgelehnte WLAN-Suchstarts bei parallelen Verbindungsversuchen. Bei anhaltendem Fehler kann die SSID manuell eingegeben werden. Version und Build im Gerätestatus prüfen.

## Build 0a02 – neue Oberfläche

Nach dem Update die Seite vollständig neu laden. „Radio“ enthält Wiedergabe und WLAN-Balken, „Sender“ die Verwaltung, „Netzwerk“ die Einrichtung, „Gerät“ Autostart und Diagnose. Die Signalbalken sind eine Orientierung: ab −55 dBm vier grüne, ab −67 dBm drei grüne, ab −75 dBm zwei gelbe, darunter ein roter Balken. Offlinezustände zeigen keine Empfangsbalken.
