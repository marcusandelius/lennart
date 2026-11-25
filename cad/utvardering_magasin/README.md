# Utvärdering av nötmagasin (simulering)

Fysiksimulering (MuJoCo) av olika magasin över doserhjulet. Nötterna är ellipsoider, 15–18,5 mm breda och
18–22 mm långa. Hjulet har samma mått som 11_doserhjul (radie 31, ficka 24,2 mm, djup 21,4 mm) och drivs av
ett servo med 1,0 Nm. Friktion 0,35 och 0,5. En cykel = ficka upp, 130 grader fram till tömning, tillbaka.

Kalibrering: dagens magasin i "handtest" (utan hjul) håller kvar 6–7 av 8 nötter, som på foto från 2026-11-25.

| Variant (funktion i designs.py) | Ryms | Levererade | Kommentar |
|---|---|---|---|
| Rakt rör, öppning 13 mm framtill (`L`, noflap) | 5 | 58 av 60 | 1–2 nötter per cykel, inga stopp |
| Rakt rör med fjädrande lapp (`L`) | 5 | 51 av 60 | 1 nöt per cykel, men stopp vid hög friktion |
| Skivmagasin, en nöt tjockt (`S`) | ca 14 | 40 av 112 | valv mellan framvägg och bakre golv |
| Spiralrör (`C3`) | ca 6 | 15 av 72 | fastnar i inloppet och på banan |
| Två rör efter varandra (`T2`) | 8 | 40 av 96 | hjulet kläms vid mellanväggen |
| Bred slits + fjädrande kant (`F`, xo=17) | ca 56 | 18 av 120 | nötterna kilar fast parvis i tratten |
| Brantare tratt 62 grader (`B`) | ca 48 | 6 av 120 | ingen förbättring |
| Dagens magasin (`A`) | ca 60 | 6 av 120 | valv över utloppet |
| Rör nederst + tratt ovanpå (`LT`) | – | 9 av 240 | valv i rörets inlopp |

Kör: `pip install mujoco`, skriv jobb som JSON-rader och kör `python3 batch.py ut.jsonl jobb.txt`, sedan `python3 summ.py ut.jsonl`.
Modellen är förenklad (stela kroppar, släta nötter). Rangordningen är trolig, procenttalen är ungefärliga.

## Ändrad mekanism: lutande plockskiva (discsim.py)

En skiva som lutar 45 grader, Ø92 mm och 16 mm tjock, med ett hål (26 mm) vid kanten. Hålet vrids ned i nöthögen,
tar med en nöt upp och släpper den genom ett utfall i bottenplattan högst upp. En skärm 26 mm över skivans övre halva
håller högen nere. Servo 1,0 Nm, 180 graders slag, 40 nötter per körning.

| Variant | Levererade | Tomma slag | Dubbla | Stopp |
|---|---|---|---|---|
| Hål 2 mm från kanten, vickning 40 grader i botten (`RP=32, wiggle=40`) | 70 av 70 | 2 av 72 | 0 | 0 |
| Samma utan vickning (`RP=32`) | 70 av 70 | 23 av 93 | 0 | 0 |
| Hål 4 mm från kanten (`RP=30`), 70 slag | 125 av 240 | många | 0 | 0 |

(5 av 40 nötter per körning hamnade utanför behållaren vid påfyllningen i simuleringen och räknas inte.)

Rörmagasinet förlängt till z = 188 rymmer 7 nötter (`L`, `ztube=188`).
