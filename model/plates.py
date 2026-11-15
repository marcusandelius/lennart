import trimesh, os, json, base64, numpy as np, collections, re
from rectpack import newPacker, MaxRectsBssf
P={p['file']:p for p in json.load(open('parts_v7.json'))}
P['00_toleranstest.stl']=dict(color='#9AA0A6',note='Valfri färg. Skrivs ut först: passningar och nötmall (22 mm)')
s=open('/mnt/user-data/outputs/lennarts-matstation-3d.html').read()
TIMES=json.loads(re.search(r'const TIMES = (\{[^}]*\});', s).group(1))
groups=collections.OrderedDict()
for f in sorted(os.listdir('stl')): groups.setdefault(f.split('_')[0],[]).append(f)
PLATE, MARGIN, GAP = 256.0, 5.0, 6.0
DUALW = 235.5                      # bredd som båda munstyckena når (X2D)
XOFF = (PLATE-DUALW)/2
items={}
for g,fs in groups.items():
    ms=[trimesh.load('stl/'+f) for f in fs]
    v=np.vstack([m.vertices for m in ms]); lo,hi=v.min(0),v.max(0)
    items[g]=dict(files=fs, meshes=ms, lo=lo, w=hi[0]-lo[0], d=hi[1]-lo[1], h=hi[2]-lo[2], tpu=all('tpu' in f for f in fs))
def pack(keys):
    pk=newPacker(pack_algo=MaxRectsBssf, rotation=True)
    for g in keys: pk.add_rect(int(np.ceil(items[g]['w']+GAP)*10), int(np.ceil(items[g]['d']+GAP)*10), rid=g)
    for _ in range(len(keys)): pk.add_bin(int((DUALW-2*MARGIN+GAP)*10), int((PLATE-2*MARGIN+GAP)*10))
    pk.pack()
    out=[]
    for b in pk:
        if len(b)==0: continue
        rects=[]
        for r in b:
            it=items[r.rid]; rot = abs(r.width - int(np.ceil(it['w']+GAP)*10)) > 1 and abs(r.width - int(np.ceil(it['d']+GAP)*10)) <= 1
            rects.append((r.rid, r.x/10+MARGIN+XOFF, r.y/10+MARGIN, rot))
        out.append(rects)
    return out
PHASES=[("Först: toleranstest och nötmall", ["00"]),
        ("1. Kan skrivas ut direkt", ["01","01b","02","02b","03","03b","05b","05c","06","06b","06c","06d","06e","16","16b","17","21","21b","22","23","24","25","04"]),
        ("2. Doseraren – när servot är uppmätt, provkör innan resten", ["10","11","12","13","14","20"]),
        ("3. När skärm, kamera och luckservo är uppmätta", ["05"]),
        ("3. När skärm, kamera och luckservo är uppmätta", ["05d","07","08","09","09b","15","18","19"])]
assert sorted(sum([p[1] for p in PHASES],[]))==sorted(items.keys()), set(items)-set(sum([p[1] for p in PHASES],[]))
plates=[]
for phase, keys in PHASES:
    a=[g for g in keys if not items[g]['tpu']]; t=[g for g in keys if items[g]['tpu']]
    a.sort(key=lambda g: (g!='00', -(items[g]['w']*items[g]['d'])))
    plates += [('ASA',p,phase) for p in pack(a)] + [('TPU',p,phase) for p in pack(t)]
Q=0.005
out=[]
for mat, rects, phase in plates:
    pl=dict(material=mat, phase=phase, items=[], hours=0.0)
    for g,x,y,rot in rects:
        it=items[g]; pl['hours']+=TIMES.get(g,0.1)
        for f,m in zip(it['files'], it['meshes']):
            v=m.vertices-it['lo']
            if rot: v=np.c_[v[:,1], it['w']-v[:,0], v[:,2]]     # 90° vridning på plattan
            v=v+[x,y,0]
            assert v.min()>-0.01 and v[:,0].max()<=PLATE+0.01 and v[:,1].max()<=PLATE+0.01, (g, v.min(0), v.max(0))
            qv=np.clip(np.round(v/Q),0,65535).astype(np.uint16)
            idx=m.faces.astype(np.uint16 if len(v)<65536 else np.uint32)
            pl['items'].append(dict(group=g, file=f, color=P.get(f,{}).get('color','#9A9A9A'), note=P.get(f,{}).get('note',''),
                                    pos=base64.b64encode(qv.tobytes()).decode(), idx=base64.b64encode(idx.tobytes()).decode(), i32=idx.dtype==np.uint32))
    pl['hours']=round(pl['hours'],2); out.append(pl)
json.dump(out, open('plates.json','w'))
for i,pl in enumerate(out):
    print(i+1, pl['phase'][:2], pl['material'], pl['hours'], sorted(set(it['group'] for it in pl['items'])))
print("storlek", round(os.path.getsize('plates.json')/1e6,2),"MB")
