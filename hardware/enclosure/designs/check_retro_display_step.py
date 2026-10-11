"""Verify the actual R5 STEP assembly and non-print references after export."""
import argparse,json,itertools
from pathlib import Path
import cadquery as cq

def check(root):
 root=Path(root)/'Retro';p=json.loads((root/'parameter.json').read_text())
 ass=cq.Assembly.importStep(str(root/'EINBAUPRUEFUNG_REFERENZEN_NICHT_DRUCKEN.step'))
 s={n.name:n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj for n in ass.children}
 names=['Unterteil','Deckel','Fronteinsatz','Resetknopf','Reset_Halteplatte','Displayhalter']
 for n in names:assert s[n].isValid() and len(s[n].Solids())==1,n
 result={'revision':'Retro V0.3 R5 Display','result':'PASS','actual_STEP':True,'intersections_mm3':{}}
 for a,b in itertools.combinations(names,2):
  v=s[a].intersect(s[b]).Volume();assert v<1e-5,(a,b,v);result['intersections_mm3'][a+' / '+b]=v
 for r in ['OLED_Panel_Referenz','OLED_Aktivflaeche_Referenz','FPC_Freiraum_Referenz']:
  for n in names:
   v=s[r].intersect(s[n]).Volume();assert v<1e-5,(r,n,v);result['intersections_mm3'][r+' / '+n]=v
 pressed=s['Resetknopf'].translate(cq.Vector(0,0,-p['reset_stroke']))
 for n in ['Deckel','Fronteinsatz','Reset_Halteplatte','Displayhalter','FPC_Freiraum_Referenz']:
  assert pressed.intersect(s[n]).Volume()<1e-5,('pressed',n)
 # Verify unobstructed optical aperture above the AA, including corner margins.
 for x in (25.5-14.81,25.5,25.5+14.81):
  for y in (27.45-7.45,27.45,27.45+7.45):
   for z in (33.1,34,35,35.9):
    assert not s['Fronteinsatz'].isInside(cq.Vector(x,y,z),1e-6),(x,y,z)
 # Confirm residual lid roof at the holder recess, away from the panel cavity.
 for z in (30.8,31.8,32.7):assert s['Deckel'].isInside(cq.Vector(7.3,29.5,z),1e-6)
 assert not s['Deckel'].isInside(cq.Vector(7.3,29.5,30.6),1e-6)
 # R4 complete cable insertion envelope must still be free of all base solids.
 for x in (78,87):
  route=cq.Solid.makeCylinder(2.25,24,cq.Vector(x,-1,6.2),cq.Vector(0,1,0))
  assert route.intersect(s['Unterteil']).Volume()<1e-5
 result.update(optical_aperture_clear=True,nominal_holder_recess_roof_mm=2.1,
               full_R4_cable_routes_clear=True,physical_panel_fit_verified=False,
               real_flex_length_and_bend_verified=False,real_adapter_modelled=False)
 (root/'PRUEFUNG/STEP_Einbaupruefung_R5.json').write_text(json.dumps(result,indent=2)+'\n')
 print('R5 actual STEP: part pairs, panel, optical aperture, FPC corridor, pressed reset and cable routes PASS',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();check(args.root)
