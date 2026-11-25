import pickle, numpy as np, trimesh, sys
from scipy.spatial import cKDTree
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
d=sys.argv[1] if len(sys.argv)>1 else 'ut'
P={n:trimesh.load(d+'/asm/%s.stl'%n) for n in ('plockskiva','doserstativ','notforrad','servo_mg996r')}
skip={'doserhus','doserhjul','notmagasin'}
def near(m,lo,hi):
    t=m.triangles; ok=((t.max(axis=1)>=lo).all(axis=1))&((t.min(axis=1)<=hi).all(axis=1))
    if not ok.any(): return None
    return trimesh.Trimesh(m.vertices,m.faces[ok],process=False)
def samp(m,dens=6.0):
    n=int(min(max(m.area*dens,2000),400000)); return np.vstack([m.sample(n),m.vertices[np.unique(m.faces)]])
def mind(a,b,pad=10):
    lo=np.maximum(a.bounds[0],b.bounds[0])-pad; hi=np.minimum(a.bounds[1],b.bounds[1])+pad
    if (lo>hi).any(): return None
    a2=near(a,lo,hi); b2=near(b,lo,hi)
    if a2 is None or b2 is None: return None
    pa=samp(a2); pb=samp(b2); dd,ii=cKDTree(pb).query(pa); i=int(np.argmin(dd)); return float(dd[i]),pa[i]
if __name__=="__main__":
    print("minsta avstånd per par (< 10 mm):")
    for k,m in P.items():
        for hn,hm in A.items():
            if hn in skip: continue
            r=mind(m,hm)
            if r and r[0]<10: print("  %-13s %-18s %5.1f mm vid %s"%(k,hn,r[0],np.round(r[1],1).tolist()))
    ks=list(P)
    for i in range(4):
        for j in range(i+1,4):
            r=mind(P[ks[i]],P[ks[j]]); print("  %-13s %-18s %5.1f mm vid %s"%(ks[i],ks[j],r[0],np.round(r[1],1).tolist()))
