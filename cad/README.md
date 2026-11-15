# Huskroppen, version 8: magnetfästen för 6 × 3 mm

Ändrat från version 7 (artefakten "Lennarts matstation – 3D-modell"):

- Magnethålen i kroppen är nu Ø6,0 × 4,0 mm med 0,3 mm infasning (förut Ø9,9 × 3,3 för 10 × 2 mm). 6,0 valdes efter provstycket: tät presspassning.
- Tre magnetklackar per långsida i stället för två. De yttre sitter kvar på samma ställe,
  mittklacken är ny (mitt på väggen). Hålen är fortfarande vinkelräta mot takfallet.
- Inget annat i kroppen är ändrat.

| Fil | Vad |
|---|---|
| `05_kropp_rod.stl` | Kroppen, röd (ändrad) |
| `05_kropp_sockel_gra.stl` | Stengrunden, grå (oförändrad, skrivs ut ihop med kroppen) |
| `06_tak_vanster_gra.stl`, `06b_tak_hoger_gra.stl` | Takhalvorna (ändrade): tre hål Ø6,0 × 4,0 mm per halva vid y = −45 / 0 / +45, minustecken vid det nya hålet. De vita delarna (`06_tak_*_vit.stl`) är oförändrade |
| `00b_magnettest_6x3.stl` | Provstycke 53 × 11 × 11 mm med fem hål 5,8 / 5,9 / 6,0 / 6,1 / 6,2 mm (1–5 prickar) |
| `magnetfasten_kropp.py` | Skriptet som gör ändringen. `python3 magnetfasten_kropp.py in.stl ut.stl 6.0` ger annan håldiameter |
| `magnetfasten_tak.py` | Skriptet som ändrar takhalvorna (samma diameterargument) |
| `magnettest.py` | Skriptet för provstycket |

Takets hål ligger mitt över kroppens hål när huset är monterat (kontrollerat mot 3D-modellens montering, avvikelse ca 0,1 mm i sidled).
