# Projekt Lennart - kalloppningen v2 (klipp 0.1-0.5), 0-15.2 s. Titeln (0.6) laggs pa i klippningen.
# Kor:  blender -b -P oppning.py -- <ut-mapp (absolut)> <bredd> <samples> [tider i sekunder ...]   (utan tider: alla rutor, fardiga hoppas over)
# v4: huset avslojas inte i oppningen. 0.3 visar bara mekaniken i farg (resten ar morkt glas, luckan oppnas fore noten), 0.4 visar alla delar utlagda pa golvet, 0.5 ligger tatt pa skarmen.
# v2: kameralins i gluggen, hasselnot som foljer hjulet och faller ut i skalen (genomskarning), rorligare kamera, morkt petroleumbla bakgrund.
# Antaganden att bekrafta: kameran ar ritad som en liten kameramodul med fyra fasthal (halbilden i kamerafaste ar ca 21 x 12 mm).
import bpy, bmesh, sys, os, math, json
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, SAMPLES, TIMES = os.path.abspath(a[0]), int(a[1]), int(a[2]), [float(x) for x in a[3:]]
os.makedirs(OUT, exist_ok=True); FPS, END = 25, 15.2
T_B, T_C, T_D, T_E = 4.2, 6.9, 9.2, 12.6   # klippgranser: tilt mot gluggen, in i mekaniken, ut till sprangskissen

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

# bakgrund: nastan svart med ett svagt petroleumblatt sken bakom bildens mitt (i bildrummet, sa att det foljer kameran)
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; wn = sc.world.node_tree; bgn = wn.nodes['Background']
tc = wn.nodes.new('ShaderNodeTexCoord'); sub = wn.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.44, 0)
sc2 = wn.nodes.new('ShaderNodeVectorMath'); sc2.operation = 'MULTIPLY'; sc2.inputs[1].default_value = (1.0, 0.62, 0); ln = wn.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
ramp = wn.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'EASE'; e0, e1 = ramp.color_ramp.elements; e0.position = 0.0; e0.color = (0.012, 0.038, 0.045, 1); e1.position = 0.62; e1.color = (0.0015, 0.003, 0.006, 1)
wn.links.new(tc.outputs['Window'], sub.inputs[0]); wn.links.new(sub.outputs[0], sc2.inputs[0]); wn.links.new(sc2.outputs[0], ln.inputs[0]); wn.links.new(ln.outputs['Value'], ramp.inputs['Fac']); wn.links.new(ramp.outputs['Color'], bgn.inputs['Color'])
lp = wn.nodes.new('ShaderNodeLightPath'); wn.links.new(lp.outputs['Is Camera Ray'], bgn.inputs['Strength'])   # bakgrunden syns men lyser inte upp scenen

bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, 'lennarts-matstation.glb'))
PARTS = {o.name: o for o in bpy.data.objects if o.type == 'MESH'}
GROUP = {d['name']: d['group'] for d in json.load(open(os.path.join(ROOT, 'delar.json'), encoding='utf-8'))}
ORIG_M = {n: o.matrix_world.copy() for n, o in PARTS.items()}; ORIG_MAT = {n: o.data.materials[0] for n, o in PARTS.items()}; ORIG_DATA = {n: o.data for n, o in PARTS.items()}
def grp(*gs): return [n for n in PARTS if GROUP.get(n) in gs]
ROOF, BOWL, INNER = grp('Tak'), grp('Skål'), grp('Inredning')

BUMPS = []   # lagerlinjer (0,2 mm) pa alla utskrivna ytor; styrkan satts per klipp
for m in set(ORIG_MAT.values()):
    nt = m.node_tree; p = nt.nodes['Principled BSDF']; t = nt.nodes.new('ShaderNodeTexCoord'); w = nt.nodes.new('ShaderNodeTexWave'); b = nt.nodes.new('ShaderNodeBump')
    w.wave_type = 'BANDS'; w.bands_direction = 'Z'; w.inputs['Scale'].default_value = 2 * math.pi / (20 * 0.0002); b.inputs['Distance'].default_value = 0.00006
    nt.links.new(t.outputs['Object'], w.inputs['Vector']); nt.links.new(w.outputs['Fac'], b.inputs['Height']); nt.links.new(b.outputs['Normal'], p.inputs['Normal']); BUMPS.append(b); p.inputs['Roughness'].default_value = 0.55

def mat(name, col, rough=0.5, alpha=1.0, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Alpha'].default_value = alpha; p.inputs['Metallic'].default_value = metal; p.inputs['Coat Weight'].default_value = coat; return m
def link(o): sc.collection.objects.link(o); return o
def prim(kind, m, loc, scale, rot=(0, 0, 0), smooth=False, **kw):
    {'cube': bpy.ops.mesh.primitive_cube_add, 'cyl': bpy.ops.mesh.primitive_cylinder_add, 'sphere': bpy.ops.mesh.primitive_uv_sphere_add}[kind](location=loc, rotation=rot, **kw)
    o = bpy.context.active_object; o.scale = scale; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = smooth
    return o

# ---------- skarmen ----------
# Skarmen ar en liten TFT med 168 x 124 pixlar: bilden samplas i pixlarnas mitt, varje pixel har smala morka glipor och svaga RGB-subpixlar.
# Syns som ett svagt rutnat i narbilderna (0.1, 0.5), inte i helbild.
PIX = (168, 124); GAP, STRIPE = 0.75, 0.35      # GAP: hur morka gliporna ar (0-1), STRIPE: hur tydliga subpixlarna ar (0-1)
def screen_mat(f):
    m = bpy.data.materials.new('scr'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']; t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(os.path.join(ROOT, f))
    N = nt.nodes.new; L = nt.links.new
    def mth(op, a, b=None):
        n = N('ShaderNodeMath'); n.operation = op
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: L(v, n.inputs[i])
        return n.outputs[0]
    uv = N('ShaderNodeTexCoord').outputs['UV']; sep = N('ShaderNodeSeparateXYZ'); L(uv, sep.inputs[0])
    gx, gy = mth('MULTIPLY', sep.outputs['X'], PIX[0]), mth('MULTIPLY', sep.outputs['Y'], PIX[1])
    cx, cy = mth('DIVIDE', mth('ADD', mth('FLOOR', gx), 0.5), PIX[0]), mth('DIVIDE', mth('ADD', mth('FLOOR', gy), 0.5), PIX[1])   # pixelns mitt
    cmb = N('ShaderNodeCombineXYZ'); L(cx, cmb.inputs[0]); L(cy, cmb.inputs[1]); L(cmb.outputs[0], t.inputs['Vector'])
    fx, fy = mth('FRACT', gx), mth('FRACT', gy)
    def edge(fr):     # 1 inne i pixeln, 0 i glipan, mjuk kant
        mr = N('ShaderNodeMapRange'); L(mth('ABSOLUTE', mth('SUBTRACT', fr, 0.5)), mr.inputs['Value']); mr.inputs['From Min'].default_value = 0.36; mr.inputs['From Max'].default_value = 0.5
        mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0; return mr.outputs[0]
    cell = mth('MULTIPLY', edge(fx), edge(fy)); cellk = mth('ADD', mth('MULTIPLY', cell, GAP), 1 - GAP)
    sub = N('ShaderNodeCombineXYZ')      # RGB-subpixlar: tre lodratta band i varje pixel
    for i, ph in enumerate((1 / 6, 0.5, 5 / 6)):
        c_ = mth('ADD', mth('MULTIPLY', mth('COSINE', mth('MULTIPLY', mth('SUBTRACT', fx, ph), 2 * math.pi)), 0.5), 0.5)
        L(mth('ADD', mth('MULTIPLY', c_, 1.6 * STRIPE), 1 - STRIPE), sub.inputs[i])
    bl = N('ShaderNodeVectorMath'); bl.operation = 'ADD'; L(t.outputs['Color'], bl.inputs[0]); bl.inputs[1].default_value = (0.0035, 0.0065, 0.0055)   # svag bakgrundsbelysning: aven svarta pixlar lyser lite, sa att rutnatet syns
    m1 = N('ShaderNodeVectorMath'); m1.operation = 'MULTIPLY'; L(bl.outputs[0], m1.inputs[0]); L(sub.outputs[0], m1.inputs[1])
    m2 = N('ShaderNodeVectorMath'); m2.operation = 'SCALE'; L(m1.outputs[0], m2.inputs[0]); L(cellk, m2.inputs['Scale'])
    L(m2.outputs[0], p.inputs['Base Color']); L(m2.outputs[0], p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value = 2.2 / (1 - GAP / 3); p.inputs['Roughness'].default_value = 0.2; return m
SCR = {'vantar': screen_mat('skarm-vantar.png'), 'verifierar': screen_mat('skarm-verifierar.png')}
# 0.5: punkterna i VERIFIERAR tands en i taget pa de tre pipen (1,70, 1,95 och 2,20 s in i klippet, se ljudmix.mjs). Den nytanda punkten blixtrar till i 0,12 s.
for n_ in ('v0', 'v1', 'v1f', 'v2', 'v2f', 'v3', 'v3f'): SCR[n_] = screen_mat('skarm-verifierar-%s.png' % n_)
SCR['av'] = screen_mat('skarm-av.png')     # slutet av 0.5: alla pixlar slocknar, titeln tar vid i samma rutnat
PIPS = [T_E + d for d in (1.70, 1.95, 2.20)]
def dots(t):
    n = sum(t >= p - 0.02 for p in PIPS); return 'v%d' % n + ('f' if n and t < PIPS[n - 1] + 0.10 else '')
me = bpy.data.meshes.new('skarm'); w_, h_ = 0.049, 0.0362; me.from_pydata([(-w_ / 2, 0, 0), (w_ / 2, 0, 0), (w_ / 2, 0, h_), (-w_ / 2, 0, h_)], [], [(0, 1, 2, 3)]); me.uv_layers.new()
for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): me.uv_layers[0].data[i].uv = c
me.materials.append(SCR['vantar']); SCREEN = link(bpy.data.objects.new('skarm', me)); SCREEN.location = (0, 0.0034, 0.0899)

# ---------- kameramodulen bakom gluggen ----------
kf = PARTS['kamerafaste']; ys = [(kf.matrix_world @ v.co) for v in kf.data.vertices]; mid = [v for v in ys if abs(v.x) < 0.013]
PL_F, PL_B = min(v.y for v in mid), max(v.y for v in mid); LZ = (min(v.z for v in mid) + max(v.z for v in mid)) / 2; print('KAMERAPLATTA y', round(PL_F, 4), round(PL_B, 4), 'z', round(LZ, 4), flush=True)
LENS_Y = PL_F - 0.0015; LENS = Vector((0, LENS_Y, LZ))
blk = mat('kam_svart', (0.012, 0.012, 0.014), 0.35); CAMPARTS = [
    prim('cube', mat('kam_pcb', (0.02, 0.16, 0.07), 0.45), (0, PL_B + 0.0008, LZ), (0.0125, 0.0008, 0.012)),
    prim('cube', blk, (0, (LENS_Y + PL_B) / 2 + 0.001, LZ), (0.00425, (PL_B - LENS_Y) / 2 + 0.001, 0.00425)),
    prim('cyl', blk, (0, LENS_Y - 0.0006, LZ), (0.0036, 0.0036, 0.0012), (math.pi / 2, 0, 0), True, vertices=64, radius=1, depth=2),
    prim('cyl', mat('kam_ring', (0.05, 0.05, 0.055), 0.25, metal=1.0), (0, LENS_Y - 0.0019, LZ), (0.0030, 0.0030, 0.0003), (math.pi / 2, 0, 0), True, vertices=64, radius=1, depth=2),
    prim('sphere', mat('kam_glas', (0.004, 0.005, 0.012), 0.04, metal=0.15, coat=1.0), (0, LENS_Y - 0.0016, LZ), (0.0025, 0.0011, 0.0025), smooth=True, segments=48, ring_count=24, radius=1)]

# ---------- hasselnot ----------
bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, radius=1); n0 = bpy.context.active_object
for v in n0.data.vertices:
    x, y, z = v.co
    if z > 0: k = 1 - 0.30 * z ** 2.2; x *= k; y *= k; z = z * 1.08 + 0.16 * z ** 6     # avsmalnande topp med liten spets
    else: z = max(z * 0.95, -0.78)                                                        # platt, blek bas
    v.co = (x * 1.04, y * 0.98, z)
for p in n0.data.polygons: p.use_smooth = True
nm = bpy.data.materials.new('hasselnot'); nm.use_nodes = True; nt = nm.node_tree; p = nt.nodes['Principled BSDF']; t = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (9, 9, 0.7); noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 2.0; noi.inputs['Detail'].default_value = 3
shell = nt.nodes.new('ShaderNodeValToRGB'); shell.color_ramp.elements[0].position = 0.3; shell.color_ramp.elements[0].color = (0.16, 0.065, 0.022, 1); shell.color_ramp.elements[1].position = 0.75; shell.color_ramp.elements[1].color = (0.42, 0.20, 0.07, 1)
capf = nt.nodes.new('ShaderNodeMapRange'); capf.inputs['From Min'].default_value = -0.70; capf.inputs['From Max'].default_value = -0.52; capf.inputs['To Min'].default_value = 1; capf.inputs['To Max'].default_value = 0
mixc = nt.nodes.new('ShaderNodeMixRGB'); mixc.inputs['Color2'].default_value = (0.62, 0.50, 0.34, 1); mixr = nt.nodes.new('ShaderNodeMapRange'); mixr.inputs['To Min'].default_value = 0.28; mixr.inputs['To Max'].default_value = 0.8
nt.links.new(t.outputs['Object'], sep.inputs[0]); nt.links.new(t.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs[0], noi.inputs['Vector']); nt.links.new(noi.outputs['Fac'], shell.inputs['Fac'])
nt.links.new(sep.outputs['Z'], capf.inputs['Value']); nt.links.new(capf.outputs[0], mixc.inputs['Fac']); nt.links.new(shell.outputs['Color'], mixc.inputs['Color1']); nt.links.new(mixc.outputs[0], p.inputs['Base Color'])
nt.links.new(capf.outputs[0], mixr.inputs['Value']); nt.links.new(mixr.outputs[0], p.inputs['Roughness']); p.inputs['Coat Weight'].default_value = 0.25
# magasinet ar fullt: notterna ligger i en hog i tratten. Platserna raknas fram av verktyg/notmagasin.py mot magasinets riktiga vaggar, sa att ingen not sticker ut.
PILE = json.load(open(os.path.join(HERE, 'notmagasin.json')))
n0.data.materials.append(nm); NR = 0.0082; NUTS = [n0] + [link(bpy.data.objects.new('not%d' % i, n0.data)) for i in range(1, len(PILE) + 1)]; print('MAGASIN', len(PILE), 'notter', flush=True)
for o in NUTS: o.scale = (NR, NR, NR)

# ---------- genomskarning vid x = 0 (klipp 0.3) ----------
SECT = ['doserhus', 'doserhjul', 'notmagasin', 'kropp', 'kropp_vit', 'kropp_sockel', 'kropp_packning', 'skal', 'skal_vit', 'lucka', 'lucka_vit', 'skarmklamma', 'skarmram', 'kamerafaste', 'solskydd', 'solskydd_vit',
        'bas', 'framgard', 'grasmatta', 'framgard_gras', 'bottenplatta', 'framgard_platta', 'elektroniklada', 'monteringsplatta', 'ellock', 'elpackning', 'genomforingar']
CUT = {}
for n in SECT:
    o = PARTS[n]; d = o.data.copy(); bm = bmesh.new(); bm.from_mesh(d); inv = o.matrix_world.inverted()
    r = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=inv @ Vector((0.0004, 0, 0)), plane_no=(inv.to_3x3() @ Vector((1, 0, 0))).normalized(), clear_outer=True)
    col = ORIG_MAT[n].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value; d.materials.append(mat('snitt_' + n, tuple(c * 0.42 for c in col[:3]), 0.85))
    try:
        f = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=[e for e in r['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])
        for g in f['geom']:
            if isinstance(g, bmesh.types.BMFace): g.material_index = 1
    except Exception as e: print('fyllning', n, e)
    bm.to_mesh(d); bm.free(); CUT[n] = d

# huset som morkt glas i genomskarningen: bara kanterna lyser svagt, mekaniken behaller sina farger
MECH = {'doserhus', 'doserhjul', 'notmagasin', 'skal', 'skal_vit', 'lucka', 'lucka_vit'}
gh = bpy.data.materials.new('glas'); gh.use_nodes = True; gn = gh.node_tree; lw = gn.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3; pw = gn.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.5
mu = gn.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY_ADD'; mu.inputs[1].default_value = 0.3; mu.inputs[2].default_value = 0.012; ge = gn.nodes.new('ShaderNodeEmission'); ge.inputs['Color'].default_value = (0.22, 0.7, 0.8, 1); ge.inputs['Strength'].default_value = 0.45
gt = gn.nodes.new('ShaderNodeBsdfTransparent'); gm = gn.nodes.new('ShaderNodeMixShader'); gn.links.new(lw.outputs['Facing'], pw.inputs[0]); gn.links.new(pw.outputs[0], mu.inputs[0]); gn.links.new(mu.outputs[0], gm.inputs[0])
gn.links.new(gt.outputs[0], gm.inputs[1]); gn.links.new(ge.outputs[0], gm.inputs[2]); gn.links.new(gm.outputs[0], [x for x in gn.nodes if x.type == 'OUTPUT_MATERIAL'][0].inputs['Surface'])
for n, d in CUT.items():
    if n not in MECH:
        for i in range(len(d.materials)): d.materials[i] = gh
sc.cycles.transparent_max_bounces = 64

# 0.4: alla delar utlagda pa golvet, sorterade efter storlek, de storsta langst bak
GROUND = -0.037; bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, GROUND)); FLOOR = bpy.context.active_object; FLOOR.data.materials.append(mat('golv', (0.016, 0.02, 0.022), 0.55))
_it = []; LAYR = {}; LAYD = {}
for n, o in PARTS.items():
    pts = [ORIG_M[n] @ v.co for v in ORIG_DATA[n].vertices]; cands = [Matrix.Identity(4)] + [Matrix.Rotation(math.radians(a_), 4, ax) for ax, a_ in (('X', -90), ('Y', 90), ('Y', 45), ('Y', -45), ('Y', 40), ('Y', -40), ('Y', 50), ('Y', -50))]
    def hz_(R): zs = [(R @ p).z for p in pts]; return max(zs) - min(zs)
    LAYR[n] = min(cands, key=lambda R: round(hz_(R), 3))   # varje del laggs i sin plattaste riktning, sa att husets form inte avslojas
    # delen bakas i sitt liggande lage, och varje los bit (t.ex. vart och ett av fonstren) sanks ner sa att den vilar pa golvet
    d = ORIG_DATA[n].copy(); bm = bmesh.new(); bm.from_mesh(d); bm.transform(LAYR[n] @ ORIG_M[n]); seen = set()
    for v0 in bm.verts:
        if v0.index in seen: continue
        isl, stack = [], [v0]; seen.add(v0.index)
        while stack:
            v = stack.pop(); isl.append(v)
            for e in v.link_edges:
                w = e.other_vert(v)
                if w.index not in seen: seen.add(w.index); stack.append(w)
        dz = GROUND - min(v.co.z for v in isl)
        for v in isl: v.co.z += dz
    pts = [v.co.copy() for v in bm.verts]; bm.to_mesh(d); bm.free(); LAYD[n] = d
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))); hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts))); _it.append((n, lo, hi))
_it.sort(key=lambda it: -(it[2].x - it[1].x) * (it[2].y - it[1].y)); LAY = {}; RW, GAP = 1.5, 0.03; x_, y_, rd = 0.0, 0.0, 0.0
for n, lo, hi in _it:
    w, d = hi.x - lo.x, hi.y - lo.y
    if x_ + w > RW: x_ = 0.0; y_ -= rd + GAP; rd = 0.0
    LAY[n] = Vector((x_ - lo.x - RW / 2, y_ - d - lo.y, 0)); x_ += w + GAP; rd = max(rd, d)
LAY_DEPTH = -(y_ - rd)
for n in LAY: LAY[n].y += LAY_DEPTH * 0.55
_rp = [v.co for v in LAYD['skarmram'].vertices]; RAM_C = LAY['skarmram'] + Vector((sum(p.x for p in _rp) / len(_rp), sum(p.y for p in _rp) / len(_rp), max(p.z for p in _rp)))   # skarmramens mitt pa golvet
import numpy as _np; _xy = _np.array([(p.x, p.y) for p in _rp]); _xy -= _xy.mean(0); _ev = _np.linalg.eigh(_xy.T @ _xy)[1][:, -1]; RAM_A = math.atan2(_ev[1], _ev[0])   # ramens langsida pa golvet
RAM_A = (RAM_A + math.pi / 2) % math.pi - math.pi / 2; RAM_ROLL = math.radians(-23); print('RAMEN', RAM_C, math.degrees(RAM_A), flush=True)
print('UTLAGGNING djup', round(LAY_DEPTH, 3), [(n, round(lo.z, 3), round(hi.z, 3)) for n, lo, hi in _it if hi.z - lo.z > 0.09], flush=True)

def light(name, loc, target, power, size, col):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = power; d.size = size; d.color = col; o = link(bpy.data.objects.new(name, d)); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
L = {'makro': [light('m1', (0.45, -0.25, 0.45), (0, 0, 0.14), 1.6, 0.25, (1, 0.7, 0.5)), light('m2', (-0.4, -0.3, 0.1), (0, 0, 0.15), 0.4, 0.4, (0.45, 0.7, 0.9)), light('m3', (-0.12, -0.3, 0.28), LENS, 0.14, 0.12, (0.8, 0.9, 1))],
     'snitt': [light('s1', (0.7, -0.35, 0.45), (0, 0.03, 0.06), 20, 0.5, (1, 0.8, 0.62)), light('s2', (0.3, 0.6, 0.3), (0, 0.04, 0.07), 6, 0.3, (0.45, 0.7, 0.9))],
     'golv': [light('g1', (2.0, 0.3, 0.9), (0, 0.1, 0), 70, 0.9, (1, 0.78, 0.58)), light('g2', (-1.2, -1.0, 0.6), (0, 0, 0), 22, 1.0, (0.45, 0.7, 0.9))],
     'hus': [light('k1', (0.9, 0.9, 0.7), (0, 0.05, 0.2), 60, 0.45, (1, 0.75, 0.55)), light('k2', (-0.8, -0.8, 0.3), (0, 0.05, 0.2), 5, 0.8, (0.45, 0.7, 0.9))]}
cam_d = bpy.data.cameras.new('cam'); CAM = link(bpy.data.objects.new('cam', cam_d)); sc.camera = CAM; cam_d.clip_start = 0.001; cam_d.dof.use_dof = True
def camera(eye, target, lens, fstop, focus=None, roll=0.0):
    CAM.location = eye; q = (Vector(target) - Vector(eye)).to_track_quat('-Z', 'Y'); CAM.rotation_euler = (q.to_matrix().to_4x4() @ Matrix.Rotation(roll, 4, 'Z')).to_euler()
    cam_d.lens = lens; cam_d.dof.aperture_fstop = fstop; cam_d.dof.focus_distance = (Vector(focus or target) - Vector(eye)).length

EX = {n: Vector((0, 0, 0)) for n in PARTS}   # sprangskissens forskjutningar (m)
def ex(names, d):
    for n in names: EX[n] += Vector(d)
for n, d in {'fotter': -0.17, 'bottenplatta': -0.135, 'framgard_platta': -0.135, 'bas': -0.10, 'framgard': -0.10, 'grasmatta': -0.055, 'framgard_gras': -0.055, 'stenar': -0.03, 'framgard_stenar': -0.03}.items(): ex([n], (0, 0, d))
ex(['framgard', 'framgard_gras', 'framgard_stenar', 'framgard_platta'], (0, -0.05, 0)); ex(ROOF, (0, 0, 0.36)); ex(['tak_v', 'tak_v_vit'], (-0.05, 0, 0)); ex(['tak_h', 'tak_h_vit'], (0.05, 0, 0)); ex(['skorsten', 'skorsten_krage'], (0.05, 0, 0.07))
ex(['nockkilar'], (0, 0, 0.05)); ex(['takpackning'], (0, 0, -0.07)); ex(BOWL, (0, -0.13, 0.02)); ex(['lucka', 'lucka_vit'], (0, -0.03, 0.06)); ex(['servokapa', 'servopackning'], (0.03, 0, 0.05))
ex(['skarmram'], (0, -0.09, 0)); ex(['solskydd', 'solskydd_vit'], (0, -0.06, 0)); ex(['kropp_packning'], (0, 0, -0.02)); ex(['doserhus'], (0, 0, 0.22)); ex(['doserhjul'], (-0.11, 0, 0.22)); ex(['notmagasin'], (0, 0, 0.28))
ex(['kamerafaste', 'skarmklamma'], (0, -0.09, 0)); ex(['elektroniklada', 'elpackning'], (0, 0.14, 0)); ex(['monteringsplatta', 'genomforingar'], (0, 0.22, 0)); ex(['ellock'], (0, 0.14, 0.05))

def sm(t, a, b): x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)          # mjuk start, mjukt stopp
def out(t, a, b, p=2.4): x = min(1, max(0, (t - a) / (b - a))); return 1 - (1 - x) ** p     # snabbt forst, sedan langsamt
def acc(t, a, b, p=2.0): x = min(1, max(0, (t - a) / (b - a))); return x ** p              # langsamt forst, sedan snabbt
def mix(p, q, k): return Vector(p) + (Vector(q) - Vector(p)) * k
def orbit(c, az, r, dz): a_ = math.radians(az); return Vector(c) + Vector((r * math.sin(a_), -r * math.cos(a_), dz))
def lights(on):
    for k, ls in L.items():
        for l in ls: l.hide_render = k != on

AXLE = Vector((0, 0.057, 0.0643)); POCKET_R = 0.0185
def wheel_angle(t): return 130 * sm(t, 7.5, 8.2)
def hatch_angle(t): return -95 * sm(t, 6.95, 7.5)   # luckan oppnas forst
def nut_path(t):   # noten ligger i hjulets ficka, foljer med 130 grader framat och rullar ut genom rannan till skalen
    th = math.radians(wheel_angle(t)); ride = AXLE + Vector((0, -POCKET_R * math.sin(th), POCKET_R * math.cos(th)))
    if t < 8.15: return ride, th
    pts = [ride, AXLE + Vector((0, -0.034 * math.sin(th), 0.034 * math.cos(th))), Vector((0, 0.013, 0.031)), Vector((0, -0.003, 0.021)), Vector((0, -0.021, 0.0125))]
    u = acc(t, 8.15, 8.85, 1.5) * (len(pts) - 1); i = min(int(u), len(pts) - 2); p = mix(pts[i], pts[i + 1], u - i)
    if t > 8.85: p.z += 0.0035 * abs(math.sin((t - 8.85) * 16)) * max(0, 1 - (t - 8.85) / 0.35)   # liten studs
    return p, th + acc(t, 8.15, 8.85, 1.5) * 5.5

def state(t):
    for n, o in PARTS.items(): o.matrix_world = ORIG_M[n]; o.data = ORIG_DATA[n]; o.hide_render = False
    SCREEN.hide_render = False; SCREEN.data.materials[0] = SCR['vantar']; FLOOR.hide_render = True
    for o in NUTS: o.hide_render = True
    for o in CAMPARTS: o.hide_render = False
    S = Vector((0, 0, 0.108))
    if t < T_C:      # 0.1 skarmen -> 0.2 gluggen: en bage runt fasaden som slutar med att kameran aker in i linsen
        lights('makro')
        for b in BUMPS: b.inputs['Strength'].default_value = 0.35
        tgt = mix(S, LENS, sm(t, 3.7, 5.1)); az = -52 + 66 * out(t, 0, T_C, 1.7); r = 0.31 - 0.085 * out(t, 0, 4.4, 2.0) - 0.197 * acc(t, 4.9, T_C, 2.2)
        camera(orbit(tgt, az, r, -0.012 + 0.016 * sm(t, 0, 5)), tgt, 85, 2.8 + 9 * acc(t, 5.4, T_C, 1.5), roll=math.radians(-7 * (1 - out(t, 0, 5.5, 2.0))))
    elif t < T_D:    # 0.3 genomskarning: hjulet vrids 130 grader och noten rullar ut i skalen, kameran foljer med ner
        lights('snitt')
        for b in BUMPS: b.inputs['Strength'].default_value = 0.2
        for n, o in PARTS.items():
            o.hide_render = n not in CUT
            if n in CUT: o.data = CUT[n]
        for o in CAMPARTS: o.hide_render = True
        for n in ('lucka', 'lucka_vit'): PARTS[n].matrix_world = ORIG_M[n] @ Matrix.Rotation(math.radians(hatch_angle(t)), 4, 'X')
        SCREEN.hide_render = True; p, th = nut_path(t); PARTS['doserhjul'].matrix_world = ORIG_M['doserhjul'] @ Matrix.Rotation(math.radians(wheel_angle(t)), 4, 'X')
        NUTS[0].hide_render = False; NUTS[0].matrix_world = Matrix.Translation(p) @ Matrix.Rotation(-th, 4, 'X') @ Matrix.Scale(NR, 4)
        for i, (x, y, z, rx, ry, rz) in enumerate(PILE):   # resten av magasinet: en full hog ovanpa hjulet
            NUTS[i + 1].hide_render = False; NUTS[i + 1].matrix_world = Matrix.Translation((x, y, z)) @ Euler((rx, ry, rz)).to_matrix().to_4x4() @ Matrix.Scale(NR, 4)
        k = out(t, T_C, 8.3, 2.6); follow = sm(t, 8.1, 8.85); tgt = mix((0, 0.05, 0.088), (0, 0.006, 0.03), follow)
        dive = acc(t, 8.95, T_D, 2.0); tgt = tgt + Vector((0, -0.01, -0.09)) * dive     # overgang ut: snabb tilt nerat forbi skalen
        camera(mix((0.62, 0.02, 0.135), (0.36, -0.075, 0.10), k) + Vector((0, -0.05, -0.05)) * follow + Vector((0, 0, -0.02)) * dive, tgt, 60, 5.6, (0.0, tgt.y, tgt.z))
    elif t < T_E:    # 0.4 alla delar utlagda pa golvet, kameran sveper lagt forbi dem
        lights('golv'); FLOOR.hide_render = False; k = sm(t, T_D - 0.4, T_E + 0.4)
        for b in BUMPS: b.inputs['Strength'].default_value = 0.2
        for n, o in PARTS.items(): o.data = LAYD[n]; o.matrix_world = Matrix.Translation(LAY[n])
        for o in CAMPARTS: o.hide_render = True
        SCREEN.hide_render = True; tgt = mix((-0.3, 0.12, -0.01), (0.3, 0.02, -0.01), k); eye = mix((-0.95, -0.5, 0.1), (0.5, -0.66, 0.15), k)
        rise = 1 - out(t, T_D, T_D + 0.45, 2.0); tgt = tgt + Vector((0, -0.25, -0.3)) * rise                       # overgang in: tilten fortsatter, nu uppat fran golvet
        crane = sm(t, T_E - 1.15, T_E - 0.02)                                                                    # overgang ut: rakt ovanfor skarmramen, som skarmen i 0.5
        lens = 36 + 49 * crane
        if crane > 0: tgt = mix(tgt, RAM_C, crane); eye = mix(eye, RAM_C + Vector((0.0001, -0.0001, 0.30)), crane)
        camera(eye, tgt, lens, 2.0 + 3.6 * crane, roll=(RAM_ROLL + math.radians(2.5)) * crane)
    else:            # 0.5 tatt pa skarmen: VERIFIERAR...
        lights('makro'); k = out(t, T_E, END, 1.8); SCREEN.data.materials[0] = SCR['av' if t >= END - 0.06 else dots(t)]
        push = acc(t, 14.5, END - 0.08, 2.2)    # overgang till titeln: kameran aker in tills skarmens pixlar fyller bilden (ca 80 pixlar over bildbredden, samma som titelns rutnat)
        for b in BUMPS: b.inputs['Strength'].default_value = 0.35
        camera(orbit(S, (16 - 16 * k) * (1 - push), (0.3 - 0.075 * k) * (1 - push) + 0.058 * push, 0.004 * (1 - push)), S + Vector((0.004 * push, 0.0034 * push, 0)), 85, 2.8 + 9 * push, focus=S + Vector((0, 0.0034, 0)), roll=math.radians(2.5 * (1 - k)) * (1 - push))

# Omtajmning: par av (ny tid, ursprunglig tid) vid varje fras, linjart daremellan
WARP = [(0.0, 0.0), (15.2, 15.2)]   # ingen omtajmning: tiderna foljer den egna inspelningen av introt. Tajmas om nar den riktiga rosten ar inspelad.
def warp(t):
    for (n0, o0), (n1, o1) in zip(WARP, WARP[1:]):
        if t <= n1: return o0 + (o1 - o0) * (t - n0) / (n1 - n0)
    return WARP[-1][1]
frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(WARP[-1][0] * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    state(min(warp(f / FPS), END - 0.001)); bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
