# Projekt Lennart - fem forslag pa overgangen fran titeln (0.6, PROJEKT LENNART) till balkongen (1.1). Bara forslag: filmen andras inte.
# Titeln ar samma som i titel.py (80 x 45 LED-pixlar a 16 px, bokstaverna och ekollonet tands mellan 0,12 och 0,72 s). Klippet till 1.1 ligger pa 2,8 s.
#   1 vandbrickor   rutnatet ar brickor som vands en och en i en vag fran ekollonet, baksidan ar balkongen
#   2 o             kameran aker in genom O:et i PROJEKT, forbi skarmens RGB-subpixlar, och balkongen syns genom halet
#   3 datamosh      titeln blir referensbild at balkongens rorelser (som nar en videofil tappar en nyckelruta) och smetas ut, sedan rensas den block for block
#   4 nedslag       ekollonet lossnar, faller och slar i bildens underkant pa slaget; en tryckvag fran nedslaget oppnar balkongen och ekollonet sprack i sina pixlar
#   5 dorren        en lysande skarva skar titeln mellan raderna, halvorna glider isar som en dorr och sommarljuset valler in
# Bakgrunden ar balkongvideon fore 1.1 (overgangar/bakom/00.jpg ..., 0,04 s per ruta fran kallklippets borjan; 1.1 borjar 0,48 s in).
# Kor:  <Blenders python> titel_overgangar.py <variant 1-5> <ut-mapp>     (skriver 1280 x 720 jpg-rutor; skriver ocksa antal rutor efter klippet i <ut-mapp>/efter.txt)
import sys, os, subprocess, math, numpy as np
VAR = int(sys.argv[1]); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); BAKOM = os.path.join(HERE, '..', 'overgangar', 'bakom'); B_T = 0.48
FPS, DUR, C, GW, GH, W, H = 25, 2.8, 16, 80, 45, 1280, 720
# ---------- titeln (samma som titel.py) ----------
F = {'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'], 'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
     'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'], 'J': ['00111', '00010', '00010', '00010', '00010', '10010', '01100'],
     'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'], 'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'],
     'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'], 'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
     'N': ['10001', '11001', '10101', '10101', '10011', '10001', '10001'], 'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001']}
NOT = ['.....##......', '......#......', '......#......', '..#########..', '.#.........#.', '#...........#', '#...........#', '#...........#', '.#.........#.', '..#########..', '..#.#####.#..', '..#.#####.#..', '..#.#####.#..', '...#.###.#...', '...#..#..#...', '....#...#....', '.....###.....']
NW, GAP_N, TW = len(NOT[0]), 3, 7 * 6 - 1; X_NOT = (GW - (NW + GAP_N + TW)) // 2; X_TXT = X_NOT + NW + GAP_N
on = np.zeros((GH, GW), bool); not_ = np.zeros((GH, GW), bool)
for r, row in enumerate(NOT):
    for c, b in enumerate(row):
        if b == '#': not_[14 + r, X_NOT + c] = True
for line, y0 in (('PROJEKT', 14), ('LENNART', 24)):
    for i, ch in enumerate(line):
        for r, row in enumerate(F[ch]):
            for c, b in enumerate(row):
                if b == '1': on[y0 + r, X_TXT + i * 6 + c] = True
rng = np.random.default_rng(7); ys, xs = np.where(on); t_on = np.full(on.shape, 1e9); t_on[ys, xs] = 0.22 + rng.random(len(ys)) * 0.5
ys, xs = np.where(not_); t_on[ys, xs] = 0.12 + rng.random(len(ys)) * 0.45
BG = np.array([6, 18, 11]) / 255; LIT = np.array([96, 214, 150]) / 255; FLASH = np.array([235, 255, 240]) / 255; BACK = np.array([0.0035, 0.0065, 0.0055]) * 1.4
u_ = (np.arange(C) + 0.5) / C; e_ = np.clip((0.5 - np.abs(u_ - 0.5)) / 0.14, 0, 1); cell = np.outer(e_, e_)[..., None] * 0.75 + 0.25
sub = np.stack([0.65 + 0.35 * 1.6 * (0.5 + 0.5 * np.cos(2 * np.pi * (u_ - ph))) for ph in (1 / 6, 0.5, 5 / 6)], -1)[None, :, :] * np.ones((C, 1, 1))
TILE = cell * sub; TILES = np.tile(TILE, (GH, GW, 1))
def farger(t):   # cellernas farg vid tiden t (45 x 80 x 3)
    age = t - t_on; return np.where((age >= 0)[..., None], np.where((age < 0.1)[..., None], FLASH, LIT), BG + BACK)
def titel(t, col=None):   # titeln utan sken
    col = farger(t) if col is None else col; return np.clip(np.kron(col, np.ones((C, C, 1))) * TILES * 1.25, 0, 1)
def glod(x):   # mjukt sken (som gblur sigma 9): nedskalat 4 ggr, gaussisk osk. sigma 2,25, uppskalat
    h_, w_ = x.shape[0] // 4, x.shape[1] // 4; d_ = x.reshape(h_, 4, w_, 4, 3).mean((1, 3))
    k_ = np.exp(-0.5 * (np.arange(-7, 8) / 2.25) ** 2); k_ /= k_.sum()
    d_ = np.apply_along_axis(lambda v: np.convolve(v, k_, 'same'), 0, d_); d_ = np.apply_along_axis(lambda v: np.convolve(v, k_, 'same'), 1, d_)
    return np.kron(d_, np.ones((4, 4, 1)))
def sken(x, g=None, k=0.55): return 1 - (1 - x) * (1 - k * glod(x if g is None else g))
def sm(t, a, b): x = np.clip((t - a) / (b - a), 0, 1); return x * x * (3 - 2 * x)
_vc = {}
def vid(t):   # balkongen vid filmtiden t (stilla fore kallklippets borjan), samma ton som 1.1
    n = int(np.clip(round((B_T + t - DUR) * FPS), 0, 49))
    if n not in _vc:
        r = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(BAKOM, '%02d.jpg' % n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        _vc[n] = np.clip(np.frombuffer(r, np.uint8).reshape(H, W, 3) / 255 * np.array([1.0, 0.973, 0.979]) + 1.8 / 255, 0, 1)
    return _vc[n]
def skala(img, s, cx=W / 2, cy=H / 2):   # skalar bilden s ganger kring (cx, cy), bilinjart
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); return sampla(img, cx + (xx - W / 2) / s, cy + (yy - H / 2) / s)
def sampla(img, x, y):   # bilinjar sampling, utanfor bilden = kanten
    x = np.clip(x, 0, img.shape[1] - 1.001); y = np.clip(y, 0, img.shape[0] - 1.001); x0 = x.astype(int); y0 = y.astype(int); fx = (x - x0)[..., None]; fy = (y - y0)[..., None]
    return (img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx) * (1 - fy) + (img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx) * fy
def skriv(img, f): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-', '-q:v', '2', os.path.join(OUT, '%04d.jpg' % f)], input=(np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes(), check=True)
NOT_C = ((X_NOT + NW / 2) * C, (14 + len(NOT) / 2) * C)   # ekollonets mitt i bildpunkter (x, y)
EFTER = {1: 0.0, 2: 0.0, 3: 0.92, 4: 0.6, 5: 0.24}[VAR]   # hur lange overgangen fortsatter in i 1.1 (s)
N = int(round((DUR + EFTER) * FPS)); open(os.path.join(OUT, 'efter.txt'), 'w').write(str(int(round(EFTER * FPS))))
STATISK = sken(titel(1.0))

# ---------- 1. vandbrickor ----------
if VAR == 1:
    TS = 80; NX, NY = W // TS, H // TS; rr = np.random.default_rng(3)
    cy_, cx_ = np.mgrid[0:NY, 0:NX]; d = np.hypot((cx_ + 0.5) * TS - NOT_C[0], (cy_ + 0.5) * TS - NOT_C[1]); d /= d.max()
    T0 = 1.80 + 0.52 * d ** 0.85 + rr.random(d.shape) * 0.05; LANG = 0.42
    for f in range(N):
        t = f / FPS; fram = STATISK if t > 1.0 else sken(titel(t))
        if t < T0.min(): skriv(fram, f); continue
        V = vid(t); ut = np.zeros((H, W, 3)) + np.array([0.004, 0.008, 0.007])
        for i in range(NY):
            for j in range(NX):
                u = (t - T0[i, j]) / LANG; y0, x0 = i * TS, j * TS
                if u <= 0: ut[y0:y0 + TS, x0:x0 + TS] = fram[y0:y0 + TS, x0:x0 + TS]; continue
                if u >= 1: ut[y0:y0 + TS, x0:x0 + TS] = V[y0:y0 + TS, x0:x0 + TS] * (1 + 0.35 * math.exp(-(u - 1) * 9)); continue   # ligger ner: en kort glans
                th = math.pi * float(sm(u, 0, 1)) ** 1.3
                c = math.cos(th); s_ = math.sin(th); w = abs(c) * TS
                if w < 1: continue
                src = (fram if c > 0 else V)[y0:y0 + TS, x0:x0 + TS]
                ljus = 0.22 + 0.78 * abs(c) + 0.45 * math.exp(-((th - 0.7) / 0.22) ** 2) + 0.3 * math.exp(-((th - 2.6) / 0.2) ** 2)
                nw = int(round(w)); xa = x0 + (TS - nw) // 2
                for k in range(nw):   # perspektiv: kanten som kommer mot kameran blir hogre
                    xr = (k + 0.5) / nw - 0.5; sx = int((k + 0.5) / nw * TS); sx = min(sx, TS - 1)
                    hk = TS * (1 + 0.6 * s_ * xr * (1 if c > 0 else -1)); nh = int(round(hk)); ya = y0 + (TS - nh) // 2
                    iy = np.clip(((np.arange(nh) + 0.5) / nh * TS).astype(int), 0, TS - 1); yb0, yb1 = max(ya, 0), min(ya + nh, H)
                    ut[yb0:yb1, xa + k] = src[iy[yb0 - ya:yb1 - ya], sx] * ljus * (1 - 0.35 * s_ * (0.5 - xr * (1 if c > 0 else -1)))   # kanten som viker bort ar morkare
        skriv(ut, f)

# ---------- 2. genom O:et ----------
if VAR == 2:
    OX = X_TXT + 2 * 6; HAL = np.zeros((GH, GW), bool); HAL[15:20, OX + 1:OX + 4] = True   # halet i O:et (3 x 5 pixlar)
    HC = ((OX + 2.5) * C, (14 + 3.5) * C); S_END = 30.0; T_A, T_P = 1.62, 1.92
    COL = farger(2.0); yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    PH = np.array([1 / 6, 0.5, 5 / 6])
    def zoom(t):
        if t < T_P: return 1 - 0.04 * float(sm(t, T_A, T_P)), 0.0
        u = min(1.0, (t - T_P) / (DUR - 1 / FPS - T_P)); return 0.96 * (S_END / 0.96) ** (u ** 2.4), u   # sista rutan fore klippet: halet tacker hela bilden
    def rendera(s, u):   # titeln skalad s ganger kring en punkt som glider mot halet, ritad direkt ur rutnatet (skarp pa alla avstand)
        k = float(sm(u, 0.0, 0.5)); cx = W / 2 + (HC[0] - W / 2) * k; cy = H / 2 + (HC[1] - H / 2) * k
        X = cx + (xx - W / 2) / s; Y = cy + (yy - H / 2) / s; gx = np.floor(X / C).astype(int); gy = np.floor(Y / C).astype(int)
        inne = (gx >= 0) & (gx < GW) & (gy >= 0) & (gy < GH); gxc = np.clip(gx, 0, GW - 1); gyc = np.clip(gy, 0, GH - 1)
        fx = X / C - gx; fy = Y / C - gy; ex = np.clip((0.5 - np.abs(fx - 0.5)) / 0.14, 0, 1); ey = np.clip((0.5 - np.abs(fy - 0.5)) / 0.14, 0, 1)
        pat = (ex * ey * 0.75 + 0.25)[..., None] * (0.65 + 0.35 * 1.6 * (0.5 + 0.5 * np.cos(2 * np.pi * (fx[..., None] - PH))))
        col = np.where(inne[..., None], COL[gyc, gxc], BG + BACK); img = np.clip(col * pat * 1.25, 0, 1)
        hal = (inne & HAL[gyc, gxc]).astype(np.float32); return img, hal
    for f in range(N):
        t = f / FPS
        if t < T_A: skriv(STATISK if t > 1.0 else sken(titel(t)), f); continue
        img = np.zeros((H, W, 3)); hal = np.zeros((H, W)); n_ = 4 if t >= T_P else 1
        for q in range(n_):   # rorelseoskarpa: fyra lagen over halva rutan
            s, u = zoom(t + (q / n_ - 0.25) * 0.5 / FPS if n_ > 1 else t); a, b = rendera(s, u); img += a / n_; hal += b / n_
        s, u = zoom(t); V = skala(vid(t), 1.12 - 0.12 * u ** 1.5) if u > 0 else vid(t)
        tona = float(sm(t, T_A + 0.1, T_P + 0.15)); V = V * tona + (BG + BACK) * (1 - tona)   # balkongen tonar fram i halet nar kameran borjar aka
        lager = img * (1 - hal[..., None]); ut = V * hal[..., None] + lager; ut = 1 - (1 - ut) * (1 - 0.55 * glod(lager)); skriv(ut, f)

# ---------- 3. datamosh ----------
if VAR == 3:
    B = 16; BY, BX = H // B, W // B; AMP = 3.0; rr = np.random.default_rng(5)
    def gra(x): return (x[::2, ::2] @ np.array([0.3, 0.59, 0.11])).astype(np.float32)
    def rorelse(a, b):   # blockvis rorelse fran a till b (halv upplosning, 8 x 8 block, +-8 steg): for varje block i b, var det kom ifran i a
        A, Bb = gra(a), gra(b); best = np.full((BY, BX), 1e18); mv = np.zeros((BY, BX, 2), int); P = 8
        Ap = np.pad(A, P, mode='edge')
        for dy in range(-P, P + 1):
            for dx in range(-P, P + 1):
                sad = np.abs(Bb - Ap[P + dy:P + dy + H // 2, P + dx:P + dx + W // 2]).reshape(BY, 8, BX, 8).sum((1, 3)) + 2 * (abs(dy) + abs(dx))
                m = sad < best; best[m] = sad[m]; mv[m] = (dy, dx)
        return mv * 2
    def flytta(img, mv, k=1.0):   # varje block hamtas fran sin plats i forra bilden (+ rorelsen)
        P = int(np.abs(mv * k).max()) + 2; ip = np.pad(img, ((P, P), (P, P), (0, 0)), mode='edge'); ut = np.empty_like(img)
        for by in range(BY):
            for bx in range(BX):
                dy, dx = (mv[by, bx] * k).round().astype(int); y0, x0 = by * B + dy + P, bx * B + dx + P; ut[by * B:(by + 1) * B, bx * B:(bx + 1) * B] = ip[y0:y0 + B, x0:x0 + B]
        return ut
    M = None; T_KLAR = DUR + EFTER - 0.12
    for f in range(N):
        t = f / FPS
        if t < DUR - 0.24: skriv(STATISK if t > 1.0 else sken(titel(t)), f); continue
        if t < DUR:   # foraning: nagra block hackar till i sidled, som en fil som borjar ga sonder
            ut = STATISK.copy(); k_ = 1 + int((t - (DUR - 0.24)) * FPS) * 3
            for _ in range(k_):
                by, bx = rr.integers(0, BY), rr.integers(0, BX - 4); w = rr.integers(2, 9); dx = rr.integers(-3, 4) * B
                ut[by * B:(by + 1) * B, bx * B:(bx + w) * B] = np.roll(STATISK, dx, 1)[by * B:(by + 1) * B, bx * B:(bx + w) * B]
            skriv(ut, f); continue
        V1, V0 = vid(t), vid(t - 1 / FPS); mv = rorelse(V0, V1)
        if M is None: M = STATISK.copy()
        res = V1 - flytta(V0, mv)   # det nya i bilden som rorelsen inte forklarar
        a_ = t - DUR; kz = 0.02 + 0.05 * float(sm(a_, 0, 0.5))   # forstarkt: blocken blommar ut fran mitten (som nar samma rorelse upprepas), plus balkongens egen rorelse
        gy_, gx_ = np.mgrid[0:BY, 0:BX]; syn = -np.stack([(gy_ + 0.5) * B - H * 0.55, (gx_ + 0.5) * B - W * 0.5], -1) * kz + rr.normal(0, 1.5, (BY, BX, 2))
        M = np.clip(flytta(M, mv * AMP + syn) + 0.85 * res, 0, 1)
        u = float(sm(t, DUR + 0.24, T_KLAR)); E = np.abs(res).mean(2).reshape(BY, B, BX, B).mean((1, 3))   # rensning: block for block, de med mest nytt forst
        rang = (E.argsort(None).argsort().reshape(BY, BX) / (BY * BX)); ny = (1 - rang) * 0.5 + rr.random((BY, BX)) * 0.5 < u
        mask = np.kron(ny, np.ones((B, B)))[..., None]; M = M * (1 - mask) + V1 * mask; skriv(M, f)

# ---------- 4. nedslag ----------
if VAR == 4:
    T_LOS, T_SLAG = 2.30, DUR; rr = np.random.default_rng(9); yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nys, nxs = np.where(not_); botten = (nys.max() + 1) * C; FALL = H - botten; G = 2 * FALL / (T_SLAG - T_LOS) ** 2
    def ekollon_y(t):   # forskjutning nerat: lossnar (vickar), faller med tyngd och slar i underkanten pa slaget
        if t < T_LOS: return -4 * float(sm(t, 2.05, T_LOS)) ** 2, 2.0 * math.sin(t * 60) * float(sm(t, 2.0, 2.2)) * (1 - float(sm(t, 2.25, T_LOS)))
        return 0.5 * G * (t - T_LOS) ** 2 - 4 * max(0.0, 1 - (t - T_LOS) / 0.08), 0.0
    SPR = [(y, x, rr.uniform(-1150, -450), rr.uniform(-420, 420), rr.uniform(0.35, 0.7)) for y, x in zip(nys, nxs)]   # skarvorna: fart upp, i sidled, livslangd
    IX, IY = NOT_C[0], H - 2.0
    for f in range(N):
        t = f / FPS
        if t < 2.0: skriv(STATISK if t > 1.0 else sken(titel(t)), f); continue
        col = farger(2.0).copy(); col[not_] = BG + BACK; bas = titel(0, col)   # rutnatet utan ekollonet
        lager = bas.copy()
        if t < T_SLAG:   # ekollonet som en egen bit som faller
            dy, dx = ekollon_y(t); ek = np.zeros_like(bas); m = np.kron(not_, np.ones((C, C)))[..., None]; e_img = titel(2.0) * m
            ek = np.roll(np.roll(e_img, int(round(dy)), 0), int(round(dx)), 1); mm = np.roll(np.roll(m, int(round(dy)), 0), int(round(dx)), 1)
            if dy > 0: ek[:int(dy)] = 0; mm[:int(dy)] = 0
            lager = lager * (1 - mm) + ek
            skriv(sken(lager), f); continue
        a = t - T_SLAG; u = min(1.0, a / 0.5); r = 1750 * (1 - (1 - u) ** 2.4); bw = 70 + 40 * u
        sk = 11 * math.exp(-a * 9) * np.array([math.sin(a * 83), math.cos(a * 71)])   # skakning
        X, Y = xx - sk[0], yy - sk[1]; dxr, dyr = X - IX, Y - IY; dd = np.hypot(dxr, dyr) + 1e-3; ux, uy = dxr / dd, dyr / dd
        prof = np.exp(-((dd - r) / bw) ** 2) * (1 - u) ** 0.7; ut = np.zeros((H, W, 3))
        V = vid(t); inne = (dd < r).astype(np.float32)[..., None]
        for ch, k in enumerate((1.0, 1.25, 1.5)):   # brytning i vagfronten, kanalerna lite olika (fargfransar)
            disp = 46 * prof * k; sx, sy = X - ux * disp, Y - uy * disp
            ut[..., ch] = (sampla(V[..., ch:ch + 1], sx, sy)[..., 0] * inne[..., 0] + sampla(lager[..., ch:ch + 1], sx, sy)[..., 0] * (1 - inne[..., 0]))
        kant = np.exp(-((dd - r) / 7) ** 2) * (1 - u) ** 1.2; ut = ut + kant[..., None] * np.array([0.75, 1.0, 0.85]) * 0.9
        ut = 1 - (1 - ut) * (1 - 0.55 * glod(lager * (1 - inne)))
        for (gy, gx, vy, vx, liv) in SPR:   # ekollonets pixlar sprutar upp och faller
            k = a / liv
            if k >= 1: continue
            n_ = max(2, int(C * (1 - 0.5 * k))); py = int(IY - (len(NOT) * C) + (gy - 14) * C + vy * a + 0.5 * 2600 * a * a); px = int(gx * C + vx * a)
            ya, yb, xa, xb = max(py, 0), min(py + n_, H), max(px, 0), min(px + n_, W)
            if ya < yb and xa < xb: ut[ya:yb, xa:xb] = ut[ya:yb, xa:xb] * k + np.array([0.6, 1.0, 0.75]) * (1 - k) * (1.2 if a < 0.08 else 1)
        skriv(ut, f)

# ---------- 5. dorren ----------
if VAR == 5:
    SY = 360; T_L0, T_L1, T_OP = 1.95, 2.24, 2.27; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    def oppen(t):   # hur langt halvorna har glidit (bildpunkter): forst en springa, sedan allt fortare
        u = float(np.clip((t - T_OP) / (DUR - 1 / FPS - T_OP), 0, 1)); return 22 * float(sm(u, 0, 0.3)) + 360 * float(sm(u, 0.22, 1.0)) ** 2.2
    VARM = np.array([1.0, 0.86, 0.62])
    for f in range(N):
        t = f / FPS
        if t < T_L0: skriv(STATISK if t > 1.0 else sken(titel(t)), f); continue
        T_ = titel(2.0); ut = None
        L = 1400 * float(sm(t, T_L0, T_L1)) ** 0.8; linje = (np.abs(xx - NOT_C[0]) < L).astype(np.float32) * (t < DUR + 0.04)
        op = oppen(t)
        if op <= 0.5: ut = sken(T_)
        else:   # halvorna: ovre glider upp, undre ner. Dorrkanterna glor, videon bakom ar overexponerad och skuggad vid kanterna
            o = int(round(op)); V = skala(vid(t), 1.06 - 0.06 * float(sm(t, T_OP, DUR + EFTER)))
            ljus = 1 + 3.2 * (1 - float(sm(t, T_OP + 0.05, DUR + EFTER)))
            V = V * ljus * (1 + 0.25 * (1 - float(sm(t, T_OP, DUR + EFTER))) * (VARM - 1)); V = V / (1 + (ljus - 1) * 0.35 * V)
            gap = (yy > SY - o) & (yy < SY + o); kantd = np.minimum(np.abs(yy - (SY - o)), np.abs(yy - (SY + o)))
            V = V * (1 - 0.55 * np.exp(-kantd / 26) * (o < 340))[..., None]
            lag = np.zeros_like(T_); lag[:max(SY - o, 0)] = T_[min(o, SY):SY] if o < SY else 0;
            if SY + o < H: lag[SY + o:] = T_[SY:H - o]
            ut = np.where(gap[..., None], V, sken(lag)); spill = np.exp(-np.maximum(0, kantd) / 60)[..., None] * (~gap)[..., None] * (1 - float(sm(t, 2.5, DUR))) * 0.6
            ut = 1 - (1 - ut) * (1 - spill * VARM * 0.8)
        ky = np.abs(yy - SY) if op <= 0.5 else np.minimum(np.abs(yy - (SY - op)), np.abs(yy - (SY + op)))
        styr = linje * (1 if op <= 0.5 else (1 - float(sm(t, 2.45, DUR))))
        karna = np.exp(-(ky / 1.6) ** 2) * styr; halo = np.exp(-(ky / 14) ** 2) * styr * 0.5
        flare = np.exp(-(np.abs(yy - SY) / 5) ** 2) * np.exp(-((xx - NOT_C[0]) / 900) ** 2) * float(np.exp(-((t - T_OP) / 0.07) ** 2)) * 1.4
        ut = 1 - (1 - ut) * (1 - np.clip((karna + halo + flare)[..., None] * np.array([0.85, 1.0, 0.9]), 0, 1)); skriv(ut, f)
print('variant', VAR, N, 'rutor')
