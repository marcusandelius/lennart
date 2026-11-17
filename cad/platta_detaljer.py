"""
Lägger detaljerna för nattplattan på egna platser, så att inget överlappar om alla filer laddas in samtidigt.
Delar i två färger (skorsten, solskydd, blomhuvuden) flyttas tillsammans och ligger kvar i varandra.
Kör:  python3 platta_detaljer.py <katalog>
"""
import sys, os, itertools
import trimesh

D = sys.argv[1]
# grupp: filer, (x0, y0) där gruppens nedre vänstra hörn hamnar
GROUPS = [
    (["21_blomlador_vit.stl"], (-100, -100)),
    (["21_blomlador_vaxter_gron.stl"], (-20, -100)),
    (["06c_skorsten_rod.stl", "06c_skorsten_vit.stl"], (25, -100)),
    (["21b_blomhuvuden_rod.stl", "21b_blomhuvuden_vit.stl"], (-100, -45)),
    (["05c_solskydd_gra.stl", "05c_solskydd_vit.stl"], (-35, -45)),
    (["05b_fonsterinsatser_gra.stl"], (-100, 5)),
]
boxes = {}
for files, (x0, y0) in GROUPS:
    ms = [trimesh.load(os.path.join(D, f)) for f in files]
    b = trimesh.util.concatenate(ms).bounds
    for f, m in zip(files, ms):
        m.apply_translation([x0 - b[0][0], y0 - b[0][1], 0])
        m.export(os.path.join(D, f))
    boxes[files[0]] = trimesh.util.concatenate(ms).bounds
    print(", ".join(files), "->", boxes[files[0]][:, :2].round(1).tolist())
for (a, ba), (b, bb) in itertools.combinations(boxes.items(), 2):
    assert (ba[1][:2] < bb[0][:2]).any() or (bb[1][:2] < ba[0][:2]).any(), (a, b)
print("inga grupper överlappar")
