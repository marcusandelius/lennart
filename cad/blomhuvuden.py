"""
Blomhuvuden för blomlådorna: tar bort de lösa flisorna (under 1 mm³, 0,1-0,3 mm tjocka) som
inte går att skriva ut och bara blir trådar eller klumpar. Kvar blir kronbladen (1,9 mm) och den
stjärnformade mitten (2,85 mm) i motsatt färg. Hålen för stjälkarna (Ø3,3 med fas) behålls.
Kör:  python3 blomhuvuden.py <rod.stl> <vit.stl>     (skriver över filerna)
"""
import sys
import numpy as np
import trimesh

for f in sys.argv[1:3]:
    m = trimesh.load(f)
    parts = m.split(only_watertight=False)
    keep = [b for b in parts if abs(b.volume) > 1.0]
    out = trimesh.util.concatenate(keep)
    assert out.is_watertight
    out.export(f)
    print(f, "behöll", len(keep), "av", len(parts), "delar; borttaget", round(sum(abs(b.volume) for b in parts if abs(b.volume) <= 1.0), 2), "mm³")
