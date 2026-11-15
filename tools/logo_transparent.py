"""Gör logotypens vita bakgrund genomskinlig och beskär kanterna.

Fyller från bildens kanter, så att bara vitt som hänger ihop med kanten blir
genomskinligt. Det vita i taket ligger innanför den svarta konturen och behålls.

  python3 tools/logo_transparent.py in.webp server/static/logo.webp
"""
import sys
from collections import deque

from PIL import Image

TOL = 40  # hur nära vitt en pixel måste vara (0–255 per kanal)


def main(src: str, dst: str) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    px = im.load()
    near_white = lambda p: all(c >= 255 - TOL for c in p[:3])
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        q.extend([(0, y), (w - 1, y)])
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i] or not near_white(px[x, y]):
            continue
        seen[i] = 1
        px[x, y] = (255, 255, 255, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                q.append((nx, ny))
    box = im.getbbox()
    im = im.crop(box)
    # Halva storleken räcker för headern (visas ca 120–200 px hög) och ger mindre fil.
    im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    im.save(dst, lossless=True)
    print(dst, im.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
