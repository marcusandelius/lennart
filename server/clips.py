"""Klipp som Pi:n spelat in vid rörelse. Sparas i DATA_DIR/clips och syns bara i adminvyn.

Varje klipp består av tre filer med samma id:
  <id>.mp4   videon (H.264)
  <id>.jpg   en miniatyrbild från ögonblicket med mest rörelse
  <id>.json  uppgifter om klippet och hur det har märkts

Klippen är underlag för att testa och träna bildigenkänningen. De kan visa
personer, så de visas aldrig publikt och läggs aldrig i repot.
"""

import csv
import io
import json
import os
import re
import threading
import time
from pathlib import Path

# Märkningar som admin kan sätta. Nyckeln sparas, texten visas.
LABELS = {
    "ekorre": "Ekorre",
    "skata": "Skata",
    "annan_fagel": "Annan fågel",
    "annat_djur": "Annat djur",
    "manniska": "Människa",
    "tomt": "Tomt (falsklarm)",
    "osaker": "Osäker",
}

ID_PATTERN = re.compile(r"^\d{8}-\d{6}-[0-9a-f]{4}$")
MAX_CLIP_BYTES = 95 * 1024 * 1024    # under Cloudflares gräns på 100 MB per anrop
MAX_THUMB_BYTES = 512 * 1024
META_FIELDS = {"started": str, "duration_s": (int, float), "frames": int, "fps": int,
               "width": int, "height": int, "peak_motion": (int, float), "brightness": (int, float)}


class ClipStore:
    def __init__(self, data_dir: str) -> None:
        self.dir = Path(data_dir) / "clips"
        self.lock = threading.Lock()
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            for leftover in self.dir.glob("*.part"):   # uppladdningar som avbröts vid en omstart
                leftover.unlink()
        except OSError:
            pass

    @staticmethod
    def valid_id(clip_id: str) -> bool:
        return bool(ID_PATTERN.match(clip_id))

    def path(self, clip_id: str, suffix: str) -> Path:
        if not self.valid_id(clip_id):
            raise ValueError("Ogiltigt id")
        return self.dir / f"{clip_id}{suffix}"

    def summary(self) -> dict:
        return {"count": len(list(self.dir.glob("*.json"))), "bytes": self.total_bytes()}

    def total_bytes(self) -> int:
        return sum(f.stat().st_size for f in self.dir.glob("*") if f.is_file())

    def save(self, clip_id: str, raw_meta: dict, body, length: int) -> str:
        """Spara ett uppladdat klipp. body läses i bitar, så att stora filer inte hamnar i minnet.

        Pi:n väljer id:t (tiden när klippet började plus fyra slumpade tecken). Om samma
        klipp laddas upp igen, till exempel när svaret inte nådde fram, skrivs det över och
        en märkning som redan gjorts behålls.
        """
        meta = {k: raw_meta[k] for k, kind in META_FIELDS.items()
                if isinstance(raw_meta.get(k), kind) and not isinstance(raw_meta.get(k), bool)}
        tmp = self.path(clip_id, ".mp4.part")
        remaining = length
        with open(tmp, "wb") as f:
            while remaining > 0:
                chunk = body.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                f.write(chunk)
                remaining -= len(chunk)
        if remaining:
            tmp.unlink(missing_ok=True)
            raise ValueError("Uppladdningen avbröts")
        os.replace(tmp, self.path(clip_id, ".mp4"))
        with self.lock:
            try:
                old = self.meta(clip_id)
            except (OSError, ValueError):
                old = {}
            meta.update({"id": clip_id, "size": length, "label": old.get("label"),
                         "labeled": old.get("labeled"),
                         "uploaded": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
            self._write_meta(clip_id, meta)
        return clip_id

    def save_thumb(self, clip_id: str, jpeg: bytes) -> None:
        if not self.path(clip_id, ".json").exists():
            raise KeyError(clip_id)
        self.path(clip_id, ".jpg").write_bytes(jpeg)

    def _write_meta(self, clip_id: str, meta: dict) -> None:
        tmp = self.path(clip_id, ".json.tmp")
        tmp.write_text(json.dumps(meta, ensure_ascii=False))
        os.replace(tmp, self.path(clip_id, ".json"))

    def meta(self, clip_id: str) -> dict:
        return json.loads(self.path(clip_id, ".json").read_text())

    def list(self) -> list[dict]:
        clips = []
        for f in sorted(self.dir.glob("*.json"), reverse=True):
            try:
                clips.append(json.loads(f.read_text()))
            except (OSError, ValueError):
                continue
        return clips

    def set_label(self, clip_id: str, label: str | None) -> dict:
        if label is not None and label not in LABELS:
            raise ValueError("Okänd märkning")
        with self.lock:
            meta = self.meta(clip_id)
            meta["label"] = label
            meta["labeled"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if label else None
            self._write_meta(clip_id, meta)
        return meta

    def delete(self, clip_id: str) -> None:
        for suffix in (".mp4", ".jpg", ".json"):
            self.path(clip_id, suffix).unlink(missing_ok=True)

    def csv(self) -> bytes:
        """Alla klipp med märkning, för att träna och utvärdera modeller."""
        out = io.StringIO()
        fields = ["id", "started", "duration_s", "fps", "width", "height", "peak_motion", "brightness", "label", "size"]
        writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for clip in sorted(self.list(), key=lambda c: c["id"]):
            writer.writerow(clip)
        return out.getvalue().encode("utf-8")
