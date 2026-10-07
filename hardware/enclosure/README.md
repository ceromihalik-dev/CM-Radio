# CM-Radio – Gehäuse V0.1

Wandgehäuse für Loud-ESP32 / ESP32-WROVER, mit CM-Radio-Schriftzug und zwei rückseitigen Schlüssellochaufnahmen. Maße und Montage stehen in `CM-Radio_Druckanleitung_V0.1.pdf`. Die tatsächliche Boardpassung ist noch zu prüfen.

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
