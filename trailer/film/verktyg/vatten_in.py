# Projekt Lennart - lagger in det nya vattnet i skalen (del 2) i de fardiga rutorna och klippen 2.1-2.6, utan att rendera om hela bilderna.
# akt_plan.py med LENNART_SKALRUTA=1 renderar bara omradet runt skalen och skriver omradena i skal.txt.
# 1. plan_frames_v9 = plan_frames_v8 med omradena inklistrade (mjuk kant innanfor omradet, sa att skarven inte syns).
# 2. Klippen 2.1-2.6 ar tidsjusterade ur rutorna. Varje ruta i ett klipp paras ihop med den mest lika rutan i plan_frames_v8,
#    och skillnaden mellan v9 och v8 for den rutan laggs pa klippets ruta. Ljudet kopieras som det ar.
# Kor:  <blender-python> film/verktyg/vatten_in.py
import subprocess, os, shutil, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.abspath(os.path.join(HERE, '..')); SB = os.path.abspath(os.path.join(F, '..', 'storyboard', 'clips'))
V8, V9, VR = os.path.join(F, 'plan_frames_v8'), os.path.join(F, 'plan_frames_v9'), os.path.join(F, 'vatten_rutor')
W, H, N = 1280, 720, len([f for f in os.listdir(V8) if f.endswith('.jpg')])
def las(args, w=W, h=H, fmt='rgb24', ch=3):
    r = subprocess.run(['ffmpeg', '-v', 'error', *args, '-f', 'rawvideo', '-pix_fmt', fmt, '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.uint8).reshape((-1, h, w, ch) if ch > 1 else (-1, h, w))
def bild(p): return las(['-i', p])[0]
def skriv(a, p): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-', '-q:v', '1', p], input=a.tobytes(), check=True)

# 1. nya rutor
os.makedirs(V9, exist_ok=True); omr = {}
for rad in open(os.path.join(VR, 'skal.txt')):
    f, x0, y0, x1, y1 = map(int, rad.split()); omr[f] = (x0, y0, x1, y1)
for f in range(N):
    src = os.path.join(V8, f'{f:04d}.jpg'); dst = os.path.join(V9, f'{f:04d}.jpg')
    if f not in omr: shutil.copyfile(src, dst); continue
    x0, y0, x1, y1 = omr[f]; a = bild(src).astype(np.float32); rp = os.path.join(VR, f'{f:04d}.jpg')
    rw, rh = map(int, subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', rp], capture_output=True, text=True).stdout.strip().split(','))
    r = las(['-i', rp], rw, rh)[0].astype(np.float32); bast = None
    for ox in (0, 1, -1):   # Blender kan gora omradet en pixel mindre an beraknat (oversta raden faller bort): valj den placering som stammer bast med den gamla bilden
        for oy in (0, 1, -1):
            X0, Y0 = x0 + ox, y0 + oy
            if X0 < 0 or Y0 < 0 or X0 + rw > W or Y0 + rh > H: continue
            g = a[Y0:Y0 + rh, X0:X0 + rw]; e = np.abs(g - r).mean()   # hela omradet: skalens kanter avgor (bara kanten ar for enfargad och gav en pixels hopp mellan rutorna)
            if bast is None or e < bast[0]: bast = (e, X0, Y0)
    x0, y0 = bast[1], bast[2]; x1, y1 = x0 + rw, y0 + rh; omr[f] = (x0, y0, x1, y1)
    yy, xx = np.mgrid[y0:y1, x0:x1]; k = 8.0   # mjuk kant 8 px innanfor omradet, utom dar omradet slutar vid bildkanten
    dx = np.minimum(np.where(x0 > 0, xx - x0, 99), np.where(x1 < W, x1 - 1 - xx, 99)); dy = np.minimum(np.where(y0 > 0, yy - y0, 99), np.where(y1 < H, y1 - 1 - yy, 99))
    m = np.clip(np.minimum(dx, dy) / k, 0, 1)[..., None]
    a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - m) + r * m; skriv(np.clip(a + 0.5, 0, 255).astype(np.uint8), dst)
print('plan_frames_v9 klar,', len(omr), 'rutor med nytt vatten', flush=True)

# 2. klippen
liten = lambda args: las([*args, '-vf', 'scale=96:54'], 96, 54, 'gray', 1).astype(np.float32)
P8 = liten(['-framerate', '25', '-i', os.path.join(V8, '%04d.jpg')])
for c in ['2_1', '2_2', '2_3', '2_4', '2_5', '2_6']:
    clip = os.path.join(SB, c + '.mp4'); bak = os.path.join(F, f'klipp_{c}_fore_vatten.mp4')
    if not os.path.exists(bak): shutil.copyfile(clip, bak)
    K = liten(['-i', bak]); idx = [int(np.abs(P8 - k).mean((1, 2)).argmin()) for k in K]
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '25', '-i', '-', '-i', bak, '-map', '0:v', '-map', '1:a', '-c:a', 'copy',
                            '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart', clip], stdin=subprocess.PIPE)
    ram = las(['-i', bak])
    for k, (fr, i) in enumerate(zip(ram, idx)):
        if i in omr:
            x0, y0, x1, y1 = omr[i]; fr = fr.astype(np.float32)
            d = bild(os.path.join(V9, f'{i:04d}.jpg'))[y0:y1, x0:x1].astype(np.float32) - bild(os.path.join(V8, f'{i:04d}.jpg'))[y0:y1, x0:x1].astype(np.float32)
            fr[y0:y1, x0:x1] += d; fr = np.clip(fr + 0.5, 0, 255).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(fr).tobytes())
    enc.stdin.close(); enc.wait(); print(c, len(ram), 'rutor, rutor i del 2:', idx[0], '-', idx[-1], flush=True)
