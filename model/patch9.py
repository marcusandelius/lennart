from lib import *
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
parts,P=load('parts_v8.json')
GREEN="#2F5D3A"; WHITE="#F2EDE1"; STONE="#8C9094"; RED="#8E2A22"
def text(txt,size,depth):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd).extrude(depth)
def add(name,m,color,var,note):
    put(parts,P,name,m,color=color,group='Skål',file='koncept',note=note)
    d=[p for p in parts if p['name']==name][0]; d['var']=var; d['concept']=True
for p in parts:
    if p['name'] in ('skal','skal_vit','lucka','lucka_vit','servokapa','servopackning'): p['var']=[0]
DW=14.5; DT=2.4; DTOP=36.0
# ---- gemensamt för dörrvarianterna: foder, namnskylt ----
def casing(left=True,right=True):
    c=box(-19,19,-3,0,DTOP+0.6,DTOP+4.2)+xz_prism([(-21,DTOP+4.2),(21,DTOP+4.2),(21,DTOP+5.6),(0,DTOP+10.5),(-21,DTOP+5.6)],-3.4,0)
    if left: c+=box(-19,-DW-0.4,-3,0,0,DTOP+0.6)
    if right: c+=box(DW+0.4,19,-3,0,0,DTOP+0.6)
    return c
sign=box(-24,24,-2.2,0,50,61)
letters=text("LENNART",6.2,0.9).rotate([90,0,0]).translate([0,-2.1,55.5])
def post(x0,x1):      # vit stolpe med hatt, rymmer dörrservot
    return box(x0,x1,-24,0,0,40)+Manifold.batch_hull([box(x0-1.4,x1+1.4,-25.4,0,40,41.5),box((x0+x1)/2-2,(x0+x1)/2+2,-14,-10,47,47.5)])
def planks(x0,x1,z0,z1,y):  # spår mellan brädorna på dörrens utsida
    m=Manifold()
    for x in np.arange(x0+5.8,x1-2,5.8): m+=box(x-0.35,x+0.35,y-0.5,y+0.01,z0,z1)
    return m
def slab(y0,y1,top,dish_y):
    s=box(-28,28,y0,y1,0,top)-Manifold.sphere(40,96).translate([0,dish_y,top+40-2.2])
    return s
# ---- 1. VINDBRYGGAN: dörren fälls ner och blir nötens ramp ----
AX1=(-1.2,1.8)
d1=box(-DW,DW,-DT,0,AX1[1]-1.2,DTOP)-planks(-DW,DW,AX1[1],DTOP,-DT+0.5)
d1+=box(-DW,-DW+1.6,0,2.2,6,DTOP-2)+box(DW-1.6,DW,0,2.2,6,DTOP-2)          # sarger på insidan: håller nöten kvar på rampen
d1v=box(-DW,DW,-DT-0.8,-DT,DTOP-4,DTOP)+box(-DW,DW,-DT-0.8,-DT,AX1[1]+1,AX1[1]+5)   # tvärslåar
d1v+=xz_prism([(-DW,AX1[1]+5),(-DW+4,AX1[1]+5),(DW,DTOP-4),(DW-4,DTOP-4)],-DT-0.8,-DT)  # snedsträva
add('v1_dorr',d1,GREEN,[1],'Koncept. Dörren är också rampen: nöten rullar ut på dörrens insida')
add('v1_dorr_vit',d1v,WHITE,[1],'Koncept')
add('v1_foder',casing(right=False)+post(DW+0.6,DW+26),WHITE,[1],'Koncept. Stolpen rymmer samma luckservo som i dag')
add('v1_trappsten',slab(-74,-38,1.4,-56),STONE,[1],'Koncept. Gropen fångar nöten')
# ---- 2. STUGDÖRREN: sidohängd dörr med hjärta ----
t=np.linspace(0,2*np.pi,60,endpoint=False)
heart=[(float(0.26*16*np.sin(a)**3), float(0.26*(13*np.cos(a)-5*np.cos(2*a)-2*np.cos(3*a)-np.cos(4*a)))) for a in t]
hz=CrossSection([heart[::-1]]).extrude(6).rotate([90,0,0]).translate([0,2,27])
d2=box(-DW,DW,-DT,0,3.2,DTOP)-planks(-DW,DW,3.2,DTOP,-DT+0.5)-hz
d2v=box(-DW,DW,-DT-0.8,-DT,DTOP-3.5,DTOP)+box(-DW,DW,-DT-0.8,-DT,3.2,6.7)+Manifold.sphere(1.9,24).translate([DW-4,-DT-1.6,17])
for z in (9,30): d2v+=box(-DW,-DW+7,-DT-0.9,-DT,z-1.1,z+1.1)                 # gångjärn
add('v2_dorr',d2,GREEN,[2],'Koncept. Sidohängd, servots axel är gångjärnet')
add('v2_dorr_vit',d2v,WHITE,[2],'Koncept')
add('v2_foder',casing(left=False)+post(-DW-26,-DW-0.6),WHITE,[2],'Koncept. Stolpen rymmer dörrservot')
mat=box(-17,17,-30,-5,2.5,3.3)
add('v2_trappsten',slab(-64,-3,2.5,-45),STONE,[2,3],'Koncept. Gropen fångar nöten')
add('v2_dorrmatta',mat,RED,[2],'Koncept. Dörrmatta')
# ---- 3. SVÄNGDÖRREN: hänger i överkanten, nöten knuffar upp den själv ----
d3=box(-DW+0.6,DW-0.6,-1.6,0,3.4,DTOP-1)-planks(-DW,DW,3.4,DTOP-1,-1.1)
ring=(cylz(0,0,0,0.8,6.5,48)-cylz(0,0,-1,2,4.6,48)).rotate([90,0,0]).translate([0,-1.6,22])
d3v=ring+box(-DW+0.6,DW-0.6,-2.4,-1.6,3.4,6.4)
add('v3_dorr',d3,GREEN,[3],'Koncept. Lätt lucka på två tappar, inget servo')
add('v3_dorr_vit',d3v,WHITE,[3],'Koncept')
roofl=Manifold.batch_hull([box(-23,23,-1,0,DTOP+12,DTOP+13.5),box(-23,23,-17,-16,DTOP+5,DTOP+6.5)])
add('v3_foder',casing(),WHITE,[3],'Koncept')
add('v3_skarmtak',roofl+yz_prism([(0,DTOP+5),(-12,DTOP+5.6),(0,DTOP+11)],-21,-19)+yz_prism([(0,DTOP+5),(-12,DTOP+5.6),(0,DTOP+11)],19,21),"#5A5E62",[3],'Koncept. Skärmtak som håller regnet från luckan')
add('v_skylt',sign,WHITE,[1,2,3],'Koncept. Namnskylt över dörren')
add('v_skylt_text',letters,RED,[1,2,3],'Koncept')
json.dump(parts,open('parts_v9.json','w')); print(len(parts),"delar")
