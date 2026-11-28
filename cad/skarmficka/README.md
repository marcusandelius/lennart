# Skärmfickan (ersätter 19_skarmklamma.stl)

Ritad i en annan dialog 2026-11-25, skriptet ligger på grenen `claude/serene-ride-2s73q0` som `model/skarmficka.py`
(måtten på kortet och motiveringen i `docs/hardvara.md` avsnitt 3.6 och `docs/beslut/beslutslogg.md` på samma gren).
Filerna här är skapade med det skriptet mot husmodellen i förhandsgranskningen.

## Version 9.22 (2026-11-28), efter provmontering
`skarmficka_v2.py` (kör: `python3 skarmficka_v2.py <parts_from_html.json> <utmapp>`, `lib.py` bredvid) ritar om fickan:
* Kortet sitter **3 mm åt höger** (sett utifrån, +x) och **5 mm lägre** (mitten z 103 i stället för 108).
  Flikarna och M3-hålen sitter kvar på klackarna.
* Höger skena går bara bakom och ovanför höger klack. Vänster skena står kvar utanför kamerafästets klackar
  (så att fickan kan sänkas ner) och en styrlist bakom dem håller hylsorna. Kortet styrs i sidled av hylsorna
  mot listerna på båda sidor (0,9 mm spel).
* Regelns tryckyta är **2,5 mm närmare skärmen**. Läppen nedtill är oförändrad.
* Bakre underkanten är avfasad 45 grader så att fickan går fri från skivkåpan (0,6 mm).
* Kontroller: inga krockar med huset eller doseringen, fickan och regeln går fritt ner ovanifrån.
  Kortmodellen är ungefärlig (tjockleken osäker), därför överlappar regeln den i modellen.
* Utskrift som förut: fickan stående med stöd under de två flikarna, regeln som den ligger utan stöd.

| Fil | Del |
|---|---|
| 19_skarmficka.stl | Fickan, stående som den sitter i huset (stöd bara under de två flikarna) |
| 19b_skarmficka_regel.stl | Regeln, som den ligger i huset (utan stöd) |
| asm/*.stl | Fickan, regeln och skärmkortet (ungefärligt, med Pico-hylsorna) i husets ram |

## Kontroll mot doseringen (`../plockskiva/sim/fickchk.py`)
* Inget överlapp mellan fickan, regeln eller kortet och doseringsdelarna. Minsta avstånd: skivkåpan 2,7 mm, stativet
  4,0 mm, förrådet 6,0 mm (fickan) och 7,8 mm (kortets hylsor).
* Fickan, regeln och kortet går fritt ned förbi doseringen. Kamerasläden måste sättas efter fickan.
* Förrådet går fritt upp och ned med fickan, regeln och kortet på plats.
* Raka Dupont-kontakter i hylsorna (ungefär 14 mm) krockar med förrådets framvägg (överlapp 728 mm3).
  Hylsornas topp ligger vid y 21,7 och förrådets framvägg vid y 29,5.
