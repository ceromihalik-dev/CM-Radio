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

## Danach

| Ziel | ID | Umfang | Fertig, wenn … | Status |
| --- | --- | --- | --- | --- |
| v0.2 | RM-14 | Radio-Browser-Sendersuche und Favoriten | Gefundene Sender übernehmen; bestehende Sender bleiben bei Ausfall des Suchdiensts nutzbar | Geplant |
| Nach stabiler API | RM-15 | Android-App | Gerät im Heimnetz finden und Sender, Lautstärke, Play/Stop bedienen; Browser-Setup bleibt verfügbar | Geplant |
| Später | RM-16 | Lokal abgesicherte OTA-Updates | Update prüfen, Einstellungen erhalten und fehlgeschlagenen Start sicher behandeln | Geplant |

Keine festen Termine zugesagt. Weitere Funktionen richten sich nach tatsächlicher Nutzung.

## Versions- und Pflegekonvention

Aktuell **v0.1.2 · Build 0a01**. Weitere Entwicklungsstände derselben Version: **0a02, 0a03 …**. Firmware, Status-API, Weboberfläche und Paketmanifest führen dieselbe Kennung. Reine Dokumentationsänderungen erhöhen den Firmware-Build nicht.

Bei Änderungen Roadmap, Bugliste und betroffene Testkriterien zusammen aktualisieren. Für Fehler stabile CMR-IDs verwenden; gelöste Einträge bleiben mit Fix-Build und Nachweis erhalten. Änderungen an Firmware müssen kompilieren und die passenden Prüfungen bestehen. Ein öffentlicher Release wird erst als vollständig hardwaregetestet bezeichnet, wenn seine Abnahmekriterien nachgewiesen sind.
