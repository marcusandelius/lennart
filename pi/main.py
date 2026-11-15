"""Lennarts matstation – första testversion på Raspberry Pi.

Visar kamerans bild live på 2"-skärmen och rapporterar status till lennart.cam.
Syftet är att se att kamera, skärm, uppkoppling och automatisk deploy fungerar,
innan igenkänning, servon och lucka läggs till.

Inställningar läses från miljön (~/.config/lennart/.env via systemd):
  LENNART_SERVER_URL, LENNART_DEVICE_TOKEN  – för heartbeat
  CAMERA_FLIP=1                              – vänd bilden 180° om kameran sitter upp och ner
  LCD_*                                      – se display.py
"""

import signal
import sys
import textwrap
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from display import HEIGHT, WIDTH, Display
from heartbeat import Heartbeat

CAMERA_RETRY_S = 30

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
    """Startar Camera Module 3 med en bildström i skärmens storlek."""
    import os

    from libcamera import Transform, controls
    from picamera2 import Picamera2

    flip = os.environ.get("CAMERA_FLIP", "0") == "1"
    cam = Picamera2()
    config = cam.create_video_configuration(
        main={"size": (WIDTH, HEIGHT), "format": "RGB888"},
        transform=Transform(hflip=flip, vflip=flip),
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

    def status() -> dict:
        # Felmeddelandet skickas med, så att fel kan felsökas från lennart.cam utan att logga in på Pi:n.
        problems = []
        if camera is None and camera_error:
            problems.append(f"Kamera: {camera_error}")
        if display is None and display_error:
            problems.append(f"Skärm: {display_error}")
        report = {"camera_ok": camera is not None, "display_ok": display is not None, "fps": round(fps, 1)}
        if problems:
            report["message"] = " · ".join(problems)[:200]
        return report

    heartbeat = Heartbeat(status)
    heartbeat.start()

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

        if display is None:
            time.sleep(1)  # utan skärm finns inget att rita, men heartbeat fortsätter
            continue

        if camera is not None:
            try:
                frame = camera.capture_array("main")[:HEIGHT, :WIDTH]
                rgb = frame[..., ::-1]  # picamera2 levererar "RGB888" i ordningen blå, grön, röd
            except Exception as e:
                camera_error = f"{type(e).__name__}: {e}"
                print(f"Kameran slutade fungera: {camera_error}", flush=True)
                camera = None
                continue
        else:
            rgb = message_screen("Ingen kamera", camera_error)
            time.sleep(0.5)

        display.show(add_status_bar(np.ascontiguousarray(rgb), heartbeat.last_ok, fps))

        frames += 1
        if now - fps_since >= 5:
            fps = frames / (now - fps_since)
            frames, fps_since = 0, now

    print("Stänger av", flush=True)
    heartbeat.stop()
    if camera is not None:
        camera.stop()
    if display is not None:
        display.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
