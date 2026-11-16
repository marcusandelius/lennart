// Projekt Lennart - arbetskopian: allt som ar producerat, i filmens ordning, som en enda film.
// Klipp som har film anvands som de ar. Klipp utan film visas som stillbild i sin planerade langd.
// Varje klipp far sitt nummer och sin titel inbrand nere till vanster.
// Kor:  node film/verktyg/arbetskopia.mjs      (laser storyboard/storyboard.html och storyboard/clips, skriver storyboard/arbetskopia.mp4 + film/Lennart - arbetskopia.mp4)
//       node film/verktyg/arbetskopia.mjs --hel  (hela filmen i 1280 x 720 med mixen fran ljudmix.mjs: film/Lennart - hela filmen 720p.mp4)
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url)), P = resolve(HERE, '..', '..'), SB = join(P, 'storyboard'), TMP = join(HERE, 'ak_tmp');
rmSync(TMP, { recursive: true, force: true }); mkdirSync(TMP, { recursive: true });
const html = readFileSync(join(SB, 'storyboard.html'), 'utf8');
const grab = (a, b) => { const i = html.indexOf(a) + a.length; return html.slice(i, html.indexOf(b, i)); };
const ACTS = new Function('return ' + grab('const ACTS = ', '\n];') + ']')(), FILM = new Function('return ' + grab('const FILM = ', ';\n'))();
const ff = (args, cwd = HERE) => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], { cwd, stdio: ['ignore', 'inherit', 'inherit'] });
const probe = (f, what) => execFileSync('ffprobe', ['-v', 'error', ...what, '-of', 'csv=p=0', f]).toString().trim();
const HEL = process.argv.includes('--hel'), [VW, VH] = HEL ? [1280, 720] : [960, 540];
const CRF = HEL ? '18' : (process.argv.find(a => /^\d+$/.test(a)) || '27'), V = ['-r', '25', '-c:v', 'libx264', '-crf', CRF, '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-ar', '48000', '-ac', '1'];
const cuts = []; let t = 0, n = 0; const list = [];
for (const [name, , , clips] of ACTS) for (const c of clips) {
  const [no, , len, title, fr] = c, key = no.replace('.', '_'), clip = join(SB, 'clips', key + '.mp4'), out = join(TMP, String(n).padStart(2, '0') + '.mp4'), film = !!FILM[no] && existsSync(clip);
  let d;
  if (film) {
    d = +probe(clip, ['-show_entries', 'format=duration']); const hasA = probe(clip, ['-select_streams', 'a', '-show_entries', 'stream=index']) !== '';
    ff(['-i', clip, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-filter_complex', `[0:v]scale=${VW}:${VH}[v]`, '-map', '[v]', '-map', hasA ? '0:a' : '1:a', '-t', d.toFixed(3), ...V, out]);
  } else {
    d = parseFloat(len.replace(',', '.')) || 3; const still = fr ? join(SB, 'frames', fr + '.jpg') : null;
    ff([...(still ? ['-loop', '1', '-i', still] : ['-f', 'lavfi', '-i', `color=c=black:s=${VW}x${VH}:r=25`]), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-filter_complex', `[0:v]scale=${VW}:${VH}:force_original_aspect_ratio=increase,crop=${VW}:${VH},eq=saturation=0.55:brightness=-0.04[v]`, '-map', '[v]', '-map', '1:a', '-t', d.toFixed(3), ...V, out]);
  }
  d = +probe(out, ['-show_entries', 'format=duration']); cuts.push([no, +t.toFixed(2), title, name, film ? 1 : 0]); t += d; list.push(`file '${out.replace(/\\/g, '/')}'`); n++;
}
writeFileSync(join(TMP, 'list.txt'), list.join('\n') + '\n');
const OUT = HEL ? join(TMP, 'hel.mp4') : join(SB, 'arbetskopia.mp4');
ff(['-f', 'concat', '-safe', '0', '-i', join(TMP, 'list.txt'), '-c', 'copy', '-movflags', '+faststart', OUT]);
if (HEL) {   // hela filmen: bilden i 720p med den fardiga mixen (kor ljudmix.mjs forst)
  const MIX = join(P, 'film', 'ljud', 'mix.wav'), HELF = join(P, 'film', 'Lennart - hela filmen 720p.mp4');
  ff(['-i', OUT, '-i', MIX, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', HELF]);
  console.log('hela filmen klar', HELF); rmSync(TMP, { recursive: true, force: true }); process.exit(0);
}
copyFileSync(OUT, join(P, 'film', 'Lennart - arbetskopia.mp4')); writeFileSync(join(SB, 'arbetskopia.json'), JSON.stringify(cuts));
writeFileSync(join(SB, 'storyboard.html'), readFileSync(join(SB, 'storyboard.html'), 'utf8').replace(/const CUTS = \[.*\];/, () => 'const CUTS = ' + JSON.stringify(cuts) + ';'));   // kapitlen i storyboardens spelare
rmSync(TMP, { recursive: true, force: true });
console.log('klar', (+probe(OUT, ['-show_entries', 'format=duration'])).toFixed(1) + ' s', (+probe(OUT, ['-show_entries', 'format=size']) / 1e6).toFixed(1) + ' MB', cuts.filter(c => c[4]).length + ' av ' + cuts.length + ' klipp har film');
