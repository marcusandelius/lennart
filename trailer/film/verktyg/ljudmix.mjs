// Projekt Lennart - ljudmixen: den inspelade rosten (bearbetad) laggs mot ratt klipp, musiken laggs under och dackas nar rosten talar.
// Kor:  node film/verktyg/ljudmix.mjs      (bygger forst arbetskopian, sedan film/ljud/mix.wav, och lagger mixen pa arbetskopian och pa klippen i storyboarden)
// Kallor: "full recording.m4a" (rosten), film/ljud/rostkedja.txt (EQ, de-esser, multibandkompressor, kompressor, limiter), film/verktyg/musik.py (musiken).
import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync, renameSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = dirname(fileURLToPath(import.meta.url)), P = resolve(HERE, '..', '..'), SB = join(P, 'storyboard'), LJ = join(P, 'film', 'ljud'); mkdirSync(LJ, { recursive: true });
const ff = a => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...a], { stdio: ['ignore', 'inherit', 'inherit'] });
const dur = f => +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString().trim();

// Replikerna: [klipp, sekunder in i klippet dar repliken borjar, start i inspelningen, slut i inspelningen]
const SEG = [
  ['0.1', 0.40, 0.40, 12.36],     // Okej, sa det har ar ett helt vanligt ... komponenter. (lopande over 0.1-0.4, som den ar inspelad)
  ['0.5', 0.45, 12.97, 13.93],    // Inget konstigt.
  ['0.6', 0.12, 15.12, 16.50],    // Det vaktar notter.
  ['1.1', 0.50, 19.75, 23.63], ['1.2', 0.25, 24.00, 27.56], ['1.3', 0.60, 28.24, 29.65], ['1.4', 0.50, 30.29, 37.30],
  ['2.1', 0.60, 39.38, 43.17], ['2.2', 0.50, 43.97, 47.07], ['2.3', 0.80, 47.60, 56.00],
  ['2.4', 1.60, 56.93, 65.83],    // Sjalva tanken ar enkel ... ar det har en ekorre?
  ['2.5', 0.30, 66.73, 68.84],    // Ar svaret nej? Ja da hander ingenting.
  ['2.6', 2.90, 70.67, 71.47],    // Ar svaret ja?
  ['2.6', 4.20, 71.88, 73.36],    // Da finns det plotsligt mat.
  ['3.1', 0.60, 74.95, 78.70], ['3.2', 0.30, 79.50, 89.66],
  ['4.1', 0.35, 92.05, 110.02],   // inkopen: scenen ar renderad efter den har tagningen (scenens tid = inspelningens tid - 91,7)
  ['5.1', 0.40, 113.15, 115.76], ['5.3', 0.40, 117.09, 122.47],
  ['6.1', 0.60, 126.15, 128.52],  // Sa har ser det ut. Jag namnde att det var manga delar.
  ['6.3', -1.50, 128.86, 133.25], // Men det var viktigt for Lennart ... (borjar strax innan huset ar fardigt). Slutar dar "honom" tystnar (under -50 dB vid 133,12)
  ['7.3', 0.50, 136.25, 146.83],
];

execFileSync('node', [join(HERE, 'arbetskopia.mjs')], { stdio: 'inherit' });
const cuts = JSON.parse(readFileSync(join(SB, 'arbetskopia.json'), 'utf8')), AK = join(SB, 'arbetskopia.mp4'), TOT = dur(AK), at = no => cuts.find(c => c[0] === no)[1];

const MU = join(LJ, 'musik.wav');
// Blenders Python har numpy. Satt BLENDER_PYTHON om den inte hittas automatiskt.
function blenderPython() {
  if (process.env.BLENDER_PYTHON) return process.env.BLENDER_PYTHON;
  const rotter = ['W:/Blender', 'C:/Program Files/Blender Foundation', '/Applications/Blender.app/Contents/Resources', '/usr/share/blender'];
  for (const r of rotter) {
    if (!existsSync(r)) continue;
    const stack = [[r, 0]];
    while (stack.length) {
      const [d, n] = stack.pop(); let items = []; try { items = readdirSync(d); } catch { continue; }
      for (const x of items) {   // python i en bin-mapp under Blenders versionsmapp, t.ex. 5.2/python/bin/python.exe
        const p = join(d, x); if (/^python(3(\.\d+)?)?(\.exe)?$/.test(x) && /[\\/]bin$/.test(d)) return p;
        if (n < 4 && !/\.(exe|dll|txt|py|json|md|zip|blend)$/i.test(x) && !['scripts', 'datafiles', 'lib', 'site-packages', 'include'].includes(x)) stack.push([p, n + 1]);
      }
    }
  }
  return 'python3';
}
const PYX = blenderPython();
// 1. rosten: forst rost.py (niva fras for fras, andetag sanks), sedan kedjan i rostkedja.txt (klickborttagning, EQ, de-esser, multiband, kompressor, mattnad, limiter)
const ROST = join(LJ, 'rost_bearbetad.wav'), KEDJA = readFileSync(join(LJ, 'rostkedja.txt'), 'utf8').trim();
const RA = join(LJ, 'rost_ra.wav'), FRAS = join(LJ, 'rost_fraser.wav');
ff(['-i', join(P, 'full recording.m4a'), '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s32le', RA]);
execFileSync(PYX, [join(HERE, 'rost.py'), RA, FRAS], { stdio: 'inherit' });
ff(['-i', FRAS, '-af', KEDJA, '-ar', '48000', '-c:a', 'pcm_s24le', ROST]);

// 2. rostsparet: varje replik klipps ut med korta toningar och laggs pa sin plats
const parts = SEG.map(([no, off, a, b], i) => `[0:a]atrim=${a}:${b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=${(b - a - 0.04).toFixed(3)}:d=0.04,adelay=${Math.round((at(no) + off) * 1000)}:all=1[s${i}]`);
const VO = join(LJ, 'rostspar.wav');
ff(['-i', ROST, '-filter_complex', parts.join(';') + ';' + SEG.map((_, i) => `[s${i}]`).join('') + `amix=inputs=${SEG.length}:normalize=0,apad=whole_dur=${TOT.toFixed(3)}[o]`, '-map', '[o]', '-ac', '1', '-c:a', 'pcm_s24le', VO]);

// 3. musiken: genereras i ratt langd. Oppningen ar gles, huvuddelen borjar nar akt 1 borjar.
// Finns en egen lat i projektmappen anvands den (System Online.mp3, gjord i Suno, -15 LUFS -> sanks 5 dB till samma referens som den genererade musiken).
const LAT = join(P, 'System Online.mp3'), egen = existsSync(LAT);
const MUSIK_IN = 1.0;   // titeln (0.6) forlangdes 1 s den 17/11. Musiken borjar lika mycket senare, sa att den ligger kvar mot allt efter titeln (byggklippen i 6.1 ar lagda pa dess slag)
if (egen) ff(['-i', LAT, '-af', `volume=-5dB,adelay=${MUSIK_IN * 1000}:all=1,apad=whole_dur=${TOT.toFixed(3)},afade=t=out:st=${(TOT - 3).toFixed(3)}:d=3`, '-t', TOT.toFixed(3), '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', MU]);
else execFileSync(PYX, [join(HERE, 'musik.py'), MU, TOT.toFixed(2), at('1.1').toFixed(2)], { stdio: 'inherit' });

// 3b. ljudeffekterna: [klipp, sekunder in i klippet, ljud, niva i dB, {dur, pitch, pan}]. Tiderna foljer scenernas egna tidtabeller. Ljud med korta namn (pip, pop, klang ...) syntetiseras i effekter.py. Ovriga namn ar filer ur Kenneys ljudpaket (CC0, kenney.nl) i film/ljud/kenney.
const FX = [
  ['0.3', 1.93, 'knack', -20],                                                                                                    // noten landar i skalen (inget servoljud)
  ['1.2', 0.04, 'klick', -29], ['1.2', 1.56, 'klick', -29, { pan: -0.35 }], ['1.2', 2.60, 'klick', -29, { pan: 0.35 }],   // korten i 1.2 kommer fram, ett mjukt klick per kort
  ['0.5', 0.22, 'glitch_002', -29], ['0.5', 0.36, 'glitch_001', -33],   // LED-skarmen glitchar over till VERIFIERAR (rutorna 321-327)
  ['0.5', 1.70, 'pip', -24], ['0.5', 1.95, 'pip', -24], ['0.5', 2.20, 'pip', -24], ['0.6', 0.0, 'duns', -14],
  ['2.1', 0.6, 'impactWood_light_003', -21], ['2.1', 0.8, 'impactWood_light_004', -31],   // noten fran 1.4 landar bland de andra pa fatet och studsar
  ['2.1', 2.5, 'impactWood_light_000', -22], ['2.1', 3.3, 'impactWood_light_002', -22], ['2.1', 4.1, 'impactWood_light_001', -22],          // skatan pickar
  ['2.3', 3.2, 'klang', -27, { pitch: 0.75 }], ['2.3', 7.7, 'klick', -22],                // molnet, kameran sanks ner
  ['2.4', 5.3, 'slutare', -18], ['2.4', 8.9, 'pip', -25], ['2.4', 9.1, 'pip', -25], ['2.4', 9.3, 'pip', -25],
  ['2.5', 0.2, 'error_004', -21],
  ['2.5', 1.6, 'tallrik', -25, { dur: 1.4, pan: -0.15 }],                                                                            // nej-signalen slar ner i fatet, som snurrar ut (32,7 s i planen = 1,6 s in i 2.5)
  ['2.6', 1.95, 'slutare', -18], ['2.6', 3.7, 'confirmation_001', -20],
  ...Array.from({ length: 9 }, (_, i) => ['2.6', 4.65 + i * 0.075, 'pop', -19, { pitch: 1 + i * 0.09, pan: (i % 3 - 1) * 0.4 }]),                // notterna poppar upp
  ['3.1', 4.1, 'click_002', -25],   // fragan skickas
  ...Array.from({ length: 36 }, (_, i) => ['3.1', 0.9 + i / 12, ['tick_001', 'tick_002', 'tick_004'][i * 5 % 3], -27 + (i * 7 % 5) * 0.8, { pitch: 0.8 + (i * 13 % 7) * 0.06 }]),          // fragan skrivs
  ...Array.from({ length: 11 }, (_, i) => ['3.1', 4.8 + i / 10, 'tick_002', -31]),                                                   // svaret skrivs
  ['3.1', 6.0, 'klang', -27],                                                               // ritningen projiceras
  ['3.2', 8.6, 'klang', -24],                                                               // huset reser sig, skarmen tands
  ['4.1', 3.75, 'impactGeneric_light_000', -19], ['4.1', 5.1, 'impactGeneric_light_001', -20], ['4.1', 6.3, 'impactGeneric_light_002', -19], ['4.1', 7.25, 'impactGeneric_light_003', -21], ['4.1', 7.45, 'impactGeneric_light_004', -21],   // Pi, kamera, skarm, servon
  ...Array.from({ length: 11 }, (_, i) => ['4.1', 0.6 + 0.2 * i + 0.4, 'tick', -32 + (i % 3) * 0.7, { pitch: 0.85 + (i * 7 % 5) * 0.06, pan: [3, 4, 5, 9].includes(i) || i === 7 || i === 8 ? 0.45 : -0.45 }]),   // "en hel del grejer": ett svagt tick per sak i kanterna (akt_inkop.py, GREJER)
  ['4.1', 9.2, 'klang', -28],                                                                          // kablarna, skarmen tands
  ...Array.from({ length: 10 }, (_, i) => ['4.1', 9.35 + i * 0.04, 'impactMetal_light_00' + (i % 5), -28, { pan: (i - 4.5) / 6 }]),                             // skruvarna
  ...Array.from({ length: 7 }, (_, i) => ['4.1', 9.8 + i * 0.06, 'knack', -24, { pitch: 1.1 + i * 0.05 }]),                                       // notterna
  ['4.2', 0.63, 'duns', -22], ['4.2', 0.93, 'duns', -22], ['4.2', 1.23, 'duns', -22],        // filamentrullarna, rullen snurrar
  // titelns pixlar tands med sma klick (overgangarna har inga egna sus, Marcus ville inte ha dem)
  ...Array.from({ length: 18 }, (_, i) => ['0.6', 0.22 + ((i * 7) % 18) / 18 * 0.5, 'tick', -33 + (i % 3), { pitch: 0.8 + (i * 5 % 7) * 0.08, pan: ((i * 3) % 7 - 3) * 0.12 }]),
  // utskriftsvaggen (akt_utskrift.py): ett latt klick per ruta som dyker fram (1.9 + 0.11 n s in i 5.2), en klang nar alla blir klara (9.1 s = 5.1 s in i 5.3)
  ...Array.from({ length: 11 }, (_, n) => { const t = 1.9 + 0.11 * (n + 1) + 0.25; return t < 4 ? ['5.2', t, 'klick', -27, { pitch: 0.8 + (n * 5 % 7) * 0.07, pan: ((n * 3) % 5 - 2) * 0.2 }] : ['5.3', t - 4, 'klick', -27, { pitch: 0.8 + (n * 5 % 7) * 0.07, pan: ((n * 3) % 5 - 2) * 0.2 }]; }),
  ['5.3', 5.1, 'klang', -23],
  // monteringen: varje del klickar pa plats 0,75 s efter att den borjat aka hem (tider ur STEPS i akt_montering.py, raknat fran 6.1)
  ...[4.0, 4.35, 4.7, 5.1, 5.45, 6.0, 6.3, 6.6, 7.3, 7.55, 7.8, 8.5, 9.1, 9.7, 10.3, 10.6, 10.9, 11.15, 11.6, 12.0, 12.5, 13.1, 13.5, 13.85, 14.1, 14.9, 15.3, 15.55, 16.1, 16.5, 17.1]
    .flatMap((t, i) => [6.6, 15.3, 15.55].includes(t) ? [['6.1', t + 0.75, 'duns', -19], ['6.1', t + 0.75, 'impactPlate_medium_00' + (i % 5), -20]] : [['6.1', t + 0.75, 'impactPlate_light_00' + (i * 3 % 5), -22, { pan: (i % 3 - 1) * 0.3 }]]),
  ['6.3', 0.3, 'klang', -26, { pitch: 0.75 }],
];
const KEN = join(LJ, 'kenney'), FXD = join(LJ, 'fx'); mkdirSync(FXD, { recursive: true });
for (const namn of new Set(FX.map(f => f[2]))) {      // Kenney-ljuden gors om till wav som effekter.py kan lasa
  const src = ['interface-sounds', 'impact-sounds'].map(p => join(KEN, p, 'Audio', namn + '.ogg')).find(existsSync);
  if (src && !existsSync(join(FXD, namn + '.wav'))) ff(['-i', src, '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', join(FXD, namn + '.wav')]);
}
const HAND = join(LJ, 'handelser.json'), EFX = join(LJ, 'effekter.wav');
writeFileSync(HAND, JSON.stringify(FX.map(([no, off, namn, db, o]) => [namn, +(at(no) + off).toFixed(3), db, o || {}])));
execFileSync(PYX, [join(HERE, 'effekter.py'), HAND, EFX, TOT.toFixed(2), FXD], { stdio: 'inherit' });

// 3c. rumston: ett svagt, jamnt brus under hela filmen sa att pauserna mellan replikerna inte blir digitalt tysta (-58 dB, drygt 38 dB under rosten)
const rumRa = join(LJ, 'rumston_ra.wav');
ff(['-f', 'lavfi', '-i', `anoisesrc=color=brown:amplitude=0.05:sample_rate=48000:seed=7:duration=${TOT.toFixed(3)}`, '-af', 'highpass=f=110,lowpass=f=2600', '-c:a', 'pcm_s24le', rumRa]);
const RUMNIVA = +spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', rumRa, '-af', 'astats', '-f', 'null', '-'], { encoding: 'utf8' }).stderr.match(/RMS level dB: (-?[0-9.]+)/)[1];
// 4. mixen: musiken ligger lagt och dackas ytterligare nar rosten talar, effekterna laggs ovanpa. Slutniva cirka -16 LUFS, toppar under -1,2 dB.
const MIX = join(LJ, 'mix.wav');
ff(['-i', VO, '-i', MU, '-i', EFX, '-i', rumRa, '-filter_complex',
  // Rosten far en mycket svag, kort rumsklang (samma tre reflexer som effekterna, 23/41/67 ms). Musiken delas i tre band: mellanregistret (700-4500 Hz, dar rosten ligger) viker tydligt nar rosten talar, bas och diskant bara lite.
  `[0:a]aecho=1:1:23|41|67:0.06|0.045|0.03,asplit=4[v][s1][s2][s3];[1:a]volume=-7dB,acrossover=split=700 4500:order=4th[ml][mm][mh];[mm][s1]sidechaincompress=threshold=0.012:ratio=5:attack=25:release=600:knee=4[mmd];[ml][s2]sidechaincompress=threshold=0.015:ratio=1.6:attack=40:release=800:knee=4[mld];[mh][s3]sidechaincompress=threshold=0.015:ratio=1.6:attack=40:release=800:knee=4[mhd];[mld][mmd][mhd]amix=inputs=3:normalize=0[md];[3:a]volume=${(-58 - RUMNIVA).toFixed(2)}dB,afade=t=in:d=1,afade=t=out:st=${(TOT - 2).toFixed(3)}:d=2,pan=stereo|c0=c0|c1=c0[rt];[v]pan=stereo|c0=c0|c1=c0[vs];[vs][md][2:a][rt]amix=inputs=4:normalize=0,volume=1.9dB,alimiter=limit=-1.2dB:attack=3:release=80:level=disabled[o]`,
  '-map', '[o]', '-t', TOT.toFixed(3), '-c:a', 'pcm_s16le', MIX]);

// 5. mixen laggs pa arbetskopian och pa varje klipp i storyboarden
const tmp = join(LJ, 'ak_tmp.mp4');
ff(['-i', AK, '-i', MIX, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', tmp]); renameSync(tmp, AK); copyFileSync(AK, join(P, 'film', 'Lennart - arbetskopia.mp4'));
cuts.forEach(([no, t0, , , film], i) => {
  if (!film) return; const clip = join(SB, 'clips', no.replace('.', '_') + '.mp4'), d = (i + 1 < cuts.length ? cuts[i + 1][1] : TOT) - t0, t = join(LJ, 'k_tmp.mp4');
  ff(['-i', clip, '-ss', t0.toFixed(3), '-t', d.toFixed(3), '-i', MIX, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', t]); renameSync(t, clip);
});
console.log('mix klar', TOT.toFixed(1) + ' s');
