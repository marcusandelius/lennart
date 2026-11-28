"""
Ny lucka på LENNART-skålen (9.19/9.20): servots egen arm i luckans högra gavel, svart ovansida och vit kant.

Förut satt luckan direkt på servoaxeln med en hylsa (Ø5,6 med ett Ø4,8-hål, 0,4 mm gods); den slirade,
glappade, gled av och sprack. Nu:
  * Servots enkla arm, ofilad (användarens mått: nav Ø7,5 x 3,5, platta 2,5 tjock, rund ände Ø10,5, 10 mm bred
    där armen börjar 4,5 mm från mitten, 5 mm vid yttersta hålet, 19,5 från mitten till spetsen), trycks på
    servoaxeln utanför brevlådans vägg och skruvas fast med sin egen skruv i axeln.
  * Luckans högra gavel (vit) har en ficka med armens form (+0,15 mm), lutad 12 grader uppåt framåt så att armen
    går fri över skålens kant. Fickan har vägg över armen och under armens yttre halva, så armen både lyfter och håller
    nere luckan. Gaveln sticker därför upp några mm över luckan, som en vindskiva. Brevlådans vägg ligger 0,4 mm
    utanför gaveln, så armen kan inte glida ut ur fickan.
  * Armens runda ände når 1,3 mm ner i skålens kant: ett hak filas i kanten under navet (x 36-40, y -14,5..-2,
    ner till z 26,6). 07_farstukvist_rod.stl i utkatalogen har haket för nya utskrifter.
  * Hålet i brevlådans vägg borras upp till Ø9 (navet Ø7,5). Brevlådans lock får en större plugg (brevlada.py).
  * Servot flyttas 0,6 mm mot luckan med distansbrickorna 26d, så att armen går fri från väggen (0,8 mm).
  * Vänster tapp: en M3 x 16-skruv genom lagerklotsen och distansringen, gängad in i valsen (Ø2,5 x 6 mm efter
    3,4 mm frigång), så att den roterar med luckan och inte kan vandra ut.
  * Luckan monteras genom att skjutas 3,3 mm åt höger över armen. Luckans vänstra ände vid axeln är därför
    3,1 mm kortare, och en distansring (08c, 3,4 mm) på tappen vid lagerklotsen hindrar luckan att glida tillbaka.
Husets ram: luckans axel längs x vid y -8, z 32,2. Utskriftsfilerna är förskjutna (-2, 25,8, -28,2), som förut.
    python3 lucka_servoarm.py lucka_src/lucka_gra_9_13_hus.stl lucka_src/lucka_vit_9_13_hus.stl <07_farstukvist_rod.stl> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh
from shapely.geometry import Point, Polygon, box as sbox
from shapely import affinity

GRA, VIT, ROD, OUT = sys.argv[1:5]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")
T = np.array([-2.0, 25.8, -28.2])             # hus -> utskrift
AXY, AXZ = -8.0, 32.2
Z_RIM = 28.2                                  # luckans undersida (skålens kant 28,0)

# servoarmen, filad (användarens mått)
A_PL, A_HUB_R, A_HUB_H = 2.5, 3.75, 3.5       # plattans tjocklek, navets radie och höjd
A_END_R, A_LEN = 5.25, 19.5                   # 9.20: ofilad arm: rund ände Ø10,5 runt navet, mitten till spetsen
A_DJ, A_WJ, A_W1 = 4.5, 10.0, 5.0             # armen börjar 4,5 mm från mitten, 10 mm bred, smalnar till 5 mm vid yttersta hålet
A_ANG = 12.0                                  # fickan lutar 12 grader uppåt framåt, så att armen går över skålens kant
NOTCH_Z = 26.6                                # hak i skålens kant under navet (y -14,5..-2, x 36..40), från 28,0 ner till 26,6
DIST = 0.6                                    # servot flyttas mot luckan med distansbrickorna 26d
A_X0 = 37.3 - DIST                            # plattans yttre yta (navet vilar på servots växeltorn, x 43,3 - 0,6)
CL = 0.15                                     # spel i fickan
X_FACE = 39.6                                 # gavelns yta mot brevlådan (väggen x 40)
X_GAV = 34.0                                  # gaveln börjar här
HEAD_R, HEAD_H = 2.7, 1.8                     # armens skruvhuvud
SLIDE = 3.3                                   # luckan skjuts så här långt vid montering
RING_L = 3.4                                  # distansringen mellan lagerklotsen (x -37) och luckan (x -33,6)


def xcyl(r, x0, x1, y=AXY, z=AXZ, s=48):
    return trimesh.creation.cylinder(radius=r, segment=[[x0, y, z], [x1, y, z]], sections=s)


def xext(poly, x0, x1):
    poly = poly.buffer(0).simplify(0.005)
    m = trimesh.creation.extrude_polygon(poly, x1 - x0)
    m.apply_transform(np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
    if m.volume < 0: m.invert()
    m.apply_translation([x0 - m.bounds[0][0], 0, 0]); return m


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def arm_outline(off=0.0, smal=True):
    """Armen som den är (ofilad), i armens eget läge: lutar A_ANG grader uppåt framåt."""
    tip_d = A_LEN - A_W1 / 2
    pts = [Point(0, 0).buffer(A_END_R + off, resolution=64), Point(-tip_d, 0).buffer(A_W1 / 2 + off, resolution=48),
           Polygon([(-A_DJ, -A_WJ / 2 - off), (-A_DJ, A_WJ / 2 + off), (-A_DJ - 0.01, A_WJ / 2 + off), (-A_DJ - 0.01, -A_WJ / 2 - off)])]
    from shapely.ops import unary_union
    o = unary_union(pts).convex_hull
    o = affinity.rotate(o, -A_ANG, origin=(0, 0))          # spetsen (y negativ) uppåt
    return affinity.translate(o, AXY, AXZ)


# armen (för kontroller och bilder)
arm = U([xext(arm_outline(), A_X0, A_X0 + A_PL), xcyl(A_HUB_R, A_X0 + A_PL - 0.01, A_X0 + A_PL + A_HUB_H)])
arm = D(arm, [xcyl(1.15, A_X0 - 1, A_X0 + 7)])

LG = trimesh.load(GRA); LV = trimesh.load(VIT)
# gamla hylsan bort (allt till höger om gavelns yta)
right = box(X_FACE, 60, -60, 10, 0, 60)
LG = D(LG, [right]); LV = D(LV, [right])
# gaveln: armens kontur + 1,2 mm gods, från x 34 till gavelns yta, inte under luckans undersida
# bakom axeln (y > -8) högst radie 5,3: den delen vrids ner i haket i skålens kant när luckan öppnas
gav2d = arm_outline(CL + 1.2).intersection(sbox(-60, -60, AXY, 60)).union(Point(AXY, AXZ).buffer(AXZ - NOTCH_Z - 0.3, resolution=64))
gav2d = gav2d.intersection(sbox(-60, Z_RIM, 10, 60))        # inget under luckans undersida (skrivs ut liggande); väggen under armen finns längs den yttre halvan
gavel = xext(gav2d, X_GAV, X_FACE)
pocket = xext(arm_outline(CL), A_X0 - 0.2, X_FACE + 1)
head = xcyl(HEAD_R, A_X0 - 0.2 - HEAD_H, A_X0, s=40)
LG = D(LG, [gavel]); LV = D(U([LV, gavel]), [pocket, head])
LG = D(LG, [pocket, head])
# vänstra änden vid axeln 3,1 mm kortare (montering: luckan skjuts 3,3 mm), tapphålet kvar
rull = box(-36.7, -33.6, -16.6, 1.0, 20.0, 45.0)
LG = D(LG, [rull]); LV = D(LV, [rull])
# 9.21: tappen är en M3 x 16-skruv genom lagerklotsen (hål Ø3,4) och distansringen; den gängar sig in i
# valsen (Ø2,5, 6 mm) och roterar med luckan, så den kan inte vandra ut. Förut Ø3,4 x 6 mm utan gänga.
LG = D(LG, [U([xcyl(1.7, -35.0, -30.4, s=40), xcyl(1.25, -30.6, -24.5, s=40)])])
for m in (LG, LV): assert m.is_watertight
for m in (LG, LV): assert m.is_watertight

# distansring 08c på tappen: C-form, 3,3 lång, ytter Ø7, inner Ø3,5, öppning 2,7
ring = D(xcyl(3.5, 0, RING_L, 0, 0, 64), [xcyl(1.75, -1, RING_L + 1, 0, 0, 48), box(-1, RING_L + 1, 1.2, 5, -1.35, 1.35)])
# skålen (07 röd) med haket under navet, i dess utskriftsram
TO_ROD = np.array([-12.4, 23.6, 0.0])
rod = trimesh.load(ROD); rod.apply_translation(-TO_ROD)
rod = D(rod, [box(36.0, 40.05, -14.5, -2.0, NOTCH_Z, 28.1)]); assert rod.is_watertight

os.makedirs(OUT, exist_ok=True); asm = os.path.join(OUT, "asm"); os.makedirs(asm, exist_ok=True)
ring_asm = D(xcyl(3.5, -37.0, -37.0 + RING_L), [xcyl(1.75, -38, -32), box(-38, -32, AXY - 1.35, AXY + 1.35, AXZ - 5, AXZ - 1.2)])   # öppningen nedåt
skruv = U([xcyl(2.75, -42.0, -40.0, s=6), xcyl(1.5, -40.01, -26.0, s=24)])
for n, m in (("lucka_svart", LG), ("lucka_vit", LV), ("servoarm", arm), ("skal_rod_hak", rod), ("distansring", ring_asm), ("tapp_m3", skruv)):
    m.export(os.path.join(asm, n + ".stl"))
for n, m in (("08_lucka_svart.stl", LG), ("08_lucka_vit.stl", LV)):
    mm = m.copy(); mm.apply_translation(T); mm = U([mm, box(500, 501, 500, 501, 500, 501)]).split(only_watertight=False)
    mm = max(mm, key=lambda q: q.volume); mm.export(os.path.join(OUT, n))           # städat efter förflyttningen


def flat(m, R):
    m = m.copy(); m.apply_transform(R); m.apply_translation(-m.bounds[0]); return m


Ry = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
flat(ring, Ry).export(os.path.join(OUT, "08c_distansring_tapp.stl"))
r2 = rod.copy(); r2.apply_translation(TO_ROD); r2.export(os.path.join(OUT, "07_farstukvist_rod.stl"))
for f in sorted(os.listdir(OUT)):
    if f.endswith(".stl"):
        m = trimesh.load(os.path.join(OUT, f)); print(f, np.round(m.extents, 1), "tät", m.is_watertight)
