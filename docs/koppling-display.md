# Koppla Waveshare 2"-skärmen till Raspberry Pi 5

Skärmen (Electrokit art.nr 41036261, "2" LCD 320x240 for Raspberry Pi Pico 4x buttons") är gjord för att sitta på en Raspberry Pi Pico. Den talar vanlig SPI, så den kopplas till Pi 5 med kopplingskablar (Dupont).

**Vilka kablar:** Pi 5 har stift (hane). Skärmkortet för Pico har troligen hylsor (hona) på baksidan, där Pico:n skulle tryckas in [verifiera genom att titta på kortet].
- Hylsor på kortet → **hane–hona**-kablar.
- Stift på kortet → **hona–hona**-kablar.

8 kablar behövs. 20 cm räcker på skrivbordet. I huset kan avståndet till elektroniklådan kräva 30 cm, och då kan SPI-hastigheten behöva sänkas (se tabellen längre ned).

> **Stäng av Pi:n och dra ur strömmen innan du kopplar.**
> Pinnarna på skärmsidan är tagna från Waveshares beskrivning av Pico-LCD-2 och är **[verifiera]**: kontrollera mot Waveshares wiki eller tryck på kortet innan du kopplar. Pi-sidan är standard för Raspberry Pi.

## Via RJ45 (från 2026-11-25)

Skärmen kopplas via två keystone-uttag, ett i elektroniklådan och ett vid skärmen, och en hel rak patchkabel. Båda uttagen får en kort bit Cat6 efter färgkod **T568B**, och på Cat6-bitarnas andra ände löds kopplingskablar: honor till Pi:n, hanar till skärmkortet. Med ett uttag i båda ändar spelar det ingen roll om patchkabeln är kopplad enligt A eller B. Steg för steg med kontroller: [kopplingsguide.html](kopplingsguide.html) (publicerad som artefakt).

**Kopplingskablarnas färger:** CLK gul, GND grå, DIN grön, CS orange, DC blå, 3,3 V röd, RST vit, BL lila.

**Erfarenhet 2026-11-25:** kopplingskablar som lades direkt i keystone-uttagen fick nästan ingen kontakt. Isoleringen är för tjock för knivarna, och bara två av åtta ledare fungerade. Det upptäcktes genom att låta Pi:n läsa av stiften med `pinctrl` (steg 2.3 i guiden), utan multimeter.

| RJ45-stift | Färg (B) | Signal | Pi 5, fysiskt stift | Skärmkortet, Pico-stift |
|---|---|---|---|---|
| 1 | vit-orange | CLK | 23 | 14 (GP10) |
| 2 | orange | GND | 6 | 13 |
| 3 | vit-grön | DIN | 19 | 15 (GP11) |
| 4 | blå | CS | 24 | 12 (GP9) |
| 5 | vit-blå | DC | 22 | 11 (GP8) |
| 6 | grön | 3,3 V | 1 | 39 (VSYS) |
| 7 | vit-brun | RST | 13 | 16 (GP12) |
| 8 | brun | BL | 12 | 17 (GP13) |

Paren är valda så att CLK tvinnas med GND och DIN med 3,3 V. Uttaget märks **SKÄRM** och får aldrig förväxlas med Pi:ns nätverksuttag.

## Kopplingstabell

| Signal | Skärmkortet (Pico-pinne) [verifiera] | Raspberry Pi 5 (GPIO) | Pi 5 fysisk pinne | Varför |
|---|---|---|---|---|
| Ström | VSYS (pinne 39) | 3,3 V | 1 | Skärmens logik går på 3,3 V. Se strömavsnittet nedan. |
| Jord | GND | GND | 6 | Gemensam jord |
| DIN (MOSI) | GP11 (pinne 15) | GPIO 10, SPI0 MOSI | 19 | Data från Pi:n till skärmen |
| CLK | GP10 (pinne 14) | GPIO 11, SPI0 SCLK | 23 | Klocka för SPI |
| CS | GP9 (pinne 12) | GPIO 8, SPI0 CE0 | 24 | Väljer skärmen på SPI-bussen |
| DC | GP8 (pinne 11) | GPIO 25 | 22 | Talar om ifall det som skickas är kommando eller bild |
| RST | GP12 (pinne 16) | GPIO 27 | 13 | Startar om skärmen |
| BL | GP13 (pinne 17) | GPIO 18 | 12 | Bakgrundsbelysning |

Knapparna på kortet (KEY0–KEY3) kopplas inte in än.

## Ström

Kortet får ström via **VSYS** (Pico-pinne 39, andra uppifrån på höger sida med USB-änden uppåt). Prövat 2026-11-20: med 3,3 V på Pico-pinnen 3V3 (36) förblev skärmen helt släckt, och på VSYS tändes bakgrundsbelysningen.

Waveshares wiki anger VSYS som strömingång och driftspänningen 2,6–5,5 V (enligt sökresultat från [wikin](https://www.waveshare.com/wiki/Pico-LCD-2), läst 2026-11-20; själva sidan gick inte att hämta automatiskt). Både 3,3 V och 5 V ligger alltså inom gränserna. Kortet har en lödbrygga märkt 3V3/VSYS och en liten regulator bredvid [verifiera vad bryggan gör]. Vi kör med Pi:ns **3,3 V (pinne 1)**.

## Hitta pinnarna

**Pi 5:** lägg Pi:n med stiftlisten längs överkanten och USB- och nätverksportarna åt höger. Pinne 1 sitter längst till vänster i den undre raden, och pinne 2 rakt ovanför. Udda nummer sitter i den undre raden, jämna i den övre. Pinne *n* sitter i kolumn *n ÷ 2, avrundat uppåt*. Undertill har pinne 1 en fyrkantig lödpunkt. Kommandot `pinout` på Pi:n ritar upp stiftlisten.

**Skärmkortet:** titta på baksidan med USB-änden uppåt. Vänster sida är Pico-pinne 1–20 uppifrån och ned, höger sida 21–40 nerifrån och upp. Alla signaler utom strömmen sitter i en obruten rad, pinne 11–17 på vänster sida:

```
  GP8  DC   11 → Pi 22
  GP9  CS   12 → Pi 24
       GND  13 → Pi 6
  GP10 CLK  14 → Pi 23
  GP11 DIN  15 → Pi 19
  GP12 RST  16 → Pi 13
  GP13 BL   17 → Pi 12
  VSYS      39 → Pi 1   (höger sida, andra uppifrån)
```

Står GP-namnen tryckta på kortet gäller de framför den här listan.

## Testa från adminvyn

Under **Skärmen** i adminvyn på lennart.cam väljer du vad skärmen visar: **kamerabilden**, **ACCESS GRANTED** (helgrön) eller **ACCESS DENIED** (helröd). Valet gäller direkt.

Läget **Demo** visar kamerabilden, och när något rör sig framför kameran lottas ACCESS GRANTED eller ACCESS DENIED fram och visas i 4 sekunder. Efter det vilar demoläget i 3 sekunder, och ett djur som blir sittande lottas inte om. Rörelse- och ljusgränsen är samma som för inspelningen. Koden finns i `pi/demo.py`.

Där finns också:
- **SPI-hastighet** (1–32 MHz). Lösa kopplingskablar klarar inte alltid 32 MHz. Gäller direkt.
- **Starta om skärmen**, som skickar skärmens startkommandon igen.
- En teknisk rad med vilken SPI-enhet och GPIO-krets programmet använder.

✓ i kortet betyder att programmet kunde starta skärmen. Skärmen kan inte svara tillbaka över SPI, så programmet märker inte om en datakabel sitter fel.

## Om skärmen är svart

| Vad du ser | Troligt fel | Gör så här |
|---|---|---|
| Helt släckt, inget sken | Ingen ström eller ingen bakgrundsbelysning | Kontrollera ström (VSYS → Pi 1), GND och BL (→ Pi 12). |
| Svagt grått sken men ingen bild | Strömmen fick komma efter att programmet startade skärmen, eller en datakabel sitter fel | Starta om tjänsten, så att skärmen startas om (se nedan). Hjälper det inte: kontrollera DIN, CLK, CS, DC och RST. CLK (Pi 23) och CS (Pi 24) sitter i samma kolumn och är lätta att byta plats på. |
| Randig eller trasig bild, eller svart trots att kablarna stämmer | För hög SPI-hastighet för kablarna | Sänk **SPI-hastighet** i adminvyn, t.ex. till 8 MHz. Kortare kablar hjälper också. |

Starta om tjänsten på Pi:n:

```bash
systemctl --user restart lennart
```

## Om bilden blir fel

Inställningarna läggs i `~/.config/lennart/.env` och börjar gälla när tjänsten startas om.

| Problem | Ändra |
|---|---|
| Bilden står upp och ner | `LCD_ROTATION=270` (standard är 90) |
| Rött och blått byter plats | `LCD_BGR=1` |
| Kamerabilden är vriden eller upp och ner | Välj rotation under **Kamera** i adminvyn på lennart.cam (0°, 90°, 180° eller 270°). |
| Randig eller trasig bild | Sänk **SPI-hastighet** i adminvyn, eller använd kortare kablar. `LCD_SPI_HZ` i `.env` gäller bara tills lennart.cam har svarat. |
| Annan pinne för DC, RST eller BL | `LCD_DC=`, `LCD_RST=`, `LCD_BL=` (GPIO-nummer) |
| Fel GPIO-krets hittas | `LCD_GPIOCHIP=` (t.ex. `13`). Normalt hittas den automatiskt: numren skiljer sig mellan kärnversioner, och på Marcus Pi heter kretsarna `gpiochip11`–`15`. |
| "SPI på stiftlisten är inte påslaget" i adminvyn | SPI är avstängt, och då finns inte `/dev/spidev0.0`. Slå på SPI (steg 4a i [SETUP-PI.md](SETUP-PI.md)) och starta om Pi:n. 2026-11-20 fanns bara `/dev/spidev10.0` på Marcus Pi. Programmet använde den, och skärmen förblev svart. |

## Kameran

Camera Module 3 Wide kopplas till Pi 5:s kamerakontakt **CAM/DISP 0** eller **1**. Pi 5 har en *mindre* kontakt (22 pinnar) än kameran (15 pinnar), så det behövs en kabel med 22 pinnar i ena änden och 15 i den andra. Om den köpta kabeln från Electrokit (art.nr 41020810) är en sådan är **[osäkert]**, så kontrollera det innan du kopplar. Den blanka sidan av kabeln vetter mot kontaktens kontaktbleck.
