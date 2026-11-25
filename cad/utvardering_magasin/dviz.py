import sys, json, numpy as np, trimesh
from discsim import run
def export(snap, out, tilt=45.0):
    S = np.load(snap, allow_pickle=True).item(); t = np.radians(tilt)
    R = trimesh.transformations.rotation_matrix(t, [1, 0, 0])         # lokalt (u,v,w) -> värld: w lutar bakåt
    soup = lambda m: [round(float(v), 2) for v in m.vertices[m.faces].ravel()]
    def hull(ps, rot=None):
        ms = [trimesh.convex.convex_hull(np.asarray(p, float)) for p in ps]; m = trimesh.util.concatenate(ms)
        if rot is not None: m.apply_transform(rot)
        m.apply_transform(R); return m
    G = {"mag": soup(hull(S["static"])), "wheel": soup(hull(S["disc"], trimesh.transformations.rotation_matrix(S["theta"], [0, 0, 1])))}
    ns = []
    for p, M, s in zip(S["pos"], S["mat"], S["size"]):
        e = trimesh.creation.icosphere(subdivisions=2, radius=1.0); e.apply_scale(s); T = np.eye(4); T[:3, :3] = np.asarray(M).reshape(3, 3); T[:3, 3] = p; e.apply_transform(T); e.apply_transform(R); ns.append(e)
    G["nuts"] = soup(trimesh.util.concatenate(ns)); json.dump(G, open(out, "w"))
if __name__ == "__main__":
    name = sys.argv[1]; a = json.loads(sys.argv[2]); r = run(snap="dsnap_%s.npy" % name, **a)
    print(name, "".join(map(str, r["per_cycle"])), "stopp", r["stall_f"], r["stall_b"], "kvar", r["left"])
    export("dsnap_%s.npy" % name, "../render/geo_%s.json" % name, a.get("tilt", 45.0))
