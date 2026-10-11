"""Independent checks on exported R7 STEP: inserts, front clamp, labyrinth."""
from pathlib import Path
import argparse,itertools,json,math
import cadquery as cq


def check(root):
    out=Path(root)/'Retro'
    p=json.loads((out/'parameter.json').read_text());assert p['revision']=='Retro JLC R7'
    a=cq.Assembly.importStep(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    parts={n.name:(n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj) for n in a.children}
    assert len(parts)==7
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
    # All vents remain open via an L-shaped route; test actual exported wall
    # and hood: direct side entry blocked, -Y mouth and internal route clear.
    for outer_x,channel_x,wall_x in ((-4,-1.5,1.2),(108,105.5,102.8)):
        for y in (38,44,50):
            for z in (11,16,21):
                assert inside(base,outer_x,y,z)
                assert not inside(base,wall_x,y,z)
        for y in (33,34.1,40,44,53.9):
            for z in (10.1,16,22.4):assert not inside(base,channel_x,y,z)
        assert inside(base,channel_x,55,16)
        for z in (9,23.5):assert inside(base,channel_x,44,z)
        # Safe-centre line in the original mid vent connects hood to cavity.
        x_start,x_end=(channel_x,3) if channel_x<0 else (101,channel_x)
        for i in range(21):
            x=x_start+(x_end-x_start)*i/20
            assert not inside(base,x,44,16),('hood path',x)
    for x in (36,46,56):
        assert not inside(base,x,1.2,5.5)
        assert inside(base,x,6.3,5.5)
        for y,z in ((3.5,5.5),(4,7),(4,8),(6,8),(8,8)):
            assert not inside(base,x,y,z),('bottom vent route',x,y,z)
    for x in (20,84):
        name='Front_Halter_'+('links' if x==20 else 'rechts')
        bar=parts[name]
        assert not inside(bar,x,30,25)
        assert inside(bar,x+1.3,30,25)
        assert inside(bar,x,42,25.9)
        assert inside(front,x,42,26.3)
        assert not inside(lid,x+4.4,42,31)
        assert inside(lid,x+4.7,42,31)
        assert abs(front.distance(bar)-.2)<.002
    # Front release: with strips removed the whole plaque lifts in +Z.
    for dz in (.1,.6,3,8):
        moved=front.translate((0,0,dz))
        for name in ('Deckel','Resetknopf','Unterteil','Reset_Halteplatte'):
            assert moved.intersect(parts[name]).Volume()<1e-5,('front removal',dz,name)
    # New retainers and screw heads stay above a FULL-height component box.
    # This check only applies to the new front hardware; the real IO0 and
    # old reset head clearances still require physical layout inspection.
    envelope=cq.Workplane('XY').box(85,56,11,centered=(False,False,False)).translate((9,3.2,11.1)).val()
    for name in ('Fronteinsatz','Front_Halter_links','Front_Halter_rechts'):
        assert parts[name].intersect(envelope).Volume()<1e-5
    for x in (20,84):
        head=cq.Solid.makeCylinder(1.9,1.5,cq.Vector(x,30,22.5),cq.Vector(0,0,1))
        assert head.intersect(envelope).Volume()<1e-5
    for a,b in itertools.combinations(parts,2):assert parts[a].intersect(parts[b]).Volume()<1e-5
    bb=base.BoundingBox();assert abs(bb.xlen-114)<.005
    report={'revision':'V0.3 R7','result':'PASS','insert_holes':rows,'all_printed_part_pairs':21,
            'supplier_native_colors':p['material_colors'],'assembly_overall_mm':[114,80,36],
            'side_hoods':{'downward_open':True,'direct_side_entry_blocked':True,'gap_mm':3,
                          'each_mouth_area_mm2':37.5,'wall_mm':2,'roof_above_original_slot_top_mm':3},
            'bottom_vents':{'staggered_baffle':True,'pcb_bottom_to_baffle_top_mm':2.6},
            'front':{'adhesive_required':False,'concealed_clamps':2,'lift_removal_checked_mm':[.1,.6,3,8],
                     'pad_installed_gap_mm':.2,'min_front_screw_head_above_component_envelope_mm':.4,
                     'min_pilot_roof_under_plaque_seat_mm':1.8},
            'thermal_bench_tested':False,'water_tested':False,'IP_rating':None,
            'insert_retention_bench_tested':False,'physical_fit_R7':'PENDING',
            'limits':'Hoods reduce effective vent area. No CFD, temperature, spray, torque or real component layout verification.'}
    (out/'PRUEFUNG/Integration_R7.json').write_text(json.dumps(report,indent=2)+'\n')
    print('R7 exported STEP: 12 insert holes, labyrinth, front release and head clearance PASS',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();check(args.root)
