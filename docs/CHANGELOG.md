# CM-Radio – Änderungen

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
