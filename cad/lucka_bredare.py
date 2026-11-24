"""
Luckan på LENNART-skålen (9.13): bredare så att den täcker hela lådan.

Förut var luckan 75 mm bred och skålen 82,4 mm, så man såg skålens röda överkant som en glipa på
3,7 mm på varje sida. Nu:
  * Vänster: luckan går ut till x -41,6, 0,4 mm utanför skålens vita kant, precis som framkanten
    redan gör. Förlängningen slutar 8,5 mm framför axeln så att den går fri från lagerklotsen när
    luckan öppnas.
  * Höger: luckan går ut till x 39,6, 0,4 mm från brevlådans vägg (x 40). Den grå plattan går ända fram till axelns hylsa.
  * Den vita gaveln flyttas ut till de nya kanterna och den vita framkanten förlängs.
  * Axel, hylsa och hål är oförändrade.
Husets ram: luckans axel ligger längs x vid y -8, z 32,2. Utskriftsfilerna ligger förskjutna (-2, 25,8, -28,2).
    python3 lucka_bredare.py <08_lucka_gra_original.stl> <08_lucka_vit_original.stl> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh
from shapely.geometry import box as sbox

GRA, VIT, OUT = sys.argv[1:4]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")
T = np.array([-2.0, 25.8, -28.2])             # hus -> utskrift
XL, XR = -41.6, 39.6                           # nya ytterkanter
CAP = 1.5                                      # gavelns tjocklek (som förut)
YL, YR, YRG = -16.5, -16.0, -12.3             # förlängningen slutar här: vänster fri från lagerklotsen, höger gavel som förut, grått fram till hylsan
YZ = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def profile(m, x, ymax):
    """Snittet i yz vid x, klippt till y < ymax."""
    pl, _ = m.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0]).to_2D(to_2D=YZ)
    return [p.intersection(sbox(-100, 0, ymax, 100)) for p in pl.polygons_full]


def extrude_x(polys, x0, x1):
    ms = []
    for p in polys:
        for q in getattr(p, "geoms", [p]):
            if q.area < 1e-3: continue
            e = trimesh.creation.extrude_polygon(q, x1 - x0)        # i (y, z), höjd längs +z
            e.apply_transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
            ms.append(e)
    return U(ms)


gra = trimesh.load(GRA); gra.apply_translation(-T)
vit = trimesh.load(VIT); vit.apply_translation(-T)
assert np.allclose(gra.bounds, [[-36, -46, 28.2], [41.5, -4, 36.2]], atol=0.01)

g_prof = lambda ymax: profile(gra, -30.0, ymax)              # plattan utan gavlar
gra2 = U([gra, extrude_x(g_prof(YL), XL + CAP, -35.9), extrude_x(g_prof(YR), 35.9, XR - CAP), extrude_x([p.intersection(sbox(YR - 0.01, 0, YRG, 100)) for p in g_prof(0)], 35.9, XR)])

front = profile(vit, 0.0, 0)                                  # den vita framkanten
cap = profile(vit, -36.75, 0)                                 # gaveln
vit_mid = I(vit, box(-36, 36, -60, 0, 0, 50))                # framkanten utan gamla gavlarna
vit2 = U([vit_mid, extrude_x(front, XL + CAP - 0.01, -35.99), extrude_x(front, 35.99, XR - CAP + 0.01),
          extrude_x([p.intersection(sbox(-100, 0, YL, 100)) for p in cap], XL, XL + CAP),
          extrude_x([p.intersection(sbox(-100, 0, YR, 100)) for p in cap], XR - CAP, XR)])
gra2 = D(gra2, [vit2])                                        # inget överlapp mellan färgerna
for m in (gra2, vit2):
    assert m.is_watertight
print("grå", np.round(gra2.bounds, 2).tolist(), "delar", len(gra2.split(only_watertight=False)))
print("vit", np.round(vit2.bounds, 2).tolist(), "delar", len(vit2.split(only_watertight=False)))
print("överlapp grå/vit", round(I(gra2, vit2).volume, 4))
os.makedirs(os.path.join(OUT, "asm"), exist_ok=True)
gra2.export(os.path.join(OUT, "asm", "lucka_gra.stl")); vit2.export(os.path.join(OUT, "asm", "lucka_vit.stl"))
for m, f in ((gra2, "08_lucka_gra.stl"), (vit2, "08_lucka_vit.stl")):
    m = m.copy(); m.apply_translation(T); m.export(os.path.join(OUT, f))
