"""W4-based physical fit prototype W5. Not the final Retro front design."""
from pathlib import Path
import argparse
import importlib.util
import itertools
import json
import shutil

import cadquery as cq
import trimesh

HERE = Path(__file__).resolve().parent
ROOT = HERE if (HERE / "CM-Radio_Gehaeuse.py").exists() else HERE.parent


def load_base():
    spec = importlib.util.spec_from_file_location("cm_enclosure", ROOT / "CM-Radio_Gehaeuse.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make(out):
    mod = load_base()
    p = json.loads((ROOT / "parameter.json").read_text(encoding="utf-8"))
    p.update({
        "revision": "W5 - Pruefmodell IR-Trichter und alle Kabel unten",
        "cable_exit_side": "usb",
        "cable_exit_diameter": 4.5,
        "ir_enabled": True,
        "ir_offset_right_of_usb_centre": 14.5,
        "ir_height_above_pcb": 5.0,
        "ir_inner_diameter": 6.0,
        "ir_outer_diameter": 8.0,
        "ir_dimensions_provisional": True,
        "prototype_notice": "W4 mechanical basis for fit checking. IR opening 6 mm inside / 8 mm outside is provisional: receiver face size not measured. Confirm at board. PCB hole pitch 58 x 49 mm; print at 100 percent. No visible version marking. USB opening unchanged; plug 12 x 8 mm, actual measured lower clearance 1 mm."
    })
    models = mod.make_models(p, engraving=True)
    out.mkdir(parents=True, exist_ok=True)
    for folder in ("STL_DRUCK", "STEP_EINZELTEILE", "PRUEFUNG", "QUELLTEXT"):
        (out / folder).mkdir(exist_ok=True)
    print_parts = {
        "CM-Radio_Unterteil_W5": "base",
        "CM-Radio_Deckel_W5": "lid_print",
        "CM-Radio_Resetknopf_W5": "button_print",
        "CM-Radio_Reset_Halteplatte_W5": "retainer_print",
        "CM-Radio_Lochraster_Probe_58x49_W5": "fit",
    }
    report = {"revision": "V0.2 W5", "unit": "mm", "parts": {}, "collisions_mm3": {}}
    for name, key in print_parts.items():
        shape = models[key].val()
        assert shape.isValid() and len(shape.Solids()) == 1, name
        bounds = mod.exact_bounds(shape)
        normalized = cq.Workplane(obj=shape.translate(cq.Vector(-bounds[0], -bounds[1], -bounds[2])))
        stl = out / "STL_DRUCK" / (name + ".stl")
        step = out / "STEP_EINZELTEILE" / (name + ".step")
        cq.exporters.export(normalized, str(stl), tolerance=.025, angularTolerance=.08)
        cq.exporters.export(normalized, str(step))
        mesh = trimesh.load_mesh(stl)
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0, name
        assert len(mesh.split(only_watertight=False)) == 1, name
        imported = cq.importers.importStep(str(step)).val()
        error = abs(imported.Volume() - shape.Volume())
        assert imported.isValid() and len(imported.Solids()) == 1 and error < max(.01, shape.Volume()*1e-6), name
        report["parts"][name] = {
            "valid": True, "solids": 1, "watertight": True,
            "winding_consistent": True, "mesh_components": 1,
            "size_mm": [bounds[i+3]-bounds[i] for i in range(3)],
            "volume_mm3": shape.Volume(), "step_volume_error_mm3": error,
            "print_z_min_mm": mod.exact_bounds(normalized.val())[2]
        }
        print(name, "PASS", flush=True)
    moving_parts = {key: models[key].val() for key in ("base", "lid", "button", "retainer")}
    for (ka, a), (kb, b) in itertools.combinations(moving_parts.items(), 2):
        volume = a.intersect(b).Volume()
        report["collisions_mm3"][ka + "__" + kb] = volume
        assert volume < 1e-5, (ka, kb, volume)
    for key in ("base", "lid", "retainer", "button"):
        volume = models[key].val().intersect(models["pcb_reference"].val()).Volume()
        report["collisions_mm3"][key + "__pcb_reference"] = volume
        assert volume < 1e-5, (key, volume)
    pressed = models["button"].translate((0, 0, -p["reset_stroke"])).val()
    for key in ("lid", "retainer", "base", "pcb_reference"):
        volume = pressed.intersect(models[key].val()).Volume()
        report["collisions_mm3"]["pressed_button__" + key] = volume
        assert volume < 1e-5, (key, volume)

    # Cross-sections verify the flare at outer, middle and inner wall faces.
    usb_x = p["board_offset_x"] + p["usb_center_x_from_board_left"]
    ir_x = usb_x + p["ir_offset_right_of_usb_centre"]
    pcb_top = p["floor"] + p["standoff_height"] + p["board_thickness_assumed"]
    ir_z = pcb_top + p["ir_height_above_pcb"]
    wall = p["wall"]
    slices = []
    for yy in (.05, wall/2, wall-.05):
        radius = p["ir_outer_diameter"]/2 - yy/wall * (p["ir_outer_diameter"]-p["ir_inner_diameter"])/2
        for dx, dz in ((1,0),(-1,0),(0,1),(0,-1)):
            assert not moving_parts["base"].isInside(cq.Vector(ir_x+dx*(radius-.03), yy, ir_z+dz*(radius-.03)), 1e-6)
            assert moving_parts["base"].isInside(cq.Vector(ir_x+dx*(radius+.03), yy, ir_z+dz*(radius+.03)), 1e-6)
        slices.append({"wall_y_mm": yy, "diameter_mm": 2*radius, "radial_checks": "PASS"})
    # Both assembled cable holes must be clear on the USB edge, and the old
    # opposite-wall openings must be closed. Check their centres and perimeters.
    for xx in p["cable_exit_x"]:
        zz = p["cable_exit_center_z"]
        for yy in (.1, wall/2, wall-.1):
            for dx,dz in ((0,0),(2.2,0),(-2.2,0),(0,2.2),(0,-2.2)):
                assert not any(s.isInside(cq.Vector(xx+dx,yy,zz+dz),1e-6) for s in (moving_parts["base"],moving_parts["lid"]))
        assert moving_parts["base"].isInside(cq.Vector(xx,p["case_y"]-.1,zz),1e-6)
    # A centred 12 x 8 mm plug housing clears the nominal CAD opening.
    # The physical 1 mm underside measurement is recorded separately; centring
    # and socket height in this envelope check are construction assumptions.
    plug = mod.box_at(usb_x-6,-.1,pcb_top+1.5-4,12,wall+.2,8).val()
    plug_collisions = {key: plug.intersect(models[key].val()).Volume() for key in ("base","lid")}
    assert all(v < 1e-5 for v in plug_collisions.values()), plug_collisions
    report["openings"] = {
        "ir_centre_x_z_mm": [ir_x, ir_z],
        "ir_diameters_outer_inner_mm": [8.0,6.0],
        "ir_size_provisional": True,
        "ir_funnel_sections": slices,
        "web_between_usb_and_ir_outer_mouth_mm": ir_x-4-(usb_x+p["usb_width"]/2),
        "speaker_cable_exit_diameter_mm": 4.5,
        "speaker_cable_exit_side": "USB side / downward when wall-mounted",
        "cable_hole_checks": "PASS",
        "old_opposite_wall_holes_closed": True,
        "nominal_plug_envelope_collision_mm3": plug_collisions,
        "nominal_plug_envelope_assumptions": "Centred on 9 x 3 mm socket extending 3 mm above PCB top; simplified cross-section, not a connector insertion-depth model",
        "measured_physical_plug_lower_clearance_mm": 1.0
    }
    report["pcb_hole_pitch_mm"] = [58,49]
    report["physical_fit_test_required"] = True
    report["full_component_clearance_checked"] = False
    assembly = cq.Assembly(name="CM_Radio_W5_Pruefmodell")
    for key,name,color in (("base","Unterteil",(.80,.82,.79)),("lid","Deckel",(.64,.73,.65)),
                           ("button","Resetknopf",(.22,.24,.22)),("retainer","Reset_Halteplatte",(.5,.5,.5))):
        assembly.add(models[key], name=name, color=cq.Color(*color))
    assembly.export(str(out / "BAUGRUPPE_NICHT_DRUCKEN.step"))
    (out / "parameter_W5.json").write_text(json.dumps(p,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out / "PRUEFUNG" / "Geometriepruefung_W5.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    shutil.copy(ROOT / "CM-Radio_Gehaeuse.py",out / "QUELLTEXT")
    shutil.copy(ROOT / "parameter.json",out / "QUELLTEXT")
    shutil.copy(HERE / "make_w5.py",out / "QUELLTEXT")
    if (HERE / "render_w5.py").exists():
        shutil.copy(HERE / "render_w5.py",out / "QUELLTEXT")
    if (HERE / "PRUEFMODELL_W5.md").exists():
        shutil.copy(HERE / "PRUEFMODELL_W5.md",out / "PRUEFMODELL_W5.md")
    for path in (ROOT / "measurements").glob("2026-10-11*.json"):
        shutil.copy(path,out / "PRUEFUNG")
    (out / "QUELLTEXT" / "requirements.txt").write_text("cadquery==2.7.0\ntrimesh>=4,<5\nnumpy\npillow\n",encoding="utf-8")
    print("Geometrie und Öffnungen PASS", flush=True)
    return p, models, report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    args = ap.parse_args()
    make(Path(args.out).resolve())
