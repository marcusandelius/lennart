import trimesh, os, json, base64, numpy as np, collections, re
from rectpack import newPacker, MaxRectsBssf
P={p['file']:p for p in json.load(open('parts_v11.json'))}
P['00_toleranstest.stl']=dict(color='#C8CCD0',note='Valfri färg. Passningar och nötmall')
NAME={"00":"Toleranstest och nötmall","01":"Bas","01b":"Framgård","02":"Gräsmatta","02b":"Framgårdens gräsmatta","03":"Bottenplatta","03b":"Framgårdens bottenplatta","04":"Fötter",
 "05":"Kropp med stengrund","05b":"Fönsterinsatser","05c":"Kamerans solskydd","05d":"Packning under kroppen","06":"Takhalva, vänster","06b":"Takhalva, höger","06c":"Skorsten","06d":"Takpackning","06e":"Nockkilar",
 "07":"Farstukvist","08":"Lucka","09":"Stolphatt","09b":"Packning under stolphatten","10":"Doserhus","11":"Doserhjul","14":"Nötmagasin","15":"Kamerafäste","16":"Elektroniklåda","16b":"Lock till elektroniklådan",
 "17":"Packning till elektroniklådan","18":"Skärmram","19":"Skärmklämma","21":"Blomlådor","21b":"Blomhuvuden","22":"Takrännor","23":"Stuprör","24":"Monteringsplatta","25":"Kabelgenomföringar"}
HOW={"00":"Skrivs ut allra först","01":"Upp och ner: ovansidan ligger mot plattan och hålrummet är öppet uppåt","01b":"Upp och ner, som basen","02":"Gräset uppåt","02b":"Gräset uppåt","03":"Ligger platt","03b":"Ligger platt","04":"Tappen uppåt",
 "05":"Står som huset står, stengrunden mot plattan. Grått de första 10 mm, sedan rött","05b":"Plattan nedåt, pluggarna uppåt","05c":"Väggsidan mot plattan","05d":"Ligger platt","06":"Undersidan mot plattan, pannorna uppåt","06b":"Undersidan mot plattan, pannorna uppåt",
 "06c":"Upp och ner: kragen mot plattan","06d":"Ligger platt","06e":"På högkant","07":"Står som den sitter","08":"Ligger platt, pannorna uppåt","09":"Står som den sitter","09b":"Ligger platt","10":"Står som det sitter",
 "11":"Hornurtaget mot plattan, axeltappen uppåt","14":"Upp och ner: överkanten mot plattan","15":"Står som det sitter","16":"Står, öppningen uppåt","16b":"Upp och ner","17":"Ligger platt","18":"Ligger platt","19":"Plattan nedåt",
 "21":"Står som de sitter","21b":"Ligger platt, ansiktet uppåt","22":"Öppningen uppåt","23":"Står som de sitter","24":"Distanserna uppåt","25":"Ligger platt"}
groups=collections.OrderedDict()
WK={'hornbrada':'Hörnbräda','sidofonster':'Sidofönster','skarmfonster':'Skärmfönstrets ram','dorroverstycke':'Dörröverstycke','kamerakrage':'Kamerakrage'}
for f in sorted(os.listdir('stl')):
    if f.startswith('05e_'):
        k=f[:-4]; parts_=k.split('_'); nm=WK[parts_[2]]+(' '+parts_[3] if len(parts_)>3 else '')
        NAME[k]=nm+', vit'; HOW[k]='Framsidan nedåt, den korta flänsen uppåt' if parts_[2]=='hornbrada' else 'Baksidan nedåt, hålen för tapparna mot plattan'
        P[f]=dict(color='#F2EDE1')
        groups.setdefault(k,[]).append(f)
    else: groups.setdefault(f.split('_')[0],[]).append(f)
PLATE, MARGIN, GAP, DUALW = 256.0, 5.0, 6.0, 235.5
XOFF=PLATE-DUALW          # höger munstycke når inte de 20,5 mm längst till vänster
items={}; times={}
def cover(m,zs):
    tz=m.vertices[m.faces][:,:,2]; lo,hi=tz.min(1),tz.max(1); return np.array([np.any((lo<=z)&(hi>=z)) for z in zs])
for g,fs in groups.items():
    ms=[trimesh.load('stl/'+f) for f in fs]
    v=np.vstack([m.vertices for m in ms]); lo,hi=v.min(0),v.max(0)
    items[g]=dict(files=fs, meshes=ms, lo=lo, w=hi[0]-lo[0], d=hi[1]-lo[1], h=hi[2]-lo[2], tpu=all('tpu' in f for f in fs))
    # tidsuppskattning: 0,20 mm lager, skal + 15 % fyllnad, färgbyten
    Hh=hi[2]-lo[2]; LH=0.2; layers=Hh/LH
    ext=sum(min(abs(m.volume), m.area*1.2+max(0,abs(m.volume)-m.area*0.6)*0.15) for m in ms)
    t=ext/11.0+layers*2.5
    if len(ms)>1:
        zs=np.arange(lo[2]+LH/2,hi[2],LH*5); cnt=np.array([cover(m,zs) for m in ms]).sum(0)
        t+=(cnt>=2).sum()*5*2*12+(cnt>=3).sum()*5*2*55
    times[g]=round(t/3600,2)
def pack(keys):
    pk=newPacker(pack_algo=MaxRectsBssf, rotation=True)
    for g in keys: pk.add_rect(int(np.ceil(items[g]['w']+GAP)*10), int(np.ceil(items[g]['d']+GAP)*10), rid=g)
    for _ in range(len(keys)): pk.add_bin(int((DUALW-2*MARGIN+GAP)*10), int((PLATE-2*MARGIN+GAP)*10))
    pk.pack(); out=[]
    for b in pk:
        if len(b)==0: continue
        rects=[]
        for r in b:
            it=items[r.rid]; rot=abs(r.width-int(np.ceil(it['w']+GAP)*10))>1 and abs(r.width-int(np.ceil(it['d']+GAP)*10))<=1
            rects.append((r.rid, r.x/10+MARGIN+XOFF, r.y/10+MARGIN, rot))
        out.append(rects)
    return out
DONE="Redan utskrivet"
PHASES=[(DONE, ["16","16b","24"]),
        (DONE, ["01"]),
        (DONE, ["03"]),
        ("Först: toleranstest och nötmall", ["00"]),
        ("Nästa: kroppen i rött och grått", ["05"]),
        ("Sedan: de vita detaljerna", [f[:-4] for f in sorted(os.listdir('stl')) if f.startswith('05e_')]),
        ("1. Kan skrivas ut direkt", ["01b","02","02b","03b","05b","05c","06","06b","06c","06d","06e","17","21","21b","22","23","25","04"]),
        ("2. Doseringen – när servot är uppmätt, provkör innan resten", ["10","11","14"]),
        ("3. När skärm, kamera och luckservo är uppmätta", ["05d","07","08","09","09b","15","18","19"])]
assert sorted(sum([p[1] for p in PHASES],[]))==sorted(items.keys()), set(items)^set(sum([p[1] for p in PHASES],[]))
plates=[]
for phase,keys in PHASES:
    a=[g for g in keys if not items[g]['tpu']]; t=[g for g in keys if items[g]['tpu']]
    a.sort(key=lambda g:-(items[g]['w']*items[g]['d']))
    plates+=[('ASA',p,phase) for p in pack(a)]+[('TPU',p,phase) for p in pack(t)]
Q=0.005; out=[]
for mat,rects,phase in plates:
    pl=dict(material=mat, phase=phase, items=[], groups=[], hours=0.0, printed=(phase==DONE))
    for g,x,y,rot in rects:
        it=items[g]; pl['hours']+=times[g]
        w,d=(it['d'],it['w']) if rot else (it['w'],it['d'])
        pl['groups'].append(dict(g=g,name=NAME[g],how=HOW[g],hours=times[g],cx=round(x+w/2,1),cy=round(y+d/2,1),top=round(float(it['h']),1),files=it['files'],
                                 colors=[P.get(f,{}).get('color','#9A9A9A') for f in it['files']]))
        for f,m in zip(it['files'],it['meshes']):
            v=m.vertices-it['lo']
            if rot: v=np.c_[v[:,1], it['w']-v[:,0], v[:,2]]
            v=v+[x,y,0]
            qv=np.clip(np.round(v/Q),0,65535).astype(np.uint16); idx=m.faces.astype(np.uint16 if len(v)<65536 else np.uint32)
            col=P.get(f,{}).get('color','#9A9A9A')
            if col.lower() in ('#2b2b2b','#1a1a1a'): col='#4A4D50'      # svarta delar syns bättre
            pl['items'].append(dict(group=g,file=f,color=col,pos=base64.b64encode(qv.tobytes()).decode(),idx=base64.b64encode(idx.tobytes()).decode(),i32=bool(idx.dtype==np.uint32)))
    pl['hours']=round(pl['hours'],2); pl['height']=max(gr['top'] for gr in pl['groups']); out.append(pl)
json.dump(out,open('plates.json','w')); json.dump(times,open('times.json','w'))
for i,pl in enumerate(out): print(i+1, pl['phase'][:2], pl['material'], pl['hours'], [gr['g'] for gr in pl['groups']])
print("total h", round(sum(times.values()),1), "| storlek", round(os.path.getsize('plates.json')/1e6,2),"MB")
