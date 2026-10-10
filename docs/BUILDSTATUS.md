# Buildstatus – CM-Radio v0.1.3 · Build 09

Datum: **10. Oktober 2026**. Lokal geprüft auf Linux x86_64 / Python 3.12. Das E3-Board ist beim Nutzer angekommen; hier kein direkter USB-Zugriff. USB-Flash und Boot von V0.1.1 sowie das Schreiben von V0.1.2 sind durch Nutzer-Screenshots bestätigt. Nutzer meldet abgelehnten WLAN-Suchstart in V0.1.2 ohne Buildkennung. Die Korrektur in Build 0a01 wurde vom Nutzer bestätigt. Ton aus beiden Lautsprechern, Lautstärke/Stop/Play und Autostart nach Stromunterbrechung sind ebenfalls bestätigt; Build 08 hat laut Nutzer am 10.10.2026 alle Prüfungen bestanden; für Build 09 steht die Favicon-Anzeige im Browser noch aus.

| Prüfung | Ergebnis |
| --- | --- |
| PlatformIO `loud_wrover` | **PASS** |
| Arduino-ESP32 / Framework | 2.0.17 / 3.20017.241212+sha.dcc1105b |
| ESP32-audioI2S | Tag 3.0.12, Commit `928c420d49fce2a09fa91f490b9fcabed6447c67` |
| ArduinoJson | 6.21.5 |
| Programmcode | 1.426.385 Bytes / 3.145.728 Bytes (45,3 %) |
| Statische RAM-Belegung | 54.136 Bytes / 327.680 Bytes (16,5 %) |
| Anwendung / Bootloader | Chip ESP32, 8 MB, 40 MHz, DIO; Checksum/Validierungshash gültig |
| Flashlayout | Keine Überlappung; zwei 3-MiB-Slots, Gesamtgröße 8 MB |
| URL-/WLAN-Eingaben | Positivfälle, ungültige Protokolle, Header-Steuerzeichen, Grenzen geprüft |
| WLAN-Suchkoordination | Vorbereitung, doppelte Anfragen, begrenzte Wiederholungen, Timeout, Wiederherstellung und millis-Überlauf: PASS (Hosttest) |
| Wiederverbindung | Backoff-Grenze und millis-Überlauf geprüft |
| Flashskript | Fünf Tests: passende Paketdatei, explizites Löschen, korrupte Datei, falsche Kapazität, korrekte Reihenfolge |
| Automatischer Erststarttest | Sechs Hosttests: gültiges Board, Fehlerzustände, ungültige Antworten, Offline-Gerät, reine GET-Abfragen, Bericht ohne private Daten; echte Boardausführung offen |
| Weboberfläche | JavaScript-Syntax, eingebettete Kopie, Bereichsnavigation, WLAN-Balken/Farben/Offlinezustände, Wiederverbindung nach Ladefehler, keine parallelen Hintergrundabfragen, Erhalt von Senderentwürfen Diagnose-Datenschutz sowie WLAN-Auswahl, leere Suchergebnisse und Fehlerbehandlung geprüft |
| Grundlegende Inbetriebnahme | **PASS** – Nutzerbestätigung am 09.10.2026 für WLAN-Suche, beide Lautsprecher, Bedienung und Autostart |
| Hardware-/Audio-Abnahme | Build 08: **PASS** laut Nutzer am 10.10.2026; Build 09: Favicon-Anzeige im Browser offen |
| GitHub Actions | Workflow veröffentlicht; aktueller Workflow-Lauf nicht geprüft |
| PlatformIO-Telemetrie | Im lokalen Build und CI deaktiviert |

Die RAM-Zahl ist die statische Linkerbelegung. Dynamische Decoder-/Netzwerkpuffer und PSRAM-Belegung müssen auf dem Board beobachtet werden. `audioReady` und `streaming` allein belegen keinen hörbaren, getrennten Stereo-Ton.

Die Binärdatei übernimmt den vom Arduino-Framework eingebetteten ESP-IDF-App-Descriptor. Deshalb kann `esptool image_info` dessen Framework-Builddatum anzeigen; die CM-Radio-Version wird im seriellen Starttext und unter `/api/v1/status` als `0.1.3`, Build `09` ausgegeben. Die Paket-Manifestdatei ordnet den Build dem Projektcommit zu.

Build 0a02: Lokale Bibliotheksobjekte und Archiv nach Linkerfehler neu erstellt; finaler Build PASS. Visuelle Browserprüfung hier nicht verfügbar; Layout und Bedienung am Gerät prüfen. Dauertest Build 0a01 laut Nutzer bisher unauffällig, Dauer und Endstatus noch offen.

Build 0a03: Build PASS; Suchtests für lokale/nationale/internationale Filter, Mirror-Fallback, HTML als Text, Codec-/URL-Filter, doppelte Streams, leere Treffer, Zehn-Sender-Grenze, UTF-8-Namensgrenze, Offline-Übernahmesperre und Länderliste PASS. Direkte HTTPS-Abfrage an de1.api.radio-browser.info: HTTP 200, zwei Ergebnisse und Access-Control-Allow-Origin: *. Zweiter Bootstrap-Mirror antwortete beim lokalen Probeversuch mit HTTP 502; dessen Verfügbarkeit wird nicht behauptet. Vollständiger Browser-/Boardtest der Suche bleibt offen.

Build 0a02 wurde vom Nutzer am 09.10.2026 als PASS abgenommen.

Build 0a04: Build/Hosttests PASS. Neue C++-Steuerungstests: Timer-Ablauf, Ersetzen/Aufheben, Grenzen, Überlauf, Lautstärkegrenze, Rampe, manueller Eingriff und stumm/sofortiger Start. UI-Tests: Grenze/Restzeit, Erhalt von Formularentwürfen, Konfigurations- und Timerbefehle, ungültige Timerdauer und inaktiver Timer. Neue Funktionen und NVS-Felder müssen am Gerät geprüft werden. Nutzer bestätigt Build 0a03 als PASS.

Build 0a04: Nutzer meldet PASS. Build 0a05: PlatformIO PASS; Sicherungsschema und strikte Pflichtfeld-/Grenzprüfung, Ersatzsender-Schwelle/Offline/Einmalwechsel, 15-Sekunden-Stillstand mit Überlauf und Web-Sicherung/Entwurfsschutz/Dateiwechsel PASS. Ein leeres lokales Audio.cpp.o und dessen Bibliotheksarchiv wurden neu erstellt; finaler Link und Firmwarebuild erfolgreich. Dynamische Sicherungspuffer und die vergrößerte Audiowarteschlange sind am Board zu beobachten. Nutzer bestätigt Build 0a05 am 09.10.2026 um 18:12 Uhr (Europe/Berlin) als PASS. Vollständige Hardwareabnahme bleibt separat offen.

Build 0a06: PlatformIO PASS; Schnellwahl/Offline-Sperre/gespeicherte Sammlung/Umordnung/Grenzen/Entwurfsschutz und tatsächliche Ersatzsender-Markierung als Hosttests PASS. Changelog aus zentraler Projektdatei generiert und Übereinstimmung geprüft. Keine Schemaänderung; Schnellwahlreihenfolge nutzt die gespeicherte Senderliste und ist dadurch bereits in Sicherungen enthalten. Visuelle und physische Boardprüfung hier nicht verfügbar; Gerätetest 0a06 offen.

Build 0a07 korrigiert den seit 0a05 gemeldeten periodischen Stream-Neustart (CMR-004) durch Entfernen des Audiozeit-Stillstandswächters. Bestätigung am betroffenen Sender steht aus.

Build 0a07: PlatformIO und Hosttests PASS. Audiozeit-Stillstandswächter entfernt; Ersatzsender- und Wiedergabesteuerungstests bestehen weiterhin. CMR-004-Gerätetest offen.

Build 0a07: Nutzer meldet PASS am 09.10.2026 um 18:26 Uhr, CMR-004 im erneuten Gerätetest behoben. Build 0a08: PlatformIO PASS, vorhandene Tests sowie OTA-Header/Größen-/Metadaten und Web-Uploadfluss PASS. Audiotask bestätigt Stilllegung vor Flashbeginn; Daten werden gehasht, der freie Slot erst nach vollständigem Upload und erfolgreicher Imagevalidierung aktiviert. Lokales leeres Settings.cpp.o wurde vor finalem erfolgreichen Build neu erstellt. Nutzer bestätigt Build 0a08 am 09.10.2026 um 18:39 Uhr (Europe/Berlin) als PASS nach dem angefragten Browserupdate-/Neustarttest mit erhaltenen Einstellungen. Gezielte Hashfehler-, Abbruch- und Stromausfalltests wurden nicht gesondert bestätigt. Keine automatische Rücknahme bei erfolgreicher Aktivierung eines später nicht startenden Builds. Visuelle Browserprüfung hier nicht verfügbar.

Build 0a09: PlatformIO PASS; Klangwerte/Grenzen/Typen, Migration alter Sicherungen, Teilfeld-Erhalt, Reglerbeschriftung, Entwurfsschutz, Neutral und Webpayload als Hosttests PASS. Ein leeres lokales WString.cpp.o und dessen Frameworkarchiv neu erstellt; finaler Build erfolgreich. Klangänderungen werden getrennt von Lautstärke/Rampe im Audiotask angewendet. NVS- und Sicherungsschema bleiben 1. Reale Hörprobe, Links-/Rechts-Zuordnung, Stromneustart und Wiederherstellung der Klangwerte OFFEN.

Build 0a09 vom Nutzer als PASS bestätigt. Build 0a0a: PlatformIO und Hosttests PASS. Flüchtige Klangvorschau getrennt von NVS/Sicherung; Reset und Speichern werden nach laufender Vorschauanfrage übertragen. Vorschau-Bündelung, Speichern bei laufender Anfrage und Fehlerzustand ohne hängendes Promise geprüft. Reale direkte Hörprobe und Neustartverhalten OFFEN.

Nutzerabnahme Build 0a0a am 09.10.2026 um 18:59 Uhr (Europe/Berlin): PASS nach angefragtem Test von direkter Klangvorschau, Zurücksetzen und Neustart ohne Speichern. Keine gesonderten Messwerte übermittelt; vollständige Hardwareabnahme bleibt separat.

v0.1.3 Build 01: PlatformIO und Hosttests PASS. Loudness-Grenzen/Stufen, Aus-Zustand, strikter Boolean, neutrale Migration alter Sicherungen und UI-Vorschau/Speichern geprüft. Ein leeres lokales AAC-Decoderobjekt und Audioarchiv vor erfolgreichem Build neu erstellt. Neue USB_ERSTINSTALLATION.txt wird automatisch in alle Firmwarepakete übernommen, passend beschriftet und durch SHA256SUMS erfasst. Physische Hörprobe/Update für 0.1.3 Build 01 offen. Voriger Nutzerstand 0.1.2 Build 0a0a PASS.

Nutzerabnahme v0.1.3 Build 01 am 09.10.2026 um 19:10 Uhr (Europe/Berlin): PASS nach angefragtem Loudness-Hörtest und Prüfung gespeicherter Werte nach Neustart. Keine gesonderten Messwerte übermittelt. USB-Erstinstallation dieses Pakets und vollständige Hardwareabnahme nicht gesondert bestätigt.

v0.1.3 Build 02: PlatformIO und Hosttests PASS. Logo-URL-/Typprüfung, Migration alter Sicherungen, Suchtreffer-Logoübernahme, Metadatentrennung/sichere Textanzeige, Bildfehler/Platzhalter und alte Ladeereignisse geprüft. Logos werden nur im Browser geladen. Sender-/Sicherungs-JSON-Puffer auf 24 KiB, Anfrage-/NVS-Grenze auf 16 KiB erweitert; dynamische Heapbelegung mit großer Sammlung am Board prüfen. USB-Anleitung bleibt enthalten. Wecker/Zeitpläne auf Nutzerwunsch gestrichen. Reale Logo-/Metadatenprüfung offen.

Nutzerabnahme v0.1.3 Build 02 am 09.10.2026 um 19:38 Uhr (Europe/Berlin): PASS nach angefragtem Test von Logos, Titelanzeige und Senderwechsel. Keine gesonderten Einzelnachweise übermittelt; vollständige Hardwareabnahme bleibt separat.

## v0.1.3 Build 03

Infobereich mit C. Mihalik, GitHub und PayPal-Unterstützungslink aus ABOUT.txt des CM-ThermoViewer 2.7 Build0017. Browserupdate und Prüfung der Linkziele am Gerät offen; Build 02 vom Nutzer als PASS bestätigt.

## v0.1.3 Build 04

Kompakte Geräteoberfläche mit sieben nativen aufklappbaren Bereichen, zwei Desktopspalten und einer Smartphonespalte. Nutzer bestätigt Build 03 als PASS; Passwortschutz vorerst zurückgestellt. Gerätetest und visuelle Abnahme auf realen Browsern offen.

## v0.1.3 Build 05

50 Lautstärkestufen in Audio/API/UI, Schema-1-Migration auf Schema 2 und Netzwerk in Gerät. Alte Sicherungen weiterhin importierbar; neue Schema-2-Daten sind nicht von älterer Firmware lesbar. Gerätetest inklusive Migration, Klang, Autostart und WLAN offen. Build 04 nicht gesondert vom Nutzer abgenommen.

Nutzerabnahme v0.1.3 Build 05 am 09.10.2026 um 20:04 Uhr (Europe/Berlin): PASS nach angefragter Prüfung von Lautstärke, Obergrenze, Neustart und WLAN-Suche. Keine gesonderten Messwerte oder Bestätigung eines Sicherungsimports übermittelt; vollständige Hardwareabnahme bleibt separat.

## v0.1.3 Build 06

Dauerhaftes Setup-Passwort mit verpflichtendem Erstwechsel, späterer Änderung und USB-Rücksetzen. Separat von Heimnetz und Sicherungen gespeichert. Hosttests für Passwortvalidierung, Pflichtoberfläche, Fehlerfall und spätere Änderung; tatsächlicher AP-Neustart, Fallback und NVS-Persistenz am Board noch zu prüfen.

Passwortreset per Taste ab Build 06: Bei laufendem Radio BOOT/IO0 10–59 Sekunden halten und loslassen. Nur Setup-/Fallback-Passwort wird auf passwort zurückgesetzt; verpflichtender Wechsel beim nächsten Browseraufruf. Nicht mit BOOT beim Einschalten verwechseln (Flashmodus). Während eines Firmwareupdates wird der Reset ignoriert; anschließend neu halten. Prüfen: kurzer Druck bewirkt nichts, ein langer Druck löst einmal aus, Heimnetz/Sender/Klang bleiben erhalten.

Werkseinstellungen über dieselbe BOOT/IO0-Taste: Bei laufendem Radio mindestens 60 Sekunden halten und loslassen. Erst das Loslassen löst den vollständigen Reset aus. Heim-WLAN, Sender, Klang, Lautstärke und Setup-Passwort werden gelöscht; Firmware bleibt installiert, Radio startet neu. Danach Erstzugang mit passwort und verpflichtender Änderung. Während Firmwareupdates werden Tastenresets ignoriert; Taste neu betätigen. Gerätetest: kurzer Druck ohne Wirkung, 10–59 s nur Passwort, ab 60 s vollständiger Reset. Vor dem Test Einstellungen sichern; Sicherung enthält keine Zugangspasswörter.

Build 07: Radio als Startseite auch im Fallback; nach Erstwechsel ebenfalls Radio, Netzwerk geschlossen. Passwort bleibt bei Neuladen und Updates gespeichert. Mindestlänge 8 wegen ESP32-WPA2; vier Zeichen technisch nicht direkt möglich. Gerätetest offen.

Nutzer bestätigt v0.1.3 Build 07 am 09.10.2026 um 20:32 Uhr (Europe/Berlin) als PASS nach angefragter Prüfung von Radio-Startseite und Passworterhalt nach Seitenneuladen und Neustart. Kein gesonderter Nachweis für Tasten-/Werksreset oder vollständige Hardwareabnahme.

## v0.1.3 Build 08

Gerätename, Mono/Stereo, Verbindungsdiagnose und Senderreparatur integriert. Hosttests und Kompilierung geprüft; Hardwareabnahme dieser vier Funktionen offen. Bluetooth nicht aktiviert.

Nutzerabnahme 09.10.2026: Build-08-Installation PASS (21:04 Europe/Berlin), 60-Minuten-Dauertest PASS und Passwortreset per BOOT PASS (21:05–21:06). Die vier neuen Funktionen und Werkseinstellungen sind damit nicht pauschal hardwareabgenommen.

Build 09: Favicon eingebettet; Hosttests einschließlich Abgleich der eingebetteten Grafik mit favicon.svg PASS. PlatformIO-Firmwarebuild PASS (1.426.385 Bytes Programmcode, 54.136 Bytes statisches RAM). Hardwareabnahme von Build 08 durch Nutzer am 10.10.2026 bestätigt; Favicon-Darstellung von Build 09 im realen Browser noch offen.

Nutzerabnahme v0.1.3 Build 09 am 10.10.2026: Favicon-Anzeige PASS. Firmware- und Hosttests PASS; Build-08-Funktionen zuvor vollständig durch Nutzer abgenommen.
