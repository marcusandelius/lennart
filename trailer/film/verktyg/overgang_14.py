# Overgangen 1.4 -> 2.1: bilden fryser, Lennart stansas ut med vit kant, och bakgrunden faller bakat och ner ur bild.
# Bakom den syns 3D-scenen, precis som forsta bildrutan i 2.1, dar den utstansade Lennart star som kartongfigur.
# Kor med Blenders python:  python overgang_14.py <forsta bildrutan i 2.1 (jpg)> <ut-mapp>
import os, sys, subprocess, numpy as np
import utstansning as u
W, H = u.W, u.H; N = 20                                     # 20 rutor = 0,8 s, sista delen av klipp 1.4
def las_bild(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'scale=%d:%d' % (W, H), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(H, W, 3).astype(np.float32)
def sm(x, a, b): x = min(1.0, max(0.0, (x - a) / (b - a))); return x * x * (3 - 2 * x)

d = np.load(os.path.join(u.FILM, 'utstansning.npz')); inre, yttre = d['inre'], d['yttre']
fot = u.las(int(d['ruta'])); ren = las_bild(sys.argv[1]); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
papper = np.median(ren[yttre & ~u.vidga(inre, 6)], axis=0)            # kantens farg som den blir i 3D
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); F = 1.3 * W

def bilinjar(img, xs, ys):
    x0 = np.clip(np.floor(xs).astype(int), 0, W - 2); y0 = np.clip(np.floor(ys).astype(int), 0, H - 2); fx = np.clip(xs - x0, 0, 1)[..., None]; fy = np.clip(ys - y0, 0, 1)[..., None]
    return (img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx) * (1 - fy) + (img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx) * fy

for k in range(N):
    # 1. kanten vaxer ut runt ekorren (rutor 0-6)
    g = 1 - (1 - min(1.0, k / 6.0)) ** 3; r = 18 * g
    ytt = yttre if g >= 1 else (u.mjuk(u.vidga(inre, max(1, int(round(r)))), max(0.6, 7 * g)) if r >= 1 else inre.copy())
    ytt = (ytt & yttre) | inre
    # 2. bakgrunden (bilden utanfor kanten) tippar bakat runt underkanten och faller ner ur bild (rutor 3-18)
    f = min(1.0, max(0.0, (k - 3) / 15.0)); th = np.radians(82) * f ** 2; drop = 0.95 * H * f ** 2.3; Hp = H + drop
    den = F * np.cos(th) - (Hp - yy) * np.sin(th); ok = den > 1e-3
    Y = np.where(ok, (Hp - yy) * F / np.where(ok, den, 1), -1); X = (xx - W / 2) * (F + Y * np.sin(th)) / F
    xs, ys = X + W / 2, H - Y; inne = ok & (Y >= 0) & (Y <= H) & (xs >= 0) & (xs <= W - 1)
    hal = u.falt(ytt.astype(np.float32), u.gauss(0.7))                           # halet i bakgrunden dar ekorren satt
    a_bg = np.where(inne, 1 - bilinjar(hal[..., None], xs, ys)[..., 0], 0)[..., None]
    bg = bilinjar(fot, xs, ys) * (1 - 0.55 * f)                                    # mörknar nar den faller bort fran ljuset
    # 3. ekorren byter over till hur den ser ut i 3D (sista rutorna, samma bild, bara ljuset)
    w = sm(k, 11, N - 1); djur = fot * (1 - w) + ren * w
    kant = papper * (1 - w) + ren * w
    a_s = u.falt(ytt.astype(np.float32), u.gauss(0.7))[..., None]; a_i = u.falt(inre.astype(np.float32), u.gauss(0.6))[..., None]
    figur = djur * a_i + kant * (1 - a_i)
    bild = ren * (1 - a_bg) + bg * a_bg
    bild = bild * (1 - a_s) + figur * a_s
    if k == N - 1: bild = ren                                                     # sista rutan = forsta rutan i 2.1
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-i', '-', '-q:v', '2', os.path.join(OUT, '%02d.jpg' % k)],
                   input=np.clip(bild, 0, 255).astype(np.uint8).tobytes(), check=True)
    print('ruta', k, flush=True)
