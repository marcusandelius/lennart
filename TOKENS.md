# Tokenlogg

En rad per arbetspass. **Moln** = AI-tjänster i molnet (claude.ai, Claude Code i molnet). **Lokalt** = modeller som körs på egen hårdvara (Pi:n eller egen dator).

Metoden anger hur siffran togs fram: *exakt* (avläst i verktyget) eller *uppskattat* (med beskrivning). claude.ai visar ingen tokenräknare, så alla siffror hittills är uppskattningar.

**"In"** räknar allt modellen läser vid varje anrop, eftersom hela kontexten läses om varje gång. En stor del av detta kommer sannolikt från cache, men hur tjänsten räknar det är [osäkert].

| Datum | Vad vi gjorde | Tokens moln | Metod moln | Tokens lokalt | Metod lokalt |
|---|---|---|---|---|---|
| 2026-10-27 – 2026-11-15 | Chatten om Lennarts matstation i claude.ai: idé, krav, 3D-modell i kod (version 1–7 med ändringar), förhandsgranskning med demo, inköpslista, utskrift, besöksliggare-demo. Se [HANDOFF](docs/historik/HANDOFF-lennarts-matstation-projekt.md). | ca 60–120 miljoner in, ca 1–2 miljoner ut [osäkert] | Uppskattat, se HANDOFF avsnitt 7: ca 860 modellanrop × 70 000–140 000 tokens kontext per anrop. Unikt innehåll ca 0,8 miljoner tokens, räknat ur transkriptens teckenantal (ca 3,5 tecken per token) och 1 500 tokens per bild. Ut: ca 300 000 tokens synlig kod och text, plus 0,5–1,5 miljoner dolt resonemang. | 0 | Ingen lokal modell användes |
| 2026-11-15 | Claude Code-session: repo-uppsättning, CLAUDE.md, deploy-workflows (Coolify och Pi), förslag på bildigenkänning, SETUP-PI-guide, flytt av kod och dokument från HANDOFF | ca 3–6 miljoner in, ca 0,1 miljon ut [osäkert] | Uppskattat med samma metod: ca 60 modellanrop × 50 000–100 000 tokens kontext. Ut uppskattat ur mängden skriven text och kod. Exakt siffra går inte att läsa av inifrån sessionen. | 0 | Ingen lokal modell användes |
| 2026-11-15 (kväll) | Läste tävlingsvillkoren. Första programvaran: kamerabild live på 2"-skärmen, heartbeat till lennart.cam, statussida och Dockerfile för Coolify. Guider för Coolify, Cloudflare och koppling av skärmen. Testade med låtsashårdvara och Docker. | ca 4–8 miljoner in, ca 0,1 miljon ut [osäkert] | Uppskattat med samma metod: ca 50 modellanrop × 80 000–150 000 tokens kontext (kontexten var stor efter HANDOFF-läsningen). Ut uppskattat ur mängden skriven kod och text. | 0 | Ingen lokal modell användes |
| 2026-11-15 (kväll, forts.) | Första push till GitHub och felsökning av deploy: curl för Coolifys hälsokontroll, spärr per jobb i workflowet, POST till Coolifys API. lennart.cam svarar med rätt version. | ca 2–4 miljoner in, ca 0,03 miljoner ut [osäkert] | Uppskattat: ca 25 modellanrop × 100 000–150 000 tokens kontext. Ut uppskattat ur mängden skriven text och kod. | 0 | Ingen lokal modell användes |
| 2026-11-15 (kväll, forts.) | Valruta, demosida och grönt tema på lennart.cam: demobilder och logotyp ut som filer, typsnitt på servern, ny text på demosidan, test med skärmdumpar i Chromium. | ca 1,5–3 miljoner in, ca 0,04 miljoner ut [osäkert] | Uppskattat: ca 30 modellanrop × 50 000–100 000 tokens kontext. Ut uppskattat ur mängden skriven kod och text. Exakt siffra går inte att läsa av inifrån sessionen. | 0 | Ingen lokal modell användes |
| 2026-11-15 (kväll, Pi) | Pi-guiden steg 1–7 med Marcus. Runnern installerad, och Pi:n deployas automatiskt vid push. Felsökning av skärmdrivrutinen (RPi.GPIO → lgpio, GPIO-krets), felmeddelanden från Pi:n visas på lennart.cam, inköpslista för kablar. | ca 4–8 miljoner in, ca 0,05 miljoner ut [osäkert] | Uppskattat: ca 40 modellanrop × 100 000–200 000 tokens kontext. Ut uppskattat ur mängden skriven text och kod. | 0 | Ingen lokal modell användes |
| 2026-11-15 (kväll, skärm) | Felsökning av skärmdrivrutinen på Pi 5 via felmeddelanden på lennart.cam och loggar i GitHub Actions: GPIO-kretsar med andra nummer, lgpio direkt i stället för gpiozero, SPI-enheten letas upp. Skärmdrivrutinen startar nu. | ca 4–8 miljoner in, ca 0,04 miljoner ut [osäkert] | Uppskattat: ca 35 modellanrop × 120 000–220 000 tokens kontext. Ut uppskattat ur mängden skriven text och kod. | 0 | Ingen lokal modell användes |
| 2026-11-15 (kväll, kylning) | Strypningsstatus från Pi:n till lennart.cam, skärmen begränsad till 10 bilder per sekund, råd om kylning | ca 1–2 miljoner in, ca 0,02 miljoner ut [osäkert] | Uppskattat: ca 10 modellanrop × 120 000–220 000 tokens kontext | 0 | Ingen lokal modell användes |

## Utanför tokenräkningen

- **Higgsfield 2026-10-27:** 12 bilder med GPT Image 2.5. Räknas i krediter, inte tokens. Antal krediter [osäkert].
- **Logotypen [verifiera datum]:** Marcus genererade den med ChatGPT. Bildgenerering räknas inte i tokens på samma sätt, och förbrukningen syns inte här [osäkert].
- **Konceptbilderna 2026-10-27:** Marcus egen generering i ett externt verktyg [osäkert vilket].

## Underlag

Topp 3 ska kunna visa underlag för tokens och AI-historik senast 15 december kl. 23.59. Spara:

- daterad historik från claude.ai, alltså chatten och dess publicerade artefakter;
- skärmdumpar av förbrukning där den visas;
- HANDOFF-filerna i [docs/historik/](docs/historik/).
