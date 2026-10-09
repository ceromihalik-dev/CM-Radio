# CM-Radio – Gehäuse V0.1 / W2

Wandgehäuse für Loud-ESP32 / ESP32-WROVER, mit CM-Radio-Schriftzug und zwei rückseitigen Schlüssellochaufnahmen. Maße und Montage stehen in `CM-Radio_Druckanleitung_V0.1.pdf`. Revision E3, Platine 85 × 56 mm und Lochraster 58 × 49 mm wurden am gelieferten Board bestätigt. Die tatsächliche Druckpassung ist noch zu prüfen.

Aktuelle Messwerte: `MESSWERTE_E3_W2.txt`. Die PDF-Anleitung und Vorschau dokumentieren W1; das Messblatt aktualisiert die dort noch offenen Maße. Die STL-/STEP-Dateien wurden für W2 neu erzeugt.

Die exportierten Modelle liegen im Repository verlustfrei komprimiert: `STL/*.stl.zip` und `STEP/*.step.zip`. Größere Archive bestehen aus den Teilen `.zip.001` und `.zip.002` bzw. `.zip.003`. Das folgende Skript fügt die Teile zusammen, prüft die Archive und entpackt alle Modelle. Die Prüfsummen in `Dateiliste.json` beziehen sich auf die entpackten STL-/STEP-Dateien.

Alle Archive im jeweiligen Unterordner entpacken, vom Projekt-Hauptordner aus:

```sh
python hardware/enclosure/extract_models.py
```

Die Modelle können auch neu aus dem parametrischen Quelltext erzeugt werden:

```sh
python -m pip install -r hardware/enclosure/requirements.txt
python hardware/enclosure/CM-Radio_Gehaeuse.py
```

Die Erzeugung schreibt die unkomprimierten Modelle in `STL` und `STEP`. Wandbefestigung: 60 mm Schraubenabstand, etwa 7 mm nach unten einhängen. Anschlüsse und Platinenhöhen am gelieferten Board prüfen; zuerst Lochraster-Probe drucken.
