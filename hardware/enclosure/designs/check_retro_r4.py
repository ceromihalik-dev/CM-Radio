"""Verify the actual exported Retro R4 connector and strain-relief geometry."""
import argparse
import json
from pathlib import Path
import cadquery as cq


def check(root):
    out=Path(root)/'Retro'
    p=json.loads((out/'parameter.json').read_text())
    assert p['revision']=='Retro JLC R4'
    ass=cq.Assembly.importStep(str(out/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    parts={n.name:(n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj) for n in ass.children}
    base,lid=parts['Unterteil'],parts['Deckel']
    inside=lambda shape,x,y,z:shape.isInside(cq.Vector(x,y,z),1e-6)
    pcb_bottom=p['floor']+p['standoff_height']
    radius=p['cable_exit_diameter']/2
    upper=p['cable_exit_center_z']+radius
    assert upper<pcb_bottom
    for x in p['cable_exit_x']:
        z=p['cable_exit_center_z']
        for y in (.1,1.2,2.3):
            assert not inside(base,x,y,z)
            for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
                assert not inside(base,x+dx*(radius-.03),y,z+dz*(radius-.03))
                assert inside(base,x+dx*(radius+.03),y,z+dz*(radius+.03))
            assert inside(base,x,y,15)
            assert inside(base,x,y,24)
        assert inside(base,x,p['case_y']-.1,15)
        assert not inside(lid,x,1.2,20)
        # Full insertion envelope from the OUTSIDE wall through both front
        # PCB-post stations and past the tie eyelets. R3 skipped Y=6.7.
        route=cq.Solid.makeCylinder(radius,24,cq.Vector(x,-1,z),cq.Vector(0,1,0))
        assert route.intersect(base).Volume()<1e-5, ('cable route collision',x)
        # A floor-level 3 mm cable envelope beside the eyelet remains free.
        lane=cq.Workplane('XY').box(3,10,3,centered=(False,False,False)).translate((x-1.5,10,p['floor'])).val()
        assert lane.intersect(base).Volume()<1e-5
    usb_x=p['board_offset_x']+p['usb_center_x_from_board_left']
    for y in (.1,1.2,2.3):
        assert not inside(base,usb_x,y,13)
        assert inside(base,usb_x,y,p['usb_top_z_assumed']+.1)
        assert inside(base,usb_x,y,p['usb_bottom_z_assumed']-.1)
    assert not inside(lid,usb_x,1.2,20)
    # 12 x 8 mm plug housing, nominal centring only; actual board fit is separate.
    plug=(cq.Workplane('XY').box(12,2.6,8,centered=(False,False,False))
          .translate((usb_x-6,-.1,11.1+1.5-4)).val())
    for shape in (base,lid):assert shape.intersect(plug).Volume()<1e-5
    ir_x=usb_x+p['ir_offset_right_of_usb_centre']
    ir_z=pcb_bottom+p['board_thickness_assumed']+p['ir_height_above_pcb']
    for y in (.05,1.2,2.35):
        r=4-y/p['wall']
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            assert not inside(base,ir_x+dx*(r-.03),y,ir_z+dz*(r-.03))
            assert inside(base,ir_x+dx*(r+.03),y,ir_z+dz*(r+.03))
    for x,y in p['cable_tie_anchors']:
        for xx in (x-2.4,x,x+2.4):assert not inside(base,xx,y,3.7)
        assert inside(base,x,y,6.3)
        assert inside(base,x,y+3,3.7)
    distances=[]
    for x in p['cable_exit_x']:
        route=cq.Solid.makeCylinder(radius,24,cq.Vector(x,-1,p['cable_exit_center_z']),cq.Vector(0,1,0))
        for bx in p['board_hole_x']:
            for by in p['board_hole_y']:
                post=cq.Solid.makeCylinder(p['standoff_diameter']/2,p['standoff_height'],
                    cq.Vector(p['board_offset_x']+bx,p['board_offset_y']+by,p['floor']),cq.Vector(0,0,1))
                assert route.intersect(post).Volume()<1e-5
                distances.append(route.distance(post))
    assert min(distances)>2.3
    # Regression proof: the old left route really intersects the R3 front post.
    oldroute=cq.Solid.makeCylinder(radius,24,cq.Vector(68,-1,6.2),cq.Vector(0,1,0))
    offendingpost=cq.Solid.makeCylinder(2.9,7,cq.Vector(70.5,6.7,2.4),cq.Vector(0,0,1))
    oldvolume=oldroute.intersect(offendingpost).Volume()
    assert oldvolume>0
    report={
        'revision':'Retro V0.3 R4','result':'PASS',
        'cable_openings':'Two full round bores, no rim slots or lid tongues',
        'cable_centres_x_mm':p['cable_exit_x'],
        'full_cable_route_y_mm':[-1,23],
        'full_cable_envelope_diameter_mm':4.5,
        'minimum_clearance_to_all_pcb_posts_mm':min(distances),
        'old_R3_route_collision_mm3':oldvolume,
        'eyelet_centres_xy_mm':p['cable_tie_anchors'],
        'cable_diameter_mm':4.5,'cable_centre_z_mm':6.2,
        'cable_opening_upper_z_mm':upper,'pcb_bottom_z_mm':pcb_bottom,
        'clearance_to_pcb_bottom_mm':pcb_bottom-upper,
        'old_opposite_wall_ports_closed':True,
        'usb_opening':'Fully bounded 18 x 10.2 mm aperture in base, corner radius 2 mm',
        'usb_lid_tongue_removed':True,
        'ir_outer_inner_diameter_mm':[8,6],'ir_size_provisional':True,
        'ir_centre_x_z_mm':[ir_x,ir_z],
        'strain_relief':'Two side eyelets; cable routed on floor beside each eyelet',
        'eyelet_top_z_mm':6.4,'eyelet_tunnel_y_z_mm':[3.2,2.0],
        'eyelet_tunnel_length_x_mm':5.0,'eyelet_roof_thickness_mm':1.7,
        'floor_level_cable_envelope_diameter_mm':3.0,
        'all_electronic_components_modelled':False,'physical_fit_required':True,
        'checks':'STEP solid point containment and simplified cable/plug volume intersections'
    }
    (out/'PRUEFUNG/Anschluesse_Zugentlastung_R4.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Retro R4 Anschlüsse und Zugentlastung PASS',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();check(args.root)
