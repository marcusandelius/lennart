# Körd 2026-11-15 i /home/claude/fix: exportera skålen (farstukvisten) igen efter breddningen.
from lib import *
import os
parts,P=load('parts_v11.json')
fmap={}
for p in parts: fmap.setdefault(p.get('file'),[]).append(p['name'])
grp=[f for f in fmap if f and f.startswith('07_')]; print(grp, [fmap[f] for f in grp])
old={f:trimesh.load('stl/'+f) for f in grp}
names=[fmap[f][0] for f in grp]
ms=[T(P,n) for n in names]
allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
A=[[1,0,0,-(lo[0]+hi[0])/2],[0,1,0,-(lo[1]+hi[1])/2],[0,0,1,-lo[2]]]
for n,f in zip(names,grp):
    man=M(P,n).transform(A); out=Manifold()
    for c in man.decompose():
        if c.volume()>1: out=out+c
    me=out.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False)
    print(f, "gamla mått", np.round(old[f].extents,1), "nya", np.round(t.extents,1), "gamla min", np.round(old[f].bounds[0],1), "nya min", np.round(t.bounds[0],1))
    t.export('stl/'+f); print("   tät:", trimesh.load('stl/'+f).is_watertight)
for f in sorted(os.listdir('stl')):
    if f.startswith('05'): print(f, trimesh.load('stl/'+f).is_watertight)
