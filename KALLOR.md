# Källor, verktyg och hjälp

Allt som bidraget bygger på och som inte är Marcus eget arbete. Lägg till en rad i samma commit som du börjar använda något nytt. Grundinnehållet kommer från [HANDOFF-filen](docs/historik/HANDOFF-lennarts-matstation-projekt.md), avsnitt 8.

## AI-modeller och tjänster

| Namn | Används till | När | Länk |
|---|---|---|---|
| Claude (Anthropic) i claude.ai | All konstruktion av 3D-modellen, kod, analys och text i chatten om matstationen. 11–15 nov var modellen Claude Opus 5.5. Modell 27 okt–11 nov [osäkert]. | 2026-10-27–11-15 | https://claude.ai |
| Funktioner i claude.ai | Artifacts (publicerade sidor), Claude Docs (projektdokumentet), webbsökning och webbhämtning, minne, kodkörning i Linux-miljö, visning av bilder | 2026-10-27–11-15 | https://claude.ai |
| Claude Code (Anthropic), molnsession | Repo-uppsättning, deploy, Pi-guide, flytt av koden från HANDOFF, beslutsunderlag | 2026-11-15– | https://claude.ai/code |
| Higgsfield, via koppling i claude.ai | 12 demobilder till besöksliggaren med bildmodellen GPT Image 2.5 (`gpt_image_2_5`) | 2026-10-27 | https://higgsfield.ai |
| Externt bildverktyg för konceptskisserna | Marcus genererade konceptbilder av huset. Claude skrev promptarna. Verktyg [osäkert vilket]. | 2026-10-27 | [osäkert] |
| ChatGPT (OpenAI) | Marcus genererade logotypen "Lennart.cam". Vilken bildmodell [osäkert]. | 2026-11-15 [verifiera] | https://chatgpt.com |
| Kopplingar i claude.ai: Notion och Gmail | Notion: tillfällig sida för att föra över demobilderna | 2026-10-27 | – |
| Bildigenkänning | *Beslutas, se [docs/beslut/bildigenkanning.md](docs/beslut/bildigenkanning.md)* | – | – |

## Bibliotek och program

| Namn | Licens | Används till | Länk |
|---|---|---|---|
| manifold3d | Apache-2.0 [verifiera] | Solidgeometri för 3D-modellen | https://github.com/elalish/manifold |
| trimesh | MIT [verifiera] | Nät, STL och GLB | https://github.com/mikedh/trimesh |
| numpy | BSD-3-Clause [verifiera] | Beräkningar | https://numpy.org |
| shapely | BSD-3-Clause [verifiera] | Analys av lager och överhäng | https://github.com/shapely/shapely |
| rectpack | Apache-2.0 [verifiera] | Packa delar på byggplattor | https://github.com/secnot/rectpack |
| matplotlib | Matplotlib-licens (PSF-baserad) [verifiera] | TextPath för text i 3D, t.ex. "LENNART" och toleranstestets etiketter | https://matplotlib.org |
| Pillow | MIT-CMU (HPND) [verifiera] | Bilder | https://python-pillow.org |
| playwright med Chromium och SwiftShader | Apache-2.0 [verifiera] | Skärmdumpar och test av sidorna | https://playwright.dev |
| markdown (Python) | BSD-3-Clause [verifiera] | Projektdokumentet i förhandsgranskningen | https://github.com/Python-Markdown/markdown |
| pymeshfix | MIT [verifiera] | Provades 2026-11-13, förstörde geometrin och **användes inte** | https://github.com/pyvista/pymeshfix |
| three.js r128 | MIT | 3D i förhandsgranskningen och minihusen, från cdnjs.cloudflare.com | https://threejs.org |
| Bambu Studio | AGPL-3.0 [verifiera] | Skivning, gjord av Marcus | https://bambulab.com/en/download/studio |
| Blender | GPL | Planerat för trailern | https://www.blender.org |
| Python 3, standardbiblioteket | PSF-licens | Webbdelen (`server/app.py`) och heartbeat på Pi:n | https://www.python.org |
| Docker-avbildningen `python:3.12-slim` | PSF-licens och Debians licenser [verifiera] | Grund för webbdelens container i Coolify | https://hub.docker.com/_/python |
| picamera2 | BSD-2-Clause [verifiera] | Kameran på Pi:n | https://github.com/raspberrypi/picamera2 |
| libcamera | LGPL-2.1 [verifiera] | Kamerastacken under picamera2 | https://libcamera.org |
| spidev (py-spidev) | MIT [verifiera] | SPI till skärmen | https://github.com/doceme/py-spidev |
| gpiozero | BSD-3-Clause [verifiera] | Installerad. Provades för skärmens styrpinnar men valde fel GPIO-krets på Pi 5, så den används inte för skärmen. | https://gpiozero.readthedocs.io |
| lgpio | Unlicense [verifiera] | Styrpinnarna till skärmen (DC, RST, BL) på Pi 5 | https://abyz.me.uk/lg/py_lgpio.html |
| ffmpeg | LGPL-2.1 eller senare, GPL-2.0 eller senare när det byggts med GPL-delar som libx264 (Debians paket gör det) [verifiera] | Gör MP4-filer av kamerabilderna vid inspelning på Pi:n. Används även för att skapa testklipp under utvecklingen. | https://ffmpeg.org |
| x264 (libx264) | GPL-2.0 eller senare [verifiera] | H.264-kodningen i ffmpeg | https://www.videolan.org/developers/x264.html |
| smbus (python3-smbus, från i2c-tools) eller smbus2 | GPL-2.0 resp. MIT [verifiera] | I2C till servokortet PCA9685 | https://i2c.wiki.kernel.org/index.php/I2C_Tools |

## Typsnitt

| Namn | Licens | Används till | Länk |
|---|---|---|---|
| Bricolage Grotesque | SIL OFL 1.1 (licenstexten ligger i `server/static/fonts/`) | Webbsidorna. På lennart.cam ligger typsnittsfilen (latin) på servern, hämtad från Google Fonts 2026-11-15. | https://github.com/ateliertriay/bricolage |
| Special Elite (Astigmatic) | Apache-2.0 (licenstexten ligger i `server/static/fonts/`) | Stämplarna på webbsidorna. På lennart.cam ligger typsnittsfilen (latin) på servern, hämtad från Google Fonts 2026-11-15. | https://fonts.google.com/specimen/Special+Elite |
| DejaVu Sans | Bitstream Vera-licens / fri [verifiera] | Text i 3D-modellen och på skärmen i huset | https://dejavu-fonts.github.io |
| Liberation Mono Bold (Liberation Fonts 2.1.5) | SIL OFL 1.1 (licenstexten ligger i `pi/fonts/`) | ACCESS GRANTED och ACCESS DENIED på skärmen i huset, som i filmtrailern. Filen kopierades 2026-11-27 ur Debianpaketet `fonts-liberation` och ligger i `pi/fonts/`, så att inget behöver installeras på Pi:n. | https://github.com/liberationfonts |

## Verktyg och tjänster för drift

| Namn | Används till | Länk |
|---|---|---|
| GitHub och GitHub Actions | Kod, versionshistorik, automatisk deploy | https://github.com |
| GitHub Actions: `actions/checkout` | Hämtar koden i deploy-jobbet på Pi:n | https://github.com/actions/checkout |
| Coolify | Hosting av webbdelen | https://coolify.io |
| Cloudflare | DNS för lennart.cam | https://www.cloudflare.com |
| Raspberry Pi OS (Bookworm) | Operativsystem på Pi:n | https://www.raspberrypi.com/software/ |

## Hårdvara

| Namn | Används till |
|---|---|
| Bambu Lab X2D Combo med AMS 2 Pro | 3D-utskrift av huset |
| Raspberry Pi 5, Camera Module 3 Wide, Waveshare 2" skärm m.m. | Se [docs/hardvara.md](docs/hardvara.md) |

## Mått och webbkällor

- **PCA9685-register** i `pi/servo.py` (MODE1, PRESCALE, LED0_ON_L, frekvens 50 Hz): från NXP:s datablad för PCA9685 [verifiera länk].
- **ST7789-kommandon** i `pi/display.py`: från Sitronix datablad för ST7789 och Waveshares beskrivning av Pico-LCD-2 [verifiera länk].
- **YOLOv8n tränad på Open Images V7** (`yolov8n-oiv7`), Ultralytics, [docs](https://docs.ultralytics.com/datasets/detect/open-images-v7/). Licens: AGPL-3.0. Exporterad till ONNX och inlagd som `pi/models/yolov8n-oiv7.onnx` 2026-11-20, se [docs/igenkanning.md](docs/igenkanning.md).
- **Open Images V7** (Google), som modellen är tränad på, [webbplats](https://storage.googleapis.com/openimages/web/factsfigures_v7.html). Licens: annoteringarna CC BY 4.0, bilderna listade som CC BY 2.0.
- **ONNX Runtime** (Microsoft), kör modellen på Pi:n, [GitHub](https://github.com/microsoft/onnxruntime). Licens: MIT.
- **Ultralytics** 8.4.216 (AGPL-3.0), **PyTorch** 2.15.0 (BSD-3-Clause), **onnx** 1.23.2 (Apache-2.0) och **onnxslim** 0.1.99 (MIT): användes bara för att exportera modellen till ONNX, i molnet. Finns inte på Pi:n.
- **AI-hjälp 2026-11-20:** en hjälpagent i Claude Code-sessionen sökte fram underlag om modeller för lokal igenkänning ([docs/beslut/bildigenkanning-modeller.md](docs/beslut/bildigenkanning-modeller.md)). Inga modeller eller data har lagts in än. De förs in här med licens när de väljs.
- **Pico-LCD-2, ström och SPI-stift:** [Waveshares wiki](https://www.waveshare.com/wiki/Pico-LCD-2), via sökresultat 2026-11-20 (sidan stänger ute automatiska anrop). Uppgifter: styrkrets ST7789VW, VCC till VSYS, 2,6–5,5 V, DIN = GP11, CLK = GP10, CS = GP9.

- **Mått från standarder och datablad:** Raspberry Pi 5 och Camera Module 3 (hålmönster 21 × 12,5 mm), Waveshare 2" skärm för Pico (varianten med knappar) samt servomått för MG996R och MG90S. Alla ska kontrolleras mot de riktiga delarna.
- **Bambu Lab wiki:** filamentgrupper för munstyckena ("H2D filament config limit") och munstyckenas räckvidd.
- **Recensioner och specifikationer:** X2D:s byggvolym, 256 × 256 mm, och 235,5 mm med båda munstyckena.
- **Electrokits produktsidor.**
- **SweClockers tävlingsvillkor:** https://projekt.sweclockers.com/asus/villkor

## Lånade resurser (bilder, ljud, typsnitt, 3D-modeller, kodsnuttar)

**I 3D-modellen: inga.** Ekorr- och skatdekalerna, handen, huset och allt annat i 3D är ritat i kod av Claude. Inga bilder eller modeller från andra har använts i dem (HANDOFF, avsnitt 8).

**På webbsidan lennart.cam:**

| Resurs | Var | Ursprung |
|---|---|---|
| Logotypen "Lennart.cam" (pixelhus med ekorre och ACCESS GRANTED) | `server/static/logo.webp` | Genererad av Marcus med ChatGPT (OpenAI), 2026-11-15 [verifiera datum]. Bakgrunden gjordes genomskinlig och bilden beskars med `tools/logo_transparent.py`. |
| 12 demobilder till besöksliggaren | `server/static/demo/` | AI-genererade med Higgsfield (se ovan), tagna ur artefakten https://claude.ai/artifact/3Pf1zaveQGaKdFKwVuLrTc. Inga personer syns. |

## Hjälp från personer och AI-sessioner

| Vem/vad | Vilken hjälp | Datum |
|---|---|---|
| Claude, chatten om Lennarts matstation i claude.ai | Konstruktion, 3D-modell, förhandsgranskning, inköpslista, utskriftsråd. Se [HANDOFF](docs/historik/HANDOFF-lennarts-matstation-projekt.md). | 2026-10-27–11-15 |
| Claude Code, molnsession | Repo-struktur, deploy-uppsättning, Pi-guide, flytt av kod och dokument, beslutsunderlag för bildigenkänning | 2026-11-15 |
| Claude Code, molnsession | Valruta, demosida och grönt tema på lennart.cam, ny text på demosidan | 2026-11-15 |
| Claude Code, molnsession | Livebild, adminvy, rotation, servostyrning | 2026-11-15 |
| Claude Code, molnsession | Inspelning vid rörelse på Pi:n, klipparkiv med märkning i adminvyn | 2026-11-18 |
| Claude Code, molnsession | Felsökning av plockskivan: utfallet och vinkeln analyserade i modellen, plockskiva med hål Ø 28 mm (`tools/plockskiva_hal28.py`), ny standardvinkel | 2026-11-27 |
| Behörig elektriker | *Planerat: elsäkerheten för utomhusström ska kontrolleras av en behörig person* | [osäkert] |

## Samtycke för bilder med personer

| Bild/fil | Person (förnamn eller beskrivning) | Samtycke givet (datum, hur) |
|---|---|---|
| *Inga ännu* | | |

Kontaktuppgifter till personerna skrivs **inte** här, eftersom repot är publikt.
