"""
Nötmagasin (14) med grepphål i stället för handtag.

Handtaget (44 x 4 mm) stack upp 10 mm över överkanten. Vid utskrift upp och ner stod magasinet
bara på handtaget och hela överkanten behövde stöd. Nu:
  * Handtaget tas bort, så magasinet står på hela överkanten (ca 750 mm²) utan stöd.
  * Ett avlångt grepphål, 30 x 12 mm, tas upp i samma vägg 4-16 mm under överkanten.
    Nötterna (18-22 mm) kan inte ramla ut genom det.
Filen ligger i utskriftsläge: överkanten mot plattan.
Kör:  python3 notmagasin_grepphal.py <14_notmagasin_original.stl> <ut.stl>
"""
import sys
import numpy as np
import trimesh
from shapely.geometry import LineString

SRC, DST = sys.argv[1:3]
RIM_Z = 10.0                        # överkanten i originalfilen (handtaget under)
SLOT_W, SLOT_H, SLOT_Z0 = 30.0, 12.0, 4.0
WALL_Y0, WALL_Y1 = -42.8, -40.4     # väggen där handtaget satt

m = trimesh.load(SRC)
keep = trimesh.creation.box(extents=[400, 400, 400]); keep.apply_translation([0, 0, RIM_Z + 200])
m = trimesh.boolean.intersection([m, keep], engine="manifold")
m.apply_translation([0, 0, -RIM_Z])
r = SLOT_H / 2
poly = LineString([(-SLOT_W / 2 + r, SLOT_Z0 + r), (SLOT_W / 2 - r, SLOT_Z0 + r)]).buffer(r, resolution=24)
slot = trimesh.creation.extrude_polygon(poly, (WALL_Y1 - WALL_Y0) + 2.0)
slot.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))   # (x, z) i planet, längs y
if slot.volume < 0: slot.invert()
slot.apply_translation([0, WALL_Y0 - 1.0 - slot.bounds[0][1], 0])
m = trimesh.boolean.difference([m, slot], engine="manifold")
m = trimesh.util.concatenate([q for q in m.split(only_watertight=False) if abs(q.volume) > 1.0])
assert m.is_watertight
m.export(DST)
n = m.face_normals; c = m.triangles_center
print("mått", np.round(m.extents, 1), "kontakt %.0f mm²" % m.area_faces[(n[:, 2] < -0.999) & (c[:, 2] < 0.05)].sum(),
      "överhäng >45°: %.0f mm²" % m.area_faces[(n[:, 2] < -0.71) & (c[:, 2] > 0.3)].sum())
