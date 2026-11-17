"""
Takrännor 9.3 och stuprör.

Ändringar mot 9.2 (efter provbiten):
  * Rännan flyttas 5 mm utåt, så att taket bara sticker in över rännans innersta femtedel.
  * Två krokar i stället för tre, i de yttersta fickorna i takets spår (husets y = -10 och 160).
    Spåret är bara tillräckligt brett för fliken i fickorna.
  * Kroken över taket är dubbelt så lång (7 mm).
  * Varje krok är en hel bygel: rem utanför takfoten, krok över kanten, en arm under takfoten
    och den provade fliken upp i spåret. Rännan hänger i byglarna.
  * Stuprörets böj lutas lite mer, så att toppen följer rännans utlopp 5 mm utåt.

Kör:  python3 takrannor_v93.py <asm_takrannor_v7.stl> <stupror_v7.stl> <stupror_T.npy> <utkatalog>
Alla mått i husets koordinater (samma som 3D-vyn).
"""
import sys, os
import numpy as np
import trimesh
from trimesh.creation import extrude_polygon, cylinder
from shapely.geometry import Polygon

G_SRC, S_SRC, S_T, OUT = sys.argv[1:5]
SHIFT = 5.0
GAP, STRAP_T, HOOK_L, HOOK_T, W = 0.3, 2.0, 7.0, 2.0, 6.0
HOOK_Y = [-10.0, 160.0]
EAVE_X, EAVE_Z1 = 113.0, 143.89
TOP_DIR = np.array([-7.44, 6.11]) / np.hypot(7.44, 6.11)
NRM = np.array([TOP_DIR[1], -TOP_DIR[0]])
BOWL_C, BOWL_R = np.array([112.0 + SHIFT, 127.65]), 6.5
BAR_Z0, BAR_Z1 = 127.0, 131.0
# den provade flikens profil (x, z), från originalrännan, nu med arm i stället för rännkant under
TAB_BODY = [(105.3, BAR_Z0), (105.3, 138.3), (107.7, 138.3), (107.7, BAR_Z0)]          # 6 mm bred
TAB_TIP = [(105.3, 138.0), (105.3, 140.89), (105.7, 140.52), (105.7, 142.12), (107.3, 140.61),
           (107.3, 139.01), (107.4, 138.0)]                                                   # 4 mm bred, som originalet
TIP_W = 4.0

U = lambda ms: trimesh.boolean.union(ms, engine="manifold")
D = lambda a, bs: trimesh.boolean.difference([a] + bs, engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")


def ext(poly, yc, w=W):
    m = extrude_polygon(Polygon(poly), w)
    m.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
    if m.volume < 0: m.invert()
    m.apply_translation([0, yc - w / 2, 0]); return m


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b


def bracket(yc):
    x0 = EAVE_X + GAP
    a = np.array([EAVE_X, EAVE_Z1]) + GAP * NRM
    b = a + HOOK_L * TOP_DIR
    c = b + HOOK_T * NRM
    d = np.array([x0 + STRAP_T, a[1] + HOOK_T * NRM[1] + 0.6])
    strap_hook = ext([(x0, 120.0), (x0 + STRAP_T, 120.0), tuple(d), tuple(c), tuple(b), tuple(a), (x0, a[1])], yc)
    # remmen får inte sticka ut under rännans botten
    cyl = cylinder(radius=BOWL_R, height=W + 2, sections=96)
    cyl.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    cyl.apply_translation([BOWL_C[0], yc, BOWL_C[1]])
    below = D(box(100, 130, yc - W, yc + W, 100, BOWL_C[1]), [cyl])
    strap_hook = D(strap_hook, [below])
    bar = ext([(105.3, BAR_Z0), (x0 + STRAP_T, BAR_Z0), (x0 + STRAP_T, BAR_Z1), (105.3, BAR_Z1)], yc)
    tab = U([ext(TAB_BODY, yc), ext(TAB_TIP, yc, TIP_W)])
    return U([strap_hook, bar, tab])


# --- rännor
src = sorted(trimesh.load(G_SRC).split(), key=lambda c: c.bounds[0][0])
names = ["22_takranna_vanster_gra.stl", "22_takranna_hoger_gra.stl"]
asm = []
for side, g, name in zip((-1, 1), src, names):
    if side < 0: g = g.copy(); g.apply_transform(np.diag([-1, 1, 1, 1]))     # bygg som höger, spegla sedan
    clean = I(g, box(90, 140, -40, 190, 100, 127.66))                          # ta bort de gamla flikarna
    clean.apply_translation([SHIFT, 0, 0])
    new = U([clean] + [bracket(y) for y in HOOK_Y])
    if side < 0: new.apply_transform(np.diag([-1, 1, 1, 1]))
    assert new.is_watertight
    new.export(os.path.join(OUT, "asm_" + name)); asm.append(new)
both = trimesh.util.concatenate(asm); both.export(os.path.join(OUT, "asm_22_takrannor_gra.stl"))

# --- stuprör: böjen (z 95-114) lutas, toppen flyttas SHIFT utåt
st = trimesh.load(S_SRC); T = np.load(S_T); st.apply_transform(T)
v = st.vertices.copy()
k = np.clip((v[:, 2] - 95.0) / (114.0 - 95.0), 0, 1)
v[:, 0] += np.sign(v[:, 0]) * SHIFT * k
st.vertices = v
assert all(c.is_watertight for c in st.split())
st.export(os.path.join(OUT, "asm_23_stupror_gra.stl"))
back = st.copy(); back.apply_transform(np.linalg.inv(T)); back.export(os.path.join(OUT, "23_stupror_gra.stl"))
print("klart: rännor", np.round(both.bounds, 1).tolist(), "stuprör", np.round(st.bounds, 1).tolist())
