"""
Bygger om magnetfästena i huskroppen (05_kropp_rod.stl) för magneter 6 x 3 mm.

Utgångsläge (version 7): fyra snedställda klackar ovanpå långsidorna, två per sida,
med Ø9,9 x 3,3 mm hål vinkelräta mot takfallet (för 10 x 2 mm magneter).

Ändring:
  * de gamla klackarna tas bort och byggs om med exakt samma profil
  * en tredje klack läggs till mitt på varje långsida (y = 75 mm i husets koordinater)
  * hålen blir Ø6,0 x 4,0 mm med 0,3 mm infasning, samma centrum som förut
    (så att takets befintliga hålpositioner fortfarande stämmer för de yttre paren)

Kör:  python3 magnetfasten_kropp.py <in.stl> <ut.stl> [hålets diameter]
"""
import sys
import numpy as np
import trimesh
from trimesh.creation import cylinder, cone, extrude_polygon
from shapely.geometry import Polygon

SRC, DST = sys.argv[1], sys.argv[2]
HOLE_D = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0   # magnet Ø6; provstycket visade att 6,0 ger tät presspassning
HOLE_DEPTH = 4.0      # magnet 3 mm + 1 mm att trycka djupare (justerar hur hårt taket sitter)
CHAMFER = 0.3         # infasning i hålets mynning
CUP_WALL = 1.2        # gods runt hålets botten där det sticker ut bakom klacken
CORBEL_W = 14.0       # klackens bredd längs väggen
Y_OFF = 70.0713       # STL-y = husets y - Y_OFF
CENTERS_Y = [30.0 - Y_OFF, 75.0 - Y_OFF, 120.0 - Y_OFF]   # tre per sida

# Takfallets lutning och klackens referenspunkt (uppmätt i version 7)
P0 = np.array([82.4, 162.15])                 # (x, z) nedre kanten på klackens snedyta
SLOPE_TOP = np.array([74.0, 170.05])          # (x, z) övre kanten
t = SLOPE_TOP - P0; t /= np.linalg.norm(t)    # uppåt längs takfallet, i xz
nrm = np.array([-t[1], t[0]]) * -1            # normal ut från snedytan
if nrm[1] < 0: nrm = -nrm
HOLE_U = 6.04                                 # hålcentrum längs snedytan från P0 (oförändrat)

body = trimesh.load(SRC)
assert body.is_watertight


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return b


def frame(side, yc):
    """Matris som tar lokala koordinater (u längs fallet, v längs väggen, w = normal) till STL."""
    tx, tz = t; nx, nz = nrm
    s = side
    origin = np.array([s * P0[0], yc, P0[1]])
    U = np.array([s * tx, 0, tz]); V = np.array([0, 1, 0]); W = np.array([s * nx, 0, nz])
    M = np.eye(4); M[:3, 0] = U; M[:3, 1] = V; M[:3, 2] = W; M[:3, 3] = origin
    return M


def corbel(side, yc):
    # profil i (x, z) för höger sida, samma som original + 0,1 mm överlapp in i väggen
    prof = [(82.5, 139.5), (74.0, 148.0), (74.0, 170.05), (82.4, 162.15), (82.4, 160.0), (82.5, 160.0)]
    poly = Polygon(prof)
    m = extrude_polygon(poly, CORBEL_W)          # i (x, y=z_prof), extruderas längs z
    # rotera så att profilens y blir z och extruderingen blir y
    R = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)
    m.apply_transform(R)
    if m.volume < 0:
        m.invert()
    m.apply_translation([0, yc - CORBEL_W / 2, 0])
    if side < 0:
        m.apply_transform(np.diag([-1, 1, 1, 1]))   # trimesh rättar vridningen själv
    return m


def local_cyl(r, w0, w1, sections=64):
    c = cylinder(radius=r, height=w1 - w0, sections=sections)
    c.apply_translation([HOLE_U, 0, (w0 + w1) / 2])
    return c


def cup(side, yc):
    c = local_cyl(HOLE_D / 2 + CUP_WALL, -(HOLE_DEPTH + CUP_WALL), -0.01)
    c.apply_transform(frame(side, yc))
    return c


def hole(side, yc):
    r = HOLE_D / 2
    parts = [local_cyl(r, -HOLE_DEPTH, 1.0)]
    # infasning: kon med radie r+CHAMFER vid ytan
    k = cone(radius=r + CHAMFER + 1.0, height=r + CHAMFER + 1.0, sections=60)   # 45 grader
    k.apply_transform(np.diag([1, 1, -1, 1]))   # spetsen nedåt (trimesh rättar vridningen själv)
    k.apply_translation([HOLE_U, 0, 1.0])
    parts.append(k)
    h = trimesh.boolean.union(parts, engine="manifold")
    h.apply_transform(frame(side, yc))
    return h


# 1) ta bort gamla klackar (två per sida)
cut = []
for side in (1, -1):
    for yc in (30.0 - Y_OFF, 120.0 - Y_OFF):
        y0, y1 = yc - CORBEL_W / 2 - 0.05, yc + CORBEL_W / 2 + 0.05
        if side > 0:
            cut += [box(70.0, 81.8, y0, y1, 139.0, 173.0), box(81.8, 82.6, y0, y1, 160.0, 173.0)]
        else:
            cut += [box(-81.8, -70.0, y0, y1, 139.0, 173.0), box(-82.6, -81.8, y0, y1, 160.0, 173.0)]
body = trimesh.boolean.difference([body] + cut, engine="manifold")

# 2) nya klackar + kopp bakom hålet
add, holes = [], []
for side in (1, -1):
    for yc in CENTERS_Y:
        add += [corbel(side, yc), cup(side, yc)]
        holes.append(hole(side, yc))
body = trimesh.boolean.union([body] + add, engine="manifold")

# koppen får inte sticka upp ovanför takfallets plan: skär bort allt ovanför snedytan inom klackarna
clip = []
for side in (1, -1):
    for yc in CENTERS_Y:
        b = trimesh.creation.box(extents=[30, CORBEL_W + 2, 10])
        b.apply_translation([HOLE_U, 0, 5.0])        # w > 0 i lokala koordinater
        b.apply_transform(frame(side, yc))
        clip.append(b)
body = trimesh.boolean.difference([body] + clip + holes, engine="manifold")

assert body.is_watertight, "inte tät"
body.export(DST)
print("klart:", DST, "ytor:", len(body.faces), "volym cm3:", round(body.volume / 1000, 1))
for side in (1, -1):
    for yc in CENTERS_Y:
        c = frame(side, yc) @ np.array([HOLE_U, 0, 0, 1])
        print(f"  hål {'höger' if side>0 else 'vänster'} y_hus={yc+Y_OFF:.1f}: mynning (x,y,z)=({c[0]:.2f},{c[1]:.2f},{c[2]:.2f})")
