"""
Takrännor med krokar (version 9.2).

Hullingarna på takrännornas flikar är för små för att skrivas ut, så rännorna fick inget fäste.
Här får varje ränna tre krokar, som riktiga takrännekrokar: en rem från rännan upp längs takfotens
lodräta ytterkant (x = ±113, z 133,65-143,89) och en krok som hakar över kanten och ligger an mot
takets ovansida. Flikarna i spåret på undersidan håller rännan i sidled, krokarna bär vikten.
Taket ändras inte.

Kör:  python3 takrannor_krokar.py <asm_takrannor.stl (monterat läge)> <utkatalog>
"""
import sys, os
import numpy as np
import trimesh
from trimesh.creation import extrude_polygon
from shapely.geometry import Polygon

SRC, OUT = sys.argv[1], sys.argv[2]
GAP = 0.3                     # spel mot taket
STRAP_T = 2.0                 # remmens tjocklek
HOOK_L, HOOK_T = 3.5, 2.0     # krokens längd längs takets ovansida och tjocklek
W = 6.0                       # krokens bredd (samma som flikarna)
TAB_Y = [-10.0, 75.0, 160.0]  # flikarnas lägen längs takfoten (husets y)
EAVE_X, EAVE_Z0, EAVE_Z1 = 113.0, 133.65, 143.89
TOP_DIR = np.array([-7.44, 6.11]) / np.hypot(7.44, 6.11)   # takets ovansida från ytterkanten och inåt (x, z)
NRM = np.array([TOP_DIR[1], -TOP_DIR[0]])                   # utåt-uppåt normal till ovansidan

U = lambda ms: trimesh.boolean.union(ms, engine="manifold")


def hook_profile():
    x0 = EAVE_X + GAP
    a = np.array([EAVE_X, EAVE_Z1]) + GAP * NRM            # krokens insida vid ytterkanten
    b = a + HOOK_L * TOP_DIR
    c = b + HOOK_T * NRM
    d = np.array([x0 + STRAP_T, a[1] + HOOK_T * NRM[1] + 0.6])
    return Polygon([(x0, 122.3), (x0 + STRAP_T, 122.3), tuple(d), tuple(c), tuple(b), tuple(a), (x0, a[1])])


def bracket(side, yc):
    m = extrude_polygon(hook_profile(), W)                 # (x, z) i planet, längs lokal z
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
    if m.volume < 0: m.invert()
    m.apply_translation([0, yc - W / 2, 0])
    if side < 0:
        m.apply_transform(np.diag([-1, 1, 1, 1]))
    return m


gutters = sorted(trimesh.load(SRC).split(), key=lambda c: c.bounds[0][0])   # vänster, höger
names = ["22_takranna_vanster_gra.stl", "22_takranna_hoger_gra.stl"]
done = []
for side, g, name in zip((-1, 1), gutters, names):
    new = U([g] + [bracket(side, y) for y in TAB_Y])
    assert new.is_watertight
    new.export(os.path.join(OUT, "asm_" + name))
    pr = new.copy(); pr.apply_translation([-(pr.bounds[0][0] + pr.bounds[1][0]) / 2, -(pr.bounds[0][1] + pr.bounds[1][1]) / 2, -pr.bounds[0][2]])
    pr.export(os.path.join(OUT, name)); done.append(pr)
    print(name, np.round(pr.extents, 1))
a, b = done[0].copy(), done[1].copy()
w = max(a.extents[0], b.extents[0]); gap = 12.0
a.apply_translation([-(w + gap) / 2, 0, 0]); b.apply_translation([(w + gap) / 2, 0, 0])
trimesh.util.concatenate([a, b]).export(os.path.join(OUT, "22_takrannor_ihop_gra.stl"))
print("ihop", np.round(trimesh.util.concatenate([a, b]).extents, 1))
