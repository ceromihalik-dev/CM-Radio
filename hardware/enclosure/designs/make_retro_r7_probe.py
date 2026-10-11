"""Optional thermal insert fit coupon with actual R7 boss sizes."""
from pathlib import Path
import argparse,json
import cadquery as cq
import trimesh
import make_designs as md
m=md.m


def export(root):
    out=Path(root)/'Retro/OPTIONAL_EINSATZPROBE';out.mkdir(parents=True,exist_ok=True)
    strip=m.rounded_box(52,16,2.4,1.5)
    strip=strip.cut(cq.Workplane('XY').polyline([(0,0),(3,0),(0,3)]).close().extrude(2.5))
    specs=[]
    for x,dia,boss,depth,model in ((8,3.2,6.8,5,'M2'),(20,3.3,6.8,5,'M2'),(32,4.0,7.8,6,'M3 SHORT'),(44,4.1,7.8,6,'M3 SHORT')):
        strip=strip.union(m.cyl(x,8,2.4,boss/2,7))
        strip=strip.cut(m.cyl(x,8,9.4-depth,dia/2,depth+.1))
        specs.append({'x_mm':x,'pilot_diameter_mm':dia,'depth_mm':depth,'boss_diameter_mm':boss,'insert':model})
    strip=strip.clean();s=strip.val();assert s.isValid() and len(s.Solids())==1
    stl=out/'CM-Radio_Einsatzprobe_R7.stl';step=out/'CM-Radio_Einsatzprobe_R7.step'
    cq.exporters.export(strip,str(stl),tolerance=.025,angularTolerance=.08);cq.exporters.export(strip,str(step))
    mesh=trimesh.load_mesh(stl);assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1
    rt=cq.importers.importStep(str(step)).val();assert rt.isValid() and len(rt.Solids())==1 and abs(rt.Volume()-s.Volume())<.01
    for j in specs:
        x=j['x_mm'];r=j['pilot_diameter_mm']/2;bottom=9.4-j['depth_mm']
        assert not rt.isInside(cq.Vector(x+r-.02,8,8.4),1e-7)
        assert rt.isInside(cq.Vector(x+r+.02,8,8.4),1e-7)
        assert not rt.isInside(cq.Vector(x,8,bottom+.02),1e-7)
        assert rt.isInside(cq.Vector(x,8,bottom-.02),1e-7)
    (out/'Probe_Masse_Pruefung.json').write_text(json.dumps({'result':'PASS','bbox_mm':[52,16,9.4],
        'optional':True,'orientation':'Chamfered corner at left; 3.2 / 3.3 / 4.0 / 4.1 mm',
        'bores':specs,'purpose':'Check actual dimensions and thermal installation before enclosure.'},indent=2)+'\n')
    print('R7 optionale Einsatzprobe PASS',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();export(args.root)
