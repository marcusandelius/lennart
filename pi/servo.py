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
import math
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
GLIDE_STEP_S = 0.02     # ny vinkel var 20:e ms under ett lugnt vrid, nära servots 50 Hz
VICK_DEG = 12           # vicket i plockläget
SWEEP_ANGLES = (10, 170)  # inte ända ut till 0° och 180°, där servot kan ta i mot sitt stopp
SWEEP_STEP_S = 0.5      # MG90S hinner 160° på cirka 0,25 s


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
                       "servo_min_us": 500, "servo_max_us": 2500, "dispense_angle": 119,
                       "pick_angle": 0, "dispense_move_ms": 1500}
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

    def _glide(self, name: str, angle: int, seconds: float) -> None:
        """Vrid lugnt till en vinkel på angiven tid. Farten ökar mjukt i början och minskar
        mot slutet, så att nöten inte kastas runt i hålet."""
        start = self.position[name]
        steps = max(1, round(seconds / GLIDE_STEP_S))
        if start is not None and start != angle:
            for i in range(1, steps):
                eased = (1 - math.cos(math.pi * i / steps)) / 2   # 0 → 1, mjukt i båda ändar
                self.board.pulse(self._channel(name), self._us(start + (angle - start) * eased))
                time.sleep(GLIDE_STEP_S)
        self._move(name, angle)

    def _test_dispense(self, pick: int, angle: int, move_s: float) -> None:
        """Plockskivans rörelse: till plockläget, ett litet vick som rör om nötterna så att en
        lägger sig i hålet, lugnt upp till utfallet där nöten faller ut, och lugnt tillbaka."""
        self._glide("doser", pick, move_s)  # okänt läge efter start: då går den direkt
        time.sleep(0.4)
        vick = pick + VICK_DEG
        for a, pause in ((vick, 0.15), (pick, 0.15), (vick, 0.15), (pick, 0.3)):
            self._move("doser", a)
            time.sleep(pause)
        self._glide("doser", angle, move_s)
        time.sleep(0.3)
        self._glide("doser", pick, move_s)

    def _sweep(self, name: str, seconds: float) -> None:
        """Svep ett vinkelservo fram och tillbaka en stund, sedan släpps signalen."""
        end = time.monotonic() + seconds
        i = 0
        while time.monotonic() < end:
            self._move(name, SWEEP_ANGLES[i % 2])
            i += 1
            time.sleep(SWEEP_STEP_S)
        self._release(name)

    # ---------- 360°-servo: ingen vinkel, bara fart och tid ----------

    def _spin(self, name: str, direction: str, ms: int, cmd: dict) -> None:
        """Snurra ett 360°-servo åt ett håll en viss tid. Pulsens avstånd från stilla-läget
        avgör farten. Servot stannar när signalen släpps."""
        sign = 1 if direction == "up" else -1
        if cmd["reverse"]:
            sign = -sign
        self.board.pulse(self._channel(name), cmd["neutral_us"] + sign * cmd["speed_us"])
        self.holding[name] = True
        self.position[name] = None  # ett 360°-servo vet inte var det står
        time.sleep(ms / 1000)
        self._release(name)

    def _test_dispense_turn(self, cmd: dict) -> None:
        """Plockskivans rörelse med 360°-servo: ett helt varv framåt. Fram till utfallet, ett kort
        stopp där nöten faller ut, och resten av varvet tillbaka till plockläget."""
        self._spin("doser", "up", cmd["up_ms"], cmd)
        time.sleep(0.3)  # nöten faller ut
        self._spin("doser", "up", cmd["rev_ms"] - cmd["up_ms"], cmd)

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
                elif action == "test_dispense" and cmd.get("kind") == "varv":
                    self._test_dispense_turn(cmd)
                    self.last = f"testade utmatning (helt varv: {cmd['up_ms']} ms till utfallet, {cmd['rev_ms']} ms totalt)"
                elif action == "spin":
                    self._spin(cmd["servo"], cmd["direction"], cmd["ms"], cmd)
                    self.last = f"{cmd['servo']} snurrade {'framåt' if cmd['direction'] == 'up' else 'bakåt'} {cmd['ms']} ms"
                elif action == "test_dispense":
                    # Äldre server skickar bara vinkeln: då gäller Pi:ns egna inställningar.
                    pick = cmd.get("pick", self.config["pick_angle"])
                    move_s = cmd.get("move_ms", self.config["dispense_move_ms"]) / 1000
                    self._test_dispense(pick, cmd["angle"], move_s)
                    time.sleep(RELEASE_AFTER_S)
                    self._release("doser")
                    self.last = f"testade utmatning ({pick}° → {cmd['angle']}°, {move_s:g} s)"
                elif action == "sweep":
                    self._sweep(cmd["servo"], cmd["seconds"])
                    self.last = f"{cmd['servo']} svepte {cmd['seconds']} s"
                print(f"Servo: {self.last}", flush=True)
            except Exception as e:
                # Tappad kontakt med kortet: försök ansluta på nytt vid nästa kommando.
                self.error = f"{type(e).__name__}: {e}"
                self.board = None
                print(f"Servo: fel – {self.error}", flush=True)
            finally:
                self.on_change()
