# Projekt Lennart - lagger in de rattade kartongfigurerna (del 2) i klippen 2.1-2.6.
# Figurerna ar nu rakt avskurna vid foten och vickar pa fotens kant i stallet for att ga ner i golvet (akt_plan.py, LENNART_FOT).
# Hela del 2 ar omrenderad till plan_frames_v10. Klippen 2.1-2.6 ar tidsjusterade ur rutorna, sa varje ruta i ett klipp paras ihop
# med den mest lika rutan i plan_frames_v9, och skillnaden mellan v10 och v9 for den rutan laggs pa klippets ruta. Ljudet kopieras som det ar.
# Kor:  <blender-python> film/verktyg/fot_in.py
import subprocess, os, shutil, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.abspath(os.path.join(HERE, '..')); SB = os.path.abspath(os.path.join(F, '..', 'storyboard', 'clips'))
V9, V10 = os.path.join(F, 'plan_frames_v9'), os.path.join(F, 'plan_frames_v10')
W, H = 1280, 720
def las(args, w=W, h=H, fmt='rgb24', ch=3):
    r = subprocess.run(['ffmpeg', '-v', 'error', *args, '-f', 'rawvideo', '-pix_fmt', fmt, '-'], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.uint8).reshape((-1, h, w, ch) if ch > 1 else (-1, h, w))
_d = {}
def delta(i):   # v10 - v9 for ruta i
    if i not in _d: _d.clear(); _d[i] = las(['-i', os.path.join(V10, f'{i:04d}.jpg')])[0].astype(np.float32) - las(['-i', os.path.join(V9, f'{i:04d}.jpg')])[0].astype(np.float32)
    return _d[i]
liten = lambda args: las([*args, '-vf', 'scale=96:54'], 96, 54, 'gray', 1).astype(np.float32)
P9 = liten(['-framerate', '25', '-i', os.path.join(V9, '%04d.jpg')])
for c in ['2_1', '2_2', '2_3', '2_4', '2_5', '2_6']:
    clip = os.path.join(SB, c + '.mp4'); bak = os.path.join(F, f'klipp_{c}_fore_fot.mp4')
    if not os.path.exists(bak): shutil.copyfile(clip, bak)
    K = liten(['-i', bak]); idx = [int(np.abs(P9 - k).mean((1, 2)).argmin()) for k in K]
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '25', '-i', '-', '-i', bak, '-map', '0:v', '-map', '1:a', '-c:a', 'copy',
                            '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-shortest', '-movflags', '+faststart', clip], stdin=subprocess.PIPE)
    for fr, i in zip(las(['-i', bak]), idx):
        enc.stdin.write(np.ascontiguousarray(np.clip(fr.astype(np.float32) + delta(i) + 0.5, 0, 255).astype(np.uint8)).tobytes())
    enc.stdin.close(); enc.wait(); print(c, len(idx), 'rutor, rutor i del 2:', idx[0], '-', idx[-1], flush=True)
