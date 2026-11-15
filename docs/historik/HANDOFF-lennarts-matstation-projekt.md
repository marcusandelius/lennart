# HANDOFF – Lennarts matstation

Skapad 2026-11-15 ur claude.ai-chatten om Lennarts matstation. Chattens exakta namn i claude.ai: [osäkert]. De två tidigare transkripten heter `lennart-matstation-projekt` och `lennarts-matstation-projekt`.

Källor för den här filen:

- Den här chatten, 2026-11-11 kl. 21.22 till 2026-11-15.
- Två sparade transkript av samma chatt före två komprimeringar: 2026-10-27 kl. 00.06–15.21, och 2026-10-27 kl. 15.22 till 2026-11-11 kl. 21.22.
- Filerna i arbetsmappen `/home/claude/fix` i chattens Linux-miljö, och filerna som levererades i `/mnt/user-data/outputs`.
- Tidsstämplarna i filnamnen på Marcus skärmdumpar, som är millisekunder sedan 1970 och har räknats om till svensk tid.

Allt som inte gick att belägga är märkt [osäkert].

> **Kontrollera innan repot görs publikt.** Filen innehåller Marcus namn och länkar till hans privata artefakter i claude.ai. Kontouppgifter och privata länkar till externa tjänster är utelämnade.

---

## 1. Projektet i korthet

**Vad:** en smart matstation för en ekorre, byggd som ett litet falurött hus med vita knutar. Den är ungefär 31 cm hög med skorsten och står på en pedestal på cirka 70 cm.

- En kamera känner igen ekorren och släpper då ut en hasselnöt till en skål med lucka.
- Andra djur, till exempel skator, får ingen nöt.
- En liten skärm visar ACCESS GRANTED i grönt för ekorren och ACCESS DENIED i rött för andra.
- Planen är en besökslogg med bild och tid, en incidentrapport vid nekade besök och en dashboard i stil med en säkerhetscentral. Dessutom en publik besöksliggare med bild på varje besök, under ett eget domännamn.

**För vem:** ekorren Lennart, som har besökt Marcus uteplats i Linköping nästan dagligen sedan början av sommaren 2026. Ägare och byggare är Marcus Andelius, kallad Macke.

**Varför:** fåglar stjäl Lennarts mat. Bygget är också Marcus bidrag till SweClockers och ASUS tävling "Gick inte. Nu går det.", där poängen är att skapa med AI. Marcus har inget CAD-program och ingen modelleringsvana, så hela 3D-modellen har Claude byggt i kod.

**Var:** utomhus under tak på uteplatsen, mot en vägg, från november till sommaren. Platsen har grönt räcke, wifi och eluttag.

**Läget 2026-11-15:**

- 3D-modellen är klar i version 7, med efterföljande ändringar.
- Delar skrivs ut på en Bambu Lab X2D Combo.
- Elektroniken från Electrokit har kommit.
- Ingen programvara för Raspberry Pi har skrivits än.

**Tävlingens ramar** från villkoren på https://projekt.sweclockers.com/asus/villkor:

- Bidrag lämnas in 16 oktober–30 november 2026 och kan ändras fram till att röstningen öppnar 1 december.
- Röstningen pågår till och med 13 december, och vinnaren presenteras 17 december.
- Bidraget ska visa vad som fanns före och vad som gjorts med AI från 16 oktober.
- Bidraget ska ange använda modeller, verktyg och bibliotek.
- Tokens ska redovisas, uppdelat på lokalt och i molnet, med en kort förklaring av hur de räknats.

---

## 2. Beslut, med datum och skäl

Datum är när beslutet togs i chatten. Saknas skälet i chatten står [osäkert].

| Datum | Beslut | Skäl |
|---|---|---|
| 2026-10-27 | Bygga en matstation där en kamera släpper ut nötter bara för ekorren | Fåglar stjäl Lennarts mat |
| [osäkert, troligen 2026-10-27] | Igenkänningen ska göras i molnet, inte lokalt | Enklast. Källa: Marcus minnesanteckningar. Det är [osäkert] om beslutet fortfarande gäller. |
| 2026-10-27 | Formen blir ett falurött hus med vita knutar och skorsten, tänkt 35 cm högt, som 3D-skrivs | Marcus val efter AI-genererade konceptbilder. Charm är viktigt. |
| 2026-10-27 | Claude bygger 3D-modellen i Python-kod och visar den i en interaktiv förhandsgranskning | Marcus har inget modelleringsprogram, och tävlingen handlar om att skapa med AI |
| 2026-10-27 | Pedestal på uteplatsen med en repstege från framgården ner till golvet | Ekorren ska kunna klättra upp. Om Lennart faktiskt använder stegen är [osäkert]. |
| 2026-10-27 | Ingen våg (lastcell och HX711). Kameran avgör ensam med 2–3 bilder per besök och läget VERIFIERAR vid osäkert svar. | Marcus valde att hoppa över vågen. Övrigt skäl [osäkert]. |
| 2026-10-27 | Ström via kabel från en 12 V-nätadapter. Ingen solpanel och inget batteri. | [osäkert] |
| 2026-10-27 | Blomlådor och stuprör på huset | Charm |
| 2026-10-28 | Alla föreslagna monteringsförbättringar byggs in ("kör på allt") | Enklare att bygga och serva |
| 2026-10-28 | ASA utomhus, TPU till packningar, grönt filament till gräset | Väderbeständighet. Ersattes delvis av PETG 2026-11-13, se nedan. |
| 2026-10-28 | AI-användningen redovisas i bidraget | Tävlingen går ut på att skapa med AI |
| 2026-10-28 | Tre större blommor per blomlåda | Inga för små detaljer, enklare men elegant |
| 2026-10-28 | Minihus i tre versioner för en testutskrift i PLA | Kul första test på den nya skrivaren |
| 2026-10-28 | Alla 3D-vyer ska gå att panorera med höger musknapp och scrollknappen | Marcus önskemål för alla framtida demovyer |
| 2026-11-11 | Delarna köps inför helgen. Electrokit-beställningen lades samma dag. | Utskriften skulle börja till helgen |
| 2026-11-11 | 4G via USB-modem och ett data-SIM i stället för wifi | SIM-kortet ligger ändå oanvänt |
| 2026-11-11 | Raspberry Pi 5 i stället för Pi 3A+ | Marcus äger redan en Pi 5 |
| 2026-11-11 | Budgeten höjdes från högst 3 000 kr till cirka 4 000 kr | Marcus beslut |
| 2026-11-11 | Snäppfästen, presspassningar, styrtappar och magneter i stället för lim. Undantag: klar silikon till kamerafönster och skärmglas. | Monteringen ska vara så enkel som möjligt |
| 2026-11-11 | Taket hålls av magneter och lyfts av för påfyllning. Elektroniken sitter på en monteringsplatta som dras rakt upp. | Enkel service |
| 2026-11-11 | Servona styrs via ett PCA9685-kort | Pi 5 har ny GPIO-hårdvara, och flera vanliga servobibliotek fungerar inte |
| 2026-11-11 | Förhandsgranskningen får flikarna 3D, Projektdokument, 3D-filer och Utskrift | Överblick över modell, dokument, filer och utskrift |
| 2026-11-11 | Doseringen byggs om: från en roterande skiva med fyra fickor till ett hjul med en ficka, som vrids 130° av ett servo | Marcus trodde att nötterna skulle fastna och föreslog ett vattenhjul. Ett halvt varv ger exakt en nöt, och det blir 3 delar i stället för 6. |
| 2026-11-11 | Nötter ska vara 18–22 mm | 22 mm är det största som går fritt. Under 18 mm kan två nötter hamna i fickan. |
| 2026-11-11 | Stengrund och fönsteröverstycken på huset | Mer charm utan att bygget blir svårare |
| 2026-11-11 | Demon får röntgenvy, knapp för att lyfta taket och en monteringsvisning i tio steg | Marcus ville se hur saker fungerar och hur monteringen går till |
| 2026-11-11 | Tre förslag på dörr i stället för skål provades | Marcus ville prova en dörr |
| 2026-11-12 | Dörrförslagen förkastades. Skålen med lucka behålls. | "Gillade öppningen som var" |
| 2026-11-12 | Demon: högre 3D-vy, ny panel, scener som spelas upp och monteringen som spelas upp av sig själv | Marcus önskemål |
| [osäkert, troligen 2026-11-12] | I demon spelas Lennart av en klisterdekal som hålls av en hand. Han äter med huvudet i skålen, utan nöt i munnen. Skatan blir också en dekal. | Kul och charmigt. Handen fick inte klippa in i huset eller i ekorren. |
| 2026-11-13 | Kroppen skrivs ut först, som test | Marcus val |
| 2026-11-13 | PETG i alla tre färger i stället för ASA | PETG-rullarna satt i skrivaren, och Bambu Studio spärrar blandning av hög- och lågtemperaturfilament |
| 2026-11-13 | Rött och grått på det ena munstycket, vitt på det andra | Tiden sjönk enligt Bambu Studio från 29 h 51 min till 20 h 56 min |
| 2026-11-13 | Utskrift utan stöd | Bara broar på 14–40 mm och utstick på 2–3 mm. Trädstöd hade lämnat märken på fasaden. |
| 2026-11-13 | Kroppen flyttades ut ur den grå remsan "Left nozzle only area" | Det vita munstycket når inte dit |
| 2026-11-13 | Separata vita detaljer ritades, men Marcus ångrade sig och lät testutskriften gå. Modellen återställdes. | "Får hålla tummarna" |
| 2026-11-14 | Utskriften fick gå vidare fast dörröverstycket hängde fritt | Felet var begränsat till 6 mm höjd |
| 2026-11-14 | Rensningstornet välte vid 89 %. Det togs bort och utskriften fortsatte. | Bara cirka 17 mm med vitt återstod |
| 2026-11-14 | Hela huset exporterades som GLB för en trailer i Blender via Claude Code | Marcus ska göra en trailer |
| 2026-11-14 | Nästa utskrifter blev elektroniklådan med lock och monteringsplatta, och sedan basen | Elektroniken ska provas, och basen behövs för kroppen |
| 2026-11-14 | Basen skrevs ut i grön PETG | Projektet stod på ABS, men rullen visade sig vara PETG |
| 2026-11-14 | Utskriftsfliken bockar av utskrivna plattor | Marcus vill hålla koll på vad som är utskrivet |
| 2026-11-15 | Ny kropp i bara rött och grått. De vita detaljerna skrivs ut separat och trycks in i fickor med tappar. | Färgbytena kostade ungefär halva tiden, dörröverstycket hängde fritt och rensningstornet välte |
| 2026-11-15 | Nöthålet breddas från 27 till 31 mm, och skålens bakvägg lika mycket | Marcus vill slippa att nötter fastnar |
| 2026-11-15 | Tre avbrutna plankspår runt kameran förlängs upp till solskyddet | Marcus såg att ett spår inte nådde upp |
| 2026-11-15 | Toleranstestet skrivs ut före den nya kroppen | Tapparna och fickorna bygger på passningarna |
| 2026-11-15 | Kamerafäste, skärmklämma och skärmram skrivs ut för ett elektroniktest i den gamla kroppen | Prova kamera och skärm med Pi 5 |

Konstaterat i chatten, inte beslutat:

- **2026-11-15:** den största nöten som går igenom är 22 mm. Det är doseringshjulets ficka som begränsar, inte nöthålet.
- **2026-11-15:** valnötter utan skal passar inte doseringen, eftersom halvorna är för stora och oregelbundna.

---

## 3. Hårdvara och delar

### 3.1 Fanns innan projektet

Detta fanns före tävlingen:

- **Hos Marcus:** Raspberry Pi 5 (minnesstorlek [osäkert]) och en lödpenna med spetssats för gänginsatser.
- **Material:** Ruthex-insatser, cirka 30 M3 och 6 M4, silikagel, Wago 221, kopplingskablar, kabelskor och krympslang. När de skaffades är [osäkert].
- **SIM:** ett oanvänt data-SIM. Om det går på Telias eller Telenors nät är [osäkert].

### 3.2 Utrustning och köpta delar

**3D-skrivare:** Bambu Lab X2D Combo. Första utskriften för bygget startade 2026-11-13.

- Byggplatta 256 × 256 mm. En remsa på 20,5 mm når bara det vänstra munstycket.
- Två munstycken och två AMS 2 Pro.
- Bara en texturerad PEI-platta.

**Electrokit, beställt 2026-11-11.** Ordagrant ur Marcus orderfil:

| Art.nr | Antal | Namn | Pris kr/st |
|---|---|---|---|
| 41036261 | 1 | 2" LCD 320x240 for Raspberry Pi Pico 4x buttons | 199 |
| 41036144 | 10 | Screw Hex socket head cap M3x16 stainless steel A2 | 1,2 |
| 41036143 | 10 | Screw Hex socket head cap M3x12 stainless steel A2 | 1,1 |
| 41035709 | 1 | Analog servo 11kg 0.18s metal, high torque | 99 |
| 41024239 | 1 | LED spotlightring for Raspberry Pi Camera | 149 |
| 41023399 | 1 | Super Glue – cyanoacrylate 3g | 6,5 |
| 41023301 | 1 | DCDC-converter step-down 3.3V/5V 5A | 149 |
| 41020810 | 1 | Raspberry Pi CSI Camera cable 500mm | 55 |
| 41020804 | 1 | Active cooler for Raspberry Pi 5 | 89 |
| 41020241 | 1 | Raspberry Pi Camera Module 3 Wide | 449 |
| 41004709 | 1 | DC jack 2.1x5.5x9.5 to terminal block | 20 |
| 41019492 | 1 | DCDC-omvandlare 8-23V / 5V 3A | 129 |
| 41017694 | 2 | Electrolytic capacitor 1000uF 16V 105C 10x16mm | 4,5 |
| 41017525 | 1 | Servo tester 3 functions | 49 |
| 41016271 | 1 | Analog micro servo 2.8kg 0.09s metal (MG90S) | 79 |
| 41013141 | 1 | Analog servo 5kg 0.18s 360° | 179 |
| 41010952 | 3 | Cable gland M16 x 1.5 ø6mm | 7,5 |

Kommentarer:

- **Servot på 11 kg** är tänkt för doseringen och motsvarar MG996R i planen. Inköpslistan hade två, varav ett i reserv, men bara ett beställdes.
- **Servot på 5 kg, 360°** snurrar runt och vet inte sitt läge, så det passar inte doseringshjulet.
- **Kamerakabeln:** om den passar Pi 5:s smalare kontakt är [osäkert] och ska kontrolleras.
- **LED-ringen:** kamerafästet är inte ritat för den.

### 3.3 Planerat men inte köpt

Pris markerat med "?" är inte kontrollerat.

| Del | Antal | Pris | Till |
|---|---|---|---|
| PCA9685, I2C-servodrivkort | 1 | 60–100 kr? | Servostyrning från Pi 5 |
| Nätadapter 12 V (Akyga AK-TB-12) | 1 | 149 kr | Strömförsörjning, inomhus eller under tak |
| 12 V-kabel, 2 × 1,5 mm², för utomhusbruk | efter behov | ? | Från adaptern till stationen |
| 4G-modem Huawei E3372-325 | 1 | cirka 395 kr? | Uppkoppling. Stöder modemet SIM-kortets LTE-band? [osäkert] |
| Ventilationspluggar M12 med membran | 2 | ? | Elektroniklådan |
| Neodymmagneter 10 × 2 mm, N35 | 8 | cirka 50 kr? | Taket |
| Polykarbonat 3 mm | bit | ? | Kamerafönster Ø24 mm |
| Akryl eller polykarbonat 1 mm | bit | ? | Skärmglas 50 × 39 mm |
| M2-skruv 6–8 mm med mutter | 4 | ? | Kameran mot kamerafästet |
| M4-skruv och brickor, rostfria A2 | några | ? | Framgård och bottenplattor |
| Klar silikon, skumtejp, VHB-tejp | – | ? | Fönster, skärm och tryckklackar |
| Vinkeljärn och skruv | 2 | ? | Förankra pedestalen i väggen |
| Ballast, sand, grus eller stål | 2–3 kg | – | I basen |
| Hasselnötter i skal, 18–22 mm | – | – | Mat |
| Jordad utomhusskarv med jordfelsbrytare | om den saknas | ? | Elsäkerheten ska kontrolleras av en behörig person |
| Klar, UV-tålig lack i sprayburk | 1 | ? | Tak och kroppens nederkant |
| Små buntband | 1 påse | ? | Monteringsplattan |
| Rep 4–5 mm och rundstav | om stegen byggs | ? | Repstegen |
| Vattentätt mikroservo | 1 | 80–250 kr? | Möjlig ersättare för luckservot (MG90S är köpt) |

Uppskattad total enligt projektdokumentet: cirka 3 300–3 700 kr utan kabel. Den summan var inte kontrollerad.

### 3.4 Filament i skrivarens AMS

Enligt Marcus skärmdump 2026-11-14 kl. 22.58:

- **AMS 1:** A1 PLA (mörk grågrön), A2 PETG röd, A3 PETG svart, A4 PETG grå.
- **AMS 2:** B1 PLA beige, B2 PLA svart, B3 PETG grön, B4 PETG vit.
- **Extern hållare:** Ext-L TPU.

I tidigare listor fanns också Fiberon ASA-CF08 Dark Red, Bambu ASA röd och vit, PrimaSelect ASA grå och svart och TPU 95A. Var dessa finns nu är [osäkert].

### 3.5 Utskrivet hittills

| Datum | Del | Material | Kommentar |
|---|---|---|---|
| 2026-11-13–14 | Kroppen version 7 med inbyggda vita detaljer | PETG i rött, grått och vitt | Testkropp. Dörröverstycket hängde fritt, rensningstornet välte vid 89 % och vänster hörnbräda blev porös. Ska användas för elektroniktest. |
| 2026-11-14 | Elektroniklåda, lock och monteringsplatta | PETG, en färg | – |
| 2026-11-14–15 | Basen | Grön PETG | Utskriven över natten |
| 2026-11-15 | Bottenplattan | PETG [osäkert vilken färg] | – |
| 2026-11-15 | Toleranstestet | Grå PETG | Pågick när filen skrevs. Resultatet är [osäkert]. |
| [osäkert] | Kamerafäste, skärmklämma och skärmram | – | Filerna levererades 2026-11-15. Om de är utskrivna är [osäkert]. |

Om minihusen från 2026-10-28 skrevs ut är [osäkert].

---

## 4. Kod, konfiguration och kommandon

### 4.1 Läs först

- **Arbetsmappen var `/home/claude/fix`** i chattens Linux-miljö. Alla skript använder relativa sökvägar dit och skriver till `/mnt/user-data/outputs`. Byt sökvägar i repot.
- **Modellgeneratorn `house.py` finns inte kvar.** Version 1–6 av modellen byggdes av `/home/claude/model/house.py`, men den mappen fanns inte längre när den här filen skrevs. Delar av koden går bara att hitta som ändringar i transkripten, och det är [osäkert] om den går att återskapa helt.
- **Geometrin finns i stället som data.** Från version 7 bärs den av JSON-filer (`parts_v8.json` och framåt) med varje dels triangelnät i base64. Varje `patch*.py` läser en sådan fil och skriver nästa.
  - `parts_v8.json` är version 7 med inbyggda vita detaljer. Det är det som skrevs ut 2026-11-13 och det som finns i GLB-filen.
  - `parts_v11.json` är det aktuella läget: kropp i rött och grått, separata vita delar, 31 mm nöthål och förlängda spår.
- **Data är inte inkluderad här.** JSON-filerna med delar och plattor och STL-filerna är data, inte kod, och är totalt flera megabyte. I avsnitt 4.6 står hur de återskapas ur de levererade filerna.
- **Ordningen som filerna kördes i:**
  1. `patch2`–`patch7`, under modellens version 1–6.
  2. `patch8.py`: doseringshjul, stengrund och överstycken.
  3. `export8.py`: STL-filer.
  4. `plates8.py`: plattlayouter.
  5. `page8.py`, `page8b.py`: förhandsgranskningen.
  6. `patch9.py`, `page9.py`: dörrförslagen, som senare förkastades.
  7. `page10`–`page13.py`: demo, dekal och hand.
  8. `patch10.py`: separata vita delar, senare återställt.
  9. Engångsskripten i avsnitt 4.4.
  10. `patch11.py` och `plates8.py`.
  11. Engångsskripten 02–05 och 09.
- **Engångsskript saknas delvis.** Många kontroller, renderingar och små sidändringar kördes som engångsskript direkt i terminalen och sparades aldrig som filer. De som ändrade modellen eller filerna 2026-11-14–15 finns i avsnitt 4.4. Övriga sådana skript, framför allt rena kontroller och skärmdumpar, är inte återgivna [osäkert vilka exakt].
- **Ingen kod för Raspberry Pi finns.** Igenkänning, servostyrning, skärm, logg och systemd-tjänst är inte påbörjade.

### 4.2 Miljö och kommandon som användes

Python-paket som användes i miljön. Installationskommandona för de flesta är [osäkert], eftersom paketen fanns förinstallerade.

```
manifold3d  trimesh  numpy  shapely  rectpack  matplotlib  Pillow  playwright  markdown
```

Uttryckligen installerat i chatten:

```bash
pip install pymeshfix --break-system-packages -q
```

`pymeshfix` provades 2026-11-13 för att laga kroppens nät, men resultatet förstörde geometrin och användes inte.

För skärmdumpar användes en lokal kopia av three.js r128 i `/home/claude/fix/npm/node_modules/three/build/three.min.js`. Exakt installationskommando är [osäkert]. Playwright startades så här, ordagrant ur skripten:

```python
b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
```

Inställningar i Bambu Studio som Marcus använde eller fick rådet att använda:

- **Lagerhöjd:** 0,20 mm.
- **Väggar:** 3–4 vägglinjer för delar med gänginsatser (fliken Styrka).
- **Kammare:** inte varmare än cirka 45 °C för PETG, och utan kammarvärme. Lucka eller dörr på glänt, men inget drag.
- **Stöd:** ingen.
- **Brätte:** "Endast yttre brätte", 5–8 mm, för stora platta delar (fliken Övrigt).
- **Flerfärg:** ladda filerna som "ett objekt med flera delar" och lägg ingenting i remsan "Left nozzle only area".
- **AMS:** synkronisera med "Skriver över" när profilens filamenttyp inte stämmer med AMS:en.
- **Gänginsatser:** lödpennan på 220–240 °C för PETG.


### 4.3 Python-filer i arbetsmappen

Alla filer i `/home/claude/fix`, ordagrant. Beskrivningen före varje fil är min, och koden är oförändrad.

**Fil: `model/lib.py`** – Gemensamma hjälpfunktioner: läsa och skriva delar i parts_v*.json, booleska kroppar och husets grundmått.

`````python
import json, base64, numpy as np, trimesh, math
from manifold3d import Manifold, Mesh, CrossSection
def load(fn='parts_v5.json'):
    parts=json.load(open(fn)); return parts, {p['name']:p for p in parts}
def T(P,n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=True)
def M(P,n):
    t=T(P,n); return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def toT(m, minvol=0.5):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    cs=[c for c in t.split(only_watertight=False) if abs(c.volume)>=minvol]
    return trimesh.util.concatenate(cs) if cs else t
def put(parts,P,n,m,**kw):
    t=toT(m)
    if n not in P: P[n]=dict(name=n,**kw); parts.append(P[n])
    else: P[n].update(kw)
    P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
    return t
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylz(cx,cy,z0,z1,r,seg=40): return Manifold.cylinder(z1-z0,r,r,seg).translate([cx,cy,z0])
def cyly(cx,cz,y0,y1,r,seg=32): return Manifold.cylinder(y1-y0,r,r,seg).rotate([-90,0,0]).translate([cx,y0,cz])
def cylx(cy,cz,x0,x1,r,seg=32): return Manifold.cylinder(x1-x0,r,r,seg).rotate([0,90,0]).translate([x0,cy,cz])
def ccw(pts):
    a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))); return pts if a>0 else pts[::-1]
def xz_prism(pts,y0,y1): return CrossSection([ccw(pts)]).extrude(y1-y0).rotate([90,0,0]).translate([0,y1,0])
def yz_prism(pts,x0,x1): return CrossSection([ccw(pts)]).extrude(x1-x0).rotate([90,0,90]).translate([x0,0,0])
HW,D,TW,PEAK=85.0,150.0,3.2,240.0; K=80/85; zu=lambda x: PEAK-abs(x)*K
def bb(m): b=m.bounding_box(); return np.round(np.array(b).reshape(2,3),1)
`````

**Fil: `model/patch2.py`** – Ändringsrunda under version 1–6 (2026-10-27–11-11): parts_new.json → parts_v2.json.

`````python
import json, base64, numpy as np, trimesh, zipfile, os, math, re
from manifold3d import Manifold, Mesh, CrossSection
parts=json.load(open('parts_new.json'))
P={p['name']:p for p in parts}
def get(n):
    p=P[n]; v=np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3); f=np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3)
    t=trimesh.Trimesh(v,f,process=True)
    return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def tm(m):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    comps=[c for c in t.split(only_watertight=False) if abs(c.volume)>=1.0]; return trimesh.util.concatenate(comps)
def put(n, m, color=None, group=None, file=None, note=None):
    t=tm(m)
    if n not in P:
        P[n]=dict(name=n,color=color,group=group,file=file,note=note); parts.append(P[n])
    P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
    return t
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylx(cy,cz,x0,x1,r,seg=32): return Manifold.cylinder(x1-x0,r,r,seg).rotate([0,90,0]).translate([x0,cy,cz])
def cylz(cx,cy,z0,z1,r,seg=48): return Manifold.cylinder(z1-z0,r,r,seg).translate([cx,cy,z0])
def ccw(pts):
    a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))); return pts if a>0 else pts[::-1]
def xz_prism(pts,y0,y1): return CrossSection([ccw(pts)]).extrude(y1-y0).rotate([90,0,0]).translate([0,y1,0])
HW,D,T,PEAK=85.0,150.0,3.2,240.0; K=80/85; zu=lambda x: PEAK-abs(x)*K

# 1) servostolpen: dräneringshål, ny hatt med kjol, TPU-packning
put('skal_vit', get('skal_vit') - cylx(-15, 19.5, 63.4, 66.6, 1.5))
hat = Manifold.batch_hull([box(38.6,67.4,-31.4,-0.2,41,43), box(49,57,-19.5,-11.5,49,49.6)])
hat = hat + (box(38.6,67.4,-31.4,-0.2,36,41) - box(39.8,66.2,-30.2,1,35,42))      # kjol runt servohuset på tre sidor
put('servokapa', hat)
P['servokapa']['note']='Vit ASA, kjolen leder vattnet förbi skarven'
put('servopackning', box(40,66,-30,-0.2,40,41) - box(42,64,-28,-2.4,39,42), '#2B2B2B','Skål','09b_stolphatt_packning_tpu.stl','TPU 95A, 1 mm, mellan servohus och hatt')

# 2) takskarven: djupare spår i takets undersida + TPU-list ovanpå gavelns läpp
def band(z_lo, z_hi, xmax=HW+0.5):
    return [(-xmax, zu(xmax)+z_lo), (0, zu(0)+z_lo), (xmax, zu(xmax)+z_lo), (xmax, zu(xmax)+z_hi), (0, zu(0)+z_hi), (-xmax, zu(xmax)+z_hi)]
groove = xz_prism(band(-0.1, 2.3), -0.6, T+0.6) + xz_prism(band(-0.1, 2.3), D-T-0.6, D+0.6)
for n in ('tak_v','tak_h'): put(n, get(n) - groove)
strip = xz_prism(band(0.6, 2.25, HW+0.3), -0.45, T+0.45) + xz_prism(band(0.6, 2.25, HW+0.3), D-T-0.45, D+0.45)
put('takpackning', strip, '#2B2B2B', 'Tak', '06d_takpackning_tpu.stl', 'TPU 95A, fyra lister som läggs i takets spår')

# 3) TPU-genomföringar i elektroniklådan (två runda i botten, en avlång i taket)
def round_grommet(cx, cy, z_floor0, z_floor1):
    g = cylz(cx,cy,z_floor0-1.0,z_floor0,6.5) + cylz(cx,cy,z_floor0,z_floor1,4.45) + cylz(cx,cy,z_floor1,z_floor1+1.0,6.5)
    return g - cylz(cx,cy,z_floor0-2,z_floor1+2,2.2) - box(cx-0.3,cx+6.6,cy-0.15,cy+0.15,z_floor0-2,z_floor1+2)   # hål + slits
EZ0=74.0
gr = round_grommet(-20,132,EZ0,EZ0+2.4) + round_grommet(30,132,EZ0,EZ0+2.4)
top = (box(-13,13,120.5,135.5,170,171) + box(-10.95,10.95,122.55,133.45,167.6,170) + box(-13,13,120.5,135.5,166.6,167.6)) - box(-7,7,126.4,129.6,165,172) - box(-0.2,0.2,119,127,165,172)   # mittslits så den kan träs på kablarna
gr = gr + top
put('genomforingar', gr, '#2B2B2B', 'Inredning', '25_genomforingar_tpu.stl', 'TPU 95A, tätar kablarna in i elektroniklådan')
json.dump(parts, open('parts_v2.json','w'))

# ---- utskriftsfiler ----
def export_group(names, files, R=np.eye(4)):
    ms=[]
    for n in names:
        p=P[n]; v=np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3); f=np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3)
        ms.append(trimesh.Trimesh(v,f,process=False))
    allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    Tm=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for m,fn in zip(ms,files):
        mm=m.copy(); mm.apply_transform(Tm@R); mm.export('stl/'+fn)
n=np.sqrt(1+K*K)
export_group(['skal','skal_vit'],['07_farstukvist_rod.stl','07_farstukvist_vit.stl'])
export_group(['servokapa'],['09_stolphatt.stl'])
export_group(['servopackning'],['09b_stolphatt_packning_tpu.stl'])
export_group(['tak_v','tak_v_vit'],['06_tak_vanster_gra.stl','06_tak_vanster_vit.stl'], trimesh.geometry.align_vectors([K/n,0,-1/n],[0,0,-1]))
export_group(['tak_h','tak_h_vit'],['06b_tak_hoger_gra.stl','06b_tak_hoger_vit.stl'], trimesh.geometry.align_vectors([-K/n,0,-1/n],[0,0,-1]))
# takpackningen: fyra raka lister platt bredvid varandra
L = math.hypot(HW+0.3, (HW+0.3)*K)
strips=[trimesh.creation.box([L, T+0.9, 1.65]).apply_translation([L/2, i*7+ (T+0.9)/2, 0.825]) for i in range(4)]
trimesh.util.concatenate(strips).export('stl/06d_takpackning_tpu.stl')
# genomföringarna platt
g1=trimesh.creation.annulus(2.2, 6.5, 1.0); 
gt=tm(round_grommet(0,0,1.0,3.4)); gt.apply_translation([-gt.bounds[0][0], -gt.bounds[0][1], -gt.bounds[0][2]])
g2=gt.copy(); g2.apply_translation([16,0,0])
tp=tm(top); tp.apply_translation(-tp.bounds[0]); tp.apply_translation([0,18,0])
trimesh.util.concatenate([gt,g2,tp]).export('stl/25_genomforingar_tpu.stl')
print("klart", [p['name'] for p in parts][-4:])
`````

**Fil: `model/patch3.py`** – Ändringsrunda: parts_v2.json → parts_v3.json.

`````python
import json, base64, numpy as np, trimesh, zipfile, os
from manifold3d import Manifold, Mesh
parts=json.load(open('parts_v2.json')); P={p['name']:p for p in parts}
def get(n):
    p=P[n]; v=np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3); f=np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3)
    t=trimesh.Trimesh(v,f,process=True); return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def tm(m):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    return trimesh.util.concatenate([c for c in t.split(only_watertight=False) if abs(c.volume)>=1.0])
def put(n,m):
    t=tm(m); P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylx(cy,cz,x0,x1,r,seg=20): return Manifold.cylinder(x1-x0,r,r,seg).rotate([0,90,0]).translate([x0,cy,cz])
HW=85.0
fb=get('blomlador'); body=get('kropp')
hooks=Manifold(); pins=Manifold(); fill=Manifold()
for s in (1,-1):
    X=lambda a,b: (a,b) if s>0 else (-b,-a)
    for yp in (62,88):
        pins += cylx(yp,57,*X(HW-3.0,HW+0.05),1.55)            # gamla tappar bort
        fill += cylx(yp,57,*X(HW-2.75,HW-0.01),1.7)             # gamla hål i väggen fylls igen
    for y in (60.5,89.5):                                          # krokar som hakar över fönstrets nedre karm
        hooks += box(*X(HW+2.2,HW+3.8),y-2.5,y+2.5,56.0,72.0)    # arm upp från lådans botten, utanför karmen
        hooks += box(*X(HW+0.3,HW+3.8),y-2.5,y+2.5,70.3,72.0)    # överliggare som vilar på karmens överkant
fb=(fb-pins)+hooks
put('blomlador',fb)
put('blomlador_vaxter', get('blomlador_vaxter')-hooks.translate([0,0,0])-box(-200,200,0,0,0,0) if False else get('blomlador_vaxter')-Manifold.batch_hull([hooks]) if False else get('blomlador_vaxter')-hooks)
put('kropp', body+fill)
P['blomlador']['note']='Vit ASA, hängs på fönstrets nedre karm med två krokar – inget lim'
json.dump(parts,open('parts_v3.json','w'))
# kollisionskontroll mot karm, rutor, växter och blommor
for a,b in [('blomlador','kropp_vit'),('blomlador','fonsterrutor'),('blomlador','kropp'),('blomlador','blomlador_vaxter'),('blomlador','blomlador_blommor_rod'),('blomlador','blomlador_blommor_vit')]:
    print(f"{a} x {b}: {(get(a)^get(b)).volume():.2f} mm3")
# utskriftsfiler för grupp 21 (bara förflyttning) och kroppen (grupp 05)
def export_group(names,files):
    ms=[]
    for n in names:
        p=P[n]; ms.append(trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=False))
    allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
    T=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for m,f in zip(ms,files): mm=m.copy(); mm.apply_transform(T); mm.export('stl/'+f); print(f, mm.is_watertight)
export_group(['blomlador','blomlador_vaxter'],['21_blomlador_vit.stl','21_blomlador_gron.stl'])
export_group(['kropp','kropp_vit'],['05_kropp_rod.stl','05_kropp_vit.stl'])
`````

**Fil: `model/patch4.py`** – Ändringsrunda: parts_v3.json → parts_v4.json.

`````python
import json, base64, numpy as np, trimesh, zipfile, os
from manifold3d import Manifold, Mesh
parts=json.load(open('parts_v3.json')); P={p['name']:p for p in parts}
def T(n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=True)
def M(t): return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def toT(m):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    return trimesh.util.concatenate([c for c in t.split(only_watertight=False) if abs(c.volume)>=0.5])
def save(n,t): P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
SHIFT, SCALE = 2.6, 0.92
def adjust(t, scale_heads):
    out=[]
    for c in t.split(only_watertight=False):
        cy=c.centroid[1]; c=c.copy()
        if scale_heads and abs(c.volume) > 20:                 # blomhuvuden: något mindre, skalas kring sin egen mitt
            ctr=c.bounding_box.centroid; c.apply_translation(-ctr); c.apply_scale(SCALE); c.apply_translation(ctr)
        if cy < 66: c.apply_translation([0, SHIFT, 0])
        elif cy > 84: c.apply_translation([0, -SHIFT, 0])
        out.append(c)
    return trimesh.util.concatenate(out)
red=adjust(T('blomlador_blommor_rod'), True); white=adjust(T('blomlador_blommor_vit'), True)
green=adjust(T('blomlador_vaxter'), False)
# grönt som hamnar utanför lådans insida (under kanten) klipps bort
box=M(T('blomlador'))
g=M(green)
inside = Manifold()
for s in (1,-1):
    x0,x1 = (86.6, 99.4) if s>0 else (-99.4,-86.6)
    inside += Manifold.cube([x1-x0, 96.4-53.6, 60]).translate([x0, 53.6, 55.9])
g = (g ^ inside) - box - M(red) - M(white)
green=toT(g)
for n,t in (('blomlador_blommor_rod',red),('blomlador_blommor_vit',white),('blomlador_vaxter',green)): save(n,t)
json.dump(parts,open('parts_v4.json','w'))
names=['blomlador','blomlador_vaxter','blomlador_blommor_rod','blomlador_blommor_vit','kropp_vit','kropp','fonsterrutor']
Ms={n:M(T(n)) for n in names}
for i,a in enumerate(names[:4]):
    for b in names[i+1:]:
        v=(Ms[a]^Ms[b]).volume()
        if v>0.05: print(f"{a} x {b}: {v:.2f}")
for n in ('blomlador_blommor_rod','blomlador_blommor_vit'):
    v=T(n).vertices; print(n, "y-utbredning", v[:,1].min().round(1), v[:,1].max().round(1))
print("lådans y:", T('blomlador').vertices[:,1].min().round(1), T('blomlador').vertices[:,1].max().round(1))
`````

**Fil: `model/patch5.py`** – Ändringsrunda: parts_v4.json → parts_v5.json.

`````python
import json, base64, numpy as np, trimesh, math
from manifold3d import Manifold, Mesh, CrossSection
parts=json.load(open('parts_v4.json')); P={p['name']:p for p in parts}
def T(n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=True)
def M(n): t=T(n); return Manifold(Mesh(vert_properties=np.asarray(t.vertices,np.float32), tri_verts=np.asarray(t.faces,np.uint32)))
def toT(m, minvol=0.5):
    me=m.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=True)
    return trimesh.util.concatenate([c for c in t.split(only_watertight=False) if abs(c.volume)>=minvol])
def put(n, m, **kw):
    t=toT(m)
    if n not in P: P[n]=dict(name=n, **kw); parts.append(P[n])
    else: P[n].update(kw)
    P[n]['pos']=base64.b64encode(t.vertices.astype(np.float32).tobytes()).decode(); P[n]['idx']=base64.b64encode(t.faces.astype(np.uint32).tobytes()).decode()
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylz(cx,cy,z0,z1,r,seg=40): return Manifold.cylinder(z1-z0,r,r,seg).translate([cx,cy,z0])
def cyly(cx,cz,y0,y1,r,seg=32): return Manifold.cylinder(y1-y0,r,r,seg).rotate([-90,0,0]).translate([cx,y0,cz])
def ccw(pts):
    a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))); return pts if a>0 else pts[::-1]
def xz_prism(pts,y0,y1): return CrossSection([ccw(pts)]).extrude(y1-y0).rotate([90,0,0]).translate([0,y1,0])
HW,D,T3,PEAK=85.0,150.0,3.2,240.0; K=80/85; zu=lambda x: PEAK-abs(x)*K
COS=HW/math.hypot(HW,80); ROOF_T=6.0/COS; zo=lambda x: zu(x)+ROOF_T; X_E=113.0
ALPHA=math.degrees(math.atan(K))
body=M('kropp'); tv=M('tak_v'); th=M('tak_h'); gut=M('takrannor')

# 1) nockkilar: fjärilsformade kilar i undersidan över nocken, pressas in – inget lim
def bowtie(shrink=0.0):
    w0,w1,L = 3.0-shrink, 6.5-shrink, 13.0-shrink
    return [(-L,-w1),(0,-w0),(L,-w1),(L,w1),(0,w0),(-L,w1)]
def key_solid(yc, shrink=0.0, depth=3.0):
    pl = CrossSection([ccw([(x, y+yc) for x,y in bowtie(shrink)])]).extrude(400).translate([0,0,-100])
    band = xz_prism([(-20, zu(20)-0.01), (0, zu(0)-0.01), (20, zu(20)-0.01), (20, zu(20)+depth-shrink), (0, zu(0)+depth-shrink), (-20, zu(20)+depth-shrink)], -50, 250)
    return pl ^ band
keys=Manifold(); recess=Manifold()
for yc in (40, 110):
    recess += key_solid(yc, 0.0, 3.0); keys += key_solid(yc, 0.06, 3.0)
tv -= recess; th -= recess
# 2) skorstenens tappar: presspassning (hål r 1,45 i stället för 1,7)
for (xp,yp) in ((24,112),(38,128)):
    th = (th + cylz(xp,yp,zo(xp)-2.95,zo(xp)-0.05,1.72)) - cylz(xp,yp,zo(xp)-2.9,zo(xp)+3,1.45)
# 6) magneter: presspassning (Ø 9,9 i stället för 10,2)
def mag(sgn,y,into_roof,r,a,b):
    # cylinder från a till b mm in i materialet (räknat från ytan)
    c=Manifold.cylinder(b-a,r,r,40).translate([0,0,a]); c=c if into_roof else c.mirror([0,0,1])
    return c.rotate([0,sgn*ALPHA,0]).translate([sgn*78,y,zu(78)-(0 if into_roof else 0.3)])
for sgn in (1,-1):
    for y in (30,120):
        body = (body + mag(sgn,y,False,5.3,0.05,3.45)) - mag(sgn,y,False,4.95,-0.05,3.3)
        if sgn<0: tv = (tv + mag(sgn,y,True,5.3,0.05,3.45)) - mag(sgn,y,True,4.95,-0.05,3.3)
        else:     th = (th + mag(sgn,y,True,5.3,0.05,3.45)) - mag(sgn,y,True,4.95,-0.05,3.3)
# 3) solskyddets tappar: presspassning i fasaden (hål r 1,25 för tapp r 1,2)
HB,HS=180.0,21.0
for xp in (-12,12):
    zp=HB+(HS-abs(xp))*K+1.5
    body = (body + cyly(xp,zp,0.0,2.7,1.5)) - cyly(xp,zp,-0.1,2.7,1.25)
# 5) fönsterinsatser: rutorna blir en insats per fönster som trycks in inifrån
py=[(57,73.5),(76.5,93)]; pz=[(70,91.5),(94.5,116)]
inserts=Manifold()
for sgn in (1,-1):
    X=lambda a,b: (a,b) if sgn>0 else (-b,-a)
    plate = box(*X(HW-T3-1.6, HW-T3), 55, 95, 68, 118)
    plugs = Manifold()
    for (a,b) in py:
        for (c,d) in pz:
            body -= box(*X(HW-T3-0.1, HW-0.95), a, b, c, d)          # öppning genom väggen
            plugs += box(*X(HW-T3, HW-1.0), a, b, c, d)               # pluggen fyller öppningen, 1 mm innanför fasaden
    inserts += plate + plugs
# 4) takrännornas flikar får små hakar som klickar fast i spåret
GX=X_E-1.0; GR=6.5
for sgn in (1,-1):
    gx=sgn*GX
    hx0,hx1 = (gx-GR-0.2, gx-GR+2.2) if sgn>0 else (gx+GR-2.2, gx+GR+0.2)
    xm=(hx0+hx1)/2
    for yh in (-10,75,160):
        for side in (-1,1):
            gut += Manifold.sphere(0.6,16).scale([1.2,1,1]).translate([xm, yh+side*2.2, zu(xm)+0.6])
# 7) fötter med tapp i bottenplattan i stället för lim
plate=M('bottenplatta'); fplate=M('framgard_platta')
BX,BY0,BY1=110.0,-50.0,165.0; FY0=-170.0; BASE_H=30.0
FEET=[(-90,-30),(90,-30),(-90,145),(90,145),(-90,-150),(90,-150)]
for (x,y) in FEET[:4]: plate -= cylz(x,y,-BASE_H-3.1,-BASE_H-1.0,2.05)
for (x,y) in FEET[4:]: fplate -= cylz(x,y,-BASE_H-3.1,-BASE_H-1.0,2.05)
feet = Manifold()
for (x,y) in FEET: feet += cylz(x,y,-BASE_H-7,-BASE_H-3,10) + cylz(x,y,-BASE_H-3.01,-BASE_H-1.1,2.1)
# 8) takpackningen lite bredare så den kläms fast i spåret
def band(z_lo, z_hi, xmax):
    return [(-xmax, zu(xmax)+z_lo), (0, zu(0)+z_lo), (xmax, zu(xmax)+z_lo), (xmax, zu(xmax)+z_hi), (0, zu(0)+z_hi), (-xmax, zu(xmax)+z_hi)]
strip = xz_prism(band(0.6,2.25,HW+0.3), -0.65, T3+0.65) + xz_prism(band(0.6,2.25,HW+0.3), D-T3-0.65, D+0.65)

put('kropp', body); put('tak_v', tv); put('tak_h', th); put('takrannor', gut)
put('bottenplatta', plate); put('framgard_platta', fplate); put('fotter', feet); put('takpackning', strip)
put('nockkilar', keys, color='#5A5E62', group='Tak', file='06e_nockkilar_gra.stl', note='Grå ASA, två kilar som pressas in över nocken – inget lim')
put('fonsterrutor', inserts, file='05b_fonsterinsatser_gra.stl', note='Grå ASA, en insats per fönster som trycks in inifrån')
P['takrannor']['note']='Grå ASA, flikarna klickar fast i spåren i taket'
P['solskydd']['note']='Grå ASA, tapparna pressas in i fasaden'
P['skorsten']['note']='Röd ASA, skrivs ut upp och ner, tapparna pressas in i taket'
P['fotter']['note']='TPU 95A, tappen trycks in i bottenplattan'
json.dump(parts, open('parts_v5.json','w'))
# kollisionskontroll i monterat läge
names=['kropp','kropp_vit','fonsterrutor','tak_v','tak_h','nockkilar','takrannor','skorsten','solskydd','takpackning','bottenplatta','framgard_platta','fotter','blomlador','elektroniklada','notmagasin','kamerafaste']
Ms={n:M(n) for n in names}
for i,a in enumerate(names):
    for b in names[i+1:]:
        v=(Ms[a]^Ms[b]).volume()
        if v>0.5: print(f"{a} x {b}: {v:.1f}")
print("klart")
`````

**Fil: `model/patch6.py`** – Ändringsrunda: parts_v5.json → parts_v6.json.

`````python
from lib import *
parts,P=load('parts_v5.json')
DH=18.0                                   # dosering, kammare, skiva, lock och magasin lyfts så mycket
SL=0.84                                   # rännans lutning (40°)
fl=lambda y: 3.0+SL*(y-3.4)               # rännans golv (ovansida)

# ---------- 1. DOSERARENS BAS: ny, högre ränna och 18 mm högre stomme ----------
base=M(P,'doserare_bas')
base=base-box(-15.6,15.6,3.0,51.6,4.5,44.2)                       # gamla rännan bort
ZC=6.0
lower=base^box(-200,200,-200,300,-10,ZC)
upper=(base^box(-200,200,-200,300,ZC,200)).translate([0,0,DH])
mid=base.slice(ZC).extrude(DH).translate([0,0,ZC])
base=lower+mid+upper
TOP=44.0+DH
def yzp(pts,x0,x1): return yz_prism(pts,x0,x1)
floor=yzp([(3.4,fl(3.4)),(51.6,fl(51.6)),(51.6,fl(51.6)-2.6),(6.5,0.0),(3.4,0.0)],-15.4,15.4)
wall_profile=[(3.4,0.0),(6.5,0.0),(51.6,fl(51.6)-2.6),(51.6,TOP),(27.0,TOP),(24.0,fl(24)+36),(3.4,fl(3.4)+36)]
walls=yzp(wall_profile,13.0,15.4)+yzp(wall_profile,-15.4,-13.0)
back=box(-15.4,15.4,51.6,54.0,fl(51.6)-2.6,TOP)                    # bakvägg i fallschaktet
rib=yzp([(6.5,0.0),(51.6,0.0),(51.6,fl(51.6)-2.5),(6.5,0.05)],-0.7,0.7)   # stödribba under golvet (skrivs ut utan stöd)
base=base+floor+walls+back+rib
put(parts,P,'doserare_bas',base,note='ASA (inte CF). Rännan är öppen upptill och rymmer nötter upp till 24 mm')
for n in ('doserare_kammare','doseringsskiva','doseringslock','avstrykare'):
    put(parts,P,n,M(P,n).translate([0,0,DH]))

# ---------- 2. MAGASINET: lyfts 18 mm och får två ben fram så det står stadigt utan skruvar ----------
hop=M(P,'notmagasin').translate([0,0,DH])
def hop_solid(o):
    sx,sy0,sy1=33+o,52-o,106+o; ux,uy0=45.6+o,40-o
    funnel=Manifold.batch_hull([box(-sx,sx,sy0,sy1,100.9,101),cylz(0,89,72.9,73,min(11.5+o,13.5))])
    flare=Manifold.batch_hull([box(-sx,sx,sy0,sy1,100.95,101),box(-ux,ux,uy0,sy1,119.9,120)])
    return (funnel+flare+box(-ux,ux,uy0,sy1,119.95,175)).translate([0,0,DH])
cav=hop_solid(0)
LID_TOP=71.0+DH
for sx in (-1,1):
    leg=cylz(sx*28,40,LID_TOP+0.2,139.0,3.2,24)+Manifold.cylinder(3,4.6,3.2,24).translate([sx*28,40,LID_TOP+0.2])   # liten fot nertill
    hop=hop+(leg-cav)
put(parts,P,'notmagasin',hop,note='ASA (inte CF), rymmer ca 0,35 liter. Står löst på locket – lyfts rakt upp')

# ---------- 3. KROPPEN: lägre nöthål, urtag i flänsen, kortare skärmfästen med stödvinklar, stöd under magnetklossarna ----------
body=M(P,'kropp')
body=body-box(-13.5,13.5,-0.1,3.3,2.9,11.6)                         # hålet i väggen går nu ner till skålens golv
body=body-box(-15.8,15.8,3.1,11.4,-0.1,4.1)                         # flänsen ger plats för rännan
for x in (-34,34):
    body=body-cyly(x,108,18.0,20.3,4.2)                             # skärmfästena 2 mm kortare
    body=body-cyly(x,108,11.5,18.1,2.0)-Manifold.cylinder(0.8,2.5,2.0,32).rotate([90,0,0]).translate([x,18.01,108])
    body=body+yzp([(3.0,104.2),(17.0,104.2),(3.0,90.2)],x-1.2,x+1.2)  # 45° stödvinkel under fästet
for sgn in (1,-1):
    for y in (30,120):
        body=body+xz_prism([(sgn*74,148.05),(sgn*82.4,148.05),(sgn*82.4,139.6)],y-7,y+7)   # 45° undersida på magnetklossen
        plus=box(-2.5,2.5,-0.6,0.6,-0.5,0.01)+box(-0.6,0.6,-2.5,2.5,-0.5,0.01)
        body=body-plus.rotate([0,sgn*90,0]).translate([sgn*(HW-TW),y,133])
put(parts,P,'kropp',body)
skal=M(P,'skal')-box(-13.5,13.5,-2.7,0.1,3.0,11.6)                   # skålens bakvägg öppnas ner till golvet
put(parts,P,'skal',skal,note='Röd ASA, samma röda som kroppen går bra')
put(parts,P,'skarmklamma',M(P,'skarmklamma').translate([0,-2,0]))

# ---------- 4. ELEKTRONIKLÅDAN: öppnas uppifrån, plattan dras rakt upp ----------
EX,EY0,EY1,EZ0,EZ1=66.0,113.0,D-TW,74.0,170.0
EBOX=[(-60,80),(60,80),(-60,164),(60,164)]
eb=box(-EX,EX,EY0,EY1,EZ0,EZ1)-box(-EX+2.4,EX-2.4,EY0+2.4,EY1+1,EZ0+2.4,EZ1+1)          # öppen upptill och mot bakväggen
rimU=(box(-EX,EX,EY1-8,EY1,EZ0,EZ1)-box(-EX+5,EX-5,EY1-9,EY1+1,EZ0+5,EZ1+1))            # förtjockad bakkant: sidor + botten
eb=eb+rimU
for (x,z) in EBOX: eb=eb+cyly(x,z,EY1-10,EY1,4.5)
groove=(box(-EX+1.4,EX-1.4,EY1-1.2,EY1+0.1,EZ0+1.4,EZ1+1)-box(-EX+3.4,EX-3.4,EY1-2,EY1+1,EZ0+3.4,EZ1+2))
eb=eb-groove
for (x,z) in EBOX: eb=eb-cyly(x,z,EY1-6.5,EY1+1,2.0)-Manifold.cylinder(0.8,2.5,2.0,32).rotate([90,0,0]).translate([x,EY1+0.01,z])
PY0=EY0+2.6                                                           # plattan står mot lådans framvägg
for sx in (-1,1):                                                     # styrskenor som håller plattan
    x0,x1=(EX-2.4-2.8,EX-2.3) if sx>0 else (-EX+2.3,-EX+2.4+2.8)
    eb=eb+box(x0,x1,PY0+3.4,PY0+5.0,EZ0+2.3,EZ1-4)
eb=eb-cylz(-20,132,EZ0-1,EZ0+3,4.5)-cylz(30,132,EZ0-1,EZ0+3,4.5)     # servokablar genom botten
put(parts,P,'elektroniklada',eb,note='ASA, minst 4 perimetrar. Sitter kvar på bakväggen – öppnas uppifrån')
gask=(box(-EX+1.6,EX-1.6,EY1-1.15,EY1,EZ0+1.6,EZ1)-box(-EX+3.2,EX-3.2,EY1-2,EY1+1,EZ0+3.2,EZ1+1))
put(parts,P,'elpackning',gask,note='TPU 95A, U-formad, ligger i spåret mot bakväggen')
# lock med kjol fram och på sidorna, genomföring för kablar
LZ=EZ1
lidE=box(-EX-2.4,EX+2.4,EY0-2.4,EY1-0.2,LZ,LZ+2.4)
lidE=lidE+(box(-EX-2.4,EX+2.4,EY0-2.4,EY1-0.2,LZ-6,LZ)-box(-EX-0.2,EX+0.2,EY0-0.2,EY1+1,LZ-7,LZ+0.1))
lidE=lidE+(box(-EX+2.7,EX-2.7,EY0+2.7,EY1-12.5,LZ-2.5,LZ)-box(-EX+4.3,EX-4.3,EY0+4.3,EY1-14.1,LZ-3,LZ+0.1))   # styrkant på undersidan
lidE=lidE-box(-11,11,122.5,133.5,LZ-3,LZ+3)-box(-14,14,119.5,136.5,LZ-3,LZ-0.001)   # plats för genomföringens fläns
put(parts,P,'ellock',lidE,color='#4A5560',group='Inredning',file='16b_elektroniklada_lock.stl',note='ASA, lyfts av för att komma åt elektroniken. Modemet tejpas ovanpå')
# monteringsplatta som glider i skenorna; Raspberry Pi 5 uppe till vänster (58 x 49 mm hålbild)
mp=box(-EX+3.0,EX-3.0,PY0,PY0+3.0,EZ0+2.6,EZ1-4)
PIX=(-54.5,3.5); PIZ=(107.5,156.5)
for x in np.arange(-50,56,10.0):
    for z in np.arange(86,160,10.0):
        if -60<=x<=30 and 102<=z<=162: continue
        mp=mp-cyly(x,z,PY0-1,PY0+4,1.7)
mp=mp-box(38,54,PY0-1,PY0+4,150,160)                                   # grepphål uppe till höger
for x in PIX:
    for z in PIZ:
        mp=mp+(cyly(x,z,PY0+2.9,PY0+7.0,3.0)-cyly(x,z,PY0+3.5,PY0+7.1,1.1))
put(parts,P,'monteringsplatta',mp,note='ASA. Dras rakt upp ur lådan med all elektronik. Pi 5 uppe till vänster, övrigt i hålrastret')
# kabelgenomföringar: två runda i botten, en avlång i locket
def rg(cx,cy,z0,z1):
    g=cylz(cx,cy,z0-1.0,z0,6.5)+cylz(cx,cy,z0,z1,4.45)+cylz(cx,cy,z1,z1+1.0,6.5)
    return g-cylz(cx,cy,z0-2,z1+2,2.2)-box(cx-0.3,cx+6.6,cy-0.15,cy+0.15,z0-2,z1+2)
gr=rg(-20,132,EZ0,EZ0+2.4)+rg(30,132,EZ0,EZ0+2.4)
top=(box(-13,13,120.5,135.5,LZ+2.4,LZ+3.4)+box(-10.95,10.95,122.55,133.45,LZ,LZ+2.4)+box(-13,13,120.5,135.5,LZ-1.0,LZ))-box(-7,7,126.4,129.6,LZ-3,LZ+5)-box(-0.2,0.2,119,127,LZ-3,LZ+5)
put(parts,P,'genomforingar',gr+top)

# ---------- 5. TAKPACKNINGEN: ligger an utan att tvinga upp taket ----------
def band(z_lo,z_hi,xmax): return [(-xmax,zu(xmax)+z_lo),(0,zu(0)+z_lo),(xmax,zu(xmax)+z_lo),(xmax,zu(xmax)+z_hi),(0,zu(0)+z_hi),(-xmax,zu(xmax)+z_hi)]
strip=xz_prism(band(0.82,2.25,HW+0.3),-0.65,TW+0.65)+xz_prism(band(0.82,2.25,HW+0.3),D-TW-0.65,D+0.65)
put(parts,P,'takpackning',strip)
json.dump(parts,open('parts_v6.json','w'))
print("klart")
`````

**Fil: `model/patch7.py`** – Ändringsrunda: parts_v6.json → parts_v7.json, alltså version 6.

`````python
from lib import *
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
parts,P=load('parts_v6.json')
def text_cs(txt,size):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd), (allp.max(0)-allp.min(0))
cs,ext=text_cs("LENNART",11.5)
print("textens mått:", ext.round(1))
letters=cs.extrude(0.8).rotate([90,0,0]).translate([0,-46.0,12.0])       # 0,8 mm upphöjda vita bokstäver på skålens framsida
sv=M(P,'skal_vit')+letters
print("krock med röda skålen:", round((letters^M(P,'skal')).volume(),2), " med luckan:", round((letters^(M(P,'lucka')+M(P,'lucka_vit'))).volume(),2), "bbox", bb(letters).tolist())
put(parts,P,'skal_vit',sv)
json.dump(parts,open('parts_v7.json','w'))
`````

**Fil: `model/patch8.py`** – 2026-11-11: doseringshjulet (doserhus, doserhjul, magasin), stengrund och fönsteröverstycken. parts_v7.json → parts_v8.json, alltså version 7. Skriver även disp.json.

`````python
from lib import *
parts,P=load('parts_v7.json')
# ---------- gamla doseringen bort ----------
for n in ('doserare_bas','doserare_kammare','doseringsskiva','doseringslock','avstrykare','notmagasin'):
    parts[:]=[p for p in parts if p['name']!=n]; P.pop(n,None)
INNER="#D8C59A"
# ---------- mått ----------
YC=57.0; R=31.0; WD=17.0; RP=12.1; SL=0.84
A=math.atan(SL); CA,SA=math.cos(A),math.sin(A)
fl=lambda y: 3.0+SL*(y-3.4)                                  # rännans golv
ZC=round(fl(YC)+12.5/CA,1)                                   # hjulets axel: fickans underkant linjerar med rännan i tömläget
DUMP=90+math.degrees(A)                                      # vridning från "ficka upp" till "töm"
ZT=ZC+R+3.4                                                  # doserhusets överkant
RC=R+1.0
print("axel z =",ZC," tömvinkel =",round(DUMP,1)," överkant =",round(ZT,1))
nrm=(SA,-CA)
foot=(YC+12.5*nrm[0], ZC+12.5*nrm[1]); hc=math.sqrt(RC**2-12.5**2)
PF=(foot[0]-hc*CA, foot[1]-hc*SA)                             # där rännans golv möter hjulet
foot2=(YC-12.5*nrm[0], ZC-12.5*nrm[1]); PU=(foot2[0]-hc*CA, foot2[1]-hc*SA)
up=lambda y: PU[1]-SL*(PU[0]-y)                               # rännans övre gräns
XL0,XL1=-WD-6.3,-WD-0.3                                       # vänster vägg
XR0,XR1=WD+0.3,WD+9.3                                         # höger vägg (servofäste)
Y0,Y1=YC-R-3.2,YC+R+3.2
DISP_PINS=[(31.1,95.1),(-31.1,95.1)]; DISP_SCREWS=[(-31.1,32.9),(31.1,32.9)]
def lead_z(x,y,z,r): return Manifold.cylinder(0.8,r,r+0.5,32).translate([x,y,z-0.79])

# ---------- 1. DOSERHUS: undre halvan, ränna, servofäste ----------
hus=box(-40,40,Y0+1.5,101,0,4)                                # fotplatta på styrtappar och två skruvar
hus+=box(-WD-0.3,WD+0.3,Y0,Y1,0,ZC)                           # massiv kloss under hjulet
hus+=box(XL0,XL1,Y0,Y1,0,ZT)+box(XR0,XR1,Y0,97,0,ZT)          # sidoväggar
hus-=cylx(YC,ZC,-WD-0.3,WD+0.3,RC,96)                         # hjulets säte
void=yz_prism([(3.3,3.0),PF,(YC,ZC),PU,(3.3,up(3.3))],-13.0,13.0)
hus-=void                                                     # rännans väg genom klossen
# rännan framför klossen: golv, sidoväggar, stödribba
yj=Y0+0.5
hus+=yz_prism([(3.4,0),(6.5,0),(yj,fl(yj)-2.6),(yj,fl(yj)),(3.4,3.0)],-15.4,15.4)
wp=[(3.4,0),(6.5,0),(yj,fl(yj)-2.6),(yj,up(yj)+2.0),(3.4,up(3.4)+2.0)]
hus+=yz_prism(wp,13.0,15.4)+yz_prism(wp,-15.4,-13.0)
hus+=yz_prism([(6.5,0),(yj,0),(yj,fl(yj)-2.5),(6.5,0.05)],-0.7,0.7)
# servo MG996R: ligger på sidan, axeln i hjulets centrum, flänsen mot höger vägg
SY0,SY1=YC-10.35-0.4,YC+30.35+0.4
hus-=box(XR0-0.1,XR1+0.1,SY0,SY1,ZC-10.3,ZC+10.3)
for y in ((SY0+SY1)/2-24.75,(SY0+SY1)/2+24.75):
    for z in (ZC-5,ZC+5):
        hus-=cylx(y,z,XR1-6.5,XR1+0.1,2.0)+Manifold.cylinder(0.8,2.0,2.5,32).rotate([0,90,0]).translate([XR1-0.79,y,z])
# vänster vägg: U-spår för hjulets axeltapp
hus-=box(XL0-0.1,XL1+0.1,YC-4.2,YC+4.2,ZC,ZT+1)+cylx(YC,ZC,XL0-0.1,XL1+0.1,4.2)
# fästen för magasinet: två skruvar framtill, uppifrån
HS=[((XL0+XL1)/2,Y0+4.7),((XR0+XR1)/2,Y0+4.7)]
for (x,y) in HS: hus-=cylz(x,y,ZT-6.5,ZT+0.1,2.0)+lead_z(x,y,ZT,2.0)
for (x,y) in DISP_SCREWS: hus-=cylz(x,y,-1,5,1.7)
for (x,y) in DISP_PINS: hus-=cylz(x,y,-1,5,2.25)+Manifold.cylinder(0.8,2.75,2.25,32).translate([x,y,-0.01])
put(parts,P,'doserhus',hus,color=INNER,group='Inredning',file='10_doserhus.stl',note='ASA (inte CF). Hjulets säte, rännan och servofästet i ett stycke')

# ---------- 2. DOSERHJUL: en ficka, en nöt ----------
hjul=cylx(YC,ZC,-WD,WD,R,128)
PD=21.5                                                       # fickans djup
pocket=cylz(0,YC,ZC+R-PD,ZC+R+2,RP,64)+Manifold.cylinder(1.6,RP,RP+1.6,64).translate([0,YC,ZC+R-1.9])   # fasad kant
hjul-=pocket
hjul+=cylx(YC,ZC,-WD-5.6,-WD+0.1,4.0,48)                      # axeltapp vänster
hjul-=cylx(YC,ZC,WD-3.4,WD+0.1,12.7,64)+cylx(YC,ZC,WD-9.5,WD-3.3,4.6,32)   # urtag för servots runda horn + nav
put(parts,P,'doserhjul',hjul,color="#C9A86A",group='Inredning',file='11_doserhjul.stl',note='ASA (inte CF). Fickan rymmer en nöt på 18–22 mm. Servots runda horn skruvas i urtaget')

# ---------- 3. MAGASIN: sadel över hjulet + tratt ----------
ZF=ZT+3.0; ZB=ZT+40.0; ZTOP=176.0
outer=Manifold.batch_hull([box(XL0,XR1,Y0,Y1,ZF-0.1,ZF),box(-48,48,37.6,108.4,ZB-0.1,ZB)])+box(-48,48,37.6,108.4,ZB-0.05,ZTOP)
outer+=box(XL0,XR1,Y0,Y1,ZT,ZF)                               # fläns som vilar på sidoväggarna
inner=Manifold.batch_hull([box(-13,13,YC-15,YC+15,ZT-0.1,ZT),box(-45.6,45.6,40,106,ZB-0.1,ZB)])+box(-45.6,45.6,40,106,ZB-0.05,ZTOP+1)
sadel=box(-WD,WD,Y0,Y1,ZC+0.4,ZT+0.05)-cylx(YC,ZC,-WD-1,WD+1,RC,96)
mag=(outer+sadel)-inner-box(-13,13,YC-15,YC+15,ZC,ZT+0.2)
for (x,y) in HS: mag-=cylz(x,y,ZT-1,ZF+0.1,1.7)+cylz(x,y,ZF,ZF+60,3.6)      # skruvhål + fri väg för skruvmejseln
mag+=box(-22,22,104.5,108.4,168,186)-box(-16,16,103,110,168,180)            # handtag
put(parts,P,'notmagasin',mag,color=INNER,group='Inredning',file='14_notmagasin.stl',note='ASA (inte CF), rymmer ca 0,35 liter. Två skruvar framtill, sedan lyfts det rakt upp')
cap=(inner^box(-200,200,-200,300,ZT,ZTOP)).volume()/1e6
print("magasinets volym:",round(cap,2),"liter")

# ---------- 4. EXTERIÖR: stengrund och fönsteröverstycken ----------
body=M(P,'kropp'); SH=10.0
sock=(body^box(-200,200,-200,300,-1,SH))+(box(-HW,HW,0,D,0,SH)-box(-HW+TW,HW-TW,TW,D-TW,-1,SH+1))
sock-=box(-13.5,13.5,-0.1,TW+0.1,2.9,SH+0.1)                  # nöthålet
jw,jd=0.9,0.5                                                 # fogar i stengrunden
joints=box(-HW-1,HW+1,-1,D+1,SH/2-jw/2,SH/2+jw/2)-box(-HW+jd,HW-jd,jd,D-jd,-1,SH+1)
for k,x in enumerate(np.arange(-HW+12,HW-5,24.0)):
    for (z0,z1,off) in ((0,SH/2,0),(SH/2,SH,12)):
        xx=x+off
        if abs(xx)<HW-4: joints+=box(xx-jw/2,xx+jw/2,-1,jd,z0,z1)+box(xx-jw/2,xx+jw/2,D-jd,D+1,z0,z1)
for k,y in enumerate(np.arange(12,D-5,24.0)):
    for (z0,z1,off) in ((0,SH/2,0),(SH/2,SH,12)):
        yy=y+off
        if 4<yy<D-4: joints+=box(HW-jd,HW+1,yy-jw/2,yy+jw/2,z0,z1)+box(-HW-1,-HW+jd,yy-jw/2,yy+jw/2,z0,z1)
sock-=joints
put(parts,P,'kropp',body^box(-200,200,-200,300,SH,400))
put(parts,P,'kropp_sockel',sock,color="#8C9094",group='Kropp',file='05_kropp_sockel_gra.stl',note='Grå ASA (samma som taket). Stengrunden skrivs ut i samma utskrift som kroppen')
white=M(P,'kropp_vit')
for sgn in (1,-1):                                            # överstycken på sidofönstren
    xs=(HW,HW+2.5) if sgn>0 else (-HW-2.5,-HW)
    white+=yz_prism([(50.5,119.8),(99.5,119.8),(99.5,122.6),(75,129.5),(50.5,122.6)],xs[0],xs[1])
white+=xz_prism([(-31.5,130.3),(31.5,130.3),(31.5,135.6),(0,143.5),(-31.5,135.6)],-2.8,0)   # överstycke på skärmfönstret
put(parts,P,'kropp_vit',white)
json.dump(parts,open('parts_v8.json','w'))
json.dump(dict(YC=YC,ZC=ZC,DUMP=DUMP,ZT=ZT,R=R,PD=PD),open('disp.json','w'))
print("klart,",len(parts),"delar")
`````

**Fil: `model/patch9.py`** – 2026-11-11: tre dörrförslag, förkastade 2026-11-12. parts_v8.json → parts_v9.json, används inte längre.

`````python
from lib import *
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
parts,P=load('parts_v8.json')
GREEN="#2F5D3A"; WHITE="#F2EDE1"; STONE="#8C9094"; RED="#8E2A22"
def text(txt,size,depth):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd).extrude(depth)
def add(name,m,color,var,note):
    put(parts,P,name,m,color=color,group='Skål',file='koncept',note=note)
    d=[p for p in parts if p['name']==name][0]; d['var']=var; d['concept']=True
for p in parts:
    if p['name'] in ('skal','skal_vit','lucka','lucka_vit','servokapa','servopackning'): p['var']=[0]
DW=14.5; DT=2.4; DTOP=36.0
# ---- gemensamt för dörrvarianterna: foder, namnskylt ----
def casing(left=True,right=True):
    c=box(-19,19,-3,0,DTOP+0.6,DTOP+4.2)+xz_prism([(-21,DTOP+4.2),(21,DTOP+4.2),(21,DTOP+5.6),(0,DTOP+10.5),(-21,DTOP+5.6)],-3.4,0)
    if left: c+=box(-19,-DW-0.4,-3,0,0,DTOP+0.6)
    if right: c+=box(DW+0.4,19,-3,0,0,DTOP+0.6)
    return c
sign=box(-24,24,-2.2,0,50,61)
letters=text("LENNART",6.2,0.9).rotate([90,0,0]).translate([0,-2.1,55.5])
def post(x0,x1):      # vit stolpe med hatt, rymmer dörrservot
    return box(x0,x1,-24,0,0,40)+Manifold.batch_hull([box(x0-1.4,x1+1.4,-25.4,0,40,41.5),box((x0+x1)/2-2,(x0+x1)/2+2,-14,-10,47,47.5)])
def planks(x0,x1,z0,z1,y):  # spår mellan brädorna på dörrens utsida
    m=Manifold()
    for x in np.arange(x0+5.8,x1-2,5.8): m+=box(x-0.35,x+0.35,y-0.5,y+0.01,z0,z1)
    return m
def slab(y0,y1,top,dish_y):
    s=box(-28,28,y0,y1,0,top)-Manifold.sphere(40,96).translate([0,dish_y,top+40-2.2])
    return s
# ---- 1. VINDBRYGGAN: dörren fälls ner och blir nötens ramp ----
AX1=(-1.2,1.8)
d1=box(-DW,DW,-DT,0,AX1[1]-1.2,DTOP)-planks(-DW,DW,AX1[1],DTOP,-DT+0.5)
d1+=box(-DW,-DW+1.6,0,2.2,6,DTOP-2)+box(DW-1.6,DW,0,2.2,6,DTOP-2)          # sarger på insidan: håller nöten kvar på rampen
d1v=box(-DW,DW,-DT-0.8,-DT,DTOP-4,DTOP)+box(-DW,DW,-DT-0.8,-DT,AX1[1]+1,AX1[1]+5)   # tvärslåar
d1v+=xz_prism([(-DW,AX1[1]+5),(-DW+4,AX1[1]+5),(DW,DTOP-4),(DW-4,DTOP-4)],-DT-0.8,-DT)  # snedsträva
add('v1_dorr',d1,GREEN,[1],'Koncept. Dörren är också rampen: nöten rullar ut på dörrens insida')
add('v1_dorr_vit',d1v,WHITE,[1],'Koncept')
add('v1_foder',casing(right=False)+post(DW+0.6,DW+26),WHITE,[1],'Koncept. Stolpen rymmer samma luckservo som i dag')
add('v1_trappsten',slab(-74,-38,1.4,-56),STONE,[1],'Koncept. Gropen fångar nöten')
# ---- 2. STUGDÖRREN: sidohängd dörr med hjärta ----
t=np.linspace(0,2*np.pi,60,endpoint=False)
heart=[(float(0.26*16*np.sin(a)**3), float(0.26*(13*np.cos(a)-5*np.cos(2*a)-2*np.cos(3*a)-np.cos(4*a)))) for a in t]
hz=CrossSection([heart[::-1]]).extrude(6).rotate([90,0,0]).translate([0,2,27])
d2=box(-DW,DW,-DT,0,3.2,DTOP)-planks(-DW,DW,3.2,DTOP,-DT+0.5)-hz
d2v=box(-DW,DW,-DT-0.8,-DT,DTOP-3.5,DTOP)+box(-DW,DW,-DT-0.8,-DT,3.2,6.7)+Manifold.sphere(1.9,24).translate([DW-4,-DT-1.6,17])
for z in (9,30): d2v+=box(-DW,-DW+7,-DT-0.9,-DT,z-1.1,z+1.1)                 # gångjärn
add('v2_dorr',d2,GREEN,[2],'Koncept. Sidohängd, servots axel är gångjärnet')
add('v2_dorr_vit',d2v,WHITE,[2],'Koncept')
add('v2_foder',casing(left=False)+post(-DW-26,-DW-0.6),WHITE,[2],'Koncept. Stolpen rymmer dörrservot')
mat=box(-17,17,-30,-5,2.5,3.3)
add('v2_trappsten',slab(-64,-3,2.5,-45),STONE,[2,3],'Koncept. Gropen fångar nöten')
add('v2_dorrmatta',mat,RED,[2],'Koncept. Dörrmatta')
# ---- 3. SVÄNGDÖRREN: hänger i överkanten, nöten knuffar upp den själv ----
d3=box(-DW+0.6,DW-0.6,-1.6,0,3.4,DTOP-1)-planks(-DW,DW,3.4,DTOP-1,-1.1)
ring=(cylz(0,0,0,0.8,6.5,48)-cylz(0,0,-1,2,4.6,48)).rotate([90,0,0]).translate([0,-1.6,22])
d3v=ring+box(-DW+0.6,DW-0.6,-2.4,-1.6,3.4,6.4)
add('v3_dorr',d3,GREEN,[3],'Koncept. Lätt lucka på två tappar, inget servo')
add('v3_dorr_vit',d3v,WHITE,[3],'Koncept')
roofl=Manifold.batch_hull([box(-23,23,-1,0,DTOP+12,DTOP+13.5),box(-23,23,-17,-16,DTOP+5,DTOP+6.5)])
add('v3_foder',casing(),WHITE,[3],'Koncept')
add('v3_skarmtak',roofl+yz_prism([(0,DTOP+5),(-12,DTOP+5.6),(0,DTOP+11)],-21,-19)+yz_prism([(0,DTOP+5),(-12,DTOP+5.6),(0,DTOP+11)],19,21),"#5A5E62",[3],'Koncept. Skärmtak som håller regnet från luckan')
add('v_skylt',sign,WHITE,[1,2,3],'Koncept. Namnskylt över dörren')
add('v_skylt_text',letters,RED,[1,2,3],'Koncept')
json.dump(parts,open('parts_v9.json','w')); print(len(parts),"delar")
`````

**Fil: `model/patch10.py`** – 2026-11-13: separata vita detaljer med fickor och tappar. parts_v8.json → parts_v10.json och STL. Återställdes 2026-11-14.

`````python
from lib import *
from manifold3d import JoinType
import os
parts,P=load('parts_v8.json')
body=M(P,'kropp'); white=M(P,'kropp_vit')
pcs=white.decompose()
fins=[c for c in pcs if c.volume()<300]                      # två små fästen för kamerans solskydd: blir röda och sitter i kroppen
pcs=[c for c in pcs if c.volume()>=300]
for f in fins: body=body+f
R_BIG,R_SMALL,GAP=1.4,1.2,0.05                                 # tappar Ø2,8/Ø2,4 i hål Ø2,9/Ø2,5: samma par som i toleranstestet
V=np.array([0,0,1.0])
def frame(o): W=np.array(o,float); return np.cross(V,W),V,W
def place(m,o,c):
    U,Vv,W=frame(o); return m.transform([[U[0],Vv[0],W[0],c[0]],[U[1],Vv[1],W[1],c[1]],[U[2],Vv[2],W[2],c[2]]])
def teardrop(r,depth):                                         # spetsen nedåt: tappen skrivs ut liggande från den stående väggen utan överhäng
    pts=[(r*math.cos(a),r*math.sin(a)) for a in np.linspace(math.radians(-45),math.radians(225),40)]+[(0,-r*math.sqrt(2))]
    return CrossSection([ccw(pts)]).extrude(depth)
def classify(c):
    b=c.bounding_box()
    if b[4]<=0.05 or (b[1]<-0.5 and b[4]<20): return (0,-1,0),0.0,'y'
    if b[4]>150.5: return (0,1,0),150.0,'y'
    if b[3]<=-84.9: return (-1,0,0),-85.0,'x'
    return (1,0,0),85.0,'x'
def slab(ax,a,b_):
    lo,hi=min(a,b_),max(a,b_); big=400
    return box(lo,hi,-big,big,-big,big) if ax=='x' else box(-big,big,lo,hi,-big,big)
red=body
new_white=[]; pegs=Manifold(); pockets=Manifold(); report=[]; meta=[]
for i,c in enumerate(pcs):
    o,w,ax=classify(c); oo=np.array(o,float); ai='xy'.index(ax)
    b=c.bounding_box(); t=abs((b[1] if o[1]<0 else b[4]) - w) if ax=='y' else abs((b[0] if o[0]<0 else b[3]) - w)
    corner=(b[5]-b[2])>150
    small=c.volume()<600
    PK=min(1.4,max(1.0,3.0-t))                                 # fickans djup i väggen
    CL=0.05 if small else 0.1                                  # spel runt delen i fickan
    # fickan: delens kontur sedd rakt framifrån, sänkt PK mm in i väggen. Delen fylls ut i fickan där det finns vägg.
    U,Vv,W=frame(o); p0=np.zeros(3); p0[ai]=w
    Rm=np.array([U,Vv,W]); to_loc=np.c_[Rm,-Rm@p0]; to_w=np.c_[Rm.T,p0]
    sil=c.transform(to_loc.tolist()).project()
    ext=sil.extrude(PK).translate([0,0,-PK]).transform(to_w.tolist())^red
    pk=sil.offset(CL,JoinType.Miter).extrude(PK+0.02).translate([0,0,-PK]).transform(to_w.tolist())
    c2=c+ext
    pockets=pockets+pk
    # tappar: där delen är minst 3 mm tjock och väggen bakom fickan är hel
    floor=w-o[ai]*PK; r=R_SMALL if c.volume()<1500 else R_BIG
    us=np.arange((b[0] if ax=='y' else b[1])+r+1.2,(b[3] if ax=='y' else b[4])-r-1.2,1.5)
    zs=np.arange(max(b[2],12.0)+r+2,b[5]-r-1.0,1.5)
    cand=[]
    for u in us:
        for z in zs:
            p=np.zeros(3); p[0 if ax=='y' else 1]=u; p[2]=z; p[ai]=floor
            po=place(Manifold.cylinder(3.0,r+0.8,r+0.8,24),o,p); pi=place(Manifold.cylinder(1.6,r+0.8,r+0.8,24),tuple(-oo),p)
            if (po^c2).volume()>po.volume()*0.995 and (pi^red).volume()>pi.volume()*0.995: cand.append(p)
    sel=[]
    if cand:
        cand=np.array(cand); n=3 if (corner or c.volume()>2500) else 2
        d=np.linalg.norm(cand[:,None]-cand[None],axis=2); i0,i1=np.unravel_index(d.argmax(),d.shape); sel=[i0,i1]
        while len(sel)<min(n,len(cand)):
            dm=np.min(np.linalg.norm(cand[:,None]-cand[sel][None],axis=2),axis=1); sel.append(int(dm.argmax()))
        for p in cand[sel]:
            pegs=pegs+place(teardrop(r,2.0),o,p)
            c2=c2-place(teardrop(r+GAP,2.3).translate([0,0,-0.01]),o,p)
    report.append((i,ax,o,'tjocklek %.1f'%t,'ficka %.1f'%PK,'Ø%.1f'%(2*r),len(cand),[tuple(np.round(p,1)) for p in (cand[sel] if len(sel) else [])]))
    new_white.append(c2); meta.append(dict(o=o,w=floor,ax=ax,corner=corner,pegs=len(sel)))
for r_ in report: print(r_)
body2=(red-pockets)+pegs
allw=Manifold()
for c in new_white: allw=allw+c
print("vit ∩ kropp:", round((allw^body2).volume(),2), "| kroppens minsta väggrest bakom fickorna ska vara ≥1,8 mm")
put(parts,P,'kropp',body2)
put(parts,P,'kropp_vit',allw,file='05e_vit_*.stl',note='Vit PETG. Nio delar som skrivs ut liggande och trycks in i fickor med tappar i kroppen')
json.dump(parts,open('parts_v10.json','w'))
# export: hörnbrädor med framsidan nedåt, övriga med baksidan nedåt
for f in os.listdir('stl'):
    if f.startswith('05e_') or f=='05_kropp_vit.stl': os.remove('stl/'+f)
cnt={}
for c,m_ in zip(new_white,meta):
    o=m_['o']; U,Vv,W=frame(o)
    Wd = -W if m_['corner'] else W                             # w uppåt från plattan
    Ud = np.cross(V,Wd); R=np.array([Ud,V,Wd]); m=c.transform(np.c_[R,np.zeros(3)].tolist()); bb=m.bounding_box()
    m=m.translate([-(bb[0]+bb[3])/2,-(bb[1]+bb[4])/2,-bb[2]])
    b=c.bounding_box()
    kind='hornbrada' if m_['corner'] else 'sidofonster' if m_['ax']=='x' else 'skarmfonster' if b[2]>80 and b[5]<150 else 'dorroverstycke' if b[5]<45 else 'kamerakrage'
    cnt[kind]=cnt.get(kind,0)+1; nm=f"05e_vit_{kind}{'_'+str(cnt[kind]) if kind in ('hornbrada','sidofonster') else ''}.stl"
    toT(m,0.1).export('stl/'+nm); t=trimesh.load('stl/'+nm)
    print(nm,"tät" if t.is_watertight else "EJ TÄT",np.round(t.extents,1),"tappar:",m_['pegs'])

def export(names, files):
    ms=[T(P,n) for n in names]
    allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for n,f in zip(names,files):
        man=M(P,n).transform(A[:3,:].tolist())
        t=toT(man,1.0); t.export('stl/'+f)
        chk=trimesh.load('stl/'+f)
        print(f, "tät" if chk.is_watertight else "EJ TÄT", np.round(chk.extents,1))
export(['kropp','kropp_sockel'],['05_kropp_rod.stl','05_kropp_sockel_gra.stl'])
for f in os.listdir('stl'):
    if f.startswith('05e_'):
        m=trimesh.load('stl/'+f, process=True); cs=[c for c in m.split(only_watertight=False) if abs(c.volume)>1 and c.is_watertight]
        trimesh.util.concatenate(cs).export('stl/'+f)
        print(f, trimesh.load('stl/'+f).is_watertight)
`````

**Fil: `model/patch11.py`** – 2026-11-15: samma som patch10.py men från parts_v11base.json till parts_v11.json. Det är aktuellt läge.

`````python
from lib import *
from manifold3d import JoinType
import os
parts,P=load('parts_v11base.json')
body=M(P,'kropp'); white=M(P,'kropp_vit')
pcs=white.decompose()
fins=[c for c in pcs if c.volume()<300]                      # två små fästen för kamerans solskydd: blir röda och sitter i kroppen
pcs=[c for c in pcs if c.volume()>=300]
for f in fins: body=body+f
R_BIG,R_SMALL,GAP=1.4,1.2,0.05                                 # tappar Ø2,8/Ø2,4 i hål Ø2,9/Ø2,5: samma par som i toleranstestet
V=np.array([0,0,1.0])
def frame(o): W=np.array(o,float); return np.cross(V,W),V,W
def place(m,o,c):
    U,Vv,W=frame(o); return m.transform([[U[0],Vv[0],W[0],c[0]],[U[1],Vv[1],W[1],c[1]],[U[2],Vv[2],W[2],c[2]]])
def teardrop(r,depth):                                         # spetsen nedåt: tappen skrivs ut liggande från den stående väggen utan överhäng
    pts=[(r*math.cos(a),r*math.sin(a)) for a in np.linspace(math.radians(-45),math.radians(225),40)]+[(0,-r*math.sqrt(2))]
    return CrossSection([ccw(pts)]).extrude(depth)
def classify(c):
    b=c.bounding_box()
    if b[4]<=0.05 or (b[1]<-0.5 and b[4]<20): return (0,-1,0),0.0,'y'
    if b[4]>150.5: return (0,1,0),150.0,'y'
    if b[3]<=-84.9: return (-1,0,0),-85.0,'x'
    return (1,0,0),85.0,'x'
def slab(ax,a,b_):
    lo,hi=min(a,b_),max(a,b_); big=400
    return box(lo,hi,-big,big,-big,big) if ax=='x' else box(-big,big,lo,hi,-big,big)
red=body
new_white=[]; pegs=Manifold(); pockets=Manifold(); report=[]; meta=[]
for i,c in enumerate(pcs):
    o,w,ax=classify(c); oo=np.array(o,float); ai='xy'.index(ax)
    b=c.bounding_box(); t=abs((b[1] if o[1]<0 else b[4]) - w) if ax=='y' else abs((b[0] if o[0]<0 else b[3]) - w)
    corner=(b[5]-b[2])>150
    small=c.volume()<600
    PK=min(1.4,max(1.0,3.0-t))                                 # fickans djup i väggen
    CL=0.05 if small else 0.1                                  # spel runt delen i fickan
    # fickan: delens kontur sedd rakt framifrån, sänkt PK mm in i väggen. Delen fylls ut i fickan där det finns vägg.
    U,Vv,W=frame(o); p0=np.zeros(3); p0[ai]=w
    Rm=np.array([U,Vv,W]); to_loc=np.c_[Rm,-Rm@p0]; to_w=np.c_[Rm.T,p0]
    sil=c.transform(to_loc.tolist()).project()
    ext=sil.extrude(PK).translate([0,0,-PK]).transform(to_w.tolist())^red
    pk=sil.offset(CL,JoinType.Miter).extrude(PK+0.02).translate([0,0,-PK]).transform(to_w.tolist())
    c2=c+ext
    pockets=pockets+pk
    # tappar: där delen är minst 3 mm tjock och väggen bakom fickan är hel
    floor=w-o[ai]*PK; r=R_SMALL if c.volume()<1500 else R_BIG
    us=np.arange((b[0] if ax=='y' else b[1])+r+1.2,(b[3] if ax=='y' else b[4])-r-1.2,1.5)
    zs=np.arange(max(b[2],12.0)+r+2,b[5]-r-1.0,1.5)
    cand=[]
    for u in us:
        for z in zs:
            p=np.zeros(3); p[0 if ax=='y' else 1]=u; p[2]=z; p[ai]=floor
            po=place(Manifold.cylinder(3.0,r+0.8,r+0.8,24),o,p); pi=place(Manifold.cylinder(1.6,r+0.8,r+0.8,24),tuple(-oo),p)
            if (po^c2).volume()>po.volume()*0.995 and (pi^red).volume()>pi.volume()*0.995: cand.append(p)
    sel=[]
    if cand:
        cand=np.array(cand); n=3 if (corner or c.volume()>2500) else 2
        d=np.linalg.norm(cand[:,None]-cand[None],axis=2); i0,i1=np.unravel_index(d.argmax(),d.shape); sel=[i0,i1]
        while len(sel)<min(n,len(cand)):
            dm=np.min(np.linalg.norm(cand[:,None]-cand[sel][None],axis=2),axis=1); sel.append(int(dm.argmax()))
        for p in cand[sel]:
            pegs=pegs+place(teardrop(r,2.0),o,p)
            c2=c2-place(teardrop(r+GAP,2.3).translate([0,0,-0.01]),o,p)
    report.append((i,ax,o,'tjocklek %.1f'%t,'ficka %.1f'%PK,'Ø%.1f'%(2*r),len(cand),[tuple(np.round(p,1)) for p in (cand[sel] if len(sel) else [])]))
    new_white.append(c2); meta.append(dict(o=o,w=floor,ax=ax,corner=corner,pegs=len(sel)))
for r_ in report: print(r_)
body2=(red-pockets)+pegs
allw=Manifold()
for c in new_white: allw=allw+c
print("vit ∩ kropp:", round((allw^body2).volume(),2), "| kroppens minsta väggrest bakom fickorna ska vara ≥1,8 mm")
put(parts,P,'kropp',body2)
put(parts,P,'kropp_vit',allw,file='05e_vit_*.stl',note='Vit PETG. Nio delar som skrivs ut liggande och trycks in i fickor med tappar i kroppen')
json.dump(parts,open('parts_v11.json','w'))
# export: hörnbrädor med framsidan nedåt, övriga med baksidan nedåt
for f in os.listdir('stl'):
    if f.startswith('05e_') or f=='05_kropp_vit.stl': os.remove('stl/'+f)
cnt={}
for c,m_ in zip(new_white,meta):
    o=m_['o']; U,Vv,W=frame(o)
    Wd = -W if m_['corner'] else W                             # w uppåt från plattan
    Ud = np.cross(V,Wd); R=np.array([Ud,V,Wd]); m=c.transform(np.c_[R,np.zeros(3)].tolist()); bb=m.bounding_box()
    m=m.translate([-(bb[0]+bb[3])/2,-(bb[1]+bb[4])/2,-bb[2]])
    b=c.bounding_box()
    kind='hornbrada' if m_['corner'] else 'sidofonster' if m_['ax']=='x' else 'skarmfonster' if b[2]>80 and b[5]<150 else 'dorroverstycke' if b[5]<45 else 'kamerakrage'
    cnt[kind]=cnt.get(kind,0)+1; nm=f"05e_vit_{kind}{'_'+str(cnt[kind]) if kind in ('hornbrada','sidofonster') else ''}.stl"
    toT(m,0.1).export('stl/'+nm); t=trimesh.load('stl/'+nm)
    print(nm,"tät" if t.is_watertight else "EJ TÄT",np.round(t.extents,1),"tappar:",m_['pegs'])

def export(names, files):
    ms=[T(P,n) for n in names]
    allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    for n,f in zip(names,files):
        man=M(P,n).transform(A[:3,:].tolist())
        t=toT(man,1.0); t.export('stl/'+f)
        chk=trimesh.load('stl/'+f)
        print(f, "tät" if chk.is_watertight else "EJ TÄT", np.round(chk.extents,1))
export(['kropp','kropp_sockel'],['05_kropp_rod.stl','05_kropp_sockel_gra.stl'])
for f in os.listdir('stl'):
    if f.startswith('05e_'):
        m=trimesh.load('stl/'+f, process=True); cs=[c for c in m.split(only_watertight=False) if abs(c.volume)>1 and c.is_watertight]
        trimesh.util.concatenate(cs).export('stl/'+f)
        print(f, trimesh.load('stl/'+f).is_watertight)
`````

**Fil: `model/checks.py`** – Äldre kontroller av krockar och rörelser.

`````python
from lib import *
import sys
fn=sys.argv[1] if len(sys.argv)>1 else 'parts_v6.json'
parts,P=load(fn)
names=[p['name'] for p in parts]
Ms={n:M(P,n) for n in names}
def inter(a,b): return (a^b).volume()
print("== KOLLISIONER I MONTERAT LÄGE (över 0,5 mm3) ==")
lst=names
for i,a in enumerate(lst):
    ba=Ms[a].bounding_box()
    for b in lst[i+1:]:
        bb_=Ms[b].bounding_box()
        if ba[0]>bb_[3] or bb_[0]>ba[3] or ba[1]>bb_[4] or bb_[1]>ba[4] or ba[2]>bb_[5] or bb_[2]>ba[5]: continue
        v=inter(Ms[a],Ms[b])
        if v>0.5: print(f"  {a} x {b}: {v:.1f}")
def U(ns): 
    m=Manifold()
    for n in ns: m=m+Ms[n]
    return m
roof=['tak_v','tak_v_vit','tak_h','tak_h_vit','skorsten','skorsten_krage','takrannor','nockkilar','takpackning']
rest=[n for n in names if n not in roof]
R=U(roof); S=U(rest); base0=inter(R,S)
print("== LYFTA TAKET rakt upp ==  (i vila:", round(base0,1),")")
for dz in (1,2,4,8,15,30,60): print(f"  +{dz} mm: {inter(R.translate([0,0,dz]),S):.1f}")
print("== ÖPPNA LUCKAN (vrids kring gångjärnet) ==")
lid=U(['lucka','lucka_vit']); others=U([n for n in names if n not in ('lucka','lucka_vit')])
for ang in (0,-15,-30,-50,-70,-90,-100):
    L=lid.translate([0,8,-32.2]).rotate([ang,0,0]).translate([0,-8,32.2]); print(f"  {ang}°: {inter(L,others):.1f}")
print("== VRIDA DOSERINGSSKIVAN ==")
disc=Ms['doseringsskiva']; o2=U(['doserare_kammare','doseringslock','avstrykare','doserare_bas','notmagasin'])
for ang in (0,30,60,90,120,150,180): print(f"  {ang}°: {inter(disc.translate([0,-64,0]).rotate([0,0,ang]).translate([0,64,0]),o2):.1f}")
print("== LYFTA MAGASINET rakt upp ==")
hop=Ms['notmagasin']; o3=U([n for n in rest if n!='notmagasin'])
for dz in (0,1,3,6,12,25,50,100,170): print(f"  +{dz}: {inter(hop.translate([0,0,dz]),o3):.1f}")
print("== LYFTA DOSERINGSLOCKET (magasinet borttaget) ==")
dl=U(['doseringslock','avstrykare']); o4=U([n for n in rest if n not in ('notmagasin','doseringslock','avstrykare')])
for dz in (0,1,3,6,12,20): print(f"  +{dz}: {inter(dl.translate([0,0,dz]),o4):.1f}")
print("== LYFTA SKIVAN (lock borttaget) ==")
o5=U([n for n in rest if n not in ('notmagasin','doseringslock','avstrykare','doseringsskiva')])
for dz in (0,2,5,10,22): print(f"  +{dz}: {inter(disc.translate([0,0,dz]),o5):.1f}")
print("== LYFTA ELEKTRONIKLOCKET och PLATTAN ==")
o6=U([n for n in rest if n not in ('ellock','genomforingar')]) if 'ellock' in Ms else None
if o6 is not None:
    for dz in (0,2,5,10): print(f"  lock +{dz}: {inter(Ms['ellock'].translate([0,0,dz]),o6):.1f}")
    o7=U([n for n in rest if n not in ('ellock','genomforingar','monteringsplatta')])
    for dz in (0,5,20,50,95): print(f"  platta +{dz}: {inter(Ms['monteringsplatta'].translate([0,0,dz]),o7):.1f}")
print("== SKRUVMEJSEL uppifrån till doserarens främre skruvar ==")
o8=U([n for n in rest])
for x in (-31.1,31.1):
    drv=cylz(x,32.9,8,235,3.0); print(f"  x={x}: {inter(drv,o8):.1f}")
`````

**Fil: `model/checks8.py`** – Kontroller: krockar i monterat läge, att hjulet kan vridas, att taket, magasinet och hjulet kan lyftas, skruvmejselns väg, luckan och nötens väg för olika nötstorlekar.

`````python
from lib import *
import sys
fn=sys.argv[1] if len(sys.argv)>1 else 'parts_v8.json'
parts,P=load(fn); names=[p['name'] for p in parts]; Ms={n:M(P,n) for n in names}
dj=json.load(open('disp.json')); YC,ZC,DUMP,R,PD=dj['YC'],dj['ZC'],dj['DUMP'],dj['R'],dj['PD']
inter=lambda a,b:(a^b).volume()
def U(ns):
    m=Manifold()
    for n in ns: m=m+Ms[n]
    return m
print("== KOLLISIONER I MONTERAT LÄGE (över 0,5 mm3) ==")
for i,a in enumerate(names):
    ba=Ms[a].bounding_box()
    for b in names[i+1:]:
        b2=Ms[b].bounding_box()
        if ba[0]>b2[3] or b2[0]>ba[3] or ba[1]>b2[4] or b2[1]>ba[4] or ba[2]>b2[5] or b2[2]>ba[5]: continue
        v=inter(Ms[a],Ms[b])
        if v>0.5: print(f"  {a} x {b}: {v:.1f}")
rot=lambda m,ang: m.translate([0,-YC,-ZC]).rotate([ang,0,0]).translate([0,YC,ZC])
print("== VRIDA HJULET 0–130° =="); o=U(['doserhus','notmagasin'])
print("  ", [round(inter(rot(Ms['doserhjul'],a),o),1) for a in (0,20,40,60,80,100,120,130)])
roof=['tak_v','tak_v_vit','tak_h','tak_h_vit','skorsten','skorsten_krage','takrannor','nockkilar','takpackning']
rest=[n for n in names if n not in roof]
print("== LYFTA TAKET ==", [round(inter(U(roof).translate([0,0,dz]),U(rest)),1) for dz in (1,5,20,60)])
print("== LYFTA MAGASINET =="); o3=U([n for n in rest if n!='notmagasin'])
print("  ", [round(inter(Ms['notmagasin'].translate([0,0,dz]),o3),1) for dz in (0,2,6,15,40,100,170)])
print("== LYFTA HJULET (magasinet borta, servot ute) =="); o4=U([n for n in rest if n not in ('notmagasin','doserhjul')])
print("  ", [round(inter(Ms['doserhjul'].translate([0,0,dz]),o4),1) for dz in (0,3,10,40,120)])
print("== SKRUVMEJSEL uppifrån ==")
o5=U(rest); o5b=U([n for n in rest if n!='notmagasin'])
for (x,y,z0,what,env_) in ((-20.3,27.5,102.5,'magasinets skruv v',o5),(21.8,27.5,102.5,'magasinets skruv h',o5),(-31.1,32.9,6,'doserhusets skruv v (magasinet borta)',o5b),(31.1,32.9,6,'doserhusets skruv h (magasinet borta)',o5b)):
    print(f"   {what}: {inter(cylz(x,y,z0,236,3.0),env_):.1f}")
print("== ÖPPNA LUCKAN ==")
lid=U(['lucka','lucka_vit']); others=U([n for n in names if n not in ('lucka','lucka_vit')])
print("  ", [round(inter(lid.translate([0,8,-32.2]).rotate([a,0,0]).translate([0,-8,32.2]),others),1) for a in (0,-30,-60,-95)])
print("== NÖTENS VÄG: ur fickan, genom rännan, ut i skålen ==")
A=math.atan(0.84); CA,SA=math.cos(A),math.sin(A); fl=lambda y: 3.0+0.84*(y-3.4)
env=Ms['doserhus']+rot(Ms['doserhjul'],DUMP)+Ms['notmagasin']+Ms['kropp']+Ms['kropp_sockel']+Ms['kropp_vit']+Ms['skal']+Ms['skal_vit']
env=env+(lid.translate([0,8,-32.2]).rotate([-95,0,0]).translate([0,-8,32.2]))
for Dn in (18,20,22):
    r=Dn/2; bad=[]
    # kulan rullar på golvlinjen: centrum = golvpunkt + r * normal
    y_sw=3.4+(r-CA*r)/0.84
    y_start=YC+12.5*SA-CA*math.sqrt((R-PD+r)**2-(12.5-r)**2)        # nöten ligger i fickans botten när hjulet står i tömläge
    pts=[(yf-SA*r, fl(yf)+CA*r) for yf in np.arange(y_start,y_sw,-1.0)]+[(y,3.0+r) for y in np.arange(y_sw-SA*r,-30,-1.5)]
    for c in pts:
        v=inter(Manifold.sphere(r-0.5,48).translate([0,c[0],c[1]]),env)
        if v>0.5: bad.append((round(c[0],1),round(c[1],1),round(v,1)))
    print(f"   Ø{Dn}: {'fri väg' if not bad else bad[:5]}")
print("== NÖT I FICKAN, hjulet i viloläge och under vridning ==")
for Dn in (18,22):
    r=Dn/2; rc=R-PD+r     # nötens centrum från axeln
    res=[]
    for ang in (0,30,60,90,120,130):
        a=math.radians(ang); c=(YC-rc*math.sin(a), ZC+rc*math.cos(a))
        res.append(round(inter(Manifold.sphere(r-0.15,48).translate([0,c[0],c[1]]), Ms['doserhus']+Ms['notmagasin']+rot(Ms['doserhjul'],ang)),1))
    print(f"   Ø{Dn}: {res}")
`````

**Fil: `model/checks_size.py`** – Samma som checks8.py men med nötterna 21–24 mm (2026-11-15).

`````python
from lib import *
import sys
fn=sys.argv[1] if len(sys.argv)>1 else 'parts_v8.json'
parts,P=load(fn); names=[p['name'] for p in parts]; Ms={n:M(P,n) for n in names}
dj=json.load(open('disp.json')); YC,ZC,DUMP,R,PD=dj['YC'],dj['ZC'],dj['DUMP'],dj['R'],dj['PD']
inter=lambda a,b:(a^b).volume()
def U(ns):
    m=Manifold()
    for n in ns: m=m+Ms[n]
    return m
print("== KOLLISIONER I MONTERAT LÄGE (över 0,5 mm3) ==")
for i,a in enumerate(names):
    ba=Ms[a].bounding_box()
    for b in names[i+1:]:
        b2=Ms[b].bounding_box()
        if ba[0]>b2[3] or b2[0]>ba[3] or ba[1]>b2[4] or b2[1]>ba[4] or ba[2]>b2[5] or b2[2]>ba[5]: continue
        v=inter(Ms[a],Ms[b])
        if v>0.5: print(f"  {a} x {b}: {v:.1f}")
rot=lambda m,ang: m.translate([0,-YC,-ZC]).rotate([ang,0,0]).translate([0,YC,ZC])
print("== VRIDA HJULET 0–130° =="); o=U(['doserhus','notmagasin'])
print("  ", [round(inter(rot(Ms['doserhjul'],a),o),1) for a in (0,20,40,60,80,100,120,130)])
roof=['tak_v','tak_v_vit','tak_h','tak_h_vit','skorsten','skorsten_krage','takrannor','nockkilar','takpackning']
rest=[n for n in names if n not in roof]
print("== LYFTA TAKET ==", [round(inter(U(roof).translate([0,0,dz]),U(rest)),1) for dz in (1,5,20,60)])
print("== LYFTA MAGASINET =="); o3=U([n for n in rest if n!='notmagasin'])
print("  ", [round(inter(Ms['notmagasin'].translate([0,0,dz]),o3),1) for dz in (0,2,6,15,40,100,170)])
print("== LYFTA HJULET (magasinet borta, servot ute) =="); o4=U([n for n in rest if n not in ('notmagasin','doserhjul')])
print("  ", [round(inter(Ms['doserhjul'].translate([0,0,dz]),o4),1) for dz in (0,3,10,40,120)])
print("== SKRUVMEJSEL uppifrån ==")
o5=U(rest); o5b=U([n for n in rest if n!='notmagasin'])
for (x,y,z0,what,env_) in ((-20.3,27.5,102.5,'magasinets skruv v',o5),(21.8,27.5,102.5,'magasinets skruv h',o5),(-31.1,32.9,6,'doserhusets skruv v (magasinet borta)',o5b),(31.1,32.9,6,'doserhusets skruv h (magasinet borta)',o5b)):
    print(f"   {what}: {inter(cylz(x,y,z0,236,3.0),env_):.1f}")
print("== ÖPPNA LUCKAN ==")
lid=U(['lucka','lucka_vit']); others=U([n for n in names if n not in ('lucka','lucka_vit')])
print("  ", [round(inter(lid.translate([0,8,-32.2]).rotate([a,0,0]).translate([0,-8,32.2]),others),1) for a in (0,-30,-60,-95)])
print("== NÖTENS VÄG: ur fickan, genom rännan, ut i skålen ==")
A=math.atan(0.84); CA,SA=math.cos(A),math.sin(A); fl=lambda y: 3.0+0.84*(y-3.4)
env=Ms['doserhus']+rot(Ms['doserhjul'],DUMP)+Ms['notmagasin']+Ms['kropp']+Ms['kropp_sockel']+Ms['kropp_vit']+Ms['skal']+Ms['skal_vit']
env=env+(lid.translate([0,8,-32.2]).rotate([-95,0,0]).translate([0,-8,32.2]))
for Dn in (21,22,23,24):
    r=Dn/2; bad=[]
    # kulan rullar på golvlinjen: centrum = golvpunkt + r * normal
    y_sw=3.4+(r-CA*r)/0.84
    y_start=YC+12.5*SA-CA*math.sqrt((R-PD+r)**2-(12.5-r)**2)        # nöten ligger i fickans botten när hjulet står i tömläge
    pts=[(yf-SA*r, fl(yf)+CA*r) for yf in np.arange(y_start,y_sw,-1.0)]+[(y,3.0+r) for y in np.arange(y_sw-SA*r,-30,-1.5)]
    for c in pts:
        v=inter(Manifold.sphere(r-0.5,48).translate([0,c[0],c[1]]),env)
        if v>0.5: bad.append((round(c[0],1),round(c[1],1),round(v,1)))
    print(f"   Ø{Dn}: {'fri väg' if not bad else bad[:5]}")
print("== NÖT I FICKAN, hjulet i viloläge och under vridning ==")
for Dn in (21,22,23,24):
    r=Dn/2; rc=R-PD+r     # nötens centrum från axeln
    res=[]
    for ang in (0,30,60,90,120,130):
        a=math.radians(ang); c=(YC-rc*math.sin(a), ZC+rc*math.cos(a))
        res.append(round(inter(Manifold.sphere(r-0.15,48).translate([0,c[0],c[1]]), Ms['doserhus']+Ms['notmagasin']+rot(Ms['doserhjul'],ang)),1))
    print(f"   Ø{Dn}: {res}")
`````

**Fil: `model/overhang.py`** – Hittar områden i en STL som saknar underlag, lager för lager.

`````python
import trimesh, numpy as np, sys, os
from shapely.ops import unary_union
from shapely.geometry import Polygon
def layers(ms, step=0.2):
    top=max(m.bounds[1][2] for m in ms)
    for z in np.arange(0.1, top, step):
        polys=[]
        for part in ms:
            if z<part.bounds[0][2] or z>part.bounds[1][2]: continue
            sec=part.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
            if sec is None: continue
            p2,T=sec.to_planar()
            for pg in p2.polygons_full:
                e=trimesh.transform_points(np.c_[np.array(pg.exterior.coords),np.zeros(len(pg.exterior.coords))],T)[:,:2]
                hs=[trimesh.transform_points(np.c_[np.array(h.coords),np.zeros(len(h.coords))],T)[:,:2] for h in pg.interiors]
                q=Polygon(e,hs)
                if q.is_valid and q.area>0.05: polys.append(q)
        yield z, (unary_union(polys) if polys else None)
def report(files, thr=1.5):
    ms=[trimesh.load('stl/'+f) for f in files]; prev=None; out=[]
    for z,cur in layers(ms):
        if prev is not None and cur is not None:
            un=cur.difference(prev.buffer(1.2))
            for g in (list(un.geoms) if hasattr(un,'geoms') else [un]):
                if g.area>thr:
                    b=g.bounds; free=not g.buffer(0.01).intersects(prev)
                    out.append((round(z,1),round(g.area,1),round((b[0]+b[2])/2),round((b[1]+b[3])/2),round(b[2]-b[0],1),round(b[3]-b[1],1),'FRITT' if free else ''))
        prev=cur
    return out
if __name__=='__main__':
    r=report(sys.argv[1:])
    for x in r: print(x)
    print(len(r),"ställen,", sum(1 for x in r if x[-1]),"helt fristående")
`````

**Fil: `model/export5.py`** – Äldre STL-export, version 5.

`````python
import json, base64, numpy as np, trimesh, math, os, zipfile, io, re
parts=json.load(open('parts_v5.json')); P={p['name']:p for p in parts}
def T(n):
    p=P[n]; return trimesh.Trimesh(np.frombuffer(base64.b64decode(p['pos']),np.float32).reshape(-1,3), np.frombuffer(base64.b64decode(p['idx']),np.uint32).reshape(-1,3), process=False)
K=80/85; n=math.sqrt(1+K*K)
def group(names, files, R=np.eye(4)):
    ms=[T(x) for x in names]; allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    Tm=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
    from manifold3d import Manifold, Mesh
    for m,f in zip(ms,files):
        mt=trimesh.Trimesh(m.vertices,m.faces,process=True)
        man=Manifold(Mesh(vert_properties=np.asarray(mt.vertices,np.float32), tri_verts=np.asarray(mt.faces,np.uint32)))
        A=(Tm@R)[:3,:]                                        # transformen görs i manifold så topologin bevaras
        me=man.transform(A.T.tolist() if False else A.tolist()).to_mesh()
        trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False).export('stl/'+f)
group(['kropp','kropp_vit'],['05_kropp_rod.stl','05_kropp_vit.stl'])
group(['tak_v','tak_v_vit'],['06_tak_vanster_gra.stl','06_tak_vanster_vit.stl'], trimesh.geometry.align_vectors([K/n,0,-1/n],[0,0,-1]))
group(['tak_h','tak_h_vit'],['06b_tak_hoger_gra.stl','06b_tak_hoger_vit.stl'], trimesh.geometry.align_vectors([-K/n,0,-1/n],[0,0,-1]))
group(['takrannor'],['22_takrannor_gra.stl'])
group(['bottenplatta'],['03_bottenplatta.stl']); group(['framgard_platta'],['03b_framgard_bottenplatta.stl'])
# fönsterinsatser: plattan mot bädden, pluggarna uppåt
ins=T('fonsterrutor'); out=[]
for c in ins.split(only_watertight=False):
    c=c.copy(); right = c.centroid[0] > 0
    c.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2 if right else np.pi/2,[0,1,0]))
    c.apply_translation(-c.bounds[0]); c.apply_translation([0 if right else 60, 0, 0]); out.append(c)
if os.path.exists('stl/05b_fonsterrutor_gra.stl'): os.remove('stl/05b_fonsterrutor_gra.stl')
trimesh.util.concatenate(out).export('stl/05b_fonsterinsatser_gra.stl')
# nockkilar: ena benet platt mot bädden
k=T('nockkilar'); ko=[]
for i,c in enumerate(k.split(only_watertight=False)):
    c=c.copy(); c.apply_transform(trimesh.geometry.align_vectors([K/n,0,-1/n],[0,0,-1])); c.apply_translation(-c.bounds[0]); c.apply_translation([0,i*20,0]); ko.append(c)
trimesh.util.concatenate(ko).export('stl/06e_nockkilar_gra.stl')
# takpackning: fyra raka lister, 4,5 mm breda
L=math.hypot(85.3, 85.3*K)
trimesh.util.concatenate([trimesh.creation.box([L,4.5,1.65]).apply_translation([L/2, i*8+2.25, 0.825]) for i in range(4)]).export('stl/06d_takpackning_tpu.stl')
# fötter: skiva + tapp uppåt, packade (riktig union)
from manifold3d import Manifold
fm=Manifold()
for i in range(6):
    x,y=(i%3)*25,(i//3)*25
    fm += Manifold.cylinder(4,10,10,48).translate([x,y,0]) + Manifold.cylinder(1.95,2.1,2.1,24).translate([x,y,3.99])
me=fm.to_mesh(); trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts)).export('stl/04_fotter_tpu.stl')
for f in sorted(os.listdir('stl')):
    m=trimesh.load('stl/'+f)
    if not m.is_watertight: print("EJ TÄT", f)
print(len(os.listdir('stl')))
`````

**Fil: `model/export6.py`** – Äldre STL-export, version 6.

`````python
from lib import *
import os, zipfile
parts,P=load('parts_v7.json')
def export(names, files, R=np.eye(4), flipz=False):
    ms=[T(P,n) for n in names]
    if flipz: R=trimesh.transformations.rotation_matrix(np.pi,[1,0,0])@R
    allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])@R
    for m,f in zip(ms,files):
        man=Manifold(Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32))).transform(A[:3,:].tolist())
        me=man.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False)
        t.export('stl/'+f)
        chk=trimesh.load('stl/'+f, process=True)
        if not chk.is_watertight:
            chk.merge_vertices(digits_vertex=3); chk.update_faces(chk.nondegenerate_faces()); chk.remove_unreferenced_vertices(); trimesh.repair.fill_holes(chk); trimesh.repair.fix_normals(chk)
            if chk.is_watertight: chk.export('stl/'+f)
            else: print("EJ TÄT:", f)
rx=lambda a: trimesh.transformations.rotation_matrix(a,[1,0,0])
export(['kropp','kropp_vit'],['05_kropp_rod.stl','05_kropp_vit.stl'])
export(['skal','skal_vit'],['07_farstukvist_rod.stl','07_farstukvist_vit.stl'])
export(['doserare_bas'],['10_doserare_bas.stl'])
export(['notmagasin'],['14_notmagasin.stl'],flipz=True)
export(['elektroniklada'],['16_elektroniklada.stl'])                       # skrivs ut stående, öppningen uppåt
export(['ellock'],['16b_elektroniklada_lock.stl'],flipz=True)              # ovansidan mot plattan
export(['elpackning'],['17_elektroniklada_packning_tpu.stl'],rx(np.pi/2))
export(['monteringsplatta'],['24_monteringsplatta.stl'],rx(np.pi/2))       # distanserna uppåt
# takpackning: fyra raka lister
L=math.hypot(85.3,85.3*K)
trimesh.util.concatenate([trimesh.creation.box([L,4.5,1.43]).apply_translation([L/2,i*8+2.25,0.715]) for i in range(4)]).export('stl/06d_takpackning_tpu.stl')
# genomföringar platt: två runda + en avlång
def rg(cx,cy,z0,z1):
    g=cylz(cx,cy,z0-1.0,z0,6.5)+cylz(cx,cy,z0,z1,4.45)+cylz(cx,cy,z1,z1+1.0,6.5)
    return g-cylz(cx,cy,z0-2,z1+2,2.2)-box(cx-0.3,cx+6.6,cy-0.15,cy+0.15,z0-2,z1+2)
top=(box(-13,13,-7.5,7.5,3.4,4.4)+box(-10.95,10.95,-5.45,5.45,1.0,3.4)+box(-13,13,-7.5,7.5,0,1.0))-box(-7,7,-1.6,1.6,-1,6)-box(-0.2,0.2,-9,-1,-1,6)
allg=rg(7,7,1.0,3.4)+rg(23,7,1.0,3.4)+top.translate([15,26,0])
toT(allg,0.1).export('stl/25_genomforingar_tpu.stl')

# ---------- 00: toleranstest + nötmall ----------
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
def text(txt,size,depth):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd).extrude(depth)
def lead(x,y,z,r): return Manifold.cylinder(0.8,r,r+0.5,32).translate([x,y,z-0.79])
Hh=8.0
tp=box(0,92,0,46,0,Hh)
tp=tp-cylz(17,23,-1,Hh+1,11.0,64)                                              # nötmall: 22 mm
tp=tp-cylz(40,12,Hh-6.0,Hh+1,2.0)-lead(40,12,Hh,2.0)                            # M3-insats
tp=tp-cylz(40,34,Hh-6.5,Hh+1,2.8)-lead(40,34,Hh,2.8)                            # M4-insats
tp=tp-cylz(56,12,Hh-3.3,Hh+1,4.95)                                              # magnetficka Ø 9,9
tp=tp-cylz(52,34,Hh-3.0,Hh+1,1.45)-cylz(60,34,Hh-3.0,Hh+1,1.25)                 # hål för tappar
def bow(sh): 
    w0,w1,Lb=3.0-sh,6.5-sh,13.0-sh
    return CrossSection([ccw([(-w1,-Lb),(-w0,0),(-w1,Lb),(w1,Lb),(w0,0),(w1,-Lb)])])
tp=tp-bow(0).extrude(3.2).translate([78,23,Hh-3.0])                             # spår för nockkil
for (txt,x,y) in (("22",17,40.5),("M3",31,12),("M4",31,34),("MAG",69,5)):
    tp=tp-text(txt,4.2,0.7).translate([x,y,Hh-0.6])
key=bow(0.06).extrude(2.95).translate([106,16,0])                               # lös nockkil
pinb=box(98,114,34,44,0,3)+cylz(102,39,2.9,6,1.4,24)+cylz(110,39,2.9,6,1.2,24)  # lösa tappar
toT(tp+key+pinb,0.1).export('stl/00_toleranstest.stl')
for f in sorted(os.listdir('stl')):
    m=trimesh.load('stl/'+f)
    if not m.is_watertight: print("EJ TÄT", f)
print(len(os.listdir('stl')),"filer")
`````

**Fil: `model/export8.py`** – STL-export för version 7, inklusive toleranstestet.

`````python
from lib import *
import os
parts,P=load('parts_v8.json')
def export(names, files, R=np.eye(4), flipz=False):
    ms=[T(P,n) for n in names]
    if flipz: R=trimesh.transformations.rotation_matrix(np.pi,[1,0,0])@R
    allv=trimesh.transform_points(np.vstack([m.vertices for m in ms]),R); lo,hi=allv.min(0),allv.max(0)
    A=trimesh.transformations.translation_matrix([-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])@R
    for m,f in zip(ms,files):
        man=Manifold(Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32))).transform(A[:3,:].tolist())
        me=man.to_mesh(); trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False).export('stl/'+f)
        chk=trimesh.load('stl/'+f, process=True)
        if not chk.is_watertight:
            chk.merge_vertices(digits_vertex=3); chk.update_faces(chk.nondegenerate_faces()); chk.remove_unreferenced_vertices(); trimesh.repair.fill_holes(chk); trimesh.repair.fix_normals(chk)
            if chk.is_watertight: chk.export('stl/'+f)
            else: print("EJ TÄT:", f)
for f in ('10_doserare_bas.stl','11_doserare_kammare.stl','12_doseringsskiva.stl','13_doseringslock.stl','20_avstrykare_tpu.stl'):
    if os.path.exists('stl/'+f): os.remove('stl/'+f)
export(['kropp','kropp_vit','kropp_sockel'],['05_kropp_rod.stl','05_kropp_vit.stl','05_kropp_sockel_gra.stl'])
export(['doserhus'],['10_doserhus.stl'])
export(['doserhjul'],['11_doserhjul.stl'],trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))   # hornurtaget mot plattan
export(['notmagasin'],['14_notmagasin.stl'],flipz=True)
# toleranstest med nötmall: 22 mm ska gå igenom, 18 mm ska inte
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
def text(txt,size,depth):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd).extrude(depth)
def lead(x,y,z,r): return Manifold.cylinder(0.8,r,r+0.5,32).translate([x,y,z-0.79])
Hh=8.0
tp=box(0,116,0,46,0,Hh)
tp=tp-cylz(16,21,-1,Hh+1,11.0,72)-cylz(43,21,-1,Hh+1,9.0,72)                    # nötmall: 22 mm och 18 mm
tp=tp-cylz(64,12,Hh-6.0,Hh+1,2.0)-lead(64,12,Hh,2.0)-cylz(64,34,Hh-6.5,Hh+1,2.8)-lead(64,34,Hh,2.8)   # M3- och M4-insats
tp=tp-cylz(80,12,Hh-3.3,Hh+1,4.95)                                              # magnetficka
tp=tp-cylz(76,34,Hh-3.0,Hh+1,1.45)-cylz(84,34,Hh-3.0,Hh+1,1.25)                 # hål för tappar
def bow(sh):
    w0,w1,Lb=3.0-sh,6.5-sh,13.0-sh
    return CrossSection([ccw([(-w1,-Lb),(-w0,0),(-w1,Lb),(w1,Lb),(w0,0),(w1,-Lb)])])
tp=tp-bow(0).extrude(3.2).translate([102,23,Hh-3.0])
for (txt,x,y,sz) in (("22",16,40.5,4.6),("18",43,40.5,4.6),("M3",56,12,4),("M4",56,34,4),("MAG",80,22,3.6)):
    tp=tp-text(txt,sz,0.7).translate([x,y,Hh-0.6])
key=bow(0.06).extrude(2.95).translate([130,16,0])
pinb=box(122,138,34,44,0,3)+cylz(126,39,2.9,6,1.4,24)+cylz(134,39,2.9,6,1.2,24)
toT(tp+key+pinb,0.1).export('stl/00_toleranstest.stl')
bad=[f for f in sorted(os.listdir('stl')) if not trimesh.load('stl/'+f).is_watertight]
print(len(os.listdir('stl')),"filer; ej täta:",bad)
`````

**Fil: `model/plates.py`** – Äldre plattlayout.

`````python
import trimesh, os, json, base64, numpy as np, collections, re
from rectpack import newPacker, MaxRectsBssf
P={p['file']:p for p in json.load(open('parts_v7.json'))}
P['00_toleranstest.stl']=dict(color='#9AA0A6',note='Valfri färg. Skrivs ut först: passningar och nötmall (22 mm)')
s=open('/mnt/user-data/outputs/lennarts-matstation-3d.html').read()
TIMES=json.loads(re.search(r'const TIMES = (\{[^}]*\});', s).group(1))
groups=collections.OrderedDict()
for f in sorted(os.listdir('stl')): groups.setdefault(f.split('_')[0],[]).append(f)
PLATE, MARGIN, GAP = 256.0, 5.0, 6.0
DUALW = 235.5                      # bredd som båda munstyckena når (X2D)
XOFF = (PLATE-DUALW)/2
items={}
for g,fs in groups.items():
    ms=[trimesh.load('stl/'+f) for f in fs]
    v=np.vstack([m.vertices for m in ms]); lo,hi=v.min(0),v.max(0)
    items[g]=dict(files=fs, meshes=ms, lo=lo, w=hi[0]-lo[0], d=hi[1]-lo[1], h=hi[2]-lo[2], tpu=all('tpu' in f for f in fs))
def pack(keys):
    pk=newPacker(pack_algo=MaxRectsBssf, rotation=True)
    for g in keys: pk.add_rect(int(np.ceil(items[g]['w']+GAP)*10), int(np.ceil(items[g]['d']+GAP)*10), rid=g)
    for _ in range(len(keys)): pk.add_bin(int((DUALW-2*MARGIN+GAP)*10), int((PLATE-2*MARGIN+GAP)*10))
    pk.pack()
    out=[]
    for b in pk:
        if len(b)==0: continue
        rects=[]
        for r in b:
            it=items[r.rid]; rot = abs(r.width - int(np.ceil(it['w']+GAP)*10)) > 1 and abs(r.width - int(np.ceil(it['d']+GAP)*10)) <= 1
            rects.append((r.rid, r.x/10+MARGIN+XOFF, r.y/10+MARGIN, rot))
        out.append(rects)
    return out
PHASES=[("Först: toleranstest och nötmall", ["00"]),
        ("1. Kan skrivas ut direkt", ["01","01b","02","02b","03","03b","05b","05c","06","06b","06c","06d","06e","16","16b","17","21","21b","22","23","24","25","04"]),
        ("2. Doseraren – när servot är uppmätt, provkör innan resten", ["10","11","12","13","14","20"]),
        ("3. När skärm, kamera och luckservo är uppmätta", ["05"]),
        ("3. När skärm, kamera och luckservo är uppmätta", ["05d","07","08","09","09b","15","18","19"])]
assert sorted(sum([p[1] for p in PHASES],[]))==sorted(items.keys()), set(items)-set(sum([p[1] for p in PHASES],[]))
plates=[]
for phase, keys in PHASES:
    a=[g for g in keys if not items[g]['tpu']]; t=[g for g in keys if items[g]['tpu']]
    a.sort(key=lambda g: (g!='00', -(items[g]['w']*items[g]['d'])))
    plates += [('ASA',p,phase) for p in pack(a)] + [('TPU',p,phase) for p in pack(t)]
Q=0.005
out=[]
for mat, rects, phase in plates:
    pl=dict(material=mat, phase=phase, items=[], hours=0.0)
    for g,x,y,rot in rects:
        it=items[g]; pl['hours']+=TIMES.get(g,0.1)
        for f,m in zip(it['files'], it['meshes']):
            v=m.vertices-it['lo']
            if rot: v=np.c_[v[:,1], it['w']-v[:,0], v[:,2]]     # 90° vridning på plattan
            v=v+[x,y,0]
            assert v.min()>-0.01 and v[:,0].max()<=PLATE+0.01 and v[:,1].max()<=PLATE+0.01, (g, v.min(0), v.max(0))
            qv=np.clip(np.round(v/Q),0,65535).astype(np.uint16)
            idx=m.faces.astype(np.uint16 if len(v)<65536 else np.uint32)
            pl['items'].append(dict(group=g, file=f, color=P.get(f,{}).get('color','#9A9A9A'), note=P.get(f,{}).get('note',''),
                                    pos=base64.b64encode(qv.tobytes()).decode(), idx=base64.b64encode(idx.tobytes()).decode(), i32=idx.dtype==np.uint32))
    pl['hours']=round(pl['hours'],2); out.append(pl)
json.dump(out, open('plates.json','w'))
for i,pl in enumerate(out):
    print(i+1, pl['phase'][:2], pl['material'], pl['hours'], sorted(set(it['group'] for it in pl['items'])))
print("storlek", round(os.path.getsize('plates.json')/1e6,2),"MB")
`````

**Fil: `model/plates8.py`** – Plattlayout för fliken Utskrift, med tidsuppskattning, faser och redan utskrivna plattor. Aktuell.

`````python
import trimesh, os, json, base64, numpy as np, collections, re
from rectpack import newPacker, MaxRectsBssf
P={p['file']:p for p in json.load(open('parts_v11.json'))}
P['00_toleranstest.stl']=dict(color='#C8CCD0',note='Valfri färg. Passningar och nötmall')
NAME={"00":"Toleranstest och nötmall","01":"Bas","01b":"Framgård","02":"Gräsmatta","02b":"Framgårdens gräsmatta","03":"Bottenplatta","03b":"Framgårdens bottenplatta","04":"Fötter",
 "05":"Kropp med stengrund","05b":"Fönsterinsatser","05c":"Kamerans solskydd","05d":"Packning under kroppen","06":"Takhalva, vänster","06b":"Takhalva, höger","06c":"Skorsten","06d":"Takpackning","06e":"Nockkilar",
 "07":"Farstukvist","08":"Lucka","09":"Stolphatt","09b":"Packning under stolphatten","10":"Doserhus","11":"Doserhjul","14":"Nötmagasin","15":"Kamerafäste","16":"Elektroniklåda","16b":"Lock till elektroniklådan",
 "17":"Packning till elektroniklådan","18":"Skärmram","19":"Skärmklämma","21":"Blomlådor","21b":"Blomhuvuden","22":"Takrännor","23":"Stuprör","24":"Monteringsplatta","25":"Kabelgenomföringar"}
HOW={"00":"Skrivs ut allra först","01":"Upp och ner: ovansidan ligger mot plattan och hålrummet är öppet uppåt","01b":"Upp och ner, som basen","02":"Gräset uppåt","02b":"Gräset uppåt","03":"Ligger platt","03b":"Ligger platt","04":"Tappen uppåt",
 "05":"Står som huset står, stengrunden mot plattan. Grått de första 10 mm, sedan rött","05b":"Plattan nedåt, pluggarna uppåt","05c":"Väggsidan mot plattan","05d":"Ligger platt","06":"Undersidan mot plattan, pannorna uppåt","06b":"Undersidan mot plattan, pannorna uppåt",
 "06c":"Upp och ner: kragen mot plattan","06d":"Ligger platt","06e":"På högkant","07":"Står som den sitter","08":"Ligger platt, pannorna uppåt","09":"Står som den sitter","09b":"Ligger platt","10":"Står som det sitter",
 "11":"Hornurtaget mot plattan, axeltappen uppåt","14":"Upp och ner: överkanten mot plattan","15":"Står som det sitter","16":"Står, öppningen uppåt","16b":"Upp och ner","17":"Ligger platt","18":"Ligger platt","19":"Plattan nedåt",
 "21":"Står som de sitter","21b":"Ligger platt, ansiktet uppåt","22":"Öppningen uppåt","23":"Står som de sitter","24":"Distanserna uppåt","25":"Ligger platt"}
groups=collections.OrderedDict()
WK={'hornbrada':'Hörnbräda','sidofonster':'Sidofönster','skarmfonster':'Skärmfönstrets ram','dorroverstycke':'Dörröverstycke','kamerakrage':'Kamerakrage'}
for f in sorted(os.listdir('stl')):
    if f.startswith('05e_'):
        k=f[:-4]; parts_=k.split('_'); nm=WK[parts_[2]]+(' '+parts_[3] if len(parts_)>3 else '')
        NAME[k]=nm+', vit'; HOW[k]='Framsidan nedåt, den korta flänsen uppåt' if parts_[2]=='hornbrada' else 'Baksidan nedåt, hålen för tapparna mot plattan'
        P[f]=dict(color='#F2EDE1')
        groups.setdefault(k,[]).append(f)
    else: groups.setdefault(f.split('_')[0],[]).append(f)
PLATE, MARGIN, GAP, DUALW = 256.0, 5.0, 6.0, 235.5
XOFF=PLATE-DUALW          # höger munstycke når inte de 20,5 mm längst till vänster
items={}; times={}
def cover(m,zs):
    tz=m.vertices[m.faces][:,:,2]; lo,hi=tz.min(1),tz.max(1); return np.array([np.any((lo<=z)&(hi>=z)) for z in zs])
for g,fs in groups.items():
    ms=[trimesh.load('stl/'+f) for f in fs]
    v=np.vstack([m.vertices for m in ms]); lo,hi=v.min(0),v.max(0)
    items[g]=dict(files=fs, meshes=ms, lo=lo, w=hi[0]-lo[0], d=hi[1]-lo[1], h=hi[2]-lo[2], tpu=all('tpu' in f for f in fs))
    # tidsuppskattning: 0,20 mm lager, skal + 15 % fyllnad, färgbyten
    Hh=hi[2]-lo[2]; LH=0.2; layers=Hh/LH
    ext=sum(min(abs(m.volume), m.area*1.2+max(0,abs(m.volume)-m.area*0.6)*0.15) for m in ms)
    t=ext/11.0+layers*2.5
    if len(ms)>1:
        zs=np.arange(lo[2]+LH/2,hi[2],LH*5); cnt=np.array([cover(m,zs) for m in ms]).sum(0)
        t+=(cnt>=2).sum()*5*2*12+(cnt>=3).sum()*5*2*55
    times[g]=round(t/3600,2)
def pack(keys):
    pk=newPacker(pack_algo=MaxRectsBssf, rotation=True)
    for g in keys: pk.add_rect(int(np.ceil(items[g]['w']+GAP)*10), int(np.ceil(items[g]['d']+GAP)*10), rid=g)
    for _ in range(len(keys)): pk.add_bin(int((DUALW-2*MARGIN+GAP)*10), int((PLATE-2*MARGIN+GAP)*10))
    pk.pack(); out=[]
    for b in pk:
        if len(b)==0: continue
        rects=[]
        for r in b:
            it=items[r.rid]; rot=abs(r.width-int(np.ceil(it['w']+GAP)*10))>1 and abs(r.width-int(np.ceil(it['d']+GAP)*10))<=1
            rects.append((r.rid, r.x/10+MARGIN+XOFF, r.y/10+MARGIN, rot))
        out.append(rects)
    return out
DONE="Redan utskrivet"
PHASES=[(DONE, ["16","16b","24"]),
        (DONE, ["01"]),
        (DONE, ["03"]),
        ("Först: toleranstest och nötmall", ["00"]),
        ("Nästa: kroppen i rött och grått", ["05"]),
        ("Sedan: de vita detaljerna", [f[:-4] for f in sorted(os.listdir('stl')) if f.startswith('05e_')]),
        ("1. Kan skrivas ut direkt", ["01b","02","02b","03b","05b","05c","06","06b","06c","06d","06e","17","21","21b","22","23","25","04"]),
        ("2. Doseringen – när servot är uppmätt, provkör innan resten", ["10","11","14"]),
        ("3. När skärm, kamera och luckservo är uppmätta", ["05d","07","08","09","09b","15","18","19"])]
assert sorted(sum([p[1] for p in PHASES],[]))==sorted(items.keys()), set(items)^set(sum([p[1] for p in PHASES],[]))
plates=[]
for phase,keys in PHASES:
    a=[g for g in keys if not items[g]['tpu']]; t=[g for g in keys if items[g]['tpu']]
    a.sort(key=lambda g:-(items[g]['w']*items[g]['d']))
    plates+=[('ASA',p,phase) for p in pack(a)]+[('TPU',p,phase) for p in pack(t)]
Q=0.005; out=[]
for mat,rects,phase in plates:
    pl=dict(material=mat, phase=phase, items=[], groups=[], hours=0.0, printed=(phase==DONE))
    for g,x,y,rot in rects:
        it=items[g]; pl['hours']+=times[g]
        w,d=(it['d'],it['w']) if rot else (it['w'],it['d'])
        pl['groups'].append(dict(g=g,name=NAME[g],how=HOW[g],hours=times[g],cx=round(x+w/2,1),cy=round(y+d/2,1),top=round(float(it['h']),1),files=it['files'],
                                 colors=[P.get(f,{}).get('color','#9A9A9A') for f in it['files']]))
        for f,m in zip(it['files'],it['meshes']):
            v=m.vertices-it['lo']
            if rot: v=np.c_[v[:,1], it['w']-v[:,0], v[:,2]]
            v=v+[x,y,0]
            qv=np.clip(np.round(v/Q),0,65535).astype(np.uint16); idx=m.faces.astype(np.uint16 if len(v)<65536 else np.uint32)
            col=P.get(f,{}).get('color','#9A9A9A')
            if col.lower() in ('#2b2b2b','#1a1a1a'): col='#4A4D50'      # svarta delar syns bättre
            pl['items'].append(dict(group=g,file=f,color=col,pos=base64.b64encode(qv.tobytes()).decode(),idx=base64.b64encode(idx.tobytes()).decode(),i32=bool(idx.dtype==np.uint32)))
    pl['hours']=round(pl['hours'],2); pl['height']=max(gr['top'] for gr in pl['groups']); out.append(pl)
json.dump(out,open('plates.json','w')); json.dump(times,open('times.json','w'))
for i,pl in enumerate(out): print(i+1, pl['phase'][:2], pl['material'], pl['hours'], [gr['g'] for gr in pl['groups']])
print("total h", round(sum(times.values()),1), "| storlek", round(os.path.getsize('plates.json')/1e6,2),"MB")
`````

**Fil: `model/page8.py`** – 2026-11-11: uppdaterar förhandsgranskningen med hjul-demo, taklyft, röntgen och montering.

`````python
import re, json, base64, zipfile, io, os, markdown
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
def region(start, end, new, keep_end=True):
    global s
    i=s.index(start); j=s.index(end, i)
    s=s[:i]+new+(s[j:] if keep_end else s[j+len(end):])
# ---------- data ----------
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v8.json').read()+s[j:]
R('const LABEL = {','const LABEL = {doserhus:"Doserhus med ränna",doserhjul:"Doserhjul",kropp_sockel:"Stengrund",')
R('const PIVOT = {doseringsskiva:[0,64,0], lucka:[0,-8,32.2], lucka_vit:[0,-8,32.2]};','const PIVOT = {doserhjul:[0,57,64.3], lucka:[0,-8,32.2], lucka_vit:[0,-8,32.2]};')
times=json.load(open('times.json'))
m=re.search(r'const TIMES = (\{[^}]*\});', s); s=s[:m.start(1)]+json.dumps(times)+s[m.end(1):]
# ---------- kontroller ----------
R('<div class="views"><button type="button" id="reset">Återställ vy</button><button type="button" data-v="close">Närbild</button></div>',
  '<div class="views"><button type="button" id="reset">Återställ vy</button><button type="button" data-v="close">Närbild</button><button type="button" data-v="front">Framifrån</button><button type="button" data-v="side">Från sidan</button><button type="button" data-v="inside">Inuti</button></div>')
R('''        <button class="act" id="lidbtn" type="button"><span class="ic" style="background:#2B7546">&#8645;</span>Öppna / Stäng lucka</button>''',
  '''        <button class="act" id="lidbtn" type="button"><span class="ic" style="background:#2B7546">&#8645;</span>Öppna / Stäng lucka</button>
        <button class="act" id="roofbtn" type="button"><span class="ic" style="background:#5A5E62">&#8679;</span>Lyft av taket</button>''')
R('''        <label class="row"><input type="checkbox" id="ghost"> Genomskinlig kropp</label>''',
  '''        <label class="row"><input type="checkbox" id="ghost"> Genomskinliga väggar och tak</label>
        <label class="row"><input type="checkbox" id="xray"> Röntgen: allt genomskinligt</label>''')
R('''      <div class="facts" id="facts"></div>''','''      <fieldset><legend>Montering</legend>
        <button class="act" id="asmStart" type="button"><span class="ic" style="background:#3B6A2B">&#9776;</span>Visa monteringen steg för steg</button>
        <div id="asmBox" hidden>
          <p class="asmt" id="asmTitle"></p><p class="asmx" id="asmText" aria-live="polite"></p>
          <div class="asmnav"><button type="button" id="asmPrev">Föregående</button><button type="button" id="asmNext">Nästa</button><button type="button" id="asmEnd">Visa allt</button></div>
        </div>
      </fieldset>
      <div class="facts" id="facts"></div>''')
R('</style>','''.asmt{font-weight:700;margin:.2rem 0 .2rem}
.asmx{margin:0 0 .6rem;color:var(--ink-2);font-size:.95rem}
.asmnav{display:flex;gap:.4rem;flex-wrap:wrap}
.asmnav button{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
.asmnav button:disabled{opacity:.45;cursor:default}
.plabel{position:absolute;transform:translate(-50%,-110%);font-size:.78rem;line-height:1.2;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:.1rem .45rem;pointer-events:none;white-space:nowrap}
.pinfo li{cursor:pointer;border-radius:6px;padding:.4rem .3rem}
.pinfo li[aria-pressed="true"]{background:var(--surface);outline:1px solid var(--line)}
.pinfo li b{display:block}
.pinfo li small{color:var(--ink-2);display:block}
</style>''')
# ---------- apply(): röntgen, taklyft, montering ----------
region('let solo = null;\nfunction apply(){', '// faktaruta och tabell', r'''let solo = null;
const xray = document.getElementById("xray"); xray.addEventListener("change", apply);
let roofLift = 0, asmStep = 0, asmAnim = 1;
const SOLID_IN_XRAY = new Set(["doserhjul","lucka","lucka_vit"]);
// monteringen i tio steg, i den ordning delarna sätts ihop
const ASM = [
  {title:"Basen", text:"Lägg ballasten i basen och skruva på bottenplattorna. Skruva ihop basen och framgården med tre skruvar och tryck i fötterna.", from:[0,0,-120], parts:["bas","framgard","bottenplatta","framgard_platta","fotter"]},
  {title:"Gräsmattorna", text:"Lägg gräsmattorna och stenplattorna på basen och framgården.", parts:["grasmatta","stenar","framgard_gras","framgard_stenar"]},
  {title:"Kroppen", text:"Lägg packningen på plats och ställ kroppen på de två styrtapparna. Dra sex skruvar inifrån.", parts:["kropp_packning","kropp","kropp_sockel","kropp_vit"]},
  {title:"Insidan av kroppen", text:"Gör klart insidan medan den är tom: fönsterinsatserna, skärmen med ram och klämma, och kameran med sitt fäste.", from:[0,90,60], parts:["fonsterrutor","skarmram","skarmklamma","kamerafaste"]},
  {title:"Elektroniken", text:"Skruva fast elektroniklådan utifrån genom bakväggen. Skjut ner monteringsplattan med all elektronik uppifrån och lägg på locket.", parts:["elpackning","elektroniklada","monteringsplatta","ellock","genomforingar"]},
  {title:"Doseringen", text:"Ställ doserhuset på sina styrtappar och dra två skruvar. Lägg hjulet i sätet och skruva fast servot från höger.", parts:["doserhus","doserhjul"]},
  {title:"Magasinet", text:"Sätt magasinet över hjulet och dra dess två skruvar framtill. Fyll på med nötter.", parts:["notmagasin"]},
  {title:"Farstukvisten", text:"Skruva fast skålen i basen, montera luckan med sitt servo och sätt på stolphatten.", from:[0,-110,30], parts:["skal","skal_vit","lucka","lucka_vit","servopackning","servokapa"]},
  {title:"Taket", text:"Pressa ihop takhalvorna med nockkilarna, tryck fast skorstenen och takrännorna och lägg taket på plats. Magneterna håller det.", parts:["tak_v","tak_v_vit","tak_h","tak_h_vit","nockkilar","skorsten","skorsten_krage","takrannor","takpackning"]},
  {title:"Detaljerna", text:"Tryck fast kamerans solskydd, häng blomlådorna på fönsterkarmarna och snäpp fast stuprören.", from:[0,-60,90], parts:["solskydd","solskydd_vit","blomlador","blomlador_vaxter","blomlador_blommor_rod","blomlador_blommor_vit","stupror","stupror_vit"]}
];
const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1));
function apply(){
  const f = ex.value/100;
  meshes.forEach(m => {
    const p = m.userData, o = EXPLODE[p.group], b = m.userData.holder.userData.base;
    let dx = o[0]*f, dy = o[1]*f, dz = o[2]*f;
    if(p.group==="Tak") dz += roofLift*150;
    let vis = solo ? p.name===solo : state[p.group];
    if(asmStep && !solo){
      const st = STEP_OF[p.name] || 1; vis = st <= asmStep;
      if(st===asmStep){ const k = 1-asmAnim, d = ASM[st-1].from || [0,0,170]; dx += d[0]*k; dy += d[1]*k; dz += d[2]*k; }
    }
    m.userData.holder.position.set(b[0]+dx, b[1]+dy, b[2]+dz);
    m.visible = vis;
    let op = 1;
    if(!solo){
      if(xray.checked && !SOLID_IN_XRAY.has(p.name)) op = 0.14;
      else if(ghost.checked && (p.group==="Kropp" || p.group==="Tak")) op = p.group==="Tak" ? 0.12 : 0.18;
    }
    m.material.opacity = op; m.material.depthWrite = op===1; m.castShadow = op===1;
  });
  const inner = !solo && ex.value==0 && state.Inredning;
  nutsGroup.visible = inner && (!asmStep || asmStep>=7);
  screenMesh.visible = !solo && state.Kropp && (!asmStep || asmStep>=4);
  camG.visible = inner && (!asmStep || asmStep>=4);
  camGlass.visible = !solo && state.Kropp && ex.value==0 && (!asmStep || asmStep>=4);
  draw();
}
''')
R('<p>Magasinet rymmer ca 0,35 liter hasselnötter</p>','<p>Magasinet rymmer ca 0,35 liter, ungefär 50 hasselnötter</p><p>Nötter: i skal, 18–22 mm</p>')
# vyknappar
R('''  else if(v==="door"){ TARGET.set(420,520,300); Object.assign(view,{th:0.22, ph:1.0, r:3000}); cam.fov=50; }''',
  '''  else if(v==="door"){ TARGET.set(420,520,300); Object.assign(view,{th:0.22, ph:1.0, r:3000}); cam.fov=50; }
  else if(v==="front"){ const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,120+z,-10); Object.assign(view,{th:0, ph:1.45, r:820}); cam.fov=32; }
  else if(v==="side" || v==="inside"){ const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,95+z,-55); Object.assign(view,{th:-1.45, ph:1.42, r:620}); cam.fov=32; if(v==="inside" && !xray.checked){ xray.checked = true; apply(); } }''')
# ---------- demo: hjul i stället för skiva, tak som lyfts ----------
region('const nutGeo = new THREE.SphereGeometry', 'new ResizeObserver(resize).observe(stage);', r'''const nutGeo = new THREE.SphereGeometry(8.5, 18, 12); nutGeo.scale(1,1,1.15);
const nutMat = new THREE.MeshStandardMaterial({color:"#8A5A2E", roughness:.7});
const wheel = meshes.find(m=>m.userData.name==="doserhjul").userData.holder;        // vrids kring sin axel
const DUMP = 130*Math.PI/180, AX = [0,57,64.3], PKT = 19.3;                           // tömvinkel, axelns läge, nötens avstånd från axeln i fickan
const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set rx(v){ lids.forEach(h=>h.rotation.x=v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};
// platser i magasinet: en nöt i halsen över hjulet, resten i tratten och lådan ovanför
const SLOTS = [[0,57,105.5],[-10,56,116],[10,56,116],[0,73,117]];
for(const y of [52,70,88]) for(const x of [-20,0,20]) SLOTS.push([x,y,132]);
for(const z of [150,166]) for(const y of [49,65.5,82,97]) for(const x of [-34,-17,0,17,34]) SLOTS.push([x+(z===166?2:0), y+(z===166?1:0), z]);
const nearAxis = p => Math.hypot(p[0], p[1]-57);
SLOTS.sort((a,b)=> (a[2]-b[2]) || (nearAxis(a)-nearAxis(b)));
const hopper = []; let pocket = null; const trayNuts = []; let busy = false;
const tweens = [];
function tween(dur, fn, delay=0){ return new Promise(res => tweens.push({t0:performance.now()+delay, dur, fn, res})); }
let raf = 0;
function tick(now){
  for(let i=tweens.length-1;i>=0;i--){ const tw=tweens[i]; const k=(now-tw.t0)/tw.dur; if(k<0) continue; const e=Math.min(1,k); tw.fn(e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2); if(e>=1){ tweens.splice(i,1); tw.res(); } }
  draw(); raf = tweens.length ? requestAnimationFrame(tick) : 0;
}
function run(){ if(!raf) raf = requestAnimationFrame(tick); }
const lerp=(a,b,t)=>a+(b-a)*t;
function path(obj, pts, dur, delay=0){
  const seg=[]; let L=0; for(let i=1;i<pts.length;i++){ const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1],pts[i][2]-pts[i-1][2]); seg.push(d); L+=d; }
  return tween(dur, t => { let s=t*L, i=0; while(i<seg.length-1 && s>seg[i]){ s-=seg[i]; i++; } const u=Math.min(1,s/seg[i]); const a=pts[i], b=pts[i+1]; obj.position.set(lerp(a[0],b[0],u),lerp(a[1],b[1],u),lerp(a[2],b[2],u)); obj.rotation.x+=0.15; }, delay);
}
function status(){ document.getElementById("status").textContent = `I magasinet: ${hopper.length + (pocket?1:0)} nötter. I skålen: ${trayNuts.length}.`; }
function demoView(){ if(view.r>1500) preset("close"); if(ex.value!=0){ ex.value=0; } if(asmStep) asmGo(0); solo=null; markRow(); apply(); }
function seat(n){ nutsGroup.remove(n); wheel.add(n); n.position.set(0,0,PKT); }                 // nöten ligger i hjulets ficka
function unseat(n){ const w=new THREE.Vector3(); n.getWorldPosition(w); nutsGroup.worldToLocal(w); wheel.remove(n); nutsGroup.add(n); n.position.copy(w); }
function loadPocket(){
  if(pocket || !hopper.length) return Promise.resolve();
  const n = hopper.shift(); pocket = n; const from = n.position.toArray();
  return path(n, [from, [0,57,Math.max(from[2],106)], [0,57,AX[2]+PKT]], 450).then(()=>seat(n));
}
const fillBtn = document.getElementById("fill"), roofBtn = document.getElementById("roofbtn");
const isFull = () => hopper.length === SLOTS.length-1 && !!pocket;
function fillLabel(){ fillBtn.lastChild.textContent = isFull() ? "Töm behållaren" : "Fyll på nötter"; }
function freeSlots(){ const used = new Set(hopper.map(n=>n.userData.slot)); return SLOTS.map((s,i)=>i).filter(i=>!used.has(i)); }
function sortHopper(){ hopper.sort((a,b)=> (a.position.z-b.position.z) || (nearAxis(a.position.toArray())-nearAxis(b.position.toArray()))); }
function addNut(i){ const n = new THREE.Mesh(nutGeo, nutMat); n.userData.slot = i; n.rotation.set(Math.random()*3,Math.random()*3,0); nutsGroup.add(n); hopper.push(n); return n; }
let roofUp = false;
async function moveRoof(upNow){
  if(roofUp===upNow) return; const a = roofLift, b = upNow ? 1 : 0;
  const tw = tween(900, t => { roofLift = a+(b-a)*t; apply(); }); run(); await tw;
  roofUp = upNow; roofBtn.lastChild.textContent = roofUp ? "Lägg på taket" : "Lyft av taket";
}
roofBtn.addEventListener("click", async () => { if(busy) return; busy=true; demoView(); await moveRoof(!roofUp); busy=false; });
fillBtn.addEventListener("click", async () => {
  if(busy) return; busy=true; demoView();
  const wasUp = roofUp; await moveRoof(true);                    // taket lyfts av, precis som när man fyller på på riktigt
  if(isFull()){
    const all = hopper.splice(0).concat(trayNuts.splice(0)); if(pocket){ unseat(pocket); all.push(pocket); pocket=null; }
    const jobs = all.map((n,i) => path(n, [n.position.toArray(), [n.position.x, n.position.y, 330]], 600, i*12).then(()=>nutsGroup.remove(n)));
    run(); await Promise.all(jobs);
  } else {
    const jobs=[]; const free = freeSlots(); if(pocket) free.shift();           // halsens plats står tom när en nöt redan ligger i fickan? nej: den fylls
    freeSlots().forEach((i,k) => { const s=SLOTS[i]; const n=addNut(i); n.position.set(s[0], s[1], 330); jobs.push(path(n, [[s[0],s[1],330],[s[0],s[1],s[2]]], 650, k*30)); });
    run(); await Promise.all(jobs); sortHopper();
    if(!pocket){ const p = loadPocket(); run(); await p; const i=freeSlots()[0]; if(i!==undefined){ const s=SLOTS[i]; const n=addNut(i); n.position.set(...s); sortHopper(); } }
  }
  if(!wasUp) await moveRoof(false);
  status(); fillLabel(); busy=false;
});
let lidIsOpen = false;
document.getElementById("lidbtn").addEventListener("click", async () => {
  if(busy) return; busy=true; demoView();
  if(!lidIsOpen){
    screen(pocket ? "ok" : "empty");
    const open = tween(900, t => { lid.rx = -1.66*t; });
    if(pocket){
      const turn = tween(1200, t => { wheel.rotation.x = DUMP*t; }, 300);          // hjulet vrider fickan framåt och nedåt
      run(); await Promise.all([open, turn]);
      const n = pocket; pocket = null; unseat(n);
      const k = trayNuts.length; const spot = [ -24 + (k%4)*16, -28 + Math.floor(k/4)%2*14, 13.2 + Math.floor(k/8)*12 ];
      trayNuts.push(n);
      const fall = path(n, [n.position.toArray(),[0,33.7,41.2],[0,18.7,28.6],[0,3.7,16.0],[0,-5,13.2],[spot[0]*0.5,-14,13.2],spot], 1500);
      const back = tween(1200, t => { wheel.rotation.x = DUMP*(1-t); }, 800);
      run(); await Promise.all([fall, back]);
      const lp = loadPocket(); run(); await lp;
    } else { run(); await open; }
    fillLabel(); lidIsOpen = true;
  } else {
    const close = tween(900, t => { lid.rx = -1.66*(1-t); }); run(); await close;
    screen("idle"); lidIsOpen = false;
  }
  status(); busy=false;
});
document.getElementById("deny").addEventListener("click", async () => {
  if(busy) return; busy=true; demoView(); screen("no");
  if(lidIsOpen){ const c = tween(700, t => { lid.rx = -1.66*(1-t); }); run(); await c; lidIsOpen=false; }
  const shake = tween(600, t => { lid.px = Math.sin(t*Math.PI*8)*1.2*(1-t); }); run(); await shake; lid.px = 0;
  setTimeout(()=>{ screen("idle"); busy=false; }, 2400);
});
// montering steg för steg
const asmBox = document.getElementById("asmBox"), asmStart = document.getElementById("asmStart");
function asmGo(n){
  asmStep = n; asmBox.hidden = !n; asmStart.hidden = !!n;
  if(!n){ asmAnim = 1; apply(); return; }
  const st = ASM[n-1];
  document.getElementById("asmTitle").textContent = `Steg ${n} av ${ASM.length}: ${st.title}`;
  document.getElementById("asmText").textContent = st.text;
  document.getElementById("asmPrev").disabled = n===1; document.getElementById("asmNext").disabled = n===ASM.length;
  asmAnim = 0; apply(); tween(900, t => { asmAnim = t; apply(); }); run();
}
asmStart.addEventListener("click", () => { if(busy) return; if(view.r>1500) preset("close"); ex.value = 0; roofLift = 0; roofUp = false; roofBtn.lastChild.textContent = "Lyft av taket"; solo = null; markRow(); asmGo(1); });
document.getElementById("asmPrev").addEventListener("click", () => { if(asmStep>1) asmGo(asmStep-1); });
document.getElementById("asmNext").addEventListener("click", () => { if(asmStep<ASM.length) asmGo(asmStep+1); });
document.getElementById("asmEnd").addEventListener("click", () => asmGo(0));
// start med fullt magasin och en nöt i hjulets ficka
SLOTS.forEach((s,i) => { const n = addNut(i); n.position.set(...s); }); sortHopper();
{ const n = hopper.shift(); pocket = n; seat(n); const m = addNut(n.userData.slot); m.position.set(...SLOTS[n.userData.slot]); sortHopper(); }
screen("idle"); status(); fillLabel();

''')
R('const isFull = () => hopper.length === SLOTS.length-1 && !!pocket;','const isFull = () => hopper.length === SLOTS.length && !!pocket;')
R('''    const jobs=[]; const free = freeSlots(); if(pocket) free.shift();           // halsens plats står tom när en nöt redan ligger i fickan? nej: den fylls
''','''    const jobs=[];
''')
R("Version 6 av 3D-modellen","Version 7 av 3D-modellen")
R("Prova demon: fyll på nötter och öppna luckan.","Prova demon: fyll på nötter, öppna luckan, lyft av taket eller följ monteringen steg för steg.")
open(p,'w').write(s); print("steg 1 klart")
`````

**Fil: `model/page8b.py`** – 2026-11-11: ny vy i fliken Utskrift, med data, zip och fillista.

`````python
import re, json, base64, zipfile, io, os, markdown
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
# ---------- Utskrift-fliken: ny vy ----------
i=s.index('// ================= UTSKRIFT: BYGGPLATTOR ================='); j=s.rindex('</script>')
s=s[:i]+r'''// ================= UTSKRIFT: BYGGPLATTOR =================
let plateView = null;
function initPlates(){
  if(plateView){ plateView.resize(); return; }
  const PLATES = JSON.parse(document.getElementById("platedata").textContent);
  const st = document.getElementById("pstage");
  const r2 = new THREE.WebGLRenderer({antialias:true, alpha:true}); r2.setPixelRatio(Math.min(window.devicePixelRatio,2));
  r2.shadowMap.enabled = true; r2.shadowMap.type = THREE.PCFSoftShadowMap; st.prepend(r2.domElement);
  const sc = new THREE.Scene(); const cam2 = new THREE.PerspectiveCamera(30,1,1,6000);
  sc.add(new THREE.HemisphereLight(0xF2F5FF, 0x77736A, 0.62));
  const l1 = new THREE.DirectionalLight(0xFFF3E0, 0.85); l1.position.set(-220,420,300); l1.castShadow = true; l1.shadow.mapSize.set(2048,2048);
  Object.assign(l1.shadow.camera,{left:-230,right:230,top:330,bottom:-230,near:1,far:1500}); sc.add(l1);
  const l2 = new THREE.DirectionalLight(0xDDE6FF, 0.3); l2.position.set(300,200,-300); sc.add(l2);
  const g = new THREE.Group(); g.rotation.x = -Math.PI/2; sc.add(g);
  // byggplattan: ljus yta med rutnät var 16:e mm
  const grid = (()=>{ const c=document.createElement("canvas"); c.width=c.height=1024; const x=c.getContext("2d");
    x.fillStyle="#C9C6BB"; x.fillRect(0,0,1024,1024); x.strokeStyle="rgba(60,55,45,.16)"; x.lineWidth=1;
    for(let i=0;i<=256;i+=16){ const q=i*4; x.beginPath(); x.moveTo(q,0); x.lineTo(q,1024); x.stroke(); x.beginPath(); x.moveTo(0,q); x.lineTo(1024,q); x.stroke(); }
    x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018); return new THREE.CanvasTexture(c); })();
  const edge = new THREE.MeshStandardMaterial({color:"#8F8C82"});
  const bed = new THREE.Mesh(new THREE.BoxGeometry(256,256,3), [edge,edge,edge,edge,new THREE.MeshStandardMaterial({map:grid, roughness:.9}),edge]);
  bed.position.set(0,0,-1.5); bed.receiveShadow = true; g.add(bed);
  const holder = new THREE.Group(); holder.position.set(-128,-128,0); g.add(holder);
  const T = new THREE.Vector3(0,30,0); const v = {th:-0.5, ph:0.85, r:640};
  const labels = document.createElement("div"); labels.style.cssText = "position:absolute;inset:0;overflow:hidden;pointer-events:none"; st.appendChild(labels);
  let current = null, picked = null;
  function place(){ cam2.position.set(T.x+v.r*Math.sin(v.ph)*Math.sin(v.th), T.y+v.r*Math.cos(v.ph), T.z+v.r*Math.sin(v.ph)*Math.cos(v.th)); cam2.lookAt(T); }
  function draw2(){
    place(); r2.render(sc, cam2);
    if(!current) return;
    const w = st.clientWidth, h = st.clientHeight; holder.updateMatrixWorld();
    current.groups.forEach((gr,k) => { const pt = new THREE.Vector3(gr.cx, gr.cy, gr.top+3).applyMatrix4(holder.matrixWorld).project(cam2);
      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });
  }
  function resize2(){ const w=st.clientWidth, h=st.clientHeight; if(!w||!h) return; r2.setSize(w,h,false); cam2.aspect=w/h; cam2.updateProjectionMatrix(); draw2(); }
  // rotera, flytta (högerklick, scrollknapp eller skift) och zooma
  const ptr = new Map(); let pan2=false, pinch=0, mid=null;
  function pan(dx,dy){ const rgt=new THREE.Vector3(), up=new THREE.Vector3(); cam2.updateMatrixWorld(); rgt.setFromMatrixColumn(cam2.matrixWorld,0); up.setFromMatrixColumn(cam2.matrixWorld,1); const k=v.r*0.0011; T.addScaledVector(rgt,-dx*k).addScaledVector(up,dy*k); }
  const cv = r2.domElement;
  cv.addEventListener("contextmenu", e=>e.preventDefault());
  cv.addEventListener("mousedown", e=>{ if(e.button===1) e.preventDefault(); });
  cv.addEventListener("pointerdown", e=>{ cv.setPointerCapture(e.pointerId); ptr.set(e.pointerId,{x:e.clientX,y:e.clientY}); pan2 = e.button===2||e.button===1||e.shiftKey;
    if(ptr.size===2){ const [a,b]=[...ptr.values()]; pinch=Math.hypot(a.x-b.x,a.y-b.y); mid={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; } });
  cv.addEventListener("pointermove", e=>{ if(!ptr.has(e.pointerId)) return; const q=ptr.get(e.pointerId); const dx=e.clientX-q.x, dy=e.clientY-q.y; ptr.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if(ptr.size===1){ if(pan2) pan(dx,dy); else { v.th-=dx*0.008; v.ph=Math.min(Math.PI/2-0.02, Math.max(0.05, v.ph-dy*0.008)); } }
    else if(ptr.size===2){ const [a,b]=[...ptr.values()]; const d=Math.hypot(a.x-b.x,a.y-b.y), m={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; if(pinch) v.r=Math.min(1800,Math.max(80,v.r*pinch/d)); if(mid) pan(m.x-mid.x,m.y-mid.y); pinch=d; mid=m; }
    draw2(); });
  const up2 = e=>{ ptr.delete(e.pointerId); pinch=0; mid=null; }; cv.addEventListener("pointerup",up2); cv.addEventListener("pointercancel",up2);
  cv.addEventListener("wheel", e=>{ e.preventDefault(); v.r=Math.min(1800,Math.max(80,v.r*(1+e.deltaY*0.001))); draw2(); }, {passive:false});
  const Q = 0.005, cache = {};
  function b64(sv,Ty){ const bin=atob(sv); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return new Ty(u.buffer); }
  function meshesOf(i){
    if(cache[i]) return cache[i];
    cache[i] = PLATES[i].items.map(it => {
      const q=b64(it.pos, Uint16Array), pos=new Float32Array(q.length); for(let k=0;k<q.length;k++) pos[k]=q[k]*Q;
      let geo=new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos,3));
      geo.setIndex(new THREE.BufferAttribute(it.i32 ? b64(it.idx,Uint32Array) : b64(it.idx,Uint16Array),1));
      geo=geo.toNonIndexed(); geo.computeVertexNormals();
      const m=new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color:it.color, roughness:.75, transparent:true})); m.castShadow=true; m.receiveShadow=true; m.userData.group=it.group; return m; });
    return cache[i];
  }
  const fmtH = h => h < 0.95 ? `ca ${Math.max(10,Math.round(h*6)*10)} min` : `ca ${String(Math.round(h*2)/2).replace(".",",")} h`;
  const box = document.getElementById("plates"), info = document.getElementById("pinfo");
  let lastPhase = null;
  PLATES.forEach((p,i) => {
    if(p.phase!==lastPhase){ const h=document.createElement("div"); h.className="ph"; h.textContent=p.phase; box.appendChild(h); lastPhase=p.phase; }
    const b=document.createElement("button"); b.type="button"; b.textContent=`Platta ${i+1}${p.material==="TPU"?" · TPU":""}`; b.dataset.i=i; b.setAttribute("aria-pressed","false");
    b.addEventListener("click",()=>show(i)); box.appendChild(b);
  });
  const total = PLATES.reduce((a,p)=>a+p.hours,0);
  function highlight(){ holder.children.forEach(m => { const dim = picked && m.userData.group!==picked; m.material.opacity = dim ? 0.15 : 1; m.material.depthWrite = !dim; m.castShadow = !dim; });
    info.querySelectorAll("li").forEach(li => li.setAttribute("aria-pressed", String(li.dataset.g===picked))); draw2(); }
  function show(i){
    current = PLATES[i]; picked = null;
    holder.clear(); meshesOf(i).forEach(m=>holder.add(m));
    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("");
    box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed", String(+b.dataset.i===i)));
    const rows = current.groups.map(gr => `<li data-g="${gr.g}" tabindex="0" role="button" aria-pressed="false"><span>${gr.colors.map(c=>`<span class="sw" style="background:${c}"></span>`).join("")}</span><span><b>${gr.name}</b>${gr.how}<small>${fmtH(gr.hours)} · ${gr.files.join(", ")}</small></span></li>`).join("");
    info.innerHTML = `<h3>Platta ${i+1} av ${PLATES.length}</h3><p style="margin:0;color:var(--ink-2)">${current.phase} · ${current.material}</p>
      <p class="ptime">${fmtH(current.hours)}<small>uppskattad tid för plattan · alla ${PLATES.length} plattor ca ${Math.round(total)} h</small></p>
      <p style="margin:0 0 .4rem;color:var(--ink-2);font-size:.9rem">Klicka på en del för att lyfta fram den.</p><ul>${rows}</ul>`;
    info.querySelectorAll("li").forEach(li => { const pick = () => { picked = picked===li.dataset.g ? null : li.dataset.g; highlight(); };
      li.addEventListener("click", pick); li.addEventListener("keydown", e => { if(e.key==="Enter"||e.key===" "){ e.preventDefault(); pick(); } }); });
    T.set(0, Math.min(110, current.height*0.42), 10); v.r = Math.max(600, 470 + current.height*2.0); v.th = -0.5; v.ph = current.height > 120 ? 1.05 : 0.85;
    highlight();
  }
  plateView = {resize: resize2};
  new ResizeObserver(resize2).observe(st);
  resize2(); show(0);
}
'''+s[j:]
R("Så här kan delarna ligga på X2D:ns byggplatta, 256 × 256 mm. Plattorna är sorterade i den ordning de bör skrivas ut, och delarna håller sig inom 235,5 mm bredd, som är vad skrivaren når när båda munstyckena används. TPU skrivs ut på egna plattor eftersom det kräver andra inställningar. Bambu Studio kan placera om delarna automatiskt, så se det här som ett förslag.",
  "Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm, och varje del har en etikett. Flera delar skrivs ut upp och ner eller liggande för att slippa stöd, så de ser inte ut som i huset. Det står vid varje del hur den ligger. Plattorna är sorterade i den ordning de bör skrivas ut, och TPU ligger på egna plattor. Bambu Studio kan placera om delarna automatiskt, så se placeringen som ett förslag.")
# ---------- data: plattor, zip, fillista ----------
a=s.index('<script id="platedata" type="application/json">')+len('<script id="platedata" type="application/json">'); b=s.index('</script>',a)
s=s[:a]+open('plates.json').read()+s[b:]
with zipfile.ZipFile('/mnt/user-data/outputs/lennarts-matstation-3d.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir('stl')): z.write('stl/'+f, f)
zb=open('/mnt/user-data/outputs/lennarts-matstation-3d.zip','rb').read()
files=[(x.filename,x.file_size) for x in zipfile.ZipFile(io.BytesIO(zb)).infolist()]
a=s.index('<script id="zipdata" type="application/octet-stream">')+len('<script id="zipdata" type="application/octet-stream">'); b=s.index('</script>',a)
s=s[:a]+base64.b64encode(zb).decode()+s[b:]
s=re.sub(r'const FILES = \[.*?\];', lambda m: 'const FILES = '+json.dumps(files)+';', s, count=1, flags=re.S)
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
print(len(files),"filer,",round(len(s)/1e6,1),"MB")
`````

**Fil: `model/page9.py`** – 2026-11-11: dörrförslagen i förhandsgranskningen (förkastade) och den rödmarkerade remsan på byggplattan.

`````python
import re, json
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)>=1, "MISSING "+a[:90]; s=s.replace(a,b) if cnt==0 else s.replace(a,b,cnt)
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v9.json').read()+s[j:]
a=s.index('<script id="platedata" type="application/json">')+len('<script id="platedata" type="application/json">'); b=s.index('</script>',a)
s=s[:a]+open('plates.json').read()+s[b:]
R('const PIVOT = {doserhjul:[0,57,64.3],','const PIVOT = {v1_dorr:[0,-1.2,1.8], v1_dorr_vit:[0,-1.2,1.8], v2_dorr:[-14.5,-2.4,0], v2_dorr_vit:[-14.5,-2.4,0], v3_dorr:[0,-0.8,35], v3_dorr_vit:[0,-0.8,35], doserhjul:[0,57,64.3],')
R('PARTS.forEach(p => {\n  const tr = document.createElement("tr");','PARTS.forEach(p => {\n  if(p.concept) return;                       // dörrvarianterna är koncept och har inga utskriftsfiler än\n  const tr = document.createElement("tr");')
R('<p>${PARTS.length} delar,','<p>${PARTS.filter(p=>!p.concept).length} delar,')
R('''      <fieldset><legend>Demo</legend>''','''      <fieldset id="entre"><legend>Entré</legend>
        <label class="row"><input type="radio" name="var" value="1" checked> Vindbryggan</label>
        <label class="row"><input type="radio" name="var" value="2"> Stugdörren</label>
        <label class="row"><input type="radio" name="var" value="3"> Svängdörren</label>
        <label class="row"><input type="radio" name="var" value="0"> Skålen med lucka (nuvarande)</label>
        <p class="status" id="vtxt" aria-live="polite"></p>
      </fieldset>
      <fieldset><legend>Demo</legend>''')
R('let roofLift = 0, asmStep = 0, asmAnim = 1;','let roofLift = 0, asmStep = 0, asmAnim = 1, variant = 1;')
R('const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1));','const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1)); PARTS.filter(p=>p.concept).forEach(p => STEP_OF[p.name] = 8);')
R('    let vis = solo ? p.name===solo : state[p.group];','    let vis = solo ? p.name===solo : state[p.group] && (!p.var || p.var.includes(variant));')
R('''const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set rx(v){ lids.forEach(h=>h.rotation.x=v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};''',
'''// entréns fyra varianter: vilka delar som rör sig, kring vilken axel och hur långt
const DOORS = {0:{names:["lucka","lucka_vit"], axis:"x", open:-1.66}, 1:{names:["v1_dorr","v1_dorr_vit"], axis:"x", open:1.6}, 2:{names:["v2_dorr","v2_dorr_vit"], axis:"z", open:-1.4}, 3:{names:["v3_dorr","v3_dorr_vit"], axis:"x", open:-1.15}};
Object.values(DOORS).forEach(d => d.h = meshes.filter(m=>d.names.includes(m.userData.name)).map(m=>m.userData.holder));
const lid = {set t(v){ const d = DOORS[variant]; d.h.forEach(h=>h.rotation[d.axis]=d.open*v); }, set px(v){ DOORS[variant].h.forEach(h=>h.position.x=h.userData.base[0]+v); }};
const ring5 = (cy, z) => k => { const q = [[0,cy],[-13,cy-4],[13,cy-4],[-7,cy+8],[7,cy+8]][k%5]; return [q[0], q[1], z+Math.floor(k/5)*10]; };
const SPOTS = {0: k => [-24+(k%4)*16, -28+Math.floor(k/4)%2*14, 13.2+Math.floor(k/8)*12], 1: ring5(-56, 9.2), 2: ring5(-45, 10.3), 3: ring5(-45, 10.3)};
const EXITS = {0:[[0,-5,13.2]], 1:[[0,-6,12.9],[0,-34,12.5]], 2:[[0,-6,12.6],[0,-26,12.3]], 3:[[0,-6,12.6],[0,-26,12.3]]};
const VTXT = {1:"Dörren fälls ner som en vindbrygga och blir rampen som nöten rullar ut på. Samma servo som i dag, gömt i stolpen.",
  2:"En sidohängd dörr med hjärta slås upp och nöten rullar ut på trappstenen. Servots axel är gångjärnet.",
  3:"Luckan hänger i överkanten och nöten knuffar upp den själv på vägen ut. Inget servo utomhus.",
  0:"Dagens lösning: nöten rullar ner i en skål under en lucka. Det är den här som utskriftsfilerna gäller."};
const LIDTXT = {0:"Öppna / Stäng lucka", 1:"Öppna / Stäng dörren", 2:"Öppna / Stäng dörren", 3:"Släpp ut en nöt"};''')
R('const open = tween(900, t => { lid.rx = -1.66*t; });','const flap = variant===3;\n    const open = flap ? Promise.resolve() : tween(900, t => { lid.t = t; });')
R('const k = trayNuts.length; const spot = [ -24 + (k%4)*16, -28 + Math.floor(k/4)%2*14, 13.2 + Math.floor(k/8)*12 ];','const spot = SPOTS[variant](trayNuts.length);')
R('[0,3.7,16.0],[0,-5,13.2],[spot[0]*0.5,-14,13.2],spot], 1500);','[0,3.7,16.0],...EXITS[variant],spot], 1500);\n      if(flap) tween(1500, t => { lid.t = Math.sin(Math.PI*Math.min(1,Math.max(0,(t-0.45)/0.5))); });   // nöten knuffar upp luckan')
R('fillLabel(); lidIsOpen = true;','fillLabel(); lidIsOpen = !flap; if(flap) setTimeout(()=>screen("idle"), 1600);')
R('const close = tween(900, t => { lid.rx = -1.66*(1-t); }); run(); await close;','const close = tween(900, t => { lid.t = 1-t; }); run(); await close;')
R('if(lidIsOpen){ const c = tween(700, t => { lid.rx = -1.66*(1-t); }); run(); await c; lidIsOpen=false; }','if(lidIsOpen){ const c = tween(700, t => { lid.t = 1-t; }); run(); await c; lidIsOpen=false; }')
R('// montering steg för steg','''// byt entré
function setVariant(v){
  lid.t = 0; lidIsOpen = false; trayNuts.splice(0).forEach(n => nutsGroup.remove(n));
  variant = v; lid.t = 0;
  document.getElementById("lidbtn").lastChild.textContent = LIDTXT[v]; document.getElementById("vtxt").textContent = VTXT[v];
  screen("idle"); status(); apply();
}
document.getElementById("entre").addEventListener("change", e => { if(e.target.name!=="var") return; if(busy){ document.querySelector(`#entre input[value="${variant}"]`).checked = true; return; } setVariant(+e.target.value); });
// montering steg för steg''')
R('screen("idle"); status(); fillLabel();\n','setVariant(1); fillLabel();\n')
# byggplattan: rätt zon för två munstycken och mått
R('''x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018);''','''x.fillStyle="rgba(176,42,34,.20)"; x.fillRect(0,0,82,1024); x.strokeStyle="rgba(176,42,34,.55)"; x.lineWidth=3; x.beginPath(); x.moveTo(82,0); x.lineTo(82,1024); x.stroke();
    x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018);''')
R('''    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("");''','''    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("") + `<span class="plabel dim">256 mm</span><span class="plabel dim">256 mm</span><span class="plabel dim">20,5 mm: bara vänster munstycke</span>`;''')
R('''      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });''','''      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });
    [[128,-9,0],[265,128,0],[10,265,0]].forEach((q,k) => { const pt = new THREE.Vector3(...q).applyMatrix4(holder.matrixWorld).project(cam2);
      const el = labels.children[current.groups.length+k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; });''')
R('.pinfo li{cursor:pointer','.plabel.dim{background:none;border:0;color:var(--ink-2);transform:translate(-50%,-50%)}\n.pinfo li{cursor:pointer')
R("Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm, och varje del har en etikett.","Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm. Den röda remsan till vänster, 20,5 mm, når bara det vänstra munstycket, så delarna ligger utanför den. Varje del har en etikett.")
R("lyft av taket eller följ monteringen steg för steg.","lyft av taket eller följ monteringen steg för steg. Under Entré kan du växla mellan tre förslag på dörr.")
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
print("ok")
`````

**Fil: `model/page10.py`** – 2026-11-12: tar bort dörrförslagen, ny panel, scener och monteringen som spelas upp.

`````python
import re, json
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:90]; s=s.replace(a,b,1)
def region(start,end,new):
    global s
    i=s.index(start); j=s.index(end,i); s=s[:i]+new+s[j:]
# ---- bort med dörrvarianterna ----
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v8.json').read()+s[j:]
R('const PIVOT = {v1_dorr:[0,-1.2,1.8], v1_dorr_vit:[0,-1.2,1.8], v2_dorr:[-14.5,-2.4,0], v2_dorr_vit:[-14.5,-2.4,0], v3_dorr:[0,-0.8,35], v3_dorr_vit:[0,-0.8,35], doserhjul:[0,57,64.3],','const PIVOT = {doserhjul:[0,57,64.3],')
R(' Under Entré kan du växla mellan tre förslag på dörr.','')
# ---- panelen ----
region('    <aside>\n      <fieldset id="entre">','  </div>\n  <h2>Delar att skriva ut</h2>','''    <aside>
      <section class="card">
        <h3>Demo</h3>
        <button class="act big" id="visit" type="button"><span class="ic" style="background:#2B7546">&#9654;</span><span><b>Lennart kommer på besök</b><small>Kameran känner igen honom och en nöt rullar ut</small></span></button>
        <button class="act big" id="mech" type="button"><span class="ic" style="background:#8A5A2E">&#9881;</span><span><b>Se mekanismen inifrån</b><small>Samma besök, men med genomskinligt hus</small></span></button>
        <button class="act big" id="deny" type="button"><span class="ic" style="background:#B02A22">&#10005;</span><span><b>Objuden gäst</b><small>En skata försöker och får ACCESS DENIED</small></span></button>
        <div class="pair">
          <button class="act" id="fill" type="button"><span class="ic" style="background:#8A5A2E">&#8681;</span>Fyll på nötter</button>
          <button class="act" id="roofbtn" type="button"><span class="ic" style="background:#5A5E62">&#8679;</span>Lyft av taket</button>
        </div>
        <p class="status" id="status" aria-live="polite"></p>
      </section>
      <section class="card">
        <h3>Montering</h3>
        <button class="act big" id="asmStart" type="button"><span class="ic" style="background:#3B6A2B">&#9654;</span><span><b>Spela upp monteringen</b><small>Tio steg, från bas till blomlådor</small></span></button>
      </section>
      <section class="card">
        <h3>Visa</h3>
        <fieldset id="groups" class="chips"><legend class="sr">Delgrupper</legend></fieldset>
        <label class="row"><input type="checkbox" id="patio"> Uteplatsen</label>
        <label class="row"><input type="checkbox" id="ghost"> Genomskinliga väggar och tak</label>
        <label class="row"><input type="checkbox" id="xray"> Röntgen: allt genomskinligt</label>
        <label for="explode" style="display:block;margin-top:.5rem">Plocka isär</label>
        <input type="range" id="explode" min="0" max="100" value="0">
      </section>
      <div class="facts" id="facts"></div>
    </aside>
''')
R('''      <span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span>
    </div>
    <aside>''','''      <span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span>
      <div class="cap" id="cap" hidden>
        <div class="capbody"><b id="capT"></b><span id="capX" aria-live="polite"></span></div>
        <div class="capctl" id="capCtl" hidden>
          <button type="button" id="asmPrev" aria-label="Föregående steg">&#9664;</button>
          <button type="button" id="asmPlay" aria-label="Pausa">&#10074;&#10074;</button>
          <button type="button" id="asmNext" aria-label="Nästa steg">&#9654;</button>
          <button type="button" id="asmEnd" class="txt">Stäng</button>
        </div>
        <div class="capbar"><i id="capBar"></i></div>
      </div>
    </div>
    <aside>''')
R('.stage{position:relative;background:var(--stage);border-radius:14px;overflow:hidden;aspect-ratio:4/3;min-height:20rem;touch-action:none}',
  '.stage{position:relative;background:var(--stage);border-radius:18px;overflow:hidden;height:clamp(26rem,82vh,60rem);touch-action:none;border:1px solid var(--line)}\n#pstage{height:clamp(22rem,64vh,46rem)}')
R('.views{position:absolute;left:.7rem;top:.7rem;display:flex;gap:.4rem}','.views{position:absolute;left:.7rem;top:.7rem;right:.7rem;display:flex;gap:.4rem;flex-wrap:wrap}')
R('@media (min-width:60rem){.layout{grid-template-columns:1fr 19rem}}','@media (min-width:60rem){.layout{grid-template-columns:1fr 21rem;align-items:start}}')
R('aside{display:flex;flex-direction:column;gap:1.1rem}','aside{display:flex;flex-direction:column;gap:.9rem}')
R('</style>','''.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:1rem}
.card h3{margin:0 0 .7rem;font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.card button.act{background:var(--paper)}
button.act.big{padding:.7rem .8rem;border-radius:12px;gap:.7rem}
button.act.big .ic{width:2.1rem;height:2.1rem;font-size:.95rem}
button.act.big b{display:block;line-height:1.25}
button.act.big small{display:block;color:var(--ink-2);font-size:.85rem;line-height:1.3}
button.act{transition:transform .12s,border-color .12s}
button.act:not(:disabled):active{transform:scale(.985)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:.45rem}
.pair button.act{margin-bottom:0;font-size:.9rem;padding:.5rem .6rem}
.card .status{margin:.7rem 0 0}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.5rem}
.chips label.row{border:1px solid var(--line);border-radius:999px;padding:.2rem .65rem .2rem .5rem;font-size:.9rem;gap:.4rem;background:var(--paper)}
.chips input{width:.95rem;height:.95rem}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.cap{position:absolute;left:50%;bottom:1rem;transform:translateX(-50%);width:min(34rem,calc(100% - 1.6rem));background:color-mix(in srgb,var(--surface) 94%,transparent);border:1px solid var(--line);border-radius:14px;padding:.75rem 1rem .9rem;box-shadow:0 8px 28px rgba(0,0,0,.16);display:grid;grid-template-columns:1fr auto;gap:.3rem .8rem;align-items:center;overflow:hidden;animation:capin .25s ease-out}
.cap[hidden]{display:none}
@keyframes capin{from{opacity:0;transform:translate(-50%,8px)}to{opacity:1;transform:translate(-50%,0)}}
.capbody b{display:block;font-size:1.05rem;line-height:1.25}
.capbody span{display:block;color:var(--ink-2);font-size:.95rem;line-height:1.35}
.capctl{display:flex;gap:.3rem}
.capctl[hidden]{display:none}
.capctl button{font:inherit;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;min-width:2.2rem;height:2.2rem;cursor:pointer;font-size:.8rem}
.capctl button.txt{padding:0 .8rem;font-size:.9rem}
.capctl button:disabled{opacity:.4;cursor:default}
.capbar{position:absolute;left:0;right:0;bottom:0;height:4px;background:var(--line)}
.capbar i{display:block;height:100%;width:0;background:var(--accent);transition:width .35s}
.stage:has(.cap:not([hidden])) .hint{display:none}
@media (prefers-reduced-motion:reduce){.cap{animation:none}.capbar i{transition:none}}
</style>''')
# ---- apply(): utan varianter, med aktörer ----
i=s.index('let roofLift = 0, asmStep = 0, asmAnim = 1, variant = 1;'); j=s.index('const ASM = [',i)
s=s[:i]+'let roofLift = 0, asmStep = 0, asmAnim = 1, peek = 0;\nconst SOLID_IN_XRAY = new Set(["doserhjul","lucka","lucka_vit"]);\n// monteringen i tio steg, i den ordning delarna sätts ihop\n'+s[j:]
R(' PARTS.filter(p=>p.concept).forEach(p => STEP_OF[p.name] = 8);','')
R('    let vis = solo ? p.name===solo : state[p.group] && (!p.var || p.var.includes(variant));','    let vis = solo ? p.name===solo : state[p.group];')
R('''      else if((ghost.checked || (asmStep>=4 && asmStep<=7)) && (p.group==="Kropp" || p.group==="Tak")) op = p.group==="Tak" ? 0.12 : 0.2;   // under monteringen av insidan syns den genom väggarna''',
  '''      else if(p.group==="Kropp" || p.group==="Tak"){
        const g = (ghost.checked || (asmStep>=4 && asmStep<=7)) ? 1 : peek;          // insidan syns genom väggarna när den monteras eller visas
        op = 1 - g*(p.group==="Tak" ? 0.88 : 0.8);
      }''')
R('''  nutsGroup.visible = inner && (!asmStep || asmStep>=7);''','''  nutsGroup.visible = inner && (!asmStep || asmStep>=7);
  if(pocket) pocket.visible = nutsGroup.visible;                                   // nöten i hjulets ficka följer de andra nötterna
  actors.visible = !solo && ex.value==0 && !asmStep;''')
R('  if(p.concept) return;                       // dörrvarianterna är koncept och har inga utskriftsfiler än\n','')
R('<p>${PARTS.filter(p=>!p.concept).length} delar,','<p>${PARTS.length} delar,')
# ---- demo ----
region('const nutGeo = new THREE.SphereGeometry','new ResizeObserver(resize).observe(stage);', r'''const nutGeo = new THREE.SphereGeometry(8.5, 18, 12); nutGeo.scale(1,1,1.15);
const nutMat = new THREE.MeshStandardMaterial({color:"#8A5A2E", roughness:.7});
const wheel = meshes.find(m=>m.userData.name==="doserhjul").userData.holder;        // vrids kring sin axel
const DUMP = 130*Math.PI/180, AX = [0,57,64.3], PKT = 19.3;                           // tömvinkel, axelns läge, nötens avstånd från axeln i fickan
const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set t(v){ lids.forEach(h=>h.rotation.x=-1.66*v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};
// platser i magasinet: en nöt i halsen över hjulet, resten i tratten och lådan ovanför
const SLOTS = [[0,57,105.5],[-10,56,116],[10,56,116],[0,73,117]];
for(const y of [52,70,88]) for(const x of [-20,0,20]) SLOTS.push([x,y,132]);
for(const z of [150,166]) for(const y of [49,65.5,82,97]) for(const x of [-34,-17,0,17,34]) SLOTS.push([x+(z===166?2:0), y+(z===166?1:0), z]);
const nearAxis = p => Math.hypot(p[0], p[1]-57);
SLOTS.sort((a,b)=> (a[2]-b[2]) || (nearAxis(a)-nearAxis(b)));
const hopper = []; let pocket = null, served = 0, busy = false;
const tweens = [];
function tween(dur, fn, delay=0){ return new Promise(res => tweens.push({t0:performance.now()+delay, dur, fn, res})); }
let raf = 0;
function tick(now){
  for(let i=tweens.length-1;i>=0;i--){ const tw=tweens[i]; const k=(now-tw.t0)/tw.dur; if(k<0) continue; const e=Math.min(1,k); tw.fn(e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2); if(e>=1){ tweens.splice(i,1); tw.res(); } }
  draw(); raf = tweens.length ? requestAnimationFrame(tick) : 0;
}
function run(){ if(!raf) raf = requestAnimationFrame(tick); }
const lerp=(a,b,t)=>a+(b-a)*t;
const wait = ms => { const w = tween(ms, ()=>{}); run(); return w; };
function path(obj, pts, dur, delay=0){
  const seg=[]; let L=0; for(let i=1;i<pts.length;i++){ const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1],pts[i][2]-pts[i-1][2]); seg.push(d); L+=d; }
  return tween(dur, t => { let s=t*L, i=0; while(i<seg.length-1 && s>seg[i]){ s-=seg[i]; i++; } const u=Math.min(1,s/seg[i]); const a=pts[i], b=pts[i+1]; obj.position.set(lerp(a[0],b[0],u),lerp(a[1],b[1],u),lerp(a[2],b[2],u)); obj.rotation.x+=0.15; }, delay);
}
// kameran glider mellan vyer
function flyTo(o, dur=1000){
  const off = patio.checked ? PED_H+FOOT : 0;
  const a = {x:TARGET.x, y:TARGET.y, z:TARGET.z, th:view.th, ph:view.ph, r:view.r, fov:cam.fov};
  let dth = o.th-a.th; dth = Math.atan2(Math.sin(dth), Math.cos(dth));
  const tw = tween(dur, t => { TARGET.set(lerp(a.x,o.T[0],t), lerp(a.y,o.T[1]+off,t), lerp(a.z,o.T[2],t)); view.th = a.th+dth*t; view.ph = lerp(a.ph,o.ph,t); view.r = lerp(a.r,o.r,t); cam.fov = lerp(a.fov,32,t); cam.updateProjectionMatrix(); });
  run(); return tw;
}
const VIEW_VISIT = {T:[0,62,58], th:-0.62, ph:1.2, r:700}, VIEW_MECH = {T:[0,80,-40], th:-1.32, ph:1.38, r:600}, VIEW_HOME = {T:[0,105,-20], th:-0.55, ph:1.15, r:860};
// textremsan i bilden
const capEl = document.getElementById("cap"), capBar = document.getElementById("capBar");
function cap(title, text, progress){ capEl.hidden = false; document.getElementById("capT").textContent = title; document.getElementById("capX").textContent = text; if(progress!==undefined) capBar.style.width = (progress*100)+"%"; }
function capHide(){ capEl.hidden = true; capBar.style.width = "0"; }
const acts = [...document.querySelectorAll("aside button.act")];
function setBusy(b){ busy = b; acts.forEach(x => x.disabled = b); }
function status(){ document.getElementById("status").textContent = `I magasinet: ${hopper.length + (pocket?1:0)} nötter. Lennart har fått ${served}.`; }
function demoReset(){ if(asmStep) asmStop(); if(ex.value!=0) ex.value = 0; solo = null; markRow(); apply(); }
function seat(n){ nutsGroup.remove(n); wheel.add(n); n.position.set(0,0,PKT); }                 // nöten ligger i hjulets ficka
function unseat(n){ const w=new THREE.Vector3(); n.getWorldPosition(w); nutsGroup.worldToLocal(w); wheel.remove(n); nutsGroup.add(n); n.position.copy(w); n.visible = true; }
function loadPocket(){
  if(pocket || !hopper.length) return Promise.resolve();
  const n = hopper.shift(); pocket = n; const from = n.position.toArray();
  return path(n, [from, [0,57,Math.max(from[2],106)], [0,57,AX[2]+PKT]], 450).then(()=>seat(n));
}
const fillBtn = document.getElementById("fill"), roofBtn = document.getElementById("roofbtn");
const isFull = () => hopper.length === SLOTS.length && !!pocket;
function fillLabel(){ fillBtn.lastChild.textContent = isFull() ? "Töm magasinet" : "Fyll på nötter"; }
function freeSlots(){ const used = new Set(hopper.map(n=>n.userData.slot)); return SLOTS.map((s,i)=>i).filter(i=>!used.has(i)); }
function sortHopper(){ hopper.sort((a,b)=> (a.position.z-b.position.z) || (nearAxis(a.position.toArray())-nearAxis(b.position.toArray()))); }
function addNut(i){ const n = new THREE.Mesh(nutGeo, nutMat); n.userData.slot = i; n.rotation.set(Math.random()*3,Math.random()*3,0); nutsGroup.add(n); hopper.push(n); return n; }

// ---- aktörerna: Lennart och skatan ----
const actors = new THREE.Group(); nutsGroup.parent.add(actors);
function blob(r, color, pos, sc=[1,1,1]){ const m = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), new THREE.MeshStandardMaterial({color, roughness:.85})); m.position.set(...pos); m.scale.set(...sc); m.castShadow = true; return m; }
function cone(r, h, color, pos, rot){ const m = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14), new THREE.MeshStandardMaterial({color, roughness:.8})); m.position.set(...pos); m.rotation.set(...rot); m.castShadow = true; return m; }
const FUR = "#B4552B", CREAM = "#F0E2CC", DARK = "#1B1B1D";
const lennart = new THREE.Group(); {
  const g = new THREE.Group(); g.scale.setScalar(2.2); lennart.add(g);
  g.add(blob(14,FUR,[0,0,20],[1,1,1.3]), blob(10,CREAM,[0,7,19],[.9,.8,1.2]), blob(9.5,FUR,[0,7,44]), blob(4.6,CREAM,[0,15,42]), blob(1.4,DARK,[0,19.2,43.2]),
    blob(1.5,DARK,[5,13.4,47]), blob(1.5,DARK,[-5,13.4,47]), cone(2.8,8,FUR,[5,4,55],[Math.PI/2,0,0]), cone(2.8,8,FUR,[-5,4,55],[Math.PI/2,0,0]),
    blob(3.6,FUR,[7,12,27]), blob(3.6,FUR,[-7,12,27]), blob(5,FUR,[8,8,3.2],[1,1.6,.6]), blob(5,FUR,[-8,8,3.2],[1,1.6,.6]),
    blob(9,FUR,[0,-13,16]), blob(9.6,FUR,[0,-20,28]), blob(9.2,FUR,[0,-22,41]), blob(8,FUR,[0,-17,52]), blob(6.5,FUR,[0,-10,58]));
}
const skata = new THREE.Group(); {
  const g = new THREE.Group(); g.scale.setScalar(1.25); skata.add(g);
  g.add(blob(26,DARK,[0,0,46],[.8,1.45,.85]), blob(20,"#F4F4F0",[0,8,40],[.8,1.15,.8]), blob(14,DARK,[0,36,64]), cone(4.5,20,"#2A2A2E",[0,57,63],[0,0,0]),
    blob(1.6,"#EDEDED",[6.5,44,68]), blob(1.6,"#EDEDED",[-6.5,44,68]), blob(7,"#1F2B44",[0,-58,52],[.9,6,.45]), blob(14,"#F4F4F0",[17,2,50],[.3,1.2,.5]), blob(14,"#F4F4F0",[-17,2,50],[.3,1.2,.5]),
    blob(2,"#2A2A2E",[6,6,12],[1,1,6]), blob(2,"#2A2A2E",[-6,6,12],[1,1,6]));
}
lennart.visible = skata.visible = false; actors.add(lennart, skata);
function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); }); }
const SPOT = [0,-24,13.2], MOUTH = [0,33,92];

async function moveRoof(upNow){
  if(roofUp===upNow) return; const a = roofLift, b = upNow ? 1 : 0;
  const tw = tween(900, t => { roofLift = a+(b-a)*t; apply(); }); run(); await tw;
  roofUp = upNow; roofBtn.lastChild.textContent = roofUp ? "Lägg på taket" : "Lyft av taket";
}
let roofUp = false;
function setPeek(v, dur=600){ const a = peek; const tw = tween(dur, t => { peek = lerp(a,v,t); apply(); }); run(); return tw; }

// ---- Lennart kommer på besök ----
async function visit(inside){
  if(busy) return; setBusy(true); demoReset(); await moveRoof(false);
  const back = {T:[TARGET.x, TARGET.y-(patio.checked?PED_H+FOOT:0), TARGET.z], th:view.th, ph:view.ph, r:view.r}, hadX = xray.checked;
  if(inside){ xray.checked = true; apply(); await flyTo(VIEW_MECH); } else await flyTo(VIEW_VISIT);
  lennart.visible = true; lennart.rotation.z = 0; lennart.position.set(0,-235,-90);
  cap("Lennart klättrar upp", "Han tar repstegen upp till framgården.", .1);
  let h = hop(lennart, [0,-150,0], 700, 60); run(); await h; h = hop(lennart, [0,-104,0], 800, 22, 2); run(); await h;
  cap("Kameran tittar", "Den tar tre bilder och AI:n avgör vem som står där.", .3); screen("scan"); await wait(1500);
  if(!pocket){
    screen("empty"); cap("Magasinet är tomt", "Lennart får vänta. Fyll på nötter och prova igen.", 1); await wait(2400);
  } else {
    screen("ok"); cap("ACCESS GRANTED", "Det är Lennart. Luckan öppnas och hjulet vrider fram en nöt.", .5);
    const open = tween(900, t => { lid.t = t; }), turn = tween(1300, t => { wheel.rotation.x = DUMP*t; }, 350);
    run(); await Promise.all([open, turn]);
    cap("En nöt rullar ut", "Fickan släpper nöten i rännan, och den rullar ner i skålen.", .7);
    const n = pocket; pocket = null; unseat(n);
    const fall = path(n, [n.position.toArray(),[0,33.7,41.2],[0,18.7,28.6],[0,3.7,16.0],[0,-5,13.2],SPOT], 1500);
    const ret = tween(1200, t => { wheel.rotation.x = DUMP*(1-t); }, 900);
    run(); await Promise.all([fall, ret]); const lp = loadPocket(); run(); await lp;
    cap("Lennart tar sin nöt", "Sedan stängs luckan långsamt, och bara när kameran inte ser någon rörelse.", .9);
    h = hop(lennart, [0,-92,0], 450, 14); run(); await h;
    const lp0 = lennart.position; const grab = path(n, [SPOT, [0,-40,40], [lp0.x+MOUTH[0], lp0.y+MOUTH[1], MOUTH[2]]], 600); run(); await grab;
    nutsGroup.remove(n); lennart.add(n); n.position.set(...MOUTH); served++; status();
    await wait(500);
    const turnAway = tween(450, t => { lennart.rotation.z = Math.PI*t; }); run(); await turnAway;
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [0,-160,0], 800, 24, 2); run(); await Promise.all([h, close]);
    h = hop(lennart, [0,-240,-100], 600, 50); run(); await h; lennart.remove(n);
  }
  lennart.visible = false; screen("idle"); fillLabel(); status(); capHide();
  if(inside){ xray.checked = hadX; apply(); }
  await flyTo(back, 900); setBusy(false);
}
document.getElementById("visit").addEventListener("click", () => visit(false));
document.getElementById("mech").addEventListener("click", () => visit(true));
// ---- Objuden gäst ----
document.getElementById("deny").addEventListener("click", async () => {
  if(busy) return; setBusy(true); demoReset(); await moveRoof(false);
  const back = {T:[TARGET.x, TARGET.y-(patio.checked?PED_H+FOOT:0), TARGET.z], th:view.th, ph:view.ph, r:view.r};
  await flyTo(VIEW_VISIT);
  skata.visible = true; skata.position.set(260,-300,220); skata.rotation.z = 0.5;
  cap("En skata landar", "Hon har sett var nötterna kommer ut.", .15);
  let h = hop(skata, [34,-112,0], 1100, 30); run(); await h;
  cap("Kameran tittar", "Tre bilder, och AI:n avgör vem som står där.", .4); screen("scan"); await wait(1500);
  screen("no"); cap("ACCESS DENIED", "Inte en ekorre. Luckan förblir stängd och besöket sparas som en incidentrapport.", .7);
  const shake = tween(700, t => { lid.px = Math.sin(t*Math.PI*8)*1.2*(1-t); }); h = hop(skata, [34,-112,0], 900, 12, 3); run(); await Promise.all([shake, h]); lid.px = 0;
  await wait(1500);
  cap("Skatan ger upp", "Nötterna ligger kvar i magasinet.", 1);
  h = hop(skata, [-280,-320,260], 1200, 40); run(); await h;
  skata.visible = false; screen("idle"); capHide(); await flyTo(back, 900); setBusy(false);
});
// ---- taket och påfyllningen ----
roofBtn.addEventListener("click", async () => { if(busy) return; setBusy(true); demoReset(); await moveRoof(!roofUp); setBusy(false); });
fillBtn.addEventListener("click", async () => {
  if(busy) return; setBusy(true); demoReset();
  const wasUp = roofUp, emptying = isFull();
  cap(emptying ? "Magasinet töms" : "Påfyllning", "Taket hålls av magneter. Lyft av det, så ligger magasinet öppet.", .3);
  await moveRoof(true);
  if(emptying){
    const all = hopper.splice(0); if(pocket){ unseat(pocket); all.push(pocket); pocket=null; }
    const jobs = all.map((n,i) => path(n, [n.position.toArray(), [n.position.x, n.position.y, 330]], 600, i*12).then(()=>nutsGroup.remove(n)));
    run(); await Promise.all(jobs);
  } else {
    cap("Påfyllning", "Häll i hasselnötter i skal, 18–22 mm. Magasinet rymmer ungefär 50.", .7);
    const jobs = []; freeSlots().forEach((i,k) => { const s=SLOTS[i]; const n=addNut(i); n.position.set(s[0], s[1], 330); jobs.push(path(n, [[s[0],s[1],330],[s[0],s[1],s[2]]], 650, k*30)); });
    run(); await Promise.all(jobs); sortHopper();
    if(!pocket){ const p = loadPocket(); run(); await p; const i=freeSlots()[0]; if(i!==undefined){ const s=SLOTS[i]; const n=addNut(i); n.position.set(...s); sortHopper(); } }
  }
  if(!wasUp) await moveRoof(false);
  status(); fillLabel(); capHide(); setBusy(false);
});
// ---- monteringen spelas upp av sig själv ----
const asmCtl = document.getElementById("capCtl"), asmPlayBtn = document.getElementById("asmPlay");
let asmPlaying = false, asmTimer = 0;
function asmShow(n){
  clearTimeout(asmTimer); asmStep = n; const st = ASM[n-1];
  cap(`${n}. ${st.title}`, st.text, n/ASM.length);
  document.getElementById("asmPrev").disabled = n===1; document.getElementById("asmNext").disabled = n===ASM.length;
  asmAnim = 0; apply(); tween(900, t => { asmAnim = t; apply(); }); run();
  if(asmPlaying){ if(n<ASM.length) asmTimer = setTimeout(() => asmShow(n+1), 3600); else asmSetPlaying(false); }
}
function asmSetPlaying(b){ asmPlaying = b; asmPlayBtn.innerHTML = b ? "&#10074;&#10074;" : "&#9654;"; asmPlayBtn.setAttribute("aria-label", b ? "Pausa" : "Spela"); if(!b) clearTimeout(asmTimer); }
function asmStop(){ clearTimeout(asmTimer); asmPlaying = false; asmStep = 0; asmAnim = 1; asmCtl.hidden = true; capHide(); acts.forEach(x => x.disabled = false); apply(); }
document.getElementById("asmStart").addEventListener("click", async () => {
  if(busy) return; demoReset(); ex.value = 0; roofLift = 0; roofUp = false; roofBtn.lastChild.textContent = "Lyft av taket";
  acts.forEach(x => x.disabled = true); asmCtl.hidden = false; asmStep = 1; asmAnim = 0; apply();
  await flyTo(VIEW_HOME, 800); asmSetPlaying(true); asmShow(1);
});
document.getElementById("asmPrev").addEventListener("click", () => { if(asmStep>1){ asmSetPlaying(false); asmShow(asmStep-1); } });
document.getElementById("asmNext").addEventListener("click", () => { if(asmStep<ASM.length){ asmSetPlaying(false); asmShow(asmStep+1); } });
asmPlayBtn.addEventListener("click", () => { if(asmPlaying) asmSetPlaying(false); else { asmSetPlaying(true); asmShow(asmStep<ASM.length ? asmStep+1 : 1); } });
document.getElementById("asmEnd").addEventListener("click", asmStop);
// start med fullt magasin och en nöt i hjulets ficka
SLOTS.forEach((s,i) => { const n = addNut(i); n.position.set(...s); }); sortHopper();
{ const n = hopper.shift(); pocket = n; seat(n); const m = addNut(n.userData.slot); m.position.set(...SLOTS[n.userData.slot]); sortHopper(); }
screen("idle"); status(); fillLabel();

''')
R('''  else if(mode==="empty"){''','''  else if(mode==="scan"){ c.fillStyle="#F2C14E"; c.font="bold 30px Courier New, monospace"; c.fillText("VERIFIERAR…",168,124); }
  else if(mode==="empty"){''')
R("Prova demon: fyll på nötter, öppna luckan, lyft av taket eller följ monteringen steg för steg.","Prova demon: låt Lennart komma på besök, titta på mekanismen inifrån eller spela upp monteringen.")
# rester av dörrvarianterna
s=re.sub(r'\n// byt entré\nfunction setVariant.*?\n// montering steg för steg','',s,flags=re.S)
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
for k in ('variant','setVariant','v1_dorr','asmGo','asmBox','lidbtn','lidIsOpen','trayNuts'):
    print(k, s.count(k))
`````

**Fil: `model/page11.py`** – 2026-11-12: Lennart som klisterdekal i en hand.

`````python
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
i=s.index('const lennart = new THREE.Group(); {'); j=s.index('const skata = new THREE.Group(); {')
s=s[:i]+r'''// Lennart spelas av en klisterdekal som en hand håller i och låter hoppa
function stickerArt(){
  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");
  let seed = 7; const rnd = () => (seed = (seed*16807) % 2147483647) / 2147483647;
  const FURC = "#B4572B", DARKC = "#8A3F1E", LIGHT = "#DB8F55", CREAMC = "#F5E8D4";
  const ell = (x,y,rx,ry,rot,fill) => { c.beginPath(); c.ellipse(x,y,rx,ry,rot,0,Math.PI*2); c.fillStyle = fill; c.fill(); };
  const grad = (x,y,r,c0,c1) => { const g = c.createRadialGradient(x-r*.3,y-r*.35,r*.1,x,y,r); g.addColorStop(0,c0); g.addColorStop(1,c1); return g; };
  // svansen: en bred, yvig båge bakom kroppen
  c.lineCap = "round"; c.lineJoin = "round";
  const tail = () => { c.beginPath(); c.moveTo(318,418); c.bezierCurveTo(430,400,470,250,415,150); c.bezierCurveTo(395,112,360,98,335,112); };
  tail(); c.strokeStyle = DARKC; c.lineWidth = 104; c.stroke();
  tail(); c.strokeStyle = FURC; c.lineWidth = 88; c.stroke();
  tail(); c.strokeStyle = LIGHT; c.lineWidth = 34; c.globalAlpha = .55; c.stroke(); c.globalAlpha = 1;
  // kropp, lår, mage
  ell(262,332,90,112,-0.18,grad(262,332,115,LIGHT,FURC));
  ell(296,388,72,64,0,grad(296,388,74,FURC,DARKC));
  ell(214,338,46,84,-0.1,grad(214,338,86,"#FFFAF0",CREAMC));
  // bakre örat, huvud, nos
  c.beginPath(); c.moveTo(232,140); c.lineTo(262,62); c.lineTo(274,150); c.closePath(); c.fillStyle = DARKC; c.fill();
  ell(192,186,64,55,-0.1,grad(192,186,66,LIGHT,FURC));
  ell(142,202,32,25,0.1,grad(142,202,34,"#E9A56A",FURC));
  ell(160,216,30,19,0.15,CREAMC);
  ell(113,197,7,6,0,"#2B1A12");
  // främre örat med tofs
  c.beginPath(); c.moveTo(196,142); c.lineTo(222,58); c.lineTo(246,146); c.closePath(); c.fillStyle = FURC; c.fill();
  c.beginPath(); c.moveTo(208,138); c.lineTo(222,84); c.lineTo(236,140); c.closePath(); c.fillStyle = "#E7B08A"; c.fill();
  // öga
  ell(178,174,13,12,0,CREAMC); ell(178,174,9.5,9.5,0,"#17100C"); ell(174.5,170,3.2,3.2,0,"#FFFFFF");
  // arm, tass, fot
  ell(186,292,17,38,0.55,grad(186,292,38,FURC,DARKC)); ell(163,318,12,10,0,DARKC);
  ell(218,440,52,17,0,grad(218,440,52,FURC,DARKC));
  // päls: korta streck i pälsens riktning, bara ovanpå det som redan är ritat
  c.globalCompositeOperation = "source-atop"; c.lineWidth = 1.6;
  for(let k=0;k<2600;k++){ const x = 100+rnd()*380, y = 60+rnd()*400; const tailSide = x > 330; const ang = tailSide ? -1.2+rnd()*.7 : 1.1+rnd()*.8; const L = 5+rnd()*9;
    c.strokeStyle = rnd()<.5 ? "rgba(255,214,170,.20)" : "rgba(90,36,14,.20)"; c.beginPath(); c.moveTo(x,y); c.lineTo(x+Math.cos(ang)*L, y+Math.sin(ang)*L); c.stroke(); }
  c.globalCompositeOperation = "source-over";
  // morrhår
  c.strokeStyle = "rgba(40,25,15,.7)"; c.lineWidth = 1.3; [[-34,-8],[-38,2],[-32,12]].forEach(d => { c.beginPath(); c.moveTo(126,206); c.lineTo(126+d[0],206+d[1]); c.stroke(); });
  // dekalen: vit stansad kant runt motivet, sedan en svag blank yta
  const b = document.createElement("canvas"); b.width = b.height = S; const d = b.getContext("2d");
  for(let k=0;k<28;k++){ const t = k/28*Math.PI*2; d.drawImage(a, Math.cos(t)*15, Math.sin(t)*15); }
  d.globalCompositeOperation = "source-in"; d.fillStyle = "#FBFBF8"; d.fillRect(0,0,S,S);
  const back = document.createElement("canvas"); back.width = back.height = S; back.getContext("2d").drawImage(b,0,0);    // baksidan: bara vitt papper
  d.globalCompositeOperation = "source-over"; d.drawImage(a,0,0);
  d.globalCompositeOperation = "source-atop"; const gl = d.createLinearGradient(80,40,430,470); gl.addColorStop(0,"rgba(255,255,255,.28)"); gl.addColorStop(.35,"rgba(255,255,255,0)"); gl.addColorStop(.7,"rgba(255,255,255,0)"); gl.addColorStop(1,"rgba(0,0,0,.10)"); d.fillStyle = gl; d.fillRect(0,0,S,S);
  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];
}
function capsule(p0, p1, r, color){            // rundad stav mellan två punkter: fingrar och arm
  const g = new THREE.Group(), a = new THREE.Vector3(...p0), b = new THREE.Vector3(...p1), L = a.distanceTo(b), mat = new THREE.MeshStandardMaterial({color, roughness:.75});
  const cyl = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 18), mat); cyl.position.copy(a).add(b).multiplyScalar(.5); cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), b.clone().sub(a).normalize());
  const s0 = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 12), mat), s1 = s0.clone(); s0.position.copy(a); s1.position.copy(b);
  [cyl,s0,s1].forEach(m => { m.castShadow = true; g.add(m); }); return g;
}
const lennart = new THREE.Group(), sticker = new THREE.Group(); {
  const [front, back] = stickerArt(); front.anisotropy = back.anisotropy = 4;
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1); const pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, metalness:0, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  mf.castShadow = mb.castShadow = true; mf.customDepthMaterial = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:front, alphaTest:.5});
  sticker.add(mf, mb); sticker.rotation.x = Math.PI/2; sticker.position.set(0,0,64); lennart.add(sticker);
  // handen: tumme framför dekalen, pekfinger bakom, armen ut mot betraktaren
  const SKIN = "#E3B595", hand = new THREE.Group();
  hand.add(capsule([66,-17,26],[42,-5,44],8.5,SKIN), capsule([66,13,28],[42,5,46],7.5,SKIN),
    blob(8.5,SKIN,[70,12,18]), blob(8.5,SKIN,[75,9,8]), blob(8,SKIN,[79,5,-1]),
    blob(25,SKIN,[82,-6,14],[1,.62,.82]), capsule([92,-16,12],[148,-98,22],17,SKIN), capsule([140,-86,20],[250,-246,40],21,"#2E4057"));
  lennart.add(hand);
}
function faceCam(obj){ const c = actors.worldToLocal(cam.position.clone()); obj.rotation.z = Math.atan2(c.x-obj.position.x, -(c.y-obj.position.y)); }
'''+s[j:]
R('MOUTH = [0,25.5,71], LEN_X = 36, LTURN = 0.45;     // Lennart sitter snett till höger så att skålen syns','MOUTH = [-36,-4,70], LEN_X = 30;     // nosen på dekalen; Lennart står lite till höger så att skålen syns')
R('lennart.visible = true; lennart.rotation.z = LTURN; lennart.position.set(LEN_X,-235,-90);','lennart.visible = true; sticker.scale.x = 1; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart);')
R('cap("Lennart klättrar upp", "Han tar repstegen upp till framgården.", .1);','cap("Lennart kommer hoppande", "I demon spelas han av en klisterdekal.", .1);')
R('let h = hop(lennart, [LEN_X,-150,0], 700, 60); run(); await h; h = hop(lennart, [LEN_X,-100,0], 800, 22, 2); run(); await h;','let h = hop(lennart, [LEN_X+10,-165,0], 900, 34, 2); run(); await h; h = hop(lennart, [LEN_X,-104,0], 900, 26, 2); run(); await h;')
R('h = hop(lennart, [LEN_X-6,-88,0], 450, 14); run(); await h;','h = hop(lennart, [LEN_X-4,-86,0], 450, 16); run(); await h;')
R('const turnAway = tween(450, t => { lennart.rotation.z = LTURN+(Math.PI-LTURN)*t; }); run(); await turnAway;','const turnAway = tween(500, t => { sticker.scale.x = 1-2*t; n.position.x = MOUTH[0]*(1-2*t); }); run(); await turnAway;      // dekalen vänds och Lennart hoppar hem')
R('h = hop(lennart, [LEN_X-10,-160,0], 800, 24, 2); run(); await Promise.all([h, close]);\n    h = hop(lennart, [0,-240,-100], 600, 50); run(); await h; lennart.remove(n);','h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);\n    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h; lennart.remove(n);')
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
`````

**Fil: `model/page12.py`** – 2026-11-12 eller 13 [osäkert]: realistisk hand, skuggor och huvudet i skålen.

`````python
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
i=s.index('function capsule(p0, p1, r, color){'); j=s.index('function faceCam(obj)')
s=s[:i]+r'''// en hand i naturlig storlek: handflata, fem fingrar med leder och naglar, handled, underarm och ärm
const SKIN = new THREE.MeshStandardMaterial({color:"#D8A584", roughness:.62}), NAIL = new THREE.MeshStandardMaterial({color:"#F1D3C2", roughness:.3}), CLOTH = new THREE.MeshStandardMaterial({color:"#2E4057", roughness:.95});
const V = (x,y,z) => new THREE.Vector3(x,y,z);
function limb(g, a, b, r0, r1, mat=SKIN){            // avsmalnande, rundad del mellan två punkter
  const L = a.distanceTo(b), cyl = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, L, 20), mat);
  cyl.position.copy(a).add(b).multiplyScalar(.5); cyl.quaternion.setFromUnitVectors(V(0,1,0), b.clone().sub(a).normalize());
  const s0 = new THREE.Mesh(new THREE.SphereGeometry(r0, 20, 14), mat), s1 = new THREE.Mesh(new THREE.SphereGeometry(r1, 20, 14), mat); s0.position.copy(a); s1.position.copy(b);
  [cyl,s0,s1].forEach(m => { m.castShadow = m.receiveShadow = true; g.add(m); });
}
function lump(g, c, r, sc, mat=SKIN){ const m = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), mat); m.position.copy(c); m.scale.set(...sc); m.castShadow = m.receiveShadow = true; g.add(m); return m; }
function nail(g, a, b, r, away){                     // nagel på yttersta leden, på fingrets ovansida
  const d = b.clone().sub(a).normalize(), n = away.clone().sub(d.clone().multiplyScalar(away.dot(d))).normalize();
  const m = lump(g, a.clone().lerp(b,.72).add(n.clone().multiplyScalar(r*.62)), r*.86, [1,1,1], NAIL);
  m.quaternion.setFromUnitVectors(V(0,0,1), n); m.scale.set(.82,1.05,.34); const q = new THREE.Quaternion().setFromUnitVectors(V(0,1,0), d.clone().applyQuaternion(m.quaternion.clone().invert()).setZ(0).normalize()); m.quaternion.multiply(q);
}
function buildHand(){
  // handens egna axlar: y mot fingrarna, x mot tummen, z ut från handflatan
  const g = new THREE.Group();
  lump(g, V(0,50,0), 1, [41,50,14]); lump(g, V(-8,18,3), 1, [33,22,15]); lump(g, V(27,34,9), 1, [19,31,15]); lump(g, V(-30,44,5), 1, [13,34,13]);
  const curl = (base, lens, radii, flex, splay) => { let pt = base.clone(), ang = 0; const pts = [pt.clone()];
    lens.forEach((L,k) => { ang += flex[k]*Math.PI/180; pt = pt.clone().add(V(splay, Math.cos(ang), Math.sin(ang)).normalize().multiplyScalar(L)); pts.push(pt.clone()); });
    lump(g, base, radii[0]+1.2, [1,1,1]);
    for(let k=0;k<3;k++) limb(g, pts[k], pts[k+1], radii[k], radii[k+1]);
    const dz = pts[3].clone().sub(pts[2]).normalize(); nail(g, pts[2], pts[3], radii[3], V(0, dz.z, -dz.y)); };
  curl(V(9,98,-2),  [46,30,23], [10,9,8,7],     [80,85,60], 0);          // långfinger, ringfinger och lillfinger är krökta in mot handflatan
  curl(V(-10,95,-2),[42,28,22], [9.5,8.6,7.6,6.8],[85,85,60], -.05);
  curl(V(-27,87,-1),[33,20,19], [8.4,7.4,6.6,6], [88,85,60], -.1);
  // pekfinger och tumme möts i ett nyp
  const K = V(27,97,-2), J1 = V(26,117,32), J2 = V(24,113,58), I = V(22,98,72);
  lump(g, K, 11, [1,1,1]); limb(g, K, J1, 10, 9); limb(g, J1, J2, 9, 8); limb(g, J2, I, 8, 7); nail(g, J2, I, 7, V(0,1,.6));
  const B = V(31,20,10), T1 = V(52,47,34), T2 = V(46,74,55), T = V(37,89,65);
  limb(g, B, T1, 14, 11.5); limb(g, T1, T2, 11.5, 10); limb(g, T2, T, 10, 8.6); nail(g, T2, T, 8.6, V(1,-.4,-.2));
  // handled, underarm och uppkavlad ärm
  const arm = new THREE.Group(); arm.scale.set(1,1,.8); g.add(arm);
  limb(arm, V(0,8,0), V(0,-60,0), 27, 25); limb(arm, V(0,-60,0), V(0,-170,-6), 25, 36);
  limb(arm, V(0,-150,-6), V(0,-420,-22), 41, 46, CLOTH); const cuff = new THREE.Mesh(new THREE.TorusGeometry(42, 7, 12, 28), CLOTH); cuff.rotation.x = Math.PI/2; cuff.position.set(0,-150,-6); cuff.castShadow = true; arm.add(cuff);
  // vrid handen så att tummen hamnar framför dekalen, pekfingret bakom och armen kommer in från betraktarens högra sida
  const pch = T.clone().sub(I).normalize(), a = V(0,-1,0), q = a.clone().sub(pch.clone().multiplyScalar(a.dot(pch))).normalize(), r = pch.clone().cross(q);
  const P2 = V(0,-1,0), Q2 = V(.95,0,.31).normalize(), R2 = P2.clone().cross(Q2);
  const M = new THREE.Matrix4().makeBasis(P2,Q2,R2).multiply(new THREE.Matrix4().makeBasis(pch,q,r).transpose());
  g.quaternion.setFromRotationMatrix(M);
  const mid = T.clone().add(I).multiplyScalar(.5).applyMatrix4(M);
  g.position.set(40-mid.x, -mid.y, 34-mid.z);                                  // nypet hamnar på svansens nederkant
  return g;
}
const lennart = new THREE.Group(), pose = new THREE.Group(), inner = new THREE.Group(), sticker = new THREE.Group(); {
  const [front, back] = stickerArt(); front.anisotropy = back.anisotropy = 4;
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1); const pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  const depth = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:back, alphaTest:.5, side:THREE.DoubleSide});   // skuggan följer dekalens kontur
  mf.castShadow = true; mf.customDepthMaterial = depth; mf.receiveShadow = true;
  sticker.add(mf, mb); sticker.rotation.x = Math.PI/2; sticker.position.set(0,0,64);
  pose.position.set(0,0,12); inner.position.set(0,0,-12); inner.add(sticker, buildHand()); pose.add(inner); lennart.add(pose);   // pose vrids kring fötterna när han böjer sig ner
}
// mjuk skugga på marken under Lennart: gör att han ser ut att stå på gräset och lyfta när han hoppar
const shade = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d"); const g = x.createRadialGradient(64,64,4,64,64,62); g.addColorStop(0,"rgba(0,0,0,.55)"); g.addColorStop(1,"rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(0,0,128,128);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(150,150), new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c), transparent:true, depthWrite:false})); m.renderOrder = 2; m.visible = false; return m; })();
actors.add(shade);
function ground(){ const p = lennart.position; shade.visible = lennart.visible && p.z > -5 && p.y > -172 && Math.abs(p.x) < 112;      // bara över framgården
  const k = 1/(1+Math.max(0,p.z)/40); shade.position.set(p.x, p.y, 2.2); shade.rotation.z = lennart.rotation.z; shade.scale.set(.95*k, .34*k, 1); shade.material.opacity = .85*k; }
'''+s[j:]
R('function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); }); }',
  'function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); if(obj===lennart) ground(); }); }')
i=s.index('cap("Lennart tar sin nöt"'); j=s.index('lennart.visible = false; screen("idle")',i)
s=s[:i]+r'''cap("Lennart äter ur skålen", "Handen för fram honom och tippar ner huvudet till nöten.", .85);
    // hur mycket han måste luta för att nosen ska nå nöten, och var fötterna då ska stå
    const LIFT = 8, mx = MOUTH[0], mz = MOUTH[2]-12, yaw = lennart.rotation.z; let al = 0;
    while(al > -1.4 && LIFT+12 - mx*Math.sin(al) + mz*Math.cos(al) > SPOT[2]+12) al -= 0.01;
    const fx = mx*Math.cos(al) + mz*Math.sin(al), fy = MOUTH[1];
    const stand = [SPOT[0] - (fx*Math.cos(yaw) - fy*Math.sin(yaw)), SPOT[1] - (fx*Math.sin(yaw) + fy*Math.cos(yaw)), LIFT];
    h = hop(lennart, stand, 550, 18); run(); await h;
    const bow = tween(650, t => { pose.rotation.y = al*t; }); run(); await bow;
    nutsGroup.remove(n); inner.add(n); n.position.set(MOUTH[0]-3, MOUTH[1]-5, MOUTH[2]-7); served++; status();
    const nibble = tween(900, t => { pose.rotation.y = al + Math.sin(t*Math.PI*6)*0.05; }); run(); await nibble;
    cap("Lennart tar med sig nöten", "Luckan stängs långsamt, och bara när kameran inte ser någon rörelse.", .95);
    const rise = tween(600, t => { pose.rotation.y = al*(1-t); }); run(); await rise;
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);      // han hoppar baklänges hem, utan att vända sig
    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h; inner.remove(n);
  }
  shade.visible = false; pose.rotation.y = 0; '''+s[j:]
R('lennart.visible = true; sticker.scale.x = 1; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart);','lennart.visible = true; pose.rotation.y = 0; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart); ground();')
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
`````

**Fil: `model/page13.py`** – 2026-11-13 [osäkert]: dekalerna som dockor, skatan och nöten utan att den hamnar i munnen.

`````python
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
def region(a,b,new,inclusive_end=False):
    global s
    i=s.index(a); j=s.index(b,i); s=s[:i]+new+(s[j+len(b):] if inclusive_end else s[j:])
# --- dekalerna: gemensam efterbehandling, ekorre och skata ---
R('function stickerArt(){\n  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");',
  'function squirrelArt(){\n  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");')
region('  // dekalen: vit stansad kant runt motivet, sedan en svag blank yta\n','  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];\n}\n', r'''  return stickerFinish(a);
}
function stickerFinish(a){                       // vit stansad kant runt motivet, sedan en svag blank yta; baksidan är bara vitt papper
  const S = a.width, b = document.createElement("canvas"); b.width = b.height = S; const d = b.getContext("2d");
  for(let k=0;k<28;k++){ const t = k/28*Math.PI*2; d.drawImage(a, Math.cos(t)*15, Math.sin(t)*15); }
  d.globalCompositeOperation = "source-in"; d.fillStyle = "#FBFBF8"; d.fillRect(0,0,S,S);
  const back = document.createElement("canvas"); back.width = back.height = S; back.getContext("2d").drawImage(b,0,0);
  d.globalCompositeOperation = "source-over"; d.drawImage(a,0,0);
  d.globalCompositeOperation = "source-atop"; const gl = d.createLinearGradient(80,40,430,470); gl.addColorStop(0,"rgba(255,255,255,.28)"); gl.addColorStop(.35,"rgba(255,255,255,0)"); gl.addColorStop(.7,"rgba(255,255,255,0)"); gl.addColorStop(1,"rgba(0,0,0,.10)"); d.fillStyle = gl; d.fillRect(0,0,S,S);
  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];
}
function magpieArt(){
  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d"); c.translate(0,42);
  let seed = 11; const rnd = () => (seed = (seed*16807) % 2147483647) / 2147483647;
  const BLK = "#17181C", WHT = "#F6F5F0", BLU = "#1F3F6E";
  const ell = (x,y,rx,ry,rot,fill) => { c.beginPath(); c.ellipse(x,y,rx,ry,rot,0,Math.PI*2); c.fillStyle = fill; c.fill(); };
  // den långa stjärten med blågrön glans
  const tg = c.createLinearGradient(300,290,490,380); tg.addColorStop(0,"#16303F"); tg.addColorStop(.5,"#1F5A5E"); tg.addColorStop(1,"#1B2A55");
  c.beginPath(); c.moveTo(300,262); c.lineTo(494,362); c.lineTo(486,384); c.lineTo(292,318); c.closePath(); c.fillStyle = tg; c.fill();
  // ben och fötter
  c.strokeStyle = "#2A2A2E"; c.lineWidth = 7; c.lineCap = "round";
  [[226,330,220,398],[262,332,266,398]].forEach(l => { c.beginPath(); c.moveTo(l[0],l[1]); c.lineTo(l[2],l[3]); c.stroke(); c.beginPath(); c.moveTo(l[2]-20,l[3]+3); c.lineTo(l[2],l[3]); c.lineTo(l[2]+16,l[3]+4); c.stroke(); });
  // kropp, vit buk, vinge, vit skulderfläck
  ell(248,268,98,62,-0.25,BLK);
  ell(232,300,72,40,-0.2,WHT);
  const wg = c.createLinearGradient(240,240,370,310); wg.addColorStop(0,"#1B2C52"); wg.addColorStop(1,BLU); ell(302,272,74,27,0.32,wg);
  ell(268,240,46,16,0.38,WHT);
  // hals, huvud, näbb, öga
  ell(196,236,52,46,-0.3,BLK); ell(160,204,45,43,0,BLK);
  c.beginPath(); c.moveTo(124,190); c.lineTo(66,210); c.lineTo(126,224); c.closePath(); c.fillStyle = "#2B2C31"; c.fill();
  ell(150,194,8,8,0,"#6B6F78"); ell(150,194,6,6,0,"#0B0B0D"); ell(148,192,2,2,0,"#FFFFFF");
  // fjädrar: korta streck ovanpå det som redan är ritat
  c.globalCompositeOperation = "source-atop"; c.lineWidth = 1.5;
  for(let k=0;k<1800;k++){ const x = 80+rnd()*420, y = 150+rnd()*260, L = 6+rnd()*10, ang = 0.35+rnd()*.5;
    c.strokeStyle = rnd()<.5 ? "rgba(120,160,220,.16)" : "rgba(0,0,0,.14)"; c.beginPath(); c.moveTo(x,y); c.lineTo(x+Math.cos(ang)*L, y+Math.sin(ang)*L); c.stroke(); }
  c.globalCompositeOperation = "source-over";
  return stickerFinish(a);
}
''', inclusive_end=True)
# --- hand och docka ---
R('function buildHand(){','function buildHand(grip){')
region('  // vrid handen så att bara tummen hamnar framför dekalen','const lennart = new THREE.Group(), pose = new THREE.Group()', r'''  // vrid handen så att bara tummen hamnar framför dekalen, med handflatan snett upp till höger om nypet
  const pch = T.clone().sub(I).normalize(), mid0 = T.clone().add(I).multiplyScalar(.5), toPalm = V(0,50,5).sub(mid0);
  const q = toPalm.sub(pch.clone().multiplyScalar(toPalm.dot(pch))).normalize(), r = pch.clone().cross(q);
  const P2 = V(0,-1,0), Q2 = V(Math.cos(.5),0,Math.sin(.5)), R2 = P2.clone().cross(Q2);
  const M = new THREE.Matrix4().makeBasis(P2,Q2,R2).multiply(new THREE.Matrix4().makeBasis(pch,q,r).transpose());
  g.quaternion.setFromRotationMatrix(M); g.scale.setScalar(.86); arm.scale.setScalar(.86);
  const mid = mid0.applyMatrix4(M); g.position.set(grip[0]-mid.x*.86, -mid.y*.86, grip[1]-mid.z*.86);
  arm.quaternion.setFromUnitVectors(V(0,-1,0), V(.86,-.44,.24).normalize());         // armen kommer in från betraktarens högra sida, handleden är böjd
  g.userData.arm = arm;
  return g;
}
// en docka: dekal + hand. pose vrids kring fötterna när handen vinklar ner dekalen
function makePuppet(tex, grip){
  const [front, back] = tex; front.anisotropy = back.anisotropy = 4;
  const P = {root:new THREE.Group(), pose:new THREE.Group(), inner:new THREE.Group(), sticker:new THREE.Group()};
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1), pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  const depth = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:back, alphaTest:.5, side:THREE.DoubleSide});   // skuggan följer dekalens kontur
  mf.customDepthMaterial = mb.customDepthMaterial = depth;
  P.sticker.add(mf, mb); P.sticker.rotation.x = Math.PI/2; P.sticker.position.set(0,0,64);
  P.hand = buildHand(grip); P.arm = P.hand.userData.arm;
  P.pose.position.set(0,0,12); P.inner.position.set(0,0,-12); P.inner.add(P.sticker, P.hand); P.pose.add(P.inner); P.root.add(P.pose, P.arm);
  P.root.userData.puppet = P; P.root.visible = false; return P;
}
const LP = makePuppet(squirrelArt(), [46,58]), SP = makePuppet(magpieArt(), [34,52]);
const lennart = LP.root, pose = LP.pose, skata = SP.root;
''')
region('const lennart = new THREE.Group(), pose = new THREE.Group()','// mjuk skugga på marken under Lennart','')
region('function syncArm(){','function faceCam(obj)', r'''function syncArm(P){ P.root.updateMatrixWorld(true); P.arm.position.copy(P.root.worldToLocal(P.hand.getWorldPosition(new THREE.Vector3()))); }   // armen följer handleden när handen vinklas
function ground(P){ syncArm(P); const p = P.root.position; shade.visible = P.root.visible && p.z > -5 && p.y > -172 && Math.abs(p.x) < 112;      // bara över framgården
  const k = 1/(1+Math.max(0,p.z)/40); shade.position.set(p.x, p.y, 2.2); shade.rotation.z = P.root.rotation.z; shade.scale.set(.95*k, .34*k, 1); shade.material.opacity = .5*k; }
// hur mycket dockan måste luta för att nosen eller näbben ska nå en punkt, och var fötterna då ska stå
function bowTo(P, tip, target, lift){
  const mx = tip[0], mz = tip[2]-12, yaw = P.root.rotation.z; let al = 0;
  while(al > -1.4 && lift+12 - mx*Math.sin(al) + mz*Math.cos(al) > target[2]) al -= 0.01;
  const fx = mx*Math.cos(al) + mz*Math.sin(al), fy = tip[1];
  return {al, stand:[target[0] - (fx*Math.cos(yaw) - fy*Math.sin(yaw)), target[1] - (fx*Math.sin(yaw) + fy*Math.cos(yaw)), lift]};
}
function tilt(P, from, to, dur){ const tw = tween(dur, t => { P.pose.rotation.y = lerp(from,to,t); syncArm(P); }); run(); return tw; }
''')
region('const skata = new THREE.Group(); {','lennart.visible = skata.visible = false; actors.add(lennart, skata);','actors.add(lennart, skata);', inclusive_end=True)
R('if(obj===lennart) ground(); }); }','if(obj.userData.puppet) ground(obj.userData.puppet); }); }')
R('MOUTH = [-36,-4,70], LEN_X = 30;','MOUTH = [-36,-4,70], BEAK = [-44,-4,56], LEN_X = 30;')
R('faceCam(lennart); ground();','faceCam(lennart); ground(LP);')
# --- besöket: huvudet i skålen, ingen nöt i munnen ---
region('cap("Lennart äter ur skålen"','lennart.visible = false; screen("idle")', r'''cap("Lennart äter ur skålen", "Handen för fram honom och tippar ner huvudet i skålen.", .85);
    const bw = bowTo(LP, MOUTH, [SPOT[0], SPOT[1], SPOT[2]+10], 8);
    h = hop(lennart, bw.stand, 550, 18); run(); await h;
    await tilt(LP, 0, bw.al, 650);
    const eat = tween(1500, t => { pose.rotation.y = bw.al + Math.sin(t*Math.PI*8)*0.05; syncArm(LP); n.scale.setScalar(Math.max(0.001, 1-t*1.1)); }); run(); await eat;       // nöten äts upp i skålen
    nutsGroup.remove(n); n.scale.setScalar(1); served++; status();
    cap("Lennart är nöjd", "Luckan stängs långsamt, och bara när kameran inte ser någon rörelse.", .95);
    await tilt(LP, bw.al, 0, 600);
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);      // han hoppar baklänges hem, utan att vända sig
    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h;
  }
  shade.visible = false; pose.rotation.y = 0; ''')
# --- skatan ---
region('skata.visible = true; skata.position.set(260,-300,220);','skata.visible = false; screen("idle"); capHide();', r'''skata.visible = true; SP.pose.rotation.y = 0; skata.position.set(60,-300,10); faceCam(skata); ground(SP);
  cap("En skata kommer hoppande", "Även hon spelas av en klisterdekal.", .15);
  let h = hop(skata, [14,-165,0], 900, 34, 2); run(); await h; h = hop(skata, [8,-112,0], 800, 24, 2); run(); await h;
  cap("Kameran tittar", "Tre bilder, och AI:n avgör vem som står där.", .4); screen("scan"); await wait(1500);
  screen("no"); cap("ACCESS DENIED", "Inte en ekorre. Luckan förblir stängd och besöket sparas som en incidentrapport.", .65);
  await wait(900);
  cap("Skatan pickar på luckan", "Hon försöker ändå, men luckan är stängd och nötterna ligger kvar.", .85);
  const pk = bowTo(SP, BEAK, [4,-28,39], 4);
  h = hop(skata, pk.stand, 500, 16); run(); await h;
  for(let k=0;k<3;k++){ await tilt(SP, k ? pk.al*.55 : 0, pk.al, 220); const shake = tween(260, t => { lid.px = Math.sin(t*Math.PI*4)*1.0*(1-t); }); run(); await Promise.all([shake, tilt(SP, pk.al, pk.al*.55, 260)]); lid.px = 0; }
  await tilt(SP, pk.al*.55, 0, 350); await wait(500);
  cap("Skatan ger upp", "Hon hoppar därifrån utan nöt.", 1);
  h = hop(skata, [20,-170,0], 900, 28, 2); run(); await h; h = hop(skata, [80,-320,10], 800, 34, 2); run(); await h;
  shade.visible = false; ''')
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
for k in ('ground()','syncArm()','sticker.','inner.','stickerArt','LTURN'): print(k, s.count(k))
`````

**Fil: `model/shot.py`** – Skärmdumpar av demon under ett besök, för kontroll.

`````python
from playwright.sync_api import sync_playwright
from PIL import Image
import sys, time
btn=sys.argv[1] if len(sys.argv)>1 else "#visit"
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(viewport={"width":1440,"height":950}); pg.on("pageerror", lambda e: print("ERR", e))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort()); pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.abort())
    pg.goto("file:///home/claude/fix/local.html"); pg.wait_for_timeout(4000)
    bb=pg.query_selector("#stage").bounding_box(); clip={"x":bb["x"],"y":bb["y"],"width":bb["width"],"height":bb["height"]}
    pg.click(btn); seen=[]; ims=[]; t0=time.time()
    want=["Kameran tittar","Lennart äter ur skålen","Lennart tar med sig nöten"]
    while time.time()-t0<60 and len(ims)<len(want):
        t=pg.inner_text("#capT")
        if t==want[len(ims)]:
            pg.wait_for_timeout(1500 if len(ims)==1 else 700); pg.screenshot(path=f"s{len(ims)}.png",clip=clip); ims.append(Image.open(f"s{len(ims)}.png"))
        pg.wait_for_timeout(100)
    for _ in range(80):
        if not pg.evaluate("busy"): break
        pg.wait_for_timeout(500)
    print(pg.inner_text("#status"), len(ims))
    b.close()
w,h=ims[0].size; W=Image.new("RGB",(w*len(ims),h))
for i,im in enumerate(ims): W.paste(im,(i*w,0))
W.resize((1560,int(1560*h/(w*len(ims))))).save("stk.png")
`````

**Fil: `model/stage.py`** – Statiska poser och mätning av klippning mellan dekal, skål, lucka och hand, för kontroll.

`````python
from playwright.sync_api import sync_playwright
from PIL import Image
CLIP="""(P=>{ const cv=P.sticker.children[1].material.map.image, d=cv.getContext('2d').getImageData(0,0,512,512).data, mf=P.sticker.children[0]; P.root.updateMatrixWorld(true);
  let tray=0, lid=0, wall=0, n=0; for(let v=0;v<512;v+=6) for(let u=0;u<512;u+=6){ if(d[(v*512+u)*4+3]<128) continue; n++;
    const x=(u/512-.5)*118, y=(.5-v/512)*118; const w=actors.worldToLocal(mf.localToWorld(new THREE.Vector3(x,y,-x*x*0.0016)));
    const inOuter=Math.abs(w.x)<=40&&w.y>=-46&&w.y<=0&&w.z>=0&&w.z<=28, inCav=Math.abs(w.x)<37.2&&w.y>-43.2&&w.y<-2.8&&w.z>3.2;
    if(inOuter&&!inCav) tray++; if(Math.abs(w.x)<=41.5&&w.y>=-15&&w.y<=-3&&w.z>=29&&w.z<=74) lid++; if(w.y>0) wall++; }
  return {n,tray,lid,wall}; })"""
HANDCLIP="""(P=>{ const cv=P.sticker.children[1].material.map.image, d=cv.getContext('2d').getImageData(0,0,512,512).data, mf=P.sticker.children[0]; P.root.updateMatrixWorld(true);
  const inside=(x,y)=>{ const u=Math.round((x/118+.5)*512), v=Math.round((.5-y/118)*512); return u>=0&&u<512&&v>=0&&v<512&&d[(v*512+u)*4+3]>128; };
  const out={}; let idx=0; const A=new THREE.Vector3(), B=new THREE.Vector3(), C=new THREE.Vector3();
  const sd=q=>q.z+q.x*q.x*0.0016;
  [P.hand,P.arm].forEach(grp=>grp.traverse(o=>{ if(!o.isMesh) return; idx++; const g=o.geometry, pos=g.attributes.position, ix=g.index; let n=0;
    const L=k=>mf.worldToLocal(o.localToWorld(new THREE.Vector3().fromBufferAttribute(pos,k)));
    const loc=[]; for(let k=0;k<pos.count;k++) loc.push(L(k));
    for(let t=0;t<ix.count;t+=3){ const tri=[loc[ix.getX(t)],loc[ix.getX(t+1)],loc[ix.getX(t+2)]];
      for(let e=0;e<3;e++){ const a=tri[e], b=tri[(e+1)%3], sa=sd(a), sb=sd(b); if(sa*sb<0){ const f=sa/(sa-sb); if(inside(a.x+(b.x-a.x)*f, a.y+(b.y-a.y)*f)) n++; } } }
    if(n) out[idx+':'+g.type.replace('Geometry','')]=n; }));
  return out; })"""
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(viewport={"width":1440,"height":950}); pg.on("pageerror", lambda e: print("ERR", e))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort()); pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.abort())
    pg.goto("file:///home/claude/fix/local.html"); pg.wait_for_timeout(4000)
    bb=pg.query_selector("#stage").bounding_box(); clip={"x":bb["x"],"y":bb["y"],"width":bb["width"],"height":bb["height"]}
    V1="TARGET.set(0,62,58); Object.assign(view,{th:-0.62,ph:1.2,r:700}); draw();"
    BOW="(()=>{lids.forEach(h=>h.rotation.x=-1.66); LP.pose.rotation.y=0; const bw=bowTo(LP,MOUTH,[SPOT[0]+4,SPOT[1]-4,SPOT[2]+15],10); lennart.position.set(...bw.stand); LP.pose.rotation.y=bw.al; ground(LP); draw(); return bw.al;})()"
    pg.evaluate(V1+"lennart.visible=true; lennart.position.set(30,-104,0); faceCam(lennart); ground(LP); draw()"); print("handen genom ekorren, stående:", pg.evaluate(HANDCLIP+"(LP)")); pg.wait_for_timeout(400); pg.screenshot(path="a0.png",clip=clip)
    pg.evaluate("TARGET.set(40,75,95); Object.assign(view,{th:-0.45,ph:1.2,r:300}); draw(); faceCam(lennart); ground(LP); draw()"); pg.wait_for_timeout(400); pg.screenshot(path="a1.png",clip=clip)
    pg.evaluate("TARGET.set(40,75,95); Object.assign(view,{th:2.4,ph:1.1,r:300}); draw();"); pg.wait_for_timeout(400); pg.screenshot(path="a2.png",clip=clip)
    print("vinkel", pg.evaluate(V1+"faceCam(lennart);"+BOW), "klipp vy 1:", pg.evaluate(CLIP+"(LP)")); print("handen genom ekorren, böjd:", pg.evaluate(HANDCLIP+"(LP)")); pg.wait_for_timeout(400); pg.screenshot(path="a3.png",clip=clip)
    print("klipp vy inifrån:", pg.evaluate("TARGET.set(0,80,-40); Object.assign(view,{th:-1.32,ph:1.38,r:600}); draw(); faceCam(lennart);"+BOW+";"+CLIP+"(LP)")); pg.wait_for_timeout(400); pg.screenshot(path="a4.png",clip=clip)
    pg.evaluate(V1+"lennart.visible=false; lids.forEach(h=>h.rotation.x=0); skata.visible=true; skata.position.set(8,-112,0); faceCam(skata); (()=>{const pk=bowTo(SP,BEAK,[4,-28,39],4); skata.position.set(...pk.stand); SP.pose.rotation.y=pk.al; ground(SP); draw();})()"); print("handen genom skatan:", pg.evaluate(HANDCLIP+"(SP)")); pg.wait_for_timeout(400); pg.screenshot(path="a5.png",clip=clip)
    b.close()
ims=[Image.open(f"a{i}.png") for i in range(6)]
w,h=ims[0].size; W=Image.new("RGB",(w*3,h*2))
for i,im in enumerate(ims): W.paste(im,((i%3)*w,(i//3)*h))
W.resize((1560,int(1560*h*2/(w*3)))).save("stk.png")
`````

### 4.4 Engångsskript från 2026-11-14–15 som ändrade modellen eller filerna

De här kördes direkt i terminalen och sparades inte som filer i chatten. Här återges de ordagrant, i den ordning de kördes, med en kommentarsrad överst som jag har lagt till.

**Fil: `model/oneoff/01_widen_opening.py`**

`````python
# Körd 2026-11-15 i /home/claude/fix: bredda nöthålet från 27 till 31 mm i vägg, stengrund och skålens bakvägg.
from lib import *
parts,P=load('parts_v8.json')
W=15.5
cut_wall=box(-W,W,-0.3,3.5,3.0,32.5)                     # nöthålet i framväggen, nu 31 mm brett, samma överkant som förut
cut_bowl=box(-W,W,-4.5,0.1,3.0,28.5)
put(parts,P,'kropp',M(P,'kropp')-cut_wall)
put(parts,P,'kropp_sockel',M(P,'kropp_sockel')-cut_wall)
for n in ('skal','skal_vit'): put(parts,P,n,M(P,n)-cut_bowl)
json.dump(parts,open('parts_v11base.json','w'))
`````

**Fil: `model/oneoff/01b_make_patch11.sh`**

`````bash
# Körd 2026-11-15 i /home/claude/fix: patch11.py är patch10.py med andra in- och utfiler.
sed -e "s/load('parts_v8.json')/load('parts_v11base.json')/" -e "s/parts_v10.json/parts_v11.json/g" patch10.py > patch11.py && python3 patch11.py
`````

**Fil: `model/oneoff/02_export_bowl.py`**

`````python
# Körd 2026-11-15 i /home/claude/fix: exportera skålen (farstukvisten) igen efter breddningen.
from lib import *
import os
parts,P=load('parts_v11.json')
fmap={}
for p in parts: fmap.setdefault(p.get('file'),[]).append(p['name'])
grp=[f for f in fmap if f and f.startswith('07_')]; print(grp, [fmap[f] for f in grp])
old={f:trimesh.load('stl/'+f) for f in grp}
names=[fmap[f][0] for f in grp]
ms=[T(P,n) for n in names]
allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
A=[[1,0,0,-(lo[0]+hi[0])/2],[0,1,0,-(lo[1]+hi[1])/2],[0,0,1,-lo[2]]]
for n,f in zip(names,grp):
    man=M(P,n).transform(A); out=Manifold()
    for c in man.decompose():
        if c.volume()>1: out=out+c
    me=out.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False)
    print(f, "gamla mått", np.round(old[f].extents,1), "nya", np.round(t.extents,1), "gamla min", np.round(old[f].bounds[0],1), "nya min", np.round(t.bounds[0],1))
    t.export('stl/'+f); print("   tät:", trimesh.load('stl/'+f).is_watertight)
for f in sorted(os.listdir('stl')):
    if f.startswith('05'): print(f, trimesh.load('stl/'+f).is_watertight)
`````

**Fil: `model/oneoff/03_grooves.py`**

`````python
# Körd 2026-11-15 i /home/claude/fix: förläng tre avbrutna plankspår runt kameraringen upp till solskyddet.
from lib import *
parts,P=load('parts_v11.json'); k=M(P,'kropp')
# profilen på ett befintligt spår, för att kopiera den exakt
for y in (0.1,0.4,0.7):
    xs=[x for x in np.arange(11.5,14.5,0.05) if (k^box(x-0.02,x+0.02,y-0.02,y+0.02,144.9,145.1)).volume()<1e-6]
    print("y=%.1f spårbredd x %.2f..%.2f"%(y,min(xs),max(xs)))
cuts=[(-15,163.0,180.0),(13,152.0,180.0),(-1,152.0,156.0)]
add=Manifold()
for x,z0,z1 in cuts: add=add+box(x-0.5,x+0.5,-0.5,0.8,z0,z1)
before=k.volume(); k2=k-add
print("borttaget material: %.1f mm3"%(before-k2.volume()))
others=Manifold()
for p in parts:
    if p['name'] not in ('kropp',): others=others+M(P,p['name'])
print("nya spår krockar med andra delar:", round((add^others).volume(),2))
put(parts,P,'kropp',k2); json.dump(parts,open('parts_v11.json','w'))
def clean(m):
    out=Manifold()
    for c in m.decompose():
        if c.volume()>1: out=out+c
    return out
ms=[T(P,n) for n in ('kropp','kropp_sockel')]
allv=np.vstack([m.vertices for m in ms]); lo,hi=allv.min(0),allv.max(0)
A=[[1,0,0,-(lo[0]+hi[0])/2],[0,1,0,-(lo[1]+hi[1])/2],[0,0,1,-lo[2]]]
for n,f in (('kropp','05_kropp_rod.stl'),('kropp_sockel','05_kropp_sockel_gra.stl')):
    me=clean(M(P,n)).transform(A).to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False); t.export('stl/'+f)
    c=trimesh.load('stl/'+f); print(f, "tät" if c.is_watertight else "EJ TÄT", np.round(c.extents,1))
for x in (-15,-1,13):
    col=''.join('|' if (k2^box(x-0.1,x+0.1,0.05,0.35,z-0.1,z+0.1)).volume()<1e-3 else '.' for z in np.arange(140,215,1.0))
    print("x=%4d"%x, col)
`````

**Fil: `model/oneoff/04_repair_sockel.py`**

`````python
# Körd 2026-11-15 i /home/claude/fix: laga den grå stengrundens STL efter export (gör den tät igen).
import trimesh
m=trimesh.load('stl/05_kropp_sockel_gra.stl', process=True)
m.merge_vertices(digits_vertex=3); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices(); trimesh.repair.fill_holes(m); trimesh.repair.fix_normals(m)
m=trimesh.util.concatenate([c for c in m.split(only_watertight=False) if abs(c.volume)>1]); m.export('stl/05_kropp_sockel_gra.stl')
print("sockel tät:", trimesh.load('stl/05_kropp_sockel_gra.stl').is_watertight, round(m.volume))
`````

**Fil: `model/oneoff/05_kamerafaste_tabs.py`**

`````python
# Körd 2026-11-15 i /home/claude/fix: förläng kamerafästets två klackar ner till byggplattan (de började 0,47 mm upp).
import trimesh, numpy as np
from manifold3d import Manifold, Mesh
m=trimesh.load('stl/15_kamerafaste.stl'); lo,hi=m.bounds; print("bounds", np.round(lo,2), np.round(hi,2))
M_=Manifold(Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32)))
add=Manifold()
for sx in (1,-1):
    tab=M_^Manifold.cube([30,60,60]).translate([17 if sx>0 else -47,-30,lo[2]-1])
    tb=tab.bounding_box(); print("flik", sx, "nederkant z=%.2f"%tb[2], "x %.1f..%.1f y %.1f..%.1f"%(tb[0],tb[3],tb[1],tb[4]))
    sl=tab^Manifold.cube([200,200,0.3]).translate([-100,-100,tb[2]])
    sb=sl.bounding_box()
    add=add+Manifold.cube([sb[3]-sb[0], sb[4]-sb[1], tb[2]-lo[2]+0.3]).translate([sb[0],sb[1],lo[2]])
new=M_+add
me=new.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False)
t.export('stl/15_kamerafaste.stl'); c=trimesh.load('stl/15_kamerafaste.stl'); print("tät:", c.is_watertight, np.round(c.extents,1))
`````

**Fil: `model/oneoff/06_export_glb.py`**

`````python
# Körd 2026-11-14 i /home/claude/fix: hela huset som GLB för Blender (version 7, parts_v8.json).
from lib import *
import json, os, zipfile
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals
parts,P=load('parts_v8.json')
PIVOT={'doserhjul':[0,57,64.3],'lucka':[0,-8,32.2],'lucka_vit':[0,-8,32.2]}
LABEL_SV={}
# Z upp (modellen) -> Y upp (glTF); millimeter -> meter
toY=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],float)
S=np.diag([0.001,0.001,0.001,1.0])
scene=trimesh.Scene(); info=[]
def hexrgb(h): h=h.lstrip('#'); return [int(h[i:i+2],16)/255 for i in (0,2,4)]+[1.0]
for p in parts:
    n=p['name']; m=T(P,n).copy()
    piv=np.array(PIVOT.get(n,[0,0,0]),float)
    m.apply_translation(-piv)                                  # objektets origo i gångjärnet/axeln
    m.apply_transform(S@toY)
    rgb=hexrgb(p.get('color','#9A9A9A'))
    m.visual=TextureVisuals(material=PBRMaterial(name=n, baseColorFactor=rgb, metallicFactor=0.0, roughnessFactor=0.7))
    node_tf=S@toY@trimesh.transformations.translation_matrix(piv)
    node_tf[:3,:3]=np.eye(3)                                   # bara förflyttning i noden
    pw=(toY[:3,:3]@piv)*0.001; node_tf=trimesh.transformations.translation_matrix(pw)
    scene.add_geometry(m, node_name=n, geom_name=n, transform=node_tf)
    info.append(dict(name=n, group=p.get('group'), color=p.get('color'), file=p.get('file'), pivot_mm=PIVOT.get(n)))
scene.export('/mnt/user-data/outputs/lennarts-matstation.glb')
chk=trimesh.load('/mnt/user-data/outputs/lennarts-matstation.glb')
b=chk.bounds; print("delar:",len(chk.geometry),"mått (m):",np.round(b[1]-b[0],3), "storlek:", round(os.path.getsize('/mnt/user-data/outputs/lennarts-matstation.glb')/1e6,1),"MB")
json.dump(info,open('/home/claude/fix/glb_parts.json','w'),ensure_ascii=False,indent=1)
from collections import Counter; print(Counter(p.get('group') for p in parts))
`````

**Fil: `model/oneoff/07_sticker_png.py`**

`````python
# Körd 2026-11-14 i /home/claude/fix: spara dekalerna och skärmens lägen som PNG ur förhandsgranskningen (local.html = sidan med lokal three.js).
from playwright.sync_api import sync_playwright
import base64
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); pg.route("**/fonts.googleapis.com/**", lambda r: r.abort()); pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.abort())
    pg.goto("file:///home/claude/fix/local.html"); pg.wait_for_timeout(3500)
    for fn,name in (("squirrelArt","dekal-lennart.png"),("magpieArt","dekal-skata.png")):
        d=pg.evaluate(f"{fn}()[0].image.toDataURL('image/png')")
        open('/home/claude/fix/'+name,'wb').write(base64.b64decode(d.split(',')[1]))
    for mode,name in (("idle","skarm-vantar.png"),("ok","skarm-access-granted.png"),("no","skarm-access-denied.png"),("scan","skarm-verifierar.png")):
        d=pg.evaluate(f"(()=>{{ screen('{mode}'); const m=screenMesh.material.map; return (m.image||m.source.data).toDataURL('image/png'); }})()")
        open('/home/claude/fix/'+name,'wb').write(base64.b64decode(d.split(',')[1]))
    b.close()
print("ok")
`````

**Fil: `model/oneoff/09_update_page_data.py`**

`````python
# Mönstret som använts flera gånger 2026-11-12–15 för att lägga in aktuell data i förhandsgranskningen
# (delar, plattor, STL-zip och fillista). Körd i /home/claude/fix.
import re, json, base64, zipfile, io, os
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'; s=open(p).read()
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v11.json').read()+s[j:]
a=s.index('<script id="platedata" type="application/json">')+len('<script id="platedata" type="application/json">'); b=s.index('</script>',a)
s=s[:a]+open('plates.json').read()+s[b:]
with zipfile.ZipFile('/mnt/user-data/outputs/lennarts-matstation-3d.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir('stl')): z.write('stl/'+f, f)
zb=open('/mnt/user-data/outputs/lennarts-matstation-3d.zip','rb').read()
files=[(x.filename,x.file_size) for x in zipfile.ZipFile(io.BytesIO(zb)).infolist()]
a=s.index('<script id="zipdata" type="application/octet-stream">')+len('<script id="zipdata" type="application/octet-stream">'); b=s.index('</script>',a)
s=s[:a]+base64.b64encode(zb).decode()+s[b:]
s=re.sub(r'const FILES = \[.*?\];', lambda m: 'const FILES = '+json.dumps(files)+';', s, count=1, flags=re.S)
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
print(len(files),"filer")
`````

**Fil: `trailer/README.md`** – instruktionen i trailerpaketet, skapad 2026-11-14:

`````markdown
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
`````

### 4.5 Webbsidor

Koden är ordagrann, men stora datablock är ersatta med en markering `[... UTELÄMNAD: N tecken ...]`:

- modellens delar som JSON
- plattorna
- STL-filerna som base64
- projektdokumentets ögonblicksbild
- inbäddade bilder

Datablocken återskapas med skriptet i avsnitt 4.6.

**Fil: `web/lennarts-matstation-3d.html` – förhandsgranskningen som den publicerades 2026-11-15**

`````html
<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lennarts matstation – 3D-modell</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&display=swap" rel="stylesheet">
<style>
:root{--paper:#E9EEE4;--surface:#F5F7F1;--ink:#1E2E25;--ink-2:#4F6155;--line:#C7D1C3;--accent:#A23A2C;--focus:#1F5FBF;--stage:#DCE3D7;
  color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#131C17;--surface:#1A251F;--ink:#E3EADF;--ink-2:#A3B3A7;--line:#2C3B32;--accent:#E07A6B;--focus:#8DB8FF;--stage:#1E2A23;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#131C17;--surface:#1A251F;--ink:#E3EADF;--ink-2:#A3B3A7;--line:#2C3B32;--accent:#E07A6B;--focus:#8DB8FF;--stage:#1E2A23;color-scheme:dark}
*,*::before,*::after{box-sizing:inherit}
html{height:100%;scroll-padding-top:env(safe-area-inset-top,0px)}
body{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font-family:"Bricolage Grotesque",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:1rem;line-height:1.5}
.wrap{max-width:76rem;margin:0 auto;padding:clamp(1rem,3vw,2rem)}
h1{font-size:clamp(1.7rem,3.5vw,2.3rem);line-height:1;font-weight:800;letter-spacing:-.02em;margin:0 0 .3rem}
.lead{color:var(--ink-2);max-width:90ch;margin:0 0 .8rem}
.layout{display:grid;gap:1.25rem;grid-template-columns:1fr}
@media (min-width:60rem){.layout{grid-template-columns:1fr 21rem;align-items:start}}
.stage{position:relative;background:var(--stage);border-radius:18px;overflow:hidden;height:clamp(26rem,calc(100vh - 12.5rem),64rem);touch-action:none;border:1px solid var(--line)}
#pstage{height:clamp(22rem,64vh,46rem)}
.stage canvas{display:block;width:100%;height:100%;cursor:grab}
.stage canvas:active{cursor:grabbing}
.hint{position:absolute;left:.8rem;bottom:.6rem;font-size:.85rem;color:var(--ink-2);pointer-events:none}
.views{position:absolute;left:.7rem;top:.7rem;right:.7rem;display:flex;gap:.4rem;flex-wrap:wrap}
.views button{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
.reset{position:absolute;right:.7rem;top:.7rem;font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
aside{display:flex;flex-direction:column;gap:.9rem}
fieldset{border:0;margin:0;padding:0}
legend{font-weight:600;margin-bottom:.4rem}
label.row{display:flex;align-items:center;gap:.6rem;padding:.3rem 0;cursor:pointer}
.sw{width:.9rem;height:.9rem;border-radius:3px;border:1px solid var(--line);flex:none}
input[type=checkbox]{width:1.05rem;height:1.05rem;accent-color:var(--accent)}
input[type=range]{width:100%;accent-color:var(--accent)}
.facts{border-top:1px solid var(--line);padding-top:1rem;color:var(--ink-2);font-size:.95rem}
.facts p{margin:.2rem 0}
button.act{font:inherit;font-size:.95rem;display:flex;align-items:center;gap:.5rem;width:100%;text-align:left;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:10px;padding:.55rem .8rem;cursor:pointer;margin-bottom:.45rem}
button.act:hover{border-color:var(--ink-2)}
button.act:disabled{opacity:.5;cursor:default}
button.act .ic{width:1.6rem;height:1.6rem;border-radius:50%;display:grid;place-items:center;flex:none;font-size:.8rem;color:#fff}
.status{font-size:.9rem;color:var(--ink-2);margin:.2rem 0 0}
h2{font-size:1.35rem;font-weight:800;margin:2rem 0 .6rem}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.95rem;min-width:44rem}
th,td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--ink-2)}
td code{font-size:.88rem}
tr.sel{background:color-mix(in srgb,var(--accent) 10%,transparent)}
tbody tr{cursor:pointer}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px;border-radius:4px}
.tabs{display:flex;gap:.25rem;border-bottom:1px solid var(--line);margin:0 0 1rem;overflow-x:auto}
.tabs button{font:inherit;font-size:1rem;border:0;background:none;color:var(--ink-2);padding:.6rem .9rem;border-bottom:3px solid transparent;cursor:pointer;white-space:nowrap}
.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent);font-weight:600}
[role="tabpanel"][hidden]{display:none}
.doc{max-width:52rem}
.doc h2{margin:2rem 0 .6rem}
.doc h3{font-size:1.1rem;margin:1.4rem 0 .5rem}
.doc table{min-width:40rem}
.doc ul,.doc ol{padding-left:1.3rem}
.doc li{margin:.25rem 0}
.note{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.8rem 1rem;margin:0 0 1.2rem;color:var(--ink-2);max-width:52rem}
.note a,.doc a{color:var(--ink)}
.files-head{display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between;margin:0 0 1rem;max-width:60rem}
button.dl{font:inherit;border:1px solid var(--ink);background:var(--ink);color:var(--paper);border-radius:999px;padding:.55rem 1.1rem;cursor:pointer}
button.dl.small{white-space:nowrap;background:var(--surface);color:var(--ink);border-color:var(--line);padding:.3rem .8rem;font-size:.9rem}
button.dl:disabled{opacity:.5;cursor:default}
#filemsg{color:var(--ink-2);font-size:.95rem;min-height:1.4em;margin:.3rem 0 0}
.plates{display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 1rem}
.plates .ph{width:100%;font-weight:600;font-size:.95rem;margin:.6rem 0 .1rem;color:var(--ink-2)}
.plates .ph:first-child{margin-top:0}
.plates button{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
.plates button[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.plates button.done{text-decoration:line-through;color:var(--ink-2);background:transparent}
.plates button.done[aria-pressed="true"]{background:var(--ink-2);color:var(--paper);border-color:var(--ink-2)}
.pinfo .pdone{display:inline-block;vertical-align:middle;font-size:.75rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:#2B7546;color:#fff;border-radius:999px;padding:.15rem .55rem;margin-left:.4rem}
.pinfo.done li b{text-decoration:line-through;color:var(--ink-2)}
.pinfo .pmark{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.4rem .9rem;cursor:pointer;margin:0 0 .8rem}
.pinfo h3{font-size:1.3rem;font-weight:800;margin:0 0 .2rem}
.pinfo .ptime{font-size:1.8rem;font-weight:800;margin:.4rem 0 .8rem}
.pinfo .ptime small{display:block;font-size:.85rem;font-weight:400;color:var(--ink-2)}
.pinfo ul{list-style:none;padding:0;margin:0;font-size:.92rem}
.pinfo li{display:flex;gap:.5rem;align-items:flex-start;padding:.3rem 0;border-bottom:1px solid var(--line)}
.pinfo li .sw{margin-top:.3rem}
.pinfo code{font-size:.85rem}
.asmt{font-weight:700;margin:.2rem 0 .2rem}
.asmx{margin:0 0 .6rem;color:var(--ink-2);font-size:.95rem}
.asmnav{display:flex;gap:.4rem;flex-wrap:wrap}
.asmnav button{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
.asmnav button:disabled{opacity:.45;cursor:default}
.plabel{position:absolute;transform:translate(-50%,-110%);font-size:.78rem;line-height:1.2;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:.1rem .45rem;pointer-events:none;white-space:nowrap}
.plabel.dim{background:none;border:0;color:var(--ink-2);transform:translate(-50%,-50%)}
.pinfo li{cursor:pointer;border-radius:6px;padding:.4rem .3rem}
.pinfo li[aria-pressed="true"]{background:var(--surface);outline:1px solid var(--line)}
.pinfo li b{display:block}
.pinfo li small{color:var(--ink-2);display:block}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:1rem}
.card h3{margin:0 0 .7rem;font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.card button.act{background:var(--paper)}
button.act.big{padding:.7rem .8rem;border-radius:12px;gap:.7rem}
button.act.big .ic{width:2.1rem;height:2.1rem;font-size:.95rem}
button.act.big b{display:block;line-height:1.25}
button.act.big small{display:block;color:var(--ink-2);font-size:.85rem;line-height:1.3}
button.act{transition:transform .12s,border-color .12s}
button.act:not(:disabled):active{transform:scale(.985)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:.45rem}
.pair button.act{margin-bottom:0;font-size:.9rem;padding:.5rem .6rem}
.card .status{margin:.7rem 0 0}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.5rem}
.chips label.row{border:1px solid var(--line);border-radius:999px;padding:.2rem .65rem .2rem .5rem;font-size:.9rem;gap:.4rem;background:var(--paper)}
.chips input{width:.95rem;height:.95rem}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.cap{position:absolute;left:50%;bottom:1rem;transform:translateX(-50%);width:min(34rem,calc(100% - 1.6rem));background:color-mix(in srgb,var(--surface) 94%,transparent);border:1px solid var(--line);border-radius:14px;padding:.75rem 1rem .9rem;box-shadow:0 8px 28px rgba(0,0,0,.16);display:grid;grid-template-columns:1fr auto;gap:.3rem .8rem;align-items:center;overflow:hidden;animation:capin .25s ease-out}
.cap[hidden]{display:none}
@keyframes capin{from{opacity:0;transform:translate(-50%,8px)}to{opacity:1;transform:translate(-50%,0)}}
.capbody b{display:block;font-size:1.05rem;line-height:1.25}
.capbody span{display:block;color:var(--ink-2);font-size:.95rem;line-height:1.35}
.capctl{display:flex;gap:.3rem}
.capctl[hidden]{display:none}
.capctl button{font:inherit;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;min-width:2.2rem;height:2.2rem;cursor:pointer;font-size:.8rem}
.capctl button.txt{padding:0 .8rem;font-size:.9rem}
.capctl button:disabled{opacity:.4;cursor:default}
.capbar{position:absolute;left:0;right:0;bottom:0;height:4px;background:var(--line)}
.capbar i{display:block;height:100%;width:0;background:var(--accent);transition:width .35s}
.stage:has(.cap:not([hidden])) .hint{display:none}
@media (prefers-reduced-motion:reduce){.cap{animation:none}.capbar i{transition:none}}
</style>
</head>
<body>
<main class="wrap">
  <h1>Lennarts matstation</h1>
  <p class="lead">3D-modellen av huset, version 7. Låt Lennart komma på besök, titta på mekanismen inifrån eller spela upp monteringen.</p>
  <div class="tabs" role="tablist" aria-label="Innehåll">
    <button role="tab" id="t-modell" aria-controls="p-modell" aria-selected="true" data-tab="modell">Förhandsgranskning 3D</button>
    <button role="tab" id="t-dokument" aria-controls="p-dokument" aria-selected="false" data-tab="dokument" tabindex="-1">Projektdokument</button>
    <button role="tab" id="t-filer" aria-controls="p-filer" aria-selected="false" data-tab="filer" tabindex="-1">3D-filer</button>
    <button role="tab" id="t-utskrift" aria-controls="p-utskrift" aria-selected="false" data-tab="utskrift" tabindex="-1">Utskrift</button>
  </div>
  <section role="tabpanel" id="p-modell" aria-labelledby="t-modell">
  <div class="layout">
    <div class="stage" id="stage">
      <div class="views"><button type="button" id="reset">Återställ vy</button><button type="button" data-v="close">Närbild</button><button type="button" data-v="front">Framifrån</button><button type="button" data-v="side">Från sidan</button><button type="button" data-v="inside">Inuti</button></div>
      <span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span>
      <div class="cap" id="cap" hidden>
        <div class="capbody"><b id="capT"></b><span id="capX" aria-live="polite"></span></div>
        <div class="capctl" id="capCtl" hidden>
          <button type="button" id="asmPrev" aria-label="Föregående steg">&#9664;</button>
          <button type="button" id="asmPlay" aria-label="Pausa">&#10074;&#10074;</button>
          <button type="button" id="asmNext" aria-label="Nästa steg">&#9654;</button>
          <button type="button" id="asmEnd" class="txt">Stäng</button>
        </div>
        <div class="capbar"><i id="capBar"></i></div>
      </div>
    </div>
    <aside>
      <section class="card">
        <h3>Demo</h3>
        <button class="act big" id="visit" type="button"><span class="ic" style="background:#2B7546">&#9654;</span><span><b>Lennart kommer på besök</b><small>Kameran känner igen honom och en nöt rullar ut</small></span></button>
        <button class="act big" id="mech" type="button"><span class="ic" style="background:#8A5A2E">&#9881;</span><span><b>Se mekanismen inifrån</b><small>Samma besök, men med genomskinligt hus</small></span></button>
        <button class="act big" id="deny" type="button"><span class="ic" style="background:#B02A22">&#10005;</span><span><b>Objuden gäst</b><small>En skata försöker och får ACCESS DENIED</small></span></button>
        <div class="pair">
          <button class="act" id="fill" type="button"><span class="ic" style="background:#8A5A2E">&#8681;</span>Fyll på nötter</button>
          <button class="act" id="roofbtn" type="button"><span class="ic" style="background:#5A5E62">&#8679;</span>Lyft av taket</button>
        </div>
        <p class="status" id="status" aria-live="polite"></p>
      </section>
      <section class="card">
        <h3>Montering</h3>
        <button class="act big" id="asmStart" type="button"><span class="ic" style="background:#3B6A2B">&#9654;</span><span><b>Spela upp monteringen</b><small>Tio steg, från bas till blomlådor</small></span></button>
      </section>
      <section class="card">
        <h3>Visa</h3>
        <fieldset id="groups" class="chips"><legend class="sr">Delgrupper</legend></fieldset>
        <label class="row"><input type="checkbox" id="patio"> Uteplatsen</label>
        <label class="row"><input type="checkbox" id="ghost"> Genomskinliga väggar och tak</label>
        <label class="row"><input type="checkbox" id="xray"> Röntgen: allt genomskinligt</label>
        <label for="explode" style="display:block;margin-top:.5rem">Plocka isär</label>
        <input type="range" id="explode" min="0" max="100" value="0">
      </section>
      <div class="facts" id="facts"></div>
    </aside>
  </div>
  <h2>Delar att skriva ut</h2>
  <p class="lead" style="margin:0 0 .8rem">Tiderna är uppskattningar för ASA med 0,20 mm lagerhöjd. Bambu Studio ger exakt tid när du laddar filerna, och den kan skilja sig med ungefär 30 procent åt båda hållen.</p>
  <div class="tw"><table><thead><tr><th>Del</th><th>Fil</th><th>Material</th><th>Mått (mm)</th><th>Utskriftstid</th></tr></thead><tbody id="tbl"></tbody></table></div>
  </section>
  <section role="tabpanel" id="p-dokument" aria-labelledby="t-dokument" hidden>
    <p class="note">Ögonblicksbild av projektdokumentet från 11 november 2026. Den levande versionen, där man kan kommentera och redigera, finns i <a href="https://claude.ai/artifact/DsUhQhTLndz1BhiCxTa6bE" target="_blank" rel="noopener">projektdokumentet</a>.</p>
    <div class="doc">[PROJEKTDOKUMENTETS ÖGONBLICKSBILD UTELÄMNAD: 13846 tecken HTML]</div>
  </section>
  <section role="tabpanel" id="p-filer" aria-labelledby="t-filer" hidden>
    <div class="files-head">
      <p style="margin:0;max-width:40rem">Alla utskriftsfiler för matstationen. Filer med samma nummer skrivs ut tillsammans: ladda dem samtidigt i Bambu Studio och svara ja på att de ska bli ett objekt.</p>
      <button class="dl" id="dlall" type="button">Ladda ner alla (zip)</button>
    </div>
    <p id="filemsg" aria-live="polite"></p>
    <div class="tw"><table><thead><tr><th>Fil</th><th>Del</th><th>Material</th><th>Storlek</th><th></th></tr></thead><tbody id="ftbl"></tbody></table></div>
  </section>
  <section role="tabpanel" id="p-utskrift" aria-labelledby="t-utskrift" hidden>
    <p style="margin:0 0 1rem;max-width:60rem">Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm. Den röda remsan till vänster, 20,5 mm, når bara det vänstra munstycket, så delarna ligger utanför den. Varje del har en etikett. Flera delar skrivs ut upp och ner eller liggande för att slippa stöd, så de ser inte ut som i huset. Det står vid varje del hur den ligger. Plattorna är sorterade i den ordning de bör skrivas ut, och TPU ligger på egna plattor. Bambu Studio kan placera om delarna automatiskt, så se placeringen som ett förslag.</p>
    <div class="plates" id="plates" role="group" aria-label="Välj platta"></div>
    <div class="layout">
      <div class="stage" id="pstage"><span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span></div>
      <aside class="pinfo" id="pinfo"></aside>
    </div>
  </section>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script id="platedata" type="application/json">[DATA UTELÄMNAD: 2001190 tecken, se avsnitt 4.6]</script>
<script id="zipdata" type="application/octet-stream">[DATA UTELÄMNAD: 3165488 tecken, se avsnitt 4.6]</script>
<script>
const PARTS = /* DATA UTELÄMNAD: 4442274 tecken delar (JSON), se avsnitt 4.6 */ [];
const TIMES = {"00": 0.59, "01": 5.31, "01b": 3.31, "02": 2.98, "02b": 1.93, "03": 3.28, "03b": 1.85, "04": 0.2, "05": 16.49, "05b": 0.33, "05c": 0.15, "05d": 0.17, "06": 3.43, "06b": 3.43, "06c": 0.73, "06d": 0.08, "06e": 0.11, "07": 2.09, "08": 0.52, "09": 0.15, "09b": 0.01, "10": 2.46, "11": 0.9, "14": 2.53, "15": 0.19, "16": 1.89, "16b": 0.41, "17": 0.02, "18": 0.01, "19": 0.22, "21": 1.03, "21b": 0.14, "22": 0.37, "23": 0.88, "24": 0.84, "25": 0.06};   // uppskattade timmar per utskrift, 0,20 mm lager i ASA
const fmt = h => h < 0.95 ? `ca ${Math.max(10, Math.round(h*6)*10)} min` : `ca ${String(Math.round(h*2)/2).replace(".", ",")} h`;

const LABEL = {doserhus:"Doserhus med ränna",doserhjul:"Doserhjul",kropp_sockel:"Stengrund",ellock:"Lock till elektroniklådan",nockkilar:"Nockkilar",servopackning:"Packning under stolphatten",takpackning:"Takpackning (TPU-lister)",genomforingar:"Kabelgenomföringar (TPU)",monteringsplatta:"Monteringsplatta för elektroniken",blomlador:"Blomlådor",blomlador_vaxter:"Blomlådor, växter",blomlador_blommor_rod:"Blomhuvuden, röda delar",blomlador_blommor_vit:"Blomhuvuden, vita delar",takrannor:"Takrännor",stupror:"Stuprör",stupror_vit:"Stuprör, rörklammer",fonsterrutor:"Fönsterinsatser",solskydd:"Kamerans solskydd",solskydd_vit:"Solskydd, vindskiva",kropp_packning:"Packning under kroppen",tak_v:"Takhalva vänster",tak_v_vit:"Takhalva vänster, vindskivor",tak_h:"Takhalva höger",tak_h_vit:"Takhalva höger, vindskivor",skorsten_krage:"Skorstenskrage",elektroniklada:"Elektroniklåda",elpackning:"Packning till elektroniklådan",skarmram:"Svart skärmram",skarmklamma:"Skärmklämma",avstrykare:"Avstrykare vid inloppet",kropp:"Kropp, röd",kropp_vit:"Kropp, vita detaljer",kropp_rutor:"Kropp, fönsterrutor",tak:"Tak med pannor",tak_vit:"Vindskivor och skorstenskrage",skorsten:"Skorsten",bas:"Bas",bottenplatta:"Bottenplatta",fotter:"Fötter",skal:"Farstukvist (skål), röd",skal_vit:"Farstukvist, kant och servostolpe",lucka:"Lucka (farstutak), grå",lucka_vit:"Lucka, vindskiva",servokapa:"Stolphatt",grasmatta:"Gräsmatta",stenar:"Stenplattor",framgard:"Framgård",framgard_gras:"Framgård, gräsmatta",framgard_stenar:"Framgård, stenplattor",framgard_platta:"Framgård, bottenplatta",doserare_bas:"Doserare, underdel med ränna",doserare_kammare:"Doserare, kammare",doseringsskiva:"Doseringsskiva",doseringslock:"Doseringslock",notmagasin:"Nötmagasin",kamerafaste:"Kamerafäste"};
const GROUPS = ["Tak","Kropp","Skål","Inredning","Bas"];
const EXPLODE = {Tak:[0,0,150],Kropp:[0,0,0],Skål:[0,-70,0],Inredning:[0,0,0],Bas:[0,0,-70]};
const PIVOT = {doserhjul:[0,57,64.3], lucka:[0,-8,32.2], lucka_vit:[0,-8,32.2]};
const stage = document.getElementById("stage");
const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
stage.prepend(renderer.domElement);
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(32,1,1,30000);
// ljus: mjukt himmelsljus, varm sol snett framifrån vänster med skuggor, sval motljus bakifrån
scene.add(new THREE.HemisphereLight(0xEEF3FF, 0x6E6A60, 0.44));
const sun = new THREE.DirectionalLight(0xFFF1DC, 1.08); scene.add(sun); scene.add(sun.target);
sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.6; sun.shadow.radius = 3;
const fill = new THREE.DirectionalLight(0xDDE6FF, 0.28); fill.position.set(900,700,-1100); scene.add(fill);
const bounce = new THREE.DirectionalLight(0xFFE8D0, 0.12); bounce.position.set(200,-400,600); scene.add(bounce);
function aimSun(center, half){                 // solen och skuggkameran följer det som visas
  sun.target.position.copy(center); sun.position.copy(center).add(new THREE.Vector3(-0.55, 1.0, 0.75).multiplyScalar(half*3));
  const c = sun.shadow.camera; c.left = -half; c.right = half; c.top = half; c.bottom = -half; c.near = 1; c.far = half*8; c.updateProjectionMatrix();
}
const root = new THREE.Group(); root.rotation.x = -Math.PI/2; scene.add(root);
const house = new THREE.Group(); root.add(house);
function b64(s, T){ const bin = atob(s); const u = new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return new T(u.buffer); }
const meshes = [];
PARTS.forEach(p => {
  let g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(b64(p.pos, Float32Array),3));
  g.setIndex(new THREE.BufferAttribute(b64(p.idx, Uint32Array),1));
  g = g.toNonIndexed(); g.computeVertexNormals(); g.computeBoundingBox();
  const mat = new THREE.MeshStandardMaterial({color:p.color, roughness:.85, metalness:0, transparent:true, opacity:1});
  const m = new THREE.Mesh(g, mat); m.userData = p;
  const holder = new THREE.Group(); const piv = PIVOT[p.name] || [0,0,0];
  holder.userData.base = piv; holder.position.set(...piv); m.position.set(-piv[0],-piv[1],-piv[2]);
  holder.add(m); house.add(holder); m.userData.holder = holder; meshes.push(m);
  const bb = g.boundingBox; p.size = [bb.max.x-bb.min.x, bb.max.y-bb.min.y, bb.max.z-bb.min.z].map(v=>Math.round(v));
});
// kamera i sfäriska koordinater runt huset
const TARGET = new THREE.Vector3(0,135,-75);
const view = {th:-0.6, ph:1.2, r:900};
const DEF = {...view};
const nutsGroup = new THREE.Group(); house.add(nutsGroup);
function place(){ cam.position.set(TARGET.x+view.r*Math.sin(view.ph)*Math.sin(view.th), TARGET.y+view.r*Math.cos(view.ph), TARGET.z+view.r*Math.sin(view.ph)*Math.cos(view.th)); cam.lookAt(TARGET); }
const ptrs = new Map(); let pinch0 = 0, mid0 = null, panMode = false;
function pan(dx, dy){
  const right = new THREE.Vector3(), upv = new THREE.Vector3();
  cam.updateMatrixWorld(); right.setFromMatrixColumn(cam.matrixWorld,0); upv.setFromMatrixColumn(cam.matrixWorld,1);
  const k = view.r * 0.0011; TARGET.addScaledVector(right, -dx*k).addScaledVector(upv, dy*k);
}
renderer.domElement.addEventListener("contextmenu", e => e.preventDefault());
renderer.domElement.addEventListener("mousedown", e => { if(e.button === 1) e.preventDefault(); });
renderer.domElement.addEventListener("pointerdown", e => {
  renderer.domElement.setPointerCapture(e.pointerId); ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});
  panMode = e.button===2 || e.button===1 || e.shiftKey;
  if(ptrs.size===2){ const [a,b]=[...ptrs.values()]; pinch0=Math.hypot(a.x-b.x,a.y-b.y); mid0={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; }
});
renderer.domElement.addEventListener("pointermove", e => {
  if(!ptrs.has(e.pointerId)) return; const prev = ptrs.get(e.pointerId);
  const dx = e.clientX-prev.x, dy = e.clientY-prev.y;
  ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(ptrs.size===1){
    if(panMode) pan(dx, dy);
    else { view.th -= dx*0.008; view.ph = Math.min(Math.PI-0.15, Math.max(0.15, view.ph-dy*0.008)); }
  } else if(ptrs.size===2){
    const [a,b]=[...ptrs.values()]; const d=Math.hypot(a.x-b.x,a.y-b.y), mid={x:(a.x+b.x)/2,y:(a.y+b.y)/2};
    if(pinch0) view.r=Math.min(9000,Math.max(60,view.r*pinch0/d));
    if(mid0) pan(mid.x-mid0.x, mid.y-mid0.y);
    pinch0=d; mid0=mid;
  }
  draw();
});
const up = e => { ptrs.delete(e.pointerId); pinch0=0; mid0=null; };
renderer.domElement.addEventListener("pointerup", up); renderer.domElement.addEventListener("pointercancel", up);
renderer.domElement.addEventListener("wheel", e => { e.preventDefault(); view.r = Math.min(9000, Math.max(60, view.r*(1+e.deltaY*0.001))); draw(); }, {passive:false});
document.getElementById("reset").addEventListener("click", () => { solo = null; markRow(); preset(patio.checked ? "patio" : "close"); apply(); });

// kontroller
const state = {}; GROUPS.forEach(g => state[g] = true);
const gf = document.getElementById("groups");
GROUPS.forEach(g => {
  const col = PARTS.find(p => p.group===g).color;
  const l = document.createElement("label"); l.className="row";
  l.innerHTML = `<input type="checkbox" checked data-g="${g}"><span class="sw" style="background:${col}"></span>${g}`;
  gf.appendChild(l);
});
gf.addEventListener("change", e => { state[e.target.dataset.g] = e.target.checked; solo = null; markRow(); apply(); });
const ghost = document.getElementById("ghost"), ex = document.getElementById("explode");
ghost.addEventListener("change", apply); ex.addEventListener("input", apply);
let solo = null;
const xray = document.getElementById("xray"); xray.addEventListener("change", apply);
let roofLift = 0, asmStep = 0, asmAnim = 1, peek = 0;
const SOLID_IN_XRAY = new Set(["doserhjul","lucka","lucka_vit"]);
// monteringen i tio steg, i den ordning delarna sätts ihop
const ASM = [
  {title:"Basen", text:"Lägg ballasten i basen och skruva på bottenplattorna. Skruva ihop basen och framgården med tre skruvar och tryck i fötterna.", from:[0,0,-120], parts:["bas","framgard","bottenplatta","framgard_platta","fotter"]},
  {title:"Gräsmattorna", text:"Lägg gräsmattorna och stenplattorna på basen och framgården.", parts:["grasmatta","stenar","framgard_gras","framgard_stenar"]},
  {title:"Kroppen", text:"Tryck fast de vita detaljerna i sina fickor på kroppen medan den står på bänken. Lägg sedan packningen på plats, ställ kroppen på de två styrtapparna och dra sex skruvar inifrån.", parts:["kropp_packning","kropp","kropp_sockel","kropp_vit"]},
  {title:"Insidan av kroppen", text:"Gör klart insidan medan den är tom: fönsterinsatserna, skärmen med ram och klämma, och kameran med sitt fäste.", from:[0,90,60], parts:["fonsterrutor","skarmram","skarmklamma","kamerafaste"]},
  {title:"Elektroniken", text:"Skruva fast elektroniklådan utifrån genom bakväggen. Skjut ner monteringsplattan med all elektronik uppifrån och lägg på locket.", parts:["elpackning","elektroniklada","monteringsplatta","ellock","genomforingar"]},
  {title:"Doseringen", text:"Ställ doserhuset på sina styrtappar och dra två skruvar. Lägg hjulet i sätet och skruva fast servot från höger.", parts:["doserhus","doserhjul"]},
  {title:"Magasinet", text:"Sätt magasinet över hjulet och dra dess två skruvar framtill. Fyll på med nötter.", parts:["notmagasin"]},
  {title:"Farstukvisten", text:"Skruva fast skålen i basen, montera luckan med sitt servo och sätt på stolphatten.", from:[0,-110,30], parts:["skal","skal_vit","lucka","lucka_vit","servopackning","servokapa"]},
  {title:"Taket", text:"Pressa ihop takhalvorna med nockkilarna, tryck fast skorstenen och takrännorna och lägg taket på plats. Magneterna håller det.", parts:["tak_v","tak_v_vit","tak_h","tak_h_vit","nockkilar","skorsten","skorsten_krage","takrannor","takpackning"]},
  {title:"Detaljerna", text:"Tryck fast kamerans solskydd, häng blomlådorna på fönsterkarmarna och snäpp fast stuprören.", from:[0,-60,90], parts:["solskydd","solskydd_vit","blomlador","blomlador_vaxter","blomlador_blommor_rod","blomlador_blommor_vit","stupror","stupror_vit"]}
];
const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1));
function apply(){
  const f = ex.value/100;
  meshes.forEach(m => {
    const p = m.userData, o = EXPLODE[p.group], b = m.userData.holder.userData.base;
    let dx = o[0]*f, dy = o[1]*f, dz = o[2]*f;
    if(p.group==="Tak") dz += roofLift*105;
    let vis = solo ? p.name===solo : state[p.group];
    if(asmStep && !solo){
      const st = STEP_OF[p.name] || 1; vis = st <= asmStep;
      if(st===asmStep){ const k = 1-asmAnim, d = ASM[st-1].from || [0,0,170]; dx += d[0]*k; dy += d[1]*k; dz += d[2]*k; }
    }
    m.userData.holder.position.set(b[0]+dx, b[1]+dy, b[2]+dz);
    m.visible = vis;
    let op = 1;
    if(!solo){
      if(xray.checked && !SOLID_IN_XRAY.has(p.name)) op = p.group==="Inredning" ? 0.34 : 0.11;
      else if(p.group==="Kropp" || p.group==="Tak"){
        const g = (ghost.checked || (asmStep>=4 && asmStep<=7)) ? 1 : peek;          // insidan syns genom väggarna när den monteras eller visas
        op = 1 - g*(p.group==="Tak" ? 0.88 : 0.8);
      }
    }
    m.material.opacity = op; m.material.depthWrite = op===1; m.castShadow = op===1;
  });
  const inner = !solo && ex.value==0 && state.Inredning;
  nutsGroup.visible = inner && (!asmStep || asmStep>=7);
  if(pocket) pocket.visible = nutsGroup.visible;                                   // nöten i hjulets ficka följer de andra nötterna
  actors.visible = !solo && ex.value==0 && !asmStep;
  screenMesh.visible = !solo && state.Kropp && (!asmStep || asmStep>=4);
  camG.visible = inner && (!asmStep || asmStep>=4);
  camGlass.visible = !solo && state.Kropp && ex.value==0 && (!asmStep || asmStep>=4);
  draw();
}
// faktaruta och tabell
document.getElementById("facts").innerHTML = `<p>Total höjd: ca 31 cm inklusive skorsten</p><p>Bas med framgård: 220 × 335 mm</p><p>Magasinet rymmer ca 0,35 liter, ungefär 50 hasselnötter</p><p>Nötter: i skal, 18–22 mm</p><p>${PARTS.length} delar, ${Object.keys(TIMES).length} utskrifter</p><p>Total utskriftstid: ca ${Math.round(Object.values(TIMES).reduce((a,b)=>a+b,0))} timmar</p>`;
const seenJob = new Set();
const tbody = document.getElementById("tbl");
PARTS.forEach(p => {
  const tr = document.createElement("tr"); tr.dataset.n = p.name; tr.tabIndex = 0;
  const job = p.file.split("_")[0]; const first = !seenJob.has(job); seenJob.add(job);
  const tt = first ? fmt(TIMES[job]) + (PARTS.filter(q=>q.file.split("_")[0]===job).length>1 ? " för hela utskriften" : "") : "ingår ovan";
  tr.innerHTML = `<td>${LABEL[p.name]||p.name}</td><td><code>${p.file}</code></td><td>${p.note}</td><td>${p.size.join(" × ")}</td><td>${tt}</td>`;
  const pick = () => { solo = solo===p.name ? null : p.name; markRow(); apply(); stage.scrollIntoView({behavior:"smooth", block:"nearest"}); };
  tr.addEventListener("click", pick); tr.addEventListener("keydown", e => { if(e.key==="Enter"||e.key===" "){ e.preventDefault(); pick(); }});
  tbody.appendChild(tr);
});
function markRow(){ tbody.querySelectorAll("tr").forEach(tr => tr.classList.toggle("sel", tr.dataset.n===solo)); }
function resize(){ const w = stage.clientWidth, h = stage.clientHeight; if(!w || !h) return; renderer.setSize(w,h,false); cam.aspect = w/h; cam.updateProjectionMatrix(); draw(); }
function draw(){ place(); renderer.render(scene, cam); }


// ================= UTEPLATSEN =================
const PED_H = 700, FOOT = 37;                       // pedestalens höjd och husets fötter (mm)
const patioG = new THREE.Group(); root.add(patioG);
function mat(c, o={}){ return new THREE.MeshStandardMaterial(Object.assign({color:c, roughness:.9, metalness:0}, o)); }
function bx(w,d,h,c,x,y,z,parent=patioG){ const m = new THREE.Mesh(new THREE.BoxGeometry(w,d,h), typeof c==="string"?mat(c):c); m.position.set(x,y,z); parent.add(m); return m; }
function tex(draw, w=256, h=256){ const c=document.createElement("canvas"); c.width=w; c.height=h; draw(c.getContext("2d"),w,h); const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; return t; }
// golv, väggar och räcke
const concrete = tex((g,w,h)=>{ g.fillStyle="#C9CCC4"; g.fillRect(0,0,w,h); for(let i=0;i<1400;i++){ g.fillStyle=`rgba(${90+Math.random()*60|0},${95+Math.random()*60|0},${90+Math.random()*50|0},${Math.random()*.12})`; g.fillRect(Math.random()*w,Math.random()*h,2+Math.random()*5,2+Math.random()*5);} });
concrete.repeat.set(6,6);
// golvet: det främre vänstra hörnet är avskuret snett
const fshape = new THREE.Shape([new THREE.Vector2(-1600, 200), new THREE.Vector2(1300, 200), new THREE.Vector2(1300, -2345), new THREE.Vector2(-450, -2345), new THREE.Vector2(-1600, -1250)]);
concrete.repeat.set(1/480, 1/480);
const floorMesh = new THREE.Mesh(new THREE.ExtrudeGeometry(fshape, {depth:20, bevelEnabled:false}), mat("#B9BCB5",{map:concrete}));
floorMesh.position.z = -20; patioG.add(floorMesh);
const wallTex = tex((g,w,h)=>{ g.fillStyle="#9A9D9D"; g.fillRect(0,0,w,h);
  for(let i=0;i<260;i++){ const x=Math.random()*w, y=Math.random()*h, r=20+Math.random()*90, l=Math.random()<.5;
    const gr=g.createRadialGradient(x,y,0,x,y,r); gr.addColorStop(0, l?"rgba(185,188,186,.25)":"rgba(95,98,100,.22)"); gr.addColorStop(1,"rgba(0,0,0,0)"); g.fillStyle=gr; g.fillRect(x-r,y-r,r*2,r*2); }
  for(let i=0;i<5000;i++){ g.fillStyle=`rgba(${Math.random()<.5?40:150},${Math.random()<.5?42:152},${Math.random()<.5?44:150},${Math.random()*.15})`; g.fillRect(Math.random()*w,Math.random()*h,1+Math.random()*2,1+Math.random()*2); } }, 1024, 1024);
bx(2900, 30, 2500, mat("#ffffff",{map:wallTex, roughness:.95}), -150, 191, 1250);           // mörkgrå flammig vägg bakom huset
const green = mat("#2F6F63");
const iron = mat("#2C2C2C",{roughness:.6});
const greenDark = mat("#28635A");
const G0 = -2290, G1 = -1610;                                            // grindöppningen (y)
[[G1, 185]].forEach(([a,b]) => {                           // räcke i två delar
  bx(70, b-a, 950, green, 1265, (a+b)/2, 475); bx(140, b-a, 50, green, 1265, (a+b)/2, 975);
  for(let y=a+60; y<b-30; y+=110) bx(72, 8, 900, greenDark, 1265, y, 470);
});
bx(110, 110, 2500, green, 1265, 130, 1250);                             // stolpe
bx(110, 110, 2500, green, 1265, G0, 1250);                              // stolpe vid grinden
bx(120, 130 - G0 + 110, 120, green, 1265, (130 + G0)/2, 2440);           // ribba överst mellan stolparna
[G0, G1].forEach(y => { bx(100, 100, 1060, green, 1265, y, 530); bx(120, 120, 30, green, 1265, y, 1075); });   // grindstolpar
const gate = new THREE.Group(); gate.position.set(1265, G0 + 50, 0); patioG.add(gate);
const GW = G1 - G0 - 110;                                                // grindens bredd
bx(50, GW, 60, green, 0, GW/2, 920, gate); bx(50, GW, 60, green, 0, GW/2, 110, gate);
bx(50, 60, 870, green, 0, 30, 515, gate); bx(50, 60, 870, green, 0, GW-30, 515, gate);
for(let y=110; y<GW-60; y+=95) bx(34, 60, 750, green, 0, y, 515, gate);
const diag = bx(40, 50, Math.hypot(GW-60, 750), green, 0, GW/2, 515, gate); diag.rotation.x = -Math.atan2(GW-60, 750);
bx(70, 20, 20, iron, -40, GW-80, 600, gate);                             // handtag
gate.rotation.z = 0;
// utsikt: gräsmatta och staket

// pedestal
const pedTex = tex((g,w,h)=>{ for(let i=0;i<10;i++){ g.fillStyle = i%2 ? "#E9E3DC" : "#A9474D"; g.fillRect(i*w/10,0,w/10,h);} });
bx(250, 245, PED_H, mat("#3E4246",{roughness:.8}), 0, 57.5, PED_H/2);
// repstege längs pedestalens framsida
function cyl3(r, a, b, m){ const A=new THREE.Vector3(...a), B=new THREE.Vector3(...b), d=B.clone().sub(A);
  const c=new THREE.Mesh(new THREE.CylinderGeometry(r, r, d.length(), 10), m); c.position.copy(A).add(B).multiplyScalar(.5);
  c.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), d.normalize()); patioG.add(c); return c; }
const ropeTex = tex((g,w,h)=>{ g.fillStyle="#CDB78C"; g.fillRect(0,0,w,h); g.lineWidth=7; for(let i=-h;i<w+h;i+=16){ g.strokeStyle="#A89066"; g.beginPath(); g.moveTo(i,0); g.lineTo(i+h*0.6,h); g.stroke(); g.strokeStyle="#DCC9A2"; g.lineWidth=3; g.beginPath(); g.moveTo(i+6,0); g.lineTo(i+6+h*0.6,h); g.stroke(); g.lineWidth=7; } }, 64, 256);
ropeTex.repeat.set(1,6);
const barkTex = tex((g,w,h)=>{ g.fillStyle="#9A7146"; g.fillRect(0,0,w,h); for(let i=0;i<70;i++){ g.strokeStyle=`rgba(${60+Math.random()*50|0},${40+Math.random()*30|0},${20+Math.random()*20|0},${.25+Math.random()*.35})`; g.lineWidth=1+Math.random()*3; g.beginPath(); const x=Math.random()*w; g.moveTo(x,0); g.bezierCurveTo(x+Math.random()*10-5,h*.3,x+Math.random()*10-5,h*.7,x+Math.random()*8-4,h); g.stroke(); } for(let i=0;i<6;i++){ g.fillStyle="rgba(70,45,22,.55)"; g.beginPath(); g.ellipse(Math.random()*w,Math.random()*h,3+Math.random()*4,6+Math.random()*8,0,0,Math.PI*2); g.fill(); } }, 128, 128);
let seed = 11; const rnd = (a,b) => { seed = (seed*16807) % 2147483647; return a + (b-a)*(seed/2147483647); };
const ropeM = mat("#ffffff",{map:ropeTex}), knotM = mat("#B9A277");
const LT = 736, LB = 8, YT = -174, YB = -210, LX = 36, CX = 10, N = 11;
const onRope = t => [YT + (YB-YT)*t, LT + (LB-LT)*t];
// varje rep får små knickar mellan stegen
const rungs = []; for(let i=1;i<=N;i++){ const t=i/(N+0.6)+rnd(-0.012,0.012); rungs.push({t, tilt:rnd(-9,9), l:rnd(-7,9), r:rnd(-7,9), th:rnd(5.5,8.5), tone:rnd(.82,1.08)}); }
[-1,1].forEach(s => {
  const pts = [[s*LX+CX, -152, 745], [s*LX+CX, YT, LT]];
  rungs.forEach(r => { const [y,z]=onRope(r.t); pts.push([s*LX+CX + rnd(-2.5,2.5), y + rnd(-2,2), z + (s<0 ? r.tilt/2 : -r.tilt/2)]); });
  pts.push([s*LX+CX+rnd(-3,3), YB+rnd(-6,6), LB]);
  for(let i=1;i<pts.length;i++) cyl3(rnd(3.8,4.8), pts[i-1], pts[i], ropeM);
  bx(10, 10, 5, iron, s*LX+CX, -143, 739.5, patioG);
  rungs.forEach((r,i) => { const p=pts[i+2]; const k=new THREE.Mesh(new THREE.SphereGeometry(rnd(6.5,9.5),9,7), knotM); k.scale.set(rnd(.85,1.15),rnd(.8,1.1),rnd(.9,1.3)); k.position.set(p[0], p[1], p[2]+5); patioG.add(k); r[s<0?'pl':'pr']=p; });
});
cyl3(8, [-LX-12+CX, -152, 745], [LX+14+CX, -152, 745], mat("#ffffff",{map:barkTex}));
rungs.forEach(r => { const m = mat(new THREE.Color("#ffffff").multiplyScalar(r.tone), {map:barkTex});
  const a=[r.pl[0]-r.l, r.pl[1], r.pl[2]], b=[r.pr[0]+r.r, r.pr[1], r.pr[2]];
  const c=cyl3(r.th, a, b, m); c.rotation.z += rnd(-0.05,0.05); });
// jutematta
const jute = tex((g,w,h)=>{ g.fillStyle="#9C7748"; g.fillRect(0,0,w,h); for(let r=4;r<w/2;r+=4){ g.strokeStyle= r%8? "#8A6840":"#A98457"; g.lineWidth=2.4; g.beginPath(); g.arc(w/2,h/2,r,0,Math.PI*2); g.stroke(); } }, 512, 512);
const rug = new THREE.Mesh(new THREE.CircleGeometry(560, 64), mat("#ffffff",{map:jute})); rug.position.set(560,-900,2); patioG.add(rug);
// bord (Tärnö-liknande)
const wood = mat("#A8937D");
function table(x,y){ const g=new THREE.Group(); g.position.set(x,y,0); patioG.add(g);
  for(let i=0;i<6;i++) bx(550, 78, 22, wood, 0, -225+i*90, 700, g);
  bx(560, 20, 25, iron, 0, -250, 680, g); bx(560, 20, 25, iron, 0, 250, 680, g);
  [[-1,1],[1,-1]].forEach(([a,b])=>{ [-1,1].forEach(s=>{ const l=bx(16,16,760,iron, s*230, 0, 345, g); l.rotation.x = a*0.38; }); });
  return g; }
function rod(w, p1, p2, m, g, x){                          // stång mellan två punkter i stolens yz-plan
  const dy=p2[0]-p1[0], dz=p2[1]-p1[1], L=Math.hypot(dy,dz);
  const r = bx(w, w, L, m, x, (p1[0]+p2[0])/2, (p1[1]+p2[1])/2, g); r.rotation.x = Math.atan2(-dy, dz); return r; }
function chair(x,y,rot){ const g=new THREE.Group(); g.position.set(x,y,0); g.rotation.z=rot; patioG.add(g);
  const backY = z => 170 + 92*z/890, frontY = z => -262 + 72*z/450;   // benens läge på höjden z
  bx(408,16,22,iron,0,-195,438,g); bx(408,16,22,iron,0,backY(438),438,g);               // sitsram fram och bak
  [-1,1].forEach(s=>{ const X = s*196;
    bx(16, backY(438)+195+8, 22, iron, X, (backY(438)-195)/2, 438, g);                  // sitsram sidor
    rod(16, [170,0], [262,890], iron, g, X);                                            // bakben som blir ryggstöd
    rod(16, [-262,0], [-190,450], iron, g, X);                                          // framben
    rod(12, [frontY(40),40], [backY(400),400], iron, g, X);                             // kryss
    rod(12, [backY(40),40], [frontY(400),400], iron, g, X); });
  for(let i=0;i<5;i++) bx(392, 68, 16, wood, 0, -158+i*79, 457, g);                   // sitsribbor
  [690, 800].forEach(z=>{ const r=bx(408,16,78,wood,0,backY(z),z,g); r.rotation.x = Math.atan2(-92,890); });   // ryggribbor
  return g; }
const stripes = tex((g,w,h)=>{ for(let i=0;i<16;i++){ g.fillStyle = i%2 ? "#E9E3DC" : "#A9474D"; g.fillRect(i*w/16,0,w/16,h);} });
function cushion(g){ const c=new THREE.Mesh(new THREE.BoxGeometry(380,380,40), mat("#ffffff",{map:stripes})); c.position.set(0,-5,485); g.add(c);
  const btn = mat("#B9575C"); for(let i=-1;i<=1;i++) for(let j=-1;j<=1;j++){ const d=new THREE.Mesh(new THREE.SphereGeometry(7,8,6), btn); d.scale.z=.4; d.position.set(i*115,j*115-5,505); g.add(d); } }
table(720,-720);
const ch1 = chair(720, -230, 0); cushion(ch1);
const ch2 = chair(720, -1210, Math.PI); cushion(ch2);
// Lennart på bordet
function squirrel(x,y,z,rot){ const g=new THREE.Group(); g.position.set(x,y,z); g.rotation.z=rot; patioG.add(g);
  const fur=mat("#B4602A"), belly=mat("#EBD6B8"), dark=mat("#2B1A10");
  const body=new THREE.Mesh(new THREE.SphereGeometry(55,20,14), fur); body.scale.set(.85,.8,1.25); body.position.set(0,0,70); g.add(body);
  const bel=new THREE.Mesh(new THREE.SphereGeometry(40,16,12), belly); bel.scale.set(.8,.5,1.1); bel.position.set(0,-30,68); g.add(bel);
  const head=new THREE.Mesh(new THREE.SphereGeometry(34,18,12), fur); head.scale.set(1,1.15,.95); head.position.set(0,-30,152); g.add(head);
  [-1,1].forEach(s=>{ const e=new THREE.Mesh(new THREE.ConeGeometry(9,30,8), fur); e.position.set(s*17,-24,190); e.rotation.x=Math.PI/2; g.add(e);
    const eye=new THREE.Mesh(new THREE.SphereGeometry(5,8,6), dark); eye.position.set(s*15,-58,160); g.add(eye); });
  const nose=new THREE.Mesh(new THREE.SphereGeometry(5,8,6), dark); nose.position.set(0,-70,148); g.add(nose);
  const tail=new THREE.Mesh(new THREE.TorusGeometry(62,26,10,24,Math.PI*1.25), fur); tail.rotation.set(0,Math.PI/2,0); tail.position.set(0,62,118); g.add(tail);
  return g; }
// husets placering och kameravyer
function setHouseZ(){ house.position.z = patio.checked ? PED_H + FOOT : 0;
  if(!window._catcher){ window._catcher = new THREE.Mesh(new THREE.PlaneGeometry(4000, 4000), new THREE.ShadowMaterial({opacity:.14})); window._catcher.position.z = -37.2; root.add(window._catcher); }
  window._catcher.visible = !patio.checked;                 // mjuk skugga under huset när uteplatsen är avstängd
  if(patio.checked) aimSun(new THREE.Vector3(-150, 700, 1100), 2600); else aimSun(new THREE.Vector3(0, 130, 20), 330);
  scene.traverse(o => { if(o.isMesh){ const transparent = o.material && o.material.transparent && o.material.opacity < 1; o.castShadow = !transparent && o !== screenMesh; o.receiveShadow = o !== screenMesh; } }); }
const patio = document.getElementById("patio");
function preset(v){
  if(v==="patio"){ TARGET.set(80,700,1100); Object.assign(view,{th:-0.6, ph:1.22, r:5100}); cam.fov=40; }
  else if(v==="door"){ TARGET.set(420,520,300); Object.assign(view,{th:0.22, ph:1.0, r:3000}); cam.fov=50; }
  else if(v==="front"){ const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,120+z,-10); Object.assign(view,{th:0, ph:1.45, r:820}); cam.fov=32; }
  else if(v==="side" || v==="inside"){ const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,95+z,-55); Object.assign(view,{th:-1.45, ph:1.42, r:620}); cam.fov=32; if(v==="inside" && !xray.checked){ xray.checked = true; apply(); } }
  else { const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,100+z,-20); Object.assign(view,{th:-0.55, ph:1.22, r:820}); cam.fov=32; }
  cam.updateProjectionMatrix(); draw();
}
document.querySelectorAll(".views button[data-v]").forEach(b => b.addEventListener("click", () => { if(b.dataset.v==="door" && !patio.checked){ patio.checked=true; patioToggle(); } preset(b.dataset.v); }));
function patioToggle(){ patioG.visible = patio.checked; setHouseZ(); preset(patio.checked ? "patio" : "close"); apply(); }
patio.addEventListener("change", patioToggle);

// ================= DEMO =================
const scr = document.createElement("canvas"); scr.width = 336; scr.height = 248;
const sctx = scr.getContext("2d"); const stex = new THREE.CanvasTexture(scr);
const screenMesh = new THREE.Mesh(new THREE.PlaneGeometry(40.8,30.6), new THREE.MeshBasicMaterial({map:stex}));
screenMesh.rotation.x = Math.PI/2; screenMesh.position.set(0,2.9,108); house.add(screenMesh);
// kameramodul (Raspberry Pi Camera Module 3) bakom kamerahålet, lutad 35° nedåt
const camG = new THREE.Group(); camG.position.set(0, 11.2, 172.1); camG.rotation.x = 35*Math.PI/180; house.add(camG);
const pcb = new THREE.Mesh(new THREE.BoxGeometry(25, 1.2, 24), new THREE.MeshStandardMaterial({color:"#1F6B3A", roughness:.6})); camG.add(pcb);
const lensBlock = new THREE.Mesh(new THREE.BoxGeometry(8.5, 4, 8.5), new THREE.MeshStandardMaterial({color:"#1A1A1A", roughness:.5})); lensBlock.position.y = -2.6; camG.add(lensBlock);
const barrel = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 3.4, 2.4, 24), new THREE.MeshStandardMaterial({color:"#0D0D0D", roughness:.3, metalness:.4})); barrel.position.y = -5.6; camG.add(barrel);
const glassEl = new THREE.Mesh(new THREE.SphereGeometry(2.6, 16, 10, 0, Math.PI*2, 0, Math.PI/2), new THREE.MeshStandardMaterial({color:"#2A3F6B", roughness:.05, metalness:.6})); glassEl.rotation.x = Math.PI; glassEl.position.y = -6.8; camG.add(glassEl);
const ribbon = new THREE.Mesh(new THREE.BoxGeometry(16, 40, .3), new THREE.MeshStandardMaterial({color:"#E8DCC0", roughness:.8})); ribbon.position.set(0, 21, -10.5); camG.add(ribbon);   // flatkabeln går bakåt in i huset
for(const [x,z] of [[-10.5,-6.25],[10.5,-6.25],[-10.5,6.25],[10.5,6.25]]){ const sc=new THREE.Mesh(new THREE.CylinderGeometry(1.6,1.6,1,10), new THREE.MeshStandardMaterial({color:"#B8B8B8", metalness:.7, roughness:.3})); sc.position.set(x,-.9,z); camG.add(sc); }
const camGlass = new THREE.Mesh(new THREE.CylinderGeometry(12, 12, 3, 40), new THREE.MeshStandardMaterial({color:"#24313A", transparent:true, opacity:.6, roughness:.05, metalness:.2}));
camGlass.position.set(0, 2.7, 167); house.add(camGlass);
function screen(mode){
  const c = sctx; c.fillStyle = "#06120b"; c.fillRect(0,0,336,248);
  c.textAlign = "center"; c.textBaseline = "middle";
  if(mode==="ok"){ c.fillStyle="#0d3a1f"; c.fillRect(0,0,336,248); c.fillStyle="#5CFF8F"; c.font="bold 46px Courier New, monospace"; c.fillText("ACCESS",168,100); c.fillText("GRANTED",168,152); }
  else if(mode==="no"){ c.fillStyle="#3a0d0d"; c.fillRect(0,0,336,248); c.fillStyle="#FF6B5C"; c.font="bold 46px Courier New, monospace"; c.fillText("ACCESS",168,100); c.fillText("DENIED",168,152); }
  else if(mode==="scan"){ c.fillStyle="#F2C14E"; c.font="bold 30px Courier New, monospace"; c.fillText("VERIFIERAR…",168,124); }
  else if(mode==="empty"){ c.fillStyle="#F2C14E"; c.font="bold 30px Courier New, monospace"; c.fillText("MAGASINET",168,100); c.fillText("ÄR TOMT",168,140); }
  else { c.fillStyle="#3f8f5f"; c.font="24px Courier New, monospace"; c.fillText("VÄNTAR PÅ",168,104); c.fillText("BESÖKARE…",168,138); }
  stex.needsUpdate = true; draw();
}
const nutGeo = new THREE.SphereGeometry(8.5, 18, 12); nutGeo.scale(1,1,1.15);
const nutMat = new THREE.MeshStandardMaterial({color:"#8A5A2E", roughness:.7});
const wheel = meshes.find(m=>m.userData.name==="doserhjul").userData.holder;        // vrids kring sin axel
const DUMP = 130*Math.PI/180, AX = [0,57,64.3], PKT = 19.3;                           // tömvinkel, axelns läge, nötens avstånd från axeln i fickan
const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set t(v){ lids.forEach(h=>h.rotation.x=-1.66*v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};
// platser i magasinet: en nöt i halsen över hjulet, resten i tratten och lådan ovanför
const SLOTS = [[0,57,105.5],[-10,56,116],[10,56,116],[0,73,117]];
for(const y of [52,70,88]) for(const x of [-20,0,20]) SLOTS.push([x,y,132]);
for(const z of [150,166]) for(const y of [49,65.5,82,97]) for(const x of [-34,-17,0,17,34]) SLOTS.push([x+(z===166?2:0), y+(z===166?1:0), z]);
const nearAxis = p => Math.hypot(p[0], p[1]-57);
SLOTS.sort((a,b)=> (a[2]-b[2]) || (nearAxis(a)-nearAxis(b)));
const hopper = []; let pocket = null, served = 0, busy = false;
const tweens = [];
function tween(dur, fn, delay=0){ return new Promise(res => tweens.push({t0:performance.now()+delay, dur, fn, res})); }
let raf = 0;
function tick(now){
  for(let i=tweens.length-1;i>=0;i--){ const tw=tweens[i]; const k=(now-tw.t0)/tw.dur; if(k<0) continue; const e=Math.min(1,k); tw.fn(e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2); if(e>=1){ tweens.splice(i,1); tw.res(); } }
  draw(); raf = tweens.length ? requestAnimationFrame(tick) : 0;
}
function run(){ if(!raf) raf = requestAnimationFrame(tick); }
const lerp=(a,b,t)=>a+(b-a)*t;
const wait = ms => { const w = tween(ms, ()=>{}); run(); return w; };
function path(obj, pts, dur, delay=0){
  const seg=[]; let L=0; for(let i=1;i<pts.length;i++){ const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1],pts[i][2]-pts[i-1][2]); seg.push(d); L+=d; }
  return tween(dur, t => { let s=t*L, i=0; while(i<seg.length-1 && s>seg[i]){ s-=seg[i]; i++; } const u=Math.min(1,s/seg[i]); const a=pts[i], b=pts[i+1]; obj.position.set(lerp(a[0],b[0],u),lerp(a[1],b[1],u),lerp(a[2],b[2],u)); obj.rotation.x+=0.15; }, delay);
}
// kameran glider mellan vyer
function flyTo(o, dur=1000){
  const off = patio.checked ? PED_H+FOOT : 0;
  const a = {x:TARGET.x, y:TARGET.y, z:TARGET.z, th:view.th, ph:view.ph, r:view.r, fov:cam.fov};
  let dth = o.th-a.th; dth = Math.atan2(Math.sin(dth), Math.cos(dth));
  const tw = tween(dur, t => { TARGET.set(lerp(a.x,o.T[0],t), lerp(a.y,o.T[1]+off,t), lerp(a.z,o.T[2],t)); view.th = a.th+dth*t; view.ph = lerp(a.ph,o.ph,t); view.r = lerp(a.r,o.r,t); cam.fov = lerp(a.fov,32,t); cam.updateProjectionMatrix(); });
  run(); return tw;
}
const VIEW_VISIT = {T:[0,62,58], th:-0.62, ph:1.2, r:700}, VIEW_MECH = {T:[0,80,-40], th:-1.32, ph:1.38, r:600}, VIEW_HOME = {T:[0,105,-20], th:-0.55, ph:1.15, r:860};
// textremsan i bilden
const capEl = document.getElementById("cap"), capBar = document.getElementById("capBar");
function cap(title, text, progress){ capEl.hidden = false; document.getElementById("capT").textContent = title; document.getElementById("capX").textContent = text; if(progress!==undefined) capBar.style.width = (progress*100)+"%"; }
function capHide(){ capEl.hidden = true; capBar.style.width = "0"; }
const acts = [...document.querySelectorAll("aside button.act")];
function setBusy(b){ busy = b; acts.forEach(x => x.disabled = b); }
function status(){ document.getElementById("status").textContent = `I magasinet: ${hopper.length + (pocket?1:0)} nötter. Lennart har fått ${served}.`; }
function demoReset(){ if(asmStep) asmStop(); if(ex.value!=0) ex.value = 0; solo = null; markRow(); apply(); }
function seat(n){ nutsGroup.remove(n); wheel.add(n); n.position.set(0,0,PKT); }                 // nöten ligger i hjulets ficka
function unseat(n){ const w=new THREE.Vector3(); n.getWorldPosition(w); nutsGroup.worldToLocal(w); wheel.remove(n); nutsGroup.add(n); n.position.copy(w); n.visible = true; }
function loadPocket(){
  if(pocket || !hopper.length) return Promise.resolve();
  const n = hopper.shift(); pocket = n; const from = n.position.toArray();
  return path(n, [from, [0,57,Math.max(from[2],106)], [0,57,AX[2]+PKT]], 450).then(()=>seat(n));
}
const fillBtn = document.getElementById("fill"), roofBtn = document.getElementById("roofbtn");
const isFull = () => hopper.length === SLOTS.length && !!pocket;
function fillLabel(){ fillBtn.lastChild.textContent = isFull() ? "Töm magasinet" : "Fyll på nötter"; }
function freeSlots(){ const used = new Set(hopper.map(n=>n.userData.slot)); return SLOTS.map((s,i)=>i).filter(i=>!used.has(i)); }
function sortHopper(){ hopper.sort((a,b)=> (a.position.z-b.position.z) || (nearAxis(a.position.toArray())-nearAxis(b.position.toArray()))); }
function addNut(i){ const n = new THREE.Mesh(nutGeo, nutMat); n.userData.slot = i; n.rotation.set(Math.random()*3,Math.random()*3,0); nutsGroup.add(n); hopper.push(n); return n; }

// ---- aktörerna: Lennart och skatan ----
const actors = new THREE.Group(); nutsGroup.parent.add(actors);
function blob(r, color, pos, sc=[1,1,1]){ const m = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), new THREE.MeshStandardMaterial({color, roughness:.85})); m.position.set(...pos); m.scale.set(...sc); m.castShadow = true; return m; }
function cone(r, h, color, pos, rot){ const m = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14), new THREE.MeshStandardMaterial({color, roughness:.8})); m.position.set(...pos); m.rotation.set(...rot); m.castShadow = true; return m; }
const FUR = "#A9562F", CREAM = "#F0E2CC", DARK = "#1B1B1D";
// Lennart spelas av en klisterdekal som en hand håller i och låter hoppa
function squirrelArt(){
  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");
  let seed = 7; const rnd = () => (seed = (seed*16807) % 2147483647) / 2147483647;
  const FURC = "#B4572B", DARKC = "#8A3F1E", LIGHT = "#DB8F55", CREAMC = "#F5E8D4";
  const ell = (x,y,rx,ry,rot,fill) => { c.beginPath(); c.ellipse(x,y,rx,ry,rot,0,Math.PI*2); c.fillStyle = fill; c.fill(); };
  const grad = (x,y,r,c0,c1) => { const g = c.createRadialGradient(x-r*.3,y-r*.35,r*.1,x,y,r); g.addColorStop(0,c0); g.addColorStop(1,c1); return g; };
  // svansen: en bred, yvig båge bakom kroppen
  c.lineCap = "round"; c.lineJoin = "round";
  const tail = () => { c.beginPath(); c.moveTo(318,418); c.bezierCurveTo(430,400,470,250,415,150); c.bezierCurveTo(395,112,360,98,335,112); };
  tail(); c.strokeStyle = DARKC; c.lineWidth = 104; c.stroke();
  tail(); c.strokeStyle = FURC; c.lineWidth = 88; c.stroke();
  tail(); c.strokeStyle = LIGHT; c.lineWidth = 34; c.globalAlpha = .55; c.stroke(); c.globalAlpha = 1;
  // kropp, lår, mage
  ell(262,332,90,112,-0.18,grad(262,332,115,LIGHT,FURC));
  ell(296,388,72,64,0,grad(296,388,74,FURC,DARKC));
  ell(214,338,46,84,-0.1,grad(214,338,86,"#FFFAF0",CREAMC));
  // bakre örat, huvud, nos
  c.beginPath(); c.moveTo(232,140); c.lineTo(262,62); c.lineTo(274,150); c.closePath(); c.fillStyle = DARKC; c.fill();
  ell(192,186,64,55,-0.1,grad(192,186,66,LIGHT,FURC));
  ell(142,202,32,25,0.1,grad(142,202,34,"#E9A56A",FURC));
  ell(160,216,30,19,0.15,CREAMC);
  ell(113,197,7,6,0,"#2B1A12");
  // främre örat med tofs
  c.beginPath(); c.moveTo(196,142); c.lineTo(222,58); c.lineTo(246,146); c.closePath(); c.fillStyle = FURC; c.fill();
  c.beginPath(); c.moveTo(208,138); c.lineTo(222,84); c.lineTo(236,140); c.closePath(); c.fillStyle = "#E7B08A"; c.fill();
  // öga
  ell(178,174,13,12,0,CREAMC); ell(178,174,9.5,9.5,0,"#17100C"); ell(174.5,170,3.2,3.2,0,"#FFFFFF");
  // arm, tass, fot
  ell(186,292,17,38,0.55,grad(186,292,38,FURC,DARKC)); ell(163,318,12,10,0,DARKC);
  ell(218,440,52,17,0,grad(218,440,52,FURC,DARKC));
  // päls: korta streck i pälsens riktning, bara ovanpå det som redan är ritat
  c.globalCompositeOperation = "source-atop"; c.lineWidth = 1.6;
  for(let k=0;k<2600;k++){ const x = 100+rnd()*380, y = 60+rnd()*400; const tailSide = x > 330; const ang = tailSide ? -1.2+rnd()*.7 : 1.1+rnd()*.8; const L = 5+rnd()*9;
    c.strokeStyle = rnd()<.5 ? "rgba(255,214,170,.20)" : "rgba(90,36,14,.20)"; c.beginPath(); c.moveTo(x,y); c.lineTo(x+Math.cos(ang)*L, y+Math.sin(ang)*L); c.stroke(); }
  c.globalCompositeOperation = "source-over";
  // morrhår
  c.strokeStyle = "rgba(40,25,15,.7)"; c.lineWidth = 1.3; [[-34,-8],[-38,2],[-32,12]].forEach(d => { c.beginPath(); c.moveTo(126,206); c.lineTo(126+d[0],206+d[1]); c.stroke(); });
  return stickerFinish(a);
}
function stickerFinish(a){                       // vit stansad kant runt motivet, sedan en svag blank yta; baksidan är bara vitt papper
  const S = a.width, b = document.createElement("canvas"); b.width = b.height = S; const d = b.getContext("2d");
  for(let k=0;k<28;k++){ const t = k/28*Math.PI*2; d.drawImage(a, Math.cos(t)*15, Math.sin(t)*15); }
  d.globalCompositeOperation = "source-in"; d.fillStyle = "#FBFBF8"; d.fillRect(0,0,S,S);
  const back = document.createElement("canvas"); back.width = back.height = S; back.getContext("2d").drawImage(b,0,0);
  d.globalCompositeOperation = "source-over"; d.drawImage(a,0,0);
  d.globalCompositeOperation = "source-atop"; const gl = d.createLinearGradient(80,40,430,470); gl.addColorStop(0,"rgba(255,255,255,.28)"); gl.addColorStop(.35,"rgba(255,255,255,0)"); gl.addColorStop(.7,"rgba(255,255,255,0)"); gl.addColorStop(1,"rgba(0,0,0,.10)"); d.fillStyle = gl; d.fillRect(0,0,S,S);
  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];
}
function magpieArt(){
  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d"); c.translate(0,42);
  let seed = 11; const rnd = () => (seed = (seed*16807) % 2147483647) / 2147483647;
  const BLK = "#17181C", WHT = "#F6F5F0", BLU = "#1F3F6E";
  const ell = (x,y,rx,ry,rot,fill) => { c.beginPath(); c.ellipse(x,y,rx,ry,rot,0,Math.PI*2); c.fillStyle = fill; c.fill(); };
  // den långa stjärten med blågrön glans
  const tg = c.createLinearGradient(300,290,490,380); tg.addColorStop(0,"#16303F"); tg.addColorStop(.5,"#1F5A5E"); tg.addColorStop(1,"#1B2A55");
  c.beginPath(); c.moveTo(300,262); c.lineTo(494,362); c.lineTo(486,384); c.lineTo(292,318); c.closePath(); c.fillStyle = tg; c.fill();
  // ben och fötter
  c.strokeStyle = "#2A2A2E"; c.lineWidth = 7; c.lineCap = "round";
  [[226,330,220,398],[262,332,266,398]].forEach(l => { c.beginPath(); c.moveTo(l[0],l[1]); c.lineTo(l[2],l[3]); c.stroke(); c.beginPath(); c.moveTo(l[2]-20,l[3]+3); c.lineTo(l[2],l[3]); c.lineTo(l[2]+16,l[3]+4); c.stroke(); });
  // kropp, vit buk, vinge, vit skulderfläck
  ell(248,268,98,62,-0.25,BLK);
  ell(232,300,72,40,-0.2,WHT);
  const wg = c.createLinearGradient(240,240,370,310); wg.addColorStop(0,"#1B2C52"); wg.addColorStop(1,BLU); ell(302,272,74,27,0.32,wg);
  ell(268,240,46,16,0.38,WHT);
  // hals, huvud, näbb, öga
  ell(196,236,52,46,-0.3,BLK); ell(160,204,45,43,0,BLK);
  c.beginPath(); c.moveTo(124,190); c.lineTo(66,210); c.lineTo(126,224); c.closePath(); c.fillStyle = "#2B2C31"; c.fill();
  ell(150,194,8,8,0,"#6B6F78"); ell(150,194,6,6,0,"#0B0B0D"); ell(148,192,2,2,0,"#FFFFFF");
  // fjädrar: korta streck ovanpå det som redan är ritat
  c.globalCompositeOperation = "source-atop"; c.lineWidth = 1.5;
  for(let k=0;k<1800;k++){ const x = 80+rnd()*420, y = 150+rnd()*260, L = 6+rnd()*10, ang = 0.35+rnd()*.5;
    c.strokeStyle = rnd()<.5 ? "rgba(120,160,220,.16)" : "rgba(0,0,0,.14)"; c.beginPath(); c.moveTo(x,y); c.lineTo(x+Math.cos(ang)*L, y+Math.sin(ang)*L); c.stroke(); }
  c.globalCompositeOperation = "source-over";
  return stickerFinish(a);
}
// en hand i naturlig storlek: handflata, fem fingrar med leder och naglar, handled, underarm och ärm
const SKIN = new THREE.MeshStandardMaterial({color:"#D8A584", roughness:.62}), NAIL = new THREE.MeshStandardMaterial({color:"#F1D3C2", roughness:.3}), CLOTH = new THREE.MeshStandardMaterial({color:"#2E4057", roughness:.95});
const V = (x,y,z) => new THREE.Vector3(x,y,z);
function limb(g, a, b, r0, r1, mat=SKIN){            // avsmalnande, rundad del mellan två punkter
  const L = a.distanceTo(b), cyl = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, L, 20), mat);
  cyl.position.copy(a).add(b).multiplyScalar(.5); cyl.quaternion.setFromUnitVectors(V(0,1,0), b.clone().sub(a).normalize());
  const s0 = new THREE.Mesh(new THREE.SphereGeometry(r0, 20, 14), mat), s1 = new THREE.Mesh(new THREE.SphereGeometry(r1, 20, 14), mat); s0.position.copy(a); s1.position.copy(b);
  [cyl,s0,s1].forEach(m => { m.castShadow = m.receiveShadow = true; g.add(m); });
}
function lump(g, c, r, sc, mat=SKIN){ const m = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), mat); m.position.copy(c); m.scale.set(...sc); m.castShadow = m.receiveShadow = true; g.add(m); return m; }
function nail(g, a, b, r, away){                     // nagel på yttersta leden, på fingrets ovansida
  const d = b.clone().sub(a).normalize(), n = away.clone().sub(d.clone().multiplyScalar(away.dot(d))).normalize();
  const m = lump(g, a.clone().lerp(b,.72).add(n.clone().multiplyScalar(r*.62)), r*.86, [1,1,1], NAIL);
  m.quaternion.setFromUnitVectors(V(0,0,1), n); m.scale.set(.82,1.05,.34); const q = new THREE.Quaternion().setFromUnitVectors(V(0,1,0), d.clone().applyQuaternion(m.quaternion.clone().invert()).setZ(0).normalize()); m.quaternion.multiply(q);
}
function buildHand(grip){
  // handens egna axlar: y mot fingrarna, x mot tummen, z ut från handflatan
  const g = new THREE.Group();
  lump(g, V(0,50,0), 1, [41,50,14]); lump(g, V(-8,18,3), 1, [33,22,15]); lump(g, V(27,34,9), 1, [19,31,15]); lump(g, V(-30,44,5), 1, [13,34,13]);
  const curl = (base, lens, radii, flex, splay) => { let pt = base.clone(), ang = 0; const pts = [pt.clone()];
    lens.forEach((L,k) => { ang += flex[k]*Math.PI/180; pt = pt.clone().add(V(splay, Math.cos(ang), Math.sin(ang)).normalize().multiplyScalar(L)); pts.push(pt.clone()); });
    lump(g, base, radii[0]+1.2, [1,1,1]);
    for(let k=0;k<3;k++) limb(g, pts[k], pts[k+1], radii[k], radii[k+1]);
    const dz = pts[3].clone().sub(pts[2]).normalize(); nail(g, pts[2], pts[3], radii[3], V(0, dz.z, -dz.y)); };
  curl(V(9,98,-2),  [46,30,23], [10,9,8,7],     [80,85,60], 0);          // långfinger, ringfinger och lillfinger är krökta in mot handflatan
  curl(V(-10,95,-2),[42,28,22], [9.5,8.6,7.6,6.8],[85,85,60], -.05);
  curl(V(-27,87,-1),[33,20,19], [8.4,7.4,6.6,6], [88,85,60], -.1);
  // pekfinger och tumme möts i ett nyp
  const K = V(27,97,-2), J1 = V(16.5,123,36.5), J2 = V(22.8,113.7,58.6), I = V(21,98.6,72.4);       // pekfingret löper bakom dekalen ända till mellanleden
  lump(g, K, 11, [1,1,1]); limb(g, K, J1, 10, 9); limb(g, J1, J2, 9, 8); limb(g, J2, I, 8, 7); nail(g, J2, I, 7, V(0,1,.6));
  const B = V(31,20,10), T1 = V(52,47,34), T2 = V(46,74,55), T = V(38,88.4,64.6);
  limb(g, B, T1, 14, 11.5); limb(g, T1, T2, 11.5, 10); limb(g, T2, T, 10, 8.6); nail(g, T2, T, 8.6, V(1,-.4,-.2));
  // handled, underarm och uppkavlad ärm
  const arm = new THREE.Group(), armIn = new THREE.Group(); armIn.scale.set(1,1,.8); arm.add(armIn);       // armen är en egen del, så att handleden kan böjas
  limb(armIn, V(0,6,0), V(0,-60,0), 26, 25); limb(armIn, V(0,-60,0), V(0,-170,-6), 25, 36); lump(g, V(0,4,0), 1, [27,20,21]);
  limb(armIn, V(0,-150,-6), V(0,-420,-22), 41, 46, CLOTH); const cuff = new THREE.Mesh(new THREE.TorusGeometry(42, 7, 12, 28), CLOTH); cuff.rotation.x = Math.PI/2; cuff.position.set(0,-150,-6); cuff.castShadow = true; armIn.add(cuff);
  // Högerhand som kommer in från höger, i höjd med dekalen. Tummen ligger framför dekalen och pekfingret bakom.
  // Handen vrids så att pekfingret passerar dekalens plan utanför kanten (riktning D2), så att inget finger går igenom motivet.
  const mid0 = T.clone().add(I).multiplyScalar(.5), pch = T.clone().sub(I).normalize();
  const depthOf = v => v.clone().sub(mid0).dot(pch), k = (0-depthOf(J1))/(depthOf(K)-depthOf(J1)), X = J1.clone().lerp(K,k).sub(mid0);
  const d = X.sub(pch.clone().multiplyScalar(X.dot(pch))).normalize(), r = pch.clone().cross(d);
  const P2 = V(0,-1,0), D2 = V(Math.cos(1.15),0,Math.sin(1.15)), R2 = P2.clone().cross(D2);       // D2 pekar snett uppåt höger: handflatan hamnar rakt till höger om nypet
  const M = new THREE.Matrix4().makeBasis(P2,D2,R2).multiply(new THREE.Matrix4().makeBasis(pch,d,r).transpose());
  g.quaternion.setFromRotationMatrix(M); g.scale.setScalar(.86); arm.scale.setScalar(.86);
  const mid = mid0.clone().applyMatrix4(M); g.position.set(grip[0]-mid.x*.86, -mid.y*.86 + grip[0]*grip[0]*0.0016 - .7, grip[1]-mid.z*.86);      // dekalen är lätt böjd: nypet följer ytan där handen håller
  arm.quaternion.copy(g.quaternion); arm.userData.base = arm.quaternion.clone();                    // armen fortsätter rakt ut från handleden
  g.userData.arm = arm;
  return g;
}
// en docka: dekal + hand. pose vrids kring fötterna när handen vinklar ner dekalen
function makePuppet(tex, grip){
  const [front, back] = tex; front.anisotropy = back.anisotropy = 4;
  const P = {root:new THREE.Group(), pose:new THREE.Group(), inner:new THREE.Group(), sticker:new THREE.Group()};
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1), pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  const depth = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:back, alphaTest:.5, side:THREE.DoubleSide});   // skuggan följer dekalens kontur
  mf.customDepthMaterial = mb.customDepthMaterial = depth;
  P.sticker.add(mf, mb); P.sticker.rotation.x = Math.PI/2; P.sticker.position.set(0,0,64);
  P.hand = buildHand(grip); P.arm = P.hand.userData.arm;
  P.pose.position.set(0,0,12); P.inner.position.set(0,0,-12); P.inner.add(P.sticker, P.hand); P.pose.add(P.inner); P.root.add(P.pose, P.arm);
  P.root.userData.puppet = P; P.root.visible = false; return P;
}
const LP = makePuppet(squirrelArt(), [38,90]), SP = makePuppet(magpieArt(), [43,36]);       // nypet sitter vid svansens övre kant
const lennart = LP.root, pose = LP.pose, skata = SP.root;
// mjuk skugga på marken under Lennart: gör att han ser ut att stå på gräset och lyfta när han hoppar
const shade = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d"); const g = x.createRadialGradient(64,64,4,64,64,62); g.addColorStop(0,"rgba(0,0,0,.55)"); g.addColorStop(1,"rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(0,0,128,128);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(150,150), new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c), transparent:true, depthWrite:false})); m.renderOrder = 2; m.visible = false; return m; })();
actors.add(shade);
function syncArm(P){ P.arm.quaternion.setFromAxisAngle(new THREE.Vector3(0,1,0), P.pose.rotation.y*.45).multiply(P.arm.userData.base);   // armen följer med en bit, resten tar handleden
  P.root.updateMatrixWorld(true); P.arm.position.copy(P.root.worldToLocal(P.hand.getWorldPosition(new THREE.Vector3()))); }   // armen följer handleden när handen vinklas
function ground(P){ syncArm(P); const p = P.root.position; shade.visible = P.root.visible && p.z > -5 && p.y > -172 && Math.abs(p.x) < 112;      // bara över framgården
  const k = 1/(1+Math.max(0,p.z)/40); shade.position.set(p.x, p.y, 2.2); shade.rotation.z = P.root.rotation.z; shade.scale.set(.95*k, .34*k, 1); shade.material.opacity = .5*k; }
// hur mycket dockan måste luta för att nosen eller näbben ska nå en punkt, och var fötterna då ska stå
function bowTo(P, tip, target, lift){
  const mx = tip[0], mz = tip[2]-12, yaw = P.root.rotation.z; let al = 0;
  while(al > -1.4 && lift+12 - mx*Math.sin(al) + mz*Math.cos(al) > target[2]) al -= 0.01;
  const fx = mx*Math.cos(al) + mz*Math.sin(al), fy = tip[1];
  return {al, stand:[target[0] - (fx*Math.cos(yaw) - fy*Math.sin(yaw)), target[1] - (fx*Math.sin(yaw) + fy*Math.cos(yaw)), lift]};
}
function tilt(P, from, to, dur){ const tw = tween(dur, t => { P.pose.rotation.y = lerp(from,to,t); syncArm(P); }); run(); return tw; }
function faceCam(obj){ const c = actors.worldToLocal(cam.position.clone()); obj.rotation.z = Math.atan2(c.x-obj.position.x, -(c.y-obj.position.y)); }
actors.add(lennart, skata);
function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); if(obj.userData.puppet) ground(obj.userData.puppet); }); }
const SPOT = [0,-33,13.2], MOUTH = [-36,-4,70], BEAK = [-44,-4,56], LEN_X = 30;     // nosen på dekalen; Lennart står lite till höger så att skålen syns

async function moveRoof(upNow){
  if(roofUp===upNow) return; const a = roofLift, b = upNow ? 1 : 0;
  const tw = tween(900, t => { roofLift = a+(b-a)*t; apply(); }); run(); await tw;
  roofUp = upNow; roofBtn.lastChild.textContent = roofUp ? "Lägg på taket" : "Lyft av taket";
}
let roofUp = false;
function setPeek(v, dur=600){ const a = peek; const tw = tween(dur, t => { peek = lerp(a,v,t); apply(); }); run(); return tw; }

// ---- Lennart kommer på besök ----
async function visit(inside){
  if(busy) return; setBusy(true); demoReset(); await moveRoof(false);
  const back = {T:[TARGET.x, TARGET.y-(patio.checked?PED_H+FOOT:0), TARGET.z], th:view.th, ph:view.ph, r:view.r}, hadX = xray.checked;
  if(inside){ xray.checked = true; apply(); await flyTo(VIEW_MECH); } else await flyTo(VIEW_VISIT);
  lennart.visible = true; pose.rotation.y = 0; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart); ground(LP);
  cap("Lennart kommer hoppande", "I demon spelas han av en klisterdekal.", .1);
  let h = hop(lennart, [LEN_X+10,-165,0], 900, 34, 2); run(); await h; h = hop(lennart, [LEN_X,-104,0], 900, 26, 2); run(); await h;
  cap("Kameran tittar", "Den tar tre bilder och AI:n avgör vem som står där.", .3); screen("scan"); await wait(1500);
  if(!pocket){
    screen("empty"); cap("Magasinet är tomt", "Lennart får vänta. Fyll på nötter och prova igen.", 1); await wait(2400);
  } else {
    screen("ok"); cap("ACCESS GRANTED", "Det är Lennart. Luckan öppnas och hjulet vrider fram en nöt.", .5);
    const open = tween(900, t => { lid.t = t; }), turn = tween(1300, t => { wheel.rotation.x = DUMP*t; }, 350);
    run(); await Promise.all([open, turn]);
    cap("En nöt rullar ut", "Fickan släpper nöten i rännan, och den rullar ner i skålen.", .7);
    const n = pocket; pocket = null; unseat(n);
    const fall = path(n, [n.position.toArray(),[0,33.7,41.2],[0,18.7,28.6],[0,3.7,16.0],[0,-5,13.2],SPOT], 1500);
    const ret = tween(1200, t => { wheel.rotation.x = DUMP*(1-t); }, 900);
    run(); await Promise.all([fall, ret]); const lp = loadPocket(); run(); await lp;
    cap("Lennart äter ur skålen", "Handen för fram honom och tippar ner huvudet i skålen.", .85);
    const bw = bowTo(LP, MOUTH, [SPOT[0]+4, SPOT[1]-4, SPOT[2]+15], 10);      // utprovat så att dekalen går fri från skålens kant och den öppna luckan
    h = hop(lennart, bw.stand, 550, 18); run(); await h;
    await tilt(LP, 0, bw.al, 650);
    const eat = tween(1500, t => { pose.rotation.y = bw.al + Math.sin(t*Math.PI*8)*0.05; syncArm(LP); n.scale.setScalar(Math.max(0.001, 1-t*1.1)); }); run(); await eat;       // nöten äts upp i skålen
    nutsGroup.remove(n); n.scale.setScalar(1); served++; status();
    cap("Lennart är nöjd", "Luckan stängs långsamt, och bara när kameran inte ser någon rörelse.", .95);
    await tilt(LP, bw.al, 0, 600);
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);      // han hoppar baklänges hem, utan att vända sig
    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h;
  }
  shade.visible = false; pose.rotation.y = 0; lennart.visible = false; screen("idle"); fillLabel(); status(); capHide();
  if(inside){ xray.checked = hadX; apply(); }
  await flyTo(back, 900); setBusy(false);
}
document.getElementById("visit").addEventListener("click", () => visit(false));
document.getElementById("mech").addEventListener("click", () => visit(true));
// ---- Objuden gäst ----
document.getElementById("deny").addEventListener("click", async () => {
  if(busy) return; setBusy(true); demoReset(); await moveRoof(false);
  const back = {T:[TARGET.x, TARGET.y-(patio.checked?PED_H+FOOT:0), TARGET.z], th:view.th, ph:view.ph, r:view.r};
  await flyTo(VIEW_VISIT);
  skata.visible = true; SP.pose.rotation.y = 0; skata.position.set(60,-300,10); faceCam(skata); ground(SP);
  cap("En skata kommer hoppande", "Även hon spelas av en klisterdekal.", .15);
  let h = hop(skata, [14,-165,0], 900, 34, 2); run(); await h; h = hop(skata, [8,-112,0], 800, 24, 2); run(); await h;
  cap("Kameran tittar", "Tre bilder, och AI:n avgör vem som står där.", .4); screen("scan"); await wait(1500);
  screen("no"); cap("ACCESS DENIED", "Inte en ekorre. Luckan förblir stängd och besöket sparas som en incidentrapport.", .65);
  await wait(900);
  cap("Skatan pickar på luckan", "Hon försöker ändå, men luckan är stängd och nötterna ligger kvar.", .85);
  const pk = bowTo(SP, BEAK, [4,-28,39], 4);
  h = hop(skata, pk.stand, 500, 16); run(); await h;
  for(let k=0;k<3;k++){ await tilt(SP, k ? pk.al*.55 : 0, pk.al, 220); const shake = tween(260, t => { lid.px = Math.sin(t*Math.PI*4)*1.0*(1-t); }); run(); await Promise.all([shake, tilt(SP, pk.al, pk.al*.55, 260)]); lid.px = 0; }
  await tilt(SP, pk.al*.55, 0, 350); await wait(500);
  cap("Skatan ger upp", "Hon hoppar därifrån utan nöt.", 1);
  h = hop(skata, [20,-170,0], 900, 28, 2); run(); await h; h = hop(skata, [80,-320,10], 800, 34, 2); run(); await h;
  shade.visible = false; skata.visible = false; screen("idle"); capHide(); await flyTo(back, 900); setBusy(false);
});
// ---- taket och påfyllningen ----
roofBtn.addEventListener("click", async () => { if(busy) return; setBusy(true); demoReset(); await moveRoof(!roofUp); setBusy(false); });
fillBtn.addEventListener("click", async () => {
  if(busy) return; setBusy(true); demoReset();
  const wasUp = roofUp, emptying = isFull();
  cap(emptying ? "Magasinet töms" : "Påfyllning", "Taket hålls av magneter. Lyft av det, så ligger magasinet öppet.", .3);
  await moveRoof(true);
  if(emptying){
    const all = hopper.splice(0); if(pocket){ unseat(pocket); all.push(pocket); pocket=null; }
    const jobs = all.map((n,i) => path(n, [n.position.toArray(), [n.position.x, n.position.y, 330]], 600, i*12).then(()=>nutsGroup.remove(n)));
    run(); await Promise.all(jobs);
  } else {
    cap("Påfyllning", "Häll i hasselnötter i skal, 18–22 mm. Magasinet rymmer ungefär 50.", .7);
    const jobs = []; freeSlots().forEach((i,k) => { const s=SLOTS[i]; const n=addNut(i); n.position.set(s[0], s[1], 330); jobs.push(path(n, [[s[0],s[1],330],[s[0],s[1],s[2]]], 650, k*30)); });
    run(); await Promise.all(jobs); sortHopper();
    if(!pocket){ const p = loadPocket(); run(); await p; const i=freeSlots()[0]; if(i!==undefined){ const s=SLOTS[i]; const n=addNut(i); n.position.set(...s); sortHopper(); } }
  }
  if(!wasUp) await moveRoof(false);
  status(); fillLabel(); capHide(); setBusy(false);
});
// ---- monteringen spelas upp av sig själv ----
const asmCtl = document.getElementById("capCtl"), asmPlayBtn = document.getElementById("asmPlay");
let asmPlaying = false, asmTimer = 0;
function asmShow(n){
  clearTimeout(asmTimer); asmStep = n; const st = ASM[n-1];
  cap(`${n}. ${st.title}`, st.text, n/ASM.length);
  document.getElementById("asmPrev").disabled = n===1; document.getElementById("asmNext").disabled = n===ASM.length;
  asmAnim = 0; apply(); tween(900, t => { asmAnim = t; apply(); }); run();
  if(asmPlaying){ if(n<ASM.length) asmTimer = setTimeout(() => asmShow(n+1), 3600); else asmSetPlaying(false); }
}
function asmSetPlaying(b){ asmPlaying = b; asmPlayBtn.innerHTML = b ? "&#10074;&#10074;" : "&#9654;"; asmPlayBtn.setAttribute("aria-label", b ? "Pausa" : "Spela"); if(!b) clearTimeout(asmTimer); }
function asmStop(){ clearTimeout(asmTimer); asmPlaying = false; asmStep = 0; asmAnim = 1; asmCtl.hidden = true; capHide(); acts.forEach(x => x.disabled = false); apply(); }
document.getElementById("asmStart").addEventListener("click", async () => {
  if(busy) return; demoReset(); ex.value = 0; roofLift = 0; roofUp = false; roofBtn.lastChild.textContent = "Lyft av taket";
  acts.forEach(x => x.disabled = true); asmCtl.hidden = false; asmStep = 1; asmAnim = 0; apply();
  await flyTo(VIEW_HOME, 800); asmSetPlaying(true); asmShow(1);
});
document.getElementById("asmPrev").addEventListener("click", () => { if(asmStep>1){ asmSetPlaying(false); asmShow(asmStep-1); } });
document.getElementById("asmNext").addEventListener("click", () => { if(asmStep<ASM.length){ asmSetPlaying(false); asmShow(asmStep+1); } });
asmPlayBtn.addEventListener("click", () => { if(asmPlaying) asmSetPlaying(false); else { asmSetPlaying(true); asmShow(asmStep<ASM.length ? asmStep+1 : 1); } });
document.getElementById("asmEnd").addEventListener("click", asmStop);
// start med fullt magasin och en nöt i hjulets ficka
SLOTS.forEach((s,i) => { const n = addNut(i); n.position.set(...s); }); sortHopper();
{ const n = hopper.shift(); pocket = n; seat(n); const m = addNut(n.userData.slot); m.position.set(...SLOTS[n.userData.slot]); sortHopper(); }
screen("idle"); status(); fillLabel();

new ResizeObserver(resize).observe(stage);
resize(); patioG.visible = patio.checked; setHouseZ(); preset(patio.checked ? "patio" : "close"); apply();

// ================= FLIKAR =================
const TABS = ["modell","dokument","filer","utskrift"];
function showTab(name, focus){
  if(!TABS.includes(name)) name = "modell";
  TABS.forEach(t => { const b=document.getElementById("t-"+t), p=document.getElementById("p-"+t);
    const on = t===name; b.setAttribute("aria-selected", String(on)); b.tabIndex = on ? 0 : -1; p.hidden = !on; });
  if(focus) document.getElementById("t-"+name).focus();
  if(name==="modell") resize();
  if(name==="utskrift") setTimeout(initPlates, 0);   // körs när hela skriptet har laddats
}
document.querySelectorAll('[role="tab"]').forEach(b => {
  b.addEventListener("click", () => { location.hash = b.dataset.tab; });
  b.addEventListener("keydown", e => { const i=TABS.indexOf(b.dataset.tab);
    if(e.key==="ArrowRight"||e.key==="ArrowLeft"){ e.preventDefault(); const n=TABS[(i+(e.key==="ArrowRight"?1:TABS.length-1))%TABS.length]; location.hash=n; showTab(n,true); } });
});
window.addEventListener("hashchange", () => showTab(location.hash.slice(1)));
showTab(location.hash.slice(1));
// ================= 3D-FILER =================
const FILES = [["00_toleranstest.stl", 161484], ["01_bas.stl", 897184], ["01b_framgard.stl", 446984], ["02_grasmatta_gron.stl", 478184], ["02_grasmatta_stenar.stl", 2484], ["02b_framgard_grasmatta_gron.stl", 746984], ["02b_framgard_stenar.stl", 2484], ["03_bottenplatta.stl", 111084], ["03b_framgard_bottenplatta.stl", 75484], ["04_fotter_tpu.stl", 85284], ["05_kropp_rod.stl", 685184], ["05_kropp_sockel_gra.stl", 163484], ["05b_fonsterinsatser_gra.stl", 7684], ["05c_solskydd_gra.stl", 15284], ["05c_solskydd_vit.stl", 1084], ["05d_kropp_packning_tpu.stl", 80384], ["05e_vit_dorroverstycke.stl", 17484], ["05e_vit_hornbrada_1.stl", 33584], ["05e_vit_hornbrada_2.stl", 26784], ["05e_vit_hornbrada_3.stl", 33684], ["05e_vit_hornbrada_4.stl", 26784], ["05e_vit_kamerakrage.stl", 28884], ["05e_vit_sidofonster_1.stl", 36584], ["05e_vit_sidofonster_2.stl", 36584], ["05e_vit_skarmfonster.stl", 34584], ["06_tak_vanster_gra.stl", 236684], ["06_tak_vanster_vit.stl", 1284], ["06b_tak_hoger_gra.stl", 264984], ["06b_tak_hoger_vit.stl", 1284], ["06c_skorsten_rod.stl", 23484], ["06c_skorsten_vit.stl", 1484], ["06d_takpackning_tpu.stl", 2484], ["06e_nockkilar_gra.stl", 2084], ["07_farstukvist_rod.stl", 64384], ["07_farstukvist_vit.stl", 59684], ["08_lucka_gra.stl", 40884], ["08_lucka_vit.stl", 1884], ["09_stolphatt.stl", 2284], ["09b_stolphatt_packning_tpu.stl", 1684], ["10_doserhus.stl", 163684], ["11_doserhjul.stl", 78884], ["14_notmagasin.stl", 53484], ["15_kamerafaste.stl", 117084], ["16_elektroniklada.stl", 83284], ["16b_elektroniklada_lock.stl", 5684], ["17_elektroniklada_packning_tpu.stl", 1484], ["18_skarmram_svart.stl", 1684], ["19_skarmklamma.stl", 22984], ["21_blomlador_gron.stl", 256484], ["21_blomlador_vit.stl", 31884], ["21b_blomhuvuden_rod.stl", 967484], ["21b_blomhuvuden_vit.stl", 850084], ["22_takrannor_gra.stl", 142484], ["23_stupror_gra.stl", 174884], ["23_stupror_vit.stl", 49284], ["24_monteringsplatta.stl", 264184], ["25_genomforingar_tpu.stl", 69884]];
const fileInfo = {}; PARTS.forEach(p => { fileInfo[p.file] = {label: LABEL[p.name] || p.name, note: p.note}; });
fileInfo["00_toleranstest.stl"] = {label:"Toleranstest och nötmall", note:"Valfri färg. Skrivs ut först"};
const kb = n => n > 1048576 ? (n/1048576).toFixed(1).replace(".",",")+" MB" : Math.max(1,Math.round(n/1024))+" kB";
const ftbl = document.getElementById("ftbl"), msg = document.getElementById("filemsg");
FILES.forEach(([name,size]) => {
  const inf = fileInfo[name] || {label:"–", note:"–"};
  const tr = document.createElement("tr");
  tr.innerHTML = `<td><code>${name}</code></td><td>${inf.label}</td><td>${inf.note}</td><td>${kb(size)}</td><td><button class="dl small" type="button" data-f="${name}">Ladda ner</button></td>`;
  ftbl.appendChild(tr);
});
let zipBytes = null, zipObj = null;
function bytes(){ if(!zipBytes){ const b=atob(document.getElementById("zipdata").textContent.trim()); zipBytes=new Uint8Array(b.length); for(let i=0;i<b.length;i++) zipBytes[i]=b.charCodeAt(i); } return zipBytes; }
let downloads = null;
(window.claude ? window.claude.use("downloads") : Promise.resolve(null)).then(d => { downloads = d;
  if(!d){ document.querySelectorAll("button.dl").forEach(b=>b.disabled=true); msg.textContent = "Nedladdning fungerar inte i den här vyn. Be Marcus om zip-filen."; }
}).catch(() => {});
async function save(filename, data){
  if(!downloads){ msg.textContent = "Nedladdning fungerar inte i den här vyn. Be Marcus om zip-filen."; return; }
  try { await downloads.save({filename, data}); msg.textContent = `${filename} är sparad.`; }
  catch(e){ msg.textContent = e && e.code==="declined" ? "Nedladdningen avbröts." : "Det gick inte att spara filen just nu. Försök igen om en stund."; }
}
document.getElementById("dlall").addEventListener("click", () => save("lennarts-matstation-3d.zip", new Blob([bytes()])));
ftbl.addEventListener("click", async e => {
  const b = e.target.closest("button[data-f]"); if(!b) return;
  try {
    if(!zipObj) zipObj = await JSZip.loadAsync(bytes());
    const one = new JSZip(); one.file(b.dataset.f, await zipObj.file(b.dataset.f).async("uint8array"));
    const blob = await one.generateAsync({type:"blob", compression:"DEFLATE"});
    save(b.dataset.f.replace(/\.stl$/i, ".zip"), blob);              // STL kan inte sparas direkt, därför en liten zip per fil
  } catch(err){ msg.textContent = "Det gick inte att packa filen. Ladda ner alla i stället."; }
});

// ================= UTSKRIFT: BYGGPLATTOR =================
let plateView = null;
function initPlates(){
  if(plateView){ plateView.resize(); return; }
  const PLATES = JSON.parse(document.getElementById("platedata").textContent);
  const st = document.getElementById("pstage");
  const r2 = new THREE.WebGLRenderer({antialias:true, alpha:true}); r2.setPixelRatio(Math.min(window.devicePixelRatio,2));
  r2.shadowMap.enabled = true; r2.shadowMap.type = THREE.PCFSoftShadowMap; st.prepend(r2.domElement);
  const sc = new THREE.Scene(); const cam2 = new THREE.PerspectiveCamera(30,1,1,6000);
  sc.add(new THREE.HemisphereLight(0xF2F5FF, 0x77736A, 0.62));
  const l1 = new THREE.DirectionalLight(0xFFF3E0, 0.85); l1.position.set(-220,420,300); l1.castShadow = true; l1.shadow.mapSize.set(2048,2048);
  Object.assign(l1.shadow.camera,{left:-230,right:230,top:330,bottom:-230,near:1,far:1500}); sc.add(l1);
  const l2 = new THREE.DirectionalLight(0xDDE6FF, 0.3); l2.position.set(300,200,-300); sc.add(l2);
  const g = new THREE.Group(); g.rotation.x = -Math.PI/2; sc.add(g);
  // byggplattan: ljus yta med rutnät var 16:e mm
  const grid = (()=>{ const c=document.createElement("canvas"); c.width=c.height=1024; const x=c.getContext("2d");
    x.fillStyle="#C9C6BB"; x.fillRect(0,0,1024,1024); x.strokeStyle="rgba(60,55,45,.16)"; x.lineWidth=1;
    for(let i=0;i<=256;i+=16){ const q=i*4; x.beginPath(); x.moveTo(q,0); x.lineTo(q,1024); x.stroke(); x.beginPath(); x.moveTo(0,q); x.lineTo(1024,q); x.stroke(); }
    x.fillStyle="rgba(176,42,34,.20)"; x.fillRect(0,0,82,1024); x.strokeStyle="rgba(176,42,34,.55)"; x.lineWidth=3; x.beginPath(); x.moveTo(82,0); x.lineTo(82,1024); x.stroke();
    x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018); return new THREE.CanvasTexture(c); })();
  const edge = new THREE.MeshStandardMaterial({color:"#8F8C82"});
  const bed = new THREE.Mesh(new THREE.BoxGeometry(256,256,3), [edge,edge,edge,edge,new THREE.MeshStandardMaterial({map:grid, roughness:.9}),edge]);
  bed.position.set(0,0,-1.5); bed.receiveShadow = true; g.add(bed);
  const holder = new THREE.Group(); holder.position.set(-128,-128,0); g.add(holder);
  const T = new THREE.Vector3(0,30,0); const v = {th:-0.5, ph:0.85, r:640};
  const labels = document.createElement("div"); labels.style.cssText = "position:absolute;inset:0;overflow:hidden;pointer-events:none"; st.appendChild(labels);
  let current = null, picked = null;
  function place(){ cam2.position.set(T.x+v.r*Math.sin(v.ph)*Math.sin(v.th), T.y+v.r*Math.cos(v.ph), T.z+v.r*Math.sin(v.ph)*Math.cos(v.th)); cam2.lookAt(T); }
  function draw2(){
    place(); r2.render(sc, cam2);
    if(!current) return;
    const w = st.clientWidth, h = st.clientHeight; holder.updateMatrixWorld();
    current.groups.forEach((gr,k) => { const pt = new THREE.Vector3(gr.cx, gr.cy, gr.top+3).applyMatrix4(holder.matrixWorld).project(cam2);
      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });
    [[128,-9,0],[265,128,0],[10,265,0]].forEach((q,k) => { const pt = new THREE.Vector3(...q).applyMatrix4(holder.matrixWorld).project(cam2);
      const el = labels.children[current.groups.length+k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; });
  }
  function resize2(){ const w=st.clientWidth, h=st.clientHeight; if(!w||!h) return; r2.setSize(w,h,false); cam2.aspect=w/h; cam2.updateProjectionMatrix(); draw2(); }
  // rotera, flytta (högerklick, scrollknapp eller skift) och zooma
  const ptr = new Map(); let pan2=false, pinch=0, mid=null;
  function pan(dx,dy){ const rgt=new THREE.Vector3(), up=new THREE.Vector3(); cam2.updateMatrixWorld(); rgt.setFromMatrixColumn(cam2.matrixWorld,0); up.setFromMatrixColumn(cam2.matrixWorld,1); const k=v.r*0.0011; T.addScaledVector(rgt,-dx*k).addScaledVector(up,dy*k); }
  const cv = r2.domElement;
  cv.addEventListener("contextmenu", e=>e.preventDefault());
  cv.addEventListener("mousedown", e=>{ if(e.button===1) e.preventDefault(); });
  cv.addEventListener("pointerdown", e=>{ cv.setPointerCapture(e.pointerId); ptr.set(e.pointerId,{x:e.clientX,y:e.clientY}); pan2 = e.button===2||e.button===1||e.shiftKey;
    if(ptr.size===2){ const [a,b]=[...ptr.values()]; pinch=Math.hypot(a.x-b.x,a.y-b.y); mid={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; } });
  cv.addEventListener("pointermove", e=>{ if(!ptr.has(e.pointerId)) return; const q=ptr.get(e.pointerId); const dx=e.clientX-q.x, dy=e.clientY-q.y; ptr.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if(ptr.size===1){ if(pan2) pan(dx,dy); else { v.th-=dx*0.008; v.ph=Math.min(Math.PI/2-0.02, Math.max(0.05, v.ph-dy*0.008)); } }
    else if(ptr.size===2){ const [a,b]=[...ptr.values()]; const d=Math.hypot(a.x-b.x,a.y-b.y), m={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; if(pinch) v.r=Math.min(1800,Math.max(80,v.r*pinch/d)); if(mid) pan(m.x-mid.x,m.y-mid.y); pinch=d; mid=m; }
    draw2(); });
  const up2 = e=>{ ptr.delete(e.pointerId); pinch=0; mid=null; }; cv.addEventListener("pointerup",up2); cv.addEventListener("pointercancel",up2);
  cv.addEventListener("wheel", e=>{ e.preventDefault(); v.r=Math.min(1800,Math.max(80,v.r*(1+e.deltaY*0.001))); draw2(); }, {passive:false});
  const Q = 0.005, cache = {};
  function b64(sv,Ty){ const bin=atob(sv); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return new Ty(u.buffer); }
  function meshesOf(i){
    if(cache[i]) return cache[i];
    cache[i] = PLATES[i].items.map(it => {
      const q=b64(it.pos, Uint16Array), pos=new Float32Array(q.length); for(let k=0;k<q.length;k++) pos[k]=q[k]*Q;
      let geo=new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos,3));
      geo.setIndex(new THREE.BufferAttribute(it.i32 ? b64(it.idx,Uint32Array) : b64(it.idx,Uint16Array),1));
      geo=geo.toNonIndexed(); geo.computeVertexNormals();
      const m=new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color:it.color, roughness:.75, transparent:true})); m.castShadow=true; m.receiveShadow=true; m.userData.group=it.group; return m; });
    return cache[i];
  }
  const fmtH = h => h < 0.95 ? `ca ${Math.max(10,Math.round(h*6)*10)} min` : `ca ${String(Math.round(h*2)/2).replace(".",",")} h`;
  const box = document.getElementById("plates"), info = document.getElementById("pinfo");
  let lastPhase = null;
  // vilka plattor som är utskrivna: förvalt från filen, och det du själv bockar av sparas i webbläsaren
  const KEY = "lennart-utskrivna-plattor", keyOf = p => p.groups.map(g=>g.g).sort().join("+");
  let marks = {}; try { marks = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e) { marks = {}; }
  const isDone = p => (keyOf(p) in marks) ? marks[keyOf(p)] : !!p.printed;
  function setDone(p, v){ marks[keyOf(p)] = v; try { localStorage.setItem(KEY, JSON.stringify(marks)); } catch(e) {} }
  function paintButtons(){ box.querySelectorAll("button").forEach(b => { const p = PLATES[+b.dataset.i], d = isDone(p);
    b.classList.toggle("done", d); b.textContent = `${d ? "✓ " : ""}Platta ${+b.dataset.i+1}${p.material==="TPU" ? " · TPU" : ""}`; b.setAttribute("aria-label", b.textContent + (d ? ", utskriven" : "")); }); }
  PLATES.forEach((p,i) => {
    if(p.phase!==lastPhase){ const h=document.createElement("div"); h.className="ph"; h.textContent=p.phase; box.appendChild(h); lastPhase=p.phase; }
    const b=document.createElement("button"); b.type="button"; b.textContent=`Platta ${i+1}${p.material==="TPU"?" · TPU":""}`; b.dataset.i=i; b.setAttribute("aria-pressed","false");
    b.addEventListener("click",()=>show(i)); box.appendChild(b);
  });
  paintButtons();
  const total = PLATES.reduce((a,p)=>a+p.hours,0);
  function highlight(){ holder.children.forEach(m => { const dim = picked && m.userData.group!==picked; m.material.opacity = dim ? 0.15 : 1; m.material.depthWrite = !dim; m.castShadow = !dim; });
    info.querySelectorAll("li").forEach(li => li.setAttribute("aria-pressed", String(li.dataset.g===picked))); draw2(); }
  function show(i){
    current = PLATES[i]; picked = null;
    holder.clear(); meshesOf(i).forEach(m=>holder.add(m));
    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("") + `<span class="plabel dim">256 mm</span><span class="plabel dim">256 mm</span><span class="plabel dim">20,5 mm: bara vänster munstycke</span>`;
    box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed", String(+b.dataset.i===i)));
    const rows = current.groups.map(gr => `<li data-g="${gr.g}" tabindex="0" role="button" aria-pressed="false"><span>${gr.colors.map(c=>`<span class="sw" style="background:${c}"></span>`).join("")}</span><span><b>${gr.name}</b>${gr.how}<small>${fmtH(gr.hours)} · ${gr.files.join(", ")}</small></span></li>`).join("");
    const done = isDone(current), left = PLATES.reduce((a,p)=>a+(isDone(p)?0:p.hours),0), nDone = PLATES.filter(isDone).length;
    info.classList.toggle("done", done);
    info.innerHTML = `<h3>Platta ${i+1} av ${PLATES.length}${done ? ' <span class="pdone">Utskriven</span>' : ''}</h3><p style="margin:0;color:var(--ink-2)">${current.phase} · ${current.material}</p>
      <p class="ptime">${fmtH(current.hours)}<small>uppskattad tid för plattan · ${nDone} av ${PLATES.length} plattor utskrivna, ca ${Math.round(left)} h kvar av ${Math.round(total)} h</small></p>
      <button type="button" class="pmark">${done ? "Ångra: inte utskriven" : "Markera som utskriven"}</button>
      <p style="margin:0 0 .4rem;color:var(--ink-2);font-size:.9rem">Klicka på en del för att lyfta fram den.</p><ul>${rows}</ul>`;
    info.querySelector(".pmark").addEventListener("click", () => { setDone(current, !isDone(current)); paintButtons(); show(i); });
    info.querySelectorAll("li").forEach(li => { const pick = () => { picked = picked===li.dataset.g ? null : li.dataset.g; highlight(); };
      li.addEventListener("click", pick); li.addEventListener("keydown", e => { if(e.key==="Enter"||e.key===" "){ e.preventDefault(); pick(); } }); });
    T.set(0, Math.min(110, current.height*0.42), 10); v.r = Math.max(600, 470 + current.height*2.0); v.th = -0.5; v.ph = current.height > 120 ? 1.05 : 0.85;
    highlight();
  }
  plateView = {resize: resize2};
  new ResizeObserver(resize2).observe(st);
  resize2(); show(0);
}
</script>
</body>
</html>
`````

**Fil: `web/lennarts-besoksliggare.html` – demo av besöksliggaren, 2026-10-27**

`````html
<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lennarts besöksliggare</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Special+Elite&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#E9EEE4; --surface:#F5F7F1; --ink:#1E2E25; --ink-2:#4F6155; --line:#C7D1C3;
  --granted:#2B7546; --denied:#B02A22; --focus:#1F5FBF;
  color-scheme: light;
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#131C17; --surface:#1A251F; --ink:#E3EADF; --ink-2:#A3B3A7; --line:#2C3B32;
    --granted:#62C487; --denied:#F07A6E; --focus:#8DB8FF; color-scheme: dark;
  }
}
:root[data-theme="dark"]{
  --paper:#131C17; --surface:#1A251F; --ink:#E3EADF; --ink-2:#A3B3A7; --line:#2C3B32;
  --granted:#62C487; --denied:#F07A6E; --focus:#8DB8FF; color-scheme: dark;
}
*,*::before,*::after{box-sizing:inherit}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"Bricolage Grotesque", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size:1.0625rem; line-height:1.55; -webkit-font-smoothing:antialiased;
}
img{max-width:100%; display:block}
.wrap{max-width:72rem; margin:0 auto; padding:0 clamp(1rem,4vw,2.5rem)}
:focus-visible{outline:3px solid var(--focus); outline-offset:3px; border-radius:4px}

/* Hero */
.hero{display:grid; gap:clamp(1.5rem,4vw,3.5rem); grid-template-columns:1fr; align-items:center; padding:clamp(2rem,6vw,4.5rem) 0 clamp(2rem,5vw,3.5rem)}
@media (min-width:52rem){ .hero{grid-template-columns:1.05fr 1fr} }
h1{font-size:clamp(2.6rem,7vw,4.6rem); line-height:.95; font-weight:800; letter-spacing:-.025em; margin:0 0 1.25rem}
.lead{font-size:clamp(1.15rem,2vw,1.35rem); max-width:34ch; margin:0 0 1.25rem}
.week{color:var(--ink-2); max-width:42ch; margin:0}
.demo{display:inline-block; margin-top:1.5rem; font-size:.9rem; color:var(--ink-2); border:1px dashed var(--line); border-radius:6px; padding:.4rem .7rem}
.hero-photo{position:relative; border-radius:14px; overflow:hidden; aspect-ratio:4/3; background:var(--surface)}
.hero-photo img{width:100%; height:100%; object-fit:cover}

/* Stamps: the one loud thing on the page */
.stamp{
  position:absolute; font-family:"Special Elite", "Courier New", monospace; line-height:1;
  color:var(--c); border:3px solid var(--c); border-radius:6px; padding:.35em .55em .25em;
  transform:rotate(var(--r,-8deg)); background:color-mix(in srgb, var(--surface) 78%, transparent);
  mix-blend-mode:normal; letter-spacing:.04em; pointer-events:none;
  -webkit-mask-image:radial-gradient(circle at 30% 40%, #000 62%, rgba(0,0,0,.72) 100%);
          mask-image:radial-gradient(circle at 30% 40%, #000 62%, rgba(0,0,0,.72) 100%);
}
.stamp.ok{--c:var(--granted)} .stamp.no{--c:var(--denied)}
.hero-photo .stamp{right:1.1rem; bottom:1.1rem; font-size:clamp(1.3rem,3vw,1.9rem); --r:-9deg}
@media (prefers-reduced-motion:no-preference){
  .hero-photo .stamp{animation:thump .5s cubic-bezier(.2,1.6,.4,1) .35s both}
  @keyframes thump{from{transform:rotate(-9deg) scale(1.9); opacity:0} to{transform:rotate(-9deg) scale(1); opacity:1}}
}

/* Filter */
.bar{display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:1rem; border-top:2px solid var(--ink); padding:1rem 0 .5rem}
.bar h2{font-size:1.5rem; margin:0; font-weight:800; letter-spacing:-.01em}
.seg{display:inline-flex; border:1px solid var(--line); border-radius:999px; padding:3px; background:var(--surface)}
.seg button{font:inherit; font-size:.95rem; border:0; background:transparent; color:var(--ink-2); padding:.4rem .9rem; border-radius:999px; cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink); color:var(--paper)}

/* Days and visits */
.day{margin:1.75rem 0 2.5rem}
.day h3{font-size:1.05rem; font-weight:600; color:var(--ink-2); margin:0 0 .9rem}
.grid{display:grid; gap:1.25rem 1.25rem; grid-template-columns:repeat(auto-fill,minmax(min(100%,15.5rem),1fr))}
.visit{all:unset; display:block; cursor:pointer; border-radius:12px}
.visit .ph{position:relative; border-radius:12px; overflow:hidden; aspect-ratio:4/3; background:var(--surface)}
.visit .ph img{width:100%; height:100%; object-fit:cover; transition:transform .25s ease}
.visit:hover .ph img{transform:scale(1.03)}
.visit .stamp{left:.6rem; top:.6rem; font-size:.95rem; --r:-6deg}
.visit .stamp.no{--r:5deg}
.cap{display:flex; justify-content:space-between; gap:.75rem; align-items:baseline; padding:.55rem .15rem 0}
.cap b{font-weight:600}
.cap time{color:var(--ink-2); font-size:.95rem; white-space:nowrap}
.sub{color:var(--ink-2); font-size:.9rem; padding:0 .15rem}
.visit:focus-visible{outline:3px solid var(--focus); outline-offset:4px}
.empty{color:var(--ink-2)}

/* Dialog */
dialog{border:0; padding:0; border-radius:16px; width:min(46rem, calc(100vw - 2rem)); max-height:calc(100dvh - 2rem); background:var(--surface); color:var(--ink); overflow:auto}
dialog::backdrop{background:rgba(10,18,14,.6)}
.d-ph{position:relative}
.d-ph img{width:100%; aspect-ratio:4/3; object-fit:cover}
.d-ph .stamp{right:1rem; bottom:1rem; font-size:1.6rem; --r:-8deg}
.d-body{padding:1.25rem 1.5rem 1.5rem}
.d-body h4{font-size:1.6rem; font-weight:800; margin:0 0 .25rem; letter-spacing:-.01em}
.d-when{color:var(--ink-2); margin:0 0 1rem}
dl{display:grid; grid-template-columns:auto 1fr; gap:.3rem 1.25rem; margin:0 0 1.25rem}
dt{color:var(--ink-2)} dd{margin:0}
.report{border-left:3px solid var(--c); padding:.1rem 0 .1rem 1rem; margin:0}
.report.ok{--c:var(--granted)} .report.no{--c:var(--denied)}
.report small{display:block; color:var(--ink-2); font-size:.85rem; margin-bottom:.3rem}
.close{position:absolute; top:.75rem; right:.75rem; font:inherit; font-size:.95rem; border:0; border-radius:999px; padding:.45rem .9rem; background:var(--surface); color:var(--ink); cursor:pointer}
footer{border-top:1px solid var(--line); color:var(--ink-2); font-size:.9rem; padding:1.5rem 0 2.5rem; margin-top:1rem}
</style>
</head>
<body>
<main class="wrap">
  <section class="hero">
    <div>
      <h1>Lennarts besöksliggare</h1>
      <p class="lead">Varje besök vid matstationen, med bild och klockslag. Ekorrar släpps in. Alla andra får en artig incidentrapport.</p>
      <p class="week" id="week"></p>
      <span class="demo">Demoläge: bilderna är AI-genererade och besöken påhittade.</span>
    </div>
    <figure class="hero-photo" style="margin:0">
      <img id="heroImg" alt="Lennart tittar nyfiket rakt in i kameran">
      <span class="stamp ok" aria-hidden="true">INSLÄPPT</span>
    </figure>
  </section>

  <div class="bar">
    <h2>Besök</h2>
    <div class="seg" role="group" aria-label="Visa besök">
      <button type="button" data-f="all" aria-pressed="true"></button>
      <button type="button" data-f="ok" aria-pressed="false"></button>
      <button type="button" data-f="no" aria-pressed="false"></button>
    </div>
  </div>
  <div id="log"></div>

  <footer>Bilderna tas av kameran i matstationen och sparas i 90 dagar.</footer>
</main>

<dialog id="dlg" aria-labelledby="dName">
  <div class="d-ph"><img id="dImg" alt=""><span class="stamp" id="dStamp" aria-hidden="true"></span>
    <button class="close" type="button" id="dClose">Stäng</button></div>
  <div class="d-body">
    <h4 id="dName"></h4>
    <p class="d-when" id="dWhen"></p>
    <dl id="dFacts"></dl>
    <p class="report" id="dReport"></p>
  </div>
</dialog>

<script>
const VISITS = [{"id": "v12", "img": "00", "when": "2026-10-27T08:14", "who": "Lennart", "kind": "Ekorre", "ok": true, "conf": 97, "weight": "306 g", "nuts": 2, "note": "Åt båda nötterna på plats. Ingen brådska."}, {"id": "v11", "img": "03", "when": "2026-10-27T07:58", "who": "Okänd skata", "kind": "Skata", "ok": false, "conf": 99, "weight": "214 g", "case": 14, "report": "Kl. 07:58 påträffades obehörig individ (skata) vid matstationens yttre perimeter. Individen inspekterade den stängda luckan från flera vinklar. Tillträde nekades. Individen avlägsnade sig efter 41 sekunder. Hotnivå: förhöjd."}, {"id": "v10", "img": "11", "when": "2026-10-26T16:47", "who": "Lennart", "kind": "Ekorre", "ok": true, "conf": 94, "weight": "298 g", "nuts": 1, "note": "Tog nöten med sig. Troligen till ett vinterförråd."}, {"id": "v09", "img": "05", "when": "2026-10-26T13:20", "who": "Grannkatten", "kind": "Katt", "ok": false, "conf": 99, "weight": "4,1 kg", "case": 13, "report": "Kl. 13:20 genomförde en grå tabbykatt en närgången inspektion av kameran. Nosen täckte stora delar av bildfältet i 11 sekunder. Vikten översteg tillåten gräns med god marginal. Tillträde nekades. Hotnivå: hög, men sällskaplig."}, {"id": "v08", "img": "02", "when": "2026-10-26T09:05", "who": "Lennart", "kind": "Ekorre", "ok": true, "conf": 91, "weight": "311 g", "nuts": 2, "note": "Landade i full fart. Godkänd i luften."}, {"id": "v07", "img": "07", "when": "2026-10-25T17:32", "who": "Okänd igelkott", "kind": "Igelkott", "ok": false, "conf": 88, "weight": "ej på vågen", "case": 12, "report": "Kl. 17:32 registrerades en igelkott på uteplatsen nedanför stationen. Individen finns inte på listan men bedöms som uppenbart trevlig. Ingen åtgärd vidtogs. Ärendet avskrivs."}, {"id": "v06", "img": "09", "when": "2026-10-25T10:41", "who": "Okänd ringduva", "kind": "Ringduva", "ok": false, "conf": 98, "weight": "482 g", "case": 11, "report": "Kl. 10:41 intog en ringduva hela plattformen och skymde kameran. Individen visade intresse för matskålen men saknade behörighet. Tillträde nekades. Individen kvarstod i 3 minuter av ren principsak. Hotnivå: måttlig."}, {"id": "v05", "img": "08", "when": "2026-10-24T11:12", "who": "Lennart", "kind": "Ekorre", "ok": true, "conf": 93, "weight": "317 g", "nuts": 2, "note": "Kom trots regnet. Pälsen blöt, aptiten opåverkad."}, {"id": "v04", "img": "04", "when": "2026-10-24T08:03", "who": "Okänd kaja", "kind": "Kaja", "ok": false, "conf": 97, "weight": "231 g", "case": 10, "report": "Kl. 08:03 etablerade en kaja ögonkontakt med kameran. Blicken tolkades som förhandlingsförsök. Tillträde nekades. Hotnivå: förhöjd."}, {"id": "v03", "img": "10", "when": "2026-10-23T14:26", "who": "Okänd koltrast", "kind": "Koltrast", "ok": false, "conf": 96, "weight": "94 g", "case": 9, "report": "Kl. 14:26 rörde sig en koltrast över plattformen i riktning mot matskålen. Luckan förblev stängd. Individen avvek söderut. Hotnivå: låg."}, {"id": "v02", "img": "06", "when": "2026-10-23T09:37", "who": "Okänd talgoxe", "kind": "Talgoxe", "ok": false, "conf": 95, "weight": "18 g", "case": 8, "report": "Kl. 09:37 landade en talgoxe på matskålens kant. Vikten var för låg för att vågen skulle reagera, men kameran registrerade besöket. Tillträde nekades. Hotnivå: försumbar."}, {"id": "v01", "img": "01", "when": "2026-10-22T08:51", "who": "Lennart", "kind": "Ekorre", "ok": true, "conf": 98, "weight": "302 g", "nuts": 1, "note": "Inspekterade kameran personligen innan han åt."}];
const IMAGES = {"00": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 69559 tecken]", "03": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 77283 tecken]", "11": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 89083 tecken]", "05": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 88339 tecken]", "02": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 94423 tecken]", "07": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 62615 tecken]", "09": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 86059 tecken]", "08": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 79471 tecken]", "04": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 85423 tecken]", "10": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 93543 tecken]", "06": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 72071 tecken]", "01": "data:image/jpeg;base64,[BASE64 UTELÄMNAD: 75983 tecken]"};
const days = ["söndag","måndag","tisdag","onsdag","torsdag","fredag","lördag"];
const months = ["januari","februari","mars","april","maj","juni","juli","augusti","september","oktober","november","december"];
const parse = s => { const [d,t] = s.split("T"); const [y,m,da] = d.split("-").map(Number); return {y,m,da,t,date:new Date(y,m-1,da)}; };
const dayLabel = s => { const p = parse(s); const w = days[p.date.getDay()]; return w.charAt(0).toUpperCase()+w.slice(1)+" "+p.da+" "+months[p.m-1]; };
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

const okN = VISITS.filter(v=>v.ok).length, noN = VISITS.length-okN;
const nuts = VISITS.reduce((a,v)=>a+(v.nuts||0),0);
document.getElementById("week").textContent = `Den senaste veckan kom Lennart ${okN} gånger och fick ${nuts} hasselnötter. ${noN} besökare nekades, varav en katt.`;
document.getElementById("heroImg").src = IMAGES["01"];
const btns = document.querySelectorAll(".seg button");
const labels = {all:`Alla (${VISITS.length})`, ok:`Insläppta (${okN})`, no:`Nekade (${noN})`};
btns.forEach(b => { b.textContent = labels[b.dataset.f]; b.addEventListener("click", () => setFilter(b.dataset.f)); });

function setFilter(f){
  btns.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.f===f)));
  try{ sessionStorage.setItem("lennart-filter", f); }catch(e){}
  render(f);
}
function render(f){
  const list = VISITS.filter(v => f==="all" || (f==="ok") === v.ok);
  const log = document.getElementById("log");
  if(!list.length){ log.innerHTML = '<p class="empty">Inga besök att visa.</p>'; return; }
  const groups = [];
  list.forEach(v => { const k = v.when.slice(0,10); let g = groups.find(x=>x.k===k); if(!g){ g={k, items:[]}; groups.push(g);} g.items.push(v); });
  log.innerHTML = groups.map(g => `
    <section class="day"><h3>${dayLabel(g.items[0].when)}</h3><div class="grid">
    ${g.items.map(v => `
      <button class="visit" type="button" data-id="${v.id}" aria-label="${esc(v.who)}, ${parse(v.when).t}, ${v.ok?"insläppt":"nekad"}">
        <div class="ph"><img src="${IMAGES[v.img]}" alt="" loading="lazy"><span class="stamp ${v.ok?"ok":"no"}">${v.ok?"INSLÄPPT":"NEKAD"}</span></div>
        <div class="cap"><b>${esc(v.who)}</b><time datetime="${v.when}">${parse(v.when).t}</time></div>
        <div class="sub">${v.ok ? `${v.nuts} ${v.nuts===1?"nöt":"nötter"}, ${esc(v.weight)}` : `Incidentrapport nr ${v.case}`}</div>
      </button>`).join("")}
    </div></section>`).join("");
  log.querySelectorAll(".visit").forEach(el => el.addEventListener("click", () => open(el.dataset.id)));
}
const dlg = document.getElementById("dlg");
function open(id){
  const v = VISITS.find(x=>x.id===id); if(!v) return;
  document.getElementById("dImg").src = IMAGES[v.img];
  document.getElementById("dImg").alt = `Kamerabild av ${v.kind.toLowerCase()} vid matstationen`;
  const st = document.getElementById("dStamp"); st.className = "stamp "+(v.ok?"ok":"no"); st.textContent = v.ok?"INSLÄPPT":"NEKAD";
  document.getElementById("dName").textContent = v.who;
  document.getElementById("dWhen").textContent = `${dayLabel(v.when)}, kl. ${parse(v.when).t}`;
  const facts = [["Art", v.kind], ["AI:ns säkerhet", v.conf+" %"], ["Vikt på vågen", v.weight]];
  facts.push(v.ok ? ["Utdelat", `${v.nuts} ${v.nuts===1?"hasselnöt":"hasselnötter"}`] : ["Ärende", "Incidentrapport nr "+v.case]);
  document.getElementById("dFacts").innerHTML = facts.map(([k,val]) => `<dt>${k}</dt><dd>${esc(val)}</dd>`).join("");
  const r = document.getElementById("dReport"); r.className = "report "+(v.ok?"ok":"no");
  r.innerHTML = v.ok ? `<small>Anteckning</small>${esc(v.note)}` : `<small>Incidentrapport nr ${v.case}</small>${esc(v.report)}`;
  dlg.showModal();
}
document.getElementById("dClose").addEventListener("click", () => dlg.close());
dlg.addEventListener("click", e => { if(e.target === dlg) dlg.close(); });

let start = "all";
try{ start = sessionStorage.getItem("lennart-filter") || "all"; }catch(e){}
setFilter(["all","ok","no"].includes(start) ? start : "all");
</script>
</body>
</html>
`````

**Fil: `web/lennarts-minihus.html` – minihusen, 2026-10-28**

`````html
<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lennarts minihus</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&display=swap" rel="stylesheet">
<style>
:root{--paper:#E9EEE4;--surface:#F5F7F1;--ink:#1E2E25;--ink-2:#4F6155;--line:#C7D1C3;--accent:#A23A2C;--focus:#1F5FBF;--stage:#DCE3D7;
  color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#131C17;--surface:#1A251F;--ink:#E3EADF;--ink-2:#A3B3A7;--line:#2C3B32;--accent:#E07A6B;--focus:#8DB8FF;--stage:#1E2A23;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#131C17;--surface:#1A251F;--ink:#E3EADF;--ink-2:#A3B3A7;--line:#2C3B32;--accent:#E07A6B;--focus:#8DB8FF;--stage:#1E2A23;color-scheme:dark}
*,*::before,*::after{box-sizing:inherit}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Bricolage Grotesque",system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.5}
.wrap{max-width:72rem;margin:0 auto;padding:clamp(1rem,3vw,2rem)}
h1{font-size:clamp(1.9rem,4.5vw,2.8rem);line-height:1;font-weight:800;letter-spacing:-.02em;margin:.5rem 0 .5rem}
.lead{color:var(--ink-2);max-width:62ch;margin:0 0 1.25rem}
.tabs{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1rem}
.tabs button{font:inherit;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.5rem 1rem;cursor:pointer}
.tabs button[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.layout{display:grid;gap:1.25rem;grid-template-columns:1fr}
@media (min-width:58rem){.layout{grid-template-columns:1fr 20rem}}
.stage{position:relative;background:var(--stage);border-radius:14px;overflow:hidden;aspect-ratio:4/3;min-height:20rem;touch-action:none}
.stage canvas{display:block;width:100%;height:100%;cursor:grab}
.hint{position:absolute;left:.8rem;bottom:.6rem;font-size:.85rem;color:var(--ink-2);pointer-events:none}
.coinlabel{position:absolute;right:.8rem;top:.7rem;font-size:.85rem;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:.25rem .7rem;pointer-events:none}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1.1rem 1.2rem}
.card h2{font-size:1.4rem;font-weight:800;margin:0 0 .2rem}
.time{font-size:2.2rem;font-weight:800;letter-spacing:-.02em;margin:.6rem 0 0}
.time small{display:block;font-size:.9rem;font-weight:400;color:var(--ink-2);letter-spacing:0}
dl{display:grid;grid-template-columns:auto 1fr;gap:.3rem 1rem;margin:1rem 0 0}
dt{color:var(--ink-2)} dd{margin:0}
.sw{display:inline-block;width:.85rem;height:.85rem;border-radius:3px;border:1px solid var(--line);vertical-align:-.1rem;margin-right:.25rem}
.desc{color:var(--ink-2);margin:.6rem 0 0}
.files{font-size:.85rem;color:var(--ink-2);margin:.8rem 0 0;word-break:break-all}
.note{color:var(--ink-2);font-size:.9rem;margin:1.25rem 0 0;max-width:70ch}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
</style>
</head>
<body>
<main class="wrap">
  <h1>Lennarts minihus</h1>
  <p class="lead">Tre miniatyrer av matstationen, cirka 5 cm höga, för en första provutskrift på X2D:n. Bredvid huset ligger en vanlig blyertspenna, så du ser storleken.</p>
  <div class="tabs" role="group" aria-label="Välj version" id="tabs"></div>
  <div class="layout">
    <div class="stage" id="stage"><span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span>
      <span class="coinlabel">Bredvid ligger en vanlig blyertspenna, ca 18 cm, för skala</span></div>
    <aside class="card" aria-live="polite" id="info"></aside>
  </div>
  <p class="note">Tiderna är uppskattningar för PLA med 0,20 mm lagerhöjd, med ASA som jämförelse. Flerfärgsutskrifter tar lång tid i liten skala eftersom skrivaren byter färg på nästan varje lager. Bambu Studio visar den exakta tiden när du laddar filerna.</p>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const DATA = {"1": {"name": "Detaljerad", "meshes": [{"color": "#EEEBE3", "file": "mini_1_detaljerad_hus_vit.stl", "job": "hus", "pos": "[BASE64 UTELÄMNAD: 8386 tecken]", "idx": "[BASE64 UTELÄMNAD: 15874 tecken]", "vol": 918.4, "wt": true}, {"color": "#5A5E62", "file": "mini_1_detaljerad_tak_gra.stl", "job": "tak", "pos": "[BASE64 UTELÄMNAD: 28082 tecken]", "idx": "[BASE64 UTELÄMNAD: 56162 tecken]", "vol": 3124.7, "wt": true}, {"color": "#A23A2C", "file": "mini_1_detaljerad_hus_rod.stl", "job": "hus", "pos": "[BASE64 UTELÄMNAD: 24050 tecken]", "idx": "[BASE64 UTELÄMNAD: 48098 tecken]", "vol": 22130.9, "wt": true}, {"color": "#3B6A2B", "file": "mini_1_detaljerad_hus_gron.stl", "job": "hus", "pos": "[BASE64 UTELÄMNAD: 7186 tecken]", "idx": "[BASE64 UTELÄMNAD: 14178 tecken]", "vol": 10315.7, "wt": true}, {"color": "#EEEBE3", "file": "mini_1_detaljerad_tak_vit.stl", "job": "tak", "pos": "DRSXwXG0h8DqNNNBDRSXwXwCacDqNNNBDRSXwXG0h8Chj+tBDRSXwXwCacChj+tBDRSXQXG0h8DqNNNBDRSXQXwCacDqNNNBDRSXQXG0h8Chj+tBDRSXQXwCacChj+tBAAAAAHG0h8D0sjBCAAAAAHwCacD0sjBCAAAAAHG0h8DzUD5CAAAAAHwCacDzUD5CDRSXwQLG5UHqNNNBDRSXwc6S6kHqNNNBDRSXwQLG5UGhj+tBDRSXwc6S6kGhj+tBDRSXQQLG5UHqNNNBDRSXQc6S6kHqNNNBDRSXQQLG5UGhj+tBDRSXQc6S6kGhj+tBAAAAAALG5UH0sjBCAAAAAM6S6kH0sjBCAAAAAALG5UHzUD5CAAAAAM6S6kHzUD5C", "idx": "AAAAAAIAAAABAAAAAQAAAAIAAAADAAAAAAAAAAEAAAAJAAAAAAAAAAgAAAACAAAAAQAAAAMAAAAJAAAAAgAAAAoAAAADAAAAAAAAAAkAAAAIAAAAAgAAAAgAAAAKAAAAAwAAAAsAAAAJAAAAAwAAAAoAAAALAAAABAAAAAUAAAAHAAAABAAAAAcAAAAGAAAABAAAAAgAAAAFAAAABAAAAAYAAAAIAAAABQAAAAkAAAAHAAAABgAAAAcAAAALAAAABQAAAAgAAAAJAAAABgAAAAoAAAAIAAAABwAAAAkAAAALAAAABgAAAAsAAAAKAAAADAAAAA4AAAANAAAADQAAAA4AAAAPAAAADAAAAA0AAAAVAAAADAAAABQAAAAOAAAADQAAAA8AAAAVAAAADgAAABYAAAAPAAAADAAAABUAAAAUAAAADgAAABQAAAAWAAAADwAAABcAAAAVAAAADwAAABYAAAAXAAAAEAAAABEAAAATAAAAEAAAABMAAAASAAAAEAAAABQAAAARAAAAEAAAABIAAAAUAAAAEQAAABUAAAATAAAAEgAAABMAAAAXAAAAEQAAABQAAAAVAAAAEgAAABYAAAAUAAAAEwAAABUAAAAXAAAAEgAAABcAAAAWAAAA", "vol": 146.1, "wt": true}], "size": [37.8, 56.4, 50.0], "hours": 3.5, "hours_pla": 3.03, "jobs": {"hus": 2.22, "tak": 0.82}, "colors": 4, "files": ["mini_1_detaljerad_hus_gron.stl", "mini_1_detaljerad_hus_rod.stl", "mini_1_detaljerad_hus_vit.stl", "mini_1_detaljerad_tak_h_gra.stl", "mini_1_detaljerad_tak_h_vit.stl", "mini_1_detaljerad_tak_v_gra.stl", "mini_1_detaljerad_tak_v_vit.stl"]}, "2": {"name": "Vinter", "meshes": [{"color": "#EEEBE3", "file": "mini_2_vinter_vit.stl", "job": "hus", "pos": "[BASE64 UTELÄMNAD: 32802 tecken]", "idx": "[BASE64 UTELÄMNAD: 65154 tecken]", "vol": 14445.3, "wt": true}, {"color": "#A23A2C", "file": "mini_2_vinter_rod.stl", "job": "hus", "pos": "[BASE64 UTELÄMNAD: 14786 tecken]", "idx": "[BASE64 UTELÄMNAD: 29762 tecken]", "vol": 21977.9, "wt": true}], "size": [37.8, 56.4, 50.0], "hours": 2.97, "hours_pla": 2.56, "jobs": {"hus": 2.56}, "colors": 2, "files": ["mini_2_vinter_rod.stl", "mini_2_vinter_vit.stl"]}, "3": {"name": "Enf\u00e4rgad", "meshes": [{"color": "#E9E4D8", "file": "mini_3_enfargad.stl", "job": "hus", "pos": "[BASE64 UTELÄMNAD: 38802 tecken]", "idx": "[BASE64 UTELÄMNAD: 80610 tecken]", "vol": 36433.4, "wt": true}], "size": [37.8, 56.4, 50.0], "hours": 1.04, "hours_pla": 0.69, "jobs": {"hus": 0.69}, "colors": 1, "files": ["mini_3_enfargad.stl"]}};
const DESC = {
  1:"Nära originalet: panel, takpannor, blomlådor med blommor, stenplattor och grästuvor. Taket skrivs ut separat i två platta halvor och sätts på med fyra styrtappar, så huset bara behöver rött, vitt och grönt.",
  2:"Snötäckt tak med pannor och snötäckt tomt i vitt, huset i rött. Fönster och skärm som fördjupningar. Två färger, en i varje munstycke, så inga AMS-byten.",
  3:"Samma former, med panel och takpannor, i en enda färg. Snabbast och bäst som första test av skrivaren."};
const CNAME = {"#A23A2C":"röd","#EEEBE3":"vit","#5A5E62":"grå","#3B6A2B":"grön","#E9E4D8":"valfri"};
const stage = document.getElementById("stage");
const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2)); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
stage.prepend(renderer.domElement);
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(30,1,0.5,2000);
scene.add(new THREE.HemisphereLight(0xEEF3FF, 0x6E6A60, 0.5));
const sun = new THREE.DirectionalLight(0xFFF1DC, 1.0); sun.position.set(-60,110,80); sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048); const sc = sun.shadow.camera; sc.left=-120; sc.right=120; sc.top=120; sc.bottom=-120; sc.near=1; sc.far=400; sun.shadow.bias=-0.0005;
scene.add(sun);
const fill = new THREE.DirectionalLight(0xDDE6FF, 0.3); fill.position.set(80,40,-60); scene.add(fill);
const root = new THREE.Group(); root.rotation.x = -Math.PI/2; scene.add(root);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(600,600), new THREE.ShadowMaterial({opacity:.2})); ground.receiveShadow = true; root.add(ground);
// vanlig blyertspenna för skala (ca 18 cm, sexkantig Ø 7 mm) – bara i förhandsgranskningen
const pencil = new THREE.Group(); root.add(pencil);
const R6 = 3.6;                                                       // sexkantens yttre radie
const paint = (()=>{ const c=document.createElement("canvas"); c.width=1024; c.height=96; const g=c.getContext("2d");
  g.fillStyle="#F2BE22"; g.fillRect(0,0,1024,96);
  for(let i=0;i<6;i++){ g.fillStyle = i%2 ? "rgba(255,255,255,.10)" : "rgba(120,80,0,.10)"; g.fillRect(i*1024/6,0,1024/6,96); }   // lätt olika ton per sida
  g.fillStyle="#1F3B2D"; g.font="bold 40px Arial, sans-serif"; g.textBaseline="middle";
  g.save(); g.translate(0,48); g.fillText("LENNART  ·  HB  ·  2", 30, 0); g.restore();
  return new THREE.CanvasTexture(c); })();
paint.wrapS = paint.wrapT = THREE.ClampToEdgeWrapping;
function part(geo, mat, y){ const m=new THREE.Mesh(geo, mat); m.position.y=y; m.castShadow=true; m.receiveShadow=true; pencil.add(m); return m; }
const BODY = 145;
// målad kropp: texten ligger längs pennan på en av de sex sidorna
const bodyGeo = new THREE.CylinderGeometry(R6, R6, BODY, 6, 1, true);
const uv = bodyGeo.attributes.uv; for(let i=0;i<uv.count;i++){ const u=uv.getX(i), v=uv.getY(i); uv.setXY(i, v, u); } // texten längs pennan
part(bodyGeo, new THREE.MeshStandardMaterial({map:paint, roughness:.35, metalness:.05, flatShading:true}), 0);
part(new THREE.CircleGeometry(R6, 6).rotateX(-Math.PI/2), new THREE.MeshStandardMaterial({color:"#E8C493"}), -BODY/2).rotation.y = 0;
// vässad ände: trä, sedan grafit
part(new THREE.CylinderGeometry(1.05, R6*0.96, 19, 24), new THREE.MeshStandardMaterial({color:"#E3BF8E", roughness:.85}), -BODY/2 - 9.5).rotation.x = Math.PI;
part(new THREE.ConeGeometry(1.05, 4.2, 20), new THREE.MeshStandardMaterial({color:"#2E2F33", roughness:.35, metalness:.45}), -BODY/2 - 19 - 2.1).rotation.x = Math.PI;
// vågig målarkant där vässningen börjar
for(let k=0;k<6;k++){ const sc=new THREE.Mesh(new THREE.SphereGeometry(1.6, 12, 8), new THREE.MeshStandardMaterial({color:"#F2BE22", roughness:.35}));
  const a=k*Math.PI/3; sc.scale.set(1,1.4,.35); sc.position.set(Math.cos(a)*R6*0.86, -BODY/2-0.6, Math.sin(a)*R6*0.86); sc.lookAt(0, -BODY/2-0.6, 0); pencil.add(sc); }
// metallhylsa med räfflor och radiergummi
const metal = new THREE.MeshStandardMaterial({color:"#D9D7D0", metalness:.45, roughness:.32});
part(new THREE.CylinderGeometry(3.75, 3.75, 9, 40), metal, BODY/2 + 4.5);
for(const y of [1.4, 3.2, 5.8, 7.6]){ const r=new THREE.Mesh(new THREE.TorusGeometry(3.78, 0.32, 8, 40), metal); r.rotation.x=Math.PI/2; r.position.y=BODY/2+y; pencil.add(r); }
part(new THREE.CylinderGeometry(3.45, 3.5, 6, 40), new THREE.MeshStandardMaterial({color:"#E8919A", roughness:.9}), BODY/2 + 12);
const cap = part(new THREE.SphereGeometry(3.45, 32, 16, 0, Math.PI*2, 0, Math.PI/2), new THREE.MeshStandardMaterial({color:"#E8919A", roughness:.9}), BODY/2 + 15); cap.scale.y = .35;
pencil.rotation.order = 'ZYX'; pencil.rotation.y = Math.PI/6;                                         // vilar på en platt sida
pencil.position.set(30, -48, R6*Math.cos(Math.PI/6));
pencil.rotation.z = -0.9;                                              // ligger snett framför huset
function b64(s,T){ const bin=atob(s); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return new T(u.buffer); }
const groups = {};
Object.entries(DATA).forEach(([lvl,d]) => {
  const g = new THREE.Group(); g.visible = false; root.add(g); groups[lvl] = g;
  d.meshes.forEach(m => {
    let geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(b64(m.pos, Float32Array),3));
    geo.setIndex(new THREE.BufferAttribute(b64(m.idx, Uint32Array),1));
    geo = geo.toNonIndexed(); geo.computeVertexNormals();
    const mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color:m.color, roughness:.8}));
    mesh.castShadow = true; mesh.receiveShadow = true; g.add(mesh);
  });
});
const TARGET = new THREE.Vector3(24, 10, 42); const view = {th:-0.45, ph:1.05, r:360};
function place(){ cam.position.set(TARGET.x+view.r*Math.sin(view.ph)*Math.sin(view.th), TARGET.y+view.r*Math.cos(view.ph), TARGET.z+view.r*Math.sin(view.ph)*Math.cos(view.th)); cam.lookAt(TARGET); }
function draw(){ place(); renderer.render(scene, cam); }
const ptrs = new Map(); let pinch0 = 0, mid0 = null, panMode = false;
function pan(dx, dy){                                   // flytta vyn i skärmens plan
  const right = new THREE.Vector3(), upv = new THREE.Vector3();
  cam.updateMatrixWorld(); right.setFromMatrixColumn(cam.matrixWorld, 0); upv.setFromMatrixColumn(cam.matrixWorld, 1);
  const k = view.r * 0.0011; TARGET.addScaledVector(right, -dx * k).addScaledVector(upv, dy * k);
}
renderer.domElement.addEventListener("contextmenu", e => e.preventDefault());
renderer.domElement.addEventListener("mousedown", e => { if(e.button === 1) e.preventDefault(); });   // stoppa webbläsarens autoskroll på scrollknappen
renderer.domElement.addEventListener("pointerdown", e => {
  renderer.domElement.setPointerCapture(e.pointerId); ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});
  panMode = e.button === 2 || e.button === 1 || e.shiftKey;
  if(ptrs.size===2){ const [a,b]=[...ptrs.values()]; pinch0=Math.hypot(a.x-b.x,a.y-b.y); mid0={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; }
});
renderer.domElement.addEventListener("pointermove", e => {
  if(!ptrs.has(e.pointerId)) return; const p = ptrs.get(e.pointerId); const dx=e.clientX-p.x, dy=e.clientY-p.y; ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(ptrs.size===1){ if(panMode) pan(dx, dy); else { view.th -= dx*0.008; view.ph = Math.min(Math.PI/2-0.03, Math.max(0.15, view.ph - dy*0.008)); } }
  else if(ptrs.size===2){ const [a,b]=[...ptrs.values()]; const d=Math.hypot(a.x-b.x,a.y-b.y), mid={x:(a.x+b.x)/2,y:(a.y+b.y)/2};
    if(pinch0) view.r=Math.min(500,Math.max(30,view.r*pinch0/d)); if(mid0) pan(mid.x-mid0.x, mid.y-mid0.y); pinch0=d; mid0=mid; }
  draw(); });
const up = e => { ptrs.delete(e.pointerId); pinch0=0; mid0=null; };
renderer.domElement.addEventListener("pointerup", up); renderer.domElement.addEventListener("pointercancel", up);
renderer.domElement.addEventListener("wheel", e => { e.preventDefault(); view.r = Math.min(500, Math.max(30, view.r*(1+e.deltaY*0.001))); draw(); }, {passive:false});
const fmt = h => h < 0.95 ? `ca ${Math.round(h*6)*10} min` : `ca ${String(Math.round(h*2)/2).replace(".",",")} h`;
const tabs = document.getElementById("tabs"), info = document.getElementById("info");
function show(lvl){
  Object.entries(groups).forEach(([k,g]) => g.visible = (k===String(lvl)));
  tabs.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.l===String(lvl))));
  const d = DATA[lvl];
  const sw = [...new Set(d.meshes.map(m=>m.color))].map(c => `<span class="sw" style="background:${c}"></span>${CNAME[c]||""}`).join(" &nbsp;");
  info.innerHTML = `<h2>${d.name}</h2><p class="desc">${DESC[lvl]}</p>
    <p class="time">${fmt(d.hours_pla)}<small>uppskattad tid i PLA${d.jobs.tak ? ` (huset ${fmt(d.jobs.hus)} + taket ${fmt(d.jobs.tak)})` : ""}, i ASA ${fmt(d.hours)}</small></p>
    <dl><dt>Mått</dt><dd>${d.size.map(v=>String(v).replace(".",",")).join(" × ")} mm</dd><dt>Färger</dt><dd>${sw}</dd><dt>Filer</dt><dd>${d.files.length}</dd></dl>
    <p class="files">${d.files.join("<br>")}</p>`;
  draw();
}
Object.entries(DATA).forEach(([lvl,d]) => { const b=document.createElement("button"); b.type="button"; b.dataset.l=lvl; b.textContent=`${lvl}. ${d.name}`; b.addEventListener("click",()=>show(lvl)); tabs.appendChild(b); });
function resize(){ const w=stage.clientWidth,h=stage.clientHeight; renderer.setSize(w,h,false); cam.aspect=w/h; cam.updateProjectionMatrix(); draw(); }
new ResizeObserver(resize).observe(stage); resize(); show(1);
</script>
</body>
</html>
`````


### 4.6 Data och filer som inte är kod

Filer som levererades till Marcus. Publicerade sidor är privata tills Marcus delar dem.

| Fil eller länk | Innehåll |
|---|---|
| `lennarts-matstation-3d.html`, publicerad på https://claude.ai/artifact/9LQD4NfnbhvxCEfwnb7qiV | Förhandsgranskningen med 3D, demo, projektdokument, 3D-filer och utskrift. Innehåller hela aktuella modellen (`parts_v11.json`), plattorna och alla STL-filer inbäddade. |
| `lennarts-matstation-3d.zip` | Alla 57 STL-filer i aktuell version |
| `kroppen-rod-och-gra.zip` | Ny kropp: `05_kropp_rod.stl` och `05_kropp_sockel_gra.stl` |
| `kamerafaste-och-skarmfaste.zip` | `15_kamerafaste.stl`, `19_skarmklamma.stl` och `18_skarmram_svart.stl` |
| `elektroniklada-lock-monteringsplatta.zip` | `16_elektroniklada.stl`, `16b_elektroniklada_lock.stl` och `24_monteringsplatta.stl` |
| `toleranstest.stl` (samma som `platta-4-toleranstest.stl`), `platta-4-basen.stl`, `platta-7-bottenplatta.stl` | Enskilda plattor |
| `platta-13-kroppen.zip` | Kroppen version 7 i tre färger, den som skrevs ut 2026-11-13 |
| `lennarts-matstation-trailer.zip` | `lennarts-matstation.glb` (version 7, 48 delar, meter, vridpunkter för lucka och hjul), `delar.json`, `README.md`, dekaler och skärmbilder som PNG |
| `lennarts-besoksliggare.html`, https://claude.ai/artifact/3Pf1zaveQGaKdFKwVuLrTc | Demo av den publika besöksliggaren med 12 AI-genererade bilder |
| `lennarts-minihus.html`, https://claude.ai/artifact/N2Fr5AUTLH34VUrGafmF3t, och `lennarts-miniatyrer.zip` | Minihusen, 5 cm höga |
| Projektdokumentet i Claude Docs, https://claude.ai/artifact/DsUhQhTLndz1BhiCxTa6bE | Beslut, inköpslista, utskrift, montering, service och öppna frågor. Delvis inaktuellt: det säger ASA och har gamla plattnummer. |

Det här skriptet skrevs till handoffen och provades: det återskapar `parts_v11.json` exakt ur förhandsgranskningen. Det plockar ut modellen, plattorna och STL-filerna ur HTML-filen, så att skripten i avsnitt 4.3–4.4 kan köras igen. Döp om `parts_from_html.json` till `parts_v11.json` för att fortsätta därifrån.

**Fil: `tools/extract_from_html.py`**

`````python
# Nytt i handoffen 2026-11-15: plockar ut data ur den publicerade förhandsgranskningen
# (lennarts-matstation-3d.html) så att skripten i avsnitt 4 kan köras igen.
# Användning: python3 extract_from_html.py lennarts-matstation-3d.html
import sys, re, json, base64, io, zipfile, os
src = sys.argv[1] if len(sys.argv) > 1 else 'lennarts-matstation-3d.html'
s = open(src, encoding='utf-8').read()
# delarna (samma format som parts_v*.json): namn, grupp, färg, fil och triangelnät i base64
i = s.index('const PARTS = ') + len('const PARTS = '); j = s.index(';\n', i)
parts = json.loads(s[i:j]); json.dump(parts, open('parts_from_html.json', 'w'))
# plattorna i fliken Utskrift
a = s.index('<script id="platedata" type="application/json">') + len('<script id="platedata" type="application/json">'); b = s.index('</script>', a)
open('plates_from_html.json', 'w').write(s[a:b])
# alla STL-filer
a = s.index('<script id="zipdata" type="application/octet-stream">') + len('<script id="zipdata" type="application/octet-stream">'); b = s.index('</script>', a)
z = zipfile.ZipFile(io.BytesIO(base64.b64decode(s[a:b]))); os.makedirs('stl', exist_ok=True); z.extractall('stl')
print(len(parts), 'delar,', len(z.namelist()), 'STL-filer')
`````

`disp.json`, som `checks8.py` behöver, innehåller ordagrant:

`````json
{"YC": 57.0, "ZC": 64.3, "DUMP": 130.0302592718897, "ZT": 98.7, "R": 31.0, "PD": 21.5}
`````

`parts_v8.json` (version 7 med inbyggda vita detaljer) finns inte inbäddad längre. Den finns som delarna i `lennarts-matstation.glb` i trailerpaketet, och som STL i `platta-13-kroppen.zip`. Att återskapa `parts_v8.json` exakt ur dem är [osäkert].

---

## 5. Det som återstår och öppna frågor

### Nästa steg i utskriften

1. **Toleranstestet:** värdera insatserna M3 och M4, tapparna Ø2,8 och Ø2,4, nockkilen, nötmallen och magnetfickan när magneter finns. Justera vid behov kroppens tappar och klackar innan den nya kroppen skrivs ut.
2. **Den nya kroppen** i rött och grått, cirka 10–13 timmar enligt min osäkra uppskattning. Sedan de nio vita detaljerna på en egen platta.
3. **Elektroniktest i den gamla kroppen:** kamerafäste, skärmklämma och skärmram, med Pi 5, kameran och skärmen.
4. **Mätning:** mät servot på 11 kg med sitt runda horn, mikroservot, skärmkortet, LED-ringen och kameran. Justera sedan fästena.
5. **Doseringen** (doserhus, hjul och magasin) när servot är uppmätt. Provkör med riktiga hasselnötter, gärna 200 varv. Det är bygget viktigaste prov.
6. **Resten av plattorna** enligt fliken Utskrift: tak, gräsmattor, framgård, skål, lucka, blomlådor, stuprör och TPU-packningar.

### Programvara, inte påbörjad

- **Igenkänning:** ekorre eller annat djur, 2–3 bilder per besök, hög tröskel och läget VERIFIERAR vid osäkert svar. Att det sker i molnet bestämdes tidigt, men tjänst och modell är [osäkert].
- **Svarstid:** ungefär 5 sekunder från landning till svar.
- **Servostyrning via PCA9685:** hjulet vrids 130° och tillbaka. Ett litet "vick" fram och tillbaka före utmatningen. Kort tidsgräns, backa och försök igen, och varning efter flera misslyckade försök, så att servot inte står och tar i.
- **Luckan** stängs långsamt och bara när kameran inte har sett rörelse på några sekunder, så att Lennart inte kläms.
- **Skärmen:** väntar, VERIFIERAR, ACCESS GRANTED, ACCESS DENIED och tomt magasin.
- **Besökslogg** med bild och tid, incidentrapport vid nekat besök och en dashboard i säkerhetscentralstil som stannar i hemnätet.
- **Publik besöksliggare och domän.** Förslag: notkontrollen.se (Marcus favorit), lennart.security, besoksliggaren.se, ekorrvakten.se och accessgranted.nu. Om de är lediga och vad de kostar är [osäkert]. Publicera bara bilder som klassats som djur. GDPR behöver stämmas av med någon som kan reglerna, eftersom det är en juridisk fråga.
- **Uppstart och drift:** programmet ska starta av sig självt efter strömavbrott (systemd), och Pi:n ska vara på dygnet runt.

### Öppna frågor

- Vilket nät går SIM-kortet på, och stöder modemet de LTE-banden?
- Passar kamerakabeln från Electrokit Pi 5:s smala kontakt?
- Vad är pedestalen gjord av, och hur ska den fästas i väggen?
- Räcker ljuset för kameran på novembermorgnar? LED-ringen är köpt men inte inritad.
- Ska resten av huset vara PETG eller ASA? Plattorna i förhandsgranskningen är märkta ASA. PETG tål sol och värme sämre över tid.
- Hur sitter kamerakragen, som saknar tappar och bara har en tät ficka? Fönsterramarnas tappar sitter bara upptill, och blomlådorna hänger på fönsterbrädan.
- Skjuver servot faktiskt av en nöt som fastnat? Kraften vid hjulets kant är beräknad till cirka 35 N, men det är inte provat.
- Kommer Lennart att klättra i repstegen? Inte provat.
- Kompletteringar till inköpslistan: M2-skruvar till kameran, PCA9685, 12 V-adapter och kabel, 4G-modem, magneter, ventilationspluggar, glas och plast, silikon, tejp, vinkeljärn och hasselnötter.
- Projektdokumentet i Claude Docs behöver uppdateras med PETG, de nya plattnumren, Electrokit-köpet och den nya kroppen.
- Vid flerfärgsutskrifter: gör rensningstornet bredare så att det inte välter.
- Tävlingen: bidraget ska vara inlämnat senast 30 november 2026. Underlag för tokens och AI-historik ska kunna visas om bidraget hamnar bland de tre med flest röster, senast 15 december kl. 23.59.

---

## 6. Tidslinje

### Före tävlingen (före 16 oktober 2026)

- **Sedan början av sommaren 2026:** ekorren Lennart besöker Marcus uteplats nästan dagligen, och fåglar stjäl hans mat.
- **Marcus ägde redan:** Raspberry Pi 5, lödpenna och spetssats för gänginsatser.
- **Fanns också:** Ruthex-insatser och elmaterial. När de skaffades är [osäkert].
- **Ett separat mobilspel** med ekorren Lennart och en slangbella fanns som sidoprojekt i augusti 2026. Det har inte använts i det här bygget.

Inget av den här chattens arbete gjordes före 16 oktober. Chattens första meddelande är daterat 2026-10-27 kl. 00.06.

### Under tävlingen

Tider är svensk tid. Datum och tider för 2026-10-27–11-11 kommer från transkriptens tidsstämplar. För 2026-11-13–15 kommer de från skärmdumparnas filnamn.

**2026-10-27**

- **Natten mot 27 oktober, från kl. 00.06:** kravlistan och ett projektdokument i Claude Docs. En demo av besöksliggaren med 12 bilder genererade via Higgsfield med modellen GPT Image 2.5.
- **07.52–08.06:** promptar till en bild-AI för konceptskisser i fyra omgångar. Marcus genererade bilderna själv. Med vilket verktyg är [osäkert].
- **14.18–17.00:** 3D-modellen byggs i kod med en interaktiv förhandsgranskning. Uteplatsen, pedestalen, repstegen, gräset, belysningen och lucka-demon kommer till.
- **21.48–22.41:** förbättringsrundor. Vågen stryks, blomlådor och stuprör läggs till, modellen görs utskrivbar och demon får ljus och skuggor.
- **23.49:** frågan om modellen är redo för utskrift och vad som återstår.

**2026-10-28**

- Monteringsförbättringar och val av ASA och grönt filament.
- Frågor om tävlingen och AI-användningen.
- Tre större blommor per blomlåda.
- 16.15–17.08: minihus i tre versioner för en testutskrift.

**2026-10-29 till 2026-11-10**

Ingen aktivitet i den här chatten. Om projektet bearbetades i andra chattar är [osäkert].

**2026-11-11**

- **13.59–20.20:**
  - Inköpslista, vädertätning och beslutet om 4G.
  - Avtagbart tak och blomlådor utan lim.
  - Flikar i förhandsgranskningen, budget på 4 000 kr och snäppfästen.
  - Fliken Utskrift och en genomgång av hela projektet.
- **Kväll, efter kl. 21.22:**
  - Doseringen byggs om till ett hjul, stengrunden och överstyckena läggs till.
  - Demon får röntgenvy, lyftbart tak och monteringsvisning, och fliken Utskrift görs om.
  - Electrokit-ordern, och tre dörrförslag som provas.

**2026-11-12**

- Dörrförslagen tas bort. Panelen görs om och 3D-vyn blir högre. Demon får scener som spelas upp, och monteringen spelas upp av sig själv.
- Lennart som klisterdekal i en hand, sedan en mer realistisk hand, huvudet i skålen och skatan som dekal. Vilka av dessa som gjordes 12 respektive 13 november är [osäkert].

**2026-11-13**

- Fingret som klippte in i dekalen åtgärdas.
- **18.28–18.46:** kroppen förbereds i Bambu Studio. Byte till PETG, filamentgruppering, stödvarningar och test med stöd.
- **Kvällen:** utskriften startas utan stöd. Separata vita detaljer ritas men återställs.

**2026-11-14**

- **00.48:** foto av första lagren. Natten: dörröverstycket hänger fritt, och utskriften får gå vidare.
- **15.38:** rensningstornet har vält vid 89 %. Det tas bort och utskriften fortsätter. Klar cirka 17.51 enligt appen.
- GLB-paketet för trailern. Tid: [osäkert].
- **18.53–18.55:** elektroniklådan förbereds och skrivs ut.
- Utskriftsfliken får avbockning av utskrivna plattor.
- **22.58:** basen förbereds i grön PETG och skrivs ut över natten.

**2026-11-15**

- Bottenplattan skrivs ut.
- Beslut om ny kropp i rött och grått och nöthål på 31 mm.
- **17.28:** spåren vid kameraringen upptäcks och åtgärdas.
- Största nötstorlek, valnötter, toleranstestet, kamerafäste och skärmklämma, och den här handoffen.

---

## 7. Tokens

**Att redovisa:**

- **Molnet:** cirka 60–120 miljoner tokens in och 1–2 miljoner tokens ut [osäkert].
- **Lokalt:** 0.

Allt kördes i claude.ai, alltså i molnet. claude.ai visar ingen tokenräknare, så siffrorna är uppskattningar.

**Så har jag räknat:**

1. **Unikt innehåll i chatten.** Jag räknade text, kod och verktygsresultat i de två sparade transkripten:
   - Transkript 1: cirka 1,16 miljoner tecken, 125 verktygsanrop och 38 bilder.
   - Transkript 2: cirka 1,15 miljoner tecken, 364 verktygsanrop och 71 bilder.
   - Transkripten lagrar verktygsresultat två gånger, så jag halverade: cirka 1,15 miljoner tecken.
   - Med cirka 3,5 tecken per token blir det cirka 330 000 tokens. 109 bilder på cirka 1 500 tokens var ger cirka 165 000.
   - Den här sessionen, 11–15 november, finns inte som transkript. Jag uppskattar den till cirka 800 000 tecken, alltså cirka 230 000 tokens, plus cirka 65 bilder, alltså cirka 100 000 tokens [osäkert].
   - Summa: cirka 0,8 miljoner tokens unikt innehåll (0,6–1,2 miljoner).
2. **Det som faktiskt bearbetades i molnet.** Varje gång modellen svarar eller anropar ett verktyg läser den om hela kontexten:
   - Det har skett cirka 860 gånger: 141 och 422 i transkripten, och cirka 300 i den här sessionen [osäkert].
   - Kontexten per anrop består av systeminstruktioner och verktygsbeskrivningar, cirka 40 000–60 000 tokens [osäkert], plus samtalet, cirka 30 000–80 000 tokens, eftersom äldre verktygsresultat rensas löpande.
   - 860 × 70 000–140 000 ≈ 60–120 miljoner tokens in.
   - En stor del av detta återanvänds sannolikt från cache. Hur det räknas i tjänsten är [osäkert].
3. **Ut.** Koden och texten Claude skrev är cirka 300 000 tokens. Till det kommer dolt resonemang, som inte syns i transkripten och som jag uppskattar till 0,5–1,5 miljoner [osäkert]. Totalt cirka 1–2 miljoner.

**Utanför tokenräkningen:**

- **Bildgenereringen i Higgsfield:** 12 bilder med GPT Image 2.5. Den räknas i krediter, inte tokens.
- **Konceptbilderna:** Marcus egna generering i ett externt verktyg [osäkert vilket].

**Underlag:** spara daterad historik från claude.ai, alltså den här chatten och dess publicerade artefakter. I Claude Code visar sessionen själv sin förbrukning. Vilket kommando som visar tokens på Marcus abonnemang är [osäkert]. Ta skärmdumpar löpande.

---

## 8. Bibliotek, modeller, verktyg och andras material

### AI-modeller och tjänster

- **Claude från Anthropic i claude.ai:** all konstruktion, kod, analys och text. I sessionen 11–15 november var modellen Claude Opus 5.5. Vilken modell som användes 27 oktober–11 november är [osäkert].
- **Funktioner i claude.ai:** Artifacts för publicerade sidor, Claude Docs för projektdokumentet, webbsökning och webbhämtning, minne, kodkörning i en Linux-miljö och visning av bilder.
- **Higgsfield, via koppling i claude.ai:** 12 demobilder till besöksliggaren med bildmodellen GPT Image 2.5 (`gpt_image_2_5`), 2026-10-27.
- **Externt bildverktyg för konceptskisserna:** [osäkert vilket]. Claude skrev promptarna.
- **Kopplingar i claude.ai 2026-10-27:** Notion, för en tillfällig sida för demobilderna, och Gmail.

### Bibliotek och program

- **Python:** `manifold3d` för solidgeometri, `trimesh` för nät, STL och GLB, `numpy`, `shapely` för analys av lager och överhäng, `rectpack` för att packa delar på plattor, `matplotlib` (TextPath, för text i 3D som "LENNART" och etiketterna på toleranstestet) och `Pillow`.
- **Fler Python-paket:** `playwright` med Chromium och SwiftShader för skärmdumpar och test av sidorna, `markdown` för projektdokumentet i förhandsgranskningen, och `pymeshfix`, som provades men inte användes.
- **JavaScript:** three.js r128 från cdnjs.cloudflare.com i förhandsgranskningen och minihusen.
- **Typsnitt:** Bricolage Grotesque och Special Elite från Google Fonts på sidorna, och DejaVu Sans för text i 3D-modellen.
- **Bambu Studio:** skivning, gjord av Marcus.
- **Blender och Claude Code:** planerat för trailern.

### Hårdvara och andras material

- **Bambu Lab X2D Combo** med AMS 2 Pro.
- **Mått från standarder och datablad:** Raspberry Pi 5 och Camera Module 3, med hålmönstret 21 × 12,5 mm. Waveshare 2" skärm för Pico, Pico-varianten med knappar. Servomått som MG996R och MG90S. Alla ska kontrolleras mot de riktiga delarna.
- **Webbkällor:**
  - Bambu Lab wiki om filamentgrupper för munstyckena ("H2D filament config limit") och om munstyckenas räckvidd.
  - Recensioner och specifikationer för X2D:s byggvolym, 256 × 256 mm och 235,5 mm med båda munstyckena.
  - Electrokits produktsidor.
  - SweClockers tävlingsvillkor.
- **Ekorr- och skatdekalerna, handen, huset och allt annat i 3D:** ritat i kod av Claude. Inga bilder eller modeller från andra har använts i dem.

---

## Bilaga: projektdokumentet som ögonblicksbild 2026-11-11

Det här är texten i fliken Projektdokument i förhandsgranskningen, ordagrant från `doc.md`. Den levande versionen finns i Claude Docs (länk i avsnitt 4.6) och uppdaterades senare med Electrokit-köpet. Delar är inaktuella: ASA i stället för PETG, de gamla plattnumren och antalet filer.

`````markdown
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
`````
