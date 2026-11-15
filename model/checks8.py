from lib import *
import sys
fn=sys.argv[1] if len(sys.argv)>1 else 'parts_v8.json'
parts,P=load(fn); names=[p['name'] for p in parts]; Ms={n:M(P,n) for n in names}
dj=json.load(open('disp.json')); YC,ZC,DUMP,R,PD=dj['YC'],dj['ZC'],dj['DUMP'],dj['R'],dj['PD']
inter=lambda a,b:(a^b).volume()
def U(ns):
    m=Manifold()
    for n in ns: m=m+Ms[n]
    return m
print("== KOLLISIONER I MONTERAT LÄGE (över 0,5 mm3) ==")
for i,a in enumerate(names):
    ba=Ms[a].bounding_box()
    for b in names[i+1:]:
        b2=Ms[b].bounding_box()
        if ba[0]>b2[3] or b2[0]>ba[3] or ba[1]>b2[4] or b2[1]>ba[4] or ba[2]>b2[5] or b2[2]>ba[5]: continue
        v=inter(Ms[a],Ms[b])
        if v>0.5: print(f"  {a} x {b}: {v:.1f}")
rot=lambda m,ang: m.translate([0,-YC,-ZC]).rotate([ang,0,0]).translate([0,YC,ZC])
print("== VRIDA HJULET 0–130° =="); o=U(['doserhus','notmagasin'])
print("  ", [round(inter(rot(Ms['doserhjul'],a),o),1) for a in (0,20,40,60,80,100,120,130)])
roof=['tak_v','tak_v_vit','tak_h','tak_h_vit','skorsten','skorsten_krage','takrannor','nockkilar','takpackning']
rest=[n for n in names if n not in roof]
print("== LYFTA TAKET ==", [round(inter(U(roof).translate([0,0,dz]),U(rest)),1) for dz in (1,5,20,60)])
print("== LYFTA MAGASINET =="); o3=U([n for n in rest if n!='notmagasin'])
print("  ", [round(inter(Ms['notmagasin'].translate([0,0,dz]),o3),1) for dz in (0,2,6,15,40,100,170)])
print("== LYFTA HJULET (magasinet borta, servot ute) =="); o4=U([n for n in rest if n not in ('notmagasin','doserhjul')])
print("  ", [round(inter(Ms['doserhjul'].translate([0,0,dz]),o4),1) for dz in (0,3,10,40,120)])
print("== SKRUVMEJSEL uppifrån ==")
o5=U(rest); o5b=U([n for n in rest if n!='notmagasin'])
for (x,y,z0,what,env_) in ((-20.3,27.5,102.5,'magasinets skruv v',o5),(21.8,27.5,102.5,'magasinets skruv h',o5),(-31.1,32.9,6,'doserhusets skruv v (magasinet borta)',o5b),(31.1,32.9,6,'doserhusets skruv h (magasinet borta)',o5b)):
    print(f"   {what}: {inter(cylz(x,y,z0,236,3.0),env_):.1f}")
print("== ÖPPNA LUCKAN ==")
lid=U(['lucka','lucka_vit']); others=U([n for n in names if n not in ('lucka','lucka_vit')])
print("  ", [round(inter(lid.translate([0,8,-32.2]).rotate([a,0,0]).translate([0,-8,32.2]),others),1) for a in (0,-30,-60,-95)])
print("== NÖTENS VÄG: ur fickan, genom rännan, ut i skålen ==")
A=math.atan(0.84); CA,SA=math.cos(A),math.sin(A); fl=lambda y: 3.0+0.84*(y-3.4)
env=Ms['doserhus']+rot(Ms['doserhjul'],DUMP)+Ms['notmagasin']+Ms['kropp']+Ms['kropp_sockel']+Ms['kropp_vit']+Ms['skal']+Ms['skal_vit']
env=env+(lid.translate([0,8,-32.2]).rotate([-95,0,0]).translate([0,-8,32.2]))
for Dn in (18,20,22):
    r=Dn/2; bad=[]
    # kulan rullar på golvlinjen: centrum = golvpunkt + r * normal
    y_sw=3.4+(r-CA*r)/0.84
    y_start=YC+12.5*SA-CA*math.sqrt((R-PD+r)**2-(12.5-r)**2)        # nöten ligger i fickans botten när hjulet står i tömläge
    pts=[(yf-SA*r, fl(yf)+CA*r) for yf in np.arange(y_start,y_sw,-1.0)]+[(y,3.0+r) for y in np.arange(y_sw-SA*r,-30,-1.5)]
    for c in pts:
        v=inter(Manifold.sphere(r-0.5,48).translate([0,c[0],c[1]]),env)
        if v>0.5: bad.append((round(c[0],1),round(c[1],1),round(v,1)))
    print(f"   Ø{Dn}: {'fri väg' if not bad else bad[:5]}")
print("== NÖT I FICKAN, hjulet i viloläge och under vridning ==")
for Dn in (18,22):
    r=Dn/2; rc=R-PD+r     # nötens centrum från axeln
    res=[]
    for ang in (0,30,60,90,120,130):
        a=math.radians(ang); c=(YC-rc*math.sin(a), ZC+rc*math.cos(a))
        res.append(round(inter(Manifold.sphere(r-0.15,48).translate([0,c[0],c[1]]), Ms['doserhus']+Ms['notmagasin']+rot(Ms['doserhjul'],ang)),1))
    print(f"   Ø{Dn}: {res}")
