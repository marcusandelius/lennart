# Lennarts matstation

**Ett smart matställe för ekorren Lennart, som bara släpper in rätt gäst.**

Bidrag till SweClockers/ASUS-tävlingen **"Gick inte. Nu går det."** (2026) · **https://lennart.cam**

> **Gick inte:** Ekorren Lennart har besökt uteplatsen nästan varje dag sedan sommaren, men fåglarna stjäl hans mat. Att bygga något som skiljer en ekorre från en skata, utan CAD-vana och utan modelleringsprogram, gick inte.
> **Nu går det:** Med AI har ett litet falurött hus konstruerats helt i kod, skrivits ut i 3D och fått en kamera som känner igen Lennart.

## Personlig kod

<!-- Topp 3 ska enligt tävlingen lägga in en personlig kod i projektet. Klistra in den här. -->

```
[PERSONLIG KOD – läggs in om bidraget når topp 3]
```

## Vad är det?

Ett litet falurött hus med vita knutar, cirka 31 cm högt med skorsten, som står på en pedestal på uteplatsen.

- När något landar på framgården tar en kamera i gaveln 2–3 bilder.
- **Ekorre:** skärmen visar **ACCESS GRANTED** i grönt, och ett doseringshjul släpper ut en hasselnöt till skålen.
- **Andra djur**, till exempel skator, får **ACCESS DENIED** i rött och ingen nöt.
- Är svaret osäkert visar skärmen **VERIFIERAR…** och tar en ny bild.
- Varje besök loggas med bild och tid. En publik besöksliggare visar besöken på webben.

## Hur funkar det?

```
 ┌───────────────────────────────┐                    ┌──────────────────────────┐
 │ Huset (Raspberry Pi 5)        │   4G, bara         │ Webbdelen på Coolify     │
 │  kamera → bild vid rörelse    │   utgående trafik  │  besökslogg              │
 │  servo → doseringshjul, lucka │ ─────────────────▶ │  publik besöksliggare    │
 │  2" skärm → GRANTED / DENIED  │                    │  lennart.cam             │
 └───────────────────────────────┘                    └──────────────────────────┘
```

Var själva bildigenkänningen ska ske, på Pi:n, på servern eller i ett moln-API, beslutas i [docs/beslut/bildigenkanning.md](docs/beslut/bildigenkanning.md).

**Mekaniken:** ett hjul med en ficka, som i en tuggummiautomat. Ett servo vrider hjulet 130° och en nöt (18–22 mm) faller ner i rännan till skålen. Taket hålls av magneter och lyfts av för påfyllning. Elektroniken sitter på en platta som dras rakt upp ur en låda. Allt sitter ihop med snäppfästen, presspassningar och magneter i stället för lim.

## Så byggdes det med AI

- **3D-modellen** är byggd helt i Python-kod av Claude, med `manifold3d` och `trimesh`. Marcus har inget CAD-program. Koden finns i [model/](model/) och beskrivs i [docs/modellen.md](docs/modellen.md).
- **Förhandsgranskningen** med 3D, röntgenvy, monteringsvisning och demo finns i [web/](web/).
- **Beslut** med datum och skäl finns i [docs/beslut/beslutslogg.md](docs/beslut/beslutslogg.md).
- **Hela AI-historiken** finns i [docs/historik/](docs/historik/).

## Hårdvara

Raspberry Pi 5 (8 GB), Camera Module 3 Wide, Waveshare 2" skärm, servon via PCA9685, 4G-modem och 12 V-matning. Huset skrivs ut i PETG på en Bambu Lab X2D. Hela listan finns i [docs/hardvara.md](docs/hardvara.md).

## Bygga och driftsätta

**3D-utskrift:** STL-filerna återskapas ur förhandsgranskningen med [tools/extract_from_html.py](tools/extract_from_html.py). Utskriftsråd finns i [docs/modellen.md](docs/modellen.md).

**Programvaran** driftsätts automatiskt vid push till `main` ([.github/workflows/deploy.yml](.github/workflows/deploy.yml)):

1. **Webbdelen:** GitHub Actions ber Coolify bygga om och starta appen via Coolifys API.
2. **Raspberry Pi:** en GitHub-runner på Pi:n hämtar koden, installerar den och startar om systemd-tjänsten `lennart`. Runnern tar bara kontakt utåt, så inga portar öppnas och det fungerar likadant på wifi och 4G.

**Läget just nu:** Pi:n visar kamerabilden live på skärmen, rapporterar till statussidan på lennart.cam var 30:e sekund, och skickar livebild till lennart.cam när en besökare trycker på "Se live". Livebilden, kamerans rotation och servona styrs från adminvyn. Pi:n kan också spela in klipp när något rör sig. Klippen laddas upp till adminvyn och märks där (ekorre, skata …) som underlag för att välja och testa bildigenkänning. Igenkänningen kommer härnäst. lennart.cam öppnar med ett val mellan statussidan och en demo av besöksliggaren, med AI-genererade bilder och påhittade besök.

| Guide | Innehåll |
|---|---|
| [docs/SETUP-PI.md](docs/SETUP-PI.md) | Sätta upp Raspberry Pi:n från början |
| [docs/koppling-display.md](docs/koppling-display.md) | Koppla skärmen och kameran |
| [docs/koppling-servon.md](docs/koppling-servon.md) | Koppla servona via PCA9685 och testa dem från adminvyn |
| [docs/SETUP-COOLIFY.md](docs/SETUP-COOLIFY.md) | Webbdelen i Coolify och lennart.cam i Cloudflare |
| [docs/att-gora.md](docs/att-gora.md) | Det som återstår |

## Öppenhet enligt tävlingens villkor

| Fil | Innehåll |
|---|---|
| [FORE-TAVLINGEN.md](FORE-TAVLINGEN.md) | Allt som fanns före tävlingsstarten 16 okt 2026 |
| [KALLOR.md](KALLOR.md) | Modeller, bibliotek, verktyg, källor och hjälp |
| [TOKENS.md](TOKENS.md) | AI-användning per arbetspass, i molnet och lokalt |
| [docs/historik/](docs/historik/) | Orörda överlämningsfiler från AI-chattarna |

## Licens

Repot licensieras under **GNU Affero General Public License v3.0** (AGPL-3.0), se [LICENSE](LICENSE). Beslutat av Marcus 2026-11-20. Skälet är att bildigenkänningen bygger på en modell från Ultralytics, som är AGPL-3.0.

Lånade resurser (bibliotek, modeller, data, bilder) har sina egna licenser, och de står i [KALLOR.md](KALLOR.md). Om AGPL-3.0 också passar för innehåll som inte är kod, till exempel 3D-modellen och bilderna, eller om de ska ha en egen licens, är inte genomgånget [kräver granskning].
