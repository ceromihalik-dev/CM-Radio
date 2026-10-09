# CM-Radio – Änderungen

## V0.1.2 – 9. Oktober 2026

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
