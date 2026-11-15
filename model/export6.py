from lib import *
import os, zipfile
parts,P=load('parts_v7.json')
def export(names, files, R=np.eye(4), flipz=False):
    ms=[T(P,n) for n in names]
    if flipz: R=trimesh.transformations.rotation_matrix(np.pi,[1,0,0])@R
    allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])@R
    for m,f in zip(ms,files):
        man=Manifold(Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32))).transform(A[:3,:].tolist())
        me=man.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False)
        t.export('stl/'+f)
        chk=trimesh.load('stl/'+f, process=True)
        if not chk.is_watertight:
            chk.merge_vertices(digits_vertex=3); chk.update_faces(chk.nondegenerate_faces()); chk.remove_unreferenced_vertices(); trimesh.repair.fill_holes(chk); trimesh.repair.fix_normals(chk)
            if chk.is_watertight: chk.export('stl/'+f)
            else: print("EJ TÄT:", f)
rx=lambda a: trimesh.transformations.rotation_matrix(a,[1,0,0])
export(['kropp','kropp_vit'],['05_kropp_rod.stl','05_kropp_vit.stl'])
export(['skal','skal_vit'],['07_farstukvist_rod.stl','07_farstukvist_vit.stl'])
export(['doserare_bas'],['10_doserare_bas.stl'])
export(['notmagasin'],['14_notmagasin.stl'],flipz=True)
export(['elektroniklada'],['16_elektroniklada.stl'])                       # skrivs ut stående, öppningen uppåt
export(['ellock'],['16b_elektroniklada_lock.stl'],flipz=True)              # ovansidan mot plattan
export(['elpackning'],['17_elektroniklada_packning_tpu.stl'],rx(np.pi/2))
export(['monteringsplatta'],['24_monteringsplatta.stl'],rx(np.pi/2))       # distanserna uppåt
# takpackning: fyra raka lister
L=math.hypot(85.3,85.3*K)
trimesh.util.concatenate([trimesh.creation.box([L,4.5,1.43]).apply_translation([L/2,i*8+2.25,0.715]) for i in range(4)]).export('stl/06d_takpackning_tpu.stl')
# genomföringar platt: två runda + en avlång
def rg(cx,cy,z0,z1):
    g=cylz(cx,cy,z0-1.0,z0,6.5)+cylz(cx,cy,z0,z1,4.45)+cylz(cx,cy,z1,z1+1.0,6.5)
    return g-cylz(cx,cy,z0-2,z1+2,2.2)-box(cx-0.3,cx+6.6,cy-0.15,cy+0.15,z0-2,z1+2)
top=(box(-13,13,-7.5,7.5,3.4,4.4)+box(-10.95,10.95,-5.45,5.45,1.0,3.4)+box(-13,13,-7.5,7.5,0,1.0))-box(-7,7,-1.6,1.6,-1,6)-box(-0.2,0.2,-9,-1,-1,6)
allg=rg(7,7,1.0,3.4)+rg(23,7,1.0,3.4)+top.translate([15,26,0])
toT(allg,0.1).export('stl/25_genomforingar_tpu.stl')

# ---------- 00: toleranstest + nötmall ----------
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
def text(txt,size,depth):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd).extrude(depth)
def lead(x,y,z,r): return Manifold.cylinder(0.8,r,r+0.5,32).translate([x,y,z-0.79])
Hh=8.0
tp=box(0,92,0,46,0,Hh)
tp=tp-cylz(17,23,-1,Hh+1,11.0,64)                                              # nötmall: 22 mm
tp=tp-cylz(40,12,Hh-6.0,Hh+1,2.0)-lead(40,12,Hh,2.0)                            # M3-insats
tp=tp-cylz(40,34,Hh-6.5,Hh+1,2.8)-lead(40,34,Hh,2.8)                            # M4-insats
tp=tp-cylz(56,12,Hh-3.3,Hh+1,4.95)                                              # magnetficka Ø 9,9
tp=tp-cylz(52,34,Hh-3.0,Hh+1,1.45)-cylz(60,34,Hh-3.0,Hh+1,1.25)                 # hål för tappar
def bow(sh): 
    w0,w1,Lb=3.0-sh,6.5-sh,13.0-sh
    return CrossSection([ccw([(-w1,-Lb),(-w0,0),(-w1,Lb),(w1,Lb),(w0,0),(w1,-Lb)])])
tp=tp-bow(0).extrude(3.2).translate([78,23,Hh-3.0])                             # spår för nockkil
for (txt,x,y) in (("22",17,40.5),("M3",31,12),("M4",31,34),("MAG",69,5)):
    tp=tp-text(txt,4.2,0.7).translate([x,y,Hh-0.6])
key=bow(0.06).extrude(2.95).translate([106,16,0])                               # lös nockkil
pinb=box(98,114,34,44,0,3)+cylz(102,39,2.9,6,1.4,24)+cylz(110,39,2.9,6,1.2,24)  # lösa tappar
toT(tp+key+pinb,0.1).export('stl/00_toleranstest.stl')
for f in sorted(os.listdir('stl')):
    m=trimesh.load('stl/'+f)
    if not m.is_watertight: print("EJ TÄT", f)
print(len(os.listdir('stl')),"filer")
