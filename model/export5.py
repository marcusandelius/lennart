import json, base64, numpy as np, trimesh, math, os, zipfile, io, re
parts=json.load(open('parts_v5.json')); P={p['name']:p for p in parts}
def T(n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=False)
K=80/85; n=math.sqrt(1+K*K)
def group(names, files, R=np.eye(4)):
    ms=[T(x) for x in names]; allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    Tm=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    from manifold3d import Manifold, Mesh
    for m,f in zip(ms,files):
        mt=trimesh.Trimesh(m.vertices,m.faces,process=True)
        man=Manifold(Mesh(vert_properties=np.asarray(mt.vertices,np.float32), tri_verts=np.asarray(mt.faces,np.uint32)))
        A=(Tm@R)[:3,:]                                        # transformen görs i manifold så topologin bevaras
        me=man.transform(A.T.tolist() if False else A.tolist()).to_mesh()
        trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False).export('stl/'+f)
group(['kropp','kropp_vit'],['05_kropp_rod.stl','05_kropp_vit.stl'])
group(['tak_v','tak_v_vit'],['06_tak_vanster_gra.stl','06_tak_vanster_vit.stl'], trimesh.geometry.align_vectors([K/n,0,-1/n],[0,0,-1]))
group(['tak_h','tak_h_vit'],['06b_tak_hoger_gra.stl','06b_tak_hoger_vit.stl'], trimesh.geometry.align_vectors([-K/n,0,-1/n],[0,0,-1]))
group(['takrannor'],['22_takrannor_gra.stl'])
group(['bottenplatta'],['03_bottenplatta.stl']); group(['framgard_platta'],['03b_framgard_bottenplatta.stl'])
# fönsterinsatser: plattan mot bädden, pluggarna uppåt
ins=T('fonsterrutor'); out=[]
for c in ins.split(only_watertight=False):
    c=c.copy(); right = c.centroid[0] > 0
    c.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2 if right else np.pi/2,[0,1,0]))
    c.apply_translation(-c.bounds[0]); c.apply_translation([0 if right else 60, 0, 0]); out.append(c)
if os.path.exists('stl/05b_fonsterrutor_gra.stl'): os.remove('stl/05b_fonsterrutor_gra.stl')
trimesh.util.concatenate(out).export('stl/05b_fonsterinsatser_gra.stl')
# nockkilar: ena benet platt mot bädden
k=T('nockkilar'); ko=[]
for i,c in enumerate(k.split(only_watertight=False)):
    c=c.copy(); c.apply_transform(trimesh.geometry.align_vectors([K/n,0,-1/n],[0,0,-1])); c.apply_translation(-c.bounds[0]); c.apply_translation([0,i*20,0]); ko.append(c)
trimesh.util.concatenate(ko).export('stl/06e_nockkilar_gra.stl')
# takpackning: fyra raka lister, 4,5 mm breda
L=math.hypot(85.3, 85.3*K)
trimesh.util.concatenate([trimesh.creation.box([L,4.5,1.65]).apply_translation([L/2, i*8+2.25, 0.825]) for i in range(4)]).export('stl/06d_takpackning_tpu.stl')
# fötter: skiva + tapp uppåt, packade (riktig union)
from manifold3d import Manifold
fm=Manifold()
for i in range(6):
    x,y=(i%3)*25,(i//3)*25
    fm += Manifold.cylinder(4,10,10,48).translate([x,y,0]) + Manifold.cylinder(1.95,2.1,2.1,24).translate([x,y,3.99])
me=fm.to_mesh(); trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts)).export('stl/04_fotter_tpu.stl')
for f in sorted(os.listdir('stl')):
    m=trimesh.load('stl/'+f)
    if not m.is_watertight: print("EJ TÄT", f)
print(len(os.listdir('stl')))
