"""
Platta för doseringen: doserhus (10), doserhjul (11) och nötmagasin (14, med grepphål).
Alla tre i utskriftsläge och placerade på en 256 x 256-platta (plattans koordinater, 0-256),
fritt från remsan till vänster som bara vänster munstycke når (x < 20,5).
Kör:  python3 platta_dosering.py <katalog med 10/11/14> <utkatalog>
"""
import sys, os, itertools
import numpy as np
import trimesh

SRC, OUT = sys.argv[1:3]
PLACE = {                                   # filnamn: (x0, y0) för delens nedre vänstra hörn
    "14_notmagasin.stl": (30.0, 140.0),
    "10_doserhus.stl": (140.0, 140.0),
    "11_doserhjul.stl": (60.0, 55.0),
}
boxes = {}
for f, (x0, y0) in PLACE.items():
    m = trimesh.load(os.path.join(SRC, f))
    m.apply_translation([x0 - m.bounds[0][0], y0 - m.bounds[0][1], -m.bounds[0][2]])
    assert m.bounds[1][0] < 256 and m.bounds[1][1] < 256 and m.bounds[0][0] > 20.5
    m.export(os.path.join(OUT, f))
    boxes[f] = m.bounds
    print(f, np.round(m.bounds[:, :2], 1).tolist(), "höjd", round(m.bounds[1][2], 1))
for (a, ba), (b, bb) in itertools.combinations(boxes.items(), 2):
    assert (ba[1][:2] + 5 < bb[0][:2]).any() or (bb[1][:2] + 5 < ba[0][:2]).any(), (a, b)
print("inga delar närmare än 5 mm")
