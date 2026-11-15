"""
Litet provstycke för magneterna 6 x 3 mm: en bit av kroppens magnetklack med fem hål
i samma 43-gradersvinkel som i kroppen. Diametrar 5,8 / 5,9 / 6,0 / 6,1 / 6,2 mm.
Antalet prickar på framsidan under hålet = hål nr 1-5 (1 prick = 5,8 mm ... 5 prickar = 6,2 mm).
Kör:  python3 magnettest.py <ut.stl>
"""
import sys
import numpy as np
import trimesh
from trimesh.creation import cylinder, cone, extrude_polygon
from shapely.geometry import Polygon

DST = sys.argv[1]
DIAMS = [5.8, 5.9, 6.0, 6.1, 6.2]
PITCH = 13.0
DEPTH, CHAMFER, CUP_WALL = 4.0, 0.3, 1.2
P0 = np.array([82.4, 162.15]); TOP = np.array([74.0, 170.05])
t = (TOP - P0) / np.linalg.norm(TOP - P0); n = np.array([-t[1], t[0]]) * -1
HOLE_U = 6.04
Z0 = 152.0                      # provbiten kapas här (blir plattan)
L = PITCH * len(DIAMS) + 3

prof = Polygon([(82.4, Z0), (74.0, Z0), (74.0, 170.05), (82.4, 162.15)])
blk = extrude_polygon(prof, L)
blk.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
if blk.volume < 0: blk.invert()

def frame(yc):
    M = np.eye(4); M[:3, 0] = [t[0], 0, t[1]]; M[:3, 1] = [0, 1, 0]; M[:3, 2] = [n[0], 0, n[1]]
    M[:3, 3] = [P0[0], yc, P0[1]]; return M

def lcyl(r, w0, w1):
    c = cylinder(radius=r, height=w1 - w0, sections=64); c.apply_translation([HOLE_U, 0, (w0 + w1) / 2]); return c

adds, subs = [], []
for i, d in enumerate(DIAMS):
    yc = 1.5 + PITCH / 2 + i * PITCH
    r = d / 2
    cup = lcyl(r + CUP_WALL, -(DEPTH + CUP_WALL), -0.01); cup.apply_transform(frame(yc)); adds.append(cup)
    h = lcyl(r, -DEPTH, 1.0)
    k = cone(radius=r + CHAMFER + 1.0, height=r + CHAMFER + 1.0, sections=64)
    k.apply_transform(np.diag([1, 1, -1, 1])); k.apply_translation([HOLE_U, 0, 1.0])
    h = trimesh.boolean.union([h, k], engine="manifold"); h.apply_transform(frame(yc)); subs.append(h)
    # prickar på den lodräta framsidan (x = 82.4), Ø1.2 x 0.6 djupa
    for j in range(i + 1):
        dot = cylinder(radius=0.6, height=1.2, sections=24)
        dot.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
        dot.apply_translation([82.4, yc + (j - i / 2) * 2.0, Z0 + 4.5])
        subs.append(dot)

m = trimesh.boolean.union([blk] + adds, engine="manifold")
clip = []
for i in range(len(DIAMS)):
    b = trimesh.creation.box(extents=[30, PITCH + 2, 10]); b.apply_translation([HOLE_U, 0, 5.0])
    b.apply_transform(frame(1.5 + PITCH / 2 + i * PITCH)); clip.append(b)
base_cut = trimesh.creation.box(extents=[200, 200, 50]); base_cut.apply_translation([78, L / 2, Z0 - 25])
m = trimesh.boolean.difference([m] + clip + subs + [base_cut], engine="manifold")
m.apply_translation(-np.array([m.bounds[0][0], m.bounds[0][1], Z0]))
assert m.is_watertight
m.export(DST)
print("klart:", DST, np.round(m.extents, 1), "volym cm3", round(m.volume / 1000, 2))
