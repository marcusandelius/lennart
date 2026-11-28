"""Drivrutin för Waveshare 2" LCD (ST7789, 320 × 240) över SPI på Raspberry Pi 5.

Skärmen är byggd för Raspberry Pi Pico men talar vanlig SPI, så den kan kopplas
till Pi:ns SPI0 med kopplingskablar (se docs/koppling-display.md).

Varför egen drivrutin: den är kort, går att förstå rad för rad, och använder bara
spidev (SPI) och lgpio (styrpinnarna), som båda fungerar på Pi 5. Flera färdiga
bibliotek bygger på RPi.GPIO, som inte fungerar på Pi 5. Även gpiozero valde fel
bibliotek eller fel GPIO-krets på Pi 5, så pinnarna styrs med lgpio direkt.

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
GAMSET = 0x26   # välj en av panelens inbyggda kontrastkurvor (gamma)

# Kontrastkurvorna i ST7789 enligt databladet [verifiera]: 0x01 = gamma 2.2, 0x02 = 1.8, 0x04 = 2.5,
# 0x08 = 1.0. Högre gamma gör mellantonerna mörkare: färgerna blir mättade och bakgrunden mörkare.
GAMMA_CURVES = {"mjuk": 0x02, "normal": 0x01, "stark": 0x04}
COLMOD = 0x3A   # pixelformat

# MADCTL-värden för liggande bild (320 bred). Prova 90 eller 270 om bilden står upp och ner.
ROTATIONS = {90: 0x60, 270: 0xA0}


def _env_int(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


class OutputPin:
    """En GPIO-pinne som utgång, via lgpio. Pinnens nummer är samma som GPIO-numret."""

    _handles: dict = {}  # en öppen GPIO-krets delas av alla pinnar

    def __init__(self, chip: int, pin: int, initial: bool = False) -> None:
        import lgpio

        self._lgpio = lgpio
        try:
            if chip not in OutputPin._handles:
                OutputPin._handles[chip] = lgpio.gpiochip_open(chip)
            self._h = OutputPin._handles[chip]
            lgpio.gpio_claim_output(self._h, pin, int(initial))
        except Exception as e:
            raise RuntimeError(f"GPIO {pin} på gpiochip{chip}: {e}") from e
        self._pin = pin
        self.value = initial

    def on(self) -> None:
        self._lgpio.gpio_write(self._h, self._pin, 1)
        self.value = True

    def off(self) -> None:
        self._lgpio.gpio_write(self._h, self._pin, 0)
        self.value = False


class Display:
    def __init__(self) -> None:
        # Importeras här så att resten av programmet kan testas utan Pi-hårdvara.
        import spidev

        dc_pin = _env_int("LCD_DC", 25)
        rst_pin = _env_int("LCD_RST", 27)
        bl_pin = _env_int("LCD_BL", 18)
        rotation = _env_int("LCD_ROTATION", 90)
        bgr = os.environ.get("LCD_BGR", "0") == "1"

        chip = find_header_gpiochip()
        self.dc = OutputPin(chip, dc_pin)
        self.rst = OutputPin(chip, rst_pin, initial=True)
        self.bl = OutputPin(chip, bl_pin)

        bus, device = find_spi_device()
        self.spi_device = f"/dev/spidev{bus}.{device}"
        self.gpiochip = chip
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)  # SPI0 på stiftlisten, chip select CE0 (GPIO 8)
        self.spi.mode = 0
        self.spi.max_speed_hz = _env_int("LCD_SPI_HZ", 32_000_000)

        self._madctl = ROTATIONS.get(rotation, 0x60) | (0x08 if bgr else 0x00)
        self.gamma = "normal"
        self._init_panel()
        self.bl.on()

    @property
    def speed_hz(self) -> int:
        return self.spi.max_speed_hz

    def set_speed(self, hz: int) -> None:
        """Byt SPI-hastighet. Gäller från nästa överföring, utan omstart av skärmen."""
        self.spi.max_speed_hz = hz

    def set_gamma(self, name: str) -> None:
        """Byt kontrastkurva. Gäller direkt för det som visas, utan att bilden skickas om."""
        if name in GAMMA_CURVES:
            self.gamma = name
            self._command(GAMSET, bytes([GAMMA_CURVES[name]]))

    def restart(self) -> None:
        """Starta om skärmen: omstart via RST och alla startkommandon igen.

        Behövs om skärmen fick ström efter att programmet startade den.
        """
        self._init_panel()
        self.bl.on()

    def info(self) -> str:
        """Kort beskrivning för adminvyn, så att felsökning går utan att logga in på Pi:n."""
        import glob

        found = ", ".join(p.removeprefix("/dev/spidev") for p in sorted(glob.glob("/dev/spidev*")))
        return (f"{self.spi_device} i {self.speed_hz / 1e6:g} MHz, kontrast {self.gamma}, gpiochip{self.gpiochip}"
                f" (SPI-enheter: {found or 'inga'})")

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
        self._command(GAMSET, bytes([GAMMA_CURVES[self.gamma]]))
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


def find_spi_device() -> tuple[int, int]:
    """Hitta SPI-enheten för stiftlistens SPI0 med chip select CE0: /dev/spidev0.0.

    Den finns bara när SPI är påslaget (raspi-config, eller dtparam=spi=on i
    /boot/firmware/config.txt) och Pi:n har startats om. En Pi 5 kan ha
    /dev/spidev10.0 även utan det, men den bussen går inte till stiftlisten
    [verifiera], så den används inte. Kan styras med LCD_SPI_DEV, t.ex. LCD_SPI_DEV=0.0.
    """
    import glob

    if "LCD_SPI_DEV" in os.environ:
        bus, device = os.environ["LCD_SPI_DEV"].split(".")
        return int(bus), int(device)
    found = sorted(glob.glob("/dev/spidev*"))
    if "/dev/spidev0.0" in found:
        return 0, 0
    others = f" (finns bara {', '.join(found)})" if found else ""
    raise RuntimeError(f"SPI på stiftlisten är inte påslaget: /dev/spidev0.0 saknas{others}. "
                       "Slå på SPI med raspi-config och starta om Pi:n.")


def find_header_gpiochip() -> int:
    """Hitta GPIO-kretsen för stiftlisten.

    På Pi 5 sitter stiftlisten på RP1-kretsen ("pinctrl-rp1"). Dess nummer skiljer
    sig mellan kärnversioner (gpiochip4, gpiochip0, gpiochip1x …), så den letas upp
    via etiketten. Kan styras med LCD_GPIOCHIP.
    """
    if "LCD_GPIOCHIP" in os.environ:
        return int(os.environ["LCD_GPIOCHIP"])
    import lgpio

    opened, first_error = [], None
    # Numren varierar mellan kärnversioner (t.ex. 0–4 eller 11–15), så leta igenom alla.
    import glob
    chips = sorted(int(p.removeprefix("/dev/gpiochip")) for p in glob.glob("/dev/gpiochip[0-9]*"))
    for chip in chips:
        try:
            handle = lgpio.gpiochip_open(chip)
        except Exception as e:
            first_error = first_error or f"gpiochip{chip}: {e}"
            continue
        try:
            _, _, name, label = lgpio.gpio_get_chip_info(handle)
        finally:
            lgpio.gpiochip_close(handle)
        opened.append(f"{chip}={label}")
        if "rp1" in f"{name} {label}".lower():
            return chip
    if not opened:
        raise RuntimeError(f"Kan inte öppna någon GPIO-krets av {chips} ({first_error}). Är kontot med i gruppen gpio?")
    raise RuntimeError(f"Ingen GPIO-krets heter pinctrl-rp1. Hittade: {', '.join(opened)}")


def to_rgb565(rgb: np.ndarray) -> bytes:
    """Gör om RGB (8 bitar per färg) till RGB565, med den mest signifikanta byten först."""
    r = rgb[..., 0].astype(np.uint16)
    g = rgb[..., 1].astype(np.uint16)
    b = rgb[..., 2].astype(np.uint16)
    pixels = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return pixels.astype(">u2").tobytes()
