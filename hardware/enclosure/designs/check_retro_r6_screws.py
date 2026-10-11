"""Measure exported R6 pilot diameters/depths and screw axial clearance.

The printed assembly STEP is reimported; point containment measures the
actual holes rather than trusting parameters. No strength/tap process claim.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
import cadquery as cq


def check(root,reference_root=None):
    out=Path(root)/'Retro'
    p=json.loads((out/'parameter.json').read_text())
    assert p['revision']=='Retro JLC R6' and p['display_enabled'] is False
    ass=cq.Assembly.importStep(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    parts={n.name:(n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj) for n in ass.children}
    assert set(parts)=={'Unterteil','Deckel','Fronteinsatz','Resetknopf','Reset_Halteplatte'}
    inside=lambda s,x,y,z:s.isInside(cq.Vector(x,y,z),1e-7)
    report={'revision':'V0.3 R6','result':'PASS','display':False,'pilots':[],
            'method':'Reimported assembly STEP, radial/axial bisection and intersections',
            'thread_strength_verified':False,'physical_fit_required':True}

    def bore(name,part,x,y,opening,sign,diameter,depth,boss_diameter,insertion):
        shape=parts[part]
        probe_z=opening+sign*min(1.0,depth/2)
        measured=[]
        for angle in range(0,360,45):
            c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
            lo,hi=0,boss_diameter/2-.02
            assert not inside(shape,x,y,probe_z)
            assert inside(shape,x+hi*c,y+hi*s,probe_z)
            for _ in range(22):
                mid=(lo+hi)/2
                if inside(shape,x+mid*c,y+mid*s,probe_z):hi=mid
                else:lo=mid
            measured.append(lo+hi)
        assert max(abs(d-diameter) for d in measured)<.002,(name,measured)
        lo,hi=.01,depth+.1
        assert not inside(shape,x,y,opening+sign*lo)
        assert inside(shape,x,y,opening+sign*hi)
        for _ in range(22):
            mid=(lo+hi)/2
            if inside(shape,x,y,opening+sign*mid):hi=mid
            else:lo=mid
        actual_depth=(lo+hi)/2
        assert abs(actual_depth-depth)<.002,(name,actual_depth)
        assert insertion>0 and actual_depth-insertion>.65
        report['pilots'].append({'joint':name,'part':part,'xy_mm':[x,y],
              'diameter_mm':sum(measured)/len(measured),'blind_depth_mm':actual_depth,
              'reference_axial_screw_insertion_mm':insertion,
              'tip_to_hole_bottom_clearance_mm':actual_depth-insertion,
              'nominal_radial_boss_wall_mm':(boss_diameter-diameter)/2})

    board_top=p['floor']+p['standoff_height']
    for x,y in itertools.product(p['board_hole_x'],p['board_hole_y']):
        bore('PCB 2.5x6','Unterteil',p['board_offset_x']+x,p['board_offset_y']+y,
             board_top,-1,2.0,5.0,5.8,6.0-p['board_thickness_assumed'])
    inset=p['lid_boss_inset']
    # Ideal 90-degree head seats 0.3 mm below a diameter-6.2-mm countersink.
    # Check both flush and nominal seated axial insertion, using the deeper.
    sink_recess=(6.2-p['screw_reference']['lid']['head_diameter_max_mm'])/2
    insertion=8.0-(p['lid_thickness']-sink_recess)
    for x,y in itertools.product((inset,p['case_x']-inset),(inset,p['case_y']-inset)):
        bore('Deckel M3x8','Unterteil',x,y,p['base_height'],-1,2.5,6.0,7.2,insertion)
        # Passage and countersink are actual lid solids, not a tap model.
        assert not inside(parts['Deckel'],x+1.65,y,31)
        assert inside(parts['Deckel'],x+1.75,y,31)
        assert not inside(parts['Deckel'],x+3.02,y,33.55)
        assert inside(parts['Deckel'],x+3.12,y,33.55)
    rx=p['board_offset_x']+p['reset_x_from_board_left']
    ry=p['board_offset_y']+p['reset_y_from_board_front']
    plate_top=p['reset_collar_top_z']-p['reset_collar_thickness']-p['reset_stroke']
    for x in (rx-10,rx+10):
        bore('Reset 2.5x6','Deckel',x,ry,plate_top,1,2.0,5.0,6.8,
             6.0-p['reset_retainer_thickness'])
        z=plate_top-1
        assert not inside(parts['Reset_Halteplatte'],x+1.4,ry,z)
        assert inside(parts['Reset_Halteplatte'],x+1.5,ry,z)
    for a,b in itertools.combinations(parts,2):
        v=parts[a].intersect(parts[b]).Volume()
        assert v<1e-5,(a,b,v)
    report['all_printed_part_pairs_checked']=10
    report['lid_head_nominal_seating_recess_mm']=sink_recess
    report['lid_full_thread_needed_mm']=insertion
    report['old_reset_pilot_depth_mm']=3.0
    report['old_reset_screw_tip_overrun_mm']=1.0
    report['minimum_reset_pilot_front_roof_mm']=p['base_height']+p['lid_thickness']-(plate_top+5.0)
    report['limitations']='Actual screw point/thread geometry, torque, PCB components and print tolerances require a physical test.'
    if reference_root:
        old=cq.Assembly.importStep(str(Path(reference_root)/'Retro/BAUGRUPPE_NICHT_DRUCKEN.step'))
        oldparts={n.name:(n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj) for n in old.children}
        deltas={}
        for name in parts:
            added=parts[name].cut(oldparts[name]).Volume()
            removed=oldparts[name].cut(parts[name]).Volume()
            expected_added=4*math.pi*(1.05**2-1.0**2)*5 if name=='Unterteil' else 0
            expected_removed=2*math.pi*2 if name=='Deckel' else 0
            assert abs(added-expected_added)<.01,(name,'unexpected addition',added)
            assert abs(removed-expected_removed)<.01,(name,'unexpected removal',removed)
            deltas[name]={'added_mm3':added,'removed_mm3':removed}
        report['R4_STEP_geometry_regression']=deltas
    (out/'PRUEFUNG/Schrauben_Kernloecher_R6.json').write_text(json.dumps(report,indent=2)+'\n')
    print('R6 Schrauben PASS: 10 Kernlöcher; Reset-Tipreserve 1 mm, PCB 0.7 mm, Deckel 1.3 mm',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--r4-reference');args=ap.parse_args();check(args.root,args.r4_reference)
