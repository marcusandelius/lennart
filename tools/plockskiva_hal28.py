# Plockskivan med hål Ø 28 mm i stället för Ø 25 mm och större skruvhål för servohornet (2026-11-27, Claude Code-session).
#
# Utgår från 11_plockskiva.stl i version 9 av förhandsgranskningen. Den filen tas fram med
# tools/extract_from_html.py och hamnar i mappen stl/. STL-filer läggs inte i repot.
#
# Användning: python3 tools/plockskiva_hal28.py stl/11_plockskiva.stl 11_plockskiva_hal28.stl
#
# Vad skriptet gör:
# - Hittar skivans nuvarande hål (Ø 25, mitt 28 mm från skivans mitt).
# - Skär ett nytt hål Ø 28 rakt igenom skivan, med mitten 27,5 mm från skivans mitt.
#   Mitten flyttas 0,5 mm inåt så att väggen mot skivans ytterkant blir 1,1 mm i stället för 0,6 mm.
# - Kontrollerar att hela det gamla hålet ryms i det nya, så att ingen del av hålet blir mindre.
# - Gör de fyra förborrade hålen för hornets skruvar (2 mm) större, Ø 1,0 → Ø 1,7, med en grund
#   avlastning Ø 2,6 × 0,5 mm överst så att undanträngd plast inte lyfter hornets armar.
# Allt annat (servohornets urtag, omrörarens hål) lämnas orört.
# Filen ligger kvar som den skrevs ut: omrörarsidan mot byggplattan.
import sys
import numpy as np
import trimesh
from manifold3d import Manifold, Mesh

NEW_D = 28.0          # nytt hål, diameter (mm)
NEW_R_CENTER = 27.5   # nya hålets mitt, avstånd från skivans mitt (mm)
PILOT_D = 1.7         # förborrade hål för hornets skruvar (2 mm). Förut 1,0. Blir ca 1,5–1,6 i utskriften [osäkert].
RELIEF_D, RELIEF_H = 2.6, 0.5   # avlastning överst i hålen, där undanträngd plast annars lyfter hornets arm

src, dst = sys.argv[1], sys.argv[2]
t = trimesh.load(src)
disc = Manifold(Mesh(vert_properties=np.asarray(t.vertices, np.float32),
                     tri_verts=np.asarray(t.faces, np.uint32)))
z0, z1 = t.bounds[0, 2], t.bounds[1, 2]

# hitta dagens hål: den rundade öppningen som ligger längst från mitten, halvvägs upp i skivan
holes = []
for p in disc.slice((z0 + z1) / 2).to_polygons():
    p = np.array(p); c = p.mean(0); r = np.linalg.norm(p - c, axis=1)
    if r.max() - r.min() < 0.1 and 10 < r.mean() < 20:
        holes.append((np.linalg.norm(c), c, r.mean()))
assert len(holes) == 1, f"hittade {len(holes)} hål, väntade ett"
dist, c_old, r_old = holes[0]
print(f"dagens hål: Ø {2*r_old:.1f} mm, {dist:.1f} mm från mitten")

direction = c_old / dist
c_new = direction * NEW_R_CENTER
cut = Manifold.cylinder(z1 - z0 + 2, NEW_D / 2, NEW_D / 2, 192).translate([c_new[0], c_new[1], z0 - 1])
new = disc - cut

# förborrade hål för hornets skruvar: små runda hål (Ø ca 1 mm). Mät var de börjar och slutar.
pilots = []
for p in disc.slice((z0 + z1) / 2).to_polygons():
    p = np.array(p); c = p.mean(0); r = np.linalg.norm(p - c, axis=1)
    if r.max() < 1.0 and r.max() - r.min() < 0.1:
        pilots.append(c)
assert len(pilots) == 4, f"hittade {len(pilots)} skruvhål, väntade fyra"
def has_pilot(c, z):
    return any(np.linalg.norm(np.array(q).mean(0) - c) < 0.3 and np.linalg.norm(np.array(q) - np.array(q).mean(0), axis=1).max() < 1.0
               for q in disc.slice(z).to_polygons())
zs = np.arange(z0 + 0.05, z1, 0.05)
inside = [z for z in zs if has_pilot(pilots[0], z)]
pz0, pz1 = min(inside), max(inside) + 0.05     # pz1 = hornurtagets golv
print(f"skruvhål: {len(pilots)} st, Ø 1,0, z {pz0:.1f}–{pz1:.1f}")
for c in pilots:
    new = new - Manifold.cylinder(pz1 - pz0 + 0.1, PILOT_D / 2, PILOT_D / 2, 48).translate([c[0], c[1], pz0 - 0.05])
    new = new - Manifold.cylinder(RELIEF_H + 0.1, RELIEF_D / 2, RELIEF_D / 2, 48).translate([c[0], c[1], pz1 - RELIEF_H])

old_hole = Manifold.cylinder(z1 - z0, r_old, r_old, 128).translate([c_old[0], c_old[1], z0])
outside = (old_hole - cut).volume()
assert outside < 1e-3, f"det gamla hålet sticker utanför det nya ({outside:.3f} mm³)"

m = new.to_mesh()
out = trimesh.Trimesh(np.array(m.vert_properties)[:, :3], np.array(m.tri_verts), process=True)
assert out.is_watertight
out.export(dst)
rim = np.linalg.norm(t.vertices[:, :2], axis=1).max() - (NEW_R_CENTER + NEW_D / 2)
print(f"nytt hål: Ø {NEW_D:.1f} mm, {NEW_R_CENTER:.1f} mm från mitten, vägg mot ytterkanten {rim:.1f} mm")
print(f"sparad: {dst} ({out.volume:.0f} mm³, förut {t.volume:.0f} mm³)")
