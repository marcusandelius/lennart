"""Drivrutin för Waveshare 2" LCD (ST7789, 320 × 240) över SPI på Raspberry Pi 5.

Skärmen är byggd för Raspberry Pi Pico men talar vanlig SPI, så den kan kopplas
till Pi:ns SPI0 med kopplingskablar (se docs/koppling-display.md).

Varför egen drivrutin: den är kort, går att förstå rad för rad, och använder bara
spidev och gpiozero, som båda fungerar på Pi 5. Flera färdiga bibliotek bygger på
RPi.GPIO, som inte fungerar på Pi 5.

Hur skärmen fungerar: Pi:n skickar ett kommando (DC-pinnen låg) följt av data
(DC-pinnen hög). Bilden skickas som 16 bitar per pixel (RGB565): 5 bitar rött,
6 grönt och 5 blått.
"""

import os
import time

import numpy as np

WIDTH, HEIGHT = 320, 240

# ST7789-kommandon (ur databladet)
SWRESET = 0x01  # mjuk omstart
SLPOUT = 0x11   # vakna ur viloläge
NORON = 0x13    # normalt visningsläge
INVON = 0x21    # inverterade färger – den här panelen behöver det för rätt färger
DISPON = 0x29   # tänd skärmen
CASET = 0x2A    # kolumnfönster
RASET = 0x2B    # radfönster
RAMWR = 0x2C    # skriv pixlar
MADCTL = 0x36   # rotation och färgordning
COLMOD = 0x3A   # pixelformat

# MADCTL-värden för liggande bild (320 bred). Prova 90 eller 270 om bilden står upp och ner.
ROTATIONS = {90: 0x60, 270: 0xA0}


def _env_int(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


class Display:
    def __init__(self) -> None:
        # Importeras här så att resten av programmet kan testas utan Pi-hårdvara.
        import spidev
        from gpiozero import DigitalOutputDevice

        dc_pin = _env_int("LCD_DC", 25)
        rst_pin = _env_int("LCD_RST", 27)
        bl_pin = _env_int("LCD_BL", 18)
        rotation = _env_int("LCD_ROTATION", 90)
        bgr = os.environ.get("LCD_BGR", "0") == "1"

        self.dc = DigitalOutputDevice(dc_pin)
        self.rst = DigitalOutputDevice(rst_pin, initial_value=True)
        self.bl = DigitalOutputDevice(bl_pin)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # SPI0, chip select CE0 (GPIO 8)
        self.spi.mode = 0
        self.spi.max_speed_hz = _env_int("LCD_SPI_HZ", 32_000_000)

        self._madctl = ROTATIONS.get(rotation, 0x60) | (0x08 if bgr else 0x00)
        self._init_panel()
        self.bl.on()

    def _command(self, cmd: int, data: bytes = b"") -> None:
        self.dc.off()
        self.spi.writebytes([cmd])
        if data:
            self.dc.on()
            self.spi.writebytes2(data)

    def _init_panel(self) -> None:
        # Hårdvaruomstart: RST låg en kort stund.
        self.rst.off()
        time.sleep(0.02)
        self.rst.on()
        time.sleep(0.15)
        self._command(SWRESET)
        time.sleep(0.15)
        self._command(SLPOUT)
        time.sleep(0.12)
        self._command(COLMOD, bytes([0x55]))  # 16 bitar per pixel
        self._command(MADCTL, bytes([self._madctl]))
        self._command(INVON)
        self._command(NORON)
        self._command(DISPON)
        time.sleep(0.02)
        # Hela skärmen som fönster: kolumn 0–319, rad 0–239.
        self._command(CASET, bytes([0, 0, (WIDTH - 1) >> 8, (WIDTH - 1) & 0xFF]))
        self._command(RASET, bytes([0, 0, (HEIGHT - 1) >> 8, (HEIGHT - 1) & 0xFF]))

    def show(self, rgb: np.ndarray) -> None:
        """Visa en bild med formen (240, 320, 3) i RGB-ordning."""
        self._command(RAMWR, to_rgb565(rgb))

    def close(self) -> None:
        try:
            self.show(np.zeros((HEIGHT, WIDTH, 3), np.uint8))
            self.bl.off()
            self.spi.close()
        except Exception:
            pass


def to_rgb565(rgb: np.ndarray) -> bytes:
    """Gör om RGB (8 bitar per färg) till RGB565, med den mest signifikanta byten först."""
    r = rgb[..., 0].astype(np.uint16)
    g = rgb[..., 1].astype(np.uint16)
    b = rgb[..., 2].astype(np.uint16)
    pixels = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return pixels.astype(">u2").tobytes()
