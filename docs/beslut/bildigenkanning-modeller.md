# Underlag: vilken modell för lokal igenkänning på Pi 5

**Datum:** 2026-11-20
**Status:** Underlag. Marcus har inte valt modell.
**Hur det togs fram:** en hjälpagent (AI) sökte och läste källor på webben på uppdrag i Claude Code-sessionen. Siffror och tider är inte mätta på Marcus Pi. Allt markerat [verifiera] saknar källa eller ska mätas. Påståenden om licenser, särskilt AGPL, ska granskas innan de används [kräver granskning].

Bakgrund och beslutet att köra lokalt: [bildigenkanning.md](bildigenkanning.md).

## Färdiga modeller

| Modell | Klasser som är relevanta här | Licens | Pi 5-CPU |
|---|---|---|---|
| **YOLOv8n/s tränad på Open Images V7** (`yolov8n-oiv7`, `yolov8s-oiv7`), Ultralytics | **Squirrel**, Bird, Magpie, Sparrow, Raven, Person/Man/Woman/Human face, Cat, Hedgehog, Mouse, Fox. Saknas: kaja, kråka, duva, mesar, nötväcka, koltrast, råtta, mård (blir i bästa fall "Bird"). | AGPL-3.0 (kod och vikter) | Ingen publicerad mätning. Grov uppskattning 100–250 ms per bild [verifiera] |
| **MegaDetector v6** (Microsoft/Pytorch-Wildlife) | Bara animal, person, vehicle. Passar som steg 1. | MDV6-mit-yolov9-c: MIT. MDV6-apa-rtdetr-c: Apache-2.0. MDV6-yolov10-c: AGPL-3.0. | Ingen publicerad mätning [verifiera] |
| **SpeciesNet** (Google) | Klassificerare på utsnitt med 2 498 etiketter, bl.a. eurasian red squirrel, common magpie, kaja, kråka, nötskrika, ringduva, nötväcka, koltrast, igelkott, mård, katt, brun råtta, human | Apache-2.0 | EfficientNet V2 M (480 px), ONNX 112–224 MB. Troligen sekunder per bild [verifiera] |
| DeepFaune (CNRS) | squirrel, bird, cat, hedgehog, mustelid m.fl. | Oklart om CC BY-SA eller CC BY-NC-SA [verifiera] | Troligen för tung (ViT-L) |
| RF-DETR (Roboflow) | Bara COCO, ingen ekorre. Intressant vid egen träning. | Apache-2.0 | Okänd [verifiera] |

Källor: Ultralytics [open-images-v7.yaml](https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/open-images-v7.yaml) och [Pi-guide](https://raw.githubusercontent.com/ultralytics/ultralytics/main/docs/en/guides/raspberry-pi.md), [MegaDetector Model Zoo](https://microsoft.github.io/MegaDetector/model_zoo/), [SpeciesNet](https://raw.githubusercontent.com/google/cameratrapai/main/README.md), [Open Images boxable-klasser](https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv).

Referens för hastighet: Ultralytics mäter YOLO26n (COCO, 640 px) till 67 ms per bild med NCNN på Pi 5, bara inferens.

## Roboflow Universe

Sidorna gick inte att hämta automatiskt, så uppgifterna kommer från sökträffar [verifiera allt per projekt]:

- [squirrels_in_my_garden](https://universe.roboflow.com/merrick-johansen/squirrels_in_my_garden): trädgårdsbilder med ekorre, CC BY 4.0, ca 1 600 bilder.
- [animal-detection-in-the-wild](https://universe.roboflow.com/thesis-project-mlwer/animal-detection-in-the-wild): bird, cat, dog, hedgehog, marten, rodent. CC BY 4.0. Ingen ekorre.
- Flera små skatprojekt med varierande licens och kvalitet.
- Roboflow Inference (Apache-2.0 för kärnan) kan köras på Pi 5. Modellerna följer sin egen licens. Gratisnivån ger 10 credits per månad (räcker till "~30 träningar" enligt Roboflow). API-nyckel behövs för att hämta vikter [verifiera om den behövs vid varje start].

## Öppna data om egen träning behövs

- **Open Images V7** (annoteringar CC BY 4.0, bilder CC BY 2.0): Squirrel 1 810 bilder i train, Magpie 123, Bird 18 525, Hedgehog 231, Cat 12 516, Person 248 384. Kan hämtas per klass med FiftyOne.
- **iNaturalist** får bara användas icke-kommersiellt och bilderna får inte spridas, alltså inte läggas i det publika repot [kräver granskning].
- **Egna klipp från uteplatsen** är troligen viktigast: plocka ut 1–2 bilder per sekund, låt en färdig detektor föreslå rutor, och rätta sedan i Roboflow. Dela upp i träning och test per klipp och dag, inte per bild.
- **Träning** kan inte göras på Pi:n. Alternativen är Google Colab, Kaggle och Roboflows gratisträning.

## Två steg eller en detektor

| | A. Tvåsteg: generell detektor (MegaDetector) + liten klassificerare "ekorre/annat" | B. En detektor (ekorre, fågel, annat djur, person) |
|---|---|---|
| Okända djur | Fångas som "animal" och blir "annat", alltså DENIED | Kan missas, men regeln "bara säker ekorre ger nöt" ger samma utfall |
| Människor | Robust, MegaDetector är tränad på viltkameror | Kräver person-exempel (Open Images har många) |
| Arbete | Två modeller | En modell |
| Licens | Kan bli helt MIT/Apache | YOLO från Ultralytics är AGPL-3.0 |

## Agentens rekommendation

1. **Först:** prova `yolov8n-oiv7` (och `yolov8s-oiv7`) utan träning på de märkta klippen och mät tiden per bild på Pi:n.
2. **Beslutsregel:** Squirrel över en tröskel i minst 2 av 3 bilder och ingen människa ger GRANTED. Allt annat ger DENIED. En träff på en människa spärrar publicering.
3. **Reserv:** finjustera en liten detektor (YOLO26n, eller RF-DETR-N för Apache-licens) med egna klipp och utdrag ur Open Images.
4. **Senare:** tvåsteg med MDV6-mit-yolov9-c (MIT) och en liten klassificerare.

## Licensfrågan

Repot har ännu ingen licens (README: "Licens: [Beslutas]"). Med en Ultralytics-modell blir AGPL-3.0 eller GPL-3.0 för repot den enkla vägen. MIT för hela repot går dåligt ihop med AGPL-koden [kräver granskning].
