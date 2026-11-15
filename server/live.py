"""Livebilden på lennart.cam: inställningar, kommandon och vidarebefordran av bilder.

Pi:n kan inte ta emot anrop (den sitter bakom 4G-operatörens NAT), så flödet är:

  1. Pi:n håller ett anrop öppet mot /api/live/wait och väntar.
  2. När en besökare öppnar livebilden svarar servern direkt: "skicka bilder".
  3. Pi:n skickar JPEG-bilder till /api/live/frame så länge någon tittar.
  4. Servern skickar varje ny bild vidare till alla som tittar (/live.mjpg).

Ingen tittar = inga bilder skickas = ingen mobildata går åt.

Samma väntande anrop används för att skicka inställningar (t.ex. kamerans
rotation) och kommandon (t.ex. "flytta servot") till Pi:n direkt, utan att
Pi:n behöver öppna några portar.
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

CAMERA_ROTATIONS = (0, 90, 180, 270)  # grader medsols

DEFAULTS = {
    "live_enabled": True,   # av-knappen i adminvyn
    "resolution": "640x360",
    "fps": 2,               # bilder per sekund
    "quality": 70,          # JPEG-kvalitet, 30–90
    "max_view_min": 5,      # efter så här många minuter får besökaren klicka igen
    "camera_rotation": 0,   # vrid kamerabilden, t.ex. om kameran sitter på sidan
    # Servona sitter på PCA9685-kortet. Pulsbredden styr vinkeln: min_us = 0°, max_us = 180°.
    "servo_doser_channel": 0,
    "servo_lucka_channel": 1,
    "servo_min_us": 500,
    "servo_max_us": 2500,
    "dispense_angle": 130,  # så långt doseringshjulet vrids för att släppa en nöt
}

LIMITS = {
    "fps": (1, 10), "quality": (30, 90), "max_view_min": (1, 30),
    "servo_doser_channel": (0, 15), "servo_lucka_channel": (0, 15),
    "servo_min_us": (400, 1500), "servo_max_us": (1500, 2600),
    "dispense_angle": (30, 180),
}

# Vad Pi:n behöver veta om inställningarna (allt utom livebildens egna).
DEVICE_KEYS = ("camera_rotation", "servo_doser_channel", "servo_lucka_channel",
               "servo_min_us", "servo_max_us", "dispense_angle")

SERVOS = ("doser", "lucka")
COMMAND_MAX_AGE_S = 20      # äldre kommandon kastas, så att inget servo rör sig långt senare

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
        elif key == "camera_rotation":
            if value not in CAMERA_ROTATIONS or isinstance(value, bool):
                raise ValueError("camera_rotation ska vara 0, 90, 180 eller 270")
        elif key in LIMITS:
            low, high = LIMITS[key]
            if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
                raise ValueError(f"{key} ska vara ett heltal mellan {low} och {high}")
        else:
            raise ValueError(f"Okänd inställning: {key}")
        result[key] = value
    if result["servo_doser_channel"] == result["servo_lucka_channel"]:
        raise ValueError("Doseraren och luckan kan inte sitta på samma kanal")
    if result["servo_min_us"] >= result["servo_max_us"]:
        raise ValueError("servo_min_us måste vara mindre än servo_max_us")
    return result


def validate_command(cmd: dict, values: dict) -> dict:
    """Kontrollera ett servokommando från adminvyn."""
    action = cmd.get("action")
    if action == "move":
        if cmd.get("servo") not in SERVOS:
            raise ValueError("Okänt servo")
        angle = cmd.get("angle")
        if isinstance(angle, bool) or not isinstance(angle, int) or not 0 <= angle <= 180:
            raise ValueError("Vinkeln ska vara ett heltal mellan 0 och 180")
        slow = cmd.get("slow", False)
        if not isinstance(slow, bool):
            raise ValueError("slow ska vara sant eller falskt")
        return {"action": "move", "servo": cmd["servo"], "angle": angle, "slow": slow}
    if action == "release":
        if cmd.get("servo") not in SERVOS + ("alla",):
            raise ValueError("Okänt servo")
        return {"action": "release", "servo": cmd["servo"]}
    if action == "test_dispense":
        return {"action": "test_dispense", "angle": values["dispense_angle"]}
    raise ValueError("Okänt kommando")


class Settings:
    """Inställningarna sparas i DATA_DIR/settings.json, så att de överlever en deploy.

    Är DATA_DIR ingen monterad volym försvinner filen vid nästa deploy, och
    adminvyn varnar för det.
    """

    def __init__(self, data_dir: str) -> None:
        self.path = Path(data_dir) / "settings.json"
        self.values = dict(DEFAULTS)
        self.persisted = False
        # Räknas upp vid varje ändring, så att Pi:n ser när något ändrats. Startar på
        # klockslaget, så att en omstart av servern också räknas som en ändring.
        self.version = int(time.time())
        try:
            saved = json.loads(self.path.read_text())
            self.values = validate({k: v for k, v in saved.items() if k in DEFAULTS}, DEFAULTS)
        except (OSError, ValueError):
            pass
        self.persisted = self._durable()

    def _durable(self) -> bool:
        """Sparas inställningarna mellan deployer? Kräver en monterad volym, inte bara en mapp."""
        return self._writable() and os.path.ismount(self.path.parent)

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
        self.version += 1
        if self._writable():
            # Skriv till en tillfällig fil och byt namn, så att filen aldrig blir halvskriven.
            fd, tmp = tempfile.mkstemp(dir=self.path.parent)
            with os.fdopen(fd, "w") as f:
                json.dump(self.values, f)
            os.replace(tmp, self.path)
        self.persisted = self._durable()
        return self.values

    def for_device(self) -> dict:
        return {key: self.values[key] for key in DEVICE_KEYS}

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
        self.commands: list[dict] = []   # väntar på att Pi:n ska hämta dem
        self.next_command_id = 1

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

    def add_command(self, cmd: dict) -> int:
        with self.cond:
            cmd = {**cmd, "id": self.next_command_id, "created": time.time()}
            self.next_command_id += 1
            self.commands.append(cmd)
            self.cond.notify_all()  # väck Pi:ns väntande anrop
            return cmd["id"]

    def take_commands(self) -> list[dict]:
        """Lämna ut väntande kommandon till Pi:n. Gamla kommandon kastas."""
        with self.cond:
            now = time.time()
            fresh = [c for c in self.commands if now - c["created"] <= COMMAND_MAX_AGE_S]
            self.commands = []
            return [{k: v for k, v in c.items() if k != "created"} for c in fresh]

    def wait_for_device(self, known_version: int, timeout: float) -> None:
        """Pi:ns väntande anrop: återvänd när någon tittar, ett kommando väntar
        eller inställningarna ändrats sedan Pi:n senast hämtade dem."""
        with self.cond:
            self.cond.wait_for(
                lambda: self.wanted or self.commands or self.settings.version != known_version,
                timeout=timeout,
            )

    def device_reply(self) -> dict:
        """Det som skickas till Pi:n i svaret på både väntande anrop och bilder."""
        return {
            "live": self.wanted,
            **(self.settings.for_pi() if self.wanted else {}),
            "config": self.settings.for_device(),
            "config_version": self.settings.version,
            "commands": self.take_commands(),
        }

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
