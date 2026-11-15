# Sätta upp Raspberry Pi:n

Steg-för-steg-guide för Raspberry Pi 5 (8 GB) med nyinstallerat **Raspberry Pi OS Bookworm** som startar till konsol och är ansluten till wifi.

**Du kör alla kommandon själv.** Varje steg förklarar *varför*, så att du kan stå för varje del. Gör ett steg i taget och kontrollera att det fungerar innan du går vidare.

I guiden står `<du>` för ditt användarnamn. Byt ut det överallt.

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

## Steg 4 – GitHub-runnern som tjänst

**Varför:** Runnern är ett litet program från GitHub som *frågar* GitHub om det finns jobb. Den tar bara kontakt utåt, så inga portar behöver öppnas, och det fungerar likadant på wifi som på 4G bakom operatörens NAT. Etiketten `pi` gör att bara jobb som uttryckligen ber om Pi:n hamnar här.

**4a. Säkerhetsinställning i GitHub (gör först).** Repot är publikt. Gå till **Settings → Actions → General** och välj under rubriken för godkännande av workflows från forkar **"Require approval for all outside collaborators"**. Exakt formulering kan skilja sig något i GitHubs gränssnitt. Det betyder att ingen utomstående kan få ett workflow att köra utan att du godkänt det. Vårt deploy-workflow körs dessutom bara på push till `main`.

**4b. Hämta runnern.** Gå till **Settings → Actions → Runners → New self-hosted runner**, välj **Linux** och **ARM64**. Kör kommandona under *Download* på Pi:n, i ditt eget konto (inte root). GitHub visar rätt version och kontrollsumma där.

**4c. Registrera runnern.** Kör `config.sh` med token från samma sida, men lägg till namn och etikett:

```bash
./config.sh --url https://github.com/marcusandelius/lennart --token <TOKEN-FRÅN-SIDAN> --name lennart-pi --labels pi --unattended
```

Token från sidan gäller bara i en timme och bara för att registrera runnern. Den ska inte sparas någonstans.

**4d. Installera som tjänst**, så att runnern startar vid varje uppstart. Den körs som ditt konto:

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

## Steg 5 – systemd-tjänsten för appen

**Varför:** systemd startar appen vid uppstart och startar om den om den kraschar. Vi kör den som *användartjänst* under ditt konto. Då behöver deploy-jobbet aldrig `sudo`, och runnern får inga root-rättigheter. "Linger" gör att dina användartjänster körs även när du inte är inloggad, och direkt efter omstart.

```bash
sudo loginctl enable-linger <du>
```

Själva tjänstefilen (`deploy/pi/lennart.service`) installeras automatiskt av deploy-jobbet, så den behöver du inte kopiera.

✅ **Klart när:** `loginctl show-user <du> --property=Linger` visar `Linger=yes`.

---

## Steg 6 – .env med hemligheter

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

Använd nycklarna från [deploy/pi/env.example](../deploy/pi/env.example). Under test kan värdena vara tomma. Spara och lås sedan filen:

```bash
chmod 600 ~/.config/lennart/.env
```

✅ **Klart när:** `ls -l ~/.config/lennart/.env` visar `-rw-------`.

---

## Steg 7 – Test av hela kedjan

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

Du ska se raden "Lennart lever" med aktuell tid.

4. Testa omstart: `sudo reboot`. Logga in igen och kör `systemctl --user status lennart`. Tjänsten ska vara igång utan att du gjort något.

✅ **Klart när:** tjänsten kör efter en push och efter en omstart.

---

## Senare: över till 4G

Runnern och appen behöver ingen ändring, eftersom båda tar bara kontakt utåt. SSH från din dator når däremot inte Pi:n över 4G, eftersom operatören normalt delar IP-adresser bakom NAT. Vill du kunna logga in på distans tar vi det som ett eget beslut.
