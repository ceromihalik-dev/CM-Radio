# CM-Radio V0.1 – Flashen und erster Test

## Vorbereiten

Das Firmwarepaket gilt für **Loud-ESP32 / ESP32-WROVER-N8R8, 8 MB Flash**. Modulaufdruck beim Eintreffen prüfen. Bei ESP32-S3 oder einer abweichenden Flashgröße dieses Image nicht verwenden. Das Flashskript prüft Chipfamilie und Flashkapazität vor dem Schreiben.

USB-C-Datenkabel, stabiles 5-V-Netzteil bzw. geeigneten USB-Anschluss, 2,4-GHz-WLAN und einen PC bereitlegen. Für Lautsprechertests eine ausreichende Stromversorgung verwenden; ein schwacher PC-USB-Port kann bei höherer Lautstärke einen Neustart auslösen.

Lautsprecher bei ausgeschaltetem Board jeweils an den eigenen Zweipol-Ausgang anschließen. Die Ausgänge der Class-D-Verstärker besitzen **keine gemeinsame Lautsprechermasse**: Lautsprecher-Minus weder miteinander noch mit GND verbinden. Zunächst frei auf dem Tisch testen; erst nach erfolgreicher Abnahme in das Wandgehäuse setzen.

## A. Kompiliertes Erstinstallationspaket

1. ZIP entpacken. Terminal im Ordner mit `flash.py` und `CM-Radio-V0.1.0-full.bin` öffnen.
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

Optionaler API-Grundtest: `py scripts/smoke_test.py http://GERAETE-IP` aus dem Quellprojekt. Er verändert keine Einstellungen und ersetzt den Hörtest nicht. Alle weiteren Abnahmeschritte stehen in `docs/TESTPLAN.md`.
