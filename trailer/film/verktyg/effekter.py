# Projekt Lennart - ljudeffekter. Namn som finns i S syntetiseras har med numpy. Ovriga namn lases som wav ur mappen fx (Kenneys ljudpaket, CC0).
# Kor:  <Blenders python> effekter.py <handelser.json> <ut.wav> <langd i sekunder>
# handelser.json: [[namn, tid i sekunder, niva i dB, {valfritt: "dur": s, "pitch": faktor, "pan": -1..1}], ...]   (skrivs av ljudmix.mjs)
import sys, json, wave, numpy as np
EV = json.load(open(sys.argv[1], encoding='utf8')); OUT = sys.argv[2]; DUR = float(sys.argv[3]); SR = 48000; N = int(DUR * SR) + SR; rng = np.random.default_rng(3)
L = np.zeros(N); R = np.zeros(N)
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, fc):                       # enpoligt lagpassfilter
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def hp(x, fc): return x - lp(x, fc)
def norm(x): return x / (np.abs(x).max() + 1e-9)

def pip(p=1.0, **k): t = tt(0.075); return np.sin(2 * np.pi * 1320 * p * t) * np.minimum(1, t / 0.004) * np.minimum(1, (0.075 - t) / 0.02)
def klick(p=1.0, **k): t = tt(0.03); return hp(rng.normal(0, 1, len(t)), 1500) * np.exp(-t * 220) + 0.6 * np.sin(2 * np.pi * 2400 * p * t) * np.exp(-t * 300)
def tick(p=1.0, **k): t = tt(0.012); return np.sin(2 * np.pi * 3200 * p * t) * np.exp(-t * 500) + 0.4 * rng.normal(0, 1, len(t)) * np.exp(-t * 900)
def duns(p=1.0, **k): t = tt(0.3); return np.sin(2 * np.pi * (75 * p) * t * (1 + 0.6 * np.exp(-t * 40))) * np.exp(-t * 16) + 0.25 * hp(rng.normal(0, 1, len(t)), 800) * np.exp(-t * 180)
def knack(p=1.0, **k): t = tt(0.09); return (np.sin(2 * np.pi * 420 * p * t) + 0.6 * np.sin(2 * np.pi * 930 * p * t) + 0.3 * np.sin(2 * np.pi * 1710 * p * t)) * np.exp(-t * 70)
def pop(p=1.0, **k): t = tt(0.09); f = 320 * p * (1 + 2.2 * t / 0.09); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38) * np.minimum(1, t / 0.002)
def svep(p=1.0, dur=1.0, **k):       # mjukt sus som stiger i ton
    t = tt(dur); x = rng.normal(0, 1, len(t)); u = t / dur; f = 500 * p * (1 + 3.5 * u); ph = np.cumsum(f) / SR
    return (lp(hp(x, 300), 2500 * p) * 0.9 + 0.25 * np.sin(2 * np.pi * ph)) * np.sin(np.pi * u) ** 1.5
def slutare(**k): t = tt(0.14); x = hp(rng.normal(0, 1, len(t)), 2000); return x * (np.exp(-t * 180) + 0.8 * np.exp(-np.maximum(0, t - 0.07) * 200) * (t > 0.07))
def nej(**k): t = tt(0.34); s = np.sign(np.sin(2 * np.pi * 155 * t)) * 0.5 + np.sin(2 * np.pi * 155 * t); return lp(s, 900) * ((t < 0.13) | (t > 0.18)) * np.minimum(1, (0.34 - t) / 0.03)
def ja(**k):
    t = tt(0.75); a = np.sin(2 * np.pi * 660 * t) * np.exp(-t * 7); b = np.sin(2 * np.pi * 990 * np.maximum(0, t - 0.14)) * np.exp(-np.maximum(0, t - 0.14) * 6) * (t > 0.14); return (a + b) * np.minimum(1, t / 0.005)
def klang(p=1.0, **k): t = tt(0.9); return (np.sin(2 * np.pi * 1760 * p * t) + 0.5 * np.sin(2 * np.pi * 2640 * p * t) + 0.2 * np.sin(2 * np.pi * 3520 * p * t)) * np.exp(-t * 5.5) * np.minimum(1, t / 0.004)
def servo(p=1.0, dur=0.6, **k):      # litet servo: surrande ton som stiger nagot
    t = tt(dur); u = t / dur; f = 190 * p * (1 + 0.35 * np.sin(np.pi * u)); ph = np.cumsum(f) / SR; saw = 2 * (ph % 1) - 1
    return lp(saw + 0.3 * rng.normal(0, 1, len(t)), 1800) * (1 + 0.3 * np.sin(2 * np.pi * 31 * t)) * np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.05)
def tallrik(p=1.0, dur=1.4, **k):   # ett porslinsfat som snurrar ut som ett mynt: klirrande kontakter som kommer allt tatare medan de blir svagare, och ett tvart slut
    t = tt(dur + 0.25); y = np.zeros(len(t)); s_ = 0.0; n = 0
    while True:                     # en kontakt per kvarts varv; varvet foljer samma kurva som fatet i akt_plan.py (2,2 + 6 s varv per sekund)
        s_ = (-2.2 + np.sqrt(2.2 ** 2 + 4 * 3.0 * n / 4)) / (2 * 3.0); n += 1
        if s_ >= dur: break
        amp = (1 - s_ / dur) ** 1.3 * (1.0 if n > 1 else 1.25); i0 = int(s_ * SR); m = len(t) - i0; u = np.arange(m) / SR
        part = sum(g * np.sin(2 * np.pi * f * p * (1 + 0.004 * rng.normal()) * u) * np.exp(-u * dk) for f, g, dk in ((1870, 1.0, 38), (3040, 0.6, 55), (4710, 0.35, 80), (6350, 0.15, 120)))
        y[i0:] += amp * part * (0.75 + 0.5 * rng.random())
    hum = lp(rng.normal(0, 1, len(t)), 900) * np.minimum(1, t / 0.05) * np.clip(1 - t / dur, 0, 1) ** 1.6 * 0.08   # mycket svagt rullande sus under (starkare lat blasigt)
    return y + hum
S = dict(tallrik=tallrik, pip=pip, klick=klick, tick=tick, duns=duns, knack=knack, pop=pop, svep=svep, slutare=slutare, nej=nej, ja=ja, klang=klang, servo=servo)
import os
FXD = sys.argv[4] if len(sys.argv) > 4 else ''
def fil(name):      # inspelat ljud (wav, mono, 48 kHz) ur mappen fx
    w = wave.open(os.path.join(FXD, name + '.wav'), 'rb'); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float); w.close(); return x
for name, t0, db, *o in EV:
    o = o[0] if o else {}; x = norm(S[name](p=o.get('pitch', 1.0), dur=o.get('dur', 1.0)) if name in S else fil(name)) * 10 ** (db / 20); i = int(t0 * SR); pan = o.get('pan', 0.0)
    if i < 0 or i >= N: continue
    n = min(len(x), N - i); L[i:i + n] += x[:n] * (1 - 0.5 * pan) ; R[i:i + n] += x[:n] * (1 + 0.5 * pan)
def room(x):
    y = x.copy()
    for d, g in ((0.023, 0.16), (0.041, 0.11), (0.067, 0.07)):
        k = int(d * SR); y[k:] += x[:-k] * g
    return y
n = int(DUR * SR); s = np.clip(np.stack([room(L)[:n], room(R)[:n]], 1), -1, 1)
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((s * 32767).astype('<i2').tobytes()); w.close(); print('effekter klara', len(EV), 'st')
