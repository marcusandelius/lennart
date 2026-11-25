"""Utskriftskontroll lager för lager: svävande öar, ostödda ytor och tunna väggar."""
import sys, numpy as np, trimesh
from shapely.ops import unary_union
from shapely.geometry import Polygon
import shapely
LH=0.2
def layers(m):
    zs=np.arange(LH/2, m.bounds[1][2], LH)
    secs=m.section_multiplane(plane_origin=[0,0,0], plane_normal=[0,0,1], heights=zs)
    out=[]
    for z,s in zip(zs,secs):
        if s is None: out.append((z,None)); continue
        ps=[p for p in s.polygons_full if p is not None and p.area>0.01]
        # section_multiplane ger polygoner i planets egna koordinater (samma för alla lager)
        out.append((z, unary_union(ps) if ps else None))
    return out
for f in sys.argv[1:]:
    m=trimesh.load(f); L=layers(m); prev=None; isl=[]; uns=0.0; worst=(0,0); thin=(0,0); first=None
    for z,g in L:
        if g is None or g.is_empty: prev=g if g is not None else prev; continue
        if first is None: first=g.area
        if prev is not None and not prev.is_empty:
            grown=prev.buffer(LH*1.15+0.05)                       # 45 grader plus lite marginal
            for p in getattr(g,'geoms',[g]):
                if not p.intersects(prev): isl.append((round(z,1), round(p.area,1), [round(v,1) for v in p.bounds]))
            u=g.difference(grown).area; uns+=u
            if u>worst[1]: worst=(round(z,1),round(u,1))
        t=g.difference(g.buffer(-0.39).buffer(0.4)).area            # det som är smalare än 0,8 mm
        if t>thin[1]: thin=(round(z,1),round(t,1))
        prev=g
    print("%-22s höjd %.1f  första lagret %.0f mm2  svävande öar %d %s  ostödd yta totalt %.0f mm2 (värsta lagret z %.1f: %.1f mm2)  smalare än 0,8 mm som mest %.1f mm2 (z %.1f)"%(f.split('/')[-1], m.bounds[1][2], first, len(isl), isl[:4], uns, worst[0], worst[1], thin[1], thin[0]))
