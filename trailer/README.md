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
