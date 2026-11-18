# Det som återstår och öppna frågor

Hämtad ur [HANDOFF-filen](historik/HANDOFF-lennarts-matstation-projekt.md), avsnitt 5, läget 2026-11-15. Bocka av och lägg till här när saker blir klara.

## Nästa steg i utskriften

1. **Toleranstestet:** värdera insatserna M3 och M4, tapparna Ø2,8 och Ø2,4, nockkilen, nötmallen och magnetfickan när magneter finns. Justera vid behov kroppens tappar och klackar innan den nya kroppen skrivs ut.
2. **Den nya kroppen** i rött och grått, cirka 10–13 timmar enligt min osäkra uppskattning. Sedan de nio vita detaljerna på en egen platta.
3. **Elektroniktest i den gamla kroppen:** kamerafäste, skärmklämma och skärmram, med Pi 5, kameran och skärmen.
4. **Mätning:** mät servot på 11 kg med sitt runda horn, mikroservot, skärmkortet, LED-ringen och kameran. Justera sedan fästena.
5. **Doseringen** (doserhus, hjul och magasin) när servot är uppmätt. Provkör med riktiga hasselnötter, gärna 200 varv. Det är bygget viktigaste prov.
6. **Resten av plattorna** enligt fliken Utskrift: tak, gräsmattor, framgård, skål, lucka, blomlådor, stuprör och TPU-packningar.

## Programvara, inte påbörjad

- **Igenkänning:** ekorre eller annat djur, 2–3 bilder per besök, hög tröskel och läget VERIFIERAR vid osäkert svar. Att det sker i molnet bestämdes tidigt, men tjänst och modell är [osäkert].
- **Svarstid:** ungefär 5 sekunder från landning till svar.
- **Servostyrning via PCA9685:** hjulet vrids 130° och tillbaka. Ett litet "vick" fram och tillbaka före utmatningen. Kort tidsgräns, backa och försök igen, och varning efter flera misslyckade försök, så att servot inte står och tar i.
- **Luckan** stängs långsamt och bara när kameran inte har sett rörelse på några sekunder, så att Lennart inte kläms.
- **Skärmen:** väntar, VERIFIERAR, ACCESS GRANTED, ACCESS DENIED och tomt magasin.
- **Besökslogg** med bild och tid, incidentrapport vid nekat besök och en dashboard i säkerhetscentralstil som stannar i hemnätet.
- **Publik besöksliggare och domän.** Förslag: notkontrollen.se (Marcus favorit), lennart.security, besoksliggaren.se, ekorrvakten.se och accessgranted.nu. Om de är lediga och vad de kostar är [osäkert]. Publicera bara bilder som klassats som djur. GDPR behöver stämmas av med någon som kan reglerna, eftersom det är en juridisk fråga.
- **Uppstart och drift:** programmet ska starta av sig självt efter strömavbrott (systemd), och Pi:n ska vara på dygnet runt.

## Öppna frågor

- Vilket nät går SIM-kortet på, och stöder modemet de LTE-banden?
- Passar kamerakabeln från Electrokit Pi 5:s smala kontakt?
- Vad är pedestalen gjord av, och hur ska den fästas i väggen?
- Räcker ljuset för kameran på novembermorgnar? LED-ringen är köpt men inte inritad.
- Ska resten av huset vara PETG eller ASA? Plattorna i förhandsgranskningen är märkta ASA. PETG tål sol och värme sämre över tid.
- Hur sitter kamerakragen, som saknar tappar och bara har en tät ficka? Fönsterramarnas tappar sitter bara upptill, och blomlådorna hänger på fönsterbrädan.
- Skjuver servot faktiskt av en nöt som fastnat? Kraften vid hjulets kant är beräknad till cirka 35 N, men det är inte provat.
- Kommer Lennart att klättra i repstegen? Inte provat.
- Kompletteringar till inköpslistan: M2-skruvar till kameran, PCA9685, 12 V-adapter och kabel, 4G-modem, magneter, ventilationspluggar, glas och plast, silikon, tejp, vinkeljärn och hasselnötter.
- Projektdokumentet i Claude Docs behöver uppdateras med PETG, de nya plattnumren, Electrokit-köpet och den nya kroppen.
- Vid flerfärgsutskrifter: gör rensningstornet bredare så att det inte välter.
- Tävlingen: bidraget ska vara inlämnat senast 30 november 2026. Underlag för tokens och AI-historik ska kunna visas om bidraget hamnar bland de tre med flest röster, senast 15 december kl. 23.59.

## Tillagt i Claude Code-sessionerna

- **Livebilden är publik:** låt någon som kan reglerna bedöma om en publik livebild från uteplatsen är förenlig med GDPR, och vad som gäller om personer kommer i bild [kräver granskning]. Fram till dess: stäng av livebilden i adminvyn när någon som inte vill synas är vid uteplatsen.
- **Coolify:** lägg till `ADMIN_PASSWORD` och en volym på `/data` (se docs/SETUP-COOLIFY.md).
- **Inspelning vid rörelse (2026-11-18):** installera ffmpeg på Pi:n (SETUP-PI steg 10) och slå på inspelningen i adminvyn innan uppställningen ställs ut. Prova fram rörelsegränsen på plats.
- **Klippen kan visa personer:** de syns bara i adminvyn, men om de får sparas och användas för träning bör stämmas av mot GDPR [kräver granskning]. Lägg aldrig klipp i repot. Radera klipp med personer om de inte behövs.
- **LED-ringen:** kopplas in senare, så att det går att spela in även i skymning och mörker.
- **Märk klippen** under helgen och veckan, så att det finns ett facit när modeller för igenkänning ska provas.
