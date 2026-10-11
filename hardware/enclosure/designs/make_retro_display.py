"""Retro R5 display lid, panel reference from SparkFun QG-2864KSWLG01.
The 0.7 mm FPC in that drawing is NOT the board's 0.5 mm connector variant.
Mechanical prototype only; electronics and flex route are reference solids.
"""
from pathlib import Path
import argparse,json,itertools
import cadquery as cq
import make_designs as md
m=md.m
ROOT=Path(__file__).resolve().parent

def build():
 p,d,parts=md.make('Retro','R4')
 p.update(revision='Retro JLC R5 Display',display_panel_mm=[34.5,23.0,1.4],
          display_panel_centre_xy=[25.5,29.5],display_panel_front_z=32.8,
          display_active_mm=[29.42,14.7],display_active_centre_xy=[25.5,27.45],
          display_window_mm=[31.8,17.1],display_pocket_mm=[35.7,24.2],
          display_holder_top_z=30.6,display_soft_pad_thickness_mm=0.8,
          display_fpc_exit_width_mm=24.0,display_fpc_reference_width_mm=16.0,
          display_datasheet_fpc_pitch_mm=0.7,board_fpc_pitch_mm=0.5,
          display_direct_electrical_connection_verified=False,
          elecrow_fpc_free_length_user_mm=50.0,
          elecrow_fpc_length_basis='Approximate free cable length from module, user 2026-10-11',
          display_panel_variant_match_verified=False,
          display_drawing='QG-2864KSWLG01 A / QT1106P07, SparkFun PDF page 3',
          display_plaque_mm=[90,42,3],cable_ports_physical_pass=True)
 lid=parts['Deckel'];cx,cy=p['display_panel_centre_xy'];rx=43.48635;ry=48.2011
 # Enlarge the existing plaque pocket, removing two overlapping lower ribs.
 lid=lid.cut(m.rounded_box(91.2,43.2,6,3.6,32.8).translate((6.4,15.4,0)))
 plaque=m.rounded_box(90,42,3,3,33).edges('>Z').fillet(.8).translate((7,16,0))
 plaque=plaque.cut(m.cyl(rx,ry,32.9,4.3,4))
 wx,wy=p['display_active_centre_xy'];window=m.rounded_box(31.8,17.1,10,.6,28).translate((wx-15.9,wy-8.55,0))
 plaque=plaque.cut(window)
 # Subtle wider mouth at the front, leaving a 2 mm structural window throat.
 plaque=plaque.cut(m.rounded_box(32.6,17.9,.55,1.0,35.5).translate((wx-16.3,wy-8.95,0)))
 txt=cq.Workplane('XY').text('CM-Radio',7,.9,font='DejaVu Sans',kind='bold',combine=False).translate((70,29,35.2))
 plaque=plaque.cut(txt).cut(md.radio_mark(73,43,35.2,.9))
 # Rear-open U retaining plate: pads contact only glass border, not IC/flex.
 holder=m.rounded_box(38.9,27.4,2,1.8,28.6).translate((cx-19.45,cy-13.7,0))
 holder=holder.cut(m.rounded_box(31.5,20,2.2,.6,28.5).translate((cx-15.75,cy-10,0)))
 holder=holder.cut(m.box_at(cx-21,cy+9.5,28.5,42,5.2,2.2))
 screws=[(12.5,13.0),(38.5,13.0)]
 for x,y in screws:holder=holder.union(m.cyl(x,y,28.6,3.4,2))
 for x,y in screws:holder=holder.cut(m.cyl(x,y,28.5,1.45,2.2))
 # Recess leaves >=2.1 mm lid roof under the plaque, >=2.9 at screw pads.
 recess=m.rounded_box(40.1,28.6,2.2,2.2,28.5).translate((cx-20.05,cy-14.3,0))
 for x,y in screws:recess=recess.union(m.cyl(x,y,28.5,4,2.2))
 lid=lid.cut(recess)
 # Panel cavity through lid; the independent 3 mm plaque is the front stop.
 cavity=m.rounded_box(35.7,24.2,5.2,1.0,28.5).translate((cx-17.85,cy-12.1,0))
 lid=lid.cut(cavity)
 # 24 mm open upper outlet: panel flex leaves towards board's OLED connector.
 lid=lid.cut(m.box_at(cx-12,cy+11.5,28.5,24,2.3,4.4))
 for x,y in screws:lid=lid.cut(m.cyl(x,y,30.65,1,2.1))
 parts.update(Deckel=lid.clean(),Fronteinsatz=plaque.clean(),Displayhalter=holder.clean())
 # Ref panel rotated 180 degrees: flex towards +Y. Active centre offset -2.05.
 panel=m.box_at(cx-17.25,cy-11.5,31.4,34.5,23,1.4)
 active=m.box_at(wx-14.71,wy-7.35,32.81,29.42,14.7,.03)
 # Free routing CORRIDOR, not a made-up exact flex cable. Contact plane and
 # material bend radius are unverified. Length includes no service slack.
 path=[(25.5,41,31.0),(20,43.7,29.0),(20,47,21.0),(26.64615,50.52439,13.1)]
 routing=None
 for i,(a,b) in enumerate(zip(path,path[1:])):
  ra,rb=8,(11 if i==2 else 8)
  wire=cq.Wire.makePolygon([cq.Vector(a[0]-ra,a[1],a[2]-.3),cq.Vector(a[0]+ra,a[1],a[2]-.3),cq.Vector(b[0]+rb,b[1],b[2]-.3),cq.Vector(b[0]-rb,b[1],b[2]-.3)],close=True)
  s=cq.Workplane(obj=cq.Solid.extrudeLinear(wire,[],cq.Vector(0,0,.6)))
  routing=s if routing is None else routing.union(s)
 p['display_route_reference_centres_xyz_mm']=path
 p['display_route_is_actual_cable']=False
 p['display_route_reference_widths_mm']=[16,16,16,22]
 p['display_reference_tail_projection_mm']=12
 p['display_extension_needed_for_pdf_variant']=True
 p['display_flex_length_verified']=False
 p['display_minimum_bend_radius_verified']=False
 return p,d,parts,{'OLED_Panel_Referenz':panel,'OLED_Aktivflaeche_Referenz':active,'FPC_Freiraum_Referenz':routing}

def export(out):
 import trimesh,math
 out=Path(out)/'Retro';out.mkdir(parents=True,exist_ok=True)
 for f in ('STL_DRUCK','STEP_EINZELTEILE','PRUEFUNG'): (out/f).mkdir(exist_ok=True)
 p,d,parts,refs=build();report={'revision':'V0.3 R5 Display','printed_fit_tested':False,'parts':{},'collisions_mm3':{}}
 for name,part in parts.items():
  s=part.val();assert s.isValid() and len(s.Solids())==1,(name,'solid')
  x0,y0,z0,x1,y1,z1=m.exact_bounds(s);pp=part.translate((-x0,-y0,-z0));stem=f'CM-Radio_Retro_{name}_V03_R5'
  stl=out/'STL_DRUCK'/(stem+'.stl');step=out/'STEP_EINZELTEILE'/(stem+'.step')
  cq.exporters.export(pp,str(stl),tolerance=.025,angularTolerance=.08);cq.exporters.export(pp,str(step))
  mesh=trimesh.load_mesh(stl);assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
  assert len(mesh.split())==1
  rt=cq.importers.importStep(str(step)).val();assert rt.isValid() and len(rt.Solids())==1
  relative_error=abs(rt.Volume()-s.Volume())/s.Volume()
  assert relative_error<1e-4,(name,'STEP healing volume error',relative_error)
  report['parts'][name]={'valid':True,'solids':1,'stl_watertight':True,'stl_components':1,'step_roundtrip':True,'step_relative_volume_error':relative_error,'bbox_mm':[x1-x0,y1-y0,z1-z0],'volume_mm3':s.Volume()}
 for a,b in itertools.combinations(parts,2):
  v=parts[a].val().intersect(parts[b].val()).Volume();report['collisions_mm3'][a+' / '+b]=v;assert v<1e-5,(a,b,v)
 for name,ref in refs.items():
  for part in parts:
   v=ref.val().intersect(parts[part].val()).Volume();report['collisions_mm3'][name+' / '+part]=v;assert v<1e-5,(name,part,v)
 for part in ('Unterteil','Deckel','Displayhalter','Reset_Halteplatte'):
  assert parts[part].val().intersect(d['pcb_reference'].val()).Volume()<1e-5,(part,'PCB')
 pressed=parts['Resetknopf'].translate((0,0,-p['reset_stroke']))
 for part in ('Deckel','Displayhalter','Reset_Halteplatte','Fronteinsatz'):
  assert pressed.val().intersect(parts[part].val()).Volume()<1e-5,('pressed',part)
 assert pressed.val().intersect(refs['FPC_Freiraum_Referenz'].val()).Volume()<1e-5
 # Maximum drawing tolerance panel. Keep its FRONT constant at Z=32.8.
 worst=m.box_at(25.5-17.35,29.5-11.6,31.3,34.7,23.2,1.5)
 for n in parts:assert worst.val().intersect(parts[n].val()).Volume()<1e-5,('worst panel',n)
 report['display']={'panel_nominal_mm':p['display_panel_mm'],'worst_panel_mm':[34.7,23.2,1.5],'window_mm':p['display_window_mm'],'panel_face_z_mm':32.8,'rear_holder_gap_mm':.8,'front_stop_gap_mm':.2,'panel_clearance_per_side_nominal_mm':.6,'routing_reference_widths_mm':[16,16,16,22],'routing_reference_thickness_mm':.6,'routing_length_polyline_mm':sum(math.dist(a,b) for a,b in zip(p['display_route_reference_centres_xyz_mm'],p['display_route_reference_centres_xyz_mm'][1:])),'minimum_bend_radius_verified':False,'drawing_pitch_matches_board':False,'elecrow_pitch_matches_board_by_supplier':True,'elecrow_free_fpc_length_user_mm':50.0,'actual_fpc_length_bench_verified':False,'full_component_model':False,'print_is_mechanical_prototype':True}
 ass=cq.Assembly(name='CM-Radio_Retro_R5');colors={'Unterteil':(.44,.52,.41),'Deckel':(.44,.52,.41),'Fronteinsatz':(.93,.90,.79),'Resetknopf':(.18,.19,.21),'Reset_Halteplatte':(.5,.5,.5),'Displayhalter':(.5,.5,.5)}
 for n,s in parts.items():ass.add(s,name=n,color=cq.Color(*colors[n]))
 ass.export(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
 refass=cq.Assembly(name='CM-Radio_Retro_R5_Einbaupruefung')
 for n,s in parts.items():refass.add(s,name=n,color=cq.Color(*colors[n]))
 for n,s in refs.items():refass.add(s,name=n,color=cq.Color(*({'OLED_Panel_Referenz':(.08,.08,.08),'OLED_Aktivflaeche_Referenz':(.04,.13,.16),'FPC_Freiraum_Referenz':(.9,.55,.08)}[n])))
 refass.add(d['pcb_reference'],name='PCB_Referenz',color=cq.Color(.2,.5,.25))
 refass.export(str(out/'EINBAUPRUEFUNG_REFERENZEN_NICHT_DRUCKEN.step'))
 (out/'parameter.json').write_text(json.dumps(p,indent=2)+'\n');(out/'PRUEFUNG/Display_R5.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Retro R5 solids, meshes, STEP, pairs, reset, panel tolerances and routing corridor PASS',flush=True)
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('out');args=ap.parse_args();export(args.out)
