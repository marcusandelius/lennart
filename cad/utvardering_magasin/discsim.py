"""
Lutande plockskiva (myntautomat-princip). Allt i skivans lokala koordinater (u = vågrätt, v = uppför skivan, w = skivans normal),
tyngdkraften är lutad i stället för geometrin. Skivan vilar på en fast bottenplatta med ett utfallshål högst upp.
"""
import sys, json, time, numpy as np, mujoco
from nutsim import nuts

def circle(r, n=72):
    a = np.radians(np.arange(0, 360, 360 / n)); return np.c_[r * np.cos(a), r * np.sin(a)]
def prism(uv, w0, w1): uv = np.asarray(uv); return np.vstack([np.c_[uv, np.full(len(uv), w0)], np.c_[uv, np.full(len(uv), w1)]])
def holed_disc(R, hc, hh, w0, w1, octa=True):
    """Skiva med fyrkantigt/åttkantigt hål, halv sida hh, centrum (0, hc). Konvexa bitar."""
    C = circle(R); P = []
    sel = lambda f, extra: np.vstack([C[f(C)], extra])
    yl = lambda u: np.sqrt(max(R * R - u * u, 0))
    P.append(prism(sel(lambda c: c[:, 0] >= hh, [(hh, yl(hh)), (hh, -yl(hh))]), w0, w1))
    P.append(prism(sel(lambda c: c[:, 0] <= -hh, [(-hh, yl(hh)), (-hh, -yl(hh))]), w0, w1))
    P.append(prism(sel(lambda c: (np.abs(c[:, 0]) <= hh) & (c[:, 1] < hc - hh), [(-hh, hc - hh), (hh, hc - hh), (-hh, -yl(hh)), (hh, -yl(hh))]), w0, w1))
    if yl(hh) > hc + hh + 0.5:
        P.append(prism([(-hh, hc + hh), (hh, hc + hh), (-hh, yl(hh)), (hh, yl(hh))] + [tuple(c) for c in C[(np.abs(C[:, 0]) <= hh) & (C[:, 1] > hc + hh)]], w0, w1))
    if octa:
        c = hh * (1 - np.tan(np.radians(22.5)))
        for su in (-1, 1):
            for sv in (-1, 1):
                P.append(prism([(su * hh, hc + sv * hh), (su * (hh - c), hc + sv * hh), (su * hh, hc + sv * (hh - c))], w0, w1))
    return P

def build(n, seed, tilt=45.0, RD=46.0, TD=16.0, RP=30.0, HH=13.0, shroud_v=-8.0, shroud_h=26.0, mu=0.5, torque=1.0, dt=0.001, wall_h=150.0, holes=1):
    rng = np.random.default_rng(seed); mm = 0.001; meshes = []; sg = []; dg = []
    def add(pts, name, rgba, lst):
        meshes.append('<mesh name="%s" vertex="%s"/>' % (name, " ".join("%.6f" % (c * mm) for c in np.asarray(pts).ravel())))
        lst.append('<geom type="mesh" mesh="%s" rgba="%s" contype="0" conaffinity="1"/>' % (name, rgba))
    static = []
    static += holed_disc(RD + 4, RP, HH + 1.5, -3.0, 0.0, octa=False)                 # bottenplatta med utfallshål överst
    a = 0.0
    while a < 360:                                                                    # mantel
        pts = [((RD + 1 + d) * np.cos(np.radians(x)), (RD + 1 + d) * np.sin(np.radians(x)), w) for x in (a, a + 12) for d in (0, 2.4) for w in (-3.0, wall_h)]
        static.append(np.array(pts)); a += 12
    C = circle(RD + 1); yl = np.sqrt((RD + 1) ** 2 - shroud_v ** 2)
    static.append(prism(np.vstack([C[C[:, 1] >= shroud_v], [(-yl, shroud_v), (yl, shroud_v)]]), TD + shroud_h, TD + shroud_h + 2.4))   # skärm över övre halvan
    for i, p in enumerate(static): add(p, "s%d" % i, "0.2 0.2 0.2 0.3", sg)
    disc = holed_disc(RD, RP, HH, 0.0, TD)
    if holes == 2:
        pass
    for i, p in enumerate(disc): add(p, "d%d" % i, "0.8 0.66 0.4 1", dg)
    nl = nuts(n, rng); nb = []; k = 0; w = TD + shroud_h + 20.0
    while k < n:
        for u in np.arange(-30, 30.1, 24):
            for v in np.arange(-30, 30.1, 24):
                if k >= n or u * u + v * v > 34 ** 2: continue
                q = rng.normal(size=4); q /= np.linalg.norm(q); s = nl[k]
                nb.append('<body name="n%d" pos="%.5f %.5f %.5f" quat="%.4f %.4f %.4f %.4f"><freejoint/><geom type="ellipsoid" size="%.5f %.5f %.5f" density="1100"/></body>'
                          % (k, (u + rng.uniform(-1, 1)) * mm, (v + rng.uniform(-1, 1)) * mm, w * mm, *q, s[0] * mm, s[1] * mm, s[2] * mm)); k += 1
        w += 24.0
    t = np.radians(tilt); g = "0 %.4f %.4f" % (-9.81 * np.sin(t), -9.81 * np.cos(t))
    xml = ('<mujoco><compiler angle="radian"/><option timestep="%g" gravity="%s" integrator="implicitfast" cone="elliptic" impratio="20" noslip_iterations="4"/>'
           '<default><geom friction="%.2f 0.003 0.0002" solref="0.003 1" solimp="0.95 0.99 0.0005" condim="4"/></default><asset>%s</asset><worldbody>%s'
           '<body name="disc"><inertial pos="0 0 0.008" mass="0.08" diaginertia="5e-5 5e-5 9e-5"/><joint name="dj" type="hinge" axis="0 0 1" armature="2e-4" damping="0.02"/>%s</body>%s</worldbody>'
           '<actuator><position name="servo" joint="dj" kp="25" kv="0.6" forcerange="-%.3f %.3f" ctrlrange="-7 7"/></actuator></mujoco>'
           % (dt, g, mu, "".join(meshes), "".join(sg), "".join(dg), "".join(nb), torque, torque))
    return mujoco.MjModel.from_xml_string(xml), nl, static, disc

def run(n=40, seed=1, cycles=40, stop_after_empty=10, snap=None, tmove=0.8, pick=180.0, tag="", wiggle=0.0, **kw):
    m, nl, static, disc = build(n, seed, **kw); d = mujoco.MjData(m); dt = m.opt.timestep
    bid = [m.body("n%d" % i).id for i in range(n)]; jq = m.joint("dj").qposadr[0]
    W = lambda: np.array([d.xpos[b][2] for b in bid]) * 1000
    PICK = np.radians(pick); d.qpos[jq] = PICK
    def sim(T, a, b=None):
        N = int(T / dt)
        for k in range(N):
            s = (k + 1) / N; s = 3 * s * s - 2 * s ** 3; d.ctrl[0] = a if b is None else a + (b - a) * s; mujoco.mj_step(m, d)
    sim(3.5, PICK); gone = W() < -12; pre = int(gone.sum()); res = []
    for c in range(cycles):
        sim(tmove, PICK, 0.0); sim(0.5, 0.0); st_up = abs(d.qpos[jq]) > np.radians(6)
        sim(tmove, 0.0, PICK)
        if wiggle: wz = np.radians(wiggle); sim(0.35, PICK, PICK - wz); sim(0.35, PICK - wz, PICK)
        sim(0.6, PICK); st_dn = abs(d.qpos[jq] - PICK) > np.radians(6)
        new = (W() < -12) & ~gone; gone |= new; res.append((int(new.sum()), bool(st_up), bool(st_dn)))
        if gone.all(): break
        if stop_after_empty and len(res) >= stop_after_empty and all(r[0] == 0 for r in res[-stop_after_empty:]): break
    if snap:
        np.save(snap, dict(theta=float(d.qpos[jq]), pos=np.array([d.xpos[b] for b in bid]) * 1000, mat=np.array([d.xmat[b] for b in bid]), size=np.array(nl),
                           static=np.array(static, dtype=object), disc=np.array(disc, dtype=object), kw=kw), allow_pickle=True)
    return dict(tag=tag, des="skiva", kw=kw, n=n, seed=seed, mu=kw.get("mu", 0.5), start_in=n - pre, over=pre, per_cycle=[r[0] for r in res],
                stall_f=sum(r[1] for r in res), stall_b=sum(r[2] for r in res), left=int((~gone).sum()), cycles=len(res))

if __name__ == "__main__":
    a = json.loads(sys.argv[1]); t0 = time.time(); r = run(**a); r["sec"] = round(time.time() - t0); print(json.dumps(r))
