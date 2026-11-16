# Projekt Lennart - forarbete av rosten, fore EQ och kompression (det en ljudtekniker gor for hand i klippbordet).
#   1. hittar fraserna (tal mellan pauser) och jamnar ut ljudstyrkan fras for fras, hogst +-4 dB, sa att kompressorn kan arbeta mildare
#   2. sanker andetag och annat svagt ljud mellan fraserna med 8 dB (tas inte bort, da later det klippt)
# Langden andras inte, sa tiderna i ljudmix.mjs (SEG) galler fortfarande.
# Kor:  <Blenders python> rost.py <in.wav mono 32 bit> <ut.wav>
import sys, wave, numpy as np
w = wave.open(sys.argv[1], 'rb'); SR = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i4').astype(np.float64) / 2**31; w.close()
H = SR // 100                                                # 10 ms steg
n = len(x) // H; e = np.sqrt(np.convolve((x[:n * H] ** 2).reshape(n, H).mean(1), np.ones(3) / 3, 'same') + 1e-14); db = 20 * np.log10(e)
top = np.percentile(db, 95); act = db > top - 30             # tal: inom 30 dB fran de starka partierna
def runs(m):
    d = np.diff(np.concatenate([[0], m.astype(int), [0]])); return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))
for a, b in runs(~act):                                      # pauser kortare an 0,35 s hor till frasen
    if b - a < 35 and a > 0 and b < n: act[a:b] = True
for a, b in runs(act):                                       # blippar kortare an 0,12 s ar inte tal
    if b - a < 12: act[a:b] = False
fr = runs(act)
lvl = [10 * np.log10(np.mean(e[a:b][db[a:b] > top - 20] ** 2) + 1e-14) if (db[a:b] > top - 20).any() else None for a, b in fr]
mal = np.median([l for l in lvl if l is not None])
g = np.zeros(n); pts = []                                    # forstarkning i dB per 10 ms: konstant inom frasen, glider mjukt i pauserna
for (a, b), l in zip(fr, lvl):
    k = 0.0 if l is None else float(np.clip((mal - l) * 0.85, -4, 4)); pts += [(a, k), (b - 1, k)]
g = np.interp(np.arange(n), [p[0] for p in pts], [p[1] for p in pts])
pad = act.copy()                                             # 60 ms marginal runt talet sa att ordslut och ansatser inte dampas
for a, b in fr: pad[max(0, a - 6):min(n, b + 6)] = True
dmp = np.where(pad, 0.0, -8.0); dmp = np.convolve(dmp, np.ones(5) / 5, 'same')      # mjuka overgangar, 50 ms
gs = np.interp(np.arange(len(x)), np.arange(n) * H + H / 2, g + dmp)
y = np.clip(x * 10 ** (gs / 20), -1, 1)
o = wave.open(sys.argv[2], 'wb'); o.setnchannels(1); o.setsampwidth(4); o.setframerate(SR); o.writeframes((y * (2**31 - 1)).astype('<i4').tobytes()); o.close()
ks = [p[1] for p in pts[::2]]; svag = (~pad) & (db > -75)
print('rost: %d fraser, niva %.1f dB, justering %.1f till %+.1f dB (medel %.1f dB i belopp), %.1f s andetag och svagt ljud sankt 8 dB' % (len(fr), mal, min(ks), max(ks), np.mean(np.abs(ks)), svag.sum() / 100))
