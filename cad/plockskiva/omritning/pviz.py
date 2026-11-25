import sys, json, numpy as np, trimesh
import plock as K
def soup(m): return [round(float(v), 2) for v in m.vertices[m.faces].ravel()]
def hull(ps): return trimesh.util.concatenate([trimesh.convex.convex_hull(np.asarray(p, float)) for p in ps])
def qmat(q):
    w, x, y, z = q; return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def export(snap, out, chute=True):
    S = np.load(snap, allow_pickle=True).item()
    G = {"mag": soup(hull(K.static_pieces(chute)))}
    d = hull(K.disc_pieces()); d.apply_transform(trimesh.transformations.rotation_matrix(S["theta"], [0, 0, 1])); d.apply_transform(K.T); G["wheel"] = soup(d)
    ns = []
    for p, q, s in zip(S["pos"], S["quat"], S["size"]):
        e = trimesh.creation.icosphere(subdivisions=2, radius=1.0); e.apply_scale(s); M = np.eye(4); M[:3, :3] = qmat(q); M[:3, 3] = p; e.apply_transform(M); ns.append(e)
    G["nuts"] = soup(trimesh.util.concatenate(ns)); json.dump(G, open(out, "w"))
if __name__ == "__main__":
    from plocksim import run
    name = sys.argv[1]; a = json.loads(sys.argv[2])
    if a.get("geo"): K.configure(**a["geo"])
    r = run(snap="snap_%s.npy" % name, **a)
    print(name, "".join(map(str, r["per_cycle"])), "stopp", r["stall_f"], r["stall_b"], "kvar", r["left"], "fel", r["fel"], "i rännan", r["i_rannan"], "start", r["start_in"])
    export("snap_%s.npy" % name, "../render/geo_%s.json" % name)
