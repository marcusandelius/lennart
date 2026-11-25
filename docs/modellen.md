# 3D-modellen i kod

Hela huset är byggt i Python-kod av Claude, utan CAD-program. Koden ligger i [model/](../model/). Texten nedan är hämtad ur [HANDOFF-filen](historik/HANDOFF-lennarts-matstation-projekt.md), avsnitt 4.1, 4.2 och 4.6.

> Sökvägarna `/home/claude/fix` och `/mnt/user-data/outputs` kommer från chattens Linux-miljö. I repot ligger skripten i `model/`.

## 4.1 Läs först

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

## 4.2 Miljö och kommandon som användes

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


## 4.6 Data och filer som inte är kod

Filer som levererades till Marcus. Publicerade sidor är privata tills Marcus delar dem.

| Fil eller länk | Innehåll |
|---|---|
| `lennarts-matstation-3d.html`, publicerad på https://claude.ai/artifact/9LQD4NfnbhvxCEfwnb7qiV | Förhandsgranskningen med 3D, demo, projektdokument, 3D-filer och utskrift. Innehåller hela aktuella modellen (`parts_v11.json`), plattorna och alla STL-filer inbäddade. |
| `lennarts-matstation-3d.zip` | Alla 57 STL-filer i aktuell version |
| `kroppen-rod-och-gra.zip` | Ny kropp: `05_kropp_rod.stl` och `05_kropp_sockel_gra.stl` |
| `19_skarmficka.stl`, `19b_skarmficka_regel.stl` (2026-11-25) | Skärmfickan och regeln, som ersätter `19_skarmklamma.stl`. Skapas av `model/skarmficka.py`. |
| `kamerafaste-och-skarmfaste.zip` | `15_kamerafaste.stl`, `19_skarmklamma.stl` och `18_skarmram_svart.stl` |
| `elektroniklada-lock-monteringsplatta.zip` | `16_elektroniklada.stl`, `16b_elektroniklada_lock.stl` och `24_monteringsplatta.stl` |
| `toleranstest.stl` (samma som `platta-4-toleranstest.stl`), `platta-4-basen.stl`, `platta-7-bottenplatta.stl` | Enskilda plattor |
| `platta-13-kroppen.zip` | Kroppen version 7 i tre färger, den som skrevs ut 2026-11-13 |
| `lennarts-matstation-trailer.zip` | `lennarts-matstation.glb` (version 7, 48 delar, meter, vridpunkter för lucka och hjul), `delar.json`, `README.md`, dekaler och skärmbilder som PNG |
| `lennarts-besoksliggare.html`, https://claude.ai/artifact/3Pf1zaveQGaKdFKwVuLrTc | Demo av den publika besöksliggaren med 12 AI-genererade bilder |
| `lennarts-minihus.html`, https://claude.ai/artifact/N2Fr5AUTLH34VUrGafmF3t, och `lennarts-miniatyrer.zip` | Minihusen, 5 cm höga |
| Projektdokumentet i Claude Docs, https://claude.ai/artifact/DsUhQhTLndz1BhiCxTa6bE | Beslut, inköpslista, utskrift, montering, service och öppna frågor. Delvis inaktuellt: det säger ASA och har gamla plattnummer. |


Skriptet som återskapar datan ligger i [tools/extract_from_html.py](../tools/extract_from_html.py). `disp.json` ligger i [model/disp.json](../model/disp.json).

`parts_v8.json` (version 7 med inbyggda vita detaljer) finns inte inbäddad längre. Den finns som delarna i `lennarts-matstation.glb` i trailerpaketet, och som STL i `platta-13-kroppen.zip`. Att återskapa `parts_v8.json` exakt ur dem är [osäkert].
