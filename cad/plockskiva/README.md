# Plockskivan: ny dosering (ersätter 10_doserhus, 11_doserhjul och 14_notmagasin)

> **Skriv inte ut ännu.** Allt nedan är ritat och simulerat för nötter 15–18,5 mm breda och 18–22 mm långa.
> Nötterna som ska användas är ungefär 20–21 mm breda och 23–25 mm långa (uppmätt från ett foto mot linjal,
> `omritning/notter_linjal.png`). Med 20–22 × 23–25 mm stannade doseringen i alla sex simuleringarna
> (16 av 180 nötter levererade, `sim/resultat_nottstorlek.jsonl`). Delarna måste ritas om för den storleken.

En skiva (Ø85,2 mm) som lutar 45 grader åt sidan plockar en hasselnöt i taget ur förrådet och släpper den genom ett
utfall i plattan ned i rännan till skålen. En omrörare på skivans axel hindrar nötterna från att valva sig ovanför skivan.

| Fil | Del | Utskriftsläge |
|---|---|---|
| 10_doserstativ.stl | Lutande platta med kant runt skivan, servofäste, utfall och ränna | Står på sin fot. Inget stöd |
| 10b_skivkapa.stl | Kåpa över skivans främre kant, snett avskuren under skärmklämman | Står på sin underkant. Inget stöd, brim |
| 11_plockskiva.stl | Skiva med en ficka Ø26,5 mm och ett avlångt hål (8,4 × 11,4 mm) för omröraren | Ovansidan mot plattan. Inget stöd |
| 11b_omrorare.stl | Svagt kilformad fot (10,6–11,7 × 8 mm, 8 mm ned i skivan), pinne 8 × 8 mm och rakt blad 30 × 46 mm med rundade hörn (7 mm), rundad ovankant (3 mm) och 0,8 mm fas mot byggplattan, allt 8 mm tjockt | Ligger platt. Inget stöd |
| 14_notforrad.stl | Förrådet, lyfts rakt upp | Upp och ner på sin överkant. Inget stöd, brim |

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
* Förrådet rymmer 64 nötter struket och 71 med råge (`sim/resultat_kapacitet_och_blad76.jsonl`).

## Inte kontrollerat
Servots och hornets verkliga mått, servots vridområde (114 grader plus vickning), kablarnas dragning, det utskrivna
husets verkliga mått, och var skärmens kontakter verkligen hamnar. Utskriftstider är inte beräknade.

Underlaget till omritningen (hinderkarta och de varianter som inte fungerade) ligger i `omritning/`.
