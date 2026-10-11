"""Retro R7: supplier-native colors, brass inserts, removable plaque and hoods.

Inserts are ruthex RX-M3Sx4.0 / RX-M2x4, installed after printing.
Side hoods open towards -Y (down when wall mounted); no IP rating claimed.
"""
from pathlib import Path
import argparse,itertools,json
import cadquery as cq
import make_designs as md
m=md.m


def build():
    p,d,parts=md.make('Retro','R6',overrides={
        'revision':'Retro JLC R7','lid_boss_inset':5.0,'lid_boss_diameter':7.8,
        'lid_pilot_diameter':4.0,'lid_pilot_depth':6.0,
        'standoff_diameter':6.8,'board_pilot_diameter':3.2,
        'reset_screw_pilot':3.2,'reset_screw_clearance':2.4})
    p.update(display_enabled=False,front_attachment='Two concealed retaining strips, no plaque adhesive',
             front_plaque_bottom_z=32.8,front_plaque_thickness_mm=3.2,
             front_lug_centres_xy=[[20,42],[84,42]],front_screw_centres_xy=[[20,30],[84,30]],
             front_lug_bottom_z=26.2,front_retainer_top_z=26.0,
             front_pad_nominal_thickness_mm=.3,front_pad_installed_thickness_mm=.2,
             front_insert_pilot_diameter_mm=3.2,front_insert_pilot_depth_mm=5.0,
             side_hood_projection_mm=5.0,side_hood_wall_mm=2.0,
             side_hood_gap_mm=3.0,side_hood_mouth_area_mm2=37.5,
             side_hood_opening_direction='-Y, down in wall mounting',
             bottom_vent_baffle_top_z=6.8,
             main_body_mm=[104,80,36],overall_with_hoods_mm=[114,80,36],
             material_colors={'Unterteil':['3201PA-F Nylon SLS','Grayish Black'],
                              'Deckel':['3201PA-F Nylon SLS','Grayish Black'],
                              'Fronteinsatz':['3301PA Nylon SLS','White'],
                              'Resetknopf':['3201PA-F Nylon SLS','Grayish Black'],
                              'Reset_Halteplatte':['3201PA-F Nylon SLS','Grayish Black'],
                              'Front_Halter_links':['3201PA-F Nylon SLS','Grayish Black'],
                              'Front_Halter_rechts':['3201PA-F Nylon SLS','Grayish Black']},
             paint_required=False,color_sample_match_guaranteed=False,
             insert_specs={'M3':{'model':'ruthex RX-M3Sx4.0 SHORT','length_mm':4,'outer_diameter_mm':4.6,'pilot_mm':4.0,'count':4},
                           'M2':{'model':'ruthex RX-M2x4','length_mm':4,'outer_diameter_mm':3.6,'pilot_mm':3.2,'count':8}},
             insert_installation='Post-print thermal installation; not JLC standard insert service',
             screw_reference={'lid':'4 x M3x8 90-degree countersunk, head <=5.6 mm',
                              'pcb':'4 x M2x6 pan head, head <=3.8 mm',
                              'reset':'2 x M2x6 pan head, head <=3.8 mm, height <=1.5 mm',
                              'front':'2 x M2x6 pan head, head <=3.8 mm, height <=1.5 mm'},
             cable_ports_physical_pass_reference='User PASS R4; widened R7 PCB bosses require a new fit test')
    base,lid=parts['Unterteil'],parts['Deckel']
    # Outside hoods enclose all three side slots. Open -Y mouth; no direct
    # horizontal line of sight through the vent. >=2-mm shell, 3-mm air gap.
    for side in ('left','right'):
        x=-5 if side=='left' else 103.9
        hood=(cq.Workplane('YZ',origin=(x,0,0)).center(45,16.25)
              .rect(22,16.5).extrude(5.1).edges('|X').fillet(1))
        cavity_x=-3 if side=='left' else 103.9
        hood=hood.cut(m.box_at(cavity_x,33.9,10,3.1,20.1,12.5))
        base=base.union(hood)
    # The downward-facing lower vents receive a floor-mounted staggered
    # inner baffle, blocking straight entry; 2.6-mm clearance below the PCB.
    base=base.union(m.box_at(30,5.4,2.35,32,2,4.45))
    # Thicken the plaque BACK by 0.2 mm to replace the old adhesive gap with
    # a seated contact face. Front peak and branding remain at Z=36.
    rx=p['board_offset_x']+p['reset_x_from_board_left']
    ry=p['board_offset_y']+p['reset_y_from_board_front']
    backing=m.rounded_box(80,32,.25,3,32.8).translate((12,25,0))
    backing=backing.cut(m.cyl(rx,ry,32.7,4.3,.5))
    plaque=parts['Fronteinsatz'].union(backing)
    for x in (20,84):
        lug=m.rounded_box(8,7,6.7,1,26.2).translate((x-4,38.5,0))
        plaque=plaque.union(lug)
        aperture=m.rounded_box(9.2,8.2,8,1.6,26).translate((x-4.6,37.9,0))
        lid=lid.cut(aperture)
        # Insert entry at Z=26, thermal installation from inside the lid.
        lid=lid.union(m.cyl(x,30,26,3.4,4.05))
        lid=lid.cut(m.cyl(x,30,25.9,1.6,5.1))
        clamp=m.rounded_box(8,19,2,1.5,24).translate((x-4,27,0))
        clamp=clamp.cut(m.cyl(x,30,23.9,1.2,2.2))
        parts['Front_Halter_'+('links' if x==20 else 'rechts')]=clamp.clean()
    parts.update(Unterteil=base.clean(),Deckel=lid.clean(),Fronteinsatz=plaque.clean())
    d.update(base=parts['Unterteil'],lid=parts['Deckel'])
    joints=[]
    for x,y in d['lid_holes']:
        joints.append({'joint':'Deckel','part':'Unterteil','xy':[x,y],'opening_z':30,'direction':-1,'model':'M3','pilot':4.0,'depth':6.0,'boss':7.8,'screw_insertion':4.7})
    for x,y in d['pcb_holes']:
        joints.append({'joint':'PCB','part':'Unterteil','xy':[x,y],'opening_z':9.4,'direction':-1,'model':'M2','pilot':3.2,'depth':5.0,'boss':6.8,'screw_insertion':4.3})
    for x in (rx-10,rx+10):
        joints.append({'joint':'Reset','part':'Deckel','xy':[x,ry],'opening_z':24.6,'direction':1,'model':'M2','pilot':3.2,'depth':5.0,'boss':6.8,'screw_insertion':4.0})
    for x in (20,84):
        joints.append({'joint':'Front','part':'Deckel','xy':[x,30],'opening_z':26,'direction':1,'model':'M2','pilot':3.2,'depth':5.0,'boss':6.8,'screw_insertion':4.0})
    p['insert_joints']=joints
    return p,d,parts


def export(root):
    import trimesh
    out=Path(root)/'Retro';out.mkdir(parents=True,exist_ok=True)
    for folder in ('STL_DRUCK','STEP_EINZELTEILE','PRUEFUNG'):(out/folder).mkdir(exist_ok=True)
    p,d,parts=build()
    report={'revision':'V0.3 R7','printed_fit_tested':False,'parts':{},'collisions_mm3':{},'physical_thermal_tested':False}
    for name,part in parts.items():
        s=part.val();assert s.isValid() and len(s.Solids())==1,(name,'solid')
        x0,y0,z0,x1,y1,z1=m.exact_bounds(s);pp=part.translate((-x0,-y0,-z0))
        stem=f'CM-Radio_Retro_{name}_V03_R7'
        stl=out/'STL_DRUCK'/(stem+'.stl');step=out/'STEP_EINZELTEILE'/(stem+'.step')
        cq.exporters.export(pp,str(stl),tolerance=.025,angularTolerance=.08)
        cq.exporters.export(pp,str(step))
        mesh=trimesh.load_mesh(stl)
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0 and len(mesh.split())==1,(name,'mesh')
        rt=cq.importers.importStep(str(step)).val()
        assert rt.isValid() and len(rt.Solids())==1,(name,'STEP')
        error=abs(rt.Volume()-s.Volume())/s.Volume();assert error<1e-5,(name,error)
        report['parts'][name]={'valid':True,'solids':1,'stl_watertight':True,'stl_components':1,'step_roundtrip':True,'step_volume_relative_error':error,'bbox_mm':[x1-x0,y1-y0,z1-z0]}
    for a,b in itertools.combinations(parts,2):
        v=parts[a].val().intersect(parts[b].val()).Volume()
        report['collisions_mm3'][a+' / '+b]=v;assert v<1e-5,(a,b,v)
    for name in ('Unterteil','Deckel','Reset_Halteplatte','Front_Halter_links','Front_Halter_rechts','Fronteinsatz'):
        assert parts[name].val().intersect(d['pcb_reference'].val()).Volume()<1e-5,(name,'PCB')
    pressed=parts['Resetknopf'].translate((0,0,-p['reset_stroke']))
    for n in parts:
        if n!='Resetknopf':assert pressed.val().intersect(parts[n].val()).Volume()<1e-5,('pressed',n)
    ass=cq.Assembly(name='CM-Radio_Retro_R7')
    for n,s in parts.items():ass.add(s,name=n,color=cq.Color(*((.94,.94,.92) if n=='Fronteinsatz' else (.22,.23,.24))))
    ass.export(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    # Hardware is only a sizing reference, intentionally omitted from prints.
    refs=cq.Assembly(name='CM-Radio_Retro_R7_Hardware_Referenzen')
    for n,s in parts.items():refs.add(s,name=n,color=cq.Color(*((.94,.94,.92) if n=='Fronteinsatz' else (.22,.23,.24))))
    for i,j in enumerate(p['insert_joints']):
        x,y=j['xy'];spec=p['insert_specs'][j['model']]
        z=j['opening_z'] if j['direction']==1 else j['opening_z']-spec['length_mm']
        # Smooth OD envelope; printed bore is smaller to receive displaced
        # polymer during thermal installation. This is not a knurl model.
        ring=m.cyl(x,y,z,spec['outer_diameter_mm']/2,4)
        ring=ring.cut(m.cyl(x,y,z-.1,int(j['model'][1:])/2,4.2))
        refs.add(ring,name=f'Gewindeeinsatz_Referenz_{i+1}',color=cq.Color(.72,.55,.18))
    refs.add(d['pcb_reference'],name='PCB_Referenz',color=cq.Color(.2,.5,.25))
    refs.export(str(out/'HARDWARE_REFERENZEN_NICHT_DRUCKEN.step'))
    (out/'parameter.json').write_text(json.dumps(p,indent=2)+'\n')
    (out/'PRUEFUNG/Geometrie_R7.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Retro R7: 7 solids, meshes, STEP, 21 part pairs, PCB and pressed reset PASS',flush=True)
    return out


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();export(args.root)
