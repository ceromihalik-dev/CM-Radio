"""CM-Radio enclosure V0.2 / W3 IO0 actuator, millimetres, CadQuery 2.7.

Usage: python CM-Radio_Gehaeuse.py [--params parameter.json] [--out .]
Optional: --no-engraving (if system fonts are unavailable).

The editable STEP files contain the actual enclosure geometry. The PCB in the
preview is a simplified construction reference, not a complete component model.
Manufacturer data: board outline, holes, USB X and E3 IO0 solder-pad centre.
User measurements: PCB 1.7 mm, IO0 height 2.0 mm. FDM fit and switch travel need testing.
"""
from pathlib import Path
import argparse
import json
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib


def exact_bounds(shape):
    """Avoid the triangulation tolerance margin in a display bounding box."""
    b=Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped,b,False,False)
    return b.Get()


def rounded_box(x, y, h, r, z=0):
    return (cq.Workplane("XY").box(x, y, h, centered=(False, False, False))
            .edges("|Z").fillet(r).translate((0, 0, z)))


def box_at(x, y, z, sx, sy, sz):
    return cq.Workplane("XY").box(sx, sy, sz, centered=(False, False, False)).translate((x, y, z))


def cyl(x, y, z, r, h):
    return cq.Workplane("XY").center(x, y).circle(r).extrude(h).translate((0, 0, z))


def front_profile_cut(cx, cz, width, height, radius, ymax, depth):
    # XZ workplane extrudes towards negative Y.
    return (cq.Workplane("XZ").center(cx, cz)
            .sketch().rect(width, height).vertices().fillet(radius).finalize()
            .extrude(depth).translate((0, ymax, 0)))


def side_circle(cx, cz, radius, ymax, depth):
    return (cq.Workplane("XZ").center(cx, cz).circle(radius)
            .extrude(depth).translate((0, ymax, 0)))


def make_models(p, engraving=True):
    x, y, h = p["case_x"], p["case_y"], p["base_height"]
    w, f, r, lt = p["wall"], p["floor"], p["corner_radius"], p["lid_thickness"]
    inset = p["lid_boss_inset"]
    lid_holes = [(inset, inset), (x-inset, inset), (inset, y-inset), (x-inset, y-inset)]
    pcb_holes = [(p["board_offset_x"]+hx, p["board_offset_y"]+hy)
                 for hx in p["board_hole_x"] for hy in p["board_hole_y"]]
    pcb_bottom = f + p["standoff_height"]
    usb_x = p["board_offset_x"] + p["usb_center_x_from_board_left"]
    outer = rounded_box(x, y, h, r)
    cavity = rounded_box(x-2*w, y-2*w, h+1, r-w, f).translate((w,w,0))
    base = outer.cut(cavity)
    for hx,hy in lid_holes:
        base = base.union(cyl(hx,hy,f-0.05,p["lid_boss_diameter"]/2,h-f+0.05))
    for hx,hy in pcb_holes:
        base = base.union(cyl(hx,hy,f-0.05,p["standoff_diameter"]/2,p["standoff_height"]+0.05))
    for hx,hy in lid_holes:
        base = base.cut(cyl(hx,hy,h-p["lid_pilot_depth"],p["lid_pilot_diameter"]/2,p["lid_pilot_depth"]+1))
    for hx,hy in pcb_holes:
        base = base.cut(cyl(hx,hy,pcb_bottom-p["board_pilot_depth"],p["board_pilot_diameter"]/2,p["board_pilot_depth"]+1))

    # Ports are open to the rim of the base; lid tongues close the upper part.
    # This avoids wide horizontal bridges when printing the base upright.
    low = p["usb_bottom_z_assumed"]
    port_high = h+5
    base = base.cut(front_profile_cut(usb_x,(low+port_high)/2,p["usb_width"],port_high-low,
                                    p["usb_lower_corner_radius"],w+1,w+3))
    cd, cz = p["cable_exit_diameter"], p["cable_exit_center_z"]
    for cx in p["cable_exit_x"]:
        base = base.cut(side_circle(cx,cz,cd/2,y+1,w+3))
        base = base.cut(box_at(cx-cd/2,y-w-1,cz,cd,w+3,h-cz+1))
    for ax,ay in p["cable_tie_anchors"]:
        # Internal cable-tie bridge: a 4 mm horizontal tunnel, 2.5 mm high.
        anchor = box_at(ax-4,ay-3,f-0.05,8,6,5.05)
        tunnel = box_at(ax-2,ay-4,f+1,4,8,2.5)
        base = base.union(anchor.cut(tunnel))

    # Wall mounts live in the extended rear band, clear of the entire PCB outline.
    # Large holes accept the heads; upward necks hold the shanks after lowering
    # the case. The external floor stays flat for support-free FDM printing.
    if p.get("wall_mount_enabled",False):
        seat_y=p["wall_mount_seat_y"]
        entry_y=p["wall_mount_entry_y"]
        top=p["wall_mount_reinforcement_top_z"]
        rw=p["wall_mount_reinforcement_width"]
        ry=p["wall_mount_reinforcement_y"]
        cut_height=top+1
        nr=p["wall_mount_neck_width"]/2
        for cx in p["wall_mount_x"]:
            pad=rounded_box(rw,y-ry,top-f+0.05,2.0,f-0.05).translate((cx-rw/2,ry,0))
            base=base.union(pad)
            slot=cyl(cx,entry_y,-0.1,p["wall_mount_entry_diameter"]/2,cut_height)
            slot=slot.union(box_at(cx-nr,entry_y,-0.1,2*nr,seat_y-entry_y,cut_height))
            slot=slot.union(cyl(cx,seat_y,-0.1,nr,cut_height))
            base=base.cut(slot)

    # Small low side ventilation slots, away from the antenna and PCB screws.
    for vx in (36.0, 46.0, 56.0):
        cutter = front_profile_cut(vx,5.5,6.0,2.4,1.0,w+1,w+3)
        base = base.cut(cutter)

    lid = rounded_box(x,y,lt,r,h)
    lip_inset = w+p["lip_side_clearance"]
    li = lip_inset+p["lip_thickness"]
    lip = rounded_box(x-2*lip_inset,y-2*lip_inset,p["lip_height"]+0.05,
                      r-lip_inset,h-p["lip_height"]).translate((lip_inset,lip_inset,0))
    lip = lip.cut(rounded_box(x-2*li,y-2*li,p["lip_height"]+0.3,max(0.2,r-li),
                             h-p["lip_height"]-0.1).translate((li,li,0)))
    for hx,hy in lid_holes:
        lip = lip.cut(cyl(hx,hy,h-5,p["lid_boss_diameter"]/2+0.65,6))
    lip = lip.cut(box_at(usb_x-p["usb_width"]/2-1,-1,h-6,p["usb_width"]+2,w+5,8))
    for cx in p["cable_exit_x"]:
        lip = lip.cut(box_at(cx-cd/2-1,y-w-4,h-6,cd+2,w+5,8))
    lid = lid.union(lip)
    tw=p["port_tongue_thickness"]
    tc=p["port_tongue_clearance"]
    top=p["usb_top_z_assumed"]
    lid = lid.union(box_at(usb_x-p["usb_width"]/2+tc,(w-tw)/2,top,
                          p["usb_width"]-2*tc,tw,h-top+0.05))
    for cx in p["cable_exit_x"]:
        tongue = box_at(cx-cd/2+tc,y-w+(w-tw)/2,cz,cd-2*tc,tw,h-cz+0.05)
        tongue = tongue.cut(side_circle(cx,cz,cd/2,y+1,w+3))
        lid = lid.union(tongue)
    for hx,hy in lid_holes:
        lid = lid.cut(cyl(hx,hy,h-1,p["lid_clearance_hole"]/2,lt+2))
    reset_x=p["board_offset_x"]+p.get("reset_x_from_board_left",0)
    reset_y=p["board_offset_y"]+p.get("reset_y_from_board_front",0)
    for vx in p["vent_centers_x"]:
        for vy in p["vent_centers_y"]:
            if p.get("reset_enabled",False) and abs(vx-reset_x)<p["reset_guide_diameter"]/2+3 and abs(vy-reset_y)<p["vent_length"]/2+p["reset_guide_diameter"]/2+1:
                continue
            vent=(cq.Workplane("XY").center(vx,vy).slot2D(p["vent_length"],p["vent_width"],90)
                  .extrude(lt+2).translate((0,0,h-1)))
            lid=lid.cut(vent)
    actuator={}
    if p.get("reset_enabled",False):
        shaft_r=p["reset_shaft_diameter"]/2
        hole_r=shaft_r+p["reset_radial_clearance"]
        collar_top=p["reset_collar_top_z"]
        collar_bottom=collar_top-p["reset_collar_thickness"]
        plate_top=collar_bottom-p["reset_stroke"]
        plate_bottom=plate_top-p["reset_retainer_thickness"]
        tip=pcb_bottom+p["board_thickness_assumed"]+p["reset_switch_height"]+p["reset_idle_gap"]
        face=h+lt-p["reset_face_recess"]
        button=cyl(reset_x,reset_y,tip,1.25,2.0)
        button=button.union(cyl(reset_x,reset_y,tip+2.0,shaft_r,face-tip-2.0))
        button=button.union(cyl(reset_x,reset_y,collar_bottom,p["reset_collar_diameter"]/2,p["reset_collar_thickness"]))
        guide=cyl(reset_x,reset_y,collar_top,p["reset_guide_diameter"]/2,h-collar_top+0.05)
        lid=lid.union(guide).cut(cyl(reset_x,reset_y,collar_top-0.1,hole_r,h+lt-collar_top+0.3))
        # Recessed access well, leaving the lower shaft guide intact.
        lid=lid.cut(cyl(reset_x,reset_y,h+0.5,4.3,lt+0.2))
        retainer=rounded_box(26,14,p["reset_retainer_thickness"],2,plate_bottom).translate((reset_x-13,reset_y-7,0))
        retainer=retainer.cut(cyl(reset_x,reset_y,plate_bottom-0.1,hole_r,p["reset_retainer_thickness"]+0.2))
        for sx in (reset_x-p["reset_screw_spacing"]/2,reset_x+p["reset_screw_spacing"]/2):
            boss=cyl(sx,reset_y,plate_top,2.5,h-plate_top+0.05)
            boss=boss.cut(cyl(sx,reset_y,plate_top-0.1,p["reset_screw_pilot"]/2,h-plate_top-0.5))
            lid=lid.union(boss)
            retainer=retainer.cut(cyl(sx,reset_y,plate_bottom-0.1,p["reset_screw_clearance"]/2,p["reset_retainer_thickness"]+0.2))
        # Print tip-down; supports needed below shaft shoulder and retaining collar.
        button_print=button.translate((-reset_x,-reset_y,-tip))
        retainer_print=retainer.translate((-reset_x+13,-reset_y+7,-plate_bottom))
        actuator={"button":button.clean(),"button_print":button_print.clean(),"retainer":retainer.clean(),"retainer_print":retainer_print.clean(),"tip_z":tip,"stroke":p["reset_stroke"]}
    if engraving:
        texts=[("CM-Radio",10.0,x/2,y/2-9),
               ("USB-C",3.0,usb_x,7.0),("L",3.0,p["cable_exit_x"][0],y-6),
               ("R",3.0,p["cable_exit_x"][1],y-6)]
        if p.get("reset_enabled",False):
            texts.append(("RESET",2.5,reset_x,reset_y-8))
        for txt,size,tx,ty in texts:
            letters=(cq.Workplane("XY").text(txt,size,p["engraving_depth"]+0.1,
                                             font="DejaVu Sans",kind="bold",combine=False)
                     .translate((tx,ty,h+lt-p["engraving_depth"])))
            lid=lid.cut(letters)

    # Print coordinate systems: flat bed-contact faces at Z=0.
    lid_print=lid.rotate((0,0,0),(1,0,0),180).translate((0,y,h+lt))
    base=base.clean()
    lid=lid.clean()
    lid_print=lid_print.clean()

    # A low-cost mounting-hole fit jig, not part of the operating enclosure.
    xs,ys=p["board_hole_x"],p["board_hole_y"]
    jig=cq.Workplane("XY")
    parts=[]
    for hy in ys:
        parts.append(box_at(xs[0],hy-1.8,0,xs[1]-xs[0],3.6,1.6))
    for hx in xs:
        parts.append(box_at(hx-1.8,ys[0],0,3.6,ys[1]-ys[0],1.6))
    fit=parts[0]
    for pt in parts[1:]: fit=fit.union(pt)
    for hx in xs:
        for hy in ys:
            fit=fit.union(cyl(hx,hy,0,3.2,4.5))
            fit=fit.cut(cyl(hx,hy,-0.1,1.4,4.7))
    bb=fit.val().BoundingBox()
    fit=fit.translate((-bb.xmin,-bb.ymin,0)).clean()

    # Simplified PCB construction reference. Do not export it as a print part.
    pcb=rounded_box(p["board_x"],p["board_y"],p["board_thickness_assumed"],3.5,pcb_bottom)
    # The right-hand connector notch is present in both reference revisions.
    notch=box_at(63.53,18.741,pcb_bottom-0.1,p["board_x"]-63.53+1,16.002,p["board_thickness_assumed"]+0.2)
    pcb=pcb.cut(notch).translate((p["board_offset_x"],p["board_offset_y"],0))
    for hx,hy in pcb_holes:
        pcb=pcb.cut(cyl(hx,hy,pcb_bottom-0.1,p["board_hole_diameter_reference"]/2,p["board_thickness_assumed"]+0.2))
    return {"base":base,"lid":lid,"lid_print":lid_print,"fit":fit,"pcb_reference":pcb,
            "pcb_holes":pcb_holes,"lid_holes":lid_holes,**actuator}


def export_models(models,p,out):
    out=Path(out)
    for sub in ("STL","STEP"): (out/sub).mkdir(parents=True,exist_ok=True)
    for name,key in [("CM-Radio_Unterteil_V0.2","base"),("CM-Radio_Deckel_V0.2","lid_print"),
                     ("CM-Radio_Lochraster_Probe_V0.2","fit"),("CM-Radio_Resetknopf_V0.2","button_print"),("CM-Radio_Reset_Halteplatte_V0.2","retainer_print")]:
        cq.exporters.export(models[key],str(out/"STL"/(name+".stl")),tolerance=0.05,angularTolerance=0.12)
        if key!="fit": cq.exporters.export(models[key],str(out/"STEP"/(name+".step")))
    assembly=cq.Assembly(name="CM-Radio_V0_2")
    assembly.add(models["base"],name="Unterteil",color=cq.Color(0.16,0.20,0.25))
    assembly.add(models["lid"],name="Deckel",color=cq.Color(0.12,0.64,0.58))
    assembly.add(models["button"],name="IO0_Resetknopf",color=cq.Color(0.85,0.35,0.10))
    assembly.add(models["retainer"],name="Reset_Halteplatte",color=cq.Color(0.50,0.50,0.50))
    assembly.export(str(out/"STEP"/"CM-Radio_Baugruppe_V0.2.step"))
    info={"units":"mm","dimensions_body_without_screw_heads":[p["case_x"],p["case_y"],p["base_height"]+p["lid_thickness"]],
          "pcb_bottom_z":p["floor"]+p["standoff_height"],
          "pcb_top_z_assumed":p["floor"]+p["standoff_height"]+p["board_thickness_assumed"],
          "models":{}}
    for key in ("base","lid","lid_print","fit","button_print","retainer_print"):
        s=models[key].val();xmin,ymin,zmin,xmax,ymax,zmax=exact_bounds(s)
        info["models"][key]={"valid":s.isValid(),"solids":len(s.Solids()),"volume_mm3":s.Volume(),
                            "bbox_mm":[xmax-xmin,ymax-ymin,zmax-zmin],"z_min":zmin,"z_max":zmax}
    base_s,lid_s=models["base"].val(),models["lid"].val()
    info["assembly_collision_mm3"]=base_s.intersect(lid_s).Volume()
    info["pcb_base_collision_mm3"]=base_s.intersect(models["pcb_reference"].val()).Volume()
    info["reset_idle_gap_mm"]=p["reset_idle_gap"]
    info["reset_max_travel_mm"]=p["reset_stroke"]
    info["reset_tip_z_mm"]=models["tip_z"]
    info["reset_length_mm"]=p["base_height"]+p["lid_thickness"]-p["reset_face_recess"]-models["tip_z"]
    info["reset_lid_collision_mm3"]=models["button"].val().intersect(lid_s).Volume()
    info["reset_retainer_collision_mm3"]=models["button"].val().intersect(models["retainer"].val()).Volume()
    info["reset_retainer_base_collision_mm3"]=models["retainer"].val().intersect(base_s).Volume()
    pressed=models["button"].translate((0,0,-p["reset_stroke"])).val()
    info["pressed_lid_collision_mm3"]=pressed.intersect(lid_s).Volume()
    info["pressed_retainer_collision_mm3"]=pressed.intersect(models["retainer"].val()).Volume()
    assert all(info[k]<1e-5 for k in ("reset_lid_collision_mm3","reset_retainer_collision_mm3","reset_retainer_base_collision_mm3","pressed_lid_collision_mm3","pressed_retainer_collision_mm3")),info
    (out/"Geometriepruefung.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
    return info


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--params",default=str(Path(__file__).with_name("parameter.json")))
    ap.add_argument("--out",default=str(Path(__file__).parent))
    ap.add_argument("--no-engraving",action="store_true")
    args=ap.parse_args()
    p=json.loads(Path(args.params).read_text(encoding="utf-8"))
    models=make_models(p,not args.no_engraving)
    info=export_models(models,p,args.out)
    assert all(v["valid"] and v["solids"]==1 for v in info["models"].values()),info
    assert info["assembly_collision_mm3"]<1e-5,info
    assert info["pcb_base_collision_mm3"]<1e-5,info
    print(json.dumps(info,indent=2))


if __name__=="__main__": main()
