# CM-Radio V0.1 – Abnahme auf dem bestellten Board

Status vor Eintreffen: **alle physischen Tests offen**. Ergebnisse mit Datum, Modulaufdruck, PCB-Revision, Commit/Version und Netzteil dokumentieren. WLAN-Passwörter und andere Zugangsdaten nicht in Protokolle übernehmen.

| ID | Test | Erfolgskriterium | Status |
| --- | --- | --- | --- |
| HW-01 | Modul/PCB prüfen | WROVER-N8R8, richtige Revision und GPIOs | offen |
| HW-02 | Erstinstallation | Chip ESP32, 8 MB Flash erkannt; Flash ohne Fehler | offen |
| HW-03 | Boot/PSRAM | Keine Reset-Schleife, PSRAM verfügbar, Audio bereit | offen |
| NET-01 | Erstes Setup | WPA-Setup-AP, zufälliges Passwort, 192.168.4.1 erreichbar | offen |
| NET-02 | Heim-WLAN | SSID/Passwort gespeichert, AP beendet, IP/mDNS erreichbar | offen |
| NET-03 | Falsches Passwort | Nach 30 s Setup erreichbar, keine Neustart-Schleife | offen |
| AUDIO-01 | MP3-Teststream | Beide Lautsprecher geben stabil Ton aus | offen |
| AUDIO-02 | Stereo-Testdatei | Links/Rechts einzeln hörbar, keine ungewollte Monosumme | offen |
| AUDIO-03 | Lautstärke/Stop | 0 stumm, 5 leise testen, Stop beendet Ton, Play startet wieder | offen |
| AUDIO-04 | AAC-Sender | Gültiger AAC-Stream ohne Aussetzer; URL/Bitrate dokumentieren | offen |
| CFG-01 | Eigene Sender | Hinzufügen, Entfernen, Auswahl und Grenzen 1–10 funktionieren | offen |
| CFG-02 | Stromneustart | Letzter Sender/Lautstärke erhalten, Autostart erfolgt | offen |
| CFG-03 | Autostart aus | Neustart bleibt stumm, manueller Play funktioniert | offen |
| REC-01 | WLAN 60 s aus | Gerät bleibt erreichbar über Setup, nach Netzrückkehr Stream wieder aktiv | offen |
| REC-02 | Ungültiger Stream | API bleibt bedienbar, Wiederholungen, Stop/anderer Sender möglich | offen |
| API-01 | Grundtest | smoke_test.py erfolgreich, Passwort wird nicht geliefert | offen |
| API-02 | Fehlerfälle | -1/22 Lautstärke, ungültiger Index, falscher Datentyp: 400 | offen |
| UI-01 | Android | Play/Stop, Sender, WLAN und Lautstärke bedienbar | offen |
| RUN-01 | 60 Minuten | Keine Resets, keine anhaltenden Aussetzer, Heap nicht stetig sinkend | offen |
| CASE-01 | Wandgehäuse | USB/Kabel zugänglich, Temperatur und WLAN nach Einbau brauchbar | offen |

Für AUDIO-02 eine bekannte Stereo-Testdatei mit separaten Links-/Rechts-Ansagen per direkter HTTP-URL als Sender eintragen. Ein Radiosender alleine beweist keine Kanaltrennung. Zu Beginn nur niedrige Lautstärke verwenden; die elektrische Leistung lässt sich nicht aus dem Softwarewert 0–21 ableiten.

Der Ersttest muss auch die Freigabepolarität von GPIO 13 bestätigen. Wenn trotz initialisierter I²S-Schnittstelle kein Ton entsteht, Schaltplan der tatsächlich gelieferten Revision prüfen und `BoardConfig.h`/Player gezielt anpassen.
