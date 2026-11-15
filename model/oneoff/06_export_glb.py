# Körd 2026-11-14 i /home/claude/fix: hela huset som GLB för Blender (version 7, parts_v8.json).
from lib import *
import json, os, zipfile
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals
parts,P=load('parts_v8.json')
PIVOT={'doserhjul':[0,57,64.3],'lucka':[0,-8,32.2],'lucka_vit':[0,-8,32.2]}
LABEL_SV={}
# Z upp (modellen) -> Y upp (glTF); millimeter -> meter
toY=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],float)
S=np.diag([0.001,0.001,0.001,1.0])
scene=trimesh.Scene(); info=[]
def hexrgb(h): h=h.lstrip('#'); return [int(h[i:i+2],16)/255 for i in (0,2,4)]+[1.0]
for p in parts:
    n=p['name']; m=T(P,n).copy()
    piv=np.array(PIVOT.get(n,[0,0,0]),float)
    m.apply_translation(-piv)                                  # objektets origo i gångjärnet/axeln
    m.apply_transform(S@toY)
    rgb=hexrgb(p.get('color','#9A9A9A'))
    m.visual=TextureVisuals(material=PBRMaterial(name=n, baseColorFactor=rgb, metallicFactor=0.0, roughnessFactor=0.7))
    node_tf=S@toY@trimesh.transformations.translation_matrix(piv)
    node_tf[:3,:3]=np.eye(3)                                   # bara förflyttning i noden
    pw=(toY[:3,:3]@piv)*0.001; node_tf=trimesh.transformations.translation_matrix(pw)
    scene.add_geometry(m, node_name=n, geom_name=n, transform=node_tf)
    info.append(dict(name=n, group=p.get('group'), color=p.get('color'), file=p.get('file'), pivot_mm=PIVOT.get(n)))
scene.export('/mnt/user-data/outputs/lennarts-matstation.glb')
chk=trimesh.load('/mnt/user-data/outputs/lennarts-matstation.glb')
b=chk.bounds; print("delar:",len(chk.geometry),"mått (m):",np.round(b[1]-b[0],3), "storlek:", round(os.path.getsize('/mnt/user-data/outputs/lennarts-matstation.glb')/1e6,1),"MB")
json.dump(info,open('/home/claude/fix/glb_parts.json','w'),ensure_ascii=False,indent=1)
from collections import Counter; print(Counter(p.get('group') for p in parts))
