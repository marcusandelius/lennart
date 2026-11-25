import pickle, numpy as np, trimesh, sys
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
d=sys.argv[1] if len(sys.argv)>1 else 'ut'
P={n:trimesh.load(d+'/asm/%s.stl'%n) for n in ('plockskiva','doserstativ','notforrad','servo_mg996r')}
OBS=['kropp','kropp_sockel','fonsterrutor','kamerafaste','elektroniklada','ellock','monteringsplatta','skarmklamma','skarmram','genomforingar','takpackning','kropp_vit']
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
def hit(m,obs=OBS):
    out={}
    for hn in obs:
        hm=A[hn]
        if (m.bounds[0]>hm.bounds[1]).any() or (m.bounds[1]<hm.bounds[0]).any(): continue
        try: v=abs(float(I(m,hm).volume))
        except Exception as e: v=float('nan')
        if not v<0.5: out[hn]=round(v,1)
    return out
if __name__=="__main__":
    for grp in (['doserstativ','servo_mg996r','plockskiva'],['notforrad']):
        print("rakt upp:",grp)
        for dz in range(0,200,4):
            tot={}
            for k in grp:
                m=P[k].copy(); m.apply_translation([0,0,dz])
                for hn,v in hit(m).items(): tot[k+'/'+hn]=v
            if tot: print("   dz %3d  %s"%(dz,tot))
