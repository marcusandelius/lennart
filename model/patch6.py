from lib import *
parts,P=load('parts_v5.json')
DH=18.0                                   # dosering, kammare, skiva, lock och magasin lyfts så mycket
SL=0.84                                   # rännans lutning (40°)
fl=lambda y: 3.0+SL*(y-3.4)               # rännans golv (ovansida)

# ---------- 1. DOSERARENS BAS: ny, högre ränna och 18 mm högre stomme ----------
base=M(P,'doserare_bas')
base=base-box(-15.6,15.6,3.0,51.6,4.5,44.2)                       # gamla rännan bort
ZC=6.0
lower=base^box(-200,200,-200,300,-10,ZC)
upper=(base^box(-200,200,-200,300,ZC,200)).translate([0,0,DH])
mid=base.slice(ZC).extrude(DH).translate([0,0,ZC])
base=lower+mid+upper
TOP=44.0+DH
def yzp(pts,x0,x1): return yz_prism(pts,x0,x1)
floor=yzp([(3.4,fl(3.4)),(51.6,fl(51.6)),(51.6,fl(51.6)-2.6),(6.5,0.0),(3.4,0.0)],-15.4,15.4)
wall_profile=[(3.4,0.0),(6.5,0.0),(51.6,fl(51.6)-2.6),(51.6,TOP),(27.0,TOP),(24.0,fl(24)+36),(3.4,fl(3.4)+36)]
walls=yzp(wall_profile,13.0,15.4)+yzp(wall_profile,-15.4,-13.0)
back=box(-15.4,15.4,51.6,54.0,fl(51.6)-2.6,TOP)                    # bakvägg i fallschaktet
rib=yzp([(6.5,0.0),(51.6,0.0),(51.6,fl(51.6)-2.5),(6.5,0.05)],-0.7,0.7)   # stödribba under golvet (skrivs ut utan stöd)
base=base+floor+walls+back+rib
put(parts,P,'doserare_bas',base,note='ASA (inte CF). Rännan är öppen upptill och rymmer nötter upp till 24 mm')
for n in ('doserare_kammare','doseringsskiva','doseringslock','avstrykare'):
    put(parts,P,n,M(P,n).translate([0,0,DH]))

# ---------- 2. MAGASINET: lyfts 18 mm och får två ben fram så det står stadigt utan skruvar ----------
hop=M(P,'notmagasin').translate([0,0,DH])
def hop_solid(o):
    sx,sy0,sy1=33+o,52-o,106+o; ux,uy0=45.6+o,40-o
    funnel=Manifold.batch_hull([box(-sx,sx,sy0,sy1,100.9,101),cylz(0,89,72.9,73,min(11.5+o,13.5))])
    flare=Manifold.batch_hull([box(-sx,sx,sy0,sy1,100.95,101),box(-ux,ux,uy0,sy1,119.9,120)])
    return (funnel+flare+box(-ux,ux,uy0,sy1,119.95,175)).translate([0,0,DH])
cav=hop_solid(0)
LID_TOP=71.0+DH
for sx in (-1,1):
    leg=cylz(sx*28,40,LID_TOP+0.2,139.0,3.2,24)+Manifold.cylinder(3,4.6,3.2,24).translate([sx*28,40,LID_TOP+0.2])   # liten fot nertill
    hop=hop+(leg-cav)
put(parts,P,'notmagasin',hop,note='ASA (inte CF), rymmer ca 0,35 liter. Står löst på locket – lyfts rakt upp')

# ---------- 3. KROPPEN: lägre nöthål, urtag i flänsen, kortare skärmfästen med stödvinklar, stöd under magnetklossarna ----------
body=M(P,'kropp')
body=body-box(-13.5,13.5,-0.1,3.3,2.9,11.6)                         # hålet i väggen går nu ner till skålens golv
body=body-box(-15.8,15.8,3.1,11.4,-0.1,4.1)                         # flänsen ger plats för rännan
for x in (-34,34):
    body=body-cyly(x,108,18.0,20.3,4.2)                             # skärmfästena 2 mm kortare
    body=body-cyly(x,108,11.5,18.1,2.0)-Manifold.cylinder(0.8,2.5,2.0,32).rotate([90,0,0]).translate([x,18.01,108])
    body=body+yzp([(3.0,104.2),(17.0,104.2),(3.0,90.2)],x-1.2,x+1.2)  # 45° stödvinkel under fästet
for sgn in (1,-1):
    for y in (30,120):
        body=body+xz_prism([(sgn*74,148.05),(sgn*82.4,148.05),(sgn*82.4,139.6)],y-7,y+7)   # 45° undersida på magnetklossen
        plus=box(-2.5,2.5,-0.6,0.6,-0.5,0.01)+box(-0.6,0.6,-2.5,2.5,-0.5,0.01)
        body=body-plus.rotate([0,sgn*90,0]).translate([sgn*(HW-TW),y,133])
put(parts,P,'kropp',body)
skal=M(P,'skal')-box(-13.5,13.5,-2.7,0.1,3.0,11.6)                   # skålens bakvägg öppnas ner till golvet
put(parts,P,'skal',skal,note='Röd ASA, samma röda som kroppen går bra')
put(parts,P,'skarmklamma',M(P,'skarmklamma').translate([0,-2,0]))

# ---------- 4. ELEKTRONIKLÅDAN: öppnas uppifrån, plattan dras rakt upp ----------
EX,EY0,EY1,EZ0,EZ1=66.0,113.0,D-TW,74.0,170.0
EBOX=[(-60,80),(60,80),(-60,164),(60,164)]
eb=box(-EX,EX,EY0,EY1,EZ0,EZ1)-box(-EX+2.4,EX-2.4,EY0+2.4,EY1+1,EZ0+2.4,EZ1+1)          # öppen upptill och mot bakväggen
rimU=(box(-EX,EX,EY1-8,EY1,EZ0,EZ1)-box(-EX+5,EX-5,EY1-9,EY1+1,EZ0+5,EZ1+1))            # förtjockad bakkant: sidor + botten
eb=eb+rimU
for (x,z) in EBOX: eb=eb+cyly(x,z,EY1-10,EY1,4.5)
groove=(box(-EX+1.4,EX-1.4,EY1-1.2,EY1+0.1,EZ0+1.4,EZ1+1)-box(-EX+3.4,EX-3.4,EY1-2,EY1+1,EZ0+3.4,EZ1+2))
eb=eb-groove
for (x,z) in EBOX: eb=eb-cyly(x,z,EY1-6.5,EY1+1,2.0)-Manifold.cylinder(0.8,2.5,2.0,32).rotate([90,0,0]).translate([x,EY1+0.01,z])
PY0=EY0+2.6                                                           # plattan står mot lådans framvägg
for sx in (-1,1):                                                     # styrskenor som håller plattan
    x0,x1=(EX-2.4-2.8,EX-2.3) if sx>0 else (-EX+2.3,-EX+2.4+2.8)
    eb=eb+box(x0,x1,PY0+3.4,PY0+5.0,EZ0+2.3,EZ1-4)
eb=eb-cylz(-20,132,EZ0-1,EZ0+3,4.5)-cylz(30,132,EZ0-1,EZ0+3,4.5)     # servokablar genom botten
put(parts,P,'elektroniklada',eb,note='ASA, minst 4 perimetrar. Sitter kvar på bakväggen – öppnas uppifrån')
gask=(box(-EX+1.6,EX-1.6,EY1-1.15,EY1,EZ0+1.6,EZ1)-box(-EX+3.2,EX-3.2,EY1-2,EY1+1,EZ0+3.2,EZ1+1))
put(parts,P,'elpackning',gask,note='TPU 95A, U-formad, ligger i spåret mot bakväggen')
# lock med kjol fram och på sidorna, genomföring för kablar
LZ=EZ1
lidE=box(-EX-2.4,EX+2.4,EY0-2.4,EY1-0.2,LZ,LZ+2.4)
lidE=lidE+(box(-EX-2.4,EX+2.4,EY0-2.4,EY1-0.2,LZ-6,LZ)-box(-EX-0.2,EX+0.2,EY0-0.2,EY1+1,LZ-7,LZ+0.1))
lidE=lidE+(box(-EX+2.7,EX-2.7,EY0+2.7,EY1-12.5,LZ-2.5,LZ)-box(-EX+4.3,EX-4.3,EY0+4.3,EY1-14.1,LZ-3,LZ+0.1))   # styrkant på undersidan
lidE=lidE-box(-11,11,122.5,133.5,LZ-3,LZ+3)-box(-14,14,119.5,136.5,LZ-3,LZ-0.001)   # plats för genomföringens fläns
put(parts,P,'ellock',lidE,color='#4A5560',group='Inredning',file='16b_elektroniklada_lock.stl',note='ASA, lyfts av för att komma åt elektroniken. Modemet tejpas ovanpå')
# monteringsplatta som glider i skenorna; Raspberry Pi 5 uppe till vänster (58 x 49 mm hålbild)
mp=box(-EX+3.0,EX-3.0,PY0,PY0+3.0,EZ0+2.6,EZ1-4)
PIX=(-54.5,3.5); PIZ=(107.5,156.5)
for x in np.arange(-50,56,10.0):
    for z in np.arange(86,160,10.0):
        if -60<=x<=30 and 102<=z<=162: continue
        mp=mp-cyly(x,z,PY0-1,PY0+4,1.7)
mp=mp-box(38,54,PY0-1,PY0+4,150,160)                                   # grepphål uppe till höger
for x in PIX:
    for z in PIZ:
        mp=mp+(cyly(x,z,PY0+2.9,PY0+7.0,3.0)-cyly(x,z,PY0+3.5,PY0+7.1,1.1))
put(parts,P,'monteringsplatta',mp,note='ASA. Dras rakt upp ur lådan med all elektronik. Pi 5 uppe till vänster, övrigt i hålrastret')
# kabelgenomföringar: två runda i botten, en avlång i locket
def rg(cx,cy,z0,z1):
    g=cylz(cx,cy,z0-1.0,z0,6.5)+cylz(cx,cy,z0,z1,4.45)+cylz(cx,cy,z1,z1+1.0,6.5)
    return g-cylz(cx,cy,z0-2,z1+2,2.2)-box(cx-0.3,cx+6.6,cy-0.15,cy+0.15,z0-2,z1+2)
gr=rg(-20,132,EZ0,EZ0+2.4)+rg(30,132,EZ0,EZ0+2.4)
top=(box(-13,13,120.5,135.5,LZ+2.4,LZ+3.4)+box(-10.95,10.95,122.55,133.45,LZ,LZ+2.4)+box(-13,13,120.5,135.5,LZ-1.0,LZ))-box(-7,7,126.4,129.6,LZ-3,LZ+5)-box(-0.2,0.2,119,127,LZ-3,LZ+5)
put(parts,P,'genomforingar',gr+top)

# ---------- 5. TAKPACKNINGEN: ligger an utan att tvinga upp taket ----------
def band(z_lo,z_hi,xmax): return [(-xmax,zu(xmax)+z_lo),(0,zu(0)+z_lo),(xmax,zu(xmax)+z_lo),(xmax,zu(xmax)+z_hi),(0,zu(0)+z_hi),(-xmax,zu(xmax)+z_hi)]
strip=xz_prism(band(0.82,2.25,HW+0.3),-0.65,TW+0.65)+xz_prism(band(0.82,2.25,HW+0.3),D-TW-0.65,D+0.65)
put(parts,P,'takpackning',strip)
json.dump(parts,open('parts_v6.json','w'))
print("klart")
