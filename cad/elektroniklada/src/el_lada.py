"""
Ny elektroniklåda (ersätter 16_elektroniklada, 16b_elektroniklada_lock, 17_..._packning, 24_monteringsplatta, 25_genomforingar).
Husets ram, mm: framsidan är -y, bakväggens insida vid y 146,8, golvet vid z ca 3.

Tre delar (plus packningen):
  16_elbakstycke   bakstycke med golv: skruvas fast genom bakväggens fyra hål (M3, muttrar i fickor), skenor för plattan
  16b_elkapa       kåpa (framsida, sidor och tak): lyfts rakt upp, en M3-skruv uppifrån i ett torn på bakstycket
  24_komponentplatta  platta med stolpar och gänginsatser för all elektronik, skjuts ned i skenorna
  17_elpackning    TPU-packning mellan bakstycket och bakväggen
Kör:  python3 el_lada.py <utkatalog>
"""
import sys, os, json
import numpy as np
import trimesh
from shapely.geometry import Polygon, Point, box as sbox
from shapely.ops import unary_union

OUT = sys.argv[1] if len(sys.argv) > 1 else "ut"
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + list(bs), engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")

def box(x0, x1, y0, y1, z0, z1):
    m = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return m
def cyl_y(x, z, y0, y1, r, n=48):               # cylinder längs y
    m = trimesh.creation.cylinder(radius=r, height=y1 - y0, sections=n)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])); m.apply_translation([x, (y0 + y1) / 2, z]); return m
def cyl_z(x, y, z0, z1, r, n=48):
    m = trimesh.creation.cylinder(radius=r, height=z1 - z0, sections=n); m.apply_translation([x, y, (z0 + z1) / 2]); return m
def ext_xz(poly, y0, y1):                       # polygon i (x, z), utdragen längs y från y0 till y1
    if hasattr(poly, 'geoms'): return trimesh.util.concatenate([ext_xz(p, y0, y1) for p in poly.geoms if p.area > 0.01])
    m = trimesh.creation.extrude_polygon(poly, y1 - y0)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, -1, y1], [0, 1, 0, 0], [0, 0, 0, 1]], float)); return m
def ext_yz(poly, x0, x1):                       # polygon i (y, z), utdragen längs x
    m = trimesh.creation.extrude_polygon(poly, x1 - x0)
    m.apply_transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)); return m
def ext_xy(poly, z0, z1):
    m = trimesh.creation.extrude_polygon(poly, z1 - z0); m.apply_translation([0, 0, z0]); return m
def hexagon(x, z, s):                           # sexkant med nyckelvidd s, i (x, z)
    r = s / np.sqrt(3); return Polygon([(x + r * np.cos(a), z + r * np.sin(a)) for a in np.radians(np.arange(0, 360, 60))])
def clean(m, vmin=5.0):
    import io
    m = trimesh.util.concatenate([q for q in m.split(only_watertight=False) if abs(q.volume) > vmin])
    for dec in (4, 3, 5, None):
        m2 = m.copy() if dec is None else trimesh.Trimesh(np.round(m.vertices, dec), m.faces, process=True)
        m2.merge_vertices(); m2.update_faces(m2.nondegenerate_faces()); m2.remove_unreferenced_vertices()
        if not m2.is_watertight: continue
        r = trimesh.load(io.BytesIO(m2.export(file_type="stl")), file_type="stl")
        if r.is_watertight: return m2
    raise RuntimeError("delen blev inte tät")

# ---------------------------------------------------------------- mått
XO = 70.0                  # lådans halva bredd (utsida)
Y_FRONT = 111.0            # kåpans framsida (förrådets bakvägg vid 108,6)
Y_BACK = 145.6             # bakstyckets baksida (1,2 mm TPU-packning mot bakväggen vid 146,8)
Z_BOT, Z_TOP = 28.0, 170.0 # undersida och ovansida
TB = 4.0                   # bakstyckets tjocklek (muttrar i fickor)
TF = 2.4                   # golvets tjocklek
TC = 2.0                   # kåpans väggar
CH = 3.5                   # avfasning av de övre hörnen (taket lutar)
HOUSE_SCREWS = [(-60.0, 80.0), (60.0, 80.0), (-60.0, 164.0), (60.0, 164.0)]   # befintliga hål i bakväggen, Ø3,4
YB0 = Y_BACK - TB          # bakstyckets framsida
ZF = Z_BOT + TF            # golvets ovansida
# komponentplattan
TP = 3.0                   # tjocklek
YP1 = YB0 - 1.0            # plattans baksida: 1 mm framför bakstycket (plats för skruvspetsarna)
YP0 = YP1 - TP             # plattans framsida (komponenterna monteras här, framåt mot kåpan)
RAIL = 3.0                 # skenans läpp
PX = XO - TC - 2.4 - 0.3   # plattans halva bredd (65,3); 2 mm liv mellan plattan och kåpan bär skenan
PZ0, PZ1 = ZF + 0.3, Z_TOP - TC - 1.5   # plattans nederkant och överkant
TOWER = dict(x0=-(XO - TC - 0.3), x1=-60.0, y0=125.0, y1=YP0 - 1.3, z0=146.0)   # torn för kåpans skruv: sitter på vänstra skenan, utanför plattans lyftväg
INS_M3 = (2.0, 6.0)        # hål för M3-gänginsats (Ruthex M3: Ø4,0 × 5,7 mm)
INS_M25 = (1.8, 5.0)       # hål för M2,5-gänginsats (Ruthex M2,5: Ø3,6 × 4,5 mm) [verifiera]

TX = (TOWER['x0'] + TOWER['x1']) / 2
TY = (TOWER['y0'] + TOWER['y1']) / 2 - 0.6

def outline_xz(inset=0.0, z0=None, z1=None):
    """Lådans kontur sedd framifrån, med avfasade övre hörn."""
    z0 = Z_BOT if z0 is None else z0; z1 = Z_TOP if z1 is None else z1; x = XO - inset
    c = CH
    return Polygon([(-x, z0), (x, z0), (x, z1 - c), (x - c, z1), (-x + c, z1), (-x, z1 - c)])

# ---------------------------------------------------------------- 16 bakstycke med golv, skenor och torn
CAB_SLOTS = [(-31.0, 54.0), (11.0, 20.0), (42.0, 36.0)]  # kabelöppningar i golvet: (mitt x, bredd): servona, mittkorridoren (nätverk, kamera, 12 V), keystone-uttagen
SLOT_Y = (Y_FRONT + TC + 3.0, YP0 - 2.0)                 # öppningarnas djup i y

def rail_profile(side):
    x_in = XO - TC - 0.3                                  # skenan ligger an mot kåpans insida
    pts = [(x_in, YB0), (PX + 0.42, YB0), (PX + 0.42, YP1), (PX + 0.42 - (TP + 1.5), YP0 - 1.5), (x_in, YP0 - 1.5)]
    return [(side * x, y) for x, y in pts]

def bakstycke():
    back = ext_xz(outline_xz(0.0), YB0, Y_BACK)
    floor = box(-XO, XO, Y_FRONT, YB0 + 0.1, Z_BOT, ZF)
    lip_o = sbox(-(XO - TC - 0.3), Y_FRONT + TC + 0.3, XO - TC - 0.3, YB0 + 0.1)
    lip = ext_xy(lip_o.difference(lip_o.buffer(-1.6, join_style=2)), ZF - 0.1, ZF + 2.0)     # kant som håller kåpan på plats nedtill
    rails = []
    for sd in (-1, 1):
        r = ext_xy(Polygon(rail_profile(sd)), ZF - 0.1, Z_TOP - TC - 0.3)
        rails.append(I(r, ext_xz(outline_xz(TC + 0.3, z1=Z_TOP - TC - 0.3), YP0 - 10, YB0 + 0.2)))
    t = TOWER
    tp = Polygon([(t['x0'], t['y0']), (t['x1'], t['y0']), (t['x1'], t['y1'] - 3.2), (t['x1'] - 3.2, t['y1']), (t['x0'], t['y1'])])   # 45° baktill: skrivs ut utan stöd
    tower = I(ext_xy(tp, t['z0'], Z_TOP - TC - 0.3), ext_xz(outline_xz(TC + 0.3, z1=Z_TOP - TC - 0.3), t['y0'] - 1, YB0 + 1))
    yr = t['y1'] - 0.2                                                               # undersidan stiger 45° framåt från skenan: inget stöd när delen står
    tower = I(tower, ext_yz(Polygon([(yr, t['z0']), (yr + 10, t['z0']), (yr + 10, Z_TOP + 5), (t['y0'] - 5, Z_TOP + 5), (t['y0'] - 5, t['z0'] + (yr - t['y0'] + 5))]), t['x0'] - 1, t['x1'] + 1))
    lip = D(lip, [box(-XO, XO, YP0 - 2.0, YB0 + 1, ZF - 1, ZF + 3)])                 # ingen kant där plattan står
    m = U([back, floor, lip, tower] + rails)
    cuts = []
    for x0, w in CAB_SLOTS:
        cuts.append(ext_xy(sbox(x0 - w / 2, SLOT_Y[0], x0 + w / 2, SLOT_Y[1]).buffer(-3.0).buffer(3.0, 16), Z_BOT - 1, ZF + 3))
    for x, z in HOUSE_SCREWS:
        cuts.append(cyl_y(x, z, YB0 - 1, Y_BACK + 1, 1.7, 24))                       # M3 genom bakväggen
        cuts.append(ext_xz(hexagon(x, z, 5.6), YB0 - 1, YB0 + 2.6))                  # mutterficka framifrån
    cuts.append(cyl_z(TX, TY, Z_TOP - TC - 0.3 - INS_M3[1], Z_TOP, INS_M3[0], 32))   # gänginsats för kåpans skruv
    return clean(D(m, cuts))

# ---------------------------------------------------------------- 16b kåpa: framsida, sidor och tak, lyfts rakt upp
def kapa():
    outer = ext_xz(outline_xz(0.0, z0=ZF, z1=Z_TOP), Y_FRONT, YB0 - 0.2)
    inner = ext_xz(outline_xz(TC, z0=ZF - 1.0, z1=Z_TOP - TC), Y_FRONT + TC, YB0 + 1.0)
    m = D(outer, [inner])
    cuts = [cyl_z(TX, TY, Z_TOP - TC - 1, Z_TOP + 1, 1.7, 24)]
    for sd in (-1, 1):                                                               # ventilationsspringor i sidorna, uppe och nere
        for zc in list(np.arange(130.0, 160.0, 6.0)) + list(np.arange(40.0, 64.0, 6.0)):
            cuts.append(box(sd * XO - 3, sd * XO + 3, Y_FRONT + 7.0, YB0 - 6.0, zc - 1.5, zc + 1.5))
    return clean(D(m, cuts))

# ---------------------------------------------------------------- 24 komponentplatta
# Varje komponent: namn, läge (x, z för kortets nedre vänstra hörn sett framifrån), storlek (bredd, höjd, tjocklek över plattan),
# hål (dx, dz från hörnet), stolphöjd, insats ('m25' eller 'm3'). 'kropp' är komponentens volym framför plattan (för kollisionskontroll och bilder).
COMPONENTS = []           # fylls i nedan när måtten är kända

def standoff(x, z, h, ins, r_out=None):
    r_in, depth = INS_M25 if ins == 'm25' else INS_M3
    r_out = r_out or r_in + 1.6
    s = cyl_y(x, z, YP0 - h, YP0 + 0.5, r_out, 40)
    hole = cyl_y(x, z, YP0 - h - 1, YP0 - h + depth, r_in, 24)
    return s, hole

def platta():
    prof = Polygon([(-PX, YP1), (PX, YP1), (PX - TP, YP0), (-PX + TP, YP0)])        # avfasade kanter som glider i skenorna
    m = trimesh.creation.extrude_polygon(prof, PZ1 - PZ0); m.apply_translation([0, 0, PZ0])
    adds, cuts = [], []
    for c in COMPONENTS:
        x0, z0 = c['pos']
        for dx, dz in c.get('holes', []):
            s, h = standoff(x0 + dx, z0 + dz, c['standoff'], c['ins'])
            adds.append(s); cuts.append(h)
        for f in c.get('extra', []):
            a, cu = f(c); adds += a; cuts += cu
    for x, z in TIE_SLOTS:                                                               # par av springor för buntband
        for dx in (-3.5, 3.5):
            cuts.append(box(x + dx - 1.0, x + dx + 1.0, YP0 - 1, YP1 + 1, z - 2.5, z + 2.5))
    for poly in WINDOWS:                                                                 # fönster där inget sitter (sparar plast, luft)
        cuts.append(ext_xz(poly, YP0 - 1, YP1 + 1))
    m = U([m] + adds)
    return clean(D(m, cuts))
TIE_SLOTS = []
WINDOWS = []

# ---------------------------------------------------------------- komponenterna (mått från datablad, se README)
INS_M2 = (1.6, 4.5)        # hål för M2-gänginsats (Ruthex M2: Ø3,2 × 4,0 mm) [verifiera]
def standoff(x, z, h, ins, r_out=None):
    r_in, depth = {'m2': INS_M2, 'm25': INS_M25, 'm3': INS_M3}[ins]
    r_out = r_out or r_in + 1.6
    s = cyl_y(x, z, YP0 - h, YP0 + 0.5, r_out, 40)
    hole = cyl_y(x, z, YP0 - h - 1, YP0 - h + depth, r_in, 24)
    return s, hole
PI = dict(name='pi5', pos=(5.0, 81.5), size=(56.0, 85.0), standoff=4.0, ins='m25',
          holes=[(3.5, 23.5), (52.5, 23.5), (3.5, 81.5), (52.5, 81.5)])          # Pi 5 stående: USB/nätverk nedåt, GPIO till höger, USB-C till vänster
PCA = dict(name='pca9685', pos=(-59.0, 31.8), size=(62.23, 25.4), standoff=4.0, ins='m2',
           holes=[(3.3, 3.3), (59.18, 3.3), (3.3, 22.35), (59.18, 22.35)])        # servokontakterna nedåt
EKM = dict(name='ekm006', pos=(-59.0, 61.0), size=(60.0, 20.0), standoff=4.0, ins='m2',
           holes=[(3.0, 3.0), (57.0, 3.0), (3.0, 17.0), (57.0, 17.0)])            # 5 V till Pi:n, utgången till höger
COMPONENTS = [PI, PCA, EKM]
SERVO_PSU = dict(x0=-59.0, x1=-10.0, z0=84.0, z1=116.0)    # vagga för servoomvandlaren (ca 38 × 27 × 23, med öron 52) och buntband
WAGO = dict(x0=-59.0, x1=-19.0, z0=119.0, z1=146.0)        # plats för DC-jacket och två Wago 221, med buntband
KEY = dict(xs=(33.0, 51.5), z=36.0, w=14.8, d=19.3, t=1.6) # keystone-uttag, uttaget nedåt (kabeln in underifrån genom golvet)
TIE_SLOTS = [(11.0, 64.0), (11.0, 95.0), (11.0, 125.0), (-36.5, 88.0), (-36.5, 112.0), (-49.0, 132.0), (-30.0, 132.0), (-34.0, 156.0)]
WINDOWS = [sbox(14.0, 92.0, 52.0, 158.0).buffer(-3).buffer(3, 12)]   # bakom Pi:n: luft och mindre plast

def keystone_shelf():
    k = KEY; x0, x1 = k['xs'][0] - 10.0, k['xs'][1] + 10.0
    y0 = YP0 - 23.5
    shelf = box(x0, min(x1, PX - TP - 1.5), y0, YP0 + 0.5, k['z'], k['z'] + 3.0)
    cuts = []
    for xc in k['xs']:
        yc = YP0 - 11.75
        cuts.append(box(xc - k['w'] / 2, xc + k['w'] / 2, yc - k['d'] / 2, yc + k['d'] / 2, k['z'] - 1, k['z'] + 3.5))
        cuts.append(box(xc - k['w'] / 2 - 1.0, xc + k['w'] / 2 + 1.0, yc - k['d'] / 2 - 1.0, yc + k['d'] / 2 + 1.0, k['z'] + k['t'], k['z'] + 3.5))   # tunnare runt hålet (1,6 mm) så att uttaget snäpper fast
    gus = []                                                                    # hyllan är 3 mm tjock och klarar sig utan stöd
    return [shelf] + gus, cuts

def cradle(r, h_wall=4.0):
    """Låga kanter runt en rektangel på plattan (håller en del som buntas fast)."""
    o = sbox(r['x0'], r['z0'], r['x1'], r['z1']); ring = o.difference(o.buffer(-2.0, join_style=2))
    gap = sbox((r['x0'] + r['x1']) / 2 - 8, r['z0'] - 1, (r['x0'] + r['x1']) / 2 + 8, r['z1'] + 1)   # öppningar mitt på långsidorna för kablarna
    side_gap = sbox(r['x0'] - 1, (r['z0'] + r['z1']) / 2 - 6, r['x1'] + 1, (r['z0'] + r['z1']) / 2 + 6)
    ring = ring.difference(side_gap)
    return ext_xz(ring, YP0 - h_wall, YP0 + 0.5)

def platta():
    prof = Polygon([(-PX, YP1), (PX, YP1), (PX - TP, YP0), (-PX + TP, YP0)])        # avfasade kanter som glider i skenorna
    m = trimesh.creation.extrude_polygon(prof, PZ1 - PZ0)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, PZ0], [0, 0, 0, 1]], float))
    # extrude_polygon lägger profilen i (x, y) och drar ut längs z: rätt direkt
    adds, cuts = [], []
    for c in COMPONENTS:
        x0, z0 = c['pos']
        for dx, dz in c['holes']:
            s, h = standoff(x0 + dx, z0 + dz, c['standoff'], c['ins']); adds.append(s); cuts.append(h)
    a, cu = keystone_shelf(); adds += a; cuts += cu
    adds.append(cradle(SERVO_PSU)); adds.append(cradle(WAGO, 3.0))
    for x, z in TIE_SLOTS:
        for dx in (-3.5, 3.5):
            cuts.append(box(x + dx - 1.0, x + dx + 1.0, YP0 - 6, YP1 + 1, z - 2.5, z + 2.5))
    for poly in WINDOWS:
        cuts.append(ext_xz(poly, YP0 - 1, YP1 + 1))
    m = U([m] + adds)
    m = I(m, ext_xz(outline_xz(TC + 0.6, z0=PZ0 - 1, z1=Z_TOP - TC - 0.6), YP0 - 40, YB0))     # avfasade övre hörn som kåpan
    return clean(D(m, cuts))

def ghosts():
    """Komponenterna som enkla lådor framför plattan, för bilder och kontroll av plats (inte för utskrift)."""
    g = {}
    x0, z0 = PI['pos']; w, h = PI['size']
    g['pi5'] = U([box(x0, x0 + w, YP0 - 5.6, YP0 - 4.0, z0, z0 + h),                       # kortet
                  box(x0 + 2, x0 + w - 2, YP0 - 5.6 - 17.0, YP0 - 5.6, z0 - 3.0, z0 + 21.0),     # USB- och nätverksuttagen (ca 17 mm höga)
                  box(x0 + 7, x0 + 49.5, YP0 - 5.6 - 13.7, YP0 - 5.6, z0 + 22, z0 + 85 - 0.5)])  # Active Cooler (63,5 × 42,5 × 13,7)
    g['pi5_natverkskontakt'] = box(x0 + 2.0, x0 + 18.5, YP0 - 5.6 - 15.0, YP0 - 5.6 - 1.0, z0 - 25.0, z0 - 3.0)   # nätverkskabelns kontakt nedåt
    g['pi5_usbc'] = box(x0 - 22.0, x0, YP0 - 5.6 - 6.0, YP0 - 5.6, z0 + 85 - 11.2 - 4.5, z0 + 85 - 11.2 + 4.5)
    x0, z0 = PCA['pos']; w, h = PCA['size']
    g['pca9685'] = U([box(x0, x0 + w, YP0 - 5.6, YP0 - 4.0, z0, z0 + h), box(x0 + 4, x0 + w - 4, YP0 - 4 - 18.0, YP0 - 5.6, z0, z0 + 9.0),
                      box(x0 + 22, x0 + 40, YP0 - 4 - 10.1, YP0 - 5.6, z0 + h - 8, z0 + h)])
    kc = trimesh.creation.cylinder(radius=5.0, height=16.0, sections=32); kc.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])); kc.apply_translation([x0 + 11.0, YP0 - 5.6 - 5.0, z0 + 19.0]); g['kondensator'] = kc   # 1000 µF liggande på kortet
    x0, z0 = EKM['pos']; w, h = EKM['size']
    g['ekm006'] = box(x0, x0 + w, YP0 - 4 - 1.6 - 10.0, YP0 - 4.0, z0, z0 + h)
    r = SERVO_PSU; zc = (r['z0'] + r['z1']) / 2; g['servoomvandlare'] = U([box(r['x0'] + 7.5, r['x1'] - 7.5, YP0 - 23.0, YP0, zc - 13.5, zc + 13.5),
                                           box(r['x0'] + 2.5, r['x1'] - 2.5, YP0 - 2.5, YP0, zc - 6.0, zc + 6.0)])
    r = WAGO; g['wago'] = U([box(r['x0'] + 3, r['x0'] + 21.5, YP0 - 13.5, YP0, r['z0'] + 3, r['z0'] + 23.5), box(r['x0'] + 23, r['x0'] + 41.5 - 4, YP0 - 13.5, YP0, r['z0'] + 3, r['z0'] + 23.5)])
    g['dcjack'] = box(-45.0, -22.0, YP0 - 13.0, YP0, 149.0, 162.0)                   # DC-jack med skruvplint (ungefär)
    for i, xc in enumerate(KEY['xs']):
        yc = YP0 - 11.75
        g['keystone%d' % (i + 1)] = U([box(xc - 8.4, xc + 8.4, yc - 9.6, yc + 9.6, KEY['z'] + 2.4, KEY['z'] + 30.0), box(xc - 7.2, xc + 7.2, yc - 8.0, yc + 8.0, KEY['z'] - 2.0, KEY['z'] + 2.4)])
        g['rj45_%d' % (i + 1)] = box(xc - 5.9, xc + 5.9, yc - 7.0, yc + 7.0, KEY['z'] - 24.0, KEY['z'] - 2.0)
    return g

def packning():
    """17 TPU-packning mellan bakstycket och husets bakvägg (1,2 mm), med de fyra skruvhålen."""
    m = ext_xz(outline_xz(1.0, z0=Z_BOT + 1.0, z1=Z_TOP - 1.0), Y_BACK, Y_BACK + 1.2)
    return clean(D(m, [cyl_y(x, z, Y_BACK - 1, Y_BACK + 2.2, 1.8, 24) for x, z in HOUSE_SCREWS]))

def rx(m, deg):
    m = m.copy(); m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(deg), [1, 0, 0]))
    b = m.bounds; m.apply_translation([-(b[0][0] + b[1][0]) / 2, -(b[0][1] + b[1][1]) / 2, -b[0][2]]); return m

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "asm"), exist_ok=True); os.makedirs(os.path.join(OUT, "spoken"), exist_ok=True)
    parts = {'elbakstycke': bakstycke(), 'elkapa': kapa(), 'komponentplatta': platta(), 'elpackning': packning()}
    os.makedirs(os.path.join(OUT, "print"), exist_ok=True)
    for n, m, deg in (('16_elbakstycke', parts['elbakstycke'], 0), ('16b_elkapa', parts['elkapa'], 90), ('24_komponentplatta', parts['komponentplatta'], -90), ('17_elpackning', parts['elpackning'], -90)):
        rx(m, deg).export(os.path.join(OUT, "print", n + ".stl"))
    for n, m in parts.items():
        m.export(os.path.join(OUT, "asm", n + ".stl"))
        print("%-16s mått %s  volym %.1f cm3  tät %s  kroppar %d" % (n, np.round(m.extents, 1), m.volume / 1000, m.is_watertight, len(m.split(only_watertight=False))))
    for n, m in ghosts().items(): m.export(os.path.join(OUT, "spoken", n + ".stl"))
