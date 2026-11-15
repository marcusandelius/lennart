from lib import *
import os
parts,P=load('parts_v8.json')
def export(names, files, R=np.eye(4), flipz=False):
    ms=[T(P,n) for n in names]
    if flipz: R=trimesh.transformations.rotation_matrix(np.pi,[1,0,0])@R
    allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])@R
    for m,f in zip(ms,files):
        man=Manifold(Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32))).transform(A[:3,:].tolist())
        me=man.to_mesh(); trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False).export('stl/'+f)
        chk=trimesh.load('stl/'+f, process=True)
        if not chk.is_watertight:
            chk.merge_vertices(digits_vertex=3); chk.update_faces(chk.nondegenerate_faces()); chk.remove_unreferenced_vertices(); trimesh.repair.fill_holes(chk); trimesh.repair.fix_normals(chk)
            if chk.is_watertight: chk.export('stl/'+f)
            else: print("EJ TÄT:", f)
for f in ('10_doserare_bas.stl','11_doserare_kammare.stl','12_doseringsskiva.stl','13_doseringslock.stl','20_avstrykare_tpu.stl'):
    if os.path.exists('stl/'+f): os.remove('stl/'+f)
export(['kropp','kropp_vit','kropp_sockel'],['05_kropp_rod.stl','05_kropp_vit.stl','05_kropp_sockel_gra.stl'])
export(['doserhus'],['10_doserhus.stl'])
export(['doserhjul'],['11_doserhjul.stl'],trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))   # hornurtaget mot plattan
export(['notmagasin'],['14_notmagasin.stl'],flipz=True)
# toleranstest med nötmall: 22 mm ska gå igenom, 18 mm ska inte
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
def text(txt,size,depth):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd).extrude(depth)
def lead(x,y,z,r): return Manifold.cylinder(0.8,r,r+0.5,32).translate([x,y,z-0.79])
Hh=8.0
tp=box(0,116,0,46,0,Hh)
tp=tp-cylz(16,21,-1,Hh+1,11.0,72)-cylz(43,21,-1,Hh+1,9.0,72)                    # nötmall: 22 mm och 18 mm
tp=tp-cylz(64,12,Hh-6.0,Hh+1,2.0)-lead(64,12,Hh,2.0)-cylz(64,34,Hh-6.5,Hh+1,2.8)-lead(64,34,Hh,2.8)   # M3- och M4-insats
tp=tp-cylz(80,12,Hh-3.3,Hh+1,4.95)                                              # magnetficka
tp=tp-cylz(76,34,Hh-3.0,Hh+1,1.45)-cylz(84,34,Hh-3.0,Hh+1,1.25)                 # hål för tappar
def bow(sh):
    w0,w1,Lb=3.0-sh,6.5-sh,13.0-sh
    return CrossSection([ccw([(-w1,-Lb),(-w0,0),(-w1,Lb),(w1,Lb),(w0,0),(w1,-Lb)])])
tp=tp-bow(0).extrude(3.2).translate([102,23,Hh-3.0])
for (txt,x,y,sz) in (("22",16,40.5,4.6),("18",43,40.5,4.6),("M3",56,12,4),("M4",56,34,4),("MAG",80,22,3.6)):
    tp=tp-text(txt,sz,0.7).translate([x,y,Hh-0.6])
key=bow(0.06).extrude(2.95).translate([130,16,0])
pinb=box(122,138,34,44,0,3)+cylz(126,39,2.9,6,1.4,24)+cylz(134,39,2.9,6,1.2,24)
toT(tp+key+pinb,0.1).export('stl/00_toleranstest.stl')
bad=[f for f in sorted(os.listdir('stl')) if not trimesh.load('stl/'+f).is_watertight]
print(len(os.listdir('stl')),"filer; ej täta:",bad)
