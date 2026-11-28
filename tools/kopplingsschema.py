# Genererar docs/kopplingsschema.html (A4 liggande) med färgkodade kopplingar. PDF: skriv ut sidan, eller rendera med Chromium.
C = {'gul':'#e8c51a','grå':'#8a8a8a','grön':'#2f9a47','orange':'#e8771a','blå':'#2a63c7','röd':'#c4291c',
     'vit':'#ffffff','lila':'#8a4bc2','svart':'#1d1d1d','brun':'#7a4b2a'}
LIGHT = {'gul','vit'}
INK, INK2, LINE, BG, PAPER, ACC = '#1f1918', '#5e5552', '#cfc6c2', '#f3efed', '#ffffff', '#9a2b1e'
o = []
def t(x, y, s, size=12, w=400, fill=INK, anchor='start', family='Inter'):
    fam = "'IBM Plex Mono',monospace" if family == 'mono' else "'IBM Plex Sans',Arial,sans-serif"
    o.append(f'<text x="{x}" y="{y}" style="font:{w} {size}px {fam};fill:{fill}" text-anchor="{anchor}">{s}</text>')
def pin(x, y, n, col, ring=None, r=11):
    stroke = ring or INK
    sw = 3 if ring else 1.2
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:{C[col]};stroke:{stroke};stroke-width:{sw}"/>')
    t(x, y + 3.5, n, 9, 600, '#1d1d1d' if col in LIGHT else '#ffffff', 'middle', 'mono')
def dot(x, y, r=4):
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:{LINE}"/>')
def rect(x, y, w, h, fill=BG, stroke=INK2, rx=6, sw=1.2, dash=None):
    d = f';stroke-dasharray:{dash}' if dash else ''
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="fill:{fill};stroke:{stroke};stroke-width:{sw}{d}"/>')
def line(d, col, w=3, dash=None):
    ds = f';stroke-dasharray:{dash}' if dash else ''
    o.append(f'<path d="{d}" style="fill:none;stroke:{col};stroke-width:{w};stroke-linecap:round{ds}"/>')

W, H = 1123, 794
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="297mm" height="210mm">')
o.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
o.append('<defs>' + ''.join(
    f'<pattern id="st-{k}" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#ffffff"/><rect width="4" height="8" fill="{v}"/></pattern>'
    for k, v in (('o', C['orange']), ('g', C['grön']), ('b', C['blå']), ('br', C['brun']))) + '</defs>')

# Rubrik
t(30, 36, 'Kopplingsschema · Lennarts matstation', 22, 700)
t(30, 54, 'Skriv ut i färg. Stiften räknas med stiftlisten mot överkanten och USB-portarna åt höger. Uppdaterad 2026-11-28.', 11, 400, INK2)

# ---------- Rad 1: Pi:ns stiftlist ----------
t(30, 84, 'Raspberry Pi 5 · stiftlisten (förstorad)', 14, 700)
screen = {1:('3V3','röd'),6:('GND','grå'),12:('BL','lila'),13:('RST','vit'),19:('DIN','grön'),22:('DC','blå'),23:('CLK','gul'),24:('CS','orange')}
i2c = {3:('SDA','orange'),5:('SCL','brun'),9:('GND','svart'),17:('3V3','röd')}
x0, dx, ytop, ybot = 54, 28, 140, 170
rect(36, 122, 20*dx + 8, 66, BG, INK2, 6)
t(36, 104, 'kortets kant ↑', 10, 400, INK2)
for n in range(1, 41):
    c = (n + 1) // 2; x = x0 + (c - 1) * dx; y = ybot if n % 2 else ytop
    if n in screen:
        sig, col = screen[n]; pin(x, y, n, col)
    elif n in i2c:
        sig, col = i2c[n]; pin(x, y, n, col, ring='#2a63c7')
    else:
        dot(x, y); continue
    if n % 2 == 0:
        t(x, 104, sig, 10, 700, INK, 'middle', 'mono'); t(x, 116, col, 9, 400, INK2, 'middle', 'mono')
    else:
        t(x, 200, sig, 10, 700, INK, 'middle', 'mono'); t(x, 212, col, 9, 400, INK2, 'middle', 'mono')
t(36, 236, 'stift 1 = längst till vänster i undre raden', 10, 400, INK2)
t(36 + 20*dx + 8, 236, 'kolumn 12: gul (23) under, orange (24) över', 10, 400, INK2, 'end')

# Pi-översikt
px, py = 640, 96
rect(px, py, 214, 142, '#2f6b45', INK, 8)
rect(px + 10, py + 4, 130, 14, '#1d1d1d', ACC, 2, 2)
t(px + 75, py + 32, 'stiftlisten', 10, 600, '#ffffff', 'middle')
for yy, hh in ((py + 12, 34), (py + 52, 34), (py + 94, 40)):
    rect(px + 200, yy, 22, hh, '#b9b9b9', INK, 2)
rect(px + 12, py + 128, 20, 14, '#b9b9b9', INK, 2)
t(px + 22, py + 158, 'USB-C: ström', 10, 600, INK, 'middle')
rect(px + 120, py + 118, 44, 9, '#e9e2da', INK, 2); t(px + 142, py + 112, 'kamera', 9, 400, '#ffffff', 'middle')
t(px + 100, py + 72, 'Raspberry Pi 5', 12, 700, '#ffffff', 'middle')
t(px + 100, py + 88, 'ovanifrån, portarna åt höger', 9, 400, '#e6efe8', 'middle')
# Förklaring
lx, ly = 880, 88
t(lx, ly, 'Skärmen (via uttaget SKÄRM)', 11, 700)
rows = [('gul','CLK','23','14'),('grå','GND','6','13'),('grön','DIN','19','15'),('orange','CS','24','12'),('blå','DC','22','11'),('röd','3,3 V','1','39'),('vit','RST','13','16'),('lila','BL','12','17')]
t(lx + 150, ly + 16, 'Pi', 9, 600, INK2, 'end', 'mono'); t(lx + 205, ly + 16, 'skärm', 9, 600, INK2, 'end', 'mono')
for i, (col, sig, p, d) in enumerate(rows):
    y = ly + 30 + i * 13
    o.append(f'<circle cx="{lx+6}" cy="{y-4}" r="5" style="fill:{C[col]};stroke:{INK};stroke-width:1"/>')
    t(lx + 16, y, f'{col} {sig}', 10, 400, INK, 'start', 'mono'); t(lx + 150, y, p, 10, 600, INK, 'end', 'mono'); t(lx + 205, y, d, 10, 600, INK, 'end', 'mono')
y = ly + 30 + 8 * 13 + 8
t(lx, y, 'Servokortet (I2C)', 11, 700)
for i, (col, sig, p) in enumerate((('röd','VCC 3,3 V','17'),('svart','GND','9'),('orange','SDA','3'),('brun','SCL','5'))):
    yy = y + 15 + i * 13
    o.append(f'<circle cx="{lx+6}" cy="{yy-4}" r="5" style="fill:{C[col]};stroke:#2a63c7;stroke-width:2"/>')
    t(lx + 16, yy, f'{col} {sig}', 10, 400, INK, 'start', 'mono'); t(lx + 150, yy, p, 10, 600, INK, 'end', 'mono')

# ---------- Rad 2: skärmkortet och uttagen ----------
o.append('<g transform="translate(0,14)">')
t(30, 300, 'Skärmkortet · baksidan, USB-änden åt vänster', 14, 700)
dpins = {11:('DC','blå'),12:('CS','orange'),13:('GND','grå'),14:('CLK','gul'),15:('DIN','grön'),16:('RST','vit'),17:('BL','lila'),39:('VSYS','röd')}
bx0, bdx, btop, bbot = 66, 26, 352, 382
rect(44, 330, 20*bdx + 6, 74, BG, INK2, 8)
rect(22, 352, 24, 30, PAPER, INK2, 3); t(34, 371, 'USB', 8, 600, INK2, 'middle', 'mono')
for n in range(1, 41):
    if n <= 20: c, y = n, bbot
    else: c, y = 41 - n, btop
    x = bx0 + (c - 1) * bdx
    if n in dpins:
        sig, col = dpins[n]; pin(x, y, n, col, r=10)
        if y == btop:
            t(x, 322, 'VSYS · röd', 10, 700, INK, 'start', 'mono')
        else:
            t(x, 420, sig, 10, 700, INK, 'middle', 'mono'); t(x, 432, col, 9, 400, INK2, 'middle', 'mono')
    else:
        dot(x, y, 3.5)
t(44, 452, 'stift 1 längst till vänster i undre raden · 11–17 i följd · 39 = andra från vänster i övre raden', 10, 400, INK2)

kx, ky = 640, 300
t(kx, ky, 'Keystone-uttagen · båda likadana, färgkod B', 14, 700)
slots = [('url(#st-o)','vit-orange','gul','CLK'),(C['orange'],'orange','grå','GND'),('url(#st-g)','vit-grön','grön','DIN'),(C['blå'],'blå','orange','CS'),
         ('url(#st-b)','vit-blå','blå','DC'),(C['grön'],'grön','röd','3V3'),('url(#st-br)','vit-brun','vit','RST'),(C['brun'],'brun','lila','BL')]
for i, (fill, name, jcol, sig) in enumerate(slots):
    x = kx + 4 + i * 56
    t(x + 22, ky + 26, str(i + 1), 11, 700, INK, 'middle', 'mono')
    o.append(f'<rect x="{x}" y="{ky+34}" width="44" height="34" rx="4" style="fill:{fill};stroke:{INK2};stroke-width:1"/>')
    line(f'M{x+22} {ky+68} V{ky+86}', INK2, 1.2, '3 3')
    o.append(f'<circle cx="{x+22}" cy="{ky+96}" r="9" style="fill:{C[jcol]};stroke:{INK};stroke-width:1.2"/>')
    t(x + 22, ky + 122, sig, 10, 700, INK, 'middle', 'mono'); t(x + 22, ky + 134, jcol, 9, 400, INK2, 'middle', 'mono')
t(kx, ky + 156, 'Spåret: Cat6-ledare i spårets färg. Pricken: kopplingskabeln som är lödd på den ledaren.', 10, 400, INK2)

# ---------- Rad 3: servokortet ----------
t(30, 494, 'Servokortet PCA9685', 14, 700)
rect(40, 508, 480, 214, '#1e4f8a', INK, 8)
# sexpolig stiftrad
hdr = [('GND','svart'),('OE',None),('SCL','brun'),('SDA','orange'),('VCC','röd'),('V+',None)]
for i, (sig, col) in enumerate(hdr):
    y = 534 + i * 24
    if col: pin(64, y, '', col, ring='#2a63c7', r=9)
    else: o.append(f'<circle cx="64" cy="{y}" r="5" style="fill:#c9c9c9"/>')
    t(82, y + 4, sig + ('' if col else '  (kopplas inte)'), 10, 700 if col else 400, '#ffffff', 'start', 'mono')
t(52, 690, 'ordningen kan skilja,', 9, 400, '#dbe6f5'); t(52, 702, 'läs märkningen [verifiera]', 9, 400, '#dbe6f5')
# skruvplint
rect(250, 512, 80, 24, '#2fa34a', INK, 3)
t(270, 529, 'V+', 10, 700, '#ffffff', 'middle', 'mono'); t(310, 529, 'GND', 10, 700, '#ffffff', 'middle', 'mono')
o.append(f'<rect x="340" y="544" width="16" height="26" rx="5" style="fill:#2a63c7;stroke:{INK}"/>')
t(362, 556, '1000 µF', 10, 700, '#ffffff', 'start', 'mono'); t(362, 569, 'långt ben i V+', 9, 400, '#dbe6f5', 'start')
# servostift
sx0, sdx = 196, 20
for name, y in (('PWM', 616), ('V+', 640), ('GND', 664)):
    t(186, y + 4, name, 9, 700, '#ffffff', 'end', 'mono')
    for c in range(16): dot(sx0 + c * sdx, y, 3.2)
for c in range(16): t(sx0 + c * sdx, 686, str(c), 8, 400, '#dbe6f5', 'middle', 'mono')
for c, lab in ((0, 'doseraren'), (1, 'luckan')):
    x = sx0 + c * sdx
    o.append(f'<rect x="{x-8}" y="604" width="16" height="72" rx="3" style="fill:#111;opacity:.85"/>')
    for col, y in (('orange', 616), ('röd', 640), ('brun', 664)):
        o.append(f'<circle cx="{x}" cy="{y}" r="5" style="fill:{C[col]}"/>')
t(196, 708, 'kanal 0 = doseraren · kanal 1 = luckan · brun mot GND, orange/gul mot PWM', 9, 600, '#ffffff', 'start')

# ---------- Rad 3: strömmen ----------
gx = 600
t(gx, 494, 'Strömmen', 14, 700)
def box(x, y, w, h, title, sub, hot=False):
    rect(x, y, w, h, PAPER, ACC if hot else INK, 6, 2.2 if hot else 1.3)
    t(x + 10, y + 19, title, 11, 700); t(x + 10, y + 34, sub, 9, 400, INK2)
box(600, 512, 110, 42, 'Nätadapter', '12 V 3 A')
box(740, 512, 100, 42, 'DC-jack', '+ och − i plinten')
line('M710 533 H740', C['röd'], 3)
box(880, 512, 200, 42, 'DC/DC 5 A (EKM006)', 'VSEL bryggad = 5 V · EN, SS fria', True)
box(880, 600, 200, 42, 'Raspberry Pi 5', 'klippt USB-C: röd +, svart −')
box(880, 680, 200, 42, 'DC/DC 3 A', '8–23 V in, 5 V ut till servokortet')
line('M840 524 H880', C['röd'], 3); line('M858 540 V701 H880', C['röd'], 3)
t(756, 590, 'båda omvandlarna', 9, 400, INK2); t(756, 601, 'i samma plint', 9, 400, INK2)
line('M980 554 V600', '#d08a00', 3); t(988, 582, 'USB-C', 9, 700, INK2)
# servoströmmen från 3 A-omvandlaren till servokortets skruvplint
line('M270 512 V500 H556 V732 H990 V722', C['röd'], 3)
line('M310 512 V506 H548 V740 H1010 V722', C['svart'], 3)
t(566, 640, 'röd → V+', 9, 700, INK2); t(566, 652, 'svart → GND', 9, 700, INK2)
t(1020, 738, '5 V ut', 9, 700, INK2)
t(600, 762, 'All ström av innan du kopplar. Mät 5 V innan Pi:n ansluts.', 10, 700, ACC)
o.append('</g>')
# Sidfot
t(30, 780, 'Lennarts matstation · docs/kopplingsschema.html · uppgifter märkta [verifiera] är inte kontrollerade mot kortens märkning', 9, 400, INK2)
o.append('</svg>')
svg = '\n'.join(o)
html = f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><title>Kopplingsschema Lennart</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>@page {{ size: A4 landscape; margin: 0 }} html,body {{ margin:0; background:#fff }} svg {{ display:block; width:297mm; height:210mm }}</style>
</head><body>
{svg}
</body></html>'''
open('/home/user/lennart/docs/kopplingsschema.html', 'w').write(html)
open('/tmp/claude-0/-home-user-lennart/837f8152-c06c-5777-a825-ec5d70639f8c/scratchpad/kopplingsschema.svg', 'w').write(svg)
