# Projekt Lennart - lagger notterna pa fatet i del 2 sa att de vilar pa riktigt (anvands av akt_plan.py).
# De undre notterna sanks tills de vilar pa fatet. De ovre sanks tills de far kontakt med notterna under, och far glida
# hogst 5 mm i sidled ner i gropen mellan dem (lagsta lage vinner), som en riktig not som lagger sig tillratta.
# Kor:  blender -b -P notfat.py      (skriver film/notfat.json: [x, y, rz, z over golvet] for varje not i POP-ordning)
import bpy, json, os, math
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, radius=1); n0 = bpy.context.active_object     # samma notform som i akt_plan.py
for v in n0.data.vertices:
    x, y, z = v.co
    if z > 0: k = 1 - 0.30 * z ** 2.2; x *= k; y *= k; z = z * 1.08 + 0.16 * z ** 6
    else: z = max(z * 0.95, -0.78)
    v.co = (x * 1.04, y * 0.98, z)
VS = [v.co.copy() for v in n0.data.vertices]; FS = [tuple(p.vertices) for p in n0.data.polygons]; NR = 0.0085; PLATE_TOP = 0.005
BOTTOM = [(0.185, -0.15, 0.6), (0.176, -0.126, 5.1), (0.212, -0.128, 2.0), (0.228, -0.148, 1.2), (0.207, -0.158, 3.7), (0.194, -0.174, 4.4)]
TOP = [(0.196, -0.144, 0.9), (0.212, -0.146, 2.8), (0.203, -0.132, 5.6)]
def rot(rz): return Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(1.15 + 0.25 * math.sin(rz * 3), 4, 'X') @ Matrix.Scale(NR, 4)   # samma vridning som i akt_plan.py
def pts(x, y, rz, z): M = Matrix.Translation((x, y, z)) @ rot(rz); return [M @ v for v in VS]
def tree(x, y, rz, z): return BVHTree.FromPolygons(pts(x, y, rz, z), FS)
def on_plate(rz): return PLATE_TOP - min((rot(rz) @ v).z for v in VS)
out, obst = [], []
for x, y, rz in BOTTOM:
    z = on_plate(rz); out.append([x, y, rz, z]); obst.append(tree(x, y, rz, z))
for i, a in enumerate(out):        # kontroll: de undre ska inte ga in i varandra
    for j in range(i + 1, len(out)):
        if obst[i].overlap(obst[j]): print('VARNING undre notter overlappar', i, j)
def hits(x, y, rz, z): t = tree(x, y, rz, z); return any(t.overlap(o) for o in obst)
for x0, y0, rz in TOP:
    best = None
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            x, y = x0 + dx * 0.001, y0 + dy * 0.001; lo, hi = on_plate(rz), 0.05
            if not hits(x, y, rz, lo): z = lo                      # inget under: den vilar pa fatet
            else:
                for _ in range(22):                                # binarsokning efter hojden dar den precis ror vid notterna under
                    mid = (lo + hi) / 2
                    if hits(x, y, rz, mid): lo = mid
                    else: hi = mid
                z = hi - 0.00012                                   # en tiondels millimeter in i kontakten, sa att ingen glipa syns
            score = z + 0.0004 * math.hypot(dx, dy)                # lagst vinner, minsta mojliga flytt vid lika
            if best is None or score < best[0]: best = (score, x, y, z)
    _, x, y, z = best; out.append([x, y, rz, z]); obst.append(tree(x, y, rz, z + 0.00012))
    print('OVRE', round(x, 4), round(y, 4), 'z', round(z, 4), 'flytt mm', round((x - x0) * 1000, 1), round((y - y0) * 1000, 1))
json.dump([[round(v, 5) for v in r] for r in out], open(os.path.join(FILM, 'notfat.json'), 'w')); print('UNDRE z', [round(r[3], 4) for r in out[:6]])
