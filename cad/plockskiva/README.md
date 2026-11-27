# Plockskivan: ny dosering (ersätter 10_doserhus, 11_doserhjul och 14_notmagasin)

Ritad för hasselnötter 16–22 mm långa. Större nötter sorteras bort före påfyllning.

En skiva (Ø85,2 mm) som lutar 45 grader åt sidan plockar en hasselnöt i taget ur förrådet och släpper den genom ett
utfall i plattan ned i rännan till skålen. En omrörare på skivans axel hindrar nötterna från att valva sig ovanför skivan.

| Fil | Del | Utskriftsläge |
|---|---|---|
| 10_doserstativ.stl | Lutande platta med kant runt skivan, servofäste, utfall och ränna | Står på sin fot. Inget stöd |
| 10b_skivkapa.stl | Kåpa över skivans främre kant, snett avskuren under skärmklämman | Står på sin underkant. Inget stöd, brim |
| 11_plockskiva.stl | Skiva med en ficka Ø26,5 mm och ett avlångt hål (8,4 × 11,4 mm) för omröraren | Ovansidan mot plattan. Inget stöd |
| 11b_omrorare.stl | Svagt kilformad fot (10,6–11,7 × 8 mm, 8 mm ned i skivan), pinne 8 × 8 mm och rakt blad 30 × 46 mm med rundade hörn (7 mm), rundad ovankant (3 mm) och 0,8 mm fas mot byggplattan, allt 8 mm tjockt | Ligger platt. Inget stöd |
| 11c_omrorare_motiv.stl | Valfritt inlägg som fyller hasselnötsmotivet (0,6 mm) i en annan färg | Läggs till som del i samma objekt som 11b |
| 14_notforrad.stl | Förrådet, lyfts rakt upp | Upp och ner på sin överkant. Inget stöd, brim |

## Stjärnhornet och fickan
* Fickan är Ø25 mm (simulerad som Ø24,5), för nötter 16–22 mm långa. Större nötter sorteras bort före påfyllning.
* Skivans undersida har ett urtag för MG996R:s stjärnhorn, armarna 45 grader från fickan. Armarna är 2,0 mm tjocka
  (uppmätta), når ca 19 mm ut, är ca 8 mm breda vid navet och ca 5,5 mm längst ut (ur foto, `omritning/horn_matt.png`).
  Urtagets botten ligger 3,5 mm in i skivan. Hornarmarnas ovansida ligger ca 15,0 mm över ovansidan av servots
  fästöron (ur foto mot tumstock, ±0,5 mm, `omritning/servo_horn_hojd.png`). Därför är stativets platta 10,9 mm tjock
  (förut 8,4): servots öron ligger an mot undersidan, och servot sitter 2,5 mm lägre än förut.
* **Ändrat 2026-11-27:** hornet gick inte ned i urtaget, som hade 0,2 mm spel och byggde på mått ur foto. Urtaget har
  nu 0,5 mm spel runt armarna, når 22 mm ut (förut 19,5) och navet är Ø13 mm (förut Ø11,8). Hornet behöver inte sitta
  tätt i urtaget, eftersom skruvarna genom armarna låser läget. Väggen mellan urtaget och fickan är 4,1 mm. Bara
  `11_plockskiva.stl` är ändrad.
* Fyra förborrade hål Ø1,0 mm, 10,5 mm djupa, i det andra hålet på varje arm (11,2 mm från mitten: 8,0 mm till det
  innersta hålet, uppmätt, och 3,2 mm mellan hålen, ur foto), för de fyra silverfärgade skruvarna (ca 1,1 mm, ca 12 mm).
* Hålet i stativets platta runt servots axel är Ø31 mm och 2,5 mm djupt, så att skruvskallarna under hornet går fritt.

## Kanalen för skärmkortets kontakter
Förrådets framvägg har en kanal, 54 mm bred och 8 mm djup (y 29,5–37,5), från z 94 och ända upp. Kontakterna på skärmkortet
sticker enligt foto ut ca 6–9 mm bakom skärmfickans skenor (y ca 29–32) och kablarna viker av åt sidan, så de ryms i
kanalen. Förrådet går inte att lyfta förbi kontakterna; dra först av dem bakåt i kanalen (ca 5–8 mm plats bakom dem,
uppskattat ur foto) och lyft sedan förrådet. En 14 mm djup kanal gav plats att dra av kontakterna helt men sämre matning i
simuleringen (243 av 280 med plan botten, 218 av 280 med sluttande, `sim/resultat_djupare_kanal.jsonl`) och valdes bort.

## Simulering med den här geometrin (`sim/resultat.jsonl`)
40 nötter 16–20 mm långa (14–17,5 mm breda), vila 0,3 s, omröraren på. Friktion 0,35–0,5: 7 körningar, 274 av 280
nötter levererade, inga nötter fast, 95 tomma slag och 32 dubbeldoser på 336 slag, servot stannade 16 gånger och tog om.
Friktion 0,65: 30 av 40.

## Motivet på omröraren
Hasselnötsmotivet (`motiv/notmotiv.webp`) är nedsänkt 0,6 mm i bladets ovansida, 21 × 22 mm. Linjerna är förtjockade
till minst 0,45 mm och mellanrummen till minst 0,40 mm så att en 0,4 mm dysa klarar dem (`motiv/motiv_linjebredd.png`).
Motivet sitter på den sida som vetter bakåt mot ellådan när omröraren sitter på plats. För två färger: ladda
11b och 11c tillsammans som ett objekt med flera delar i Bambu Studio och ge 11c en annan färg; färgbytet sker
bara i de tre översta lagren.

## Förutsättningar i huset
* Skärmens kontakter får nå högst 27 mm in från framväggens insida. Med raka Dupont-kontakter når de ca 35 mm, så
  det krävs vinklade stiftlister (eller motsvarande) så att kontakterna ligger längs kortet.
* Skärmklämman och kamerasläden måste vara lossade när stativet sänks ned (två M3 var, uppifrån).

## Mått (husets ram, mm)
Skivans mitt (-13, 65,5, 57), axeln lutar 45 grader mot +x. Fickan plockar längst ned (180 grader) och släpper vid
66 grader, alltså 114 graders slag. Servot (MG996R) sitter under plattan med samma mått mot hornet som i det gamla
doserhuset: hornurtag Ø25,4 × 3,5 mm, öronplan 9,0 mm under skivans undersida, fyra Ø4-hål för M3-bussningar.
Rännan är 28–30 mm bred (en nöt i bredd). Under utfallet lutar golvet 38 grader; de sista 12,5 mm före mynningen
lutar det bara 12 grader, så att nöten inte kommer snett mot öppningen i framväggen.

Servorörelse: 180 -> 66 grader på ca 0,9 s, vila 0,3 s, tillbaka, vicka 40 grader fram och tillbaka i botten.
Om servot inte når fram: vrid tillbaka och försök igen.

## Montering
1. Sex M3-bussningar i stativet: fyra underifrån för servot, två i öronen för kåpan.
2. Servots runda horn skruvas i skivans urtag med de små skruvarna från servopåsen.
3. Skivan läggs på plattan, servot skjuts upp underifrån och skruvas fast, hornskruven dras genom hålet mitt i skivan.
4. Kåpan skruvas på med två M3 × 8.
5. Stativet sänks ned på de två bakre styrtapparna (skärmklämma och kamerasläde lossade) och skruvas framme till höger.
6. Skärmklämma och kamerasläde tillbaka. Förrådet lyfts rakt ned, haken på vänster sida griper över stativets överkant.
7. Omröraren sänks rakt ned med pinnen i spåret i förrådets golv och trycks de sista 10 mm snett ned i det avlånga
   hålet i skivan tills foten kläms fast. Foten passar bara på två sätt, och båda är rätt. Den sitter 8 mm ned i skivan
   (hålet är 9,0 mm djupt; under det ligger 3,5 mm fritt för hornskruvens skalle) och bladet hamnar 1 mm över förrådets golv. Inget lim.

För att ta ur förrådet: dra omröraren 10 mm snett uppåt ur skivan, lyft den rakt upp, och lyft sedan förrådet.

## Kontroller (`sim/slutkontroll.txt`)
* Överlapp mot husmodellen och mellan delarna: 0 mm3.
* Stativ med servo, skiva och kåpa går fritt rakt ned när skärmklämma och kamerasläde är lossade. Förrådet går fritt
  rakt upp med allt annat på plats. Skivan och omröraren går fritt hela slaget.
* Omröraren går fritt ur och i: 10 mm längs skivans axel och sedan rakt upp genom spåret (9,2 mm brett) i förrådets golv.
  Rakt upp längs axeln eller rakt upp utan de första millimetrarna går inte.
* Minsta avstånd: skärmklämma 3,0 mm (kåpan), kamerasläde 3,7 mm, kropp 4,0 mm, ellåda 4,4 mm, fönsterinsatser 10 mm,
  tak över 14 mm. Rännans hals har 0,8 mm mot sockelns kanal (styrpassning).
* Utskrift lager för lager: inga svävande öar utom flisor under 0,5 mm2, inget överhäng brantare än 45 grader utöver
  17 mm2 i stativet.

## Simulering (`sim/resultat.jsonl`, 40 nötter per körning, vila 0,3 s)
* Friktion 0,35–0,5: 14 körningar. 13 tömde förrådet (högst 2 nötter kvar), en stannade med 11 nötter kvar när en nöt
  fastnade i rännan. 62 dubbeldoser och 28 tomma slag på 505 slag. Servot stannade 20 gånger och klarade nästa försök.
* Friktion 0,65 (klibbiga nötter): en av två körningar stannade med 23 nötter kvar.
* Utan omrörare (`sim/resultat_utan_omrorare.jsonl`): med 40 nötter tömdes förrådet i 5 av 8 körningar, i de andra tre
  valvade sig nötterna och 13–23 blev kvar. Med 15 nötter tömdes det i 4 av 4. Utan omrörare blev det färre dubbeldoser
  (8 på 271 slag) och servot stannade bara en gång.
* Förrådet rymmer ca 75 nötter 16–20 mm långa (en fyllningssimulering, `sim/notlagen_forhandsgranskning.json`).

## Inte kontrollerat
Servots och hornets verkliga mått, servots vridområde (114 grader plus vickning), kablarnas dragning, det utskrivna
husets verkliga mått, och var skärmens kontakter verkligen hamnar. Utskriftstider är inte beräknade.

Underlaget till omritningen (hinderkarta och de varianter som inte fungerade) ligger i `omritning/`.
