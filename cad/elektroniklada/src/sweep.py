import pickle, numpy as np, trimesh
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
skip=('elektroniklada','ellock','monteringsplatta','genomforingar','elpackning','doserhus','doserhjul','notmagasin','skarmklamma',
      'tak_v','tak_h','tak_v_vit','tak_h_vit','takpackning','nockkilar','skorsten','skorsten_krage','solskydd','solskydd_vit')
for k in skip: A.pop(k,None)
for n in ('notforrad','doserstativ','plockskiva','skivkapa','omrorare'): A['ny_'+n]=trimesh.load('../p2/ut5/asm/%s.stl'%n)
for n,f in (('skarmficka','19_skarmficka'),('regel','19b_skarmficka_regel'),('skarmkort','skarmkort_ungefar')): A[n]=trimesh.load('../ficka/ut/%s.stl'%f)
L=lambda n: trimesh.load('ut/asm/%s.stl'%n)
B,K,P=L('elbakstycke'),L('elkapa'),L('komponentplatta')
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    return abs(float(I(a,b).volume))
def sweep(name,m,others,dz_max=110,step=2.0):
    worst={}
    for dz in np.arange(0,dz_max+0.01,step):
        mm=m.copy(); mm.apply_translation([0,0,dz])
        for on,o in others.items():
            v=vol(mm,o)
            if v>0.05: worst[on]=max(worst.get(on,(0,0)),(v,dz))
    print(name, 'kollisioner:' , {k:(round(v[0],1),v[1]) for k,v in worst.items()} or 'inga')
sweep('kåpa upp (tak av)', K, dict(A, elbakstycke=B, komponentplatta=P))
sweep('platta upp (kåpa av)', P, dict(A, elbakstycke=B), dz_max=150)
# kåpan i sitt läge mot de andra
print('kåpa vs bakstycke', round(vol(K,B),2), ' kåpa vs platta', round(vol(K,P),2), ' platta vs bakstycke', round(vol(P,B),2))
