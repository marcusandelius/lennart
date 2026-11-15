"""Webbdelen för Lennarts matstation – första testversion.

Gör det här:
  POST /api/heartbeat  Pi:n rapporterar att den lever (kräver enhetsnyckel).
  GET  /api/status     Senaste rapporten som JSON.
  GET  /               Statussidan med en valruta: Status eller Demo.
  GET  /status         Statussidan utan valruta: visar om Pi:n hörs av.
  GET  /demo           Demo av besöksliggaren med AI-genererade bilder.
  GET  /static/...     Logotyp, typsnitt, stilmall och demobilder.
  GET  /healthz        För Coolifys hälsokontroll.

Bara Pythons standardbibliotek, så att varje rad går att förstå och inget
behöver installeras. Ersätts av en riktig app när bildigenkänningen är beslutad.

Miljövariabler (sätts i Coolify, aldrig i repot):
  LENNART_DEVICE_TOKEN  delad nyckel som Pi:n skickar med. Samma värde i Pi:ns .env.
  PORT                  port att lyssna på (standard 8000).
  SOURCE_COMMIT         commit som Coolify byggde, om Coolify skickar med den.
"""

import hmac
import json
import os
import threading
import time
from collections import deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("PORT", "8000"))
DEVICE_TOKEN = os.environ.get("LENNART_DEVICE_TOKEN", "")
SERVER_VERSION = os.environ.get("SOURCE_COMMIT", "")[:7] or "okänd"
MAX_BODY = 16 * 1024  # en heartbeat är några hundra byte
STALE_AFTER_S = 120   # ingen kontakt på två minuter = Pi:n räknas som tyst

# Fält som Pi:n får rapportera. Allt annat ignoreras, så att inget oväntat visas publikt.
ALLOWED_FIELDS = {
    "host": str,
    "version": str,
    "uptime_s": (int, float),
    "cpu_temp_c": (int, float),
    "network": str,
    "camera_ok": bool,
    "display_ok": bool,
    "fps": (int, float),
    "message": str,
    "throttled": str,
}

HERE = Path(__file__).parent
INDEX_HTML = (HERE / "index.html").read_bytes()
DEMO_HTML = (HERE / "demo.html").read_bytes()

# Statiska filer läses in en gång vid start. Bara filer som finns här kan hämtas,
# så en adress som /static/../app.py ger 404 i stället för att läsa utanför mappen.
CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".jpg": "image/jpeg",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
    ".txt": "text/plain; charset=utf-8",
}
STATIC_DIR = HERE / "static"
STATIC_FILES = {
    "/static/" + f.relative_to(STATIC_DIR).as_posix(): (f.read_bytes(), CONTENT_TYPES[f.suffix])
    for f in sorted(STATIC_DIR.rglob("*"))
    if f.is_file() and f.suffix in CONTENT_TYPES
}

_lock = threading.Lock()
_history: deque = deque(maxlen=50)  # i minnet: nollställs vid omstart, räcker för test


def clean_report(raw: dict) -> dict:
    report = {}
    for key, kind in ALLOWED_FIELDS.items():
        value = raw.get(key)
        if isinstance(value, kind) and not (kind is not bool and isinstance(value, bool)):
            report[key] = value[:(200 if key == "message" else 80)] if isinstance(value, str) else value
    return report


def status_payload() -> dict:
    with _lock:
        latest = _history[-1] if _history else None
        count = len(_history)
    now = time.time()
    if latest is None:
        return {"online": False, "seen_ago_s": None, "report": None,
                "server_version": SERVER_VERSION, "heartbeats": 0}
    ago = now - latest["received_at"]
    return {
        "online": ago < STALE_AFTER_S,
        "seen_ago_s": round(ago),
        "report": latest["report"],
        "server_version": SERVER_VERSION,
        "heartbeats": count,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "lennart"
    sys_version = ""

    def _send(self, status: int, body: bytes, content_type: str, cache: str = "no-store") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, data: dict) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in ("/", "/status"):
            self._send(200, INDEX_HTML, "text/html; charset=utf-8", "no-cache")
        elif path == "/demo":
            self._send(200, DEMO_HTML, "text/html; charset=utf-8", "no-cache")
        elif path in STATIC_FILES:
            body, content_type = STATIC_FILES[path]
            # En timme i webbläsarens cache räcker, och ändringar syns snart efter en deploy.
            self._send(200, body, content_type, "public, max-age=3600")
        elif path == "/api/status":
            self._json(200, status_payload())
        elif path == "/healthz":
            self._send(200, b"ok", "text/plain; charset=utf-8")
        else:
            self._json(404, {"fel": "Finns inte"})

    def do_POST(self) -> None:
        if self.path != "/api/heartbeat":
            self._json(404, {"fel": "Finns inte"})
            return
        if not DEVICE_TOKEN:
            self._json(503, {"fel": "Servern saknar LENNART_DEVICE_TOKEN"})
            return
        sent = self.headers.get("Authorization", "")
        if not hmac.compare_digest(sent.encode(), f"Bearer {DEVICE_TOKEN}".encode()):
            self._json(401, {"fel": "Fel eller saknad enhetsnyckel"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if not 0 < length <= MAX_BODY:
            self._json(413, {"fel": "Fel storlek på meddelandet"})
            return
        try:
            raw = json.loads(self.rfile.read(length))
            if not isinstance(raw, dict):
                raise ValueError
        except ValueError:
            self._json(400, {"fel": "Ogiltig JSON"})
            return
        with _lock:
            _history.append({"received_at": time.time(), "report": clean_report(raw)})
        self._json(200, {"ok": True})

    def log_message(self, fmt: str, *args) -> None:
        # Logga inte hälsokontrollerna, de kommer hela tiden.
        if not args or "/healthz" not in str(args[0]):
            super().log_message(fmt, *args)


def main() -> None:
    if not DEVICE_TOKEN:
        print("Varning: LENNART_DEVICE_TOKEN saknas – heartbeat från Pi:n kommer att nekas.", flush=True)
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Lennart-servern lyssnar på port {PORT} (version {SERVER_VERSION})", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
