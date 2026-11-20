"""
Monteringsplatta (24) för snabbare utskrift.

Plattan syns inte, så bara funktionen är kvar:
  * Ytterkanten och tjockleken (3 mm) är oförändrade: plattan skjuts ner i spåret mellan lådans
    bakvägg och listerna (spåret är ca 4,25 mm, listerna griper ca 2,2 mm av kanten).
  * Stolparna för Pi 5 (Ø6, hål Ø2,2 för M2,5 direkt i plasten), hålraden överst och de två
    hålkolumnerna till höger för buntband och kabelöppningen är kvar.
  * Två fönster tas upp: under Pi:n (mellan stolparna) och mellan Pi:n och hålkolumnerna.
    Kvar blir en ram på minst 7 mm och minst 4 mm material runt stolpar och hål.
    Pi:n får dessutom luft underifrån.
Kör:  python3 monteringsplatta_snabb.py <24_monteringsplatta.stl> <ut.stl>
"""
import sys
import numpy as np
import trimesh
from shapely.geometry import box as sbox

SRC, DST = sys.argv[1:3]
R = 3.0                                    # rundade hörn i fönstren
WINDOWS = [(-46.0, -37.7, -4.0, 19.6),     # under Pi:n, mellan stolparna (x -54,5 och 3,5)
           (10.5, -37.7, 34.0, 19.6)]      # mellan Pi:ns högra stolpar och hålkolumnen x = 40

m = trimesh.load(SRC)
cuts = []
for x0, y0, x1, y1 in WINDOWS:
    poly = sbox(x0 + R, y0 + R, x1 - R, y1 - R).buffer(R, resolution=12)
    c = trimesh.creation.extrude_polygon(poly, 5.0); c.apply_translation([0, 0, -1.0])
    cuts.append(c)
out = trimesh.boolean.difference([m] + cuts, engine="manifold")
assert out.is_watertight
out.export(DST)
print("volym %.1f -> %.1f cm3 (%.0f %% mindre)" % (m.volume / 1000, out.volume / 1000, 100 * (1 - out.volume / m.volume)))
