import sys, numpy as np, trimesh
import plock as K
from chk import A, P, vol, mind
L=np.load('../plock/sky_fixed.npy'); X0,Y0,RES=-88,-12,0.5
print("== punkter som ligger rakt under fasta hinder i huset (ska vara 0)")
for n,m in P.items():
    p=np.vstack([m.sample(60000), m.vertices]); ix=((p[:,0]-X0)/RES).astype(int); iy=((p[:,1]-Y0)/RES).astype(int)
    low=L[iy,ix]; b=np.isfinite(low)&(low>p[:,2]); print("   %-13s %d"%(n,int(b.sum())), ("x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f"%(p[b,0].min(),p[b,0].max(),p[b,1].min(),p[b,1].max(),p[b,2].min(),p[b,2].max())) if b.any() else "")
print("== skivan läggs i: tippas kring sin främre kant och dras bakåt (överlapp mot stativet, mm3)")
Pf=K.W([-K.RD,0,K.GAP])[0]; ax=K.EV
worst=0
for th in np.arange(0,16.5,1.5):
    m=P['plockskiva'].copy(); m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(th), -ax, Pf)); v=vol(m,P['doserstativ']); worst=max(worst,v)
    if th in (0,6,12,15): print("   tippad %4.1f grader: %.1f   (bakkanten lyft %.1f mm)"%(th,v,2*K.RD*np.sin(np.radians(th))))
R=trimesh.transformations.rotation_matrix(np.radians(15), -ax, Pf); d=R[:3,:3]@K.EU
for sh in (5,15,30,50,80):
    m=P['plockskiva'].copy(); m.apply_transform(R); m.apply_translation(d*sh); v=vol(m,P['doserstativ']); worst=max(worst,v); print("   tippad 15 grader, dragen %2d mm bakåt: %.1f"%(sh,v))
print("   största överlapp längs vägen: %.1f"%worst)
print("== omröraren: lyft 8 mm, vriden ett kvarts varv, sedan upp längs axeln")
Rq=trimesh.transformations.rotation_matrix(np.pi/2, K.EW, K.C); bad=[]
for t in np.arange(8,130,3):
    m=P['omrorare'].copy(); m.apply_transform(Rq); m.apply_translation(K.EW*t)
    for n in ('notforrad','doserstativ'):
        v=vol(m,P[n]); 
        if v>0.5: bad.append((round(float(t)),n,round(v,1)))
print("   ", "fritt hela vägen" if not bad else bad[:6])
m=P['omrorare'].copy(); m.apply_translation(K.EW*8); print("   lyft 8 mm rakt: överlapp mot förrådet %.1f"%vol(m,P['notforrad']))
print("== minsta avstånd")
REL=['kropp','kropp_sockel','fonsterrutor','kamerafaste','elektroniklada','ellock','monteringsplatta','skarmklamma','genomforingar','tak_v','tak_h','takpackning','nockkilar','kontakter']
for k,m in P.items():
    for hn in REL:
        r=mind(m,A[hn],pad=12)
        if r and r[0]<12: print("   %-13s %-16s %5.1f mm vid %s"%(k,hn,r[0],np.round(r[1],0).tolist()))
ks=list(P)
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        r=mind(P[ks[i]],P[ks[j]],pad=3)
        if r and r[0]<3: print("   %-13s %-16s %5.2f mm vid %s"%(ks[i],ks[j],r[0],np.round(r[1],0).tolist()))
