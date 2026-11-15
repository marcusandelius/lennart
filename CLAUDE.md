# CLAUDE.md – regler för alla sessioner i det här repot

Det här repot är Marcus bidrag till SweClockers/ASUS-tävlingen **"Gick inte. Nu går det."**
Repot är **publikt**. Läs hela filen innan du gör något.

## Viktiga datum

| Vad | Datum |
|---|---|
| Tävlingsstart (gräns för "före tävlingen") | 16 okt 2026 |
| Sista inlämning (bidraget kan ändras fram till att röstningen öppnar) | 30 nov 2026 |
| Röstning | 1–13 dec 2026 |
| Underlag för tokens och AI-historik om bidraget är topp 3 | senast 15 dec 2026 kl. 23.59 |
| Vinnaren presenteras | 17 dec 2026 |

Villkoren finns på https://projekt.sweclockers.com/asus/villkor. Om något här verkar strida mot villkoren gäller villkoren. Säg i så fall till.

Enligt villkoren, som de återges i HANDOFF-filen (inte kontrollerat direkt mot sidan) [verifiera], ska bidraget:
- visa vad som fanns före och vad som gjorts med AI från 16 oktober;
- ange använda modeller, verktyg och bibliotek;
- redovisa tokens, uppdelat på lokalt och i molnet, med en kort förklaring av hur de räknats.

## Projektet i korthet

**Lennarts matstation:** ett 3D-utskrivet falurött hus på uteplatsen i vilket en kamera känner igen ekorren Lennart. Raspberry Pi 5 släpper då ut en hasselnöt via ett servostyrt doseringshjul. Andra djur nekas, och skärmen visar ACCESS GRANTED eller ACCESS DENIED. Webbdelen på Coolify blir besökslogg och publik besöksliggare. Detaljer finns i `docs/` och i `docs/historik/`.

## Regler

1. **Svenska.** Allt som syns i bidraget skrivs på svenska: README, dokumentation, texter i gränssnittet, felmeddelanden som visas för användare och commit-meddelanden. Kod (variabelnamn, funktionsnamn) får vara på engelska.

2. **Marcus bestämmer och kör allt på Pi:n.** Claude kör aldrig kommandon på Raspberry Pi:n och loggar aldrig in på den.
   - Ge ett steg i taget och vänta på "klart" innan nästa steg.
   - Förklara **varför** för varje kommando och varje val, så att Marcus kan stå för varje del inför jury och publik.
   - Föreslå, men bestäm inte. Vid vägval: ge en rekommendation och vänta på beslut.

3. **TOKENS.md efter varje arbetspass.** Lägg till en rad med:
   datum · vad vi gjorde · tokens i molnet (exakt eller uppskattat, och **hur** det togs fram) · tokens lokalt.
   Om du inte kan läsa av exakt förbrukning: skriv "uppskattat" och beskriv metoden. Hitta aldrig på exakta siffror.

4. **FORE-TAVLINGEN.md.** Allt som fanns före **16 okt 2026** (kod, idéer, modeller, bilder, 3D-filer, hårdvara, research) förs in där med datum och källa.

5. **KALLOR.md.** Varje bibliotek, modell, verktyg, lånad resurs (bilder, ljud, typsnitt, 3D-modeller, kodsnuttar) och all hjälp Marcus fått (personer, AI-sessioner, forumtrådar) förs in där med licens och länk. Lägg till posten i samma commit som det nya beroendet.

6. **Inga hemligheter i repot.** API-nycklar, tokens och lösenord hamnar aldrig i en commit, inte heller i exempel, loggar eller skärmdumpar.
   - CI/deploy: **GitHub Secrets**.
   - Raspberry Pi: `.env`-fil på Pi:n (se `docs/SETUP-PI.md`). `.env` står i `.gitignore`.
   - Mallar heter `.env.example` och innehåller bara tomma nycklar.
   - Om en hemlighet ändå hamnar i chatten eller repot: säg till direkt, och påminn om att den ska bytas (roteras).

7. **Bilder på personer** läggs bara in om personen har gett sitt samtycke. Notera samtycket i KALLOR.md (vem, när, hur, ej kontaktuppgifter). Är du osäker: lägg inte in bilden.

8. **Säkerhet i GitHub Actions.** Repot är publikt och Pi:n kör en self-hosted runner.
   - Workflows som använder `runs-on: [self-hosted, ...]` får **aldrig** triggas av `pull_request`, `pull_request_target`, `issue_comment` eller andra händelser som utomstående kan starta. Bara `push` till `main`.
   - Varje sådant jobb har även villkoret `if: github.repository == 'marcusandelius/lennart'`.
   - Lägg aldrig till `workflow_dispatch` eller nya triggers på Pi-jobb utan att Marcus uttryckligen bett om det.

9. **Påhitta inte.** Siffror, namn, datum, citat och källor som inte går att belägga markeras `[osäkert]` eller `[verifiera]`.

10. **Små commits** med beskrivande meddelanden på svenska. De är Marcus daterade historik i tävlingen.

## Struktur

```
CLAUDE.md            – den här filen
README.md            – bidraget: vad, hur, bygge (+ plats för personlig kod)
TOKENS.md            – tokenlogg per arbetspass
FORE-TAVLINGEN.md    – allt som fanns före 16 okt 2026
KALLOR.md            – källor, licenser, hjälp, samtycken
docs/                – beslut, research, guider
docs/historik/       – HANDOFF-filer från tidigare chattar, orörda
docs/beslut/         – beslutslogg och beslutsunderlag
model/               – 3D-modellen i Python (ordagrant ur HANDOFF)
web/                 – förhandsgranskning, besöksliggare-demo, minihus
trailer/             – underlag för trailern i Blender
tools/               – hjälpskript, t.ex. extract_from_html.py
pi/                  – programvaran på Raspberry Pi:n (än så länge en testapp)
deploy/pi/           – systemd-tjänst och mallar för Pi:n
scripts/             – skript som körs av deploy
.github/workflows/   – deploy till Coolify och Pi
```

## Öppna beslut

- Var bildigenkänningen körs: se `docs/beslut/bildigenkanning.md`. **Inget byggs förrän Marcus beslutat.**
- Övriga öppna frågor: `docs/att-gora.md`.

## Bra att veta

- Filerna i `model/` och `web/` är ordagranna ur HANDOFF-filen. Ändra dem bara med ett tydligt commit-meddelande, så att det syns vad som gjorts i chatten och vad som gjorts här.
- Geometridatan (`parts_v*.json`) och STL-filerna finns inte i repot. De återskapas med `tools/extract_from_html.py` ur den publicerade förhandsgranskningen.
- Nya beslut läggs till i `docs/beslut/beslutslogg.md` med datum och skäl.
