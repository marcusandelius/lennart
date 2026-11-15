# Projektdokumentet – ögonblicksbild 2026-11-11

Ordagrant ur [HANDOFF-filen](historik/HANDOFF-lennarts-matstation-projekt.md), bilagan. **Delvis inaktuellt:** det säger ASA i stället för PETG och har gamla plattnummer. Aktuella beslut finns i [beslut/beslutslogg.md](beslut/beslutslogg.md).

Här finns allt som behövs för att köpa in, skriva ut och bygga stationen.

## Kort om projektet

Stationen är ett litet falurött hus, cirka 31 cm högt, som står på en pedestal på uteplatsen. När något landar på framgården tar en kamera i gaveln bilder, och en moln-AI avgör om det är en ekorre. Är det Lennart visar skärmen ACCESS GRANTED, luckan öppnas och doseraren släpper en hasselnöt. Andra djur får ACCESS DENIED och en incidentrapport. Bygget är Marcus bidrag till SweClockers AI-tävling "Gick inte. Nu går det.", och AI-användningen redovisas i bidraget.

## Beslut

| Område | Beslut |
| --- | --- |
| Dator | Raspberry Pi 5, som redan finns. |
| Uppkoppling | 4G via USB-modem och ett data-SIM. Wifi används inte. |
| Ström | 12 V nätadapter inomhus eller under tak, kabel ut till stationen. Omvandlare i elektroniklådan gör 5 V. |
| Igenkänning | Moln-AI. Svar inom cirka 5 sekunder efter att Lennart landat. |
| Våg | Ingen. Kameran avgör ensam, med 2–3 bilder per besök och hög säkerhetströskel. |
| Dosering | Ett hjul med en ficka, som i en tuggummiautomat. Ett servo vrider hjulet 130 grader, och fickan släpper en nöt i rännan ner till skålen. |
| Nötter | Hasselnötter i skal, 18–22 mm. Nötmallen i toleranstestet har två hål: nöten ska gå genom 22-hålet men inte genom 18-hålet. |
| Material | ASA för allt som står ute, TPU för packningar. Inget kolfiberfyllt filament i doseraren, där nötterna rör sig. |
| Budget | Cirka 4 000 kr. |

## Inköpslista

Priserna kommer från Marcus anteckningar, mest Electrokit, november 2026. Där det står "pris?" är priset inte kontrollerat. Kolla lagret innan du beställer.

### Elektronik

| Del | Antal | Ca-pris | Var | Kommentar |
| --- | --- | --- | --- | --- |
| Raspberry Pi 5 | 1 | – | Finns redan | |
| Kamerakabel för Pi 5, 22 till 15 pin | 1 | 45 kr | Electrokit | Pi 5 har en mindre kamerakontakt än kameran levereras med. |
| Aktiv kylare till Pi 5 | 1 | ca 60 kr, pris? | Valfri | Behövs om den saknas. Elektroniklådan är tät. |
| Raspberry Pi Camera Module 3 Wide | 1 | 449 kr | Electrokit | |
| microSD-kort, typ High Endurance | 1 | ca 150 kr, pris? | Valfri | Stationen skriver bilder dygnet runt, och vanliga kort slits ut. |
| 4G-modem Huawei E3372-325 | 1 | ca 395 kr, pris? | PriceRunner | Kontrollera att LTE-banden passar SIM-kortets nät (Telia eller Telenor). |
| USB-förlängning 20–30 cm, gärna vinklad | 1 | ca 50 kr, pris? | Valfri | Från Pi:ns USB-port upp till modemet på elektroniklådans lock. |
| Nätadapter 12 V 3 A (Akyga AK-TB-12) | 1 | 149 kr | Electrokit | Inte gjord för att stå ute. |
| Utomhuskabel 2 × 1,5 mm² | Efter placering | pris? | Valfri | Mät avståndet till ett jordat uttag med jordfelsbrytare. |
| DC/DC 12→5 V 5 A (EKM006) | 1 | 149 kr | Electrokit | Pi, modem och skärm. |
| DC/DC 8–23→5 V 3 A | 1 | 129 kr | Electrokit | Bara servona. Gemensam jord med Pi:n. |
| Elektrolytkondensator 1000 µF 16 V | 2 | 11 kr | Electrokit | Mot spänningsdippar från servona. |
| Servodrivkort PCA9685, I2C | 1 | ca 60–100 kr, pris? | Valfri | Ger stabila servosignaler från Pi 5 och håller servonas ström borta från Pi:n. |
| Servo MG996R | 2 | 99 kr per styck | Electrokit | Doseringen. Köp varianten som vrider 180 grader, inte den som snurrar runt. Ett i reserv. |
| Luckservo: vattentätt mikroservo, eller MG90S | 1–2 | ca 80–250 kr, pris? | Valfri | Luckservot sitter utomhus. MG90S (79 kr hos Electrokit) fungerar men är inte vattentätt. |
| Waveshare 2" IPS ST7789, Pico-varianten | 1 | 199 kr | Electrokit | Mät kortet när det kommer. Skärmklämman behöver de exakta måtten. |

### Hölje och montering

| Del | Antal | Ca-pris | Var | Kommentar |
| --- | --- | --- | --- | --- |
| Kabelförskruvning M16 × 1,5 | 3 | 23 kr | Electrokit | Två används, en är reserv, till exempel för extern 4G-antenn. |
| Ventilationsplugg M12 med membran | 2 | pris? | Till exempel Elfa | En för huset, en för elektroniklådan. |
| Neodymmagnet 10 × 2 mm, N35 | 8 | ca 50 kr, pris? | Valfri | Håller taket. Pressas in. Ju djupare de trycks, desto lättare släpper taket. |
| Polykarbonat 3 mm och akryl eller polykarbonat 1 mm | En liten bit av varje | ca 100 kr, pris? | Valfri | Kamerafönster Ø24 mm och skärmglas 50 × 39 mm. |
| Rostfria skruvar A2 | Se kommentar | ca 100 kr, pris? | Valfri | M3-sortiment 6–16 mm, 6 st M4 × 12 mm, 3 st M4 med mutter, 4 st M2,5 och 4 gummibrickor M3. |
| Skumtejp och VHB-tejp | – | pris? | Valfri | Skärmklämman och modemet. |
| Klar silikon | 1 tub | pris? | Valfri | Bara till kamerafönstret och skärmglaset. Allt annat snäpps eller pressas ihop. |
| Grön ASA | 1 kg | pris? | Valfri | Gräs, bas och framgård drar cirka 0,6–0,7 kg. |
| Vinkeljärn och skruv | 2 | pris? | Valfri | Förankrar pedestalen i väggen. |
| Klar, UV-tålig lack på sprayburk | 1 | pris? | Valfri | Tätar ytan på taket och kroppens nederkant. |
| Små buntband | 1 påse | pris? | Valfri | Fäster omvandlare och kablar i monteringsplattans hålraster. |

### Övrigt

| Del | Antal | Kommentar |
| --- | --- | --- |
| Ballast: sand i påse, grus eller stålbitar | 2–3 kg | Läggs i basens hålrum. |
| Osaltade, orostade hasselnötter i skal | – | Högst 22 mm. Sortera med nötmallen. |
| Jordad utomhusskarv med jordfelsbrytare | Om det saknas | Elsäkerheten ska kontrolleras av en behörig person. |
| Rep, 4–5 mm, och rundstav till repstegen | Om du bygger stegen | Stegen ingår inte i utskriften. |

Totalt cirka 3 300–3 700 kr utan kabel.

**Finns redan:** Raspberry Pi 5, lödpenna med spetssats för insatser, Ruthex-insatser (bygget behöver cirka 30 st M3 och 6 st M4), silikagel, Wago 221, kopplingskablar, kabelskor och krympslang. Filament: Fiberon ASA-CF08 Dark Red, Bambu ASA röd och vit, PrimaSelect ASA grå och svart, och TPU 95A.

## Utskrift

- **Skrivare:** Bambu Lab X2D. 0,20 mm lagerhöjd, brätte på stora delar, och förvärm kammaren för ASA. Skrivaren levereras med två härdade munstycken, så ASA-CF08 går bra.
- **Omfång:** 49 filer på 15 plattor, cirka 59 timmar. Fliken Utskrift i 3D-modellen visar varje platta och hur delarna ligger.
- **Bredd:** när båda munstyckena används når skrivaren 235,5 mm i bredd, inte 256. Alla plattor är lagda inom den bredden.
- **Flerfärgsdelar:** ladda alla filer med samma nummer samtidigt i Bambu Studio och svara ja på att de ska bli ett objekt.

**Ordning:**

1. Toleranstestet med nötmallen, cirka 25 minuter. Det visar om presspassningarna blir lagom på just den här skrivaren.
2. Allt som inte beror på omätta delar: bas, framgård, gräsmattor, bottenplattor, fötter, tak, skorsten, takrännor, stuprör, blomlådor, elektroniklådan med lock och monteringsplatta.
3. Doseringen: doserhuset, hjulet och magasinet, när MG996R är uppmätt. Provkör med servo och riktiga hasselnötter, gärna 200 varv i rad.
4. Kroppen, farstukvisten, luckan, skärmklämman och kamerafästet, när skärmen, kameran och luckservot är uppmätta.

## Montering i korthet

1. Pressa in alla insatser med lödpenna innan delarna monteras.
2. Skruva fast kroppen i basen. Två styrtappar visar läget.
3. Gör klart insidan av kroppen medan den är tom: fönsterinsatserna, kamerafönstret och skärmglaset (klar silikon), skärmen med sin klämma, kameran med sitt fäste, kabelförskruvningarna och ventilationspluggarna.
4. Skruva fast elektroniklådan utifrån genom bakväggen, med gummibricka under skruvskallarna. Lådan sitter sedan kvar. Spraytesta den med vatten först.
5. Bygg elektroniken på monteringsplattan vid skrivbordet och skjut ner plattan i lådan uppifrån. Stäng av PIN-koden på SIM-kortet och tejpa modemet på lådans lock.
6. Ställ doserhuset på sina två styrtappar och dra de två främre skruvarna. Lägg hjulet i sätet, skjut in servot från höger och skruva fast det, och skruva servots runda horn i hjulet. Sätt magasinet ovanpå och dra dess två skruvar.
7. Montera farstukvisten, luckan, luckservot och stolphatten.
8. Pressa in magneterna: alla i kroppen med samma pol uppåt (märkt +), alla i taket med motsatt pol nedåt (märkt −). Pressa ihop takhalvorna med nockkilarna och tryck fast skorstenen och takrännorna.
9. Tryck fast kamerans solskydd, häng på blomlådorna och snäpp fast stuprören.
10. Lacka utsidan med klar, UV-tålig lack, särskilt taket och kroppens nederkant.
11. Förankra pedestalen i väggen och ställ huset på den.

## Service

- **Fylla på nötter:** lyft av taket och häll i magasinet.
- **Nöt som fastnat:** lyft av taket, lossa magasinets två skruvar framtill och lyft magasinet rakt upp. Hjulet och rännan ligger då öppna.
- **Elektroniken:** lyft av taket och lådans lock, och dra monteringsplattan rakt upp. Inga skruvar.

## Bra att veta i drift

- **Nötterna** ska vara 18–22 mm. För stora nötter fastnar, och för små gör att två nötter kan hamna i fickan.
- **Doseringen:** låt servot göra en liten rörelse fram och tillbaka innan varje utmatning. Det skakar om nötterna i magasinet så att en nöt lägger sig i fickan.
- **Luckan** ska bara stängas när kameran inte har sett någon rörelse på några sekunder, och långsamt, så att Lennart aldrig kläms.
- **Servona** styrs via PCA9685-kortet. Stäng av signalen efter varje rörelse, så att servona inte står och surrar.
- **Ljuset** är svagt under tak på morgonen i november. Testa kameran på plats tidigt. Blir bilderna för mörka behövs en liten lampa.
- **Pedestalen** måste vara förankrad eller tung. Huset väger några kilo och står 70 cm upp, och Lennart landar med fart.
- **Skuggläge** först: låt stationen logga besök i några dagar utan att släppa nötter, och lägg nötter i skålen för hand så att Lennart vänjer sig.

## Mjukvara och drift

Allt körs som ett Python-program på Pi:n, startat av systemd så att det kommer igång av sig självt efter ett strömavbrott. Vid rörelse tar kameran 2–3 bilder och skickar dem till moln-AI:n, som svarar med art och säkerhet. Ett osäkert svar ger läget "VERIFIERAR…" och en ny bild. Varje besök loggas med bild och tid i SQLite. Spärrtid och ett dagligt maxantal nötter skyddar mot överutfodring, och utan svar från molnet blir det ingen nöt. Besöksliggaren kan vara publik, medan säkerhetscentralen hålls privat. Publicera bara bilder som AI:n har klassat som djur, så att inga människor hamnar på den publika sidan.

## Besökssidan och domän

Utöver säkerhetscentralen får stationen en charmig, publik besöksliggare: varje besök med bild, klockslag och en stämpel, INSLÄPPT eller NEKAD, och incidentrapporten ett klick bort.

| Domän | Varför |
| --- | --- |
| notkontrollen.se | Nötkontrollen utan ö, och "not" läses som "nej" på engelska. Passar NEKAD-stämpeln. |
| lennart.security | Säkerhetscentral-tonen i själva adressen. Toppdomänen är dyrare än .se. |
| besoksliggaren.se | Sidans eget namn, tydligt för svenska besökare. |
| ekorrvakten.se | Enkel att säga högt och komma ihåg. |
| accessgranted.nu | Skärmens egen fras, internationell för ett tävlingsbidrag. |

Tillgänglighet och pris är inte kontrollerade. Undvik å, ä och ö i domänen.

## Öppna frågor

- Ska alla ekorrar släppas in, eller bara Lennart?
- Vilket nät ligger SIM-kortet på, och stöder modemet de LTE-banden?
- Exakta mått på skärmkortet, MG996R med sitt runda horn och luckservot när de har kommit.
- Vad är pedestalen gjord av, och hur fästs den i väggen?
- Räcker ljuset för kameran på morgonen i november?
- Finns det en deadline för tävlingsbidraget?
