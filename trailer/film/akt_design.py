# Projekt Lennart - del 3: designen. Ett Claude-fonster projicerar ritningen pa ett papper, och huset reser sig ur ritningen.
# Kor:  blender -b -P akt_design.py -- <ut-mapp (absolut)> <bredd> <samples> [tider i sekunder ...]
# Kraver film/ritning.png (gors av ritning.py + ffmpeg).
import bpy, sys, os, math
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, SAMPLES, TIMES = os.path.abspath(a[0]), int(a[1]), int(a[2]), [float(x) for x in a[3:]]
os.makedirs(OUT, exist_ok=True); FPS, END = 25, 20.0; GROUND = -0.037
FRAGA = 'Hjälp mig rita ett hus åt Lennart. Han är en\nekorre och vill ha sina nötter ifred.'; SVAR = 'Absolut. Här är ett första utkast:'

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
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; wn = sc.world.node_tree; bgn = wn.nodes['Background']
tc = wn.nodes.new('ShaderNodeTexCoord'); sub = wn.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0)
s2 = wn.nodes.new('ShaderNodeVectorMath'); s2.operation = 'MULTIPLY'; s2.inputs[1].default_value = (1.0, 0.62, 0); ln = wn.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
ramp = wn.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'EASE'; e0, e1 = ramp.color_ramp.elements; e0.position = 0.0; e0.color = (0.012, 0.038, 0.045, 1); e1.position = 0.66; e1.color = (0.0015, 0.003, 0.006, 1)
lp = wn.nodes.new('ShaderNodeLightPath'); wn.links.new(tc.outputs['Window'], sub.inputs[0]); wn.links.new(sub.outputs[0], s2.inputs[0]); wn.links.new(s2.outputs[0], ln.inputs[0]); wn.links.new(ln.outputs['Value'], ramp.inputs['Fac'])
wn.links.new(ramp.outputs['Color'], bgn.inputs['Color']); wn.links.new(lp.outputs['Is Camera Ray'], bgn.inputs['Strength'])

def link(o): sc.collection.objects.link(o); return o
def mat(name, col, rough=0.5, coat=0.0, emit=None, es=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = rough; p.inputs['Coat Weight'].default_value = coat
    if emit: p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = es
    return m
def P_(m): return m.node_tree.nodes['Principled BSDF']

# ---------- huset: genomskinligt ovanfor RISE, lera under, farg under COL ----------
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, 'lennarts-matstation.glb'))
PARTS = {o.name: o for o in bpy.data.objects if o.type == 'MESH'}; RISES, COLS = [], []
def wrap(m):
    nt = m.node_tree; outn = [x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL'][0]; src = outn.inputs['Surface'].links[0].from_socket
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Position'], sep.inputs[0]); R = nt.nodes.new('ShaderNodeValue'); C = nt.nodes.new('ShaderNodeValue'); RISES.append(R); COLS.append(C)
    def front(v, soft):
        lo = nt.nodes.new('ShaderNodeMath'); lo.operation = 'SUBTRACT'; lo.inputs[1].default_value = soft; mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0; mr.inputs['To Max'].default_value = 1
        nt.links.new(v.outputs[0], lo.inputs[0]); nt.links.new(sep.outputs['Z'], mr.inputs['Value']); nt.links.new(v.outputs[0], mr.inputs['From Min']); nt.links.new(lo.outputs[0], mr.inputs['From Max']); return mr
    def band(v, col, k):
        f1, f2 = front(v, 0.003), front(v, 0.02); b = nt.nodes.new('ShaderNodeMath'); b.operation = 'SUBTRACT'; nt.links.new(f1.outputs[0], b.inputs[0]); nt.links.new(f2.outputs[0], b.inputs[1])
        g = nt.nodes.new('ShaderNodeMath'); g.operation = 'MULTIPLY'; g.inputs[1].default_value = k; nt.links.new(b.outputs[0], g.inputs[0]); e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*col, 1); nt.links.new(g.outputs[0], e.inputs['Strength']); return f1, e
    fr, gr = band(R, (0.45, 0.9, 1.0), 3.0); fc, gc = band(C, (1.0, 0.42, 0.18), 1.8)
    clay = nt.nodes.new('ShaderNodeBsdfPrincipled'); clay.inputs['Base Color'].default_value = (0.62, 0.62, 0.64, 1); clay.inputs['Roughness'].default_value = 0.65
    m1 = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(fc.outputs[0], m1.inputs[0]); nt.links.new(clay.outputs[0], m1.inputs[1]); nt.links.new(src, m1.inputs[2])
    a1 = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(m1.outputs[0], a1.inputs[0]); nt.links.new(gr.outputs[0], a1.inputs[1]); a2 = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(a1.outputs[0], a2.inputs[0]); nt.links.new(gc.outputs[0], a2.inputs[1])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(fr.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(a2.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], outn.inputs['Surface'])
_done = set()
for o in PARTS.values():
    for m in o.data.materials:
        if m and m.name not in _done: _done.add(m.name); wrap(m)

def quad_mesh(w, h, z0=0.0):
    me = bpy.data.meshes.new('q'); me.from_pydata([(-w / 2, 0, z0), (w / 2, 0, z0), (w / 2, 0, z0 + h), (-w / 2, 0, z0 + h)], [], [(0, 1, 2, 3)]); me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): me.uv_layers[0].data[i].uv = c
    return me
scr = bpy.data.materials.new('scr'); scr.use_nodes = True; sp = P_(scr); st = scr.node_tree.nodes.new('ShaderNodeTexImage'); st.image = bpy.data.images.load(os.path.join(ROOT, 'skarm-vantar.png'))
scr.node_tree.links.new(st.outputs['Color'], sp.inputs['Emission Color']); sp.inputs['Base Color'].default_value = (0.004, 0.006, 0.005, 1); sp.inputs['Roughness'].default_value = 0.2
sm_ = quad_mesh(0.049, 0.0362); sm_.materials.append(scr); SCREEN = link(bpy.data.objects.new('skarm', sm_)); SCREEN.location = (0, 0.0034, 0.0899)

# ---------- mattsattning (README: ca 0,31 m hogt med skorsten, basen ca 0,22 m bred) ----------
dm = mat('matt', (0, 0, 0), 0.5, emit=(0.8, 0.9, 1), es=1.6); DIMS = []
def dbar(p, q, th=0.0008):
    p, q = Vector(p), Vector(q); bpy.ops.mesh.primitive_cube_add(location=(p + q) / 2); o = bpy.context.active_object; d = q - p
    o.scale = (max(abs(d.x) / 2, th), max(abs(d.y) / 2, th), max(abs(d.z) / 2, th)); o.data.materials.append(dm); DIMS.append(o)
def dlabel(text, loc, rot):
    c = bpy.data.curves.new('t', 'FONT'); c.body = text; c.size = 0.02; c.align_x = 'CENTER'; c.align_y = 'CENTER'; o = link(bpy.data.objects.new('t', c)); o.location = loc; o.rotation_euler = rot; c.materials.append(dm); DIMS.append(o)
X1, Y1 = 0.17, -0.06; dbar((X1, Y1, -0.037), (X1, Y1, 0.276)); dbar((X1 - 0.012, Y1, -0.037), (X1 + 0.012, Y1, -0.037)); dbar((X1 - 0.012, Y1, 0.276), (X1 + 0.012, Y1, 0.276)); dlabel('0,31 m', (X1 + 0.05, Y1, 0.12), (math.pi / 2, 0, math.radians(20)))
Y2, Z2 = -0.215, -0.033; dbar((-0.112, Y2, Z2), (0.112, Y2, Z2)); dbar((-0.112, Y2 - 0.012, Z2), (-0.112, Y2 + 0.012, Z2)); dbar((0.112, Y2 - 0.012, Z2), (0.112, Y2 + 0.012, Z2)); dlabel('0,22 m', (0, Y2 - 0.03, Z2), (math.radians(60), 0, 0))

# ---------- pappret med ritningen, som ritas upp fran vanster till hoger ----------
PW, PH, PC = 1.024, 0.524, Vector((0.05, -0.047, GROUND + 0.0012))
pm = bpy.data.materials.new('papper'); pm.use_nodes = True; nt = pm.node_tree; pp = P_(pm); pp.inputs['Roughness'].default_value = 0.85
img = nt.nodes.new('ShaderNodeTexImage'); img.image = bpy.data.images.load(os.path.join(HERE, 'ritning.png')); uv = nt.nodes.new('ShaderNodeTexCoord'); sepu = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(uv.outputs['UV'], sepu.inputs[0]); nt.links.new(uv.outputs['UV'], img.inputs['Vector'])
noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 30; nt.links.new(uv.outputs['UV'], noi.inputs['Vector']); nsc = nt.nodes.new('ShaderNodeMath'); nsc.operation = 'MULTIPLY'; nsc.inputs[1].default_value = 0.05; nt.links.new(noi.outputs['Fac'], nsc.inputs[0])
pos = nt.nodes.new('ShaderNodeMath'); pos.operation = 'ADD'; nt.links.new(sepu.outputs['X'], pos.inputs[0]); nt.links.new(nsc.outputs[0], pos.inputs[1]); DRAW = nt.nodes.new('ShaderNodeValue')
def pfront(soft):
    lo = nt.nodes.new('ShaderNodeMath'); lo.operation = 'SUBTRACT'; lo.inputs[1].default_value = soft; mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0; mr.inputs['To Max'].default_value = 1
    nt.links.new(DRAW.outputs[0], lo.inputs[0]); nt.links.new(pos.outputs[0], mr.inputs['Value']); nt.links.new(DRAW.outputs[0], mr.inputs['From Min']); nt.links.new(lo.outputs[0], mr.inputs['From Max']); return mr
f1, f2 = pfront(0.004), pfront(0.05); inv = nt.nodes.new('ShaderNodeInvert'); nt.links.new(img.outputs['Color'], inv.inputs['Color']); ink = nt.nodes.new('ShaderNodeMath'); ink.operation = 'MULTIPLY'; nt.links.new(inv.outputs['Color'], ink.inputs[0]); nt.links.new(f1.outputs[0], ink.inputs[1])
colm = nt.nodes.new('ShaderNodeMixRGB'); colm.inputs['Color1'].default_value = (0.86, 0.86, 0.83, 1); colm.inputs['Color2'].default_value = (0.02, 0.09, 0.3, 1); nt.links.new(ink.outputs[0], colm.inputs['Fac']); nt.links.new(colm.outputs[0], pp.inputs['Base Color'])
wet = nt.nodes.new('ShaderNodeMath'); wet.operation = 'SUBTRACT'; nt.links.new(f1.outputs[0], wet.inputs[0]); nt.links.new(f2.outputs[0], wet.inputs[1])   # nyritade linjer lyser en stund
GLOW = nt.nodes.new('ShaderNodeValue'); gadd = nt.nodes.new('ShaderNodeMath'); gadd.operation = 'ADD'; nt.links.new(wet.outputs[0], gadd.inputs[0]); nt.links.new(GLOW.outputs[0], gadd.inputs[1])
gmul = nt.nodes.new('ShaderNodeMath'); gmul.operation = 'MULTIPLY'; nt.links.new(gadd.outputs[0], gmul.inputs[0]); nt.links.new(ink.outputs[0], gmul.inputs[1]); gk = nt.nodes.new('ShaderNodeMath'); gk.operation = 'MULTIPLY'; gk.inputs[1].default_value = 5.0; nt.links.new(gmul.outputs[0], gk.inputs[0])
pp.inputs['Emission Color'].default_value = (0.35, 0.75, 1.0, 1)
# nar huset fargas loses pappret upp utat fran husets mitt, med en lysande bla kant (samma sprak som nar ritningen ritades)
HU, HV = (0.0 - (PC.x - PW / 2)) / PW, (0.0 - (PC.y - PH / 2)) / PH
ofs = nt.nodes.new('ShaderNodeVectorMath'); ofs.operation = 'SUBTRACT'; ofs.inputs[1].default_value = (HU, HV, 0); nt.links.new(uv.outputs['UV'], ofs.inputs[0])
skl = nt.nodes.new('ShaderNodeVectorMath'); skl.operation = 'MULTIPLY'; skl.inputs[1].default_value = (PW, PH, 0); nt.links.new(ofs.outputs[0], skl.inputs[0])
dst_ = nt.nodes.new('ShaderNodeVectorMath'); dst_.operation = 'LENGTH'; nt.links.new(skl.outputs[0], dst_.inputs[0])
noi2 = nt.nodes.new('ShaderNodeTexNoise'); noi2.inputs['Scale'].default_value = 9; nt.links.new(uv.outputs['UV'], noi2.inputs['Vector'])
nmu = nt.nodes.new('ShaderNodeMath'); nmu.operation = 'MULTIPLY_ADD'; nmu.inputs[1].default_value = 0.05; nt.links.new(noi2.outputs['Fac'], nmu.inputs[0]); nt.links.new(dst_.outputs['Value'], nmu.inputs[2])
ERASE = nt.nodes.new('ShaderNodeValue'); ERASE.outputs[0].default_value = -1.0
def efront(w):
    hi = nt.nodes.new('ShaderNodeMath'); hi.operation = 'ADD'; hi.inputs[1].default_value = w; nt.links.new(ERASE.outputs[0], hi.inputs[0])
    mr = nt.nodes.new('ShaderNodeMapRange'); nt.links.new(nmu.outputs[0], mr.inputs['Value']); nt.links.new(ERASE.outputs[0], mr.inputs['From Min']); nt.links.new(hi.outputs[0], mr.inputs['From Max']); return mr
ea, eg = efront(0.006), efront(0.05)
nt.links.new(ea.outputs[0], pp.inputs['Alpha'])
egi = nt.nodes.new('ShaderNodeMath'); egi.operation = 'SUBTRACT'; nt.links.new(ea.outputs[0], egi.inputs[0]); nt.links.new(eg.outputs[0], egi.inputs[1])   # smal glodande rand precis utanfor kanten
egk = nt.nodes.new('ShaderNodeMath'); egk.operation = 'MULTIPLY'; egk.inputs[1].default_value = 2.6; nt.links.new(egi.outputs[0], egk.inputs[0])
esum = nt.nodes.new('ShaderNodeMath'); esum.operation = 'ADD'; nt.links.new(gk.outputs[0], esum.inputs[0]); nt.links.new(egk.outputs[0], esum.inputs[1])
nt.links.new(esum.outputs[0], pp.inputs['Emission Strength'])
me = bpy.data.meshes.new('papper'); me.from_pydata([(-PW / 2, -PH / 2, 0), (PW / 2, -PH / 2, 0), (PW / 2, PH / 2, 0), (-PW / 2, PH / 2, 0)], [], [(0, 1, 2, 3)]); me.uv_layers.new()
for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): me.uv_layers[0].data[i].uv = c
me.materials.append(pm); PAPER = link(bpy.data.objects.new('papper', me)); PAPER.location = PC

# ---------- Claude-fonstret ----------
def rrect(w, h, r, d, m, name='ruta'):
    pts = []
    for cx, cz, a0 in [(w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180)]:
        pts += [(cx + r * math.cos(math.radians(a0 + 90 * i / 8)), cz + r * math.sin(math.radians(a0 + 90 * i / 8))) for i in range(9)]
    n = len(pts); vs = [(x, -d / 2, z) for x, z in pts] + [(x, d / 2, z) for x, z in pts]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], [list(range(n)), list(range(2 * n - 1, n - 1, -1))] + [(i, i + n, (i + 1) % n + n, (i + 1) % n) for i in range(n)]); me.materials.append(m); return link(bpy.data.objects.new(name, me))
# ---------- Claude-fonstret: morkt lage, orange logotyp, fragan skrivs i inmatningsrutan och skickas upp som en bubbla ----------
WIN = link(bpy.data.objects.new('fonster', None)); WIN_AT = Vector((0.05, 0.46, 0.5)); WIN.rotation_euler = (math.radians(-14), 0, 0); WW, WH = 0.56, 0.38; WOBJ = []
def child(o, x, z, y=0.0): o.parent = WIN; o.location = (x, y, z); WOBJ.append(o); return o
def lys(name, col, es=1.0): return mat(name, (0, 0, 0), 0.5, emit=col, es=es)
C_BG, C_KANT, C_BUB, C_IN, C_TXT, C_DOV, C_OR = (0.0194, 0.0194, 0.0176), (0.05, 0.05, 0.045), (0.0065, 0.0065, 0.006), (0.032, 0.032, 0.029), (0.95, 0.94, 0.91), (0.33, 0.32, 0.29), (0.694, 0.185, 0.095)
ORANGE = lys('orange', C_OR, 1.5); TXM = lys('text', C_TXT, 1.15); DOV = lys('dov', C_DOV, 1.0)
child(rrect(WW, WH, 0.024, 0.01, lys('fonster', C_BG, 1.5)), 0, 0)
child(rrect(WW + 0.005, WH + 0.005, 0.0265, 0.004, lys('fonsterkant', C_KANT, 1.4)), 0, 0, 0.004)
def spark(R, m=None):        # logotypen: en stjarna av tolv ojamna stralar
    vs, fs_ = [], []; rays = [(0, 1.0, 0.115), (31, 0.86, 0.10), (58, 0.97, 0.12), (92, 0.9, 0.105), (120, 1.0, 0.11), (149, 0.84, 0.10), (181, 0.98, 0.115), (212, 0.88, 0.105), (240, 1.0, 0.12), (268, 0.86, 0.10), (300, 0.96, 0.115), (329, 0.9, 0.10)]
    for a, ln, w in rays:
        a = math.radians(a + 8); d = Vector((math.cos(a), math.sin(a))); n = Vector((-d.y, d.x)); i = len(vs)
        for p in (d * 0.1 - n * w * 0.75, d * ln - n * w * 0.5, d * ln + n * w * 0.5, d * 0.1 + n * w * 0.75): vs.append((p.x * R, 0, p.y * R))
        fs_.append((i, i + 1, i + 2, i + 3))
    i = len(vs); vs += [(0.2 * R * math.cos(k * math.pi / 8), 0, 0.2 * R * math.sin(k * math.pi / 8)) for k in range(16)]; fs_.append(tuple(range(i, i + 16)))
    me = bpy.data.meshes.new('logo'); me.from_pydata(vs, [], fs_); me.materials.append(m or ORANGE); return link(bpy.data.objects.new('logo', me))
UI = typsnitt('segoeui.ttf', 'SFNS.ttf', 'HelveticaNeue.ttc', 'DejaVuSans.ttf'); SERIF = typsnitt('georgia.ttf', 'Georgia.ttf', 'DejaVuSerif.ttf')
def text(body, size, x, z, font=UI, ay='CENTER', m=None, ax='LEFT'):
    c = bpy.data.curves.new('t', 'FONT'); c.body = body; c.font = font or c.font; c.size = size; c.align_x = ax; c.align_y = ay; c.space_line = 1.3; c.materials.append(m or TXM)
    o = link(bpy.data.objects.new('t', c)); o.rotation_euler = (math.pi / 2, 0, 0); child(o, x, z, -0.0095); return c, o
LX = -WW / 2 + 0.034; child(spark(0.015), LX + 0.012, WH / 2 - 0.036, -0.008); text('Claude', 0.027, LX + 0.036, WH / 2 - 0.037, SERIF)
# bubblan med den skickade fragan: bredden foljer texten
TS = 0.0178; T_Q, oq = text(FRAGA, TS, 0, 0, UI, 'TOP'); bpy.context.view_layer.update(); tw, th = oq.dimensions.x, oq.dimensions.y; BW, BH = tw + 0.04, th + 0.034
BX, BZ = WW / 2 - 0.03 - BW / 2, WH / 2 - 0.078 - BH / 2; oq.location = (BX - BW / 2 + 0.02, -0.0095, BZ + BH / 2 - 0.015)
BUB = [child(rrect(BW, BH, 0.018, 0.003, lys('bubbla', C_BUB, 1.5)), BX, BZ, -0.005), oq]
# svaret: liten logotyp, text i serif, och ett kort for ritningen
AZ = BZ - BH / 2 - 0.036; ASP = child(spark(0.0095), LX + 0.009, AZ, -0.008); T_A, oa = text('', 0.0192, LX + 0.03, AZ, SERIF)
KW, KH = 0.3, 0.05; KX, KZ = LX + 0.03 + KW / 2, AZ - 0.052
KORT = [child(rrect(KW, KH, 0.012, 0.003, lys('kort', C_IN, 1.4)), KX, KZ, -0.005), child(rrect(0.03, 0.03, 0.007, 0.002, ORANGE), KX - KW / 2 + 0.026, KZ, -0.0075)]
KORT += [text('Ritning 1 · Lennarts matstation', 0.0125, KX - KW / 2 + 0.05, KZ + 0.008)[1], text('Ritar utkast …', 0.0105, KX - KW / 2 + 0.05, KZ - 0.011, UI, 'CENTER', DOV)[1]]
# inmatningsrutan langst ner, med skicka-knapp
IW, IH = WW - 0.06, 0.07; IZ = -WH / 2 + 0.03 + IH / 2
child(rrect(IW, IH, 0.018, 0.003, lys('inruta', C_IN, 1.4)), 0, IZ, -0.005); child(rrect(IW + 0.003, IH + 0.003, 0.0195, 0.002, lys('inkant', (0.075, 0.075, 0.068), 1.3)), 0, IZ, -0.0035)
T_IN, oin = text('', TS * 0.93, -IW / 2 + 0.02, IZ + IH / 2 - 0.014, UI, 'TOP'); _, PLH = text('Svara Claude …', TS * 0.93, -IW / 2 + 0.02, IZ + IH / 2 - 0.014, UI, 'TOP', DOV)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.0135, depth=0.002, rotation=(math.pi / 2, 0, 0)); knapp = bpy.context.active_object; knapp.data.materials.append(ORANGE); child(knapp, IW / 2 - 0.026, IZ - IH / 2 + 0.024, -0.0075)
pil = bpy.data.meshes.new('pil'); a_ = 0.0062; pil.from_pydata([(-a_, 0, 0), (0, 0, a_), (a_, 0, 0), (a_ * 0.3, 0, 0), (a_ * 0.3, 0, -a_), (-a_ * 0.3, 0, -a_), (-a_ * 0.3, 0, 0)], [], [(0, 1, 2), (6, 3, 4, 5)]); pil.materials.append(lys('pil', C_BG, 1.0))
child(link(bpy.data.objects.new('pil', pil)), IW / 2 - 0.026, IZ - IH / 2 + 0.024, -0.0088)
# projektionen: en tunn orange ljusfana fran fonstrets underkant ner till en lysande linje som sveper over pappret och ritar upp ritningen
BEAM_S = bpy.data.materials.new('fana'); BEAM_S.use_nodes = True; bn = BEAM_S.node_tree; be = bn.nodes.new('ShaderNodeEmission'); be.inputs['Color'].default_value = (1.0, 0.72, 0.5, 1); bt = bn.nodes.new('ShaderNodeBsdfTransparent'); bm = bn.nodes.new('ShaderNodeAddShader')
btc = bn.nodes.new('ShaderNodeTexCoord'); bsx = bn.nodes.new('ShaderNodeSeparateXYZ'); bpw = bn.nodes.new('ShaderNodeMath'); bpw.operation = 'POWER'; bpw.inputs[1].default_value = 1.8; bma = bn.nodes.new('ShaderNodeMath'); bma.operation = 'MULTIPLY_ADD'; bma.inputs[1].default_value = 0.16; bma.inputs[2].default_value = 0.012
PRJ = bn.nodes.new('ShaderNodeValue'); bmu = bn.nodes.new('ShaderNodeMath'); bmu.operation = 'MULTIPLY'   # ljuset ar starkast vid fonstret och tonar ut mot pappret
bn.links.new(btc.outputs['Generated'], bsx.inputs[0]); bn.links.new(bsx.outputs['Z'], bpw.inputs[0]); bn.links.new(bpw.outputs[0], bma.inputs[0]); bn.links.new(bma.outputs[0], bmu.inputs[0]); bn.links.new(PRJ.outputs[0], bmu.inputs[1]); bn.links.new(bmu.outputs[0], be.inputs['Strength'])
bn.links.new(bt.outputs[0], bm.inputs[0]); bn.links.new(be.outputs[0], bm.inputs[1]); bn.links.new(bm.outputs[0], [x for x in bn.nodes if x.type == 'OUTPUT_MATERIAL'][0].inputs['Surface'])
WM = Matrix.Translation(WIN_AT) @ WIN.rotation_euler.to_matrix().to_4x4(); src = [WM @ Vector((x, -0.012, -WH / 2 + z)) for x, z in [(-0.1, 0.0), (0.1, 0.0), (0.1, 0.006), (-0.1, 0.006)]]
dst = [PC + Vector((x * 0.004, y * PH / 2, 0.002)) for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
bme = bpy.data.meshes.new('fana'); bme.from_pydata(src + dst, [], [(i, (i + 1) % 4, (i + 1) % 4 + 4, i + 4) for i in range(4)]); bme.materials.append(BEAM_S); BEAM = link(bpy.data.objects.new('fana', bme)); BEAM.visible_shadow = False
bpy.ops.mesh.primitive_cube_add(size=1); SCAN = bpy.context.active_object; SCAN.scale = (0.005, PH, 0.0006); SCAN_M = lys('svep', (1.0, 0.45, 0.2), 9.0); SCAN.data.materials.append(SCAN_M); SCAN.visible_shadow = False
sd = bpy.data.lights.new('proj', 'SPOT'); sd.spot_size = math.radians(40); sd.spot_blend = 0.8; sd.color = (1.0, 0.6, 0.38); sd.shadow_soft_size = 0.02; SPOT = link(bpy.data.objects.new('proj', sd)); SPOT.location = WM @ Vector((0, -0.03, -WH / 2))
SPOT.rotation_euler = (PC - SPOT.location).to_track_quat('-Z', 'Y').to_euler()

bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, GROUND)); bpy.context.active_object.data.materials.append(mat('golv', (0.016, 0.02, 0.022), 0.34))
def light(loc, target, power, size, col):
    d = bpy.data.lights.new('l', 'AREA'); d.energy = power; d.size = size; d.color = col; o = link(bpy.data.objects.new('l', d)); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return d
KEY = light((-0.8, -1.1, 1.2), (0.05, -0.05, 0.1), 46, 1.0, (1, 0.94, 0.86)); RIM = light((1.2, 0.9, 0.7), (0.05, 0, 0.15), 22, 0.4, (0.45, 0.7, 0.9))
cam_d = bpy.data.cameras.new('cam'); CAM = link(bpy.data.objects.new('cam', cam_d)); sc.camera = CAM; cam_d.clip_start = 0.01; cam_d.dof.use_dof = True

def sm(t, a, b): x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)
def mix(p, q, k): return Vector(p) + (Vector(q) - Vector(p)) * k
def typed(s, t, t0, cps): return s[:max(0, min(len(s), int((t - t0) * cps)))]
IN_MAX = IW - 0.05                 # inmatningsrutan ar en rad: nar texten nar hoger kant rullar den at vanster, som i ett riktigt textfalt
def rad(s):
    i = 0
    while True:
        T_IN.body = s[i:]; bpy.context.view_layer.update()
        if oin.dimensions.x <= IN_MAX or i >= len(s): return s[i:]
        i += 1

# Tider: fonstret in 0.3 | fragan skrivs i inmatningsrutan 0.9-3.9 | skickas 4.1 | svaret 4.8-5.9 | ritningen projiceras 6.0-9.4 | huset reser sig 9.8-13.6 | farg 13.4-16.6 | matt 16.4-18.6 | skarm 18.2
def state(t):
    x = min(1.0, max(0.0, (t - 0.3) / 0.45)); pop = 1 - (1 - x) ** 3 + 0.08 * math.sin(math.pi * x); away = sm(t, 9.9, 11.2)
    WIN.location = WIN_AT + Vector((0, 0.1 * away, 0.008 * math.sin(t * 1.1) + 0.5 * away)); k = max(pop * (1 - 0.5 * away), 0.001); WIN.scale = (k, k, k)
    for o in WOBJ: o.hide_render = t < 0.3 or away > 0.99
    sent = t >= 4.1; T_IN.body = '' if sent else rad(typed(FRAGA, t, 0.9, 27).replace('\n', ' ')); PLH.hide_render = PLH.hide_render or len(T_IN.body) > 0
    for o in BUB: o.hide_render = o.hide_render or not sent
    ASP.hide_render = ASP.hide_render or t < 4.5; ps = 1 + (0.14 * math.sin(t * 10) if t < 6.0 else 0); ASP.scale = (ps, ps, ps); T_A.body = typed(SVAR, t, 4.8, 32)
    for o in KORT: o.hide_render = o.hide_render or t < 6.0
    d_ = -0.02 + 1.15 * sm(t, 6.0, 9.4) ** 0.9 if t > 6.0 else -0.1; sx = PC.x - PW / 2 + min(1.0, max(0.0, d_)) * PW
    for i, (dx, dy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]): bme.vertices[4 + i].co = (sx + dx * 0.004, PC.y + dy * PH / 2, PC.z + 0.002)
    bme.update(); SCAN.location = (sx, PC.y, PC.z + 0.0022)
    proj = sm(t, 5.9, 6.2) * (1 - sm(t, 9.3, 9.6)); PRJ.outputs[0].default_value = proj; BEAM.hide_render = proj < 0.01; SCAN.hide_render = proj < 0.01; sd.energy = 2.5 * proj
    SPOT.rotation_euler = (Vector((sx, PC.y, PC.z)) - SPOT.location).to_track_quat('-Z', 'Y').to_euler()
    DRAW.outputs[0].default_value = -0.02 + 1.15 * sm(t, 6.0, 9.4) ** 0.9 if t > 6.0 else -0.1; GLOW.outputs[0].default_value = 0.5 * sm(t, 9.2, 9.9) * (1 - sm(t, 11.5, 13.5))
    KEY.energy = 46 * (0.45 + 0.55 * sm(t, 9.6, 12.0)); RIM.energy = 22 * (0.5 + 0.5 * sm(t, 9.6, 12.0))
    rise = GROUND - 0.03 + 0.37 * sm(t, 9.8, 13.6); col = GROUND - 0.03 + 0.37 * sm(t, 13.4, 16.6)
    for R in RISES: R.outputs[0].default_value = rise
    for C in COLS: C.outputs[0].default_value = col
    for o in PARTS.values(): o.hide_render = t < 9.8
    SCREEN.hide_render = t < 13.6; sp.inputs['Emission Strength'].default_value = 2.2 * sm(t, 18.2, 18.6)
    dv = sm(t, 16.4, 17.0) * (1 - sm(t, 19.2, 19.8)); P_(dm).inputs['Alpha'].default_value = dv
    for o in DIMS: o.hide_render = dv < 0.01
    ERASE.outputs[0].default_value = -1.0 if t < 14.0 else 0.1 + 0.75 * min(1.0, (t - 14.0) / 2.3) ** 1.5; PAPER.hide_render = t > 16.4
    # kameran: snett ovanifran mot papper och fonster -> sjunker ner till trekvartsvy av huset
    back = sm(t, 5.0, 7.4); down = sm(t, 9.6, 14.5); orbit = sm(t, 13.0, END); wide = sm(t, 12.4, 15.6)   # wide: zoomar ut nar det gra huset star pa ritningen
    eye = mix(mix(WIN_AT + Vector((0.1 - 0.05 * t / 5, -1.0, 0.27)), (0.36, -1.76, 1.02), back), (0.5, -0.92, 0.3), down); eye = eye + Vector((0.12 * orbit, 0.05 * orbit, 0))
    tgt = mix(mix(WIN_AT + Vector((0, 0, -0.01)), (0.05, 0.12, 0.3), back), (0.02, 0.0, 0.1), down)
    dn = 1 - sm(t, 0.0, 1.0) ** 0.8          # overgang in fran 2.6: kameran kommer uppifran och tiltar ner mot fonstret
    eye = eye + Vector((0, 0.05, 0.18)) * dn; tgt = tgt + Vector((0, 0.2, 0.9)) * dn
    CAM.location = eye; CAM.rotation_euler = (tgt - eye).to_track_quat('-Z', 'Y').to_euler(); cam_d.lens = 46 - 4 * back + 13 * down - 12 * wide; cam_d.dof.aperture_fstop = 8 - 2.4 * down; cam_d.dof.focus_distance = (tgt - eye).length

frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(END * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    state(f / FPS); bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
