# Projekt Lennart - del 6: monteringen. Sprangskiss -> alla 48 delar hittar hem i byggordning -> fardig stuga. 22 s, en kamerabana.
# Kor:  blender -b -P akt_montering.py -- <ut-mapp (absolut)> <bredd> <samples> [tider i sekunder ...]
import bpy, sys, os, math, json
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, SAMPLES, TIMES = os.path.abspath(a[0]), int(a[1]), int(a[2]), [float(x) for x in a[3:]]
os.makedirs(OUT, exist_ok=True); FPS, END = 25, 22.0

bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = 'CYCLES'; pr = bpy.context.preferences.addons['cycles'].preferences; sc.cycles.device = 'CPU'
for kind in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
    try:
        pr.compute_device_type = kind; pr.get_devices(); ds = [d for d in pr.devices if d.type == kind]
        if ds:
            for d in pr.devices: d.use = d.type == kind
            sc.cycles.device = 'GPU'; break
    except Exception: pass
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6; sc.render.use_persistent_data = True
sc.render.resolution_x = WIDTH; sc.render.resolution_y = WIDTH * 9 // 16; sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 95
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception as e: print('look', e)
MASK = os.environ.get('LENNART_MASK') == '1'   # maskläge: bara husets alfa (genomskinlig bakgrund, PNG), för att kunna lägga byggklippen bakom huset (verktyg/byggklipp_6.py)
if MASK: sc.render.film_transparent = True; sc.cycles.use_denoising = False; sc.cycles.max_bounces = 1; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; wn = sc.world.node_tree; bgn = wn.nodes['Background']
tc = wn.nodes.new('ShaderNodeTexCoord'); sub = wn.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.46, 0)
s2 = wn.nodes.new('ShaderNodeVectorMath'); s2.operation = 'MULTIPLY'; s2.inputs[1].default_value = (1.0, 0.62, 0); ln = wn.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
ramp = wn.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'EASE'; e0, e1 = ramp.color_ramp.elements; e0.position = 0.0; e0.color = (0.012, 0.038, 0.045, 1); e1.position = 0.62; e1.color = (0.0015, 0.003, 0.006, 1)
lp = wn.nodes.new('ShaderNodeLightPath'); wn.links.new(tc.outputs['Window'], sub.inputs[0]); wn.links.new(sub.outputs[0], s2.inputs[0]); wn.links.new(s2.outputs[0], ln.inputs[0]); wn.links.new(ln.outputs['Value'], ramp.inputs['Fac'])
wn.links.new(ramp.outputs['Color'], bgn.inputs['Color']); wn.links.new(lp.outputs['Is Camera Ray'], bgn.inputs['Strength'])

bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, 'lennarts-matstation.glb'))
PARTS = {o.name: o for o in bpy.data.objects if o.type == 'MESH'}; ORIG_M = {n: o.matrix_world.copy() for n, o in PARTS.items()}
for o in PARTS.values(): o.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.55
def link(o): sc.collection.objects.link(o); return o

# skarmen
sm_ = bpy.data.materials.new('scr'); sm_.use_nodes = True; snt = sm_.node_tree; sp = snt.nodes['Principled BSDF']; st = snt.nodes.new('ShaderNodeTexImage'); st.image = bpy.data.images.load(os.path.join(ROOT, 'skarm-vantar.png'))
snt.links.new(st.outputs['Color'], sp.inputs['Emission Color']); sp.inputs['Base Color'].default_value = (0.004, 0.006, 0.005, 1); sp.inputs['Roughness'].default_value = 0.2
me = bpy.data.meshes.new('skarm'); w_, h_ = 0.049, 0.0362; me.from_pydata([(-w_ / 2, 0, 0), (w_ / 2, 0, 0), (w_ / 2, 0, h_), (-w_ / 2, 0, h_)], [], [(0, 1, 2, 3)]); me.uv_layers.new()
for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): me.uv_layers[0].data[i].uv = c
me.materials.append(sm_); SCREEN = link(bpy.data.objects.new('skarm', me)); SCREEN.location = (0, 0.0034, 0.0899)

# Byggordning: (delar, forskjutning i sprangskissen, starttid). Varje del aker rakt hem pa 0,8 s och satter sig.
STEPS = [
    (['fotter'], (0, 0, -0.17), 4.0), (['bottenplatta', 'framgard_platta'], (0, 0, -0.135), 4.35), (['bas', 'framgard'], (0, 0, -0.10), 4.7),
    (['grasmatta', 'framgard_gras'], (0, 0, -0.055), 5.1), (['stenar', 'framgard_stenar'], (0, 0, -0.03), 5.45),
    (['kropp_packning'], (0, 0, 0.05), 6.0), (['kropp_sockel'], (0, 0, 0.09), 6.3), (['kropp', 'kropp_vit'], (0, 0, 0.14), 6.6),
    (['fonsterrutor'], (0, 0, 0.26), 7.3), (['stupror', 'stupror_vit'], (0, -0.12, 0.14), 7.55), (['blomlador', 'blomlador_vaxter', 'blomlador_blommor_rod', 'blomlador_blommor_vit'], (0, -0.2, 0.14), 7.8),
    (['doserhus'], (0, 0, 0.30), 8.5), (['doserhjul'], (-0.12, 0, 0.30), 9.1), (['notmagasin'], (0, 0, 0.38), 9.7),
    (['skarmklamma'], (0, 0, 0.24), 10.3), (['kamerafaste'], (0, 0, 0.28), 10.6), (['skarmram'], (0, -0.14, 0.14), 10.9), (['solskydd', 'solskydd_vit'], (0, -0.12, 0.14), 11.15),
    (['monteringsplatta', 'genomforingar'], (0, 0.2, 0.1), 11.6, (0, 0, 0.26)), (['elektroniklada', 'elpackning'], (0, 0.27, 0.1), 12.0, (0, 0, 0.3)), (['ellock'], (0, 0.27, 0.18), 12.5, (0, 0, 0.3)),
    (['skal', 'skal_vit'], (0, -0.2, 0.14), 13.1), (['lucka', 'lucka_vit'], (0, -0.24, 0.2), 13.5), (['servopackning'], (0.06, -0.2, 0.2), 13.85), (['servokapa'], (0.06, -0.2, 0.26), 14.1),
    (['takpackning'], (0, 0, 0.30), 14.9), (['tak_v', 'tak_v_vit'], (-0.17, 0, 0.33), 15.3), (['tak_h', 'tak_h_vit'], (0.17, 0, 0.33), 15.55),
    (['takrannor'], (0, 0, 0.44), 16.1), (['nockkilar'], (0, 0, 0.4), 16.5), (['skorsten', 'skorsten_krage'], (0.22, 0, 0.42), 17.1, (0, 0, 0.2))]
DUR = 0.8; missing = set(PARTS) - {n for s in STEPS for n in s[0]}
if missing: print('SAKNAS I BYGGORDNINGEN', sorted(missing), flush=True)

def light(loc, target, power, size, col):
    d = bpy.data.lights.new('l', 'AREA'); d.energy = power; d.size = size; d.color = col; o = link(bpy.data.objects.new('l', d)); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
light((-1.1, -1.2, 1.5), (0, 0.05, 0.2), 34, 1.3, (1, 0.93, 0.85)); light((1.2, 1.0, 0.8), (0, 0.05, 0.25), 17, 0.5, (0.45, 0.7, 0.9)); light((0.2, -0.3, 1.6), (0, 0.07, 0.1), 7, 0.6, (1, 0.95, 0.9))
cam_d = bpy.data.cameras.new('cam'); CAM = link(bpy.data.objects.new('cam', cam_d)); sc.camera = CAM; cam_d.clip_start = 0.01; cam_d.dof.use_dof = True

def sm(t, a, b): x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)
def settle(u):   # snabbt forst, bromsar in, en liten oversvangning och sedan stilla
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    c = 1.35; v = u - 1; return 1 + (c + 1) * v ** 3 + c * v ** 2
# kamerans nycklar: tid, vinkel runt huset (grader), avstand, hojd over malpunkten, malpunktens hojd, brannvidd
KEYS = [(0.0, 62, 2.85, 0.28, 0.22, 60), (4.0, 50, 2.55, 0.32, 0.19, 60), (7.0, 42, 1.5, 0.3, 0.1, 60), (10.0, 32, 1.0, 0.62, 0.11, 58), (12.8, 24, 0.95, 0.56, 0.1, 58),
        (14.6, 16, 0.92, 0.2, 0.07, 60), (17.4, 22, 1.25, 0.38, 0.17, 62), (22.0, 27, 1.12, 0.07, 0.118, 56)]
def spline(t, ch):   # mjuk kurva genom nycklarna (Catmull-Rom), sa att kameran aldrig stannar eller rycker
    ts = [k[0] for k in KEYS]; i = max(0, min(len(KEYS) - 2, max(j for j in range(len(KEYS)) if ts[j] <= t) if t >= ts[0] else 0)); i = min(i, len(KEYS) - 2)
    p0, p1, p2, p3 = (KEYS[max(i - 1, 0)][ch], KEYS[i][ch], KEYS[i + 1][ch], KEYS[min(i + 2, len(KEYS) - 1)][ch]); u = (t - ts[i]) / (ts[i + 1] - ts[i])
    m1 = (p2 - p0) / (ts[i + 1] - ts[max(i - 1, 0)]) * (ts[i + 1] - ts[i]) if i > 0 else (p2 - p1); m2 = (p3 - p1) / (ts[min(i + 2, len(KEYS) - 1)] - ts[i]) * (ts[i + 1] - ts[i]) if i < len(KEYS) - 2 else (p2 - p1)
    return (2 * u ** 3 - 3 * u ** 2 + 1) * p1 + (u ** 3 - 2 * u ** 2 + u) * m1 + (-2 * u ** 3 + 3 * u ** 2) * p2 + (u ** 3 - u ** 2) * m2

def state(t):
    for i, st in enumerate(STEPS):
        names, off, t0 = st[:3]; k = settle((t - t0) / DUR); breathe = 1 + 0.025 * math.sin(t * 1.4 + i * 0.7) * (1 - k)
        d = (Vector(off) * (1 - k) ** 2 + Vector(st[3]) * 2 * k * (1 - k) if len(st) > 3 else Vector(off) * (1 - k)) * breathe   # med mellanpunkt: en bage in over vaggen i stallet for rakt igenom den
        for n in names: PARTS[n].matrix_world = Matrix.Translation(d) @ ORIG_M[n]
    ang = math.radians(-95 * math.sin(math.pi * sm(t, 14.3, 15.5)) ** 2)   # luckan provoppnas en gang
    if t > 14.3:
        for n in ('lucka', 'lucka_vit'): PARTS[n].matrix_world = ORIG_M[n] @ Matrix.Rotation(ang, 4, 'X')
    SCREEN.hide_render = t < 11.7; sp.inputs['Emission Strength'].default_value = 2.3 * sm(t, 18.6, 18.9) * (0.6 + 0.4 * min(1, max(0, (t - 18.9) * 4)))
    az = math.radians(spline(t, 1)); r = spline(t, 2); tz = spline(t, 4); tgt = Vector((0, 0.02, tz)); eye = tgt + Vector((r * math.sin(az), -r * math.cos(az), spline(t, 3)))
    CAM.location = eye; CAM.rotation_euler = (tgt - eye).to_track_quat('-Z', 'Y').to_euler(); cam_d.lens = spline(t, 5); cam_d.dof.aperture_fstop = 5.6; cam_d.dof.focus_distance = (tgt - eye).length

frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(END * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.' + ('png' if MASK else 'jpg'))
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    state(f / FPS); bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
