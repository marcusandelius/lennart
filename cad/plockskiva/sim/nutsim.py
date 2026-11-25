"""
Fysiksimulering (MuJoCo) av nötmagasin över doserhjulet. Alla mått i mm i husets ram:
hjulets axel längs x genom (y 57, z 64.3), radie 31, bredd x -17..17, fickan 24.2 mm rakt upp vid vinkel 0.
Varje magasin beskrivs som en lista konvexa bitar (punktmoln). Nötterna är ellipsoider.
"""
import numpy as np, mujoco

CY, CZ, RW = 57.0, 64.3, 31.0
RS = 32.2                    # sadelns innerradie
PW = 12.1                    # fickans halva bredd
PF = 9.6                     # fickans botten (radie)
T = 2.4                      # väggtjocklek


def plate(quad, n, t=T):
    """Konvex platta: inre fyrhörning (4 punkter) plus samma förskjuten utåt längs n."""
    q = np.asarray(quad, float); n = np.asarray(n, float); n = n / np.linalg.norm(n)
    return np.vstack([q, q + n * t])


def hopper(levels, t=T):
    """levels: [(z, x0, x1, y0, y1), ...] uppifrån och ned. Ger väggplattor mellan nivåerna."""
    P = []
    for (za, a0, a1, b0, b1), (zb, c0, c1, d0, d1) in zip(levels[:-1], levels[1:]):
        P.append(plate([(a0, b0, za), (a0, b1, za), (c0, d1, zb), (c0, d0, zb)], (-1, 0, 0), t))
        P.append(plate([(a1, b0, za), (a1, b1, za), (c1, d1, zb), (c1, d0, zb)], (1, 0, 0), t))
        P.append(plate([(a0, b0, za), (a1, b0, za), (c1, d0, zb), (c0, d0, zb)], (0, -1, 0), t))
        P.append(plate([(a0, b1, za), (a1, b1, za), (c1, d1, zb), (c0, d1, zb)], (0, 1, 0), t))
    return P


def saddle(a_open0, a_open1, x0=-17.0, x1=17.0, step=6.0, groove=None, r_front=None):
    """Sadeln runt hjulets övre halva (vinkel 0 = +y, 90 = rakt upp, 180 = -y). Öppen mellan a_open0 och a_open1."""
    P = []
    def arc(a0, a1, xa, xb):
        RS_ = r_front if (r_front and a0 >= a_open1 - 1e-6) else RS
        a = a0
        while a < a1 - 1e-6:
            b = min(a + step, a1); pts = []
            for ang in (a, b):
                for r in (RS_, RS_ + 3.0):
                    for x in (xa, xb):
                        pts.append((x, CY + r * np.cos(np.radians(ang)), CZ + r * np.sin(np.radians(ang))))
            P.append(np.array(pts)); a = b
    for a0, a1 in ((0.0, a_open0), (a_open1, 180.0)):
        if groove is None: arc(a0, a1, x0, x1)
        else:
            arc(a0, a1, x0, -groove); arc(a0, a1, groove, x1)
    return P


def side_cheeks(a_open0, a_open1, xin, x0=-17.0, x1=17.0, step=6.0):
    """Sadelns kanter inom öppningen: från xin ut till x0/x1 (när öppningen är smalare än hjulet)."""
    P = []
    a = a_open0
    while a < a_open1 - 1e-6:
        b = min(a + step, a_open1)
        for xa, xb in ((x0, -xin), (xin, x1)):
            pts = []
            for ang in (a, b):
                for r in (RS, RS + 3.0):
                    for x in (xa, xb):
                        pts.append((x, CY + r * np.cos(np.radians(ang)), CZ + r * np.sin(np.radians(ang))))
            P.append(np.array(pts))
        a = b
    return P


def wheel_pieces(bump=None):
    """Hjulet i lokala koordinater (axel x, fickan mot +z). Konvexa bitar."""
    ang = np.radians(np.arange(0, 360, 5.0)); circ = np.c_[RW * np.cos(ang), RW * np.sin(ang)]   # (y, z)
    def prism(yz, xa, xb): return np.vstack([np.c_[np.full(len(yz), xa), yz], np.c_[np.full(len(yz), xb), yz]])
    def clip(pred, extra): return np.vstack([circ[pred(circ)], extra])
    s = np.sqrt(RW ** 2 - PW ** 2)
    P = [prism(clip(lambda c: c[:, 0] >= PW, [(PW, s), (PW, -s)]), -17, 17),
         prism(clip(lambda c: c[:, 0] <= -PW, [(-PW, s), (-PW, -s)]), -17, 17),
         prism(clip(lambda c: (np.abs(c[:, 0]) <= PW) & (c[:, 1] < 0), [(-PW, PF), (PW, PF), (-PW, -s), (PW, -s)]), -17, 17)]
    top = clip(lambda c: (np.abs(c[:, 0]) <= PW) & (c[:, 1] > 0), [(-PW, PF), (PW, PF), (-PW, s), (PW, s)])
    P += [prism(top, PW, 17), prism(top, -17, -PW)]
    c = PW * (1 - np.tan(np.radians(22.5)))                    # åttkantiga hörn, så att fickan blir nästan rund
    for sx in (-1, 1):
        for sy in (-1, 1):
            tri = [(sx * PW, sy * PW), (sx * (PW - c), sy * PW), (sx * PW, sy * (PW - c))]
            P.append(np.array([(x, y, z) for x, y in tri for z in (PF, s - 0.5)]))
    if bump:                                                    # (vinkel från fickan i grader, höjd, radie)
        a, h, r = bump; a = np.radians(90 - a)
        P.append(("sphere", (0.0, (RW + h - r) * np.cos(a), (RW + h - r) * np.sin(a)), r))
    return P


def nuts(n, rng, pointed=False, sizes=(15.0, 18.5, 18.0, 22.0)):
    N = []
    for _ in range(n):
        w = rng.uniform(sizes[0], sizes[1]); l = rng.uniform(sizes[2], sizes[3]); t = w * rng.uniform(0.9, 1.0)
        N.append((w / 2, t / 2, max(l, w + 0.5) / 2))
    return N


def build(pieces, nutlist, spawn, wheel=True, mu=0.5, bump=None, chimney=None, torque=1.0, seed=0, dt=0.0005, flap=None):
    """spawn: lista av (x, y, z) i mm för nötternas startlägen."""
    rng = np.random.default_rng(seed)
    mm = 0.001; meshes = []; geoms = []
    def add(pts, name, rgba):
        v = " ".join("%.6f" % (c * mm) for c in np.asarray(pts).ravel())
        meshes.append('<mesh name="%s" vertex="%s"/>' % (name, v))
        return '<geom type="mesh" mesh="%s" rgba="%s" contype="0" conaffinity="1"/>' % (name, rgba)
    for i, p in enumerate(pieces): geoms.append(add(p, "h%d" % i, "0.2 0.2 0.2 0.35"))
    if chimney:
        for i, p in enumerate(chimney): geoms.append(add(p, "c%d" % i, "0.5 0.5 0.9 0.2"))
    wb = ""
    if wheel:
        wg = []
        for i, p in enumerate(wheel_pieces(bump)):
            if isinstance(p, tuple): wg.append('<geom type="sphere" pos="%.5f %.5f %.5f" size="%.5f" rgba="0.9 0.3 0.3 1" contype="0" conaffinity="1"/>' % (*[c * mm for c in p[1]], p[2] * mm))
            else: wg.append(add(p, "w%d" % i, "0.6 0.6 0.6 1"))
        wb = ('<body name="wheel" pos="0 %.5f %.5f"><inertial pos="0 0 0" mass="0.09" diaginertia="5e-5 3e-5 3e-5"/>'
              '<joint name="wj" type="hinge" axis="1 0 0" armature="2e-4" damping="0.02"/>%s</body>') % (CY * mm, CZ * mm, "".join(wg))
    nb = []
    for i, ((a, b, c), (x, y, z)) in enumerate(zip(nutlist, spawn)):
        q = rng.normal(size=4); q /= np.linalg.norm(q)
        vol = 4 / 3 * np.pi * a * b * c * 1e-9
        nb.append('<body name="n%d" pos="%.5f %.5f %.5f" quat="%.4f %.4f %.4f %.4f"><freejoint/>'
                  '<geom type="ellipsoid" size="%.5f %.5f %.5f" density="1100" rgba="0.72 0.45 0.2 1"/></body>'
                  % (i, x * mm, y * mm, z * mm, *q, a * mm, b * mm, c * mm))
    fb = ""
    if flap:   # dict(x0, x1, y, zh (gångjärn), L, k)
        fb = ('<body name="flap" pos="%.5f %.5f %.5f"><inertial pos="0 0 %.5f" mass="0.002" diaginertia="2e-7 2e-7 2e-7"/>'
              '<joint name="fj" type="hinge" axis="-1 0 0" stiffness="%.4f" damping="0.003" limited="true" range="0 1.4"/>'
              '<geom type="box" size="%.5f 0.0006 %.5f" pos="0 0 %.5f" rgba="0.2 0.6 0.9 1" contype="0" conaffinity="1"/></body>'
              % ((flap["x0"] + flap["x1"]) / 2 * mm, flap["y"] * mm, flap["zh"] * mm, -flap["L"] / 2 * mm, flap["k"],
                 (flap["x1"] - flap["x0"]) / 2 * mm, flap["L"] / 2 * mm, -flap["L"] / 2 * mm))
    act = '<actuator><position name="servo" joint="wj" kp="25" kv="0.6" forcerange="-%.3f %.3f" ctrlrange="-0.5 3.5"/></actuator>' % (torque, torque) if wheel else ""
    xml = ('<mujoco><compiler angle="radian"/><option timestep="%g" integrator="implicitfast" cone="elliptic" impratio="20" noslip_iterations="4"/>'
           '<default><geom friction="%.2f 0.003 0.0002" solref="0.003 1" solimp="0.95 0.99 0.0005" condim="4"/></default>'
           '<asset>%s</asset><worldbody><geom type="plane" pos="0 0 -0.25" size="1 1 0.01" friction="1 0.1 0.1"/>%s%s%s</worldbody>%s</mujoco>'
           % (dt, mu, "".join(meshes), "".join(geoms), wb + fb, "".join(nb), act))
    return mujoco.MjModel.from_xml_string(xml)


def grid_spawn(n, x0, x1, y0, y1, z0, pitch=24.0, rng=None):
    S = []; z = z0
    while len(S) < n:
        for x in np.arange(x0 + 12, x1 - 11.9, pitch):
            for y in np.arange(y0 + 12, y1 - 11.9, pitch):
                j = rng.uniform(-1.0, 1.0, 3) if rng is not None else np.zeros(3)
                S.append((x + j[0], y + j[1], z + j[2]))
        z += pitch
    return S[:n]


def chimney_walls(x0=-45.6, x1=45.6, y0=40.0, y1=106.0, z0=176.0, z1=600.0):
    return hopper([(z1, x0, x1, y0, y1), (z0, x0, x1, y0, y1)])
