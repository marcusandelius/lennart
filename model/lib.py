import json, base64, numpy as np, trimesh, math
from manifold3d import Manifold, Mesh, CrossSection
def load(fn='parts_v5.json'):
    parts=json.load(open(fn)); return parts, {p['name']:p for p in parts}
def T(P,n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=True)
def M(P,n):
    t=T(P,n); return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def toT(m, minvol=0.5):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    cs=[c for c in t.split(only_watertight=False) if abs(c.volume)>=minvol]
    return trimesh.util.concatenate(cs) if cs else t
def put(parts,P,n,m,**kw):
    t=toT(m)
    if n not in P: P[n]=dict(name=n,**kw); parts.append(P[n])
    else: P[n].update(kw)
    P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
    return t
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylz(cx,cy,z0,z1,r,seg=40): return Manifold.cylinder(z1-z0,r,r,seg).translate([cx,cy,z0])
def cyly(cx,cz,y0,y1,r,seg=32): return Manifold.cylinder(y1-y0,r,r,seg).rotate([-90,0,0]).translate([cx,y0,cz])
def cylx(cy,cz,x0,x1,r,seg=32): return Manifold.cylinder(x1-x0,r,r,seg).rotate([0,90,0]).translate([x0,cy,cz])
def ccw(pts):
    a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))); return pts if a>0 else pts[::-1]
def xz_prism(pts,y0,y1): return CrossSection([ccw(pts)]).extrude(y1-y0).rotate([90,0,0]).translate([0,y1,0])
def yz_prism(pts,x0,x1): return CrossSection([ccw(pts)]).extrude(x1-x0).rotate([90,0,90]).translate([x0,0,0])
HW,D,TW,PEAK=85.0,150.0,3.2,240.0; K=80/85; zu=lambda x: PEAK-abs(x)*K
def bb(m): b=m.bounding_box(); return np.round(np.array(b).reshape(2,3),1)
