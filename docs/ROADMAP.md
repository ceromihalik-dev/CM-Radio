# CM-Radio – Roadmap

Stand: **9. Oktober 2026 · v0.1.2 · Build 0a01**. Referenzhardware: geliefertes Loud-ESP32 E3 / ESP32-WROVER-N8R8, zwei 3-W-/8-Ω-Lautsprecher.

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

## Nächste Schritte – v0.1.2 stabilisieren

| Priorität | ID | Arbeit | Abnahme | Status |
| --- | --- | --- | --- | --- |
| 1 | RM-08 | Dauerbetrieb prüfen | Zunächst 30 Minuten als Zwischenprüfung, danach RUN-01: 60 Minuten ohne Resets/anhaltende Aussetzer; Heap beobachten | Offen |
| 1 | RM-09 | WLAN- und Stream-Wiederverbindung | Falsches Passwort, WLAN-Unterbrechung und ungültiger Stream nach NET-03 / REC-01 / REC-02 | Offen |
| 1 | RM-10 | Audio und Einstellungen vollständig prüfen | Getrennte Links-/Rechts-Testdatei, AAC, eigene Sender, gespeicherte Lautstärke, Autostart aus | Offen |
| 2 | RM-11 | USB-Update komfortabler machen | Fehler verständlich anzeigen, passende Python-Umgebung nutzen; Bootmodus-Hilfe; Einstellungen erhalten | Geplant; siehe CMR-002 / CMR-003 |
| 2 | RM-12 | Hardware-Testprotokoll und Release-Abnahme abschließen | Offene Kriterien aus TESTPLAN erfüllen und konkrete Version/Build dokumentieren; CI-Ergebnis prüfen | Offen |
| 2 | RM-13 | Wandgehäuse praktisch prüfen | Lochraster, Anschlüsse, Wandmontage, Temperatur und WLAN nach Einbau | Offen |

## Funktionserweiterungen vor der Android-App

Verbindliche Wünsche vom **09.10.2026**. Die folgenden Funktionen werden zunächst in Firmware und Weboberfläche integriert und geprüft. Versionsziele außer dem aktuellen Stand sind vorläufig; es sind keine festen Termine zugesagt.

| Reihenfolge | ID | Umfang | Fertig, wenn … | Status |
| --- | --- | --- | --- | --- |
| 1 | RM-17 | GUI deutlich aufwerten | Moderne, übersichtliche Oberfläche für Handy und Desktop; klare Navigation für Wiedergabe, Sender, Klang, Netzwerk, Updates und Infos; gut lesbare Zustände und verständliche Rückmeldungen | Geplant |
| 2 | RM-18 | Netzwerkstärke grafisch anzeigen | WLAN-Empfang als Balken von Grün über Gelb bis Rot darstellen; dBm-Wert und Text ergänzen; getrennte Anzeige für offline und laufende Verbindung; Anzeige regelmäßig aktualisieren | Geplant |
| 3 | RM-14 | Radiosender international, national und lokal suchen; Favoriten | Radio-Browser als vorgesehene Quelle; Suche nach Name und Land sowie lokalen/regionalen Sendern über Ort/Region oder Suchbegriffe, soweit Verzeichnisdaten das ermöglichen; Ergebnisse abspielen und speichern; Suchdienstausfall blockiert bestehende Sender nicht | Geplant |
| 4 | RM-19 | Klangeigenschaften: Höhen, Bässe, Loudness und Balance | Regler mit neutraler Grundeinstellung, Rücksetzen und Speicherung; hörbare Wirkung ohne störende Übersteuerung; CPU-/Speicherbedarf und echte Links-/Rechts-Balance am Board prüfen | Geplant; technische Umsetzung in der Audiokette prüfen |
| 5 | RM-16 | Updatefunktion in der Weboberfläche | Firmware lokal über den Browser aktualisieren; Zielhardware und Version/Build prüfen, Fortschritt/Ergebnis anzeigen und Einstellungen erhalten; Zugriff absichern und Rückweg bei fehlgeschlagenem Start vorsehen | Geplant; OTA statt ausschließlich USB |
| 6 | RM-20 | Erstellerinformationen und Unterstützungslink integrieren | Infobereich mit abgestimmten Erstellerangaben, Projekt-/GitHub-Link und frei aufrufbarem Unterstützungslink; Zieladresse vor Integration festlegen | Geplant; Erstellerangaben und Unterstützungsadresse noch festzulegen |
| 7 | RM-21 | Changelog in der Oberfläche integrieren | Aktuelle Version/Build und Änderungen direkt am Gerät anzeigen; ältere Einträge nachvollziehbar erhalten; veröffentlichte Angaben stimmen mit Repository und Paket überein | Geplant |
| Danach | RM-15 | Android-App, sobald alle vorgesehenen Funktionen integriert sind | RM-14 und RM-16 bis RM-21 integriert und geprüft, stabile API vorhanden; App findet das Gerät und bedient Wiedergabe, Sender, Klang sowie Netzwerk-/Updateinformationen; Browser-Setup bleibt verfügbar | Geplant; Beginn erst nach Funktionsintegration |

Die Reihenfolge dient der Umsetzung und kann nach Abhängigkeiten angepasst werden. **Die Android-App beginnt erst nach Integration und Prüfung der oben vorgesehenen Funktionen.** RM-08 bis RM-13 zur Stabilität und Hardwareabnahme laufen weiter. Wünsche werden als Roadmap-Einträge geführt und nicht als bestätigte Bugs.

## Versions- und Pflegekonvention

Aktuell **v0.1.2 · Build 0a01**. Weitere Entwicklungsstände derselben Version: **0a02, 0a03 …**. Firmware, Status-API, Weboberfläche und Paketmanifest führen dieselbe Kennung. Reine Dokumentationsänderungen erhöhen den Firmware-Build nicht.

Bei Änderungen Roadmap, Bugliste und betroffene Testkriterien zusammen aktualisieren. Für Fehler stabile CMR-IDs verwenden; gelöste Einträge bleiben mit Fix-Build und Nachweis erhalten. Änderungen an Firmware müssen kompilieren und die passenden Prüfungen bestehen. Ein öffentlicher Release wird erst als vollständig hardwaregetestet bezeichnet, wenn seine Abnahmekriterien nachgewiesen sind.
