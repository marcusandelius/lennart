"""Livebilden på lennart.cam: inställningar och vidarebefordran av bilder.

Pi:n kan inte ta emot anrop (den sitter bakom 4G-operatörens NAT), så flödet är:

  1. Pi:n håller ett anrop öppet mot /api/live/wait och väntar.
  2. När en besökare öppnar livebilden svarar servern direkt: "skicka bilder".
  3. Pi:n skickar JPEG-bilder till /api/live/frame så länge någon tittar.
  4. Servern skickar varje ny bild vidare till alla som tittar (/live.mjpg).

Ingen tittar = inga bilder skickas = ingen mobildata går åt.
"""

import json
import os
import tempfile
import threading
import time
from pathlib import Path

# Upplösningar som admin kan välja. Kameran levererar 1280 × 720, så större går inte.
RESOLUTIONS = {
    "426x240": (426, 240),
    "640x360": (640, 360),
    "960x540": (960, 540),
    "1280x720": (1280, 720),
}

DEFAULTS = {
    "live_enabled": True,   # av-knappen i adminvyn
    "resolution": "640x360",
    "fps": 2,               # bilder per sekund
    "quality": 70,          # JPEG-kvalitet, 30–90
    "max_view_min": 5,      # efter så här många minuter får besökaren klicka igen
}

LIMITS = {"fps": (1, 10), "quality": (30, 90), "max_view_min": (1, 30)}

MAX_VIEWERS = 25            # skyddar Pi:ns uppkoppling och servern
NO_FRAME_GIVE_UP_S = 20     # ingen bild från Pi:n på så här länge = avsluta strömmen


def validate(changes: dict, current: dict) -> dict:
    """Kontrollera ändringar från adminvyn. Okända fält och fel värden ger ValueError."""
    result = dict(current)
    for key, value in changes.items():
        if key == "live_enabled":
            if not isinstance(value, bool):
                raise ValueError("live_enabled ska vara sant eller falskt")
        elif key == "resolution":
            if value not in RESOLUTIONS:
                raise ValueError(f"Okänd upplösning: {value}")
        elif key in LIMITS:
            low, high = LIMITS[key]
            if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
                raise ValueError(f"{key} ska vara ett heltal mellan {low} och {high}")
        else:
            raise ValueError(f"Okänd inställning: {key}")
        result[key] = value
    return result


class Settings:
    """Inställningarna sparas i DATA_DIR/settings.json, så att de överlever en deploy.

    Finns ingen skrivbar DATA_DIR (ingen volym i Coolify) hålls de bara i minnet,
    och adminvyn säger det.
    """

    def __init__(self, data_dir: str) -> None:
        self.path = Path(data_dir) / "settings.json"
        self.values = dict(DEFAULTS)
        self.persisted = False
        try:
            saved = json.loads(self.path.read_text())
            self.values = validate({k: v for k, v in saved.items() if k in DEFAULTS}, DEFAULTS)
        except (OSError, ValueError):
            pass
        self.persisted = self._writable()

    def _writable(self) -> bool:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            probe = self.path.parent / ".skrivtest"
            probe.write_text("ok")
            probe.unlink()
            return True
        except OSError:
            return False

    def update(self, changes: dict) -> dict:
        self.values = validate(changes, self.values)
        if self._writable():
            # Skriv till en tillfällig fil och byt namn, så att filen aldrig blir halvskriven.
            fd, tmp = tempfile.mkstemp(dir=self.path.parent)
            with os.fdopen(fd, "w") as f:
                json.dump(self.values, f)
            os.replace(tmp, self.path)
            self.persisted = True
        else:
            self.persisted = False
        return self.values

    def for_pi(self) -> dict:
        width, height = RESOLUTIONS[self.values["resolution"]]
        return {"width": width, "height": height, "fps": self.values["fps"], "quality": self.values["quality"]}


class LiveRelay:
    """Håller reda på tittare och senaste bilden från Pi:n."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.cond = threading.Condition()
        self.viewers = 0
        self.frame: bytes | None = None
        self.frame_id = 0
        self.frame_time = 0.0

    @property
    def wanted(self) -> bool:
        return self.settings.values["live_enabled"] and self.viewers > 0

    def notify(self) -> None:
        with self.cond:
            self.cond.notify_all()

    def add_viewer(self) -> bool:
        with self.cond:
            if self.viewers >= MAX_VIEWERS:
                return False
            self.viewers += 1
            self.cond.notify_all()  # väck Pi:ns väntande anrop
            return True

    def remove_viewer(self) -> None:
        with self.cond:
            self.viewers = max(0, self.viewers - 1)
            self.cond.notify_all()

    def wait_until_wanted(self, timeout: float) -> bool:
        """Används av Pi:ns väntande anrop: returnerar True så fort någon tittar."""
        with self.cond:
            return self.cond.wait_for(lambda: self.wanted, timeout=timeout)

    def put_frame(self, jpeg: bytes) -> None:
        with self.cond:
            self.frame = jpeg
            self.frame_id += 1
            self.frame_time = time.time()
            self.cond.notify_all()

    def wait_frame(self, last_id: int, timeout: float) -> tuple[int, bytes] | None:
        """Vänta på en bild som är nyare än last_id. None om ingen kommer eller livebilden stängs av."""
        with self.cond:
            ok = self.cond.wait_for(
                lambda: self.frame_id != last_id or not self.settings.values["live_enabled"],
                timeout=timeout,
            )
            if not ok or not self.settings.values["live_enabled"] or self.frame is None:
                return None
            return self.frame_id, self.frame

    def info(self) -> dict:
        age = time.time() - self.frame_time if self.frame_time else None
        width, height = RESOLUTIONS[self.settings.values["resolution"]]
        return {
            "enabled": self.settings.values["live_enabled"],
            "viewers": self.viewers,
            "max_viewers": MAX_VIEWERS,
            "resolution": f"{width} × {height}",
            "fps": self.settings.values["fps"],
            "max_view_min": self.settings.values["max_view_min"],
            "last_frame_age_s": round(age) if age is not None else None,
        }
