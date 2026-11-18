"""
Platta i svart PETG: kamerasläde (15), skärmklämma (19) och stuprör (23) med vita rörklammer.
Stuprören flyttas ihop (de låg 240 mm isär), varje rör tar med sig sina två klammer.
Släden och klämman läggs framför. Allt i ett gemensamt koordinatsystem, inget överlappar.
Kör:  python3 platta_svart.py <cad-katalog> <utkatalog>
"""
import sys, os, itertools
import numpy as np
import trimesh

C, OUT = sys.argv[1:3]
load = lambda f: trimesh.load(os.path.join(C, f))
gra, vit = load("stupror/23_stupror_gra.stl"), load("stupror/23_stupror_vit.stl")
pipes, clamps = gra.split(only_watertight=False), vit.split(only_watertight=False)
sv_out, vi_out, boxes = [], [], {}
for p in pipes:
    side = np.sign(p.bounds.mean(0)[0])
    cl = [c for c in clamps if np.sign(c.bounds.mean(0)[0]) == side]
    grp = trimesh.util.concatenate([p] + cl).bounds
    # vänster rör: högerkant vid x = -4, höger rör: vänsterkant vid x = 4. Bakkant vid y = 46.
    dx = (-4 - grp[1][0]) if side < 0 else (4 - grp[0][0])
    dy = 46 - grp[1][1]
    for m in [p] + cl: m.apply_translation([dx, dy, 0])
    sv_out.append(p); vi_out += cl
    boxes["stuprör %+d" % side] = trimesh.util.concatenate([p] + cl).bounds
sk, ka = load("19_skarmklamma.stl"), load("15_kamerafaste.stl")
sk.apply_translation([-74 - sk.bounds[0][0], -4 - sk.bounds[1][1], 0])     # fram till vänster
ka.apply_translation([10 - ka.bounds[0][0], -4 - ka.bounds[1][1], 0])      # fram till höger
boxes["skärmklämma"], boxes["kamerasläde"] = sk.bounds, ka.bounds
for (a, ba), (b, bb) in itertools.combinations(boxes.items(), 2):
    assert (ba[1][:2] < bb[0][:2]).any() or (bb[1][:2] < ba[0][:2]).any(), (a, b)
files = {"23_stupror_svart.stl": trimesh.util.concatenate(sv_out), "23_stupror_vit.stl": trimesh.util.concatenate(vi_out),
         "19_skarmklamma_svart.stl": sk, "15_kamerasläde_svart.stl": ka}
for n, m in files.items():
    assert m.is_watertight and m.bounds[0][2] > -0.01
    m.export(os.path.join(OUT, n))
allb = trimesh.util.concatenate(list(files.values())).bounds
for k, b in boxes.items(): print(k, np.round(b[:, :2], 1).tolist(), "höjd", round(b[1][2], 1))
print("hela plattan", np.round(allb[1][:2] - allb[0][:2], 1).tolist(), "mm")
