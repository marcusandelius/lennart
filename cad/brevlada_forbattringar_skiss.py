import sys, json, numpy as np, trimesh
from shapely.geometry import Polygon, MultiPolygon
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
src = open('/home/user/lennart/cad/brevlada.py').read().split('# ---------------- distans')[0]
DZ = 4.0
rep = [("X0, X1, Y0, Y1, ZT = 40.0, 74.0, -30.0, -2.0, 46.0", "X0, X1, Y0, Y1, ZT = 40.0, 74.0, -30.0, -2.0, 50.0"),
       ("fr + 0.6, 4.0, 33.0)", "fr + 0.6, 4.0, 37.0)"), ("fr + 0.7, 4.6, 32.4)", "fr + 0.7, 4.6, 36.4)"),
       ("36.8, 40.8)", "40.8, 44.8)"), ("fr + 0.3, 40.8, 42.2)", "fr + 0.3, 44.8, 46.2)"),
       ("fr, 40.8, 42.2).vertices", "fr, 44.8, 46.2).vertices"), ("39.1, 39.11)", "43.1, 43.11)"),
       ("XC, 29.5, 32)", "XC, 31.5, 32)"), ("28.85, 30.15)", "30.85, 32.15)"),
       # tvärväggen bort: brickan skruvas i golvet
       ("bh = U([box(BH0, BH1, Y0 + T - 0.01, -16.5, T - 0.01, ZT), box(BH0, BH1, Y0 + T - 0.01, Y1, T - 0.01, 6.0)])",
        "bh = box(CX1 + 0.5, CX1 + 8.5, -26.5, -17.0, T - 0.01, 5.0)"),
       ("bh = D(bh, [xcyl(2.0, BH0 - 1, BH1 + 1, y, z, 32) for y, z in INS])", "bh = D(bh, [trimesh.creation.cylinder(radius=2.0, segment=[[CX1 + 4.5, y, 1], [CX1 + 4.5, y, 6]]) for y in (-24.0, -19.5)])")]
for a, b in rep:
    assert src.count(a) == 1, a; src = src.replace(a, b)
sys.argv = ['x', '/dev/null', '/dev/null']
exec(src)
G = json.load(open('../render/geo_alt.json'))
def put(k, m, t=(0, 0, 0)):
    m = m.copy(); m.apply_translation(t); G[k] = np.round(m.vertices[m.faces].reshape(-1), 2).tolist()
cyl = lambda r, a, b, s=24: trimesh.creation.cylinder(radius=r, segment=[a, b], sections=s)
# 1. dränering i golvet, droppnäsa bak på locket
body = D(body, [cyl(1.0, [x, y, -1], [x, y, 3]) for x, y in ((44.5, -26), (69.5, -26), (69.5, -5))])
band = D(ext_y(outer, Y1 - 0.01, -0.5), [ext_y(Point(XC, ZT).buffer(R_O - 1.2, resolution=96).intersection(sbox(X0 - 1, ZT - 1, X1 + 1, ZT + R_O)), Y1 - 1, 0)])
band = D(band, [box(X0 - 1, X1 + 1, -3, 1, ZT - 1, ZT + 0.8)])          # droppnäsa: bandet slutar 0,8 över väggarna
hat2 = D(U([hat, band]), [PIL])
# 2. magneter 6x3: i väggarnas överkant och i lockets läppar
mag = [cyl(3.0, [x, -16, ZT - 3.2], [x, -16, ZT - 0.2]) for x in (X0 + 1.0 + 0.0, X1 - 1.0)]
mag_l = [cyl(3.0, [x, -16, ZT + 0.2], [x, -16, ZT + 2.5]) for x in (X0 + 1.0, X1 - 1.0)]
# 3. brickan med fot, skruvas lodrätt i golvet
fot = box(CX1 - 0.01, CX1 + 9, -27.0, -16.5, 5.0, 8.0)
bricka = U([carrier(0.0), fot])
bricka = D(bricka, [cyl(1.7, [CX1 + 4.5, y, 4], [CX1 + 4.5, y, 9]) for y in (-24.0, -19.5)])
skruv = U([cyl(2.7, [CX1 + 4.5, y, 8.0], [CX1 + 4.5, y, 9.6]) for y in (-24.0, -19.5)])
# 4. kabeln: ut i nedre änden, spår i golvet bakåt, upp bakom servot till hålet
sv = trimesh.load('../bv2/servo_ghost.stl')
pts = np.array([[67, -8, 15.4], [67, -8, 3.2], [67, -1.0, 3.2], [53, -1.0, 3.2], [53, -1.0, 30], [53, 1.5, 30]], float)
kab = U([cyl(0.75, pts[i], pts[i + 1], 12) for i in range(len(pts) - 1)] + [trimesh.creation.icosphere(1, radius=0.75).apply_translation(p) for p in pts[1:-1]])
krok = U([box(59, 61, -2.0, -1.2, 2, 5.0), box(59, 61, -2.0, 0.0, 4.4, 5.0)])
spar = box(52, 68, -2.0, -0.1, 1.2, 2.1)
body = D(body, [spar])
# 6. tidningshållare på högra sidan med en hoprullad tidning
hx, hz = X1 + 4.2, 17.0
hall = D(cyl(3.9, [hx, -29, hz], [hx, -11, hz], 32), [cyl(3.3, [hx, -30, hz], [hx, -10, hz], 32), box(hx - 5, hx + 5, -30, -10, hz + 2.2, hz + 5)])
hall = U([hall, box(X1 - 0.01, hx - 2.5, -27, -25, hz - 3, hz + 1), box(X1 - 0.01, hx - 2.5, -15, -13, hz - 3, hz + 1)])
tidn = cyl(3.2, [hx, -32.5, hz], [hx, -12, hz], 32)
# 7. stenplatta
sten = D(box(X0 - 3, X1 + 9, Y0 - 4, -2.5, -0.3, 1.8), [box(X0, X1, Y0, Y1, -1, 3)])
# 8. husnummer och 9. gångjärn och nyckelhål (svarta)
tp = TextPath((0, 0), '7', size=7.5, prop=FontProperties(family='DejaVu Sans', weight='bold'))
polys = [Polygon(p) for p in tp.to_polygons() if len(p) > 2]
polys.sort(key=lambda p: -p.area); shape = polys[0]
for p in polys[1:]: shape = shape.difference(p) if shape.contains(p) else shape.union(p)
num = trimesh.creation.extrude_polygon(shape, 0.6)
num.apply_transform(np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
c = num.bounds.mean(0); num.apply_translation([XC - c[0], Y0 - 0.3 - num.bounds[0][1] - 0.0 - 0.3, 10.5 - num.bounds[0][2]])
gj = U([cyl(0.8, [X0 + 3.4, Y0 - 0.9, z - 2.5], [X0 + 3.4, Y0 - 0.9, z + 2.5], 16) for z in (9.0, 32.0)] +
       [box(X0 + 3.4, X0 + 7.5, Y0 - 0.5, Y0 + 0.1, z - 1.2, z + 1.2) for z in (9.0, 32.0)])
nyckel = U([cyl(0.9, [XC, Y0 - 0.4, 27.6], [XC, Y0 + 0.1, 27.6], 16), box(XC - 0.4, XC + 0.4, Y0 - 0.4, Y0 + 0.1, 25.4, 27.6)])
svart = U([lock, num, gj, nyckel])
put('f_lada', body); put('f_lada_snitt', D(body, [box(X0 - 5, X1 + 5, Y0 - 5, Y0 + T + 0.3, -1, ZT + 5)])); put('f_lock', hat2); put('f_svart', svart); put('f_hall', hall); put('f_tidn', tidn); put('f_sten', sten)
put('f_lock_upp', hat2, (0, 0, 30)); put('f_mag', U(mag)); put('f_mag_upp', U(mag_l), (0, 0, 30))
put('f_bricka', bricka); put('f_skruv', skruv); put('f_servo', sv); put('f_kabel', kab); put('f_krok', krok)
json.dump(G, open('../render/geo_forb.json', 'w'))
S0 = json.load(open('../render/shots_brev2.json'))
base = [s for s in S0[0]['o']['show'] if s[0] not in ('vit', 'tak', 'handtag')] + [['vit_utan', '#F2F2EE']]
W = '#EEEBE3'
ute = base + [['f_lada', W], ['f_lock', W], ['f_svart', '#1A1A1A'], ['f_hall', '#1A1A1A'], ['f_tidn', '#F7F5EE'], ['f_sten', '#8C8F92']]
inne = base + [['f_lada_snitt', W], ['f_mag', '#5A5E62'], ['f_hall', '#1A1A1A'], ['f_tidn', '#F7F5EE'], ['f_sten', '#8C8F92'],
               ['f_bricka', '#2A2B2E'], ['f_skruv', '#B8B8B8'], ['f_servo', '#2B5C8A'], ['f_kabel', '#E07B39'], ['f_krok', '#2A2B2E']]
o1 = dict(S0[0]['o'], title='Förslag: utsidan', sub='4 mm högre, tidningshållare med tidning, stenplatta, husnummer, gångjärn och nyckelhål. Lockets bakkant går nästan ända in till väggen.', show=ute, pos=[175, -215, 120], at=[52, -15, 32])
o2 = dict(S0[1]['o'], title='Förslag: insidan', sub='Framväggen bortskuren. Brickan har en fot som skruvas lodrätt i golvet (2 × M3 ovanifrån), kabeln (orange) går i ett spår i golvet och en krok bakom servot. Magneter i väggarnas överkant och lockets läppar, dräneringshål i golvet.',
          show=inne, pos=[38, -125, 100], at=[58, -14, 22], fov=32, labels=[{"p": [61.6, -21.75, 12], "t": "Skruvar ovanifrån"}, {"p": [73, -16, 50], "t": "Magnet"}, {"p": [67, -8, 8], "t": "Kabel i spår"}, {"p": [44.5, -26, 4], "t": "Dränering"}])
o3 = dict(S0[0]['o'], title='Förslag: bakifrån ovanifrån', sub='Lockets bakkant (droppnäsan) går ut till 0,5 mm från väggen, så regn längs väggen inte faller ner på servot.', show=ute,
          pos=[95, 40, 150], at=[57, -15, 45])
json.dump([{'file': 'forb_ute.png', 'o': o1}, {'file': 'forb_inne.png', 'o': o2}], open('../render/shots_forb.json', 'w'), ensure_ascii=False)
for n, m in (('lada', body), ('lock', hat2), ('bricka', bricka), ('kabel', kab), ('mag', U(mag + mag_l))): m.export('sn_%s.stl' % n)
print('ok', body.is_watertight, hat2.is_watertight)
