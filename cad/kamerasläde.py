"""
Kamerasläde (version 9.1) för Raspberry Pi Camera Module 3 Wide.

Kameran lutar 35 grader nedåt, som i det ursprungliga fästet, så att den ser framgården.
Släden vilar med två vågräta flikar på kameraklackarna (x = ±22, ovansida z = 175, insats vid y = -58)
och skruvas fast uppifrån med två M3 x 10. Flikarnas spår ger 5 mm rörelse fram och tillbaka,
så att linsen kan skjutas fram tills den nästan nuddar fönstret.

Kameran skruvas på fyra distanser (hål 21 x 12,5 mm, Ø2,2 genomgående, M2 med mutter bakom).
Linsens mitt antas ligga mitt mellan hålraderna, som i det förra fästet.

Kör:  python3 kamerasläde.py <utkatalog>
Skriver 15_kamerafaste.stl (utskriftsläge) och asm_kamerafaste.stl (monterat, kroppens koordinater).
"""
import sys, os
import numpy as np
import trimesh
from trimesh.creation import cylinder, box as tbox

OUT = sys.argv[1]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")

TILT = np.radians(35.0)
A = np.array([0, -np.cos(TILT), -np.sin(TILT)])      # linsens riktning, ut och ner
UP = np.array([0, -np.sin(TILT), np.cos(TILT)])      # kortets "upp"
X = np.array([1.0, 0, 0])
H_NOM = 10.0                                          # linsens höjd över kortets framsida (antagen)
TIP = np.array([0, -62.8, 167.7])                     # linsens spets i nominellt läge, ca 1 mm från fönstret
ORIG = TIP - H_NOM * A                                # kortets framsida, på linsens axel
BOARD_T, STANDOFF, PLATE_T = 1.0, 4.0, 3.0
HX, HU = 10.5, 6.25
CAM_X, CAM_Y, CAM_TOP = 22.0, -58.0, 175.0
SLIDE = 2.5
FL_Y0, FL_Y1 = -63.5, -49.5                           # flikens utsträckning i y (nominellt)

M = np.eye(4); M[:3, 0] = X; M[:3, 1] = UP; M[:3, 2] = -A; M[:3, 3] = ORIG   # lokal: x, u (upp längs kortet), w (bakåt ut ur kortet)


def lbox(x0, x1, u0, u1, w0, w1):
    b = tbox(extents=[x1 - x0, u1 - u0, w1 - w0]); b.apply_translation([(x0 + x1) / 2, (u0 + u1) / 2, (w0 + w1) / 2])
    b.apply_transform(M); return b


def lcyl(r, x, u, w0, w1, sec=40):
    c = cylinder(radius=r, height=w1 - w0, sections=sec); c.apply_translation([x, u, (w0 + w1) / 2])
    c.apply_transform(M); return c


def box(x0, x1, y0, y1, z0, z1):
    b = tbox(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def vcyl(r, x, y, z0, z1, sec=40):
    c = cylinder(radius=r, height=z1 - z0, sections=sec); c.apply_translation([x, y, (z0 + z1) / 2]); return c


W_PF = BOARD_T + STANDOFF                  # plattans framsida (w, bakåt från kortets framsida)
W_PB = W_PF + PLATE_T
PX, PU0, PU1 = 18.0, -14.0, 13.0

parts = [lbox(-PX, PX, PU0, PU1, W_PF, W_PB)]                      # lutande platta
for sx in (1, -1):
    for su in (1, -1):
        parts.append(lcyl(2.6, sx * HX, su * HU, BOARD_T, W_PF + 0.5))   # distanser
for s in (1, -1):
    xa, xb = sorted([s * 15.0, s * 26.5])
    flange = box(xa, xb, FL_Y0, FL_Y1, CAM_TOP, CAM_TOP + 4.0)
    parts.append(flange)
    # liv mellan plattans kant och fliken (x 15-18): konvext hölje av plattkanten och flikens inre del
    ca, cb = sorted([s * 15.0, s * 18.0])
    edge = lbox(ca, cb, PU0, PU1, W_PF, W_PB)
    fin = box(ca, cb, FL_Y0, FL_Y1, CAM_TOP, CAM_TOP + 4.0)
    parts.append(trimesh.convex.convex_hull(np.vstack([edge.vertices, fin.vertices])))
sled = U(parts)

holes = []
for sx in (1, -1):
    for su in (1, -1):
        holes.append(lcyl(1.1, sx * HX, su * HU, -1, W_PB + 1, sec=24))          # M2 genomgående
holes.append(lbox(-7.0, 7.0, -10.0, 3.5, W_PF - 1, W_PB + 1))                     # öppning för kontakt och komponenter
for s in (1, -1):
    r = 1.7
    holes += [vcyl(r, s * CAM_X, CAM_Y - SLIDE, CAM_TOP - 1, CAM_TOP + 5), vcyl(r, s * CAM_X, CAM_Y + SLIDE, CAM_TOP - 1, CAM_TOP + 5),
              box(s * CAM_X - r, s * CAM_X + r, CAM_Y - SLIDE, CAM_Y + SLIDE, CAM_TOP - 1, CAM_TOP + 5)]
sled = D(sled, holes)
assert sled.is_watertight
sled.export(os.path.join(OUT, "asm_kamerafaste.stl"))

# utskriftsläge: den lutande plattans baksida mot byggplattan, distanserna och flikarna uppåt
pr = sled.copy()
pr.apply_transform(trimesh.transformations.rotation_matrix(np.radians(235), [1, 0, 0]))
pr.apply_translation([-(pr.bounds[0][0] + pr.bounds[1][0]) / 2, -(pr.bounds[0][1] + pr.bounds[1][1]) / 2, -pr.bounds[0][2]])
pr.export(os.path.join(OUT, "15_kamerafaste.stl"))
print("kamerasläde:", np.round(pr.extents, 1), "volym cm3", round(pr.volume / 1000, 2))
