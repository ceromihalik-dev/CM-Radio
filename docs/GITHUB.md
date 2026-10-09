# Öffentliche Entwicklung auf GitHub

Repository: **[ceromihalik-dev/CM-Radio](https://github.com/ceromihalik-dev/CM-Radio)**, **Public**, Standardbranch **main**. Dieses Projekt enthält Firmware, Bedienoberfläche, lokale API, Hardware-Referenzen, Tests und GitHub Actions. Keine WLAN-Konfiguration oder Zugangsdaten einchecken.

## Lokale Entwicklung

Den öffentlichen Quellstand klonen und Änderungen auf einem eigenen Branch entwickeln:

```sh
git clone https://github.com/ceromihalik-dev/CM-Radio.git
cd CM-Radio
git switch -c feature/meine-aenderung
```

Build und Tests stehen in der README. Änderungen anschließend auf dem eigenen Branch pushen und als Pull Request nach `main` übernehmen.

## Build und Release

GitHub Actions muss den Workflow `Firmware` ausführen. Der Build erzeugt ein herunterladbares `CM-Radio-WROVER-V0.1.1`-Artefakt. Erst nach erfolgreichem Workflow einen passenden Tag setzen, zum Beispiel `v0.1.1`; der Tag-Workflow baut erneut und erstellt automatisch einen öffentlichen Release mit dem Flashpaket.

```sh
git tag v0.1.1
git push origin v0.1.1
```

Der erste Release bleibt ausdrücklich als **Build-geprüft, Hardwaretests ausstehend** gekennzeichnet. Die Abnahme wird anschließend mit Platinenrevision und Testdatum ergänzt. Für Änderungen Branch und Pull Request verwenden; `main` muss kompilieren. Spätere Versionswechsel benötigen eine passende Versionsanpassung in BoardConfig, Paketierung und Workflow.

Der Workflow kann auch unter Actions → Firmware → Run workflow manuell gestartet werden. Ein grüner Build ersetzt die physische Board-Abnahme nicht.
