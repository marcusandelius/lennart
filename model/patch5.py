import json, base64, numpy as np, trimesh, math
from manifold3d import Manifold, Mesh, CrossSection
parts=json.load(open('parts_v4.json')); P={p['name']:p for p in parts}
def T(n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=True)
def M(n): t=T(n); return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def toT(m, minvol=0.5):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    return trimesh.util.concatenate([c for c in t.split(only_watertight=False) if abs(c.volume)>=minvol])
def put(n, m, **kw):
    t=toT(m)
    if n not in P: P[n]=dict(name=n, **kw); parts.append(P[n])
    else: P[n].update(kw)
    P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylz(cx,cy,z0,z1,r,seg=40): return Manifold.cylinder(z1-z0,r,r,seg).translate([cx,cy,z0])
def cyly(cx,cz,y0,y1,r,seg=32): return Manifold.cylinder(y1-y0,r,r,seg).rotate([-90,0,0]).translate([cx,y0,cz])
def ccw(pts):
    a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))); return pts if a>0 else pts[::-1]
def xz_prism(pts,y0,y1): return CrossSection([ccw(pts)]).extrude(y1-y0).rotate([90,0,0]).translate([0,y1,0])
HW,D,T3,PEAK=85.0,150.0,3.2,240.0; K=80/85; zu=lambda x: PEAK-abs(x)*K
COS=HW/math.hypot(HW,80); ROOF_T=6.0/COS; zo=lambda x: zu(x)+ROOF_T; X_E=113.0
ALPHA=math.degrees(math.atan(K))
body=M('kropp'); tv=M('tak_v'); th=M('tak_h'); gut=M('takrannor')

# 1) nockkilar: fjärilsformade kilar i undersidan över nocken, pressas in – inget lim
def bowtie(shrink=0.0):
    w0,w1,L = 3.0-shrink, 6.5-shrink, 13.0-shrink
    return [(-L,-w1),(0,-w0),(L,-w1),(L,w1),(0,w0),(-L,w1)]
def key_solid(yc, shrink=0.0, depth=3.0):
    pl = CrossSection([ccw([(x, y+yc) for x,y in bowtie(shrink)])]).extrude(400).translate([0,0,-100])
    band = xz_prism([(-20, zu(20)-0.01), (0, zu(0)-0.01), (20, zu(20)-0.01), (20, zu(20)+depth-shrink), (0, zu(0)+depth-shrink), (-20, zu(20)+depth-shrink)], -50, 250)
    return pl ^ band
keys=Manifold(); recess=Manifold()
for yc in (40, 110):
    recess += key_solid(yc, 0.0, 3.0); keys += key_solid(yc, 0.06, 3.0)
tv -= recess; th -= recess
# 2) skorstenens tappar: presspassning (hål r 1,45 i stället för 1,7)
for (xp,yp) in ((24,112),(38,128)):
    th = (th + cylz(xp,yp,zo(xp)-2.95,zo(xp)-0.05,1.72)) - cylz(xp,yp,zo(xp)-2.9,zo(xp)+3,1.45)
# 6) magneter: presspassning (Ø 9,9 i stället för 10,2)
def mag(sgn,y,into_roof,r,a,b):
    # cylinder från a till b mm in i materialet (räknat från ytan)
    c=Manifold.cylinder(b-a,r,r,40).translate([0,0,a]); c=c if into_roof else c.mirror([0,0,1])
    return c.rotate([0,sgn*ALPHA,0]).translate([sgn*78,y,zu(78)-(0 if into_roof else 0.3)])
for sgn in (1,-1):
    for y in (30,120):
        body = (body + mag(sgn,y,False,5.3,0.05,3.45)) - mag(sgn,y,False,4.95,-0.05,3.3)
        if sgn<0: tv = (tv + mag(sgn,y,True,5.3,0.05,3.45)) - mag(sgn,y,True,4.95,-0.05,3.3)
        else:     th = (th + mag(sgn,y,True,5.3,0.05,3.45)) - mag(sgn,y,True,4.95,-0.05,3.3)
# 3) solskyddets tappar: presspassning i fasaden (hål r 1,25 för tapp r 1,2)
HB,HS=180.0,21.0
for xp in (-12,12):
    zp=HB+(HS-abs(xp))*K+1.5
    body = (body + cyly(xp,zp,0.0,2.7,1.5)) - cyly(xp,zp,-0.1,2.7,1.25)
# 5) fönsterinsatser: rutorna blir en insats per fönster som trycks in inifrån
py=[(57,73.5),(76.5,93)]; pz=[(70,91.5),(94.5,116)]
inserts=Manifold()
for sgn in (1,-1):
    X=lambda a,b: (a,b) if sgn>0 else (-b,-a)
    plate = box(*X(HW-T3-1.6, HW-T3), 55, 95, 68, 118)
    plugs = Manifold()
    for (a,b) in py:
        for (c,d) in pz:
            body -= box(*X(HW-T3-0.1, HW-0.95), a, b, c, d)          # öppning genom väggen
            plugs += box(*X(HW-T3, HW-1.0), a, b, c, d)               # pluggen fyller öppningen, 1 mm innanför fasaden
    inserts += plate + plugs
# 4) takrännornas flikar får små hakar som klickar fast i spåret
GX=X_E-1.0; GR=6.5
for sgn in (1,-1):
    gx=sgn*GX
    hx0,hx1 = (gx-GR-0.2, gx-GR+2.2) if sgn>0 else (gx+GR-2.2, gx+GR+0.2)
    xm=(hx0+hx1)/2
    for yh in (-10,75,160):
        for side in (-1,1):
            gut += Manifold.sphere(0.6,16).scale([1.2,1,1]).translate([xm, yh+side*2.2, zu(xm)+0.6])
# 7) fötter med tapp i bottenplattan i stället för lim
plate=M('bottenplatta'); fplate=M('framgard_platta')
BX,BY0,BY1=110.0,-50.0,165.0; FY0=-170.0; BASE_H=30.0
FEET=[(-90,-30),(90,-30),(-90,145),(90,145),(-90,-150),(90,-150)]
for (x,y) in FEET[:4]: plate -= cylz(x,y,-BASE_H-3.1,-BASE_H-1.0,2.05)
for (x,y) in FEET[4:]: fplate -= cylz(x,y,-BASE_H-3.1,-BASE_H-1.0,2.05)
feet = Manifold()
for (x,y) in FEET: feet += cylz(x,y,-BASE_H-7,-BASE_H-3,10) + cylz(x,y,-BASE_H-3.01,-BASE_H-1.1,2.1)
# 8) takpackningen lite bredare så den kläms fast i spåret
def band(z_lo, z_hi, xmax):
    return [(-xmax, zu(xmax)+z_lo), (0, zu(0)+z_lo), (xmax, zu(xmax)+z_lo), (xmax, zu(xmax)+z_hi), (0, zu(0)+z_hi), (-xmax, zu(xmax)+z_hi)]
strip = xz_prism(band(0.6,2.25,HW+0.3), -0.65, T3+0.65) + xz_prism(band(0.6,2.25,HW+0.3), D-T3-0.65, D+0.65)

put('kropp', body); put('tak_v', tv); put('tak_h', th); put('takrannor', gut)
put('bottenplatta', plate); put('framgard_platta', fplate); put('fotter', feet); put('takpackning', strip)
put('nockkilar', keys, color='#5A5E62', group='Tak', file='06e_nockkilar_gra.stl', note='Grå ASA, två kilar som pressas in över nocken – inget lim')
put('fonsterrutor', inserts, file='05b_fonsterinsatser_gra.stl', note='Grå ASA, en insats per fönster som trycks in inifrån')
P['takrannor']['note']='Grå ASA, flikarna klickar fast i spåren i taket'
P['solskydd']['note']='Grå ASA, tapparna pressas in i fasaden'
P['skorsten']['note']='Röd ASA, skrivs ut upp och ner, tapparna pressas in i taket'
P['fotter']['note']='TPU 95A, tappen trycks in i bottenplattan'
json.dump(parts, open('parts_v5.json','w'))
# kollisionskontroll i monterat läge
names=['kropp','kropp_vit','fonsterrutor','tak_v','tak_h','nockkilar','takrannor','skorsten','solskydd','takpackning','bottenplatta','framgard_platta','fotter','blomlador','elektroniklada','notmagasin','kamerafaste']
Ms={n:M(n) for n in names}
for i,a in enumerate(names):
    for b in names[i+1:]:
        v=(Ms[a]^Ms[b]).volume()
        if v>0.5: print(f"{a} x {b}: {v:.1f}")
print("klart")
