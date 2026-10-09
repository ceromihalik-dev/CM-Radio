# CM-Radio – Flashen und erster Test

Die ausführliche Windows-USB-Anleitung liegt in jedem Paket als USB_ERSTINSTALLATION.txt. Sie enthält die passenden Versions- und Dateinamen sowie den Unterschied zwischen Erstinstallation und Updates nach OTA.

## Vorbereiten

Das Firmwarepaket gilt für **Loud-ESP32 / ESP32-WROVER-N8R8, 8 MB Flash**. Modulaufdruck beim Eintreffen prüfen. Bei ESP32-S3 oder einer abweichenden Flashgröße dieses Image nicht verwenden. Das Flashskript prüft Chipfamilie und Flashkapazität vor dem Schreiben.

USB-C-Datenkabel, stabiles 5-V-Netzteil bzw. geeigneten USB-Anschluss, 2,4-GHz-WLAN und einen PC bereitlegen. Für Lautsprechertests eine ausreichende Stromversorgung verwenden; ein schwacher PC-USB-Port kann bei höherer Lautstärke einen Neustart auslösen.

Lautsprecher bei ausgeschaltetem Board jeweils an den eigenen Zweipol-Ausgang anschließen. Die Ausgänge der Class-D-Verstärker besitzen **keine gemeinsame Lautsprechermasse**: Lautsprecher-Minus weder miteinander noch mit GND verbinden. Zunächst frei auf dem Tisch testen; erst nach erfolgreicher Abnahme in das Wandgehäuse setzen.

## A. Kompiliertes Erstinstallationspaket

1. ZIP entpacken. Terminal im Ordner mit `flash.py` und `CM-Radio-V0.1.3-full.bin` öffnen.
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

## Build 0a03 – Radiosender suchen

„Sender“ öffnen und Suchbereich wählen: „International“ weltweit, „National“ im gewählten Land oder „Lokal / regional“ nach Ort/Region bzw. Sendernamen. Weitere Länder lassen sich nachladen. Ohne Suchbegriff werden bei international/national beliebte Sender angezeigt. Lokale Suchbegriffe werden gegen Sendernamen und Regionsangaben abgefragt; eine Entfernungssuche gibt es noch nicht.

„Sender suchen“ benötigt Internet im Handy-/PC-Browser. Einen Treffer über „Zur Sammlung hinzufügen“ übernehmen und anschließend „Änderungen speichern“ drücken. Danach unter „Radio“ auswählen und abspielen. Maximal zehn Sender bleiben gespeichert; bestehende Entwürfe bleiben erhalten. Eine Verzeichnisstörung beeinträchtigt die gespeicherte Sammlung nicht. Senderdaten können veraltet sein; Hörprobe erforderlich.

Suchbegriff und Land werden an Radio-Browser übertragen; WLAN-Passwörter werden nicht übertragen. Quelle und API: https://docs.radio-browser.info/ .

## Build 0a04 – Sleep-Timer, sanfter Start und Grenze

Unter „Radio“ Sleep-Timer mit 15/30/60 Minuten oder eigener Dauer 1–180 Minuten setzen. „Timer aufheben“ beendet nur den Timer, „Stoppen“ beendet Wiedergabe und Timer. Senderwechsel lässt die Restzeit weiterlaufen. Nach Stromneustart ist kein Timer aktiv. Die Restzeit wird regelmäßig mit dem Gerätestatus aktualisiert.

Unter „Gerät“ maximale Lautstärke 0–21 und sanften Start 0–30 Sekunden einstellen und speichern. 0 Sekunden schaltet die Rampe ab; Standard 5 Sekunden. Eine Grenze von 0 schaltet die Ausgabe stumm. Absenken der Grenze reduziert auch den gespeicherten Zielwert; Erhöhen hebt die Lautstärke nicht automatisch an. Manuelle Lautstärkeänderungen beenden eine laufende Rampe.

Update wie zuvor mit `firmware.bin` an 0x10000 ohne Löschen. Vorhandene Sender/WLAN bleiben gespeichert; neue Felder erhalten Standardwerte. Nach Update Seite vollständig neu laden und Migration am Gerät prüfen.

## Build 0a05 testen

Update weiterhin ausschließlich `firmware.bin` an `0x10000` schreiben, ohne Flash zu löschen. Unter **Gerät** Ersatzsender aus der gespeicherten Liste auswählen und Wiedergabeeinstellungen speichern. Bei ungespeicherten Senderentwürfen zuerst die Sammlung speichern.

**Sicherung herunterladen** exportiert gespeicherte Sender und vorhandene Wiedergabeeinstellungen ohne WLAN-Zugangsdaten. Zum Wiederherstellen Datei auswählen, **Datei prüfen**, Zusammenfassung kontrollieren, anschließend **Geprüfte Sicherung übernehmen**. Übernahme ersetzt diese Einstellungen, stoppt Audio und beendet den Timer; Heim-WLAN bleibt erhalten. Danach manuell starten. Klang wurde später ergänzt; Wecker/Zeitpläne entfallen auf Nutzerwunsch.

Ersatzsender wird nach drei erfolglosen Verbindungsversuchen bei vorhandenem WLAN aktiviert. Die Wartezeit hängt von Stream-Timeouts ab. Ein automatischer Rückwechsel erfolgt nicht; manuelles Play beginnt erneut mit dem ausgewählten Sender. Bei WLAN-Ausfall allein erfolgt kein Wechsel. Bei Änderung eines bereits laufenden Ersatzsenders wird die neue Auswahl beim nächsten Wiedergabestart verwendet.

## Build 0a06 testen

Nach dem Firmwareupdate die Seite mit Strg+F5 neu laden. Unter Radio startet ein Tipp auf eine Schnellwahlkachel den gespeicherten Sender. Unter Sender ändern Nach oben/Nach unten die Reihenfolge als Entwurf; Änderungen speichern übernimmt sie dauerhaft. Der Ersatzsender wird dabei anhand seiner Streamadresse erhalten. Unter Gerät stehen aktuelle und bisherige Änderungen zum Aufklappen bereit, ohne Internetverbindung zum Changelog.

## Build 0a07

Korrektur gegen seit 0a05 gemeldete periodische Stream-Neustarts. Nach Update Strg+F5, denselben Sender mindestens zehn Minuten testen. Einstellungen bleiben beim Schreiben nur von firmware.bin erhalten.

## Build 0a08 – Update im Browser

Einmalig 0a08 per USB flashen und mit Strg+F5 neu laden. Für spätere Updates: ZIP entpacken, unter Gerät manifest.json und firmware.bin aus demselben Paket auswählen, Paket prüfen, Checkbox zur Installation aktivieren und Firmware installieren. Keine full.bin, kein Bootloader. Größe/Header/SHA-256 werden vor Aktivierung geprüft. Netzteil während des Schreibens angeschlossen lassen. Nach automatischem Neustart Verbindung abwarten, Seite mit Strg+F5 neu laden und installierten Build prüfen. Einstellungen bleiben erhalten; Autostart gilt beim Neustart.

Erster Test: Das Paket 0a08 nochmals über den Browser installieren und Neustart sowie erhaltenes WLAN/Sender prüfen. Bei fehlerhafter Datei bleibt die bisherige Firmware aktiv und Audio kann manuell neu gestartet werden. Bei verloren gegangener Antwort nach vollständiger Übertragung zuerst den installierten Build prüfen. Pakete vor 0a08 haben noch keine passenden Update-Metadaten. Das Update lädt Dateien lokal vom Handy/PC, nicht automatisch von GitHub. Nach OTA kann der aktive Slot wechseln; die bisherige USB-Anweisung 0x10000 trifft dann nicht zwingend die aktive Anwendung. Für USB-Recovery den aktiven Slot klären, statt blind nur 0x10000 zu überschreiben.

## Build 0a09 – Klang

Über Gerät/Firmwareupdate die manifest.json und firmware.bin aus Paket 0a09 installieren. Nach Neustart Strg+F5. Unter Gerät Bässe/Höhen/Balance einstellen und Klang speichern. Neutral einstellen ist erst ein Entwurf und braucht Speichern. Bei Balance −16 darf nur der linke Kanal, bei +16 nur der rechte Kanal hörbar sein; physische Zuordnung der angeschlossenen Lautsprecher prüfen. Danach Balance Mitte speichern. Klangwerte nach Stromneustart und nach Sicherung/Wiederherstellung prüfen. Alte Sicherungen ohne Klangfelder stellen neutralen Klang her.

## Build 0a0a – Direkt hören

Über Browserupdate installieren, danach Strg+F5. Regler unter Gerät verändern den Klang direkt als Vorschau. Klang dauerhaft speichern macht die Werte neustartfest. Gespeicherte Werte wiederherstellen verwirft die Vorschau. Neutral hören setzt die Vorschau auf 0; nur Speichern übernimmt dauerhaft. Sicherungen enthalten die gespeicherten Werte. Vorschau bleibt bei Senderwechsel und Stop/Play bestehen, nach Neustart gilt gespeicherter Klang.

## v0.1.3 · Build 01

Update über Browser mit manifest.json und firmware.bin, dann Strg+F5. Loudness bei leiser Wiedergabe unter Gerät ein-/ausschalten; direkt hörbare Vorschau. Klang dauerhaft speichern übernimmt die Wahl. Zur USB-Erstinstallation die beigefügte USB_ERSTINSTALLATION.txt verwenden.

## v0.1.3 · Build 02

Nach Browserupdate Strg+F5. Logos für neue Suchtreffer werden bei vorhandener geeigneter HTTPS-Favicon-Adresse übernommen. Für bestehende Sender Logo-Adresse unter Sender ergänzen und Änderungen speichern. Bei fehlendem/defektem Logo erscheint ein CM-Platzhalter, Audio bleibt unabhängig. Bilder werden vom Handy/PC geladen und brauchen dessen Internetzugang. Interpret/Titel werden aus gängigen Streammetadaten getrennt; nicht jeder Sender liefert sie.
