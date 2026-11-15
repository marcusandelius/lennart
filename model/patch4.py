import json, base64, numpy as np, trimesh, zipfile, os
from manifold3d import Manifold, Mesh
parts=json.load(open('parts_v3.json')); P={p['name']:p for p in parts}
def T(n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=True)
def M(t): return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def toT(m):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    return trimesh.util.concatenate([c for c in t.split(only_watertight=False) if abs(c.volume)>=0.5])
def save(n,t): P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
SHIFT, SCALE = 2.6, 0.92
def adjust(t, scale_heads):
    out=[]
    for c in t.split(only_watertight=False):
        cy=c.centroid[1]; c=c.copy()
        if scale_heads and abs(c.volume) > 20:                 # blomhuvuden: något mindre, skalas kring sin egen mitt
            ctr=c.bounding_box.centroid; c.apply_translation(-ctr); c.apply_scale(SCALE); c.apply_translation(ctr)
        if cy < 66: c.apply_translation([0, SHIFT, 0])
        elif cy > 84: c.apply_translation([0, -SHIFT, 0])
        out.append(c)
    return trimesh.util.concatenate(out)
red=adjust(T('blomlador_blommor_rod'), True); white=adjust(T('blomlador_blommor_vit'), True)
green=adjust(T('blomlador_vaxter'), False)
# grönt som hamnar utanför lådans insida (under kanten) klipps bort
box=M(T('blomlador'))
g=M(green)
inside = Manifold()
for s in (1,-1):
    x0,x1 = (86.6, 99.4) if s>0 else (-99.4,-86.6)
    inside += Manifold.cube([x1-x0, 96.4-53.6, 60]).translate([x0, 53.6, 55.9])
g = (g ^ inside) - box - M(red) - M(white)
green=toT(g)
for n,t in (('blomlador_blommor_rod',red),('blomlador_blommor_vit',white),('blomlador_vaxter',green)): save(n,t)
json.dump(parts,open('parts_v4.json','w'))
names=['blomlador','blomlador_vaxter','blomlador_blommor_rod','blomlador_blommor_vit','kropp_vit','kropp','fonsterrutor']
Ms={n:M(T(n)) for n in names}
for i,a in enumerate(names[:4]):
    for b in names[i+1:]:
        v=(Ms[a]^Ms[b]).volume()
        if v>0.05: print(f"{a} x {b}: {v:.2f}")
for n in ('blomlador_blommor_rod','blomlador_blommor_vit'):
    v=T(n).vertices; print(n, "y-utbredning", v[:,1].min().round(1), v[:,1].max().round(1))
print("lådans y:", T('blomlador').vertices[:,1].min().round(1), T('blomlador').vertices[:,1].max().round(1))
