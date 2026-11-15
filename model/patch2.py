import json, base64, numpy as np, trimesh, zipfile, os, math, re
from manifold3d import Manifold, Mesh, CrossSection
parts=json.load(open('parts_new.json'))
P={p['name']:p for p in parts}
def get(n):
    p=P[n]; v=np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3); f=np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3)
    t=trimesh.Trimesh(v,f,process=True)
    return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def tm(m):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    comps=[c for c in t.split(only_watertight=False) if abs(c.volume)>=1.0]; return trimesh.util.concatenate(comps)
def put(n, m, color=None, group=None, file=None, note=None):
    t=tm(m)
    if n not in P:
        P[n]=dict(name=n,color=color,group=group,file=file,note=note); parts.append(P[n])
    P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
    return t
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylx(cy,cz,x0,x1,r,seg=32): return Manifold.cylinder(x1-x0,r,r,seg).rotate([0,90,0]).translate([x0,cy,cz])
def cylz(cx,cy,z0,z1,r,seg=48): return Manifold.cylinder(z1-z0,r,r,seg).translate([cx,cy,z0])
def ccw(pts):
    a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))); return pts if a>0 else pts[::-1]
def xz_prism(pts,y0,y1): return CrossSection([ccw(pts)]).extrude(y1-y0).rotate([90,0,0]).translate([0,y1,0])
HW,D,T,PEAK=85.0,150.0,3.2,240.0; K=80/85; zu=lambda x: PEAK-abs(x)*K

# 1) servostolpen: dräneringshål, ny hatt med kjol, TPU-packning
put('skal_vit', get('skal_vit') - cylx(-15, 19.5, 63.4, 66.6, 1.5))
hat = Manifold.batch_hull([box(38.6,67.4,-31.4,-0.2,41,43), box(49,57,-19.5,-11.5,49,49.6)])
hat = hat + (box(38.6,67.4,-31.4,-0.2,36,41) - box(39.8,66.2,-30.2,1,35,42))      # kjol runt servohuset på tre sidor
put('servokapa', hat)
P['servokapa']['note']='Vit ASA, kjolen leder vattnet förbi skarven'
put('servopackning', box(40,66,-30,-0.2,40,41) - box(42,64,-28,-2.4,39,42), '#2B2B2B','Skål','09b_stolphatt_packning_tpu.stl','TPU 95A, 1 mm, mellan servohus och hatt')

# 2) takskarven: djupare spår i takets undersida + TPU-list ovanpå gavelns läpp
def band(z_lo, z_hi, xmax=HW+0.5):
    return [(-xmax, zu(xmax)+z_lo), (0, zu(0)+z_lo), (xmax, zu(xmax)+z_lo), (xmax, zu(xmax)+z_hi), (0, zu(0)+z_hi), (-xmax, zu(xmax)+z_hi)]
groove = xz_prism(band(-0.1, 2.3), -0.6, T+0.6) + xz_prism(band(-0.1, 2.3), D-T-0.6, D+0.6)
for n in ('tak_v','tak_h'): put(n, get(n) - groove)
strip = xz_prism(band(0.6, 2.25, HW+0.3), -0.45, T+0.45) + xz_prism(band(0.6, 2.25, HW+0.3), D-T-0.45, D+0.45)
put('takpackning', strip, '#2B2B2B', 'Tak', '06d_takpackning_tpu.stl', 'TPU 95A, fyra lister som läggs i takets spår')

# 3) TPU-genomföringar i elektroniklådan (två runda i botten, en avlång i taket)
def round_grommet(cx, cy, z_floor0, z_floor1):
    g = cylz(cx,cy,z_floor0-1.0,z_floor0,6.5) + cylz(cx,cy,z_floor0,z_floor1,4.45) + cylz(cx,cy,z_floor1,z_floor1+1.0,6.5)
    return g - cylz(cx,cy,z_floor0-2,z_floor1+2,2.2) - box(cx-0.3,cx+6.6,cy-0.15,cy+0.15,z_floor0-2,z_floor1+2)   # hål + slits
EZ0=74.0
gr = round_grommet(-20,132,EZ0,EZ0+2.4) + round_grommet(30,132,EZ0,EZ0+2.4)
top = (box(-13,13,120.5,135.5,170,171) + box(-10.95,10.95,122.55,133.45,167.6,170) + box(-13,13,120.5,135.5,166.6,167.6)) - box(-7,7,126.4,129.6,165,172) - box(-0.2,0.2,119,127,165,172)   # mittslits så den kan träs på kablarna
gr = gr + top
put('genomforingar', gr, '#2B2B2B', 'Inredning', '25_genomforingar_tpu.stl', 'TPU 95A, tätar kablarna in i elektroniklådan')
json.dump(parts, open('parts_v2.json','w'))

# ---- utskriftsfiler ----
def export_group(names, files, R=np.eye(4)):
    ms=[]
    for n in names:
        p=P[n]; v=np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3); f=np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3)
        ms.append(trimesh.Trimesh(v,f,process=False))
    allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    Tm=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for m,fn in zip(ms,files):
        mm=m.copy(); mm.apply_transform(Tm@R); mm.export('stl/'+fn)
n=np.sqrt(1+K*K)
export_group(['skal','skal_vit'],['07_farstukvist_rod.stl','07_farstukvist_vit.stl'])
export_group(['servokapa'],['09_stolphatt.stl'])
export_group(['servopackning'],['09b_stolphatt_packning_tpu.stl'])
export_group(['tak_v','tak_v_vit'],['06_tak_vanster_gra.stl','06_tak_vanster_vit.stl'], trimesh.geometry.align_vectors([K/n,0,-1/n],[0,0,-1]))
export_group(['tak_h','tak_h_vit'],['06b_tak_hoger_gra.stl','06b_tak_hoger_vit.stl'], trimesh.geometry.align_vectors([-K/n,0,-1/n],[0,0,-1]))
# takpackningen: fyra raka lister platt bredvid varandra
L = math.hypot(HW+0.3, (HW+0.3)*K)
strips=[trimesh.creation.box([L, T+0.9, 1.65]).apply_translation([L/2, i*7+ (T+0.9)/2, 0.825]) for i in range(4)]
trimesh.util.concatenate(strips).export('stl/06d_takpackning_tpu.stl')
# genomföringarna platt
g1=trimesh.creation.annulus(2.2, 6.5, 1.0); 
gt=tm(round_grommet(0,0,1.0,3.4)); gt.apply_translation([-gt.bounds[0][0], -gt.bounds[0][1], -gt.bounds[0][2]])
g2=gt.copy(); g2.apply_translation([16,0,0])
tp=tm(top); tp.apply_translation(-tp.bounds[0]); tp.apply_translation([0,18,0])
trimesh.util.concatenate([gt,g2,tp]).export('stl/25_genomforingar_tpu.stl')
print("klart", [p['name'] for p in parts][-4:])
