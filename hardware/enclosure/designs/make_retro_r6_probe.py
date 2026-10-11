"""Optional screw-fit coupon; never part of the installed enclosure."""
import argparse
import json
from pathlib import Path
import cadquery as cq
import trimesh
import make_designs as design


def export(root):
    out=Path(root)/'Retro/OPTIONAL_KERNLOCHPROBE';out.mkdir(parents=True,exist_ok=True)
    m=design.m
    strip=m.rounded_box(52,16,2.4,1.5,0)
    # Chamfered left end identifies the 2.0-mm end; no tiny printed lettering.
    wedge=cq.Workplane('XY').polyline([(0,0),(3,0),(0,3)]).close().extrude(2.5)
    strip=strip.cut(wedge)
    specs=[]
    for x,diameter,outer,depth in ((8,2.0,5.8,5),(20,2.1,5.8,5),(32,2.2,5.8,5),(44,2.5,7.2,6)):
        strip=strip.union(m.cyl(x,8,2.4,outer/2,7))
        strip=strip.cut(m.cyl(x,8,9.4-depth,diameter/2,depth+.1))
        specs.append({'x_mm':x,'pilot_diameter_mm':diameter,'depth_mm':depth,'boss_diameter_mm':outer})
    shape=strip.clean().val();assert shape.isValid() and len(shape.Solids())==1
    stl=out/'CM-Radio_Kernlochprobe_R6.stl'
    cq.exporters.export(shape,str(stl),tolerance=.025,angularTolerance=.08)
    step=out/'CM-Radio_Kernlochprobe_R6.step';cq.exporters.export(shape,str(step))
    mesh=trimesh.load_mesh(stl);assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
    imported=cq.importers.importStep(str(step)).val()
    assert imported.isValid() and len(imported.Solids())==1
    assert abs(imported.Volume()-shape.Volume())<.01
    for item in specs:
        x=item['x_mm'];r=item['pilot_diameter_mm']/2;bottom=9.4-item['depth_mm']
        for dx,dz,expected in ((r-.02,-1,False),(r+.02,-1,True),(0,-item['depth_mm']+.02,False),(0,-item['depth_mm']-.02,True)):
            assert imported.isInside(cq.Vector(x+dx,8,9.4+dz),1e-7)==expected
    report={'result':'PASS','bbox_mm':[52,16,9.4],'optional':True,'installed_part':False,
            'orientation':'Chamfered corner at left; bores left-to-right 2.0, 2.1, 2.2, 2.5 mm',
            'bores':specs,'printed_thread_strength_verified':False,
            'purpose':'Compare measured hole size and chosen screw fit in the same material/process.'}
    (out/'Probe_Masse_Pruefung.json').write_text(json.dumps(report,indent=2)+'\n')
    print('R6 optionale Kernlochprobe PASS',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();export(args.root)
