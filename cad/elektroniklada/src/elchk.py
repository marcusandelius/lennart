import pickle, numpy as np, trimesh, sys
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
for k in ('elektroniklada','ellock','monteringsplatta','genomforingar','elpackning','doserhus','doserhjul','notmagasin','skarmklamma'): A.pop(k,None)
for n in ('notforrad','doserstativ','plockskiva','skivkapa','omrorare','servo_mg996r'): A['ny_'+n]=trimesh.load('../p2/ut5/asm/%s.stl'%n)
for n,f in (('skarmficka','19_skarmficka'),('regel','19b_skarmficka_regel'),('skarmkort','skarmkort_ungefar')): A[n]=trimesh.load('../ficka/ut/%s.stl'%f)
d=sys.argv[1] if len(sys.argv)>1 else 'ut'
import os
P={f[:-4]:trimesh.load(os.path.join(d,'asm',f)) for f in sorted(os.listdir(os.path.join(d,'asm'))) if f.endswith('.stl')}
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    try: return abs(float(I(a,b).volume))
    except Exception: return float('nan')
print('== överlapp mot huset och doseringen (mm3)')
n0=0
for k,m in P.items():
    for hn,hm in A.items():
        v=vol(m,hm)
        if v>0.05: print('  ',k,hn,round(v,1)); n0+=1
print('   antal', n0)
from scipy.spatial import cKDTree
def mind(a,b,pad=10):
    lo=np.maximum(a.bounds[0],b.bounds[0])-pad; hi=np.minimum(a.bounds[1],b.bounds[1])+pad
    if (lo>hi).any(): return None
    pa=a.sample(40000); pa=pa[((pa>=lo)&(pa<=hi)).all(1)]; pb=b.sample(80000); pb=pb[((pb>=lo)&(pb<=hi)).all(1)]
    if len(pa)==0 or len(pb)==0: return None
    dd,_=cKDTree(pb).query(pa); i=int(np.argmin(dd)); return float(dd[i]), pa[i]
print('== minsta avstånd (< 10 mm)')
for k,m in P.items():
    for hn,hm in A.items():
        r=mind(m,hm)
        if r and r[0]<10: print('   %-14s %-16s %5.1f mm vid %s'%(k,hn,r[0],np.round(r[1],0).tolist()))
