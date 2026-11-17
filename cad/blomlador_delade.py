"""
Blomlådor delade i två delar per låda:
  * Lådan (vit): botten sänkt 1,5 mm, skrivs ut liggande på framsidan (plan mot plattan, inget stöd under botten).
  * Växtinsats (grön): växterna står på en 1,5 mm jordplatta som släpps ner i lådan
    (0,25 mm spel runt om). Skrivs ut stående, plattan mot byggplattan.
Kör:  python3 blomlador_delade.py <21_blomlador_vit_v7.stl> <21_blomlador_gron_v7.stl> <utkatalog> [monterat-katalog]
"""
import sys, os
import numpy as np
import trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VIT, GRON, OUT = sys.argv[1:4]
ASM = sys.argv[4] if len(sys.argv) > 4 else None     # valfritt: spara även monterat läge (för förhandsvisning)
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


from blad import leaf
# blad i lådans lokala koordinater: x från baksidan (väggsidan) mot framsidan, y längs lådan,
# azimut 0 = framåt, 90 = +y, 180 = bakåt, 270 = -y. (x, y, azimut, längd, bredd)
LEAVES = [
    # stjälken vid y = -12,9
    (9.0, -13.9, 262, 14.0, 3.3), (9.8, -11.9, 80, 11.5, 3.0), (10.5, -12.9, 12, 7.0, 2.6), (8.2, -12.9, 192, 7.0, 2.6),
    # stjälken vid y = 0
    (9.0, -1.0, 265, 14.0, 3.3), (9.8, 1.0, 95, 14.0, 3.3), (10.5, 0.0, 350, 7.0, 2.6), (8.2, 0.0, 168, 9.0, 2.8),
    # stjälken vid y = 12,9
    (9.0, 11.9, 278, 11.5, 3.0), (9.8, 13.9, 98, 14.0, 3.3), (10.5, 12.9, 8, 7.0, 2.6), (8.2, 12.9, 188, 7.0, 2.6),
    # fyllnad i ändarna och mellan stjälkarna
    (6.0, -17.0, 250, 7.0, 2.6), (6.0, 17.0, 110, 7.0, 2.6), (11.5, -18.0, 285, 6.5, 2.4), (11.5, 18.0, 75, 6.5, 2.4),
    (6.0, -6.5, 205, 9.0, 2.8), (6.0, 6.5, 155, 9.0, 2.8), (11.0, -6.5, 320, 7.0, 2.5), (11.0, 6.5, 40, 7.0, 2.5),
]
LOG = []
STEM_Y = [-12.9, 0.0, 12.9]
STEM_X = 9.5
LEAF_SCALE = 1.4          # bladen räcker en bit över kanten
RIM = 24.6                # lådans överkant
FLOWER_Z, FLOWER_R = 28.0, 7.6   # blomhuvudenas undersida och radie med marginal


def vaxter(side, back, gron):
    """Stjälkarna från originalet (utan bladklumpar) och nya, smala blad."""
    olds = [p for p in gron.split(only_watertight=False) if np.sign(p.bounds.mean(0)[0]) == side and p.bounds[1][2] > 30]
    stems = []
    for y in STEM_Y:
        p = min(olds, key=lambda q: abs(q.bounds.mean(0)[1] - y))
        x = back + side * STEM_X
        c1 = trimesh.creation.cylinder(radius=1.75, height=11.5, sections=48); c1.apply_translation([x, y, 15 + 11.5 / 2])
        c2 = trimesh.creation.cylinder(radius=2.8, height=15.0, sections=48); c2.apply_translation([x, y, 26.5 + 7.5])
        stems.append(I(p, U([c1, c2])))
    leaves = []
    for lx, ly, az, L, w in LEAVES:
        azw = az if side > 0 else 180 - az                     # spegla för vänster låda
        L *= LEAF_SCALE
        while True:                                            # korta bladet tills det går fritt
            lf = leaf([back + side * lx, ly, FLOOR - 0.3], azw, L, w)
            if leaf_ok(lf, side, back) or L < 4: break
            L -= 0.5
        leaves.append(lf); LOG.append(round(L, 1))
    return stems + leaves


def leaf_ok(lf, side, back):
    """Under kanten (z < RIM) måste bladet rymmas i lådans insida så att insatsen kan sänkas ner rakt,
    och uppe vid blommorna (z > FLOWER_Z) får det inte gå in under ett blomhuvud."""
    v = lf.vertices
    lo = v[v[:, 2] < RIM]
    lx = (lo[:, 0] - back) * side
    if (lx < IN_X[0] + 0.4).any() or (lx > IN_X[1] - 0.4).any() or (np.abs(lo[:, 1]) > IN_Y - 0.4).any():
        return False
    hi = v[v[:, 2] > FLOWER_Z]
    for y in STEM_Y:
        if len(hi) and (np.hypot(hi[:, 0] - (back + side * STEM_X), hi[:, 1] - y) < FLOWER_R).any():
            return False
    return True


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
    plate = box(xi0 + CLR, xi1 - CLR, -IN_Y + CLR, IN_Y - CLR, FLOOR - PLATE, FLOOR + 0.05)
    cuts = []
    for px0, px1, py0, py1 in POSTS:
        a, b = sorted([back + side * px0, back + side * px1])
        cuts.append(box(a - POST_CLR, b + POST_CLR, py0 - POST_CLR, py1 + POST_CLR, FLOOR - PLATE - 1, 60))
    ins = D(U([plate] + vaxter(side, back, gron)), cuts)
    ins = max(ins.split(only_watertight=False), key=lambda p: abs(p.volume))     # bara den sammanhängande insatsen
    if ASM:
        lad.export(os.path.join(ASM, f"asm_lada_{int(side):+d}.stl")); ins.export(os.path.join(ASM, f"asm_insats_{int(side):+d}.stl"))
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
