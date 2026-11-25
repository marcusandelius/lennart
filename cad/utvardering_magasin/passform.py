import pickle, json, numpy as np, trimesh
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('A_parts.pkl','rb')).items()}
I=lambda a,b: trimesh.boolean.intersection([a,b],engine='manifold')
U=lambda ms: trimesh.boolean.union(ms,engine='manifold')
c=s=np.sqrt(0.5)
def build(Cy=74.0, Cz=48.0, R=46.0, exit_deg=50.0, xs=-1):
    C=np.array([0,Cy,Cz]); eu=np.array([1.0,0,0]); ev=np.array([0,-c,s]); ew=np.array([0,s,c])
    T=np.eye(4); T[:3,0]=eu; T[:3,1]=ev; T[:3,2]=ew; T[:3,3]=C
    def loc_box(u0,u1,v0,v1,w0,w1):
        b=trimesh.creation.box(extents=[u1-u0,v1-v0,w1-w0]); b.apply_translation([(u0+u1)/2,(v0+v1)/2,(w0+w1)/2]); b.apply_transform(T); return b
    def loc_cyl(r,w0,w1,u=0,v=0):
        m=trimesh.creation.cylinder(radius=r,height=w1-w0,sections=96); m.apply_translation([u,v,(w0+w1)/2]); m.apply_transform(T); return m
    def box(x0,x1,y0,y1,z0,z1):
        b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
    P={}
    P['skal']=loc_cyl(R+2.4,-3.0,22.0)                                   # bottenplatta + lutande krage
    P['skiva']=loc_cyl(R,0.0,16.0)
    # förråd: lodräta väggar ovanför den lutande kragen
    yf=Cy-(R+2.4)*c+22.0*s; zf=Cz+(R+2.4)*s+22.0*c                         # kragens övre framkant
    yb=Cy+(R+2.4)*c+22*s; zb=Cz-(R+2.4)*s+22*c                           # kragens övre bakkant
    from shapely.geometry import Polygon
    prof=Polygon([(27.0,zf+(yf-27.0)*0.7),(27.0,185.0),(110.5,185.0),(110.5,72.0),(min(yb,145.0),72.0),(min(yb,145.0),zb),(Cy+10,Cz+12),(yf,zf)])   # förrådets profil i (y,z)
    f=trimesh.creation.extrude_polygon(prof,96.8); f.apply_transform(np.array([[0,0,1,-48.4],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float)); P['forrad']=f
    sx0,sx1=(-30.7,10.0) if xs<0 else (-10.0,30.7)
    P['servo']=U([loc_box(sx0,sx1,-9.85,9.85,-46.0,-3.0), loc_box(sx0-7.0,sx1+7.0,-9.85,9.85,-30.5,-28.0)])
    a=np.radians(exit_deg); ue=-xs*32.0*np.sin(a); ve=32.0*np.cos(a)       # utfallet på motsatt sida om servot
    e=C+ue*eu+ve*ev-3.0*ew
    ysf=Cy-9.85*c-46*s                                                    # servots framkant
    z0=e[2]-12.0; ym=ysf-5.0; zm=z0-(e[1]-ym)*1.0                          # rännans golv: 45 grader rakt fram, sedan sväng in mot mitten
    seg1=[(e[0]+dx,e[1]+dy,zz) for dx in (-14,14) for dy,zz in ((15,z0+15),(15,z0+41),(-15,z0-15),(-15,z0+11))]+[(e[0]+dx,ym+dy,zm+dz) for dx in (-14,14) for dy in (-4,4) for dz in (0,26)]
    seg2=[(e[0]+dx,ym+dy,zm+dz) for dx in (-14,14) for dy in (-4,4) for dz in (0,26)]+[(x,y,z) for x in (-14,14) for y in (3.4,9.0) for z in (3.5,30.0)]
    P['ranna']=U([trimesh.convex.convex_hull(np.array(seg1)),trimesh.convex.convex_hull(np.array(seg2))])
    P['_info']=dict(ysf=ysf,zm=zm,ym=ym,slope2=float(np.degrees(np.arctan((zm-3.5)/np.hypot(ym-6.0,e[0])))))
    return P,e,(yf,zf)
if __name__=="__main__":
    import sys
    kw=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
    P,e,(yf,zf)=build(**kw); info=P.pop("_info"); print("servots framkant y %.1f, rännans sista del lutar %.0f grader"%(info["ysf"],info["slope2"])); print("utfall vid",np.round(e,1),"kragens överkant fram",round(yf,1),round(zf,1))
    for k,m in P.items(): print("%-8s"%k,np.round(m.bounds,1).tolist())
    skip={'doserhus','doserhjul','notmagasin'}
    print("krockar (mm³):")
    tot=0
    for hn,hm in A.items():
        if hn in skip: continue
        for k,m in P.items():
            if (m.bounds[0]>hm.bounds[1]).any() or (m.bounds[1]<hm.bounds[0]).any(): continue
            try: v=I(m,hm).volume
            except Exception as ex: v=float('nan')
            if not (abs(v)<1.0): print("  ",k,"mot",hn,round(float(v),1)); tot+=abs(v) if v==v else 0
    print("summa",round(tot,1))
    print("servo mot ränna:",round(float(I(P['servo'],P['ranna']).volume),1),"| servo mot golv z<0:",round(float(P['servo'].bounds[0][2]),1))
    # fria avstånd
    for hn in ('skarmklamma','kamerafaste','elektroniklada','monteringsplatta','kropp','tak_v','tak_h','kropp_sockel'):
        hm=A[hn]; d=min(float(np.min(trimesh.proximity.closest_point(hm, m.sample(3000))[1])) for m in P.values())
        print("  minsta avstånd till %-16s %.1f mm"%(hn,d))
    pickle.dump({k:(np.asarray(m.vertices),np.asarray(m.faces)) for k,m in P.items()},open('passform.pkl','wb'))
