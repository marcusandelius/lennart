"""Demoläge för skärmen: ACCESS GRANTED eller ACCESS DENIED på slump när något rör sig.

Tills bildigenkänningen finns visar demoläget hur stationen ska bete sig:
skärmen visar kamerabilden, och när något rör sig framför kameran lottas
ACCESS GRANTED eller ACCESS DENIED fram och visas i några sekunder.

Rörelsen mäts på samma sätt som för inspelningen (se recorder.py): bilden krymps
till ungefär 80 × 45 bildpunkter i gråskala och jämförs med en långsamt
uppdaterad bakgrundsbild. Rörelsegränsen och ljusgränsen är desamma som för
inspelningen och ställs in i adminvyn.
"""

import random

import numpy as np

from recorder import PIXEL_CHANGE, SMALL_STEP, WARMUP_S

HOLD_S = 4.0       # så länge ACCESS-bilden visas
COOLDOWN_S = 3.0   # vila efter varje visning, så att samma rörelse inte lottas om och om igen
RESULTS = ("granted", "denied")


class DemoMode:
    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()
        self.triggers = 0   # antal lottningar sedan start
        self.reset()

    def reset(self) -> None:
        """Börja om, t.ex. när demoläget slås på. Bakgrunden lärs in på nytt."""
        self.background = None
        self.warm_until = 0.0
        self.moving_frames = 0
        self.motion = 0.0          # senaste rörelsevärdet i promille
        self.brightness = None     # senaste ljusstyrkan, 0–100
        self.showing = None        # "granted" eller "denied" medan en ACCESS-bild visas
        self.until = 0.0
        self.quiet_until = 0.0

    def screen(self, now: float) -> str:
        """Vad skärmen ska visa just nu: "camera", "granted" eller "denied"."""
        if self.showing is not None and now >= self.until:
            self.showing = None
        return self.showing or "camera"

    def feed(self, rgb: np.ndarray, now: float, sensitivity: float, min_brightness: float) -> None:
        """Anropas med varje kamerabild (RGB, redan roterad) medan demoläget är på."""
        small = rgb[::SMALL_STEP, ::SMALL_STEP].astype(np.float32)
        gray = small[..., 0] * 0.299 + small[..., 1] * 0.587 + small[..., 2] * 0.114
        self.brightness = round(float(gray.mean()) / 255 * 100, 1)
        if self.background is None or self.background.shape != gray.shape:
            self.background = gray
            self.warm_until = now + WARMUP_S
            self.moving_frames, self.motion = 0, 0.0
            return
        diff = np.abs(gray - self.background)
        diff -= np.median(diff)                      # räkna bort ljusändringar över hela bilden
        self.motion = float((diff > PIXEL_CHANGE).mean() * 1000)
        resting = now < self.warm_until or self.showing is not None or now < self.quiet_until
        # Bakgrunden följer långsamt med, så att skuggor och ljus som ändras sakta inte räknas.
        # Medan en ACCESS-bild visas och under vilan efteråt går det fortare, så att ett djur
        # som blir sittande räknas som bakgrund. Då är det bara ny rörelse som lottas.
        rate = 0.3 if now < self.warm_until else 0.1 if resting else 0.02
        self.background += (gray - self.background) * rate

        if resting or self.brightness < min_brightness:
            self.moving_frames = 0
            return
        # Två bilder i rad över gränsen krävs, så att enstaka brus inte räknas som rörelse.
        self.moving_frames = self.moving_frames + 1 if self.motion >= sensitivity else 0
        if self.moving_frames >= 2:
            self.showing = self.rng.choice(RESULTS)
            self.until = now + HOLD_S
            self.quiet_until = self.until + COOLDOWN_S
            self.moving_frames = 0
            self.triggers += 1
            print(f"Demoläge: rörelse ({self.motion:.0f} ‰), lottade ACCESS {self.showing.upper()}", flush=True)

    def info(self, now: float, sensitivity: float, min_brightness: float) -> str:
        if now < self.warm_until:
            state = "lär in bakgrunden"
        elif self.showing is not None:
            state = f"visar ACCESS {self.showing.upper()}"
        elif self.brightness is not None and self.brightness < min_brightness:
            state = f"för mörkt (ljus {self.brightness:.0f}, gräns {min_brightness})"
        else:
            state = f"väntar på rörelse (just nu {self.motion:.0f} ‰, gräns {sensitivity} ‰)"
        return f"Demoläge: {state} · {self.triggers} lottningar sedan start"
