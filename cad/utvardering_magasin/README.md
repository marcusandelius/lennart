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
