# Projekt Lennart - del 4 (klipp 4.1 och 4.2): inkopen. Varje del glider in pa det ord dar rosten namner den:
# Raspberry Pi, kameramodul, LED-skarm, servomotorer, kablar, skruvar, notter. Sedan filamentet. 16 s.
# Tiderna i T foljer den inspelade rosten.
# Kor:  blender -b -P akt_inkop.py -- <ut-mapp (absolut)> <bredd> <samples> [tider i sekunder ...]
# Komponenterna ar generiska modeller byggda for att se ratt ut (enkortsdator, kameramodul, skarm, servon), inte exakta kopior av de inkopta delarna.
import bpy, sys, os, math
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, SAMPLES, TIMES = os.path.abspath(a[0]), int(a[1]), int(a[2]), [float(x) for x in a[3:]]
os.makedirs(OUT, exist_ok=True); FPS, END = 25, 18.6
T = dict(pi=3.35, kamera=4.7, skarm=5.9, servo=6.85, kablar=8.4, skruvar=8.95, notter=9.4, pan=(10.3, 12.6), rullar=10.5, push=12.4, snurr=16.2)   # efter inspelningen "full recording.m4a": scenens tid = inspelningens tid - 91,7 s

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
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 8; sc.render.use_persistent_data = True
sc.render.resolution_x = WIDTH; sc.render.resolution_y = WIDTH * 9 // 16; sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 95
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception as e: print('look', e)
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.012, 0.015, 1)

def link(o): sc.collection.objects.link(o); return o
def mat(name, col, rough=0.5, metal=0.0, coat=0.0, trans=0.0, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal; p.inputs['Coat Weight'].default_value = coat; p.inputs['Transmission Weight'].default_value = trans
    if emit: p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = 1.0
    return m
M = dict(pcb=mat('pcb', (0.012, 0.16, 0.07), 0.4, coat=0.5), pcbk=mat('pcbk', (0.012, 0.014, 0.018), 0.4, coat=0.5), chip=mat('chip', (0.02, 0.02, 0.022), 0.35), steel=mat('steel', (0.62, 0.63, 0.65), 0.28, 1.0),
         gold=mat('gold', (0.9, 0.62, 0.2), 0.25, 1.0), blk=mat('blk', (0.012, 0.012, 0.014), 0.45), beige=mat('beige', (0.78, 0.74, 0.66), 0.5), servo=mat('servo', (0.03, 0.16, 0.6), 0.3, coat=0.3),
         white=mat('white', (0.86, 0.86, 0.84), 0.4), glass=mat('glass', (0.004, 0.005, 0.012), 0.04, 0.15, 1.0), clear=mat('clear', (0.75, 0.78, 0.8), 0.12, trans=1.0),
         label=mat('label', (0, 0, 0), 0.5, emit=(0.55, 0.8, 0.82)), cable=mat('cable', (0.015, 0.015, 0.017), 0.5))

def empty(name, loc=(0, 0, 0), parent=None): o = link(bpy.data.objects.new(name, None)); o.location = loc; o.parent = parent; return o
def box(par, size, loc, m, bevel=0.0005, rot=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=(0, 0, rot)); o = bpy.context.active_object; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); o.data.materials.append(m); o.parent = par
    if bevel: b = o.modifiers.new('b', 'BEVEL'); b.width = bevel; b.segments = 3
    return o
def cyl(par, r, h, loc, m, rot=(0, 0, 0), verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot); o = bpy.context.active_object; o.data.materials.append(m); o.parent = par
    for p in o.data.polygons: p.use_smooth = len(p.vertices) == 4
    return o

FONT = typsnitt('consola.ttf', 'Menlo.ttc', 'DejaVuSansMono.ttf'); LABELS = {}
def label(key, text, loc):
    c = bpy.data.curves.new('t', 'FONT'); c.body = text; c.font = FONT or c.font; c.size = 0.0075; c.align_x = 'CENTER'; c.space_character = 1.12; c.fill_mode = 'FRONT'; o = link(bpy.data.objects.new('t', c)); o.location = (loc[0], loc[1], 0.0003); c.materials.append(M['label']); LABELS[key] = o

# ---------- komponenter (origo i komponentens mitt, z = 0 pa underlaget) ----------
def computer(loc):
    e = empty('dator', loc); box(e, (0.085, 0.056, 0.0014), (0, 0, 0.0027), M['pcb'], 0.0003)
    box(e, (0.014, 0.014, 0.0014), (-0.012, 0.002, 0.0041), M['steel'], 0.0003); box(e, (0.011, 0.013, 0.001), (0.008, 0.002, 0.0039), M['chip'], 0.0002); box(e, (0.006, 0.006, 0.001), (-0.028, -0.012, 0.0039), M['chip'], 0.0002)
    for y in (-0.0155, 0.0035): box(e, (0.0175, 0.0145, 0.0155), (0.0365, y, 0.0112), M['steel'], 0.0006)
    box(e, (0.0205, 0.016, 0.0135), (0.035, 0.0205, 0.0102), M['steel'], 0.0006)
    box(e, (0.051, 0.0052, 0.0026), (-0.0085, 0.0245, 0.0047), M['blk'], 0.0002)
    for i in range(20):
        for j in range(2): box(e, (0.0006, 0.0006, 0.006), (-0.0326 + i * 0.00254, 0.0232 + j * 0.00254, 0.0075), M['gold'], 0)
    box(e, (0.0035, 0.022, 0.0052), (-0.0395, 0.0, 0.006), M['beige'], 0.0003); box(e, (0.009, 0.0075, 0.0032), (0.03, -0.0245, 0.005), M['steel'], 0.0008); box(e, (0.012, 0.006, 0.006), (-0.016, -0.0245, 0.0064), M['blk'], 0.0004)
    for x in (-0.039, 0.019):
        for y in (-0.0245, 0.0245): cyl(e, 0.003, 0.0002, (x, y, 0.00345), M['gold']); cyl(e, 0.00135, 0.0003, (x, y, 0.0035), M['blk'])
    return e
def camera_module(loc):
    e = empty('kamera', loc); box(e, (0.025, 0.024, 0.0012), (0, 0, 0.0024), M['pcbk'], 0.0003); box(e, (0.0085, 0.0085, 0.005), (0, 0.002, 0.0055), M['blk'], 0.0005)
    cyl(e, 0.0034, 0.0016, (0, 0.002, 0.0086), M['blk']); cyl(e, 0.0029, 0.0004, (0, 0.002, 0.0095), M['steel'])
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, 0.002, 0.0094)); g = bpy.context.active_object; g.scale = (0.0024, 0.0024, 0.001); g.data.materials.append(M['glass']); g.parent = e
    for p in g.data.polygons: p.use_smooth = True
    box(e, (0.019, 0.0035, 0.003), (0, -0.0098, 0.0045), M['beige'], 0.0003)
    for x in (-0.0105, 0.0105):
        for y in (-0.0065, 0.006): cyl(e, 0.0019, 0.0002, (x, y, 0.00305), M['gold']); cyl(e, 0.001, 0.0003, (x, y, 0.0031), M['blk'])
    return e
def screen(loc):
    e = empty('skarm', loc); box(e, (0.072, 0.046, 0.0016), (0, 0, 0.0028), M['pcbk'], 0.0003); box(e, (0.054, 0.041, 0.0022), (0.004, 0, 0.0047), M['chip'], 0.0004)
    m = bpy.data.materials.new('scr'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']; t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(os.path.join(ROOT, 'skarm-vantar.png'))
    nt.links.new(t.outputs['Color'], p.inputs['Emission Color']); p.inputs['Base Color'].default_value = (0.004, 0.006, 0.005, 1); p.inputs['Roughness'].default_value = 0.15; p.inputs['Emission Strength'].default_value = 0.0
    me = bpy.data.meshes.new('bild'); w, h = 0.049, 0.0362; me.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)]); me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): me.uv_layers[0].data[i].uv = c
    me.materials.append(m); o = link(bpy.data.objects.new('bild', me)); o.location = (0.004, 0, 0.0059); o.parent = e
    box(e, (0.0052, 0.0215, 0.0026), (-0.0315, 0, 0.0049), M['blk'], 0.0002)
    for i in range(8): box(e, (0.0006, 0.0006, 0.005), (-0.0315, -0.0089 + i * 0.00254, 0.0072), M['gold'], 0)
    return e, p
def servo(loc):
    e = empty('servo', loc); box(e, (0.0228, 0.0122, 0.0225), (0, 0, 0.01125), M['servo'], 0.0008); box(e, (0.0325, 0.0122, 0.0025), (0, 0, 0.0175), M['servo'], 0.0006)
    cyl(e, 0.0058, 0.004, (0.0055, 0, 0.0245), M['servo']); cyl(e, 0.0024, 0.0035, (0.0055, 0, 0.028), M['white']); box(e, (0.021, 0.0052, 0.0016), (0.0055 + 0.0062, 0, 0.0302), M['white'], 0.0007)
    for x in (-0.0138, 0.0138): cyl(e, 0.0011, 0.0027, (x, 0, 0.0176), M['blk'])
    return e
def power(loc):
    e = empty('strom', loc)
    for i in range(4): bpy.ops.mesh.primitive_torus_add(major_radius=0.026 - i * 0.0008, minor_radius=0.0016, major_segments=96, minor_segments=12, location=(0, 0, 0.0016 + i * 0.0031)); o = bpy.context.active_object; o.data.materials.append(M['cable']); o.parent = e; [setattr(p, 'use_smooth', True) for p in o.data.polygons]
    return e
def screw(loc):
    e = empty('skruv', loc); cyl(e, 0.0011, 0.0085, (0, 0, 0.0022), M['steel'], (math.pi / 2, 0, 0), 24); cyl(e, 0.0022, 0.0016, (0, 0.005, 0.0022), M['steel'], (math.pi / 2, 0, 0), 24); return e
def spool(loc, col, name):
    e = empty(name, loc); fm = bpy.data.materials.new('fil_' + name); fm.use_nodes = True; nt = fm.node_tree; p = nt.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = 0.38
    tcn = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.rings_direction = 'Z'; wv.inputs['Scale'].default_value = 2 * math.pi / (20 * 0.00175); bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 1.0; bm.inputs['Distance'].default_value = 0.0008
    mr = nt.nodes.new('ShaderNodeMixRGB'); mr.blend_type = 'MULTIPLY'; mr.inputs['Fac'].default_value = 0.55; mr.inputs['Color1'].default_value = (*col, 1); nt.links.new(wv.outputs['Color'], mr.inputs['Color2']); nt.links.new(mr.outputs[0], p.inputs['Base Color'])
    nt.links.new(tcn.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], p.inputs['Normal'])
    cyl(e, 0.088, 0.054, (0, 0, 0.031), fm, verts=128); cyl(e, 0.1, 0.003, (0, 0, 0.0025), M['clear'], verts=128); cyl(e, 0.1, 0.003, (0, 0, 0.0595), M['clear'], verts=128)
    cyl(e, 0.03, 0.0605, (0, 0, 0.0312), M['blk'], verts=64); cyl(e, 0.0265, 0.0008, (0, 0, 0.0617), M['chip'], verts=64)
    cyl(e, 0.012, 0.0006, (0, 0, 0.0622), M['blk'], verts=48); box(e, (0.02, 0.003, 0.0008), (0.0, 0.0, 0.0622), M['steel'], 0.0003)
    return e

# ---------- sladdar: parallella ledare langs en rak bana med rundade horn ----------
def wire_paths(path, offs, R=0.006, n=8):
    path = [Vector(p) for p in path]; out = []
    for d in offs:
        pts = []
        for i, p in enumerate(path):
            if i == 0 or i == len(path) - 1:
                s = (path[1] - path[0]) if i == 0 else (path[-1] - path[-2]); s.normalize(); pts.append([p + Vector((-s.y, s.x)) * d]); continue
            d1 = (p - path[i - 1]).normalized(); d2 = (path[i + 1] - p).normalized(); n1 = Vector((-d1.y, d1.x)); n2 = Vector((-d2.y, d2.x)); q = p + (n1 + n2) * d / (1 + n1.dot(n2))
            turn = 1 if d1.x * d2.y - d1.y * d2.x > 0 else -1; r = max(0.0009, R - d * turn); ang = math.acos(max(-1, min(1, d1.dot(d2)))); tl = r * math.tan(ang / 2); c = q - d1 * tl + n1 * turn * r; a0 = math.atan2((q - d1 * tl - c).y, (q - d1 * tl - c).x)
            pts.append([c + Vector((math.cos(a0 + turn * ang * k / n), math.sin(a0 + turn * ang * k / n))) * r for k in range(n + 1)])
        out.append([v for g in pts for v in g])
    return out
WIRES = []
def wires(path, offs, radius, mats, z, t0, t1, R=0.006):
    for pts, m in zip(wire_paths(path, offs, R), mats):
        c = bpy.data.curves.new('w', 'CURVE'); c.dimensions = '3D'; s = c.splines.new('POLY'); s.points.add(len(pts) - 1)
        for i, v in enumerate(pts): s.points[i].co = (v.x, v.y, z, 1)
        c.bevel_depth = radius; c.bevel_resolution = 3; c.use_fill_caps = True; c.materials.append(m); c.bevel_factor_end = 0.0; o = link(bpy.data.objects.new('w', c)); WIRES.append((o, t0, t1))
RAINBOW = [mat('w%d' % i, c, 0.45) for i, c in enumerate([(0.25, 0.1, 0.03), (0.7, 0.04, 0.03), (0.85, 0.3, 0.03), (0.85, 0.7, 0.05), (0.08, 0.45, 0.1), (0.04, 0.15, 0.6), (0.3, 0.08, 0.5), (0.35, 0.35, 0.36)])]
SERVOW = [RAINBOW[0], RAINBOW[1], RAINBOW[2]]

# ---------- uppstallning ----------
bpy.ops.mesh.primitive_plane_add(size=6, location=(0.3, 0, 0)); bpy.context.active_object.data.materials.append(mat('yta', (0.008, 0.042, 0.055), 0.42))
P = {}   # namn -> (objekt, viloplats, starttid, riktning in i bild)
def place(key, obj, t0, frm): P[key] = (obj, Vector(obj.location), t0, Vector(frm))
place('dator', computer((0, 0.008, 0)), T['pi'], (0, 0.45, 0)); label('dator', 'RASPBERRY PI', (-0.082, -0.012))
place('kamera', camera_module((-0.125, 0.055, 0)), T['kamera'], (-0.4, 0, 0.3))   # in ovanfor sakerna i kanten; label('kamera', 'KAMERAMODUL', (-0.125, 0.075))
SCR, SCR_P = screen((0.135, 0.052, 0)); place('skarm', SCR, T['skarm'], (0.4, 0, 0.3)); label('skarm', 'LED-SKÄRM', (0.139, 0.082))
place('servo1', servo((-0.168, -0.05, 0)), T['servo'], (-0.4, 0, 0.3)); S2 = servo((-0.096, -0.048, 0)); S2.scale = (1.75, 1.75, 1.75); place('servo2', S2, T['servo'] + 0.2, (-0.4, 0, 0.3)); label('servo2', 'SERVOMOTORER', (-0.132, -0.022))   # en mikroservo och en storre
label('kablar', 'KABLAR', (0.035, 0.094))
for i in range(10): place('skruv%d' % i, screw((-0.054 + i * 0.012, -0.128, 0)), T['skruvar'] + i * 0.04, (0, -0.3, 0))
label('skruv9', 'SKRUVAR', (0, -0.147))
# hasselnotter: en liten hog
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
n0.data.materials.append(nm)
NUTP = [(0.0, 0.0, 35), (0.019, 0.004, 110), (-0.018, 0.007, 250), (0.008, -0.017, 180), (-0.011, -0.014, 70), (0.028, -0.013, 300), (-0.03, -0.008, 150)]
for i, (dx, dy, rz) in enumerate(NUTP):
    n_ = n0 if i == 0 else link(bpy.data.objects.new('not%d' % i, n0.data)); n_.scale = (0.0085,) * 3; n_.rotation_euler = (math.radians(68 + (i * 37) % 30), 0, math.radians(rz)); n_.location = (0.15 + dx, -0.055 + dy, 0.008)
    place('not%d' % i, n_, T['notter'] + i * 0.06, (0, -0.3, 0))   # nedifran, sa att de inte glider over sakerna i hogerkanten
label('not6', 'NÖTTER', (0.15, -0.092))
# filamentet som kopts: rod, gron, vit, gra och svart. Den roda (stugans farg) ligger forst, och det ar i dess nav kameran aker in i slutet
SPOOLS = [spool(p, c, 'rulle%d' % i) for i, (p, c) in enumerate([((0.5, 0.0, 0), (0.635, 0.227, 0.172)), ((0.72, 0.0, 0), (0.07, 0.38, 0.13)), ((0.61, 0.212, 0), (0.93, 0.92, 0.89)),
                                                                  ((0.94, 0.0, 0), (0.13, 0.14, 0.15)), ((0.83, 0.212, 0), (0.025, 0.025, 0.028))])]
for i, s_ in enumerate(SPOOLS): place('rulle%d' % i, s_, T['rullar'] + i * 0.3, (0.75, 0, 0))
label('rulle0', 'FILAMENT', (0.72, -0.118))

# ---------- "en hel del grejer": det som ocksa kopts men inte namns, generiska modeller langs bordets kanter. De landar under forsta meningen ----------
def ljusring(loc):
    e = empty('ljusring', loc); bpy.ops.mesh.primitive_torus_add(major_radius=0.0125, minor_radius=0.0045, major_segments=64, minor_segments=8, location=(0, 0, 0.0008)); o = bpy.context.active_object; o.scale = (1, 1, 0.16); o.data.materials.append(M['pcbk']); o.parent = e
    led = mat('lysdiod', (0.95, 0.86, 0.55), 0.2, emit=(1.0, 0.85, 0.5))
    for i in range(12): a = 2 * math.pi * i / 12; box(e, (0.0032, 0.0032, 0.0012), (0.0125 * math.cos(a), 0.0125 * math.sin(a), 0.0019), led, 0.0004, a)
    box(e, (0.006, 0.0035, 0.0028), (0, -0.0185, 0.0016), M['white'], 0.0004)
    return e
def kamerakabel(loc):
    e = empty('kamerakabel', loc); stark = mat('forstarkning', (0.05, 0.2, 0.65), 0.4)
    for i in range(3):
        box(e, (0.036, 0.011, 0.0005), (0, (i - 1) * 0.0045, 0.0004 + i * 0.0006), M['beige'], 0.0002)
        cyl(e, 0.0003 + 0.0003 * i, 0.011, ((0.018 if i % 2 == 0 else -0.018), (i - 0.5) * 0.0045, 0.0007 + i * 0.0006), M['beige'], (math.pi / 2, 0, 0), 16)
    box(e, (0.006, 0.0112, 0.0009), (-0.015, -0.0045, 0.0009), stark, 0.0002); box(e, (0.006, 0.0112, 0.0009), (0.015, 0.0045, 0.0021), stark, 0.0002)
    return e
KOND = mat('kondensator', (0.02, 0.03, 0.09), 0.35, coat=0.4)
def kondensatorer(loc):
    e = empty('kondensatorer', loc)
    for k, x in enumerate((-0.0065, 0.0065)):
        cyl(e, 0.005, 0.016, (x, 0, 0.005), KOND, (math.pi / 2, 0, 0)); cyl(e, 0.0049, 0.0012, (x, 0.0083, 0.005), M['steel'], (math.pi / 2, 0, 0))
        for dx in (-0.0018, 0.0018): cyl(e, 0.0003, 0.012, (x + dx, -0.014, 0.004), M['steel'], (math.pi / 2, 0, 0), 12)
    return e
def kabelgenomforingar(loc):
    e = empty('kabelgenomforingar', loc)
    for x, y in ((-0.011, 0.007), (0.011, 0.007)): cyl(e, 0.0105, 0.004, (x, y, 0.002), M['blk'], verts=6); cyl(e, 0.0085, 0.009, (x, y, 0.0085), M['blk'], verts=32); cyl(e, 0.0042, 0.0016, (x, y, 0.0136), M['chip'], verts=32)
    ligg = empty('liggande', (0.0, -0.014, 0.0105), e); ligg.rotation_euler = (math.pi / 2, 0, 0.35)
    cyl(ligg, 0.0105, 0.004, (0, 0, -0.008), M['blk'], verts=6); cyl(ligg, 0.0085, 0.009, (0, 0, -0.0015), M['blk'], verts=32); cyl(ligg, 0.0042, 0.0016, (0, 0, 0.0036), M['chip'], verts=32)
    return e
# tuberna (superlim och silikon): vit tub som plattas ut mot en vikt ande, rafflad vit skruvkork, och en liten tryckt etikett utan marke
def tubetikett(namn, falt, romber):   # etiketten runt tuben: ett fargat falt, roda varningsromber och gra smatext. Bildens x = langs tuben, y = runt tuben (0,25 = ovansidan)
    import numpy as np
    W_, H_ = 512, 256; px = np.ones((H_, W_, 4), np.float32); px[..., :3] = (0.9, 0.9, 0.88); yy, xx = np.mgrid[0:H_, 0:W_]
    for (u0, u1, v0, v1, col) in falt: px[(xx >= u0 * W_) & (xx <= u1 * W_) & (yy >= v0 * H_) & (yy <= v1 * H_)] = (*col, 1)
    for cx in romber:
        cy = int(0.25 * H_); d = np.abs(xx - cx) + np.abs(yy - cy); R = 15
        px[d <= R] = (0.95, 0.95, 0.93, 1); px[(d <= R) & (d >= R - 3)] = (0.8, 0.05, 0.04, 1)
        px[(np.abs(xx - cx) <= 2) & (yy >= cy - 3) & (yy <= cy + 7)] = (0.02, 0.02, 0.02, 1); px[(np.abs(xx - cx) <= 2) & (yy >= cy - 8) & (yy <= cy - 5)] = (0.02, 0.02, 0.02, 1)
    for r_, (x0, x1) in enumerate([(150, 450), (150, 420), (150, 440), (150, 300)]):    # smatext pa sidan mot kameran
        y = int(0.31 * H_) + r_ * 6; px[(yy >= y) & (yy <= y + 1) & (xx >= x0) & (xx <= x1)] = (0.22, 0.22, 0.24, 1)
    img = bpy.data.images.new(namn, W_, H_, alpha=True); img.pixels = px.ravel(); img.pack(); return img
TUB_TYPSNITT = typsnitt('segoeuib.ttf', 'Helvetica.ttc', 'DejaVuSans-Bold.ttf')
def tub(namn, loc, L, r, etikett, text, storlek, textfarg):
    e = empty(namn, loc); N, S = 48, 28; vs, uvs, fs = [], [], []
    for a_ in range(S + 1):
        u = a_ / S; f = u ** 1.6; A, B = r * (1 + 0.5 * f), r * (1 - 0.9 * f); x = u * L
        for b_ in range(N + 1):
            th = 2 * math.pi * b_ / N; vs.append((x, A * math.cos(th), B * math.sin(th) + B)); uvs.append((u, b_ / N))
    for a_ in range(S):
        for b_ in range(N): k = a_ * (N + 1) + b_; fs.append((k, k + N + 1, k + N + 2, k + 1))
    me = bpy.data.meshes.new(namn); me.from_pydata(vs, [], fs); me.uv_layers.new(); uv = me.uv_layers[0].data
    for li, l in enumerate(me.loops): uv[li].uv = uvs[l.vertex_index]
    for p in me.polygons: p.use_smooth = True
    m = bpy.data.materials.new(namn + '_tub'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']; t = nt.nodes.new('ShaderNodeTexImage'); t.image = etikett
    nt.links.new(t.outputs['Color'], p.inputs['Base Color']); p.inputs['Roughness'].default_value = 0.32; p.inputs['Metallic'].default_value = 0.15
    me.materials.append(m); kropp = link(bpy.data.objects.new(namn + '_kropp', me)); kropp.parent = e
    vit = mat(namn + '_vit', (0.9, 0.9, 0.88), 0.3, 0.15)
    box(e, (0.006, 2 * r * 1.5, 0.0012), (L + 0.0025, 0, 0.0008 + r * 0.1), vit, 0.0004)                     # den vikta anden
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=r, radius2=r * 0.55, depth=r * 0.35, location=(-r * 0.17, 0, r), rotation=(0, -math.pi / 2, 0)); k = bpy.context.active_object; k.data.materials.append(vit); k.parent = e
    for v in k.data.polygons: v.use_smooth = True
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r * 0.6, depth=r * 0.95, location=(-r * 0.35 - r * 0.47, 0, r), rotation=(0, math.pi / 2, 0)); c = bpy.context.active_object
    for vi, v in enumerate(c.data.vertices):                                                                   # raffling: varannan kant lite indragen
        if (vi // 2) % 2: v.co.x *= 0.92; v.co.y *= 0.92
    c.data.materials.append(mat(namn + '_kork', (0.95, 0.95, 0.93), 0.45)); c.parent = e
    # texten som sager vad det ar: platt text ovanfor tuben, projicerad ner pa den rundade ytan
    cu = bpy.data.curves.new(namn + '_text', 'FONT'); cu.body = text; cu.font = TUB_TYPSNITT or cu.font; cu.size = storlek; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.space_character = 1.05
    cu.materials.append(mat(namn + '_textfarg', textfarg, 0.5)); to = link(bpy.data.objects.new(namn + '_text', cu)); to.parent = e; to.location = (0.47 * L, -0.0006 * r / 0.0055, 2 * r + 0.004)
    bpy.context.view_layer.objects.active = to; to.select_set(True); bpy.ops.object.convert(target='MESH'); to = bpy.context.active_object; to.select_set(False)
    sw = to.modifiers.new('ner', 'SHRINKWRAP'); sw.target = kropp; sw.wrap_method = 'PROJECT'; sw.use_project_z = True; sw.use_negative_direction = True; sw.use_positive_direction = False; sw.offset = 0.00012
    return e
SUPERLIM_ETIKETT = tubetikett('etikett_superlim', [(0.1, 0.92, 0.12, 0.17, (0.78, 0.06, 0.05)), (0.1, 0.92, 0.33, 0.38, (0.78, 0.06, 0.05))], [52, 84])
SILIKON_ETIKETT = tubetikett('etikett_silikon', [(0.1, 0.9, 0.0, 1.0, (0.95, 0.74, 0.08))], [56])
def superlim(loc): return tub('superlim', loc, 0.034, 0.0055, SUPERLIM_ETIKETT, 'SUPERLIM', 0.0042, (0.05, 0.05, 0.06))
def silikon(loc): return tub('silikon', loc, 0.07, 0.011, SILIKON_ETIKETT, 'SILIKON', 0.0072, (0.05, 0.05, 0.06))
def kylare(loc):
    e = empty('kylare', loc); alu = mat('aluminium', (0.55, 0.56, 0.58), 0.35, 1.0); box(e, (0.03, 0.03, 0.002), (0, 0, 0.001), alu, 0.0003)
    for i in range(9): box(e, (0.0012, 0.03, 0.006), (-0.0135 + i * 0.0034, 0, 0.005), alu, 0.0001)
    cyl(e, 0.0115, 0.0012, (0.002, 0, 0.0084), M['blk']); cyl(e, 0.004, 0.0014, (0.002, 0, 0.0088), M['chip'])
    return e
def omvandlare(loc, col):
    e = empty('omvandlare', loc); pcb = mat('omv%.2f' % col[2], col, 0.4, coat=0.5); box(e, (0.032, 0.019, 0.0014), (0, 0, 0.0007), pcb, 0.0003)
    box(e, (0.009, 0.009, 0.0055), (-0.004, 0, 0.0042), M['chip'], 0.0008); box(e, (0.004, 0.003, 0.001), (0.006, 0.004, 0.0019), M['chip'], 0.0002)
    for x in (-0.0125, 0.0125): box(e, (0.006, 0.01, 0.0075), (x, 0, 0.0052), mat('plint', (0.03, 0.18, 0.5), 0.4), 0.0005)
    return e
def dckontakt(loc):
    e = empty('dckontakt', loc); cyl(e, 0.0042, 0.016, (-0.004, 0, 0.0042), M['blk'], (0, math.pi / 2, 0)); box(e, (0.009, 0.01, 0.009), (0.008, 0, 0.0045), mat('gronplint', (0.05, 0.32, 0.12), 0.45), 0.0006)
    return e
def servotestare(loc):
    e = empty('servotestare', loc); box(e, (0.03, 0.024, 0.0014), (0, 0, 0.0007), M['pcb'], 0.0003); cyl(e, 0.005, 0.006, (0.006, 0.002, 0.0044), M['white']); cyl(e, 0.0012, 0.0045, (0.006, 0.002, 0.0085), M['white'])
    box(e, (0.012, 0.0026, 0.006), (-0.007, -0.008, 0.0044), M['blk'], 0.0002); box(e, (0.004, 0.004, 0.002), (-0.008, 0.006, 0.0024), M['white'], 0.0004)
    return e
GREJER = [('ljusring', ljusring((-0.218, 0.075, 0)), -1), ('kamerakabel', kamerakabel((-0.218, 0.033, 0)), -1), ('kondensatorer', kondensatorer((-0.218, -0.007, 0)), -1),
          ('kylare', kylare((0.222, 0.075, 0)), 1), ('omvandlare1', omvandlare((0.222, 0.036, 0), (0.012, 0.16, 0.07)), 1), ('omvandlare2', omvandlare((0.222, 0.0, 0), (0.02, 0.05, 0.3)), 1),
          ('kabelgenomforingar', kabelgenomforingar((-0.218, -0.05, 0)), -1), ('dckontakt', dckontakt((0.224, -0.036, 0)), 1), ('servotestare', servotestare((0.222, -0.074, 0)), 1),
          ('superlim', superlim((-0.214, -0.097, 0)), -1), ('silikon', silikon((-0.15, -0.128, 0)), -1)]
for i, (key, obj, sida) in enumerate(GREJER): place(key, obj, 0.6 + 0.2 * i, (0.3 * sida, 0, 0))

wires([(-0.125, 0.044), (-0.125, 0.008), (-0.0415, 0.008)], [(i - 6.5) * 0.0011 for i in range(14)], 0.00052, [M['beige']] * 14, 0.0052, T['kablar'], T['kablar'] + 0.6, 0.012)        # kamerans flatkabel
wires([(0.103, 0.052), (0.078, 0.052), (0.078, 0.078), (-0.0085, 0.078), (-0.0085, 0.036)], [(i - 3.5) * 0.00254 for i in range(8)], 0.00075, RAINBOW, 0.0068, T['kablar'] + 0.1, T['kablar'] + 0.8, 0.012)   # skarmens ledare
wires([(-0.168, -0.062), (-0.168, -0.098), (-0.011, -0.098), (-0.011, -0.02)], [(i - 1) * 0.0013 for i in range(3)], 0.00058, SERVOW, 0.0052, T['kablar'] + 0.15, T['kablar'] + 0.8)   # yttre sladden till den yttre stiften, sa att de inte korsar varandra
wires([(-0.096, -0.066), (-0.096, -0.088), (-0.021, -0.088), (-0.021, -0.02)], [(i - 1) * 0.0013 for i in range(3)], 0.00058, SERVOW, 0.0052, T['kablar'] + 0.25, T['kablar'] + 0.85)

# ---------- konturer: under den forsta meningen ritas en streckad kontur upp dar varje del ska landa. Nar delen landar lyser konturen till och tonar ner ----------
bpy.context.view_layer.update()
def fotavtryck(keys, pad=0.004):
    ps = [c.matrix_world @ Vector(v) for k in keys for c in [P[k][0]] + list(P[k][0].children_recursive) if c.type == 'MESH' for v in c.bound_box]
    return min(p.x for p in ps) - pad, min(p.y for p in ps) - pad, max(p.x for p in ps) + pad, max(p.y for p in ps) + pad
def kontur(namn, rect, r=0.003, streck=0.003, lucka=0.002, bredd=0.0006):
    x0, y0, x1, y1 = rect; pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):   # rundade horn, moturs
        for i in range(7): a = math.radians(a0 + 15 * i); pts.append(Vector((cx + r * math.cos(a), cy + r * math.sin(a))))
    pts.append(pts[0]); L = [0.0]
    for i in range(1, len(pts)): L.append(L[-1] + (pts[i] - pts[i - 1]).length)
    def at(s):
        for i in range(1, len(pts)):
            if L[i] >= s: u = (s - L[i - 1]) / max(L[i] - L[i - 1], 1e-9); return pts[i - 1].lerp(pts[i], u)
        return pts[-1]
    vs, fs, uvs = [], [], []; s = 0.0
    while s < L[-1] - 1e-6:
        e = min(s + streck, L[-1]); a, b = at(s), at(e); d = (b - a).normalized() if (b - a).length > 1e-9 else Vector((1, 0)); n = Vector((-d.y, d.x)) * bredd / 2
        k = len(vs); vs += [(a.x - n.x, a.y - n.y, 0.00025), (b.x - n.x, b.y - n.y, 0.00025), (b.x + n.x, b.y + n.y, 0.00025), (a.x + n.x, a.y + n.y, 0.00025)]; fs.append((k, k + 1, k + 2, k + 3))
        uvs += [s / L[-1]] * 4; s = e + lucka
    me = bpy.data.meshes.new(namn); me.from_pydata(vs, [], fs); me.uv_layers.new(); uv = me.uv_layers[0].data
    for i, l in enumerate(me.loops): uv[i].uv = (uvs[l.vertex_index], 0)
    m = bpy.data.materials.new(namn); m.use_nodes = True; nt = m.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF']); outp = nt.nodes['Material Output']
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.55, 0.8, 0.82, 1); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    tc = nt.nodes.new('ShaderNodeUVMap'); sx = nt.nodes.new('ShaderNodeSeparateXYZ'); lt = nt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.0
    nt.links.new(tc.outputs['UV'], sx.inputs[0]); nt.links.new(sx.outputs['X'], lt.inputs[0]); nt.links.new(lt.outputs[0], mx.inputs['Fac']); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], outp.inputs['Surface'])
    me.materials.append(m); link(bpy.data.objects.new(namn, me)); return lt.inputs[1], em.inputs['Strength']
KONTURER = []   # (hur langt den ritats, styrka, tid da den borjar ritas, tid da delen landar)
for i, (keys, t_land) in enumerate([(['dator'], T['pi']), (['kamera'], T['kamera']), (['skarm'], T['skarm']), (['servo1'], T['servo']), (['servo2'], T['servo'] + 0.2),
                                    (['skruv%d' % j for j in range(10)], T['skruvar']), (['not%d' % j for j in range(7)], T['notter'])]):
    KONTURER.append((*kontur('kontur%d' % i, fotavtryck(keys)), 0.55 + 0.32 * i, t_land + 0.45))

def light(loc, target, power, size, col):
    d = bpy.data.lights.new('l', 'AREA'); d.energy = power; d.size = size; d.color = col; o = link(bpy.data.objects.new('l', d)); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
light((-0.5, 0.45, 0.8), (0.1, 0, 0), 13, 0.9, (1, 0.95, 0.88)); light((1.1, -0.5, 0.35), (0.4, 0, 0), 9, 0.4, (0.45, 0.7, 0.9))
cam_d = bpy.data.cameras.new('cam'); CAM = link(bpy.data.objects.new('cam', cam_d)); sc.camera = CAM; cam_d.clip_start = 0.01; cam_d.dof.use_dof = True; cam_d.lens = 50

def sm(t, a, b): x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)
def out(t, a, b, p=3.0): x = min(1, max(0, (t - a) / (b - a))); return 1 - (1 - x) ** p
def mix(p, q, k): return Vector(p) + (Vector(q) - Vector(p)) * k
def state(t):
    for key, (o, rest, t0, frm) in P.items():
        o.location = rest + frm * (1 - out(t, t0, t0 + 0.45)); vis = t >= t0
        for c in [o] + list(o.children_recursive): c.hide_render = not vis
        if key in LABELS: LABELS[key].hide_render = t < t0 + 0.3
    LABELS['kablar'].hide_render = t < T['kablar'] + 0.3
    for ritad, styrka, t0, t_land in KONTURER:
        ritad.default_value = 1.001 * out(t, t0, t0 + 0.8, 2.0)                                    # strecken ritas runt konturen
        blink = math.exp(-max(0.0, t - t_land) * 6.0) if t >= t_land else 0.0                      # lyser till nar delen landar
        styrka.default_value = 0.55 * (1 - 0.6 * sm(t, t_land, t_land + 0.8)) + 2.2 * blink
    for o, t0, t1 in WIRES: o.data.bevel_factor_end = sm(t, t0, t1); o.hide_render = t <= t0
    SCR_P.inputs['Emission Strength'].default_value = 2.0 * sm(t, T['kablar'] + 0.8, T['kablar'] + 1.1)
    for i, s in enumerate(SPOOLS): s.rotation_euler = (0, 0, -3.0 * (1 - out(t, T['rullar'] + i * 0.3, T['rullar'] + 0.9 + i * 0.3)) + (2.2 * max(0, t - T['snurr']) ** 2 if i == 0 else 0))
    pan = sm(t, *T['pan']); push = sm(t, T['push'], END)
    vid = 1.13 - 0.05 * sm(t, 0.0, T['pan'][0]); e0 = Vector((0.0, -0.025, 0.0)) + Vector((0.0, -0.175, 0.66)) * vid
    # panoreringen landar over alla fem rullarna, sedan aker kameran in mot den roda
    tgt = mix(mix((0.0, -0.025, 0.0), (0.7, 0.06, 0.03), pan), (0.5, 0.0, 0.03), push); eye = mix(mix(e0, (0.7, -0.43, 0.98), pan), (0.5, -0.215, 0.2), push) + Vector((0.02 * t / END, 0, -0.03 * out(t, 0, T['pan'][0], 1.5) * (1 - push)))
    hub = Vector((0.5, 0.009, 0.0625)); dive = min(1.0, max(0.0, (t - (END - 0.75)) / 0.71)) ** 2.2     # overgang ut: in i rullens svarta nav tills bilden ar svart
    if dive > 0: eye = mix(eye, hub + (eye - hub).normalized() * 0.014, dive); tgt = mix(tgt, hub, dive)
    CAM.location = eye; CAM.rotation_euler = (tgt - eye).to_track_quat('-Z', 'Y').to_euler(); cam_d.dof.aperture_fstop = 5.6 - 2.8 * push; cam_d.dof.focus_distance = (tgt - eye).length

frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(END * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    state(f / FPS); bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
