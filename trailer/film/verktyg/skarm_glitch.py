# Projekt Lennart - glitchen nar LED-skarmen byter fran VANTAR PA BESOKARE till VERIFIERAR (0.5).
# Bygger sex bilder ur skarmens egna bilder, sa att glitchen hamnar i skarmens pixelrutnat: pixelrader som forskjuts i sidled,
# block med brusiga pixlar och farger som glider isar. Allt flyttas i hela skarmpixlar (bilderna har 2 x 2 bildpunkter per pixel).
# Kor:  <blender-python> film/verktyg/skarm_glitch.py      (skriver skarm-glitch-1.png ... skarm-glitch-6.png i projektets rot)
import subprocess, os, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
W, H = 336, 248
def las(f):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(ROOT, f), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.uint8).reshape(H, W, 3).astype(np.int16)
def skriv(a, f):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-', os.path.join(ROOT, f)], input=np.clip(a, 0, 255).astype(np.uint8).tobytes(), check=True)
VA, VE = las('skarm-vantar.png'), las('skarm-verifierar-v0.png'); BG = VE[2, 2].copy()   # skarmens morka bakgrund
rng = np.random.default_rng(7)
def band(a, y0, y1, dx):    # pixelrader y0-y1 (skarmpixlar) flyttas dx skarmpixlar i sidled
    a = a.copy(); s = a[2 * y0:2 * y1].copy(); a[2 * y0:2 * y1] = BG; dx *= 2
    if dx > 0: a[2 * y0:2 * y1, dx:] = s[:, :-dx]
    else: a[2 * y0:2 * y1, :dx] = s[:, -dx:]
    return a
def rgb(a, k):              # rott at hoger, blatt at vanster, k skarmpixlar
    a = a.copy(); k *= 2; a[:, k:, 0] = a[:, :-k, 0].copy(); a[:, :-k, 2] = a[:, k:, 2].copy(); return a
def brus(a, n):             # n block med slumpade pixlar i skarmens gronvita ton
    a = a.copy()
    for _ in range(n):
        w, h = rng.integers(6, 30), rng.integers(1, 5); x, y = rng.integers(0, 168 - w), rng.integers(0, 124 - h)
        v = rng.random((h, w)) ** 3; c = np.stack([60 + 150 * v, 120 + 135 * v, 90 + 120 * v], -1) * (rng.random((h, w, 1)) > 0.35)
        a[2 * y:2 * (y + h), 2 * x:2 * (x + w)] = np.repeat(np.repeat(c, 2, 0), 2, 1)
    return a
g = {}
g[1] = band(band(VA, 48, 52, 9), 64, 67, -6)                      # VANTAR PA rader 45-57, BESOKARE 62-75, VERIFIERAR 53-68
g[2] = brus(rgb(band(band(band(VA, 44, 50, -14), 53, 58, 11), 66, 72, 22), 2), 4)
g[3] = brus(rgb(np.concatenate([band(VA, 0, 60, 17)[:120], band(VE, 60, 124, -10)[120:]]), 3), 6)
g[4] = rgb(band(VE, 55, 62, 7), 2)
g[5] = band(VE, 60, 64, -4)
g[6] = band(brus(VA, 2), 40, 44, -20)   # reserv: ett kort ryck i VANTAR, anvands inte just nu
for k, a in g.items(): skriv(a, f'skarm-glitch-{k}.png')
print('klar', len(g), 'bilder')
