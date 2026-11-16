# Stansar ut Lennart ur sista bildrutan i klipp 1.4, som en dekal med vit kant.
# Ger film/lennart-utstansad.png (RGBA, 1280x720) som anvands som kartongfigur i akt_plan.py, och masker till overgangen (overgang_14.py).
# Kor med Blenders python (har numpy):  python utstansning.py [bildruta]
import os, sys, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE)
W, H = 1280, 720; RUTA = int(sys.argv[1]) if __name__ == '__main__' and len(sys.argv) > 1 else 184; KANT = 18

def las(ruta):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(FILM, 'klipp_1_4_original.mp4'), '-vf', 'select=eq(n\\,%d),scale=%d:%d:flags=lanczos' % (ruta, W, H),
                        '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(H, W, 3).astype(np.float32)

def falt(m, k):   # faltning med FFT, samma storlek
    pad = np.zeros((H + 2 * 64, W + 2 * 64), np.float32); pad[64:64 + H, 64:64 + W] = m
    K = np.zeros_like(pad); kh, kw = k.shape; K[:kh, :kw] = k; K = np.roll(K, (-(kh // 2), -(kw // 2)), (0, 1))
    return np.real(np.fft.irfft2(np.fft.rfft2(pad) * np.fft.rfft2(K), pad.shape))[64:64 + H, 64:64 + W]
def skiva(r): y, x = np.mgrid[-r:r + 1, -r:r + 1]; return (x * x + y * y <= r * r).astype(np.float32)
def gauss(s): r = int(3 * s); y, x = np.mgrid[-r:r + 1, -r:r + 1]; g = np.exp(-(x * x + y * y) / (2 * s * s)); return (g / g.sum()).astype(np.float32)
def vidga(m, r): return falt(m.astype(np.float32), skiva(r)) > 0.5
def krymp(m, r): return ~vidga(~m, r)
def mjuk(m, s): return falt(m.astype(np.float32), gauss(s)) > 0.5
def sammanhang(m, fro):   # allt i m som hanger ihop med fro (geodetisk utvidgning)
    s = fro & m
    while True:
        n = m & (s | np.roll(s, 1, 0) | np.roll(s, -1, 0) | np.roll(s, 1, 1) | np.roll(s, -1, 1))
        if (n == s).all(): return s
        s = n

def utstansa(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]; lum = 0.3 * r + 0.59 * g + 0.11 * b
    varm = (r - b > 22) & (r > g - 4)                                  # pals: rod-orange till brun
    vit = (lum > 150) & (r - b > 4) & (r >= g - 6)                     # magen: ljus och svagt varm (platen och himlen ar kalla)
    m = varm | vit
    m = krymp(vidga(m, 3), 3)                                          # stang sma hal
    fro = np.zeros_like(m); fro[330:470, 600:760] = True                 # mitt i kroppen
    m = sammanhang(krymp(m, 2), fro); m = vidga(m, 2) & (varm | vit | vidga(m, 1))
    kant = np.zeros_like(m); kant[0, :] = kant[-1, :] = True; kant[:, 0] = kant[:, -1] = True
    m = ~sammanhang(~m, kant & ~m)                                       # fyll hal som inte nar kanten (ogat)
    m = m & ~((r - b < 8) & (lum > 95))                                  # men inte ljus kall bakgrund som blev innesluten mellan svansen och huvudet
    m = sammanhang(mjuk(krymp(vidga(m, 6), 6), 2.5), fro)               # jamn kontur, en enda bit
    return m

if __name__ == '__main__':
    img = las(RUTA); inre = utstansa(img)
    yttre = mjuk(vidga(inre, KANT), 7)
    np.savez_compressed(os.path.join(FILM, 'utstansning.npz'), inre=inre, yttre=yttre, ruta=RUTA)
    papper = np.array([246, 243, 236], np.float32)
    rgba = np.zeros((H, W, 4), np.float32); rgba[..., :3] = np.where(inre[..., None], img, papper); rgba[..., 3] = 255 * yttre
    # mjuk kant pa alfa sa att stansningen inte blir taggig
    a = falt(yttre.astype(np.float32), gauss(0.8)); rgba[..., 3] = 255 * np.clip(a, 0, 1)
    ut = os.path.join(FILM, 'lennart-utstansad.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '%dx%d' % (W, H), '-i', '-', ut], input=rgba.astype(np.uint8).tobytes(), check=True)
    prov = np.where(yttre[..., None], rgba[..., :3], img * 0.25 + np.array([0, 40, 60]) * 0.75)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-i', '-', os.path.join(FILM, 'utstansning_prov.jpg')], input=prov.astype(np.uint8).tobytes(), check=True)
    print('klar', ut, 'andel', round(float(inre.mean()), 3))
