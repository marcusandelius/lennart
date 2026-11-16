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
T = dict(pi=3.35, kamera=4.7, skarm=6.25, servo=7.3, kablar=8.4, skruvar=8.95, notter=9.4, pan=(10.3, 12.6), rullar=10.5, push=12.4, snurr=16.2)   # efter inspelningen "full recording.m4a": scenens tid = inspelningens tid - 91,7 s

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
place('kamera', camera_module((-0.125, 0.055, 0)), T['kamera'], (-0.4, 0, 0)); label('kamera', 'KAMERAMODUL', (-0.125, 0.075))
SCR, SCR_P = screen((0.135, 0.052, 0)); place('skarm', SCR, T['skarm'], (0.4, 0, 0)); label('skarm', 'LED-SKÄRM', (0.139, 0.082))
place('servo1', servo((-0.15, -0.05, 0)), T['servo'], (-0.4, 0, 0)); place('servo2', servo((-0.105, -0.05, 0)), T['servo'] + 0.2, (-0.4, 0, 0)); label('servo2', 'SERVOMOTORER', (-0.127, -0.028))
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
    place('not%d' % i, n_, T['notter'] + i * 0.06, (0.3, 0, 0))
label('not6', 'NÖTTER', (0.15, -0.092))
SPOOLS = [spool((0.5 + i * 0.215, 0.0, 0), c, 'rulle%d' % i) for i, c in enumerate([(0.635, 0.227, 0.172), (0.93, 0.92, 0.89), (0.35, 0.37, 0.38)])]
for i, s_ in enumerate(SPOOLS): place('rulle%d' % i, s_, T['rullar'] + i * 0.3, (0.75, 0, 0))
label('rulle0', 'FILAMENT', (0.5, -0.118))

wires([(-0.125, 0.044), (-0.125, 0.008), (-0.0415, 0.008)], [(i - 6.5) * 0.0011 for i in range(14)], 0.00052, [M['beige']] * 14, 0.0052, T['kablar'], T['kablar'] + 0.6, 0.012)        # kamerans flatkabel
wires([(0.103, 0.052), (0.078, 0.052), (0.078, 0.078), (-0.0085, 0.078), (-0.0085, 0.036)], [(i - 3.5) * 0.00254 for i in range(8)], 0.00075, RAINBOW, 0.0068, T['kablar'] + 0.1, T['kablar'] + 0.8, 0.012)   # skarmens ledare
wires([(-0.15, -0.062), (-0.15, -0.098), (-0.02, -0.098), (-0.02, -0.02)], [(i - 1) * 0.0013 for i in range(3)], 0.00058, SERVOW, 0.0052, T['kablar'] + 0.15, T['kablar'] + 0.8)
wires([(-0.105, -0.062), (-0.105, -0.088), (-0.012, -0.088), (-0.012, -0.02)], [(i - 1) * 0.0013 for i in range(3)], 0.00058, SERVOW, 0.0052, T['kablar'] + 0.25, T['kablar'] + 0.85)

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
    for o, t0, t1 in WIRES: o.data.bevel_factor_end = sm(t, t0, t1); o.hide_render = t <= t0
    SCR_P.inputs['Emission Strength'].default_value = 2.0 * sm(t, T['kablar'] + 0.8, T['kablar'] + 1.1)
    for i, s in enumerate(SPOOLS): s.rotation_euler = (0, 0, -3.0 * (1 - out(t, T['rullar'] + i * 0.3, T['rullar'] + 0.9 + i * 0.3)) + (2.2 * max(0, t - T['snurr']) ** 2 if i == 0 else 0))
    pan = sm(t, *T['pan']); push = sm(t, T['push'], END)
    tgt = mix((0.0, -0.025, 0.0), (0.5, 0.0, 0.03), pan); eye = mix(mix((0.0, -0.2, 0.66), (0.5, -0.3, 0.62), pan), (0.5, -0.215, 0.2), push) + Vector((0.02 * t / END, 0, -0.03 * out(t, 0, T['pan'][0], 1.5) * (1 - push)))
    hub = Vector((0.5, 0.009, 0.0625)); dive = min(1.0, max(0.0, (t - (END - 0.75)) / 0.71)) ** 2.2     # overgang ut: in i rullens svarta nav tills bilden ar svart
    if dive > 0: eye = mix(eye, hub + (eye - hub).normalized() * 0.014, dive); tgt = mix(tgt, hub, dive)
    CAM.location = eye; CAM.rotation_euler = (tgt - eye).to_track_quat('-Z', 'Y').to_euler(); cam_d.dof.aperture_fstop = 5.6 - 2.8 * push; cam_d.dof.focus_distance = (tgt - eye).length

frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(END * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    state(f / FPS); bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
