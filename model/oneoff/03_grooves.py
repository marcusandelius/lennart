# Körd 2026-11-15 i /home/claude/fix: förläng tre avbrutna plankspår runt kameraringen upp till solskyddet.
from lib import *
parts,P=load('parts_v11.json'); k=M(P,'kropp')
# profilen på ett befintligt spår, för att kopiera den exakt
for y in (0.1,0.4,0.7):
    xs=[x for x in np.arange(11.5,14.5,0.05) if (k^box(x-0.02,x+0.02,y-0.02,y+0.02,144.9,145.1)).volume()<1e-6]
    print("y=%.1f spårbredd x %.2f..%.2f"%(y,min(xs),max(xs)))
cuts=[(-15,163.0,180.0),(13,152.0,180.0),(-1,152.0,156.0)]
add=Manifold()
for x,z0,z1 in cuts: add=add+box(x-0.5,x+0.5,-0.5,0.8,z0,z1)
before=k.volume(); k2=k-add
print("borttaget material: %.1f mm3"%(before-k2.volume()))
others=Manifold()
for p in parts:
    if p['name'] not in ('kropp',): others=others+M(P,p['name'])
print("nya spår krockar med andra delar:", round((add^others).volume(),2))
put(parts,P,'kropp',k2); json.dump(parts,open('parts_v11.json','w'))
def clean(m):
    out=Manifold()
    for c in m.decompose():
        if c.volume()>1: out=out+c
    return out
ms=[T(P,n) for n in ('kropp','kropp_sockel')]
allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
A=[[1,0,0,-(lo[0]+hi[0])/2],[0,1,0,-(lo[1]+hi[1])/2],[0,0,1,-lo[2]]]
for n,f in (('kropp','05_kropp_rod.stl'),('kropp_sockel','05_kropp_sockel_gra.stl')):
    me=clean(M(P,n)).transform(A).to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False); t.export('stl/'+f)
    c=trimesh.load('stl/'+f); print(f, "tät" if c.is_watertight else "EJ TÄT", np.round(c.extents,1))
for x in (-15,-1,13):
    col=''.join('|' if (k2^box(x-0.1,x+0.1,0.05,0.35,z-0.1,z+0.1)).volume()<1e-3 else '.' for z in np.arange(140,215,1.0))
    print("x=%4d"%x, col)
