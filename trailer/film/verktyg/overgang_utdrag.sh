#!/usr/bin/env bash
# Projekt Lennart - gor ett utdrag (13,8-21,5 s i hela filmen) for ett forslag pa overgangen titel -> 1.1 ur titel_overgangar.py.
# Slutet av 0.5 och borjan av 1.1 tas ur hela filmen, titeln och overgangen ur forslagets rutor. Ljudet ar filmens, plus forslagets egna smaljud.
# Byggs i separata steg (tre bilddelar, ljud, ihopslagning): en enda ffmpeg-korning med samma fil som tre ingangar hangde sig.
# Mellanfiler hamnar i overgangar/tmp_v<N>/ och skrivs over nasta gang.
# Kor (fran film/):  bash verktyg/overgang_utdrag.sh <variant 1-5> <utfil.mp4>
set -e
V=$1; UT=$2; D=overgangar/v$V; E=$(cat $D/efter.txt); FILM="Lennart - hela filmen 720p.mp4"; FX=ljud/fx
S0=13.8; T11=18.08; SLUT=21.5
B=$(awk "BEGIN{print $T11 + $E/25}")
T=overgangar/tmp_v$V; mkdir -p $T
KOD=(-an -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -r 25)
ffmpeg -v error -y -nostdin -ss $S0 -i "$FILM" -t 1.48 "${KOD[@]}" $T/a.mp4
ffmpeg -v error -y -nostdin -framerate 25 -i $D/%04d.jpg "${KOD[@]}" $T/b.mp4
ffmpeg -v error -y -nostdin -ss $B -i "$FILM" -t $(awk "BEGIN{print $SLUT-$B}") "${KOD[@]}" $T/c.mp4
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > $T/lista.txt
# smaljud: fil, tid i utdraget (s), niva (dB). Tiderna raknas fran titelns borjan (0.6) + 1,48 s
declare -a L=()
case $V in
  1) i=0; for t in 1.97 2.05 2.12 2.19 2.25 2.31 2.37 2.43 2.49 2.55 2.61 2.67; do f=(tick_001 tick_002 tick_004); L+=("${f[$((i%3))]} $(awk "BEGIN{print $t+1.48}") $((-31 - i%3))"); i=$((i+1)); done ;;
  2) L+=("impactGeneric_light_002 $(awk "BEGIN{print 2.80+1.48}") -26") ;;
  3) L+=("glitch_001 $(awk "BEGIN{print 2.56+1.48}") -31" "glitch_002 $(awk "BEGIN{print 2.80+1.48}") -27" "glitch_001 $(awk "BEGIN{print 3.30+1.48}") -34") ;;
  4) L+=("tick_002 $(awk "BEGIN{print 2.30+1.48}") -30" "impactPlate_medium_001 $(awk "BEGIN{print 2.80+1.48}") -21" "impactGeneric_light_000 $(awk "BEGIN{print 2.80+1.48}") -24") ;;
  5) L+=("click_002 $(awk "BEGIN{print 1.95+1.48}") -31" "impactGeneric_light_003 $(awk "BEGIN{print 2.27+1.48}") -28") ;;
esac
ffmpeg -v error -y -nostdin -ss $S0 -i "$FILM" -t $(awk "BEGIN{print $SLUT-$S0}") -vn -c:a pcm_s16le -ar 48000 -ac 2 $T/m.wav
IN=(-i $T/m.wav); FC=""; MIX="[0:a]"; n=1
for l in "${L[@]}"; do set -- $l; IN+=(-i $FX/$1.wav); ms=$(awk "BEGIN{printf \"%d\", $2*1000}"); FC+="[$n:a]volume=${3}dB,adelay=${ms}|${ms},aformat=sample_rates=48000:channel_layouts=stereo[x$n];"; MIX+="[x$n]"; n=$((n+1)); done
FC+="${MIX}amix=inputs=$n:normalize=0:duration=first[au]"
ffmpeg -v error -y -nostdin "${IN[@]}" -filter_complex "$FC" -map "[au]" -c:a pcm_s16le $T/ljud.wav
ffmpeg -v error -y -nostdin -f concat -safe 0 -i $T/lista.txt -i $T/ljud.wav -map 0:v -map 1:a -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart "$UT"
echo "$UT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$UT") s"
