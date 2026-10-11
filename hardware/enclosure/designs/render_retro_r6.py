"""Render actual exported R6 STEP; no conceptual image geometry."""
import argparse
import json
from pathlib import Path
import numpy as np
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont
from render_retro_r3_details import view


def render(root):
    root=Path(root)/'Retro'
    a=cq.Assembly.importStep(str(root/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    p=json.loads((root/'parameter.json').read_text())
    image=Image.new('RGB',(1860,1100),'#f7f7f7');d=ImageDraw.Draw(image)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f=lambda s:ImageFont.truetype(font,s)
    d.text((40,24),'CM-Radio Retro | V0.3 R6 ohne Display',font=f(36),fill='#172929')
    d.text((40,76),'104 × 80 × 36 mm · Vorschau aus den geprüften CAD-Dateien',font=f(24),fill='#45615a')
    image.paste(view(a.children,58,-70),(20,115))
    image.paste(view([n for n in a.children if n.name=='Deckel'],-65,-70),(940,115))
    e,az=np.deg2rad([-65,-70])
    cam=np.array([np.cos(e)*np.cos(az),np.cos(e)*np.sin(az),np.sin(e)])
    right=np.array([-np.sin(az),np.cos(az),0]);up=np.cross(cam,right)
    rx=p['board_offset_x']+p['reset_x_from_board_left']
    ry=p['board_offset_y']+p['reset_y_from_board_front']
    z=p['reset_collar_top_z']-p['reset_collar_thickness']-p['reset_stroke']
    for x in (rx-10,rx+10):
        v=np.array([x,ry,z])-np.array([52,40,18])
        px=940+450+float(v@right)*6.3;py=115+400-float(v@up)*6.3
        d.ellipse((px-15,py-15,px+15,py+15),outline='#c75a21',width=4)
        d.line((1460,810,px,py+15),fill='#c75a21',width=3)
    d.text((60,915),'Front: zehn runde Rippen und separater Einsatz',font=f(24),fill='#172929')
    d.text((980,835),'Reset-Kernlöcher Ø 2,0 × 5,0 mm',font=f(23),fill='#97411a')
    d.text((980,915),'Deckel von innen, Knopf / Halteplatte ausgeblendet',font=f(22),fill='#172929')
    d.text((60,970),'PCB: Ø 2,0 × 5 mm   |   Deckel: Ø 2,5 × 6 mm → M3 schneiden',font=f(27),fill='#172929')
    d.text((60,1020),'Farben als Vorschlag: Salbeigrün matt / Elfenbein · Druckpassung am Muster prüfen',font=f(24),fill='#45615a')
    image.save(root/'CAD_Vorschau_R6.png')
    print('Retro R6 CAD-Vorschau gerendert',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();render(args.root)
