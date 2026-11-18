# Sätta upp Raspberry Pi:n

Steg-för-steg-guide för Raspberry Pi 5 (8 GB) med nyinstallerat **Raspberry Pi OS Bookworm** som startar till konsol och är ansluten till wifi.

**Du kör alla kommandon själv.** Varje steg förklarar *varför*, så att du kan stå för varje del. Gör ett steg i taget och kontrollera att det fungerar innan du går vidare.

I guiden står `<du>` för ditt användarnamn. Byt ut det överallt.

## Så uppdateras Pi:n automatiskt

Pi:n **hämtar** själv uppdateringarna. Det sker genom GitHub-runnern (steg 5):

1. Runnern är ett litet program som håller en utgående anslutning till GitHub öppen och frågar om det finns jobb.
2. När du pushar till `main` får runnern jobbet direkt. Den hämtar koden och kör [scripts/pi-deploy.sh](../scripts/pi-deploy.sh), som kopierar appen och startar om tjänsten.
3. Resultatet och loggen syns i GitHub under **Actions**, och statussidan på lennart.cam visar vilken commit Pi:n kör.

Eftersom Pi:n bara tar kontakt utåt behöver inga portar öppnas, och det fungerar likadant på wifi som på 4G.

**Alternativet** vore en timer på Pi:n som kör `git pull` med några minuters mellanrum. Det är enklare, men ger ingen logg i GitHub och uppdaterar med fördröjning. Därför används runnern.

**Det du behöver göra på Pi:n:** steg 1–7 nedan, en gång. Efter det sker allt vid push.

---

## Steg 1 – Eget användarkonto och SSH-nyckel

**Varför:** Ett personligt konto gör att allt som händer på Pi:n kan knytas till dig. Med SSH-nyckel i stället för lösenord kan bara den dator som har den privata nyckeln logga in. Det skyddar mot gissade lösenord. Nyckeln skapas på *din dator*, och den privata delen lämnar aldrig datorn.

**1a. Skapa kontot (på Pi:n).** Hoppa över det här om kontot du skapade vid första start redan är ditt eget.

```bash
sudo adduser <du>
```

Ge kontot rätt att använda sudo, kameran (`video`), GPIO och modemets serieport (`dialout`):

```bash
sudo usermod -aG sudo,video,gpio,i2c,spi,dialout <du>
```

**1b. Slå på SSH (på Pi:n):**

```bash
sudo systemctl enable --now ssh
```

Ta reda på Pi:ns IP-adress på wifi:

```bash
hostname -I
```

**1c. Skapa en nyckel (på din dator)**, om du inte redan har en `~/.ssh/id_ed25519`:

```bash
ssh-keygen -t ed25519 -C "lennart-pi"
```

Kopiera den publika nyckeln till Pi:n:

```bash
ssh-copy-id <du>@<pi-ip>
```

Testa att du kommer in utan lösenord:

```bash
ssh <du>@<pi-ip>
```

**1d. Stäng av lösenordsinloggning över SSH (på Pi:n).** Gör det först när 1c fungerar, annars låser du ute dig själv.

```bash
echo "PasswordAuthentication no" | sudo tee /etc/ssh/sshd_config.d/10-lennart.conf
```

```bash
sudo systemctl restart ssh
```

Öppna ett **nytt** terminalfönster och testa `ssh <du>@<pi-ip>` igen innan du stänger det gamla.

✅ **Klart när:** du loggar in med SSH utan att få frågan om lösenord.

---

## Steg 2 – Värdnamn

**Varför:** Ett eget namn gör att Pi:n känns igen i nätverket, i GitHub-runnerlistan och i loggar. `raspi-config` uppdaterar både värdnamnet och `/etc/hosts` på en gång, så att `sudo` inte klagar på ett okänt värdnamn.

```bash
sudo raspi-config nonint do_hostname lennart
```

```bash
sudo reboot
```

✅ **Klart när:** `hostname` visar `lennart`. Du kan då också nå Pi:n med `ssh <du>@lennart.local` på samma nät.

---

## Steg 3 – Uppdateringar och verktyg

**Varför:** En nyinstallerad Pi har ofta flera veckor gamla paket, och säkerhetsfixar ska in innan den kopplas mot internet på riktigt. `full-upgrade` tar också med paket som byter beroenden, till exempel kärnan. Verktygen behövs av deploy-skriptet: `git` för koden, `rsync` för att kopiera den, och `python3-venv` för Python-miljön.

```bash
sudo apt update
```

```bash
sudo apt full-upgrade -y
```

```bash
sudo apt install -y git rsync python3-venv curl
```

```bash
sudo reboot
```

**Automatiska säkerhetsuppdateringar** rekommenderas, eftersom Pi:n ska stå ute utan tillsyn:

```bash
sudo apt install -y unattended-upgrades
```

Över 4G kostar nedladdningar data. Säkerhetsuppdateringar är dock oftast små.

✅ **Klart när:** `sudo apt update` säger att alla paket är uppdaterade.

---

## Steg 4 – Kamera och skärm

**Varför:** Kameran och skärmen behöver drivrutiner och bibliotek innan appen kan använda dem. Allt installeras med `apt`, alltså Raspberry Pi OS egna paket. De är byggda för just Pi 5, och `picamera2` finns inte som vanligt pip-paket för Pi:ns kamera. SPI är bussen som skärmen pratar över, och den är avstängd från början.

**4a. Slå på SPI:**

```bash
sudo raspi-config nonint do_spi 0
```

(`0` betyder "på" i raspi-config.)

**4b. Installera biblioteken.** `--no-install-recommends` hoppar över grafiska tillägg som inte behövs på en Pi utan skrivbord.

```bash
sudo apt install -y python3-picamera2 python3-spidev python3-gpiozero python3-lgpio python3-pil python3-numpy fonts-dejavu-core --no-install-recommends
```

| Paket | Till |
|---|---|
| `python3-picamera2` | Kameran |
| `python3-spidev` | SPI till skärmen |
| `python3-lgpio` | Styrpinnarna DC, RST och BL. Fungerar på Pi 5. (`python3-gpiozero` installeras också inför servona, men skärmen använder lgpio direkt.) |
| `python3-pil` | Text på skärmen |
| `python3-numpy` | Räkna om bilden till skärmens färgformat |
| `fonts-dejavu-core` | Typsnittet för texten |

**4c. Stäng av och koppla in.**

```bash
sudo poweroff
```

Dra ur strömmen och koppla skärmen och kameran enligt [koppling-display.md](koppling-display.md). Läs avsnittet om kamerakabeln först. Starta sedan Pi:n igen.

**4d. Testa kameran:**

```bash
rpicam-hello --list-cameras
```

Kameran ska synas i listan, till exempel som `imx708_wide`.

```bash
ls /dev/spidev0.0
```

Filen ska finnas. Det betyder att SPI är på.

✅ **Klart när:** kameran syns i listan och `/dev/spidev0.0` finns. Skärmen testas i steg 8, när appen deployas.

---

## Steg 5 – GitHub-runnern som tjänst

**Varför:** Runnern är ett litet program från GitHub som *frågar* GitHub om det finns jobb. Den tar bara kontakt utåt, så inga portar behöver öppnas, och det fungerar likadant på wifi som på 4G bakom operatörens NAT. Etiketten `pi` gör att bara jobb som uttryckligen ber om Pi:n hamnar här.

**5a. Säkerhetsinställning i GitHub (gör först).** Repot är publikt. Gå till **Settings → Actions → General** och välj under rubriken för godkännande av workflows från forkar **"Require approval for all outside collaborators"**. Exakt formulering kan skilja sig något i GitHubs gränssnitt. Det betyder att ingen utomstående kan få ett workflow att köra utan att du godkänt det. Vårt deploy-workflow körs dessutom bara på push till `main`.

**5b. Hämta runnern.** Gå till **Settings → Actions → Runners → New self-hosted runner**, välj **Linux** och **ARM64**. Kör kommandona under *Download* på Pi:n, i ditt eget konto (inte root). GitHub visar rätt version och kontrollsumma där.

**5c. Registrera runnern.** Kör `config.sh` med token från samma sida, men lägg till namn och etikett:

```bash
./config.sh --url https://github.com/marcusandelius/lennart --token <TOKEN-FRÅN-SIDAN> --name lennart-pi --labels pi --unattended
```

Token från sidan gäller bara i en timme och bara för att registrera runnern. Den ska inte sparas någonstans.

**5d. Installera som tjänst**, så att runnern startar vid varje uppstart. Den körs som ditt konto:

```bash
sudo ./svc.sh install <du>
```

```bash
sudo ./svc.sh start
```

```bash
sudo ./svc.sh status
```

✅ **Klart när:** runnern syns som **Idle** med etiketten `pi` under Settings → Actions → Runners.

---

## Steg 6 – systemd-tjänsten för appen

**Varför:** systemd startar appen vid uppstart och startar om den om den kraschar. Vi kör den som *användartjänst* under ditt konto. Då behöver deploy-jobbet aldrig `sudo`, och runnern får inga root-rättigheter. "Linger" gör att dina användartjänster körs även när du inte är inloggad, och direkt efter omstart.

```bash
sudo loginctl enable-linger <du>
```

Själva tjänstefilen (`deploy/pi/lennart.service`) installeras automatiskt av deploy-jobbet, så den behöver du inte kopiera.

✅ **Klart när:** `loginctl show-user <du> --property=Linger` visar `Linger=yes`.

---

## Steg 7 – .env med hemligheter

**Varför:** Adresser och nycklar ska inte ligga i det publika repot. De läggs i en fil som bara ditt konto kan läsa, utanför mappen som deploy skriver över. Tjänsten läser filen när den startar.

```bash
mkdir -p ~/.config/lennart
```

```bash
chmod 700 ~/.config/lennart
```

```bash
nano ~/.config/lennart/.env
```

Skriv in nycklarna från [deploy/pi/env.example](../deploy/pi/env.example):

```
LENNART_SERVER_URL=https://lennart.cam
LENNART_DEVICE_TOKEN=<samma nyckel som i Coolify>
```

Enhetsnyckeln skapar du en gång, på Pi:n eller din dator. Den ska vara lång och slumpmässig:

```bash
openssl rand -hex 32
```

Samma nyckel läggs in som miljövariabel i Coolify (se [SETUP-COOLIFY.md](SETUP-COOLIFY.md)). Den ska **inte** in i GitHub eller i repot. Spara och lås sedan filen:

```bash
chmod 600 ~/.config/lennart/.env
```

✅ **Klart när:** `ls -l ~/.config/lennart/.env` visar `-rw-------`.

---

## Steg 8 – Test av hela kedjan

**Varför:** Vi vill se att en push till `main` faktiskt hamnar på Pi:n och att tjänsten startar, innan den riktiga appen läggs in.

1. Gör en push till `main` (eller slå ihop arbetsgrenen till `main`).
2. Följ jobbet under **Actions → Deploy**. Jobbet **Raspberry Pi → systemd** ska bli grönt. Jobbet **Webbdelen → Coolify** blir grönt men visar varningen "Coolify-secrets saknas ännu" tills secrets finns, och det är väntat.
3. Kontrollera på Pi:n:

```bash
systemctl --user status lennart
```

```bash
journalctl --user -u lennart -n 20 --no-pager
```

Du ska se raderna "Skärmen är igång", "Kameran är igång" och "Heartbeat: kontakt med servern".

På skärmen ska kamerabilden synas live, med en statusrad överst: en grön prick betyder kontakt med lennart.cam. På https://lennart.cam ska det stå "Stationen är igång", med samma version (commit) som i GitHub.

4. Testa omstart: `sudo reboot`. Logga in igen och kör `systemctl --user status lennart`. Tjänsten ska vara igång utan att du gjort något.

✅ **Klart när:** tjänsten kör efter en push och efter en omstart.

---

## Steg 9 – Servokortet (när PCA9685 har kommit)

**Varför:** Servokortet tar emot kommandon över I2C, en tvåtrådsbuss på stiften 3 och 5. I2C är avstängt från början, precis som SPI var. Python behöver paketet `smbus` för att prata I2C, och `i2c-tools` ger kommandot `i2cdetect`, som visar om kortet svarar.

**9a. Slå på I2C och installera paketen:**

```bash
sudo raspi-config nonint do_i2c 0
```

```bash
sudo apt install -y python3-smbus i2c-tools
```

**9b. Stäng av och koppla in** enligt [koppling-servon.md](koppling-servon.md):

```bash
sudo poweroff
```

**9c. Starta igen och kontrollera att kortet svarar:**

```bash
i2cdetect -y 1
```

Talet `40` ska synas i tabellen. Det är kortets adress.

Appen behöver inte startas om: den letar efter kortet varje gång ett servokommando kommer.

✅ **Klart när:** `40` syns, och adminvyn på lennart.cam visar `✓ PCA9685 på I2C-buss 1` under Servon efter att du tryckt på **Flytta**.

---

## Steg 10 – ffmpeg för inspelning av klipp

Pi:n kan spela in klipp när något rör sig framför kameran. Klippen blir underlag för att testa och kanske träna bildigenkänningen. Appen räknar själv ut när något rör sig, men själva videofilen (MP4) görs av programmet **ffmpeg**, som inte finns på Pi:n från början.

**10a. Kontrollera om ffmpeg redan finns:**

```bash
ffmpeg -version
```

*Varför:* ffmpeg packar kamerabilderna till H.264-video, så att ett klipp på en minut blir några MB i stället för flera GB. Det följer med Raspberry Pi OS med skrivbord, men inte med Lite. Marcus Pi rapporterade 2026-11-18 att ffmpeg fanns. Visar kommandot en version är du klar med 10a–10b.

**10b. Bara om det står `command not found`:** installera ffmpeg och starta om appen, så att den hittar det.

```bash
sudo apt install -y ffmpeg
```

```bash
systemctl --user restart lennart
```

**10c. Slå på inspelningen** på lennart.cam/admin, under **Inspelning vid rörelse**: kryssa i **Spela in när något rör sig** och tryck **Spara**.

✅ **Klart när:** kortet visar `✓ Lär in bakgrunden` och efter några sekunder `✓ Väntar på rörelse`. Vifta med handen framför kameran. Efter cirka 10 sekunder ska raden visa `1 klipp sedan start`, och strax efter syns klippet under **Klipp** i adminvyn.

**Bra att veta:**
- Klippen sparas först i `~/lennart-data/clips` på Pi:n och laddas sedan upp. Där ligger de högst 5 GB innan de äldsta uppladdade tas bort. Gränsen kan ändras med `LENNART_CLIP_LOCAL_GB` i `.env`.
- Blir det många tomma klipp av blad och skuggor: höj **Rörelsegräns** i adminvyn. Missas djur: sänk den.
- Inget spelas in när det är mörkt. Gränsen heter **Lägsta ljusstyrka**.
- Klippen kan visa personer. De syns bara i adminvyn och ska aldrig läggas i repot.

---

## Senare: över till 4G

Runnern och appen behöver ingen ändring, eftersom båda tar bara kontakt utåt. Klippen från inspelningen kan däremot dra mycket mobildata: sänk upplösningen till 640 × 360 eller stäng av inspelningen i adminvyn innan Pi:n går över till 4G. SSH från din dator når däremot inte Pi:n över 4G, eftersom operatören normalt delar IP-adresser bakom NAT. Vill du kunna logga in på distans tar vi det som ett eget beslut.
