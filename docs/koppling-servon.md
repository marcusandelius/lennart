# Koppla servona till Raspberry Pi 5 via PCA9685

Servona styrs via ett **PCA9685-kort** (16 kanaler, I2C). Kortet skapar servosignalerna, så att Pi 5 bara behöver skicka kommandon över två trådar. Servona får egen ström från 5 V-omvandlaren, inte från Pi:n.

> **Stäng av all ström innan du kopplar.** Pi-sidan är standard för Raspberry Pi. Kontrollera märkningen på ditt PCA9685-kort, eftersom placeringen av stiften skiljer sig mellan tillverkare [verifiera].

## PCA9685 till Pi 5 (4 kablar med snabbkoppling)

Kopplingskablar hona–hona på servokortet och hane–hona på Pi:n, ihopstuckna i mitten. Färger: VCC röd, GND svart, SDA orange, SCL brun. Varje knippe krymps ihop för sig.

| PCA9685 | Raspberry Pi 5 | Fysisk pinne | Varför |
|---|---|---|---|
| VCC | 3,3 V | 17 | Kortets logik. Pinne 1 är upptagen av skärmen. |
| GND | GND | 9 | Gemensam jord |
| SDA | GPIO 2 (SDA) | 3 | Data över I2C |
| SCL | GPIO 3 (SCL) | 5 | Klocka för I2C |

**V+ på PCA9685** får **inte** kopplas till Pi:n.

## Servona via RJ45 (senare, valfritt)

För bänktestet sitter servona direkt i PCA9685 (doseraren i kanal 0, luckan i kanal 1), eftersom deras egna kontakter redan går att lossa. RJ45 nedan läggs till vid monteringen om det behövs, med ett kretskort på 4 × 6 cm som servokoppling i stället för lödda Y-skarvar.


PCA9685 sitter i elektroniklådan. En rak patchkabel går från uttaget **SERVON** i lådans vägg till en servokoppling vid doseraren, där båda servona ansluts med lödda Y-skarvar (Wago 221 går också bra). Färgkod **T568B**. Steg för steg: [kopplingsguide.html](kopplingsguide.html).

| RJ45-stift | Färg (B) | Signal | PCA9685 | Servokopplingen |
|---|---|---|---|---|
| 1 | vit-orange | Doserare, signal | Kanal 0, PWM | Doserarservots orange/gula |
| 2 | orange | GND | Kanal 0, GND | Lödd Y-skarv → båda servonas bruna |
| 3 | vit-grön | Lucka, signal | Kanal 1, PWM | Luckservots orange/gula |
| 6 | grön | V+ 5 V | Kanal 0, V+ | Lödd Y-skarv → båda servonas röda |
| 4, 5, 7, 8 | – | Används inte | Klipps korta och isoleras | Klipps korta och isoleras |

**Varför bara fyra ledare:** uttagen för skärm och servon ser likadana ut. Stiften är valda så att en förväxling inte kortsluter Pi:ns styrstift. Skärmen får då 5 V på VSYS (tål 2,6–5,5 V enligt Waveshare) och servosignaler på CLK och DIN. Servona får Pi:ns 3,3 V och SPI-signaler [verifiera, prova inte med flit]. En ledare var för V+ och GND ger cirka 0,2 V spänningsfall vid 2,5 A på 0,5 m [uppskattat].

## Ström till servona

| Från | Till | Varför |
|---|---|---|
| DC/DC-omvandlaren 8–23 V → 5 V 3 A, `+` | PCA9685, skruvplinten `V+` | Servona drar mycket ström när de startar, och det ska inte gå genom Pi:n. |
| Samma omvandlare, `−` | PCA9685, skruvplinten `GND` | Gemensam jord med Pi:n, via kortets GND |
| Kondensator 1000 µF 16 V | Över `V+` och `GND` på skruvplinten. Det långa benet (`+`) till V+ och den randiga sidan (`−`) till GND. | Jämnar ut spänningsdippar när servona startar |

## Servona i kortet

| Servo | Kanal | Kabelfärger (vanligast) |
|---|---|---|
| Plockskivan, doseringen (just nu 360°-servot på 5 kg, se nedan) | 0 | Brun = GND, röd = V+, orange/gul = signal |
| Luckan (MG90S) | 1 | Samma |

Kanalerna går att ändra i adminvyn, under fliken **Servokort**.

## Slå på I2C och installera paketet (på Pi:n)

Görs en gång, se steg 9 i [SETUP-PI.md](SETUP-PI.md).

## Testa från adminvyn

1. Logga in på https://lennart.cam/admin.
2. Under fliken **Servokort** ska det stå "Servokortet är anslutet", med en grön prick, när kortet hittats.
3. Öppna fliken **Nötdosering** och välj vilket servo som driver plockskivan: **360°-servo** (just nu) eller **Vinkelservo**. Fliken visar då knapparna och inställningarna som passar. Allt sparas direkt när det ändras.

### Plockskivan med 360°-servo (just nu)

Ett 360°-servo har ingen vinkel. Pulsen styr fart och riktning: vid servots stilla-punkt (ofta runt 1500 µs) står det still, längre puls snurrar åt ena hållet och kortare åt det andra. Servot stannar när signalen släpps. Därför kan servot inte veta var skivan står, och **lägena sparas som tid från plockläget**.

En utmatning är **ett helt varv framåt**: fram till utfallet, ett stopp på 0,3 s där nöten faller ut, och resten av varvet tillbaka till plockläget. Skivan går bara åt ett håll, så det spelar ingen roll om servot går lika fort åt båda hållen. Marcus har provat för hand att skivan kan snurra ett helt varv (2026-11-27).

Fliken **Nötdosering** guidar i fem steg. Gör det utan nötter först:

1. **Lär känna servot:** tryck **Starta**. Stationen snurrar skivan en kort stund i taget, och du svarar **Bakåt**, **Stod still** eller **Framåt**. Guiden provar först full fart åt båda hållen och halverar sedan intervallet efter varje svar, som när man gissar ett tal. Efter ungefär 9 prov har den hittat servots stilla-punkt och vilket håll som är framåt, och sparar båda. Med **Ångra senaste svaret** och **Kör samma prov igen** går det att rätta ett felklick. Ställ sedan in **Fart** med reglaget, från Lugn till Snabb.
2. **Spara plockläget:** knuffa tills hålet står längst ner i nöthögen och tryck **Spara som plockläge**. En räknare börjar då om från 0 ms. Knuffens längd ställs med reglaget bredvid knappen, från 20 till 2 000 ms. Ta långa knuffar första biten och korta sista biten.
3. **Spara utfallet:** knuffa framåt tills hålet står mitt över utfallet och tryck **Spara som utfall**. Räknarens tid sparas.
4. **Spara ett helt varv:** knuffa vidare tills hålet är tillbaka i plockläget och tryck **Spara som helt varv**.
5. **Finjustera och testa:** steg 5 är en guide i två delar. **A** kör tiden till utfallet, och du svarar med ett reglage hur långt hålet kom, till exempel "ungefär 70 % av vägen". Sidan räknar om tiden. **B** kör vidare runt till plockläget, med den tid som återstår av ett helt varv efter A. A och B blir alltså tillsammans alltid ett helt varv, så hålet kommer tillbaka nära plockläget även om A var fel, och inget behöver göras om. Du svarar var hålet stannade jämfört med plockläget, och sidan rättar tiden **från utfallet till plockläget**. Svaren ges i steg om 1 % (A) och en halv procent av ett varv (B), och − och + bredvid reglagen flyttar ett steg i taget. Kör A och B igen tills båda stämmer, och tryck sedan **Testa utmatning**.

Under **Tiderna i siffror** står de två delarna var för sig: **Till utfallet** och **Från utfallet till plockläget**. Skriv in en tid eller använd − och + (10 ms per tryck). Ändras den ena delen behåller den andra sin tid. Exempel: 670 ms till utfallet och 1 560 ms därifrån till plockläget ger ett helt varv på 2 230 ms.

**Varannan utmatning bakåt (sedan 2026-11-28):** med **Varannan utmatning bakåt** påslagen går varannan utmatning ett helt varv framåt och varannan ett helt varv bakåt. Bakåt har egna tider, eftersom servot sällan går lika fort åt båda hållen. Bakåt når hålet utfallet efter den långa vägen runt, och sedan plockläget efter den korta. Välj **Bakåt** under Riktning i steg 5 och prova fram tiderna med samma A och B. **Börja från framåt-tiderna** ger en första gissning. Pi:n håller reda på vilket håll nästa utmatning går, och adminvyn visar det. Efter en omstart av Pi:n börjar den framåt. **Bara framåt** och **Bara bakåt** kör en utmatning åt ett bestämt håll. Bakåt kräver att servot kan backa, alltså att guiden **Lär känna servot** i steg 1 har hittat stilla-punkten.

**Gå till plockläget** (vid räknaren i steg 2 och i steg 5) kör framåt resten av varvet, enligt sidans räkning av hur långt skivan snurrat sedan plockläget sparades. Den går framåt i stället för att backa, eftersom servot går olika fort åt olika håll. Den blir lika exakt som tiden för ett helt varv, och den tiden rättas i B. Står hålet lite fel efteråt: knuffa sista biten. Räkningen finns i webbläsaren och nollställs om fliken stängs.

Under **Justera för hand och knuffa bakåt** längst ner finns stilla-punkten och riktningen, om de behöver ändras för hand, och knappen **Knuffa bakåt**. Det behövs sällan efter guiden.

**Varför guiden behövs:** 360°-servot står still vid en signal som skiljer sig från servo till servo. Programmet antog 1500 µs. Ligger servots egen stilla-punkt en bit därifrån går både framåt och bakåt åt samma håll, och farten blir olika åt de två hållen. Så var det 2026-11-27: knuffa bakåt gick åt samma håll som framåt, Omvänd riktning hjälpte bara ibland, och farten motsvarade inte inställningen. Farten räknas från stilla-punkten, så när den är rätt stämmer farten åt båda hållen. Den ökar ändå inte jämnt hela vägen, och den sjunker när skivan bär nötter.

Har servot en justerskruv för stilla-punkten [verifiera på servot] och guiden säger att skivan går åt samma håll båda gångerna: vrid skruven lite och kör guiden igen.

**Felet växer för varje varv.** Är tiden för ett helt varv 2 % fel har hålet glidit en femtedel av ett varv efter 10 nötter. Kolla då och då att hålet står i plockläget, och knuffa tillrätta vid behov. En givare som känner av när skivan passerar plockläget, till exempel en magnet i skivan och en hallgivare, skulle låta servot hitta hem varje varv. Det är inte beslutat.

### Plockskivan med vinkelservo

1. Dra reglaget till exempelvis 90° och tryck **Flytta**. Servot vrider sig och släpps efter en sekund.
2. **Testa utmatning** går till plocklägets vinkel (standard 0°), gör ett vick på 12° två gånger och vrids sedan lugnt upp till utmatningsvinkeln (standard 119°). Vridet tar den tid som står i **Tid för vridet** (standard 1 500 ms), med mjuk start och inbromsning. Efter ett stopp på 0,3 s vrids skivan lika lugnt tillbaka.

Titta när skivan står still uppe: hålet ska ligga mitt över utfallet. Vinklarna och tiden ändras i fliken **Nötdosering**, utan ny deploy.

### Luckan

Servots vinklar säger inget om vilket håll som är öppet, eftersom det beror på hur servot sitter i luckan. Därför sparas luckans två lägen i fliken **Luckan**:

1. Flytta luckan försiktigt med **−5°**, **−1°**, **+1°** och **+5°**. Reglaget börjar där stationen senast rapporterade luckan, så att första steget inte blir ett stort hopp.
2. Flytta till stängt läge och tryck **Spara som stängd**. Flytta till öppet läge och tryck **Spara som öppen**.
3. Använd sedan **Öppna** och **Stäng**. Luckan rör sig långsamt. Innan lägena är sparade gör knapparna ingenting.

### Testbänk och "Vilken sorts servo är det?"

I fliken **Servokort** finns en testbänk för valfri kanal 0–15. Guiden skickar två signaler, två sekunder var, en åt varje håll. Du svarar om servot vred sig och stannade (vinkelservo), snurrade hela tiden (360°-servo) eller inte reagerade. Gäller det nötdoseringens kanal kan inställningen för skivan ändras med en knapp. Under **Skicka en egen signal** går det att prova valfri signal i en sekund.

## Testa från statussidan

När du är inloggad (via https://lennart.cam/admin) visas rutan **Testa stationen** längst ner på https://lennart.cam/status. Den syns inte för andra besökare, och servern kontrollerar inloggningen vid varje tryck.

| Knapp | Vad som händer |
|---|---|
| Plockskivan | Samma rörelse som **Testa utmatning** i adminvyn. |
| Lilla servot | MG90S på kanal 1 sveper mellan 10° och 170° i 3 sekunder och släpps sedan. |
| ACCESS GRANTED / ACCESS DENIED | Skärmen visar bilden i 4 sekunder och går sedan tillbaka till sitt vanliga läge. |

| Problem | Gör så här |
|---|---|
| `Inget servokort svarar på I2C-buss …` | Kontrollera SDA, SCL, VCC och GND. Kör `i2cdetect -y 1` på Pi:n: `40` ska synas. |
| `Ingen /dev/i2c-* finns` | I2C är inte påslaget, eller Pi:n behöver startas om (steg 9). |
| Servot rör sig inte, men kortet hittas | Ström saknas på V+, eller servot sitter på fel kanal. |
| Servot brummar eller står och tar i vid 0° eller 180° | Minska intervallet för pulsen i adminvyn, fliken **Servokort**, till exempel 600–2400 µs. |
| Pi:n startar om när servot rör sig | Servona får ström från Pi:n. V+ ska komma från omvandlaren, inte från Pi:n. |
