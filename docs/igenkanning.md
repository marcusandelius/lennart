# Bildigenkänning på Pi:n

**Status 2026-11-20:** test. Modellen är vald för ett första försök men är inte inbyggd i stationen än. Demoläget lottar fortfarande ACCESS GRANTED eller DENIED.

Beslut och underlag: [beslut/bildigenkanning.md](beslut/bildigenkanning.md) och [beslut/bildigenkanning-modeller.md](beslut/bildigenkanning-modeller.md).

## Modellen

**YOLOv8n tränad på Open Images V7** (`yolov8n-oiv7`) från Ultralytics. Den hittar 601 sorters objekt och ritar en ruta runt varje, bland annat **Squirrel**, Bird, Magpie, Person, Cat och Hedgehog. Licens: AGPL-3.0.

Stationen bryr sig bara om fyra grupper. Grupperingen finns i `GROUPS` i [`pi/detect.py`](../pi/detect.py):

| Grupp | Open Images-klasser (urval) |
|---|---|
| ekorre | Squirrel |
| fågel | Bird, Magpie, Sparrow, Raven, Woodpecker … |
| människa | Person, Man, Woman, Boy, Girl, Human face … |
| annat djur | Cat, Dog, Hedgehog, Mouse, Fox, Rabbit … |

## Varför ONNX

Modellen är tränad i PyTorch. PyTorch är stort och långsamt att installera på Pi:n och behövs inte för att *köra* modellen. Därför exporterades den till formatet ONNX, och på Pi:n körs den med **ONNX Runtime** (MIT-licens), som bara behöver numpy.

Exporten gjordes i Claude Code-sessionen 2026-11-20, i en Linux-container i molnet:

```bash
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
```

```bash
pip install ultralytics onnx onnxslim onnxruntime
```

```bash
yolo export model=yolov8n-oiv7.pt format=onnx imgsz=640 opset=17 simplify=True
```

Versioner: Python 3.13, torch 2.15.0+cpu, ultralytics 8.4.216, onnx 1.23.2, onnxslim 0.1.99, onnxruntime 1.32.0. Vikterna (`yolov8n-oiv7.pt`) hämtade Ultralytics automatiskt vid exporten.

| Fil | SHA-256 |
|---|---|
| `yolov8n-oiv7.pt` (hämtad, inte i repot) | `3851dfbf39ed2a076b1f39215cc22dba64eb5646f282bf964703785b0bed6a41` |
| `pi/models/yolov8n-oiv7.onnx` (13,6 MB) | `33b2922ca0018e3051208e59d1eb9592aaf133d033f7b380bc2572b3ac62d785` |

**Kontroll:** `pi/detect.py` kördes på Ultralytics två exempelbilder och gav samma klasser, nästan samma sannolikheter och rutor som Ultralytics egen `predict`. De små skillnaderna beror på att Ultralytics fyller ut bilden lite annorlunda. Tid per bild i molncontainern: cirka 80–150 ms. Pi 5 är inte mätt än.

## Testa på klippen på Pi:n

`pi/detect.py` kan köras från kommandoraden på inspelade klipp. Den plockar ut två bilder per sekund ur varje klipp och skriver ut den högsta sannolikheten per grupp och de troligaste klasserna, plus tid per bild. Resultatet sparas också som CSV i `~/lennart-data/detektering-test.csv`. Klippens namn är samma som i klipparkivet på lennart.cam, så resultatet kan jämföras med märkningen där.

ONNX Runtime installeras automatiskt vid deploy, i den virtuella miljön `~/lennart-app/.venv` (från `pi/requirements.txt`). Stationens program körs fortfarande med systemets Python och påverkas inte.

```bash
~/lennart-app/.venv/bin/python ~/lennart-app/detect.py --limit 20
```

## Plan för beslutet ekorre eller inte

Förslag, inte byggt. Trösklarna ska provas fram på riktiga klipp:

- **ACCESS GRANTED** bara om ekorre syns över tröskeln i minst 2 av 3 bilder **och** ingen människa syns.
- Allt annat ger **ACCESS DENIED**: fåglar, andra djur, okända djur och osäkra fall. Utan säkert svar blir det ingen nöt.
- En bild där en människa syns publiceras aldrig.
