# CM-Radio Modell 3 Retro – V0.3 R5 Display

Stand 11.10.2026, mm, Maßstab 1:1 / 100 %. **Mechanischer Display-Prototyp**.
Die Kabelauslässe aus R4 wurden vom Anwender mit PASS bestätigt. Das Unterteil
bleibt gegenüber R4 unverändert. R5-Displaypassung und Elektrik sind noch nicht
am tatsächlichen Modul getestet; keine endgültige Fertigungsfreigabe.

## Konstruktion

- Außenmaße 104×80×36 mm, keine sichtbare Versionsnummer.
- Sechs Druckteile: Unterteil, Deckel, Fronteinsatz, Resetknopf,
  Reset-Halteplatte und neuer Displayhalter.
- Das Panel sitzt links im neuen 90×42×3-mm-Fronteinsatz. Schriftzug und
  Radiozeichen liegen rechts. Acht Retro-Rippen bleiben erhalten; zwei Rippen
  entfallen zugunsten der größeren Front. Die Front bleibt ein Klebeeinsatz.
- Panelreferenz 34,5×23×1,4 mm, Mitte X=25,5 / Y=29,5 mm. Blickrichtung nach +Z,
  Anschlussfahne nach +Y zur oberen Platinenkante. Gegenüber der Datenblatt-
  Frontansicht um 180° gedreht; spätere Software muss dies berücksichtigen.
- Paneltasche 35,7×24,2 mm, nominal 0,6 mm Spiel je Seite. Die Zeichnung nennt
  ±0,2 mm für die Panelkanten und ±0,1 mm für die Dicke.
- Sichtfenster 31,8×17,1 mm, Eckenradius 0,6 mm, abgesetzter größerer Mund an
  der Front. Referenz der aktiven Fläche: 29,42×14,7 mm, Mitte X=25,5/Y=27,45.
  Der Versatz stammt aus der Maßzeichnung (2,1 mm vom gegenüberliegenden
  Panelrand zur aktiven Fläche); nicht einfach Panelmitte gleich Bildmitte setzen.
- Paneloberfläche Z=32,8, Rückseite Z=31,4. Es liegt 3,2 mm hinter der Front.
  Der rückseitige U-Halter endet Z=30,6 und trägt weiche Randpolster ca. 0,8 mm.
  Zum Fronteinsatz bleibt nominal 0,2 mm Abstand; **Glas nicht verspannen**.
- Zwei Halterschrauben bei X=12,5/38,5, Y=13 mm. Durchgang Ø2,9 mm, gedruckter
  Pilot Ø2 mm, Tiefe 2,1 mm. Ausgangswert 2,5×4 mm Kunststoffschrauben;
  Länge und Gewindeeingriff am gefertigten Teil prüfen, kein Durchschrauben.
- Deckelrecess für Halter lässt nominal mindestens 2,1 mm Dachstärke im
  überdeckten Bereich; Fronteinsatz separat 3 mm. Keine behauptete komplette
  Wandstärken- oder Fertigungsfreigabe.
- Resetmechanik bleibt an den gemessenen IO0-Koordinaten. Neuer Deckel und
  Fronteinsatz benötigen den vorhandenen Retro-Resetknopf, nicht W4/W5-Knöpfe.

## Wichtig: Das Datenblatt ist eine andere Anschlussvariante

Die vom Anwender verlinkte SparkFun-Zeichnung QG-2864KSWLG01 A / QT1106P07
zeigt **30 Kontakte im 0,7-mm-Raster** mit 22 mm breitem Kontaktende.
Elecrow/Sonocotta nennt für das zuvor gewählte Modul **30 Kontakte im 0,5-mm-
Raster**. Der E3-Gerber bestätigt 0,5 mm. Diese Varianten sind nicht direkt
steckbar. Die verwendeten Panelabmessungen sind die konkrete CAD-Auslegungsbasis;
identische Abmessungen des Elecrow-Moduls wurden dadurch NICHT nachgewiesen.

Die Gesamtprojektion in der Zeichnung beträgt 35 mm bei 23 mm Panelhöhe,
entsprechend ca. 12 mm überstehender Flexfahne. Bereits die Höhenüberbrückung
vom Panel zum Board ist größer. Deshalb kann diese kurze Fahne den gezeichneten
Deckel-zu-Platine-Weg **nicht direkt** überbrücken.

**Elecrow-Modul:** Der Anwender hat ca. **50 mm reine Kabellänge ab Modul**
bestätigt. Gegenüber dem etwa 26-mm-Referenzweg bleiben nominal ca. 24 mm
für Bögen und Lageanpassung. Eine Verlängerung ist voraussichtlich nicht nötig;
noch kein Nachweis der realen Einstecktiefe, Steckerkante oder des Biegeradius.
Elecrow-0,5-mm-Modul am passenden 0,5-mm-Boardanschluss verwenden und
Kontaktseite kontrollieren. Die kurze 0,7-mm-Fahne der SparkFun-Zeichnung ist
NICHT die tatsächliche Elecrow-Fahne; die Zeichnung dient als Panelreferenz.

Nur für genau dieses andere Datenblattmodul braucht es eine elektrisch geprüfte Adapterlösung
mit Verlängerung; Pinbelegung, Kontaktseite, Raster und zusätzliche Bauteile
müssen anhand der tatsächlichen Hardware bestätigt werden. Diese Adapterplatine
ist NICHT entworfen, nicht mitgeliefert und im CAD nicht als reale Hardware
modelliert. Für das tatsächlich gewählte Elecrow-Modul ist die vom Anwender bestätigte
50-mm-Fahne die Auslegungsgrundlage; eine solche Adapterplatine ist dafür
nicht vorgesehen.
Kein beliebiges 30-poliges FFC-Kabel bestellen oder ungeprüft einstecken.

## Flexkabel und Deckel öffnen

Der nach oben offene 24-mm-Ausgang lässt das Kabel ohne Klemmung aus dem
Panelbereich austreten. Danach nach links an der Reset-Halteplatte vorbei
zum OLED-Stecker führen. Der orange Referenzkörper ist ein **geplanter freier
Korridor**, kein Modell eines konkreten Kabels und kein nachgewiesener Biegeradius:
16 mm breit im Verlauf, am Anschlussende auf 22 mm erweitert, 0,6 mm dick.
Die Referenz hat ca. 26 mm Mittellinienweg; genauen Wert im Prüfbericht lesen.
Dieser Wert ist **keine bestellbare Kabellänge**: Einstecktiefe, echte Anschluss-
position, weiche Bögen, Adapter und Service-Schlaufe kommen hinzu.

Die Lötpadreihe liegt im Gehäuse bei ca. X=26,646/Y=50,524. Z=13,1 mm für den
Korridor-Endpunkt ist eine Planungsannahme und NICHT die gemessene Steckerhöhe.
Der zulässige Biegeradius steht nicht in der Zeichnung; keine harte 180°-Falte,
kein Knicken am Panelansatz oder am Kontaktende. Das tatsächliche Kabel muss
in der Passprobe spannungsfrei bleiben und außerhalb der Resetbewegung liegen.

Zum Öffnen den Deckel nur wenige Millimeter anheben, Kabelzug vermeiden und
zuerst die Steckverbindung entriegeln. Der Deckel darf nicht frei am Flex hängen.
Das Gehäuse ist weiterhin belüftet und hat keine IP-Schutzfreigabe.
Für den Badeinsatz eine transparente Abdeckung vor dem Display einplanen,
falls Spritzer/Kondensat auftreten; Fenster und Gehäuse sind nicht abgedichtet.

## Erstmontage und Prüfablauf

1. Zunächst nur neuen Deckel, Fronteinsatz und Displayhalter als Passprobe
   drucken. R4-Unterteil, Resetknopf und Reset-Halteplatte weiterverwenden.
   Alternativ alle sechs Teile einmal aus STL_DRUCK bestellen/drucken.
2. Tatsächliches Panel und Flex vermessen. Panel muss ohne Druck in die Tasche
   passen; aktive Fläche muss vollständig sichtbar sein. Einsteckkontakt und
   tatsächliche Anschlusshöhe des Boards prüfen. 0,7/0,5-mm-Abweichung lösen.
3. Strom trennen. Panel von innen mit der Fahne nach +Y einsetzen. Kleine weiche,
   elektrisch isolierende Polster an den Glasrändern auf dem U-Halter setzen.
   Keine vollflächige Pressung auf Glas, Polarizer, IC oder Flexbond.
4. Halter anschrauben. 0,8 mm nominalen rückseitigen Spalt durch geeignete
   Randpolster überbrücken; weich fixieren, nicht zwischen Schrauben verspannen.
   Pilotlöcher bei Bedarf vor der Elektronikmontage nacharbeiten. Die Schraube
   darf nicht in die Frontfläche treten. Papier-/Kunststoff-Testpanel zuerst.
5. Reset und Halteplatte montieren, Freigängigkeit mit unbetätigter und gedrückter
   Taste testen. Tatsächliches Flexkabel mit weichem Bogen seitlich verlegen;
   kein Kontakt zu Bauteilen, Schrauben, Taster oder scharfen Druckkanten.
6. Fronteinsatz erst nach Fenster-/Panelprobe mit geeigneter dünner Klebefolie
   befestigen. Nominal 0,2 mm Klebespalt. Keine Kleber-/Lackreste im Displayfach.
7. Deckel vorsichtig schließen und erneut öffnen. Kabel muss spannungsfrei
   bleiben. USB, Ton, IR, Reset und Wandmontage prüfen.
8. Eine Bildanzeige benötigt eine separate Firmwareerweiterung. In dieser
   Lieferung ist keine OLED-Firmware enthalten. Vorschautext ist Platzhalter.

## Drucken, JLC3DP und Autodesk Fusion

Auslegung wie R4: Nylon SLS/MJF, bisheriges Materialziel 3301PA weiß,
außen Salbeigrün matt RAL 6021, Fronteinsatz Elfenbein RAL 1015.
Führung, Displaytasche, Klebesitz und Piloten nicht lackieren. Maße und
Oberflächenauftrag durch Fertiger prüfen lassen. Glas und Drucktoleranzen
machen einen kleinen Passdruck vor der Bestellung sinnvoll.

FDM: nicht skalieren; Unterteil und Halter mit flacher Unterseite aufs Bett.
Deckel/Fronteinsatz in Montageorientierung Front oben, Slicer-Stützen/Brim
für Rückseitenkonturen berücksichtigen. Die Dateien beginnen jeweils bei Z=0.
Stützreste vollständig aus Displayfach, Piloten und Resetführung entfernen.
Die geschlossene R4-Kabelbohrung und USB-/IR-Geometrie bleiben unverändert.

STEP_EINZELTEILE sind bearbeitbare Volumenkörper. Die Baugruppe enthält nur
Druckteile. EINBAUPRUEFUNG_REFERENZEN_NICHT_DRUCKEN.step enthält zusätzlich
Panel, aktive Fläche, PCB und orange Kabelraumreferenz. Niemals die Baugruppen
oder die Referenzkörper als Druckteile bestellen. STEP bietet keine native
Fusion-Zeitleiste; nach Import Einheiten mm prüfen und als Fusion-Entwurf speichern.

## Nachweise und Reproduktion

Geschlossene Einzelkörper, wasserdichte STLs, STEP-Reimport, alle 15 Druckteil-
Paarungen, Display mit Maßtoleranzen, gedrückter Reset und Kabelraum geprüft.
STEP-Heilung verändert das Deckelvolumen geringfügig; Fehler wird im Bericht
quantifiziert, Obergrenze 0,01 %. Diese Prüfungen ersetzen keine echte Passprobe.
Unterseiten-/Oberseitenbauteile und Adapter sind nicht vollständig modelliert.

```sh
python -m pip install -r requirements.txt
python designs/make_retro_display.py ../NEU_EXPORT
python designs/check_retro_display_step.py ../NEU_EXPORT
python designs/render_retro_display.py ../NEU_EXPORT
```

Quellen (11.10.2026):
- https://cdn.sparkfun.com/assets/2/6/8/9/7/1.3inch-SH1106-OLED_Datasheet.pdf
- https://www.elecrow.com/ssh1106-30-pin-oled-module.html
- https://github.com/sonocotta/esp32-audio-dock
