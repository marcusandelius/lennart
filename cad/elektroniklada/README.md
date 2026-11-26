# Nya elektroniklådan (ersätter 16, 16b, 17, 24 och 25)

Lådan består av tre delar i svart PETG och en packning i TPU. Allt skruvas i gängor (insatser), inte direkt i plasten.

| Fil | Del | Utskrift |
|---|---|---|
| `16_elbakstycke.stl` | Bakstycke med golv, två skenor och ett torn för kåpans skruv. Skruvas fast i bakväggen och sitter kvar | Står på golvet som i huset. Inga stöd |
| `16b_elkapa.stl` | Kåpa: framsida, sidor och tak i ett stycke, öppen bak och nedåt | Ligger på framsidan, öppningen uppåt. Inga stöd |
| `24_komponentplatta.stl` | Komponentplatta som glider i skenorna | Ligger på baksidan, distanserna uppåt. Inga stöd |
| `17_elpackning_tpu.stl` | Packning 1,2 mm mellan bakstycket och bakväggen | TPU, ligger platt |
| `asm/` | Delarna i husets koordinater (för kontroll och förhandsgranskning) | – |
| `komponenter/` | Komponenterna som enkla lådor (bara för kontroll av plats) | – |
| `src/` | Skripten. `el_lada.py ut` skapar allt; kontrollerna läser husmodellen (`A_parts.pkl`) och doseringen ur arbetsmappen | – |

Utskriftskontroll lager för lager (`src/printchk.py`): inga svävande öar. Ostödda ytor finns bara som korta broar
över ventilationsspringorna, keystone-hålen och tornets undersida (45°).

## Mått och läge
* Lådan är 140 mm bred och går från 28 mm över golvet upp till 170 mm. Under lådan finns cirka 25 mm för kablarnas böjar.
* Bakstycket: 4 mm bakvägg som täcker samma fyra skruvhål (±60, 80 och 164) och de gamla Ø16-hålen.
* Golvet har tre öppningar: vänster 54 mm (servona, PCA9685 sitter rakt ovanför), mitten 20 mm (nätverk, kamerans
  flatkabel och 12 V) och höger 36 mm (keystone-uttagen). Varje öppning är ungefär 20 mm djup.
* Komponentplattan, sett framifrån:
  * Längst ned till vänster: PCA9685, servokontakterna nedåt mot golvöppningen.
  * Ovanför: EKM006 (5 V till Pi:n), servoomvandlaren i en vagga med buntband, och två Wago 221.
  * Högst upp till vänster: DC-jacket.
  * Höger: Raspberry Pi 5, stående, med USB och nätverk nedåt mot mittöppningen.
  * Nere till höger: hylla för två keystone-uttag. Kablarna kommer in underifrån.
* Avstånd till kåpans insida framtill: Pi 2,0 mm, servoomvandlaren 1,6 mm, PCA9685 2,6 mm, keystone 3,2 mm.

## Kontroller (`src/elchk.py`, `src/ghostchk.py`, `src/sweep.py`)
* Inga överlapp med huset, doseringen eller skärmfickan. Minsta avstånd:
  * bakväggen 1,2 mm (packningen)
  * förrådet och stativet 2,4 mm
  * taket 5,4 mm
* Komponenterna krockar inte med varandra eller med lådan.
* Kåpan går fritt rakt upp när taket är av.
* Plattan går fritt rakt upp ur skenorna när kåpan är av. Tornet sitter på vänstra skenan, utanför plattans väg.

## Gängor, skruvar och muttrar
| Var | Antal | Vad |
|---|---|---|
| Komponentplattan, Pi 5 | 4 | M2,5-insats (hål Ø3,6 × 5) + M2,5 × 6 |
| Komponentplattan, PCA9685 och EKM006 | 8 | M2-insats (hål Ø3,2 × 4,5) + M2 × 5 |
| Tornet uppe till vänster | 1 | M3-insats (hål Ø4,0 × 6) + M3 × 8 genom kåpans tak |
| Bakväggen | 4 | M3 × 10 utifrån, med gummibricka, och M3-mutter i fickan på bakstyckets insida |

Hålmåtten för insatserna är tagna från Ruthex tabell [verifiera mot förpackningen]. Använd inte längre skruv än
M3 × 10 i bakväggen: spetsen ska inte nå komponentplattan, som sitter 1 mm framför bakstycket.

## Mät innan utskrift
* Servoomvandlaren: vaggan är 49 × 32 mm. Hålen i öronen är inte kända, så den hålls med buntband.
* DC-jacket: platsen är ungefär 23 × 13 mm, och det fästs med buntband.
* Pi 5 med Active Cooler: räknat med 4 mm distans + 1,6 mm kort + 13,7 mm kylare.

## Isärtagning
1. Lyft av taket.
2. Skruva ur kåpans skruv och lyft kåpan rakt upp. Nu når du alla kontakter med plattan på plats.
3. Dra ur kontakterna och lyft plattan rakt upp ur skenorna.
