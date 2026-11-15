import json, base64, numpy as np, trimesh, zipfile, os
from manifold3d import Manifold, Mesh
parts=json.load(open('parts_v2.json')); P={p['name']:p for p in parts}
def get(n):
    p=P[n]; v=np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3); f=np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3)
    t=trimesh.Trimesh(v,f,process=True); return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def tm(m):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    return trimesh.util.concatenate([c for c in t.split(only_watertight=False) if abs(c.volume)>=1.0])
def put(n,m):
    t=tm(m); P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylx(cy,cz,x0,x1,r,seg=20): return Manifold.cylinder(x1-x0,r,r,seg).rotate([0,90,0]).translate([x0,cy,cz])
HW=85.0
fb=get('blomlador'); body=get('kropp')
hooks=Manifold(); pins=Manifold(); fill=Manifold()
for s in (1,-1):
    X=lambda a,b: (a,b) if s>0 else (-b,-a)
    for yp in (62,88):
        pins += cylx(yp,57,*X(HW-3.0,HW+0.05),1.55)            # gamla tappar bort
        fill += cylx(yp,57,*X(HW-2.75,HW-0.01),1.7)             # gamla hål i väggen fylls igen
    for y in (60.5,89.5):                                          # krokar som hakar över fönstrets nedre karm
        hooks += box(*X(HW+2.2,HW+3.8),y-2.5,y+2.5,56.0,72.0)    # arm upp från lådans botten, utanför karmen
        hooks += box(*X(HW+0.3,HW+3.8),y-2.5,y+2.5,70.3,72.0)    # överliggare som vilar på karmens överkant
fb=(fb-pins)+hooks
put('blomlador',fb)
put('blomlador_vaxter', get('blomlador_vaxter')-hooks.translate([0,0,0])-box(-200,200,0,0,0,0) if False else get('blomlador_vaxter')-Manifold.batch_hull([hooks]) if False else get('blomlador_vaxter')-hooks)
put('kropp', body+fill)
P['blomlador']['note']='Vit ASA, hängs på fönstrets nedre karm med två krokar – inget lim'
json.dump(parts,open('parts_v3.json','w'))
# kollisionskontroll mot karm, rutor, växter och blommor
for a,b in [('blomlador','kropp_vit'),('blomlador','fonsterrutor'),('blomlador','kropp'),('blomlador','blomlador_vaxter'),('blomlador','blomlador_blommor_rod'),('blomlador','blomlador_blommor_vit')]:
    print(f"{a} x {b}: {(get(a)^get(b)).volume():.2f} mm3")
# utskriftsfiler för grupp 21 (bara förflyttning) och kroppen (grupp 05)
def export_group(names,files):
    ms=[]
    for n in names:
        p=P[n]; ms.append(trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=False))
    allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
    T=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for m,f in zip(ms,files): mm=m.copy(); mm.apply_transform(T); mm.export('stl/'+f); print(f, mm.is_watertight)
export_group(['blomlador','blomlador_vaxter'],['21_blomlador_vit.stl','21_blomlador_gron.stl'])
export_group(['kropp','kropp_vit'],['05_kropp_rod.stl','05_kropp_vit.stl'])
