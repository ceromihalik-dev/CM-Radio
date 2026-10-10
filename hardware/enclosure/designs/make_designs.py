"""CM-Radio Retro/Wave V0.3, JLC3DP SLS/MJF nylon; all coordinates in mm.

Uses the confirmed E3 mechanical source beside this directory. Export each
component separately; assembly STEP is for inspection, never a print item.
"""
from pathlib import Path
import argparse, importlib.util, json, math, shutil
import cadquery as cq
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mechanics',ROOT.parent/'CM-Radio_Gehaeuse.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def radio_mark(cx,cy,z,depth):
    outer=m.rounded_box(13,9,depth,1.5,z).translate((cx-6.5,cy-4.5,0))
    inner=m.rounded_box(11,7,depth+0.2,0.5,z-0.1).translate((cx-5.5,cy-3.5,0))
    mark=outer.cut(inner).union(m.cyl(cx-2.5,cy,z,1.4,depth))
    mark=mark.union(m.box_at(cx+1,cy-2,z,3,1,depth)).union(m.box_at(cx+1,cy+1,z,3,1,depth))
    antenna=(cq.Workplane('XY').center(cx+4,cy+7).slot2D(7,1,45).extrude(depth).translate((0,0,z)))
    return mark.union(antenna)

def branding(part,z):
    txt=(cq.Workplane('XY').text('CM-Radio',8,0.9,font='DejaVu Sans',kind='bold',combine=False)
         .translate((57,31,z-0.8)))
    # Keep the mark clear of the measured IO0 reset aperture; R1 clipped its
    # upper-left corner. The fixed switch coordinates determine this layout.
    return part.cut(txt).cut(radio_mark(61,40,z-0.8,0.9))

def wave_height(x,y):
    """Two flowing surface terraces, with a soft perimeter, in millimetres."""
    t=max(0,min(1,(x-48)/56));s=t*t*(3-2*t)
    lower=-8+43*s;upper=88-43*s
    low=0.5*(1-math.tanh((y-lower)/4))
    high=0.5*(1+math.tanh((y-upper)/4))
    ex=max(0,1-min(max(0,x),max(0,104-x))/3)
    ey=max(0,1-min(max(0,y),max(0,80-y))/3)
    return 35.8-2.0*(low+high)-1.2*max(ex*ex,ey*ey)

def wave_envelope():
    """Closed trimming volume with a cubic B-spline top surface.

    No thin applied strips: the broad relief is part of the solid lid. Uniform
    2-mm stations resolve the 3-mm perimeter roll. It cannot affect anything
    below the front plate, including the lip, screw posts and reset guide.
    """
    from OCP.GeomAPI import GeomAPI_PointsToBSplineSurface
    from OCP.TColgp import TColgp_Array2OfPnt
    from OCP.gp import gp_Pnt
    from OCP.GeomAbs import GeomAbs_C2
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
    from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
    from OCP.gp import gp_Vec
    xs=list(range(-2,107,2));ys=list(range(-2,83,2))
    points=TColgp_Array2OfPnt(1,len(xs),1,len(ys))
    for i,x in enumerate(xs,1):
        for j,y in enumerate(ys,1):
            points.SetValue(i,j,gp_Pnt(x,y,wave_height(x,y)))
    # A cubic approximation avoids the high-degree multi-wire loft's
    # overshooting/folding between closely spaced perimeter sections.
    surface=GeomAPI_PointsToBSplineSurface(points,3,3,GeomAbs_C2,0.003).Surface()
    top=cq.Face(BRepBuilderAPI_MakeFace(surface,1e-7).Face())
    # A downward sweep closes the curved face with matching side boundaries.
    # Its lower copy is below Z=0, clear of the entire actual lid mechanism.
    solid=cq.Shape.cast(BRepPrimAPI_MakePrism(top.wrapped,gp_Vec(0,0,-40),True).Shape()).fix()
    assert solid.isValid() and len(solid.Solids())==1
    return cq.Workplane(obj=solid)

def make(style):
    p=json.loads((ROOT.parent/'parameter.json').read_text())
    p.update(version='0.3',revision=style+' JLC R2',corner_radius=7.0,
             lid_thickness=3.6 if style=='Retro' else 6.0,
             lip_side_clearance=0.6,lip_thickness=2.0,port_tongue_clearance=0.6,
             reset_radial_clearance=0.6,reset_collar_thickness=1.8,
             reset_collar_top_z=27.0,reset_screw_pilot=2.0,reset_screw_clearance=2.9,
             vent_centers_x=[],vent_centers_y=[])
    # SLS/MJF guidance avoids small deep blind bores. Shallow printed pilot
    # pockets are drilling guides: complete the screw holes after delivery.
    p['lid_pilot_depth']=6.0;p['board_pilot_depth']=5.0
    d=m.make_models(p,False);base,lid=d['base'],d['lid'];h=p['base_height'];top=h+p['lid_thickness']
    rx=p['board_offset_x']+p['reset_x_from_board_left'];ry=p['board_offset_y']+p['reset_y_from_board_front']
    # Round only exterior front edges; do not alter bores or mating faces.
    exterior=[e for e in lid.edges().vals() if abs(e.BoundingBox().zmin-top)<1e-6 and abs(e.BoundingBox().zmax-top)<1e-6 and min(e.Center().x,104-e.Center().x,e.Center().y,80-e.Center().y)<3.0]
    if style=='Retro':
        lid=lid.newObject(exterior).fillet(1.2)
    for ax,ay in p['cable_tie_anchors']:
        base=base.union(m.box_at(ax-4,ay-3,7.35,8,6,0.55))
    # Strengthen retaining-plate mounting bosses (outside the PCB components
    # reference envelope); retain their shallow 2 mm printed drill guides.
    plate_top=p['reset_collar_top_z']-p['reset_collar_thickness']-p['reset_stroke']
    for sx in (rx-10,rx+10):
        lid=lid.union(m.cyl(sx,ry,plate_top,3.4,h-plate_top+0.05))
        lid=lid.cut(m.cyl(sx,ry,plate_top-0.1,1.0,3.1))
    # Rounded side slots follow the selected concepts. In the mounted side
    # view, Y is vertical and Z is depth: Retro has three vertical slits;
    # Wave has nine horizontal slits. Both side walls are fully accessible.
    vents=[(44,z,14,0) for z in (11,16,21)] if style=='Retro' else [(y,16,12,90) for y in (18,23,28,33,38,43,48,53,58)]
    for vy,vz,length,angle in vents:
        for edge in (0,p['case_x']-p['wall']):
            slot=(cq.Workplane('YZ',origin=(edge-0.1,0,0)).center(vy,vz)
                  .slot2D(length,2.4,angle).extrude(p['wall']+0.2))
            base=base.cut(slot)
    pieces={}
    if style=='Retro':
        # Wide solid decoration, no thin freestanding lattice.
        for y in (8,11.5,15,18.5,22,60,63.5,67,70.5,74):
            rib=(m.rounded_box(82,2.6,2.2,1.25,top-0.05)
                 .edges('>Z').fillet(1.1).translate((11,y-1.3,0)))
            lid=lid.union(rib)
        pocket=m.rounded_box(81.2,33.2,0.9,3.6,top-0.8).translate((11.4,24.4,0))
        lid=lid.cut(pocket)
        plaque=(m.rounded_box(80,32,3.0,3,top-0.6)
                .edges('>Z').fillet(0.8).translate((12,25,0)))
        plaque=plaque.cut(m.cyl(rx,ry,top-1,4.3,5.0))
        plaque=branding(plaque,top+2.4)
        # 0.2 mm nominal adhesive space below independent color plaque.
        d['button']=d['button'].union(m.cyl(rx,ry,top-0.5,3,2.6))
        pieces['Fronteinsatz']=plaque
        # Front screws: head pockets maintain >=2 mm floor around the bore.
        for x,y in d['lid_holes']:
            cone=cq.Solid.makeCone(1.7,3.1,1.4,cq.Vector(x,y,top-1.4),cq.Vector(0,0,1))
            lid=lid.cut(cone)
    else:
        # Hidden rear M3 screws. Base posts stop below the lid posts, leaving
        # 0.6 mm axial space; only screw clamping bridges this intentional gap.
        for x,y in d['lid_holes']:
            base=base.cut(m.cyl(x,y,23.0,3.7,8.0))
            base=base.cut(m.cyl(x,y,-0.1,1.7,31))
            cone=cq.Solid.makeCone(3.1,1.7,1.4,cq.Vector(x,y,0),cq.Vector(0,0,1))
            base=base.cut(cone)
            # Close old front clearance hole with a full-thickness cap.
            lid=lid.union(m.cyl(x,y,h,1.8,p['lid_thickness']))
            lid=lid.union(m.cyl(x,y,23.6,3.6,h-23.6+0.1))
            lid=lid.cut(m.cyl(x,y,23.5,1.25,7.4))
        # Trim the front with a smooth cubic height field. Two broad
        # 2-mm terraces replace the narrow, flat-bottom R1 engravings.
        # The machining blank is 0.2 mm above the surface peak: avoid nearly
        # coincident front faces in the Boolean. Detach the result from its
        # Workplane history so an empty Boolean cannot recover the old blank.
        trimmed=lid.val().intersect(wave_envelope().val(),tol=1e-6).clean()
        assert trimmed.isValid() and len(trimmed.Solids())==1, 'Wave surface Boolean failed'
        lid=cq.Workplane(obj=trimmed)
        assert not trimmed.Solids()[0].isInside(cq.Vector(96,10,35.0),1e-6), 'Wave trim lost'
        lid=branding(lid,35.8)
        assert not lid.val().Solids()[0].isInside(cq.Vector(96,10,35.0),1e-6), 'Wave branding lost trim'
        d['button']=d['button'].cut(m.box_at(0,0,35.5,104,80,10))
        p['wave_finished_peak_z_mm']=35.8
    pieces.update(Unterteil=base.clean(),Deckel=lid.clean(),Resetknopf=d['button'].clean(),Reset_Halteplatte=d['retainer'].clean())
    d.update(base=pieces['Unterteil'],lid=pieces['Deckel'])
    return p,d,pieces

def export(style,out):
    import trimesh
    p,d,parts=make(style);out=Path(out)/style;out.mkdir(parents=True,exist_ok=True)
    for folder in ('STL_DRUCK','STEP_EINZELTEILE','PRUEFUNG'): (out/folder).mkdir(exist_ok=True)
    report={'design':style,'revision':'V0.3-R2','unit':'mm','printed_fit_tested':False,'parts':{},'collisions_mm3':{}}
    for name,part in parts.items():
        shape=part.val();assert shape.isValid() and len(shape.Solids())==1,(style,name)
        x0,y0,z0,x1,y1,z1=m.exact_bounds(shape)
        # Print data: one closed component, min Z=0; no multi-part assembly.
        printpart=part.translate((-x0,-y0,-z0));stem=f'CM-Radio_{style}_{name}_V03_R2'
        stl=out/'STL_DRUCK'/(stem+'.stl');step=out/'STEP_EINZELTEILE'/(stem+'.step')
        cq.exporters.export(printpart,str(stl),tolerance=0.025,angularTolerance=0.08)
        cq.exporters.export(printpart,str(step))
        mesh=trimesh.load_mesh(stl);assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,(style,name,'mesh')
        roundtrip=cq.importers.importStep(str(step)).val();assert roundtrip.isValid() and len(roundtrip.Solids())==1
        assert abs(roundtrip.Volume()-shape.Volume())<max(0.01,shape.Volume()*1e-6)
        report['parts'][name]={'valid':True,'solids':1,'stl_watertight':True,'stl_winding_consistent':True,'step_roundtrip':True,'bbox_mm':[x1-x0,y1-y0,z1-z0],'volume_mm3':shape.Volume(),'faces':len(mesh.faces)}
    # Assembly collision tests, excluding touching surfaces and virtual PCB
    # screw holes. These do not substitute the actual component layout.
    for a,b in [('Unterteil','Deckel'),('Resetknopf','Deckel'),('Resetknopf','Reset_Halteplatte'),('Reset_Halteplatte','Unterteil')]:
        v=parts[a].val().intersect(parts[b].val()).Volume();report['collisions_mm3'][a+' / '+b]=v;assert v<1e-5,(style,a,b,v)
    for part in ('Unterteil','Deckel','Reset_Halteplatte'):
        v=parts[part].val().intersect(d['pcb_reference'].val()).Volume();report['collisions_mm3'][part+' / PCB']=v;assert v<1e-5,(style,part,'pcb',v)
    if 'Fronteinsatz' in parts:
        for name in ('Deckel','Resetknopf'):
            v=parts['Fronteinsatz'].val().intersect(parts[name].val()).Volume();report['collisions_mm3']['Fronteinsatz / '+name]=v;assert v<1e-5,(name,v)
    pressed=parts['Resetknopf'].translate((0,0,-p['reset_stroke']))
    for name in ('Deckel','Reset_Halteplatte','Fronteinsatz'):
        if name in parts:
            v=pressed.val().intersect(parts[name].val()).Volume();assert v<1e-5,(name,'pressed',v)
            report['collisions_mm3']['Reset gedrueckt / '+name]=v
    maxhead=p['wall_mount_head_underside_gap']+p['wall_mount_screw_head_height_max']
    report['mechanics']={'wall_mm':2.4,'floor_mm':2.4,'min_deck_design_mm':2.2 if style=='Retro' else 2.6,'lip_mm':2.0,'lid_clearance_per_side_mm':0.6,'reset_radial_clearance_mm':0.6,'reset_gap_mm':0.3,'reset_travel_mm':0.6,'pcb_hole_spacing_mm':[58,49],'pcb_bottom_z_mm':9.4,'pcb_thickness_mm':1.7,'screw_head_top_z_max_mm':maxhead,'screw_head_to_pcb_bottom_vertical_margin_mm':9.4-maxhead,'cable_diameter_mm':3.0,'mount_screw_spacing_mm':60.0}
    report['design_details']={'ribs':10,'rib_width_mm':2.6,'rib_height_mm':2.15,'rib_top_radius_mm':1.1,'plaque_mm':[80,32,3.0]} if style=='Retro' else {'surface':'cubic B-spline','wave_height_difference_mm':2.0,'transition_width_10_90_mm':8.8,'perimeter_roll_mm':1.2,'perimeter_band_mm':3.0}
    ass=cq.Assembly(name='CM-Radio_'+style)
    colors={'Unterteil':(0.44,0.52,0.41) if style=='Retro' else (0.18,0.19,0.21),'Deckel':(0.44,0.52,0.41) if style=='Retro' else (0.05,0.43,0.48),'Fronteinsatz':(0.93,0.90,0.79),'Resetknopf':(0.18,0.19,0.21),'Reset_Halteplatte':(0.5,0.5,0.5)}
    for name,part in parts.items():ass.add(part,name=name,color=cq.Color(*colors[name]))
    ass.export(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    (out/'PRUEFUNG'/'Geometriepruefung.json').write_text(json.dumps(report,indent=2))
    (out/'parameter.json').write_text(json.dumps(p,indent=2))
    print(style,'PASS',flush=True)
    return p,d,parts,report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default=str(ROOT/'export'));ap.add_argument('--design',choices=['Retro','Wave','all'],default='all');args=ap.parse_args()
    for s in (['Retro','Wave'] if args.design=='all' else [args.design]):export(s,args.out)
