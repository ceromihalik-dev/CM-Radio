# CM-Radio-Firmwarekonzept V0.1

**Datum:** 7. Oktober 2026 · **Firmware:** 0.1.0 · **Ziel:** Nach Eintreffen des Boards über USB installieren, WLAN einrichten und die beiden Lautsprecher testen.

## Verbindliche Ausgangsbasis

Elecrow/Sonocotta Loud-ESP32, ESP32-WROVER-N8R8, 8 MB physischer Flash und 8 MB physische PSRAM, USB-C, zwei integrierte MAX98357-I²S-Verstärker. Zwei vorhandene Deckenlautsprecher mit je 3 W / 8 Ω. WLAN-Internetradio, Android-Steuerung, automatischer Start nach Einschalten, kein weiteres Audio- oder Verstärkermodul. Frühere ATOMS3R-Pläne sind ersetzt.

Die Gehäuse-Rückseite besitzt die bereits geplante Wandbefestigung mit zwei Schlüssellochaufnahmen. Die Firmware benötigt weder Display noch zusätzliche Gehäusetasten. USB-C bleibt für Erstinstallation und Diagnose zugänglich.

## Technische Entscheidung

PlatformIO Core **6.1.18**, Espressif32-Plattform **6.9.0**, Arduino-ESP32 **2.0.17**, Frameworkpaket **3.20017.241212+sha.dcc1105b**, ESP32-audioI2S **Git-Tag 3.0.12**, ArduinoJson **6.21.5**. Diese Kombination wird bewusst gemeinsam festgelegt; ein Upgrade einer einzelnen Audio-/Framework-Komponente wird erst nach neuem Build und Gerätetest übernommen.

Das generische `esp-wrover-kit`-Profil liefert die klassische ESP32-/PSRAM-Toolchain. Die CM-Radio-Pins und 8-MB-Partitionen überschreiben die entscheidenden Werte; die Platine ist kein Espressif-Entwicklungsdisplay. GPIO 16/17 bleiben für PSRAM reserviert. Ein ESP32-S3 ist ein anderes Ziel und wird von diesem Firmwarepaket ausgeschlossen.

| Funktion | GPIO |
| --- | --- |
| I²S BCLK | 26 |
| I²S LRCLK / WS | 25 |
| I²S DATA | 22 |
| Verstärkerfreigabe | 13, HIGH aktiv |

Die Zuordnung folgt der Herstellerdokumentation. Die konkrete Platinenrevision und Freigabepolarität werden beim ersten Hardwaretest gegengeprüft. Das Board bestimmt die Links-/Rechts-Zuordnung der beiden Verstärker; die Firmware gibt Stereo aus und mischt nicht absichtlich auf Mono.

## Ablauf nach Stromzufuhr

1. Verstärkerfreigabe auf LOW, seriellen Monitor starten.
2. NVS-Konfiguration laden und Schema sowie Grenzen prüfen. Ohne gültigen Datensatz gelten ein Beispielstream, Lautstärke 5/21 und Autostart aktiv.
3. Tatsächliche Flashgröße und PSRAM prüfen. Bei unpassender Hardware bleibt Audio deaktiviert; die Weboberfläche zeigt den Diagnosezustand.
4. Audio-Task starten und den gewählten Sender anfordern, wenn Autostart aktiv ist.
5. WLAN ohne blockierende Warteschleife verbinden. Ohne gespeichertes WLAN sofort Setup-AP öffnen; bei Verbindungsproblemen nach 30 Sekunden.
6. Nach erfolgreicher WLAN-Verbindung Setup-AP schließen, mDNS `cm-radio.local` anbieten und angeforderten Stream wiedergeben.

Das Setup-WLAN `CM-Radio-XXXXXX` verwendet pro Neustart einen neuen zufälligen 16-stelligen Schlüssel. SSID und Schlüssel erscheinen ausschließlich im seriellen Monitor. Ein Captive-DNS erleichtert das Öffnen des Setups; `http://192.168.4.1` funktioniert als direkte Adresse.

## Komponenten und Zuständigkeiten

Der Arduino-Hauptloop auf Core 1 bedient HTTP, DNS, WLAN-Zustand und NVS. Ein eigener Audio-Task auf Core 0 besitzt das `Audio`-Objekt. HTTP-Handler übergeben ausschließlich feste Befehle über eine FreeRTOS-Queue. Ein geschützter Status-Snapshot überträgt Titel und Audiozustand zur API. Damit greift der Webserver nicht gleichzeitig auf den Decoder zu.

Die Audio-Queue ist auf acht Befehle begrenzt. Bei Überlast antwortet die API mit 503. Netzwerk-Verbindungsaufrufe der Bibliothek können die Audio-Task kurz blockieren; die Web-Task bleibt davon getrennt. Stoppen oder Senderwechsel kann deshalb während eines Verbindungsversuchs verzögert wirksam werden.

Der Stream wird nach Fehlern mit Wartezeiten 2, 4, 8, 16 und maximal 32 Sekunden erneut angefordert. Bei fehlendem WLAN wird stummgeschaltet und auf Netzrückkehr gewartet. Die API meldet `streaming`, wenn die Bibliothek einen aktiven Stream meldet; dies bestätigt noch keine tatsächlich hörbare Ausgabe.

## Persistenz

Ein JSON-Datensatz mit Schema 1 liegt im NVS-Namespace `cm-radio`, Schlüssel `config`. Gespeichert werden SSID und WLAN-Passwort, Senderliste, gewählter Sender, Lautstärke und Autostart. Die Browser-/Status-API liefert das WLAN-Passwort nicht zurück. Ein Speichervorgang ersetzt den gesamten Datensatz, sodass die NVS-Schlüssel nicht einzeln auseinanderlaufen.

Lautstärkeänderungen werden nach zwei Sekunden Ruhe gespeichert, um unnötige Flash-Schreibzyklen zu reduzieren. `settingsPending` zeigt diese Zeitspanne an. Stromausfall innerhalb dieser zwei Sekunden kann die letzte Änderung verlieren. Senderwechsel und andere Einstellungen werden direkt gespeichert; Speicherfehler erscheinen als API-Fehler bzw. Diagnose.

Stoppen beendet die aktuelle Wiedergabe, ändert aber die Autostart-Einstellung nicht. Bei erneuter Stromzufuhr wird deshalb wieder gestartet, sofern Autostart aktiv ist. Nach Entfernung des aktuellen Senders wird gestoppt und der erste verbleibende Sender als Startauswahl gespeichert.

## Bedienung und API

V0.1 wird auf Android im Browser bedient. Anzeige von Sender, Streamtitel, Verbindungszustand und Speicherstatus; Play/Stop; Lautstärke 0–21; bis zu zehn Sender hinzufügen/entfernen; WLAN konfigurieren; Autostart einstellen. Inhalte und JavaScript sind im Flash eingebettet, ohne CDN oder App-Store.

Die lokale API `/api/v1/` umfasst Status, Senderliste, Wiedergabe, Lautstärke, Konfiguration und WLAN. JSON-Schreibzugriffe prüfen Datentypen und Grenzwerte. Ein Browser-Origin-Test verhindert einfache fremde Webseitenzugriffe; es gibt keine Benutzeranmeldung. Der Einsatz ist für ein vertrauenswürdiges Heimnetz vorgesehen. CM-Radio betreibt weder Cloudkonto noch Fernzugriff.

Ein Sender benötigt eine direkte HTTP(S)-Stream-Adresse. MP3/AAC stehen im Ersttest im Vordergrund; weitere Bibliotheksformate und Playlisten werden erst nach Boardtests freigegeben. Die Bibliothek unterstützt HTTPS, prüft in diesem Stand Serverzertifikate jedoch nicht strikt. Der mitgelieferte Radio-Paradise-MP3-Stream ist ein austauschbarer Funktionstest und noch kein garantierter Lieblingssender.

## Flashlayout und Aktualisierung

| Bereich | Start | Größe |
| --- | --- | --- |
| NVS | 0x9000 | 20 KiB |
| OTA-Auswahl | 0xE000 | 8 KiB |
| Anwendung 0 | 0x10000 | 3 MiB |
| Anwendung 1 | 0x310000 | 3 MiB |
| Reserviertes Dateisystem | 0x610000 | 1984 KiB |

V0.1 flasht Anwendung 0 über USB. Anwendung 1 reserviert Platz für spätere OTA-Unterstützung; V0.1 enthält noch keinen OTA-Endpunkt. Das vollständige Erstinstallationsimage enthält Bootloader, Partitionstabelle, OTA-Auswahl und Anwendung. Erstinstallation löscht Werksfirmware und Einstellungen. Spätere USB-Updates verwenden PlatformIO mit dem unveränderten Layout und erhalten den NVS-Datensatz.

Bei klassischem ESP32 kann die zur Verfügung stehende PSRAM-Heapgröße kleiner als die physische 8-MB-Bestückung sein. Deshalb wird im Gerätetest PSRAM-Verfügbarkeit geprüft, nicht pauschal ein gemeldeter Heap von exakt 8 MB verlangt.

## Öffentliche Entwicklung und Abnahme

Repository: `ceromihalik-dev/CM-Radio`, öffentlich, Standardbranch `main`, GPL-3.0-or-later. GitHub Actions führt Host-Prüfungen aus, kompiliert die Firmware und stellt das Flashpaket als Build-Artefakt bereit. Tags `v*` erzeugen nach erfolgreichem Build einen Release. Konfigurationsdaten und Zugangsdaten bleiben außerhalb des Repositories.

Vor Freigabe als hardwaregetesteter Stand: Flash-/PSRAM-Erkennung, WLAN-Setup, beide Kanäle, Lautstärke, Play/Stop, Senderwechsel, Persistenz nach Neustart, Autostart, falsches WLAN-Passwort, Netzunterbrechung und mindestens 60 Minuten Dauerbetrieb. Erst danach folgt die Radio-Browser-Integration und anschließend die eigenständige Android-App. Die genaue Abnahme steht in `TESTPLAN.md`.

## Hersteller- und Abhängigkeitsquellen

- https://github.com/sonocotta/esp32-audio-dock — README, Abschnitt Loud-ESP32 / GPIOs.
- https://www.elecrow.com/loud-esp32.html — bestellte Boardfamilie.
- https://github.com/platformio/platform-espressif32/blob/v6.9.0/platform.json — Toolchainbasis.
- https://github.com/schreibfaul1/ESP32-audioI2S/tree/3.0.12 — Audiobibliothek und API.
- https://radioparadise.com/listen/stream-links — Beispielstream-Anbieter.
