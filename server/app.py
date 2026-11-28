"""Webbdelen för Lennarts matstation.

Adresser:
  GET  /                 Statussidan med en valruta: Status eller Demo.
  GET  /status           Statussidan utan valruta, med livebild och status från Pi:n.
  GET  /demo             Demo av besöksliggaren med AI-genererade bilder.
  GET  /live.mjpg        Livebilden som bildström (startar när besökaren klickar).
  GET  /api/status       Senaste rapporten från Pi:n som JSON.
  GET  /api/live/info    Om livebilden är på, antal tittare med mera.
  GET  /admin            Adminvyn (kräver inloggning).
  GET  /admin/login      Inloggningssidan.
  POST /admin/login      Logga in.
  POST /admin/logout     Logga ut.
  GET  /api/admin/state  Inställningar och läge för adminvyn (kräver inloggning).
  GET  /api/admin/session  Om webbläsaren är inloggad, så att statussidan vet om testknapparna ska visas.
  POST /api/admin/settings  Ändra inställningar (kräver inloggning).
  POST /api/admin/servo  Skicka ett kommando till Pi:n: servona, en kort skärmbild eller omstart av skärmen (kräver inloggning).
  POST /api/heartbeat    Pi:n rapporterar att den lever (kräver enhetsnyckel).
  GET  /api/live/wait    Pi:n väntar på tittare, kommandon eller nya inställningar (kräver enhetsnyckel).
  POST /api/device/settings  Pi:n skickar sin kopia av inställningarna, om servern saknar egna (kräver enhetsnyckel).
  POST /api/live/frame   Pi:n skickar en bild till livebilden (kräver enhetsnyckel).
  GET  /static/...       Logotyp, typsnitt, stilmall och demobilder.
  GET  /healthz          För Coolifys hälsokontroll.

Bara Pythons standardbibliotek, så att varje rad går att förstå och inget
behöver installeras.

Miljövariabler (sätts i Coolify, aldrig i repot):
  LENNART_DEVICE_TOKEN  delad nyckel som Pi:n skickar med. Samma värde i Pi:ns .env.
  ADMIN_PASSWORD        lösenord till adminvyn. Saknas det är adminvyn avstängd.
  DATA_DIR              mapp där inställningarna sparas (standard /data, en volym i Coolify).
  PORT                  port att lyssna på (standard 8000).
  SOURCE_COMMIT         commit som Coolify byggde, om Coolify skickar med den.
"""

import hmac
import json
import os
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import re

import admin
from clips import LABELS, MAX_CLIP_BYTES, MAX_THUMB_BYTES, ClipStore
from live import (CAMERA_ROTATIONS, DISPLAY_MODES, LCD_SPI_MHZ, LIMITS, NO_FRAME_GIVE_UP_S, REC_RESOLUTIONS,
                  RESOLUTIONS, LiveRelay, Settings, validate_command)

PORT = int(os.environ.get("PORT", "8000"))
DEVICE_TOKEN = os.environ.get("LENNART_DEVICE_TOKEN", "")
SERVER_VERSION = os.environ.get("SOURCE_COMMIT", "")[:7] or "okänd"
DATA_DIR = os.environ.get("DATA_DIR", "/data")
MAX_BODY = 16 * 1024          # en heartbeat är några hundra byte
MAX_FRAME = 1_500_000         # en JPEG på 1280 × 720 är normalt långt mindre
STALE_AFTER_S = 120           # ingen kontakt på två minuter = Pi:n räknas som tyst
LIVE_WAIT_S = 50              # så länge Pi:ns väntande anrop hålls öppet
BOUNDARY = b"lennartbild"

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
    "camera_rotation": int,
    "display_mode": str,
    "display_info": str,
    "demo_info": str,
    "servo_ok": bool,
    "servo_info": str,
    "recording_ok": bool,
    "recording_info": str,
}
LONG_FIELDS = ("message", "servo_info", "recording_info", "display_info", "demo_info")

HERE = Path(__file__).parent
PAGES = {name: (HERE / f"{name}.html").read_text(encoding="utf-8") for name in ("index", "demo", "admin", "login", "clips")}

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
_history: deque = deque(maxlen=50)  # i minnet: nollställs vid omstart

settings = Settings(DATA_DIR)
relay = LiveRelay(settings)
clips = ClipStore(DATA_DIR)
CLIP_FILE = re.compile(r"^/api/admin/clips/([0-9a-f-]+)\.(mp4|jpg)$")
CLIP_ACTION = re.compile(r"^/api/admin/clips/([0-9a-f-]+)/(label|delete)$")
CLIP_UPLOAD = re.compile(r"^/api/clips/([0-9a-f-]+)(/thumb)?$")


def clean_report(raw: dict) -> dict:
    report = {}
    for key, kind in ALLOWED_FIELDS.items():
        value = raw.get(key)
        if isinstance(value, kind) and not (kind is not bool and isinstance(value, bool)):
            report[key] = value[:(200 if key in LONG_FIELDS else 80)] if isinstance(value, str) else value
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

    # ---------- hjälpfunktioner ----------

    def _send(self, status: int, body: bytes, content_type: str, cache: str = "no-store", headers=()) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        for name, value in headers:
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, data: dict) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def _html(self, page: str, status: int = 200, **values) -> None:
        html = PAGES[page]
        for key, value in values.items():
            html = html.replace("{{" + key + "}}", value)
        self._send(status, html.encode(), "text/html; charset=utf-8", "no-cache",
                   [("X-Frame-Options", "DENY"), ("Referrer-Policy", "same-origin")])

    def _redirect(self, location: str, cookie: str | None = None) -> None:
        headers = [("Location", location)]
        if cookie:
            headers.append(("Set-Cookie", cookie))
        self._send(303, b"", "text/plain; charset=utf-8", headers=headers)

    def _client_ip(self) -> str:
        # lennart.cam går via Cloudflare, som skickar besökarens adress i CF-Connecting-IP.
        # Utan den skulle alla besökare se ut att komma från Cloudflares adresser och dela
        # samma spärr efter felaktiga inloggningar.
        cloudflare = self.headers.get("CF-Connecting-IP", "").strip()
        if cloudflare:
            return cloudflare
        # Annars: bakom Coolifys proxy (Traefik) är sista adressen i X-Forwarded-For den som proxyn såg.
        forwarded = self.headers.get("X-Forwarded-For", "")
        return forwarded.split(",")[-1].strip() if forwarded else self.client_address[0]

    def _same_origin(self) -> bool:
        # Skydd mot att en annan webbplats skickar formulär hit (CSRF), utöver SameSite-kakan.
        origin = self.headers.get("Origin")
        return origin is None or urlparse(origin).netloc == self.headers.get("Host", "")

    def _admin_ok(self) -> bool:
        return admin.valid(admin.token_from_cookie(self.headers.get("Cookie")))

    def _device_ok(self) -> bool:
        if not DEVICE_TOKEN:
            self._json(503, {"fel": "Servern saknar LENNART_DEVICE_TOKEN"})
            return False
        sent = self.headers.get("Authorization", "")
        if not hmac.compare_digest(sent.encode(), f"Bearer {DEVICE_TOKEN}".encode()):
            self._json(401, {"fel": "Fel eller saknad enhetsnyckel"})
            return False
        return True

    def _read_body(self, limit: int) -> bytes | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if not 0 < length <= limit:
            self._json(413, {"fel": "Fel storlek på meddelandet"})
            return None
        return self.rfile.read(length)

    def _read_json(self, limit: int) -> dict | None:
        body = self._read_body(limit)
        if body is None:
            return None
        try:
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError
            return data
        except ValueError:
            self._json(400, {"fel": "Ogiltig JSON"})
            return None

    # ---------- GET ----------

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in ("/", "/status"):
            self._html("index")
        elif path == "/demo":
            self._html("demo")
        elif path in STATIC_FILES:
            body, content_type = STATIC_FILES[path]
            # En timme i webbläsarens cache räcker, och ändringar syns snart efter en deploy.
            self._send(200, body, content_type, "public, max-age=3600")
        elif path == "/api/status":
            self._json(200, status_payload())
        elif path == "/api/live/info":
            self._json(200, relay.info())
        elif path == "/live.mjpg":
            self._stream_live()
        elif path == "/api/live/wait":
            if self._device_ok():
                query = parse_qs(urlparse(self.path).query)
                try:
                    known = int(query.get("v", ["0"])[0])
                except ValueError:
                    known = 0
                relay.wait_for_device(known, timeout=LIVE_WAIT_S)
                self._json(200, relay.device_reply())
        elif path == "/admin":
            if not admin.enabled():
                self._html("login", 503, fel="Adminvyn är inte påslagen. Sätt ADMIN_PASSWORD i Coolify.")
            elif self._admin_ok():
                self._html("admin")
            else:
                self._redirect("/admin/login")
        elif path == "/admin/login":
            self._html("login", fel="")
        elif path == "/api/admin/session":
            self._json(200, {"admin": self._admin_ok()})
        elif path == "/api/admin/state":
            if not self._admin_ok():
                self._json(401, {"fel": "Inte inloggad"})
                return
            self._json(200, {
                "settings": settings.values,
                "persisted": settings.persisted,
                "resolutions": list(RESOLUTIONS),
                "rec_resolutions": list(REC_RESOLUTIONS),
                "rotations": list(CAMERA_ROTATIONS),
                "display_modes": list(DISPLAY_MODES),
                "lcd_spi_mhz": list(LCD_SPI_MHZ),
                "limits": LIMITS,
                "live": relay.info(),
                "status": status_payload(),
                "clips": clips.summary(),
            })
        elif path == "/admin/klipp":
            if self._admin_ok():
                self._html("clips")
            else:
                self._redirect("/admin/login")
        elif path == "/api/admin/clips":
            if self._admin_ok():
                self._json(200, {"clips": clips.list(), "labels": LABELS, "bytes": clips.total_bytes(),
                                 "max_bytes": settings.values["clips_max_gb"] * 1024 ** 3})
            else:
                self._json(401, {"fel": "Inte inloggad"})
        elif path == "/api/admin/clips.csv":
            if self._admin_ok():
                self._send(200, clips.csv(), "text/csv; charset=utf-8", "private, no-store",
                           [("Content-Disposition", 'attachment; filename="lennart-klipp.csv"')])
            else:
                self._json(401, {"fel": "Inte inloggad"})
        elif CLIP_FILE.match(path):
            if self._admin_ok():
                clip_id, kind = CLIP_FILE.match(path).groups()
                self._send_clip_file(clip_id, kind)
            else:
                self._json(401, {"fel": "Inte inloggad"})
        elif path == "/healthz":
            self._send(200, b"ok", "text/plain; charset=utf-8")
        else:
            self._json(404, {"fel": "Finns inte"})

    def _send_clip_file(self, clip_id: str, kind: str) -> None:
        """Skicka en video eller miniatyrbild. Videon skickas i delar (Range), så att
        webbläsaren kan spola och så att Safari över huvud taget spelar upp den."""
        if not clips.valid_id(clip_id):
            self._json(404, {"fel": "Finns inte"})
            return
        file = clips.path(clip_id, "." + kind)
        try:
            size = file.stat().st_size
        except OSError:
            self._json(404, {"fel": "Finns inte"})
            return
        content_type = "video/mp4" if kind == "mp4" else "image/jpeg"
        start, end, status = 0, size - 1, 200
        wanted = re.match(r"^bytes=(\d*)-(\d*)$", self.headers.get("Range", "").strip())
        if wanted and size > 0 and (wanted.group(1) or wanted.group(2)):
            first, last = wanted.groups()
            if first:
                start = int(first)
                end = min(int(last), size - 1) if last else size - 1
            else:  # "bytes=-500" betyder de sista 500 byten
                start = max(size - int(last), 0)
            if start > end or start >= size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            status = 206
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "private, max-age=3600")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Robots-Tag", "noindex")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        try:
            with open(file, "rb") as f:
                f.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    chunk = f.read(min(256 * 1024, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # webbläsaren avbröt, till exempel när man spolar

    def _stream_live(self) -> None:
        """Skicka livebilden som en ström av JPEG-bilder (multipart/x-mixed-replace).

        Webbläsaren visar strömmen i en vanlig <img>. Strömmen slutar efter
        max_view_min minuter, när admin stänger av livebilden, eller när Pi:n
        slutar skicka bilder.
        """
        if not settings.values["live_enabled"]:
            self._json(503, {"fel": "Livebilden är avstängd"})
            return
        if not relay.add_viewer():
            self._json(503, {"fel": "Många tittar just nu. Försök igen om en stund."})
            return
        try:
            self.send_response(200)
            self.send_header("Content-Type", f"multipart/x-mixed-replace; boundary={BOUNDARY.decode()}")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Accel-Buffering", "no")
            self.send_header("Connection", "close")
            self.end_headers()
            deadline = time.monotonic() + settings.values["max_view_min"] * 60
            last_id, last_frame_at = relay.frame_id, time.monotonic()  # vänta på en färsk bild
            while time.monotonic() < deadline:
                got = relay.wait_frame(last_id, timeout=5)
                if got is None:
                    if not settings.values["live_enabled"]:
                        break
                    if time.monotonic() - last_frame_at > NO_FRAME_GIVE_UP_S:
                        break
                    continue
                last_id, jpeg = got
                last_frame_at = time.monotonic()
                self.wfile.write(b"--" + BOUNDARY + b"\r\nContent-Type: image/jpeg\r\nContent-Length: "
                                 + str(len(jpeg)).encode() + b"\r\n\r\n" + jpeg + b"\r\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass  # besökaren stängde fliken
        finally:
            relay.remove_viewer()

    # ---------- POST ----------

    def do_POST(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/api/heartbeat":
            if not self._device_ok():
                return
            raw = self._read_json(MAX_BODY)
            if raw is None:
                return
            with _lock:
                _history.append({"received_at": time.time(), "report": clean_report(raw)})
            self._json(200, {"ok": True})
        elif path == "/api/device/settings":
            if self._device_ok():
                raw = self._read_json(64 * 1024)
                if raw is None:
                    return
                adopted = settings.adopt(raw)
                if adopted:
                    relay.notify()
                    print("Inställningarna återställdes från stationens kopia", flush=True)
                self._json(200, {"adopted": adopted})
        elif path == "/api/live/frame":
            if not self._device_ok():
                return
            if self.headers.get("Content-Type") != "image/jpeg":
                self._json(415, {"fel": "Bara image/jpeg"})
                return
            jpeg = self._read_body(MAX_FRAME)
            if jpeg is None:
                return
            if not jpeg.startswith(b"\xff\xd8"):
                self._json(400, {"fel": "Inte en JPEG-bild"})
                return
            relay.put_frame(jpeg)
            self._json(200, {"continue": relay.wanted, **relay.device_reply()})
        elif CLIP_UPLOAD.match(path):
            if self._device_ok():
                clip_id, thumb = CLIP_UPLOAD.match(path).groups()
                self._receive_clip(clip_id, bool(thumb))
        elif CLIP_ACTION.match(path):
            if not self._admin_ok():
                self._json(401, {"fel": "Inte inloggad"})
                return
            if not self._same_origin():
                self._json(403, {"fel": "Fel ursprung"})
                return
            clip_id, action = CLIP_ACTION.match(path).groups()
            if not clips.valid_id(clip_id) or not clips.path(clip_id, ".json").exists():
                self._json(404, {"fel": "Klippet finns inte"})
                return
            if action == "delete":
                clips.delete(clip_id)
                print(f"Admin raderade klipp {clip_id}", flush=True)
                self._json(200, {"ok": True})
                return
            raw = self._read_json(512)
            if raw is None:
                return
            try:
                self._json(200, clips.set_label(clip_id, raw.get("label")))
            except ValueError as e:
                self._json(400, {"fel": str(e)})
        elif path == "/admin/login":
            self._login()
        elif path == "/admin/logout":
            if not self._same_origin():
                self._json(403, {"fel": "Fel ursprung"})
                return
            admin.end_session(admin.token_from_cookie(self.headers.get("Cookie")))
            self._redirect("/status", admin.cookie_header("", max_age=0))
        elif path == "/api/admin/settings":
            if not self._admin_ok():
                self._json(401, {"fel": "Inte inloggad"})
                return
            if not self._same_origin():
                self._json(403, {"fel": "Fel ursprung"})
                return
            changes = self._read_json(4096)
            if changes is None:
                return
            try:
                settings.update(changes)
            except ValueError as e:
                self._json(400, {"fel": str(e)})
                return
            relay.notify()  # väck strömmar och Pi:ns väntande anrop, så att ändringen gäller direkt
            print(f"Admin ändrade inställningar: {changes}", flush=True)
            self._json(200, {"settings": settings.values, "persisted": settings.persisted})
        elif path == "/api/admin/servo":
            if not self._admin_ok():
                self._json(401, {"fel": "Inte inloggad"})
                return
            if not self._same_origin():
                self._json(403, {"fel": "Fel ursprung"})
                return
            raw = self._read_json(1024)
            if raw is None:
                return
            try:
                cmd = validate_command(raw, settings.values)
            except ValueError as e:
                self._json(400, {"fel": str(e)})
                return
            command_id = relay.add_command(cmd)
            print(f"Admin skickade kommando {command_id}: {cmd}", flush=True)
            reply = {"ok": True, "id": command_id}
            if not status_payload()["online"]:
                reply["varning"] = "Stationen hörs inte av. Kommandot kastas om det inte hämtas inom 20 sekunder."
            self._json(200, reply)
        else:
            self._json(404, {"fel": "Finns inte"})

    def _receive_clip(self, clip_id: str, thumb: bool) -> None:
        if not clips.valid_id(clip_id):
            self._json(400, {"fel": "Ogiltigt id"})
            return
        if thumb:
            if self.headers.get("Content-Type") != "image/jpeg":
                self._json(415, {"fel": "Bara image/jpeg"})
                return
            jpeg = self._read_body(MAX_THUMB_BYTES)
            if jpeg is None:
                return
            try:
                clips.save_thumb(clip_id, jpeg)
            except KeyError:
                self._json(404, {"fel": "Klippet finns inte"})
                return
            self._json(200, {"ok": True})
            return
        if self.headers.get("Content-Type") != "video/mp4":
            self._json(415, {"fel": "Bara video/mp4"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            meta = json.loads(self.headers.get("X-Clip-Meta", "{}"))
            if not isinstance(meta, dict):
                raise ValueError
        except ValueError:
            self._json(400, {"fel": "Ogiltig Content-Length eller X-Clip-Meta"})
            return
        if not 0 < length <= MAX_CLIP_BYTES:
            self._json(413, {"fel": "Klippet är för stort"})
            return
        if clips.total_bytes() + length > settings.values["clips_max_gb"] * 1024 ** 3:
            # Pi:n behåller klippet och försöker igen senare, när admin har rensat eller höjt gränsen.
            self.close_connection = True
            self._json(507, {"fel": "Klipputrymmet på servern är fullt"})
            return
        try:
            clips.save(clip_id, meta, self.rfile, length)
        except (ValueError, OSError) as e:
            self.close_connection = True
            self._json(400, {"fel": f"Klippet kunde inte sparas: {e}"})
            return
        print(f"Tog emot klipp {clip_id} ({length // 1024} kB)", flush=True)
        self._json(200, {"ok": True, "id": clip_id})

    def _login(self) -> None:
        if not admin.enabled():
            self._html("login", 503, fel="Adminvyn är inte påslagen. Sätt ADMIN_PASSWORD i Coolify.")
            return
        if not self._same_origin():
            self._html("login", 403, fel="Inloggningen måste ske från lennart.cam.")
            return
        ip = self._client_ip()
        if admin.locked_out(ip):
            self._html("login", 429, fel="För många felaktiga försök. Vänta en kvart och försök igen.")
            return
        body = self._read_body(2048)
        if body is None:
            return
        password = parse_qs(body.decode("utf-8", "replace")).get("password", [""])[0]
        if admin.check_password(ip, password):
            print(f"Admin loggade in från {ip}", flush=True)
            self._redirect("/admin", admin.cookie_header(admin.new_session()))
        else:
            tried = password.strip()
            print(f"Felaktigt adminlösenord från {ip}: {len(tried)} tecken, "
                  f"fingeravtryck {admin.fingerprint(tried)}", flush=True)
            self._html("login", 401, fel="Fel lösenord.")

    def log_message(self, fmt: str, *args) -> None:
        # Logga inte det som sker hela tiden: hälsokontroller och livebilder.
        line = str(args[0]) if args else ""
        if not any(p in line for p in ("/healthz", "/api/live/frame", "/api/live/wait", "/api/clips/")):
            super().log_message(fmt, *args)


def main() -> None:
    if not DEVICE_TOKEN:
        print("Varning: LENNART_DEVICE_TOKEN saknas – Pi:n kommer att nekas.", flush=True)
    if not admin.enabled():
        print("Obs: ADMIN_PASSWORD saknas – adminvyn är avstängd.", flush=True)
    else:
        # Bara längden, aldrig lösenordet, så att det går att jämföra med det man skriver in.
        print(f"Adminvyn är på. Lösenordet har {len(admin.ADMIN_PASSWORD)} tecken, "
              f"fingeravtryck {admin.fingerprint(admin.ADMIN_PASSWORD)}.", flush=True)
    if not settings.persisted:
        print(f"Obs: {DATA_DIR} är ingen volym – inställningar försvinner vid nästa deploy.", flush=True)
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    httpd.daemon_threads = True  # öppna livebilder ska inte hindra omstart
    print(f"Lennart-servern lyssnar på port {PORT} (version {SERVER_VERSION})", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
