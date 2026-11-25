"""
Plockskivan: CAD för de tre nya doseringsdelarna (husets ram, mm). Måtten kommer från plock.py, samma som simuleringen.
  11_plockskiva.stl   skivan med en ficka
  10_doserstativ.stl  lutande platta med servofäste, utfall och ränna
  14_notforrad.stl    krage, skärm och förråd i ett stycke
Kör:  python3 plock_cad.py <utkatalog>
"""
import sys, os
import numpy as np
import trimesh
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
import plock as K

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + list(bs), engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")
T = K.T; c = s = K.c
BIG = 400.0

def lcyl(r, w0, w1, u=0.0, v=0.0, n=128):
    m = trimesh.creation.cylinder(radius=r, height=w1 - w0, sections=n); m.apply_translation([u, v, (w0 + w1) / 2]); m.apply_transform(T); return m
def lbox(u0, u1, v0, v1, w0, w1):
    m = trimesh.creation.box(extents=[u1 - u0, v1 - v0, w1 - w0]); m.apply_translation([(u0 + u1) / 2, (v0 + v1) / 2, (w0 + w1) / 2]); m.apply_transform(T); return m
def box(x0, x1, y0, y1, z0, z1):
    m = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return m
def ext(poly, z0, z1):
    ms = []
    for p in getattr(poly, "geoms", [poly]):
        if p.area < 0.01: continue
        m = trimesh.creation.extrude_polygon(p, z1 - z0); m.apply_translation([0, 0, z0]); ms.append(m)
    return ms[0] if len(ms) == 1 else U(ms)
def ext_xz(poly, y0, y1):                     # polygon i (x, z), utdragen längs y
    m = trimesh.creation.extrude_polygon(poly, y1 - y0)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, -1, y1], [0, 1, 0, 0], [0, 0, 0, 1]], float)); return m
w_ge = lambda a: lbox(-BIG, BIG, -BIG, BIG, a, a + BIG)          # halvrymder i lokala koordinater
v_ge = lambda a: lbox(-BIG, BIG, a, a + BIG, -BIG, BIG)
def clean(m):
    m = trimesh.util.concatenate([q for q in m.split(only_watertight=False) if abs(q.volume) > 20.0])
    m = trimesh.Trimesh(np.round(m.vertices, 4), m.faces, process=True); m.merge_vertices(); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices(); return m

C = K.C; RD, TD, GAP, RP = K.RD, K.TD, K.GAP, K.RP; RC, WALL = K.RC, K.WALL; WS, WT, WTOP, VS = K.WS, K.WT, K.WTOP, K.VS
UF, UB, XL, ZT = K.UF, K.UB, K.XL, K.ZT; SR, ST, RX = K.SLAB_R, K.SLAB_T, K.RX
uE, vE = -RP * np.sin(K.QX), RP * np.cos(K.QX)
POCKET_R = 13.25

# ---------------------------------------------------------------- 11 plockskiva (lokala koordinater, fickan nederst = plockläget)
def disc_local():
    t = np.eye(4); m = trimesh.creation.cylinder(radius=RD, height=TD, sections=180); m.apply_translation([0, 0, GAP + TD / 2])
    cyl = lambda r, w0, w1, u=0.0, v=0.0: (lambda q: (q.apply_translation([u, v, (w0 + w1) / 2]), q)[1])(trimesh.creation.cylinder(radius=r, height=w1 - w0, sections=96))
    cone = trimesh.creation.cone(radius=POCKET_R + 3.0, height=3.0, sections=96); cone.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    cone.apply_translation([0, -RP, GAP + TD + 1.5])                                    # fas 1,5 mm runt fickans överkant
    cuts = [cyl(POCKET_R, GAP - 1, GAP + TD + 1, 0, -RP), cone,
            cyl(12.7, GAP - 1, GAP + 3.5), cyl(4.6, GAP + 3.4, GAP + 9.5), cyl(3.5, GAP, GAP + TD + 1)]
    return D(m, cuts)
disc = disc_local()
assert disc.is_watertight
disc_asm = disc.copy(); disc_asm.apply_transform(T)
dp = disc.copy(); dp.apply_translation([0, 0, -(GAP + TD)]); dp.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))   # ovansidan mot plattan

# ---------------------------------------------------------------- 10 doserstativ
slab = lcyl(SR, -ST, 0.0)
# rännan: tratt i planet, golvet lutar 38 grader mot mynningen
inner = Polygon(K.CH_POLY); outer = inner.buffer(WALL, join_style=2).intersection(sbox(-200, K.CH_B[1], 200, K.EX[1] + 15.1))
inner = unary_union([inner, sbox(K.CH_B[0] - K.CH_W, K.CH_B[1] - 2, K.CH_B[0] + K.CH_W, K.CH_B[1] + 1)])
nrm = np.array([K.CH_K * K.CH_T[0], K.CH_K * K.CH_T[1], 1.0]); nrm /= np.linalg.norm(nrm)        # golvplanets normal (uppåt)
R_ = trimesh.geometry.align_vectors([0, 0, 1], nrm); below = box(-BIG, BIG, -BIG, BIG, -BIG, 0.0); below.apply_transform(R_); below.apply_translation(K.CH_B)
channel = D(ext(inner, -20, 200), [below])
under_slab = lbox(-BIG, BIG, -BIG, BIG, -BIG, -ST + 0.6)                                           # allt under plattans undersida
cap = box(-BIG, BIG, -BIG, BIG, -BIG, 0.0); cap.apply_transform(R_); cap.apply_translation(K.CH_B + np.array([0, 0, 30.0 / nrm[2]]))    # 30 mm över golvet
allowed = U([I(under_slab, lcyl(SR - 0.5, -BIG, 0.0)), I(under_slab, cap)])                        # väggarna går upp till plattan under den, annars 30 mm över golvet
chute = D(I(ext(outer, 0.0, 200), allowed), [channel])
# stöd: bakre gavel, liten främre gavel, vägg under plattans nederkant, fot
PL = C[0] + C[2] - ST / c + 0.8                                                                     # x + z på plattans undersida (plus överlapp)
tri = lambda x0, x1: Polygon([(x0, 0), (x1, 0), (x1, max(PL - x1, 0.0)), (x0, PL - x0)])
yg = C[1] + 12.6; u_r = yg - C[1]; xr = c * np.sqrt(SR ** 2 - (u_r + 3) ** 2)
gavel_bak = ext_xz(tri(C[0] - xr - s * ST, C[0] + xr - s * ST), yg, yg + 3.0)
u_f = 20.0 - C[1]; xf = c * np.sqrt(SR ** 2 - u_f ** 2)
gavel_fram = ext_xz(tri(17.5, C[0] + xf - s * ST), 20.0, 23.0)
kantvagg = ext_xz(tri(22.0, 25.0), 21.0, yg + 2.0)
fot_poly = unary_union([sbox(-40, 18, 40, 100), outer])
fot = ext(fot_poly, 0.0, 3.0)
stand = U([slab, chute, gavel_bak, gavel_fram, kantvagg, fot])
holes = [lcyl(RX, -ST - 60, 2.0, uE, vE),                                                           # utfall
         lbox(-10.3, 10.3, -10.4, 30.7, -ST - 60, -1.0), lcyl(13.5, -2.0, 1.0),                     # servots kropp och horn
         channel]
for su in (-5.0, 5.0):
    for vv in (10.15 - 24.75, 10.15 + 24.75): holes.append(lcyl(2.0, -ST - 1, -ST + 7.0, su, vv, n=32))   # M3-bussningar för servot
for (x, y, d) in ((31.1, 32.9, 3.4), (31.1, 95.1, 4.5), (-31.1, 95.1, 4.5)):
    h = trimesh.creation.cylinder(radius=d / 2, height=20, sections=32); h.apply_translation([x, y, 0]); holes.append(h)
for sx in (-1, 1): holes.append(box(min(sx * 15.6, sx * 200), max(sx * 15.6, sx * 200), 0.0, 11.5, -1.0, 4.7))   # fri från sockelns klack vid mynningen
stand = clean(D(stand, holes))
assert stand.is_watertight

# ---------------------------------------------------------------- 14 nötförråd
us = np.linspace(UB, UF, 49)
arc = [(C[0] + c * np.sqrt(RC ** 2 - u * u) + s * WTOP, C[1] + u) for u in us]
F_in = Polygon([(XL, C[1] + UF), (XL, C[1] + UB)] + arc); F_out = F_in.buffer(WALL, join_style=2)
strips = F_out.difference(sbox(-BIG, C[1] + UF, BIG, C[1] + UB))
zlo = -50.0
E_out = ext(F_out, zlo, ZT); E_in = ext(F_in, zlo, ZT + 5)
urange_o = lbox(UF - WALL, UB + WALL, -BIG, 0.0, WT - 1.0, WTOP)
filled = U([lcyl(RC + WALL, 0.0, WT), I(lcyl(RC + WALL, WT - 0.5, WTOP), urange_o),
            I(E_out, w_ge(WTOP - 2.5)), I(I(E_out, w_ge(WS)), v_ge(VS)), I(ext(strips, zlo, ZT), w_ge(WS)),
            lcyl(52.7, 0.3, 2.7)])
V_in = U([lcyl(RC, -5.0, WS), I(lcyl(RC, WS - 0.5, WTOP + 0.5), lbox(UF, UB, -BIG, VS, WS - 1.0, WTOP + 1.0)),
          I(E_in, w_ge(WTOP)), I(I(E_in, w_ge(WT)), v_ge(VS))])
skirt = D(lcyl(52.7, -5.0, 0.5), [lcyl(50.3, -6.0, 1.0)])
a = np.radians(44.0); wedge = Polygon([(0, 0), (90 * np.sin(a), -90 * np.cos(a)), (-90 * np.sin(a), -90 * np.cos(a))])
wm = trimesh.creation.extrude_polygon(wedge, 12.0); wm.apply_translation([0, 0, -8.0]); wm.apply_transform(T)
ring_cut = D(wm, [lcyl(49.85, -9.0, 5.0)])                                                           # ta bort kjolen och flänsen nedtill, där plattan möter foten
def ext_yz(pts, x0=-BIG, x1=BIG):               # polygon i (y, z), utdragen längs x
    m = trimesh.creation.extrude_polygon(Polygon(pts), x1 - x0)
    m.apply_transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)); return m
# snitt i 45 grader så att de går att skriva ut utan stöd: fritt från skärmfästet (fram) och ellådan (bak)
cuts = [ext_yz([(-50, 86.2 - 71.8), (21.8, 86.2), (21.8, 300), (-50, 300)]), ext_yz([(112.2, 73.6), (200, 73.6 - 87.8), (200, 300), (112.2, 300)])]
grown = ext_yz([(-50, 62.7 - 50), (23.0, 85.7), (23.0, 300), (-50, 300)])                          # bakom snittet framtill lämnas en 1,2 mm vägg
hopper = D(U([filled, skirt]), [D(V_in, [grown]), ring_cut, lcyl(RC, -6.0, 0.31)] + cuts)
hopper = clean(hopper)
assert hopper.is_watertight

# ---------------------------------------------------------------- servo (bara för bilder och passform)
servo = U([lbox(-9.85, 9.85, 10.15 - 20.35, 10.15 + 20.35, -ST - 30.0, -1.1), lbox(-9.85, 9.85, 10.15 - 27.25, 10.15 + 27.25, -ST - 2.5, -ST), lcyl(5.5, -1.2, 3.0)])

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "asm"), exist_ok=True)
    disc_asm.export(os.path.join(OUT, "asm", "plockskiva.stl")); stand.export(os.path.join(OUT, "asm", "doserstativ.stl")); hopper.export(os.path.join(OUT, "asm", "notforrad.stl")); servo.export(os.path.join(OUT, "asm", "servo_mg996r.stl"))
    dp.export(os.path.join(OUT, "11_plockskiva.stl"))
    sp = stand.copy(); sp.apply_translation([-sp.bounds[:, 0].mean(), -sp.bounds[:, 1].mean(), -sp.bounds[0][2]]); sp.export(os.path.join(OUT, "10_doserstativ.stl"))
    hp = hopper.copy(); hp.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])); hp.apply_translation([-hp.bounds[:, 0].mean(), -hp.bounds[:, 1].mean(), -hp.bounds[0][2]]); hp.export(os.path.join(OUT, "14_notforrad.stl"))
    for n_, m in (("plockskiva", dp), ("doserstativ", sp), ("notforrad", hp)):
        nz = m.face_normals[:, 2]; cz = m.triangles_center[:, 2]; ar = m.area_faces
        print("%-12s mått %s  volym %.0f cm3  kroppar %d  kontakt %.0f mm2  överhäng brantare än 45 grader %.0f mm2" %
              (n_, np.round(m.extents, 1), m.volume / 1000, len(m.split(only_watertight=False)), ar[(nz < -0.999) & (cz < 0.05)].sum(), ar[(nz < -0.72) & (cz > 0.3)].sum()))
