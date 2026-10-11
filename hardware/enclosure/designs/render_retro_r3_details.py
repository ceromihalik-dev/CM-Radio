"""CAD detail preview of Retro R3 cable bores, bounded USB aperture and eyelets."""
from pathlib import Path
import argparse
import numpy as np
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont
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


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args()
    root=Path(args.root)/'Retro'
    a=cq.Assembly.importStep(str(root/'BAUGRUPPE_NICHT_DRUCKEN.step'))
    image=Image.new('RGB',(1860,1080),'#f7f7f7');d=ImageDraw.Draw(image)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=lambda s:ImageFont.truetype(font,s)
    d.text((40,24),'CM-Radio Retro V0.3 R3 | Anschlussänderungen',font=f(36),fill='#172929')
    image.paste(view(a.children,58,-70),(20,100))
    image.paste(view([n for n in a.children if n.name=='Unterteil'],78,-70),(940,100))
    e,a=np.deg2rad([78,-70]);cam=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)]);right=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(cam,right)
    for x,label,lx in ((73,'Öse 1',1180),(92,'Öse 2',1650)):
        v=np.array([x,14,6.4])-np.array([52,40,18]);px=940+450+float(v@right)*6.3;py=100+400-float(v@up)*6.3
        d.ellipse((px-12,py-12,px+12,py+12),outline='#cf5b1f',width=3)
        d.line((lx+35,830,px,py+12),fill='#cf5b1f',width=3)
        d.text((lx,835),label,font=f(22),fill='#8f3711')
    d.text((60,905),'USB-Ausschnitt und zwei Bohrungen im Unterteil',font=f(24),fill='#172929')
    d.text((980,905),'Neue niedrige Ösen neben den Kabelwegen',font=f(24),fill='#172929')
    d.text((60,955),'Kabel Ø 4,5 mm | Oberkante 0,95 mm unter PCB-Unterseite | Ösenhöhe Z=6,4 mm',font=f(25),fill='#172929')
    d.text((60,1000),'IR-Trichter Ø 8/6 mm (Prüfmaß) | Platinen-Lochraster 58 × 49 mm',font=f(24),fill='#172929')
    image.save(root/'Anschlussdetail_R3.png')
    print('R3 Anschlussdetail gerendert',flush=True)
