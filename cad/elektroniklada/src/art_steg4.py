"""Steg 4: nya elektroniklådan (bakstycke, kåpa, komponentplatta, packning) i artefakten."""
import json, re, base64, io, zipfile, os
import numpy as np, trimesh
p = 'art/matstation.html'; s = open(p, encoding='utf8').read()
b64 = lambda a: base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()
def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, a[:80]; s = s.replace(a, b) if n == 0 else s.replace(a, b, n)
E = 'el/ut/'
A = {n: trimesh.load(E + 'asm/%s.stl' % n) for n in ('elbakstycke', 'elkapa', 'komponentplatta', 'elpackning')}
PR = {n: trimesh.load(E + 'print/%s.stl' % n) for n in ('16_elbakstycke', '16b_elkapa', '24_komponentplatta', '17_elpackning')}
for m in list(A.values()) + list(PR.values()): m.merge_vertices()
komp = trimesh.util.concatenate([trimesh.load(E + 'spoken/' + f) for f in sorted(os.listdir(E + 'spoken'))])
BLK = '#232427'

# ---- delarna i 3D-vyn
L = s.split('\n')
pi = [n for n, l in enumerate(L) if 'const PARTS' in l[:40]][0]; line = L[pi]; i = line.index('['); P, end = json.JSONDecoder().raw_decode(line[i:])
dec = lambda q: trimesh.Trimesh(np.frombuffer(base64.b64decode(q['pos']), '<f4').reshape(-1, 3), np.frombuffer(base64.b64decode(q['idx']), '<u4').reshape(-1, 3))
oldvol = {q['name']: abs(dec(q).volume) for q in P if q['name'] in ('elektroniklada', 'ellock', 'monteringsplatta')}
NEW = {'elektroniklada': ('elbakstycke', '16_elbakstycke.stl', 'Svart PETG. Skruvas fast utifrån genom bakväggen med fyra M3 × 10 och muttrar i fickorna. Golv med fem kabelöppningar, skenor för komponentplattan, ett torn uppe till höger med en M2,5-gänga för kåpans skruv och ett Ø26-hål för muttern på strömkabelns förskruvning (vänstra Ø16-hålet i bakväggen)'),
       'ellock': ('elkapa', '16b_elkapa.stl', 'Svart PETG. Framsida, sidor och tak i ett stycke. Lyfts rakt upp när taket är av, hålls av en M2,5 uppifrån i tornet. Två fönster, öppna nedåt: höger kant för GPIO-kontakterna och nere till höger för PCA9685:s servokontakter och kamerans flatkabel, så att kåpan går att lyfta med allt inkopplat. Slutet tak; ventilation genom lameller högst upp framtill och sneda springor i sidorna, så att vatten som rinner på utsidan inte kommer in. Fena på taket att lyfta i'),
       'monteringsplatta': ('komponentplatta', '24_komponentplatta.stl', 'Svart PETG. Glider i skenorna och lyfts rakt upp. Gängor för Pi 5 (4 × M2,5), PCA9685 och EKM006 (8 × M2) på 3 mm distanser. PCA9685 ligger under Pi:n, servoomvandlaren står i en vagga med buntband till vänster och EKM006 sitter ovanför, vriden 10 grader. En bred slits öppen nedåt för förskruvningen och strömkabeln, så att plattan kan lyftas med kabeln kvar. Keystone-uttaget och DC-jacket ligger under lådan. Pi:n använder wifi'),
       'elpackning': ('elpackning', '17_elpackning_tpu.stl', 'TPU 95A, 1,2 mm. Ligger mellan bakstycket och bakväggen')}
out = []
for q in P:
    if q['name'] == 'genomforingar': continue
    if q['name'] in NEW:
        an, fn, note = NEW[q['name']]; m = A[an]
        q.update(file=fn, note=note, color=BLK if an != 'elpackning' else '#2B2B2B', pos=b64(m.vertices.astype('<f4')), idx=b64(m.faces.astype('<u4')))
    out.append(q)
L[pi] = line[:i] + json.dumps(out, ensure_ascii=False) + line[i + end:]
s = '\n'.join(L)

rep('ellock:"Lock till elektroniklådan"', 'ellock:"Elektroniklådans kåpa"')
rep('monteringsplatta:"Monteringsplatta för elektroniken"', 'monteringsplatta:"Komponentplatta"')
rep('elektroniklada:"Elektroniklåda",elpackning:"Packning till elektroniklådan"', 'elektroniklada:"Elektroniklådans bakstycke",elpackning:"Packning bakom elektroniklådan (TPU)"')
# tider: skalade efter volymen jämfört med den gamla lådan [ungefärliga]
r = 1.89 / oldvol['elektroniklada'] if oldvol['elektroniklada'] > 0 else 0.02e-3
hrs = {'16': round(A['elbakstycke'].volume * r, 2), '16b': round(A['elkapa'].volume * r, 2), '24': round(A['komponentplatta'].volume * r, 2), '17': 0.6}
ti = [n for n, l in enumerate(s.split('\n')) if l.startswith('const TIMES = ')][0]
L = s.split('\n'); T, te = json.JSONDecoder().raw_decode(L[ti][len('const TIMES = '):]); T.pop('25', None); T.update(hrs)
L[ti] = 'const TIMES = ' + json.dumps(T, ensure_ascii=False) + L[ti][len('const TIMES = ') + te:]; s = '\n'.join(L)
print('tider', hrs, 'gamla volymer', {k: round(v / 1000, 1) for k, v in oldvol.items()})

# ---- komponenterna (ungefärliga lådor) syns i 3D-vyn med inredningen
a = 'const KORT = {pos:'
rep(a, 'const KOMP = {pos:"%s", idx:"%s"};      // elektronikens komponenter som enkla lådor (för att se platsen)\nconst kompMesh = (() => { const g = new THREE.BufferGeometry(); const f = b => new Uint8Array([...atob(b)].map(c=>c.charCodeAt(0))).buffer; g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(f(KOMP.pos)),3)); g.setIndex(new THREE.BufferAttribute(new Uint32Array(f(KOMP.idx)),1)); g.computeVertexNormals(); const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({color:"#2E7D4F", roughness:.6})); m.castShadow = true; house.add(m); return m; })();\n' % (b64(komp.vertices.astype('<f4')), b64(komp.faces.astype('<u4'))) + a)
rep('  kortMesh.visible = !solo && ex.value==0 && state.Inredning && (!asmStep || asmStep>=5);',
    '  kortMesh.visible = !solo && ex.value==0 && state.Inredning && (!asmStep || asmStep>=5);\n  kompMesh.visible = !solo && ex.value==0 && state.Inredning && (!asmStep || asmStep>=6);')

# ---- texter
rep('elektroniklådan med lock och monteringsplatta.</li>', 'elektroniklådan (bakstycke, kåpa och komponentplatta i svart PETG, packningen i TPU).</li>')
rep('<li>Skruva fast elektroniklådan utifrån genom bakväggen, med gummibricka under skruvskallarna. Lådan sitter sedan kvar. Spraytesta den med vatten först.</li>',
    '<li>Lägg M3-muttrar i de fyra fickorna på bakstyckets insida och skruva fast bakstycket utifrån genom bakväggen med fyra M3 × 10, med TPU-packningen emellan och gummibricka under skruvskallarna. Bakstycket sitter sedan kvar.</li>')
rep('<li>Bygg elektroniken på monteringsplattan vid skrivbordet och skjut ner plattan i lådan uppifrån. Stäng av PIN-koden på SIM-kortet och tejpa modemet på lådans lock.</li>',
    '<li>Smält in gängorna: 4 × M2,5 (Pi 5) och 8 × M2 (PCA9685, EKM006) i komponentplattan, 1 × M2,5 i tornet uppe till höger på bakstycket. Bygg elektroniken på plattan vid skrivbordet och skjut ner den i skenorna uppifrån. Strömkabeln går in genom förskruvningen M16 i det vänstra Ø16-hålet (montera förskruvningen före bakstycket), skalas cirka 1 cm innanför och går ned genom kanalen och golvet till DC-jacket under lådan. Keystone-uttaget och DC-jacket ligger under lådan, och 12 V-ledarna till EKM006 och servoomvandlaren går upp genom golvet. Servoomvandlaren buntas fast i sin vagga. Servona kopplas i PCA9685 genom fönstret nere till höger. Pi:n använder wifi. Sätt en blindplugg M16 i det högra Ø16-hålet. Lägg på kåpan och skruva en M2,5 uppifrån i tornet. Routern står på kant till vänster om doseringen.</li>')
rep('<li><strong>Elektroniken:</strong> lyft av taket och lådans lock, och dra monteringsplattan rakt upp. Inga skruvar.</li>',
    '<li><strong>Elektroniken:</strong> lyft av taket, skruva ur kåpans skruv och lyft kåpan rakt upp. Då når du alla kontakter med plattan kvar. Ska plattan ut: dra ur kontakterna och lyft den rakt upp ur skenorna.</li>')
rep('{title:"Elektroniken", text:"Skruva fast elektroniklådan utifrån genom bakväggen. Skjut ner monteringsplattan med all elektronik uppifrån och lägg på locket.", parts:["elpackning","elektroniklada","monteringsplatta","ellock","genomforingar"]}',
    '{title:"Elektroniken", text:"Skruva fast bakstycket utifrån genom bakväggen med packningen emellan. Skjut ner komponentplattan med elektroniken i skenorna, koppla in kablarna genom golvet och fönstren och lägg på kåpan med en skruv uppifrån.", parts:["elpackning","elektroniklada","monteringsplatta","ellock"]}')

rep('<td>Från Pi:ns USB-port upp till modemet på elektroniklådans lock.</td>', '<td>Behövs bara om ett USB-modem används i stället för routern.</td>')
rep('<td>Fäster omvandlare och kablar i monteringsplattans hålraster.</td>', '<td>Fäster servoomvandlaren och kablarna i komponentplattans buntbandshål.</td>')
# ---- utskriftsplattorna
L = s.split('\n'); pli = [n for n, l in enumerate(L) if 'id="platedata"' in l][0]
pd = re.sub(r'^<script[^>]*>', '', L[pli]); pd = re.sub(r'</script>.*$', '', pd); PL = json.loads(pd)
def enc(m):
    big = len(m.vertices) > 65535
    return b64(np.clip(np.round(m.vertices / 0.005), 0, 65535).astype('<u2')), b64(m.faces.astype('<u4' if big else '<u2')), big
def at(m, x0, y0):
    m = m.copy(); m.apply_translation([x0 - m.bounds[0][0], y0 - m.bounds[0][1], -m.bounds[0][2]]); return m
def group(g, name, how, h, ms, files, colors):
    bb = np.vstack([m.bounds for m in ms])
    return dict(g=g, name=name, how=how, hours=h, cx=round(float((bb[:, 0].min() + bb[:, 0].max()) / 2), 1), cy=round(float((bb[:, 1].min() + bb[:, 1].max()) / 2), 1), top=round(float(bb[:, 2].max()), 1), files=files, colors=colors)
def item(g, fn, m, c):
    it = dict(group=g, file=fn, color=c); it['pos'], it['idx'], it['i32'] = enc(m); return it
PL = [x for x in PL if not any(it['file'] in ('16_elektroniklada.stl', '24_monteringsplatta.stl') for it in x['items'])]
for x in PL:
    x['items'] = [it for it in x['items'] if it['file'] not in ('17_elektroniklada_packning_tpu.stl', '25_genomforingar_tpu.stl')]
    x['groups'] = [g for g in x['groups'] if g['g'] not in ('17', '25')]
    if x['groups']:
        x['hours'] = round(sum(g['hours'] for g in x['groups']), 2); x['height'] = max(g['top'] for g in x['groups'])
PL = [x for x in PL if x['groups']]
kap = at(PR['16b_elkapa'], 58, 18); bak = at(PR['16_elbakstycke'], 58, kap.bounds[1][1] + 8)
pla = at(PR['24_komponentplatta'], 128 - 65.3, 128 - 68); pac = at(PR['17_elpackning'], 128 - 69, 128 - 70)
PH = '4. Nya elektroniklådan (ersätter den gamla)'
new = [dict(material='PETG', phase=PH, printed=False, items=[item('16', '16_elbakstycke.stl', bak, BLK), item('16b', '16b_elkapa.stl', kap, BLK)],
            groups=[group('16', 'Elektroniklådans bakstycke', 'Står på golvet, som i huset. Inga stöd', hrs['16'], [bak], ['16_elbakstycke.stl'], [BLK]),
                    group('16b', 'Elektroniklådans kåpa', 'Ligger på framsidan, öppningen uppåt. Inga stöd', hrs['16b'], [kap], ['16b_elkapa.stl'], [BLK])]),
       dict(material='PETG', phase=PH, printed=False, items=[item('24', '24_komponentplatta.stl', pla, BLK)],
            groups=[group('24', 'Komponentplatta', 'Ligger på baksidan, distanserna uppåt. Inga stöd', hrs['24'], [pla], ['24_komponentplatta.stl'], [BLK])]),
       dict(material='TPU', phase=PH, printed=False, items=[item('17', '17_elpackning_tpu.stl', pac, '#2B2B2B')],
            groups=[group('17', 'Packning bakom elektroniklådan', 'Ligger platt', hrs['17'], [pac], ['17_elpackning_tpu.stl'], ['#2B2B2B'])])]
for x in new: x['hours'] = round(sum(g['hours'] for g in x['groups']), 2); x['height'] = max(g['top'] for g in x['groups'])
PL += new
for x in new: print('platta', x['material'], [np.round([g['cx'], g['cy'], g['top']], 1).tolist() for g in x['groups']])
L[pli] = '<script id="platedata" type="application/json">' + json.dumps(PL, ensure_ascii=False) + '</script>'

# ---- zip och fillista
zi = pli + 1; m0 = re.match(r'^(<script[^>]*>)(.*?)(</script>.*)$', L[zi], re.S)
zin = zipfile.ZipFile(io.BytesIO(base64.b64decode(m0.group(2)))); buf = io.BytesIO(); zout = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=9); sizes = {}
GONE = {'16_elektroniklada.stl': '16_elbakstycke.stl', '16b_elektroniklada_lock.stl': '16b_elkapa.stl', '17_elektroniklada_packning_tpu.stl': '17_elpackning_tpu.stl',
        '24_monteringsplatta.stl': '24_komponentplatta.stl', '25_genomforingar_tpu.stl': None}
SRC = {'16_elbakstycke.stl': '16_elbakstycke', '16b_elkapa.stl': '16b_elkapa', '17_elpackning_tpu.stl': '17_elpackning', '24_komponentplatta.stl': '24_komponentplatta'}
for n in zin.namelist():
    if n in GONE: continue
    d = zin.read(n); zout.writestr(n, d); sizes[n] = len(d)
for n, src in SRC.items():
    d = open(E + 'print/%s.stl' % src, 'rb').read(); zout.writestr(n, d); sizes[n] = len(d)
zout.close(); L[zi] = m0.group(1) + base64.b64encode(buf.getvalue()).decode() + m0.group(3)
fi = [n for n, l in enumerate(L) if l.startswith('const FILES = ')][0]
F = json.loads(L[fi][len('const FILES = '):].rstrip(';')); names = []
for f, _ in F:
    if f in GONE:
        if GONE[f]: names.append(GONE[f])
    else: names.append(f)
L[fi] = 'const FILES = ' + json.dumps([[f, sizes[f]] for f in names], ensure_ascii=False) + ';'
s = '\n'.join(L); open(p, 'w', encoding='utf8').write(s)
left = [m.start() for m in re.finditer('monteringsplatt|genomför|elektroniklada_lock|lådans lock', s)]
print('klart; kvar:', [s[i - 70:i + 30].replace('\n', ' ') for i in left][:8])
