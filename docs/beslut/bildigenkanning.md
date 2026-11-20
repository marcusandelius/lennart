# Beslut: var ska bildigenkänningen köras?

**Status:** Inriktning beslutad 2026-11-20: lokalt på Pi:n (se Beslut längst ned). Modellen är inte vald.
**Datum:** 2026-11-15 (reviderat samma dag efter att HANDOFF-filen lästs)

> Siffror märkta [verifiera] är typiska storleksordningar, inte mätningar. De ska mätas på riktigt innan beslutet blir slutgiltigt.

## Uppgiften

Ur HANDOFF-filen och projektdokumentet:

- Avgöra **ekorre eller annat djur** (främst skator och andra fåglar) på 2–3 bilder per besök. Hög tröskel, och läget **VERIFIERAR** vid osäkert svar.
- Svar inom **ca 5 sekunder** från landning.
- Pi:n går över **4G** (USB-modem, data-SIM). Under bygget används wifi.
- **Utan svar blir det ingen nöt.** Det säkra läget är att neka.
- Besöksliggaren ska ha **en bild per besök** på webben. Bara bilder som klassats som djur får publiceras, så att inga människor hamnar på den publika sidan.
- Kameran är köpt: **Camera Module 3 Wide**, och fästet är ritat för den.
- **Tidigare beslut** (troligen 2026-10-27): igenkänningen ska göras i molnet, eftersom det är enklast. HANDOFF-filen säger att det är [osäkert] om beslutet fortfarande gäller.
- **Tidsram:** 15 dagar kvar till inlämningen 30 november.

## Alternativen

### A. På Pi:n (Pi 5:s processor, eventuellt AI-kamera)

En färdig, liten bildmodell körs på Pi:n, till exempel en klassificerare tränad på ImageNet, som har klasser för ekorre och skata [verifiera].

- **Svarstid:** under 1 s per bild på Pi 5:s processor för små modeller [verifiera]. Ingen nätverksfördröjning.
- **Träffsäkerhet:** osäker. Färdiga modeller är tränade på tydliga bilder, och verkliga bilder från matplatsen visar ofta halva djur, motljus och morgonmörker. Bra säkerhet kräver troligen egen träning på bilder från platsen, och sådana bilder finns inte än.
- **Kostnad:** 0 kr löpande. AI-kameran (Sony IMX500) skulle ersätta den redan köpta Camera Module 3 Wide, och då måste fästet kontrolleras [verifiera mått och pris].
- **4G:** fungerar även utan täckning.
- **Data:** bilden till besöksliggaren måste ändå skickas, men det kan ske i efterhand och påverkar inte svarstiden.

### B. Egen modell på servern i Coolify

Pi:n skickar bilden till webbdelen, som kör en modell.

- **Svarstid:** uppladdning ca 0,2–0,5 s för en nedskalad bild på 50–80 KB över 4G, plus beräkning på en vanlig VPS ca 0,2–2 s [verifiera]. Totalt ca 1–3 s.
- **Träffsäkerhet:** samma problem som A, eftersom det är samma typ av modell. Det enda som vinns är mer beräkningskraft.
- **Kostnad:** servern finns redan, men en tyngre modell kan kräva en större VPS.
- **4G:** kräver uppkoppling.

### C. Moln-API med bildförståelse, anropat via servern

Pi:n skickar bilden till webbdelen på Coolify. Servern frågar ett moln-API med bildförståelse, till exempel en AI-modell som kan beskriva bilder, och får tillbaka art och säkerhet. API-nyckeln ligger bara på servern.

- **Svarstid:** uppladdning ca 0,2–0,5 s plus API-svar ca 1–3 s [verifiera]. Totalt ca 2–4 s, vilket ryms inom 5 s med normal 4G-täckning.
- **Träffsäkerhet:** hög utan egen träning. Sådana modeller skiljer ekorre från skata även på dåliga bilder, och kan dessutom svara "människa" så att den bilden aldrig publiceras.
- **Kostnad:** betalas per bild. Med 2–3 bilder per besök och några tiotal besök per dag blir det några tusen bilder per månad [verifiera prislista för vald tjänst].
- **4G:** kräver uppkoppling. Utan svar blir det ingen nöt, vilket redan är projektets regel.
- **Data:** 3 bilder × 60 KB × 50 besök ≈ 9 MB per dag, eller ca 0,3 GB per månad [räkneexempel]. Bilden ska ändå till servern för besöksliggaren, så samma uppladdning gör båda sakerna.
- **Integritet:** bilderna skickas till en tredje part. Bilder där människor syns ska raderas och aldrig publiceras. GDPR behöver stämmas av med någon som kan reglerna [kräver granskning].

## Jämförelse

| | A. Pi:n | B. Egen modell, Coolify | C. Moln-API via Coolify |
|---|---|---|---|
| Svarstid (typiskt) | **< 1 s** | 1–3 s | 2–4 s |
| Klarar 5 s med dålig 4G | **Ja** | Oftast | Oftast |
| Fungerar utan nät | **Ja** | Nej | Nej (ger ingen nöt) |
| Ekorre eller skata utan egen träning | Osäkert | Osäkert | **Ja** |
| Känner igen människor och stoppar publicering | Med extra modell | Med extra modell | **Ja, i samma svar** |
| Data per besök över 4G | Liten, bilden kan skickas senare | ~150–250 KB | ~150–250 KB (samma som besöksliggaren behöver) |
| Löpande kostnad | **0 kr** | VPS | Per bild |
| Arbete att bygga | Mest (välja, testa, kanske träna) | Mycket | **Minst** |
| Stämmer med tidigare beslut | Nej | Nej | **Ja** |

## Rekommendation

**C: moln-API via servern i Coolify.** Pi:n sköter rörelsedetektering, tar 2–3 bilder, skalar ner dem och skickar dem till webbdelen. Servern frågar API:et, sparar besöket och svarar Pi:n med GRANTED, DENIED eller VERIFIERAR.

Skälen:

1. **Träffsäkerhet är viktigast.** Varje fel ger en skata en nöt, eller nekar Lennart. C är det enda alternativet som skiljer ekorre från skata på riktiga bilder utan egen träning.
2. **Tiden.** 15 dagar till inlämning räcker inte för att samla in bilder och träna en egen modell.
3. **Bilden ska till servern ändå** för besöksliggaren, så C kostar nästan ingen extra data.
4. **API-nyckeln stannar på servern** som hemlighet. Pi:n har bara en enhetsnyckel som går att byta.
5. **Det stämmer med det tidiga beslutet** om igenkänning i molnet.

**Ändring mot förra versionen av underlaget:** innan HANDOFF-filen fanns rekommenderade jag A, eftersom jag inte visste vad som skulle kännas igen eller att bilderna ändå ska till servern.

**Plan B:** om svarstiden över 4G visar sig vara för lång, kan Pi:n få en liten lokal modell som förfilter. Den släpper igenom tydliga fall direkt och skickar bara de osäkra vidare. Det tar vi i så fall som ett eget beslut efter mätning.

**Bara Lennart eller alla ekorrar?** Ingen av lösningarna kan säkert känna igen en *enskild* ekorre. Det är en öppen fråga i projektdokumentet, och rekommendationen ovan förutsätter "alla ekorrar".

## Att bestämma om du väljer C

- **Vilken tjänst och modell.** Jag tar fram ett förslag med pris och svarstid när du valt väg.
- **Var bilderna sparas** och hur länge.

## Nästa steg efter beslut

1. Mät svarstiden: först på wifi, sedan över 4G när modemet finns.
2. Lägg in vald modell eller tjänst i KALLOR.md och beslutet i beslutsloggen.
3. Skriv in beslutet här, med datum.

## Beslut

**2026-11-20, inriktning:** Marcus vill att igenkänningen körs **lokalt på Pi:n**, som objektdetektering på videon med en egen klass för ekorre (alternativ A). Ett moln-API (C) väljs alltså bort. Vilken modell som används, och om en färdig modell räcker eller om en egen behöver tränas, är inte avgjort. Underlag tas fram av en hjälpagent och läggs till här.
