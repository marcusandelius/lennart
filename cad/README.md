# Huskroppen, version 9

## Version 9: lodräta insatshål för skärmklämman och kamerafästet

Insatshålen (Ruthex M3, Ø4,0 × 6,5 mm) för skärmklämman och kameran pekade vågrätt bakåt
och gick inte att nå med lödkolven. Nu är de lodräta och öppnar uppåt, så insatserna
pressas in uppifrån när taket är av.

- `05_kropp_rod.stl`: skärmklackarna sitter kvar (x = ±34, ovansida 112 mm), hålen är nu lodräta.
  Kameraklackarna är större (x = ±22, ovansida 175 mm, 14 mm ut från väggen) med lodräta hål.
- `19_skarmklamma.stl`: samma ram och lister, plus två vågräta flikar som vilar på klackarna.
  M3 × 10 uppifrån. Hålen är avlånga (2 mm), så klämman kan backas om skärmen är tjockare än väntat.
  Utskrift: som förut, ramen mot plattan. Flikarna står upp.
- `15_kamerafaste.stl`: ny kamerasläde. Camera Module 3 skruvas på fyra distanser (Ø2,2, M2 med mutter
  på baksidan). Flikarna har 5 mm långa spår: skjut fram släden tills linsen nästan nuddar fönstret
  och dra åt två M3 × 10. Utskrift: ramens baksida mot plattan, distanser och flikar uppåt.
  Antaganden att kontrollera: linsens mitt ligger mitt mellan kortets hålrader (som i förra fästet),
  och linsen sticker ut 7–12 mm från kortet.

## Version 8: magnetfästen för 6 × 3 mm

Ändrat från version 7 (artefakten "Lennarts matstation – 3D-modell"):

- Magnethålen i kroppen är nu Ø6,0 × 4,0 mm med 0,3 mm infasning (förut Ø9,9 × 3,3 för 10 × 2 mm). 6,0 valdes efter provstycket: tät presspassning.
- Tre magnetklackar per långsida i stället för två. De yttre sitter kvar på samma ställe,
  mittklacken är ny (mitt på väggen). Hålen är fortfarande vinkelräta mot takfallet.
- Inget annat i kroppen är ändrat.

| Fil | Vad |
|---|---|
| `05_kropp_rod.stl` | Kroppen, röd (version 9) |
| `05_kropp_sockel_gra.stl` | Stengrunden, grå (oförändrad, skrivs ut ihop med kroppen) |
| `06_tak_vanster_gra.stl`, `06b_tak_hoger_gra.stl` | Takhalvorna (ändrade): tre hål Ø6,0 × 4,0 mm per halva vid y = −45 / 0 / +45, minustecken vid det nya hålet. De vita delarna (`06_tak_*_vit.stl`) är oförändrade |
| `00b_magnettest_6x3.stl` | Provstycke 53 × 11 × 11 mm med fem hål 5,8 / 5,9 / 6,0 / 6,1 / 6,2 mm (1–5 prickar) |
| `magnetfasten_kropp.py` | Skriptet som gör ändringen. `python3 magnetfasten_kropp.py in.stl ut.stl 6.0` ger annan håldiameter |
| `magnetfasten_tak.py` | Skriptet som ändrar takhalvorna (samma diameterargument) |
| `magnettest.py` | Skriptet för provstycket |
| `insatsklackar.py` | Skriptet för version 9: klackar, skärmklämma och kamerasläde |

Takets hål ligger mitt över kroppens hål när huset är monterat (kontrollerat mot 3D-modellens montering, avvikelse ca 0,1 mm i sidled).
