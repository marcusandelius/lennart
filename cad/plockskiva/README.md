# Plockskivan: ny dosering (ersätter 10_doserhus, 11_doserhjul och 14_notmagasin)

En skiva som lutar 45 grader åt sidan plockar en hasselnöt i taget ur förrådet och släpper den genom ett utfall i plattan
ned i rännan till skålen.

| Fil | Del | Utskriftsläge |
|---|---|---|
| 10_doserstativ.stl | Lutande platta med servofäste, utfall och ränna | Står på sin fot. Inget stöd |
| 11_plockskiva.stl | Skiva Ø93,2 x 16 mm med en ficka Ø26,5 mm | Ovansidan mot plattan, hornurtaget uppåt. Inget stöd |
| 14_notforrad.stl | Krage, skärm och förråd i ett stycke | Upp och ner på sin överkant. Inget stöd |

Mått (husets ram, mm): skivans mitt (-1,5, 64, 57), axeln lutar 45 grader mot +x. Fickan plockar längst ned (180 grader) och
släpper vid 55 grader, alltså 125 graders slag. Servot (MG996R) sitter under plattan med samma mått mot hornet som i det gamla
doserhuset: hornurtag Ø25,4 x 3,5 mm, öronplan 9,0 mm under skivans undersida, fyra Ø4-hål för M3-bussningar.

Servorörelse: 180 -> 55 grader på ca 0,9 s, vila 0,3 s, tillbaka, vicka 40 grader fram och tillbaka i botten.

## Kontroller
* `sim/plock_cad.py` bygger delarna, `sim/fit.py` räknar överlapp mot husmodellen: 0 mm3 mot alla delar utom de tre som ersätts,
  och 0 mellan de nya delarna. Minsta avstånd: skärmfäste 0,8 mm, ellåda 0,8 mm, kamerafäste 1,8 mm, fönsterinsatser 2,7 mm.
* `sim/plocksim.py` simulerar nötter, skiva, servo (1,0 Nm) och ränna med samma mått. 16 körningar med 40 nötter:
  603 av 640 nötter levererade genom rännans mynning. 15 körningar tömde förrådet helt. En körning (vila 0,7 s, friktion 0,5)
  låste sig efter tre nötter när två nötter föll ut samtidigt. Med vila 0,3 s: 320 av 320, inga stopp.
* Förrådet rymmer 68 nötter i simuleringen.

Inte kontrollerat: kablar, det utskrivna husets verkliga mått, servots verkliga vridområde och hornets mått.
