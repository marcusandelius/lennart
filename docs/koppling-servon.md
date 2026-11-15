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
| Doseringshjulet (servot på 11 kg) | 0 | Brun = GND, röd = V+, orange/gul = signal |
| Luckan (MG90S) | 1 | Samma |

Kanalerna går att ändra i adminvyn under "Inställningar för servona".

## Slå på I2C och installera paketet (på Pi:n)

Görs en gång, se steg 9 i [SETUP-PI.md](SETUP-PI.md).

## Testa från adminvyn

1. Logga in på https://lennart.cam/admin.
2. Under **Servon** ska det stå `✓ PCA9685 på I2C-buss 1 …` när kortet hittats.
3. Dra reglaget för doseringshjulet till exempelvis 90° och tryck **Flytta**. Servot vrider sig och släpps efter en sekund.
4. **Testa utmatning** gör ett litet vick, vrider till utmatningsvinkeln (130°) och tillbaka.

| Problem | Gör så här |
|---|---|
| `Inget servokort svarar på I2C-buss …` | Kontrollera SDA, SCL, VCC och GND. Kör `i2cdetect -y 1` på Pi:n: `40` ska synas. |
| `Ingen /dev/i2c-* finns` | I2C är inte påslaget, eller Pi:n behöver startas om (steg 9). |
| Servot rör sig inte, men kortet hittas | Ström saknas på V+, eller servot sitter på fel kanal. |
| Servot brummar eller står och tar i vid 0° eller 180° | Minska intervallet för pulsbredden i adminvyn, till exempel 600–2400 µs. |
| Pi:n startar om när servot rör sig | Servona får ström från Pi:n. V+ ska komma från omvandlaren, inte från Pi:n. |
