# Projekt Lennart - klipp 1.2 "Nastan varje dag": tre mobilklipp i hojdformat som kort bredvid varandra.
# Korten har rundade horn, en mjuk skugga och en tunn ljus kant. De glider upp och tonar fram ett i taget
# (mitten, vanster, hoger) pa samma tider som forut. Bakgrunden ar mittenklippet, kraftigt oskarpt och mork i filmens blagrona ton.
# Kor:  <blender-python> film/verktyg/tre_rutor.py <ut.mp4> [ljud fran.mp4]
import subprocess, sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.abspath(os.path.join(HERE, '..', '..'))
UT = sys.argv[1]; LJUD = sys.argv[2] if len(sys.argv) > 2 else None
W, H, FPS, DUR = 1280, 720, 25, 3.92; N = round(DUR * FPS)
CW, CH, R, GAP = 334, 594, 26, 40                         # kortet i 9:16, hornradie, mellanrum
X0 = (W - 3 * CW - 2 * GAP) // 2; Y0 = (H - CH) // 2
GR = 'eq=contrast=1.06:saturation=1.1'
# (fil, start i klippet, kortets plats 0-2 fran vanster, tid da kortet kommer)
KORT = [('PXL_20260708_101333609.TS.mp4', 12.6, 1, 0.0), ('1000007512.mp4', 14.0, 0, 1.52), ('VID-20261114-WA0000~3.mp4', 8.6, 2, 2.56)]

def las(args, w, h):
    r = subprocess.run(['ffmpeg', '-v', 'error', *args, '-frames:v', str(N), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(r, np.uint8).reshape(-1, h, w, 3)
    if len(a) < N: a = np.concatenate([a, np.repeat(a[-1:], N - len(a), 0)])
    return a
def kort(f, ss):   # klippet i kortets storlek med en langsam inzoomning, som de andra mobilklippen i akt 1
    return las(['-ss', str(ss), '-t', str(DUR + 0.2), '-i', os.path.join(P, f), '-vf', f"fps={FPS},{GR},scale=w='2*trunc({CW // 2}*(1+0.03*t))':h=-2:eval=frame,crop={CW}:{CH}"], CW, CH)
def mask(w, h, r):   # rundad rektangel med mjuk kant (en pixel)
    y, x = np.mgrid[0:h, 0:w] + 0.5
    dx = np.maximum(np.abs(x - w / 2) - (w / 2 - r), 0); dy = np.maximum(np.abs(y - h / 2) - (h / 2 - r), 0)
    return np.clip(r - np.hypot(dx, dy) + 0.5, 0, 1).astype(np.float32)
def blur(a, s):
    k = np.exp(-0.5 * (np.arange(-3 * s, 3 * s + 1) / s) ** 2); k /= k.sum()
    a = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 0, a); return np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 1, a)

M = mask(CW, CH, R)
KANT = np.clip(mask(CW + 2, CH + 2, R + 1) - np.pad(M, 1), 0, 1)          # en pixel bred ljus kant runt kortet
PADS = 60; SKUGGA = blur(np.pad(M, PADS), 18) * 0.62                      # skuggan, nedforskjuten
# bakgrunden: mittenklippet oskarpt, morkt och avfargat, blandat med filmens blagrona botten och en vinjett
bg = las(['-ss', '12.6', '-t', str(DUR + 0.2), '-i', os.path.join(P, KORT[0][0]), '-vf', f'fps={FPS},scale={W}:-2,crop={W}:{H},gblur=sigma=50,eq=saturation=0.4'], W, H).astype(np.float32)
yy, xx = np.mgrid[0:H, 0:W]; rr = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
BOTTEN = (np.array([7, 21, 26], np.float32) * (1.35 - 0.55 * np.clip(rr, 0, 1.4))[..., None])
VINJ = (1 - 0.35 * np.clip(rr - 0.3, 0, 1) ** 1.5)[..., None]
KLIPP = [(kort(f, ss), X0 + plats * (CW + GAP), b) for f, ss, plats, b in KORT]

enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        *(['-i', LJUD, '-map', '0:v', '-map', '1:a', '-c:a', 'copy', '-shortest'] if LJUD else []),
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', UT], stdin=subprocess.PIPE)
for n in range(N):
    t = n / FPS; im = (bg[n] * 0.22 + BOTTEN * 0.85) * VINJ
    for frames, x, b in KLIPP:
        p = min(max((t - b) / 0.55, 0), 1)
        if p <= 0: continue
        e = 1 - (1 - p) ** 3; a = min(max((t - b) / 0.32, 0), 1); y = Y0 + round(34 * (1 - e))
        sy, sx = y - PADS + 14, x - PADS                                    # skuggan
        y1, y2 = max(sy, 0), min(sy + SKUGGA.shape[0], H)
        im[y1:y2, sx:sx + SKUGGA.shape[1]] *= (1 - SKUGGA[y1 - sy:y2 - sy] * a)[..., None]
        k = (M * a)[..., None]; reg = im[y:y + CH, x:x + CW]
        im[y:y + CH, x:x + CW] = reg * (1 - k) + frames[n].astype(np.float32) * k
        kr = (KANT * a * 0.16)[..., None]; reg = im[y - 1:y + CH + 1, x - 1:x + CW + 1]
        im[y - 1:y + CH + 1, x - 1:x + CW + 1] = reg * (1 - kr) + 255 * kr
    enc.stdin.write(np.clip(im, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('klar', UT, N, 'rutor')
