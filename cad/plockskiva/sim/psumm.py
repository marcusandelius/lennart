import sys, json
R=[json.loads(l) for l in open(sys.argv[1])]; R.sort(key=lambda r:(r['tag'],r['mu'],r['seed']))
for r in R:
    pc=r['per_cycle']; print('%-10s mu %.2f seed %d | %s | lev %d/%d tomma %d dubbla %d stopp %d+%d kvar %d fel %d ränna %d | %ds'%(r['tag'],r['mu'],r['seed'],''.join(map(str,pc)),sum(pc),r['start_in'],pc.count(0),sum(1 for x in pc if x>1),r['stall_f'],r['stall_b'],r['left'],r['fel'],r['i_rannan'],r['sec']))
