"""Check actual STEP front heights after Boolean operations and export.

Usage: python check_front.py <export root>. The vertical grid is a surface
sampling check, not a full wall-thickness proof or a physical fit test.
"""
import argparse,json,math
from pathlib import Path
import cadquery as cq
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCP.gp import gp_Lin,gp_Pnt,gp_Dir

def check_front(root,style):
    root=Path(root)
    params=json.loads((root/style/'parameter.json').read_text())
    rx=params['board_offset_x']+params['reset_x_from_board_left']
    ry=params['board_offset_y']+params['reset_y_from_board_front']
    h=params['base_height'];inset=params['lid_boss_inset']
    asm=cq.Assembly.importStep(str(root/style/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    lid=next(n.obj for n in asm.children if n.name=='Deckel')
    lid=lid.val() if isinstance(lid,cq.Workplane) else lid
    engine=IntCurvesFace_ShapeIntersector();engine.Load(lid.wrapped,1e-7)
    heights=[]
    xs=[.25,.5,1,2,3]+list(range(4,101,2))+[101,102,103,103.5,103.75]
    ys=[.25,.5,1,2,3]+list(range(4,77,2))+[77,78,79,79.5,79.75]
    holes=[(rx,ry,5.0)]
    if style=='Retro':
        holes.extend((a,b,3.5) for a in (inset,params['case_x']-inset)
                     for b in (inset,params['case_y']-inset))
    def points(x,y):
        engine.Perform(gp_Lin(gp_Pnt(x,y,0),gp_Dir(0,0,1)),h,40)
        return [engine.Pnt(i).Z() for i in range(1,engine.NbPnt()+1)]
    for x in xs:
        for y in ys:
            if any(math.hypot(x-a,y-b)<r for a,b,r in holes):continue
            pts=points(x,y)
            if pts:heights.append((max(pts)-h,x,y))
    minimum=min(heights)
    assert minimum[0]>=(2.15 if style=='Retro' else 2.5),minimum
    report={'minimum_sampled_plate_thickness_mm':minimum[0],
            'at_xy_mm':minimum[1:],'sample_count':len(heights),
            'exclusions':'Reset well and Retro countersink wedges',
            'method':'Vertical STEP intersections; 2-mm grid plus perimeter stations',
            'is_full_wall_thickness_analysis':False}
    if style=='Wave':
        difference=max(points(96,40))-max(points(96,10))
        assert difference>1.8,('Wave relief missing from STEP',difference)
        report['measured_terrace_height_difference_mm']=difference
    (root/style/'PRUEFUNG'/'Frontflaechenpruefung.json').write_text(json.dumps(report,indent=2))
    print(style,'surface PASS',report,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args()
    for style in ('Retro','Wave'):check_front(args.root,style)
