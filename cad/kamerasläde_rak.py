"""
Kamerasläde 9.8, rak kamera centrerad i kamerahålet (Raspberry Pi Camera Module 3 Wide).

Kamerahålet i gaveln (kroppens koordinater): axel x = 0, z = 167, Ø18. Fönstret (polykarbonat Ø24 x 3)
ligger i fickan på insidan, dess insida vid y = -63,87.
  * Kortet står lodrätt, linsen pekar rakt ut längs -y och ligger på hålets axel.
  * Linsens spets ca 1 mm bakom fönstret (antagen linshöjd 10 mm över kortets framsida).
  * 9.8: två långa spår (ett per hålkolumn) i stället för fyra korta hål. Kameran kan flyttas fritt
    från 2 mm upp till 10 mm ner jämfört med 9.7 (9.7 satt för högt). Distanserna är lösa (köpta M2-distanser,
    ca 4 mm): skruv M2 genom kameran, distansen och spåret, bricka och mutter bakom plattan.
  * Släden hänger på samma kameraklackar som förut (x = ±22, ovansida z = 175, insats y = -58)
    med två M3 x 10 uppifrån. Spåren i flikarna ger justering fram och tillbaka.
Kör:  python3 kamerasläde_rak.py <utkatalog>
Skriver 15_kamerafaste.stl (utskriftsläge) och asm_kamerafaste.stl (monterat, kroppens koordinater).
"""
import sys, os
import numpy as np
import trimesh
from trimesh.creation import cylinder, box as tbox
from shapely.geometry import LineString

OUT = sys.argv[1]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")

LZ = 167.0                     # hålets axel (höjd)
H_LENS = 10.0                  # linsens höjd över kortets framsida (antagen)
TIP_Y = -62.8                  # linsens spets, ca 1 mm bakom fönstret
B_FRONT = TIP_Y + H_LENS       # kortets framsida (y)
B_T, STANDOFF, PLATE_T = 1.0, 4.0, 3.5
P_FRONT = B_FRONT + B_T + STANDOFF
P_BACK = P_FRONT + PLATE_T
HX, HZ = 10.5, 6.25           # hålbild 21 x 12,5 mm
UP, DOWN = 2.0, 10.0          # kameran kan flyttas 2 mm upp och 10 mm ner från hålets axel
CAM_X, CAM_Y, CAM_TOP, SLIDE = 22.0, -58.0, 175.0, 2.5
FL_Y0 = CAM_Y - SLIDE - 1.7 - 1.0    # flikens framkant (väggen är vid y = -64,67)
PX, PZ0, PZ1 = 18.0, 144.5, 179.0
SLOT_Z0, SLOT_Z1 = LZ - HZ - DOWN, LZ + HZ + UP   # spårets mittlinje


def box(x0, x1, y0, y1, z0, z1):
    b = tbox(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def vcyl(r, x, y, z0, z1, sec=40):
    c = cylinder(radius=r, height=z1 - z0, sections=sec); c.apply_translation([x, y, (z0 + z1) / 2]); return c


def ycapsule(r, x, z, half, y0, y1):
    """avlång tapp/hål i (x, z), längs z, extruderad längs y"""
    poly = LineString([(x, z - half), (x, z + half)]).buffer(r, resolution=16)
    m = trimesh.creation.extrude_polygon(poly, y1 - y0)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
    if m.volume < 0: m.invert()
    m.apply_translation([0, y0, 0]); return m


parts = [box(-PX, PX, P_FRONT, P_BACK, PZ0, PZ1),                     # lodrät platta bakom kameran
         box(-26.5, 26.5, P_FRONT, P_BACK, 171.0, PZ1)]                # tvärslå uppe som bär flikarna
for s in (1, -1):
    xa, xb = sorted([s * 15.0, s * 26.5])
    parts.append(box(xa, xb, FL_Y0, P_BACK, CAM_TOP, CAM_TOP + 4.0))  # flik som vilar på klacken
    # stag under fliken på insidan av klacken (x 15-17,5), från flikens bakre del ner till plattan
    ca, cb = sorted([s * 15.0, s * 17.5])
    tri = [box(ca, cb, -52.0, P_BACK, CAM_TOP - 0.01, CAM_TOP + 4.0), box(ca, cb, P_FRONT, P_BACK, 163.0, CAM_TOP)]
    parts.append(trimesh.convex.convex_hull(np.vstack([t.vertices for t in tri])))
sled = U(parts)

holes = []
for sx in (1, -1):
    holes.append(ycapsule(1.15, sx * HX, (SLOT_Z0 + SLOT_Z1) / 2, (SLOT_Z1 - SLOT_Z0) / 2, P_FRONT - 1, P_BACK + 1))   # långt spår, M2
holes.append(box(-7.0, 7.0, P_FRONT - 1, P_BACK + 1, 147.0, 171.0))                         # komponenter och flatkabel
for s in (1, -1):
    r = 1.7
    holes += [vcyl(r, s * CAM_X, CAM_Y - SLIDE, CAM_TOP - 1, CAM_TOP + 5), vcyl(r, s * CAM_X, CAM_Y + SLIDE, CAM_TOP - 1, CAM_TOP + 5),
              box(s * CAM_X - r, s * CAM_X + r, CAM_Y - SLIDE, CAM_Y + SLIDE, CAM_TOP - 1, CAM_TOP + 5)]
sled = D(sled, holes)
assert sled.is_watertight
sled.export(os.path.join(OUT, "asm_kamerafaste.stl"))

# utskriftsläge: plattans baksida mot byggplattan, distanser och flikar uppåt
pr = sled.copy()
pr.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
pr.apply_translation([-(pr.bounds[0][0] + pr.bounds[1][0]) / 2, -(pr.bounds[0][1] + pr.bounds[1][1]) / 2, -pr.bounds[0][2]])
# lösa distanshylsor bredvid släden: av (köpta distanser används), sätt SPACERS = 6 för att skriva ut egna
SPACERS = 0
sp = []
for n in range(SPACERS):
    t = D(cylinder(radius=2.3, height=STANDOFF, sections=40), [cylinder(radius=1.15, height=STANDOFF + 2, sections=24)])
    t.apply_translation([pr.bounds[0][0] + 4 + n * 7.5, pr.bounds[0][1] - 6, STANDOFF / 2])
    sp.append(t)
pr = trimesh.util.concatenate([pr] + sp)
pr.apply_translation([-(pr.bounds[0][0] + pr.bounds[1][0]) / 2, -(pr.bounds[0][1] + pr.bounds[1][1]) / 2, -pr.bounds[0][2]])
pr.export(os.path.join(OUT, "15_kamerafaste.stl"))
print("kortets framsida y = %.2f, plattan y %.2f..%.2f, flikens framkant y = %.2f" % (B_FRONT, P_FRONT, P_BACK, FL_Y0))
print("spår z %.2f..%.2f: linsen kan stå på z %.1f..%.1f (hålets axel %.1f)" % (SLOT_Z0, SLOT_Z1, LZ - DOWN, LZ + UP, LZ))
print("kamerasläde:", np.round(pr.extents, 1), "volym cm3", round(pr.volume / 1000, 2))
