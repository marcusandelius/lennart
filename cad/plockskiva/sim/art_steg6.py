"""Steg 6 (efter art_steg5.py): stativet med flyttad rännvägg (2026-11-27)."""
import json, re, base64, io, zipfile
import numpy as np, trimesh
p = 'art/matstation.html'; s = open(p, encoding='utf8').read()
b64 = lambda a: base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()
NEW_PRINT = '/home/user/lennart/cad/plockskiva/10_doserstativ.stl'
NEW_ASM = 'ranna/ut/asm/doserstativ.stl'
pr = trimesh.load(NEW_PRINT); pr.merge_vertices(); asm = trimesh.load(NEW_ASM); asm.merge_vertices()
L = s.split('\n')
# 3D-vyn
pi = [n for n, l in enumerate(L) if 'const PARTS' in l[:40]][0]; line = L[pi]; i = line.index('['); P, end = json.JSONDecoder().raw_decode(line[i:])
hit = [q for q in P if q['file'] == '10_doserstativ.stl']; assert len(hit) == 1, [q['name'] for q in hit]
q = hit[0]; old = trimesh.Trimesh(np.frombuffer(base64.b64decode(q['pos']), '<f4').reshape(-1, 3), np.frombuffer(base64.b64decode(q['idx']), '<u4').reshape(-1, 3))
print('del', q['name'], 'gammal mitt', np.round(old.bounds.mean(0), 1), 'ny mitt', np.round(asm.bounds.mean(0), 1))
q.update(pos=b64(asm.vertices.astype('<f4')), idx=b64(asm.faces.astype('<u4')))
q['note'] = q['note'].rstrip('.') + '. Rännans sneda vägg under utfallshålet flyttad 6 mm utåt 2026-11-27'
L[pi] = line[:i] + json.dumps(P, ensure_ascii=False) + line[i + end:]
# utskriftsplattan
pli = [n for n, l in enumerate(L) if 'id="platedata"' in l][0]
pd = re.sub(r'^<script[^>]*>', '', L[pli]); pd = re.sub(r'</script>.*$', '', pd); PL = json.loads(pd)
n_ = 0
for x in PL:
    for it in x['items']:
        if it['file'] == '10_doserstativ.stl':
            ov = np.frombuffer(base64.b64decode(it['pos']), '<u2').reshape(-1, 3) * 0.005
            m = pr.copy(); m.apply_translation([ov[:, 0].min() - m.bounds[0][0], ov[:, 1].min() - m.bounds[0][1], -m.bounds[0][2]])
            big = len(m.vertices) > 65535
            it['pos'] = b64(np.clip(np.round(m.vertices / 0.005), 0, 65535).astype('<u2')); it['idx'] = b64(m.faces.astype('<u4' if big else '<u2')); it['i32'] = big; n_ += 1
print('plattor uppdaterade', n_)
L[pli] = '<script id="platedata" type="application/json">' + json.dumps(PL, ensure_ascii=False) + '</script>'
# zip och fillista
zi = pli + 1; m0 = re.match(r'^(<script[^>]*>)(.*?)(</script>.*)$', L[zi], re.S)
zin = zipfile.ZipFile(io.BytesIO(base64.b64decode(m0.group(2)))); buf = io.BytesIO(); zout = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=9); sizes = {}
for n in zin.namelist():
    d = open(NEW_PRINT, 'rb').read() if n == '10_doserstativ.stl' else zin.read(n)
    zout.writestr(n, d); sizes[n] = len(d)
zout.close(); L[zi] = m0.group(1) + base64.b64encode(buf.getvalue()).decode() + m0.group(3)
fi = [n for n, l in enumerate(L) if l.startswith('const FILES = ')][0]
F = json.loads(L[fi][len('const FILES = '):].rstrip(';'))
L[fi] = 'const FILES = ' + json.dumps([[f, sizes.get(f, sz)] for f, sz in F], ensure_ascii=False) + ';'
s = '\n'.join(L); open(p, 'w', encoding='utf8').write(s); print('klart')
