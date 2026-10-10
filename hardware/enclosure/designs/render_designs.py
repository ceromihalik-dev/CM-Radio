from pathlib import Path
import numpy as np,cadquery as cq
from PIL import Image,ImageDraw,ImageFont
import argparse
ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args()
root=Path(args.root)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def view(nodes,elev,azim):
 w,h=900,800;buf=np.full((h,w),-np.inf);rgb=np.full((h,w,3),247,dtype=np.uint8)
 e,a=np.deg2rad([elev,azim]);cam=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)]);right=np.array([-np.sin(a),np.cos(a),0]);up=np.cross(cam,right);scale=6.3
 for node in nodes:
  if node.name=='Reset_Halteplatte':continue
  obj=node.obj.val() if isinstance(node.obj,cq.Workplane) else node.obj
  verts,faces=obj.tessellate(.04,.1);vv=np.array([[v.x,v.y,v.z] for v in verts]);ff=np.array(faces);vv-=np.array([52,40,18]);project=np.column_stack((vv@right*scale+w/2,-vv@up*scale+h/2,vv@cam));color=np.array(node.color.toTuple()[:3])*255
  for idx in ff:
   tri=project[idx];xx,yy=tri[:,0],tri[:,1];den=(yy[1]-yy[2])*(xx[0]-xx[2])+(xx[2]-xx[1])*(yy[0]-yy[2])
   if abs(den)<1e-8:continue
   x0=max(0,int(np.floor(xx.min())));x1=min(w-1,int(np.ceil(xx.max())));y0=max(0,int(np.floor(yy.min())));y1=min(h-1,int(np.ceil(yy.max())))
   if x1<x0 or y1<y0:continue
   x,y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
   b0=((yy[1]-yy[2])*(x-xx[2])+(xx[2]-xx[1])*(y-yy[2]))/den;b1=((yy[2]-yy[0])*(x-xx[2])+(xx[0]-xx[2])*(y-yy[2]))/den;b2=1-b0-b1;depth=b0*tri[0,2]+b1*tri[1,2]+b2*tri[2,2]
   region=buf[y0:y1+1,x0:x1+1];mask=(b0>=-1e-8)&(b1>=-1e-8)&(b2>=-1e-8)&(depth>region)
   if not mask.any():continue
   normal=np.cross(vv[idx[1]]-vv[idx[0]],vv[idx[2]]-vv[idx[0]]);normal/=max(np.linalg.norm(normal),1e-12);shade=.60+.38*max(0,normal@np.array([-.3,-.4,.866]));region[mask]=depth[mask];rgb[y0:y1+1,x0:x1+1][mask]=np.clip(color*shade,0,255)
 return Image.fromarray(rgb)
for style in ('Retro','Wave'):
 a=cq.Assembly.importStep(str(root/style/'BAUGRUPPE_NICHT_DRUCKEN.step'));im=Image.new('RGB',(1860,1010),'#f7f7f7');d=ImageDraw.Draw(im);d.text((40,25),'CM-Radio '+style+' | V0.3 R1',font=ImageFont.truetype(font,36),fill='#172929');im.paste(view(a.children,65,-70),(20,100));im.paste(view(a.children,-65,-70),(940,100));d.text((70,930),'Tatsächliches CAD – Front',font=ImageFont.truetype(font,24),fill='#172929');d.text((990,930),'Rückwand und Schlüssellochaufnahmen',font=ImageFont.truetype(font,24),fill='#172929');im.save(root/style/'CAD_Vorschau.png');print(style,'rendered',flush=True)
