# Nya elektroniklådan (ersätter 16, 16b, 17, 24 och 25)

Tre delar i svart PETG och en packning i TPU. Allt skruvas i gängor (insatser), inte direkt i plasten.

| Fil | Del | Utskrift |
|---|---|---|
| `16_elbakstycke.stl` | Bakstycke med golv, fem kabelöppningar, två skenor, ett torn uppe till höger för kåpans skruv och ett hål för förskruvningens mutter. Skruvas fast i bakväggen och sitter kvar | Står på golvet som i huset. Inga stöd |
| `16b_elkapa.stl` | Kåpa: framsida, sidor och tak, öppen bak och nedåt, med två fönster | Ligger på framsidan, öppningen uppåt. Inga stöd |
| `24_komponentplatta.stl` | Komponentplatta som glider i skenorna | Ligger på baksidan, distanserna uppåt. Inga stöd |
| `17_elpackning_tpu.stl` | Packning 1,2 mm mellan bakstycket och bakväggen | TPU, ligger platt |
| `asm/`, `komponenter/` | Delarna och komponenterna (med kontakter och böjda kablar) i husets koordinater | – |
| `src/` | Skripten. `el_lada.py ut` skapar allt; kontrollerna läser husmodellen och doseringen ur arbetsmappen | – |

## Strömkabeln genom bakväggen
Strömkabeln går in genom det vänstra Ø16-hålet i bakväggen (x −42, 92 mm upp) med kabelförskruvningen M16, som
tidigare. Det högra Ø16-hålet sitter bakom Pi:n och täcks av packningen och bakstycket. Sätt en blindplugg M16 i det.
1. Montera förskruvningen i bakväggen före bakstycket. Muttern på insidan hamnar i ett Ø26-hål i bakstycket
   (droppformat, så att det skrivs ut utan stöd) och i packningen.
2. Kabeln går rakt in genom en slits i komponentplattan. Slitsen är öppen nedåt, så att plattan kan lyftas och sänkas
   med kabeln på plats.
3. Skala av ytterhöljet cirka 1 cm innanför förskruvningen. Förskruvningen tätar mot höljet, och ledarna inuti
   böjs nedåt i kanalen (x −48 till −36) och går genom golvet till DC-jacket under lådan. En hel utomhuskabel kan
   inte böjas på de cirka 20 mm som finns. Kontrollera att förskruvningens klämområde passar kabeln [verifiera].
4. Sätt en DC-hankontakt med skruvplint på kabeländen, eller koppla ledarna direkt till omvandlarna.

Ingenting på plattan får sitta i kanalen under förskruvningen. Därför står PCA9685 på högkant, EKM006 ligger ovanför
och servoomvandlaren ligger under lådan.

## Djupet och fönstren
Från plattan till kåpans insida är det 24,6 mm, och mer går inte att få: förrådet och stativet står 2,4 mm framför
kåpan och bakväggen bakom. Kontakt plus böjd kabel behöver 24,6 mm från kortets ovansida (uppmätt). Därför har kåpan
två fönster, öppna nedåt, där kontakterna sticker ut i fri yta:
* Höger kant, framför Pi:ns GPIO-kontakter (7–20 mm fritt framför, där förrådet rundar av).
* Till vänster, framför PCA9685:s kanal 0 och 1 (6–19 mm fritt framför, även med förrådets lyftväg).

## Layout (sett framifrån)
* Raspberry Pi 5 till höger, stående: USB och nätverk nedåt, GPIO till höger, USB-C till vänster, minneskortet uppåt.
* PCA9685 stående till höger om kanalen: servokontakterna på vänster kant, kontrollkontakten uppåt, plinten åt höger.
* EKM006 liggande ovanför: 5 V ut till vänster (USB-C-kabeln till Pi:n), 12 V in till höger.
* Under lådan (27 mm höjd): servoomvandlaren, DC-jacket och keystone-uttaget. Buntbandshål i golvet.
* Golvöppningar från vänster: fler kablar, strömkabeln, 12 V och 5 V till EKM006 och PCA9685, nätverk och flatkabel,
  GPIO-kabeln och fler kablar.
* Routern står på kant till vänster om doseringen. Lådan går inte in i dess plats.

## Kontroller (`src/elchk.py`, `src/ghostchk.py`, `src/sweep2.py`)
* Inga överlapp med huset, doseringen eller skärmfickan. Servokontakterna når som närmast 2,8 mm från förrådet.
* Komponenterna krockar inte med varandra eller med lådan.
* Kåpan går fritt rakt upp med allt inkopplat.
* Plattan går fritt rakt upp med komponenterna kvar och strömkabeln på plats, när servokontakterna är urdragna.

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
3. Dra ur servona, nätverkskabeln, flatkabeln och ledarna som går till det under lådan, och lyft plattan ur skenorna.
   Strömkabeln sitter kvar i sin slits.
