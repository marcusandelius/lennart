# Skärmfickan (ersätter 19_skarmklamma.stl)

Ritad i en annan dialog 2026-11-25, skriptet ligger på grenen `claude/serene-ride-2s73q0` som `model/skarmficka.py`
(måtten på kortet och motiveringen i `docs/hardvara.md` avsnitt 3.6 och `docs/beslut/beslutslogg.md` på samma gren).
Filerna här är skapade med det skriptet mot husmodellen i förhandsgranskningen. Fickan och regeln är utskrivna.

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
