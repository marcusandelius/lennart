# Nytt i handoffen 2026-11-15: plockar ut data ur den publicerade förhandsgranskningen
# (lennarts-matstation-3d.html) så att skripten i avsnitt 4 kan köras igen.
# Användning: python3 extract_from_html.py lennarts-matstation-3d.html
import sys, re, json, base64, io, zipfile, os
src = sys.argv[1] if len(sys.argv) > 1 else 'lennarts-matstation-3d.html'
s = open(src, encoding='utf-8').read()
# delarna (samma format som parts_v*.json): namn, grupp, färg, fil och triangelnät i base64
i = s.index('const PARTS = ') + len('const PARTS = '); j = s.index(';\n', i)
parts = json.loads(s[i:j]); json.dump(parts, open('parts_from_html.json', 'w'))
# plattorna i fliken Utskrift
a = s.index('<script id="platedata" type="application/json">') + len('<script id="platedata" type="application/json">'); b = s.index('</script>', a)
open('plates_from_html.json', 'w').write(s[a:b])
# alla STL-filer
a = s.index('<script id="zipdata" type="application/octet-stream">') + len('<script id="zipdata" type="application/octet-stream">'); b = s.index('</script>', a)
z = zipfile.ZipFile(io.BytesIO(base64.b64decode(s[a:b]))); os.makedirs('stl', exist_ok=True); z.extractall('stl')
print(len(parts), 'delar,', len(z.namelist()), 'STL-filer')
