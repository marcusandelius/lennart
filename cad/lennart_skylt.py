"""
LENNART-skylt (9.11): texten på farstukvistens skål som en egen skylt som skrivs ut liggande.

Bokstäverna satt som upphöjd vit text på skålens lodräta framsida och blev randiga när de skrevs
ut lager för lager. Nu:
  * Skylten: en röd platta (63 x 12,5 x 1,15 mm) med vita bokstäver (0,8 mm höga, samma form och
    läge som förut) och en smal vit ram. Skrivs ut liggande med texten uppåt, två färger.
  * Skålen (röd) får en 1,2 mm djup ficka i framsidan där skylten limmas in i jämnhöjd.
    Framväggen är 3 mm, så 1,8 mm finns kvar bakom.
  * Bokstäverna tas bort ur 07_farstukvist_vit.
Kör efter brevlada.py:
    python3 lennart_skylt.py <07_farstukvist_rod_original.stl> <brevlada/07_farstukvist_vit.stl> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh

ROD, VIT, OUT = sys.argv[1:4]
U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
FACE = -22.4                                  # skålens framsida (07-filens ram)
PX0, PX1, PZ0, PZ1, DEPTH = -44.0, 19.2, 5.6, 18.4, 1.2      # fickan
CLR, GLUE = 0.15, 0.05                        # spel runt skylten, limspalt bakom
RIM_W, RIM_H = 0.5, 0.5                       # vit ram


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


vit = trimesh.load(VIT)
parts = vit.split(only_watertight=False)
letters = [p for p in parts if p.bounds[1][1] < FACE + 0.4 and p.bounds[0][2] > PZ0 and p.bounds[1][2] < PZ1 and p.bounds[0][0] > PX0 and p.bounds[1][0] < PX1]
assert len(letters) == 7, len(letters)
rest = [p for p in parts if not any(p is q for q in letters)]
new_vit = trimesh.util.concatenate(rest)
assert new_vit.is_watertight
new_vit.export(os.path.join(OUT, "07_farstukvist_vit.stl"))

rod = trimesh.load(ROD)
rod = D(rod, [box(PX0, PX1, FACE - 1, FACE + DEPTH, PZ0, PZ1)])
assert rod.is_watertight
rod.export(os.path.join(OUT, "07_farstukvist_rod.stl"))

# skylten i skålens ram, sedan liggande
sx0, sx1, sz0, sz1 = PX0 + CLR, PX1 - CLR, PZ0 + CLR, PZ1 - CLR
plate = box(sx0, sx1, FACE, FACE + DEPTH - GLUE, sz0, sz1)
rim = D(box(sx0, sx1, FACE - RIM_H, FACE + 0.01, sz0, sz1), [box(sx0 + RIM_W, sx1 - RIM_W, FACE - RIM_H - 1, FACE + 1, sz0 + RIM_W, sz1 - RIM_W)])
white = U(letters + [rim])
plate = D(plate, [white])                                                    # inget överlapp mellan färgerna
R = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])          # framsidan uppåt, texten läsbar ovanifrån
for m in (plate, white): m.apply_transform(R)
lo = plate.bounds[0].copy(); c = (plate.bounds[0] + plate.bounds[1]) / 2
for m in (plate, white): m.apply_translation([-c[0], -c[1], -lo[2]])
assert plate.is_watertight and white.is_watertight
plate.export(os.path.join(OUT, "07c_lennart_skylt_rod.stl"))
white.export(os.path.join(OUT, "07c_lennart_skylt_vit.stl"))
print("skylt", np.round(trimesh.util.concatenate([plate, white]).extents, 2), "ficka", PX1 - PX0, "x", PZ1 - PZ0, "x", DEPTH)
