import pickle, numpy as np, trimesh, sys
import plock as K
from chk import mind
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
F=lambda n: trimesh.load('../ficka/ut/%s.stl'%n)
A.pop('skarmklamma')
A['skarmficka']=F('19_skarmficka'); A['regel']=F('19b_skarmficka_regel'); A['skarmkort']=F('skarmkort_ungefar')
def bx(x0,x1,y0,y1,z0,z1):
    m=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
# raka Dupont-hus i hylsorna: 14 mm bakom hylsornas topp (y 21,7), 2,54 mm tjocka rader, plus 3 mm för kablarnas böj
ZC, HZ = 108.0, 17.78/2
dup=[bx(-25.4,25.4,21.7,35.7,ZC+s*HZ-1.6,ZC+s*HZ+1.6) for s in (1,-1)]
A['dupont']=trimesh.util.concatenate(dup)
P={n:trimesh.load('ut5/asm/%s.stl'%n) for n in ('plockskiva','doserstativ','skivkapa','omrorare','notforrad','servo_mg996r')}
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    try: return abs(float(I(a,b).volume))
    except Exception: return float('nan')
print("== överlapp mellan doseringen och skärmfickan, regeln, kortet och raka Dupont-kontakter (mm3)")
for k,m in P.items():
    for hn in ('skarmficka','regel','skarmkort','dupont'):
        v=vol(m,A[hn]); print("   %-13s %-11s %.1f"%(k,hn,v)) if v>0.05 else None
print("== minsta avstånd")
for k,m in P.items():
    for hn in ('skarmficka','regel','skarmkort','dupont'):
        r=mind(m,A[hn],pad=15)
        if r and r[0]<15: print("   %-13s %-11s %5.1f mm vid %s"%(k,hn,r[0],np.round(r[1],0).tolist()))
FIX=['kropp','kropp_sockel','kropp_vit','fonsterrutor','elektroniklada','ellock','monteringsplatta','genomforingar','takpackning']
def sweep(parts, obs, vec, steps, label):
    bad=[]
    for t in steps:
        for k in parts:
            m=(P[k] if k in P else A[k]).copy(); m.apply_translation(np.array(vec)*t)
            for hn,hm in obs.items():
                v=vol(m,hm)
                if v>0.5: bad.append((round(float(t),1),k,hn,round(v,1)))
    print("== %s: %s"%(label, "fritt hela vägen" if not bad else "KROCK %s … (%d)"%(bad[:5],len(bad))))
up=np.arange(1,160,3)
sweep(['skarmficka','regel','skarmkort'], dict({n:A[n] for n in ('kamerafaste',)}, **{n:P[n] for n in ('doserstativ','skivkapa','plockskiva','servo_mg996r')}), [0,0,1], up, "skärmfickan, regeln och kortet sänks ned med doseringen på plats (förrådet inte på plats)")
obs={n:A[n] for n in FIX+['skarmficka','regel','skarmkort','kamerafaste']}
for n in ('doserstativ','plockskiva','skivkapa','servo_mg996r'): obs[n]=P[n]
sweep(['notforrad'], obs, [0,0,1], np.arange(0.5,200,2.5), "förrådet rakt upp med skärmfickan, regeln och kortet på plats (utan kablar)")
obs['dupont']=A['dupont']
sweep(['notforrad'], obs, [0,0,1], np.arange(0.5,60,2.5), "förrådet rakt upp med raka Dupont-kontakter i hylsorna")
m=P['notforrad']; s=m.section(plane_origin=[0,0,108],plane_normal=[0,0,1]); 
pts=np.asarray(s.vertices); sel=pts[np.abs(pts[:,0])<25]; print("förrådets framvägg vid z 108, |x|<25: y från %.1f"%sel[:,1].min())
