# CM-Radio – Roadmap

Stand: **9. Oktober 2026 · v0.1.3 · Build 07**. Referenzhardware: geliefertes Loud-ESP32 E3 / ESP32-WROVER-N8R8, zwei 3-W-/8-Ω-Lautsprecher.

Diese Datei ist die verbindliche Projekt-Roadmap. Fehler und deren Abnahme stehen in [BUGLISTE.md](BUGLISTE.md), einzelne Hardwarekriterien im [TESTPLAN.md](TESTPLAN.md). Aussagen im Chat werden bei der nächsten Projektaktualisierung hier mit Datum und Nachweis übernommen. Ein bestandener Teiltest ersetzt keine vollständige Hardwareabnahme.

## Erreicht

| ID | Meilenstein | Status / Nachweis |
| --- | --- | --- |
| RM-01 | Firmwarebasis: lokale Websteuerung/API, Senderverwaltung, NVS, Audio-Task, MP3/AAC-Unterstützung | Implementiert und Build/Hosttests bestanden; einzelne Funktionen noch nicht auf Hardware abgenommen |
| RM-02 | USB-Erstinstallation und Update | Nutzer-Screenshots bestätigen Schreiben und Hashprüfung von V0.1.1 und V0.1.2 |
| RM-03 | Setup und Suche nach verfügbaren 2,4-GHz-WLANs | PASS: Nutzer bestätigt Suche in Build 0a01 am 09.10.2026 |
| RM-04 | Grundlegende Tonwiedergabe und Bedienung | PASS: Nutzer bestätigt Ton aus beiden Lautsprechern sowie Lautstärke, Stop und Play am 09.10.2026 |
| RM-05 | Automatischer Start nach Stromunterbrechung | PASS: Nutzer bestätigt USB abziehen/wieder einstecken am 09.10.2026; Erhalt eigener Sender und Lautstärke noch separat prüfen |
| RM-06 | Web-Wiederverbindung und Diagnosebericht | Implementiert, Hosttests PASS; vollständiger Gerätetest offen |
| RM-07 | Wandgehäuse W2: Schraubbefestigung und gemessener E3-Lochraster | CAD erstellt und geprüft; Druck, Passform und Betrieb im Gehäuse offen |

## Nächste Schritte – Stabilität und Hardwareabnahme

| Priorität | ID | Arbeit | Abnahme | Status |
| --- | --- | --- | --- | --- |
| 1 | RM-08 | Dauerbetrieb prüfen | Zunächst 30 Minuten als Zwischenprüfung, danach RUN-01: 60 Minuten ohne Resets/anhaltende Aussetzer; Heap beobachten | Nutzer meldet bisher unauffälligen Dauertest; genaue Dauer und Endstatus offen |
| 1 | RM-09 | WLAN- und Stream-Wiederverbindung | Falsches Passwort, WLAN-Unterbrechung und ungültiger Stream nach NET-03 / REC-01 / REC-02 | Offen |
| 1 | RM-10 | Audio und Einstellungen vollständig prüfen | Getrennte Links-/Rechts-Testdatei, AAC, eigene Sender, gespeicherte Lautstärke, Autostart aus | Offen |
| 2 | RM-11 | USB-Update komfortabler machen | Fehler verständlich anzeigen, passende Python-Umgebung nutzen; Bootmodus-Hilfe; Einstellungen erhalten | Geplant; siehe CMR-002 / CMR-003 |
| 2 | RM-12 | Hardware-Testprotokoll und Release-Abnahme abschließen | Offene Kriterien aus TESTPLAN erfüllen und konkrete Version/Build dokumentieren; CI-Ergebnis prüfen | Offen |
| 2 | RM-13 | Wandgehäuse praktisch prüfen | Lochraster, Anschlüsse, Wandmontage, Temperatur und WLAN nach Einbau | Offen |

## Funktionserweiterungen vor der Android-App

Verbindliche Wünsche vom **09.10.2026**. Die folgenden Funktionen werden zunächst in Firmware und Weboberfläche integriert und geprüft. Versionsziele außer dem aktuellen Stand sind vorläufig; es sind keine festen Termine zugesagt.

| Reihenfolge | ID | Umfang | Fertig, wenn … | Status |
| --- | --- | --- | --- | --- |
| 1 | RM-17 | GUI deutlich aufwerten | Moderne, übersichtliche Oberfläche für Handy und Desktop; klare Navigation für Wiedergabe, Sender, Klang, Netzwerk, Updates und Infos; gut lesbare Zustände und verständliche Rückmeldungen | Erste Umsetzung in Build 0a02, Nutzerabnahme PASS; Gerät in Build 04 für Smartphone und Desktop kompakt gegliedert; Gerätetest Build 04 offen |
| 2 | RM-18 | Netzwerkstärke grafisch anzeigen | WLAN-Empfang als Balken von Grün über Gelb bis Rot darstellen; dBm-Wert und Text ergänzen; getrennte Anzeige für offline und laufende Verbindung; Anzeige regelmäßig aktualisieren | Implementiert in Build 0a02, Hosttests PASS; Nutzerabnahme des Builds PASS |
| 3 | RM-14 | Radiosender international, national und lokal suchen; Favoriten | Radio-Browser als vorgesehene Quelle; Suche nach Name und Land sowie lokalen/regionalen Sendern über Ort/Region oder Suchbegriffe, soweit Verzeichnisdaten das ermöglichen; Ergebnisse abspielen und speichern; Suchdienstausfall blockiert bestehende Sender nicht | Erste Umsetzung in Build 0a03, Softwaretests und Nutzerabnahme PASS |
| 4 | RM-19 | Klangeigenschaften: Höhen, Bässe, Loudness und Balance | Regler mit neutraler Grundeinstellung, Rücksetzen und Speicherung; hörbare Wirkung ohne störende Übersteuerung; CPU-/Speicherbedarf und echte Links-/Rechts-Balance am Board prüfen | Teilumsetzung in Build 0a09: Bässe, Höhen und Balance; Nutzer bestätigt 0a09 PASS. Direkte Klangvorschau ergänzt in 0a0a; Hosttests PASS, Nutzer bestätigt Gerätetest PASS am 09.10.2026. Loudness implementiert in v0.1.3 Build 01; Hosttests PASS, Nutzer bestätigt Gerätetest PASS am 09.10.2026 |
| 5 | RM-16 | Updatefunktion in der Weboberfläche | Firmware lokal über den Browser aktualisieren; Zielhardware und Version/Build prüfen, Fortschritt/Ergebnis anzeigen und Einstellungen erhalten; Zugriff absichern und Rückweg bei fehlgeschlagenem Start vorsehen | Teilumsetzung Build 0a08: lokaler Paketupload, Größen-/Hashprüfung und freier Slot. Hosttests PASS; Nutzer bestätigt Build 0a08 und Browserupdate-Test als PASS am 09.10.2026. Passwortschutz für Updates/Änderungen auf Nutzerwunsch vorerst zurückgestellt; Signaturen und Rückweg bei fehlerhaftem Start noch offen |
| 6 | RM-20 | Erstellerinformationen und Unterstützungslink integrieren | Infobereich mit abgestimmten Erstellerangaben, Projekt-/GitHub-Link und frei aufrufbarem Unterstützungslink; Zieladresse vor Integration festlegen | Implementiert in v0.1.3 Build 03: C. Mihalik, GitHub und PayPal-Ziel aus CM IR Viewer übernommen; Nutzer bestätigt Build 03 PASS am 09.10.2026 |
| 7 | RM-21 | Changelog in der Oberfläche integrieren | Aktuelle Version/Build und Änderungen direkt am Gerät anzeigen; ältere Einträge nachvollziehbar erhalten; veröffentlichte Angaben stimmen mit Repository und Paket überein | Implementiert in Build 0a06; Hosttests PASS, Gerätetest offen |
| 8 | RM-22 | Sleep-Timer | Voreinstellungen 15/30/60 Minuten und frei wählbare Dauer; Restzeit anzeigen, Timer ändern/abbrechen; bei Ablauf Wiedergabe stoppen | Implementiert in Build 0a04; Nutzer meldet Build PASS am 09.10.2026 |
| 9 | RM-23 | Wecker und Zeitplan | Entfällt aus dem Funktionsumfang auf Nutzerwunsch vom 09.10.2026 | Gestrichen; keine Voraussetzung für Android |
| 10 | RM-24 | Sanfter Start | Beim Einschalten, Autostart  Lautstärke von leise auf Zielwert erhöhen; Rampendauer einstellen; Stop und manuelle Lautstärkeänderung wirken sofort | Implementiert in Build 0a04; Nutzer meldet Build PASS am 09.10.2026 |
| 11 | RM-25 | Maximale Lautstärke begrenzen | Gespeicherte Obergrenze gilt für Web/API, Autostart ; Regler und Zielwerte überschreiten die Grenze nicht | Implementiert in Build 0a04; Nutzer meldet Build PASS am 09.10.2026 |
| 12 | RM-26 | Ersatzsender bei Ausfall | Ersatzsender festlegen; nach begrenzten erfolglosen Streamversuchen umschalten; Wechsel anzeigen; kein endloser Wechselkreislauf; manuelles Stoppen bleibt wirksam | Implementiert in 0a05; Hosttests PASS; Nutzer bestätigt Build 0a05 als PASS am 09.10.2026 |
| 13 | RM-27 | Einstellungen sichern und wiederherstellen | Sender/Favoriten, Klang, Lautstärkegrenze als versionierte Datei exportieren/importieren; vor Übernahme auf Gültigkeit prüfen; WLAN-Passwörter und Zugangsdaten standardmäßig ausschließen | Sender und vorhandene Wiedergabeeinstellungen implementiert in 0a05; Hosttests PASS; Nutzer bestätigt Build 0a05 als PASS am 09.10.2026. Klang ergänzt in 0a09, Gerätetest offen; Wecker/Zeitpläne entfallen |
| 14 | RM-28 | Senderlogos und Titelanzeige | Senderlogo sowie Titel/Interpret anzeigen, soweit Daten verfügbar; Platzhalter bei fehlenden Angaben; ausgefallene Logoquellen blockieren die Wiedergabe nicht | Implementiert in v0.1.3 Build 02; Hosttests PASS, Nutzer bestätigt Gerätetest PASS am 09.10.2026 |
| 15 | RM-29 | Schnellwahl | Große Favoritenkacheln zum direkten Starten; Reihenfolge ändern und dauerhaft speichern; aktiven Sender eindeutig markieren | Implementiert in Build 0a06; Hosttests PASS, Gerätetest offen |
| Danach | RM-15 | Android-App, sobald alle vorgesehenen Funktionen integriert sind | RM-14 und RM-16 bis RM-29 außer gestrichenem RM-23 integriert und geprüft, stabile API vorhanden; App findet das Gerät und bedient Wiedergabe, Sender, Klang und Sleep-Timer sowie Netzwerk-/Updateinformationen; Browser-Setup bleibt verfügbar | Geplant; Beginn erst nach Funktionsintegration |

Die Reihenfolge dient der Umsetzung und kann nach Abhängigkeiten angepasst werden. **Die Android-App beginnt erst nach Integration und Prüfung der oben vorgesehenen Funktionen.** RM-08 bis RM-13 zur Stabilität und Hardwareabnahme laufen weiter. Wünsche werden als Roadmap-Einträge geführt und nicht als bestätigte Bugs.

## Versions- und Pflegekonvention

Aktuell **v0.1.3 · Build 08**. Weitere Builds innerhalb dieser Version: **07, 08 …**. Firmware, Status-API, Weboberfläche und Paketmanifest führen dieselbe Kennung. Jedes neue Firmware-ZIP enthält eine ausführliche USB-Erstinstallationsanleitung. Reine Dokumentationsänderungen erhöhen den Firmware-Build nicht.

Bei Änderungen Roadmap, Bugliste und betroffene Testkriterien zusammen aktualisieren. Für Fehler stabile CMR-IDs verwenden; gelöste Einträge bleiben mit Fix-Build und Nachweis erhalten. Änderungen an Firmware müssen kompilieren und die passenden Prüfungen bestehen. Ein öffentlicher Release wird erst als vollständig hardwaregetestet bezeichnet, wenn seine Abnahmekriterien nachgewiesen sind.

Build 0a07 korrigiert den seit 0a05 gemeldeten periodischen Stream-Neustart (CMR-004) durch Entfernen des Audiozeit-Stillstandswächters. Bestätigung am betroffenen Sender steht aus.

Build 05: 50 Lautstärkestufen mit abgerundeter Migration alter Lautstärkegrenzen; Netzwerk unter Gerät. Build und Hosttests PASS; Nutzer bestätigt Build 05 am 09.10.2026 um 20:04 Uhr als PASS (Lautstärke, Obergrenze, Neustart und WLAN-Suche). Build 04 ohne gesonderte Nutzerabnahme.

Build 06: dauerhafter Setup-/Fallback-Zugang, Erstpasswort passwort mit verpflichtendem Wechsel; später unter Gerät → Netzwerk änderbar. Separate NVS-Speicherung, aus Backup ausgeschlossen, USB-Zurücksetzen nur dieses Zugangs möglich. Build und Hosttests PASS; Gerätetest offen. Allgemeiner Bedien-/Update-Passwortschutz bleibt zurückgestellt.

Passwortreset per Taste ab Build 06: Bei laufendem Radio BOOT/IO0 10–59 Sekunden halten und loslassen. Nur Setup-/Fallback-Passwort wird auf passwort zurückgesetzt; verpflichtender Wechsel beim nächsten Browseraufruf. Nicht mit BOOT beim Einschalten verwechseln (Flashmodus). Während eines Firmwareupdates wird der Reset ignoriert; anschließend neu halten. Prüfen: kurzer Druck bewirkt nichts, ein langer Druck löst einmal aus, Heimnetz/Sender/Klang bleiben erhalten.

Werkseinstellungen über dieselbe BOOT/IO0-Taste: Bei laufendem Radio mindestens 60 Sekunden halten und loslassen. Erst das Loslassen löst den vollständigen Reset aus. Heim-WLAN, Sender, Klang, Lautstärke und Setup-Passwort werden gelöscht; Firmware bleibt installiert, Radio startet neu. Danach Erstzugang mit passwort und verpflichtender Änderung. Während Firmwareupdates werden Tastenresets ignoriert; Taste neu betätigen. Gerätetest: kurzer Druck ohne Wirkung, 10–59 s nur Passwort, ab 60 s vollständiger Reset. Vor dem Test Einstellungen sichern; Sicherung enthält keine Zugangspasswörter.

Build 07: Radio als Startseite auch im Fallback; nach Erstwechsel ebenfalls Radio, Netzwerk geschlossen. Passwort bleibt bei Neuladen und Updates gespeichert. Mindestlänge 8 wegen ESP32-WPA2; vier Zeichen technisch nicht direkt möglich. Gerätetest offen.

Nutzer bestätigt v0.1.3 Build 07 am 09.10.2026 um 20:32 Uhr (Europe/Berlin) als PASS nach angefragter Prüfung von Radio-Startseite und Passworterhalt nach Seitenneuladen und Neustart. Kein gesonderter Nachweis für Tasten-/Werksreset oder vollständige Hardwareabnahme.

## v0.1.3 Build 08

Gerätename, Mono/Stereo, Verbindungsdiagnose und Senderreparatur integriert. Hosttests und Kompilierung geprüft; Hardwareabnahme dieser vier Funktionen offen. Bluetooth nicht aktiviert.

| ID | Funktion | Stand |
| --- | --- | --- |
| RM-30 | Gerätename ändern | Build 08 implementiert; Boardtest offen |
| RM-31 | Mono/Stereo | Build 08 implementiert; Boardtest offen |
| RM-32 | Verbindungsqualität anzeigen | Build 08 implementiert; Boardtest offen |
| RM-33 | Sender automatisch wiederfinden | Build 08 implementiert; Boardtest offen |
