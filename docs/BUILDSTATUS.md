# Buildstatus – CM-Radio v0.1.2 · Build 0a05

Datum: **9. Oktober 2026**. Lokal geprüft auf Linux x86_64 / Python 3.12. Das E3-Board ist beim Nutzer angekommen; hier kein direkter USB-Zugriff. USB-Flash und Boot von V0.1.1 sowie das Schreiben von V0.1.2 sind durch Nutzer-Screenshots bestätigt. Nutzer meldet abgelehnten WLAN-Suchstart in V0.1.2 ohne Buildkennung. Die Korrektur in Build 0a01 wurde vom Nutzer bestätigt. Ton aus beiden Lautsprechern, Lautstärke/Stop/Play und Autostart nach Stromunterbrechung sind ebenfalls bestätigt; vollständige Hardwareabnahme bleibt offen.

| Prüfung | Ergebnis |
| --- | --- |
| PlatformIO `loud_wrover` | **PASS** |
| Arduino-ESP32 / Framework | 2.0.17 / 3.20017.241212+sha.dcc1105b |
| ESP32-audioI2S | Tag 3.0.12, Commit `928c420d49fce2a09fa91f490b9fcabed6447c67` |
| ArduinoJson | 6.21.5 |
| Programmcode | 1.308.009 Bytes / 3.145.728 Bytes (41,6 %) |
| Statische RAM-Belegung | 51.932 Bytes / 327.680 Bytes (15,8 %) |
| Anwendung / Bootloader | Chip ESP32, 8 MB, 40 MHz, DIO; Checksum/Validierungshash gültig |
| Flashlayout | Keine Überlappung; zwei 3-MiB-Slots, Gesamtgröße 8 MB |
| URL-/WLAN-Eingaben | Positivfälle, ungültige Protokolle, Header-Steuerzeichen, Grenzen geprüft |
| WLAN-Suchkoordination | Vorbereitung, doppelte Anfragen, begrenzte Wiederholungen, Timeout, Wiederherstellung und millis-Überlauf: PASS (Hosttest) |
| Wiederverbindung | Backoff-Grenze und millis-Überlauf geprüft |
| Flashskript | Fünf Tests: passende Paketdatei, explizites Löschen, korrupte Datei, falsche Kapazität, korrekte Reihenfolge |
| Automatischer Erststarttest | Sechs Hosttests: gültiges Board, Fehlerzustände, ungültige Antworten, Offline-Gerät, reine GET-Abfragen, Bericht ohne private Daten; echte Boardausführung offen |
| Weboberfläche | JavaScript-Syntax, eingebettete Kopie, Bereichsnavigation, WLAN-Balken/Farben/Offlinezustände, Wiederverbindung nach Ladefehler, keine parallelen Hintergrundabfragen, Erhalt von Senderentwürfen Diagnose-Datenschutz sowie WLAN-Auswahl, leere Suchergebnisse und Fehlerbehandlung geprüft |
| Grundlegende Inbetriebnahme | **PASS** – Nutzerbestätigung am 09.10.2026 für WLAN-Suche, beide Lautsprecher, Bedienung und Autostart |
| Hardware-/Audio-Abnahme | **OFFEN** – siehe TESTPLAN.md |
| GitHub Actions | Workflow veröffentlicht; aktueller Workflow-Lauf nicht geprüft |
| PlatformIO-Telemetrie | Im lokalen Build und CI deaktiviert |

Die RAM-Zahl ist die statische Linkerbelegung. Dynamische Decoder-/Netzwerkpuffer und PSRAM-Belegung müssen auf dem Board beobachtet werden. `audioReady` und `streaming` allein belegen keinen hörbaren, getrennten Stereo-Ton.

Die Binärdatei übernimmt den vom Arduino-Framework eingebetteten ESP-IDF-App-Descriptor. Deshalb kann `esptool image_info` dessen Framework-Builddatum anzeigen; die CM-Radio-Version wird im seriellen Starttext und unter `/api/v1/status` als `0.1.2` ausgegeben. Die Paket-Manifestdatei ordnet den Build dem Projektcommit zu.

Build 0a02: Lokale Bibliotheksobjekte und Archiv nach Linkerfehler neu erstellt; finaler Build PASS. Visuelle Browserprüfung hier nicht verfügbar; Layout und Bedienung am Gerät prüfen. Dauertest Build 0a01 laut Nutzer bisher unauffällig, Dauer und Endstatus noch offen.

Build 0a03: Build PASS; Suchtests für lokale/nationale/internationale Filter, Mirror-Fallback, HTML als Text, Codec-/URL-Filter, doppelte Streams, leere Treffer, Zehn-Sender-Grenze, UTF-8-Namensgrenze, Offline-Übernahmesperre und Länderliste PASS. Direkte HTTPS-Abfrage an de1.api.radio-browser.info: HTTP 200, zwei Ergebnisse und Access-Control-Allow-Origin: *. Zweiter Bootstrap-Mirror antwortete beim lokalen Probeversuch mit HTTP 502; dessen Verfügbarkeit wird nicht behauptet. Vollständiger Browser-/Boardtest der Suche bleibt offen.

Build 0a02 wurde vom Nutzer am 09.10.2026 als PASS abgenommen.

Build 0a04: Build/Hosttests PASS. Neue C++-Steuerungstests: Timer-Ablauf, Ersetzen/Aufheben, Grenzen, Überlauf, Lautstärkegrenze, Rampe, manueller Eingriff und stumm/sofortiger Start. UI-Tests: Grenze/Restzeit, Erhalt von Formularentwürfen, Konfigurations- und Timerbefehle, ungültige Timerdauer und inaktiver Timer. Neue Funktionen und NVS-Felder müssen am Gerät geprüft werden. Nutzer bestätigt Build 0a03 als PASS.

Build 0a04: Nutzer meldet PASS. Build 0a05: PlatformIO PASS; Sicherungsschema und strikte Pflichtfeld-/Grenzprüfung, Ersatzsender-Schwelle/Offline/Einmalwechsel, 15-Sekunden-Stillstand mit Überlauf und Web-Sicherung/Entwurfsschutz/Dateiwechsel PASS. Ein leeres lokales Audio.cpp.o und dessen Bibliotheksarchiv wurden neu erstellt; finaler Link und Firmwarebuild erfolgreich. Dynamische Sicherungspuffer und die vergrößerte Audiowarteschlange sind am Board zu beobachten. Physischer 0a05-Test offen.
