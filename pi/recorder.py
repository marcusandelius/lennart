"""Inspelning av klipp när något rör sig framför kameran.

Klippen är underlag för att testa och träna bildigenkänningen. Så här fungerar det:

1. **Rörelse:** varje kamerabild krymps till ungefär 80 × 45 bildpunkter i gråskala
   och jämförs med en långsamt uppdaterad bakgrundsbild. Om tillräckligt stor del av
   bilden har ändrats (rörelsegränsen i promille, ställs in i adminvyn) startar ett klipp.
   Ljusförändringar som gäller hela bilden, till exempel när ett moln drar förbi,
   räknas bort genom att medianen av skillnaden dras ifrån.
2. **Inspelning:** bilderna skickas till ffmpeg, som gör en MP4-fil (H.264). De senaste
   sekunderna före rörelsen sparas hela tiden i minnet och kommer med i början av
   klippet, så att man ser djuret komma. Klippet slutar när det varit stilla en stund
   eller när det nått längsta tillåtna längd.
3. **Uppladdning:** klippen sparas först på Pi:n (~/lennart-data/clips) och laddas
   sedan upp till lennart.cam i en egen tråd. Går uppkopplingen ner ligger de kvar
   och laddas upp senare.

Ingen inspelning sker när det är för mörkt, eftersom kameran inte ser något då.
"""

import collections
import http.client
import json
import os
import queue
import secrets
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
from PIL import Image

CLIP_DIR = Path(os.environ.get("LENNART_CLIP_DIR", str(Path.home() / "lennart-data" / "clips")))
LOCAL_MAX_BYTES = float(os.environ.get("LENNART_CLIP_LOCAL_GB", "5")) * 1024 ** 3
MIN_FREE_BYTES = 1024 ** 3        # lämna minst 1 GB ledigt på minneskortet
PIXEL_CHANGE = 25                 # så mycket (av 255) en bildpunkt ska ändras för att räknas som rörelse
WARMUP_S = 3                      # lär in bakgrunden innan något får starta ett klipp
SMALL_STEP = 16                   # 1280 × 720 → 80 × 45 för rörelsedetekteringen

DEFAULTS = {"recording_enabled": False, "rec_resolution": "1280x720", "rec_fps": 15,
            "motion_sensitivity": 10, "pre_roll_s": 2, "post_roll_s": 5, "max_clip_s": 60,
            "min_brightness": 15}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Clip:
    """Ett klipp som håller på att spelas in. ffmpeg körs i en egen process och matas från en egen tråd."""

    def __init__(self, first_t: float, shape: tuple, fps: int) -> None:
        started = utc_now()
        self.id = started.strftime("%Y%m%d-%H%M%S-") + secrets.token_hex(2)
        self.started = started.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.t0 = first_t
        self.shape = shape
        self.fps = fps
        self.written = 0          # antal bilder som skickats till ffmpeg, inklusive dubbletter
        self.dropped = 0
        self.last_motion_t = first_t
        self.peak_motion = 0.0
        self.peak_frame = None
        self.brightness = None
        self.queue: queue.Queue = queue.Queue(maxsize=fps * 4)
        self.part = CLIP_DIR / f"{self.id}.mp4.part"
        h, w = shape[:2]
        self.process = subprocess.Popen(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
             "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
             "-g", str(fps * 2), "-threads", "2", "-movflags", "+faststart", "-f", "mp4", str(self.part)],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.thread = threading.Thread(target=self._write, daemon=True)
        self.thread.start()

    def add(self, t: float, frame: np.ndarray) -> None:
        """Lägg till en bild i rätt takt.

        Kameraloopen går inte exakt i inspelningens takt. För att klippet ska spelas upp
        i verklig hastighet räknas ut hur många bilder som borde finnas vid tiden t.
        Kommer bilderna för tätt hoppas en över, kommer de för glest upprepas den senaste.
        """
        due = int((t - self.t0) * self.fps) + 1
        repeat = min(due - self.written, self.fps)   # aldrig mer än en sekunds upprepning
        if repeat <= 0:
            return
        self.written += repeat
        try:
            self.queue.put_nowait((frame, repeat))
        except queue.Full:
            self.dropped += repeat  # ffmpeg hinner inte med; hellre tappa bilder än fastna

    @property
    def duration_s(self) -> float:
        return self.written / self.fps

    def _write(self) -> None:
        stdin = self.process.stdin
        while True:
            item = self.queue.get()
            if item is None:
                break
            frame, repeat = item
            data = frame.tobytes()
            try:
                for _ in range(repeat):
                    stdin.write(data)
            except (BrokenPipeError, OSError):
                break
        try:
            stdin.close()
        except OSError:
            pass

    def finish(self, on_done) -> None:
        """Avsluta klippet i bakgrunden: vänta in ffmpeg, spara miniatyrbild och uppgifter."""
        self.queue.put(None)

        def finalize() -> None:
            self.thread.join()
            err = self.process.stderr.read().decode("utf-8", "replace").strip()
            code = self.process.wait()
            if code != 0 or not self.part.exists():
                self.part.unlink(missing_ok=True)
                on_done(self, f"ffmpeg avslutades med kod {code}: {err[-150:]}")
                return
            self.part.rename(CLIP_DIR / f"{self.id}.mp4")
            if self.peak_frame is not None:
                img = Image.fromarray(self.peak_frame)
                img.thumbnail((480, 480))
                img.save(CLIP_DIR / f"{self.id}.jpg", quality=80)
            h, w = self.shape[:2]
            meta = {"started": self.started, "duration_s": round(self.duration_s, 1), "frames": self.written,
                    "fps": self.fps, "width": w, "height": h, "peak_motion": round(self.peak_motion, 1),
                    "brightness": self.brightness, "dropped": self.dropped}
            # Uppgiftsfilen skrivs sist. Finns den är klippet färdigt och kan laddas upp.
            tmp = CLIP_DIR / f"{self.id}.json.tmp"
            tmp.write_text(json.dumps(meta))
            tmp.rename(CLIP_DIR / f"{self.id}.json")
            on_done(self, None)

        threading.Thread(target=finalize, daemon=True).start()


class Recorder:
    def __init__(self) -> None:
        self.config = dict(DEFAULTS)
        self.ffmpeg = shutil.which("ffmpeg")
        self.background = None
        self.warm_until = 0.0
        self.pre_roll: collections.deque = collections.deque()
        self.clip: Clip | None = None
        self.motion = 0.0           # senaste rörelsevärdet i promille
        self.brightness = None      # senaste ljusstyrkan, 0–100
        self.moving_frames = 0
        self.clips_done = 0
        self.last_error = ""
        self.lock = threading.Lock()
        try:
            CLIP_DIR.mkdir(parents=True, exist_ok=True)
            for leftover in CLIP_DIR.glob("*.part"):   # klipp som avbröts av en omstart
                leftover.unlink()
        except OSError as e:
            self.last_error = f"Kan inte skapa {CLIP_DIR}: {e}"

    # ---------- inställningar och status ----------

    def configure(self, config: dict) -> None:
        with self.lock:
            was_on = self.config["recording_enabled"]
            self.config.update({k: v for k, v in config.items() if k in DEFAULTS})
            if self.config["recording_enabled"] and not was_on:
                self.background = None   # börja om med bakgrunden när inspelningen slås på

    @property
    def enabled(self) -> bool:
        return bool(self.config["recording_enabled"]) and self.ffmpeg is not None

    @property
    def fps(self) -> int:
        return int(self.config["rec_fps"])

    @property
    def ok(self) -> bool:
        return self.ffmpeg is not None and not self.last_error

    def info(self, pending_uploads: int) -> str:
        if self.ffmpeg is None:
            return "ffmpeg saknas på Pi:n. Kör: sudo apt install ffmpeg"
        if self.last_error:
            return f"Fel: {self.last_error}"
        if not self.config["recording_enabled"]:
            state = "Avstängd i adminvyn"
        elif self.clip is not None:
            state = f"Spelar in ({self.clip.duration_s:.0f} s, rörelse {self.motion:.0f} ‰)"
        elif self.brightness is not None and self.brightness < self.config["min_brightness"]:
            state = f"För mörkt för inspelning (ljus {self.brightness:.0f}, gräns {self.config['min_brightness']})"
        elif time.monotonic() < self.warm_until:
            state = "Lär in bakgrunden"
        else:
            state = f"Väntar på rörelse (just nu {self.motion:.0f} ‰, gräns {self.config['motion_sensitivity']} ‰)"
        return f"{state} · {self.clips_done} klipp sedan start · {pending_uploads} kvar att ladda upp"

    # ---------- bilder från kameran ----------

    def feed(self, rgb: np.ndarray) -> None:
        """Anropas med varje kamerabild (RGB, redan roterad)."""
        if not self.enabled:
            if self.clip is not None:
                self._end_clip()
            self.pre_roll.clear()
            return
        now = time.monotonic()
        motion = self._detect(rgb, now)
        frame = self._scale(rgb)

        if self.clip is not None and frame.shape != self.clip.shape:
            self._end_clip()   # rotationen ändrades mitt i ett klipp

        if self.clip is None:
            keep = self.config["pre_roll_s"]
            self.pre_roll.append((now, frame))
            while self.pre_roll and now - self.pre_roll[0][0] > keep:
                self.pre_roll.popleft()
            if motion and self._may_start():
                self._start_clip(now, frame)
            return

        clip = self.clip
        clip.add(now, frame)
        if self.motion >= clip.peak_motion:
            clip.peak_motion, clip.peak_frame = self.motion, frame
        if motion:
            clip.last_motion_t = now
        if now - clip.last_motion_t > self.config["post_roll_s"] or clip.duration_s >= self.config["max_clip_s"]:
            self._end_clip()

    def _scale(self, rgb: np.ndarray) -> np.ndarray:
        if self.config["rec_resolution"] == "640x360" and max(rgb.shape[:2]) >= 1280:
            return np.ascontiguousarray(rgb[::2, ::2])
        return rgb

    def _detect(self, rgb: np.ndarray, now: float) -> bool:
        small = rgb[::SMALL_STEP, ::SMALL_STEP].astype(np.float32)
        gray = small[..., 0] * 0.299 + small[..., 1] * 0.587 + small[..., 2] * 0.114
        self.brightness = round(float(gray.mean()) / 255 * 100, 1)
        if self.background is None or self.background.shape != gray.shape:
            self.background = gray
            self.warm_until = now + WARMUP_S
            self.motion, self.moving_frames = 0.0, 0
            return False
        diff = np.abs(gray - self.background)
        diff -= np.median(diff)                      # räkna bort ljusändringar över hela bilden
        self.motion = float((diff > PIXEL_CHANGE).mean() * 1000)
        # Bakgrunden följer långsamt med, så att skuggor och ljus som ändras sakta inte räknas.
        # Under ett klipp går det ännu långsammare, så att ett djur som sitter still inte blir bakgrund direkt.
        if now < self.warm_until:
            rate = 0.3
        else:
            rate = 0.005 if self.clip is not None else 0.02
        self.background += (gray - self.background) * rate
        if now < self.warm_until:
            return False
        limit = self.config["motion_sensitivity"]
        if self.clip is not None:
            return self.motion >= limit / 2          # lite lägre gräns för att fortsätta än för att starta
        # Två bilder i rad krävs för att starta, så att enstaka brus inte ger ett klipp.
        self.moving_frames = self.moving_frames + 1 if self.motion >= limit else 0
        return self.moving_frames >= 2

    def _may_start(self) -> bool:
        if self.brightness is not None and self.brightness < self.config["min_brightness"]:
            return False
        try:
            if shutil.disk_usage(CLIP_DIR).free < MIN_FREE_BYTES:
                self.last_error = "Minneskortet är nästan fullt"
                return False
        except OSError:
            return False
        return True

    def _start_clip(self, now: float, frame: np.ndarray) -> None:
        first_t = self.pre_roll[0][0] if self.pre_roll else now
        try:
            clip = Clip(first_t, frame.shape, self.fps)
        except OSError as e:
            self.last_error = f"Kunde inte starta ffmpeg: {e}"
            return
        clip.brightness = self.brightness
        clip.peak_motion, clip.peak_frame = self.motion, frame
        for t, old in self.pre_roll:
            clip.add(t, old)
        self.pre_roll.clear()
        self.clip = clip
        print(f"Rörelse ({self.motion:.0f} ‰): spelar in klipp {clip.id}", flush=True)

    def _end_clip(self) -> None:
        clip, self.clip = self.clip, None
        print(f"Klipp {clip.id} klart: {clip.duration_s:.1f} s, {clip.dropped} tappade bilder", flush=True)
        clip.finish(self._clip_done)

    def _clip_done(self, clip: Clip, error: str | None) -> None:
        if error:
            self.last_error = error
            print(f"Klipp {clip.id} misslyckades: {error}", flush=True)
        else:
            self.last_error = ""
            self.clips_done += 1

    def stop(self) -> None:
        if self.clip is not None:
            self._end_clip()


class ClipUploader:
    """Laddar upp färdiga klipp till lennart.cam, ett i taget och äldst först."""

    def __init__(self) -> None:
        url = urlparse(os.environ.get("LENNART_SERVER_URL", ""))
        self.secure = url.scheme == "https"
        self.host = url.netloc
        self.token = os.environ.get("LENNART_DEVICE_TOKEN", "")
        self._stop = threading.Event()
        self.last_error = ""

    @property
    def enabled(self) -> bool:
        return bool(self.host and self.token)

    @staticmethod
    def waiting() -> list[Path]:
        """Färdiga klipp som inte laddats upp än. Uppladdade klipp har en .done-fil."""
        try:
            return sorted(p for p in CLIP_DIR.glob("*.json") if not p.with_suffix(".done").exists())
        except OSError:
            return []

    def _post(self, path: str, body, length: int, content_type: str, extra: dict) -> tuple[int, str]:
        cls = http.client.HTTPSConnection if self.secure else http.client.HTTPConnection
        conn = cls(self.host, timeout=120)
        try:
            headers = {"Authorization": f"Bearer {self.token}", "User-Agent": "lennart-pi",
                       "Content-Type": content_type, "Content-Length": str(length), **extra}
            conn.request("POST", path, body=body, headers=headers)
            response = conn.getresponse()
            return response.status, response.read(500).decode("utf-8", "replace")
        finally:
            conn.close()

    def upload(self, meta_file: Path) -> int:
        clip_id = meta_file.stem
        video = meta_file.with_suffix(".mp4")
        meta = json.loads(meta_file.read_text())
        size = video.stat().st_size
        with open(video, "rb") as f:
            status, text = self._post(f"/api/clips/{clip_id}", f, size, "video/mp4",
                                      {"X-Clip-Meta": json.dumps(meta)})
        if status != 200:
            self.last_error = f"Servern svarade {status} på klipp {clip_id}: {text[:120]}"
            return status
        thumb = meta_file.with_suffix(".jpg")
        if thumb.exists():
            jpeg = thumb.read_bytes()
            self._post(f"/api/clips/{clip_id}/thumb", jpeg, len(jpeg), "image/jpeg", {})
        meta_file.with_suffix(".done").touch()
        self.last_error = ""
        print(f"Laddade upp klipp {clip_id} ({size // 1024} kB)", flush=True)
        return status

    def cleanup(self) -> None:
        """Rensa gamla klipp på Pi:n när de tar mer plats än LENNART_CLIP_LOCAL_GB.

        Uppladdade klipp tas bort först. Klipp som inte laddats upp tas bara bort om
        utrymmet ändå är slut, så att minneskortet aldrig blir fullt.
        """
        try:
            files = [f for f in CLIP_DIR.iterdir() if f.is_file()]
        except OSError:
            return
        total = sum(f.stat().st_size for f in files)
        if total <= LOCAL_MAX_BYTES:
            return
        ids = sorted({f.name.split(".")[0] for f in files if f.suffix == ".json"})
        uploaded = [i for i in ids if (CLIP_DIR / f"{i}.done").exists()]
        for clip_id in uploaded + [i for i in ids if i not in uploaded]:
            if total <= LOCAL_MAX_BYTES:
                break
            if clip_id not in uploaded:
                print(f"Tar bort klipp {clip_id} som inte hunnit laddas upp, utrymmet är slut", flush=True)
            for suffix in (".mp4", ".jpg", ".json", ".done"):
                f = CLIP_DIR / f"{clip_id}{suffix}"
                if f.exists():
                    total -= f.stat().st_size
                    f.unlink()

    def _run(self) -> None:
        backoff = 5
        while not self._stop.is_set():
            self.cleanup()
            waiting = self.waiting()
            if not waiting:
                self._stop.wait(5)
                continue
            try:
                status = self.upload(waiting[0])
            except (OSError, http.client.HTTPException, ValueError) as e:
                self.last_error = f"Uppladdningen misslyckades: {type(e).__name__}: {e}"
                status = 0
            if status == 200:
                backoff = 5
                continue
            if status in (400, 413):
                # Servern tar aldrig emot just det här klippet. Markera det, så att kön inte fastnar.
                waiting[0].with_suffix(".done").write_text(self.last_error)
                continue
            # Nätverksfel, fullt på servern (507) eller servern nere: försök igen senare.
            wait = 600 if status == 507 else backoff
            print(f"{self.last_error} – försöker igen om {wait} s", flush=True)
            self._stop.wait(wait)
            backoff = min(backoff * 2, 300)

    def start(self) -> None:
        if not self.enabled:
            print("Uppladdning av klipp avstängd: LENNART_SERVER_URL eller LENNART_DEVICE_TOKEN saknas i .env", flush=True)
            return
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()
