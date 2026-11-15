"""Förbindelsen med lennart.cam: livebild, inställningar och kommandon.

Livebilden skickas bara när någon tittar.

Pi:n håller ett anrop öppet mot /api/live/wait. Servern svarar så fort en
besökare öppnar livebilden, och då skickar Pi:n JPEG-bilder till
/api/live/frame tills servern säger att ingen tittar längre.

Samma väntande anrop ger också nya inställningar (t.ex. kamerans rotation) och
kommandon (t.ex. "flytta servot") direkt när de ändras i adminvyn.

Anslutningen till servern återanvänds mellan bilderna (keep-alive), så att
varje bild inte kostar en ny krypterad uppkoppling. Det sparar data över 4G.
"""

import http.client
import io
import json
import os
import threading
import time
from urllib.parse import urlparse

from PIL import Image


class LiveSender:
    def __init__(self, get_frame, on_config, on_commands) -> None:
        url = urlparse(os.environ.get("LENNART_SERVER_URL", ""))
        self.secure = url.scheme == "https"
        self.host = url.netloc
        self.token = os.environ.get("LENNART_DEVICE_TOKEN", "")
        self.get_frame = get_frame       # ger senaste kamerabilden (RGB, numpy) eller None
        self.on_config = on_config       # anropas med nya inställningar från adminvyn
        self.on_commands = on_commands   # anropas med kommandon från adminvyn
        self.config_version = 0          # vilken version av inställningarna Pi:n har
        self.active = False              # True medan någon tittar
        self.fps = 2.0
        self._conn = None
        self._stop = threading.Event()

    @property
    def enabled(self) -> bool:
        return bool(self.host and self.token)

    def _connection(self, timeout: float) -> http.client.HTTPConnection:
        if self._conn is None:
            cls = http.client.HTTPSConnection if self.secure else http.client.HTTPConnection
            self._conn = cls(self.host, timeout=timeout)
        self._conn.timeout = timeout
        if self._conn.sock is not None:
            self._conn.sock.settimeout(timeout)
        return self._conn

    def _request(self, method: str, path: str, body: bytes | None, content_type: str, timeout: float) -> dict:
        headers = {"Authorization": f"Bearer {self.token}", "User-Agent": "lennart-pi"}
        if body is not None:
            headers["Content-Type"] = content_type
        try:
            conn = self._connection(timeout)
            conn.request(method, path, body=body, headers=headers)
            resp = conn.getresponse()
            data = resp.read()
        except (OSError, http.client.HTTPException):
            if self._conn is not None:
                self._conn.close()
            self._conn = None
            raise
        if resp.status != 200:
            raise RuntimeError(f"servern svarade {resp.status}: {data[:120]!r}")
        return json.loads(data)

    def _handle(self, reply: dict) -> None:
        """Ta hand om inställningar och kommandon som kom med ett svar från servern."""
        if "config" in reply and reply.get("config_version") != self.config_version:
            self.config_version = reply.get("config_version", 0)
            self.on_config(reply["config"])
        if reply.get("commands"):
            self.on_commands(reply["commands"])

    @staticmethod
    def encode(rgb, width: int, height: int, quality: int) -> bytes:
        img = Image.fromarray(rgb)
        if img.height > img.width and width > height:
            width, height = height, width  # bilden är vriden 90°, så livebilden blir stående
        if img.size != (width, height):
            img = img.resize((width, height), Image.BILINEAR)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=quality)
        return buf.getvalue()

    def _stream(self, cfg: dict) -> None:
        """Skicka bilder tills servern säger att ingen tittar längre."""
        self.active = True
        print(f"Livebild: någon tittar, skickar {cfg['width']}×{cfg['height']} i {cfg['fps']} bilder/s", flush=True)
        sent = 0
        try:
            while not self._stop.is_set():
                started = time.monotonic()
                self.fps = float(cfg["fps"])
                rgb = self.get_frame()
                if rgb is None:
                    time.sleep(0.5)  # kameran har inte levererat någon bild än
                    continue
                jpeg = self.encode(rgb, cfg["width"], cfg["height"], cfg["quality"])
                reply = self._request("POST", "/api/live/frame", jpeg, "image/jpeg", timeout=10)
                self._handle(reply)
                sent += 1
                if not reply.get("continue"):
                    break
                cfg = reply  # admin kan ha ändrat upplösning eller bilder per sekund
                spare = 1 / self.fps - (time.monotonic() - started)
                if spare > 0:
                    time.sleep(spare)
        finally:
            self.active = False
            print(f"Livebild: ingen tittar längre ({sent} bilder skickade)", flush=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                reply = self._request("GET", f"/api/live/wait?v={self.config_version}", None, "", timeout=70)
                self._handle(reply)
                if reply.get("live"):
                    self._stream(reply)
            except Exception as e:
                print(f"Livebild: {type(e).__name__}: {e}", flush=True)
                self._stop.wait(10)  # vänta lite innan nästa försök, t.ex. om nätet är borta

    def start(self) -> None:
        if not self.enabled:
            print("Livebild avstängd: LENNART_SERVER_URL eller LENNART_DEVICE_TOKEN saknas i .env", flush=True)
            return
        threading.Thread(target=self._run, name="live", daemon=True).start()

    def stop(self) -> None:
        self._stop.set()
