import json, numpy as np, trimesh
from shapely.geometry import Polygon
U=lambda ms: trimesh.boolean.union(ms, engine="manifold"); D=lambda a,bs: trimesh.boolean.difference([a]+bs, engine="manifold")
def box(x0,x1,y0,y1,z0,z1):
    b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
def cyl(r,p0,p1,s=24):
    return trimesh.creation.cylinder(radius=r,segment=[p0,p1],sections=s)
def ext_x(poly,x0,x1):   # polygon i (y,z), extruderas längs x
    m=trimesh.creation.extrude_polygon(Polygon(poly),x1-x0)
    m.apply_transform(np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float)); 
    if m.volume<0: m.invert()
    m.apply_translation([x0-m.bounds[0][0],0,0]); return m
G=json.load(open('../render/geo_brev2.json'))
def put(k,m): G[k]=np.round(m.vertices[m.faces].reshape(-1),2).tolist()
vit=trimesh.load('/home/user/lennart/cad/brevlada/07_farstukvist_vit.stl'); vit.apply_translation([12.4,-23.6,0])
put('vit_utan', U([p for p in vit.split(only_watertight=False) if p.bounds[0][0]<39.9]))
put('servo_x', trimesh.load('../bv2/servo_ghost.stl'))
rng=np.random.default_rng(3)
# ---------- 1 vedlår
X0,X1,YF,YB=40,76,-25,-2
body=box(X0,X1,YF,YB,0,40)
body=D(body,[box(X0+2,X1-2,YF+2,YB+1,2,40)])
gro=[box(x-0.35,x+0.35,YF-0.1,YF+0.5,1,39) for x in np.arange(X0+5,X1-3,4.5)]
gro+=[box(X1-0.5,X1+0.1,y-0.35,y+0.35,1,39) for y in np.arange(YF+4.5,YB-1,4.5)]
body=D(body,gro)
knut=U([box(X0-0.6,X0+3,YF-0.6,YF+3,0,40.5),box(X1-3,X1+0.6,YF-0.6,YF+3,0,40.5),box(X1-3,X1+0.6,YB-3,YB,0,40.5)])
lock=ext_x([(YF-2.5,40),(YB,50.5),(YB,52.5),(YF-2.5,42)],X0-1.5,X1+1.5)
beslag=U([box(x-1.5,x+1.5,YF-1.0,YF-0.4,28,41) for x in (X0+8,X1-8)])
logs=[]; ends=[]
for i,(x,z,r) in enumerate([(84,4,4.0),(93,4,4.2),(88.5,11.2,3.9),(102,3.8,3.6)]):
    a=np.array([x,-26,z]); b=np.array([x+rng.uniform(-1,1),-9,z]); logs.append(cyl(r,a,b)); ends.append(cyl(r-0.3,a-[0,0.3,0],a+[0,0.2,0]))
put('a_lar',body); put('a_knut',knut); put('a_lock',lock); put('a_beslag',beslag); put('a_ved',U(logs)); put('a_vedande',U(ends))
# ---------- 2 väggbrevlåda (grund, på väggen)
X0,X1,YF,YB=40,74,-17,-2
b=box(X0,X1,YF,YB,8,48)
tak=ext_x([(YF-3,46.5),(YB,53),(YB,55),(YF-3,48.5)],X0-1.5,X1+1.5)
ram=D(box(X0+3,X1-3,YF-0.6,YF+0.1,12,40),[box(X0+3.8,X1-3.8,YF-0.7,YF+0.2,12.8,39.2)])
ink=box(X0+6,X1-6,YF-1.6,YF+0.1,42,43.6)
skylt=box(X0+9,X1-9,YF-0.8,YF+0.1,22,28)
fot=U([box(x-1.5,x+1.5,YF+2,YB,3,8.01) for x in (X0+4,X1-4)])
put('b_lada',U([b,fot])); put('b_tak',tak); put('b_ram',ram); put('b_ink',ink); put('b_skylt',skylt)
# ---------- 3 odlingslåda med växter
X0,X1,YF,YB=40,76,-26,-2
o=box(X0,X1,YF,YB,0,44)
o=D(o,[box(X0-0.1,X1+0.1,YF-0.1,YB+0.1,z-0.35,z+0.35) for z in np.arange(5.5,44,5.5)])
kant=D(box(X0-1.5,X1+1.5,YF-1.5,YB,44,46),[box(X0+1.5,X1-1.5,YF+1.5,YB+1,43,47)])
jord=box(X0+1.5,X1-1.5,YF+1.5,YB-0.5,43,45.2)
gr=[]; bl=[]
for i in range(16):
    x=rng.uniform(X0+4,X1-4); y=rng.uniform(YF+4,YB-3); h=rng.uniform(6,14)
    c=trimesh.creation.cone(radius=rng.uniform(2.2,3.6),height=h,sections=10); c.apply_translation([x,y,45]); gr.append(c)
for i in range(9):
    x=rng.uniform(X0+5,X1-5); y=rng.uniform(YF+5,YB-4)
    s=trimesh.creation.icosphere(1,radius=rng.uniform(1.4,2.1)); s.apply_translation([x,y,rng.uniform(52,58)]); bl.append(s)
put('c_lada',o); put('c_kant',kant); put('c_jord',jord); put('c_gron',U(gr)); put('c_blom',U(bl))
json.dump(G,open('../render/geo_alt.json','w'))
S0=json.load(open('../render/shots_brev2.json'))[0]['o']
base=[s for s in S0['show'] if s[0] not in ('vit','tak','handtag')]+[['vit_utan','#F2F2EE']]
def shot(f,t,sub,parts): return {'file':f,'o':dict(S0,title=t,sub=sub,show=base+parts)}
shots=[shot('alt_a_vedlar.png','A. Vedlår','Låda av gråa, väderbitna stående brädor, vita knutar och lutande lock. Några vedträn bredvid.',
            [['a_lar','#8A7F70'],['a_knut','#EEEBE3'],['a_lock','#5A5E62'],['a_beslag','#1A1A1A'],['a_ved','#7A5230'],['a_vedande','#D2A86E']]),
       shot('alt_b_vaggbrevlada.png','B. Väggbrevlåda','Grund låda (15 mm djup) på väggen med snedtak, inkast och namnskylt.',
            [['b_lada','#2F4A3A'],['b_tak','#22352A'],['b_ram','#2F4A3A'],['b_ink','#1A1A1A'],['b_skylt','#EEEBE3']]),
       shot('alt_c_odlingslada.png','C. Odlingslåda','Låda av liggande brädor med växter i locket. Locket med växterna lyfts av för att komma åt servot.',
            [['c_lada','#8A6A48'],['c_kant','#EEEBE3'],['c_jord','#3B2A1E'],['c_gron','#3F7A33'],['c_blom','#E0B23A']])]
json.dump(shots,open('../render/shots_alt.json','w'),ensure_ascii=False)
# kontroll: omsluter skalen servot?
sv=trimesh.load('../bv2/servo_ghost.stl')
for n,shell in (('vedlår',U([box(40,76,-25,-2,0,40),ext_x([(-25,39.9),(-2,50.5),(-2,40),(-25,40)],40,76)])),('väggbrevlåda',box(40,74,-17,-2,8,48)),('odlingslåda',box(40,76,-26,-2,0,44))):
    print(n,'servot utanför skalet (mm³):',round(sv.volume-trimesh.boolean.intersection([sv,shell],engine='manifold').volume,1))
