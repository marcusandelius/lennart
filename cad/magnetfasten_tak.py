"""
Byter magnethålen i takhalvorna (06_tak_vanster_gra.stl, 06b_tak_hoger_gra.stl) mot 6 x 3 mm.

Version 7: två hål Ø9,9 x 3,3 mm per halva, på takets undersida vid y = -45 och +45
(mittemot kroppens klackar). Taket skrivs ut med undersidan mot plattan.
Version 8: gamla hålen fylls, tre hål Ø5,9 x 4,0 mm med 0,3 mm infasning vid y = -45, 0, +45,
samma mått som i kroppen. Godset ovanför hålet blir minst 2,0 mm.

Kör:  python3 magnetfasten_tak.py <in.stl> <ut.stl> [hålets diameter]
"""
import sys
import numpy as np
import trimesh
from trimesh.creation import cylinder, cone

SRC, DST = sys.argv[1], sys.argv[2]
HOLE_D = float(sys.argv[3]) if len(sys.argv) > 3 else 5.9
HOLE_DEPTH, CHAMFER = 4.0, 0.3
OLD_R, OLD_DEPTH = 9.9 / 2, 3.3
Y_HOLES_OLD = [-45.0, 45.0]
Y_HOLES_NEW = [-45.0, 0.0, 45.0]

m = trimesh.load(SRC)
assert m.is_watertight
# hålens x: vänster halva -32.3, höger +32.3 (läses av från filen för säkerhets skull)
X = -32.3 if abs(m.bounds[0][0] + 80.41) < 0.1 else 32.3


def cyl(r, z0, z1, x, y, sec=64):
    c = cylinder(radius=r, height=z1 - z0, sections=sec)
    c.apply_translation([x, y, (z0 + z1) / 2]); return c


# 1) fyll de gamla hålen
plugs = [cyl(OLD_R + 0.25, 0.0, OLD_DEPTH + 0.1, X, y) for y in Y_HOLES_OLD]
m = trimesh.boolean.union([m] + plugs, engine="manifold")

# 2) nya hål från undersidan (z = 0) uppåt, infasning mot plattan
holes = []
r = HOLE_D / 2
for y in Y_HOLES_NEW:
    h = cyl(r, -1.0, HOLE_DEPTH, X, y)
    k = cone(radius=r + CHAMFER + 1.0, height=r + CHAMFER + 1.0, sections=60)  # 45 grader, spets uppåt
    k.apply_translation([X, y, -1.0])
    holes.append(trimesh.boolean.union([h, k], engine="manifold"))
# minustecknet (polaritet) som de gamla hålen har 10 mm bort: 5 x 1,2 mm, 0,6 mm djupt
for y in [yy for yy in Y_HOLES_NEW if yy not in Y_HOLES_OLD]:
    mark = trimesh.creation.box(extents=[5.0, 1.2, 0.7]); mark.apply_translation([X, y + 10.0, 0.25])
    holes.append(mark)
m = trimesh.boolean.difference([m] + holes, engine="manifold")
assert m.is_watertight
m.export(DST)
print("klart:", DST, "hål vid x =", X, "y =", Y_HOLES_NEW, "volym cm3", round(m.volume / 1000, 2))
