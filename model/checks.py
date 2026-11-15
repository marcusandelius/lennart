from lib import *
import sys
fn=sys.argv[1] if len(sys.argv)>1 else 'parts_v6.json'
parts,P=load(fn)
names=[p['name'] for p in parts]
Ms={n:M(P,n) for n in names}
def inter(a,b): return (a^b).volume()
print("== KOLLISIONER I MONTERAT LÄGE (över 0,5 mm3) ==")
lst=names
for i,a in enumerate(lst):
    ba=Ms[a].bounding_box()
    for b in lst[i+1:]:
        bb_=Ms[b].bounding_box()
        if ba[0]>bb_[3] or bb_[0]>ba[3] or ba[1]>bb_[4] or bb_[1]>ba[4] or ba[2]>bb_[5] or bb_[2]>ba[5]: continue
        v=inter(Ms[a],Ms[b])
        if v>0.5: print(f"  {a} x {b}: {v:.1f}")
def U(ns): 
    m=Manifold()
    for n in ns: m=m+Ms[n]
    return m
roof=['tak_v','tak_v_vit','tak_h','tak_h_vit','skorsten','skorsten_krage','takrannor','nockkilar','takpackning']
rest=[n for n in names if n not in roof]
R=U(roof); S=U(rest); base0=inter(R,S)
print("== LYFTA TAKET rakt upp ==  (i vila:", round(base0,1),")")
for dz in (1,2,4,8,15,30,60): print(f"  +{dz} mm: {inter(R.translate([0,0,dz]),S):.1f}")
print("== ÖPPNA LUCKAN (vrids kring gångjärnet) ==")
lid=U(['lucka','lucka_vit']); others=U([n for n in names if n not in ('lucka','lucka_vit')])
for ang in (0,-15,-30,-50,-70,-90,-100):
    L=lid.translate([0,8,-32.2]).rotate([ang,0,0]).translate([0,-8,32.2]); print(f"  {ang}°: {inter(L,others):.1f}")
print("== VRIDA DOSERINGSSKIVAN ==")
disc=Ms['doseringsskiva']; o2=U(['doserare_kammare','doseringslock','avstrykare','doserare_bas','notmagasin'])
for ang in (0,30,60,90,120,150,180): print(f"  {ang}°: {inter(disc.translate([0,-64,0]).rotate([0,0,ang]).translate([0,64,0]),o2):.1f}")
print("== LYFTA MAGASINET rakt upp ==")
hop=Ms['notmagasin']; o3=U([n for n in rest if n!='notmagasin'])
for dz in (0,1,3,6,12,25,50,100,170): print(f"  +{dz}: {inter(hop.translate([0,0,dz]),o3):.1f}")
print("== LYFTA DOSERINGSLOCKET (magasinet borttaget) ==")
dl=U(['doseringslock','avstrykare']); o4=U([n for n in rest if n not in ('notmagasin','doseringslock','avstrykare')])
for dz in (0,1,3,6,12,20): print(f"  +{dz}: {inter(dl.translate([0,0,dz]),o4):.1f}")
print("== LYFTA SKIVAN (lock borttaget) ==")
o5=U([n for n in rest if n not in ('notmagasin','doseringslock','avstrykare','doseringsskiva')])
for dz in (0,2,5,10,22): print(f"  +{dz}: {inter(disc.translate([0,0,dz]),o5):.1f}")
print("== LYFTA ELEKTRONIKLOCKET och PLATTAN ==")
o6=U([n for n in rest if n not in ('ellock','genomforingar')]) if 'ellock' in Ms else None
if o6 is not None:
    for dz in (0,2,5,10): print(f"  lock +{dz}: {inter(Ms['ellock'].translate([0,0,dz]),o6):.1f}")
    o7=U([n for n in rest if n not in ('ellock','genomforingar','monteringsplatta')])
    for dz in (0,5,20,50,95): print(f"  platta +{dz}: {inter(Ms['monteringsplatta'].translate([0,0,dz]),o7):.1f}")
print("== SKRUVMEJSEL uppifrån till doserarens främre skruvar ==")
o8=U([n for n in rest])
for x in (-31.1,31.1):
    drv=cylz(x,32.9,8,235,3.0); print(f"  x={x}: {inter(drv,o8):.1f}")
