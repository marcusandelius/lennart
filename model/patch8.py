from lib import *
parts,P=load('parts_v7.json')
# ---------- gamla doseringen bort ----------
for n in ('doserare_bas','doserare_kammare','doseringsskiva','doseringslock','avstrykare','notmagasin'):
    parts[:]=[p for p in parts if p['name']!=n]; P.pop(n,None)
INNER="#D8C59A"
# ---------- mått ----------
YC=57.0; R=31.0; WD=17.0; RP=12.1; SL=0.84
A=math.atan(SL); CA,SA=math.cos(A),math.sin(A)
fl=lambda y: 3.0+SL*(y-3.4)                                  # rännans golv
ZC=round(fl(YC)+12.5/CA,1)                                   # hjulets axel: fickans underkant linjerar med rännan i tömläget
DUMP=90+math.degrees(A)                                      # vridning från "ficka upp" till "töm"
ZT=ZC+R+3.4                                                  # doserhusets överkant
RC=R+1.0
print("axel z =",ZC," tömvinkel =",round(DUMP,1)," överkant =",round(ZT,1))
nrm=(SA,-CA)
foot=(YC+12.5*nrm[0], ZC+12.5*nrm[1]); hc=math.sqrt(RC**2-12.5**2)
PF=(foot[0]-hc*CA, foot[1]-hc*SA)                             # där rännans golv möter hjulet
foot2=(YC-12.5*nrm[0], ZC-12.5*nrm[1]); PU=(foot2[0]-hc*CA, foot2[1]-hc*SA)
up=lambda y: PU[1]-SL*(PU[0]-y)                               # rännans övre gräns
XL0,XL1=-WD-6.3,-WD-0.3                                       # vänster vägg
XR0,XR1=WD+0.3,WD+9.3                                         # höger vägg (servofäste)
Y0,Y1=YC-R-3.2,YC+R+3.2
DISP_PINS=[(31.1,95.1),(-31.1,95.1)]; DISP_SCREWS=[(-31.1,32.9),(31.1,32.9)]
def lead_z(x,y,z,r): return Manifold.cylinder(0.8,r,r+0.5,32).translate([x,y,z-0.79])

# ---------- 1. DOSERHUS: undre halvan, ränna, servofäste ----------
hus=box(-40,40,Y0+1.5,101,0,4)                                # fotplatta på styrtappar och två skruvar
hus+=box(-WD-0.3,WD+0.3,Y0,Y1,0,ZC)                           # massiv kloss under hjulet
hus+=box(XL0,XL1,Y0,Y1,0,ZT)+box(XR0,XR1,Y0,97,0,ZT)          # sidoväggar
hus-=cylx(YC,ZC,-WD-0.3,WD+0.3,RC,96)                         # hjulets säte
void=yz_prism([(3.3,3.0),PF,(YC,ZC),PU,(3.3,up(3.3))],-13.0,13.0)
hus-=void                                                     # rännans väg genom klossen
# rännan framför klossen: golv, sidoväggar, stödribba
yj=Y0+0.5
hus+=yz_prism([(3.4,0),(6.5,0),(yj,fl(yj)-2.6),(yj,fl(yj)),(3.4,3.0)],-15.4,15.4)
wp=[(3.4,0),(6.5,0),(yj,fl(yj)-2.6),(yj,up(yj)+2.0),(3.4,up(3.4)+2.0)]
hus+=yz_prism(wp,13.0,15.4)+yz_prism(wp,-15.4,-13.0)
hus+=yz_prism([(6.5,0),(yj,0),(yj,fl(yj)-2.5),(6.5,0.05)],-0.7,0.7)
# servo MG996R: ligger på sidan, axeln i hjulets centrum, flänsen mot höger vägg
SY0,SY1=YC-10.35-0.4,YC+30.35+0.4
hus-=box(XR0-0.1,XR1+0.1,SY0,SY1,ZC-10.3,ZC+10.3)
for y in ((SY0+SY1)/2-24.75,(SY0+SY1)/2+24.75):
    for z in (ZC-5,ZC+5):
        hus-=cylx(y,z,XR1-6.5,XR1+0.1,2.0)+Manifold.cylinder(0.8,2.0,2.5,32).rotate([0,90,0]).translate([XR1-0.79,y,z])
# vänster vägg: U-spår för hjulets axeltapp
hus-=box(XL0-0.1,XL1+0.1,YC-4.2,YC+4.2,ZC,ZT+1)+cylx(YC,ZC,XL0-0.1,XL1+0.1,4.2)
# fästen för magasinet: två skruvar framtill, uppifrån
HS=[((XL0+XL1)/2,Y0+4.7),((XR0+XR1)/2,Y0+4.7)]
for (x,y) in HS: hus-=cylz(x,y,ZT-6.5,ZT+0.1,2.0)+lead_z(x,y,ZT,2.0)
for (x,y) in DISP_SCREWS: hus-=cylz(x,y,-1,5,1.7)
for (x,y) in DISP_PINS: hus-=cylz(x,y,-1,5,2.25)+Manifold.cylinder(0.8,2.75,2.25,32).translate([x,y,-0.01])
put(parts,P,'doserhus',hus,color=INNER,group='Inredning',file='10_doserhus.stl',note='ASA (inte CF). Hjulets säte, rännan och servofästet i ett stycke')

# ---------- 2. DOSERHJUL: en ficka, en nöt ----------
hjul=cylx(YC,ZC,-WD,WD,R,128)
PD=21.5                                                       # fickans djup
pocket=cylz(0,YC,ZC+R-PD,ZC+R+2,RP,64)+Manifold.cylinder(1.6,RP,RP+1.6,64).translate([0,YC,ZC+R-1.9])   # fasad kant
hjul-=pocket
hjul+=cylx(YC,ZC,-WD-5.6,-WD+0.1,4.0,48)                      # axeltapp vänster
hjul-=cylx(YC,ZC,WD-3.4,WD+0.1,12.7,64)+cylx(YC,ZC,WD-9.5,WD-3.3,4.6,32)   # urtag för servots runda horn + nav
put(parts,P,'doserhjul',hjul,color="#C9A86A",group='Inredning',file='11_doserhjul.stl',note='ASA (inte CF). Fickan rymmer en nöt på 18–22 mm. Servots runda horn skruvas i urtaget')

# ---------- 3. MAGASIN: sadel över hjulet + tratt ----------
ZF=ZT+3.0; ZB=ZT+40.0; ZTOP=176.0
outer=Manifold.batch_hull([box(XL0,XR1,Y0,Y1,ZF-0.1,ZF),box(-48,48,37.6,108.4,ZB-0.1,ZB)])+box(-48,48,37.6,108.4,ZB-0.05,ZTOP)
outer+=box(XL0,XR1,Y0,Y1,ZT,ZF)                               # fläns som vilar på sidoväggarna
inner=Manifold.batch_hull([box(-13,13,YC-15,YC+15,ZT-0.1,ZT),box(-45.6,45.6,40,106,ZB-0.1,ZB)])+box(-45.6,45.6,40,106,ZB-0.05,ZTOP+1)
sadel=box(-WD,WD,Y0,Y1,ZC+0.4,ZT+0.05)-cylx(YC,ZC,-WD-1,WD+1,RC,96)
mag=(outer+sadel)-inner-box(-13,13,YC-15,YC+15,ZC,ZT+0.2)
for (x,y) in HS: mag-=cylz(x,y,ZT-1,ZF+0.1,1.7)+cylz(x,y,ZF,ZF+60,3.6)      # skruvhål + fri väg för skruvmejseln
mag+=box(-22,22,104.5,108.4,168,186)-box(-16,16,103,110,168,180)            # handtag
put(parts,P,'notmagasin',mag,color=INNER,group='Inredning',file='14_notmagasin.stl',note='ASA (inte CF), rymmer ca 0,35 liter. Två skruvar framtill, sedan lyfts det rakt upp')
cap=(inner^box(-200,200,-200,300,ZT,ZTOP)).volume()/1e6
print("magasinets volym:",round(cap,2),"liter")

# ---------- 4. EXTERIÖR: stengrund och fönsteröverstycken ----------
body=M(P,'kropp'); SH=10.0
sock=(body^box(-200,200,-200,300,-1,SH))+(box(-HW,HW,0,D,0,SH)-box(-HW+TW,HW-TW,TW,D-TW,-1,SH+1))
sock-=box(-13.5,13.5,-0.1,TW+0.1,2.9,SH+0.1)                  # nöthålet
jw,jd=0.9,0.5                                                 # fogar i stengrunden
joints=box(-HW-1,HW+1,-1,D+1,SH/2-jw/2,SH/2+jw/2)-box(-HW+jd,HW-jd,jd,D-jd,-1,SH+1)
for k,x in enumerate(np.arange(-HW+12,HW-5,24.0)):
    for (z0,z1,off) in ((0,SH/2,0),(SH/2,SH,12)):
        xx=x+off
        if abs(xx)<HW-4: joints+=box(xx-jw/2,xx+jw/2,-1,jd,z0,z1)+box(xx-jw/2,xx+jw/2,D-jd,D+1,z0,z1)
for k,y in enumerate(np.arange(12,D-5,24.0)):
    for (z0,z1,off) in ((0,SH/2,0),(SH/2,SH,12)):
        yy=y+off
        if 4<yy<D-4: joints+=box(HW-jd,HW+1,yy-jw/2,yy+jw/2,z0,z1)+box(-HW-1,-HW+jd,yy-jw/2,yy+jw/2,z0,z1)
sock-=joints
put(parts,P,'kropp',body^box(-200,200,-200,300,SH,400))
put(parts,P,'kropp_sockel',sock,color="#8C9094",group='Kropp',file='05_kropp_sockel_gra.stl',note='Grå ASA (samma som taket). Stengrunden skrivs ut i samma utskrift som kroppen')
white=M(P,'kropp_vit')
for sgn in (1,-1):                                            # överstycken på sidofönstren
    xs=(HW,HW+2.5) if sgn>0 else (-HW-2.5,-HW)
    white+=yz_prism([(50.5,119.8),(99.5,119.8),(99.5,122.6),(75,129.5),(50.5,122.6)],xs[0],xs[1])
white+=xz_prism([(-31.5,130.3),(31.5,130.3),(31.5,135.6),(0,143.5),(-31.5,135.6)],-2.8,0)   # överstycke på skärmfönstret
put(parts,P,'kropp_vit',white)
json.dump(parts,open('parts_v8.json','w'))
json.dump(dict(YC=YC,ZC=ZC,DUMP=DUMP,ZT=ZT,R=R,PD=PD),open('disp.json','w'))
print("klart,",len(parts),"delar")
