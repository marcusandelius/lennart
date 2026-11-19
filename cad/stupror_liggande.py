"""
Stuprör 9.6: liggande utskrift.

Stående stod röret på en punkt (spetsen av utkastaren, ca 3 mm² kontakt) och var 117 mm högt
och bara 8,4 mm tjockt, så det lossnade. Här läggs varje rör ner på sidan:
  * Röret ligger nästan i ett lodrätt plan: böjen upptill pekar ca 41 grader snett utåt-framåt,
    utkastaren nertill ca 35 grader. Utkastaren vrids runt rörets axel så att den pekar som böjen.
  * Röret läggs med sidan som vetter utåt-bakåt mot plattan. 9.6: i stället för en köl kapas röret
    plant 0,45 mm in (rörväggen är 1,27 mm, ca 0,8 mm blir kvar). Fasetten är ca 3,8 mm bred och
    går i jämnhöjd med röret, så den syns knappt. Klamrarnas ringar kapas i samma plan.
    Pinnarna pekar ca 40 grader uppåt.
Kör:  python3 stupror_liggande.py <23_stupror_gra.stl> <23_stupror_vit.stl> <stupror_T.npy> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh

G, V, TF, OUT = sys.argv[1:5]
FLAT = 0.45                # 9.6: i stället för köl kapas röret plant 0,45 mm in (vägg kvar ca 0,8 mm)
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")
T = np.load(TF)
g, v = trimesh.load(G), trimesh.load(V)
g.apply_transform(T); v.apply_transform(T)                 # husets koordinater


def ang(dx, dy): return np.arctan2(dy, dx)




laid = []
for pipe in g.split(only_watertight=False):
    side = np.sign(pipe.bounds.mean(0)[0])
    clamps = [c for c in v.split(only_watertight=False) if np.sign(c.bounds.mean(0)[0]) == side]
    vv = pipe.vertices
    sec = pipe.section(plane_origin=[0, 0, 50], plane_normal=[0, 0, 1]).bounds
    ax = (sec[0][:2] + sec[1][:2]) / 2                          # det raka rörets axel
    top = vv[vv[:, 2] > 113][:, :2].mean(0) - ax
    sho = vv[vv[:, 2] < 8][:, :2].mean(0) - ax
    a_top, a_sho = ang(*top), ang(*sho)
    # 1) vrid utkastaren runt axeln så att den ligger i samma plan som böjen
    low = vv[:, 2] < 14.0
    rot = a_top - a_sho
    c, s = np.cos(rot), np.sin(rot)
    p = vv[low, :2] - ax
    vv = vv.copy(); vv[low, :2] = ax + p @ np.array([[c, s], [-s, c]])
    pipe = trimesh.Trimesh(vv, pipe.faces, process=False)
    assert pipe.is_watertight
    # 2) nytt koordinatsystem: e1 = böjens riktning (vågrätt), e3 = upp = -n, där n pekar utåt-bakåt
    d = np.array([np.cos(a_top), np.sin(a_top), 0.0])
    n = np.array([-d[1], d[0], 0.0])
    if n[1] < 0: n = -n                                         # bakåt (+y)
    e3 = -n; e1 = d; e2 = np.cross(e3, e1)
    M = np.eye(4); M[:3, :3] = np.array([e1, e2, e3]); M[:3, 3] = -M[:3, :3] @ np.array([ax[0], ax[1], 0.0])
    house_z = lambda m: m.vertices[:, 2].copy()
    hz = house_z(pipe)
    for m in [pipe] + clamps: m.apply_transform(M)
    zmin = min(m.bounds[0][2] for m in [pipe] + clamps)
    for m in [pipe] + clamps: m.apply_translation([0, 0, -zmin])
    tube_bot = pipe.bounds[0][2]
    # 3) plan fasett: kapa rör och klammer under planet tube_bot + FLAT och sänk ner till z = 0
    cut = tube_bot + FLAT
    big = trimesh.creation.box(extents=[1000, 1000, 100]); big.apply_translation([0, 0, cut + 50])
    black = I(pipe, big)
    white = U([I(c, big) for c in clamps])
    for m in (black, white): m.apply_translation([0, 0, -cut])
    white = D(white, [black])
    black = trimesh.util.concatenate([q for q in black.split(only_watertight=False) if abs(q.volume) > 1.0])
    white = trimesh.util.concatenate([q for q in white.split(only_watertight=False) if abs(q.volume) > 1.0])
    assert black.is_watertight and white.is_watertight
    laid.append((side, black, white))
    print("rör %+d: vridning av utkastaren %.1f grader, fasett %.2f mm, mått %s" %
          (side, np.degrees(rot), FLAT, np.round(black.extents, 1).tolist()))

# lägg rören bredvid varandra, 6 mm isär
out_b, out_w, x = [], [], 0.0
for side, b, w in sorted(laid, key=lambda t: t[0]):
    grp = trimesh.util.concatenate([b, w]).bounds
    for m in (b, w): m.apply_translation([x - grp[0][0], -(grp[0][1] + grp[1][1]) / 2, 0])
    x = trimesh.util.concatenate([b, w]).bounds[1][0] + 6.0
    out_b.append(b); out_w.append(w)
B, W = trimesh.util.concatenate(out_b), trimesh.util.concatenate(out_w)
cx = (min(B.bounds[0][0], W.bounds[0][0]) + max(B.bounds[1][0], W.bounds[1][0])) / 2
for m in (B, W): m.apply_translation([-cx, 0, 0])
for m, n in ((B, "23_stupror_liggande_svart.stl"), (W, "23_stupror_liggande_vit.stl")):
    f = os.path.join(OUT, n); m.export(f)
    # efter export slås hörn ihop och nollvolymsflisor blir egna kroppar: rensa och spara igen
    r = trimesh.load(f)
    r = trimesh.util.concatenate([q for q in r.split(only_watertight=False) if abs(q.volume) > 1.0])
    r.export(f); r = trimesh.load(f)
    assert r.is_watertight, n
allb = trimesh.util.concatenate([B, W]).bounds
print("platta", np.round(allb[1] - allb[0], 1).tolist())
