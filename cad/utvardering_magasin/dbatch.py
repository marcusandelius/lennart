import sys, json, time
from multiprocessing import Pool
from discsim import run
def go(a):
    t0 = time.time(); r = run(**a); r["sec"] = round(time.time() - t0); return r
if __name__ == "__main__":
    out = sys.argv[1]; jobs = [json.loads(l) for l in open(sys.argv[2]) if l.strip()]
    with Pool(4) as p:
        for r in p.imap_unordered(go, jobs): open(out, "a").write(json.dumps(r) + "\n")
