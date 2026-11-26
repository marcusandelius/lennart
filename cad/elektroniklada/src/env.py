import pickle, numpy as np, trimesh, shapely, shapely.affinity
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
RES=1.0; X0,X1,Y0,Y1=-86,86,100,152
W=int((X1-X0)/RES); H=int((Y1-Y0)/RES)
GX,GY=np.meshgrid(X0+(np.arange(W)+0.5)*RES, Y0+(np.arange(H)+0.5)*RES)
def maps(names, z0=-5, z1=260, dz=1.0):
    low=np.full((H,W),np.inf); high=np.full((H,W),-np.inf)
    for n in names:
        m=A[n]
        for z in np.arange(max(z0,m.bounds[0][2]+0.01)+0.137, min(z1,m.bounds[1][2]), dz):
            sec=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
            if sec is None: continue
            try: p2,T=sec.to_2D()
            except Exception: continue
            a=np.zeros((H,W),bool)
            for poly in p2.polygons_full:
                poly=shapely.affinity.affine_transform(poly,[T[0,0],T[0,1],T[1,0],T[1,1],T[0,3],T[1,3]])
                if not poly.is_valid: poly=poly.buffer(0)
                a|=shapely.contains_xy(poly,GX,GY)
            low[a&(low>z)]=z; high[a&(high<z)]=z
    return low, high
skip={'elektroniklada','ellock','monteringsplatta','genomforingar','elpackning','doserhus','doserhjul','notmagasin','skarmklamma'}
names=[n for n in A if n not in skip and A[n].bounds[1][1]>Y0 and A[n].bounds[0][1]<Y1]
print('delar i området:', names)
res={}
for n in names: res[n]=maps([n])
pickle.dump((res,(X0,Y0,RES,W,H)),open('envmaps.pkl','wb'))
