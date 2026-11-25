# Skärmficka för Waveshare Pico-LCD-2: ersätter skärmklämman (19_skarmklamma.stl).
# Ritad i Claude Code 2026-11-25 efter Marcus foton av kortet. Måtten på kortet är
# avlästa ur foton med tumstock och är osäkra (se docs/hardvara.md, avsnitt 3.6).
#
# Kortet skjuts ner ovanifrån mellan två sidoskenor och vilar på en hylla nedtill.
# En läpp nedtill och en regel upptill trycker kortet mot skärmramen. Regeln läggs
# i två spår i skenorna när kortet sitter på plats. Fickan skruvas fast i klackarna
# med samma två M3 som den gamla klämman.
#
# Utskrift: fickan stående som i huset (hyllan och skenornas underkant mot plattan).
# Då behöver bara de två flikarna stöd underifrån. Regeln skrivs ut som den ligger
# i huset, utan stöd.
#
# Användning (läser modellen ur förhandsgranskningen, se tools/extract_from_html.py):
#   python3 skarmficka.py parts_from_html.json [utmapp]
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

src = sys.argv[1] if len(sys.argv) > 1 else 'parts_from_html.json'
out = sys.argv[2] if len(sys.argv) > 2 else '.'
os.makedirs(out, exist_ok=True)
parts, P = load(src)

# ---------- husets mått (uppmätta i modellen, version 9) ----------
Y_RAM = 3.2           # skärmramens baksida = kortets framsida
ZC = 108.0            # mitt i skärmfönstret (ramen går z 88,5–127,5)
PIL_X = 30.0          # klackarnas insida (klackarna går x ±30–38, y 3,3–18)
PIL_TOP = 112.0       # klackarnas ovansida
HOLE = (34.0, 10.6)   # hål för M3-insats i klackarna (Ø4)

# ---------- kortets mått, ur foton 2026-11-25 [verifiera] ----------
KW, KH = 48.0, 32.0   # kortets bredd och höjd (46–50 × 31–33)
T_LCD, T_PCB = 3.6, 2.9   # displayen, kortet med glipa
Y_BACK = Y_RAM + T_LCD + T_PCB          # kortets baksida, ca 9,7
H_HDR = 12.0                            # hylsornas höjd över kortet
HDR_L, HDR_W = 50.8, 2.54               # 20 hål à 2,54 mm
HDR_Z = 17.78 / 2                       # Pico-raderna sitter 17,78 mm isär
BTN_X0, BTN_X1 = 15.0, 21.5             # knapparna i hörnen
BTN_IN, BTN_OUT, BTN_H = 2.7, 1.3, 3.5  # hur långt de når in över kortet, ut över kanten, och höjd

# ---------- fickans mått ----------
# Allt som sänks ner ovanifrån måste gå fritt förbi kamerafästets klackar ovanför skärmen
# (x ±18–26 med y ≤ 17,6, och kamerakragen x ±16 med y ≤ 5,4, z ca 151–183).
Y_FREE = 17.9         # bakom klackarna är det fritt över hela bredden
Y_COLLAR = 5.7        # bakom kamerakragen är det fritt för |x| < 16
GX0 = 26.3            # skenornas insida: förbi klackarna (x 26) och hylsorna (x 25,4)
GX1 = PIL_X - 0.3     # skenornas utsida, intill klackarna för skruvarna
Z_SHELF = ZC - KH / 2 # hyllans ovansida = kortets underkant
Z_BOT = Z_SHELF - 3.0
Z_TOP = 126.0
Y_LIP = Y_BACK + 0.5  # läppens och regelns tryckyta (skumtejp om kortet glappar)
LIP_X = 12.0          # läpp och regel trycker bara mitt på, mellan knapparna
SHELF_X = 14.4        # hyllan mitt under kortet, innanför knapparna
Z_HDR_LO = ZC - HDR_Z - HDR_W / 2       # nedre hylsradens underkant
Z_HDR_HI = ZC + HDR_Z + HDR_W / 2       # övre hylsradens överkant
GROOVE_Y = (Y_FREE + 0.2, Y_FREE + 2.8) # regelns spår i skenorna
Y_GUIDE = 23.5

def fickan():
    f = Manifold()
    for s in (1, -1):
        def bx(x0, x1, y0, y1, z0, z1):
            a, b = sorted((s * x0, s * x1)); return box(a, b, y0, y1, z0, z1)
        f += bx(GX0, GX1, Y_RAM + 0.1, Y_GUIDE, Z_BOT, Z_TOP)          # sidoskena
        f += bx(GX0, 38.0, 3.6, 18.0, PIL_TOP, PIL_TOP + 3.0)          # flik på klacken
        f -= cylz(s * HOLE[0], HOLE[1], PIL_TOP - 1, PIL_TOP + 4, 1.7) # M3
        f -= bx(GX0 - 0.1, GX0 + 2.2, GROOVE_Y[0] - 0.2, GROOVE_Y[1] + 0.2, Z_HDR_HI + 0.4, Z_TOP + 1)  # spår för regeln
        f += bx(SHELF_X - 0.1, GX0 + 0.1, Y_FREE, Y_GUIDE, Z_BOT, Z_SHELF)   # tvärslå bak, bakom knapparna
    f += box(-SHELF_X, SHELF_X, Y_COLLAR, Y_GUIDE, Z_BOT, Z_SHELF)      # hylla under kortet
    lip = box(-LIP_X, LIP_X, Y_LIP, Y_LIP + 4.0, Z_SHELF - 0.1, Z_HDR_LO - 0.6)
    zt = Z_HDR_LO - 0.6                                                # avfasning så att kortet glider in
    lip -= yz_prism([(Y_LIP - 0.1, zt - 1.5), (Y_LIP + 1.5, zt + 0.1), (Y_LIP - 0.1, zt + 0.1)], -LIP_X - 1, LIP_X + 1)
    return f + lip

def regeln():
    zb = Z_HDR_HI + 0.6
    r = box(-(GX0 + 2.0), GX0 + 2.0, GROOVE_Y[0], GROOVE_Y[1], zb, zb + 3.5)   # bom i spåren
    r += box(-LIP_X, LIP_X, Y_LIP, GROOVE_Y[1], zb, zb + 3.5)                   # tryckyta mitt på
    r += box(-4, 4, GROOVE_Y[0], GROOVE_Y[1], zb + 3.4, Z_TOP + 4)              # grepp
    return r

def kortet():
    k = box(-KW / 2, KW / 2, Y_RAM, Y_BACK, ZC - KH / 2, ZC + KH / 2)
    for s in (1, -1):
        k += box(-HDR_L / 2, HDR_L / 2, Y_BACK, Y_BACK + H_HDR, ZC + s * HDR_Z - HDR_W / 2, ZC + s * HDR_Z + HDR_W / 2)
        for sx in (1, -1):
            a, b = sorted((sx * BTN_X0, sx * BTN_X1))
            e = ZC + s * KH / 2
            z0, z1 = sorted((e - s * BTN_IN, e + s * BTN_OUT))
            k += box(a, b, Y_BACK, Y_BACK + BTN_H, z0, z1)
    return k

F, R, K = fickan(), regeln(), kortet()

# ---------- kontroller ----------
print('fickan', bb(F).tolist(), 'volym', round(F.volume()), 'mm3')
print('regeln', bb(R).tolist(), 'volym', round(R.volume()), 'mm3')
print('kortet + hylsor', bb(K).tolist())
print('krock fickan/kortet:', round((F ^ K).volume(), 2), ' regeln/kortet:', round((R ^ K).volume(), 2), ' fickan/regeln:', round((F ^ R).volume(), 2))
# kortet skjuts ner ovanifrån: svep det uppåt och se att inget tar emot
sweep = Manifold.batch_hull([K, K.translate([0, 0, 40])])
hdrs = Manifold()
for s in (1, -1):
    hdrs += box(-HDR_L / 2, HDR_L / 2, Y_BACK, Y_BACK + H_HDR, ZC + s * HDR_Z - HDR_W / 2, ZC + s * HDR_Z + HDR_W / 2 + 40)
print('krock när kortet skjuts ner (kanter):', round((F ^ (box(-KW/2, KW/2, Y_RAM, Y_BACK, ZC - KH/2, ZC + KH/2 + 40))).volume(), 2),
      ' (hylsor):', round((F ^ hdrs).volume(), 2))
skip = {'skarmklamma', 'skarmram'}
for p in parts:
    if p['name'] in skip: continue
    m = M(P, p['name'])
    for n, part in (('fickan', F), ('regeln', R), ('kortet', K)):
        v = (m ^ part).volume()
        if v > 0.01: print(f'krock {n}/{p["name"]}: {v:.2f} mm3')
mag = M(P, 'notmagasin') ^ box(-30, 30, 0, 60, Z_BOT, Z_TOP)
print('fritt djup bakom hylsorna till magasinet:', round(bb(mag)[0][1] - (Y_BACK + H_HDR), 1), 'mm')

toT(F).export(os.path.join(out, '19_skarmficka.stl'))
toT(R).export(os.path.join(out, '19b_skarmficka_regel.stl'))
toT(K).export(os.path.join(out, 'skarmkort_ungefar.stl'))
json.dump(dict(KW=KW, KH=KH, Y_BACK=Y_BACK, GX0=GX0, Z_SHELF=Z_SHELF, Y_LIP=Y_LIP), open(os.path.join(out, 'skarmficka.json'), 'w'))
# fickan sänks ner ovanifrån när taket är av: inget får ta emot på vägen
for n, part in (('fickan', F), ('regeln', R)):
    path = Manifold()
    for dz in range(1, 101, 1): path += part.translate([0, 0, dz])
    for p in parts:
        if p['name'] in skip | {'tak_v', 'tak_h', 'takpackning', 'kamerafaste', 'notmagasin'}: continue
        v = (M(P, p['name']) ^ path).volume()
        if v > 0.01: print(f'i vägen när {n} sänks ner: {p["name"]} {v:.2f} mm3')
print('klart')
