import pickle, json, numpy as np, trimesh, os
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
G={}
def put(k,m,t=(0,0,0)):
    m=m.copy(); m.apply_translation(t); G[k]=np.round(m.vertices[m.faces].reshape(-1),2).tolist()
put('kropp',A['kropp']); put('kropp_vit',A['kropp_vit']); put('kropp_sockel',A['kropp_sockel'])
for n in ('notforrad','doserstativ','plockskiva'): put(n,trimesh.load('../p2/ut5/asm/%s.stl'%n))
L=lambda n: trimesh.load('ut/asm/%s.stl'%n)
for n in ('elbakstycke','elkapa','komponentplatta','elpackning'): put(n,L(n))
sp={f[:-4]:trimesh.load('ut/spoken/'+f) for f in os.listdir('ut/spoken')}
groups={'k_pi':['pi5'],'k_pi_kontakt':['pi5_natverkskontakt','pi5_usbc'],'k_pca':['pca9685'],'k_kond':['kondensator'],'k_ekm':['ekm006'],
        'k_psu':['servoomvandlare'],'k_wago':['dcjack'],'k_key':['keystone1','keystone2'],'k_rj':['rj45_1','rj45_2']}
for g,ns in groups.items():
    m=trimesh.util.concatenate([sp[n] for n in ns])
    put(g,m); put(g+'_upp',m,(0,0,120))
put('elkapa_upp',L('elkapa'),(0,0,265)); put('komponentplatta_upp',L('komponentplatta'),(0,0,120))
# utskriftsläge
off={'16_elbakstycke':(-80,30,0),'16b_elkapa':(80,30,0),'24_komponentplatta':(80,-130,0),'17_elpackning':(-80,-130,0)}
for n,t in off.items(): put('p_'+n,trimesh.load('ut/print/%s.stl'%n),t)
json.dump(G,open('../render/geo_el.json','w'))
print(len(G))
