# Sätta upp webbdelen i Coolify och lennart.cam i Cloudflare

Webbdelen ligger i [server/](../server/) och byggs av Coolify från [server/Dockerfile](../server/Dockerfile). GitHub Actions ber Coolify bygga om vid varje push till `main`.

Menyer och knappar i Coolify byter ibland namn mellan versioner. Det som är märkt [verifiera] ska kontrolleras mot din version.

---

## 1. Skapa appen i Coolify

1. **Projects → + Add**, och döp projektet till `Lennart`. Välj miljön `production`.
2. **+ New → Public Repository.** Repot är publikt, så Coolify behöver ingen inloggning mot GitHub.
   - Repository URL: `https://github.com/marcusandelius/lennart`
   - Branch: `main`
   - Build Pack: **Dockerfile**
   - Base Directory: `/server`. Det gör att Coolify bara bygger webbdelen, inte hela repot.
   - Ports Exposes: `8000`
3. **Domains:** `https://lennart.cam`. Med `https://` framför hämtar Coolify ett gratis certifikat från Let's Encrypt.

**Varför "Public Repository":** det ger Coolify läsrätt utan att du behöver koppla ett GitHub-konto. Coolify behöver bara läsa koden.

## 2. Miljövariabel med enhetsnyckeln

Under **Environment Variables**, lägg till:

| Namn | Värde | Kommentar |
|---|---|---|
| `LENNART_DEVICE_TOKEN` | Nyckeln från `openssl rand -hex 32` | Samma värde som i `.env` på Pi:n. **Inte** "Build Variable", den behövs bara när appen körs [verifiera namn på rutan]. |

**Varför här och inte i GitHub:** nyckeln används av appen när den körs, inte av GitHub Actions. Den ska bara finnas på två ställen: i Coolify och i `.env` på Pi:n.

## 3. Hälsokontroll och deploy

- **Healthcheck:** sökväg `/healthz`, **port `8000`**. Coolify ser då om appen faktiskt svarar efter en deploy. Står porten kvar på 80 misslyckas kontrollen, eftersom appen lyssnar på 8000. Coolify kör kontrollen med `curl` inuti containern, och därför installeras `curl` i Dockerfile.
- **Ports Exposes** under General ska också vara `8000`. Annars skickar Coolify trafiken från lennart.cam till fel port.
- **Automatisk deploy från Coolify:** stäng av "Auto Deploy" under Advanced [verifiera]. Det är GitHub Actions som startar deployen, annars kan det bli två deployer per push.
- **Commit-nummer på statussidan (valfritt):** slå på "Include Source Commit in Build" under Advanced [verifiera]. Då visar lennart.cam vilken commit servern kör.
- Tryck **Deploy** en gång för hand och kontrollera att bygget blir grönt.

## 4. Uppgifterna som GitHub Actions behöver

Lägg in dem i GitHub under **Settings → Secrets and variables → Actions → New repository secret**. **De här tre räcker.** Pi-jobbet behöver inga secrets, eftersom runnern redan är inloggad och `.env` ligger på Pi:n.

| Secret | Vad | Var du hittar den |
|---|---|---|
| `COOLIFY_URL` | Adressen till **Coolify-panelen**, till exempel `https://coolify.dindoman.se`. Alltså inte lennart.cam. | Den adress du loggar in på Coolify med |
| `COOLIFY_TOKEN` | API-token | **Keys & Tokens → API Tokens → Create**, med rätten "deploy" [verifiera] |
| `COOLIFY_APP_UUID` | Appens id | I adressfältet när du står på appen i Coolify (`…/application/<uuid>`), eller i appens inställningar |

- **API-åtkomst** måste slås på i Coolifys inställningar, och om "Allowed IPs for API" är ifyllt måste GitHub Actions släppas in. Annars svarar Coolify `403 {"message":"You are not allowed to access the API."}` och jobbet blir rött. Det hände 2026-11-15. GitHubs servrar har många olika adresser, så lämna fältet tomt eller öppet. Token skyddar fortfarande API:et.
- **Coolify-panelen måste gå att nå från internet**, eftersom GitHubs servrar anropar den. Ligger panelen bakom IP-spärr eller Cloudflare Access fungerar deploy-anropet inte.
- Om en token någon gång hamnar i chatten, i en logg eller i repot: skapa en ny och ta bort den gamla.

## 5. lennart.cam i Cloudflare

1. **DNS → Add record:**
   - Typ `A`, namn `@` (alltså `lennart.cam`), värde = Coolify-serverns IP-adress.
   - Valfritt: typ `CNAME`, namn `www`, värde `lennart.cam`. Lägg i så fall också till `https://www.lennart.cam` under Domains i Coolify.
2. **Proxy-status: börja med "DNS only"** (grått moln).
   **Varför:** Coolify hämtar certifikatet från Let's Encrypt genom att svara på en kontroll via domänen. Det är enklast utan Cloudflare emellan.
3. När https://lennart.cam fungerar med giltigt certifikat kan du slå på **Proxied** (orange moln). Gör du det:
   - **SSL/TLS-läge: Full (strict).** Använd aldrig "Flexible", det ger en evig omdirigering eftersom Coolify själv skickar vidare till https.
   - **Bot Fight Mode måste vara av**, eller så behövs ett undantag för `/api/heartbeat`. Annars kan Cloudflare blockera Pi:ns rapporter, eftersom de inte kommer från en webbläsare.

## 6. Test

1. Öppna https://lennart.cam. Där ska det stå **"Ingen kontakt än"** tills Pi:n är igång.
2. Från din dator, med enhetsnyckeln:

```bash
curl -X POST https://lennart.cam/api/heartbeat -H "Authorization: Bearer <NYCKELN>" -H "Content-Type: application/json" -d '{"host":"test","message":"hej"}'
```

Svaret ska bli `{"ok": true}`, och sidan ska visa "Stationen är igång" i två minuter.

3. Pusha en ändring till `main` och följ **Actions → Deploy → Webbdelen → Coolify**. Jobbet ska bli grönt, och Coolify ska visa en ny deploy.

> Kommandot i punkt 2 innehåller nyckeln. Kör det i din egen terminal, och klistra inte in det med nyckeln i en chatt.
