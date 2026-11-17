"""
Blomlådor delade i två delar per låda:
  * Lådan (vit): botten sänkt 1,5 mm, skrivs ut liggande på framsidan (plan mot plattan, inget stöd under botten).
  * Växtinsats (grön): växterna står på en 1,5 mm jordplatta som släpps ner i lådan
    (0,25 mm spel runt om). Skrivs ut stående, plattan mot byggplattan.
Kör:  python3 blomlador_delade.py <21_blomlador_vit_v7.stl> <21_blomlador_gron_v7.stl> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh

VIT, GRON, OUT = sys.argv[1:4]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")
FLOOR, PLATE, CLR = 16.0, 1.5, 0.25
IN_X = (1.6, 14.4)        # lådans insida i x, räknat från lådans baksida (väggsidan)
POSTS = [(2.2, 3.8, 12.0, 17.0), (2.2, 3.8, -17.0, -12.0)]   # upphängningens stolpar inne i lådan (x från baksidan, y)
POST_CLR = 0.3
IN_Y = 21.4               # ± i y


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


vit = trimesh.load(VIT); gron = trimesh.load(GRON)
boxes, inserts = [], []
for c in vit.split(only_watertight=False):
    side = np.sign(c.bounds.mean(0)[0])                       # +1 höger låda (baksidan mot x = 85), -1 vänster
    back = c.bounds[0][0] if side > 0 else c.bounds[1][0]
    xi0, xi1 = sorted([back + side * IN_X[0], back + side * IN_X[1]])
    pocket = box(xi0, xi1, -IN_Y, IN_Y, FLOOR - PLATE, FLOOR + 0.01)
    keep = []
    for px0, px1, py0, py1 in POSTS:                          # stolparna ska stå kvar
        a, b = sorted([back + side * px0, back + side * px1])
        keep.append(box(a, b, py0, py1, FLOOR - PLATE - 1, FLOOR + 1))
    lad = D(c, [D(pocket, keep)])
    plants = trimesh.util.concatenate([p for p in gron.split(only_watertight=False) if np.sign(p.bounds.mean(0)[0]) == side])
    foot = box(xi0 + CLR, xi1 - CLR, -IN_Y + CLR, IN_Y - CLR, FLOOR - PLATE, 60)
    ins = U([box(xi0 + CLR, xi1 - CLR, -IN_Y + CLR, IN_Y - CLR, FLOOR - PLATE, FLOOR + 0.05), I(plants, foot)])
    cuts = []
    for px0, px1, py0, py1 in POSTS:
        a, b = sorted([back + side * px0, back + side * px1])
        cuts.append(box(a - POST_CLR, b + POST_CLR, py0 - POST_CLR, py1 + POST_CLR, FLOOR - PLATE - 1, 60))
    ins = D(ins, cuts)
    ins = trimesh.util.concatenate([p for p in ins.split(only_watertight=False) if abs(p.volume) > 1.0])   # bort med lösa bladspetsar
    # utskriftslägen
    lad.apply_transform(trimesh.transformations.rotation_matrix(side * np.pi / 2, [0, 1, 0]))   # framsidan nedåt
    for m in (lad, ins):
        m.apply_translation([-(m.bounds[0][0] + m.bounds[1][0]) / 2, -(m.bounds[0][1] + m.bounds[1][1]) / 2, -m.bounds[0][2]])
    assert lad.is_watertight and ins.is_watertight
    boxes.append(lad); inserts.append(ins)


def row(ms, gap=6.0):
    out, x = [], 0.0
    for m in ms:
        m = m.copy(); m.apply_translation([x - m.bounds[0][0], 0, 0]); out.append(m); x = m.bounds[1][0] + gap
    r = trimesh.util.concatenate(out); r.apply_translation([-(r.bounds[0][0] + r.bounds[1][0]) / 2, 0, 0]); return r


row(boxes).export(os.path.join(OUT, "21_blomlador_vit.stl"))
row(inserts).export(os.path.join(OUT, "21_blomlador_vaxter_gron.stl"))
for n, ms in (("lådor", boxes), ("växtinsatser", inserts)):
    print(n, [np.round(m.extents, 1).tolist() for m in ms])
