"""Independent checks on exported R8 STEP: inserts, glued front and removal of vent protection."""
from pathlib import Path
import argparse,itertools,json,math
import cadquery as cq


def check(root):
    out=Path(root)/'Retro'
    p=json.loads((out/'parameter.json').read_text());assert p['revision']=='Retro JLC R8'
    a=cq.Assembly.importStep(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    parts={n.name:(n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj) for n in a.children}
    assert len(parts)==5
    inside=lambda s,x,y,z:s.isInside(cq.Vector(x,y,z),1e-7)
    base,lid,front=parts['Unterteil'],parts['Deckel'],parts['Fronteinsatz']
    rows=[]
    for j in p['insert_joints']:
        s=parts[j['part']];x,y=j['xy'];z=j['opening_z'];sign=j['direction']
        probe=z+sign*1.0;diameters=[]
        for angle in range(0,360,45):
            c,t=math.cos(math.radians(angle)),math.sin(math.radians(angle))
            lo,hi=0,j['boss']/2-.01
            assert not inside(s,x,y,probe) and inside(s,x+hi*c,y+hi*t,probe)
            for _ in range(23):
                mid=(lo+hi)/2
                if inside(s,x+mid*c,y+mid*t,probe):hi=mid
                else:lo=mid
            diameters.append(lo+hi)
        assert max(abs(d-j['pilot']) for d in diameters)<.002,(j,diameters)
        lo,hi=.01,j['depth']+.05
        assert not inside(s,x,y,z+sign*lo) and inside(s,x,y,z+sign*hi)
        for _ in range(23):
            mid=(lo+hi)/2
            if inside(s,x,y,z+sign*mid):hi=mid
            else:lo=mid
        depth=(lo+hi)/2;assert abs(depth-j['depth'])<.002
        assert depth-j['screw_insertion']>.65
        spec=p['insert_specs'][j['model']]
        wall=(j['boss']-spec['outer_diameter_mm'])/2
        assert wall>=1.599999
        rows.append({'joint':j['joint'],'xy_mm':[x,y],'pilot_diameter_mm':sum(diameters)/len(diameters),
                     'pilot_depth_mm':depth,'insert':spec['model'],'insert_length_mm':4,
                     'boss_radial_wall_to_insert_OD_mm':wall,
                     'nominal_screw_insertion_mm':j['screw_insertion'],
                     'screw_tip_to_pilot_bottom_mm':depth-j['screw_insertion']})
    assert len(rows)==10
    assert len([r for r in rows if r['joint']=='Deckel'])==4
    assert len([r for r in rows if r['joint']=='PCB'])==4
    assert len([r for r in rows if r['joint']=='Reset'])==2
    assert set(parts)=={'Unterteil','Deckel','Fronteinsatz','Resetknopf','Reset_Halteplatte'}
    # Both former hood volumes must be empty; every side slot has a direct path.
    for outside,wall,start,end in ((-4,1.2,-1,4),(108,102.8,100,105)):
        for y in (38,44,50):
            for z in (11,16,21):
                assert not inside(base,outside,y,z),('remaining hood',outside,y,z)
                assert not inside(base,wall,y,z),('closed side slot',wall,y,z)
        for z in (11,16,21):
            for i in range(31):
                x=start+(end-start)*i/30
                assert not inside(base,x,44,z),('blocked direct vent',x,z)
    # Original lower vents remain open, former inner baffle no longer exists.
    for x in (36,46,56):
        for y in (-1,1.2,3.5,6.3,8):
            assert not inside(base,x,y,5.5),('bottom vent / remaining baffle',x,y)
    bb=base.BoundingBox()
    assert abs(bb.xmin)<.005 and abs(bb.xmax-104)<.005
    assert abs(bb.ylen-80)<.005
    # Former front lug apertures have been closed; internal screw bosses removed.
    for x in (20,84):
        assert inside(lid,x,42,31),('front aperture remains',x)
        assert not inside(lid,x,30,28),('front insert boss remains',x)
        assert not inside(front,x,42,30),('front lug remains',x)
    fb=front.BoundingBox()
    assert abs(fb.zmin-33)<.005 and abs(fb.zmax-36)<.005
    assert abs(fb.xlen-80)<.005 and abs(fb.ylen-32)<.005
    assert abs(front.distance(lid)-.2)<.002,('adhesive gap',front.distance(lid))
    # The engraving does not cut into the glue plane.
    for x in (20,52,84):
        for y in (28,40,54):
            assert inside(front,x,y,33.01)
            assert inside(lid,x,y,32.79)
            assert not inside(front,x,y,32.9) and not inside(lid,x,y,32.9)
    for a,b in itertools.combinations(parts,2):assert parts[a].intersect(parts[b]).Volume()<1e-5
    report={'revision':'V0.3 R8','result':'PASS','insert_holes':rows,
            'all_printed_part_pairs':10,'supplier_native_colors':p['material_colors'],
            'assembly_overall_mm':[104,80,36],
            'ventilation':{'side_hoods_removed':True,'bottom_baffle_removed':True,
                          'side_slots_directly_open':True,'lower_slots_open':True},
            'front':{'adhesive_required':True,'adhesive_gap_mm':.2,
                     'dimensions_mm':[80,32,3],'concealed_clamps':0,
                     'front_insert_bosses_removed':True,'old_lug_apertures_closed':True},
            'thermal_bench_tested':False,'insert_retention_bench_tested':False,
            'physical_fit_R8':'PENDING',
            'limits':'CAD checks only; no physical print fit, adhesive retention, insert torque or full component layout verification.'}
    (out/'PRUEFUNG/Integration_R8.json').write_text(json.dumps(report,indent=2)+'\n')
    print('R8 exported STEP: 10 insert holes, open vents, glued front and removal checks PASS',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();check(args.root)
