# Mönstret som använts flera gånger 2026-11-12–15 för att lägga in aktuell data i förhandsgranskningen
# (delar, plattor, STL-zip och fillista). Körd i /home/claude/fix.
import re, json, base64, zipfile, io, os
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'; s=open(p).read()
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v11.json').read()+s[j:]
a=s.index('<script id="platedata" type="application/json">')+len('<script id="platedata" type="application/json">'); b=s.index('</script>',a)
s=s[:a]+open('plates.json').read()+s[b:]
with zipfile.ZipFile('/mnt/user-data/outputs/lennarts-matstation-3d.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir('stl')): z.write('stl/'+f, f)
zb=open('/mnt/user-data/outputs/lennarts-matstation-3d.zip','rb').read()
files=[(x.filename,x.file_size) for x in zipfile.ZipFile(io.BytesIO(zb)).infolist()]
a=s.index('<script id="zipdata" type="application/octet-stream">')+len('<script id="zipdata" type="application/octet-stream">'); b=s.index('</script>',a)
s=s[:a]+base64.b64encode(zb).decode()+s[b:]
s=re.sub(r'const FILES = \[.*?\];', lambda m: 'const FILES = '+json.dumps(files)+';', s, count=1, flags=re.S)
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
print(len(files),"filer")
