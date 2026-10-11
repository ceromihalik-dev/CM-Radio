"""Render actual R5 CAD, with clearly labelled non-print OLED/FPC references."""
from pathlib import Path
from types import SimpleNamespace
import argparse,json
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont
from render_retro_r3_details import view
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();root=Path(args.root)/'Retro'
 ass=cq.Assembly.importStep(str(root/'EINBAUPRUEFUNG_REFERENZEN_NICHT_DRUCKEN.step'))
 f=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
 nodes=[n for n in ass.children if n.name not in ('FPC_Freiraum_Referenz','PCB_Referenz')]
 # Sample display text, only in the preview. No firmware functionality implied.
 for text,y,size in [('CM-Radio',31,3.5),('Display',25.5,2.6),('128 x 64',22,2.1)]:
  obj=cq.Workplane('XY').text(text,size,.02,font='DejaVu Sans',kind='bold',combine=False).translate((25.5,y,32.85))
  nodes.append(SimpleNamespace(name='Vorschau_Text',obj=obj,color=cq.Color(.7,.91,.93)))
 back=[]
 for n in ass.children:
  if n.name in ('Unterteil','PCB_Referenz','Fronteinsatz','OLED_Aktivflaeche_Referenz'):continue
  back.append(SimpleNamespace(name='Resetplatte' if n.name=='Reset_Halteplatte' else n.name,obj=n.obj,color=n.color))
 im=Image.new('RGB',(1860,1060),'#f7f7f7');d=ImageDraw.Draw(im)
 d.text((40,25),'CM-Radio Retro V0.3 R5 | Display im Deckel',font=f(36),fill='#172929')
 im.paste(view(nodes,70,-90),(20,95));im.paste(view(back,-75,-90),(940,95))
 d.text((50,875),'Front mit Displayfenster und neuem Fronteinsatz',font=f(24),fill='#172929')
 d.text((970,875),'Deckel von innen: Halter, Reset und Kabelraum',font=f(24),fill='#172929')
 d.text((50,930),'Panel 34,5 × 23 × 1,4 mm | Fenster 31,8 × 17,1 mm | Gehäuse 104 × 80 × 36 mm',font=f(24),fill='#172929')
 d.text((50,977),'Orange: geplanter Freiraum, kein maßgetreues Kabel | Displaytext nur Vorschau',font=f(24),fill='#8f3711')
 d.text((50,1015),'Elecrow-Flex ca. 50 mm bestätigt | Panelpassung, Kontaktlage und Biegeradius am Modul prüfen',font=f(22),fill='#8f3711')
 im.save(root/'Display_Vorschau_R5.png');print('R5 preview rendered',flush=True)
