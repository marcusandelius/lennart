"""Skickar en livstecken-rapport ("heartbeat") till webbdelen på lennart.cam.

Pi:n tar bara kontakt utåt, så det fungerar likadant på wifi och 4G.
Rapporten innehåller inga bilder, bara status. Enhetsnyckeln skickas så att
servern vet att rapporten kommer från just den här Pi:n.
"""

import json
import os
import socket
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

INTERVAL_S = 30


def cpu_temp_c() -> float | None:
    try:
        return int(Path("/sys/class/thermal/thermal_zone0/temp").read_text()) / 1000
    except (OSError, ValueError):
        return None


def uptime_s() -> float | None:
    try:
        return float(Path("/proc/uptime").read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


def default_interface() -> str:
    """Vilket nätverkskort som används för internet, t.ex. wlan0 (wifi) eller ett 4G-modem."""
    try:
        for line in Path("/proc/net/route").read_text().splitlines()[1:]:
            fields = line.split()
            if len(fields) > 1 and fields[1] == "00000000":
                return fields[0]
    except OSError:
        pass
    return "okänd"


def read_version() -> str:
    path = Path(__file__).parent / "VERSION"
    try:
        return path.read_text().strip()[:7] or "okänd"
    except OSError:
        return "okänd"


class Heartbeat:
    def __init__(self, status_fn) -> None:
        self.url = os.environ.get("LENNART_SERVER_URL", "").rstrip("/")
        self.token = os.environ.get("LENNART_DEVICE_TOKEN", "")
        self.status_fn = status_fn          # funktion som ger kamera- och displaystatus
        self.version = read_version()
        self.last_ok: bool | None = None    # None = inte försökt än
        self._stop = threading.Event()

    @property
    def enabled(self) -> bool:
        return bool(self.url and self.token)

    def report(self) -> dict:
        data = {
            "host": socket.gethostname(),
            "version": self.version,
            "uptime_s": uptime_s(),
            "cpu_temp_c": cpu_temp_c(),
            "network": default_interface(),
        }
        data.update(self.status_fn())
        return {k: v for k, v in data.items() if v is not None}

    def send_once(self) -> bool:
        body = json.dumps(self.report()).encode()
        req = urllib.request.Request(
            f"{self.url}/api/heartbeat",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "lennart-pi",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                ok = resp.status == 200
        except urllib.error.HTTPError as e:
            print(f"Heartbeat nekades av servern: {e.code}", flush=True)
            ok = False
        except (urllib.error.URLError, OSError) as e:
            print(f"Heartbeat nådde inte servern: {e}", flush=True)
            ok = False
        if ok and self.last_ok is not True:
            print("Heartbeat: kontakt med servern", flush=True)
        self.last_ok = ok
        return ok

    def _run(self) -> None:
        while not self._stop.is_set():
            self.send_once()
            self._stop.wait(INTERVAL_S)

    def start(self) -> None:
        if not self.enabled:
            print("Heartbeat avstängd: LENNART_SERVER_URL eller LENNART_DEVICE_TOKEN saknas i .env", flush=True)
            return
        threading.Thread(target=self._run, name="heartbeat", daemon=True).start()

    def stop(self) -> None:
        self._stop.set()


if __name__ == "__main__":
    # Testa från kommandoraden: skickar en rapport och skriver ut svaret.
    hb = Heartbeat(lambda: {"message": "test från kommandoraden"})
    if not hb.enabled:
        raise SystemExit("Sätt LENNART_SERVER_URL och LENNART_DEVICE_TOKEN först.")
    print(json.dumps(hb.report(), ensure_ascii=False))
    raise SystemExit(0 if hb.send_once() else 1)
