"""
Fönsterinsatser med mindre pluggar: plattan (z 0-1,8) är oförändrad, pluggarna som trycks in i
fönstret (z 1,8-3,8) krymps 1 mm på varje sida, från 21,5 x 16,5 till 19,5 x 14,5 mm.
Kör:  python3 fonsterinsatser_mindre.py <in.stl> <ut.stl> [krympning mm]
"""
import sys
import numpy as np
import trimesh
from shapely.geometry import JOIN_STYLE

SRC, DST = sys.argv[1:3]
SHRINK = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
PLATE_TOP, TOP = 1.8, 3.8
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")

m = trimesh.load(SRC)
cut = trimesh.creation.box(extents=[1000, 1000, PLATE_TOP]); cut.apply_translation([0, 0, PLATE_TOP / 2])
plate = I(m, cut)
pl, _ = m.section(plane_origin=[0, 0, (PLATE_TOP + TOP) / 2], plane_normal=[0, 0, 1]).to_2D(to_2D=np.eye(4))
plugs = []
for p in pl.polygons_full:
    q = p.buffer(-SHRINK, join_style=JOIN_STYLE.mitre)
    e = trimesh.creation.extrude_polygon(q, TOP - PLATE_TOP + 0.01); e.apply_translation([0, 0, PLATE_TOP - 0.01])
    plugs.append(e)
    b = np.array(p.bounds); nb = np.array(q.bounds)
    print("plugg %.1f x %.1f -> %.1f x %.1f" % (b[2] - b[0], b[3] - b[1], nb[2] - nb[0], nb[3] - nb[1]))
out = U([plate] + plugs)
assert out.is_watertight
out.export(DST)
print("klar", np.round(out.bounds, 2).tolist())
