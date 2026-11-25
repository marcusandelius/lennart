"""
Plockskivan, omritad: fem delar för doseringen (husets ram, mm, framsidan är -y). Måtten kommer från plock.py, samma som simuleringen.
  10_doserstativ.stl   lutande platta med kant runt skivan, servofäste, utfall och ränna
  10b_skivkapa.stl     kåpa över skivans främre kant (två M3 i stativet), snett avskuren under skärmklämman
  11_plockskiva.stl    skivan med en ficka
  11b_omrorare.stl     omrörare som trycks ned i skivans mitt
  14_notforrad.stl     förrådet, lyfts rakt upp
Kör:  python3 cad5.py <utkatalog> ['{"zt": 150}']
"""
import sys, os, json
import numpy as np
import trimesh
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
import plock as K

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
if len(sys.argv) > 2: K.configure(**json.loads(sys.argv[2]))
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
w_ge = lambda a: lbox(-BIG, BIG, -BIG, BIG, a, a + BIG)          # halvrymder
v_ge = lambda a: lbox(-BIG, BIG, a, a + BIG, -BIG, BIG)
y_le = lambda a: box(-BIG, BIG, a - BIG, a, -BIG, BIG)
y_ge = lambda a: box(-BIG, BIG, a, a + BIG, -BIG, BIG)
z_le = lambda a: box(-BIG, BIG, -BIG, BIG, a - BIG, a)
z_ge = lambda a: box(-BIG, BIG, -BIG, BIG, a, a + BIG)
def clean(m, vmin=20.0):
    m = trimesh.util.concatenate([q for q in m.split(only_watertight=False) if abs(q.volume) > vmin])
    import io
    for dec in (4, 3, 5, 2, None):                      # avrunda så att filen förblir tät när den läses in igen
        m2 = m.copy() if dec is None else trimesh.Trimesh(np.round(m.vertices, dec), m.faces, process=True)
        m2.merge_vertices(); m2.update_faces(m2.nondegenerate_faces()); m2.remove_unreferenced_vertices()
        if not m2.is_watertight: continue
        r = trimesh.load(io.BytesIO(m2.export(file_type="stl")), file_type="stl")
        if r.is_watertight: return m2
    raise RuntimeError("delen blev inte tät")

C = K.C; RD, TD, GAP, RP = K.RD, K.TD, K.GAP, K.RP; RC, WALL = K.RC, K.WALL; RO = RC + WALL
WR, WS, WT, WTOP, VS = K.WR, K.WS, K.WT, K.WTOP, K.VS
UF, UB, XL, ZT = K.UF, K.UB, K.XL, K.ZT; ST, RX, KK = K.SLAB_T, K.RX, K.KK
YCF, YCB = K.YF - WALL, K.YB + WALL            # förrådets ytterväggar fram och bak (raka)
uE, vE = -RP * np.sin(K.QX), RP * np.cos(K.QX)
POCKET_R = 13.25
LUGS = [(-39.8, -31.6), (-25.5, -43.9)]        # skruvöron för kåpan (lokala u, v), radie 50,8
SQ = 8.4                                       # fyrkantshål i skivans mitt för omröraren

# ---------------------------------------------------------------- 11 plockskiva (lokala koordinater, fickan nederst = plockläget)
def disc_local():
    m = trimesh.creation.cylinder(radius=RD, height=TD, sections=180); m.apply_translation([0, 0, GAP + TD / 2])
    def cyl(r, w0, w1, u=0.0, v=0.0):
        q = trimesh.creation.cylinder(radius=r, height=w1 - w0, sections=96); q.apply_translation([u, v, (w0 + w1) / 2]); return q
    hc = POCKET_R + 1.8                                                                   # fas 0,8 mm runt fickans överkant
    cone = trimesh.creation.cone(radius=hc, height=hc, sections=96); cone.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    cone.apply_translation([0, -RP, GAP + TD + 1.0])
    sq = trimesh.creation.box(extents=[SQ, SQ, TD]); sq.apply_translation([0, 0, GAP + 9.4 + TD / 2])    # fyrkantshål från hornskruvens urtag upp till ovansidan
    cuts = [cyl(POCKET_R, GAP - 1, GAP + TD + 1, 0, -RP), cone,
            cyl(12.7, GAP - 1, GAP + 3.5), cyl(4.6, GAP + 3.4, GAP + 9.5), cyl(3.5, GAP, GAP + TD + 1), sq]
    return D(m, cuts)
disc = clean(disc_local())
assert disc.is_watertight
disc_asm = disc.copy(); disc_asm.apply_transform(T)
dp = disc.copy(); dp.apply_translation([0, 0, -(GAP + TD)]); dp.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))   # ovansidan mot plattan

# ---------------------------------------------------------------- 10 doserstativ
slab = I(lcyl(RO, -ST, 0.0), y_le(YCB))
gapw = Polygon([(0, 0)] + [(70 * np.cos(a), 70 * np.sin(a)) for a in np.radians(np.linspace(-21, 21, 12))])
gap_m = trimesh.creation.extrude_polygon(gapw, 60.0); gap_m.apply_translation([0, 0, -20.0]); gap_m.apply_transform(T)
rim = D(lcyl(RO, -0.1, WR), [lcyl(RC, -1.0, WR + 1.0), gap_m])                              # kant runt skivan, 1 mm över skivans ovansida, öppen längst bak där förrådets bakvägg står
def yplane(k, x0=-BIG, x1=BIG):                 # halvrymden z <= y + k
    m = trimesh.creation.extrude_polygon(Polygon([(-150, -300), (200, -300), (200, 200 + k), (-150, -150 + k)]), x1 - x0)
    m.apply_transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)); return m
ears = [D(lcyl(6.0, -ST, WR, u, v, n=48), [lcyl(RC, -0.05, WR + 1.0)]) for u, v in LUGS]
# kåpa över skivans främre kant: krage upp till ett lock 26 mm över skivan, snett avskuret 3 mm under skärmklämman
env_out = I(I(lcyl(RO, WR, WT), yplane(KK)), y_le(YCF - 0.4))
kon = trimesh.creation.cone(radius=RC, height=RC, sections=128); kon.apply_translation([0, 0, WS - 6.5]); kon.apply_transform(T)   # locket är snett inåt (45 grader) så att kåpan kan skrivas ut stående
env_in = I(U([lcyl(RC, WR - 1.0, WS - 6.5), I(kon, lbox(-BIG, BIG, -BIG, BIG, WS - 6.6, WS))]), yplane(KK - 1.7))
crescent = D(env_out, [env_in])
a0_, a1_ = np.radians(206.0), np.radians(247.0)
wedge = Polygon([(0, 0)] + [(70 * np.cos(a), 70 * np.sin(a)) for a in np.linspace(a0_, a1_, 30)])
wedge_m = trimesh.creation.extrude_polygon(wedge, 60.0); wedge_m.apply_translation([0, 0, -20.0]); wedge_m.apply_transform(T)
band = I(D(lcyl(RO + 2.6, WR, WR + 2.5), [lcyl(RO + 0.4, WR - 1.0, WR + 3.0)]), wedge_m)             # band utanför förrådets krage, fram till det andra skruvörat
flange = I(I(D(lcyl(RO + 1.5, WR + 0.02, WR + 2.4), [lcyl(RO - 1.0, WR - 1.0, WR + 3.0)]), wedge_m), y_le(YCF - 0.45))
tabs = [lcyl(4.5, WR, WR + 3.0, u, v, n=48) for u, v in LUGS]
kapa = D(U([crescent, band, flange] + tabs), [lcyl(1.7, WR - 1.0, WR + 4.0, u, v, n=32) for u, v in LUGS] + [lcyl(6.4, -ST - 1.0, WR, u, v, n=48) for u, v in LUGS])
kapa = clean(kapa, vmin=5.0)
assert kapa.is_watertight
# rännan: tratt i planet, golvet lutar mot mynningen
inner = Polygon(K.CH_POLY); outer = inner.buffer(WALL, join_style=2).intersection(sbox(-200, K.CH_B[1], 200, K.EX[1] + 15.1))
inner = unary_union([inner, sbox(K.CH_B[0] - K.CH_W, K.CH_B[1] - 2, K.CH_B[0] + K.CH_W, K.CH_B[1] + 1)])
nrm = np.array([K.CH_K * K.CH_T[0], K.CH_K * K.CH_T[1], 1.0]); nrm /= np.linalg.norm(nrm)        # golvplanets normal (uppåt)
R_ = trimesh.geometry.align_vectors([0, 0, 1], nrm); below = box(-BIG, BIG, -BIG, BIG, -BIG, 0.0); below.apply_transform(R_); below.apply_translation(K.CH_B)
channel = D(ext(inner, -20, 200), [below])
under_slab = lbox(-BIG, BIG, -BIG, BIG, -BIG, -ST + 0.6)                                           # allt under plattans undersida
cap = box(-BIG, BIG, -BIG, BIG, -BIG, 0.0); cap.apply_transform(R_); cap.apply_translation(K.CH_B + np.array([0, 0, 30.0 / nrm[2]]))    # 30 mm över golvet
allowed = U([I(under_slab, lcyl(RO - 0.5, -BIG, 0.0)), I(under_slab, cap)])                        # väggarna går upp till plattan under den, annars 30 mm över golvet
chute = D(I(ext(outer, 0.0, 200), allowed), [channel])
# stöd under plattan: bakre gavel och vägg under plattans nederkant, kapade så att inget sticker ut utanför plattan
PL = C[0] + C[2] - ST / c + 0.8                                                                     # x + z på plattans undersida (plus överlapp)
tri = lambda x0, x1: Polygon([(x0, 0), (x1, 0), (x1, max(PL - x1, 0.0)), (x0, PL - x0)])
shadow = trimesh.convex.convex_hull(np.vstack([slab.vertices, slab.vertices * [1, 1, 0]]))          # plattan och allt rakt under den
yg = C[1] + 12.6
gavel_bak = I(ext_xz(tri(-80.0, PL - 1.0), yg, yg + 3.0), shadow)
xk = C[0] + c * RO - s * ST                                                                         # plattans nederkant (undersidan)
kantvagg = I(ext_xz(tri(xk - 4.5, xk - 1.5), C[1] - 26.0, yg + 2.0), shadow)
fot_poly = unary_union([sbox(-40, 22, 40, 100), outer])
fot = ext(fot_poly, 0.0, 3.0)
stand = U([slab, rim, chute, gavel_bak, kantvagg, fot] + ears)
holes = [lcyl(RX, -ST - 0.2, 2.0, uE, vE), I(channel, lbox(-BIG, BIG, -BIG, BIG, -BIG, -K.SKIN)),    # utfall genom plattan; över rännan är plattan urtagen underifrån till 3 mm
         lbox(-10.15, 10.15, -10.4, 30.7, -ST - 60, -1.0), lcyl(13.0, -2.0, 1.0)]                   # servots kropp och horn
for su in (-5.0, 5.0):
    for vv in (10.15 - 24.75, 10.15 + 24.75): holes.append(lcyl(2.0, -ST - 1, -ST + 7.0, su, vv, n=32))   # M3-bussningar för servot
for u, v in LUGS: holes.append(lcyl(2.0, WR - 6.5, WR + 1.0, u, v, n=32))                           # M3-bussningar för kåpan
for (x, y, d) in ((31.1, 32.9, 3.4), (31.1, 95.1, 4.5), (-31.1, 95.1, 4.5)):
    h = trimesh.creation.cylinder(radius=d / 2, height=20, sections=32); h.apply_translation([x, y, 0]); holes.append(h)
for sx in (-1, 1): holes.append(box(min(sx * 15.0, sx * 200), max(sx * 15.0, sx * 200), 0.0, 12.5, -1.0, 5.7))   # fri från sockelns klack vid mynningen
stand = clean(D(stand, holes))
assert stand.is_watertight

# ---------------------------------------------------------------- 11b omrörare: fyrkantsfot, ansats, pinne och blad (plan del, 8 mm tjock)
A0, A1, AR = 48.0, 92.0, 15.0
prof = unary_union([sbox(-4.0, GAP + 12.0, 4.0, A1), sbox(-6.5, GAP + TD, 6.5, GAP + TD + 2.4), sbox(-AR, A0, AR, A1)])
ag = trimesh.creation.extrude_polygon(prof, 8.0)                                                    # (a, w) i planet, tjocklek längs z
ag_print = ag.copy()
ag_asm = ag.copy(); ag_asm.apply_transform(np.array([[0, 0, 1, -4.0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))   # tjocklek -> u, a -> v (mot fickan), w -> w
ag_asm.apply_transform(T)

# ---------------------------------------------------------------- 14 nötförråd
us = np.linspace(UB, UF, 49)
arc = [(C[0] + c * np.sqrt(RC ** 2 - u * u) + s * WTOP, C[1] + u) for u in us]
F_in = Polygon([(XL, C[1] + UF), (XL, C[1] + UB)] + arc); F_out = F_in.buffer(WALL, join_style=2)
zlo = -50.0
E_out = ext(F_out, zlo, ZT); E_in = ext(F_in, zlo, ZT + 5)
urange_o = lbox(UF - WALL, UB + WALL, -BIG, 0.0, WT - 1.0, WTOP)
filled = U([lcyl(RO, WR, WT), I(lcyl(RO, WT - 0.5, WTOP), urange_o),
            I(E_out, w_ge(WTOP - 2.5)), I(I(E_out, w_ge(WS)), v_ge(VS))])
V_in = U([lcyl(RC, WR - 1.0, WS), I(lcyl(RC, WS - 0.5, WTOP + 0.5), lbox(UF, UB, -BIG, VS, WS - 1.0, WTOP + 1.0)),
          I(E_in, w_ge(WTOP)), I(I(E_in, w_ge(WT)), v_ge(VS))])
region = U([lcyl(RO, WR, WTOP), I(E_out, w_ge(WS))])                                               # där väggarna ska finnas: över skivan och i förrådet
wall_f = I(I(box(-BIG, BIG, YCF, K.YF - 0.02, -BIG, ZT), U([w_ge(WS), I(z_ge(YCF + KK - 1.7), w_ge(WR + 0.8))])), region)   # framvägg: ned till lockets nivå och det sneda taket
wall_b = I(I(box(-BIG, BIG, K.YB + 0.02, YCB, -BIG, ZT), w_ge(WR)), region)                                # bakvägg: ned till stativets kant
skirt = I(D(lcyl(RO + 2.8, WR - 8.0, WR + 3.0), [lcyl(RO + 0.4, WR - 9.0, WR), lcyl(RC, WR - 9.0, WR + 4.0)]), v_ge(10.0))   # hake över stativets överkant
ybox = box(-BIG, BIG, YCF, YCB, -BIG, BIG)
hopper = U([I(D(filled, [V_in]), ybox), wall_f, wall_b, I(skirt, ybox)])
notch = lbox(-7.5, 7.5, VS - 1.0, 7.5, WS - 1.0, WT + 1.0)                                          # urtag i skärmen för omrörarens pinne
hopper = clean(D(hopper, [notch]))
assert hopper.is_watertight

# ---------------------------------------------------------------- servo (bara för bilder och passform)
servo = U([lbox(-9.85, 9.85, 10.15 - 20.35, 10.15 + 20.35, -ST - 30.0, -1.1), lbox(-9.85, 9.85, 10.15 - 27.25, 10.15 + 27.25, -ST - 2.5, -ST), lcyl(5.5, -1.2, 3.0)])

def report(name, m):
    nz = m.face_normals[:, 2]; cz = m.triangles_center[:, 2]; ar = m.area_faces
    print("%-12s mått %s  volym %.0f cm3  kroppar %d  kontakt %.0f mm2  överhäng brantare än 45 grader %.0f mm2" %
          (name, np.round(m.extents, 1), m.volume / 1000, len(m.split(only_watertight=False)), ar[(nz < -0.999) & (cz < 0.05)].sum(), ar[(nz < -0.72) & (cz > 0.3)].sum()))

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "asm"), exist_ok=True)
    for n_, m in (("plockskiva", disc_asm), ("doserstativ", stand), ("skivkapa", kapa), ("omrorare", ag_asm), ("notforrad", hopper), ("servo_mg996r", servo)):
        m.export(os.path.join(OUT, "asm", n_ + ".stl"))
    def bed(m): m = m.copy(); m.apply_translation([-m.bounds[:, 0].mean(), -m.bounds[:, 1].mean(), -m.bounds[0][2]]); return m
    flip = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
    sp = bed(stand); kp = kapa.copy(); kp.apply_transform(np.linalg.inv(T)); kp = bed(kp); hp = hopper.copy(); hp.apply_transform(flip); hp = bed(hp); ap = bed(ag_print)
    for f_, m in (("10_doserstativ", sp), ("10b_skivkapa", kp), ("11_plockskiva", dp), ("11b_omrorare", ap), ("14_notforrad", hp)):
        m.export(os.path.join(OUT, f_ + ".stl")); report(f_, m)
