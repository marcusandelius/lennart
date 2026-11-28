"""
Ny lucka på LENNART-skålen (9.19): servots egen arm i luckans högra gavel, svart ovansida och vit kant.

Förut satt luckan direkt på servoaxeln med en hylsa (Ø5,6 med ett Ø4,8-hål, 0,4 mm gods); den slirade,
glappade, gled av och sprack. Nu:
  * Servots enkla arm (användarens mått: nav Ø7,5 x 3,5, platta 2,5 tjock, 19,5 från mitten till spetsen)
    filas till en remsa 5,6 mm bred med rund ände Ø8 runt navet (filmall 29). Armen trycks på servoaxeln
    utanför brevlådans vägg och skruvas fast med sin egen skruv i axeln.
  * Luckans högra gavel (vit) har en ficka med armens form (+0,15 mm). Fickan har väggar ovanför och under
    remsan, så armen både lyfter och håller nere luckan. Brevlådans vägg ligger 0,4 mm utanför gaveln,
    så armen kan inte glida ut ur fickan.
  * Hålet i brevlådans vägg borras upp till Ø9 (navet Ø7,5). Brevlådans lock får en större plugg (brevlada.py).
  * Servot flyttas 0,6 mm mot luckan med distansbrickorna 26d, så att armen går fri från väggen (0,8 mm).
  * Luckan monteras genom att skjutas 3,3 mm åt höger över armen. Luckans vänstra ände vid axeln är därför
    3,1 mm kortare, och en distansring (08c, 3,4 mm) på tappen vid lagerklotsen hindrar luckan att glida tillbaka.
  * Gaveln är rund (radie 4) bakom axeln, så att den går fri från skålens kant när luckan öppnas.
Husets ram: luckans axel längs x vid y -8, z 32,2. Utskriftsfilerna är förskjutna (-2, 25,8, -28,2), som förut.
    python3 lucka_servoarm.py lucka_src/lucka_gra_9_13_hus.stl lucka_src/lucka_vit_9_13_hus.stl <utkatalog>
"""
import sys, os
import numpy as np
import trimesh
from shapely.geometry import Point, Polygon, box as sbox

GRA, VIT, OUT = sys.argv[1:4]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")
T = np.array([-2.0, 25.8, -28.2])             # hus -> utskrift
AXY, AXZ = -8.0, 32.2
Z_RIM = 28.2                                  # luckans undersida (skålens kant 28,0)

# servoarmen, filad (användarens mått)
A_PL, A_HUB_R, A_HUB_H = 2.5, 3.75, 3.5       # plattans tjocklek, navets radie och höjd
A_END_R, A_HALF, A_LEN = 4.0, 2.8, 19.5       # rund ände runt navet, halva remsans bredd, mitten till spetsen
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


def arm_outline(off=0.0):
    tip = AXY - (A_LEN - A_HALF)
    strip = sbox(tip, AXZ - A_HALF - off, AXY, AXZ + A_HALF + off).union(Point(tip, AXZ).buffer(A_HALF + off, resolution=48))
    return strip.union(Point(AXY, AXZ).buffer(A_END_R + off, resolution=64))


# armen (för kontroller och bilder)
arm = U([xext(arm_outline(), A_X0, A_X0 + A_PL), xcyl(A_HUB_R, A_X0 + A_PL - 0.01, A_X0 + A_PL + A_HUB_H)])
arm = D(arm, [xcyl(1.15, A_X0 - 1, A_X0 + 7)])

LG = trimesh.load(GRA); LV = trimesh.load(VIT)
# gamla hylsan bort (allt till höger om gavelns yta)
right = box(X_FACE, 60, -60, 10, 0, 60)
LG = D(LG, [right]); LV = D(LV, [right])
# gaveln: armens kontur + 1,2 mm gods, från x 34 till gavelns yta, inte under luckans undersida
# bakom axeln (y > -8) högst radie 4: den delen vrids ner mot skålens kant när luckan öppnas
gav2d = arm_outline(CL + 1.2).intersection(sbox(-60, Z_RIM, AXY, 60)).union(Point(AXY, AXZ).buffer(4.0, resolution=64)).intersection(sbox(-60, Z_RIM, 10, 60))
gavel = xext(gav2d, X_GAV, X_FACE)
pocket = xext(arm_outline(CL), A_X0 - 0.2, X_FACE + 1)
head = xcyl(HEAD_R, A_X0 - 0.2 - HEAD_H, A_X0, s=40)
LG = D(LG, [gavel]); LV = D(U([LV, gavel]), [pocket, head])
LG = D(LG, [pocket, head])
# vänstra änden vid axeln 3,1 mm kortare (montering: luckan skjuts 3,3 mm), tapphålet kvar
rull = box(-36.7, -33.6, -16.6, 1.0, 20.0, 45.0)
LG = D(LG, [rull]); LV = D(LV, [rull])
for m in (LG, LV): assert m.is_watertight

# distansring 08c på tappen: C-form, 3,3 lång, ytter Ø7, inner Ø3,5, öppning 2,7
ring = D(xcyl(3.5, 0, RING_L, 0, 0, 64), [xcyl(1.75, -1, RING_L + 1, 0, 0, 48), box(-1, RING_L + 1, 1.2, 5, -1.35, 1.35)])
# filmall 29: armens filade form, 2 mm tjock, hål Ø7,8 som sitter över navet
mall = D(xext(arm_outline(), 0, 2.0), [xcyl(3.9, -1, 3)])
mall.apply_translation([-mall.bounds[0][0], 0, 0])

os.makedirs(OUT, exist_ok=True); asm = os.path.join(OUT, "asm"); os.makedirs(asm, exist_ok=True)
for n, m in (("lucka_svart", LG), ("lucka_vit", LV), ("servoarm_filad", arm)):
    m.export(os.path.join(asm, n + ".stl"))
for n, m in (("08_lucka_svart.stl", LG), ("08_lucka_vit.stl", LV)):
    mm = m.copy(); mm.apply_translation(T); mm.export(os.path.join(OUT, n))


def flat(m, R):
    m = m.copy(); m.apply_transform(R); m.apply_translation(-m.bounds[0]); return m


Ry = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
flat(ring, Ry).export(os.path.join(OUT, "08c_distansring_tapp.stl"))
flat(mall, Ry).export(os.path.join(OUT, "29_filmall_servoarm.stl"))
for f in sorted(os.listdir(OUT)):
    if f.endswith(".stl"):
        m = trimesh.load(os.path.join(OUT, f)); print(f, np.round(m.extents, 1), "tät", m.is_watertight)
