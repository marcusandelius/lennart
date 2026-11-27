"""Rännan: släpp en nöt i taget genom utfallshålet (skivan står i släppläget) och räkna hur många som fastnar."""
import sys, json, numpy as np, mujoco
import plock as K

def variant(slope=38.0, land=12.0, wide=0.0, skin=3.0, shift=0.0):
    K.configure(slope=slope, land=land); K.SKIN = skin
    if shift:                                                          # flytta den sneda främre vänstra väggen utåt parallellt
        F = K.CH_FUN.copy(); N = K.CH_NECK.copy()
        a, b = np.array(F[3], float), np.array(F[4], float); dvec = (b - a) / np.linalg.norm(b - a); nrm = np.array([dvec[1], -dvec[0]])
        if nrm @ (np.array([K.EX[0], K.EX[1]]) - a) > 0: nrm = -nrm          # utåt = bort från utfallet
        a2 = a + nrm * shift
        t3 = (F[2][0] - a2[0]) / dvec[0]; p3 = a2 + dvec * t3                    # skärning med den raka vänstra väggen (x = F[2].x)
        t4 = (N[3][0] - a2[0]) / dvec[0]; p4 = a2 + dvec * t4                    # skärning med halsens vänstra vägg (x = N[3].x)
        F[3] = p3; F[4] = p4; N[3] = p4
        K.CH_FUN = F; K.CH_NECK = N; K.CH_POLY = np.array([N[0], N[1], F[0], F[1], F[2], F[3], F[4]])
    if wide:
        F = K.CH_FUN.copy(); F[3] = (F[3][0], F[3][1] - wide)          # vänstra raka väggen fortsätter längre fram innan den viker mot halsen
        K.CH_FUN = F; K.CH_POLY = np.array([K.CH_NECK[0], K.CH_NECK[1], F[0], F[1], F[2], F[3], F[4]])

def build(mu):
    mm = 0.001; meshes = []; geoms = []
    def add(pts, name, rgba="0.3 0.3 0.3 1"):
        meshes.append('<mesh name="%s" vertex="%s"/>' % (name, " ".join("%.6f" % (v * mm) for v in np.asarray(pts).ravel())))
        geoms.append('<geom name="g_%s" type="mesh" mesh="%s" rgba="%s" contype="0" conaffinity="1"/>' % (name, name, rgba))
    for i, p in enumerate(K.static_pieces(True)): add(p, "s%d" % i)
    for i, p in enumerate(K.disc_pieces()):                            # skivan i släppläget (fickan över hålet)
        q = np.asarray(p, float); uv = K.rot(q[:, :2], K.QX); add(K.W(np.c_[uv, q[:, 2]]), "d%d" % i)
    xml = ('<mujoco><option timestep="0.001" integrator="implicitfast" cone="elliptic" impratio="20" noslip_iterations="4"/>'
           '<default><geom friction="%.2f 0.003 0.0002" solref="0.003 1" solimp="0.95 0.99 0.0005" condim="4"/></default><asset>%s</asset><worldbody>'
           '<geom type="plane" pos="0 0 -0.02" size="1 1 0.01"/>%s<body name="n" pos="0 0 0.5"><freejoint/><geom name="ng" type="ellipsoid" size="0.009 0.008 0.008" density="1100"/></body>'
           '</worldbody></mujoco>' % (mu, "".join(meshes), "".join(geoms)))
    return mujoco.MjModel.from_xml_string(xml)

def trials(n=60, seed=1, mu=0.5, Lr=(16, 22), Wr=(14, 18), T=2.0):
    m = build(mu); d = mujoco.MjData(m); rng = np.random.default_rng(seed); gid = m.geom("ng").id
    res = []; uE, vE = -K.RP * np.sin(K.QX), K.RP * np.cos(K.QX)
    start = K.W([uE, vE, K.GAP + K.TD * 0.5])[0]
    for t in range(n):
        L, W = rng.uniform(*Lr), rng.uniform(*Wr); W = min(W, L)
        m.geom_size[gid] = np.array([L / 2, W / 2, W / 2 * rng.uniform(0.9, 1.0)]) * 0.001
        m.geom_rbound[gid] = L / 2 * 0.001 * 1.05
        mujoco.mj_resetData(m, d)
        q = rng.normal(size=4); q /= np.linalg.norm(q)
        d.qpos[:3] = (start + np.r_[rng.uniform(-2, 2, 2), 0]) * 0.001; d.qpos[3:7] = q
        out = False; k = 0
        while k < int(T / 0.001):
            mujoco.mj_step(m, d); k += 1
            if k % 50 == 0:
                p = d.qpos[:3] * 1000
                if p[1] < K.CH_B[1] - 1.0 or p[2] < 2.0: out = True; break
        touch = sorted({m.geom(d.contact[i].geom1 if d.contact[i].geom2 == gid else d.contact[i].geom2).name or str(d.contact[i].geom1) for i in range(d.ncon) if gid in (d.contact[i].geom1, d.contact[i].geom2)})
        res.append((round(L, 1), round(W, 1), out, [round(v, 1) for v in d.qpos[:3] * 1000], touch))
    return res

if __name__ == "__main__":
    a = json.loads(sys.argv[1]); variant(**a.get("geo", {}))
    r = trials(n=a.get("n", 60), seed=a.get("seed", 1), mu=a.get("mu", 0.5), Lr=tuple(a.get("L", (16, 22))), Wr=tuple(a.get("W", (14, 18))))
    stuck = [x for x in r if not x[2]]
    print(json.dumps(dict(geo=a.get("geo", {}), mu=a.get("mu", 0.5), n=len(r), fast=len(stuck), exempel=stuck[:6])))
