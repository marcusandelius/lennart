# Plockskivan: hål Ø 28 mm och vinkel

Felsökt och ändrad 2026-11-27 i en Claude Code-session. Marcus har skrivit ut den nya skivan, och den **fungerar** (Marcus, 2026-11-27). Vilken utmatningsvinkel som används på stationen är [verifiera i adminvyn].

## Doseringen i korthet

Doseringen i version 9 av modellen är en **plockskiva**: en skiva Ø 85 mm och 16 mm tjock, som lutar 45° på doserstativet. Ett servo (MG996R) vrider skivan så att hålet går från botten av nöthögen upp till **utfallet**, ett hål i stativets platta. Där faller nöten ner i rännan (rutschkanan) till skålen. Omröraren sitter i det avlånga hålet mitt i skivan.

Version 9 finns bara i den publicerade förhandsgranskningen (https://claude.ai/artifact/9LQD4NfnbhvxCEfwnb7qiV), inte i `model/`. Delarna och STL-filerna tas fram med `tools/extract_from_html.py`. Plockskivan heter `doserhjul` i datan och `11_plockskiva.stl` som fil.

> `model/patch8.py` beskriver ett **äldre** doseringshjul (en rulle med en radiell ficka). Det används inte längre.

## Problemet

Vissa nötter föll inte ner i rännan utan blev kvar i skivans hål.

## Vad analysen i modellen visade

- **Utfallet i stativet** är Ø 26 mm. Skivans hål var Ø 25 mm, och vid 114° låg det precis över utfallet.
- **Nöten ligger an nedåt.** Skivan lutar 45°, så nöten trycks mot hålets nedersta vägg. Den faller bara ut om den väggen ligger över utfallet. Annars vilar nöten på stativets kant och följer med tillbaka.
- **Vinkelintervallet** med det gamla hålet var cirka 112–121° för nötter på 18–22 mm.
- **Pi:n vred 130°** som standard. Värdet kom från det gamla doseringshjulet. Vid 130° vilar de flesta nötterna på stativets kant.
- **Ovanför skivan** finns ingen krock med förrådet eller skivkåpan för nötter upp till 24 mm, längs hela vägen från 0 till 122°.

Beräkningarna förenklar nöten till ett klot som ligger an mot hålets nedre vägg, och tittar bara på stativets översta kant. De visar läget, men provet med riktiga nötter är det som avgör.

## Ändringar i skivan

Skivan tas fram med [tools/plockskiva_hal28.py](../tools/plockskiva_hal28.py) ur `11_plockskiva.stl` (version 9). Resten av skivan är oförändrad.

| | Förut | Nu |
|---|---|---|
| Nöthålet | Ø 25 mm, mitt 28 mm från skivans mitt | **Ø 28 mm, mitt 27,5 mm från skivans mitt** |
| Vägg mellan hålet och ytterkanten | 2,1 mm | 1,1 mm (0,6 mm om mitten inte flyttats) |
| Förborrade hål för hornets skruvar (2 mm) | Ø 1,0 mm | **Ø 1,7 mm**, med avlastning Ø 2,6 × 0,5 mm överst |
| Utmatningsvinkel, standard | 130° | **119°** (intervall cirka 116–123° enligt modellen) |

- **Gamla hålet ryms i det nya**, så ingen del av hålet blev mindre.
- **Skruvhålen:** i den förra skivan reste sig hornets arm när skruvarna drogs. Troliga orsaker är att skruven hamnade i ett horn-hål utan förborrat hål under, och att hålet på Ø 1,0 mm var för litet för en skruv på 2 mm.
- **Hornurtaget** gjordes större (0,5 mm spel) i artefakten samma dag, innan den här ändringen.

## Utskrift

| Inställning | Värde |
|---|---|
| Material | Svart PETG |
| Byggplatta | Textured PEI |
| Placering | Som filen ligger: omrörarsidan nedåt |
| Stöd | Inga |
| Lagerhöjd | 0,20 mm |
| Väggar | 2 |
| Gles ifyllnad | 15 % |
| Brätte | Inget |
| Elefantfotskompensation | 0,1–0,15 mm (sidan mot plattan vänds upp mot förrådet, där nöten går in) |
| Söm | Bak, eller scarf seam |
| Kammare | Lucka eller lock på glänt, högst cirka 45 °C |

Kolla i förhandsgranskningen att den tunna väggen (1,1 mm) mot ytterkanten är fylld hela vägen upp.

## Montering

1. Lägg i hornet utan skruvar. Det ska gå ner utan värmepistol.
2. Använd hålet i varje arm som ligger rakt över skivans förborrade hål, 11,2 mm från mitten. Borra gärna upp de hålen i hornet till cirka 2,1 mm, så att skruven bara får fäste i skivan och drar ner hornet.
3. Skruva fast utan att dra för hårt. Kolla med en linjal att varken hornet eller skruvhuvudena sticker upp. Glappet mot stativets platta är bara cirka 0,6 mm.
4. Lim (tvåkomponentsepoxi) går att använda om hornet glappar, men då sitter hornet fast i skivan för gott. Det är Marcus val.

## Provkörning

Skivan drivs just nu av ett **360°-servo** (Marcus, 2026-11-27), inte av MG996R. Ett 360°-servo har ingen vinkel, så utmatningsvinkeln 119° gäller inte. Lägena sparas i stället som tid från plockläget, och en utmatning är ett helt varv framåt.

1. Spara plockläget, utfallet och ett helt varv i adminvyn, fliken **Nötdosering**, enligt [koppling-servon.md](koppling-servon.md#plockskivan-med-360-servo-just-nu).
2. Finjustera med **Prova: till utfallet** och **Prova: resten av varvet**. När skivan står still vid utfallet ska hålet ligga mitt över det.
3. Prova med små och stora nötter. Justera tiden till utfallet med 10–20 ms i taget om någon blir kvar.
4. Med **Varannan utmatning bakåt** (standard sedan 2026-11-28) behövs även bakåt-tiderna: välj Bakåt i steg 5 och prova fram dem på samma sätt.
5. Kör flera utmatningar i rad och kolla att hålet fortfarande hamnar i plockläget. Om det glider: justera tiden för ett helt varv.

Med ett vinkelservo gäller i stället **Utmatningsvinkel**, **Plocklägets vinkel** och **Tid för vridet**.
