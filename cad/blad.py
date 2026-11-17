"""
Blad för blomlådornas växtinsatser.

Ett blad är ett smalt, spetsigt blad (lansettformat) som växer upp från jorden och böjer sig utåt.
Det ligger i ett lodrätt plan (azimut + lodlinje) och är THICK mm tjockt vid foten och THICK_TIP i spetsen, så att bladets breda sida
syns från sidan. Lutningen från lodlinjen går från 8 grader vid foten till högst 42 grader i spetsen,
så att det kan skrivas ut stående utan stöd.
"""
import numpy as np
import trimesh

THICK = 1.2       # vid foten
THICK_TIP = 0.8   # i spetsen (två linjer med 0,4-munstycke)


def leaf(base, azimuth_deg, length, width, theta0=8.0, theta1=42.0, n=14):
    az = np.radians(azimuth_deg)
    A = np.array([np.cos(az), np.sin(az), 0.0])          # riktning bladet lutar åt
    Z = np.array([0.0, 0.0, 1.0])
    B = np.cross(Z, A)                                    # tjockleksriktning (vågrät)
    s = np.linspace(0, 1, n + 1)
    th = np.radians(theta0 + (theta1 - theta0) * s ** 1.6)
    ds = length / n
    pts = [np.array(base, float)]
    for i in range(n):
        t = 0.5 * (th[i] + th[i + 1])
        pts.append(pts[-1] + ds * (np.sin(t) * A + np.cos(t) * Z))
    # bredd: smal fot, bredast vid ca 35 %, spetsig topp
    w = width * np.clip((s ** 0.55) * ((1 - s) ** 0.85) / (0.35 ** 0.55 * 0.65 ** 0.85), 0, 1)
    w = np.maximum(w, np.where(s < 0.5, 1.4, 0.35))
    secs = []
    for i in range(n + 1):
        T = np.sin(th[i]) * A + np.cos(th[i]) * Z
        W = np.cross(B, T); W /= np.linalg.norm(W)
        c = pts[i]
        secs.append([c + sw * w[i] / 2 * W + sb * (THICK + (THICK_TIP - THICK) * s[i]) / 2 * B for sw in (-1, 1) for sb in (-1, 1)])
    # loft: fyra hörn per tvärsnitt, sidor mellan tvärsnitten och lock i båda ändar -> en tät yta
    order = [0, 1, 3, 2]                                   # runt tvärsnittet
    V = np.array([secs[i][k] for i in range(n + 1) for k in order])
    F = []
    for i in range(n):
        for k in range(4):
            a, b = i * 4 + k, i * 4 + (k + 1) % 4
            c, d = a + 4, b + 4
            F += [[a, b, d], [a, d, c]]
    F += [[0, 2, 1], [0, 3, 2]]
    e = n * 4
    F += [[e, e + 1, e + 2], [e, e + 2, e + 3]]
    m = trimesh.Trimesh(V, np.array(F), process=True)
    trimesh.repair.fix_normals(m)
    if m.volume < 0: m.invert()
    return m
