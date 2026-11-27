"""Servon via PCA9685-kortet (I2C) på Raspberry Pi 5.

Varför ett servokort: Pi 5 kan inte ge stabila servosignaler själv, och servona
ska ha egen ström. PCA9685 skapar 16 servosignaler och tar emot kommandon över
I2C (två trådar: SDA och SCL). Se docs/koppling-servon.md.

Hur ett servo styrs: en puls var 20:e millisekund (50 Hz). Pulsens längd avgör
vinkeln, typiskt 500 µs = 0° och 2500 µs = 180°. Kortet räknar tiden i 4096 steg
per period, så pulslängden räknas om till steg.

Signalen släpps efter varje rörelse, så att servot inte står och surrar och
drar ström i onödan.
"""

import glob
import os
import queue
import threading
import time

ADDRESS = 0x40          # PCA9685:s standardadress
MODE1, MODE2, PRESCALE, LED0_ON_L = 0x00, 0x01, 0xFE, 0x06
OSC_HZ = 25_000_000     # kortets inbyggda oscillator
PWM_HZ = 50             # servon vill ha 50 pulser per sekund
PERIOD_US = 1_000_000 / PWM_HZ
RELEASE_AFTER_S = 1.0   # släpp signalen så här länge efter en rörelse


def _open_bus(number: int):
    try:
        from smbus2 import SMBus
    except ImportError:
        from smbus import SMBus  # paketet python3-smbus
    return SMBus(number)


def find_bus() -> int:
    """Hitta I2C-bussen där PCA9685 svarar. Normalt buss 1 (stift 3 och 5), kan styras med SERVO_I2C_BUS."""
    if "SERVO_I2C_BUS" in os.environ:
        return int(os.environ["SERVO_I2C_BUS"])
    buses = sorted(int(p.removeprefix("/dev/i2c-")) for p in glob.glob("/dev/i2c-[0-9]*"))
    if not buses:
        raise RuntimeError("Ingen /dev/i2c-* finns. Är I2C påslaget (raspi-config) och Pi:n omstartad?")
    for number in sorted(buses, key=lambda n: n != 1):  # prova buss 1 först
        try:
            bus = _open_bus(number)
            try:
                bus.read_byte_data(ADDRESS, MODE1)
                return number
            finally:
                bus.close()
        except OSError:
            continue
    raise RuntimeError(f"Inget servokort (PCA9685, adress 0x40) svarar på I2C-buss {buses}. Kontrollera kablarna.")


class PCA9685:
    def __init__(self) -> None:
        self.bus_number = find_bus()
        self.bus = _open_bus(self.bus_number)
        prescale = round(OSC_HZ / (4096 * PWM_HZ)) - 1  # = 121 för 50 Hz
        self.bus.write_byte_data(ADDRESS, MODE1, 0x10)          # viloläge, krävs för att ändra frekvens
        self.bus.write_byte_data(ADDRESS, PRESCALE, prescale)
        self.bus.write_byte_data(ADDRESS, MODE1, 0x20)          # vakna, med automatisk registerstegning
        time.sleep(0.005)
        self.bus.write_byte_data(ADDRESS, MODE1, 0xA0)          # starta om PWM
        self.bus.write_byte_data(ADDRESS, MODE2, 0x04)          # vanliga utgångar (totem pole)

    def pulse(self, channel: int, microseconds: float) -> None:
        ticks = max(0, min(4095, round(microseconds * 4096 / PERIOD_US)))
        reg = LED0_ON_L + 4 * channel
        self.bus.write_i2c_block_data(ADDRESS, reg, [0, 0, ticks & 0xFF, ticks >> 8])

    def off(self, channel: int) -> None:
        reg = LED0_ON_L + 4 * channel
        self.bus.write_i2c_block_data(ADDRESS, reg, [0, 0, 0, 0x10])  # bit 4 i OFF_H = helt av


class ServoController:
    """Tar emot kommandon från lennart.cam och utför dem ett i taget i en egen tråd."""

    def __init__(self, on_change) -> None:
        self.config = {"servo_doser_channel": 0, "servo_lucka_channel": 1,
                       "servo_min_us": 500, "servo_max_us": 2500, "dispense_angle": 119}
        self.on_change = on_change         # anropas efter varje kommando, t.ex. för att rapportera direkt
        self.board: PCA9685 | None = None
        self.error = ""
        # Senast beordrade vinkel. Servot står kvar ungefär där även när signalen släppts,
        # så den används som start för långsamma rörelser. None = okänd (efter start).
        self.position = {"doser": None, "lucka": None}
        self.holding = {"doser": False, "lucka": False}  # skickas signal just nu?
        self.last = ""
        self._queue: queue.Queue = queue.Queue()
        threading.Thread(target=self._run, name="servo", daemon=True).start()

    # ---------- status till lennart.cam ----------

    @property
    def ok(self) -> bool:
        return self.board is not None

    def info(self) -> str:
        if self.board is None:
            return f"Servokort: {self.error or 'inte anslutet än'}"
        def show(name):
            angle = self.position[name]
            where = "okänt läge" if angle is None else f"{angle}°"
            return f"{name} {where}{'' if self.holding[name] else ' (släppt)'}"
        text = f"PCA9685 på I2C-buss {self.board.bus_number} · {show('doser')} · {show('lucka')}"
        return f"{text} · senast: {self.last}" if self.last else text

    # ---------- kommandon ----------

    def submit(self, cmd: dict) -> None:
        self._queue.put(cmd)

    def _connect(self) -> bool:
        if self.board is not None:
            return True
        try:
            self.board = PCA9685()
            self.error = ""
            print(f"Servokortet hittat på I2C-buss {self.board.bus_number}", flush=True)
            return True
        except Exception as e:
            self.error = f"{type(e).__name__}: {e}"
            print(f"Servokortet gick inte att nå: {self.error}", flush=True)
            return False

    def _channel(self, name: str) -> int:
        return self.config[f"servo_{name}_channel"]

    def _us(self, angle: float) -> float:
        low, high = self.config["servo_min_us"], self.config["servo_max_us"]
        return low + (high - low) * angle / 180

    def _move(self, name: str, angle: int, slow: bool = False) -> None:
        start = self.position[name]
        if slow and start is not None:
            step = 2 if angle > start else -2
            for a in range(start, angle, step):     # 2° var 30:e ms ≈ 65° per sekund
                self.board.pulse(self._channel(name), self._us(a))
                time.sleep(0.03)
        self.board.pulse(self._channel(name), self._us(angle))
        self.position[name] = angle
        self.holding[name] = True

    def _release(self, name: str) -> None:
        self.board.off(self._channel(name))
        self.holding[name] = False

    def _test_dispense(self, angle: int) -> None:
        # Ett litet vick skakar om nötterna så att en lägger sig i fickan, sedan ut och tillbaka.
        for a, pause in ((0, 0.4), (12, 0.15), (0, 0.15), (12, 0.15), (0, 0.3), (angle, 0.8), (0, 0.6)):
            self._move("doser", a)
            time.sleep(pause)

    def _run(self) -> None:
        while True:
            cmd = self._queue.get()
            try:
                if not self._connect():
                    continue
                action = cmd.get("action")
                if action == "move":
                    self._move(cmd["servo"], cmd["angle"], cmd.get("slow", False))
                    self.last = f"{cmd['servo']} till {cmd['angle']}°"
                    time.sleep(RELEASE_AFTER_S)
                    self._release(cmd["servo"])
                elif action == "release":
                    for name in (("doser", "lucka") if cmd["servo"] == "alla" else (cmd["servo"],)):
                        self._release(name)
                    self.last = f"släppte {cmd['servo']}"
                elif action == "test_dispense":
                    self._test_dispense(cmd["angle"])
                    time.sleep(RELEASE_AFTER_S)
                    self._release("doser")
                    self.last = f"testade utmatning ({cmd['angle']}°)"
                print(f"Servo: {self.last}", flush=True)
            except Exception as e:
                # Tappad kontakt med kortet: försök ansluta på nytt vid nästa kommando.
                self.error = f"{type(e).__name__}: {e}"
                self.board = None
                print(f"Servo: fel – {self.error}", flush=True)
            finally:
                self.on_change()
