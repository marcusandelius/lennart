# Nya elektroniklådan (ersätter 16, 16b, 17, 24 och 25)

Tre delar i svart PETG och en packning i TPU. Allt skruvas i gängor (insatser), inte direkt i plasten.

| Fil | Del | Utskrift |
|---|---|---|
| `16_elbakstycke.stl` | Bakstycke med golv, fyra kabelöppningar, två skenor och ett torn uppe till höger för kåpans skruv. Skruvas fast i bakväggen och sitter kvar | Står på golvet som i huset. Inga stöd |
| `16b_elkapa.stl` | Kåpa: framsida, sidor och tak, öppen bak och nedåt, med tre fönster | Ligger på framsidan, öppningen uppåt. Inga stöd |
| `24_komponentplatta.stl` | Komponentplatta som glider i skenorna | Ligger på baksidan, distanserna uppåt. Inga stöd |
| `17_elpackning_tpu.stl` | Packning 1,2 mm mellan bakstycket och bakväggen | TPU, ligger platt |
| `asm/`, `komponenter/` | Delarna och komponenterna (med kontakter och böjda kablar) i husets koordinater | – |
| `src/` | Skripten. `el_lada.py ut` skapar allt; kontrollerna läser husmodellen och doseringen ur arbetsmappen | – |

## Djupet och fönstren
Från plattan till kåpans insida är det 24,6 mm, och mer går inte att få: förrådet och stativet står 2,4 mm framför
kåpan och bakväggen bakom. Kontakt plus böjd kabel behöver 24,6 mm från kortets ovansida (uppmätt), alltså cirka
5 mm mer än det finns. Därför har kåpan tre fönster där kontakterna sticker ut i fri yta. Alla är öppna nedåt, så att
kåpan går att lyfta med allt inkopplat:
* Höger kant, framför Pi:ns GPIO-kontakter. Förrådet rundar av där, så det finns 7–20 mm fritt framför kåpan.
* Nere till vänster, framför PCA9685:s kanal 0–3 (30 mm fritt framför stativet). Servokablarna går ut här.
* Vänster sida, för PCA9685:s vinklade kontrollkontakt (cirka 6 mm till husets vägg).

En utbuktning i stället för fönster går inte att skriva ut med kåpan liggande på framsidan.

## Layout (sett framifrån)
* Raspberry Pi 5 till höger, stående: USB och nätverk nedåt, GPIO till höger, USB-C till vänster, minneskortet uppåt
  (sticker ut fritt). Nätverkskabeln går rakt ned genom den tredje golvöppningen, och kamerans flatkabel bredvid.
* PCA9685 liggande längst ned till vänster: kontrollkontakten till vänster, servokontakterna nedåt, plinten uppåt.
* EKM006 stående i mitten: 12 V in nedtill, 5 V ut upptill (den klippta USB-C-kabeln till Pi:n).
* Servoomvandlaren stående till vänster i en vagga med buntband.
* Keystone-uttaget och DC-jacket ligger löst under lådan (27 mm höjd). Kablarna går upp genom golvet.
  Båda omvandlarna kopplas direkt i DC-jackets plint (beslutsloggen 2026-11-25).
* Routern står på kant till vänster om doseringen. Lådan och fönstren går inte in i dess plats.
* Golvöppningar från vänster: kontrollkablar och servoomvandlaren, 12 V till EKM006, nätverk och flatkabel, GPIO-kabeln
  till keystone-uttaget och fler kablar.

## Kontroller (`src/elchk.py`, `src/ghostchk.py`, `src/sweep2.py`)
* Inga överlapp med huset, doseringen eller skärmfickan. Kontakterna når som närmast 3 mm från förrådet (GPIO).
* Komponenterna krockar inte med varandra eller med lådan.
* Kåpan går fritt rakt upp med allt inkopplat.
* Plattan går fritt rakt upp med komponenterna och kontrollkablarna kvar, när servokontakterna, nätverket,
  flatkabeln och 12 V är urdragna.

## Gängor och skruvar
| Var | Antal | Vad |
|---|---|---|
| Pi 5 | 4 | M2,5-insats (hål Ø3,6 × 5) + M2,5 × 6 |
| PCA9685 och EKM006 | 8 | M2-insats (hål Ø3,2 × 4,5) + M2 × 5 |
| Tornet uppe till höger | 1 | M2,5-insats + M2,5 × 8 genom kåpans tak |
| Bakväggen | 4 | M3 × 10 utifrån med gummibricka, M3-mutter i fickan på bakstyckets insida |

PCA9685 är en kopia. Uppmätt cirka 56,5 × 19,5 mm mellan hålens mitt och cirka Ø3 hål. Plattan följer Adafruits mått
(55,9 × 19,05), och en M2 i ett Ø3-hål tar upp skillnaden. Hålen för insatserna följer Ruthex tabell [verifiera].

## Isärtagning
1. Lyft av taket.
2. Skruva ur kåpans skruv och lyft kåpan rakt upp. Allt kan sitta inkopplat.
3. Dra ur servona, nätverkskabeln, flatkabeln, 12 V och GPIO-kabeln till keystone-uttaget, och lyft plattan ur skenorna.
