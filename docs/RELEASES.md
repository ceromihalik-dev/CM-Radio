# GitHub-Releases

Firmware-Releases stehen unter https://github.com/ceromihalik-dev/CM-Radio/releases zum Download.

Nach einem Push auf main oder einem manuellen Start des Firmware-Workflows erstellt GitHub erst nach erfolgreicher Kompilierung und Softwareprüfung ein Release. Version und Build werden aus manifest.json übernommen. Das Tagformat lautet v0.1.3-build09; der Download heißt CM-Radio_Firmware_v0.1.3_Build_09.zip.

Das ZIP enthält die Update-Dateien manifest.json und firmware.bin sowie die vollständige USB-Erstinstallationsanleitung USB_ERSTINSTALLATION.txt. Bestehende Releases werden nicht überschrieben. Für neue Firmware muss die Buildnummer erhöht werden; Dokumentationsänderungen erzeugen kein zusätzliches Release derselben Version.

Softwaretests und Geräteabnahme werden getrennt angegeben. Eine erfolgreiche GitHub-Kompilierung ersetzt keine Prüfung am Board.
