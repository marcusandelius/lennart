import pickle, numpy as np, trimesh
from PIL import Image, ImageDraw
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
RES=0.5; X0,X1,Y0,Y1=-88,88,-12,152
W=int((X1-X0)/RES); H=int((Y1-Y0)/RES)
import shapely, shapely.affinity
GX,GY=np.meshgrid(X0+(np.arange(W)+0.5)*RES, Y0+(np.arange(H)+0.5)*RES)
def lowmap(names, z0=12.0, z1=215.0, dz=1.0):
    low=np.full((H,W),np.inf)
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
            low[a&(low>z)]=z
    return low
if __name__=="__main__":
    fixed=['kropp','kropp_vit','fonsterrutor','elektroniklada','monteringsplatta','genomforingar','takpackning']
    L=lowmap(fixed); np.save('sky_fixed.npy',L)
    for n in ('skarmklamma','kamerafaste','ellock','skarmram'): np.save('sky_%s.npy'%n, lowmap([n]))
    # skriv ut karta (2 mm rutor): lägsta hinder ovanför z=12
    step=int(4/RES)
    print("lägsta hinder över z=12 (dm-siffra av z/20; . = fritt), x från -88 till 88 →, y uppifrån 152 ned till -12")
    for j in range(H-1,-1,-step):
        row=''
        for i in range(0,W,step):
            v=L[j:j+step,i:i+step].min() if j+step<=H else L[j,i]
            row+='.' if np.isinf(v) else chr(ord('0')+int(min(v,199)//20))
        print('%4d '%(Y0+j*RES), row)
