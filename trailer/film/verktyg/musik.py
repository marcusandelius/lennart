# Projekt Lennart - bakgrundsmusik. En egen, enkel komposition som genereras helt lokalt med numpy (ingen nedladdning, inga rattigheter att klarera).
# Kor:  W:\Blender\5.2\python\bin\python.exe musik.py <ut.wav> <langd i sekunder> [starttid for huvuddelen]
# Uppbyggnad: knappta strangar (pizzicato) i ett studsande ostinato, marimba-motiv, mjuk platta, bas och en latt shaker. D-dur, 96 slag per minut.
# Fram till "starttid for huvuddelen" spelas bara platta och ett glest tickande (oppningen ar spand), darefter hela arrangemanget.
import sys, wave, numpy as np
OUT, DUR = sys.argv[1], float(sys.argv[2]); MAIN = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
SR = 48000; BPM = 96; BEAT = 60 / BPM; BAR = 4 * BEAT; N = int((DUR + 4) * SR); rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    n = min(len(sig), N - i); L[i:i + n] += sig[:n] * gain * (1 - pan) / 2 * 1.4; R[i:i + n] += sig[:n] * gain * (1 + pan) / 2 * 1.4
def pluck(m, dur=1.2, bright=0.5):          # Karplus-Strong: knappt strang
    f = hz(m); p = int(SR / f); buf = rng.uniform(-1, 1, p); k = np.ones(3) / 3
    for _ in range(int(2 + (1 - bright) * 6)): buf = np.convolve(np.r_[buf[-1], buf, buf[0]], k, 'valid')
    n = int(dur * SR); out = np.empty(n); reps = n // p + 1; damp = 0.996
    for r in range(reps):
        a, b = r * p, min(n, (r + 1) * p); out[a:b] = buf[:b - a]; buf = damp * 0.5 * (buf + np.roll(buf, 1))
    return out * np.exp(-np.arange(n) / SR * 2.2)
def marimba(m, dur=0.9):
    t = np.arange(int(dur * SR)) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 16) + 0.1 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 30)) * (1 - np.exp(-t * 900))
def pad(notes, dur):
    t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for m in notes:
        for d in (-0.06, 0.05): s += np.sin(2 * np.pi * hz(m + d) * t + rng.uniform(0, 6)) + 0.25 * np.sin(2 * np.pi * hz(m + d) * 2 * t)
    env = np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 0.9); return s * env / len(notes) * (1 + 0.08 * np.sin(2 * np.pi * 0.23 * t))
def bass(m, dur):
    t = np.arange(int(dur * SR)) / SR; f = hz(m); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 2.5) * (1 - np.exp(-t * 200))
def shaker(dur=0.09):
    n = int(dur * SR); x = rng.normal(0, 1, n); x = np.diff(np.r_[0, x]); return x * np.exp(-np.arange(n) / SR * 45)
def tick():
    t = np.arange(int(0.05 * SR)) / SR; return np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 120)

# ackord: D - Bm - G - A, sedan D - F#m - G - A. (grundton for basen, treklang, toner till ostinatot)
CH = [(38, [62, 66, 69], [62, 66, 69, 74]), (35, [59, 62, 66], [59, 62, 66, 71]), (31, [59, 62, 67], [55, 59, 62, 67]), (33, [57, 61, 64], [57, 61, 64, 69]),
      (38, [62, 66, 69], [62, 66, 69, 74]), (30, [61, 66, 69], [57, 61, 66, 69]), (31, [59, 62, 67], [55, 59, 62, 67]), (33, [57, 61, 64], [57, 61, 64, 69])]
OST = [0, 2, 1, 3, 2, 1, 3, 2]                         # attondelar: studsande monster over ackordets toner
MOT = {0: [(0, 78), (1.5, 76), (2, 74), (3, 69)], 2: [(0, 74), (1, 76), (1.5, 74), (2.5, 71)], 4: [(0, 78), (1.5, 81), (2, 78), (3, 76)], 6: [(0.5, 74), (1.5, 71), (2, 69)]}
bars = int(DUR / BAR) + 1
for b in range(bars):
    t0 = b * BAR; root, tri, arp = CH[b % 8]; full = t0 >= MAIN; sec = (b // 8) % 4     # sektion: 0 glest, 1 fullt, 2 fullt med motiv, 3 lugnare
    add(pad(tri, BAR + 0.9), t0, 0.0, 0.11 if full else 0.16)
    if not full:
        for q in range(4): add(tick(), t0 + q * BEAT, 0.3 if q % 2 else -0.3, 0.05)
        add(bass(root + 12, BAR), t0, 0, 0.16); continue
    for e in range(8):
        if sec == 3 and e % 2: continue
        add(pluck(arp[OST[e]], 0.9, 0.55), t0 + e * BEAT / 2 + rng.uniform(-0.004, 0.004), -0.35 if e % 2 else 0.25, 0.30 * (1.0 if e % 4 == 0 else 0.72))
    add(bass(root, BEAT * 1.9), t0, 0, 0.42); add(bass(root + 7 if b % 2 else root, BEAT * 1.5), t0 + 2 * BEAT, 0, 0.3)
    if sec in (1, 2):
        for e in range(8):
            if e % 2: add(shaker(), t0 + e * BEAT / 2, 0.5, 0.05)
    if sec == 2 or (sec == 1 and b % 8 >= 4):
        for bt, m in MOT.get(b % 8, []): add(marimba(m), t0 + bt * BEAT, 0.15, 0.2)

# enkel rymd: nagra fordrojningar
def room(x):
    y = x.copy()
    for d, g in ((0.031, 0.22), (0.047, 0.18), (0.073, 0.14), (0.113, 0.1), (0.191, 0.07)):
        k = int(d * SR); y[k:] += x[:-k] * g
    return y
L, R = room(L), room(R[::1]); n = int(DUR * SR); L, R = L[:n], R[:n]; t = np.arange(n) / SR
env = np.minimum(1, t / 1.5) * np.minimum(1, (DUR - t) / 3.5); L *= env; R *= env
pk = max(np.abs(L).max(), np.abs(R).max()); s = np.stack([L, R], 1) / pk * 0.7
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((s * 32767).astype('<i2').tobytes()); w.close(); print('klar', OUT, round(DUR, 1), 's')
