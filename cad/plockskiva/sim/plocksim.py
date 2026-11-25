import sys, json, time, numpy as np, mujoco
from nutsim import nuts
import plock as K

def build(n, seed, mu=0.5, torque=1.0, dt=0.001, chute=True, geo=None, agit=None, sizes=None):
    if geo: K.configure(**geo)
    rng = np.random.default_rng(seed); mm = 0.001; meshes = []; sg = []; dg = []
    def add(pts, name, lst, rgba="0.3 0.3 0.3 0.3"):
        meshes.append('<mesh name="%s" vertex="%s"/>' % (name, " ".join("%.6f" % (v * mm) for v in np.asarray(pts).ravel())))
        lst.append('<geom type="mesh" mesh="%s" rgba="%s" contype="0" conaffinity="1"/>' % (name, rgba))
    st = K.static_pieces(chute)
    for i, p in enumerate(st): add(p, "s%d" % i, sg)
    dc = K.disc_pieces()
    for i, p in enumerate(dc): add(p, "d%d" % i, dg, "0.8 0.66 0.4 1")      # lokala koordinater, kroppen bär lutningen
    if agit:                                    # omrörare på skivans axel: pinne genom skärmen och en arm ovanför (lokala mått i mm)
        a0_, a1_, w0_, w1_, th_, fi_ = agit[:6]   # armen går från a0 till a1 i riktningen fi (grader, skivans egen ram: 270 = uppför skivan i plockläget, 180 = bakåt)
        rt_ = agit[6] if len(agit) > 6 else 0.0   # rundad topp med den radien
        w1r_ = w1_; w1_ = w1_ - rt_
        dg.append('<geom type="cylinder" fromto="0 0 %.4f 0 0 %.4f" size="0.005" rgba="0.8 0.3 0.2 1" contype="0" conaffinity="1"/>' % ((K.GAP + K.TD) * mm, w0_ * mm))
        cen, hl, f_ = (a0_ + a1_) / 2, (a1_ - a0_) / 2, np.radians(fi_)
        dg.append('<geom type="box" pos="%.4f %.4f %.4f" euler="0 0 %.5f" size="%.4f %.4f %.4f" rgba="0.8 0.3 0.2 1" contype="0" conaffinity="1"/>' % (cen * np.cos(f_) * mm, cen * np.sin(f_) * mm, (w0_ + w1_) / 2 * mm, f_, hl * mm, th_ * mm, (w1_ - w0_) / 2 * mm))
    if agit and rt_ > 0:
        tx, ty = -np.sin(f_) * th_, np.cos(f_) * th_
        dg.append('<geom type="cylinder" fromto="%.4f %.4f %.4f %.4f %.4f %.4f" size="%.4f" rgba="0.8 0.3 0.2 1" contype="0" conaffinity="1"/>' % (cen * np.cos(f_) * mm - tx * mm, cen * np.sin(f_) * mm - ty * mm, w1_ * mm, cen * np.cos(f_) * mm + tx * mm, cen * np.sin(f_) * mm + ty * mm, w1_ * mm, rt_ * mm))
    R = K.T[:3, :3]; q = mujoco.mju_mat2Quat if False else None
    quat = np.zeros(4); mujoco.mju_mat2Quat(quat, R.flatten())
    nl = nuts(n, rng, sizes=tuple(sizes)) if sizes else nuts(n, rng); nb = []; k = 0; z = K.ZT + 15.0
    xs = np.arange(K.XL + 14, K.XARC0 - 6, 23.0); ys = np.arange(K.YF + 13, K.YB - 12, 23.0)
    while k < n:
        for x in xs:
            for y in ys:
                if k >= n: break
                qq = rng.normal(size=4); qq /= np.linalg.norm(qq); a = nl[k]
                nb.append('<body name="n%d" pos="%.5f %.5f %.5f" quat="%.4f %.4f %.4f %.4f"><freejoint/><geom type="ellipsoid" size="%.5f %.5f %.5f" density="1100"/></body>'
                          % (k, (x + rng.uniform(-1, 1)) * mm, (y + rng.uniform(-1, 1)) * mm, z * mm, *qq, a[0] * mm, a[1] * mm, a[2] * mm)); k += 1
        z += 24.0
    # fyllnadsschakt ovanför förrådet så att inget hamnar utanför
    for i, (x0, x1, y0, y1) in enumerate(((K.XL - 3, K.XL, K.YF - 3, K.YB + 3), (K.XARC0 + 16, K.XARC0 + 19, K.YF - 3, K.YB + 3), (K.XL - 3, K.XARC0 + 19, K.YF - 3, K.YF), (K.XL - 3, K.XARC0 + 19, K.YB, K.YB + 3))):
        add(np.array([(x, y, zz) for x in (x0, x1) for y in (y0, y1) for zz in (K.ZT, K.ZT + 400)]), "f%d" % i, sg, "0.5 0.5 0.9 0.1")
    xml = ('<mujoco><compiler angle="radian"/><option timestep="%g" integrator="implicitfast" cone="elliptic" impratio="20" noslip_iterations="4"/>'
           '<default><geom friction="%.2f 0.003 0.0002" solref="0.003 1" solimp="0.95 0.99 0.0005" condim="4"/></default><asset>%s</asset><worldbody>'
           '<geom type="plane" pos="0 0 -0.02" size="1 1 0.01" friction="1 0.1 0.1"/>%s'
           '<body name="disc" pos="%.5f %.5f %.5f" quat="%.6f %.6f %.6f %.6f"><inertial pos="0 0 0.008" mass="0.08" diaginertia="5e-5 5e-5 9e-5"/>'
           '<joint name="dj" type="hinge" axis="0 0 1" armature="2e-4" damping="0.02"/>%s</body>%s</worldbody>'
           '<actuator><position name="servo" joint="dj" kp="25" kv="0.6" forcerange="-%.3f %.3f" ctrlrange="-7 7"/></actuator></mujoco>'
           % (dt, mu, "".join(meshes), "".join(sg), *(K.C * mm), *quat, "".join(dg), "".join(nb), torque, torque))
    return mujoco.MjModel.from_xml_string(xml), nl, st, dc

def run(n=40, seed=1, cycles=40, stop_after_empty=12, snap=None, tmove=0.9, wiggle=40.0, tag="", record=None, dwell=0.7, **kw):
    m, nl, st, dc = build(n, seed, **kw); d = mujoco.MjData(m); dt = m.opt.timestep
    bid = [m.body("n%d" % i).id for i in range(n)]; jq = m.joint("dj").qposadr[0]
    P = lambda: np.array([d.xpos[b] for b in bid]) * 1000
    PICK = np.pi; EXIT = float(K.QX); d.qpos[jq] = PICK; frames = []; kk = [0]
    def sim(T, a, b=None, ph=0):
        N = int(T / dt)
        for k in range(N):
            x = (k + 1) / N; x = 3 * x * x - 2 * x ** 3; d.ctrl[0] = a if b is None else a + (b - a) * x; mujoco.mj_step(m, d); kk[0] += 1
            if record and ph and kk[0] % record == 0: frames.append((ph, float(d.qpos[jq]), np.hstack([np.array([d.xpos[b_] for b_ in bid]) * 1000, np.array([d.xquat[b_] for b_ in bid])])))
    sim(4.0, PICK)
    p = P(); inside = (p[:, 2] > 20) & (p[:, 0] > K.XL - 5) & (p[:, 1] > 15) & ~((p[:, 1] < 20) & (p[:, 2] < 40)); over = int((p[:, 2] > K.ZT - 2).sum())
    out = lambda p: ((p[:, 1] < 3.0) & (p[:, 2] < 45)) | ((p[:, 2] < 0.0) & (p[:, 1] < K.CH_B[1] + 12.0) & (np.abs(p[:, 0] - K.CH_B[0]) < 30.0))   # ute genom rännans mynning
    below = lambda p: (p[:, 2] < 30) & ~out(p) & (np.hypot(p[:, 0] - K.CH_B[0], 0) > 30)     # hamnat fel (på golvet utanför rännan)
    gone = out(p); pre = int(gone.sum()); res = []; wz = np.radians(wiggle)
    if record: sim(0.6, PICK, ph=1)
    for c in range(cycles):
        sim(tmove, PICK, EXIT, ph=2); sim(dwell, EXIT, ph=3); su = abs(d.qpos[jq] - EXIT) > np.radians(6)
        sim(tmove, EXIT, PICK, ph=4)
        if wiggle: sim(0.35, PICK, PICK - wz, ph=4); sim(0.35, PICK - wz, PICK, ph=4)
        sim(0.7, PICK, ph=1); sd = abs(d.qpos[jq] - PICK) > np.radians(6)
        p = P(); new = out(p) & ~gone; gone |= new; res.append((int(new.sum()), bool(su), bool(sd)))
        if (gone | ~inside).all(): break
        if stop_after_empty and len(res) >= stop_after_empty and all(r[0] == 0 for r in res[-stop_after_empty:]): break
    p = P(); stuck = int(((p[:, 2] < 60) & ~gone & (p[:, 1] < 60) & (p[:, 2] < 52) & (np.abs(p[:, 0]) < 30)).sum())
    if snap: np.save(snap, dict(theta=float(d.qpos[jq]), pos=p, quat=np.array([d.xquat[b] for b in bid]), size=np.array(nl)), allow_pickle=True)
    if record: np.save(record if isinstance(record, str) else "rec.npy", dict(frames=frames, size=np.array(nl)), allow_pickle=True)
    return dict(tag=tag, des="plock", kw=kw, n=n, seed=seed, mu=kw.get("mu", 0.5), start_in=int(inside.sum()), over=over, pre=pre, per_cycle=[r[0] for r in res],
                stall_f=sum(r[1] for r in res), stall_b=sum(r[2] for r in res), left=int((inside & ~gone).sum()), fel=int(below(p).sum()), i_rannan=stuck, cycles=len(res))

if __name__ == "__main__":
    a = json.loads(sys.argv[1]); t0 = time.time(); r = run(**a); r["sec"] = round(time.time() - t0); print(json.dumps(r))
