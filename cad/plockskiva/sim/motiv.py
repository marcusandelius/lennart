"""Hasselnötsmotivet som polygoner i mm (för nedsänkning i omrörarens blad).
motiv(bild, bredd_mm, min_linje, min_mellanrum) -> (shapely-geometri centrerad i origo, uppåt = +y, info)"""
import numpy as np
from PIL import Image
from skimage import morphology, measure
from shapely.geometry import Polygon
from shapely.ops import unary_union

def motiv(path, size_mm=22.0, min_line=0.5, min_gap=0.45, thr=128):
    im = np.asarray(Image.open(path).convert('L'), float)
    black = im < thr
    ys, xs = np.where(black); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    black = black[y0:y1 + 1, x0:x1 + 1]
    s = size_mm / max(black.shape)                      # mm per bildpunkt
    rl = max(1, int(round(min_line / 2 / s))); rg = max(1, int(round(min_gap / 2 / s)))
    if min_line > 0:
        sk = morphology.skeletonize(black)
        b2 = black | morphology.binary_dilation(sk, morphology.disk(rl))      # varje svart linje minst min_line bred
    else: b2 = black
    white = ~b2
    if min_gap > 0: white = morphology.binary_opening(white, morphology.disk(rg))   # vita mellanrum smalare än min_gap försvinner
    b3 = ~white
    b3 = morphology.remove_small_objects(b3, int(0.25 / s / s)); b3 = ~morphology.remove_small_objects(~b3, int(0.25 / s / s))
    pad = np.pad(b3, 2)
    geom = None
    for cnt in measure.find_contours(pad.astype(float), 0.5):
        if len(cnt) < 4: continue
        p = Polygon([((c[1] - 2) * s, -(c[0] - 2) * s) for c in cnt]).buffer(0)
        if p.is_empty: continue
        geom = p if geom is None else geom.symmetric_difference(p)
    geom = geom.simplify(0.02).buffer(0)
    cx, cy = (geom.bounds[0] + geom.bounds[2]) / 2, (geom.bounds[1] + geom.bounds[3]) / 2
    from shapely import affinity
    geom = affinity.translate(geom, -cx, -cy)
    # kontroll: smalaste svarta och vita partier
    dist = lambda m: np.array(__import__('scipy.ndimage', fromlist=['x']).distance_transform_edt(m))
    def minw(m):
        skel = morphology.skeletonize(m); d = dist(m)[skel]
        return 2 * np.percentile(d, 1) * s if len(d) else 0
    info = dict(skala=s, storlek=(round(geom.bounds[2] - geom.bounds[0], 1), round(geom.bounds[3] - geom.bounds[1], 1)),
                yta=round(geom.area, 1), smalaste_linje=round(minw(b3), 2), smalaste_mellanrum=round(minw(~b3 & np.pad(np.ones((b3.shape[0]-4, b3.shape[1]-4), bool), 2)), 2))
    return geom, info

if __name__ == "__main__":
    import sys
    g, info = motiv(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 22.0)
    print(info)
