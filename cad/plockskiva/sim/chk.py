import pickle, sys, numpy as np, trimesh
from scipy.spatial import cKDTree
import plock as K
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
d=sys.argv[1] if len(sys.argv)>1 else 'ut'
NAMES=('plockskiva','doserstativ','skivkapa','omrorare','notforrad','servo_mg996r')
P={n:trimesh.load(d+'/asm/%s.stl'%n) for n in NAMES}
def bx(x0,x1,y0,y1,z0,z1):
    m=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
A['kontakter']=bx(-26,26,12,27,97.8,131.0)   # antagen plats för skärmens kontakter med vinklade stiftlister (ligger längs kortet, uppåt)
KABEL=bx(-27,27,12,27,96,131)
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    try: return abs(float(I(a,b).volume))
    except Exception: return float('nan')
SKIP={'doserhus','doserhjul','notmagasin'}
HOUSE=[n for n in A if n not in SKIP]
def near(m,lo,hi):
    t=m.triangles; ok=((t.max(axis=1)>=lo).all(axis=1))&((t.min(axis=1)<=hi).all(axis=1))
    return trimesh.Trimesh(m.vertices,m.faces[ok],process=False) if ok.any() else None
def samp(m,dens=4.0):
    n=int(min(max(m.area*dens,3000),120000)); return np.vstack([m.sample(n),m.vertices[np.unique(m.faces)]])
def mind(a,b,pad=9):
    lo=np.maximum(a.bounds[0],b.bounds[0])-pad; hi=np.minimum(a.bounds[1],b.bounds[1])+pad
    if (lo>hi).any(): return None
    a2=near(a,lo,hi); b2=near(b,lo,hi)
    if a2 is None or b2 is None: return None
    pa=samp(a2); pb=samp(b2); dd,ii=cKDTree(pb).query(pa); i=int(np.argmin(dd)); return float(dd[i]),pa[i]
what=sys.argv[2] if len(sys.argv)>2 else 'fit,dist,in,rot'
if 'fit' in what:
    print("== överlapp mot huset (mm3), bara de som inte är noll")
    for k,m in P.items():
        for hn in HOUSE:
            v=vol(m,A[hn])
            if not v<0.5: print("   %s / %s: %.1f"%(k,hn,v))
    print("== överlapp mellan de nya delarna (mm3)")
    ks=list(P)
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            v=vol(P[ks[i]],P[ks[j]])
            if not v<0.05: print("   %s / %s: %.2f"%(ks[i],ks[j],v))
if 'dist' in what:
    print("== minsta avstånd (< 9 mm)")
    REL=['kropp','kropp_sockel','fonsterrutor','kamerafaste','elektroniklada','ellock','monteringsplatta','skarmklamma','genomforingar','tak_v','tak_h','takpackning','nockkilar','kontakter']
    for k,m in P.items():
        for hn in REL:
            r=mind(m,A[hn])
            if r and r[0]<9: print("   %-13s %-16s %5.1f mm vid %s"%(k,hn,r[0],np.round(r[1],0).tolist()))
if 'in' in what:
    FIX=['kropp','kropp_sockel','kropp_vit','fonsterrutor','elektroniklada','ellock','monteringsplatta','genomforingar','takpackning']
    def sweep(parts, obs, vec, steps, label):
        bad=[]
        for t in steps:
            for k in parts:
                m=P[k].copy(); m.apply_translation(np.array(vec)*t)
                for hn,hm in obs.items():
                    v=vol(m,hm)
                    if not v<0.5: bad.append((round(float(t),1),k,hn,round(v,1)))
        print("== %s: %s"%(label, "fritt hela vägen" if not bad else "KROCK %s ... (%d)"%(bad[:6],len(bad))))
    up=np.arange(2,200,3)
    sweep(['doserstativ','servo_mg996r','plockskiva','skivkapa'], {n:A[n] for n in FIX}, [0,0,1], up, "stativ med servo, skiva och kåpa rakt ned (klämma och kamerasläde lossade)")
    sweep(['doserstativ','servo_mg996r','plockskiva','skivkapa'], {n:A[n] for n in FIX+['skarmklamma','kamerafaste']}, [0,0,1], up, "samma, med klämma och kamerasläde kvar (väntas krocka)")
    obs={n:A[n] for n in FIX+['skarmklamma','kamerafaste','kontakter']}; obs['kabelzon']=KABEL
    for n in ('doserstativ','plockskiva','skivkapa','servo_mg996r'): obs[n]=P[n]
    sweep(['notforrad'], obs, [0,0,1], np.arange(0.5,200,2.5), "förrådet rakt upp med allt annat på plats")
    obs2={n:P[n] for n in ('notforrad','doserstativ','skivkapa')}
    sweep(['omrorare'], obs2, K.EW, np.arange(1,120,3), "omröraren upp längs skivans axel")
    
if 'rot' in what:
    R=lambda q: trimesh.transformations.rotation_matrix(q, K.EW, K.C)
    worst=0; 
    for qd in range(0,360,6):
        m=P['plockskiva'].copy(); m.apply_transform(R(np.radians(qd)))
        for n in ('doserstativ','skivkapa','notforrad','servo_mg996r'): worst=max(worst,vol(m,P[n]))
    print("== skivan vriden ett helt varv: största överlapp %.2f mm3"%worst)
    worst=0
    for qd in range(-20,180,5):          # plockläget är 0; utfallet ligger 114 grader bort, vickningen åt samma håll
        m=P['omrorare'].copy(); m.apply_transform(R(-np.radians(qd)))
        for n in ('doserstativ','skivkapa','notforrad'): 
            v=vol(m,P[n]); 
            if v>worst: worst=v; wq=(qd,n)
    print("== omröraren vriden -20..180 grader: största överlapp %.2f mm3 %s"%(worst, wq if worst>0.05 else ""))
for k,m in P.items(): print(k, np.round(m.bounds,1).tolist())
