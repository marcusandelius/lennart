# Byggklippen i monteringen (6.1-6.2): fyra klipp från bygget svävar i varsitt hörn bakom huset, i vita ramar med rundade hörn.
# Klippen läggs bakom huset med husets mask (akt_montering.py i maskläge), så huset skymmer dem när det växer i bild.
# De poppar upp med olika mellanrum i början av sprängskissen och krymper bort strax innan huset är färdigt (6.3). Inga övertoningar.
# Kör med Blenders python (har numpy):
#   python byggklipp_6.py <rutor (jpg)> <mask (png)> <mapp med 1.mp4-4.mp4> <ut.mp4> [rutor att spara som jpg ...]
import os, sys, math, subprocess
import numpy as np

BG, MASK, KLIPP, UT = sys.argv[1:5]; SPARA = {int(x) for x in sys.argv[5:]}
W, H, FPS, N = 1280, 720, 25, len([f for f in os.listdir(BG) if f.endswith('.jpg')])
CW, CH, KANT, R_UT = 288, 162, 6, 15                  # klippets storlek, den vita kanten och hörnradien (pixlar i 720p)
OW, OH = CW + 2 * KANT, CH + 2 * KANT
SKUGGA = (0, 10, 18, 0.5)                             # förskjutning x, y, oskärpa, styrka

# (hörn, mitt x, mitt y, dyker upp, försvinner, startpunkt i klippet s, fas)
KORT = [(1, 212, 150, 0.45, 17.10, 0.0, 0.0), (4, 1068, 572, 0.70, 16.85, 0.5, 1.7),
        (2, 1068, 150, 1.20, 17.35, 0.0, 3.1), (3, 212, 572, 1.40, 17.00, 1.0, 4.4)]
POP_IN, POP_UT = 0.5, 0.35

def back_out(u, c=1.7):  # växer fram med en liten översvängning
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    v = u - 1; return 1 + (c + 1) * v ** 3 + c * v ** 2
def back_in(u, c=1.4): u = min(1.0, max(0.0, u)); return (c + 1) * u ** 3 - c * u ** 2
def sm(t, a, b): x = min(1.0, max(0.0, (t - a) / (b - a))); return x * x * (3 - 2 * x)

def rundad(w, h, r):  # mjuk alfa för en rektangel med rundade hörn (kantutjämnad)
    y, x = np.mgrid[0:h, 0:w] + 0.5
    dx = np.maximum(np.maximum(r - x, x - (w - r)), 0); dy = np.maximum(np.maximum(r - y, y - (h - r)), 0)
    return np.clip(r - np.sqrt(dx ** 2 + dy ** 2) + 0.5, 0, 1).astype(np.float32)
def oskarpa(a, r):  # box-oskärpa tre gånger, ungefär gaussisk
    for _ in range(3):
        for ax in (0, 1):
            c = np.cumsum(np.pad(a, [(r + 1, r)] * 1 + [(0, 0)] if ax == 0 else [(0, 0), (r + 1, r)], mode='edge'), axis=ax)
            a = ((c[2 * r + 1:] - c[:-2 * r - 1]) if ax == 0 else (c[:, 2 * r + 1:] - c[:, :-2 * r - 1])) / (2 * r + 1)
    return a

YTTRE = rundad(OW, OH, R_UT); INRE = rundad(CW, CH, R_UT - KANT)
P = 40; SKUGG_A = np.zeros((OH + 2 * P, OW + 2 * P), np.float32); SKUGG_A[P:P + OH, P:P + OW] = YTTRE; SKUGG_A = oskarpa(SKUGG_A, SKUGGA[2] // 3)

def las_klipp(i, start, n):  # klippet som rgb-rutor i 25 bilder/s, beskuret till 16:9, utan ljud; loopas om det är för kort
    p = os.path.join(KLIPP, '%d.mp4' % i)
    cmd = ['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-ss', str(start), '-i', p, '-an', '-vf',
           'fps=%d,scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,setsar=1' % (FPS, CW, CH, CW, CH), '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    b = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, CH, CW, 3)

def las_rutor(cmd, kanaler):
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE); n = W * H * kanaler
    while True:
        b = pr.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, kanaler)

def lagg(dst, src, alfa, cx, cy, s):  # lägger src (h, w, 3) med alfa (h, w) skalad s gånger, centrerad i (cx, cy), bilinjärt
    h, w = alfa.shape; hw, hh = w * s / 2, h * s / 2
    x0, x1 = max(0, int(math.floor(cx - hw))), min(W, int(math.ceil(cx + hw)) + 1); y0, y1 = max(0, int(math.floor(cy - hh))), min(H, int(math.ceil(cy + hh)) + 1)
    if x1 <= x0 or y1 <= y0 or s <= 0.01: return
    xs = (np.arange(x0, x1) + 0.5 - cx) / s + w / 2 - 0.5; ys = (np.arange(y0, y1) + 0.5 - cy) / s + h / 2 - 0.5
    xi = np.clip(np.floor(xs).astype(int), -1, w - 1); yi = np.clip(np.floor(ys).astype(int), -1, h - 1); fx = (xs - xi)[None, :, None]; fy = (ys - yi)[:, None, None]
    pre = np.concatenate([src * alfa[..., None], alfa[..., None]], axis=2); pre = np.pad(pre, ((1, 1), (1, 1), (0, 0)))   # förmultiplicerad, med en tom kant runt
    a_ = pre[yi + 1][:, xi + 1]; b_ = pre[yi + 1][:, xi + 2]; c_ = pre[yi + 2][:, xi + 1]; d_ = pre[yi + 2][:, xi + 2]
    v = (a_ * (1 - fx) + b_ * fx) * (1 - fy) + (c_ * (1 - fx) + d_ * fx) * fy
    reg = dst[y0:y1, x0:x1]; reg *= (1 - v[..., 3:]); reg += v[..., :3]

def main():
    klipp = {k[0]: las_klipp(k[0], k[5], int((k[4] - k[3]) * FPS) + 2) for k in KORT}
    ut = None if UT == '-' else subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                                                  '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', UT], stdin=subprocess.PIPE)
    bg = las_rutor(['ffmpeg', '-v', 'error', '-framerate', str(FPS), '-i', os.path.join(BG, '%04d.jpg'), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], 3)
    mk = las_rutor(['ffmpeg', '-v', 'error', '-framerate', str(FPS), '-i', os.path.join(MASK, '%04d.png'), '-vf', 'alphaextract', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], 1)
    vit = np.full((OH, OW, 3), (243, 242, 238), np.float32); svart = np.zeros(SKUGG_A.shape + (3,), np.float32)
    for f, (b, m) in enumerate(zip(bg, mk)):
        t = f / FPS; hus = b.astype(np.float32); bild = hus.copy(); a = m[..., 0].astype(np.float32)[..., None] / 255
        djup = sm(t, 0, 15)                                   # kameran åker in: klippen glider lite utåt och växer, som om de låg bakom huset
        for (i, cx, cy, t_in, t_ut, _, fas) in KORT:
            if t < t_in or t > t_ut + POP_UT: continue
            s = back_out((t - t_in) / POP_IN) * (1 - back_in((t - t_ut) / POP_UT)) * (1 + 0.06 * djup)
            x = cx + (cx - W / 2) * 0.05 * djup - 14 * djup + 2.5 * math.sin(t * 1.2 + fas); y = cy + (cy - H / 2) * 0.05 * djup + 4 * math.sin(t * 1.5 + fas * 1.3)
            lagg(bild, svart, SKUGG_A * SKUGGA[3], x + SKUGGA[0] * s, y + SKUGGA[1] * s, s)
            kort = vit.copy(); kort[KANT:KANT + CH, KANT:KANT + CW] = vit[KANT:KANT + CH, KANT:KANT + CW] * (1 - INRE[..., None]) + klipp[i][min(int((t - t_in) * FPS), len(klipp[i]) - 1)] * 0.94 * INRE[..., None]
            lagg(bild, kort, YTTRE, x, y, s)
        bild = hus * a + bild * (1 - a)                       # huset överst
        o = np.clip(bild + 0.5, 0, 255).astype(np.uint8)
        if ut: ut.stdin.write(o.tobytes())
        if f in SPARA:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-i', '-', '-q:v', '2', os.path.splitext(UT)[0] + '_%04d.jpg' % f if ut else os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '..', 'test_byggklipp', '%04d.jpg' % f)], input=o.tobytes(), check=True)
        if f % 50 == 0: print('ruta', f, flush=True)
    if ut: ut.stdin.close(); ut.wait()

main()
