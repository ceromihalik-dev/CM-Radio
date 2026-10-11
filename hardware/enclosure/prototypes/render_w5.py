"""Render the actual W5 assembly using the existing CAD z-buffer renderer."""
from pathlib import Path
import argparse
import numpy as np
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont
def view(nodes,elev,azim):
 w,h=900,800;buf=np.full((h,w),-np.inf);rgb=np.full((h,w,3),247,dtype=np.uint8)
 e,a=np.deg2rad([elev,azim]);cam=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)]);right=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(cam,right);scale=6.3
 for node in nodes:
  if node.name=='Reset_Halteplatte':continue
  obj=node.obj.val() if isinstance(node.obj,cq.Workplane) else node.obj
  verts,faces=obj.tessellate(.025,.08);vv=np.array([[v.x,v.y,v.z] for v in verts]);ff=np.array(faces);vv-=np.array([52,40,18]);project=np.column_stack((vv@right*scale+w/2,-vv@up*scale+h/2,vv@cam));color=np.array(node.color.toTuple()[:3])*255
  # Smooth lighting within each CAD face. OCCT keeps separate vertices at
  # face boundaries, so intentional hard edges remain sharp. No mesh edits.
  normals=np.zeros_like(vv);fn=np.cross(vv[ff[:,1]]-vv[ff[:,0]],vv[ff[:,2]]-vv[ff[:,0]])
  for col in range(3):np.add.at(normals,ff[:,col],fn)
  normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
  vertex_shade=.42+.58*np.maximum(0,normals@np.array([-.15,-.80,.581]))
  for idx in ff:
   tri=project[idx];xx,yy=tri[:,0],tri[:,1];den=(yy[1]-yy[2])*(xx[0]-xx[2])+(xx[2]-xx[1])*(yy[0]-yy[2])
   if abs(den)<1e-8:continue
   x0=max(0,int(np.floor(xx.min())));x1=min(w-1,int(np.ceil(xx.max())));y0=max(0,int(np.floor(yy.min())));y1=min(h-1,int(np.ceil(yy.max())))
   if x1<x0 or y1<y0:continue
   x,y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
   b0=((yy[1]-yy[2])*(x-xx[2])+(xx[2]-xx[1])*(y-yy[2]))/den;b1=((yy[2]-yy[0])*(x-xx[2])+(xx[0]-xx[2])*(y-yy[2]))/den;b2=1-b0-b1;depth=b0*tri[0,2]+b1*tri[1,2]+b2*tri[2,2]
   region=buf[y0:y1+1,x0:x1+1];mask=(b0>=-1e-8)&(b1>=-1e-8)&(b2>=-1e-8)&(depth>region)
   if not mask.any():continue
   shade=b0*vertex_shade[idx[0]]+b1*vertex_shade[idx[1]]+b2*vertex_shade[idx[2]];region[mask]=depth[mask];rgb[y0:y1+1,x0:x1+1][mask]=np.clip(shade[mask,None]*color,0,255)
 return Image.fromarray(rgb)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root')
    args=ap.parse_args()
    root=Path(args.root)
    assembly=cq.Assembly.importStep(str(root/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    canvas=Image.new('RGB',(1860,1080),'#f7f7f7')
    draw=ImageDraw.Draw(canvas)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f=lambda size: ImageFont.truetype(font,size)
    draw.text((40,24),'CM-Radio | Prüfmodell V0.2 W5',font=f(36),fill='#172929')
    canvas.paste(view(assembly.children,58,-70),(20,100))
    base=[n for n in assembly.children if n.name=='Unterteil']
    canvas.paste(view(base,58,-70),(940,100))
    draw.text((60,905),'Montiert: USB, IR und Kabel an der unteren Kante',font=f(24),fill='#172929')
    draw.text((980,905),'Unterteil: alte obere Kabelöffnungen geschlossen',font=f(23),fill='#172929')
    draw.text((60,955),'104 × 80 × 32,4 mm | Platinen-Lochraster 58 × 49 mm | Kabel Ø 4,5 mm',font=f(25),fill='#172929')
    draw.text((60,1000),'IR-Trichter Ø 8 mm außen / Ø 6 mm innen: vorläufige Größe für den Passungstest',font=f(24),fill='#172929')
    canvas.save(root/'CM-Radio_Pruefmodell_W5_Vorschau.png')
    print('CAD-Vorschau erzeugt',flush=True)


if __name__=='__main__': main()
