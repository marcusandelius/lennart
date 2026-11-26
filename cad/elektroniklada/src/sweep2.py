"""Komponenterna (med kontakter) mot huset och doseringen, och lyften med komponenterna på plats."""
import pickle, os, numpy as np, trimesh
from scipy.spatial import cKDTree
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
for k in ('elektroniklada','ellock','monteringsplatta','genomforingar','elpackning','doserhus','doserhjul','notmagasin','skarmklamma'): A.pop(k,None)
for n in ('notforrad','doserstativ','plockskiva','skivkapa','omrorare','servo_mg996r'): A['ny_'+n]=trimesh.load('../p2/ut5/asm/%s.stl'%n)
for n,f in (('skarmficka','19_skarmficka'),('regel','19b_skarmficka_regel'),('skarmkort','skarmkort_ungefar')): A[n]=trimesh.load('../ficka/ut/%s.stl'%f)
G={f[:-4]:trimesh.load('ut/spoken/'+f) for f in os.listdir('ut/spoken')}
L=lambda n: trimesh.load('ut/asm/%s.stl'%n)
B,K,P=L('elbakstycke'),L('elkapa'),L('komponentplatta')
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    return abs(float(I(a,b).volume))
def mind(a,b,pad=12):
    lo=np.maximum(a.bounds[0],b.bounds[0])-pad; hi=np.minimum(a.bounds[1],b.bounds[1])+pad
    if (lo>hi).any(): return None
    pa=a.sample(30000); pa=pa[((pa>=lo)&(pa<=hi)).all(1)]; pb=b.sample(120000); pb=pb[((pb>=lo)&(pb<=hi)).all(1)]
    if len(pa)==0 or len(pb)==0: return None
    d,_=cKDTree(pb).query(pa); i=int(np.argmin(d)); return float(d[i]), pa[i]
noroof={k:v for k,v in A.items() if not k.startswith(('tak','takp','nock','skorsten','solskydd'))}
print('== komponenterna mot huset och doseringen')
for g,gm in G.items():
    for hn,hm in A.items():
        v=vol(gm,hm)
        if v>0.05: print('   ÖVERLAPP',g,hn,round(v,1))
    for hn,hm in A.items():
        r=mind(gm,hm)
        if r and r[0]<4: print('   %-24s %-14s %4.1f mm vid %s'%(g,hn,r[0],np.round(r[1]).tolist()))
GU=trimesh.util.concatenate(list(G.values()))
def sweep(name,m,others,dz_max,step=2.0):
    worst={}
    for dz in np.arange(0,dz_max+0.01,step):
        mm=m.copy(); mm.apply_translation([0,0,dz])
        for on,o in others.items():
            v=vol(mm,o)
            if v>0.05: worst[on]=max(worst.get(on,(0,0)),(round(v,1),dz))
    print(name,'kollisioner:',worst or 'inga')
sweep('kåpan upp, allt inkopplat', K, dict(noroof, elbakstycke=B, komponentplatta=P, **{'k_'+k:v for k,v in G.items()}), 120)
PG=trimesh.util.concatenate([P]+list(G.values()))
sweep('plattan upp med komponenterna, kåpan av', PG, dict(noroof, elbakstycke=B), 160)
