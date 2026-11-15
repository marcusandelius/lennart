import trimesh, numpy as np, sys, os
from shapely.ops import unary_union
from shapely.geometry import Polygon
def layers(ms, step=0.2):
    top=max(m.bounds[1][2] for m in ms)
    for z in np.arange(0.1, top, step):
        polys=[]
        for part in ms:
            if z<part.bounds[0][2] or z>part.bounds[1][2]: continue
            sec=part.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
            if sec is None: continue
            p2,T=sec.to_planar()
            for pg in p2.polygons_full:
                e=trimesh.transform_points(np.c_[np.array(pg.exterior.coords),np.zeros(len(pg.exterior.coords))],T)[:,:2]
                hs=[trimesh.transform_points(np.c_[np.array(h.coords),np.zeros(len(h.coords))],T)[:,:2] for h in pg.interiors]
                q=Polygon(e,hs)
                if q.is_valid and q.area>0.05: polys.append(q)
        yield z, (unary_union(polys) if polys else None)
def report(files, thr=1.5):
    ms=[trimesh.load('stl/'+f) for f in files]; prev=None; out=[]
    for z,cur in layers(ms):
        if prev is not None and cur is not None:
            un=cur.difference(prev.buffer(1.2))
            for g in (list(un.geoms) if hasattr(un,'geoms') else [un]):
                if g.area>thr:
                    b=g.bounds; free=not g.buffer(0.01).intersects(prev)
                    out.append((round(z,1),round(g.area,1),round((b[0]+b[2])/2),round((b[1]+b[3])/2),round(b[2]-b[0],1),round(b[3]-b[1],1),'FRITT' if free else ''))
        prev=cur
    return out
if __name__=='__main__':
    r=report(sys.argv[1:])
    for x in r: print(x)
    print(len(r),"ställen,", sum(1 for x in r if x[-1]),"helt fristående")
