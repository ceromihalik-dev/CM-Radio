# Buildstatus – CM-Radio V0.1.1

Datum: **9. Oktober 2026**. Lokal geprüft auf Linux x86_64 / Python 3.12. Das E3-Board ist beim Nutzer angekommen; hier kein direkter USB-Zugriff. Flashen und akustische Tests stehen aus.

| Prüfung | Ergebnis |
| --- | --- |
| PlatformIO `loud_wrover` | **PASS** |
| Arduino-ESP32 / Framework | 2.0.17 / 3.20017.241212+sha.dcc1105b |
| ESP32-audioI2S | Tag 3.0.12, Commit `928c420d49fce2a09fa91f490b9fcabed6447c67` |
| ArduinoJson | 6.21.5 |
| Programmcode | 1.269.645 Bytes / 3.145.728 Bytes (40,4 %) |
| Statische RAM-Belegung | 51.508 Bytes / 327.680 Bytes (15,7 %) |
| Anwendung / Bootloader | Chip ESP32, 8 MB, 40 MHz, DIO; Checksum/Validierungshash gültig |
| Flashlayout | Keine Überlappung; zwei 3-MiB-Slots, Gesamtgröße 8 MB |
| URL-/WLAN-Eingaben | Positivfälle, ungültige Protokolle, Header-Steuerzeichen, Grenzen geprüft |
| Wiederverbindung | Backoff-Grenze und millis-Überlauf geprüft |
| Flashskript | Fünf Tests: passende Paketdatei, explizites Löschen, korrupte Datei, falsche Kapazität, korrekte Reihenfolge |
| Automatischer Erststarttest | Sechs Hosttests: gültiges Board, Fehlerzustände, ungültige Antworten, Offline-Gerät, reine GET-Abfragen, Bericht ohne private Daten; echte Boardausführung offen |
| Weboberfläche | JavaScript-Syntax, eingebettete Kopie, Wiederverbindung nach Ladefehler, keine parallelen Hintergrundabfragen, Erhalt von Senderentwürfen und Diagnose-Datenschutz geprüft |
| Hardware-/Audio-Abnahme | **OFFEN** – siehe TESTPLAN.md |
| GitHub Actions | Workflow veröffentlicht; bisher kein Workflow-Lauf vorhanden |
| PlatformIO-Telemetrie | Im lokalen Build und CI deaktiviert |

Die RAM-Zahl ist die statische Linkerbelegung. Dynamische Decoder-/Netzwerkpuffer und PSRAM-Belegung müssen auf dem Board beobachtet werden. `audioReady` und `streaming` allein belegen keinen hörbaren, getrennten Stereo-Ton.

Die Binärdatei übernimmt den vom Arduino-Framework eingebetteten ESP-IDF-App-Descriptor. Deshalb kann `esptool image_info` dessen Framework-Builddatum anzeigen; die CM-Radio-Version wird im seriellen Starttext und unter `/api/v1/status` als `0.1.1` ausgegeben. Die Paket-Manifestdatei ordnet den Build dem Projektcommit zu.
