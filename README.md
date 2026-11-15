# Lennart

Bidrag till SweClockers/ASUS-tävlingen **"Gick inte. Nu går det."** (2026)

> **[Fylls i]** En mening om vad Lennart är och vilket problem som "inte gick" men nu går.

## Personlig kod

<!-- Topp 3 ska enligt tävlingen lägga in en personlig kod i projektet. Klistra in den här. -->

```
[PERSONLIG KOD – läggs in om bidraget når topp 3]
```

## Vad är det?

**[Fylls i från HANDOFF-filerna]**

- Vad det gör
- Vem det är till för
- Varför det "inte gick" förut

## Hur funkar det?

```
 ┌─────────────────────┐        4G / wifi        ┌──────────────────────┐
 │  Raspberry Pi 5     │  ─────────────────────▶ │  Webbdel på Coolify  │
 │  kamera + appen     │   (bara utgående trafik) │                      │
 └─────────────────────┘                          └──────────────────────┘
```

**[Fylls i]** Var bildigenkänningen sker beslutas i [docs/beslut/bildigenkanning.md](docs/beslut/bildigenkanning.md).

## Hårdvara

| Del | Kommentar |
|---|---|
| Raspberry Pi 5, 8 GB | Raspberry Pi OS Bookworm |
| 4G-modem | Köps senare. Under bygget används wifi. |
| **[Fylls i]** | Kamera, hölje (3D-utskrift) med mera |

## Hur det byggs och driftsätts

Allt driftsätts automatiskt vid push till `main` ([.github/workflows/deploy.yml](.github/workflows/deploy.yml)):

1. **Webbdelen**: GitHub Actions ber Coolify bygga om och starta appen via Coolifys API.
2. **Raspberry Pi**: en GitHub-runner på Pi:n hämtar koden, installerar och startar om systemd-tjänsten `lennart`. Runnern tar bara kontakt utåt, så inga portar öppnas och det fungerar likadant på wifi och 4G.

Sätta upp Pi:n från början: [docs/SETUP-PI.md](docs/SETUP-PI.md).

## Öppenhet

| Fil | Innehåll |
|---|---|
| [FORE-TAVLINGEN.md](FORE-TAVLINGEN.md) | Allt som fanns före tävlingsstarten 16 okt 2026 |
| [KALLOR.md](KALLOR.md) | Bibliotek, modeller, verktyg, lånade resurser och hjälp |
| [TOKENS.md](TOKENS.md) | AI-användning per arbetspass |
| [docs/historik/](docs/historik/) | Orörda överlämningsfiler från tidigare AI-chattar |

## Licens

**[Beslutas]**
