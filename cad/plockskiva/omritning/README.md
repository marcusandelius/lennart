# Omritning av plockskivan (pågår)

Kontrollen den 25 november visade att delarna i mappen ovanför inte går att montera. Här ligger underlaget för omritningen.

## Vad som sitter i vägen (husets ram, mm, framsidan är -y)
Uppmätt i husmodellen med `skymap.py` (lägsta hinder ovanför varje punkt) och `insert.py` (lyft rakt upp i steg).

| Hinder | Läge |
|---|---|
| Skärmklämma | x ±38, y 4,5–21, z 87–129. Ramen sitter vid y 17–21 med en öppning x ±24, z 95–121 för kontakterna |
| Kamerasläde | x ±26,5, y 7–26, z från 145 |
| Kameraklackar i kroppen | x ±(20–26,5), y upp till 17,5, z från 153 |
| Skärmklackar i kroppen | x ±(30–38), y upp till 17,5, z från 91 |
| Ellåda | x ±66, y från 113, z 74–170 |
| Ellådans lock | x ±68,5, y från 110,5, z från 164 |
| Magnetklackar | x från ±72–74,5, z från 143. På höger sida även en ribba från z 44 vid x från 73 |
| Skärmens kontakter (antagande) | kretskortets baksida vid y 12, stiftlist 8,5 mm, Dupont-hus 14 mm: stela delar till y ca 34,5, rader vid z ca 99 och 117 |

Fri öppning rakt uppifrån mitt i huset: y 26–110,5 (84,5 mm). Den gamla skivan är Ø93,2.

## Riktning
* Skiva Ø85,2 (fickans mittradie 28 i stället för 32), mitt vid (-13, 65,5, 57), utfall vid 65 grader.
* Stativet får en kant runt skivan upp till strax över skivans ovansida. Förrådet börjar där och kan då lyftas rakt upp.
* Förrådets bakvägg rak vid y 106,2–108,6, framvägg vid y 28,5 eller längre bak bakom skärmen.
* Omrörare på skivans axel.

## Simuleringar (40 nötter, vila 0,3 s)
`r1.jsonl`, `r2.jsonl`: mindre skiva utan omrörare. I 10 av 16 körningar blev nötter kvar: nötterna valvade sig ovanför skivan
och matningen stannade med 1–31 nötter kvar (bild `valv_utan_omrorare.png`).
`r3.jsonl`: samma mått med ett blad på skivans axel (halv längd 15 mm, 48–76 mm över plattan).
8 av 8 körningar tömde förrådet. Kvar att trimma: 19 stopp på vägen upp och 26 dubbeldoser på 323 slag.

Inget i den här mappen är ritat som utskriftsfiler ännu.

## Utfall
Omritningen är klar och ligger i mappen ovanför (fem delar). Varianten med raka skärmkontakter och ett urtag i
förrådet bakom skärmen fungerade inte i simuleringen: förrådet blev för smalt och omröraren låste sig eller lämnade
nötter kvar. Den ritade varianten kräver därför att skärmens kontakter ligger längs kortet (högst 27 mm in från väggen).
Två fel i den första utskickade versionen hittades också under arbetet: stativets platta hade ett stort hål över
hela rännan (flera nötter hade kunnat falla igenom per slag), och rännan under utfallet var för låg i den ritade
delen jämfört med den simulerade.
