"""Retro R8: open vents, glued plaque, retained brass insert mounting."""
import argparse
import make_designs as md
from make_retro_r7 import export


def build():
    p,d,parts=md.make('Retro','R6',overrides={
        'revision':'Retro JLC R8','lid_boss_inset':5.0,'lid_boss_diameter':7.8,
        'lid_pilot_diameter':4.0,'lid_pilot_depth':6.0,
        'standoff_diameter':6.8,'board_pilot_diameter':3.2,
        'reset_screw_pilot':3.2,'reset_screw_clearance':2.4})
    p.update(display_enabled=False,front_attachment='Adhesive on recessed seat',
             front_plaque_bottom_z=33.0,front_plaque_thickness_mm=3.0,
             front_adhesive_gap_mm=.2,front_side_clearance_mm=.6,
             protected_ventilation=False,side_hoods=False,bottom_vent_baffle=False,
             main_body_mm=[104,80,36],overall_mm=[104,80,36],
             material_colors={name:['3301PA Nylon SLS','White'] if name=='Fronteinsatz'
                              else ['3201PA-F Nylon SLS','Grayish Black'] for name in parts},
             paint_required=False,color_sample_match_guaranteed=False,
             insert_specs={'M3':{'model':'ruthex RX-M3Sx4.0 SHORT','length_mm':4,'outer_diameter_mm':4.6,'pilot_mm':4.0,'count':4},
                           'M2':{'model':'ruthex RX-M2x4','length_mm':4,'outer_diameter_mm':3.6,'pilot_mm':3.2,'count':6}},
             insert_installation='Post-print thermal installation; not JLC standard insert service',
             screw_reference={'lid':'4 x M3x8 90-degree countersunk, head <=5.6 mm',
                              'pcb':'4 x M2x6 pan head, head <=3.8 mm',
                              'reset':'2 x M2x6 pan head, head <=3.8 mm, height <=1.5 mm'},
             cable_ports_physical_pass_reference='User PASS R4; widened insert PCB bosses require a new fit test')
    joints=[]
    for x,y in d['lid_holes']:
        joints.append({'joint':'Deckel','part':'Unterteil','xy':[x,y],'opening_z':30,'direction':-1,'model':'M3','pilot':4.0,'depth':6.0,'boss':7.8,'screw_insertion':4.7})
    for x,y in d['pcb_holes']:
        joints.append({'joint':'PCB','part':'Unterteil','xy':[x,y],'opening_z':9.4,'direction':-1,'model':'M2','pilot':3.2,'depth':5.0,'boss':6.8,'screw_insertion':4.3})
    rx=p['board_offset_x']+p['reset_x_from_board_left']
    ry=p['board_offset_y']+p['reset_y_from_board_front']
    for x in (rx-10,rx+10):
        joints.append({'joint':'Reset','part':'Deckel','xy':[x,ry],'opening_z':24.6,'direction':1,'model':'M2','pilot':3.2,'depth':5.0,'boss':6.8,'screw_insertion':4.0})
    p['insert_joints']=joints
    return p,d,parts


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args()
    export(args.root,build,'R8')
