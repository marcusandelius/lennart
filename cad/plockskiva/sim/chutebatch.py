import sys, json, subprocess
from multiprocessing import Pool
def go(a): 
    r = subprocess.run([sys.executable, 'chutesim.py', json.dumps(a)], capture_output=True, text=True)
    return (r.stdout.strip().splitlines() or ['FEL ' + r.stderr[-300:]])[-1]
if __name__ == '__main__':
    jobs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    with Pool(4) as p:
        for line in p.imap_unordered(go, jobs): print(line, flush=True); open(sys.argv[2], 'a').write(line + '\n')
