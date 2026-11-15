from lib import *
from manifold3d import JoinType
import os
parts,P=load('parts_v11base.json')
body=M(P,'kropp'); white=M(P,'kropp_vit')
pcs=white.decompose()
fins=[c for c in pcs if c.volume()<300]                      # två små fästen för kamerans solskydd: blir röda och sitter i kroppen
pcs=[c for c in pcs if c.volume()>=300]
for f in fins: body=body+f
R_BIG,R_SMALL,GAP=1.4,1.2,0.05                                 # tappar Ø2,8/Ø2,4 i hål Ø2,9/Ø2,5: samma par som i toleranstestet
V=np.array([0,0,1.0])
def frame(o): W=np.array(o,float); return np.cross(V,W),V,W
def place(m,o,c):
    U,Vv,W=frame(o); return m.transform([[U[0],Vv[0],W[0],c[0]],[U[1],Vv[1],W[1],c[1]],[U[2],Vv[2],W[2],c[2]]])
def teardrop(r,depth):                                         # spetsen nedåt: tappen skrivs ut liggande från den stående väggen utan överhäng
    pts=[(r*math.cos(a),r*math.sin(a)) for a in np.linspace(math.radians(-45),math.radians(225),40)]+[(0,-r*math.sqrt(2))]
    return CrossSection([ccw(pts)]).extrude(depth)
def classify(c):
    b=c.bounding_box()
    if b[4]<=0.05 or (b[1]<-0.5 and b[4]<20): return (0,-1,0),0.0,'y'
    if b[4]>150.5: return (0,1,0),150.0,'y'
    if b[3]<=-84.9: return (-1,0,0),-85.0,'x'
    return (1,0,0),85.0,'x'
def slab(ax,a,b_):
    lo,hi=min(a,b_),max(a,b_); big=400
    return box(lo,hi,-big,big,-big,big) if ax=='x' else box(-big,big,lo,hi,-big,big)
red=body
new_white=[]; pegs=Manifold(); pockets=Manifold(); report=[]; meta=[]
for i,c in enumerate(pcs):
    o,w,ax=classify(c); oo=np.array(o,float); ai='xy'.index(ax)
    b=c.bounding_box(); t=abs((b[1] if o[1]<0 else b[4]) - w) if ax=='y' else abs((b[0] if o[0]<0 else b[3]) - w)
    corner=(b[5]-b[2])>150
    small=c.volume()<600
    PK=min(1.4,max(1.0,3.0-t))                                 # fickans djup i väggen
    CL=0.05 if small else 0.1                                  # spel runt delen i fickan
    # fickan: delens kontur sedd rakt framifrån, sänkt PK mm in i väggen. Delen fylls ut i fickan där det finns vägg.
    U,Vv,W=frame(o); p0=np.zeros(3); p0[ai]=w
    Rm=np.array([U,Vv,W]); to_loc=np.c_[Rm,-Rm@p0]; to_w=np.c_[Rm.T,p0]
    sil=c.transform(to_loc.tolist()).project()
    ext=sil.extrude(PK).translate([0,0,-PK]).transform(to_w.tolist())^red
    pk=sil.offset(CL,JoinType.Miter).extrude(PK+0.02).translate([0,0,-PK]).transform(to_w.tolist())
    c2=c+ext
    pockets=pockets+pk
    # tappar: där delen är minst 3 mm tjock och väggen bakom fickan är hel
    floor=w-o[ai]*PK; r=R_SMALL if c.volume()<1500 else R_BIG
    us=np.arange((b[0] if ax=='y' else b[1])+r+1.2,(b[3] if ax=='y' else b[4])-r-1.2,1.5)
    zs=np.arange(max(b[2],12.0)+r+2,b[5]-r-1.0,1.5)
    cand=[]
    for u in us:
        for z in zs:
            p=np.zeros(3); p[0 if ax=='y' else 1]=u; p[2]=z; p[ai]=floor
            po=place(Manifold.cylinder(3.0,r+0.8,r+0.8,24),o,p); pi=place(Manifold.cylinder(1.6,r+0.8,r+0.8,24),tuple(-oo),p)
            if (po^c2).volume()>po.volume()*0.995 and (pi^red).volume()>pi.volume()*0.995: cand.append(p)
    sel=[]
    if cand:
        cand=np.array(cand); n=3 if (corner or c.volume()>2500) else 2
        d=np.linalg.norm(cand[:,None]-cand[None],axis=2); i0,i1=np.unravel_index(d.argmax(),d.shape); sel=[i0,i1]
        while len(sel)<min(n,len(cand)):
            dm=np.min(np.linalg.norm(cand[:,None]-cand[sel][None],axis=2),axis=1); sel.append(int(dm.argmax()))
        for p in cand[sel]:
            pegs=pegs+place(teardrop(r,2.0),o,p)
            c2=c2-place(teardrop(r+GAP,2.3).translate([0,0,-0.01]),o,p)
    report.append((i,ax,o,'tjocklek %.1f'%t,'ficka %.1f'%PK,'Ø%.1f'%(2*r),len(cand),[tuple(np.round(p,1)) for p in (cand[sel] if len(sel) else [])]))
    new_white.append(c2); meta.append(dict(o=o,w=floor,ax=ax,corner=corner,pegs=len(sel)))
for r_ in report: print(r_)
body2=(red-pockets)+pegs
allw=Manifold()
for c in new_white: allw=allw+c
print("vit ∩ kropp:", round((allw^body2).volume(),2), "| kroppens minsta väggrest bakom fickorna ska vara ≥1,8 mm")
put(parts,P,'kropp',body2)
put(parts,P,'kropp_vit',allw,file='05e_vit_*.stl',note='Vit PETG. Nio delar som skrivs ut liggande och trycks in i fickor med tappar i kroppen')
json.dump(parts,open('parts_v11.json','w'))
# export: hörnbrädor med framsidan nedåt, övriga med baksidan nedåt
for f in os.listdir('stl'):
    if f.startswith('05e_') or f=='05_kropp_vit.stl': os.remove('stl/'+f)
cnt={}
for c,m_ in zip(new_white,meta):
    o=m_['o']; U,Vv,W=frame(o)
    Wd = -W if m_['corner'] else W                             # w uppåt från plattan
    Ud = np.cross(V,Wd); R=np.array([Ud,V,Wd]); m=c.transform(np.c_[R,np.zeros(3)].tolist()); bb=m.bounding_box()
    m=m.translate([-(bb[0]+bb[3])/2,-(bb[1]+bb[4])/2,-bb[2]])
    b=c.bounding_box()
    kind='hornbrada' if m_['corner'] else 'sidofonster' if m_['ax']=='x' else 'skarmfonster' if b[2]>80 and b[5]<150 else 'dorroverstycke' if b[5]<45 else 'kamerakrage'
    cnt[kind]=cnt.get(kind,0)+1; nm=f"05e_vit_{kind}{'_'+str(cnt[kind]) if kind in ('hornbrada','sidofonster') else ''}.stl"
    toT(m,0.1).export('stl/'+nm); t=trimesh.load('stl/'+nm)
    print(nm,"tät" if t.is_watertight else "EJ TÄT",np.round(t.extents,1),"tappar:",m_['pegs'])

def export(names, files):
    ms=[T(P,n) for n in names]
    allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for n,f in zip(names,files):
        man=M(P,n).transform(A[:3,:].tolist())
        t=toT(man,1.0); t.export('stl/'+f)
        chk=trimesh.load('stl/'+f)
        print(f, "tät" if chk.is_watertight else "EJ TÄT", np.round(chk.extents,1))
export(['kropp','kropp_sockel'],['05_kropp_rod.stl','05_kropp_sockel_gra.stl'])
for f in os.listdir('stl'):
    if f.startswith('05e_'):
        m=trimesh.load('stl/'+f, process=True); cs=[c for c in m.split(only_watertight=False) if abs(c.volume)>1 and c.is_watertight]
        trimesh.util.concatenate(cs).export('stl/'+f)
        print(f, trimesh.load('stl/'+f).is_watertight)
