# Overgangen 1.4 -> 2.1 som ett fall (prov): Lennart tappar noten, kameran tiltar ner efter den och klippet sker mitt i rorelsen.
# 2.1 fortsatter med samma not som faller ner pa fatet (akt_plan.py med LENNART_FALL=1).
# Noten ar en renderad hasselnot (verktyg/not_sprite.py) som laggs pa mobilklippet. Bakgrunden flyttas uppat med rorelseoskarpa, som om kameran foljer noten ner.
# Kor:  <Blenders python> fall_14.py <sprite-mapp> <ut-mapp for 1.4-rutor> <forsta rutan i 2.1 (jpg)> [forsta ruta att skriva]
import os, sys, subprocess, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE)
SPR, UT, R21 = sys.argv[1], sys.argv[2], sys.argv[3]; FORST = int(sys.argv[4]) if len(sys.argv) > 4 else 0; os.makedirs(UT, exist_ok=True)
W, H, N, SISTA = 1280, 720, 8, 204            # de sista N rutorna (196-203) ar fallet
TASS = (1060.0, 385.0)                         # under Lennarts tassar i ruta 196 (bildens koordinater i 1280 x 720)
SLUT = (640.0, 421.0)                          # dar noten star i bilden nar 2.1 tar vid (samma som forsta rutan i 2.1)
NOT_D = 58.0                                   # notens bredd i bilden, ungefar som tassarna
def sm(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def las(n):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(FILM, 'klipp_1_4_original.mp4'), '-vf', 'select=eq(n\\,%d),scale=%d:%d:flags=lanczos' % (n, W, H), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
def las_png(p):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(160, 160, 4).astype(np.float32) / 255
def skriv(img, p): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-i', '-', '-q:v', '2', p], input=(np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes(), check=True)
def lage(s):   # (var noten ar i originalbilden, var den syns i bilden): den faller allt fortare, kameran foljer och lagger den mot mitten
    xw, yw = TASS[0] - 15 * s, TASS[1] + 1400 * s * s + 60 * s
    xt, yt = TASS[0] + (SLUT[0] - TASS[0]) * sm(s * 1.15), TASS[1] + (SLUT[1] - TASS[1]) * s
    return (xw, yw), (xt, yt)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
# Slappet genererat med Higgsfield (Seedance 2.5, startbild = ruta 176 ur mobilklippet). LENNART_GEN14=0 ger tillbaka bara mobilklippet.
# Fran ruta 177 anvands de genererade rutorna, forskjutna och skalade sa att de ligger exakt pa mobilklippet. Den genererade starten, dar Lennart sitter nastan still,
# kortas med 18 rutor sa att slappet hinner ske fore tilten. I tilten ar den genererade noten bortretuscherad och den renderade noten tar over pa samma plats.
GEN = os.environ.get('LENNART_GEN14', '1') == '1'; GEN_DIR = os.path.join(FILM, 'higgsfield_14', 'gen'); GEN_FRAN, GEN_HOPP = 177, 18
G_S, G_DX, G_DY = 1.021, 10.4, 10.4                                                       # skala och forskjutning (pixlar i 1280 x 720), anpassade mot ruta 176
G_NOT = {36: (1002, 466), 38: (1004, 475), 40: (1004, 499), 42: (1005, 519), 44: (1008, 549), 46: (1011, 574), 48: (1018, 613)}   # den genererade notens mitt (genererade rutans koordinater)
def g_not(g):
    ks = sorted(G_NOT); g = min(max(g, ks[0]), ks[-1]); a = max(k for k in ks if k <= g); b = min(k for k in ks if k >= g)
    pa, pb = G_NOT[a], G_NOT[b]; f = 0 if a == b else (g - a) / (b - a); x, y = pa[0] + (pb[0] - pa[0]) * f, pa[1] + (pb[1] - pa[1]) * f
    return ((x - W / 2 + G_DX) * G_S + W / 2, (y - H / 2 + G_DY) * G_S + H / 2)              # i mobilklippets bild
def las_gen(g, tvatta=False):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(GEN_DIR, '%03d.jpg' % g), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    img = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    if tvatta:   # ta bort noten: ytan runt den hamtas fran en ruta 16 rutor senare, nar noten ligger langt nedanfor
        ren = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(GEN_DIR, '%03d.jpg' % (g + 16)), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        ks = sorted(G_NOT); gg = min(max(g, ks[0]), ks[-1]); a_ = max(k for k in ks if k <= gg); b_ = min(k for k in ks if k >= gg); f = 0 if a_ == b_ else (gg - a_) / (b_ - a_)
        nx = G_NOT[a_][0] + (G_NOT[b_][0] - G_NOT[a_][0]) * f; ny = G_NOT[a_][1] + (G_NOT[b_][1] - G_NOT[a_][1]) * f
        m = np.clip((62 - np.hypot(XX - nx, YY - ny)) / 14, 0, 1)[..., None]; img = img * (1 - m) + ren * m
    X = (XX - W / 2) / G_S + W / 2 - G_DX; Y = (YY - H / 2) / G_S + H / 2 - G_DY
    x0 = np.clip(np.floor(X).astype(np.int32), 0, W - 2); y0 = np.clip(np.floor(Y).astype(np.int32), 0, H - 2); fx = np.clip(X - x0, 0, 1)[..., None]; fy = np.clip(Y - y0, 0, 1)[..., None]
    return img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy) + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy
def ruta(n, tvatta=False): return las_gen(n - GEN_FRAN + GEN_HOPP, tvatta) if GEN and n >= GEN_FRAN else las(n)
NOT_D0 = NOT_D   # storleken nar 2.1 tar vid
if GEN: TASS = g_not(SISTA - N - GEN_FRAN + GEN_HOPP); NOT_D = 80 * G_S; print('TASS', TASS, flush=True)
MORK = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', R21, '-vf', 'scale=%d:%d,gblur=sigma=70' % (W, H), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout, np.uint8).reshape(H, W, 3).astype(np.float32) / 255   # morkret ar 2.1:s forsta bild, mycket oskarp, sa att tonen moter klippet
def flytta(img, dx, dy):   # bilden flyttad (dx, dy). Utanfor bilden ar det morkt, med en mjuk kant, som om kameran tiltar ner forbi banken ut i morkret
    xs, ys = XX + dx, YY + dy; xi = np.clip(xs.astype(np.int32), 0, W - 1); yi = np.clip(ys.astype(np.int32), 0, H - 1)
    d = np.minimum(np.minimum(xs, W - 1 - xs), np.minimum(ys, H - 1 - ys)); a = np.clip(1 + d / 260, 0, 1)[..., None] ** 1.5   # lang mjuk kant: bilden tonar ut i skuggan
    return img[yi, xi] * a + MORK * (1 - a)
spr = [las_png(os.path.join(SPR, f)) for f in sorted(os.listdir(SPR)) if f.endswith('.png')]
for n in range(FORST, SISTA - N):
    p = os.path.join(UT, '%03d.jpg' % (n + 1))
    if not os.path.exists(p): skriv(ruta(n), p)
for k in range(N):
    s0, s1 = k / N, (k + 1) / N; src = ruta(SISTA - N + k, tvatta=True)
    # rorelseoskarpa: medel av bilden over halva tiden mellan foregaende och den har rutan
    acc = np.zeros_like(src); M = 20
    for j in range(M):
        s = s1 - 0.5 * (s1 - s0) * j / (M - 1); (xw, yw), (xt, yt) = lage(s); acc += flytta(src, xw - xt, yw - yt)
    img = acc / M * (1 - 0.55 * s1 ** 2.5)                                  # morknar mot 2.1:s morka scen
    # noten, med en liten oskarpa i fallriktningen
    (xw, yw), (xt, yt) = lage(s1); (_, _), (xt0, yt0) = lage(s0 + 0.5 * (s1 - s0))
    sp = spr[min(len(spr) - 1, round(k * (len(spr) - 1) / (N - 1)))]; sc_ = (NOT_D + (NOT_D0 - NOT_D) * sm(s1)) / 123.0; sz = int(160 * sc_)   # fran den genererade notens storlek till den i 2.1
    b = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '160x160', '-i', '-', '-vf', 'scale=%d:%d:flags=lanczos,gblur=sigma=0.8' % (sz, sz), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'],
                       input=(sp * 255).astype(np.uint8).tobytes(), capture_output=True, check=True).stdout
    sp = np.frombuffer(b, np.uint8).reshape(sz, sz, 4).astype(np.float32) / 255
    if GEN: sp[..., :3] *= 1 + (np.array([0.86, 0.67, 0.51], np.float32) - 1) * (1 - sm(s1 / 0.6))   # borjar i den genererade notens varmare ton, ar som i 2.1 nar den tar vid
    sp[..., :3] *= sp[..., 3:]   # formultiplicerad
    lay = np.zeros((H, W, 4), np.float32); steg = 24
    for j in range(steg):   # notens egen rorelse i bilden under slutartiden
        cx = xt0 + (xt - xt0) * j / (steg - 1); cy = yt0 + (yt - yt0) * j / (steg - 1); x0, y0 = int(cx - sz / 2), int(cy - sz / 2)
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + sz), min(H, y0 + sz)
        if xb > xa and yb > ya: lay[ya:yb, xa:xb] += sp[ya - y0:yb - y0, xa - x0:xb - x0] / steg
    img = img * (1 - lay[..., 3:]) + lay[..., :3]
    skriv(img, os.path.join(UT, '%03d.jpg' % (SISTA - N + k + 1)))
    print('1.4 ruta', SISTA - N + k, 'noten', round(xt), round(yt), flush=True)
