# CM-Radio – Änderungen

## v0.1.3 · Build 06 — 09.10.2026

- Dauerhafter Setup-/Fallback-Zugang: bei leerem Speicher Erstpasswort passwort; erster Browseraufruf verlangt einen Wechsel auf ein eigenes Passwort (8–63 druckbare ASCII-Zeichen, nicht passwort). Auch Upgrades ohne gespeichertes Setup-Passwort verlangen diesen einmaligen Schritt.
- Neues Passwort separat in NVS gespeichert; bleibt bei Neustart, Browserupdate, Wiederherstellung und reset-wifi erhalten. Nicht in Backup, Status, Diagnose oder serieller Ausgabe des eigenen Passworts enthalten. Vollständiges Flash-Erase setzt auch diesen Zugang zurück.
- Spätere Änderung unter Gerät → Netzwerk → Fallback-Zugang mit bisherigem Passwort und zweimaliger Eingabe des neuen Passworts. Bei aktivem CM-Radio-WLAN Neustart des Access Points nach kurzer Verzögerung; erneut mit neuem Passwort verbinden. Heim-WLAN-Passwort bleibt getrennt.
- Einstellungsänderungen und Updatevorbereitung bis zum verpflichtenden Wechsel serverseitig gesperrt. Kein allgemeiner Passwortschutz für die Bedienung im Heim-WLAN.
- BOOT/IO0 bei laufendem Radio zehn Sekunden halten setzt nur das Setup-Passwort zurück; erst nach zuvor beobachtetem Loslassen, einmal je langem Druck. Kurzer Druck ohne Wirkung; während Firmwareupdate ignoriert. BOOT beim Einschalten bleibt Flashmodus. Hosttest für Haltezeit, erneutes Drücken und Zeitüberlauf.
- USB-Befehl reset-ap-password setzt nur Setup-Zugang auf passwort zurück; Browser verlangt erneut Passwortwechsel. Sender, Heim-WLAN und Klang bleiben erhalten.
- Fußzeile auf aktuelle Buildkennung korrigiert. USB-Anleitung angepasst; Hosttests für Passwortgrenzen, Pflichtwechsel, Eingabebestätigung, Speicherfehler und spätere Änderung ergänzt. Gerätetest offen.

## v0.1.3 · Build 05 — 09.10.2026

- 50 tatsächliche Lautstärkestufen über setVolumeSteps(50) der Audiobibliothek; 0 bleibt stumm, 50 hat dieselbe maximale Verstärkung wie vorher 21. Regler, API, Obergrenze und sanfter Start nutzen 0–50. Loudness folgt der relativen Lautstärke; ab 36 keine zusätzliche Anhebung.
- NVS und neue Sicherungen verwenden Schema 2. Alte Schema-1-Werte werden beim Laden und Import mit floor(Wert × 50 / 21) umgerechnet; Grenzen steigen dadurch nicht über die bisherige relative Verstärkung. Beispiel: 5 wird 11, 21 wird 50. Sender, WLAN und Klang bleiben erhalten. Neue Schema-2-Werte werden unverändert geladen. Rückkehr zu älterer Firmware erfordert eine alte Sicherung bzw. Neueinrichtung, weil diese Schema 2 nicht versteht.
- Netzwerk in Gerät integriert: WLAN-Suche und Zugangsdaten als achter aufklappbarer Bereich. Hauptnavigation enthält Radio, Sender und Gerät. WLAN-Knopf und Einrichtungsmodus öffnen direkt Gerät → Netzwerk.
- Hosttests für alte/neue Sicherungen, Skalenmigration und 50er Lautstärkegrenze erweitert. Gerätetest Build 05 offen; für Build 04 liegt keine gesonderte PASS-Meldung vor.

## v0.1.3 · Build 04 — 09.10.2026

- Gerät kompakter gegliedert: sieben aufklappbare Bereiche für Wiedergabe, Klang, Sicherung, Firmwareupdate, Projektinfos, Changelog und technische Diagnose. Standardmäßig geschlossen; mehrere Bereiche können gleichzeitig geöffnet bleiben.
- Desktop zeigt zwei Spalten, Smartphone eine Spalte. Kürzere Abstände, kompakte Hilfetexte und vollständige Schaltflächen mit ausreichend großen Touch-Flächen. Gerätestatus mit Version/Build, WLAN und Speicherzustand bleibt oben sichtbar.
- Bestehende Formularwerte, direkte Klangvorschau, Speicherung, Sicherung und Updateablauf bleiben erhalten. Aufklappen benötigt keinen Netzwerkzugriff.
- Nutzer bestätigt Build 03 am 09.10.2026 um 19:49 Uhr als PASS. Passwortschutz für Updates und Änderungen auf Nutzerwunsch vorerst zurückgestellt.
- Gerätetest der neuen Anordnung auf Smartphone und Desktop für Build 04 offen.

## v0.1.3 · Build 03 — 09.10.2026

- Infobereich unter Gerät mit Ersteller C. Mihalik, öffentlichem GitHub-Projektlink und freiwilligem PayPal-Unterstützungslink. Angaben aus ABOUT.txt des CM IR Viewers / CM-ThermoViewer 2.7 Build0017 übernommen.
- Externe Links öffnen erst beim Anklicken einen neuen Tab; keine automatische Abfrage des Spendenanbieters. Infotext und Changelog bleiben lokal auf dem Radio verfügbar.
- Nutzer bestätigt v0.1.3 Build 02 als PASS. Prüfung des Infobereichs und der Linkziele am Gerät für Build 03 offen.

## v0.1.3 · Build 02 — 09.10.2026

- Senderlogos in Hauptansicht und Schnellwahl. Radiosendersuche übernimmt geeignete HTTPS-Favicons; eigene Logo-Adresse unter Sender möglich. Speichern, Neustart und Sicherung erhalten Logos; alte Daten laden ohne Logo.
- Bilder lädt ausschließlich der Browser, mit unterdrücktem Referrer. Fehlende/ungültige/defekte Hauptlogos bzw. acht Sekunden Ladezeit zeigen den CM-Platzhalter; derselbe Fehler wird nicht bei jeder Statusabfrage erneut angefordert. Ersatzsender nutzt seine tatsächliche Logo-Zuordnung.
- Titelanzeige trennt gängige Metadaten im Format Interpret - Titel (auch Gedankenstrich); andere Angaben bleiben als kompletter Titel erhalten. Technische Streammeldung getrennt anzeigen; fehlende Titel ausdrücklich kennzeichnen. Sendermetadaten werden als Text angezeigt.
- Sender-/Sicherungsdaten dürfen nun bis 16 KiB enthalten; Speicherpuffer für Logo-URLs erweitert. Logo-Adressen optional und auf HTTPS ohne Zugangsdaten begrenzt.
- Wecker und Zeitpläne entfallen auf Nutzerwunsch. RM-23 bleibt als gestrichene historische Referenz, blockiert Android-Voraussetzungen nicht mehr.
- v0.1.3 Build 01 vom Nutzer als PASS bestätigt. Logo-/Metadaten-Hörtest für Build 02 offen.


## v0.1.3 · Build 01 — 09.10.2026

- Neue Versions-/Buildkennung nach Nutzerwunsch: v0.1.3, Build 01; folgende Builds 02, 03 usw.
- Schaltbare Loudness unter Gerät, auch in direkter Klangvorschau: bei tatsächlicher Lautstärke 1 bis 14 bis zu +4 dB Bass und +2 dB Höhen, ab 15 ohne Zusatzanhebung, bei 0 ohne Anhebung. Gesamt-EQ-Werte höchstens +6 dB.
- Loudness folgt Lautstärkeregler und sanftem Start im Audiotask; Tone-Koeffizienten nur bei geänderten effektiven Gainwerten neu gesetzt. Bestehende Bass-/Höhenwerte und Balance bleiben als Grundlage erhalten.
- Loudness in NVS, Status, Klangvorschau, Diagnose und Sicherungen; alte Daten laden ausgeschaltet. Gespeicherte Werte wiederherstellen und Neutral hören berücksichtigen Loudness.
- Jedes neue Firmware-ZIP enthält automatisch USB_ERSTINSTALLATION.txt mit ausführlichen Windows-/PowerShell-Schritten, BOOT/RST, WLAN, Fehlersuche und OTA-Slot-Hinweisen. Paketgenerator setzt passende Version/Build/Dateinamen ein.
- Ausgangsstand v0.1.2 Build 0a0a vom Nutzer als PASS bestätigt; Hörprobe und Updateabnahme für v0.1.3 Build 01 offen.


## v0.1.2 · Build 0a0a — 09.10.2026

- Klangvorschau beim Verschieben von Bässen, Höhen und Balance, ohne dauerhafte Speicherung. Schnelle Bewegungen werden gebündelt und Vorschauanfragen nacheinander gesendet.
- Klang dauerhaft speichern übernimmt die aktuellen Reglerwerte nach Ende einer laufenden Vorschauanfrage. Gespeicherte Werte wiederherstellen verwirft die Vorschau und stellt den dauerhaft gespeicherten Klang wieder ein.
- Neutral hören wendet neutrale Werte vorübergehend an. Erst Speichern übernimmt sie dauerhaft. Sicherungen exportieren weiterhin nur gespeicherte Werte; Neustart lädt gespeicherten Klang.
- Aktive Vorschau wird im Status angezeigt und beim erneuten Öffnen der Oberfläche erkennbar. Wiederherstellung und Update bleiben bei offenen Klangänderungen gesperrt.
- Nutzer bestätigt Build 0a09 als PASS. Direkte Klangvorschau und Rücksetzen für 0a0a am Board noch zu prüfen.


## v0.1.2 · Build 0a09 — 09.10.2026

- Klangregler unter Gerät: Bässe und Höhen von −12 bis +6 dB, Balance von −16 (nur links) bis +16 (nur rechts). Neutral setzt alle Regler auf 0; Speichern wendet den Entwurf an und erhält ihn dauerhaft.
- Klangbefehle laufen ausschließlich im Audiotask und benötigen keinen Stream-Neustart. Die Mitte des Equalizers bleibt neutral. Die vorhandene Lautstärkegrenze und der sanfte Start bleiben getrennt davon erhalten.
- Klangdaten in Status, Konfiguration, Diagnose und Einstellungssicherung. Alte NVS-Daten und Schema-1-Sicherungen ohne Klangfelder laden neutral; neue Felder werden streng geprüft. Wiederherstellung zeigt Klangwerte in der Vorschau und reiht die Anwendung nach Stop ein.
- Ungespeicherte Klangentwürfe bleiben bei Statusabfragen erhalten und blockieren Wiederherstellung sowie Firmwareinstallation. Loudness bleibt geplant.
- Build 0a08 einschließlich Browserupdate-/Neustarttest vom Nutzer als PASS bestätigt. Hörprobe, Kanalzuordnung und Klangpersistenz für 0a09 offen.


## v0.1.2 · Build 0a08 — 09.10.2026

- Lokales Firmwareupdate unter Gerät: manifest.json und firmware.bin aus demselben Paket auswählen, Paket prüfen, Installation ausdrücklich bestätigen. Uploadfortschritt und Neustarthinweis anzeigen.
- Updatepakete enthalten Größe, SHA-256 und Hardwareziel der Anwendungsfirmware. Das Radio prüft diese Daten und den ESP32-Imageheader, schreibt den freien OTA-Slot und aktiviert ihn erst nach vollständiger Prüfung und vollständigem HTTP-Upload.
- Audio und Timer werden vor dem Schreiben im Audiotask gestoppt. Ausstehende Einstellungen werden vorher gespeichert; Änderungen sind während des Updates gesperrt. Fehler oder unvollständige Dateien aktivieren keinen neuen Slot. Nach Fehler Audio bei Bedarf manuell starten.
- Sitzungstoken und Browser-Ursprungsprüfung begrenzen den Upload auf die vorbereitete Sitzung; kein automatisch heruntergeladenes Internetupdate und keine signierten Pakete.
- Nutzer bestätigt Build 0a07 am 09.10.2026 um 18:26 Uhr als PASS; CMR-004 im erneuten Gerätetest behoben. Physischer Update-/Neustarttest für 0a08 offen.


## v0.1.2 · Build 0a07 — 09.10.2026

- Korrektur für CMR-004: seit 0a05 gemeldeter Stream-Neustart nach ungefähr zehn Sekunden. Der in 0a05 eingeführte Audiozeit-Stillstandswächter wurde entfernt: die berechnete Audiozeit ist kein zuverlässiger Verbindungsnachweis für jeden Livestream.
- Laufende Streams werden nicht mehr wegen einer unveränderten Audiozeitanzeige gestoppt. Wiederverbindung nach tatsächlichem Verbindungsende und Ersatzsender nach erfolglosen Verbindungsversuchen bleiben erhalten.
- Build 0a05 PASS-Meldung bleibt historisch erhalten; spätere Regression separat dokumentiert. Korrektur muss am betroffenen Sender geprüft werden.


## v0.1.2 · Build 0a06 — 09.10.2026

- Schnellwahl: große Senderkacheln starten gespeicherte Sender direkt. Der tatsächlich aktive Haupt- oder Ersatzsender wird gekennzeichnet. Offline oder bei nicht bereitem Audio sind die Kacheln gesperrt.
- Reihenfolge unter Sender mit Nach oben/Nach unten ändern und dauerhaft speichern. Haupt- und Ersatzsenderzuordnung bleibt anhand der Streamadresse erhalten. Ungespeicherte Entwürfe verändern die Schnellwahl nicht.
- Vollständiger bisheriger Projekt-Changelog unter Gerät, offline vom Radio verfügbar. Inhalte werden aus docs/CHANGELOG.md erzeugt und beim Hostcheck auf Übereinstimmung geprüft.
- Build 0a05 vom Nutzer als PASS bestätigt. Gerätetest für 0a06 offen.


## v0.1.2 · Build 0a05 — 09.10.2026

- Versionierte JSON-Sicherung der vorhandenen Sender und Wiedergabeeinstellungen. WLAN-Zugangsdaten und laufende Timer bleiben ausgeschlossen.
- Wiederherstellung mit serverseitiger Prüfung, Vorschau und eigener Übernahme. Ungültige Dateien verändern keine Einstellungen. Übernahme erhält das Heim-WLAN, stoppt Audio und hebt den Sleep-Timer auf.
- Ersatzsender nach drei erfolglosen Streamversuchen bei verfügbarem WLAN. Pro Wiedergabestart höchstens ein Wechsel; kein automatischer Rückwechsel. Identische Streamadressen werden übersprungen.
- Stillstehende Audiozeit löst nach 15 Sekunden einen neuen Verbindungsversuch aus. Stoppen und Sleep-Timer bleiben wirksam.
- Hosttests für Schema/Typen/Grenzen, Ersatzsender und Webübernahme ergänzt. Nutzer bestätigt Build 0a05 als PASS. Build 0a04 vom Nutzer als PASS bestätigt.


## v0.1.2 · Build 0a04 – 9. Oktober 2026

- Sleep-Timer mit 15/30/60-Minuten-Schnellwahl und eigener Dauer 1–180 Minuten; Restzeit anzeigen, Dauer ändern oder aufheben. Ablauf stoppt Audio inklusive Wiederholungen. Manuelles Stoppen hebt den Timer auf; Senderwechsel behält ihn bei. Stromneustart startet ohne Timer.
- Sanfter Start von 0–30 Sekunden (Standard 5; 0 aus), angewendet bei Play, Autostart und erneuter Streamverbindung. Manuelle Lautstärkeänderung beendet die laufende Rampe.
- Gespeicherte maximale Lautstärke 0–21 (Standard 21) in UI und API; Absenkung reduziert gespeicherten Zielwert und tatsächliche Ausgabe. Audio-Task begrenzt auch eingereihte Lautstärkebefehle.
- Neue optionale Konfigurationsfelder werden im bestehenden NVS-Schema gespeichert; vorhandene WLAN-/Senderdaten laden weiter mit Standardwerten für die neuen Felder.
- Konfigurationsänderungen bleiben als ausstehend sichtbar, bis der Audio-Befehl eingereiht wurde. Sleep-Timer und Rampen werden ausschließlich im Audio-Task verwaltet.
- Build/Hosttests PASS; neue Funktionen und Erhalt der Einstellungen müssen am Board geprüft werden.
- Nutzerabnahme von Build 0a03 am 09.10.2026: PASS.

## v0.1.2 · Build 0a03 – 9. Oktober 2026

- Radiosendersuche im Senderbereich: international, national nach Land und lokal über Namen/Regionsangaben. Lokale Suche benötigt einen Begriff; keine GPS-/Umkreissuche.
- Länderliste nachladen; bis zu 30 geeignete Treffer anzeigen. MP3/AAC und HTTP(S) berücksichtigen, bekannte andere Codecs/HLS sowie doppelte Streamadressen ausfiltern.
- Treffer als Entwurf zur Sammlung hinzufügen; bestehende Entwürfe erhalten. Erst „Änderungen speichern“ schreibt die Sammlung aufs Gerät; Grenze bleibt zehn Sender.
- Suchanfragen laufen ausschließlich im Browser über HTTPS zu Radio-Browser. Serverliste wird bei Bedarf geladen; Zeitlimits und Wechsel auf andere Verzeichnisserver vorgesehen. Suche sendet Suchbegriff/Land, keine WLAN-Zugangsdaten.
- Build/Hosttests PASS; echte Verzeichnisabfrage mit CORS erfolgreich. Vollständiger Browser-/Boardtest der Suche offen.
- Nutzerabnahme von Build 0a02 am 09.10.2026: PASS.

## v0.1.2 · Build 0a02 – 9. Oktober 2026

- Neue responsive Weboberfläche mit Navigation für Radio, Sender, Netzwerk und Gerät; größere Wiedergabebedienung und sichtbar beschriftete Senderfelder.
- Grafischer WLAN-Empfang mit vier Balken: Grün für guten, Gelb für mittleren und Rot für schwachen Empfang. Text und dBm ergänzen die Farbe; Setup, offline und fehlender Gerätestatus werden separat dargestellt.
- Einrichtung öffnet bei aktivem Setup automatisch den Netzwerkbereich.
- Grundtests von Build 0a01 am Board bestätigt: WLAN-Suche, beide Lautsprecher, Lautstärke/Stop/Play und Autostart nach Stromunterbrechung. Dauertest vom Nutzer als bisher erfolgreich eingeschätzt; bestätigte Dauer und abschließender Gerätestatus fehlen noch.
- Build 0a02 benötigt einen erneuten Test der Oberfläche am Gerät. Noch keine neue Sendersuche, Klangregler oder OTA-Updates enthalten.

## v0.1.2 · Build 0a01 – 9. Oktober 2026

- WLAN-Suche pausiert Verbindungsversuche und startet nach kurzer Vorbereitung; begrenzte Startwiederholungen und Timeout.
- Einheitliche Buildkennung in Status-API, Startausgabe, Weboberfläche und Paketmanifest.
- Asynchrone Suche nach verfügbaren 2,4-GHz-WLANs im Setup; Auswahl übernimmt den WLAN-Namen. Signalstärke und offene/gesicherte Netze werden angezeigt. Manuelle Eingabe bleibt möglich.
- USB-Flash und erster Boot von V0.1.1 am gelieferten Board bestätigt; Audio- und weitere Hardwaretests bleiben offen.

## V0.1.1 – 9. Oktober 2026

- Webbedienung lädt nach einem Verbindungsfehler automatisch neu; keine parallelen Status-Abfragefolgen.
- Einzelne Anfragen werden nach sechs Sekunden beendet; erneute Prüfung bleibt möglich.
- Offlineanzeige und gesperrte Wiedergabeaktionen, solange der Gerätestatus nicht verfügbar ist.
- Diagnosebericht im Browser ohne WLAN-Zugangsdaten, IP oder Senderdaten.
- API ergänzt niedrigsten freien Heap und Neustartgrund.
- Hardwarebasis: geliefertes Loud-ESP32 E3; Firmware-Abnahme auf dem Board noch offen.

## V0.1.0

WROVER-Firmware, Setup-WLAN, lokale Webbedienung, NVS, Stereo-Audio und Erststarttest vorbereitet.
