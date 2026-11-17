# Filmen – läget

Senast uppdaterad 2026-11-16. Skriven för att arbetet ska kunna fortsätta på vilken dator som helst, och av vilken session som helst.

## Beslut som gäller

- Berättarrösten är Marcus egen (`full recording.m4a`). Rösten bearbetas lokalt och skickas aldrig till någon tjänst.
- Huset får inte visas före del 3. Del 0 visar bara skärmen, gluggen, mekaniken i genomskärning och delarna utspridda på golvet.
- Luckan öppnas först, sedan rullar nöten.
- I filmen visas bildigenkänningen som ett moln. Var den faktiskt körs är fortfarande ett öppet beslut, se `docs/beslut/bildigenkanning.md`. Ändras beslutet behöver del 2 ändras.
- Inga sus eller swoosh-ljud på övergångarna.
- Inga toningar mellan klipp. Övergångarna bärs av kamerarörelser, matchklipp och former som fortsätter in i nästa bild.
- Rekonstruktioner i 3D märks som sådana. Inga påhittade konstruktionsdetaljer visas som verkliga.
- Klippens längder följer rösten. Ändras en scen ska dess klipp ha samma längd, annars hamnar rösten fel. Tiderna står i `SEG` i `verktyg/ljudmix.mjs`.

## Delarna

| Del | Innehåll | Läge |
|---|---|---|
| 0 Öppningen | Skärmen, gluggen, nötens väg, 48 delar, VERIFIERAR, titeln | Klar. Fullt nötmagasin, pixlar på skärmen, punkterna tänds på pipen. 0.4 är variant D: de 48 delarna i ett rutnät på ett golv som är en släckt LED-skärm. |
| 1 Lennart | Riktiga mobilklipp | Klar. Klipp 1.4 slutar med en snabb panorering åt höger. |
| 2 Problemet och planen | Fat, skata, kamera i sladd, moln, ja och nej | Klar. Landar ur panoreringen från 1.4, fatet snurrar vid nej, nötterna vilar på riktigt. |
| 3 Designen | Claude-fönstret ritar huset, huset reser sig | Klar. Ett litet munstycke fälls ut under fönstret och projicerar ritningen. |
| 4 Inköpen | Komponenterna på blå yta, filamentet | Klar. Allt annat som köptes landar längs kanterna, konturer visar var huvuddelarna ska ligga, fem filamentfärger. Det svarta filamentet är blankt så att det syns. |
| 5 Utskriften | Lager för lager (5.1) och utskriftsväggen (5.2–5.3) | 5.1 är en stillbild ur 3D. Väggen visar platshållare tills de riktiga timelapse-klippen finns. |
| 6 Monteringen | Sprängskiss, delarna hittar hem | Fyra byggklipp svävar bakom huset i 6.1–6.2, än så länge platshållare. Elektroniken från inköpen saknas. |
| 7 På riktigt | Huset ute, fågel nekas, Lennart får en nöt | Väntar på riktig film. Stillbilder tills dess. |

## Övergångar

| Skarv | Hur |
|---|---|
| 0.3 → 0.4 | Snabb tilt nerför skålen, 0.4 tar vid i samma tilt och landar rakt ovanför golvet |
| 0.4 → 0.5 | In i pixlarna: kameran dyker rakt ner mot en tom ruta tills golvets pixlar fyller bilden, och 0.5 backar ut ur skärmens pixlar medan den tänds |
| 0.5 → 0.6 | In i skärmens pixlar, titeln tänds i samma rutnät (`verktyg/titel.py`). En hasselnöt i pixlar står till vänster om texten och tänds strax före den. |
| 1.4 → 2.1 | Lennart tappar nöten. Kameran tiltar ner efter den, bilden glider ut i skuggan och klippet sker mitt i fallet. I 2.1 landar samma nöt bland de andra på fatet (`verktyg/fall_14.py`, `akt_plan.py`) |
| 2.6 → 3.1 | Kameran tittar upp förbi molnet, 3.1 kommer uppifrån ner mot fönstret |
| 3.2 → 4.1 | Snabb panorering, gjord i efterhand på bildrutorna |
| 4.2 → 5.1 | In i filamentrullens svarta nav |
| 5.3 → 6.1 | Utskriftsväggen öppnar sig som dörrar |
| 6.3 → 7.1 | Planerad: skärmens sken i 3D blir skärmens sken på det riktiga huset |

## Nästa steg

1. Timelapse-klippen från skrivaren (10–13 st) i `timelapse/`, sedan renderas `akt_utskrift.py` om med dem.
2. Riktig film till del 7 när huset står ute.
3. Fyra riktiga klipp från bygget till monteringen. De ersätter platshållarna (se Byggklippen nedan).
4. Elektroniken i monteringen (del 6).
5. 5.1 som rörlig bild i stället för stillbild, gärna en skärminspelning från slicern eller ett närklipp på munstycket.
6. Storyboardens röstspalt har fortfarande den gamla manustexten, inte orden i inspelningen.

## Att kontrollera före publicering

- Sunos villkor för musiken med Marcus abonnemang [verifiera].
- Claude-logotypen i del 3 är en egen ritad tolkning. Om Anthropics logotyp får användas så [verifiera].

## Vattenstämpeln

Scener som väntar på riktigt material står i listan `VANTAR` i `storyboard/storyboard.html`. De får texten VÄNTAR PÅ MATERIAL i storyboarden och i filmen (`verktyg/arbetskopia.mjs`). Ta bort en scen ur listan när dess material är på plats.

## Hur saker är gjorda

- **Rösten:** `verktyg/rost.py` jämnar ut nivån fras för fras och sänker andetag. Sedan `ljud/rostkedja.txt` i ffmpeg: klickborttagning, EQ, de-esser, multibandkompressor, kompressorer, lätt mättnad och limiter. Rösten ligger runt −19 LUFS och mixen runt −15 LUFS.
- **Musiken:** viker i mellanregistret när rösten talar (`sidechaincompress` per band). Den börjar 1 s in i filmen (`MUSIK_IN` i `ljudmix.mjs`), eftersom titeln förlängdes 1 s den 17/11. Då ligger den kvar mot allt efter titeln, där byggklippen i 6.1 är lagda på slagen. Ändras längden på något före 1.1 ska `MUSIK_IN` ändras lika mycket.
- **Effekterna:** syntetiseras i `verktyg/effekter.py`, eller hämtas ur Kenneys ljudpaket (CC0). Tiderna står i `FX` i `ljudmix.mjs`, räknat från varje klipps början.
- **Fallet 1.4 → 2.1:** nöten som faller i 1.4 är en renderad hasselnöt (`blender -b -P verktyg/not_sprite.py -- <mapp> 8`) som `verktyg/fall_14.py` lägger på de sista åtta rutorna i mobilklippet. Videon flyttas uppåt med rörelseoskärpa, som om kameran följer nöten ner, och tonar ut i mörker med samma ton som första rutan i 2.1. I `akt_plan.py` börjar 2.1 med att kameran åker ner med samma nöt (upprätt, spetsen uppåt) och bromsar in i bilden av fatet. Nöten landar efter 0,6 s bland de andra och de rycker till. Det är den översta nöten på fatet, så skatan äter den sedan. `LENNART_FALL=0` ger tillbaka den gamla panoreringen (`verktyg/panorering_14.py`). Lennarts tassar öppnas aldrig i videon; nöten dyker upp under dem mitt i rörelsen.
- **Inköpen:** sakerna i kanterna av 4.1 och de fem filamentfärgerna kommer från kvittot och Marcus egen lista. Alla delar är generiska modeller. Panoreringen in från 3.2 läggs på de första sju rutorna med `verktyg/panorering_41.py` efter renderingen.
- **Byggklippen i monteringen:** `verktyg/byggklipp_6.py` lägger fyra klipp i vita ramar bakom huset i 6.1–6.2. De poppar upp och krymper bort på musikens slag (ca 99 slag/min) och är borta när kameran åker nära, ca 9 s in. Klippen görs lite mjuka, mörkare, kallare och mindre mättade (`KLIPP_VF`), så att huset är skarpast i bilden. Huset hålls överst med en mask som `akt_montering.py` renderar i maskläge (`LENNART_MASK=1`, bara alfa, går snabbt). Klippen läses från en mapp med `1.mp4`–`4.mp4`, utan ljud. När de riktiga klippen finns räcker det att köra skriptet igen, utan att rendera om huset. Platshållarna ligger lokalt i `byggklipp/platshallare/` och committas inte.
- **Munstycket i designen:** `akt_design.py` låter ett litet munstycke växa fram ur chattfönstrets underkant 5,3–5,9 s. Det är varmgrått som fönstret med en tunn ring i Claudes orange. Det vrider sig mjukt mot pappret, följer linjen som sveper över det (ljuset kommer ur spetsen), vrids tillbaka och krymper bort 9,45–9,95 s. Alla rörelser börjar och slutar mjukt (`sms`). Formen väljs med `LENNART_MUNSTYCKE_VARIANT` (A kon, B lins, C skrivarhuvud, D kapsel, D är vald) och `LENNART_MUNSTYCKE=0` stänger av det.
- **Delarna i 0.4:** `oppning.py` lägger varje lös bit plant i sin tunnaste riktning (den sida av höljet som ger lägst höjd), med långsidan längs x. Delarna sorteras i sex grupper i två rader: stomme, tak och bas bak, skål, elektronik och inredning fram. Skärmramen, som kameran åker ner genom, ligger i inredningen längst till höger. Husets stomme ligger på rygg som ett rör till vänster, och 0.4 börjar inne i den. Elektroniken är samma generiska modeller som i inköpen och läses från `elektronik.blend`, som görs med `blender -b -P verktyg/elektronik_export.py`. Ändras modellerna i `akt_inkop.py` ska exporten köras om. Numren 01–48 bredvid husets delar stängs av med `LENNART_NUMMER=0`.
- **Varianter av 0.3 (prov 17/11):** `LENNART_03` i `oppning.py` väljer K (nuvarande genomskärning med glashuset, i filmen), S (snittet: rakt från sidan utan perspektiv, bara mekaniken, snittskraffering på snittytorna), M (makro med fartramp: kort skärpedjup, slowmotion när nöten släpper ur hjulet) eller H (kameran rullar med doseringshjulet). Varianterna renderas med rörelseoskärpa. I M ändras mekanikens tajming, så ljudeffekterna behöver flyttas om den väljs. Bara K används i filmen tills Marcus valt.
- **Varianter av 0.4 (prov 17/11):** `LENNART_04` i `oppning.py` väljer K (byggsatsen, i filmen), A (en lång linje som slutar genom stommen och ner i ramen), B (byggsatsen, slutar på LED-skärmen som tänds), C (ovanifrån), D (golvet är en släckt LED-skärm, kameran dyker in i pixlarna) eller E (en grön skanning). Marcus valde D (17/11), som nu är förvalt och ligger i filmen. Byggsatsen i grupper (K) och elektroniken används bara av varianterna K, B och E; D visar husets 48 delar utan elektroniken.
- **Nötterna:** platserna räknas fram mot modellens riktiga form (`verktyg/notmagasin.py`, `verktyg/notfat.py`).
- **Bildrutor:** när bara en del av en scen ändras renderas bara de bildrutorna om. Bildrutorna finns inte i repot, så ta fram de övriga ur scenens mp4 med `ffmpeg -i "Lennart - del 3 designen v6.mp4" ut/%04d.jpg` först.
