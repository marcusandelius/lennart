"""Objektdetektering med YOLOv8n tränad på Open Images V7 (601 klasser, bl.a. ekorre).

Modellen körs lokalt på Pi:ns processor med ONNX Runtime. PyTorch och Ultralytics
behövs inte på Pi:n: modellen exporterades till ONNX i förväg (se docs/igenkanning.md).

Så här går det till:
1. **Förbehandling:** bilden skalas ner så att den ryms i 640 × 640 med bibehållna
   proportioner, och resten fylls med grått ("letterbox"), precis som vid träningen.
2. **Modellen** ger 8 400 förslag på rutor, var och en med en sannolikhet per klass.
3. **Efterbearbetning:** förslag under tröskeln kastas, och överlappande rutor för
   samma klass slås ihop (NMS), så att varje djur bara får en ruta.

Klasserna grupperas sedan i det som spelar roll för stationen: ekorre, fågel,
människa och annat djur.

Testa på inspelade klipp från kommandoraden (kräver ffmpeg):
    python3 detect.py                    # alla klipp i ~/lennart-data/clips
    python3 detect.py --limit 20         # de 20 senaste
    python3 detect.py klipp.mp4 bild.jpg # enskilda filer
"""

import argparse
import ast
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

MODEL_PATH = Path(os.environ.get("LENNART_MODEL", Path(__file__).parent / "models" / "yolov8n-oiv7.onnx"))
INPUT_SIZE = 640
CONF_THRESHOLD = 0.25   # lägsta sannolikhet för att en ruta ska räknas
IOU_THRESHOLD = 0.45    # så mycket två rutor får överlappa innan den svagare kastas

# Open Images-klasser grupperade efter vad stationen behöver veta.
GROUPS = {
    "ekorre": {"Squirrel"},
    "fågel": {"Bird", "Magpie", "Sparrow", "Raven", "Woodpecker", "Owl", "Blue jay", "Canary", "Duck",
              "Goose", "Eagle", "Falcon", "Parrot", "Swan", "Penguin", "Ostrich", "Turkey", "Chicken"},
    "människa": {"Person", "Man", "Woman", "Boy", "Girl", "Human face", "Human body", "Human head",
                 "Human hand", "Human arm", "Human leg", "Human foot", "Human eye", "Human ear",
                 "Human nose", "Human mouth", "Human hair", "Human beard"},
    "annat djur": {"Cat", "Dog", "Hedgehog", "Mouse", "Hamster", "Raccoon", "Fox", "Rabbit", "Skunk",
                   "Otter", "Animal", "Mammal", "Deer", "Horse", "Bat (Animal)", "Frog", "Lizard",
                   "Snake", "Tortoise", "Insect", "Butterfly", "Moths and butterflies", "Bee", "Spider"},
}


def group_of(name: str) -> str | None:
    for group, names in GROUPS.items():
        if name in names:
            return group
    return None


class Detector:
    def __init__(self, model_path: Path = MODEL_PATH, threads: int | None = None) -> None:
        import onnxruntime as ort

        options = ort.SessionOptions()
        if threads:
            options.intra_op_num_threads = threads
        self.session = ort.InferenceSession(str(model_path), options, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        # Ultralytics sparar klassnamnen i modellfilens metadata, som en Python-ordbok i text.
        meta = self.session.get_modelmeta().custom_metadata_map
        self.names = {int(k): v for k, v in ast.literal_eval(meta["names"]).items()}

    def _letterbox(self, rgb: np.ndarray) -> tuple[np.ndarray, float, int, int]:
        h, w = rgb.shape[:2]
        scale = min(INPUT_SIZE / h, INPUT_SIZE / w)
        nh, nw = round(h * scale), round(w * scale)
        resized = np.asarray(Image.fromarray(rgb).resize((nw, nh), Image.BILINEAR))
        canvas = np.full((INPUT_SIZE, INPUT_SIZE, 3), 114, np.uint8)  # grått, som vid träningen
        top, left = (INPUT_SIZE - nh) // 2, (INPUT_SIZE - nw) // 2
        canvas[top:top + nh, left:left + nw] = resized
        return canvas, scale, left, top

    def detect(self, rgb: np.ndarray, conf: float = CONF_THRESHOLD) -> list[dict]:
        """Hitta objekt i en RGB-bild (höjd × bredd × 3). Rutorna anges i bildens egna bildpunkter."""
        canvas, scale, left, top = self._letterbox(rgb)
        x = canvas.transpose(2, 0, 1)[None].astype(np.float32) / 255.0
        out = self.session.run(None, {self.input_name: x})[0][0]   # (4 + klasser, 8400)
        boxes, scores = out[:4].T, out[4:].T                        # (8400, 4), (8400, klasser)
        cls = scores.argmax(1)
        best = scores[np.arange(len(cls)), cls]
        keep = best >= conf
        boxes, cls, best = boxes[keep], cls[keep], best[keep]
        if not len(best):
            return []
        # Från mittpunkt, bredd och höjd i 640-bilden till hörn i originalbilden.
        cx, cy, bw, bh = boxes.T
        h, w = rgb.shape[:2]
        x1 = np.clip((cx - bw / 2 - left) / scale, 0, w)
        y1 = np.clip((cy - bh / 2 - top) / scale, 0, h)
        x2 = np.clip((cx + bw / 2 - left) / scale, 0, w)
        y2 = np.clip((cy + bh / 2 - top) / scale, 0, h)
        corners = np.stack([x1, y1, x2, y2], 1)
        result = []
        for c in np.unique(cls):
            idx = np.where(cls == c)[0]
            for i in _nms(corners[idx], best[idx], IOU_THRESHOLD):
                j = idx[i]
                name = self.names[int(c)]
                result.append({"class": name, "group": group_of(name), "score": round(float(best[j]), 3),
                               "box": [round(float(v)) for v in corners[j]]})
        return sorted(result, key=lambda d: -d["score"])


def _nms(boxes: np.ndarray, scores: np.ndarray, iou: float) -> list[int]:
    """Behåll den säkraste rutan och kasta de som överlappar den för mycket. Upprepa."""
    order = scores.argsort()[::-1]
    keep = []
    area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    while len(order):
        i = order[0]
        keep.append(int(i))
        xx1 = np.maximum(boxes[i, 0], boxes[order[1:], 0])
        yy1 = np.maximum(boxes[i, 1], boxes[order[1:], 1])
        xx2 = np.minimum(boxes[i, 2], boxes[order[1:], 2])
        yy2 = np.minimum(boxes[i, 3], boxes[order[1:], 3])
        inter = np.clip(xx2 - xx1, 0, None) * np.clip(yy2 - yy1, 0, None)
        overlap = inter / (area[i] + area[order[1:]] - inter + 1e-9)
        order = order[1:][overlap < iou]
    return keep


# ---------- test på inspelade klipp ----------

def video_frames(path: Path, every_s: float):
    """Läs bilder ur en video med ffmpeg, en bild per every_s sekunder."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height", "-of", "csv=p=0", str(path)],
                           capture_output=True, text=True, check=True)
    w, h = map(int, probe.stdout.strip().split(",")[:2])
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps=1/{every_s}",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    size = w * h * 3
    try:
        while True:
            buf = proc.stdout.read(size)
            if len(buf) < size:
                break
            yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    finally:
        proc.stdout.close()
        proc.wait()


def main() -> int:
    parser = argparse.ArgumentParser(description="Testa objektdetekteringen på klipp eller bilder.")
    parser.add_argument("files", nargs="*", type=Path, help="MP4- eller bildfiler. Standard: klippen på Pi:n.")
    parser.add_argument("--limit", type=int, default=0, help="bara de N senaste klippen")
    parser.add_argument("--every", type=float, default=0.5, help="sekunder mellan bilderna som testas (standard 0,5)")
    parser.add_argument("--csv", type=Path, default=Path.home() / "lennart-data" / "detektering-test.csv")
    args = parser.parse_args()

    files = args.files or sorted((Path.home() / "lennart-data" / "clips").glob("*.mp4"))
    if args.limit:
        files = files[-args.limit:]
    if not files:
        print("Inga filer att testa.")
        return 1

    detector = Detector()
    print(f"Modell: {MODEL_PATH.name}, {len(detector.names)} klasser. Testar {len(files)} filer.\n")
    rows, times = [], []
    for path in files:
        frames = [np.asarray(Image.open(path).convert("RGB"))] if path.suffix.lower() in (".jpg", ".jpeg", ".png") \
            else video_frames(path, args.every)
        best: dict[str, float] = {}          # högsta sannolikhet per grupp i hela klippet
        top: dict[str, float] = {}           # högsta sannolikhet per klass
        n = 0
        for rgb in frames:
            started = time.perf_counter()
            found = detector.detect(rgb)
            times.append((time.perf_counter() - started) * 1000)
            n += 1
            for d in found:
                if d["group"]:
                    best[d["group"]] = max(best.get(d["group"], 0), d["score"])
                top[d["class"]] = max(top.get(d["class"], 0), d["score"])
        classes = ", ".join(f"{c} {s:.2f}" for c, s in sorted(top.items(), key=lambda kv: -kv[1])[:4]) or "inget"
        print(f"{path.stem}: {n} bilder · ekorre {best.get('ekorre', 0):.2f} · fågel {best.get('fågel', 0):.2f}"
              f" · människa {best.get('människa', 0):.2f} · annat djur {best.get('annat djur', 0):.2f} · {classes}")
        rows.append({"klipp": path.stem, "bilder": n, **{g: round(best.get(g, 0), 3) for g in GROUPS},
                     "klasser": classes})

    if times:
        t = np.array(times)
        print(f"\nTid per bild: median {np.median(t):.0f} ms, snabbast {t.min():.0f} ms, långsammast {t.max():.0f} ms"
              f" ({len(t)} bilder)")
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Resultatet sparades i {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
