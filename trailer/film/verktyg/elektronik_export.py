# Sparar elektroniken och de andra inköpta sakerna ur akt_inkop.py som en egen .blend, så att öppningen (0.4) kan lägga ut samma generiska modeller bland husets delar.
# Kör:  blender -b -P verktyg/elektronik_export.py
# Ut: film/elektronik.blend. En tom (empty) per sak, med origo i sakens mitt och z = 0 på underlaget, i liggande läge.
import bpy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE); UT = os.path.join(FILM, 'elektronik.blend')
KALLA = os.path.join(FILM, 'akt_inkop.py'); src = open(KALLA, encoding='utf-8').read()
src = src[:src.index('# ---------- konturer')]                     # allt fram till konturerna: material, modellerna och uppställningen
tmp = os.path.join(os.environ.get('TEMP', '/tmp'), 'lennart_elektronik_tmp')
sys.argv = [sys.argv[0], '--', tmp, '640', '1']
g = {'__file__': KALLA, '__name__': '__main__'}; exec(compile(src, KALLA, 'exec'), g)
# nya exemplar av varje sak, i origo (namn: sakens nyckel i öppningen)
SAKER = [('pi', g['computer']), ('kameramodul', g['camera_module']), ('skarmmodul', lambda l: g['screen'](l)[0]), ('servo_stor', g['servo']), ('servo_liten', g['servo']),
         ('kabelrulle', g['power']), ('ljusring', g['ljusring']), ('kamerakabel', g['kamerakabel']), ('kondensatorer', g['kondensatorer']), ('kylare', g['kylare']),
         ('omvandlare1', lambda l: g['omvandlare'](l, (0.012, 0.16, 0.07))), ('omvandlare2', lambda l: g['omvandlare'](l, (0.02, 0.05, 0.3))), ('dckontakt', g['dckontakt']),
         ('servotestare', g['servotestare']), ('kabelgenomforingar_e', g['kabelgenomforingar']), ('superlim', g['superlim']), ('silikon', g['silikon'])]
ut = set()
for namn, f in SAKER:
    e = f((0, 0, 0)); e.name = 'E_' + namn
    if namn == 'servo_stor': e.scale = (1.75, 1.75, 1.75)
    for o in [e] + list(e.children_recursive): ut.add(o); o.hide_render = False
for i in range(6): e = g['screw']((0, 0, 0)); e.name = 'E_skruv%d' % i; ut.update([e] + list(e.children_recursive))
bpy.data.libraries.write(UT, ut, fake_user=True, compress=True)
print('SPARAD', UT, len(ut), 'objekt', flush=True)
