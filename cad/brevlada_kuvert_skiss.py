import sys, json, numpy as np, trimesh
from shapely.geometry import Polygon, LineString
src = open('/home/user/lennart/cad/brevlada.py').read().split('# ---------------- distans')[0]
ns = {}; sys.argv = ['x', '/dev/null', '/dev/null']; exec(src, ns)
U, D, box = ns['U'], ns['D'], ns['box']; body, hat, lock = ns['body'], ns['hat'], ns['lock']; fr = ns['Y0']; X0, X1 = ns['X0'], ns['X1']
W, H, TH = 21.0, 14.0, 0.8           # kuvertet: bredd, höjd, tjocklek
TILT, ROT = 64.0, 11.0               # lutning från horisontalplanet, vridning i planet
TONG = (3.0, 11.0, 5.0)              # tunga in i lådan: u från, u till, längd
P0 = np.array([46.5, fr + 0.6, 39.75])     # vänstra nedre hörnet, i springan
def frame():
    t, r = np.radians(TILT), np.radians(ROT)
    u0 = np.array([1.0, 0, 0]); v0 = np.array([0, -np.cos(t), np.sin(t)])
    u = np.cos(r) * u0 + np.sin(r) * v0; v = -np.sin(r) * u0 + np.cos(r) * v0; n = np.cross(u, v)
    return u, v, n
def plate(poly, th, off=0.0):
    u, v, n = frame()
    m = trimesh.creation.extrude_polygon(poly, th); m.apply_translation([0, 0, -th / 2 + off])
    T = np.eye(4); T[:3, 0], T[:3, 1], T[:3, 2], T[:3, 3] = u, v, n, P0
    m.apply_transform(T); return m
env = Polygon([(0, 0), (W, 0), (W, H), (0, H)]).buffer(0.4, join_style=1).buffer(-0.4, join_style=1)
tongue = Polygon([(TONG[0], -TONG[2]), (TONG[1], -TONG[2]), (TONG[1], 0.5), (TONG[0], 0.5)])
letter = plate(env.union(tongue), TH)
# fliken: V-formade linjer, 0,25 mm djupa på framsidan (mot betraktaren)
flap = LineString([(0.3, H - 0.3), (W / 2, H * 0.42), (W - 0.3, H - 0.3)]).buffer(0.28)
diag = [LineString([(0.3, 0.3), (W * 0.38, H * 0.55)]).buffer(0.22), LineString([(W - 0.3, 0.3), (W * 0.62, H * 0.55)]).buffer(0.22)]
groove = plate(flap.union(diag[0]).union(diag[1]).intersection(env), 0.5, off=TH / 2)   # n pekar mot betraktaren: spåren på framsidan
u, v, n = frame(); print('normal', np.round(n, 2))
letter = D(letter, [groove])
# kanal i framväggen för tungan (+0,25 spel) och mörk springa under läppen
chan = plate(Polygon([(TONG[0] - 0.25, -TONG[2] - 1), (TONG[1] + 0.25, -TONG[2] - 1), (TONG[1] + 0.25, 1.5), (TONG[0] - 0.25, 1.5)]).union(Polygon([(-0.5, -0.8), (W + 0.5, -0.8), (W + 0.5, 3.0), (-0.5, 3.0)])), TH + 0.5)
gap = box(X0 + 5.0, X1 - 5.0, fr - 2.0, fr + 0.6, 39.6, 40.9)
body2 = D(body, [chan, gap])
I = lambda a, b: trimesh.boolean.intersection([a, b], engine='manifold')
print('brev/låda', round(I(letter, body2).volume, 3), 'brev/lock', round(I(letter, hat).volume, 3), 'brev bounds', np.round(letter.bounds, 1).tolist())
inside = I(letter, box(X0, X1, fr + 2.0, -2, 0, 46)); print('tunga inne i lådan, mm3', round(inside.volume, 2), np.round(inside.bounds, 1).tolist() if inside.volume > 0 else '')
sv = trimesh.load('../bv2/servo_ghost.stl'); print('brev/servo', round(I(letter, sv).volume, 3))
letter.export('brev_asm.stl'); body2.export('lada_med_springa.stl')
G = json.load(open('../render/geo_alt.json'))
def put(k, m): G[k] = np.round(m.vertices[m.faces].reshape(-1), 2).tolist()
put('l_lada', body2); put('l_lock', hat); put('l_handtag', lock); put('l_brev', letter)
json.dump(G, open('../render/geo_brev_kuvert.json', 'w'))
S0 = json.load(open('../render/shots_brev2.json'))[0]['o']
base = [s for s in S0['show'] if s[0] not in ('vit', 'tak', 'handtag')] + [['vit_utan', '#F2F2EE']]
sh = base + [['l_lada', '#EEEBE3'], ['l_lock', '#EEEBE3'], ['l_handtag', '#1A1A1A'], ['l_brev', '#FFFFFF']]
json.dump([{'file': 'kuvert_snett.png', 'o': dict(S0, title='Brev i brevinkastet', sub='Ett tunt kuvert (21 × 14 mm, 0,8 mm tjockt) sticker snett upp ur springan. En tunga går in i en kanal genom framväggen.', show=sh)},
           {'file': 'kuvert_fram.png', 'o': dict(S0, title='', sub='', show=sh, pos=[57, -700, 48], at=[57, -15, 40], fov=7)},
           {'file': 'kuvert_sida.png', 'o': dict(S0, title='', sub='', show=sh, pos=[500, -40, 48], at=[57, -30, 44], fov=9)}],
          open('../render/shots_kuvert.json', 'w'), ensure_ascii=False)
