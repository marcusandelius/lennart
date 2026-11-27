"""
Brevlådan vid farstukvisten (9.9): servohus för luckservot (MG90S) i form av en brevlåda.

Ersätter det gamla servohuset i 07_farstukvist_vit (för litet för MG90S) och stolphatten (09)
och dess packning (09b). Mått i husets koordinater (samma som 3D-vyn).

  * Luckans axel: y = -8, z = 32,2, längs x. Luckans högra ände är en fyrkanthylsa med ett
    Ø4,8 mm hål, 3 mm djupt (x 38,5-41,5). Servots axel trycks rakt in i hålet.
  * Brevlådan: x 40-74, y -30 till -2 (öppen baksida mot husväggen), z 0-46. Kabeln går genom
    hålet i husväggen bakom (x 52-54, z 28-32). 9.14: 6 mm bredare åt höger (var x 40-68), eftersom
    servot är längre längs axeln än vad 9.9 antog. Hörnlisten sticker bara ut 1,6 mm från väggen och
    lådan slutar 2 mm från väggen, så lådan går fritt framför den.
  * Väggen mot luckan har en slits, 9 mm bred och öppen uppåt, så att servots axel kan sänkas på
    plats. Luckan sätts på sist och följer servots axel, så ±1,7 mm fel i läget gör inget.
  * Servot (WS-MG90S, mått från användarens ritning: kropp 22,8 lång, 12 bred, 22,8 hög till
    ovansidan, örats undersida 16 över botten, 32 till hornets topp, öronhål 27,7 isär, öronen
    31,8 långa; axeln ca 6 mm från kortänden; axelns topp utan horn antas 30,8 över botten) skruvas
    med sina egna skruvar i servobrickan (26). Brickan sänks ner ovanifrån och skruvas med två
    M3 i insatser i en tvärvägg, genom förstorade hål (Ø6,5, ±1,7 mm). Tre varianter av brickan
    med servofickan 2 mm lägre (a), som ritat (b) och 2 mm högre (c).
  * Axelns topp hamnar 0,8 mm från botten i luckans hål (2,2 mm i hålet). Om servots axel är kortare
    än antaget läggs distansen (26d, 0,6 mm) mellan öronen och brickan, då går axeln 0,6 mm djupare
    (axeln når då 38,7, 0,2 mm från hålets botten).
  * Handtaget på dörren är en egen svart del (07_farstukvist_svart), tre färger i ett objekt.
  * Locket (09, 9.10): rundad båge med samma bredd och djup som lådan, sitter direkt på väggarna
    så att det ser ut som en del av brevlådan (som en Habo). Två läppar på sidornas insida styr
    det. Ingen packning. Öppet bak mot husväggen. Skrivs ut med framsidan mot plattan, utan stöd.
  * Framsidan: inramning (spår) längs sidor och båge, dörr, brevinkast under bågen.
Kör:  python3 brevlada.py <07_farstukvist_vit.stl med en tidigare brevlåda> <utkatalog>
(den gamla brevlådan är en egen kropp i filen och byts ut)
"""
import sys, os
import numpy as np
import trimesh
from shapely.geometry import Point, box as sbox

SRC_VIT, OUT = sys.argv[1:3]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
TO_STL = np.array([-12.4, 23.6, 0.0])         # husets ram -> 07-filens ram

AX_Y, AX_Z = -8.0, 32.2                       # luckans axel
X0, X1, Y0, Y1, ZT = 40.0, 74.0, -30.0, -2.0, 46.0
T = 2.0
S_W, S_L, S_SPL, S_HOLE = 12.2, 22.8, 6.0, 27.7
S_EAR, S_TOP, S_TIP, S_EARL = 16.0, 22.8, 30.8, 31.8   # från servots botten: örats undersida, ovansidan, axelns topp; öronens längd
X_TIP = 39.3                                  # axelns topp (luckans hål slutar 38,5)
X_BOT = X_TIP + S_TIP                         # servots botten, 70,1
X_TOP = X_BOT - S_TOP                         # servots ovansida
EAR = X_BOT - S_EAR                           # örats undersida = brickans framsida
CX0, CX1 = EAR, EAR + 3.0                     # servobrickan
BH0, BH1 = X_TOP + 0.8, EAR                   # tvärväggen, mellan servots ovansida och örat
INS = [(-22.3, 9.0), (-22.3, 38.0)]           # M3-insatser (y, z), i tvärväggens främre del
ADJ = 1.7                                     # justering med förstorade hål


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def xcyl(r, x0, x1, y, z, s=40):
    c = trimesh.creation.cylinder(radius=r, height=x1 - x0, sections=s)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])); c.apply_translation([(x0 + x1) / 2, y, z]); return c


def ycyl(r, y0, y1, x, z, s=40):
    c = trimesh.creation.cylinder(radius=r, height=y1 - y0, sections=s)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])); c.apply_translation([x, (y0 + y1) / 2, z]); return c


def ext_y(poly, y0, y1):
    m = trimesh.creation.extrude_polygon(poly, y1 - y0)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
    if m.volume < 0: m.invert()
    m.apply_translation([0, y0 - m.bounds[0][1], 0]); return m


XC = (X0 + X1) / 2

# ---------------- brevlådans kropp
body = D(box(X0, X1, Y0, Y1, 0, ZT), [box(X0 + T, X1 - T, Y0 + T, Y1 + 1, T, ZT + 1)])
body = D(body, [box(X0 - 1, X0 + T + 1, AX_Y - 4.5, AX_Y + 4.5, 27.5, ZT + 1)])          # slits för luckans hylsa
# tvärvägg (L-form): främre del med insatserna + låg list i botten, öppen uppåt och bakåt för servot
bh = U([box(BH0, BH1, Y0 + T - 0.01, -16.5, T - 0.01, ZT), box(BH0, BH1, Y0 + T - 0.01, Y1, T - 0.01, 6.0)])
bh = D(bh, [xcyl(2.0, BH0 - 1, BH1 + 1, y, z, 32) for y, z in INS])                     # hål för M3-insatser (Ø4)
body = U([body, bh])
# framsidan (y = -30), som en Habo-brevlåda: inramning (spår) längs sidor och båge, dörr,
# brevinkast precis under bågen, svart handtag
fr = Y0
GR_IN, GR_W, GR_D = 1.4, 0.6, 0.45            # inramningens spår: avstånd från kanten, bredd, djup
frame = U([box(X0 + GR_IN, X0 + GR_IN + GR_W, fr - 0.01, fr + GR_D, GR_IN, ZT + 0.01),
           box(X1 - GR_IN - GR_W, X1 - GR_IN, fr - 0.01, fr + GR_D, GR_IN, ZT + 0.01),
           box(X0 + GR_IN, X1 - GR_IN, fr - 0.01, fr + GR_D, GR_IN, GR_IN + GR_W)])
door = box(X0 + 3.6, X1 - 3.6, fr - 0.01, fr + 0.6, 4.0, 33.0)
door_in = box(X0 + 4.2, X1 - 4.2, fr - 0.1, fr + 0.7, 4.6, 32.4)
body = D(body, [frame, D(door, [door_in])])
slot = box(X0 + 4.0, X1 - 4.0, fr - 1.0, fr + 0.3, 36.8, 40.8)
lip = box(X0 + 3.6, X1 - 3.6, fr - 1.7, fr + 0.3, 40.8, 42.2)
lip_ch = trimesh.convex.convex_hull(np.vstack([box(X0 + 3.6, X1 - 3.6, fr - 1.7, fr, 40.8, 42.2).vertices,
                                               box(X0 + 3.6, X1 - 3.6, fr - 0.01, fr, 39.1, 39.11).vertices]))
# handtaget (svart): rund knopp med en tvärslå, sticker ut 1,6 mm, sitter 0,4 mm in i väggen
lock = U([ycyl(1.4, fr - 1.6, fr + 0.4, XC, 29.5, 32), box(XC - 2.8, XC + 2.8, fr - 1.4, fr + 0.4, 28.85, 30.15)])
body = D(U([body, slot, lip, lip_ch]), [lock])
# hörnlisten (x 73-, sticker ut till y -1,6): högra väggens bakkant dras in till y -2,6 där
PIL = box(72.5, X1 + 1, -2.6, 1.0, -1, ZT + 30)
body = D(body, [PIL])
assert body.is_watertight

# ---------------- locket: samma bredd och djup som lådan, sitter direkt på väggarna (z 46)
# Bågen fortsätter sidorna utan kjol. Två läppar på sidornas insida styr locket och skyddar mot stänk.
R_O = (X1 - X0) / 2
outer = sbox(X0, ZT, X1, ZT + 0.01).union(Point(XC, ZT).buffer(R_O, resolution=96)).intersection(sbox(X0, ZT, X1, ZT + R_O + 1))
hat = ext_y(outer, Y0, Y1)
inner = Point(XC, ZT).buffer(R_O - T, resolution=96).intersection(sbox(X0, ZT - 1, X1, ZT + R_O))
hat = D(hat, [ext_y(inner, Y0 + T, Y1 + 0.5)])                                             # ihåligt, öppet bak
arc = Point(XC, ZT).buffer(R_O - GR_IN, resolution=96).difference(Point(XC, ZT).buffer(R_O - GR_IN - GR_W, resolution=96)).intersection(sbox(X0, ZT - 0.01, X1, ZT + R_O))
hat = D(hat, [ext_y(arc, Y0 - 0.01, Y0 + GR_D)])                                           # inramningen fortsätter över bågen
CL, LT, LH = 0.12, 1.4, 4.0                    # läpparnas spel mot lådans väggar, tjocklek, höjd
# 9.11: läpparna sitter ihop med lockets sidovägg och framvägg (en förbindning ovanför z 46).
# I 9.10 hade de spel åt alla håll och satt inte fast i locket alls.
lips = []
for xa, xb, xc, xd in ((X0 + T + CL, X0 + T + CL + LT, X0 + T - 0.6, X0 + T + CL + LT),
                       (X1 - T - CL - LT, X1 - T - CL, X1 - T - CL - LT, X1 - T + 0.6)):
    lips.append(box(xa, xb, Y0 + T + CL, Y1 - 0.5, ZT - LH, ZT + 0.01))        # läppen ner i lådan
    lips.append(box(xc, xd, Y0 + T - 0.6, Y1 - 0.5, ZT, ZT + 2.5))              # förbindning in i lockets väggar
lips = U(lips)
hat = U([hat, lips])
hat = D(hat, [PIL])
assert hat.is_watertight and len(hat.split(only_watertight=False)) == 1, 'locket ska vara en enda kropp'


# ---------------- servobricka, tre varianter
def carrier(dz):
    c = box(CX0, CX1, -27.0, -2.5, 4.0, ZT - 0.5)
    z_lo = AX_Z - (S_L - S_SPL) + dz; z_hi = AX_Z + S_SPL + dz
    c = D(c, [box(CX0 - 1, CX1 + 1, AX_Y - S_W / 2 - 0.2, Y1 + 1, z_lo - 0.2, z_hi + 0.2)])
    zc = (z_lo + z_hi) / 2
    c = D(c, [xcyl(0.85, CX0 - 1, CX1 + 1, AX_Y, zc + s * S_HOLE / 2, 20) for s in (-1, 1)])     # servots skruvar
    c = D(c, [xcyl(1.6 + ADJ, CX0 - 1, CX1 + 1, y, z, 32) for y, z in INS])                     # M3, förstorade
    assert c.is_watertight
    return c


# ---------------- distans 0,6 mm mellan öronen och brickan (om axeln inte når tillräckligt långt in)
def shim(th=0.6):
    zc = AX_Z + S_SPL - S_L / 2
    box = lambda x0, x1, y0, y1, za, zb: globals()['box'](x0, x1, y0, y1, min(za, zb), max(za, zb))
    pads = [box(EAR - th, EAR, AX_Y - S_W / 2, AX_Y + S_W / 2, zc + s * (S_L / 2 + 0.3), zc + s * (S_EARL / 2)) for s in (-1, 1)]
    bar = box(EAR - th, EAR, -16.4, AX_Y - S_W / 2 - 0.3 + 0.01, zc - S_EARL / 2, zc + S_EARL / 2)
    legs = [box(EAR - th, EAR, -16.4, AX_Y - S_W / 2 + 0.5, zc + s * (S_L / 2 + 0.3), zc + s * (S_EARL / 2)) for s in (-1, 1)]
    sh = U(pads + legs + [bar])
    sh = D(sh, [xcyl(1.1, EAR - th - 1, EAR + 1, AX_Y, zc + s * S_HOLE / 2, 20) for s in (-1, 1)])
    assert sh.is_watertight and len(sh.split(only_watertight=False)) == 1
    return sh


# ---------------- 07_farstukvist_vit: gamla servohuset bort, brevlådan in
vit = trimesh.load(SRC_VIT)
parts = vit.split(only_watertight=False)
old = [p for p in parts if p.bounds[0][0] > 27.0 and p.bounds[1][0] > 50.0]
assert len(old) == 1, len(old)
keep = [p for p in parts if p is not old[0]]
b_stl = body.copy(); b_stl.apply_translation(TO_STL)
new_vit = U(keep + [b_stl])
assert new_vit.is_watertight
new_vit.export(os.path.join(OUT, "07_farstukvist_vit.stl"))
l_stl = lock.copy(); l_stl.apply_translation(TO_STL)
assert l_stl.is_watertight
l_stl.export(os.path.join(OUT, "07_farstukvist_svart.stl"))                   # handtaget, svart, samma ram

asm = os.path.join(OUT, "asm"); os.makedirs(asm, exist_ok=True)
for n, m in (("brevlada_kropp", body), ("brevlada_handtag", lock), ("brevlada_tak", hat), ("servobricka", carrier(0.0)), ("servodistans", shim())):
    m.export(os.path.join(asm, n + ".stl"))


def lay(m, R=None):
    m = m.copy()
    if R is not None: m.apply_transform(R)
    m.apply_translation([-(m.bounds[0][0] + m.bounds[1][0]) / 2, -(m.bounds[0][1] + m.bounds[1][1]) / 2, -m.bounds[0][2]])
    return m


Rx = lambda a: trimesh.transformations.rotation_matrix(np.radians(a), [1, 0, 0])
Ry = lambda a: trimesh.transformations.rotation_matrix(np.radians(a), [0, 1, 0])
lay(hat, Rx(90)).export(os.path.join(OUT, "09_brevlada_tak.stl"))               # framsidan mot plattan, öppen bak uppåt
for tag, dz in (("a_lagre", -2.0), ("b", 0.0), ("c_hogre", 2.0)):
    lay(carrier(dz), Ry(-90)).export(os.path.join(OUT, "26_servobricka_%s.stl" % tag))
lay(shim(), Ry(-90)).export(os.path.join(OUT, "26d_servodistans_0_6mm.stl"))
for f in sorted(os.listdir(OUT)):
    if f.endswith(".stl"):
        m = trimesh.load(os.path.join(OUT, f)); print(f, np.round(m.extents, 1), "tät", m.is_watertight)
