"""Stationens kopia av alla inställningar från adminvyn.

Varför: inställningarna sparas på servern. Om servern startar om utan sina sparade
inställningar, till exempel efter en deploy utan volym, skulle allt som kalibrerats i
adminvyn (servotider, lägen och kontrast) försvinna. Stationen sparar därför en kopia
varje gång inställningarna ändras, och skickar den till servern när servern ber om den.
Kopian används också direkt när stationen startar, innan servern har svarat.

Filen ligger utanför appens mapp (~/lennart-app), eftersom deployen skriver över den mappen.
"""

import json
import os
import tempfile
from pathlib import Path

STATE_DIR = Path(os.environ.get("LENNART_STATE_DIR", str(Path.home() / ".local" / "state" / "lennart")))
PATH = STATE_DIR / "settings.json"

_last: dict | None = None


def load() -> dict | None:
    try:
        data = json.loads(PATH.read_text())
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def save(values: dict) -> None:
    """Spara kopian om den har ändrats. Skrivs till en tillfällig fil som sedan byter namn,
    så att filen aldrig blir halvskriven om strömmen går."""
    global _last
    if not isinstance(values, dict) or values == _last:
        return
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=STATE_DIR)
        with os.fdopen(fd, "w") as f:
            json.dump(values, f)
        os.replace(tmp, PATH)
        _last = dict(values)
    except OSError as e:
        print(f"Kopian av inställningarna kunde inte sparas: {e}", flush=True)
