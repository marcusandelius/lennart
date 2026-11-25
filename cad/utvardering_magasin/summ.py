import sys, json, collections
R=[json.loads(l) for l in open(sys.argv[1])]
G=collections.defaultdict(list)
for r in R: G[(r['tag'],r['mu'])].append(r)
print('%-14s %-5s %-4s %-9s %-6s %-6s %-6s %-5s %s'%('variant','mu','körn','levererat','tomma','dubbla','stopp','kvar','mönster per körning'))
for (t,mu),rs in sorted(G.items()):
    n=sum(r['n'] for r in rs); dl=sum(sum(r['per_cycle']) for r in rs)
    emp=sum(r['per_cycle'].count(0) for r in rs); dbl=sum(sum(1 for x in r['per_cycle'] if x>=2) for r in rs); st=sum(r['stall_f']+r['stall_b'] for r in rs); left=sum(r['left'] for r in rs)
    print('%-14s %-5s %-4d %3d/%-5d %-6d %-6d %-6d %-5d %s'%(t,mu,len(rs),dl,n,emp,dbl,st,left,' '.join(''.join(map(str,r['per_cycle'])) for r in sorted(rs,key=lambda r:r['seed']))[:110]))
