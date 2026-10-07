# CM-Radio – nächste Entwicklungsschritte

1. **V0.1.0:** USB-Installation, WLAN, MP3/AAC, Stereo, NVS, Autostart, Weboberfläche und lokale API. Build prüfen, dann Hardware-Abnahme nach `TESTPLAN.md`.
2. **V0.1.1:** Fehler aus realem Boardtest beheben, bestätigte PCB-Revision dokumentieren, Audio- und Wiederanlaufverhalten stabilisieren.
3. **V0.2:** Radio-Browser-Sendersuche und Favoriten ergänzen; Suchdienstausfälle sollen bestehende Sender nicht blockieren.
4. **Danach Android-App:** An die vorhandene `/api/v1`-Schnittstelle anbinden, Geräte-IP/mDNS-Erkennung und Bedienung im WLAN. Browser bleibt als Einrichtung und Rückweg verfügbar.
5. **Später:** Lokal abgesicherte OTA-Updates und weitere Funktionen anhand tatsächlicher Nutzung. Der zweite Anwendungsslot ist bereits reserviert.

Neue Arbeiten als fokussierte GitHub-Issues und Änderungen über Branches/Pull Requests nachvollziehbar halten. `main` muss kompilieren. Ein Release darf nur als „hardwaregetestet“ bezeichnet werden, wenn der zugehörige Testplan ausgefüllt ist.
