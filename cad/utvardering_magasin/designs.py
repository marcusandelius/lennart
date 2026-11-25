import numpy as np
from nutsim import hopper, saddle, side_cheeks, plate, CY, CZ, RS

TOP = (176.0, -45.6, 45.6, 40.0, 106.0)
ang = lambda y: np.degrees(np.arccos((y - CY) / RS))      # sadelvinkel för ett y vid öppningskanten
zs = lambda y: CZ + np.sqrt(RS ** 2 - (y - CY) ** 2)


def A():
    """Dagens magasin: tratt 50 grader, utlopp 26 x 30."""
    L = [TOP, (138.6, -45.6, 45.6, 40.0, 106.0), (98.6, -13.0, 13.0, 42.0, 72.0), (92.5, -13.0, 13.0, 42.0, 72.0)]
    return hopper(L) + saddle(ang(72.0), ang(42.0)) + side_cheeks(ang(72.0), ang(42.0), 13.0)


def B(deg=62.0, xo=13.0, y1=72.0):
    """Brantare tratt, samma utlopp, utloppet vidgas 1 mm nedåt."""
    h = (45.6 - xo) * np.tan(np.radians(deg)); zt = min(98.6 + h, 170.0)
    L = [TOP, (zt, -45.6, 45.6, 40.0, 106.0), (98.6, -xo, xo, 42.0, y1), (zs(y1) - 0.3, -xo - 1.0, xo + 1.0, 41.0, y1 + 1.0)]
    return hopper(L) + saddle(ang(y1 + 1.0), ang(41.0)) + side_cheeks(ang(y1 + 1.0), ang(41.0), xo + 1.0)


def D(deg=62.0, xo=14.0, y1=80.0):
    """Långt utlopp längs hjulets rörelse (rörlig botten), brant tratt."""
    return B(deg, xo, y1)


# ---- C: spiral (helix) med en nöts bredd -------------------------------------------------------
HC = (0.0, 75.0); HRI, HRO = 5.0, 31.0; HRM = (HRI + HRO) / 2
HK = HRM * np.tan(np.radians(25.0))            # mm fall per radian (25 graders lutning i mitten av banan)
H_END = np.radians(270.0); H_STOP_X = 13.5
H_FLOOR_END = H_END - np.arcsin(H_STOP_X / HRM)   # golvet slutar där utloppet börjar (x = -13,5)
H_START = np.radians(-90.0)
hz = lambda f: 97.0 + (H_END - f) * HK


def C(step=12.0):
    """Spiral: en nöts bred bana (26 mm) runt en mittstolpe, 25 graders lutning, slutar över fickan."""
    P = []; f = H_START; st = np.radians(step)
    pt = lambda r, a, z: (HC[0] + r * np.cos(a), HC[1] + r * np.sin(a), z)
    while f < H_FLOOR_END - 1e-6:
        g = min(f + st, H_FLOOR_END)
        P.append(np.array([pt(r, a, hz(a) - d) for a in (f, g) for r in (HRI - 1, HRO + 1) for d in (0.0, 2.4)]))      # golv
        f = g
    f = np.radians(-90.0)
    while f < np.radians(270.0) - 1e-6:                                                                              # yttervägg
        g = f + st
        zlo = 88.0
        P.append(np.array([pt(r, a, z) for a in (f, g) for r in (HRO, HRO + 2.4) for z in (zlo, 176.0)]))
        f = g
    a = np.radians(np.arange(0, 360, 30.0)); P.append(np.array([pt(HRI, x, z) for x in a for z in (88.0, 176.0)]))   # mittstolpe
    P.append(np.array([(x, y, z) for x in (H_STOP_X, H_STOP_X + 2.4) for y in (44.0, 70.0) for z in (90.0, hz(H_START) - 2.4)]))  # stopp
    P.append(np.array([(x, y, z) for x in (-2.4, 0.0) for y in (44.0, 70.0) for z in (hz(H_START) - 2.4, 176.0)]))   # vägg bakom starten
    return P + saddle(ang(70.0), ang(44.0)) + side_cheeks(ang(70.0), ang(44.0), 13.5)


def C_spawn(n, rng, **_):
    S = []
    for k in range(n):
        a = np.radians(-70.0 + 50.0 * (k % 6) + 8.0 * (k // 6)); z = 190.0 + 26.0 * (k // 6) + (k % 6) * 6.0
        S.append((HC[0] + HRM * np.cos(a), HC[1] + HRM * np.sin(a), z))
    return S


def E():
    """Skivmagasin: en nöts tjockt (27 mm) rakt över hjulet, lutande botten 50 grader."""
    y1 = 70.0
    L = [(176.0, -13.5, 13.5, 40.0, 106.0), (140.0, -13.5, 13.5, 40.0, 106.0), (97.5, -13.5, 13.5, 43.0, y1), (zs(y1) - 0.3, -13.5, 13.5, 43.0, y1)]
    return hopper(L) + saddle(ang(y1), ang(43.0)) + side_cheeks(ang(y1), ang(43.0), 13.5)


def E_spawn(n, rng, **_):
    return [(rng.uniform(-1, 1), 52.0 + 22.0 * (k % 3), 185.0 + 24.0 * (k // 3)) for k in range(n)]


# ---- F: långt smalt utlopp + fjädrande lapp vid kanten där fickan lämnar -----------------------
def F(deg=62.0, xo=12.0, y1=80.0, gate=13.0, yF=42.0):
    """Tratt ned till ett utlopp som är en nöt brett (2*xo) och långt längs hjulet. Framkanten är öppen `gate` mm
    över hjulet och täcks av en fjädrande lapp. Sadeln framför är upplyft så att en nöt som följer med går fri."""
    zr = CZ + np.sqrt(31.0 ** 2 - (yF - CY) ** 2); zg = zr + gate
    h = (45.6 - xo) * np.tan(np.radians(deg)); zt = min(98.6 + h, 170.0)
    L = [TOP, (zt, -45.6, 45.6, 40.0, 106.0), (98.6, -xo, xo, yF, y1)]
    P = []
    for (za, a0, a1, b0, b1), (zb, c0, c1, d0, d1) in zip(L[:-1], L[1:]):
        P.append(plate([(a0, b0, za), (a0, b1, za), (c0, d1, zb), (c0, d0, zb)], (-1, 0, 0)))
        P.append(plate([(a1, b0, za), (a1, b1, za), (c1, d1, zb), (c1, d0, zb)], (1, 0, 0)))
        P.append(plate([(a0, b1, za), (a1, b1, za), (c1, d1, zb), (c0, d1, zb)], (0, 1, 0)))
        if za > zg:                                              # framväggen slutar vid luckans överkant
            t = (max(zb, zg) - za) / (zb - za); e0, e1, f0 = a0 + (c0 - a0) * t, a1 + (c1 - a1) * t, b0 + (d0 - b0) * t
            P.append(plate([(a0, b0, za), (a1, b0, za), (e1, f0, max(zb, zg)), (e0, f0, max(zb, zg))], (0, -1, 0)))
    for sx in (-1, 1):                                           # raka sidoväggar ned förbi hjulet, även framför lappen
        P.append(np.array([(sx * x, y, z) for x in (xo, xo + 2.4) for y in (16.0, y1 + 1.0) for z in (58.0, 98.6)]))
    P.append(np.array([(x, y, z) for x in (-xo, xo) for y in (y1, y1 + 2.4) for z in (zs(y1) - 0.3, 98.6)]))   # bakkant
    return P + saddle(ang(y1 + 1.0), ang(yF), r_front=31.0 + gate + 1.5)


def F_flap(deg=62.0, xo=12.0, y1=80.0, gate=13.0, yF=42.0, k=0.135, Lf=30.0):
    zr = CZ + np.sqrt(31.0 ** 2 - (yF - CY) ** 2)
    return dict(x0=-xo + 0.5, x1=xo - 0.5, y=yF - 0.8, zh=zr + 1.5 + Lf, L=Lf, k=k)


# ---- C2: spiral med fjädrande lapp vid kanten där fickan lämnar ----------------------------------
def C2(deg=32.0, ztop=152.0, gate=13.0, step=12.0, ceiling=False):
    k = HRM * np.tan(np.radians(deg)); span = (ztop - 97.0) / k; f0 = H_END - span
    hz2 = lambda f: 97.0 + (H_END - f) * k
    zr = CZ + np.sqrt(31.0 ** 2 - (44.0 - CY) ** 2); zg = zr + gate
    P = []; f = f0; st = np.radians(step)
    pt = lambda r, a, z: (HC[0] + r * np.cos(a), HC[1] + r * np.sin(a), z)
    while f < H_FLOOR_END - 1e-6:
        g = min(f + st, H_FLOOR_END)
        P.append(np.array([pt(r, a, hz2(a) - d) for a in (f, g) for r in (HRI - 1, HRO + 1) for d in (0.0, 2.4)]))
        f = g
    f = np.radians(-90.0)
    while f < np.radians(270.0) - 1e-6:
        g = f + st; mid = np.degrees((f + g) / 2) % 360
        zlo = zg if abs(mid - 270.0) < 27.0 or mid < -63 + 0 else 88.0
        if abs(((mid - 270.0 + 180) % 360) - 180) < 27.0: zlo = zg
        P.append(np.array([pt(r, a, z) for a in (f, g) for r in (HRO, HRO + 2.4) for z in (zlo, 176.0)]))
        f = g
    a = np.radians(np.arange(0, 360, 30.0)); P.append(np.array([pt(HRI, x, z) for x in a for z in (88.0, 176.0)]))
    P.append(np.array([(x, y, z) for x in (H_STOP_X, H_STOP_X + 2.4) for y in (20.0, 70.0) for z in (60.0, hz2(f0) - 2.4)]))       # stopp
    P.append(np.array([(x, y, z) for x in (-H_STOP_X - 2.4, -H_STOP_X) for y in (20.0, 44.0) for z in (60.0, zg)]))                # sida framför lappen
    xs = HC[0] + HRM * np.cos(f0)
    P.append(np.array([(HC[0] + r * np.cos(f0) + dx * np.sin(f0), HC[1] + r * np.sin(f0) - dx * np.cos(f0), z)
                       for r in (HRI, HRO) for dx in (0.0, 2.4) for z in (hz2(f0) - 2.4, 176.0)]))                               # vägg bakom starten
    return P + saddle(ang(70.0), ang(44.0), r_front=31.0 + gate + 1.5) + side_cheeks(ang(70.0), ang(44.0), 13.5)


def C2_flap(deg=32.0, ztop=152.0, gate=13.0, k=0.135, Lf=30.0, **_):
    zr = CZ + np.sqrt(31.0 ** 2 - (44.0 - CY) ** 2)
    return dict(x0=-13.0, x1=13.0, y=43.0, zh=zr + 1.5 + Lf, L=Lf, k=k)


def C2_spawn(n, rng, deg=32.0, ztop=152.0, **_):
    k = HRM * np.tan(np.radians(deg)); span = (ztop - 97.0) / k; f0 = H_END - span
    S = []
    for i in range(n):
        a = f0 + np.radians(12.0) + (i % 5) * (span - np.radians(40.0)) / 5.0; z = 190.0 + 28.0 * (i // 5) + (i % 5) * 5.0
        S.append((HC[0] + HRM * np.cos(a), HC[1] + HRM * np.sin(a), z))
    return S


# ---- C3: slutet spiralrör (en nöt i taget) och L: rakt rör ---------------------------------------
G_RI, G_RO = 7.0, 31.0; G_RM = (G_RI + G_RO) / 2; G_HALF = 12.0
G_DA = np.arcsin(G_HALF / G_RM)


def _cell(gate, x_half=G_HALF, y0=44.0, y1=68.0):
    """Sidoplattor framför luckan + upplyft sadel. Gemensamt för rör och spiral."""
    zr = CZ + np.sqrt(31.0 ** 2 - (y0 - CY) ** 2); zg = zr + gate
    P = [np.array([(sx * x, y, z) for x in (x_half, x_half + 2.4) for y in (18.0, y0 + 3.0) for z in (58.0, zg)]) for sx in (-1, 1)]
    return P, zg


def C3(deg=30.0, ztop=150.0, gate=13.0, step=10.0, head=23.0, **_):
    k = G_RM * np.tan(np.radians(deg)); span = (ztop - 97.0) / k; f0 = H_END - span; fe = H_END - G_DA
    hz2 = lambda f: 97.0 + (H_END - f) * k
    pt = lambda r, a, z: (HC[0] + r * np.cos(a), HC[1] + r * np.sin(a), z)
    P, zg = _cell(gate); st = np.radians(step)
    f = f0
    while f < fe - 1e-6:                                             # golv
        g = min(f + st, fe); P.append(np.array([pt(r, a, hz2(a) - d) for a in (f, g) for r in (G_RI - 1, G_RO + 1) for d in (0.0, 2.4)])); f = g
    f = f0 + np.radians(55.0)
    while f < H_END + G_DA - 1e-6:                                   # tak (öppet de första 55 graderna = påfyllning)
        g = min(f + st, H_END + G_DA); zc = lambda a: max(hz2(min(a, fe)), 97.0) + head
        P.append(np.array([pt(r, a, zc(a) + d) for a in (f, g) for r in (G_RI - 1, G_RO + 1) for d in (0.0, 2.4)])); f = g
    f = f0 - np.radians(5)
    while f < H_END + np.radians(45.0) - 1e-6:                       # yttervägg, med lucka framtill
        g = f + st; mid = np.degrees((f + g) / 2)
        zlo = zg if abs(mid - 270.0) < 30.0 else 86.0
        P.append(np.array([pt(r, a, z) for a in (f, g) for r in (G_RO, G_RO + 2.4) for z in (zlo, 176.0)])); f = g
    a = np.radians(np.arange(0, 360, 30.0)); P.append(np.array([pt(G_RI, x, z) for x in a for z in (86.0, 176.0)]))
    P.append(np.array([(x, y, z) for x in (G_HALF, G_HALF + 2.4) for y in (44.0, 69.0) for z in (86.0, 97.0 + head + 2.4)]))      # stopp efter cellen
    P.append(np.array([(HC[0] + r * np.cos(f0) + dx * np.sin(f0), HC[1] + r * np.sin(f0) - dx * np.cos(f0), z)
                       for r in (G_RI, G_RO) for dx in (0.0, 2.4) for z in (hz2(f0) - 2.4, 176.0)]))                            # vägg bakom starten
    return P + saddle(ang(69.0), ang(44.0), r_front=31.0 + gate + 1.5) + side_cheeks(ang(69.0), ang(44.0), G_HALF)


def C3_flap(gate=13.0, k=0.135, Lf=30.0, **_):
    zr = CZ + np.sqrt(31.0 ** 2 - (44.0 - CY) ** 2)
    return dict(x0=-G_HALF + 0.5, x1=G_HALF - 0.5, y=43.2, zh=zr + 1.5 + Lf, L=Lf, k=k)


def C3_spawn(n, rng, deg=30.0, ztop=150.0, **_):
    k = G_RM * np.tan(np.radians(deg)); f0 = H_END - (ztop - 97.0) / k; a = f0 + np.radians(28.0)
    return [(HC[0] + G_RM * np.cos(a) + rng.uniform(-1, 1), HC[1] + G_RM * np.sin(a) + rng.uniform(-1, 1), 185.0 + 60.0 * i) for i in range(n)]


def L(gate=13.0, w=G_HALF, ztube=176.0, **_):
    """Rakt lodrätt rör, 24 mm, rakt över fickan."""
    P, zg = _cell(gate, w)
    c = w * (1 - np.tan(np.radians(22.5)))
    oc = [(w, -w + c), (w, w - c), (w - c, w), (-w + c, w), (-w, w - c), (-w, -w + c), (-w + c, -w), (w - c, -w)]   # åttkant
    for i in range(8):
        (xa, ya), (xb, yb) = oc[i], oc[(i + 1) % 8]; n = np.array([(xa + xb) / 2, (ya + yb) / 2, 0.0]); n /= np.linalg.norm(n)
        front = (ya + yb) / 2 < -w + c / 2 + 0.1 and abs(xa + xb) < 1.0
        zlo = zg if (ya < -w + c + 0.1 and yb < -w + c + 0.1) else 84.0
        P.append(plate([(xa, 56.0 + ya, ztube), (xb, 56.0 + yb, ztube), (xb, 56.0 + yb, zlo), (xa, 56.0 + ya, zlo)], n))
    return P + saddle(ang(68.0), ang(44.0), r_front=31.0 + gate + 1.5) + side_cheeks(ang(68.0), ang(44.0), w)


def L_flap(gate=13.0, k=0.135, Lf=30.0, w=G_HALF, **_):
    zr = CZ + np.sqrt(31.0 ** 2 - (44.0 - CY) ** 2)
    return dict(x0=-w + 3.0, x1=w - 3.0, y=43.2, zh=zr + 1.5 + Lf, L=Lf, k=k)


def L_spawn(n, rng, **_):
    return [(rng.uniform(-1, 1), 56.0 + rng.uniform(-1, 1), 190.0 + 60.0 * i) for i in range(n)]


# ---- S: skivmagasin, en nöt tjockt, lodräta väggar ända ned på hjulet, lutande golv bakom ---------
def S(w=12.25, yF=42.0, yR=80.0, floor=45.0, gate=13.0, ytop=106.0, **_):
    zr = CZ + np.sqrt(31.0 ** 2 - (yF - CY) ** 2); zg = zr + gate
    zR = zs(yR) + 0.5; zB = zR + (ytop - yR) * np.tan(np.radians(floor))
    P = []
    for sx in (-1, 1):                                                              # lodräta sidor
        P.append(np.array([(sx * x, y, z) for x in (w, w + 2.4) for y in (16.0, ytop + 2.4) for z in (58.0, 176.0)]))
    P.append(np.array([(x, y, z) for x in (-w, w) for y in (yF - 2.4, yF) for z in (zg, 176.0)]))            # framvägg över luckan
    P.append(np.array([(x, y, z) for x in (-w, w) for y in (ytop, ytop + 2.4) for z in (zB - 3.0, 176.0)]))  # bakvägg
    P.append(np.array([(x, yR, zR), (x2 := x, yR, zR - 2.4), (x, ytop, zB), (x, ytop, zB - 2.4)] if False else
                      [(sx, y, z) for sx in (-w, w) for (y, z) in ((yR, zR), (yR, zR - 2.4), (ytop, zB), (ytop, zB - 2.4))]))  # lutande golv
    return P + saddle(ang(yR), ang(yF), r_front=31.0 + gate + 1.5)


def S_flap(w=12.25, yF=42.0, gate=13.0, k=0.06, Lf=30.0, **_):
    zr = CZ + np.sqrt(31.0 ** 2 - (yF - CY) ** 2)
    return dict(x0=-w + 0.5, x1=w - 0.5, y=yF - 3.2, zh=zr + 1.5 + Lf, L=Lf, k=k)


def S_spawn(n, rng, yF=42.0, ytop=106.0, **_):
    ys = np.arange(yF + 12.0, ytop - 11.0, 21.0)
    return [(rng.uniform(-1, 1), ys[i % len(ys)] + rng.uniform(-1, 1), 190.0 + 26.0 * (i // len(ys)) + 5.0 * (i % len(ys))) for i in range(n)]


# ---- T2: två raka rör efter varandra längs hjulet (skivmagasin med mellanvägg) ---------------------
def T2(w=12.25, gate=13.0, ysplit=69.8, yR=87.0, ytop=94.4, **_):
    P = S(w=w, yR=yR, ytop=ytop, gate=gate)
    zr = CZ + np.sqrt(31.0 ** 2 - (ysplit - CY) ** 2)
    P.append(np.array([(x, y, z) for x in (-w, w) for y in (ysplit - 1.2, ysplit + 1.2) for z in (zr + gate, 176.0)]))   # mellanvägg med öppning nedtill
    return P


def T2_flap(**kw): return S_flap(**kw)


def T2_spawn(n, rng, **_):
    return [(rng.uniform(-1, 1), (56.0, 82.2)[i % 2] + rng.uniform(-1, 1), 190.0 + 60.0 * (i // 2) + 25.0 * (i % 2)) for i in range(n)]


# ---- LT: rör nederst, tratt ovanpå -----------------------------------------------------------------
def LT(ztube=135.0, deg=62.0, **_):
    h = (45.6 - G_HALF) * np.tan(np.radians(deg)); zt = min(ztube + h, 172.0)
    return L(ztube=ztube) + hopper([TOP, (zt, -45.6, 45.6, 40.0, 106.0), (ztube, -G_HALF, G_HALF, 44.0, 68.0)])


def LT_flap(**kw): return L_flap(**kw)
