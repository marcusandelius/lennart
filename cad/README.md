# Huskroppen, version 8: magnetfästen för 6 × 3 mm

Ändrat från version 7 (artefakten "Lennarts matstation – 3D-modell"):

- Magnethålen i kroppen är nu Ø5,9 × 4,0 mm med 0,3 mm infasning (förut Ø9,9 × 3,3 för 10 × 2 mm).
- Tre magnetklackar per långsida i stället för två. De yttre sitter kvar på samma ställe,
  mittklacken är ny (mitt på väggen). Hålen är fortfarande vinkelräta mot takfallet.
- Inget annat i kroppen är ändrat.

| Fil | Vad |
|---|---|
| `05_kropp_rod.stl` | Kroppen, röd (ändrad) |
| `05_kropp_sockel_gra.stl` | Stengrunden, grå (oförändrad, skrivs ut ihop med kroppen) |
| `00b_magnettest_6x3.stl` | Provstycke med fem hål 5,8 / 5,9 / 6,0 / 6,1 / 6,2 mm (1–5 prickar) |
| `magnetfasten_kropp.py` | Skriptet som gör ändringen. `python3 magnetfasten_kropp.py in.stl ut.stl 6.0` ger annan håldiameter |
| `magnettest.py` | Skriptet för provstycket |

Taket (06, 06b) har fortfarande Ø9,9-hål på två ställen per halva och behöver samma ändring.
