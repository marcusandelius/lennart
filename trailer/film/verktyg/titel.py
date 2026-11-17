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
# Overgangen till 1.1 (LENNART_TILL = bild, 1280 x 720, forsta rutan i 1.1): pixlarna blir bilden. I ett svep fran ekollonet och utat tar varje cell
# fargen fran 1.1 och bokstaverna slocknar, sedan okar upplosningen i tre steg (160, 320, 640 celler i bredd) och 1.1 tar vid i full upplosning pa slaget.
TILL = os.environ.get('LENNART_TILL')
if TILL:
    r_ = subprocess.run(['ffmpeg', '-v', 'error', '-i', TILL, '-vf', 'scale=1280:720', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    TB = np.frombuffer(r_, np.uint8).reshape(720, 1280, 3).astype(np.float64) / 255
    def mosaik(c):   # bilden i celler om c px: medelfarg per cell
        h_, w_ = 720 // c, 1280 // c; return TB.reshape(h_, c, w_, c, 3).mean((1, 3))
    M80 = mosaik(C); ys_, xs_ = np.mgrid[0:GH, 0:GW]; nc = np.argwhere(not_).mean(0)
    d_ = np.hypot((ys_ - nc[0]) * 1.0, xs_ - nc[1]); d_ /= d_.max(); t_sw = 2.08 + 0.38 * d_ + np.random.default_rng(3).random(d_.shape) * 0.06   # svepet: 2,08-2,52 s
    STEG = [(2.56, 8), (2.64, 4), (2.72, 2)]   # (fran tid, cellstorlek i px)
    def cellbild(c, gap):   # en cellbild med glipor, normerad sa att ljusstyrkan behalls; gap 0-1 hur tydliga gliporna ar
        u_ = (np.arange(c) + 0.5) / c; e_ = np.clip((0.5 - np.abs(u_ - 0.5)) / 0.14, 0, 1); cl = np.outer(e_, e_)[..., None] * 0.75 + 0.25
        sb = np.stack([0.65 + 0.35 * 1.6 * (0.5 + 0.5 * np.cos(2 * np.pi * (u_ - ph))) for ph in (1 / 6, 0.5, 5 / 6)], -1)[None, :, :] * np.ones((c, 1, 1))
        tl = cl * sb; tl = tl / tl.mean((0, 1)); return 1 + (tl - 1) * gap
GLOW = 0.55
for f in range(int(round(DUR * FPS))):
    t = f / FPS; age = t - t_on; glow = GLOW
    col = np.where((age >= 0)[..., None], np.where((age < 0.1)[..., None], FLASH, LIT), BG + BACK)
    img = np.kron(col, np.ones((C, C, 1))) * np.tile(TILE, (GH, GW, 1)); img = np.clip(img * 1.25, 0, 1)
    if TILL and t >= 2.08:
        steg = [s_ for s_ in STEG if t >= s_[0]]
        if not steg:   # svepet: celler som har bytt visar 1.1 i 80 x 45, en ruta lite ljusare nar de byter
            k_ = (t >= t_sw)[..., None]; fl = 1 + 0.35 * ((t - t_sw) < 0.045)[..., None]
            mc = np.kron(M80 * fl, np.ones((C, C, 1))) * np.tile(cellbild(C, 0.85), (GH, GW, 1))
            img = np.where(np.kron(k_, np.ones((C, C, 1))) > 0, np.clip(mc, 0, 1), img); glow = GLOW * 0.6
        else:
            c = steg[-1][1]; gap = {8: 0.6, 4: 0.3, 2: 0.08}[c]
            img = np.clip(np.kron(mosaik(c), np.ones((c, c, 1))) * np.tile(cellbild(c, gap), (720 // c, 1280 // c, 1)), 0, 1); glow = {8: 0.25, 4: 0.12, 2: 0.04}[c]
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720', '-i', '-', '-vf', 'format=gbrp,split[a][b];[b]gblur=sigma=9[g];[a][g]blend=all_mode=screen:all_opacity=%.3f,format=yuvj444p' % glow, '-q:v', '2', os.path.join(OUT, '%04d.jpg' % f)],
                       input=(img * 255).astype(np.uint8).tobytes())
print('titel', f + 1, 'rutor')
