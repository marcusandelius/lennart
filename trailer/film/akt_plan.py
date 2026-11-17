# Projekt Lennart - del 2: problemet och planen, i samma 3D-stil som resten.
# En mork scen. Ett fat med notter och en skal med vatten, figurerna som utstansade kartongfigurer, en kamera som sanks ner i en sladd, ett moln som svarar ja eller nej.
# Huset visas inte har: det avslojas forst i del 3.
# Kor:  blender -b -P akt_plan.py -- <ut-mapp (absolut)> <bredd> <samples> [tider i sekunder ...]
import bpy, sys, os, math, json
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, SAMPLES, TIMES = os.path.abspath(a[0]), int(a[1]), int(a[2]), [float(x) for x in a[3:]]
os.makedirs(OUT, exist_ok=True); FPS, END = 25, 44.5; GROUND = -0.037

def typsnitt(*namn):   # letar upp ett typsnitt pa den har datorn; annars Blenders inbyggda (texten blir da i ett annat typsnitt)
    import glob
    mappar = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'typsnitt'), r'C:\Windows\Fonts', os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', '/System/Library/Fonts', '/System/Library/Fonts/Supplemental', '/usr/share/fonts', os.path.expanduser('~/.fonts')]
    for n in namn:
        for m in mappar:
            hit = glob.glob(os.path.join(m, '**', n), recursive=True) if os.path.isdir(m) else []
            if hit: return bpy.data.fonts.load(hit[0])
    print('TYPSNITT saknas:', namn, '- anvander Blenders inbyggda', flush=True); return bpy.data.fonts.load('<builtin>') if '<builtin>' in [f.filepath for f in bpy.data.fonts] else None
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = 'CYCLES'; pr = bpy.context.preferences.addons['cycles'].preferences; sc.cycles.device = 'CPU'
for kind in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
    try:
        pr.compute_device_type = kind; pr.get_devices(); ds = [d for d in pr.devices if d.type == kind]
        if ds:
            for d in pr.devices: d.use = d.type == kind
            sc.cycles.device = 'GPU'; break
    except Exception: pass
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 8; sc.cycles.transparent_max_bounces = 64; sc.render.use_persistent_data = True
sc.render.resolution_x = WIDTH; sc.render.resolution_y = WIDTH * 9 // 16; sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 95
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception as e: print('look', e)
# bakgrund: samma morka petroleumbla sken som i oppningen
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; wn = sc.world.node_tree; bgn = wn.nodes['Background']
tc = wn.nodes.new('ShaderNodeTexCoord'); sub = wn.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0)
s2 = wn.nodes.new('ShaderNodeVectorMath'); s2.operation = 'MULTIPLY'; s2.inputs[1].default_value = (1.0, 0.62, 0); ln = wn.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
ramp = wn.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'EASE'; e0, e1 = ramp.color_ramp.elements; e0.position = 0.0; e0.color = (0.012, 0.038, 0.045, 1); e1.position = 0.66; e1.color = (0.0015, 0.003, 0.006, 1)
lp = wn.nodes.new('ShaderNodeLightPath'); wn.links.new(tc.outputs['Window'], sub.inputs[0]); wn.links.new(sub.outputs[0], s2.inputs[0]); wn.links.new(s2.outputs[0], ln.inputs[0]); wn.links.new(ln.outputs['Value'], ramp.inputs['Fac'])
wn.links.new(ramp.outputs['Color'], bgn.inputs['Color']); wn.links.new(lp.outputs['Is Camera Ray'], bgn.inputs['Strength'])

def link(o): sc.collection.objects.link(o); return o
def mat(name, col, rough=0.5, metal=0.0, coat=0.0, emit=None, es=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal; p.inputs['Coat Weight'].default_value = coat
    if emit: p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = es
    return m
def P_(m): return m.node_tree.nodes['Principled BSDF']




def quad_mesh(w, h, z0=0.0):
    me = bpy.data.meshes.new('q'); me.from_pydata([(-w / 2, 0, z0), (w / 2, 0, z0), (w / 2, 0, z0 + h), (-w / 2, 0, z0 + h)], [], [(0, 1, 2, 3)]); me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): me.uv_layers[0].data[i].uv = c
    return me
# ---------- kameran: en enkel kamera som sanks ner i en sladd och tittar pa den som kommer ----------
from mathutils import Euler
HANG = link(bpy.data.objects.new('upphangning', None)); HANG_AT = Vector((-0.01, -0.14, 0.24)); RIG = link(bpy.data.objects.new('kamera', None)); RIG.parent = HANG; RIG_ROT = Euler((0, 0.3, -0.62)); RIG.rotation_euler = RIG_ROT; RIG.scale = (1.3, 1.3, 1.3); RIGO = []
def rig(o, loc, par=None): o.parent = par or RIG; o.location = loc; RIGO.append(o); return o
kb = mat('kamerahus', (0.03, 0.032, 0.035), 0.42, coat=0.3); ks = mat('kamerasilver', (0.6, 0.61, 0.63), 0.28, metal=1.0); FLASH_M = mat('blixt', (0.8, 0.8, 0.8), 0.2, emit=(1, 1, 1), es=0.0)
def box(sx, sy, sz, m, loc, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.active_object; o.scale = (sx, sy, sz); bpy.ops.object.transform_apply(scale=True)
    if bevel: b = o.modifiers.new('b', 'BEVEL'); b.width = bevel; b.segments = 4
    for p in o.data.polygons: p.use_smooth = bool(bevel)
    o.data.materials.append(m); return rig(o, loc)
def cyl(r, d, m, loc, axis='X'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=d, rotation=(0, math.pi / 2, 0) if axis == 'X' else (0, 0, 0)); o = bpy.context.active_object
    for p in o.data.polygons: p.use_smooth = len(p.vertices) == 4
    o.data.materials.append(m); return o
box(0.046, 0.1, 0.062, kb, (0, 0, 0), 0.007); box(0.047, 0.101, 0.012, ks, (0, 0, 0.029), 0.003)
rig(cyl(0.027, 0.02, ks, None), (0.03, 0.006, -0.004)); rig(cyl(0.023, 0.03, kb, None), (0.04, 0.006, -0.004)); rig(cyl(0.0175, 0.002, mat('lins', (0.01, 0.02, 0.06), 0.03, coat=1.0), None), (0.0555, 0.006, -0.004))
box(0.003, 0.024, 0.011, FLASH_M, (0.0235, -0.03, 0.016)); rig(cyl(0.007, 0.006, ks, None, 'Z'), (0, -0.03, 0.038))
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.003); o = bpy.context.active_object; o.data.materials.append(mat('lampa', (0, 0, 0), 0.3, emit=(1.0, 0.15, 0.1), es=6.0)); rig(o, (0.0235, 0.04, 0.02))
rig(cyl(0.0022, 1.4, mat('sladd', (0.02, 0.02, 0.022), 0.5), None, 'Z'), (0, 0, 0.73), HANG)
fd = bpy.data.lights.new('blixtljus', 'POINT'); fd.shadow_soft_size = 0.02; fd.color = (1, 0.97, 0.92); FL = link(bpy.data.objects.new('blixtljus', fd)); FL.parent = RIG; FL.location = (0.07, -0.03, 0.016)
LENS = Matrix.Translation(HANG_AT) @ RIG_ROT.to_matrix().to_4x4() @ (Vector((0.065, 0.006, -0.004)) * 1.3)

# ---------- kartongfigurer: dekalen pa utstansad, 3 mm tjock kartong med fot ----------
def standee(name, png, h, sink):
    e = link(bpy.data.objects.new(name, None)); img = bpy.data.images.load(os.path.join(ROOT, png))
    def layer_mat(front):
        m = bpy.data.materials.new(name + ('_f' if front else '_k')); m.use_nodes = True; n2 = m.node_tree; p = n2.nodes['Principled BSDF']; t = n2.nodes.new('ShaderNodeTexImage'); t.image = img; t.extension = 'CLIP'
        n2.links.new(t.outputs['Alpha'], p.inputs['Alpha']); p.inputs['Roughness'].default_value = 0.6
        if front: n2.links.new(t.outputs['Color'], p.inputs['Base Color'])
        else: p.inputs['Base Color'].default_value = (0.62, 0.52, 0.4, 1)
        return m
    mf, mk = layer_mat(True), layer_mat(False)
    for i in range(6):
        me = quad_mesh(h, h, -sink * h); me.materials.append(mf if i == 0 else mk); o = link(bpy.data.objects.new(name + str(i), me)); o.location = (0, 0.0006 * i, 0); o.parent = e
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1, depth=1, location=(0, 0.0015, 0.0015)); b = bpy.context.active_object; b.scale = (h * 0.2, h * 0.11, 0.003); b.data.materials.append(mat(name + '_fot', (0.62, 0.52, 0.4), 0.7)); b.parent = e
    return e
BIRD = standee('skata', 'dekal-skata.png', 0.3, 0.135); SQ = standee('lennart', 'dekal-lennart.png', 0.22, 0.085)


# ---------- fatet och hasselnotterna ----------
PLATE = link(bpy.data.objects.new('fat', None)); PLATE.location = (0.2, -0.14, GROUND); cer = mat('porslin', (0.86, 0.85, 0.82), 0.25, coat=0.6)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.075, depth=0.005, location=(0, 0, 0.0025)); o = bpy.context.active_object; o.data.materials.append(cer); o.parent = PLATE
bpy.ops.mesh.primitive_torus_add(major_radius=0.072, minor_radius=0.0045, major_segments=96, minor_segments=16, location=(0, 0, 0.006)); o = bpy.context.active_object; o.data.materials.append(cer); o.parent = PLATE
for p in o.data.polygons: p.use_smooth = True
bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, radius=1); n0 = bpy.context.active_object
for v in n0.data.vertices:
    x, y, z = v.co
    if z > 0: k = 1 - 0.30 * z ** 2.2; x *= k; y *= k; z = z * 1.08 + 0.16 * z ** 6
    else: z = max(z * 0.95, -0.78)
    v.co = (x * 1.04, y * 0.98, z)
for p in n0.data.polygons: p.use_smooth = True
# samma hasselnot som i oppningen: adrat skal och blek bas
nm = bpy.data.materials.new('hasselnot'); nm.use_nodes = True; nt_n = nm.node_tree; p_n = nt_n.nodes['Principled BSDF']; t_n = nt_n.nodes.new('ShaderNodeTexCoord'); sep = nt_n.nodes.new('ShaderNodeSeparateXYZ')
mp = nt_n.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (9, 9, 0.7); noi = nt_n.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 2.0; noi.inputs['Detail'].default_value = 3
shell = nt_n.nodes.new('ShaderNodeValToRGB'); shell.color_ramp.elements[0].position = 0.3; shell.color_ramp.elements[0].color = (0.16, 0.065, 0.022, 1); shell.color_ramp.elements[1].position = 0.75; shell.color_ramp.elements[1].color = (0.42, 0.20, 0.07, 1)
capf = nt_n.nodes.new('ShaderNodeMapRange'); capf.inputs['From Min'].default_value = -0.70; capf.inputs['From Max'].default_value = -0.52; capf.inputs['To Min'].default_value = 1; capf.inputs['To Max'].default_value = 0
mixc = nt_n.nodes.new('ShaderNodeMixRGB'); mixc.inputs['Color2'].default_value = (0.62, 0.50, 0.34, 1); mixr = nt_n.nodes.new('ShaderNodeMapRange'); mixr.inputs['To Min'].default_value = 0.28; mixr.inputs['To Max'].default_value = 0.8
nt_n.links.new(t_n.outputs['Object'], sep.inputs[0]); nt_n.links.new(t_n.outputs['Object'], mp.inputs['Vector']); nt_n.links.new(mp.outputs[0], noi.inputs['Vector']); nt_n.links.new(noi.outputs['Fac'], shell.inputs['Fac'])
nt_n.links.new(sep.outputs['Z'], capf.inputs['Value']); nt_n.links.new(capf.outputs[0], mixc.inputs['Fac']); nt_n.links.new(shell.outputs['Color'], mixc.inputs['Color1']); nt_n.links.new(mixc.outputs[0], p_n.inputs['Base Color'])
nt_n.links.new(capf.outputs[0], mixr.inputs['Value']); nt_n.links.new(mixr.outputs[0], p_n.inputs['Roughness']); p_n.inputs['Coat Weight'].default_value = 0.25
n0.data.materials.append(nm); NR = 0.0085; NUTS = [n0] + [link(bpy.data.objects.new('not%d' % i, n0.data)) for i in range(1, 15)]
# notternas vilolagen raknas fram av verktyg/notfat.py (de undre vilar pa fatet, de ovre har kontakt med notterna under): [x, y, rz, z over golvet]
import json; POP = json.load(open(os.path.join(HERE, 'notfat.json'))); NUT_REST = POP[:6]
BOWL = link(bpy.data.objects.new('vattenskal', None)); BOWL.location = (0.075, -0.215, GROUND)
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=(0, 0, 0.026)); o = bpy.context.active_object; o.scale = (0.046, 0.046, 0.026)
for v in o.data.vertices:
    if v.co.z > 0: v.co = (v.co.x * 0.9, v.co.y * 0.9, -0.12 if (v.co.x ** 2 + v.co.y ** 2) < 0.8 else 0.0)
for p in o.data.polygons: p.use_smooth = True
o.data.materials.append(cer); o.parent = BOWL
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.039, depth=0.001, location=(0, 0, 0.0245)); o = bpy.context.active_object; o.data.materials.append(mat('vatten', (0.16, 0.42, 0.62), 0.04, coat=1.0)); o.parent = BOWL

# ---------- molnet: mjuka klot som smalter ihop, lyser inifran i svarets farg ----------
# byggt av overlappande klot med platt undersida, som en mjuk leksak
_lumps = []
for (x, y, z, r) in [(-0.095, 0.0, 0.0, 0.048), (-0.04, 0.012, 0.034, 0.064), (0.035, 0.0, 0.046, 0.076), (0.1, 0.01, 0.008, 0.054), (0.0, -0.02, 0.0, 0.058), (0.062, -0.018, -0.002, 0.052), (-0.055, -0.016, -0.006, 0.046)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=r, location=(x, y, z)); o = bpy.context.active_object; _lumps.append(o)
    for v in o.data.vertices:
        if v.co.z + z < -0.03: v.co.z = -0.03 - z + (v.co.z + z + 0.03) * 0.25
    for p in o.data.polygons: p.use_smooth = True
bpy.ops.object.select_all(action='DESELECT')
for o in _lumps: o.select_set(True)
bpy.context.view_layer.objects.active = _lumps[0]; bpy.ops.object.join(); CLOUD = bpy.context.active_object; CLOUD.name = 'moln'; cme = CLOUD.data
CLOUD_M = bpy.data.materials.new('moln'); CLOUD_M.use_nodes = True; cp = P_(CLOUD_M); cp.inputs['Base Color'].default_value = (0.93, 0.95, 0.97, 1); cp.inputs['Roughness'].default_value = 0.55; cp.inputs['Subsurface Weight'].default_value = 0.5; cp.inputs['Subsurface Radius'].default_value = (0.05, 0.05, 0.05)
cme.materials.append(CLOUD_M); CLOUD_AT = Vector((0.46, 0.06, 0.305)); CLOUD.scale = (1, 0.8, 1)
FONT = typsnitt('consolab.ttf', 'Menlo.ttc', 'DejaVuSansMono-Bold.ttf')
def stadium(w, h, d, m):
    r = h / 2; pts = [(w / 2 - r + r * math.cos(-math.pi / 2 + math.pi * i / 24), r * math.sin(-math.pi / 2 + math.pi * i / 24)) for i in range(25)] + [(-w / 2 + r + r * math.cos(math.pi / 2 + math.pi * i / 24), r * math.sin(math.pi / 2 + math.pi * i / 24)) for i in range(25)]
    n = len(pts); vs = [(x, -d / 2, z) for x, z in pts] + [(x, d / 2, z) for x, z in pts]
    me = bpy.data.meshes.new('skylt'); me.from_pydata(vs, [], [list(range(n)), list(range(2 * n - 1, n - 1, -1))] + [(i, i + n, (i + 1) % n + n, (i + 1) % n) for i in range(n)]); me.materials.append(m); return link(bpy.data.objects.new('skylt', me))
PILL = link(bpy.data.objects.new('svar', None)); PILL_AT = Vector((CLOUD_AT.x + 0.04, CLOUD_AT.y - 0.085, CLOUD_AT.z - 0.03))
RIM_M = mat('skyltkant', (0, 0, 0), 0.3, emit=(1, 1, 1), es=3.0); body = stadium(0.325, 0.07, 0.012, mat('skylt', (0.012, 0.017, 0.021), 0.22, coat=0.6)); body.parent = PILL
rim = stadium(0.333, 0.078, 0.006, RIM_M); rim.location = (0, 0.005, 0); rim.parent = PILL; PILL_OBJS = [body, rim]
COLS = dict(fraga=(1.0, 0.72, 0.23), ver=(1.0, 0.72, 0.23), nej=(1.0, 0.28, 0.22), ja=(0.3, 0.95, 0.5)); TXTG = {}; DOTS = []
def bar(parent, m, l, w, x, y, ang):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.active_object; o.scale = (l, w, 0.003); o.location = (x, y, 0.0015); o.rotation_euler = (0, 0, ang); o.data.materials.append(m); o.parent = parent; return o
for key, body_, size in [('fraga', 'ÄR DET EN EKORRE?', 0.027), ('ver', 'VERIFIERAR', 0.031), ('nej', 'INGEN EKORRE', 0.03), ('ja', 'EKORRE', 0.034)]:
    m = mat('t_' + key, (0, 0, 0), 0.3, emit=COLS[key], es=3.2); c = bpy.data.curves.new('t', 'FONT'); c.body = body_; c.font = FONT or c.font; c.size = size; c.align_x = 'CENTER'; c.align_y = 'CENTER'; c.extrude = 0.0012; c.materials.append(m)
    half = len(body_) * 0.55 * size / 2; shift = dict(fraga=0.0, ver=-0.02, nej=0.02, ja=0.022)[key]
    o = link(bpy.data.objects.new('t_' + key, c)); o.rotation_euler = (math.pi / 2, 0, 0); o.location = (shift, -0.0065, 0); o.parent = PILL; TXTG[key] = [o]
    if key == 'nej': TXTG[key] += [bar(o, m, 0.03, 0.006, -half - 0.024, 0, 0.785), bar(o, m, 0.03, 0.006, -half - 0.024, 0, -0.785)]
    if key == 'ja': TXTG[key] += [bar(o, m, 0.016, 0.006, -half - 0.036, -0.004, -0.785), bar(o, m, 0.034, 0.006, -half - 0.02, 0.002, 0.96)]
    if key == 'ver':
        for i in range(3):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.0042, location=(half + 0.014 + i * 0.014, -0.006, 0.002)); d_ = bpy.context.active_object; d_.data.materials.append(m); d_.parent = o; TXTG[key].append(d_); DOTS.append(d_)
# signalen: bilden som kameran tog flyger upp till molnet som ett litet lysande kort, svaret kommer tillbaka som en puls i svarets farg
SIG_M = mat('signal', (0, 0, 0), 0.3, emit=(1, 1, 1), es=7.0)
def card(png):
    img = bpy.data.images.load(os.path.join(ROOT, png)); m = bpy.data.materials.new('kort'); m.use_nodes = True; n2 = m.node_tree; p = n2.nodes['Principled BSDF']; t = n2.nodes.new('ShaderNodeTexImage'); t.image = img; t.extension = 'CLIP'
    mixc = n2.nodes.new('ShaderNodeMixRGB'); mixc.inputs['Color1'].default_value = (0.02, 0.05, 0.06, 1); n2.links.new(t.outputs['Alpha'], mixc.inputs['Fac']); n2.links.new(t.outputs['Color'], mixc.inputs['Color2'])
    n2.links.new(mixc.outputs[0], p.inputs['Base Color']); n2.links.new(mixc.outputs[0], p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value = 1.6
    e = link(bpy.data.objects.new('kort', None)); me = quad_mesh(0.052, 0.052, -0.026); me.materials.append(m); q = link(bpy.data.objects.new('kortbild', me)); q.parent = e
    me2 = quad_mesh(0.06, 0.06, -0.03); me2.materials.append(SIG_M); q2 = link(bpy.data.objects.new('kortram', me2)); q2.location = (0, 0.001, 0); q2.parent = e; return e
CARD = dict(bird=card('dekal-skata.png'), sq=card('dekal-lennart.png'))
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.009); HEAD = bpy.context.active_object; HEAD.data.materials.append(SIG_M)
for p in HEAD.data.polygons: p.use_smooth = True
SIG_A, SIG_C, SIG_B = LENS, Vector((0.16, -0.1, 0.5)), Vector((0.37, -0.02, 0.31)); DN_C, DN_B = Vector((0.3, -0.1, 0.2)), Vector((0.2, -0.14, GROUND + 0.02))
def bez(u): return (1 - u) ** 2 * SIG_A + 2 * u * (1 - u) * SIG_C + u ** 2 * SIG_B
tc_ = bpy.data.curves.new('spar', 'CURVE'); tc_.dimensions = '3D'; sp_ = tc_.splines.new('POLY'); sp_.points.add(59)
for i, p in enumerate(sp_.points): p.co = (*bez(i / 59), 1)
tc_.bevel_depth = 0.0016; tc_.bevel_resolution = 3; tc_.materials.append(SIG_M); TRAIL = link(bpy.data.objects.new('spar', tc_))
def bez2(u): return (1 - u) ** 2 * SIG_B + 2 * u * (1 - u) * DN_C + u ** 2 * DN_B
tc2 = bpy.data.curves.new('spar2', 'CURVE'); tc2.dimensions = '3D'; sp2 = tc2.splines.new('POLY'); sp2.points.add(59)
for i, p in enumerate(sp2.points): p.co = (*bez2(i / 59), 1)
tc2.bevel_depth = 0.0016; tc2.bevel_resolution = 3; tc2.materials.append(SIG_M); TRAIL2 = link(bpy.data.objects.new('spar2', tc2))

bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, GROUND)); bpy.context.active_object.data.materials.append(mat('golv', (0.016, 0.02, 0.022), 0.34))
def light(loc, target, power, size, col):
    d = bpy.data.lights.new('l', 'AREA'); d.energy = power; d.size = size; d.color = col; o = link(bpy.data.objects.new('l', d)); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
light((-0.8, -1.1, 1.2), (0.15, -0.05, 0.1), 46, 1.0, (1, 0.94, 0.86)); light((1.2, 0.9, 0.7), (0.15, 0, 0.15), 22, 0.4, (0.45, 0.7, 0.9))
cam_d = bpy.data.cameras.new('cam'); CAM = link(bpy.data.objects.new('cam', cam_d)); sc.camera = CAM; cam_d.clip_start = 0.01; cam_d.dof.use_dof = True

def sm(t, a, b): x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)
def mix(p, q, k): return Vector(p) + (Vector(q) - Vector(p)) * k
def hops(t, t0, xs, dur=0.36, gap=0.07, h=0.05):   # en rad hopp mellan x-lagen: ger (x, hojd, lutning)
    if t <= t0: return xs[0], 0.0, 0.0
    k = (t - t0) / (dur + gap); i = int(k)
    if i >= len(xs) - 1: return xs[-1], 0.0, 0.0
    u = min(1.0, (k - i) * (dur + gap) / dur); return xs[i] + (xs[i + 1] - xs[i]) * u, h * 4 * u * (1 - u), 0.22 * math.sin(math.pi * u) * (1 if xs[i + 1] < xs[i] else -1)
def pulse(t, t0, w=0.28): x = (t - t0) / w; return math.sin(math.pi * x) if 0 < x < 1 else 0.0
def place(fig, x, y, z, lean, face):
    fig.location = (x, y, GROUND + z); fig.rotation_euler = (0, lean, 0); fig.scale = (face, 1, 1)
def flip(t, t0, d=0.24): return math.cos(math.pi * sm(t, t0, t0 + d))   # 1 -> -1, som ett kort som vands

# Tidpunkter (sekunder). Rosten ar lagd efter arbetsrosten och stams av mot den riktiga inspelningen.
T = dict(bird_in=0.5, pecks=(2.5, 3.3, 4.1), bird_out=4.9, sq_in=5.5, sq_look=7.4, drop=(15.3, 17.3), sq_out=20.2, bird2_in=21.6, flash1=25.6, up1=(26.6, 28.2), ask1=29.2, no=31.3, down1=(31.5, 32.7),
         bird2_out=35.0, sq2_in=36.3, flash2=37.75, up2=(37.85, 38.8), yes=39.5, down2=(39.65, 40.45), pop=40.45, sq_bowl=41.6)

PAN_GRAD, PAN_TID = 24.0, 0.36   # panoreringen in: vinkel vid forsta rutan, och hur lange den bromsar (sekunder)
# Fallet: i stallet for panoreringen tappar Lennart noten i slutet av 1.4. Har faller den ovanifran, kameran foljer med ner
# och noten landar bland de andra pa fatet med en liten studs. Det ar den ovre noten pa fatet som faller (FK), sa att skatan sedan ater den som vanligt.
FALL = os.environ.get('LENNART_FALL', '1') == '1'   # LENNART_FALL=0 ger tillbaka panoreringen
if FALL: PAN_GRAD = 0.0; bpy.app.handlers.frame_change_pre.append(lambda sc_, *_: state(sc_.frame_current_final / FPS) if sc_.render.use_motion_blur else None)
FK = max(range(6), key=lambda i: NUT_REST[i][3]); F_TL, F_H, F_V0 = 0.6, 0.5, 0.6; F_A = 2 * (F_H - F_V0 * F_TL) / F_TL ** 2   # landar efter 0,6 s, faller 0,5 m
def fall_nut(t):   # (forskjutning fran vilolaget, hur mycket av vridningen som ar kvar (1 -> 0), studsens vickning)
    if t < F_TL: return Vector((0, 0, F_H - F_V0 * t - 0.5 * F_A * t * t)), (1 - t / F_TL) ** 1.5, 0.0
    u = (t - F_TL) / 0.2; u2 = (t - F_TL - 0.2) / 0.12; z = 0.012 * 4 * u * (1 - u) if u < 1 else (0.003 * 4 * u2 * (1 - u2) if u2 < 1 else 0.0)
    return Vector((0.006 * (1 - math.exp(-(t - F_TL) * 9)), 0, z)), 0.0, 0.35 * math.exp(-(t - F_TL) * 10) * math.sin((t - F_TL) * 30)
PLATE_AT = PLATE.location.copy(); WOB_A, WOB_D = 6.0, 1.4      # fatets snurr: storsta lutning i grader, langd i sekunder
def wob_phase(s): return 2 * math.pi * (2.2 * s + 3.0 * s * s)   # varvet gar fran 2 till 10 varv per sekund
def state(t):
    # kameran sanks ner i sin sladd, gungar till och hanger sedan still
    d0, d1 = T['drop']; u = sm(t, d0, d1); sw = 0.14 * math.exp(-(t - d1 + 0.4) * 1.5) * math.sin((t - d1 + 0.4) * 6.5) if t > d1 - 0.4 else 0.0
    HANG.location = HANG_AT + Vector((0, 0, 0.75 * (1 - u) ** 2 + 0.012 * sw)); HANG.rotation_euler = (0, sw, 0)
    for o in RIGO: o.hide_render = t < d0
    fl = pulse(t, T['flash1'], 0.22) + pulse(t, T['flash2'], 0.22); P_(FLASH_M).inputs['Emission Strength'].default_value = 60 * fl; fd.energy = 4 * fl
    # fatet och notterna. Nar nej-signalen slar ner i det tomma fatet snurrar det som ett mynt pa ett bord: lutningen minskar
    # medan varvet gar allt fortare, tills det plotsligt ligger still (samma kurva som snurrljudet i effekter.py, 'tallrik')
    tw_ = t - T['down1'][1]
    if 0 <= tw_ < WOB_D:
        a_ = math.radians(WOB_A) * min(1.0, tw_ / 0.05) * (1 - tw_ / WOB_D) ** 1.3; ph_ = wob_phase(tw_)
        R_ = Matrix.Rotation(ph_, 4, 'Z') @ Matrix.Rotation(a_, 4, 'X') @ Matrix.Rotation(-ph_, 4, 'Z')
        PLATE.matrix_world = Matrix.Translation(PLATE_AT + Vector((0, 0, 0.075 * math.sin(a_)))) @ R_
    else: PLATE.matrix_world = Matrix.Translation(PLATE_AT)
    for i, (x, y, rz, zr) in enumerate(NUT_REST):
        gone = t >= T['pecks'][i // 2]; NUTS[i].hide_render = gone; NUTS[i].matrix_world = Matrix.Translation((x, y, GROUND + zr)) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(1.15 + 0.25 * math.sin(rz * 3), 4, 'X') @ Matrix.Scale(NR, 4)
    if FALL and t < 2.0:
        x, y, rz, zr = NUT_REST[FK]; p_, kvar, wob = fall_nut(t); th = 1.15 + 0.25 * math.sin(rz * 3)   # borjar uppratt med spetsen uppat (som i 1.4) och tumlar ner i sitt vilolage
        NUTS[FK].matrix_world = Matrix.Translation(Vector((x, y, GROUND + zr)) + p_) @ Matrix.Rotation(rz * (1 - kvar), 4, 'Z') @ Matrix.Rotation(th * (1 - kvar) + wob, 4, 'X') @ Matrix.Rotation(-0.15 * th * kvar, 4, 'Y') @ Matrix.Scale(NR, 4)
        if t > F_TL:   # de andra notterna rycker till nar den slar ner
            for i in range(6):
                if i != FK and not NUTS[i].hide_render: NUTS[i].matrix_world = NUTS[i].matrix_world @ Matrix.Rotation(0.06 * math.exp(-(t - F_TL) * 14) * math.sin((t - F_TL) * 45 + i * 1.7), 4, 'X')
    for i, (x, y, rz, zr) in enumerate(POP):   # notterna poppar upp ur fatet, en i taget
        u = (t - T['pop'] - i * 0.075) / 0.45; n_ = NUTS[6 + i]; n_.hide_render = u <= 0
        if u > 0:
            v = min(1.0, u); p_ = mix((0.2, -0.14, 0.012), (x, y, zr), min(1.0, v * 1.3)) + Vector((0, 0, GROUND + (0.07 + 0.02 * (i % 3)) * 4 * v * (1 - v)))
            n_.matrix_world = Matrix.Translation(p_) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(1.15 + 0.25 * math.sin(rz * 3) + (1 - v) * 5, 4, 'X') @ Matrix.Scale(NR * min(1.0, v * 2.5), 4)
    # skatan
    if t < T['bird2_in'] - 1.2:
        if t < T['bird_out']: x, z, ln_ = hops(t, T['bird_in'], [0.82, 0.66, 0.51, 0.385]); ln_ += -0.42 * sum(pulse(t, tp - 0.14) for tp in T['pecks']); face = flip(t, T['bird_out'] - 0.3)
        else: x, z, ln_ = hops(t, T['bird_out'], [0.385, 0.55, 0.72, 0.95]); ln_ = -ln_; face = -1
    else:
        if t < T['bird2_out']: x, z, ln_ = hops(t, T['bird2_in'], [0.95, 0.76, 0.58, 0.42]); face = flip(t, T['bird2_out'] - 0.3)
        else: x, z, ln_ = hops(t, T['bird2_out'], [0.42, 0.6, 0.78, 0.98]); ln_ = -ln_; face = -1
    place(BIRD, x, -0.14, z, ln_, face)
    # Lennart
    if t < T['sq2_in'] - 1.2:
        if t < T['sq_out']: x, z, ln_ = hops(t, T['sq_in'], [0.9, 0.72, 0.55, 0.4]); ln_ += -0.2 * sm(t, T['sq_look'], T['sq_look'] + 0.4) * (1 - sm(t, 8.4, 8.9)) + 0.1 * sm(t, 8.5, 9.1) * (1 - sm(t, 14.6, 15.4)); face = flip(t, T['sq_out'] - 0.3)
        else: x, z, ln_ = hops(t, T['sq_out'], [0.4, 0.57, 0.75, 0.98]); ln_ = -ln_; face = -1
    else:
        x, z, ln_ = hops(t, T['sq2_in'], [0.98, 0.78, 0.6, 0.44]); face = 1
        if t >= T['sq_bowl']: x, z, ln_ = hops(t, T['sq_bowl'], [0.44, 0.39, 0.345], 0.3, 0.06, 0.035); ln_ += -0.16 * sm(t, T['sq_bowl'] + 0.8, T['sq_bowl'] + 1.3)
    place(SQ, x, -0.14, z, ln_, face)
    # molnet, fragan och signalen
    think = (T['up1'][1] - 0.15 <= t < T['no']) or (T['up2'][1] - 0.15 <= t < T['yes'])
    if t >= T['yes']: col, es = (0.25, 0.95, 0.5), 0.35 + 1.0 * (1 - sm(t, T['yes'], T['yes'] + 1.5)) + 0.25
    elif t >= T['no'] and t < T['bird2_out'] + 1.0: col, es = (1.0, 0.22, 0.18), (0.4 + 1.0 * (1 - sm(t, T['no'], T['no'] + 1.5))) * (1 - sm(t, T['bird2_out'], T['bird2_out'] + 1.0)) + 0.05
    elif think: col, es = (1.0, 0.7, 0.22), 0.55 + 0.35 * math.sin(t * 9)
    else: col, es = (0.8, 0.9, 1.0), 0.05
    cp.inputs['Emission Color'].default_value = (*col, 1); cp.inputs['Emission Strength'].default_value = es
    CLOUD.location = CLOUD_AT + Vector((0, 0, 0.006 * math.sin(t * 1.3))); CLOUD.hide_render = t < 12.7; cs = max(0.001, sm(t, 12.7, 13.3)); CLOUD.scale = (cs, 0.8 * cs, cs)
    r1 = T['ask1'] <= t < T['bird2_out'] + 0.6; r2 = t >= T['up2'][1] - 0.1; key = None
    if r2: key, t0, first = ('ja', T['yes'], False) if t >= T['yes'] else ('ver', T['up2'][1] - 0.1, True)
    elif r1: key, t0, first = ('nej', T['no'], False) if t >= T['no'] else ('ver', T['no'] - 0.8, False) if t >= T['no'] - 0.8 else ('fraga', T['ask1'], True)
    for k2, objs in TXTG.items():
        for o in objs: o.hide_render = k2 != key
    for o in PILL_OBJS: o.hide_render = key is None
    PILL.location = PILL_AT + Vector((0, 0, 0.006 * math.sin(t * 1.3)))
    if key:
        x = min(1.0, (t - t0) / 0.3); s_ = 1 - (1 - x) ** 3 + 0.1 * math.sin(math.pi * x); s_ = s_ if first else 0.78 + 0.22 * s_
        if not r2: s_ *= 1 - sm(t, T['bird2_out'] + 0.2, T['bird2_out'] + 0.6)
        PILL.scale = (max(s_, 0.001),) * 3; P_(RIM_M).inputs['Emission Color'].default_value = (*COLS[key], 1)
        for i, d_ in enumerate(DOTS): k_ = 0.55 + 0.75 * max(0.0, math.sin(t * 11 - i * 1.1)); d_.scale = (k_, k_, k_)
    for o in list(CARD.values()) + [HEAD, TRAIL, TRAIL2] + [c for e in CARD.values() for c in e.children]: o.hide_render = True
    runs = [(T['up1'], 'bird', (1.0, 0.86, 0.6)), (T['down1'], None, (1.0, 0.25, 0.2)), (T['up2'], 'sq', (1.0, 0.86, 0.6)), (T['down2'], None, (0.3, 0.95, 0.5))]
    for (a_, b_), who, c_ in runs:
        if not (a_ <= t <= b_ + 0.3): continue
        u = sm(t, a_, b_) * 0.6 + 0.4 * min(1.0, (t - a_) / (b_ - a_)); fade = max(0.0, (t - b_) / 0.3); P_(SIG_M).inputs['Emission Color'].default_value = (*c_, 1)
        cv = tc_ if who else tc2; (TRAIL if who else TRAIL2).hide_render = False; cv.bevel_factor_start = min(1.0, max(0.0, u - 0.4) + fade); cv.bevel_factor_end = u
        if who and t < b_:
            e = CARD[who]; k_ = sm(u, 0.0, 0.18) * (1 - 0.75 * sm(u, 0.78, 1.0)); e.location = bez(u) + Vector((0, -0.012, 0)); e.scale = (max(k_, 0.001),) * 3; e.rotation_euler = (0, 0.5 * (1 - u) - 0.1, 0)
            for c in e.children: c.hide_render = False
        if not who and t < b_: HEAD.location = bez2(u); HEAD.hide_render = False
    # kameran: nara fatet -> helbild med hus och moln -> in mot skalen
    wide = sm(t, 9.8, 15.6); close = sm(t, 40.3, END - 0.2)
    eye = mix(mix((0.47, -1.12, 0.16), (0.32, -1.52, 0.27), wide), (0.31, -0.84, 0.2), close) + Vector((0.05 * t / END, 0, 0))
    tgt = mix(mix((0.31, -0.14, 0.075), (0.24, -0.05, 0.165), wide), (0.27, -0.14, 0.06), close)
    # overgang in: slutet av en snabb panorering at hoger (1.4 panorerar at det hall Lennart tittar). Kameran ar vriden at vanster och bromsar in pa bilden.
    # Rorelseoskarpan laggs pa efterat (verktyg/panorering_14.py).
    if FALL and t < 1.2:   # fallet: kameran aker ner med noten (noten star still i bilden) och bromsar in i den vanliga bilden strax innan noten landar
        x, y, rz, zr = NUT_REST[FK]; h = max(0.0, fall_nut(t)[0].z) if t < F_TL else 0.0; xx = h - 0.06; k_ = 0.08
        dz = max(0.0, 0.5 * (xx + math.sqrt(xx * xx + k_ * k_)) - 0.5 * (-0.06 + math.sqrt(0.06 ** 2 + k_ * k_))); c_ = min(1.0, dz / 0.25)
        tgt = mix(tgt, Vector((x, y, tgt.z)), c_) + Vector((0, 0, dz)); eye = eye + (tgt - eye) * 0.6 * c_ + Vector((0, 0, dz))
    sving = math.radians(PAN_GRAD) * max(0.0, 1 - t / PAN_TID) ** 3
    if sving > 0: tgt = eye + Matrix.Rotation(sving, 3, 'Z') @ (tgt - eye)
    # overgang ut: kameran lyfter och tittar upp forbi molnet, ut i det tomma morkret (3.1 fortsatter nerat mot Claude-fonstret)
    up = sm(t, END - 1.35, END) ** 1.4; tgt0 = tgt.copy()     # skarpan stannar pa fatet medan kameran tittar upp
    if up > 0: eye = eye + Vector((0, -0.08, 0.22)) * up; tgt = tgt + Vector((0.1, 0.25, 1.1)) * up
    CAM.location = eye; CAM.rotation_euler = (tgt - eye).to_track_quat('-Z', 'Y').to_euler(); cam_d.lens = 60 - 5 * wide; cam_d.dof.aperture_fstop = 5.6; cam_d.dof.focus_distance = (tgt0 - eye).length

frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(END * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    if FALL and f < 30:   # fallet: riktig rorelseoskarpa. Scenen raknas om vid varje delruta som Cycles fragar efter
        sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5; sc.frame_set(f); state(sc.frame_current_final / FPS)
    else: sc.render.use_motion_blur = False; state(f / FPS)
    bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
