import os, numpy as np, trimesh
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    try: return abs(float(I(a,b).volume))
    except Exception: return float('nan')
P={f[:-4]:trimesh.load('ut/asm/'+f) for f in os.listdir('ut/asm')}
G={f[:-4]:trimesh.load('ut/spoken/'+f) for f in os.listdir('ut/spoken')}
print('== komponenter mot lådans delar (mm3)')
for g,gm in G.items():
    for p,pm in P.items():
        v=vol(gm,pm)
        if v>0.5: print('  ',g,p,round(v,1))
print('== komponenter mot varandra')
ks=list(G)
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        v=vol(G[ks[i]],G[ks[j]])
        if v>0.5: print('  ',ks[i],ks[j],round(v,1))
print('== avstånd till kåpans insida framtill (y 113,0)')
for g,gm in G.items(): print('   %-20s främst y %.1f  (%.1f mm kvar)'%(g, gm.bounds[0][1], gm.bounds[0][1]-113.0))
