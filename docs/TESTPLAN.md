# CM-Radio V0.1 – Abnahme auf dem bestellten Board

Stand 09.10.2026: **Grundlegende Inbetriebnahme von v0.1.2 · Build 0a01 bestanden; vollständige Hardwareabnahme offen**. PASS beruht auf Nutzerbestätigung, TEILWEISE auf eingeschränktem Nachweis. Ergebnisse mit Datum, Modulaufdruck, PCB-Revision, Commit/Version und Netzteil dokumentieren. WLAN-Passwörter und andere Zugangsdaten nicht in Protokolle übernehmen.

| ID | Test | Erfolgskriterium | Status |
| --- | --- | --- | --- |
| HW-01 | Modul/PCB prüfen | WROVER-N8R8, richtige Revision und GPIOs | TEILWEISE – E3/Modul anhand Boardfotos zugeordnet; GPIOs durch Grundbetrieb gestützt |
| HW-02 | Erstinstallation | Chip ESP32, 8 MB Flash erkannt; Flash ohne Fehler | PASS – Nutzer-Screenshots von Flash und Hashprüfung, 09.10.2026 |
| HW-03 | Boot/PSRAM | Keine Reset-Schleife, PSRAM verfügbar, Audio bereit | TEILWEISE – Boot/PSRAM-Ausgabe und hörbarer Ton bestätigt; Dauerbeobachtung offen |
| NET-01 | Erstes Setup | WPA-Setup-AP, zufälliges Passwort, 192.168.4.1 erreichbar | PASS – Bootausgabe und Nutzung der Einrichtung bestätigt, 09.10.2026 |
| NET-02 | Heim-WLAN | SSID/Passwort gespeichert, AP beendet, IP/mDNS erreichbar | TEILWEISE – Radiowiedergabe bestätigt; AP-Ende und mDNS separat offen |
| NET-04 | WLAN-Suche | Sichtbare 2,4-GHz-Netzwerke finden und auswählen | PASS – Nutzerbestätigung für Build 0a01, 09.10.2026 |
| NET-03 | Falsches Passwort | Nach 30 s Setup erreichbar, keine Neustart-Schleife | offen |
| AUDIO-01 | MP3-Teststream | Beide Lautsprecher geben stabil Ton aus | TEILWEISE – beide Lautsprecher bestätigt; Codec und Dauerstabilität nicht separat protokolliert |
| AUDIO-02 | Stereo-Testdatei | Links/Rechts einzeln hörbar, keine ungewollte Monosumme | offen |
| AUDIO-03 | Lautstärke/Stop | 0 stumm, 5 leise testen, Stop beendet Ton, Play startet wieder | TEILWEISE – Lautstärke/Stop/Play PASS laut Nutzer; exakte Werte 0/5 offen |
| AUDIO-04 | AAC-Sender | Gültiger AAC-Stream ohne Aussetzer; URL/Bitrate dokumentieren | offen |
| CFG-01 | Eigene Sender | Hinzufügen, Entfernen, Auswahl und Grenzen 1–10 funktionieren | offen |
| CFG-02 | Stromneustart | Letzter Sender/Lautstärke erhalten, Autostart erfolgt | TEILWEISE – Autostart nach USB-Trennung PASS; individuelle gespeicherte Werte offen |
| CFG-03 | Autostart aus | Neustart bleibt stumm, manueller Play funktioniert | offen |
| REC-01 | WLAN 60 s aus | Gerät bleibt erreichbar über Setup, nach Netzrückkehr Stream wieder aktiv | offen |
| REC-02 | Ungültiger Stream | API bleibt bedienbar, Wiederholungen, Stop/anderer Sender möglich | offen |
| API-01 | Grundtest | 19 Erststart-Kriterien PASS, JSON-Bericht erstellt; keine Zugangsdaten im Bericht | offen |
| API-02 | Fehlerfälle | -1/22 Lautstärke, ungültiger Index, falscher Datentyp: 400 | offen |
| UI-01 | Android | Play/Stop, Sender, WLAN und Lautstärke bedienbar | offen |
| RUN-01 | 60 Minuten | Keine Resets, keine anhaltenden Aussetzer, Heap nicht stetig sinkend | offen |
| CASE-01 | Wandgehäuse | USB/Kabel zugänglich, Temperatur und WLAN nach Einbau brauchbar | offen |

Für AUDIO-02 eine bekannte Stereo-Testdatei mit separaten Links-/Rechts-Ansagen per direkter HTTP-URL als Sender eintragen. Ein Radiosender alleine beweist keine Kanaltrennung. Zu Beginn nur niedrige Lautstärke verwenden; die elektrische Leistung lässt sich nicht aus dem Softwarewert 0–21 ableiten.

Der Ersttest muss auch die Freigabepolarität von GPIO 13 bestätigen. Wenn trotz initialisierter I²S-Schnittstelle kein Ton entsteht, Schaltplan der tatsächlich gelieferten Revision prüfen und `BoardConfig.h`/Player gezielt anpassen.

## Bestätigte Grundtests – 09.10.2026

Nutzerbestätigungen für v0.1.2 · Build 0a01: WLAN-Suche funktioniert; Ton aus beiden Lautsprechern; Lautstärke, Stoppen und Abspielen funktionieren; Autostart nach USB abziehen und wieder einstecken funktioniert. Eine separate Links-/Rechts-Testdatei und ein Dauerbetrieb sind damit nicht nachgewiesen. Der vorgeschlagene 30-Minuten-Test ist eine Zwischenprüfung; RUN-01 verlangt weiterhin 60 Minuten. Netzteil im Test noch nicht dokumentiert.

## Neuer Stand Build 0a02

Navigation Radio/Sender/Netzwerk/Gerät auf Handy und Desktop prüfen; WLAN-Balken mit dBm und Setup-/Offlinezustand vergleichen; Play/Stop, Lautstärke, Senderverwaltung und WLAN-Suche erneut prüfen. Status: OFFEN.

Dauertest Build 0a01: Nutzer am 09.10.2026 um 17:05 Uhr (Europe/Berlin) meldet „scheint erfolgreich“. Bislang unauffällig; RUN-01 bleibt bis Bestätigung von mindestens 60 Minuten und Endstatus offen.

## Build 0a02 – Nutzerabnahme

09.10.2026: Nutzer bestätigt „Build 0a02 pass“. Grundabnahme der neuen Oberfläche dokumentiert; Langzeit-/Stereo-Spezialtests bleiben separat offen.

## Build 0a03 – Sendersuche (offen)

1. National / Deutschland: „Deutschlandfunk“ suchen, Treffer übernehmen, speichern, unter Radio auswählen und hören.
2. International: Sendername suchen; Landfilter darf nicht wirken.
3. Lokal / regional: z. B. „Berlin“ suchen; Ergebnisse anhand der Namen/Regionsdaten beurteilen, keine Umkreisgarantie.
4. Weitere Länder laden und Auswahl prüfen.
5. Mehrere Treffer hinzufügen, doppelte Adresse nicht mehrfach übernehmen, maximal zehn Sender.
6. Suche bei ausgefallenem Verzeichnis/fehlendem Browserinternet prüfen; bestehende Sammlung und Wiedergabe bleiben nutzbar.
7. Stromneustart: neu gespeicherter Sender bleibt vorhanden.

## Build 0a03 – Nutzerabnahme

09.10.2026: Nutzer bestätigt „0a03 pass“. Grundabnahme der Sendersuche dokumentiert.

## Build 0a04 – Gerätetest (offen)

1. Nach Update WLAN, vorhandene Sender und Lautstärke prüfen. Neue Standardwerte: Grenze 21, sanfter Start 5 Sekunden.
2. Grenze z. B. auf 8 speichern; Regler bleibt ≤8. `POST /volume` mit 9 muss 400 liefern. Grenze reduzieren, auch während einer Rampe, und keine Ausgabe über der Grenze beobachten.
3. Sanften Start auf 5 Sekunden setzen, Zielwert bei niedriger Lautstärke wählen, Stop/Play und Autostart prüfen. Manuelle Regleränderung beendet die Rampe. 0 Sekunden deaktiviert sie.
4. Eigenen Sleep-Timer 1 Minute setzen; Restzeit prüfen; Ablauf stoppt den Stream ohne automatischen Wiederanlauf. Timer während laufender Wiedergabe ändern und aufheben; Stop hebt ihn ebenfalls auf.
5. Timer bleibt bei Senderwechsel aktiv. Neustart startet ohne Timer; Autostart gilt weiterhin nach gespeicherter Einstellung.
6. Grenze und Rampendauer nach Stromneustart erhalten.
