"""Generate the current three-page R8 explosion/BOM/material PDF from CAD."""
from pathlib import Path
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader

PDF_NAME = 'CM-Radio_Retro_R8_Explosion_Materialliste.pdf'
ROWS = [
    ['A','4','M3 × 8 mm','90° Senkkopf; Kopf-Ø ≤ 5,6 mm. Länge einschließlich Kopf.','Deckel'],
    ['B','4','M2 × 6 mm','Linsen-/Flachrundkopf; Kopf-Ø ≤ 3,8 mm. Länge unter Kopf.','Platine'],
    ['C','2','M2 × 6 mm','Kopf-Ø ≤ 3,8 mm; Kopfhöhe ≤ 1,5 mm. Länge unter Kopf.','Reset-Halteplatte'],
    ['D','4','ruthex RX-M3Sx4.0 SHORT','M3-Messing; Länge 4,0 mm; außen Ø 4,6 mm. R8-Aufnahme Ø 4,0 × 6,0 mm.','Unterteil / Deckel'],
    ['E','4','ruthex RX-M2x4','M2-Messing; Länge 4,0 mm; außen Ø 3,6 mm. R8-Aufnahme Ø 3,2 × 5,0 mm.','Unterteil / Platine'],
    ['F','2','ruthex RX-M2x4','M2-Messing; Länge 4,0 mm; außen Ø 3,6 mm. R8-Aufnahme Ø 3,2 × 5,0 mm.','Deckel / Reset']]


def create(root):
    root = Path(root)
    font = Path('/usr/share/fonts/truetype/dejavu')
    pdfmetrics.registerFont(TTFont('CM', str(font/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('CM-Bold', str(font/'DejaVuSans-Bold.ttf')))
    ink = colors.HexColor('#193436')
    accent = colors.HexColor('#48646d')
    body = ParagraphStyle('body', fontName='CM', fontSize=8.5, leading=12, textColor=ink)
    small = ParagraphStyle('small', parent=body, fontSize=7.6, leading=10.5)
    bold = ParagraphStyle('bold', parent=body, fontName='CM-Bold')
    c = canvas.Canvas(str(root/PDF_NAME), pagesize=A4, invariant=1)
    c.setTitle('CM-Radio Retro R8 - Explosion, Materialliste und Resin-Hinweis')
    c.setAuthor('CM-Radio')

    def text(y, s, size=11):
        c.setFont('CM-Bold', size)
        c.setFillColor(ink)
        c.drawString(15*mm, y*mm, s)

    def para(y, s, style=body):
        p = Paragraph(s, style)
        _, h = p.wrap(180*mm, 1000)
        assert y-h/mm > 22, ('PDF overflow', y, h/mm)
        p.drawOn(c, 15*mm, y*mm-h)
        return y-h/mm-7

    def header(title, sub):
        text(282, 'CM-Radio | Retro V0.3 R8', 10)
        text(269, title, 19)
        para(261, sub, small)

    def footer(n):
        c.setStrokeColor(colors.HexColor('#d8e0e2'))
        c.line(15*mm, 17*mm, 195*mm, 17*mm)
        c.setFont('CM', 7)
        c.setFillColor(accent)
        c.drawString(15*mm, 11*mm, 'Stand 11.10.2026 | Ohne Display | CAD geprüft; physische R8-Abnahme offen')
        c.drawString(184*mm, 11*mm, f'{n}/3')
        c.showPage()

    def table(y, headings, rows, widths):
        data = [[Paragraph(x, bold) for x in headings]]
        data += [[Paragraph(x, small) for x in r] for r in rows]
        t = Table(data, colWidths=[x*mm for x in widths])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1ecee')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),8), ('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8f8')]),
            ('LINEBELOW',(0,0),(-1,0),.6,accent)]))
        _, h = t.wrap(180*mm, 1000)
        assert y-h/mm > 22
        t.drawOn(c, 15*mm, y*mm-h)
        return y-h/mm-10

    header('Explosionszeichnung', '104 × 80 × 36 mm | 5 Druckteile | Front zum Aufkleben')
    c.drawImage(str(root/'CM-Radio_Retro_R8_Explosionszeichnung.png'), 15*mm, 39*mm,
                width=180*mm, height=216*mm, preserveAspectRatio=True, mask='auto')
    para(32, 'Resetknopf von <b>innen</b> einsetzen. Front: 0,2 mm Klebeschicht; Führung kleberfrei. '
         '<b>Resin-Montagehinweis auf Seite 2 und 3 beachten.</b>', small)
    footer(1)

    header('Schrauben und Gewindeeinsätze', 'Referenzhardware der unveränderten R8-Geometrie - Resin-Montage noch anzupassen')
    y = table(249, ['Bild','Stk.','Teil','Ausführung / Maße','Einbauort'], ROWS, [11,12,41,77,39])
    text(y, 'Einkauf zusammengefasst'); y -= 7
    y = para(y, '<b>4 × M3-Senkschraube 8 mm + 6 × M2-Schraube 6 mm</b><br/>'
             '<b>4 × M3-SHORT-Einsatz + 6 × M2-Einsatz</b><br/>'
             '10 Schrauben und 10 Messinggewinde; keine Frontschrauben. '
             'Alle M2-Schrauben können mit Kopfhöhe ≤ 1,5 mm gewählt werden.')
    text(y, 'Bei Resin: keine thermische Montage'); y -= 7
    y = para(y, '<b>Keinen Lötkolben und kein gewaltsames Einpressen verwenden.</b> '
             'Die R8-Pilotbohrungen sind kleiner als die Einsatzaußendurchmesser. '
             'Für Klebemontage müssen die Aufnahmen an reale Einsätze und Klebstoff angepasst '
             'und zuerst am Muster geprüft werden. Dieses Release enthält keine dafür '
             'angepassten Bohrungen. Thermische Montage gilt nur für geeigneten Thermoplast.')
    text(y, 'Zusätzlich für die Montage'); y -= 7
    y = para(y, 'Zum tatsächlichen Material passender Frontkleber; Klebeschicht nominal 0,2 mm. '
             'Zwei Kabelbinder für Ösentunnel 3,2 × 2,0 mm. '
             'Zwei separate Wandschrauben: Schaft Ø 3,5-4,0 mm, Kopf Ø ≤ 8 mm, Höhe ≤ 3 mm. '
             'Länge und Dübel nach Wandaufbau wählen. '
             'Optionale Einsatzprobe: zusätzlich zwei M2- und zwei M3-SHORT-Einsätze.')
    para(y, 'Einbaukoordinaten: RETRO_R8_MONTAGE.md. Aktuelle Resin-Anweisung: RESIN_HINWEIS_R8.md. '
         'Herstellerabmessungen: ruthex RX-M3Sx4.0 SHORT / RX-M2x4. '
         'CAD-Prüfung ersetzt keine Passungs- oder Festigkeitsprüfung am Druckmuster.', small)
    footer(2)

    header('Druckmaterialien und Resin-Fertigung', 'Nutzerentscheid 11.10.2026: alle fünf Gehäuseteile aus Resin')
    rows = [[part,'1','SLA Resin','Nach tatsächlichem Auftrag'] for part in
            ['Unterteil','Deckel','Fronteinsatz','Resetknopf','Reset-Halteplatte']]
    y = table(249, ['Druckteil','Menge','Verfahren / Material','Sorte / Farbe'], rows, [44,16,47,73])
    text(y, 'Materialwahl im Auftrag'); y -= 7
    y = para(y, 'Die konkrete Resin-Sorte und Farbe aller fünf Teile ist nicht bestätigt. '
             '<b>9600 Resin wird von JLC3DP in Mattweiß angeboten.</b> '
             'Andere Resin-Sorten können andere Eigenschaften und Farben besitzen. '
             'Die grauschwarz/weißen Vorschaubilder zeigen die bisherige Gestaltung; '
             'sie bestätigen keine Auftragsfarbe. Die frühere Nylon-Auslegung bleibt Referenz.')
    text(y, 'Bestellen und montieren'); y -= 7
    y = para(y, 'Je fünf Einzel-STLs oder fünf Einzel-STEPs, Menge 1 pro Teil, mm / 100 %. '
             'Baugruppen, Explosions-STEP und Hardware-Referenzen nicht drucken. '
             'Keinen Standard-Gewindeeinsatzservice bestellen. '
             'Zusätzliche Schleif-/Lackierbearbeitung nur nach Wunsch beauftragen.<br/>'
             '<b>Resin-Gewindeaufnahmen vor der Montage anpassen und am Muster prüfen.</b> '
             'Deckel, Reset und Front trocken prüfen; Einsatzhalt und Frontkleber testen. '
             'Eine physische R8-Abnahme liegt noch nicht vor.')
    text(y, 'Zollbeschreibung'); y -= 7
    y = para(y, '3D-printed resin (plastic) enclosure parts. No electronic components included.<br/>'
             'Deutsch: 3D-gedruckte Gehäuseteile aus Kunstharz (Kunststoff). '
             'Keine elektronischen Bauteile enthalten.')
    para(y, 'Quellen: jlc3dp.com/help/article/photosensitive-9600-resin<br/>'
         'formlabs.com/blog/adding-screw-threads-3d-printed-parts/<br/>'
         'Weitere Angaben: DRUCKMATERIALIEN_R8.md / RESIN_HINWEIS_R8.md.', small)
    footer(3)
    c.save()
    pages = PdfReader(root/PDF_NAME).pages
    assert len(pages) == 3
    content = '\n'.join(p.extract_text() for p in pages)
    for expected in ['Resin', 'keine thermische Montage', '10 Schrauben', 'SHORT', 'No electronic']:
        assert expected in content, expected
    with (root/'CM-Radio_Retro_R8_Materialliste.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['Bild','Menge','Teil','Ausführung / Maße','Einbauort'])
        w.writerows(ROWS)
    return root/PDF_NAME
