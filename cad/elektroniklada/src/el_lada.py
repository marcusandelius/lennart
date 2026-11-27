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
def teardrop(x, z, r):                          # cirkel med 45°-spets uppåt, i (x, z)
    t = np.radians(np.linspace(45, -225, 49))
    pts = [(x + r * np.cos(a), z + r * np.sin(a)) for a in t] + [(x, z + r * np.sqrt(2))]
    return Polygon(pts)
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
TOWER = dict(x0=61.0, x1=XO - TC - 0.3, y0=125.0, y1=YP0 - 1.3, z0=146.0)   # torn för kåpans skruv: sitter på högra skenan, utanför plattans och kablarnas lyftväg
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
GLAND = (-42.0, 92.0)      # befintligt Ø16-hål i bakväggen: kabelförskruvning M16 för 12 V
GLAND_R = 13.0             # hål för förskruvningens mutter i bakstycket och packningen (Ø26)
CHAN_X = (-47.5, -36.5)    # kanal för strömkabeln: plattan har en slits öppen nedåt och inget sitter på plattan här under förskruvningen
PLATE_SLOT = (-54.0, -30.0, GLAND[1] + 13.0)   # slitsen i plattan runt förskruvningen (x0, x1, överkant), öppen nedåt: plats för gängan och muttern
CAB_SLOTS = [(-60.0, 12.0), (-42.0, 12.0), (-3.0, 12.0), (14.5, 16.0), (45.0, 30.0)]   # samma som det utskrivna bakstycket  # kabelöppningar i golvet: (mitt x, bredd): kontrollkablarna och servoomvandlaren, 12 V till EKM006, nätverk och kamerans flatkabel, GPIO-kabeln och fler kablar
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
    tp = Polygon([(t['x0'], t['y0']), (t['x1'], t['y0']), (t['x1'], t['y1']), (t['x0'] + 3.2, t['y1']), (t['x0'], t['y1'] - 3.2)])   # 45° baktill mot plattan: skrivs ut utan stöd
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
    cuts.append(cyl_z(TX, TY, Z_TOP - TC - 0.3 - INS_M25[1], Z_TOP, INS_M25[0], 32))   # M2,5-gänginsats för kåpans skruv
    cuts.append(ext_xz(teardrop(GLAND[0], GLAND[1], GLAND_R), YB0 - 1, Y_BACK + 1))   # förskruvningens mutter, droppformat (spets uppåt) så att hålet skrivs ut utan stöd
    for x in (-24.0, 26.0):                                                          # buntbandshål i golvet (för det som ligger under lådan)
        for y in (118.0, 138.5):
            cuts.append(box(x - 2.5, x + 2.5, y - 1.0, y + 1.0, Z_BOT - 1, ZF + 3))
    return clean(D(m, cuts))

# ---------------------------------------------------------------- 16b kåpa: framsida, sidor och tak, lyfts rakt upp
def kapa():
    outer = ext_xz(outline_xz(0.0, z0=ZF, z1=Z_TOP), Y_FRONT, YB0 - 0.2)
    inner = ext_xz(outline_xz(TC, z0=ZF - 1.0, z1=Z_TOP - TC), Y_FRONT + TC, YB0 + 1.0)
    m = D(outer, [inner])
    cuts = [cyl_z(TX, TY, Z_TOP - TC - 1, Z_TOP + 1, 1.45, 24)]       # M2,5 genom taket
    # ventilation högst upp framtill: väggen förtjockad inåt, springorna lutar 45 grader uppåt in mot lådan (vatten som rinner på utsidan kommer inte in)
    LB = dict(x0=-58.0, x1=48.0, y1=Y_FRONT + TC + 6.0, z0=152.0, z1=Z_TOP - TC)
    m = U([m, I(box(LB['x0'], LB['x1'], Y_FRONT + 0.5, LB['y1'], LB['z0'], LB['z1']), ext_xz(outline_xz(TC - 0.5, z0=ZF, z1=Z_TOP - TC + 0.5), Y_FRONT, YB0))])
    dep = LB['y1'] - Y_FRONT; zo = 155.0; hs = 2.5                                    # springans öppning utanpå (z zo..zo+hs), stiger dep mm in till insidan
    for xc in np.arange(LB['x0'] + 9.0, LB['x1'] - 6.0, 13.0):
        sl = ext_yz(Polygon([(Y_FRONT - 1.0, zo - 1.0), (Y_FRONT - 1.0, zo + hs - 1.0), (LB['y1'] + 1.0, zo + hs + dep + 1.0), (LB['y1'] + 1.0, zo + dep + 1.0)]), xc - 5.0, xc + 5.0)
        cuts.append(sl)
    for x0, x1, z1 in KAPA_FRONT_WIN:                                                # fönster framtill, öppna nedåt, med fasade kanter (1 mm) så att kablarna inte skavs
        poly = Polygon([(x0 - 1.0, Y_FRONT - 0.01), (x1 + 1.0, Y_FRONT - 0.01), (x1, Y_FRONT + 1.0), (x1 + 1.0, Y_FRONT + TC + 0.01), (x0 - 1.0, Y_FRONT + TC + 0.01), (x0, Y_FRONT + 1.0)])
        cuts.append(ext_xy(poly, ZF - 1, z1))
        cuts.append(box(x0 - 1.0, x1 + 1.0, Y_FRONT + 0.5, Y_FRONT + 1.5, z1 - 0.01, z1 + 1.0))   # droppkant: spår i fönstrets ovankant, vattnet släpper utanför
    for sd in (-1, 1):                                                               # ventilationsspringor i sidorna, sneda (stiger inåt) så att vatten som rinner längs sidan inte kommer in
        for zc in list(np.arange(130.0, 160.0, 6.0)) + list(np.arange(40.0, 64.0, 6.0)):
            xo, xi = sd * (XO + 1.0), sd * (XO - TC - 1.0)
            pts = [(xo, zc - 0.75 - 0.5), (xo, zc + 0.75 - 0.5), (xi, zc + 0.75 + 2.5), (xi, zc - 0.75 + 2.5)]
            cuts.append(ext_xz(Polygon(pts if sd > 0 else pts[::-1]).buffer(0), Y_FRONT + 7.0, YB0 - 6.0))
    # grepp på taket: en låg fena att nypa i när kåpan lyfts av (skrivs ut från framkanten och uppåt, utan stöd)
    fin = ext_yz(Polygon([(Y_FRONT, Z_TOP - 0.5), (Y_FRONT + 22.0, Z_TOP - 0.5), (Y_FRONT + 22.0, Z_TOP + 2.5), (Y_FRONT + 21.0, Z_TOP + 4.0), (Y_FRONT, Z_TOP + 4.0)]), -1.5, 1.5)
    dam = ext_yz(Polygon([(YB0 - 4.5, Z_TOP - 0.5), (YB0 - 2.0, Z_TOP - 0.5), (YB0 - 2.0, Z_TOP + 1.5), (YB0 - 2.5, Z_TOP + 1.5)]), -58.0, 58.0)   # låg vall på taket före skarven mot bakstycket: vatten leds åt sidorna, inte in i skarven
    gus = ext_xy(Polygon([(XO - TC + 0.01, Y_FRONT + TC - 0.01), (XO - TC - 2.4, Y_FRONT + TC - 0.01), (XO - TC + 0.01, Y_FRONT + TC + 7.0)]), ZF + 2.5, 144.0)   # förstyvning i högra innerhörnet (sidan hänger annars fritt bredvid GPIO-fönstret)
    rib = box(45.0, 47.0, Y_FRONT + TC - 0.01, Y_FRONT + TC + 2.0, ZF + 2.5, 66.0)          # ribba på insidan av remsan mellan fönstren
    # hakar i de främre hörnen nedtill: går över golvkanten och ned bakom den, så att sladdar inte kan trycka ut kåpans nederkant (framåt eller åt sidan)
    hooks = []
    xl_in = XO - TC - 0.3 - 1.6                  # golvkantens insida i x (66,1)
    yl_in = Y_FRONT + TC + 0.3 + 1.6             # golvkantens insida i y (114,9)
    zl = ZF + 2.0                                # golvkantens överkant (32,4)
    for sd in (-1, 1):
        xo, xi = sd * (XO - TC + 0.01), sd * (xl_in - 0.3 - 2.3)            # från sidoväggen in till benets insida
        body = box(min(xo, xi), max(xo, xi), Y_FRONT + TC - 0.01, yl_in + 4.0, zl + 0.6, zl + 3.6)          # över kanten
        leg = ext_yz(Polygon([(yl_in + 0.3, zl + 0.6), (yl_in + 4.0, zl + 0.6), (yl_in + 4.0, ZF + 0.2), (yl_in + 2.7, ZF + 0.2)]), min(sd * (xl_in - 0.3), xi), max(sd * (xl_in - 0.3), xi))   # ned bakom kanten, 45 grader fram (skrivs ut utan stöd)
        hooks += [body, leg]
    m = U([m, fin, dam, gus, rib] + hooks)
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
    hole = cyl_y(x, z, YP0 - h - 1, YP1 + 1.0, r_in, 24)        # genomgående: undanträngd plast kommer ut bakåt (1 mm luft bakom plattan)
    return s, hole
SO = 3.0                                                   # distanshöjd (kortens undersida 3 mm framför plattan)
PCB = YP0 - SO - 1.6                                       # kortens ovansida (y)
PLUG = 24.6                                                # kontakt + böjd kabel från kortets ovansida (uppmätt)
YPL = PCB - PLUG                                           # så långt fram kontakterna når (genom fönstren i kåpan)
PI = dict(name='pi5', pos=(3.5, 77.0), size=(56.0, 85.0), standoff=SO, ins='m25',
          holes=[(3.5, 23.5), (52.5, 23.5), (3.5, 81.5), (52.5, 81.5)])          # Pi 5 stående: USB/nätverk nedåt, GPIO till höger, USB-C till vänster, minneskortet uppåt
PCA = dict(name='pca9685', pos=(-18.7, 31.5), size=(62.23, 25.4), standoff=SO, ins='m2',
           holes=[(3.0, 3.1), (59.2, 3.1), (3.0, 22.4), (59.2, 22.4)])            # 56,2 x 19,3 mellan hålen: mitt emellan Adafruit (55,9 x 19,05) och uppmätt kopia (56,5 x 19,5); M2 i Ø3-hål med bricka tar upp resten. Liggande under Pi:n: kontrollkontakten åt höger (mot GPIO), servokontakterna längs överkanten, kanal 0 och 1 till höger, plinten nedtill
EKM = dict(name='ekm006', pos=(-60.0, 123.0), size=(60.0, 20.0), standoff=SO, ins='m2', rot=-10.0,
           holes=[(3.0, 3.0), (57.0, 3.0), (3.0, 17.0), (57.0, 17.0)])            # ovanför servoomvandlaren, vriden 10 grader medurs (vänster ände uppåt) och 5 mm högre: 12 V in till vänster, 5 V ut till höger (USB-C-kabeln till Pi:n)
COMPONENTS = [PI, PCA, EKM]
SERVO_PSU = dict(x0=-29.5, x1=2.0, z0=60.0, z1=116.0)    # stående vagga för servoomvandlaren (23 mm hög, 47–48 mm mellan öronens hål), buntband ovanför
TIE_SLOTS = [(-30.0, 158.0), (-13.75, 118.5), (-13.75, 60.0), (35.0, 64.0), (52.0, 64.0)]   # servoomvandlarens båda öron, kablarna vid servofönstret
WINDOWS = [sbox(14.0, 90.0, 52.0, 154.0).buffer(-3).buffer(3, 12)]   # bakom Pi:n: luft och mindre plast
# fönster i kåpan, öppna nedåt så att kåpan går att lyfta med allt inkopplat: (x0, x1, z1)
KAPA_FRONT_WIN = [(52.5, 64.5, 158.0),                    # framför Pi:ns GPIO-kontakter (förrådet rundar av här: 7–20 mm fritt framför)
                  (14.0, 40.0, 62.0)]                     # framför PCA9685:s kanal 0 och 1 och för kamerans flatkabel, nere till höger (3–30 mm fritt framför, även med förrådets lyftväg)
KAPA_SIDE_WIN = None

def cradle(r, h_wall=4.0):
    """Låga kanter runt en rektangel på plattan (håller en del som buntas fast)."""
    o = sbox(r['x0'], r['z0'], r['x1'], r['z1']); ring = o.difference(o.buffer(-2.0, join_style=2))
    gap = sbox((r['x0'] + r['x1']) / 2 - 8, r['z0'] - 1, (r['x0'] + r['x1']) / 2 + 8, r['z1'] + 1)   # öppningar mitt på kortsidorna för kablarna
    side_gap = sbox(r['x0'] - 1, (r['z0'] + r['z1']) / 2 - 6, r['x1'] + 1, (r['z0'] + r['z1']) / 2 + 6)
    ring = ring.difference(gap).difference(side_gap)
    return ext_xz(ring, YP0 - h_wall, YP0 + 0.5)

def platta():
    prof = Polygon([(-PX, YP1), (PX, YP1), (PX - TP, YP0), (-PX + TP, YP0)])        # avfasade kanter som glider i skenorna
    m = trimesh.creation.extrude_polygon(prof, PZ1 - PZ0)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, PZ0], [0, 0, 0, 1]], float))
    adds, cuts = [], []
    for c in COMPONENTS:
        x0, z0 = c['pos']; cx, cz = x0 + c['size'][0] / 2, z0 + c['size'][1] / 2; a = np.radians(c.get('rot', 0.0))
        for dx, dz in c['holes']:
            px, pz = x0 + dx - cx, z0 + dz - cz; px, pz = cx + px * np.cos(a) - pz * np.sin(a), cz + px * np.sin(a) + pz * np.cos(a)   # vridet moturs (sett framifrån)
            s, h = standoff(px, pz, c['standoff'], c['ins'], r_out=3.2); adds.append(s); cuts.append(h)
    for x, z in TIE_SLOTS:
        for dx in (-3.5, 3.5):
            cuts.append(box(x + dx - 1.0, x + dx + 1.0, YP0 - 6, YP1 + 1, z - 2.5, z + 2.5))
    for poly in WINDOWS:
        cuts.append(ext_xz(poly, YP0 - 1, YP1 + 1))
    sl = unary_union([sbox(PLATE_SLOT[0], PZ0 - 3, PLATE_SLOT[1], PLATE_SLOT[2]).buffer(-2.0).buffer(2.0, 16), sbox(PLATE_SLOT[0], PZ0 - 3, PLATE_SLOT[1], PLATE_SLOT[2] - 2.0)])
    cuts.append(ext_xz(sl, YP0 - 1, YP1 + 1))                                        # slits för förskruvningen och strömkabeln, öppen nedåt, rundade övre hörn (R2)
    cuts.append(cyl_y(-50.0, 158.0, YP0 - 1, YP1 + 1, 6.0, 48))                       # fingerhål att lyfta plattan i
    for sx, x_e in ((-1, -PX), (1, PX)):                                              # infasade nedre hörn som hittar in i skenorna
        cuts.append(ext_xz(Polygon([(x_e - sx * 3.0, PZ0 - 1), (x_e + sx * 1, PZ0 - 1), (x_e + sx * 1, PZ0 + 4.0)]), YP0 - 6, YP1 + 1))
    for x_e in (PLATE_SLOT[0], PLATE_SLOT[1]):                                        # och vid slitsens nedre öppning
        sx = 1 if x_e == PLATE_SLOT[0] else -1
        cuts.append(ext_xz(Polygon([(x_e + sx * 2.0, PZ0 - 1), (x_e - sx * 0.5, PZ0 - 1), (x_e - sx * 0.5, PZ0 + 2.5)]), YP0 - 6, YP1 + 1))
    adds.append(box(PLATE_SLOT[0] - 2.0, PLATE_SLOT[0], YP0 - 3.0, YP0 + 0.5, PZ0 + 3.0, PLATE_SLOT[2] + 8.0))   # ribba längs benets innerkant (benet bredvid slitsen)
    adds.append(cradle(SERVO_PSU))
    m = U([m] + adds)
    m = I(m, ext_xz(outline_xz(TC + 0.6, z0=PZ0 - 1, z1=Z_TOP - TC - 0.6), YP0 - 40, YB0))     # avfasade övre hörn som kåpan
    return clean(D(m, cuts))

def ghosts():
    """Komponenterna med kontakter och böjda kablar som enkla lådor (för bilder och kontroll av plats, inte för utskrift)."""
    g = {}
    x0, z0 = PI['pos']; w, h = PI['size']; z1 = z0 + h
    g['pi5'] = U([box(x0, x0 + w, PCB, PCB + 1.6, z0, z1),                                  # kortet
                  box(x0 + 2, x0 + w - 2, PCB - 17.0, PCB, z0 - 3.0, z0 + 21.0),           # USB- och nätverksuttagen
                  box(x0 + 20, x0 + 36, PCB + 1.6, PCB + 2.8, z1 - 1, z1 + 2.5)])          # minneskortet sticker ut uppåt
    g['pi5_gpio'] = box(x0 + w - 5.2, x0 + w + 0.2, YPL, PCB, z1 - 58.0, z1 - 6.0)          # Dupont-kontakterna på GPIO med böjda kablar
    # nätverksuttaget används inte (wifi); under det finns ca 17 mm fritt till PCA9685 för en vinklad kontakt med låg profil
    g['pi5_usbc'] = box(x0 - 40.0, x0, PCB - 7.0, PCB, z1 - 11.2 - 4.5, z1 - 11.2 + 4.5)    # USB-C med böjskydd, 40 mm åt vänster
    g['pi5_flatkabel'] = box(x0 + 3, x0 + 19, PCB - 15.0, PCB, z1 - 60.0, z1 - 42.0)       # kamerans flatkabel går upp 15 mm och böjer nedåt
    x0, z0 = PCA['pos']; w, h = PCA['size']; zt = z0 + h; x1 = x0 + w
    g['pca9685'] = U([box(x0, x1, PCB, PCB + 1.6, z0, zt),
                      box(x1 - 52.0, x1 - 9.0, PCB - 8.5, PCB, zt - 8.0, zt - 1.5),        # stiftlisterna längs överkanten
                      box(x1 - 16.0, x1 - 6.0, PCB - 16.0, PCB, z0 + 2.0, z0 + 12.0),      # stående kondensator på kortet
                      box(x1 - 36.2, x1 - 26.2, PCB - 10.0, PCB, z0, z0 + 8.0)])           # plinten
    g['pca9685_servokontakter'] = box(x1 - 15.0, x1 - 9.5, YPL, PCB, zt - 8.5, zt - 1.0)   # kanal 0 och 1 med böjda kablar (genom fönstret)
    g['pca9685_kontroll'] = U([box(x1, x1 + 14.0, PCB - 6.0, PCB + 1.6, z0 + 5.0, z0 + 20.5),
                               box(x1 + 14.0, x1 + 17.0, PCB - 6.0, PCB, z0 + 5.0, z0 + 40.0)])   # vinklade kontrollstift med Dupont-kontakter åt höger, kablarna upp mot GPIO
    x0, z0 = EKM['pos']; w, h = EKM['size']
    e = U([box(x0, x0 + w, PCB, PCB + 1.6, z0, z0 + h), box(x0 + 1, x0 + w - 1, PCB - 10.0, PCB, z0, z0 + h),
           box(x0 - 7.0, x0, PCB - 8.0, PCB, z0 + 4, z0 + h - 4), box(x0 + w, x0 + w + 2.0, PCB - 8.0, PCB, z0 + 4, z0 + h - 4)])   # plintar med ledare i båda ändar
    e.apply_transform(trimesh.transformations.rotation_matrix(-np.radians(EKM.get('rot', 0.0)), [0, 1, 0], [x0 + w / 2, 0, z0 + h / 2])); g['ekm006'] = e   # vriden moturs sett framifrån
    gx, gz = GLAND; c = (CHAN_X[0] + CHAN_X[1]) / 2
    g['stromkabel'] = U([cyl_y(gx, gz, 141.0, 146.8, 11.0, 6),                                         # förskruvningens mutter (nyckelvidd 19)
                         box(c - 4.5, c + 4.5, 117.0, 146.8, gz - 4.5, gz + 4.5),                    # kabeln rakt in
                         box(c - 4.5, c + 4.5, 117.0, 126.0, ZF - 2.0, gz + 4.5)])                   # och nedåt i kanalen, genom golvet
    r = SERVO_PSU; xc, zc = (r['x0'] + r['x1']) / 2, (r['z0'] + r['z1']) / 2
    g['servoomvandlare'] = U([box(xc - 13.5, xc + 13.5, YP0 - 23.0, YP0, zc - 19.0, zc + 19.0),
                              box(xc - 5.0, xc + 5.0, YP0 - 3.0, YP0, zc - 26.0, zc + 26.0),
                              box(xc - 4.0, xc + 4.0, YP0 - 16.0, YP0 - 4.0, zc - 29.5, zc + 29.5)])   # öron och ledare i båda ändar
    return g

def packning():
    """17 TPU-packning mellan bakstycket och husets bakvägg (1,2 mm), med de fyra skruvhålen."""
    m = ext_xz(outline_xz(1.0, z0=Z_BOT + 1.0, z1=Z_TOP - 1.0), Y_BACK, Y_BACK + 1.2)
    return clean(D(m, [cyl_y(x, z, Y_BACK - 1, Y_BACK + 2.2, 1.8, 24) for x, z in HOUSE_SCREWS] + [cyl_y(GLAND[0], GLAND[1], Y_BACK - 1, Y_BACK + 2.2, GLAND_R, 48)]))

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
