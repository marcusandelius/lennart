# Körd 2026-11-15 i /home/claude/fix: bredda nöthålet från 27 till 31 mm i vägg, stengrund och skålens bakvägg.
from lib import *
parts,P=load('parts_v8.json')
W=15.5
cut_wall=box(-W,W,-0.3,3.5,3.0,32.5)                     # nöthålet i framväggen, nu 31 mm brett, samma överkant som förut
cut_bowl=box(-W,W,-4.5,0.1,3.0,28.5)
put(parts,P,'kropp',M(P,'kropp')-cut_wall)
put(parts,P,'kropp_sockel',M(P,'kropp_sockel')-cut_wall)
for n in ('skal','skal_vit'): put(parts,P,n,M(P,n)-cut_bowl)
json.dump(parts,open('parts_v11base.json','w'))
