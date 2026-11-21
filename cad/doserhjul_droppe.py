"""
Doserhjul (11) med droppformad nötficka.

Fickan är ett runt hål (Ø24,2, vidare Ø27 vid mynningen) som går in från hjulets kant. Hjulet
skrivs ut med axeln lodrätt, så hålets tak blir ett platt överhäng, och där hålet möter
ytterkanten blev det kvar 0,3 mm tunna flisor som började i luften ("floating cantilever").
Här får hålet ett tak med 45 graders lutning (droppform) upp till z = 32, så att det går att
skriva ut utan stöd. Flisorna försvinner. Hjulets ovansida (z = 34,5) har kvar 2,5 mm material.
Fickans botten (x = 9,5) och storlek nedåt är oförändrade.
Kör:  python3 doserhjul_droppe.py <11_doserhjul_original.stl> <ut.stl>
"""
import sys
import numpy as np
import trimesh
from shapely.geometry import Polygon

SRC, DST = sys.argv[1:3]
ZC, R, Z_TOP = 17.0, 13.5, 32.0          # hålets mitt och mynningens radie, takets platta topp
X0, X1 = 9.55, 40.0                       # från fickans botten och ut förbi kanten

t = R / np.sqrt(2)                        # tangentpunkt vid 45 grader
yt, zt = t, ZC + t
y_top = yt - (Z_TOP - zt)
roof = Polygon([(-yt, zt), (-y_top, Z_TOP), (y_top, Z_TOP), (yt, zt), (0, ZC)])
prism = trimesh.creation.extrude_polygon(roof, X1 - X0)       # (y, z) i planet, längs x
prism.apply_transform(np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
if prism.volume < 0: prism.invert()
prism.apply_translation([X0 - prism.bounds[0][0], 0, 0])

w = trimesh.load(SRC)
out = trimesh.boolean.difference([w, prism], engine="manifold")
out = trimesh.util.concatenate([q for q in out.split(only_watertight=False) if abs(q.volume) > 1.0])
assert out.is_watertight
out.export(DST)
n = out.face_normals; c = out.triangles_center; a = out.area_faces
print("tak: 45 grader från y = ±%.1f, z = %.1f upp till platt topp %.1f mm bred på z = %.1f" % (yt, zt, 2 * y_top, Z_TOP))
print("kroppar", len(out.split(only_watertight=False)), "plant överhäng över z 20: %.0f mm²" %
      a[(n[:, 2] < -0.999) & (c[:, 2] > 20)].sum(), "(före: %.0f)" % w.area_faces[(w.face_normals[:, 2] < -0.999) & (w.triangles_center[:, 2] > 20)].sum())
