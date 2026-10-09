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

## Build 0a05 – Sicherung und Ersatzsender

Build 0a04: Nutzer meldet PASS am 09.10.2026. Die vollständige Hardwareabnahme und die genaue Dauer des Dauertests bleiben offen.

1. Unter Gerät Sicherung herunterladen. Inhalt: Sender/Auswahl und Wiedergabeeinstellungen; keine SSID, kein WLAN-Passwort.
2. Einstellungen ändern und speichern. Sicherung auswählen, prüfen, Zusammenfassung kontrollieren, übernehmen. Radio stoppt, Timer endet; Heim-WLAN und Bedienbarkeit bleiben erhalten. Manuell starten und Neustart prüfen: wiederhergestellte Werte bleiben erhalten.
3. Fehlerhafte JSON-Datei, falsches Schema und Lautstärke oberhalb der Grenze prüfen: keine Übernahme, bestehende Einstellungen unverändert.
4. Einen funktionierenden Ersatzsender speichern. Einen separaten Testsendeplatz mit `http://127.0.0.1:9/unreachable` anlegen und starten. Nach drei gescheiterten Versuchen muss der Ersatz spielen und als Ersatzsender angezeigt werden. Verbindungs-Timeouts können die Wartezeit verlängern.
5. Ersatzsender ebenfalls unerreichbar: keine Wechselkette. Stop und Sleep-Timer beenden die Wiedergabe. Manuelles Play startet erneut mit dem ausgewählten Hauptsender.
6. WLAN-Unterbrechung allein löst keinen Ersatzwechsel aus. Nach WLAN-Rückkehr erfolgen reguläre Verbindungsversuche.

Hostprüfungen: strikte Sicherungstypen und Grenzen, unbekannte Zugangsdaten ohne Übernahme, Ersatzwechsel-Schwelle, identische URLs, einmaliger Wechsel, Offlinezustand, Timerüberlauf, Stillstand sowie Web-Dateiprüfung/Entwurfsschutz/Dateiwechsel geprüft. Nutzer bestätigt Build 0a05 am 09.10.2026 um 18:12 Uhr (Europe/Berlin) als PASS. Die Meldung gilt als Buildabnahme; gesonderte Messwerte und Einzelnachweise wurden nicht übermittelt. Vollständige Hardwareabnahme bleibt separat offen.

## Build 0a06 – Schnellwahl und Changelog

1. Radioansicht: alle gespeicherten Sender als große Kacheln sichtbar, ein Tipp startet den richtigen Sender. Markierung nur bei tatsächlich laufendem Stream, auch beim Ersatzsender. Stoppen entfernt die Markierung.
2. Unter Sender Reihenfolge ändern: erste/letzte Position dürfen nicht über Grenzen verschoben werden. Vor Speichern bleibt die Schnellwahl unverändert; nach Speichern und Stromneustart bleibt die neue Reihenfolge erhalten. Auswahl und Ersatzsender bleiben dem ursprünglichen Stream zugeordnet.
3. Ungespeicherte Wiedergabeeinstellungen zuerst speichern, bevor Sender umgeordnet werden. Fehlgeschlagene Speicherung darf keine neue Schnellwahl anzeigen.
4. Bei nicht erreichbarem Gerät oder nicht bereitem Audio sind Kacheln gesperrt; nach Wiederverbindung bedienbar. Mit einem zweiten Browser die gespeicherte Sammlung ändern: für neue Kacheln Seite neu laden.
5. Unter Gerät Changelog aufklappen: Build 0a06 und die bisherigen Einträge müssen auch ohne Internet am Handy/PC lesbar sein.

Hosttests: direkte Senderwahl, Offline-Sperre, sichere Textdarstellung, Entwurfstrennung, gespeicherte Reihenfolge, Grenzbuttons, Schutz offener Wiedergabeeinstellungen und tatsächliche Ersatzsender-Markierung PASS. Changelog-Synchronität und eingebettete UI geprüft. Gerätetest 0a06 OFFEN.

## Build 0a07 – CMR-004

Denselben betroffenen Sender mindestens zehn Minuten hören: kein periodischer Abbruch oder Neuladen. Danach Stop/Play, Sleep-Timer, Ersatzsender und WLAN-Wiederverbindung prüfen. Gerätetest offen.

## Build 0a08 – Lokales OTA-Update

Nutzerabnahme 0a07: PASS am 09.10.2026 um 18:26 Uhr; keine gesonderte Laufzeit übermittelt. CMR-004 im erneuten Gerätetest behoben.

1. 0a08 einmalig per USB installieren. Mit Strg+F5 laden, laufenden Sender und Timer starten, Lautstärke verändern. Paket 0a08 in der Oberfläche auswählen, prüfen und bestätigen. Audio/Timer stoppen vor Upload; Fortschritt sichtbar; Neustart; WLAN, Sender, Lautstärke und Wiedergabeeinstellungen bleiben erhalten. Installierten Build prüfen.
2. Datei mit verändertem Byte, gleicher Größe und unverändertem Manifest über Browser installieren: Hashfehler, kein neuer Slot aktiv, Radio weiter erreichbar, manuelles Play möglich.
3. Falscher Dateiname/Größe/Manifest/ESP32-Header: abgelehnt. Ohne Installationscheckbox kein Upload. Ungespeicherte Formularentwürfe blockieren Installation.
4. Transfer abbrechen (Browser schließen/Verbindung trennen): kein erfolgreiches Aktivieren einer Teilfirmware, später wieder erreichbar. Stromunterbrechung als separaten, kontrollierten Recoverytest prüfen; hier keine physische Garantie behauptet.
5. Neustart nach erfolgreichem Upload, Autostart an/aus und Senderdauerbetrieb prüfen. Zweiten Upload durchführen, um beide OTA-Slots nacheinander zu verwenden.

Hosttests PASS: Hashmetadaten, in Teilen eintreffender Header, ESP32-Chip-ID, falsche Magicbytes, Übergröße/Teilimage; UI-Paketprüfung, ausdrückliche Zustimmung, Entwurfsschutz, Uploadpfad/Token/Progress, Fehleranzeige und Bedienungssperre. Echte SHA-Prüfung/Flashaktivierung/Neustart am Board OFFEN. Kein direkter USB-Zugriff hier.

Nutzerabnahme Build 0a08 am 09.10.2026 um 18:39 Uhr (Europe/Berlin): PASS nach angefragtem Browserupdate-/Neustarttest mit erhaltenem WLAN, Sendern und Einstellungen. Gezielte Negativtests und Stromausfall-/Recoverytests wurden nicht gesondert bestätigt und bleiben offen.

## Build 0a09 – Klang

1. Browserupdate aus 0a08 durchführen, Strg+F5; vorhandenes WLAN/Sender erhalten und Klang zunächst neutral.
2. Bei moderater Lautstärke Bässe/Höhen getrennt verändern und speichern; hörbare Wirkung, kein Verbindungsabbruch/Stream-Neustart. Während eines sanften Starts Klang speichern: Lautstärkerampe läuft weiter.
3. Balance −16 speichern: nur linker Kanal; +16: nur rechter Kanal. Mitte speichern: beide. Stereoquelle und Verkabelung berücksichtigen. Dadurch wird kein Mono-Stream in Stereo umgewandelt.
4. Werte speichern, Stromneustart: erhalten. Sicherung exportieren, ändern, wiederherstellen: ursprüngliche Klangwerte erhalten, Radio gestoppt; manuell starten. Alte Sicherung ohne Klangwerte: alle drei 0.
5. Neutral einstellen und speichern. Vor Speichern bleibt Entwurf über Statusabfragen erhalten; Restore/Update mit ungespeicherten Klangentwürfen blockiert.

Hosttests: strikte Typen/Grenzen, positive/negative Endwerte, neutrale Migration alter Sicherungen, Erhalt nicht angegebener Teilfelder, Reglerbeschriftung, Entwurferhalt, Neutralaktion, POST-Klangpayload und ungültige Eingaben PASS. Hörprobe/Neustart/Sicherung am Board OFFEN.

## Build 0a0a – Direkte Klangvorschau

Build 0a09 vom Nutzer am 09.10.2026 um 18:51 Uhr als PASS bestätigt.

1. Bässe/Höhen/Balance bewegen: hörbare Änderung ohne Speichern und ohne Stream-Neustart. Schnell hin- und herbewegen: letzter Reglerwert gewinnt.
2. Gespeicherte Werte wiederherstellen: vorheriger Klang und Reglerwerte wieder da. Neutral hören: neutraler Klang als Vorschau. Neustart ohne Speichern: vorher gespeicherte Werte geladen.
3. Während Vorschau Klang dauerhaft speichern, auch identische zuvor gespeicherte Zahlen: Vorschau beendet, Werte bleiben nach Neustart erhalten.
4. Vorschau aktiv und Sicherung herunterladen: nur gespeicherte Werte enthalten. Seite neu laden: Vorschau erkennbar; mit Restore/Update erst nach Speichern oder Zurücksetzen fortfahren.
5. Stop/Play und Senderwechsel: Vorschau bleibt. Netzunterbrechung beim Verstellen: Fehler angezeigt; erneut einstellen oder gespeicherte Werte wiederherstellen.

Hosttests: Bündelung aktueller Reglerwerte, serialisierte Vorschau, Speichern während laufender Anfrage, Rücksetzen, Fehlerrückgabe ohne hängenden Zustand PASS. Reale Hörprobe und Vorschau-/Persistenzabgrenzung OFFEN.

Nutzerabnahme Build 0a0a am 09.10.2026 um 18:59 Uhr (Europe/Berlin): PASS nach angefragtem Test von direkter Klangvorschau, Zurücksetzen und Neustart ohne Speichern. Keine gesonderten Messwerte übermittelt; vollständige Hardwareabnahme bleibt separat.

## v0.1.3 · Build 01

1. Browserupdate installieren; Version 0.1.3 und Build 01 prüfen. WLAN/Sender/Klangwerte bleiben, Loudness alter Daten aus.
2. Bei Lautstärke 3–5 Loudness ein-/ausschalten: Bass-/Höhenwirkung hören, kein Stream-Neustart. Bei Stufe 15 soll keine zusätzliche Anhebung mehr wirken. Lautstärkegrenze beachten.
3. Sanften Start und Lautstärkeänderung: effektive EQ-Anzeige folgt der tatsächlichen Lautstärke. Bass/Höhen an oberer Grenze: angewendete Werte maximal +6 dB. Balance weiterhin korrekt.
4. Ohne Speichern vorhören, gespeicherte Werte wiederherstellen; mit Speichern Neustart und Sicherung/Wiederherstellung prüfen. Neutral hören setzt Loudness vorübergehend aus.
5. ZIP enthält ausführliche USB_ERSTINSTALLATION.txt mit Version 0.1.3, Build 01 und CM-Radio-V0.1.3-full.bin; keine Platzhalter. Erstinstallation an bereits belegtem Gerät nur als bewusst separater Resettest.

Hosttests: Loudness aus/bei 0/bei 1/bei 15, maximale EQ-Grenzen über alle Lautstärkestufen, strikte boolesche Sicherungswerte und UI-Vorschau/Speichern geprüft. Hörprobe, Update und vollständige USB-Erstinstallation dieses Pakets OFFEN.

Nutzerabnahme v0.1.3 Build 01 am 09.10.2026 um 19:10 Uhr (Europe/Berlin): PASS nach angefragtem Loudness-Hörtest und Prüfung gespeicherter Werte nach Neustart. Keine gesonderten Messwerte übermittelt. USB-Erstinstallation dieses Pakets und vollständige Hardwareabnahme nicht gesondert bestätigt.

## v0.1.3 · Build 02

1. Browserupdate und Strg+F5. Bestehende Sender bleiben ohne Logo erhalten. Radiosender mit gültiger HTTPS-Logoquelle suchen, hinzufügen und speichern; Hauptansicht/Schnellwahl zeigen Bild.
2. Unter Sender eigene HTTPS-Logo-Adresse speichern; Neustart und Sicherung/Wiederherstellung erhalten sie. Altes Backup ohne Logo lädt leer.
3. Logoquelle defekt oder Browser ohne Internet: Platzhalter, Audio läuft weiter. Senderwechsel während Bild lädt: altes Bild/Fehler überschreibt neue Anzeige nicht. Beim Ersatzsender muss dessen Logo erscheinen.
4. Sender mit Interpret - Titel: getrennte Zeilen, Sonderzeichen als Text; ohne Format kompletter Titel, ohne Metadaten klare Ersatzanzeige. Streammeldungen getrennt. Manuelles Stop/Play und Dauertest prüfen.

Hosttests: HTTPS-Logo-/Typprüfung, Migration alter Sicherungen, Metadatentrennung/Textdarstellung, Fehlerplatzhalter, alte Ladeereignisse und Wiederholungsunterdrückung PASS. Physische Logo-/Metadatenabnahme offen. Wecker/Zeitpläne werden nicht mehr als Abnahmekriterien geführt.

Nutzerabnahme v0.1.3 Build 02 am 09.10.2026 um 19:38 Uhr (Europe/Berlin): PASS nach angefragtem Test von Logos, Titelanzeige und Senderwechsel. Keine gesonderten Einzelnachweise übermittelt; vollständige Hardwareabnahme bleibt separat.

## v0.1.3 Build 03 – Infobereich

- Browserupdate aus demselben Paket durchführen; nach Neustart Strg+F5 und Build 03 prüfen.
- Unter Gerät Ersteller C. Mihalik sowie GitHub- und PayPal-Link prüfen; beide Ziele öffnen in einem neuen Tab. Keine Spende für den Test erforderlich.
- Wiedergabe bleibt beim Aufrufen des Infobereichs und Öffnen der Links aktiv.
- Ohne Internet bleibt der Infotext verfügbar; externe Seiten benötigen Internet.

Gerätetest: offen.

## v0.1.3 Build 04 – Geräteoberfläche

- Build 03: Nutzer meldet PASS am 09.10.2026 um 19:49 Uhr (Europe/Berlin).
- Nach Browserupdate Strg+F5: Version/Build, WLAN und Speicherzustand oben prüfen.
- Desktop: zwei Spalten; Smartphone: eine Spalte ohne horizontales Scrollen. Alle sieben Bereiche per Maus, Touch und Tastatur öffnen/schließen.
- Klangvorschau, Speichern, Neutral und Zurücksetzen prüfen. Ungespeicherte Werte bleiben beim Schließen/Öffnen erhalten.
- Wiedergabeeinstellungen, Sicherungsdownload, Wiederherstellungsvorschau, Projektlinks, Changelog und Diagnose erreichbar; Audio läuft beim Aufklappen weiter.

Gerätetest Build 04: offen.

## v0.1.3 Build 05 – Lautstärke und Netzwerk

- Vor Update Sicherung herunterladen. Nach Browserupdate Strg+F5: Build 05 prüfen.
- Alte Lautstärke/Grenze werden abgerundet umgerechnet (5 → 11, 21 → 50); Lautstärke steigt durch Migration nicht. Alte Sicherung importieren und prüfen. Neue Sicherung nutzt Schema 2, erneuter Import ändert Werte nicht.
- Regler 0 stumm, 1–50 feinere Abstufung; Obergrenze, sanfter Start, Loudness, Speichern und Neustart prüfen. Hohe Lautstärke nur bei Bedarf wählen.
- Hauptnavigation Radio/Sender/Gerät; Netzwerk dort öffnen. WLAN-Knopf springt direkt zum Bereich, WLAN-Suche und Speichern funktionieren.
- Smartphone/Desktop: acht Bereiche, ein bzw. zwei Spalten; Klangentwürfe bleiben beim Schließen erhalten.

Gerätetest: offen.

Nutzerabnahme v0.1.3 Build 05 am 09.10.2026 um 20:04 Uhr (Europe/Berlin): PASS nach angefragter Prüfung von Lautstärke, Obergrenze, Neustart und WLAN-Suche. Keine gesonderten Messwerte oder Bestätigung eines Sicherungsimports übermittelt; vollständige Hardwareabnahme bleibt separat.

## v0.1.3 Build 06 – Setup/Fallback-Passwort

- Nach Browserupdate Strg+F5: Build 06; erstmalig eigenes Setup-Passwort zweimal festlegen. passwort, weniger als acht Zeichen und unterschiedliche Bestätigungen abweisen.
- Erstinstallation: CM-Radio-WLAN mit passwort erreichbar; Änderung verpflichtend vor WLAN-Konfiguration. AP-Neustart und Wiederverbinden mit neuem Passwort prüfen.
- Heim-WLAN ausschalten: nach etwa 30 Sekunden Fallback mit eigenem Passwort, 192.168.4.1 erreichbar. Passwort bleibt nach Stromneustart gleich. Heim-WLAN wiederherstellen: automatischer Rückwechsel.
- Unter Gerät → Netzwerk → Fallback-Zugang mit falschem altem Passwort Änderung abweisen; korrektes altes Passwort und bestätigtes neues Passwort speichern. Bei aktivem AP erneut verbinden.
- Backup/Diagnose enthalten kein Setup-Passwort. Sicherungsimport und reset-wifi verändern es nicht.
- USB reset-ap-password setzt nur Setup-Passwort zurück und verlangt erneut Wechsel; Sender, Klang und Heim-WLAN erhalten.

Gerätetest: offen.

Passwortreset per Taste ab Build 06: Bei laufendem Radio BOOT/IO0 10–59 Sekunden halten und loslassen. Nur Setup-/Fallback-Passwort wird auf passwort zurückgesetzt; verpflichtender Wechsel beim nächsten Browseraufruf. Nicht mit BOOT beim Einschalten verwechseln (Flashmodus). Während eines Firmwareupdates wird der Reset ignoriert; anschließend neu halten. Prüfen: kurzer Druck bewirkt nichts, ein langer Druck löst einmal aus, Heimnetz/Sender/Klang bleiben erhalten.

Werkseinstellungen über dieselbe BOOT/IO0-Taste: Bei laufendem Radio mindestens 60 Sekunden halten und loslassen. Erst das Loslassen löst den vollständigen Reset aus. Heim-WLAN, Sender, Klang, Lautstärke und Setup-Passwort werden gelöscht; Firmware bleibt installiert, Radio startet neu. Danach Erstzugang mit passwort und verpflichtender Änderung. Während Firmwareupdates werden Tastenresets ignoriert; Taste neu betätigen. Gerätetest: kurzer Druck ohne Wirkung, 10–59 s nur Passwort, ab 60 s vollständiger Reset. Vor dem Test Einstellungen sichern; Sicherung enthält keine Zugangspasswörter.

## v0.1.3 Build 07

Nach Browserupdate und Strg+F5 Radio als Startseite prüfen, auch im Fallback. Eigenes Setup-Passwort nach Seitenneuladen und Stromneustart unverändert, keine erneute Wechselaufforderung. Nach explizitem Passwortreset Wechsel erforderlich; danach Radio, Netzwerk geschlossen. WLAN-Knopf öffnet weiterhin Gerät → Netzwerk. Mindestlänge 8 bleibt technisch erforderlich. Gerätetest offen.

Nutzer bestätigt v0.1.3 Build 07 am 09.10.2026 um 20:32 Uhr (Europe/Berlin) als PASS nach angefragter Prüfung von Radio-Startseite und Passworterhalt nach Seitenneuladen und Neustart. Kein gesonderter Nachweis für Tasten-/Werksreset oder vollständige Hardwareabnahme.

## Build 08 – Abnahme am Board

1. Gerätenamen auf Radio Wohnzimmer ändern, neue Adresse radio-wohnzimmer.local öffnen; Neustart und Sicherungsimport prüfen. Bei Fallback neue SSID prüfen; bisheriges Setup-Passwort muss gelten.
2. Stereo-Teststream bei neutraler Balance hören; Mono einschalten: beide Lautsprecher müssen den gemischten Inhalt wiedergeben. Balance links/rechts und Rückkehr zu Stereo prüfen; Neustart erhält Einstellung.
3. Heim-WLAN unterbrechen und wiederherstellen: Ausfallzähler erhöht sich einmal pro Ausfall, Offlinezeit läuft; Stream-Ausfall getrennt von WLAN anzeigen. Zähler nach Neustart null.
4. Sender aus Suche speichern (UUID), nur seine URL absichtlich ungültig ändern, Namen beibehalten. Manuelle Wiederfindung muss korrekte Adresse speichern; danach Autoreparatur nach drei Versuchen bei geschlossenem Browser prüfen. Mehrdeutiger/fehlender Treffer darf nichts überschreiben. Während Suche Stop/Senderwechsel auslösen: verspätetes Ergebnis darf nicht starten oder überschreiben. Ersatzsender bleibt aktiv bis manuellem Start.
5. Verzeichnis nicht erreichbar: Audio/UI weiter bedienbar, Fehlermeldung; keine Dauerschleife und keine URL-Änderung.

Diese Hardwaretests sind noch nicht durchgeführt.
