# Projekt Lennart - fyller notmagasinet med hasselnotter som ligger helt inne i tratten (anvands av oppning.py, klipp 0.3).
# Varje not provas mot modellens riktiga vaggar: avstand till magasinet, hjulet och doserhuset minst notens storsta radie,
# vaggar at alla sidor (annars ar punkten utanfor magasinet) och notens topp under kanten. Notterna fylls pa nedifran som en hog.
# Kor:  blender -b -P notmagasin.py      (skriver film/notmagasin.json)
import bpy, json, os, random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE); ROOT = os.path.dirname(FILM)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, 'lennarts-matstation.glb'))
dg = bpy.context.evaluated_depsgraph_get()
def tree(n):
    o = bpy.data.objects[n]; me = o.evaluated_get(dg).to_mesh(); vs = [o.matrix_world @ v.co for v in me.vertices]
    return BVHTree.FromPolygons(vs, [tuple(p.vertices) for p in me.polygons])
MAG, HJUL, HUS = tree('notmagasin'), tree('doserhjul'), tree('doserhus')
NR = 0.0082; C = 1.26 * NR            # notens storsta radie (spetsen ar 1,24 x NR fran mitten)
RIM = 0.175                           # magasinets ovre kant (vaggarna slutar mellan 0,17 och 0,18)
def inne(p):
    for d in (Vector((0, 1, 0)), Vector((0, -1, 0)), Vector((-1, 0, 0))):   # vaggar runt om (framsidan x > 0 ar bortskuren i genomskarningen)
        h = MAG.ray_cast(p, d, 0.12)
        if h[0] is None or h[1].dot(d) > 0: return False                      # ingen vagg, eller vi ar inne i vaggens material (vaggens normal pekar mot oss fran halrummet)
    loc, nor, _, dist = MAG.find_nearest(p)
    if dist < C or (p - loc).dot(nor) < 0: return False
    for T in (HJUL, HUS):
        q = T.find_nearest(p)
        if q[3] is not None and q[3] < C: return False
    if (Vector((p.y, p.z)) - Vector((0.057, 0.0643))).length < 0.0312 + C: return False   # hjulet roterar: hogen ligger ovanfor hela hjulets cirkel, inte i fickan
    return p.z + C <= RIM
rng = random.Random(5); cand = [Vector((rng.uniform(-0.046, 0.0), rng.uniform(0.02, 0.11), rng.uniform(0.096, RIM))) for _ in range(60000)]
cand.sort(key=lambda p: p.z); pile = []
for p in cand:
    if all((p - q).length >= 1.9 * NR for q in pile) and inne(p): pile.append(p)
out = [[round(p.x, 5), round(p.y, 5), round(p.z, 5), round(rng.uniform(0, 6.28), 3), round(rng.uniform(-0.6, 0.6), 3), round(rng.uniform(0, 6.28), 3)] for p in pile]
json.dump(out, open(os.path.join(FILM, 'notmagasin.json'), 'w')); print('NOTTER', len(out), 'z', round(min(p.z for p in pile), 4), round(max(p.z for p in pile), 4))
