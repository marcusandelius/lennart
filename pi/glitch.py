"""Glitch-effekt när skärmen byter läge, till exempel från VÄNTAR PÅ BESÖKARE… till ACCESS GRANTED.

Övergången är några bilder där den gamla och den nya skärmbilden blandas med typiska
digitala störningar:
- horisontella band som förskjuts i sidled,
- färgkanalerna rött och blått som glider isär,
- några rader med brus.

Störningen är starkast i mitten av övergången. Bilden byter från den gamla till den nya
ungefär halvvägs, med ett par snabba flimmer fram och tillbaka.

Det här är en egen tolkning. Trailerns glitch (12–13 s) är inte jämförd än [verifiera].
"""

import numpy as np

FRAMES = 8  # cirka 0,4 s på skärmen, som klarar ungefär 20 bilder per sekund


def frames(old: np.ndarray, new: np.ndarray, count: int = FRAMES, seed: int | None = None) -> list[np.ndarray]:
    """Bilderna mellan old och new, utan själva slutbilden. Båda har formen (höjd, bredd, 3)."""
    rng = np.random.default_rng(seed)
    height, width = new.shape[:2]
    out = []
    for k in range(1, count + 1):
        t = k / (count + 1)                   # 0 → 1 genom övergången
        strength = float(np.sin(np.pi * t))   # 0 i början och slutet, 1 i mitten
        flicker = 0.25 < t < 0.75 and rng.random() < 0.35  # flimmer bara i mitten av övergången
        img = (old if (t < 0.5) != flicker else new).copy()

        # Förskjutna band
        for _ in range(int(2 + 6 * strength)):
            y = int(rng.integers(0, height))
            band = img[y:y + int(rng.integers(3, 25))]
            band[:] = np.roll(band, int(rng.integers(-60, 61) * strength), axis=1)

        # Rött och blått glider isär
        shift = int(2 + 8 * strength)
        img[..., 0] = np.roll(img[..., 0], shift, axis=1)
        img[..., 2] = np.roll(img[..., 2], -shift, axis=1)

        # Brusrader
        for _ in range(int(1 + 4 * strength)):
            y = int(rng.integers(0, height))
            rows = img[y:y + int(rng.integers(1, 4))]
            rows[:] = rng.integers(0, 256, size=rows.shape, dtype=np.uint8)

        out.append(img)
    return out
