import sys, json, numpy as np, trimesh
SRC = open('/home/user/lennart/cad/brevlada.py').read().split('# ---------------- distans')[0]
G = json.load(open('../render/geo_alt.json'))
def put(k, m): G[k] = np.round(m.vertices[m.faces].reshape(-1), 2).tolist()
sv = trimesh.load('../bv2/servo_ghost.stl')
def variant(y0, ins_y, front_tv, tvarvagg=True):
    s = SRC
    for a, b in [("X0, X1, Y0, Y1, ZT = 40.0, 74.0, -30.0, -2.0, 46.0", "X0, X1, Y0, Y1, ZT = 40.0, 74.0, %.1f, -2.0, 46.0" % y0),
                 ("INS = [(-22.3, 9.0), (-22.3, 38.0)]", "INS = [(%.1f, 9.0), (%.1f, 38.0)]" % (ins_y, ins_y)),
                 ("Y0 + T - 0.01, -16.5, T - 0.01, ZT)", "Y0 + T - 0.01, %.1f, T - 0.01, ZT)" % front_tv),
                 ("c = box(CX0, CX1, -27.0, -2.5, 4.0, ZT - 0.5)", "c = box(CX0, CX1, Y0 + 3.0, -2.5, 4.0, ZT - 0.5)")]:
        assert s.count(a) == 1, a; s = s.replace(a, b)
    if not tvarvagg:
        s = s.replace("body = U([body, bh])", "pass")
    ns = {}; sys.argv = ['x', '/dev/null', '/dev/null']; exec(s, ns)
    return ns
out = {}
for tag, args in (('A', (-22.5, -17.8, -14.7, True)), ('B', (-17.0, -17.8, -14.7, False))):
    ns = variant(*args); D = ns['D']; box = ns['box']
    body, hat, lock = ns['body'], ns['hat'], ns['lock']
    car = ns['carrier'](0.0)
    I = lambda a, b: trimesh.boolean.intersection([a, b], engine='manifold')
    print(tag, 'servo/låda', round(I(sv, body).volume, 2), 'servo/bricka', round(I(sv, car).volume, 2), 'bricka/låda', round(I(car, body).volume, 2),
          'djup från väggen', -args[0])
    put(tag + '_lada', body); put(tag + '_lock', hat); put(tag + '_handtag', lock); put(tag + '_bricka', car)
put('servo_x', sv)
json.dump(G, open('../render/geo_tunn.json', 'w'))
S0 = json.load(open('../render/shots_brev2.json'))[0]['o']
base = [s for s in S0['show'] if s[0] not in ('vit', 'tak', 'handtag')] + [['vit_utan', '#F2F2EE']]
W = '#EEEBE3'
cur = [['vit', '#F2F2EE'], ['tak', '#F2F2EE'], ['handtag', '#1A1A1A']]
G2 = json.load(open('../render/geo_brev2.json'))
for k in ('vit', 'tak', 'handtag'): G['nu_' + k] = G2[k]
json.dump(G, open('../render/geo_tunn.json', 'w'))
var = {'nu': [['nu_vit', W], ['nu_tak', W], ['nu_handtag', '#1A1A1A']],
       'A': [['A_lada', W], ['A_lock', W], ['A_handtag', '#1A1A1A']],
       'B': [['B_lada', W], ['B_lock', W], ['B_handtag', '#1A1A1A']]}
base_nu = [s for s in base if s[0] != 'vit_utan']
shots = []
for t in ('nu', 'A', 'B'):
    sh = (base_nu if t == 'nu' else base) + var[t]
    shots.append({'file': 'tunn_%s_snett.png' % t, 'o': dict(S0, title='', sub='', show=sh, pos=[180, -220, 130], at=[45, -15, 35], fov=34)})
    shots.append({'file': 'tunn_%s_sida.png' % t, 'o': dict(S0, title='', sub='', show=sh, pos=[600, -60, 60], at=[57, -25, 30], fov=13)})
json.dump(shots, open('../render/shots_tunn.json', 'w'), ensure_ascii=False)
