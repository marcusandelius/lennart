import sys, json, numpy as np, trimesh
from shapely.geometry import Polygon, LineString
src = open('/home/user/lennart/cad/brevlada.py').read().split('# ---------------- distans')[0]
ns = {}; sys.argv = ['x', '/dev/null', '/dev/null']; exec(src, ns)
U, D, box = ns['U'], ns['D'], ns['box']; body, hat, lock = ns['body'], ns['hat'], ns['lock']; fr = ns['Y0']; X0, X1 = ns['X0'], ns['X1']
W, H, TH = 22.0, 15.0, 0.8           # kuvertet: bredd, höjd, tjocklek
TILT, ROT = 64.0, 11.0               # lutning från horisontalplanet, vridning i planet
UC, VC = 57.0, -2.6                  # kuvertets nederkant (mitt) i planet: x och avstånd under springan
P0 = np.array([0.0, fr + 0.6, 39.75])     # springans linje i kuvertets plan (u = x)
from shapely import affinity
def frame():
    t = np.radians(TILT)
    u = np.array([1.0, 0, 0]); v = np.array([0, -np.cos(t), np.sin(t)]); return u, v, np.cross(u, v)
def plate(poly, th, off=0.0):
    u, v, n = frame()
    m = trimesh.creation.extrude_polygon(poly, th); m.apply_translation([0, 0, -th / 2 + off])
    T = np.eye(4); T[:3, 0], T[:3, 1], T[:3, 2], T[:3, 3] = u, v, n, P0
    m.apply_transform(T); return m
def place(g):   # kuvertets egna koordinater (a, b) -> planet (u, v)
    g = affinity.translate(g, -W / 2, 0); g = affinity.rotate(g, ROT, origin=(0, 0)); return affinity.translate(g, UC, VC)
rect = place(Polygon([(0, 0), (W, 0), (W, H), (0, H)]).buffer(0.4, join_style=1).buffer(-0.4, join_style=1))
SL = -0.7                                                     # det synliga slutar strax under springans linje (dolt under läppen)
synl = rect.intersection(Polygon([(-100, SL), (200, SL), (200, 100), (-100, 100)]))
TU0, TU1, TL = 60.0, 67.0, 8.0                               # tungan: x från, x till, längd under springan
tongue = Polygon([(TU0, -TL), (TU1, -TL), (TU1, SL + 0.01), (TU0, SL + 0.01)]).buffer(0.5, join_style=1).buffer(-0.5, join_style=1).intersection(Polygon([(TU0, -TL), (TU1, -TL), (TU1, SL + 0.01), (TU0, SL + 0.01)])).union(Polygon([(TU0, -1.5), (TU1, -1.5), (TU1, SL + 0.01), (TU0, SL + 0.01)]))
letter = plate(synl.union(tongue), TH)
# fliken: V-linjer och sidovikar, 0,25 mm djupa på framsidan
lines = LineString([(0.3, H - 0.3), (W / 2, H * 0.42), (W - 0.3, H - 0.3)]).buffer(0.28).union(
        LineString([(0.3, 0.3), (W * 0.38, H * 0.55)]).buffer(0.22)).union(LineString([(W - 0.3, 0.3), (W * 0.62, H * 0.55)]).buffer(0.22))
groove = plate(place(lines).intersection(synl), 0.5, off=TH / 2)
u, v, n = frame(); print('normal', np.round(n, 2))
letter = D(letter, [groove])
# kanal i framväggen för tungan (+0,25 spel) och mörk springa under läppen
CL = 0.15                                                      # spel per sida i slitsen (kuvertet ska gå att dra ur)
chan = plate(Polygon([(TU0 - 0.3, -TL - 0.6), (TU1 + 0.3, -TL - 0.6), (TU1 + 0.3, 1.5), (TU0 - 0.3, 1.5)]).union(Polygon([(X0 + 4.0, SL - 0.3), (X1 - 4.0, SL - 0.3), (X1 - 4.0, 3.0), (X0 + 4.0, 3.0)])), TH + 2 * CL)
u_, v_, n_ = frame()
hyl = trimesh.convex.convex_hull(np.vstack([P0 + a * u_ + b * v_ + c * n_ for a in (TU0 - 2.0, TU1 + 2.0) for b in (-TL - 1.8, -0.5) for c in (-2.0, 2.0)]))
hyl = trimesh.boolean.intersection([hyl, box(X0 + 2, X1 - 2, fr + 2 - 0.01, fr + 2 + 6.0, 2, ns['ZT'])], engine='manifold')
body = U([body, hyl])
gap = box(X0 + 4.0, X1 - 4.0, fr - 2.0, fr + 0.6, 39.6, 40.9)
body2 = D(body, [chan, gap])
I = lambda a, b: trimesh.boolean.intersection([a, b], engine='manifold')
print('brev/låda', round(I(letter, body2).volume, 3), 'brev/lock', round(I(letter, hat).volume, 3), 'brev bounds', np.round(letter.bounds, 1).tolist())
inside = I(letter, box(X0, X1, fr + 2.0, -2, 0, 46)); print('tunga inne i lådan, mm3', round(inside.volume, 2), np.round(inside.bounds, 1).tolist() if inside.volume > 0 else '')
sv = trimesh.load('../bv2/servo_ghost.stl'); print('brev/servo', round(I(letter, sv).volume, 3))
letter.export('brev_asm.stl'); body2.export('lada_med_springa.stl')
G = json.load(open('../render/geo_alt.json'))
def put(k, m): G[k] = np.round(m.vertices[m.faces].reshape(-1), 2).tolist()
put('l_lada', body2); put('l_lock', hat); put('l_handtag', lock); put('l_brev', letter)
letter_print = letter
json.dump(G, open('../render/geo_brev_kuvert.json', 'w'))
S0 = json.load(open('../render/shots_brev2.json'))[0]['o']
base = [s for s in S0['show'] if s[0] not in ('vit', 'tak', 'handtag')] + [['vit_utan', '#F2F2EE']]
sh = base + [['l_lada', '#EEEBE3'], ['l_lock', '#EEEBE3'], ['l_handtag', '#1A1A1A'], ['l_brev', '#FFFFFF']]
sh0 = [x for x in sh if x[0] != 'l_brev']
json.dump([{'file': 'kuvert_snett.png', 'o': dict(S0, title='Löstagbart kuvert', sub='Kuvertet (22 × 15 mm) trycks ner i en lutande slits under läppen och sitter med friktion. Ingen lim.', show=sh)},
           {'file': 'kuvert_fram.png', 'o': dict(S0, title='', sub='', show=sh, pos=[57, -700, 48], at=[57, -15, 40], fov=7)},
           {'file': 'kuvert_utan.png', 'o': dict(S0, title='', sub='', show=sh0, pos=[57, -700, 48], at=[57, -15, 40], fov=7)},
           {'file': 'kuvert_sida.png', 'o': dict(S0, title='', sub='', show=sh, pos=[500, -40, 48], at=[57, -30, 44], fov=9)}],
          open('../render/shots_kuvert.json', 'w'), ensure_ascii=False)
car = ns['carrier'](0.0)
sw = U([car.copy().apply_translation([0, 0, dz]) for dz in np.arange(0, 50, 1.0)])
print('hylsa/bricka (sänkning)', round(I(hyl, sw).volume, 2), 'hylsa/servo', round(I(hyl, sv).volume, 2), 'hylsa x', np.round(hyl.bounds[:, 0], 1))
