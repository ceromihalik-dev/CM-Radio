# CM-Radio – Bugliste

Stand: **9. Oktober 2026 · v0.1.2 · Build 0a01**.

Status: **OFFEN** = ungelöst; **FIXED** = Korrektur implementiert, Gerätetest offen; **PASS** = Nutzer bestätigt Korrektur am Board; **WORKAROUND** = umgehbar, Verbesserung offen. Priorität P1 blockiert die Inbetriebnahme, P2 behindert die Nutzung, P3 verbessert Komfort/Diagnose.

## Übersicht

| ID | Thema | Priorität | Status | Ziel / Fix |
| --- | --- | --- | --- | --- |
| CMR-001 | WLAN-Suche: „WLAN-Suche konnte nicht starten“ | P1 | PASS | v0.1.2 · Build 0a01 |
| CMR-002 | USB-Update erreicht Downloadmodus nicht automatisch | P2 | WORKAROUND | Verbesserte Update-Hilfe, Ziel-Build noch nicht festgelegt |
| CMR-003 | Flashskript meldet fehlendes esptool nur als Prozessfehler | P3 | WORKAROUND | Verständlicher Hinweis zur Python-Umgebung, Ziel-Build noch nicht festgelegt |

Aktuell kein gemeldeter Fehler ohne nutzbare Umgehung. Offene Hardwaretests stehen im [TESTPLAN.md](TESTPLAN.md); sie sind keine bestätigten Bugs.

## CMR-001 – WLAN-Suche startet nicht

- **Gemeldet:** 09.10.2026, V0.1.2 vor Einführung der Buildkennung.
- **Symptom:** Einrichtungsseite meldet „WLAN-Suche konnte nicht starten“; keine Netzwerkliste.
- **Technische Einordnung:** Möglicher Konflikt mit laufenden Station-Verbindungsversuchen bzw. noch nicht abgeschlossener Vorbereitung des WLAN-Treibers. Der konkrete Treiberfehler wurde am Board nicht separat protokolliert.
- **Korrektur:** Build 0a01 pausiert Wiederverbindung während der Suche, beendet einen unvollständigen Verbindungsversuch, wartet vor dem Start und wiederholt abgelehnte Starts höchstens dreimal. Zeitlimit und Wiederherstellung sind vorgesehen.
- **Softwareprüfung:** Build PASS; Hosttests für Vorbereitung, doppelte Anfragen, Wiederholungen, Timeout, Wiederherstellung und millis-Überlauf PASS.
- **Boardabnahme:** Nutzer bestätigt am 09.10.2026: „wlan suche funktioniert jetzt.“
- **Status:** PASS. Bei erneutem Auftreten neuen Nachweis und betroffenen Build ergänzen.

## CMR-002 – Manueller Downloadmodus beim USB-Update

- **Gemeldet:** 09.10.2026; esptool an COM5 meldet „Wrong boot mode detected (0x13)“.
- **Einordnung:** Der automatische Wechsel in den Flashmodus gelang bei diesem Versuch nicht; Ursache der Reset-/Bootsteuerung noch nicht bestimmt.
- **Umgehung:** Bei „Connecting…“ IO0 gedrückt halten, RST kurz drücken, IO0 beim beginnenden Schreiben loslassen. Seriellen Monitor vorher schließen.
- **Nachweis:** Folgescreenshot zeigt geschriebenes Anwendungsimage und „Hash of data verified“.
- **Nächster Schritt:** Update-Hilfe/Fehlerausgabe verbessern; vor Änderungen am Resetverfahren Verhalten am gelieferten Board prüfen.
- **Status:** WORKAROUND; siehe RM-11. Kein vollständiger Softwarefix behauptet.

## CMR-003 – Python-Umgebung und esptool

- **Gemeldet:** 09.10.2026; esptool war in Python 3.14 installiert, Flashskript lief mit Python 3.13. Das Skript zeigte einen allgemeinen Prozessfehler.
- **Umgehung:** Installation und Start mit derselben Python-Version: `py -3.13 -m pip install esptool==4.8.1`; anschließend `py -3.13 flash.py --port COM5 --erase` ausschließlich zur Erstinstallation. Für Updates die Anleitung in ERSTSTART verwenden.
- **Nachweis:** Installation in Python 3.13 und anschließendes Flashen erfolgreich.
- **Nächster Schritt:** Fehlendes esptool vorab verständlich melden und Ausgabe fehlgeschlagener Geräteprüfungen sichtbar machen.
- **Status:** WORKAROUND; siehe RM-11.

## Neue Meldungen

Je Meldung nächste freie CMR-ID, Datum, Version/Build, erwartetes und tatsächliches Verhalten, Reproduktionsschritte, Priorität, Status und Abnahmekriterium ergänzen. Keine WLAN-Passwörter oder unverdeckten Setup-Passwörter veröffentlichen. Für öffentliche Nachweise Geräte-/Netzwerkdaten auf das notwendige Maß beschränken.
