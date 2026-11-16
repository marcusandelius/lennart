# Lennarts matstation – underlag för trailer

Det här är hela huset som 3D-modell, plus bilder som kan användas i en trailer. Allt är version 7 av modellen.

## Filer

- `lennarts-matstation.glb` – hela huset monterat, 48 delar som egna objekt med namn och färg.
- `delar.json` – alla delar med grupp, färg och eventuell vridpunkt i millimeter.
- `dekal-lennart.png`, `dekal-skata.png` – klisterdekalerna från demon, med genomskinlig bakgrund.
- `skarm-vantar.png`, `skarm-verifierar.png`, `skarm-access-granted.png`, `skarm-access-denied.png` – skärmens fyra lägen.

## Import i Blender

Använd File > Import > glTF 2.0. Modellen är i meter, och efter importen pekar Z uppåt och husets framsida mot −Y. Mittlinjen ligger på X = 0.

## Delar som rör sig

| Rörelse | Objekt | Hur |
|---|---|---|
| Luckan öppnas | `lucka`, `lucka_vit` | Origo sitter i gångjärnet. Vrid kring X till −95° för helt öppen. |
| Doseringshjulet släpper en nöt | `doserhjul` | Origo sitter i axeln. Vrid kring X till +130° och tillbaka. |
| Taket lyfts av | `tak_v`, `tak_v_vit`, `tak_h`, `tak_h_vit`, `skorsten`, `skorsten_krage`, `takrannor`, `takpackning`, `nockkilar` | Flytta rakt upp längs Z, ungefär 0,10–0,15 m. |

Övriga delar har origo i husets nollpunkt och står på rätt plats från början.

## Skärmen

Skärmen syns genom skärmramen på framsidan, mitt på huset (X = 0), ungefär 0,09–0,13 m över marken. Lägg en av skärmbilderna på ett plan precis bakom skärmramens öppning, vänt mot −Y.

## Delarna per grupp

- **Kropp:** kropp, kropp_vit, fonsterrutor, solskydd, solskydd_vit, kropp_packning, blomlador, blomlador_vaxter, blomlador_blommor_rod, blomlador_blommor_vit, stupror, stupror_vit, kropp_sockel
- **Tak:** tak_v, tak_v_vit, tak_h, tak_h_vit, skorsten, skorsten_krage, takrannor, takpackning, nockkilar
- **Bas:** bas, framgard, framgard_gras, framgard_stenar, framgard_platta, grasmatta, stenar, bottenplatta, fotter
- **Skål:** skal, skal_vit, lucka, lucka_vit, servokapa, servopackning
- **Inredning:** kamerafaste, elektroniklada, elpackning, monteringsplatta, skarmram, skarmklamma, genomforingar, ellock, doserhus, doserhjul, notmagasin

## Mått

Huset är cirka 0,31 m högt med skorsten och står på en bas som är cirka 0,22 m bred. Pedestalen och uteplatsen ingår inte.

## Filmen

Trailern för bidraget, cirka 3 minuter. Allt i 3D renderas i Blender med Python-skript, och ljudet mixas med ffmpeg. Storyboarden är en webbsida med alla klipp. Var filmen står och vad som återstår finns i [film/LAGE.md](film/LAGE.md).

### Mappar

| Mapp eller fil | Innehåll |
|---|---|
| `film/*.py` | En Blender-scen per del: `oppning.py` (0), `akt_plan.py` (2), `akt_design.py` (3), `akt_inkop.py` (4), `akt_utskrift.py` (5), `akt_montering.py` (6) |
| `film/verktyg/` | Byggskript: `ljudmix.mjs` (röst, musik, effekter, mix), `arbetskopia.mjs` (hela filmen), `effekter.py`, `musik.py`, `rost.py`, `titel.py`, `notmagasin.py`, `notfat.py` |
| `film/Lennart - *.mp4` | Senaste renderade versionen av varje del, och hela filmen i 720p |
| `film/ljud/` | Röstkedjan (`rostkedja.txt`), Whisper-utskriften av rösten och Kenneys ljudpaket |
| `film/timelapse/` | Timelapse-klippen från skrivaren (just nu tre platshållarbilder) |
| `storyboard/` | `storyboard.html`, ett klipp per scen (`clips/`) och stillbilder (`frames/`) |
| `full recording.m4a` | Berättarrösten, inspelad av Marcus |
| `System Online.mp3` | Musiken, gjord av Marcus i Suno |
| `PXL_*.mp4`, `VID-*.mp4`, `1000007512.mp4` | Riktiga klipp på Lennart till del 1 |

Ljud och video ligger i **Git LFS**. Renderade bildrutor, Whisper-modellen och mellanfiler (wav) finns inte i repot. De återskapas av skripten.

### Komma igång på en ny dator

1. Installera [Git LFS](https://git-lfs.com), [Blender 5.2](https://www.blender.org), [ffmpeg](https://ffmpeg.org) och [Node.js](https://nodejs.org).
2. Klona repot. Kör `git lfs pull` om ljud och video ser ut som små textfiler.
3. Bygg ljudet och arbetskopian: `node trailer/film/verktyg/ljudmix.mjs`
4. Bygg hela filmen i 720p: `node trailer/film/verktyg/arbetskopia.mjs --hel`

Skripten letar upp Blenders Python själva. Hittas den inte, sätt miljövariabeln `BLENDER_PYTHON` till sökvägen.

### Rendera en scen

```
blender -b -P trailer/film/akt_design.py -- <ut-mapp> 1280 48 [tider i sekunder ...]
```

Bredd 1280 och 48 samples är filmens kvalitet. Utan tider renderas alla bildrutor, och bildrutor som redan finns hoppas över. Utan grafikkort tar det många timmar.

### Typsnitt

Texterna i 3D-scenerna använder Consolas, Segoe UI och Georgia från Windows. De får inte spridas och ligger därför inte i repot. På andra datorer letar skripten efter liknande typsnitt, eller i `film/typsnitt/` (som inte versionshanteras), och använder annars Blenders inbyggda typsnitt. Texten i filmen ser då annorlunda ut.
