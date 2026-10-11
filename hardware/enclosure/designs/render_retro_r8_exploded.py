"""Exploded actual R8 solids; screws/inserts are simplified reference bodies.

Explosion distances are visual only, not mounting dimensions. No enclosure
geometry is altered. Reset button is shown UNDER the lid (insert from inside).
"""
from pathlib import Path
from types import SimpleNamespace
import argparse,csv,json
import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw,ImageFont


def make_nodes(root):
    p=json.loads((root/'parameter.json').read_text())
    assert p['revision']=='Retro JLC R8'
    a=cq.Assembly.importStep(str(root/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    shifts={'Unterteil':0,'Deckel':110,'Fronteinsatz':140,
            'Resetknopf':75,'Reset_Halteplatte':50}
    nodes=[];assembly=cq.Assembly(name='R8_Explosionsansicht_KEIN_DRUCKTEIL')
    def add(name,s,color):
        shape=s.val() if isinstance(s,cq.Workplane) else s
        assert shape.isValid()
        nodes.append(SimpleNamespace(name=name,obj=shape,color=cq.Color(*color)))
        assembly.add(shape,name=name,color=cq.Color(*color))
    for n in a.children:
        shape=n.obj.val() if isinstance(n.obj,cq.Workplane) else n.obj
        add(n.name,shape.translate((0,0,shifts[n.name])),
            (.96,.96,.94) if n.name=='Fronteinsatz' else (.33,.35,.36))
    hardware=cq.Assembly.importStep(str(root/'HARDWARE_REFERENZEN_NICHT_DRUCKEN.step'))
    pcb=next(n for n in hardware.children if n.name=='PCB_Referenz')
    pcb=pcb.obj.val() if isinstance(pcb.obj,cq.Workplane) else pcb.obj
    add('Platine_Referenz',pcb.translate((0,0,35)),(.19,.49,.32))
    # Brass smooth-OD references: no thread/knurl details. Thermal fit not shown.
    for i,j in enumerate(p['insert_joints']):
        x,y=j['xy'];spec=p['insert_specs'][j['model']]
        dz={'Deckel':8,'PCB':28,'Reset':68}[j['joint']]
        z=j['opening_z']+(0 if j['direction']==1 else -4)+dz
        ring=cq.Solid.makeCylinder(spec['outer_diameter_mm']/2,4,cq.Vector(x,y,z))
        ring=ring.cut(cq.Solid.makeCylinder(int(j['model'][1:])/2,4.2,cq.Vector(x,y,z-.1)))
        add(f'Einsatz_{i+1}_{j["joint"]}',ring,(.85,.62,.23))
        # Screw envelopes: M3 90-degree countersunk including head length 8;
        # M2 nominal 6-mm shank, 1.3-mm pan head shown within permitted height.
        if j['joint']=='Deckel':
            tip=25.3+135
            screw=cq.Solid.makeCylinder(1.5,6.7,cq.Vector(x,y,tip))
            screw=screw.fuse(cq.Solid.makeCone(1.5,2.8,1.3,cq.Vector(x,y,tip+6.7)))
        elif j['joint']=='PCB':
            tip=5.1+49
            screw=cq.Solid.makeCylinder(1,6,cq.Vector(x,y,tip))
            screw=screw.fuse(cq.Solid.makeCylinder(1.9,1.3,cq.Vector(x,y,tip+6)))
        else:
            seat=22.6+36
            screw=cq.Solid.makeCylinder(1,6,cq.Vector(x,y,seat))
            screw=screw.fuse(cq.Solid.makeCylinder(1.9,1.3,cq.Vector(x,y,seat-1.3)))
        add(f'Schraube_{i+1}_{j["joint"]}',screw,(.62,.65,.68))
    assert len(nodes)==26 # 5 printed, 1 PCB reference, 10 inserts, 10 screws
    assembly.export(str(root/'EXPLOSION_NICHT_DRUCKEN.step'))
    return p,nodes


def render(root):
    root=Path(root)/'Retro';p,nodes=make_nodes(root)
    w,h=2000,2400;scale=10.;centre=np.array([52,40,88.])
    elev,azim=25,-65;e,a=np.deg2rad([elev,azim])
    cam=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
    right=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(cam,right)
    def project(v):
        q=np.asarray(v)-centre
        return np.array([q@right*scale+w/2,-q@up*scale+1120,q@cam])
    buf=np.full((h,w),-np.inf);rgb=np.full((h,w,3),255,dtype=np.uint8)
    for node in nodes:
        obj=node.obj;verts,faces=obj.tessellate(.03,.10)
        vv=np.array([[v.x,v.y,v.z] for v in verts]);ff=np.array(faces)
        q=vv-centre;pr=np.column_stack((q@right*scale+w/2,-q@up*scale+1120,q@cam))
        color=np.array(node.color.toTuple()[:3])*255
        normals=np.zeros_like(vv)
        fn=np.cross(vv[ff[:,1]]-vv[ff[:,0]],vv[ff[:,2]]-vv[ff[:,0]])
        for col in range(3):np.add.at(normals,ff[:,col],fn)
        normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
        light=np.array([.15,-.8,.58]);light/=np.linalg.norm(light)
        shades=.48+.52*np.maximum(0,normals@light)
        for idx in ff:
            tri=pr[idx];xx,yy=tri[:,0],tri[:,1]
            den=(yy[1]-yy[2])*(xx[0]-xx[2])+(xx[2]-xx[1])*(yy[0]-yy[2])
            if abs(den)<1e-8:continue
            x0=max(0,int(np.floor(xx.min())));x1=min(w-1,int(np.ceil(xx.max())))
            y0=max(0,int(np.floor(yy.min())));y1=min(h-1,int(np.ceil(yy.max())))
            if x1<x0 or y1<y0:continue
            x,y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
            b0=((yy[1]-yy[2])*(x-xx[2])+(xx[2]-xx[1])*(y-yy[2]))/den
            b1=((yy[2]-yy[0])*(x-xx[2])+(xx[0]-xx[2])*(y-yy[2]))/den;b2=1-b0-b1
            depth=b0*tri[0,2]+b1*tri[1,2]+b2*tri[2,2]
            region=buf[y0:y1+1,x0:x1+1]
            mask=(b0>=-1e-8)&(b1>=-1e-8)&(b2>=-1e-8)&(depth>region)
            if not mask.any():continue
            shade=b0*shades[idx[0]]+b1*shades[idx[1]]+b2*shades[idx[2]]
            region[mask]=depth[mask]
            rgb[y0:y1+1,x0:x1+1][mask]=np.clip(shade[mask,None]*color,0,255)
    im=Image.fromarray(rgb);d=ImageDraw.Draw(im)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f=lambda s:ImageFont.truetype(font,s)
    d.text((60,30),'CM-Radio Retro | Explosionszeichnung R8',font=f(46),fill='#193436')
    d.text((60,95),'Ohne Display · offene Lüftung · Fronteinsatz zum Aufkleben',font=f(30),fill='#5a6b70')
    # Thin assembly axis provides orientation, without implying exact distances.
    # Leaders end at the projected actual selected body surface.
    labels=[('1','Unterteil',(104,40,18),'R',1840),
            ('2','Platine',(94,25,45),'R',1600),
            ('3','Reset-Halteplatte',(32,44,73),'L',1390),
            ('4','Resetknopf',(43.49,48.20,102),'L',1080),
            ('5','Deckel',(104,40,144),'R',795),
            ('6','Klebefront',(92,40,175),'R',390),
            ('A','4 × M3 Schrauben',(99,5,167),'R',570),
            ('B','4 × M2 Schrauben',(70.5,6.7,61),'R',1420),
            ('C','2 × M2 Schrauben',(33.49,48.20,60),'L',1550),
            ('D','4 × M3 SHORT',(5,5,36),'L',1900),
            ('E','4 × M2 Einsätze',(12.5,6.7,35),'L',1750),
            ('F','2 × M2 Einsätze',(33.49,48.20,95),'L',930)]
    for num,label,anchor,side,ly in labels:
        px,py,_=project(anchor);cx=70 if side=='L' else 1660
        edge=cx+330 if side=='L' else cx-25
        color='#9a6c20' if num in 'DEF' else '#48646d'
        d.line([(edge,ly+24),(edge+(35 if side=='L' else -35),ly+24),(px,py)],fill=color,width=2)
        d.ellipse((px-5,py-5,px+5,py+5),fill=color)
        d.ellipse((cx,ly,cx+44,ly+44),fill=color)
        bbox=d.textbbox((0,0),num,font=f(26));tw=bbox[2]-bbox[0]
        d.text((cx+22-tw/2,ly+5),num,font=f(26),fill='white')
        d.text((cx+56,ly+7),label,font=f(27),fill='#193436')
    d.text((60,2260),'5 Druckteile + vorhandene Platine · 10 Schrauben + 10 Messinggewindeeinsätze',font=f(29),fill='#193436')
    d.text((60,2310),'Explosionsabstände ohne Maßstab. Hardware / PCB vereinfacht; keine Druckteile.',font=f(27),fill='#5a6b70')
    im.save(root/'CM-Radio_Retro_R8_Explosionszeichnung.png')
    (root/'PRUEFUNG/Explosionszeichnung_R8.json').write_text(json.dumps({
        'revision':'V0.3 R8','printed_solids_from_exported_STEP':5,
        'PCB_reference':1,'simplified_screw_references':10,'simplified_insert_references':10,
        'view_only_explosion_step':True,'enclosure_geometry_changed':False,
        'explosion_Z_offsets_mm':{'Unterteil':0,'PCB':35,'Reset_Halteplatte':50,
                                  'Resetknopf':75,'Deckel':110,'Fronteinsatz':140},
        'reset_button_insert_from_inside':True,'physical_fit_tested':False},indent=2)+'\n')
    print('R8 exploded view: actual 5 parts + PCB, 10 screws, 10 inserts',flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args();render(args.root)
