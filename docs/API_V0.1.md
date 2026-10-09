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
