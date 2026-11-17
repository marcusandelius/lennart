# Projekt Lennart - titeln (0.6): PROJEKT LENNART och ett ekollon i skarmens pixelrutnat. Kameran i 0.5 aker in tills skarmens pixlar fyller bilden
# och slocknar; titeln fortsatter i samma rutnat (80 x 45 pixlar a 16 px), och bokstavernas pixlar tands i slumpvis ordning.
# Kor:  <Blenders python> titel.py <ut-mapp> [langd i s]      (skriver 1280 x 720 jpg-rutor via ffmpeg)
import sys, os, subprocess, numpy as np
OUT = sys.argv[1]; DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 2.8; FPS = 25; C = 16; GW, GH = 80, 45; os.makedirs(OUT, exist_ok=True)
F = {  # 5 x 7-typsnitt
 'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'], 'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
 'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'], 'J': ['00111', '00010', '00010', '00010', '00010', '10010', '01100'],
 'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'], 'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'],
 'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'], 'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
 'N': ['10001', '11001', '10101', '10101', '10011', '10001', '10001'], 'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001']}
# en not i pixlar (EK ekollon, vald: kanns igen bast i pixlar. H1 och H2 ar hasselnotter; valj med LENNART_NOT) till vanster om texten, lika hog som de tva raderna (samma not som Lennart far i filmen): liten spets, rund kropp med en glans och den ljusa basen nertill
NOTER = {'EK': ['.....##......', '......#......', '......#......', '..#########..', '.#.........#.', '#...........#', '#...........#', '#...........#', '.#.........#.', '..#########..', '..#.#####.#..', '..#.#####.#..', '..#.#####.#..', '...#.###.#...', '...#..#..#...', '....#...#....', '.....###.....'],
         'H1': ['.......#.......', '......#.#......', '....##...##....', '...#...#...#...', '..#...#.#...#..', '.#...#...#...#.', '.#..#.....#..#.', '#...#.....#...#', '#..#.......#..#', '#..#.......#..#', '#..#.......#..#', '.#...........#.', '.#...........#.', '..###########..', '..###########..', '...#.#.#.#.#...', '....#######....'],
         'H2': ['.......#.......', '.......#.......', '......#.#......', '.....#.#.#.....', '....#..#..#....', '...#..#.#..#...', '..#..#...#..#..', '.#..#.....#..#.', '.#..#.....#..#.', '#..#.......#..#', '#..#.......#..#', '#..#.......#..#', '.#...........#.', '.#############.', '.#############.', '..#.#.#.#.#.#..', '...#########...']}
NOT = NOTER[os.environ.get('LENNART_NOT', 'EK')]
NW, GAP_N, TW = len(NOT[0]), 3, 7 * 6 - 1; X_NOT = (GW - (NW + GAP_N + TW)) // 2; X_TXT = X_NOT + NW + GAP_N
on = np.zeros((GH, GW), bool); not_ = np.zeros((GH, GW), bool)
for r, row in enumerate(NOT):
    for c, b in enumerate(row):
        if b == '#': not_[14 + r, X_NOT + c] = True
for line, y0 in (('PROJEKT', 14), ('LENNART', 24)):
    x0 = X_TXT
    for i, ch in enumerate(line):
        for r, row in enumerate(F[ch]):
            for c, b in enumerate(row):
                if b == '1': on[y0 + r, x0 + i * 6 + c] = True
rng = np.random.default_rng(7); ys, xs = np.where(on); t_on = np.full(on.shape, 1e9); t_on[ys, xs] = 0.22 + rng.random(len(ys)) * 0.5   # pixlarna tands mellan 0,22 och 0,72 s
ys, xs = np.where(not_); t_on[ys, xs] = 0.12 + rng.random(len(ys)) * 0.45   # noten tands lite fore texten, mellan 0,12 och 0,57 s
BG = np.array([6, 18, 11]) / 255; LIT = np.array([96, 214, 150]) / 255; FLASH = np.array([235, 255, 240]) / 255; BACK = np.array([0.0035, 0.0065, 0.0055]) * 1.4
# en cell: mjuka morka glipor och svaga RGB-subpixlar (samma som skarmens material i oppning.py)
u = (np.arange(C) + 0.5) / C; e = np.clip((0.5 - np.abs(u - 0.5)) / 0.14, 0, 1); cell = np.outer(e, e)[..., None] * 0.75 + 0.25
sub = np.stack([0.65 + 0.35 * 1.6 * (0.5 + 0.5 * np.cos(2 * np.pi * (u - ph))) for ph in (1 / 6, 0.5, 5 / 6)], -1)[None, :, :] * np.ones((C, 1, 1))
TILE = cell * sub
# Overgangen till 1.1 (LENNART_BAKOM = mapp med balkongvideon fore 1.1, rutor 00.jpg, 01.jpg ... a 0,04 s fran kallklippets borjan; LENNART_BAKOM_T = tiden i
# kallklippet dar 1.1 borjar): pixlarna lossnar och avslojar videon bakom. Bakgrundens pixlar lossnar forst, fran nagra stallen runt kanterna och utat,
# faller en bit med tyngd, krymper och slocknar. Bokstaverna och ekollonet svavar en stund over balkongen och faller sist, sa att 1.1 tar vid pa slaget.
BAKOM = os.environ.get('LENNART_BAKOM'); B_T = float(os.environ.get('LENNART_BAKOM_T', '0.48'))
if BAKOM:
    def bakom(t):   # videon bakom: kallklippets tid B_T + (t - DUR), stilla fore kallklippets borjan
        n_ = int(round(max(0.0, B_T + t - DUR) * FPS)); p_ = os.path.join(BAKOM, '%02d.jpg' % n_)
        r_ = subprocess.run(['ffmpeg', '-v', 'error', '-i', p_, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(r_, np.uint8).reshape(720, 1280, 3) / 255 * np.array([1.0, 0.973, 0.979])   # samma ton som 1.1
    rr = np.random.default_rng(11); ys_, xs_ = np.mgrid[0:GH, 0:GW]
    fron = [(0, rr.uniform(0, GW)), (GH - 1, rr.uniform(0, GW)), (rr.uniform(0, GH), 0), (rr.uniform(0, GH), GW - 1), (0, 0), (GH - 1, GW - 1), (rr.uniform(0, GH), rr.uniform(0, GW))]
    dist = np.min([np.hypot(ys_ - a_, xs_ - b_) for a_, b_ in fron], 0); dist /= dist.max()
    t_los = 1.70 + 0.55 * dist ** 0.9 + rr.random(dist.shape) * 0.10; lang = np.full(dist.shape, 0.28)
    tand = on | not_; t_los[tand] = 2.52 + rr.random(tand.sum()) * 0.08; lang[tand] = 0.16   # bokstaverna sist och fortare
    vx = rr.uniform(-60, 60, dist.shape); G_ = 2600.0
def glod(x):   # mjukt sken (som gblur sigma 9 med skarmblandning): nedskalat 4 ggr, gaussisk osk. sigma 2,25, uppskalat
    h_, w_ = x.shape[0] // 4, x.shape[1] // 4; d_ = x.reshape(h_, 4, w_, 4, 3).mean((1, 3))
    k_ = np.exp(-0.5 * (np.arange(-7, 8) / 2.25) ** 2); k_ /= k_.sum()
    d_ = np.apply_along_axis(lambda v: np.convolve(v, k_, 'same'), 0, d_); d_ = np.apply_along_axis(lambda v: np.convolve(v, k_, 'same'), 1, d_)
    return np.kron(d_, np.ones((4, 4, 1)))
for f in range(int(round(DUR * FPS))):
    t = f / FPS; age = t - t_on
    col = np.where((age >= 0)[..., None], np.where((age < 0.1)[..., None], FLASH, LIT), BG + BACK)
    img = np.kron(col, np.ones((C, C, 1))) * np.tile(TILE, (GH, GW, 1)); img = np.clip(img * 1.25, 0, 1)
    if BAKOM and t >= 1.70:
        sitter = t < t_los; A = np.kron(sitter[..., None].astype(float), np.ones((C, C, 1))); T_ = img * A
        for (cy, cx) in np.argwhere(~sitter):
            a_ = t - t_los[cy, cx]; k_ = a_ / lang[cy, cx]
            if k_ >= 1: continue
            al = 1 - k_; s_ = 1 - 0.45 * k_; n_ = max(2, int(round(C * s_))); ix = (np.arange(n_) * C / n_).astype(int)
            blk = img[cy * C:(cy + 1) * C, cx * C:(cx + 1) * C][np.ix_(ix, ix)]
            y0_ = int(round(cy * C + (C - n_) / 2 + 0.5 * G_ * a_ * a_)); x0_ = int(round(cx * C + (C - n_) / 2 + vx[cy, cx] * a_))
            ya, yb, xa, xb = max(y0_, 0), min(y0_ + n_, 720), max(x0_, 0), min(x0_ + n_, 1280)
            if ya >= yb or xa >= xb: continue
            b_ = blk[ya - y0_:yb - y0_, xa - x0_:xb - x0_]
            T_[ya:yb, xa:xb] = T_[ya:yb, xa:xb] * (1 - al) + b_ * al; A[ya:yb, xa:xb] = A[ya:yb, xa:xb] * (1 - al) + al
        bas = bakom(t) * (1 - A) + T_; ut = 1 - (1 - bas) * (1 - 0.55 * glod(T_))
    else:
        ut = 1 - (1 - img) * (1 - 0.55 * glod(img)) if BAKOM else None
    if ut is not None:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720', '-i', '-', '-q:v', '2', os.path.join(OUT, '%04d.jpg' % f)], input=(np.clip(ut, 0, 1) * 255).astype(np.uint8).tobytes())
        continue
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720', '-i', '-', '-vf', 'format=gbrp,split[a][b];[b]gblur=sigma=9[g];[a][g]blend=all_mode=screen:all_opacity=0.55,format=yuvj444p', '-q:v', '2', os.path.join(OUT, '%04d.jpg' % f)],
                       input=(img * 255).astype(np.uint8).tobytes())
print('titel', f + 1, 'rutor')
