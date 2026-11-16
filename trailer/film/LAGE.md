# Filmen – läget

Senast uppdaterad 2026-11-16. Skriven för att arbetet ska kunna fortsätta på vilken dator som helst, och av vilken session som helst.

## Beslut som gäller

- Berättarrösten är Marcus egen (`full recording.m4a`). Rösten bearbetas lokalt och skickas aldrig till någon tjänst.
- Huset får inte visas före del 3. Del 0 visar bara skärmen, gluggen, mekaniken i genomskärning och delarna utspridda på golvet.
- Luckan öppnas först, sedan rullar nöten.
- I filmen visas bildigenkänningen som ett moln. Var den faktiskt körs är fortfarande ett öppet beslut, se `docs/beslut/bildigenkanning.md`. Ändras beslutet behöver del 2 ändras.
- Inga toningar mellan klipp. Övergångarna bärs av kamerarörelser, matchklipp och former som fortsätter in i nästa bild.
- Rekonstruktioner i 3D märks som sådana. Inga påhittade konstruktionsdetaljer visas som verkliga.
- Klippens längder följer rösten. Ändras en scen ska dess klipp ha samma längd, annars hamnar rösten fel. Tiderna står i `SEG` i `verktyg/ljudmix.mjs`.

## Delarna

| Del | Innehåll | Läge |
|---|---|---|
| 0 Öppningen | Skärmen, gluggen, nötens väg, 48 delar, VERIFIERAR, titeln | Klar. Fullt nötmagasin, pixlar på skärmen, punkterna tänds på pipen. |
| 1 Lennart | Riktiga mobilklipp | Klar. Klipp 1.4 fryser och zoomar in på nöten i slutet. |
| 2 Problemet och planen | Fat, skata, kamera i sladd, moln, ja och nej | Klar. Fatet snurrar vid nej, nötterna vilar på riktigt. |
| 3 Designen | Claude-fönstret ritar huset, huset reser sig | Klar |
| 4 Inköpen | Komponenterna på blå yta, filamentet | Klar |
| 5 Utskriften | Slicern (5.1) och utskriftsväggen (5.2–5.3) | 5.1 är en stillbild. Väggen visar platshållare tills de riktiga timelapse-klippen finns. |
| 6 Monteringen | Sprängskiss, delarna hittar hem | Första renderingen. Elektroniken från inköpen saknas. |
| 7 På riktigt | Huset ute, fågel nekas, Lennart får en nöt | Väntar på riktig film. Stillbilder tills dess. |

## Övergångar

| Skarv | Hur |
|---|---|
| 0.3 → 0.4 | Snabb tilt nerför skålen, 0.4 börjar med en tilt upp från golvet |
| 0.4 → 0.5 | Kameran lägger sig ovanför skärmramen på golvet, i samma utsnitt som skärmen i 0.5 |
| 0.5 → 0.6 | In i skärmens pixlar, titeln tänds i samma rutnät (`verktyg/titel.py`) |
| 1.4 → 2.1 | Matchklipp: nöten i tassarna blir en 3D-hasselnöt på samma plats i bilden |
| 2.6 → 3.1 | Kameran tittar upp förbi molnet, 3.1 kommer uppifrån ner mot fönstret |
| 3.2 → 4.1 | Snabb panorering, gjord i efterhand på bildrutorna |
| 4.2 → 5.1 | In i filamentrullens svarta nav |
| 5.3 → 6.1 | Utskriftsväggen öppnar sig som dörrar |
| 6.3 → 7.1 | Planerad: skärmens sken i 3D blir skärmens sken på det riktiga huset |

## Nästa steg

1. Timelapse-klippen från skrivaren (10–13 st) i `timelapse/`, sedan renderas `akt_utskrift.py` om med dem.
2. Riktig film till del 7 när huset står ute.
3. Elektroniken i monteringen (del 6).
4. Slicern (5.1) som rörlig bild i stället för stillbild.
5. Storyboardens röstspalt har fortfarande den gamla manustexten, inte orden i inspelningen.

## Att kontrollera före publicering

- Sunos villkor för musiken med Marcus abonnemang [verifiera].
- Claude-logotypen i del 3 är en egen ritad tolkning. Om Anthropics logotyp får användas så [verifiera].

## Hur saker är gjorda

- **Rösten:** `verktyg/rost.py` jämnar ut nivån fras för fras och sänker andetag. Sedan `ljud/rostkedja.txt` i ffmpeg: klickborttagning, EQ, de-esser, multibandkompressor, kompressorer, lätt mättnad och limiter. Rösten ligger runt −19 LUFS och mixen runt −15 LUFS.
- **Musiken:** viker i mellanregistret när rösten talar (`sidechaincompress` per band).
- **Effekterna:** syntetiseras i `verktyg/effekter.py`, eller hämtas ur Kenneys ljudpaket (CC0). Tiderna står i `FX` i `ljudmix.mjs`, räknat från varje klipps början.
- **Nötterna:** platserna räknas fram mot modellens riktiga form (`verktyg/notmagasin.py`, `verktyg/notfat.py`).
- **Bildrutor:** när bara en del av en scen ändras renderas bara de bildrutorna om. Bildrutorna finns inte i repot, så ta fram de övriga ur scenens mp4 med `ffmpeg -i "Lennart - del 3 designen v5.mp4" ut/%04d.jpg` först.
