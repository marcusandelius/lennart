# Koppla servona till Raspberry Pi 5 via PCA9685

Servona styrs via ett **PCA9685-kort** (16 kanaler, I2C). Kortet skapar servosignalerna, så att Pi 5 bara behöver skicka kommandon över två trådar. Servona får egen ström från 5 V-omvandlaren, inte från Pi:n.

> **Stäng av all ström innan du kopplar.** Pi-sidan är standard för Raspberry Pi. Kontrollera märkningen på ditt PCA9685-kort, eftersom placeringen av stiften skiljer sig mellan tillverkare [verifiera].

## PCA9685 till Pi 5 (4 kablar, hona–hona)

| PCA9685 | Raspberry Pi 5 | Fysisk pinne | Varför |
|---|---|---|---|
| VCC | 3,3 V | 17 | Kortets logik. Pinne 1 är upptagen av skärmen. |
| GND | GND | 9 | Gemensam jord |
| SDA | GPIO 2 (SDA) | 3 | Data över I2C |
| SCL | GPIO 3 (SCL) | 5 | Klocka för I2C |

**V+ på PCA9685** får **inte** kopplas till Pi:n.

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

Ett 360°-servo har ingen vinkel. Pulsen styr fart och riktning: 1500 µs är stilla, längre puls snurrar åt ena hållet och kortare åt det andra. Servot stannar när signalen släpps. Därför styrs rörelsen med **tid**, och skivan vet aldrig exakt var den står. Små fel kan växa för varje utmatning, så kolla läget då och då.

Fliken **Nötdosering** guidar i fem steg. Gör det utan nötter först:

1. **Kolla riktningen:** tryck **Knuffa upp ▶**. Rör sig hålet från nöthögen mot utfallet är riktningen rätt. Annars kryssar du i **Omvänd riktning**.
2. **Ställ hålet i plockläget:** knuffa tills hålet står längst ner i nöthögen. Välj 50, 100 eller 250 ms per knuff.
3. **Hitta tiden upp:** tryck **Snurra upp**. Stannar hålet före utfallet, öka tiden med **+**. Åker det förbi, minska med **−**. Knuffa tillbaka mellan försöken.
4. **Hitta tiden ner:** med hålet vid utfallet, tryck **Snurra ner** och justera tills hålet hamnar i plockläget. Tiden blir sällan exakt lika lång som tiden upp, eftersom 360°-servon ofta går olika fort åt olika håll och skivan lutar.
5. **Testa en hel utmatning.**

Under **Fart och stilla-läge** längst ner finns två inställningar till. **Farten** är 120 µs från stilla som standard, vilket är lugnt. Ändrar du farten måste tiderna provas fram igen. Kryper servot när det borde stå still, justera **Stilla-läge** 5 µs i taget (normalt 1500).

**Testa utmatning** gör sedan: ett litet vick (80 ms upp och ner, två gånger) som rör om nötterna, snurr upp till utfallet, ett stopp på 0,3 s där nöten faller ut, och snurr tillbaka ner. Testet utgår från att hålet står i plockläget när det börjar.

### Plockskivan med vinkelservo

1. Dra reglaget till exempelvis 90° och tryck **Flytta**. Servot vrider sig och släpps efter en sekund.
2. **Testa utmatning** går till plocklägets vinkel (standard 0°), gör ett vick på 12° två gånger och vrids sedan lugnt upp till utmatningsvinkeln (standard 119°). Vridet tar den tid som står i **Tid för vridet** (standard 1 500 ms), med mjuk start och inbromsning. Efter ett stopp på 0,3 s vrids skivan lika lugnt tillbaka.

Titta när skivan står still uppe: hålet ska ligga mitt över utfallet. Vinklarna och tiden ändras i fliken **Nötdosering**, utan ny deploy.

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
