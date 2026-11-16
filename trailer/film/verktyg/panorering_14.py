# Overgangen 1.4 -> 2.1: en snabb panorering at hoger, dit Lennart tittar. Klippet sker mitt i rorelseoskarpan.
# 1.4: de sista 8 rutorna glider at hoger (och zoomar in till 2,5 ganger, sa att bilden har marginal att glida i) med vaxande riktningsoskarpa, och morknar nar den nar fagelautomatens morka sida.
# 2.1: forsta rutorna ar renderade med kameran vriden at vanster (akt_plan.py, PAN_GRAD/PAN_TID); har laggs oskarpan pa, avtagande i samma takt som vridningen bromsar.
# Kor:  python panorering_14.py <mapp med 2.1-rutor (0000.jpg ...)> <ut-mapp for 1.4-rutor> <ut-mapp for 2.1-rutor>
import os, sys, subprocess, math
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE)
W, H, N14, R_MAX = 1280, 720, 8, 150
PAN_GRAD, PAN_TID, FPS, HFOV = 24.0, 0.36, 25, 2 * math.degrees(math.atan(18 / 60))
plan, ut14, ut21 = sys.argv[1:4]
for d in (ut14, ut21): os.makedirs(d, exist_ok=True)
def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)

# 1.4: rutorna 0-196 som de ar, 197-203 panorerar
ff('-i', os.path.join(FILM, 'klipp_1_4_original.mp4'), '-vf', 'select=lt(n\\,%d),scale=%d:%d:flags=lanczos' % (204 - N14, W, H), '-fps_mode', 'passthrough', '-q:v', '2', os.path.join(ut14, '%03d.jpg'))
for k in range(N14):
    s = (k + 1) / N14; Z = 1 + 1.5 * s ** 2; mw = (Z - 1) * W / 2; r = 4 + (R_MAX - 4) * s ** 2.2   # kameran vrider och trycker in samtidigt
    x = int(2 * mw * 0.999); vf = 'select=eq(n\\,%d),scale=%d:%d:flags=lanczos,crop=%d:%d:%d:%d,dblur=angle=0:radius=%d,colorchannelmixer=rr=%.3f:gg=%.3f:bb=%.3f' % (204 - N14 + k, int(W * Z), int(H * Z), W, H, x, int((Z - 1) * H / 2), r, *[1 - 0.5 * s ** 2.5] * 3)
    ff('-i', os.path.join(FILM, 'klipp_1_4_original.mp4'), '-vf', vf, '-frames:v', '1', '-q:v', '2', os.path.join(ut14, '%03d.jpg' % (204 - N14 + k + 1)))

# 2.1: oskarpa efter hur fort kameran vrider sig (grader per ruta -> pixlar)
for f in range(int(PAN_TID * FPS) + 1):
    t = f / FPS; w = 3 * PAN_GRAD / PAN_TID * max(0.0, 1 - t / PAN_TID) ** 2 / FPS; r = 0.5 * w * W / HFOV
    src = os.path.join(plan, '%04d.jpg' % f)
    ff('-i', src, '-vf', 'dblur=angle=0:radius=%d' % max(1, round(r)) if r >= 1 else 'null', '-q:v', '2', os.path.join(ut21, '%04d.jpg' % f))
    print('2.1 ruta', f, 'oskarpa', round(r), flush=True)
