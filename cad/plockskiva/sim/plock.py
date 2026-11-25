"""
Plockskivan: gemensam geometri för simulering och CAD. Husets ram, mm. Framsidan är -y.
Skivan lutar 45 grader med överkanten mot -x. Lokala axlar: u = +y, v = uppför skivan, w = skivans normal.
"""
import numpy as np
c = s = np.sqrt(0.5)
EU = np.array([0.0, 1.0, 0.0]); EV = np.array([-c, 0.0, s]); EW = np.array([s, 0.0, c])
RD, TD, GAP = 46.6, 16.0, 0.6        # skivans radie, tjocklek, spalt mot plattan
RP, RH = 32.0, 13.0                  # fickans mittradie och radie
RC, WALL = 47.4, 2.4                 # kragens innerradie, väggtjocklek
WS, WT = 42.6, 45.0                  # skärmens under- och ovansida (26 mm över skivan)
VS = -8.0                            # skärmens nederkant
QX = np.radians(55.0)                # utfallets läge (0 = högst upp), fickan plockar vid 180
RX = 14.0                            # utfallshålets radie
SLAB_R, SLAB_T = 50.0, 8.4           # stativets lutande platta
YF, YB = 29.9, 107.1                 # förrådets innermått i y
CH_W, CH_W0, CH_H = 13.0, 17.0, 30.0  # rännans halva innerbredd nedtill och upptill, kanthöjd

def configure(Cx=-1.5, Cy=64.0, Cz=57.0, dl=16.0, zt=144.0, xl=-30.0):
    """dl = hur långt kragen fortsätter luta utåt ovanför skärmens plan innan väggen blir lodrät (ger bredare öppning)."""
    global C, T, DL, ZT, XL, UF, UB, PLANE, XARC0, EX, CH_A, CH_B, WTOP
    C = np.array([Cx, Cy, Cz]); DL = dl; ZT = zt; XL = xl; WTOP = WT + DL
    T = np.eye(4); T[:3, 0] = EU; T[:3, 1] = EV; T[:3, 2] = EW; T[:3, 3] = C
    UF, UB = YF - C[1], YB - C[1]
    PLANE = C[0] + C[2] + WT / c
    XARC0 = C[0] + c * np.sqrt(RC ** 2 - UF ** 2) + s * WTOP
    EX = W([-RP * np.sin(QX), RP * np.cos(QX), -SLAB_T])[0]
    global CH_B, CH_T, CH_K, CH_POLY
    CH_B = np.array([0.0, 3.4, 3.5]); CH_K = np.tan(np.radians(38.0))
    t_ = CH_B[:2] - EX[:2]; CH_T = t_ / np.linalg.norm(t_)                                 # rännans riktning i planet
    yb = EX[1] + 13.5; NECK = 12.0                                                         # rännans bakkant; halsen är rak fram till y = 12 (sockeln)
    global CH_NECK, CH_FUN
    CH_NECK = np.array([(CH_B[0] - CH_W, CH_B[1]), (CH_B[0] + CH_W, CH_B[1]), (CH_B[0] + CH_W, NECK), (CH_B[0] - CH_W, NECK)])
    CH_FUN = np.array([(CH_B[0] + CH_W, NECK), (EX[0] + CH_W0, yb), (EX[0] - CH_W0, yb), (EX[0] - CH_W0, EX[1] + 0.5), (CH_B[0] - CH_W, NECK)])   # moturs
    CH_POLY = np.array([CH_NECK[0], CH_NECK[1], CH_FUN[0], CH_FUN[1], CH_FUN[2], CH_FUN[3], CH_FUN[4]])
def chute_z(p): return CH_B[2] + CH_K * float(np.dot(CH_B[:2] - np.asarray(p)[:2], CH_T))  # golvets höjd
def W(p): p = np.atleast_2d(np.asarray(p, float)); return p @ T[:3, :3].T + C
zplane = lambda x: PLANE - x
configure()

def circle(r, n=72, a0=0.0): a = np.radians(np.arange(0, 360, 360 / n) + a0); return np.c_[r * np.cos(a), r * np.sin(a)]
def prism(uv, w0, w1): uv = np.asarray(uv, float); return np.vstack([np.c_[uv, np.full(len(uv), w0)], np.c_[uv, np.full(len(uv), w1)]])
def rot(uv, q): uv = np.asarray(uv, float); return uv @ np.array([[np.cos(q), np.sin(q)], [-np.sin(q), np.cos(q)]])   # vrid moturs q
def holed(R, hc, hh, w0, w1, octa=True, q=0.0):
    """Rund platta med hål (halv sida hh) på avståndet hc från mitten, hålet vridet q från +v. Konvexa bitar, lokala koordinater."""
    Cc = circle(R); yl = lambda u: np.sqrt(max(R * R - u * u, 0)); P = []
    sel = lambda f, extra: np.vstack([Cc[f(Cc)], extra])
    P.append(sel(lambda p: p[:, 0] >= hh, [(hh, yl(hh)), (hh, -yl(hh))]))
    P.append(sel(lambda p: p[:, 0] <= -hh, [(-hh, yl(hh)), (-hh, -yl(hh))]))
    P.append(sel(lambda p: (np.abs(p[:, 0]) <= hh) & (p[:, 1] < hc - hh), [(-hh, hc - hh), (hh, hc - hh), (-hh, -yl(hh)), (hh, -yl(hh))]))
    if yl(hh) > hc + hh + 0.5:
        P.append(np.array([(-hh, hc + hh), (hh, hc + hh), (-hh, yl(hh)), (hh, yl(hh))] + [tuple(p) for p in Cc[(np.abs(Cc[:, 0]) <= hh) & (Cc[:, 1] > hc + hh)]]))
    if octa:
        k = hh * (1 - np.tan(np.radians(22.5)))
        for su in (-1, 1):
            for sv in (-1, 1): P.append(np.array([(su * hh, hc + sv * hh), (su * (hh - k), hc + sv * hh), (su * hh, hc + sv * (hh - k))]))
    return [prism(rot(p, q), w0, w1) for p in P]

def disc_pieces():                       # skivan i sitt eget läge q = 0 (fickan högst upp), lokala koordinater
    return holed(RD, RP, RH, GAP, GAP + TD)

def static_pieces(chute=True):
    """Allt fast som nötterna kan röra vid, som konvexa punktmoln i husets ram."""
    L = []                                                     # lokala bitar
    L += holed(SLAB_R, RP, RX, -3.0, 0.0, octa=True, q=QX)     # plattans ovansida med utfallshål
    a = 0.0
    while a < 360:                                             # krage upp till skärmen
        L.append(np.array([((RC + d) * np.cos(np.radians(x)), (RC + d) * np.sin(np.radians(x)), w) for x in (a, a + 10) for d in (0, WALL) for w in (0.0, WTOP if (np.sin(np.radians(a + 5)) * RC < VS) else WT)])); a += 10
    Cc = circle(RC + WALL, 144); yv = np.sqrt((RC + WALL) ** 2 - VS ** 2)
    L.append(prism(np.vstack([Cc[Cc[:, 1] >= VS], [(-yv, VS), (yv, VS)]]), WS, WT))                       # skärm över övre halvan
    for sgn, ue in ((-1, UF), (1, UB)):                                                                  # lock över kanterna av nedre halvan
        sel = Cc[(sgn * Cc[:, 0] >= sgn * ue) & (Cc[:, 1] <= VS)]; ye = np.sqrt((RC + WALL) ** 2 - ue ** 2)
        L.append(prism(np.vstack([sel, [(ue, VS), (ue, -ye), (sgn * yv, VS)]]), WS, WT))
    vend = (C[0] + s * WS - (XL - WALL)) / c
    L.append(prism([(UF - WALL, VS), (UB + WALL, VS), (UB + WALL, vend), (UF - WALL, vend)], WS, WT))     # förrådets lutande golv
    P = [W(p) for p in L]
    zb = lambda x: zplane(x) - 0.5
    for y0, y1 in ((YF - WALL, YF), (YB, YB + WALL)):                                                    # fram- och bakvägg
        P.append(np.array([(x, y, z) for y in (y0, y1) for x, z in ((XL - WALL, zb(XL - WALL)), (XARC0, zb(XARC0)), (XARC0, ZT), (XL - WALL, ZT))]))
    P.append(np.array([(x, y, z) for x in (XL - WALL, XL) for y in (YF - WALL, YB + WALL) for z in (zb(XL) - 3, ZT)]))   # vägg mot -x
    us = np.linspace(UF, UB, 13)
    arc3 = np.array([W([u, -np.sqrt(RC ** 2 - u * u), WTOP])[0] for u in us]); arc = arc3[:, :2]            # bågvägg mot +x, börjar där kragen slutar
    for (xa, ya, za), (xb, yb, zb_) in zip(arc3[:-1], arc3[1:]):
        n = np.array([yb - ya, -(xb - xa)]); n /= np.linalg.norm(n)
        if n[0] < 0: n = -n
        pts = []
        for (x, y, z0) in ((xa, ya, za), (xb, yb, zb_)):
            for d in (0.0, WALL):
                for z in (z0 - 3.0, ZT): pts.append((x + n[0] * d, y + n[1] * d, z))
        P.append(np.array(pts))
    if chute:
        import trimesh
        Q = [np.array([(x, y, chute_z((x, y)) + dz) for x, y in poly for dz in (-WALL, 0.0)]) for poly in (CH_NECK, CH_FUN)]             # golv i två konvexa delar
        edges = [(CH_NECK[1], CH_NECK[2]), (CH_NECK[3], CH_NECK[0])] + [(CH_FUN[i], CH_FUN[i + 1]) for i in range(4)]                  # väggar (mynningen och skarven är öppna)
        for p0, p1 in edges:
            e = p1 - p0; nrm = np.array([e[1], -e[0]]) / np.linalg.norm(e)                                                        # utåt (konturen går moturs)
            Q.append(np.array([(p[0] + nrm[0] * d_, p[1] + nrm[1] * d_, chute_z(p) + dz) for p in (p0, p1) for d_ in (0.0, WALL) for dz in (-WALL, 45.0)]))
        o_ = W([0, 0, -SLAB_T])[0]
        for q in Q:                                                   # kapa allt som sticker upp genom plattans undersida
            h = trimesh.convex.convex_hull(q).slice_plane(o_, -EW, cap=True)
            if len(h.vertices) >= 4: P.append(np.asarray(h.vertices))
    return P
