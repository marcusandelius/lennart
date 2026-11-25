import sys, numpy as np, mujoco, time
from nutsim import *
import designs
def handtest(des, n, seed, mu, T=4.0, dt=0.0005):
    rng = np.random.default_rng(seed)
    pieces = getattr(designs, des)()
    nl = nuts(n, rng); sp = grid_spawn(n, -40, 40, 44, 102, 150.0, rng=rng)
    m = build(pieces, nl, sp, wheel=False, mu=mu, chimney=chimney_walls(), seed=seed, dt=dt)
    d = mujoco.MjData(m); t0 = time.time()
    for _ in range(int(T / m.opt.timestep)): mujoco.mj_step(m, d)
    z = np.array([d.body("n%d" % i).xpos[2] for i in range(n)]) * 1000
    return int((z > 80).sum()), time.time() - t0
des, mu = sys.argv[1], float(sys.argv[2]); DT = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0005
for n in (8, 20):
    r = [handtest(des, n, s, mu, dt=DT) for s in range(10)]
    print(des, "mu", mu, "nötter", n, "kvar i magasinet:", [a for a, _ in r], "tid/körning %.1f s" % np.mean([b for _, b in r]))
