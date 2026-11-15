# Beslut: var ska bildigenkänningen köras?

**Status:** Förslag, väntar på Marcus beslut. Inget byggs innan dess.
**Datum:** 2026-11-15

> **Förbehåll:** Underlaget är skrivet innan HANDOFF-filerna fanns i repot. Vad som ska kännas igen (och hur svårt det är) styr valet. Förslaget ses över när HANDOFF-filerna har lästs.
> Siffror märkta [verifiera] är typiska storleksordningar, inte mätningar. De ska mätas på riktigt innan beslutet blir slutgiltigt.

## Krav

- Svar inom **ca 5 sekunder** från att bilden tas.
- Ska fungera över **4G** (ojämn täckning, data kostar pengar, uppkopplingen kan försvinna).
- Inga öppna portar på Pi:n.

## Alternativen

### A. På Pi:n (Pi 5 med CPU, eventuellt AI-kamera)

En liten bildmodell (t.ex. klassificering eller objektdetektering i storleken "nano/mobile") körs direkt på Pi:n. Bara *resultatet* skickas till webbdelen, och vid behov en liten miniatyrbild.

- **Svarstid:** ungefär 0,1–1 s per bild på Pi 5:s CPU för små modeller [verifiera]. Med AI-kamera (Sony IMX500) körs modellen i själva kamerasensorn, vilket blir snabbare och nästan inte belastar Pi:n [verifiera]. Ingen nätverksfördröjning.
- **Kostnad:** ingen löpande kostnad. AI-kameran kostar en engångssumma [verifiera pris].
- **4G:** fungerar även utan täckning, eftersom resultat kan köas och skickas när nätet är tillbaka.
- **Data:** ca 1 KB per resultat, eller ca 20–50 KB med miniatyrbild.
- **Nackdel:** begränsat till små modeller. AI-kameran kräver att modellen konverteras till kamerans format, vilket är extra arbete.

### B. På servern i Coolify

Pi:n skickar varje bild till webbdelen, som kör modellen.

- **Svarstid:** uppladdning plus beräkning plus svar. En bild på 100–200 KB tar ca 0,2–1 s att ladda upp över 4G [verifiera], och beräkningen på en vanlig VPS utan GPU tar ca 0,2–2 s [verifiera]. Totalt ofta 1–3 s, men det varierar med täckningen.
- **Kostnad:** servern finns redan. En större modell kan kräva mer CPU och minne, alltså en dyrare VPS.
- **4G:** kräver uppkoppling för varje bild. Utan täckning blir det inget svar.
- **Data:** ca 100–200 KB per bild. 100 bilder per dag blir ca 10–20 MB per dag, eller 0,3–0,6 GB per månad [räkneexempel].
- **Fördel:** modellen kan bytas utan att röra Pi:n, och servern har mer kraft än Pi:n.

### C. Moln-API (t.ex. en AI-tjänst med bildförståelse)

Pi:n eller servern skickar bilden till ett externt API.

- **Svarstid:** ca 1–5 s inklusive uppladdning [verifiera], vilket ligger nära gränsen på 5 s när 4G-täckningen är dålig.
- **Kostnad:** betalas per bild. Liten för en demo, men den växer med publiken under röstningen [verifiera prislista].
- **4G:** kräver uppkoppling. Samma datamängd som B.
- **Integritet:** bilderna lämnar din kontroll. Om personer kan synas i bilden är det en GDPR-fråga som behöver granskas [kräver granskning].
- **Fördel:** förstår *vad som helst* (fri text, ovanliga saker) utan egen träning.
- **Hemlighet:** API-nyckeln måste skyddas, alltså ligga på servern som GitHub Secret och aldrig på Pi:n i klartext i repot.

## Jämförelse

| | A. Pi:n | B. Coolify | C. Moln-API |
|---|---|---|---|
| Svarstid (typiskt) | **< 1 s** | 1–3 s | 1–5 s |
| Klarar 5 s även med dålig 4G | **Ja** | Oftast | Tveksamt |
| Fungerar utan nät | **Ja** (köar resultat) | Nej | Nej |
| Data per bild över 4G | **~1–50 KB** | ~100–200 KB | ~100–200 KB |
| Löpande kostnad | **0 kr** | VPS (finns redan) | Per bild |
| Modellens förmåga | Liten, specifik | Mellan | **Störst, generell** |
| Bilder lämnar enheten | **Nej** | Till din egen server | Till tredje part |
| Berättelse i tävlingen | "Allt sker i lådan" | Klassisk klient/server | "AI i molnet" |

## Rekommendation (preliminär)

**A: kör igenkänningen på Pi:n**, med en liten modell på CPU:n först. Det är det enda alternativet som säkert klarar 5 s även när 4G-täckningen är dålig, och det skickar minst data. Bilderna stannar dessutom i lådan, vilket förenklar integritetsfrågan. AI-kameran köps bara om CPU:n visar sig vara för långsam när vi mäter.

Webbdelen på Coolify tar emot resultat och miniatyrer och visar dem.

**Undantag:** om det som ska kännas igen kräver "förståelse" (fri beskrivning, många olika saker, text i bild) räcker inte en liten modell. Då blir **C via servern** det realistiska valet: Pi:n skickar bilden till webbdelen, som anropar API:et med nyckeln som hemlighet. Detta avgörs när HANDOFF-filerna är lästa.

## Nästa steg efter beslut

1. Mät svarstiden på riktigt, både på Pi:n och över 4G när modemet finns.
2. Lägg in vald modell eller tjänst i KALLOR.md med licens.
3. Skriv in beslutet här, med datum.

## Beslut

*Väntar på Marcus.*
