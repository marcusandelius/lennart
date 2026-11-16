# Stammer av fargen pa den utstansade Lennart i 3D mot den riktiga bildrutan.
# Jamfor forsta bildrutan i 2.1 (renderad) med bildrutan i 1.4, kanal for kanal, och skriver om lennart-utstansad.png sa att renderingen hamnar pa filmens farger.
# Kor:  python utstansning_kalibrera.py <renderad 0000.jpg>
import os, sys, subprocess, numpy as np
import utstansning as u
FILM = u.FILM; W, H = u.W, u.H
def las_bild(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'scale=%d:%d' % (W, H), '-f', 'rawvideo', '-pix_fmt', 'rgba' if p.endswith('.png') else 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(H, W, -1).astype(np.float32)
d = np.load(os.path.join(FILM, 'utstansning.npz')); inre = d['inre']; kar = u.krymp(inre, 4)
fot = u.las(int(d['ruta'])); ren = las_bild(sys.argv[1]); tex = las_bild(os.path.join(FILM, 'lennart-utstansad.png'))
ny = tex.copy(); fel = []
for c in range(3):
    t_, r_, f_ = tex[..., c][kar], ren[..., c][kar], fot[..., c][kar]
    # renderingen som funktion av texturen: medianen per texturniva, gjord stigande
    bins = np.linspace(0, 255, 33); mid = (bins[:-1] + bins[1:]) / 2; ut = np.full(32, np.nan)
    for i in range(32):
        s = (t_ >= bins[i]) & (t_ < bins[i + 1])
        if s.sum() > 30: ut[i] = np.median(r_[s])
    ok = ~np.isnan(ut); x, y = mid[ok], np.maximum.accumulate(ut[ok])
    y = y + np.arange(len(y)) * 1e-3                                    # strikt stigande
    # vilken texturniva ger filmens niva? (invers av kurvan)
    x, y = np.concatenate([[0.0], x, [255.0]]), np.concatenate([[min(0.0, y[0] - 1)], y, [max(255.0, y[-1] + 1)]])
    inv = np.interp(fot[..., c], y, x)
    ny[..., c] = np.where(inre, np.clip(inv, 0, 255), tex[..., c])
    fel.append(float(np.abs(r_ - f_).mean()))
print('medelfel per kanal fore:', [round(e, 1) for e in fel])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '%dx%d' % (W, H), '-i', '-', os.path.join(FILM, 'lennart-utstansad.png')], input=ny.astype(np.uint8).tobytes(), check=True)
print('skrev om lennart-utstansad.png')
