import sys, json, numpy as np, mujoco, time
from nutsim import *
import designs

DUMP = np.radians(130.0)

def run(des, n, seed, mu=0.5, cycles=50, dt=0.001, noflap=False, sweep=None, tsweep=0.7, stop_after_empty=None, tag='', kw=None, bump=None, torque=1.0, groove=None, spawn_box=(-40, 40, 44, 102, 185.0), snap=None):
    rng = np.random.default_rng(seed)
    pieces = getattr(designs, des)(**(kw or {}))
    nl = nuts(n, rng); sp = getattr(designs, des + '_spawn')(n, rng, **(kw or {})) if hasattr(designs, des + '_spawn') else grid_spawn(n, *spawn_box, rng=rng)
    fl = getattr(designs, des + '_flap')(**(kw or {})) if (hasattr(designs, des + '_flap') and not noflap) else None
    m = build(pieces, nl, sp, wheel=True, mu=mu, chimney=chimney_walls(), seed=seed, bump=bump, torque=torque, dt=dt, flap=fl)
    d = mujoco.MjData(m); dt = m.opt.timestep
    bid = [m.body("n%d" % i).id for i in range(n)]
    Z = lambda: np.array([d.xpos[b][2] for b in bid]) * 1000
    def sim(T, target0, target1=None):
        N = int(T / dt)
        for k in range(N):
            s = (k + 1) / N; s = 3 * s * s - 2 * s ** 3
            d.ctrl[0] = target0 if target1 is None else target0 + (target1 - target0) * s
            mujoco.mj_step(m, d)
    jq = m.joint("wj").qposadr[0]
    if sweep is not None:                      # fickan vilar i tömningsläget, sveper bakåt till `sweep` grader och fram igen
        BACK = np.radians(sweep); d.qpos[jq] = DUMP; sim(3.0, DUMP)
    else:
        sim(3.0, 0.0)
    z = Z(); cap_in = int(((z > 80) & (z < 176)).sum()); over = int((z >= 176).sum())
    gone = z < 45; res = []
    for c in range(cycles):
        if sweep is not None:
            sim(tsweep, DUMP, BACK); sim(0.3, BACK)
            stall_b = abs(d.qpos[jq] - BACK) > np.radians(6)
            sim(tsweep, BACK, DUMP); sim(0.5, DUMP)
            stall_f = abs(d.qpos[jq] - DUMP) > np.radians(6)
        else:
            sim(0.5, 0.0, DUMP); sim(0.4, DUMP)
            stall_f = abs(d.qpos[jq] - DUMP) > np.radians(6)
            sim(0.5, DUMP, 0.0); sim(0.5, 0.0)
            stall_b = abs(d.qpos[jq]) > np.radians(6)
        z = Z(); new = (z < 45) & ~gone; gone |= new
        res.append((int(new.sum()), bool(stall_f), bool(stall_b)))
        if gone.all(): break
        if stop_after_empty and len(res) >= stop_after_empty and all(r[0] == 0 for r in res[-stop_after_empty:]): break
    if snap is not None:
        np.save(snap, dict(flap=(float(d.qpos[m.joint('fj').qposadr[0]]) if fl else None), theta=float(d.qpos[m.joint('wj').qposadr[0]]), pos=np.array([d.xpos[b] for b in bid]) * 1000, mat=np.array([d.xmat[b] for b in bid]), size=np.array(nl)), allow_pickle=True)
    left = int((~gone).sum())
    return dict(tag=tag, des=des, kw=kw, n=n, seed=seed, mu=mu, start_in=cap_in, over=over, per_cycle=[r[0] for r in res],
                stall_f=sum(r[1] for r in res), stall_b=sum(r[2] for r in res), left=left, cycles=len(res))

if __name__ == "__main__":
    a = json.loads(sys.argv[1]); t0 = time.time()
    r = run(**a); r["sec"] = round(time.time() - t0)
    print(json.dumps(r))
