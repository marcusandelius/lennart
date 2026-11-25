# Hårdvara och delar

Hämtad ur [HANDOFF-filen](historik/HANDOFF-lennarts-matstation-projekt.md), avsnitt 3, läget 2026-11-15.

## 3.1 Fanns innan projektet

Detta fanns före tävlingen:

- **Hos Marcus:** Raspberry Pi 5 (minnesstorlek [osäkert]) och en lödpenna med spetssats för gänginsatser.
- **Material:** Ruthex-insatser, cirka 30 M3 och 6 M4, silikagel, Wago 221, kopplingskablar, kabelskor och krympslang. När de skaffades är [osäkert].
- **SIM:** ett oanvänt data-SIM. Om det går på Telias eller Telenors nät är [osäkert].

## 3.2 Utrustning och köpta delar

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

## 3.3 Planerat men inte köpt

Pris markerat med "?" är inte kontrollerat.

| Del | Antal | Pris | Till |
|---|---|---|---|
| PCA9685, I2C-servodrivkort | 1 | 60–100 kr? | Servostyrning från Pi 5 |
| Kopplingskablar (Dupont), blandsats hane–hane, hane–hona och hona–hona, 20 cm (gärna även 30 cm) | 1 sats | ? | Skärmen (8 st) och PCA9685 (4 st) till Pi:n. Tillagt 2026-11-15. Kontrollera först om "kopplingskablar" i 3.1 är sådana. |
| Tvinnad tvåledare, cirka 0,75 mm², röd och svart | cirka 1 m | ? | 5 V från DC/DC-omvandlaren (8–23 V → 5 V, 3 A) till PCA9685:s skruvplint för servoström. Tillagt 2026-11-15. |
| Servoförlängning, 3-pol, 30 cm | 0–2 | ? | Bara om servonas kablar inte når från elektroniklådan till doseraren och luckan. Mät först. Tillagt 2026-11-15. |
| USB-C-kabel med öppna ledare ("pigtail") | 1 | ? | Möjligt sätt att mata Pi 5 från 5 V-omvandlaren (5 A). Beslutas senare. Tillagt 2026-11-15. |
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

## 3.4 Filament i skrivarens AMS

Enligt Marcus skärmdump 2026-11-14 kl. 22.58:

- **AMS 1:** A1 PLA (mörk grågrön), A2 PETG röd, A3 PETG svart, A4 PETG grå.
- **AMS 2:** B1 PLA beige, B2 PLA svart, B3 PETG grön, B4 PETG vit.
- **Extern hållare:** Ext-L TPU.

I tidigare listor fanns också Fiberon ASA-CF08 Dark Red, Bambu ASA röd och vit, PrimaSelect ASA grå och svart och TPU 95A. Var dessa finns nu är [osäkert].

## 3.5 Utskrivet hittills

| Datum | Del | Material | Kommentar |
|---|---|---|---|
| 2026-11-13–14 | Kroppen version 7 med inbyggda vita detaljer | PETG i rött, grått och vitt | Testkropp. Dörröverstycket hängde fritt, rensningstornet välte vid 89 % och vänster hörnbräda blev porös. Ska användas för elektroniktest. |
| 2026-11-14 | Elektroniklåda, lock och monteringsplatta | PETG, en färg | – |
| 2026-11-14–15 | Basen | Grön PETG | Utskriven över natten |
| 2026-11-15 | Bottenplattan | PETG [osäkert vilken färg] | – |
| 2026-11-15 | Toleranstestet | Grå PETG | Pågick när filen skrevs. Resultatet är [osäkert]. |
| [osäkert] | Kamerafäste, skärmklämma och skärmram | – | Filerna levererades 2026-11-15. Om de är utskrivna är [osäkert]. |

Om minihusen från 2026-10-28 skrevs ut är [osäkert].

## 3.6 Mått på skärmkortet (Waveshare Pico-LCD-2)

Avlästa 2026-11-25 ur fyra foton av kortet med tumstock (snett tagna, utan skjutmått). Räkna med ±1–2 mm. Inget av måtten är uppmätt med skjutmått [verifiera].

| Mått | Värde | Hur det togs fram |
|---|---|---|
| Kortets bredd (långsidan) | ca 46–50 mm, ritat som 48 | Två foton med tumstock, som gav olika värden |
| Kortets höjd (kortsidan) | ca 31–33 mm, ritat som 32 | Två foton med tumstock |
| Displayen | ca 3,6 mm tjock, nästan lika stor som kortet | Fotot från sidan, skalat mot kortets längd |
| Kortet med glipa mot displayen | ca 2,9 mm | Samma foto |
| Pico-hylsorna | ca 12 mm höga, 2 × 20 hål, 50,8 mm långa. Längre än kortet, så de sticker ut i båda ändar. | Höjden ur fotot från sidan. Längden är 20 × 2,54 mm. |
| Avstånd mellan hylsraderna | 17,78 mm (Pico-standard) | Inte uppmätt. Antaget att raderna sitter mitt på kortet [verifiera]. |
| Totalt djup, displayens framsida till hylsornas topp | ca 18,5 mm | Fotot från sidan och fotot med tumstocken stående |
| Knapparna KEY0–KEY3 | Sidoknappar i hörnen på långsidorna, på baksidan. De sticker ut ca 1,3 mm över kanten, når ca 2,7 mm in och är ca 3,5 mm höga. | Foton uppifrån, ungefärligt |
| Blå flik | Troligen dragfliken på skärmens skyddsfilm [verifiera] | Foto |

Används av `model/skarmficka.py`. Fritt djup bakom hylsorna till nötmagasinet är ca 7,8 mm enligt modellen, så raka Dupont-kontakter (ca 14 mm) får inte plats där [verifiera mot kablarna].

