import sys, numpy as np, trimesh
import plock as K
d=sys.argv[1] if len(sys.argv)>1 else 'ut5'
P={n:trimesh.load(d+'/asm/%s.stl'%n) for n in ('omrorare','notforrad','doserstativ','plockskiva','skivkapa')}
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def vol(a,b):
    if (a.bounds[0]>b.bounds[1]).any() or (a.bounds[1]<b.bounds[0]).any(): return 0.0
    return abs(float(I(a,b).volume))
obs=('notforrad','doserstativ','plockskiva','skivkapa')
def path(label, steps):
    bad=[]; pos=np.zeros(3); n=0
    for vec,dist,st in steps:
        for t in np.arange(st, dist+1e-6, st):
            m=P['omrorare'].copy(); m.apply_translation(pos+np.array(vec)*t); n+=1
            for o in obs:
                v=vol(m,P[o])
                if v>0.5: bad.append((round(float(np.linalg.norm(pos+np.array(vec)*t)),1),o,round(v,1)))
        pos=pos+np.array(vec)*dist
    print("%s: %s (%d lägen)"%(label, "fritt hela vägen" if not bad else "KROCK %s … (%d)"%(bad[:5],len(bad)), n))
path("rakt upp längs skivans axel 60 mm", [(K.EW,60,2.0)])
path("lodrätt upp 120 mm", [((0,0,1),120,2.0)])
path("5 mm längs axeln, sedan lodrätt upp 120 mm", [(K.EW,5,1.0),((0,0,1),120,2.0)])
