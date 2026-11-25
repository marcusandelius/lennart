import pickle, numpy as np, trimesh, sys
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
P={n:trimesh.load('ut/asm/%s.stl'%n) for n in ('plockskiva','doserstativ','notforrad','servo_mg996r')}
skip={'doserhus','doserhjul','notmagasin'}; tot=0
print("krockar mot huset (mm3):")
for hn,hm in A.items():
    if hn in skip: continue
    for k,m in P.items():
        if (m.bounds[0]>hm.bounds[1]).any() or (m.bounds[1]<hm.bounds[0]).any(): continue
        try: v=float(I(m,hm).volume)
        except Exception: v=float('nan')
        if not abs(v)<0.5: print("   %s mot %s: %.1f"%(k,hn,v)); tot+=abs(v) if v==v else 0
print("   summa %.1f"%tot)
print("krockar mellan de nya delarna (mm3):")
ks=list(P)
for i in range(4):
    for j in range(i+1,4): print("   %s / %s: %.2f"%(ks[i],ks[j],float(I(P[ks[i]],P[ks[j]]).volume)))
print("minsta avstånd:")
for hn in ('skarmklamma','kamerafaste','elektroniklada','ellock','monteringsplatta','kropp','tak_v','tak_h','fonsterrutor','genomforingar','kropp_sockel','skal'):
    hm=A[hn]; best=(1e9,None)
    for k,m in P.items():
        d=float(np.min(np.abs(trimesh.proximity.signed_distance(hm, m.sample(6000))))) if False else float(np.min(trimesh.proximity.closest_point(hm, m.sample(6000))[1]))
        if d<best[0]: best=(d,k)
    print("   %-16s %.1f mm (%s)"%(hn,best[0],best[1]))
for k,m in P.items(): print(k, np.round(m.bounds,1).tolist())
