# Overgangen 3.2 -> 4.1: de forsta sju rutorna i del 4 landar ur en snabb panorering (innehallet glider at hoger och bromsar in).
# Bilden flyttas i sidled (kanterna fylls ut med sina egna pixlar) och far riktningsoskarpa som avtar. Samma panorering som slutet av 3.2.
# Kor:  python panorering_41.py <mapp med renderade rutor> <ut-mapp>   (rutorna 0000-0006 skrivs till ut-mappen, ovriga kopieras)
import os, sys, shutil, subprocess
src, dst = sys.argv[1:3]; os.makedirs(dst, exist_ok=True)
for f in sorted(os.listdir(src)):
    if f.endswith('.jpg'): shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))
for k in range(7):
    a = ((7 - k) / 7) ** 2; sh = round(400 - a * 380); r = max(1, round(a * 170)); f = '%04d.jpg' % k
    vf = 'pad=2080:720:400:0,fillborders=left=400:right=400:mode=smear,crop=1280:720:%d:0,dblur=angle=0:radius=%d,eq=brightness=%.4f' % (sh, r, -0.03 * a)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(src, f), '-vf', vf, '-q:v', '2', os.path.join(dst, f)], check=True)
    print('ruta', k, 'forskjutning', 400 - sh, 'oskarpa', r, flush=True)
