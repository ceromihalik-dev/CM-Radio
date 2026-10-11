"""Actual STEP previews and an insert-position drawing for Retro R7."""
from pathlib import Path
from types import SimpleNamespace
import argparse,json
import numpy as np
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont
from render_retro_r3_details import view


def render(root):
    root=Path(root)/'Retro'
    a=cq.Assembly.importStep(str(root/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    p=json.loads((root/'parameter.json').read_text())
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=lambda s:ImageFont.truetype(font,s)
    # Show both front clamp strips and the actual reset retainer from behind.
    inside=[]
    for n in a.children:
        if n.name=='Unterteil':continue
        color=cq.Color(.48,.49,.50) if n.name.startswith('Front_Halter') else n.color
        inside.append(SimpleNamespace(name=n.name+'_visible',obj=n.obj,color=color))
    image=Image.new('RGB',(1860,1100),'#f7f7f7');d=ImageDraw.Draw(image)
    d.text((40,24),'CM-Radio Retro | V0.3 R7 ohne Display',font=f(36),fill='#172929')
    d.text((40,77),'JLC3DP: Grauschwarz / Weiß · Gesamtbreite mit Schutzhauben 114 mm',font=f(24),fill='#45615a')
    image.paste(view(a.children,58,-70),(20,115))
    image.paste(view(inside,-65,-70),(940,115))
    d.text((60,915),'Seitliche Schutzhauben mit Öffnung nach unten',font=f(24),fill='#172929')
    d.text((980,915),'Front von innen mit zwei verdeckten Haltebügeln',font=f(23),fill='#172929')
    d.text((60,970),'12 Messingeinsätze · Front austauschbar · Keine Klebung des Fronteinsatzes',font=f(27),fill='#172929')
    d.text((60,1020),'CAD-Geometrie geprüft · Druckpassung, Einsatzhalt und Temperatur am Muster prüfen',font=f(24),fill='#45615a')
    image.save(root/'CAD_Vorschau_R7.png')
    # Print/install coordinate drawing. Base print origin is +5 mm in X
    # because the left hood extends to assembly X=-5. Lid origin stays X=0.
    image=Image.new('RGB',(1860,1150),'#f7f7f7');d=ImageDraw.Draw(image)
    d.text((40,24),'CM-Radio R7 | Einsetzplan für 12 Messinggewinde',font=f(34),fill='#172929')
    d.text((40,76),'Eigenmontage nach dem Druck; kein Auftrag für JLC3DPs Standard-Einsatzservice',font=f(23),fill='#45615a')
    image.paste(view([n for n in a.children if n.name=='Unterteil'],90,-90),(20,135))
    image.paste(view([n for n in a.children if n.name=='Deckel'],-90,-90),(940,135))
    def project(x,y,z,elev,ox):
        e,az=np.deg2rad([elev,-90]);cam=np.array([np.cos(e)*np.cos(az),np.cos(e)*np.sin(az),np.sin(e)])
        right=np.array([-np.sin(az),np.cos(az),0]);up=np.cross(cam,right)
        v=np.array([x,y,z])-np.array([52,40,18])
        return ox+450+float(v@right)*6.3,135+400-float(v@up)*6.3
    for j in p['insert_joints']:
        x,y=j['xy'];isbase=j['part']=='Unterteil'
        px,py=project(x,y,j['opening_z'],90 if isbase else -90,20 if isbase else 940)
        color='#c99424' if j['model']=='M3' else '#c15d32'
        d.ellipse((px-12,py-12,px+12,py+12),outline=color,width=4)
        tx,ty=px+16,py-12
        if j['model']=='M3' and x<10:tx=px-52
        if j['joint']=='Reset':tx,ty=px-16,py+16
        d.text((tx,ty),j['model'],font=f(19),fill=color)
    d.text((60,925),'Unterteil: 4 × M3 SHORT + 4 × M2',font=f(25),fill='#172929')
    d.text((980,925),'Deckel: 2 × M2 Reset + 2 × M2 Front',font=f(25),fill='#172929')
    d.text((60,980),'M3: ruthex RX-M3Sx4.0 · Bohrung Ø 4,0 × 6 mm',font=f(25),fill='#976c19')
    d.text((60,1025),'M2: ruthex RX-M2x4 · Bohrung Ø 3,2 × 5 mm',font=f(25),fill='#97411a')
    d.text((60,1070),'Lagekoordinaten und Schraubenlängen: RETRO_R7_MONTAGE.md · Bohrungen vor Einsetzen prüfen',font=f(22),fill='#45615a')
    image.save(root/'Gewindeeinsaetze_Einsetzplan_R7.png')
    print('R7 Vorschau und Einsetzplan aus STEP gerendert',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();render(args.root)
