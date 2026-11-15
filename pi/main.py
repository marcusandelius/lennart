"""Lennarts matstation – programmet på Raspberry Pi.

Visar kamerans bild live på 2"-skärmen, rapporterar status till lennart.cam,
skickar livebild när någon tittar där och tar emot inställningar och
servokommandon från adminvyn. Igenkänningen läggs till senare.

Inställningar läses från miljön (~/.config/lennart/.env via systemd):
  LENNART_SERVER_URL, LENNART_DEVICE_TOKEN  – för heartbeat
  CAMERA_FLIP=1                              – vänd bilden 180° tills adminvyn säger något annat
  DISPLAY_FPS                                – bilder per sekund på skärmen (standard 10)
  LCD_*                                      – se display.py
"""

import os
import math
import signal
import sys
import textwrap
import threading
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from display import HEIGHT, WIDTH, Display
from heartbeat import Heartbeat
from live import LiveSender
from servo import ServoController

CAMERA_RETRY_S = 30
# Kameran levererar 1280 × 720 (16:9). Livebilden skalas ner till vald upplösning,
# och skärmen får var fjärde bildpunkt (320 × 180) med svarta kanter upptill och nedtill.
CAMERA_SIZE = (1280, 720)
# Skärmen är en förhandsvisning, så 10 bilder per sekund räcker. Färre bilder ger
# mindre processorlast och värme. Kan ändras med DISPLAY_FPS i .env.
DISPLAY_FPS = float(os.environ.get("DISPLAY_FPS", "10"))

GREEN = (60, 200, 90)
RED = (230, 70, 60)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)


def load_font(size: int):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


FONT_SMALL = load_font(14)
FONT_BIG = load_font(26)


def start_camera():
    """Startar Camera Module 3 med en bildström i 1280 × 720. Rotationen görs i mjukvaran."""
    from libcamera import controls
    from picamera2 import Picamera2

    cam = Picamera2()
    config = cam.create_video_configuration(
        main={"size": CAMERA_SIZE, "format": "RGB888"},
        buffer_count=4,
    )
    cam.configure(config)
    cam.start()
    try:
        cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})  # autofokus hela tiden
    except Exception:
        pass  # kameror utan autofokus klarar sig utan
    return cam


def message_screen(title: str, detail: str = "") -> np.ndarray:
    img = Image.new("RGB", (WIDTH, HEIGHT), (40, 20, 18))
    draw = ImageDraw.Draw(img)
    draw.text((16, 80), title, font=FONT_BIG, fill=WHITE)
    for i, line in enumerate(textwrap.wrap(detail, 34)[:5]):
        draw.text((16, 124 + i * 18), line, font=FONT_SMALL, fill=GREY)
    return np.asarray(img)


def rotate(rgb: np.ndarray, degrees: int) -> np.ndarray:
    """Vrid bilden medsols i steg om 90°. np.rot90 vrider motsols, därav minustecknet."""
    turns = (degrees // 90) % 4
    return np.ascontiguousarray(np.rot90(rgb, -turns)) if turns else rgb


def for_display(rgb: np.ndarray) -> np.ndarray:
    """Skala ner kamerabilden så att den ryms på skärmen, centrerad med svarta kanter."""
    h, w = rgb.shape[:2]
    step = max(math.ceil(h / HEIGHT), math.ceil(w / WIDTH))  # 4 för liggande bild, 6 för stående
    small = rgb[::step, ::step][:HEIGHT, :WIDTH]
    canvas = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    top, left = (HEIGHT - small.shape[0]) // 2, (WIDTH - small.shape[1]) // 2
    canvas[top:top + small.shape[0], left:left + small.shape[1]] = small
    return canvas


def add_status_bar(rgb: np.ndarray, server_ok: bool | None, fps: float) -> np.ndarray:
    img = Image.fromarray(rgb)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH, 20), fill=(0, 0, 0))
    color = GREY if server_ok is None else GREEN if server_ok else RED
    draw.ellipse((6, 5, 16, 15), fill=color)
    draw.text((22, 2), "lennart.cam", font=FONT_SMALL, fill=WHITE)
    draw.text((WIDTH - 70, 2), f"{fps:4.1f} fps", font=FONT_SMALL, fill=WHITE)
    return np.asarray(img)


def main() -> int:
    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, stop)  # systemd stoppar tjänsten med SIGTERM
    signal.signal(signal.SIGINT, stop)

    display, display_error = None, ""
    try:
        display = Display()
        print("Skärmen är igång", flush=True)
    except Exception as e:
        display_error = f"{type(e).__name__}: {e}"
        print(f"Skärmen gick inte att starta: {display_error}", flush=True)

    # Starta kameran innan första rapporten, så att den inte felaktigt säger "fel".
    camera, camera_error, camera_tried = None, "", time.monotonic()
    try:
        camera = start_camera()
        print("Kameran är igång", flush=True)
    except Exception as e:
        camera_error = f"{type(e).__name__}: {e}"
        print(f"Kameran gick inte att starta: {camera_error}", flush=True)
    fps = 0.0

    # Inställningar från adminvyn. CAMERA_FLIP gäller bara tills servern har svarat.
    device = {"camera_rotation": 180 if os.environ.get("CAMERA_FLIP", "0") == "1" else 0}

    # Efter varje servokommando skickas en rapport direkt, så att adminvyn ser resultatet.
    servo = ServoController(on_change=lambda: threading.Thread(target=heartbeat.send_once, daemon=True).start())

    def status() -> dict:
        # Felmeddelandet skickas med, så att fel kan felsökas från lennart.cam utan att logga in på Pi:n.
        problems = []
        if camera is None and camera_error:
            problems.append(f"Kamera: {camera_error}")
        if display is None and display_error:
            problems.append(f"Skärm: {display_error}")
        report = {"camera_ok": camera is not None, "display_ok": display is not None, "fps": round(fps, 1),
                  "camera_rotation": device["camera_rotation"], "servo_ok": servo.ok, "servo_info": servo.info()[:200]}
        if problems:
            report["message"] = " · ".join(problems)[:200]
        return report

    heartbeat = Heartbeat(status)
    heartbeat.start()

    # Senaste kamerabilden delas med livebilden, som skickar den när någon tittar.
    latest = {"rgb": None}

    def on_config(config: dict) -> None:
        device.update(config)
        servo.config.update({k: v for k, v in config.items() if k in servo.config})
        print(f"Nya inställningar från lennart.cam: {config}", flush=True)

    def on_commands(commands: list) -> None:
        for cmd in commands:
            print(f"Kommando från lennart.cam: {cmd}", flush=True)
            servo.submit(cmd)

    live = LiveSender(lambda: latest["rgb"], on_config, on_commands)
    live.start()

    frames, fps_since = 0, time.monotonic()
    while running:
        now = time.monotonic()
        if camera is None and now - camera_tried > CAMERA_RETRY_S:
            camera_tried = now
            try:
                camera = start_camera()
                print("Kameran är igång", flush=True)
            except Exception as e:
                camera_error = f"{type(e).__name__}: {e}"
                print(f"Kameran gick inte att starta: {camera_error}", flush=True)

        # Kameran behövs bara när skärmen ska visa något eller någon tittar på livebilden.
        if camera is None or (display is None and not live.active):
            latest["rgb"] = None
            if display is not None and camera is None:
                display.show(add_status_bar(message_screen("Ingen kamera", camera_error), heartbeat.last_ok, fps))
            time.sleep(0.5)
            continue

        try:
            frame = camera.capture_array("main")
        except Exception as e:
            camera_error = f"{type(e).__name__}: {e}"
            print(f"Kameran slutade fungera: {camera_error}", flush=True)
            camera = None
            continue
        rgb = np.ascontiguousarray(frame[..., ::-1])  # picamera2 levererar "RGB888" i ordningen blå, grön, röd
        rgb = rotate(rgb, device["camera_rotation"])
        latest["rgb"] = rgb

        if display is not None:
            display.show(add_status_bar(for_display(rgb), heartbeat.last_ok, fps))

        # Vänta in nästa bild: skärmens takt, eller livebildens om ingen skärm finns.
        target_fps = DISPLAY_FPS if display is not None else max(live.fps, 1)
        spare = 1 / target_fps - (time.monotonic() - now)
        if spare > 0:
            time.sleep(spare)

        frames += 1
        if now - fps_since >= 5:
            fps = frames / (now - fps_since)
            frames, fps_since = 0, now

    print("Stänger av", flush=True)
    heartbeat.stop()
    live.stop()
    if camera is not None:
        camera.stop()
    if display is not None:
        display.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
