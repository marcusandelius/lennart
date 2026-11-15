# Koppla Waveshare 2"-skärmen till Raspberry Pi 5

Skärmen (Electrokit art.nr 41036261, "2" LCD 320x240 for Raspberry Pi Pico 4x buttons") är gjord för att sitta på en Raspberry Pi Pico. Den talar vanlig SPI, så den kopplas till Pi 5 med kopplingskablar (Dupont).

**Vilka kablar:** Pi 5 har stift (hane). Skärmkortet för Pico har troligen hylsor (hona) på baksidan, där Pico:n skulle tryckas in [verifiera genom att titta på kortet].
- Hylsor på kortet → **hane–hona**-kablar.
- Stift på kortet → **hona–hona**-kablar.

8 kablar behövs. 20 cm räcker på skrivbordet. I huset kan avståndet till elektroniklådan kräva 30 cm, och då kan SPI-hastigheten behöva sänkas (se tabellen längre ned).

> **Stäng av Pi:n och dra ur strömmen innan du kopplar.**
> Pinnarna på skärmsidan är tagna från Waveshares beskrivning av Pico-LCD-2 och är **[verifiera]**: kontrollera mot Waveshares wiki eller tryck på kortet innan du kopplar. Pi-sidan är standard för Raspberry Pi.

## Kopplingstabell

| Signal | Skärmkortet (Pico-pinne) [verifiera] | Raspberry Pi 5 (GPIO) | Pi 5 fysisk pinne | Varför |
|---|---|---|---|---|
| Ström | VSYS eller 3V3 [verifiera] | 3,3 V | 1 | Skärmens logik går på 3,3 V. Se strömavsnittet nedan. |
| Jord | GND | GND | 6 | Gemensam jord |
| DIN (MOSI) | GP11 (pinne 15) | GPIO 10, SPI0 MOSI | 19 | Data från Pi:n till skärmen |
| CLK | GP10 (pinne 14) | GPIO 11, SPI0 SCLK | 23 | Klocka för SPI |
| CS | GP9 (pinne 12) | GPIO 8, SPI0 CE0 | 24 | Väljer skärmen på SPI-bussen |
| DC | GP8 (pinne 11) | GPIO 25 | 22 | Talar om ifall det som skickas är kommando eller bild |
| RST | GP12 (pinne 16) | GPIO 27 | 13 | Startar om skärmen |
| BL | GP13 (pinne 17) | GPIO 18 | 12 | Bakgrundsbelysning |

Knapparna på kortet (KEY0–KEY3) kopplas inte in än.

## Ström

Kontrollera i Waveshares schema om kortets strömingång tål 5 V eller ska ha 3,3 V. **Koppla 3,3 V (pinne 1) om du är osäker.** Logiken är 3,3 V, och 5 V på fel ställe kan skada kortet.

## Om bilden blir fel

Inställningarna läggs i `~/.config/lennart/.env` och börjar gälla när tjänsten startas om.

| Problem | Ändra |
|---|---|
| Bilden står upp och ner | `LCD_ROTATION=270` (standard är 90) |
| Rött och blått byter plats | `LCD_BGR=1` |
| Kamerabilden är upp och ner | `CAMERA_FLIP=1` |
| Randig eller trasig bild | Kortare kablar, eller sänk `LCD_SPI_HZ=16000000` |
| Annan pinne för DC, RST eller BL | `LCD_DC=`, `LCD_RST=`, `LCD_BL=` (GPIO-nummer) |
| Fel GPIO-krets eller SPI-enhet hittas | `LCD_GPIOCHIP=` (t.ex. `13`) eller `LCD_SPI_DEV=` (t.ex. `10.0`). Normalt hittas de automatiskt: numren skiljer sig mellan kärnversioner, och på Marcus Pi heter kretsarna `gpiochip11`–`15`. |

## Kameran

Camera Module 3 Wide kopplas till Pi 5:s kamerakontakt **CAM/DISP 0** eller **1**. Pi 5 har en *mindre* kontakt (22 pinnar) än kameran (15 pinnar), så det behövs en kabel med 22 pinnar i ena änden och 15 i den andra. Om den köpta kabeln från Electrokit (art.nr 41020810) är en sådan är **[osäkert]**, så kontrollera det innan du kopplar. Den blanka sidan av kabeln vetter mot kontaktens kontaktbleck.
