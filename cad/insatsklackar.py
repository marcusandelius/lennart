"""
Lodräta insatshål för skärmklämman och kamerafästet (version 9).

Version 8 hade fyra klackar på framväggens insida med vågräta M3-insatshål (Ø4,0) som pekade
bakåt in i huset. Lödkolven kom inte åt dem. Här blir hålen lodräta och öppnar uppåt,
så att insatserna kan pressas in uppifrån när taket är av.

  * Skärmklackarna (x = ±34, oförändrade i läge och form): det vågräta hålet fylls igen,
    nytt lodrätt hål Ø4,0 x 6,5 i klackens ovansida (z = 112) vid y = -59,5.
  * Kameraklackarna byggs om: x 18-26, ovansida z = 175, 14,4 mm ut från väggen med
    45-graders stöd under, lodrätt hål Ø4,0 x 6,5 vid y = -58.
  * Ny skärmklämma: samma ram, plus två vågräta flikar som vilar på klackarna,
    avlånga hål (2 mm spel) för M3-skruv uppifrån.
  * Nytt kamerafäste: en släde. Kameran skruvas på distanser framför en ram, flikarna
    vilar på klackarna och har 5 mm långa spår, så att kameran kan skjutas fram tills
    linsen nästan nuddar fönstret.

Kör:  python3 insatsklackar.py <kropp_in.stl> <skarmklamma_v7.stl> <utkatalog>
Koordinater: kroppens STL (x åt sidan, y framåt-bakåt där framväggens insida är y = -66,87, z uppåt).
"""
import sys, os
import numpy as np
import trimesh
from trimesh.creation import cylinder, box as tbox, extrude_polygon
from shapely.geometry import Polygon

BODY_IN, CLAMP_IN, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")

WALL = -66.87            # framväggens insida
INS_D, INS_DEPTH = 4.0, 6.5    # Ruthex M3, samma som förut
SLOT_W = 3.4             # M3 genomgående


def box(x0, x1, y0, y1, z0, z1):
    b = tbox(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def cyl(r, x, y, z0, z1, sec=48):
    """Lodrät cylinder."""
    c = cylinder(radius=r, height=z1 - z0, sections=sec)
    c.apply_translation([x, y, (z0 + z1) / 2]); return c


def insert_hole(x, y, ztop):
    h = cyl(INS_D / 2, x, y, ztop - INS_DEPTH, ztop + 1)
    ch = trimesh.creation.cone(radius=INS_D / 2 + 0.5 + 1.0, height=INS_D / 2 + 0.5 + 1.0, sections=48)
    ch.apply_transform(np.diag([1, 1, -1, 1])); ch.apply_translation([x, y, ztop + 1.0])   # 0,5 mm fas
    return U([h, ch])


def wedge_x(x0, x1, y_front, z_top, z_low_front):
    """Klack: block från väggen till y_front, ovansida z_top, undersida z_low_front, 45 grader ner mot väggen."""
    depth = y_front - WALL
    prof = Polygon([(WALL - 0.3, z_top), (y_front, z_top), (y_front, z_low_front),
                    (WALL - 0.3, z_low_front - depth - 0.3)])
    m = extrude_polygon(prof, x1 - x0)       # (y,z) i planet, extruderat längs lokal z
    T = np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)
    m.apply_transform(T)
    if m.volume < 0: m.invert()
    return m


def slot(x, y0, y1, z0, z1, w=SLOT_W):
    """Avlångt hål längs y, lodrätt genom z0..z1."""
    r = w / 2
    return U([cyl(r, x, y0, z0, z1), cyl(r, x, y1, z0, z1), box(x - r, x + r, y0, y1, z0, z1)])


# ---------------------------------------------------------------- kroppen
SCR_X, SCR_Y, SCR_TOP = 34.0, -59.47, 112.0
CAM_X, CAM_Y, CAM_TOP = 22.0, -58.0, 175.0
CAM_FRONT, CAM_H = -52.5, 8.0

body = trimesh.load(BODY_IN)
add, sub = [], []
for s in (1, -1):
    # skärmklacken: fyll det gamla vågräta hålet (blocket x 30-38, y vägg..-52,07, z 104-112)
    xa, xb = sorted([s * 30.0, s * 38.0])
    add.append(box(xa, xb, WALL - 0.3, -52.07, 104.0, 112.0))
    sub.append(insert_hole(s * SCR_X, SCR_Y, SCR_TOP))
    # kameraklacken: ny, större
    xa, xb = sorted([s * 18.0, s * 26.0])
    add.append(wedge_x(xa, xb, CAM_FRONT, CAM_TOP, CAM_TOP - CAM_H))
    sub.append(insert_hole(s * CAM_X, CAM_Y, CAM_TOP))
body = U([body] + add)
body = D(body, sub)
assert body.is_watertight
body.export(os.path.join(OUT, "05_kropp_rod.stl"))
print("kropp:", round(body.volume / 1000, 1), "cm3")

# ---------------------------------------------------------------- skärmklämman
# Gammal klämma i utskriftsläge: ram 76 x 42 x 3 (z 0-3), lister x ±26-30 upp till z 9.
# Monterad: x = x, z_hus = y + 108, y_hus = -49,07 - z.
cl = trimesh.load(CLAMP_IN)
c_add, c_sub = [], []
for s_ in (1, -1):
    xa, xb = sorted([s_ * 30.0, s_ * 38.0])
    c_add.append(cyl(1.8, s_ * 34.0, 0.0, 0.0, 3.0))                 # fyll det gamla hålet
    # flik: hus-z 112-116 -> y 4-8; från ramen (z 0) fram till hus-y -65,5 -> z 16,43
    c_add.append(box(xa, xb, 4.0, 8.0, 0.0, 16.43))
    # spår: hus-y -59,47 (klämman tryckt mot klacken) till 2 mm bakåt -> z 10,4..12,4, genom y
    sl = slot(0, 10.4, 12.4, -3, 3)                       # byggd lodrät, roteras så att den går längs y
    sl.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))   # z->y, y->-z
    sl.apply_transform(np.diag([1, 1, -1, 1]))            # y-sidan av spåret tillbaka till +z
    sl.apply_translation([s_ * 34.0, 6.0, 0.0])
    c_sub.append(sl)
clamp = D(U([cl] + c_add), c_sub)
assert clamp.is_watertight
clamp.export(os.path.join(OUT, "19_skarmklamma.stl"))
print("klämma:", np.round(clamp.extents, 1))

# ---------------------------------------------------------------- kamerasläden
# Byggs monterad (hus-koordinater) med ramens framsida på Y_P (nominellt läge), vänds sedan för utskrift.
LENS_Z = 167.0                     # fönstrets mitt
Y_P = -49.5                        # ramens framsida, nominellt (linsen ca 10 mm hög)
T_PLATE, STANDOFF = 3.0, 4.0
HX, HZ = 10.5, 6.25                # Camera Module 3: hål 21 x 12,5 mm, linsen mitt emellan hålraderna
yb = Y_P + T_PLATE
parts = [
    box(-15, 15, Y_P, yb, 153.0, CAM_TOP),                       # ram
    box(-26.5, 26.5, Y_P, yb, CAM_TOP, CAM_TOP + 4.0),           # överliggare
]
for s_ in (1, -1):
    xa, xb = sorted([s_ * 15.0, s_ * 26.5])
    parts.append(box(xa, xb, Y_P - 14.5, yb, CAM_TOP, CAM_TOP + 4.0))   # flik över klacken
for sx in (1, -1):
    for sz in (1, -1):
        parts.append(cyl(2.6, sx * HX, 0, 0, 1))  # platshållare, ersätts nedan
parts = parts[:-4]
so = []
for sx in (1, -1):
    for sz in (1, -1):
        c = cylinder(radius=2.6, height=STANDOFF + T_PLATE, sections=40)
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
        c.apply_translation([sx * HX, Y_P - STANDOFF + (STANDOFF + T_PLATE) / 2, LENS_Z + sz * HZ])
        so.append(c)
sled = U(parts + so)
holes = []
for sx in (1, -1):
    for sz in (1, -1):
        c = cylinder(radius=1.1, height=20, sections=32)
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
        c.apply_translation([sx * HX, Y_P, LENS_Z + sz * HZ]); holes.append(c)
holes.append(box(-7.0, 7.0, Y_P - 1, yb + 1, 157.0, 172.5))     # öppning för kontakt och komponenter
for s_ in (1, -1):
    # spår: klackens hål (y = -58) ska nås när ramens framsida ligger mellan -52 och -47
    holes.append(slot(s_ * CAM_X, Y_P - 11.0, Y_P - 6.0, CAM_TOP - 1, CAM_TOP + 5))
sled = D(sled, holes)
assert sled.is_watertight
sled.export(os.path.join(OUT, "asm_kamerafaste.stl"))      # monterat läge, för kontroll
# utskriftsläge: ramens baksida mot plattan (hus-y -> -z), överliggaren uppåt i plattans y
pr = sled.copy()
pr.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], float))
pr.apply_translation(-pr.bounds[0] * [1, 1, 1] - [pr.extents[0] / 2, pr.extents[1] / 2, 0])
pr.export(os.path.join(OUT, "15_kamerafaste.stl"))
print("kamerafäste:", np.round(pr.extents, 1))
