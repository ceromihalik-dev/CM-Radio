# CM-Radio – lokale API V0.1

Basis: `http://cm-radio.local/api/v1` oder `http://GERAETE-IP/api/v1`. Antwortformat JSON; Schreibzugriffe mit `Content-Type: application/json`. Senderindizes beginnen bei 0. Keine Anmeldung, Nutzung im vertrauenswürdigen lokalen Netz. WLAN-Passwörter werden nicht ausgelesen. Unbekannte Endpunkte liefern 404.

| Methode / Pfad | Anfrage | Ergebnis |
| --- | --- | --- |
| GET `/status` | – | Version, Board, WLAN/IP, Flash/PSRAM, Audiozustand, Titel, Lautstärke, Speicherstatus |
| GET `/stations` | – | `{"stations":[{"name":"…","url":"http://…"}]}` |
| PUT `/stations` | `{"stations":[{"name":"…","url":"http://…"}]}` | Gesamte Liste ersetzen, 1–10 Sender |
| POST `/play` | `{"station":0}` | Sender speichern und Wiedergabe anfordern |
| POST `/stop` | `{}` | Wiedergabe stoppen, Autostart bleibt erhalten |
| POST `/volume` | `{"volume":5}` | Lautstärke 0–21, nach 2 s Ruhe speichern |
| GET `/config` | – | `{"ssid":"…","autoplay":true}` |
| POST `/config` | `{"autoplay":true}` | Autostart dauerhaft setzen |
| POST `/wifi` | `{"ssid":"…","password":"…"}` | Dauerhaft speichern, nach 1,5 s Verbindung wechseln |

Erfolgreiche Schreibzugriffe: **202** mit `{"accepted":true}`. Audio arbeitet asynchron; danach `/status` abfragen. Das ist keine Bestätigung bereits hörbaren Tons.

Fehler: **400** ungültige Werte/JSON, **403** fremder Browser-Origin, **413** Körper über 8192 Bytes, **415** falscher Content-Type, **503** Audio nicht bereit / Queue voll, **507** NVS-Schreiben gescheitert. JSON-Fehlerformat `{"error":"…"}`. Bei einem Queue-Fehler nach bereits erfolgreichem Speichern kann die Konfiguration übernommen sein; `/status` prüfen und Wiedergabe erneut anfordern.

Namen: 1–63 UTF-8-Bytes. URLs: weniger als 384 Bytes, HTTP(S), keine Leerzeichen/Steuerzeichen und keine Benutzerinformationen im Host. Die API kann nicht garantieren, dass eine syntaktisch gültige URL einen unterstützten Audiostream liefert. WLAN-SSID: 1–32 Bytes; offenes WLAN mit leerem Passwort oder WPA-Passwort 8–63 Bytes. WPA-Enterprise ist nicht Teil V0.1.

`state` ist `error`, `stopped`, `connecting` oder `streaming`. `requested` beschreibt die gewünschte Wiedergabe; `running` den Bibliotheksstatus. `settingsPending:true` bedeutet, dass eine Lautstärkeänderung noch nicht im NVS gespeichert ist. Für Kanalnachweis oder Dauerstabilität gibt es keinen API-Ersatz.

```sh
curl http://cm-radio.local/api/v1/status
curl -X POST http://cm-radio.local/api/v1/play -H 'Content-Type: application/json' -d '{"station":0}'
curl -X POST http://cm-radio.local/api/v1/volume -H 'Content-Type: application/json' -d '{"volume":5}'
curl -X POST http://cm-radio.local/api/v1/stop -H 'Content-Type: application/json' -d '{}'
```

V0.1.1 ergänzt `/status` um `minFreeHeap` (Bytes) und `resetReason` (numerischer ESP32/ESP-IDF-Neustartgrund). Vorhandene Felder und API-Pfade bleiben erhalten.

## WLAN-Suche (V0.1.2)

`POST /api/v1/wifi/scan` mit `{}` startet asynchron (202). `GET /api/v1/wifi/scan` liefert `scanning` und `networks` mit `ssid`, `rssi`, `channel`, `secure`. Während der Suche erneut abfragen; fehlgeschlagene oder nicht gestartete Suche: 503. Maximal 20 unterschiedliche sichtbare SSIDs, stärkste zuerst. Versteckte Netzwerke manuell eingeben. Kein Passwort wird zurückgegeben.

Build 0a01 ergänzt `/status` um `build`. Die WLAN-Suche pausiert Wiederverbindung, bereitet den Start 300 ms vor und wiederholt abgelehnte Starts höchstens dreimal. Zeitlimit 12 Sekunden. Speichern während der Suche: 409.

## Sendersuche (Build 0a03)

Die Weboberfläche fragt Radio-Browser direkt im Handy-/PC-Browser ab; keine zusätzliche Suchroute auf dem ESP32. Übernahme nutzt weiterhin `PUT /api/v1/stations`. Namen sind auf 63 UTF-8-Bytes begrenzt, Streamadressen auf 383. Änderungen werden erst nach explizitem Speichern geschrieben. Eine spätere Android-App muss die Verzeichnissuche ebenfalls integrieren. API-Quelle: https://docs.radio-browser.info/ .

## Wiedergabekomfort (Build 0a04)

`POST /api/v1/config` akzeptiert jetzt Teiländerungen mit `autoplay` (bool), `volumeLimit` (int 0–21) und/oder `softStartSeconds` (int 0–30). Mindestens ein bekanntes Feld ist erforderlich, ungültige Felder liefern 400. Die Grenze wird gespeichert; ein höherer gespeicherter Lautstärkewert wird abgesenkt. Bei Erhöhung bleibt der aktuelle Zielwert erhalten. `GET /config` liefert die beiden neuen Werte. `POST /volume` über der gespeicherten Grenze: 400.

`POST /api/v1/sleep` mit `{"minutes":15}` startet/ersetzt den Timer; 0 hebt ihn auf, maximal 180. Antwort 202 bedeutet eingereiht, 400 ungültiger Wert, 503 Audio nicht bereit oder Queue voll. Timer wirkt auch bei Senderwechsel, wird bei manuellem Stop und Stromneustart aufgehoben.

`GET /status` ergänzt `volumeLimit`, `softStartSeconds`, `effectiveVolume` (tatsächlicher Audio-Reglerwert), `ramping`, `sleepRemainingSeconds`, `audioConfigPending`. `volume` bleibt der gespeicherte Zielwert. `maxVolume` bleibt die Hardware-/API-Skala 21. `audioConfigPending` bezeichnet die noch nicht eingereihte Anwendung gespeicherter Einstellungen; Verarbeitung im Audio-Task ist asynchron.

## Ergänzungen Build 0a05

- `GET /api/v1/backup`: JSON `{format:"CM-Radio-Backup",schema:1,sourceVersion,sourceBuild,settings}`. Settings enthält `stations:[{name,url}]`, `selected`, `volume`, `autoplay`, `volumeLimit`, `softStartSeconds`, `fallbackStation`. Keine WLAN-Zugangsdaten und keine laufenden Timer.
- `POST /api/v1/restore/validate`: Sicherungsobjekt, maximal 8192 Bytes. Prüft alle Pflichtfelder ohne Änderung und antwortet mit `valid:true`, `stationCount`, `volume`, `volumeLimit`, `wifiPreserved:true`. Fehler HTTP 400.
- `POST /api/v1/restore`: gleiche Prüfung, anschließend persistente Übernahme; HTTP 202. Heim-WLAN bleibt erhalten. Stop wird vor der neuen Audiokonfiguration eingereiht und hebt den Timer auf. Kein unmittelbarer Autostart; die gespeicherte Autostart-Einstellung gilt beim nächsten Neustart. Bei Speicherfehler keine erfolgreiche Übernahme.
- `POST /api/v1/config`: optional `fallbackStation` als Integer, `-1` = aus oder gültiger gespeicherter Senderindex. Bestehende Felder unverändert. Senderlistenänderungen erhalten die Ersatzzuordnung anhand der Streamadresse, Entfernen deaktiviert sie.
- Status ergänzt `fallbackStation`, `fallbackActive`, `requestedStation` und `restoreStopPending`; `station` nennt den hörbaren Ersatzsender. `audioConfigPending` umfasst auch die noch einzureihende Ersatzkonfiguration. HTTP 202 bestätigt die Annahme, nicht bereits erfolgte Ausführung im Audiotask.

Schema 1: 1–10 Sender, Namen maximal 63 UTF-8-Bytes und nicht leer, HTTP(S)-URLs maximal 383 Bytes ohne Zugangsdaten/Steuerzeichen; Auswahl gültig; Lautstärke 0–21 und höchstens Grenze; sanfter Start 0–30 Sekunden; Autoplay strikt Boolean. Alle genannten Einstellungsfelder sind Pflichtfelder. Unbekannte Felder werden nicht übernommen. Künftige Klang-/Zeitplanfunktionen sind noch kein Bestandteil der Sicherung.

Ersatzwechsel: drei Verbindungsversuche ohne stabilen Stream, nur bei verbundenem WLAN, höchstens einmal bis zum nächsten Play/Stop. Identische URLs lösen keinen Wechsel aus. Ein laufender Ersatz wird bei Änderung seiner Konfiguration nicht unmittelbar umgeschaltet. 15 Sekunden ohne Fortschritt der Audiozeit lösen einen neuen Verbindungsversuch aus.

## Ergänzung Build 0a06

Status ergänzt `playingStationIndex`: Senderindex des im Audiotask aktuell angeforderten Streams, anhand der tatsächlichen URL auf die gespeicherte Sammlung abgebildet; `-1`, wenn kein Stream angefordert oder keine passende gespeicherte Adresse vorhanden ist. Die Oberfläche markiert diesen Index nur bei `state:"streaming"`. `stationIndex` bleibt die dauerhaft gewählte Hauptsenderauswahl; `fallbackStation` die konfigurierte Ersatzsenderauswahl. Mehrere Einträge mit gleicher URL markieren den ersten Treffer. Schnellwahl verwendet die bestehende Play-API, Reihenfolge die bestehende Stations-PUT-API; keine Schemaänderung.

Ab Build 0a07 entfällt der Audiozeit-Stillstandswächter. Eine unveränderte berechnete Audiozeit löst keinen Stream-Neustart aus. Die reguläre Wiederverbindung nach Verbindungsende bleibt erhalten.

## Firmwareupdate Build 0a08

`POST /api/v1/update/prepare` mit JSON `{target:"CM-Radio-WROVER-N8R8",file:"firmware.bin",size,sha256}`: size strikt Integer 1024–3145728, sha256 genau 64 Kleinbuchstaben/Hexziffern. Ziel, tatsächliche 8-MiB-Flashgröße und freier OTA-Slot müssen passen. Ausstehende NVS-Daten werden gespeichert. HTTP 202 liefert einen zufälligen Sitzungstoken; bestehende Sitzung HTTP 409. Vorbereitung stoppt Audio und Timer asynchron. Vor Upload `GET /api/v1/update/status` abfragen, bis `phase:"prepared"` und `audioStopped:true`.

`POST /api/v1/update` als multipart/form-data mit genau einer Datei im Feld `firmware`, Dateiname `firmware.bin`, Header `X-CM-Update-Token`. Headerprüfung (ESP32-Chip-ID), Größenbegrenzung und SHA-256 erfolgen im Streamingbetrieb. Firmware wird in den inaktiven Slot geschrieben; Aktivierung erst nach erfolgreichem Hash, vollständigem Multipart-Upload und Update.end(false). HTTP 200 und Neustart nach etwa 1,8 Sekunden. Ungültige Daten HTTP 400, ungültige Sitzung/Ursprung HTTP 403. Mehrere Dateien führen zum Abbruch ohne Aktivierung.

`POST /api/v1/update/cancel` mit demselben Tokenheader beendet Vorbereitung bzw. nicht aktivierten Upload. Bereits aktivierte Firmware kann nicht mehr so abgebrochen werden. Zeitlimits: Vorbereitung 60 Sekunden, Upload insgesamt 180 Sekunden ab Vorbereitung, Browser-Upload 120 Sekunden. Statusfelder: phase (`idle`, `prepared`, `receiving`, `verified`, `failed`, `rebooting`), error, received, size, audioStopped. Status enthält keinen Token. Allgemeiner Gerätestatus ergänzt `updating`.

Während aktiver Sitzung lehnen bestehende JSON-Schreibendpunkte Änderungen mit HTTP 409 ab. GET-Abfragen bleiben verfügbar, während der WebServer den Upload verarbeitet sind parallele Abfragen jedoch blockiert. Audio bleibt bei Fehler gestoppt; nach Ende/Abbruch wieder manuell starten. Bei Erfolg gilt Autostart nach Neustart. HTTP-Transport im lokalen Netz, keine Benutzeranmeldung oder Signaturprüfung; Sitzungstoken ist kein Schutz vor allen lokalen Netzteilnehmern. SHA-256 prüft Dateiintegrität relativ zum gewählten Manifest, nicht dessen Herkunft. Nur vertrauenswürdige Projektpakete verwenden. Automatischer Internetbezug und automatische Rücknahme eines erfolgreich aktivierten, aber später fehlerhaften Builds sind nicht implementiert.

## Klang Build 0a09

GET config und GET status ergänzen `bass`, `treble` und `balance`. POST config nimmt beliebige Teilmengen als strikte Integer an: bass/treble −12 bis +6 dB, balance −16 bis +16 (negativ links, positiv rechts). Nicht angegebene Felder bleiben erhalten. Bool, String, Bruchzahlen und Bereichsüberschreitungen: HTTP 400 ohne Persistenz. Konfiguration wird vor Audioanwendung gespeichert; HTTP 202 bestätigt Annahme. `audioConfigPending` umfasst ausstehende Klangbefehle. Audio.setTone(bass,0,treble) und setBalance(balance) ausschließlich im Audiotask, ohne Neustart der Wiedergabe oder Änderung der Lautstärkerampe.

Sicherungsschema bleibt 1 und exportiert diese drei Klangfelder. Alte Sicherungen ohne Klangfelder werden mit neutralen Werten 0 importiert; mitgelieferte Felder müssen dieselben strikten Grenzen erfüllen. Restore/validate ergänzt die drei Werte in der Vorschau. NVS bleibt Schema 1 und lädt fehlende Klangfelder neutral. Lautstärkegrenze begrenzt weiterhin den Lautstärkeregler, nicht einen gemessenen Schalldruckpegel. Loudness ist nicht implementiert.

## Klangvorschau Build 0a0a

`POST /api/v1/sound/preview` mit allen drei strikten Integerfeldern `{bass,treble,balance}` und den Grenzen aus 0a09. Queueannahme HTTP 202, ungültige/unvollständige Werte 400, laufende Restore/Klanganwendung 409, Audio nicht bereit/Queue voll 503. Nur Audio-Queue und flüchtiger Vorschauzustand werden geändert, kein NVS und keine gespeicherten Klangwerte. Status und Konfiguration ergänzen `soundPreview`, `previewBass`, `previewTreble`, `previewBalance`. Diese nennen angenommene Ziele; HTTP 202 ist kein Nachweis einer bereits erfolgten Audioanwendung. `bass`, `treble`, `balance` bleiben dauerhaft gespeicherte Werte.

`POST /api/v1/sound/reset` mit `{}` stellt gespeicherte Werte über die Audiowarteschlange wieder her und beendet die Vorschau. POST config mit mindestens einem Klangfeld beendet Vorschau und reiht gespeicherte Klangwerte auch dann erneut ein, wenn die gespeicherten Zahlen unverändert sind. Andere Konfigurationsfelder allein verändern die Vorschau nicht. Sicherungen exportieren nur gespeicherten Klang. Restore und Neustart laden gespeicherte Werte; Stop/Play und Senderwechsel erhalten die flüchtige Vorschau. Die UI bündelt Reglerbewegungen in etwa 100-ms-Abständen, höchstens eine Vorschauanfrage gleichzeitig. Vor Speichern/Reset beendet sie ausstehende Vorschauübertragungen, um späte Überschreibungen zu vermeiden.

## v0.1.3 Build 01 – Loudness

`loudness` ist optionales strikt boolesches Feld in POST config sowie POST sound/preview und wird in NVS und Schema-1-Sicherungen gespeichert. Fehlende Felder in alten Daten/Sicherungen laden false. Vorschau ohne das Feld verwendet false; alle drei Zahlenfelder bleiben Pflicht. GET config/status ergänzen gespeichertes loudness und previewLoudness. Status ergänzt effectiveBass/effectiveTreble: die im Audiotask angewendeten dB-Werte einschließlich Loudness. Sicherungen enthalten gespeicherte Werte; temporäre Vorschau bleibt ausgeschlossen.

Loudness-Zusatz bei tatsächlicher Audio-Lautstärke v (nach Rampe/Grenze): für 1<=v<15 Bass floor((15-v)*4/14), Höhen floor(Basszusatz/2); sonst 0. Werte werden auf maximal +6 dB begrenzt. Balance bleibt unverändert. Neutral hören schaltet auch Loudness in der Vorschau aus; Rücksetzen lädt die gespeicherte Loudnesswahl. Dies ist eine einfache lautstärkeabhängige Klangkorrektur, keine kalibrierte Schalldruckregelung. Versionsnummer 0.1.3, Build 01.

## v0.1.3 Build 02 – Logos und Metadaten

Senderobjekte in GET/PUT stations, NVS und Sicherung ergänzen optionales `logo`: leer oder HTTPS-URL mit denselben Längen-/Steuerzeichen-/Zugangsdaten-Grenzen wie Streamadressen (maximal 383 Bytes). Falsche Typen/URLs HTTP 400; fehlend = leer. Status ergänzt `stationLogo`: Logo des tatsächlich angeforderten Streams anhand playingStationIndex, im gestoppten Zustand Logo der ausgewählten Station. Kein Treffer für den laufenden Stream = leeres Logo. Schema bleibt 1; alte Daten kompatibel.

Anfrage- und NVS-Textlimit für Sender/Sicherungen nun 16384 Bytes (vorher 8192); entsprechende JSON-Puffer 24576 Bytes. Senderlogos sind URL-Verweise, keine eingebetteten Dateien. ESP32 lädt keine Bilder herunter. Browser verlangt HTTPS, unterdrückt Referrer und zeigt bei Fehler bzw. acht Sekunden ohne Hauptlogo einen Platzhalter. Externe Bildquellen benötigen Internet im Browser und sehen die Bildanfrage; Ausfall verändert Audio nicht.

`title` bleibt die unveränderte Streammetadaten-Zeichenfolge. Die UI trennt erstes Muster 'Interpret - Titel' mit Leerraum und Bindestrich/typografischem Gedankenstrich; weitere Trennzeichen bleiben im Titel. Dies ist eine Anzeigeheuristik, keine verifizierte Interpretenerkennung. Ohne Muster vollständiger Titel, ohne Metadaten Ersatztext; technische Meldung separat. Wecker/Zeitpläne entfallen aus dem Projektumfang.

## v0.1.3 Build 05 – Lautstärkeskala und Migration

Ab diesem Build überschreiben folgende Angaben die historische 21er-Skala: volume/volumeLimit/effectiveVolume nutzen 0–50, maxVolume und volumeSteps im Status sind 50. Der Audio-Task verwendet setVolumeSteps(50) mit derselben quadratischen Verstärkungskurve. POST /volume ist zusätzlich auf die gespeicherte Grenze beschränkt. POST /config akzeptiert volumeLimit 0–50. Loudness ist an die relative Skala angepasst, ab 36 ohne Zusatzanhebung.

Neue NVS-Daten und Sicherungen verwenden Schema 2. Schema-1-NVS und -Sicherungen validieren zunächst Werte 0–21, dann Umrechnung floor(Wert × 50 / 21) für Lautstärke und Grenze. Schema-2-Werte werden unverändert übernommen; Restore/validate zeigt bereits umgerechnete Werte. Maximaler JSON-Body 16 KiB, Logo- und Klangfelder wie in Build 02. Ältere Firmware versteht Schema 2 nicht.

## v0.1.3 Build 06 – Setup-Passwort

GET /status ergänzt setupPasswordRequired (bool). POST /setup/password: JSON {password:string,currentPassword?:string}. Neues Passwort 8–63 druckbare ASCII-Zeichen, nicht passwort. Nach Erstwechsel currentPassword erforderlich und mit gespeichertem Passwort verglichen; 403 bei Abweichung. Speicherung separat in NVS, vor Änderung des laufenden AP; Speicherfehler 507. Erfolg 200 {accepted:true,reconnectRequired:bool}. Bei aktivem AP Neustart nach 2500 ms; erneute Verbindung mit neuem Passwort erforderlich.

Bis zum Erstwechsel normale JSON-Schreibaktionen und Updatevorbereitung mit 428 gesperrt; während geplanter AP-Umstellung JSON-Schreiben 409 bzw. Updatevorbereitung 428. Lesezugriffe bleiben verfügbar. Origin-Prüfung wie bisher; dies ist kein allgemeiner Zugriffsschutz für Bedienung im Heimnetz. Setup-Passwort nie in Status/Backup/Diagnose. reset-ap-password per USB setzt nur den Setup-Zugang zurück, reset-wifi erhält ihn.

Passwortreset per Taste ab Build 06: Bei laufendem Radio BOOT/IO0 10–59 Sekunden halten und loslassen. Nur Setup-/Fallback-Passwort wird auf passwort zurückgesetzt; verpflichtender Wechsel beim nächsten Browseraufruf. Nicht mit BOOT beim Einschalten verwechseln (Flashmodus). Während eines Firmwareupdates wird der Reset ignoriert; anschließend neu halten. Prüfen: kurzer Druck bewirkt nichts, ein langer Druck löst einmal aus, Heimnetz/Sender/Klang bleiben erhalten.

Werkseinstellungen über dieselbe BOOT/IO0-Taste: Bei laufendem Radio mindestens 60 Sekunden halten und loslassen. Erst das Loslassen löst den vollständigen Reset aus. Heim-WLAN, Sender, Klang, Lautstärke und Setup-Passwort werden gelöscht; Firmware bleibt installiert, Radio startet neu. Danach Erstzugang mit passwort und verpflichtender Änderung. Während Firmwareupdates werden Tastenresets ignoriert; Taste neu betätigen. Gerätetest: kurzer Druck ohne Wirkung, 10–59 s nur Passwort, ab 60 s vollständiger Reset. Vor dem Test Einstellungen sichern; Sicherung enthält keine Zugangspasswörter.
