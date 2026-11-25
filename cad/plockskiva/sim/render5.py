import json, pickle, os, numpy as np, trimesh
import plock as K
A={k:trimesh.Trimesh(v,f,process=False) for k,(v,f) in pickle.load(open('../A_parts.pkl','rb')).items()}
P={n:trimesh.load('ut5/asm/%s.stl'%n) for n in ('plockskiva','doserstativ','skivkapa','omrorare','notforrad','servo_mg996r')}
def soup(m): return [round(float(v), 2) for v in m.vertices[m.faces].ravel()]
def moved(m, d): m=m.copy(); m.apply_translation(d); return m
def bx(x0,x1,y0,y1,z0,z1):
    m=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
G={n:soup(m) for n,m in P.items()}
for n in ('skarmklamma','kamerafaste','elektroniklada','ellock','kropp','kropp_sockel'): G[n]=soup(A[n])
G['kontakter']=soup(trimesh.util.concatenate([bx(-25.4,25.4,21.7,35.7,108+s_*8.89-1.6,108+s_*8.89+1.6) for s_ in (1,-1)]))
for n_,f_ in (('ficka','19_skarmficka'),('regel','19b_skarmficka_regel'),('kort','skarmkort_ungefar')): G[n_]=soup(trimesh.load('../ficka/ut/%s.stl'%f_))
E=K.EW
G['x_stativ']=soup(P['doserstativ']); G['x_servo']=soup(moved(P['servo_mg996r'], -E*45)); G['x_skiva']=soup(moved(P['plockskiva'], E*38))
G['x_kapa']=soup(moved(P['skivkapa'], E*38+np.array([0,-38,0]))); G['x_forrad']=soup(moved(P['notforrad'], np.array([20,0,95]))); G['x_omr']=soup(moved(P['omrorare'], E*150))
if os.path.exists('snap_kap85.npy'):
    S=np.load('snap_kap85.npy',allow_pickle=True).item(); ns=[]
    def qmat(q):
        w,x,y,z=q; return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
    for p,q,s in zip(S['pos'],S['quat'],S['size']):
        if p[2] > K.ZT - 2 or p[2] < 20: continue
        e=trimesh.creation.icosphere(subdivisions=2,radius=1.0); e.apply_scale(s); M=np.eye(4); M[:3,:3]=qmat(q); M[:3,3]=p; e.apply_transform(M); ns.append(e)
    G['nuts']=soup(trimesh.util.concatenate(ns)); print('nötter i bilden', len(ns))
# utskriftsläge
x=0
for f,k in (('14_notforrad','u_forrad'),('10_doserstativ','u_stativ'),('11_plockskiva','u_skiva'),('10b_skivkapa','u_kapa'),('11b_omrorare','u_omr')):
    m=trimesh.load('ut5/%s.stl'%f); tr=[x - m.bounds[0][0], -m.bounds[:,1].mean(), 0]; m.apply_translation(tr); x = m.bounds[1][0] + 14; G[k]=soup(m)
    if f=='11b_omrorare' and os.path.exists('ut5/11c_omrorare_motiv.stl'):
        il=trimesh.load('ut5/11c_omrorare_motiv.stl'); il.apply_translation(tr); G['u_omr_motiv']=soup(il)
G['bed']=soup(bx(-10, x, -70, 70, -1.0, 0.0))
json.dump(G, open('../render/geo_v5.json','w')); print('klar', {k: len(v)//9 for k,v in G.items()}, 'bredd', round(x))
