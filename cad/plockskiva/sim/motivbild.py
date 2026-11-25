import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage import morphology
from shapely import affinity
from motiv import motiv
def rast(g, res=0.05, pad=1.0):
    minx, miny, maxx, maxy = g.bounds; W = int((maxx - minx + 2 * pad) / res); H = int((maxy - miny + 2 * pad) / res)
    im = Image.new('1', (W, H), 0); d = ImageDraw.Draw(im)
    for p in getattr(g, 'geoms', [g]):
        tr = lambda cs: [((x - minx + pad) / res, (maxy + pad - y) / res) for x, y in cs]
        d.polygon(tr(p.exterior.coords), fill=1)
        for h in p.interiors: d.polygon(tr(h.coords), fill=0)
    return np.array(im, bool)
path, outp = sys.argv[1], sys.argv[2]; sets = [tuple(float(v) for v in x.split(',')) for x in sys.argv[3:]]
tiles = []
for sz, ml, mg in sets:
    g, info = motiv(path, sz, ml, mg); print(sz, ml, mg, info)
    m = rast(g); r = int(round(0.2 / 0.05))
    pr = morphology.binary_opening(m, morphology.disk(r))                 # svart (nedsänkt) som en 0,4 mm dysa kan göra
    pr = ~morphology.binary_opening(~pr, morphology.disk(r))              # och vita mellanrum som överlever
    lost = m & ~pr; gained = pr & ~m
    rgb = np.full(m.shape + (3,), 235, np.uint8); rgb[pr] = (60, 40, 30); rgb[lost] = (230, 60, 40); rgb[gained] = (60, 120, 230)
    t = Image.fromarray(rgb).resize((560, int(560 * m.shape[0] / m.shape[1])), Image.LANCZOS)
    c = Image.new('RGB', (580, t.height + 60), (245, 245, 240)); c.paste(t, (10, 50)); ImageDraw.Draw(c).text((10, 10), "%.0f mm, minsta linje %.2f, mellanrum %.2f: rött = försvinner (%.0f %%)" % (sz, ml, mg, 100 * lost.sum() / max(m.sum(), 1)), fill=(20, 20, 20))
    tiles.append(c)
H = max(t.height for t in tiles); out = Image.new('RGB', (sum(t.width for t in tiles), H), (245, 245, 240)); x = 0
for t in tiles: out.paste(t, (x, 0)); x += t.width
out.save(outp)
