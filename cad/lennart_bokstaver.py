"""
LENNART-bokstäver (9.12): texten på farstukvistens skål som lösa bokstäver som sätts dit efteråt.

Skålen ser ut exakt som förut (vita bokstäver 0,8 mm upphöjda direkt på den röda framsidan, ingen ram,
ingen ficka). Skillnaden är att bokstäverna inte skrivs ut stående med skålen (de blev randiga), utan:
  * 07c_lennart_bokstaver.stl: de sju bokstäverna, vita, liggande med framsidan mot plattan.
    Varje bokstav har två styrpinnar (Ø1,4 x 1,2 mm) på baksidan.
  * 07_farstukvist_rod.stl: skålen med två hål (Ø1,7 x 1,5 mm) per bokstav. Hålen ligger helt bakom
    bokstäverna och syns inte när de sitter på plats.
  * Bokstäverna tas bort ur 07_farstukvist_vit.
Kör efter brevlada.py:
    python3 lennart_bokstaver.py <07_farstukvist_rod_original.stl> <brevlada/07_farstukvist_vit.stl> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh
from shapely.ops import unary_union
from shapely.geometry import Point

ROD, VIT, OUT = sys.argv[1:4]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
FACE = -22.4                                  # skålens framsida (07-filens ram), bokstäverna sticker ut mot -y
PX0, PX1, PZ0, PZ1 = -44.0, 19.2, 5.6, 18.4   # textens område
PEG_R, PEG_L = 0.7, 1.2                       # styrpinne
HOLE_R, HOLE_D = 0.85, 1.5                    # hål i skålen (framväggen är 3 mm)
HIDE = 0.15                                   # minsta kant runt hålet bakom bokstaven
XZ = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])


def cyl_y(x, z, r, y0, y1):
    c = trimesh.creation.cylinder(radius=r, height=y1 - y0, sections=32)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    c.apply_translation([x, (y0 + y1) / 2, z]); return c


vit = trimesh.load(VIT)
parts = vit.split(only_watertight=False)
inbox = lambda p: (p.bounds[1][1] < FACE + 0.4 and p.bounds[0][2] > PZ0 and p.bounds[1][2] < PZ1
                   and p.bounds[0][0] > PX0 and p.bounds[1][0] < PX1)
letters = sorted([p for p in parts if inbox(p)], key=lambda p: p.bounds[0][0])
assert len(letters) == 7, len(letters)
rest = [p for p in parts if not inbox(p)]
new_vit = trimesh.util.concatenate(rest)
assert new_vit.is_watertight
new_vit.export(os.path.join(OUT, "07_farstukvist_vit.stl"))

# två pinnar per bokstav, så långt ifrån varandra som möjligt inom strecken
pegs, holes, out = [], [], []
for p in letters:
    s = p.section(plane_origin=[0, FACE - 0.3, 0], plane_normal=[0, 1, 0])
    pl, T = s.to_2D(to_2D=XZ)
    poly = unary_union(list(pl.polygons_full)).buffer(-(HOLE_R + HIDE))
    assert not poly.is_empty
    xs, zs = np.meshgrid(np.arange(poly.bounds[0], poly.bounds[2] + 0.01, 0.1), np.arange(poly.bounds[1], poly.bounds[3] + 0.01, 0.1))
    P = np.array([q for q in np.c_[xs.ravel(), zs.ravel()] if poly.contains(Point(q))])
    d = np.linalg.norm(P[:, None] - P[None], axis=2); i, j = np.unravel_index(d.argmax(), d.shape)
    pts = [P[i], P[j]]
    pts = [trimesh.transform_points([[a, b, 0]], T)[0] for a, b in pts]   # tillbaka till 3D (x, z)
    L = U([p] + [cyl_y(q[0], q[2], PEG_R, FACE - 0.05, FACE + PEG_L) for q in pts])
    assert L.is_watertight and len(L.split(only_watertight=False)) == 1
    out.append(L)
    holes += [cyl_y(q[0], q[2], HOLE_R, FACE - 1, FACE + HOLE_D) for q in pts]
    print("bokstav x %.1f..%.1f  pinnar %s  avstånd %.1f" % (p.bounds[0][0], p.bounds[1][0],
          [tuple(np.round([q[0], q[2]], 1)) for q in pts], d.max()))

rod = trimesh.load(ROD)
rod = D(rod, holes)
assert rod.is_watertight
rod.export(os.path.join(OUT, "07_farstukvist_rod.stl"))
for L in out:  # pinnarna får inte gå i skålen utanför hålen
    assert trimesh.boolean.intersection([L, rod], engine="manifold").volume < 1e-6

trimesh.util.concatenate(out).export(os.path.join(OUT, "asm", "lennart_bokstaver.stl"))  # monterat läge

# liggande med framsidan mot plattan (Rx +90: -y -> -z)
B = trimesh.util.concatenate(out)
B.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
c = (B.bounds[0] + B.bounds[1]) / 2; B.apply_translation([-c[0], -c[1], -B.bounds[0][2]])
B.export(os.path.join(OUT, "07c_lennart_bokstaver.stl"))
print("bokstäver", np.round(B.extents, 2), "kontaktyta", round(sum(f for f, n in zip(B.area_faces, B.face_normals) if n[2] < -0.99), 1), "mm²")
