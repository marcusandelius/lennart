# Projekt Lennart - kalloppningen v2 (klipp 0.1-0.5), 0-15.2 s. Titeln (0.6) laggs pa i klippningen.
# Kor:  blender -b -P oppning.py -- <ut-mapp (absolut)> <bredd> <samples> [tider i sekunder ...]   (utan tider: alla rutor, fardiga hoppas over)
# v4: huset avslojas inte i oppningen. 0.3 visar bara mekaniken i farg (resten ar morkt glas, luckan oppnas fore noten), 0.4 visar alla delar utlagda pa golvet, 0.5 ligger tatt pa skarmen. v5: 0.4 ar en ordnad upplaggning med elektroniken och borjar inne i husets stomme.
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
for k_, f_ in ((1, 1.0), (2, 1.35), (3, 1.6), (4, 1.2), (5, 1.0)):   # glitchen nar LED-skarmen byter till VERIFIERAR (verktyg/skarm_glitch.py), nagra rutor lyser starkare
    SCR['g%d' % k_] = screen_mat('skarm-glitch-%d.png' % k_); _p = SCR['g%d' % k_].node_tree.nodes['Principled BSDF']; _p.inputs['Emission Strength'].default_value *= f_
GLITCH = {321: 'g1', 322: 'g2', 323: 'vantar', 324: 'g3', 325: 'av', 326: 'g4', 327: 'g5'}   # rutnummer -> skarmbild, 12,84-13,08 s
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

# Varianter av 0.3 (LENNART_03, prov for Marcus): K = nuvarande genomskarning med glashuset, S = snittet: rakt fran sidan utan perspektiv, bara mekaniken,
# snittytorna i varm orange; M = makro med fartramp: kort skarpedjup, slowmotion nar noten slapper ur hjulet; H = last vid hjulet: kameran snurrar med hjulet.
VAR03 = os.environ.get('LENNART_03', 'H')
if VAR03 == 'H': ge.inputs['Color'].default_value = (0.25, 0.75, 0.5, 1)
if VAR03 == 'S':   # snittytorna far snittskraffering som pa en ritning: delens egen farg med tata diagonala linjer i en morkare ton
    for n in MECH:
        if len(CUT[n].materials) < 2: continue
        col = ORIG_MAT[n].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value[:3]
        hm = mat('skraff_' + n, col, 0.8); ht = hm.node_tree; hp = ht.nodes['Principled BSDF']; tc_ = ht.nodes.new('ShaderNodeTexCoord'); sx_ = ht.nodes.new('ShaderNodeSeparateXYZ')
        ad = ht.nodes.new('ShaderNodeMath'); ad.operation = 'ADD'; dv = ht.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = 0.0032
        fr = ht.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; lt = ht.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.16
        mx = ht.nodes.new('ShaderNodeMixRGB'); mx.inputs['Color1'].default_value = (*col, 1); mx.inputs['Color2'].default_value = (col[0] * 0.5, col[1] * 0.42, col[2] * 0.36, 1)
        ht.links.new(tc_.outputs['Object'], sx_.inputs[0]); ht.links.new(sx_.outputs['Y'], ad.inputs[0]); ht.links.new(sx_.outputs['Z'], ad.inputs[1]); ht.links.new(ad.outputs[0], dv.inputs[0])
        ht.links.new(dv.outputs[0], fr.inputs[0]); ht.links.new(fr.outputs[0], lt.inputs[0]); ht.links.new(lt.outputs[0], mx.inputs['Fac']); ht.links.new(mx.outputs[0], hp.inputs['Base Color'])
        CUT[n].materials[1] = hm
def _pchip(ks):   # mjuk, monoton kurva genom punkterna (ny tid -> mekanikens tid)
    xs = [k[0] for k in ks]; ys = [k[1] for k in ks]; d = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(len(ks) - 1)]
    m = [d[0]] + [2 * d[i - 1] * d[i] / (d[i - 1] + d[i]) for i in range(1, len(d))] + [d[-1]]
    def f(t):
        if t <= xs[0]: return ys[0]
        if t >= xs[-1]: return ys[-1]
        i = max(j for j in range(len(xs) - 1) if xs[j] <= t); h = xs[i + 1] - xs[i]; u = (t - xs[i]) / h
        return (2 * u ** 3 - 3 * u ** 2 + 1) * ys[i] + (u ** 3 - 2 * u ** 2 + u) * h * m[i] + (-2 * u ** 3 + 3 * u ** 2) * ys[i + 1] + (u ** 3 - u ** 2) * h * m[i + 1]
    return f
TAU_M = _pchip([(6.9, 6.9), (7.3, 7.55), (7.7, 8.08), (8.55, 8.33), (8.85, 8.85), (9.2, 9.2)])   # M: snabbt fram till slappet, slowmotion nar noten tippar ur fickan, snabbt ner i skalen

# 0.4: alla delar utlagda pa golvet som en ordnad upplaggning. Varje los bit ligger plant i sin tunnaste riktning med langsidan langs x, och delarna ar sorterade i grupper
# (stomme, tak, bas, skal, elektronik, inredning) fran vanster till hoger. Husets stomme ligger pa rygg langst till vanster, som ett ror; 0.4 borjar inne i den.
# Elektroniken ar samma generiska modeller som i inkopen (film/elektronik.blend, gors med verktyg/elektronik_export.py). Numren 01-48 bredvid husets delar stangs av med LENNART_NUMMER=0.
import numpy as _np
GROUND = -0.037; bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, GROUND)); FLOOR = bpy.context.active_object; FLOOR.data.materials.append(mat('golv', (0.016, 0.02, 0.022), 0.55))
def _oar(pts):   # plattaste riktningen: den sida av holjet som ger lagst hojd laggs mot golvet, sedan vrids langsidan langs x (minsta omskrivna rektangel)
    P_ = _np.array([tuple(p) for p in pts]); bm = bmesh.new(); vs = [bm.verts.new(p) for p in pts]
    try: res = bmesh.ops.convex_hull(bm, input=vs); fs = [g for g in res['geom'] if isinstance(g, bmesh.types.BMFace)]
    except Exception: fs = []
    best = None
    for f in fs:
        f.normal_update(); n = f.normal.copy()
        if n.length < 0.5: continue
        d_ = P_ @ _np.array(tuple(n)); k = (round(float(d_.max() - d_.min()), 4), -f.calc_area())
        if best is None or k < best[0]: best = (k, n)
    bm.free(); n = best[1] if best else Vector((0, 0, -1))
    R = n.rotation_difference(Vector((0, 0, -1))).to_matrix().to_4x4(); Q = P_ @ _np.array(R.to_3x3()).T; bA = None
    for k in range(90):
        a_ = math.radians(k * 2); c, s = math.cos(a_), math.sin(a_); xs = c * Q[:, 0] - s * Q[:, 1]; ys = s * Q[:, 0] + c * Q[:, 1]; w, d = float(_np.ptp(xs)), float(_np.ptp(ys))
        if bA is None or w * d < bA[0] - 1e-9: bA = (w * d, a_, w, d)
    return Matrix.Rotation(bA[1] + (0 if bA[2] >= bA[3] else math.pi / 2), 4, 'Z') @ R
def _oar_fast(pts): return _oar(pts if len(pts) < 6000 else pts[::max(1, len(pts) // 6000)])
def _islands(bm):
    seen = set(); out_ = []
    for v0 in bm.verts:
        if v0.index in seen: continue
        isl, stack = [], [v0]; seen.add(v0.index)
        while stack:
            v = stack.pop(); isl.append(v)
            for e in v.link_edges:
                w = e.other_vert(v)
                if w.index not in seen: seen.add(w.index); stack.append(w)
        out_.append(isl)
    return out_
def _bb(cos): a_ = _np.array([tuple(c) for c in cos]); return Vector(a_.min(0)), Vector(a_.max(0))
LAY = {n: Vector((0, 0, 0)) for n in PARTS}; LAYD = {}; _BM = {}; BLOCK = {}   # BLOCK: namn -> (bredd, djup) i blockets egna koordinater (horn i origo)
KROPP_R = Matrix.Rotation(math.radians(-90), 4, 'Z') @ Matrix.Rotation(math.radians(-90), 4, 'X')   # stommen pa rygg: roret (dess hojd) langs +x, framsidan uppat
for n in PARTS:
    bm = bmesh.new(); bm.from_mesh(ORIG_DATA[n]); bm.transform(ORIG_M[n]); bm.verts.ensure_lookup_table(); isl = _islands(bm)
    if n == 'kropp': bm.transform(KROPP_R); pieces = [list(bm.verts)]
    else:
        pieces = isl if 2 <= len(isl) <= 12 else [list(bm.verts)]
        for pc in pieces:
            M_ = _oar_fast([v.co for v in pc])
            for v in pc: v.co = M_ @ v.co
    # bitarna i en rad (bryts efter 0,3 m), storst forst, med lika avstand
    info = sorted([(pc, *_bb([v.co for v in pc])) for pc in pieces], key=lambda it: -(it[2].x - it[1].x) * (it[2].y - it[1].y))
    x_, y_, rd, W_ = 0.0, 0.0, 0.0, 0.0
    for pc, lo, hi in info:
        w, d = hi.x - lo.x, hi.y - lo.y
        if x_ > 0 and x_ + w > 0.3: x_ = 0.0; y_ += rd + 0.008; rd = 0.0
        sh = Vector((x_ - lo.x, y_ - lo.y, GROUND - lo.z))
        for v in pc: v.co += sh
        x_ += w + 0.008; rd = max(rd, d); W_ = max(W_, x_ - 0.008)
    _BM[n] = bm; BLOCK[n] = (W_, y_ + rd)
# elektroniken
ELEK_ALL, ELEK = [], []
_EP = os.path.join(HERE, 'elektronik.blend')
if os.path.exists(_EP):
    with bpy.data.libraries.load(_EP) as (_src, _dst): _dst.objects = list(_src.objects)
    for o in _dst.objects:
        if o is None: continue
        sc.collection.objects.link(o); ELEK_ALL.append(o)
    bpy.context.view_layer.update()
    for o in ELEK_ALL:
        if o.parent is None and o.name.startswith('E_'):
            cos = [m_.matrix_world @ v.co for m_ in [o] + list(o.children_recursive) if m_.type == 'MESH' for v in m_.data.vertices]
            lo, hi = _bb(cos); ELEK.append(o); BLOCK[o.name] = (hi.x - lo.x, hi.y - lo.y); o['lo'] = tuple(lo)
GRUPPER = [('Kropp', [n for n in PARTS if GROUP.get(n) == 'Kropp' and n != 'kropp']), ('Tak', grp('Tak')), ('Bas', grp('Bas')), ('Skål', grp('Skål')),
           ('Elektronik', [o.name for o in ELEK]), ('Inredning', grp('Inredning'))]
GAP, GGAP, GW = 0.028, 0.07, 0.5
RADER = [['Kropp', 'Tak', 'Bas'], ['Skål', 'Elektronik', 'Inredning']]   # bakre raden och framre raden; kameran sveper over den framre fran vanster och slutar vid skarmramen
GD = dict(GRUPPER); PK = {}; SZ = {}; POS = {}; GX = {}
for g, names in GRUPPER:   # varje grupp packas for sig i rader, storst forst
    x_, y_, rd, gw = 0.0, 0.0, 0.0, 0.0
    for n in sorted(names, key=lambda n: -BLOCK[n][0] * BLOCK[n][1]):
        w, d = BLOCK[n]
        if x_ > 0 and x_ + w > GW: x_ = 0.0; y_ += rd + GAP; rd = 0.0
        PK[n] = (x_, -y_ - d); x_ += w + GAP; rd = max(rd, d); gw = max(gw, x_ - GAP)
    SZ[g] = (gw, y_ + rd)
COLW = [max(SZ[RADER[r][c]][0] for r in range(2)) for c in range(3)]; ROWD = [max(SZ[g][1] for g in rad) for rad in RADER]
LAYOUT_X0 = -(sum(COLW) + 2 * GGAP) / 2; Y_TOP = (sum(ROWD) + GGAP) / 2 + 0.06; y0 = Y_TOP
for r, rad in enumerate(RADER):
    x0 = LAYOUT_X0
    for c, g in enumerate(rad):
        for n in GD[g]: POS[n] = Vector((x0 + PK[n][0], y0 + PK[n][1], 0))
        GX[g] = (round(x0, 2), round(y0, 2)); x0 += COLW[c] + GGAP
    y0 -= ROWD[r] + GGAP
LAYOUT_X1 = LAYOUT_X0 + sum(COLW) + 2 * GGAP; LAYOUT_Y0 = min(p.y for p in POS.values()); LAYOUT_Y1 = Y_TOP; FRAMRAD_Y = Y_TOP - ROWD[0] - GGAP - ROWD[1] / 2
# stommen: roret ligger framfor forsta gruppen, med oppningen mot delarna
_kb = _bb([v.co for v in _BM['kropp'].verts]); KL = _kb[1].x - _kb[0].x; KD = _kb[1].y - _kb[0].y; KH = _kb[1].z - _kb[0].z
POS['kropp'] = Vector((LAYOUT_X0 - 0.07 - KL, FRAMRAD_Y - KD / 2, 0)); BLOCK['kropp'] = (KL, KD)
# Varianter av 0.4 (LENNART_04, prov for Marcus): K = byggsatsen i grupper (nuvarande), A = en lang rak linje som slutar genom stommen och ner i ramen,
# B = byggsatsen, slutar pa LED-skarmen pa golvet som tands, C = ovanifran: lyfter over byggsatsen och dyker ner i ramen,
# D = delarna i ett rutnat pa ett golv som ar en enorm slackt LED-skarm; kameran dyker in i golvets pixlar, E = en gron skanning sveper over delarna.
VAR04 = os.environ.get('LENNART_04', 'D')
def _vrid(n):   # vrider ett block 90 grader i sina egna koordinater, sa att kortsidan hamnar langs x
    W_, D_ = BLOCK[n]
    for v in _BM[n].verts: x, y = v.co.x, v.co.y; v.co.x = D_ - y; v.co.y = x
    BLOCK[n] = (D_, W_)
if VAR04 == 'A':   # alla delar pa en lang rad langs x, kortsidan i fardriktningen. Sist stommen (roret) och efter den skarmramen
    ordn = [n for g in ('Bas', 'Tak', 'Skål', 'Elektronik', 'Inredning', 'Kropp') for n in sorted(GD[g], key=lambda n: -BLOCK[n][0] * BLOCK[n][1]) if n != 'skarmram']
    x_ = 0.0
    for n in ordn + ['skarmram']:
        if n in _BM and BLOCK[n][0] > BLOCK[n][1] + 0.002 and n != 'skarmram': _vrid(n)
        if n == 'skarmram':
            if BLOCK[n][0] > BLOCK[n][1]: _vrid(n)               # ramens langsida tvars fardriktningen, sa att den ligger rak i bild nar kameran tittar ner
            x_ += KL + 0.1 + 0.06                                  # plats for stommen, sedan ramen
        w, d = BLOCK[n]; POS[n] = Vector((x_, -d / 2, 0)); x_ += w + 0.025
    LINE_X1 = POS['skarmram'].x; POS['kropp'] = Vector((LINE_X1 - 0.06 - KL, -KD / 2, 0)); off = x_ / 2   # linjen centreras kring origo, dar ljuset ar
    for n in POS: POS[n].x -= off
    LINE_X1 -= off; LAYOUT_X0, LAYOUT_X1 = -off, x_ - off; print('LINJEN', round(x_, 2), 'm', flush=True)
SKMOD = next((o.name for o in ELEK if o.name.startswith('E_skarmmodul')), None)
if VAR04 == 'D':   # husets 48 delar och LED-skarmen i ett rutnat 7 x 7, en sak per ruta. Skarmen ligger i mittenrutan och kameran dyker ner i den
    alla = ['kropp'] + [n for g in ('Kropp', 'Tak', 'Bas', 'Skål', 'Inredning') for n in sorted(GD[g], key=lambda n: -BLOCK[n][0] * BLOCK[n][1])]
    if SKMOD: alla.insert(len(alla) // 2, SKMOD)
    BLOCK['kropp'] = (KL, KD); CELL = max(max(BLOCK[n]) for n in alla) + 0.05; GX8, GY6 = (7, 7) if SKMOD else (8, 6)
    for i, n in enumerate(alla):
        cx, cy = (i % GX8 - (GX8 - 1) / 2) * CELL, ((GY6 - 1) / 2 - i // GX8) * CELL; w, d = BLOCK[n]; POS[n] = Vector((cx - w / 2, cy - d / 2, 0))
    LAYOUT_X0, LAYOUT_X1, LAYOUT_Y0, LAYOUT_Y1 = -GX8 / 2 * CELL, GX8 / 2 * CELL, -GY6 / 2 * CELL, GY6 / 2 * CELL; print('RUTNAT', round(CELL, 3), flush=True)
for n, bm in _BM.items():
    lo = _bb([v.co for v in bm.verts])[0] if n == 'kropp' else Vector((0, 0, 0)); sh = POS[n] - Vector((lo.x, lo.y, 0)) + (Vector((0, 0, GROUND - lo.z)) if n == 'kropp' else Vector())
    for v in bm.verts: v.co += sh
    d = ORIG_DATA[n].copy(); bm.to_mesh(d); bm.free(); LAYD[n] = d
for o in ELEK:
    lo = Vector(o['lo']); o.location = Vector(o.location) + POS[o.name] - Vector((lo.x, lo.y, 0)) + Vector((0, 0, GROUND - lo.z))
_kc = _bb([v.co for v in LAYD['kropp'].vertices]); K_X0, K_X1 = _kc[0].x, _kc[1].x; K_Y = (_kc[0].y + _kc[1].y) / 2; K_Z = (_kc[0].z + _kc[1].z) / 2
print('KNOLL', 'x', round(LAYOUT_X0, 3), round(LAYOUT_X1, 3), 'y', round(LAYOUT_Y0, 3), round(LAYOUT_Y1, 3), 'stomme', round(K_X0, 3), round(K_X1, 3), round(K_Y, 3), round(K_Z, 3), {g: (round(a_, 2), round(b_, 2)) for g, (a_, b_) in GX.items()}, flush=True)
# nummer 01-48 bredvid husets delar, som i en monteringsanvisning (valbart)
NUMMER = []
if os.environ.get('LENNART_NUMMER', '1') == '1':
    _f = bpy.data.fonts.load('C:/Windows/Fonts/consola.ttf') if os.path.exists('C:/Windows/Fonts/consola.ttf') else None; _nm = mat('nummer', (0.35, 0.37, 0.38), 0.6)
    _ord = ['kropp'] + [n for g, names in GRUPPER if g != 'Elektronik' for n in sorted(names, key=lambda n: (-POS[n].y, POS[n].x))]
    for i, n in enumerate(_ord):
        cu = bpy.data.curves.new('nr%d' % i, 'FONT'); cu.body = '%02d' % (i + 1); cu.size = 0.011
        if _f: cu.font = _f
        o = link(bpy.data.objects.new('nr%d' % i, cu)); o.data.materials.append(_nm); o.location = (POS[n].x, POS[n].y - 0.014, GROUND + 0.0002); NUMMER.append(o)
_rp = [v.co for v in LAYD['skarmram'].vertices]; RAM_C = LAY['skarmram'] + Vector((sum(p.x for p in _rp) / len(_rp), sum(p.y for p in _rp) / len(_rp), max(p.z for p in _rp)))   # skarmramens mitt pa golvet
_xy = _np.array([(p.x, p.y) for p in _rp]); _xy -= _xy.mean(0); _ev = _np.linalg.eigh(_xy.T @ _xy)[1][:, -1]; RAM_A = math.atan2(_ev[1], _ev[0])   # ramens langsida pa golvet
RAM_A = (RAM_A + math.pi / 2) % math.pi - math.pi / 2; RAM_ROLL = math.radians(-23); print('RAMEN', RAM_C, math.degrees(RAM_A), flush=True)
# --- tillbehor till varianterna av 0.4 ---
VAROBJ = []   # syns bara i 0.4
# svart inuti skarmramen, sa att kameran dyker ner i morker (A, C, E, K)
_rlo, _rhi = _bb(_rp); bpy.ops.mesh.primitive_plane_add(size=1, location=(RAM_C.x, RAM_C.y, GROUND + 0.0004)); RSV = bpy.context.active_object
RSV.scale = ((_rhi.x - _rlo.x) * 0.8, (_rhi.y - _rlo.y) * 0.8, 1); _rsm = mat('ram_svart', (0.0, 0.0, 0.0), 1.0); _rsm.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.0; RSV.data.materials.append(_rsm); VAROBJ.append(RSV)
RSV['bara'] = 'ACEK'
# golvet: morknar mot slutet av linjen (A)
_gm = FLOOR.data.materials[0]; _gn = _gm.node_tree; _gp = _gn.nodes['Principled BSDF']; _gtc = _gn.nodes.new('ShaderNodeTexCoord'); _gsx = _gn.nodes.new('ShaderNodeSeparateXYZ')
_gmr = _gn.nodes.new('ShaderNodeMapRange'); _gmix = _gn.nodes.new('ShaderNodeMixRGB'); _gmix.blend_type = 'MULTIPLY'; _gmix.inputs['Fac'].default_value = 1.0
_gmix.inputs['Color1'].default_value = _gp.inputs['Base Color'].default_value[:]; _gn.links.new(_gtc.outputs['Object'], _gsx.inputs[0]); _gn.links.new(_gsx.outputs['X'], _gmr.inputs['Value'])
_gn.links.new(_gmr.outputs[0], _gmix.inputs['Color2']); _gn.links.new(_gmix.outputs[0], _gp.inputs['Base Color'])
_gmr.inputs['To Min'].default_value = 1.0; _gmr.inputs['To Max'].default_value = 1.0
if VAR04 == 'A': _gmr.inputs['From Min'].default_value = LINE_X1 - 1.4; _gmr.inputs['From Max'].default_value = LINE_X1; _gmr.inputs['To Max'].default_value = 0.4
# golvet som LED-skarm (D): samma pixlar som skarmen i 0.5, morkt grona med mjuka morka glipor
PIX = 0.004
if VAR04 == 'D':
    pm = bpy.data.materials.new('golv_skarm'); pm.use_nodes = True; nt_ = pm.node_tree; pp = nt_.nodes['Principled BSDF']; pp.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1); pp.inputs['Roughness'].default_value = 0.9; pp.inputs['Specular IOR Level'].default_value = 0.15
    tc_ = nt_.nodes.new('ShaderNodeTexCoord'); sx_ = nt_.nodes.new('ShaderNodeSeparateXYZ'); nt_.links.new(tc_.outputs['Object'], sx_.inputs[0]); kant = []
    for ax in ('X', 'Y'):
        m1 = nt_.nodes.new('ShaderNodeMath'); m1.operation = 'DIVIDE'; m1.inputs[1].default_value = PIX; nt_.links.new(sx_.outputs[ax], m1.inputs[0])
        m2 = nt_.nodes.new('ShaderNodeMath'); m2.operation = 'FRACT'; nt_.links.new(m1.outputs[0], m2.inputs[0])
        m3 = nt_.nodes.new('ShaderNodeMath'); m3.operation = 'SUBTRACT'; m3.inputs[1].default_value = 0.5; nt_.links.new(m2.outputs[0], m3.inputs[0])
        m4 = nt_.nodes.new('ShaderNodeMath'); m4.operation = 'ABSOLUTE'; nt_.links.new(m3.outputs[0], m4.inputs[0])
        m5 = nt_.nodes.new('ShaderNodeMath'); m5.operation = 'MULTIPLY_ADD'; m5.inputs[1].default_value = -1 / 0.14; m5.inputs[2].default_value = 0.5 / 0.14; m5.use_clamp = True; nt_.links.new(m4.outputs[0], m5.inputs[0]); kant.append(m5)
    mm = nt_.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; nt_.links.new(kant[0].outputs[0], mm.inputs[0]); nt_.links.new(kant[1].outputs[0], mm.inputs[1])
    ma = nt_.nodes.new('ShaderNodeMath'); ma.operation = 'MULTIPLY_ADD'; ma.inputs[1].default_value = 0.75; ma.inputs[2].default_value = 0.25; nt_.links.new(mm.outputs[0], ma.inputs[0])
    PIX_S = nt_.nodes.new('ShaderNodeMath'); PIX_S.operation = 'MULTIPLY'; PIX_S.inputs[1].default_value = 0.5; nt_.links.new(ma.outputs[0], PIX_S.inputs[0])
    pp.inputs['Emission Color'].default_value = (0.024, 0.07, 0.043, 1); GOLV_EM = pp.inputs['Emission Color']
    GOLV_GRON, GOLV_SLUT = (0.024, 0.07, 0.043, 1), (0.0012, 0.0035, 0.0022, 1)   # nar kameran sjunker mot LED-skarmen tonar golvets pixlar ut till nastan slackt, sa att skarmen ar det enda som lyser (valt fore dampat midnattsblatt)
    if os.environ.get('LENNART_GOLV') == 'bla': GOLV_SLUT = (0.009, 0.015, 0.046, 1)   # provet med dampat midnattsblatt
    # ett mjukt sken av tanda pixlar runt LED-skarmen i mitten: 1 + HALO_G * exp(-r^2 / s^2), r fran HALO_X/HALO_Y i golvets koordinater
    HALO_X = nt_.nodes.new('ShaderNodeValue'); HALO_Y = nt_.nodes.new('ShaderNodeValue'); HALO_G = nt_.nodes.new('ShaderNodeValue'); HALO_G.outputs[0].default_value = 0.0
    _dx = nt_.nodes.new('ShaderNodeMath'); _dx.operation = 'SUBTRACT'; nt_.links.new(sx_.outputs['X'], _dx.inputs[0]); nt_.links.new(HALO_X.outputs[0], _dx.inputs[1])
    _dy = nt_.nodes.new('ShaderNodeMath'); _dy.operation = 'SUBTRACT'; nt_.links.new(sx_.outputs['Y'], _dy.inputs[0]); nt_.links.new(HALO_Y.outputs[0], _dy.inputs[1])
    _x2 = nt_.nodes.new('ShaderNodeMath'); _x2.operation = 'MULTIPLY'; nt_.links.new(_dx.outputs[0], _x2.inputs[0]); nt_.links.new(_dx.outputs[0], _x2.inputs[1])
    _r2 = nt_.nodes.new('ShaderNodeMath'); _r2.operation = 'MULTIPLY_ADD'; nt_.links.new(_dy.outputs[0], _r2.inputs[0]); nt_.links.new(_dy.outputs[0], _r2.inputs[1]); nt_.links.new(_x2.outputs[0], _r2.inputs[2])
    _ex = nt_.nodes.new('ShaderNodeMath'); _ex.operation = 'MULTIPLY'; _ex.inputs[1].default_value = -1 / 0.22 ** 2; nt_.links.new(_r2.outputs[0], _ex.inputs[0])
    _e = nt_.nodes.new('ShaderNodeMath'); _e.operation = 'EXPONENT'; nt_.links.new(_ex.outputs[0], _e.inputs[0])
    _g = nt_.nodes.new('ShaderNodeMath'); _g.operation = 'MULTIPLY_ADD'; nt_.links.new(_e.outputs[0], _g.inputs[0]); nt_.links.new(HALO_G.outputs[0], _g.inputs[1]); _g.inputs[2].default_value = 1.0
    _hs = nt_.nodes.new('ShaderNodeMath'); _hs.operation = 'MULTIPLY'; nt_.links.new(PIX_S.outputs[0], _hs.inputs[0]); nt_.links.new(_g.outputs[0], _hs.inputs[1])
    nt_.links.new(_hs.outputs[0], pp.inputs['Emission Strength'])
    FLOOR_D = pm
# skanningen (E): en tunn gron linje pa golvet och ett smalt gront ljus som sveper over delarna
if VAR04 == 'E':
    bpy.ops.mesh.primitive_plane_add(size=1); SCANB = bpy.context.active_object; SCANB.scale = (0.006, LAYOUT_Y1 - LAYOUT_Y0 + 0.2, 1); SCAN_M = mat('skanning', (0, 0, 0), 0.5)
    P_s = SCAN_M.node_tree.nodes['Principled BSDF']; P_s.inputs['Emission Color'].default_value = (0.38, 0.84, 0.59, 1); P_s.inputs['Emission Strength'].default_value = 6.0; SCANB.data.materials.append(SCAN_M); VAROBJ.append(SCANB)
    sl = bpy.data.lights.new('skanljus', 'AREA'); sl.shape = 'RECTANGLE'; sl.size = 0.03; sl.size_y = LAYOUT_Y1 - LAYOUT_Y0 + 0.3; sl.energy = 12; sl.color = (0.38, 0.9, 0.6); SCANL = link(bpy.data.objects.new('skanljus', sl)); VAROBJ.append(SCANL)
# LED-skarmen bland elektroniken (B): dess bild tands
SKARM_B = None
for o in ELEK_ALL:
    if o.type == 'MESH' and o.name.startswith('bild') and o.parent and o.parent.name.startswith('E_skarmmodul'): SKARM_B = o
SKARM_P = SKARM_B.data.materials[0].node_tree.nodes['Principled BSDF'] if SKARM_B else None
for o in VAROBJ: o.hide_render = True
if VAR04 == 'D': FLOOR.data.materials[0] = FLOOR_D
if VAR04 == 'A':   # ett langt mjukt ljus over hela linjen
    la = bpy.data.lights.new('linjeljus', 'AREA'); la.shape = 'RECTANGLE'; la.size = LAYOUT_X1 - LAYOUT_X0 + 0.6; la.size_y = 0.6; la.energy = 260; la.color = (1, 0.82, 0.64)
    LA = link(bpy.data.objects.new('linjeljus', la)); LA.location = (0, -0.55, 0.75); LA.rotation_euler = (Vector((0, 0.05, GROUND)) - LA.location).to_track_quat('-Z', 'Y').to_euler(); LA['bara'] = 'A'; VAROBJ.append(LA); LA.hide_render = True

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
GOLV_E = [l.data.energy for l in L['golv']]; GOLV_P = [l.location.copy() for l in L['golv']]; SNITT_E = [l.data.energy for l in L['snitt']]
WE0 = [n for n in wn.nodes if n.type == 'VALTORGB'][0].color_ramp.elements[0]; WE0_C = tuple(WE0.color)
OVERG = VAR03 == 'H' and VAR04 == 'D'   # det osynliga klippet: 0.3 landar rakt ovanfor golvet, 0.4 borjar i exakt samma lage och stiger
H0 = 0.06; FLOOR_P4 = FLOOR.location.copy()
D_START = Vector(((LAYOUT_X0 + LAYOUT_X1) / 2, (LAYOUT_Y0 + LAYOUT_Y1) / 2, GROUND))      # mitt i rutnatet, i hornet mellan fyra rutor dar golvet ar tomt; 0.4 stiger rakt upp harifran
if VAR04 == 'D' and SKMOD:   # mittenrutan har nu skarmen, sa 0.4 borjar i hornet snett nedanfor den. Avstandet ar helt antal golvpixlar, sa att pixlarna i 0.3 ar desamma
    _h = round(CELL / 2 / PIX) * PIX; D_START = D_START + Vector((_h, -_h, 0))
D_SKARM = VAR04 == 'D' and SKMOD is not None and SKARM_B is not None   # 0.4 slutar i LED-skarmen i stallet for i golvets pixlar
T_E4 = END if D_SKARM else T_E   # med LED-skarmen ar 0.4 och 0.5 en enda tagning: kameran svavar over skarmen, som visar VERIFIERAR, och aker in i pixlarna till titeln
P3 = Vector((0.62, -0.012, -0.0305))                                                     # platsen pa golvet framfor huset dar 0.3 landar
FLOOR_P3 = FLOOR_P4 + (P3 - D_START)                                                        # golvet flyttas sa att pixlarna under P3 ar exakt de under D_START
def YAW(t): return math.radians(90 - 68 * sm(t, 8.9, T_D + 2.2))                           # kamerans vridning, hojd och brannvidd ar gemensamma kurvor over klippet,
def HUP(t): return H0 * (2.9 / H0) ** sm(t, 9.1, 10.6)                                      # sa att rorelsen fortsatter utan avbrott (hojden stiger med jamn upplevd fart)
def LENS_G(t): return 85 - 50 * sm(t, 8.86, 9.12) - 5 * sm(t, 9.12, 10.4)

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

def cam03(t, tm, p):   # kameran i varianterna av 0.3
    if VAR03 == 'S':     # rakt fran sidan utan perspektiv. Foljer noten ner och fortsatter nerat ut i morkret
        f_ = sm(t, 8.0, 8.9); dn = acc(t, 8.8, T_D, 1.8)
        cy = 0.035 + (0.008 - 0.035) * f_; cz = 0.10 + (0.045 - 0.10) * f_ - 0.13 * dn
        eye = Vector((0.6, cy, cz)); camera(eye, eye + Vector((-1, 0, 0)), 50, 32); cam_d.type = 'ORTHO'; cam_d.ortho_scale = 0.30 - 0.06 * sm(t, 7.2, 8.6); cam_d.dof.use_dof = False
    elif VAR03 == 'M':   # makro: borjar pa hogen i magasinet, tiltar och drar skarpan till noten i fickan, kretsar under slowmotion, noten rullar mot kameran
        pile = Vector((0.0, 0.074, 0.106)); tgt = mix(pile, p + (AXLE - p) * 0.25, sm(t, 6.95, 7.45)); tgt = mix(tgt, p, sm(t, 8.2, 8.75))
        dive = acc(t, 8.95, T_D, 2.0); tgt = tgt + Vector((0, -0.006, -0.05)) * dive
        az = math.radians(24 + 24 * sm(t, 7.6, 8.7)); el = math.radians(7 + 20 * sm(t, 8.45, 9.0) + 40 * dive); r = 0.25 - 0.06 * sm(t, 7.4, 8.5) + 0.04 * sm(t, 8.5, 9.0)
        eye = tgt + r * Vector((math.cos(el) * math.cos(az), -math.cos(el) * math.sin(az), math.sin(el)))
        camera(eye, tgt, 100, 2.4, mix(pile, p, sm(t, 7.0, 7.4)))   # skarpan flyttas fran hogen till noten och ligger sedan pa noten
    elif VAR03 == 'H':   # last vid hjulet: kameran rullar med hjulet sa att hjulet och noten star still och resten snurrar, slapper sedan, foljer noten ner och landar rakt ovanfor golvet
        rel = sm(t, 8.1, 8.95); roll = math.radians(wheel_angle(t)) * (1 - rel); D = 0.34 + 0.30 * sm(t, 7.05, 8.2)
        tgt = mix(AXLE, Vector((0, -0.012, 0.028)), sm(t, 8.15, 8.9))
        if not OVERG:
            dive = acc(t, 8.9, T_D, 2.0); el = math.radians(55) * dive
            eye = tgt + D * Vector((math.cos(el), 0, math.sin(el))); camera(eye, tgt + Vector((0, 0, -0.04)) * dive, 85, 4.0, tgt, roll=roll); return
        b = sm(t, 8.8, 9.1); w = sm(t, 8.82, 9.08)                                   # noten hinner landa i skalen, sedan ner mot golvet och borjar stiga redan fore klippet
        eye = mix(tgt + Vector((D, 0, 0)), P3 + Vector((0, 0, HUP(t))), b)
        f_ = Vector((-1, 0, 0)).slerp(Vector((0, 0, -1)), w) if 0 < w < 1 else (Vector((-1, 0, 0)) if w <= 0 else Vector((0, 0, -1)))
        y_ = YAW(t); uh = mix(Vector((0, 0, 1)), Vector((-math.sin(y_), math.cos(y_), 0)), w).normalized(); rt_ = f_.cross(uh).normalized(); up_ = rt_.cross(f_)
        CAM.location = eye; CAM.rotation_euler = (Matrix((rt_, up_, -f_)).transposed() @ Matrix.Rotation(roll, 3, 'Z')).to_euler()
        golv = min(2.0, (eye.z - P3.z) / max(-f_.z, 1e-3)); cam_d.lens = LENS_G(t); cam_d.dof.aperture_fstop = 4.0 + 1.6 * b
        cam_d.dof.focus_distance = max(0.03, (tgt - eye).length * (1 - w) + golv * w)          # skarpan foljer med fran noten till golvet

def state(t):
    cam_d.type = 'PERSP'; cam_d.dof.use_dof = True; FLOOR.location = FLOOR_P4; WE0.color = WE0_C
    if VAR04 == 'D': HALO_G.outputs[0].default_value = 0.0; GOLV_EM.default_value = GOLV_GRON
    for l, e_, p_ in zip(L['golv'], GOLV_E, GOLV_P): l.location = p_; l.data.energy = e_
    for l, e_ in zip(L['snitt'], SNITT_E): l.data.energy = e_
    for o in ELEK_ALL + NUMMER + VAROBJ: o.hide_render = not (T_D <= t < T_E4)   # elektroniken och numren finns bara i 0.4
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
        tm = TAU_M(t) if VAR03 == 'M' else t
        if VAR03 in 'SM':
            for n in CUT:
                if n not in MECH: PARTS[n].hide_render = True
        for n in ('lucka', 'lucka_vit'): PARTS[n].matrix_world = ORIG_M[n] @ Matrix.Rotation(math.radians(hatch_angle(tm)), 4, 'X')
        SCREEN.hide_render = True; p, th = nut_path(tm); PARTS['doserhjul'].matrix_world = ORIG_M['doserhjul'] @ Matrix.Rotation(math.radians(wheel_angle(tm)), 4, 'X')
        NUTS[0].hide_render = False; NUTS[0].matrix_world = Matrix.Translation(p) @ Matrix.Rotation(-th, 4, 'X') @ Matrix.Scale(NR, 4)
        for i, (x, y, z, rx, ry, rz) in enumerate(PILE):   # resten av magasinet: en full hog ovanpa hjulet
            NUTS[i + 1].hide_render = False; NUTS[i + 1].matrix_world = Matrix.Translation((x, y, z)) @ Euler((rx, ry, rz)).to_matrix().to_4x4() @ Matrix.Scale(NR, 4)
        if OVERG:
            FLOOR.hide_render = False; FLOOR.location = FLOOR_P3; WE0.color = (0.010, 0.034, 0.022, 1); kl = sm(t, 8.7, 9.15)
            for l, e_, p_ in zip(L['golv'], GOLV_E, GOLV_P): l.hide_render = False; l.location = p_ + (P3 - D_START); l.data.energy = e_ * kl
            for l, e_ in zip(L['snitt'], SNITT_E): l.data.energy = e_ * (1 - kl)
        if VAR03 != 'K': cam03(t, tm, p); return
        k = out(t, T_C, 8.3, 2.6); follow = sm(t, 8.1, 8.85); tgt = mix((0, 0.05, 0.088), (0, 0.006, 0.03), follow)
        dive = acc(t, 8.95, T_D, 2.0); tgt = tgt + Vector((0, -0.01, -0.09)) * dive     # overgang ut: snabb tilt nerat forbi skalen
        camera(mix((0.62, 0.02, 0.135), (0.36, -0.075, 0.10), k) + Vector((0, -0.05, -0.05)) * follow + Vector((0, 0, -0.02)) * dive, tgt, 60, 5.6, (0.0, tgt.y, tgt.z))
    elif t < T_E4:   # 0.4 (och 0.5 med LED-skarmen): se VAR04 overst i upplaggningen. K: borjar inne i stommen (roret), aker ut, stiger och sveper over grupperna, sedan ner genom skarmramen
        lights('golv'); FLOOR.hide_render = False; u = t - T_D
        for b in BUMPS: b.inputs['Strength'].default_value = 0.2
        for n, o in PARTS.items(): o.data = LAYD[n]; o.matrix_world = Matrix.Translation(LAY[n])
        for o in CAMPARTS: o.hide_render = True
        SCREEN.hide_render = True
        for o in VAROBJ: o.hide_render = VAR04 not in o.get('bara', VAR04)
        for l, e0 in zip(L['golv'], GOLV_E): l.data.energy = e0 * (0.3 if VAR04 == 'E' else 1.0)
        if VAR04 == 'D':
            for o in ELEK_ALL: o.hide_render = True
            if D_SKARM:   # bara LED-skarmen syns av elektroniken. Den vaknar nar kameran ar som hogst och lyser in i klippet (slutbilden ar dess morka pixlar under texten, som 0.5 borjar)
                _sk = bpy.data.objects[SKMOD]
                for o in [_sk] + list(_sk.children_recursive): o.hide_render = False
                SKARM_B.data.materials[0] = SCR['vantar'] if (u > 1.55 and not (1.6 < u < 1.66) and not (1.74 < u < 1.77)) else SCR['av']
                _n = round(t * FPS)   # rorelseoskarpans delrutor far samma bild som rutan
                if _n in GLITCH: SKARM_B.data.materials[0] = SCR[GLITCH[_n]]   # skarmen glitchar over fran VANTAR till VERIFIERAR nar kameran kommit fram
                elif _n > max(GLITCH): SKARM_B.data.materials[0] = SCR['av' if t >= END - 0.06 else dots(t)]   # VERIFIERAR, punkterna pa pipen, slacks infor titeln
                _lc = FLOOR.matrix_world.inverted() @ SKARM_B.matrix_world.translation; HALO_X.outputs[0].default_value = _lc.x; HALO_Y.outputs[0].default_value = _lc.y
                _b = sm(t, 11.6, 12.8); GOLV_EM.default_value = tuple(g_ + (b_ - g_) * _b for g_, b_ in zip(GOLV_GRON, GOLV_SLUT))
                HALO_G.outputs[0].default_value = 5.0 * sm(u, 1.6, 2.3) * (1 - 0.75 * sm(t, 12.0, 13.0))    # golvets pixlar runt skarmen tands strax efter den och dampas nar kameran kommer ner, sa att skarmen ar det ljusaste
        if VAR04 in 'KBE':
            ext = sm(u, 0.0, 1.15); rise = sm(u, 0.55, 2.0); pan = sm(u, 0.6, 2.6)
            e_in = Vector((K_X0 + 0.04 + (K_X1 + 0.16 - K_X0 - 0.04) * ext, K_Y, K_Z + 0.03 * ext))
            t_in = Vector((K_X1 + 0.7, K_Y + 0.05, GROUND + 0.01 + 0.3 * (1 - out(u, 0, 0.6, 2.0))))      # overgang in: tilten fran 0.3 fortsatter nerat, inne i roret
            px = LAYOUT_X0 + 0.3 + (LAYOUT_X1 - 0.75 - LAYOUT_X0 - 0.3) * pan
            e_ov = Vector((px - 0.05, LAYOUT_Y0 - 0.38, 0.58)); t_ov = Vector((px + 0.1, (LAYOUT_Y0 + LAYOUT_Y1) / 2 - 0.05, GROUND))
            eye = mix(e_in, e_ov, rise); tgt = mix(t_in, t_ov, rise)
            crane = sm(t, T_E - 1.45, T_E - 0.45); dive = acc(t, T_E - 0.8, T_E - 0.02, 2.0)                        # overgang ut: upp over malet pa golvet och rakt ner
            MAL = RAM_C; hojd = 0.30 - 0.255 * dive
            if VAR04 == 'B' and SKARM_B:   # malet ar LED-skarmen bland elektroniken. Den tands, visar vantbilden och slocknar strax fore klippet (0.5 borjar pa den slackta skarmen)
                MAL = SKARM_B.matrix_world.translation + Vector((0, -0.011, 0)); hojd = 0.30 - 0.245 * dive   # slutar pa den morka delen under texten, som 0.5 borjar
                pa = u > 2.25 and not (2.3 < u < 2.36)   # tands med ett litet flimmer och ar tand in i klippet; slutbilden ar skarmens morka pixlar, som i 0.5
                SKARM_B.data.materials[0] = SCR['vantar'] if pa else SCR['av']
            if VAR04 == 'E':   # skanningen sveper fran vanster till skarmramen, en gron linje och ett smalt gront ljus
                xs = LAYOUT_X0 - 0.1 + (RAM_C.x + 0.45 - LAYOUT_X0 + 0.1) * sm(u, 0.25, 2.5); my = (LAYOUT_Y0 + LAYOUT_Y1) / 2   # passerar ramen och tonar ut innan kameran dyker
                SCANB.location = (xs, my, GROUND + 0.0006); SCANL.location = (xs, my, GROUND + 0.22); SCANL.rotation_euler = (0, 0, 0)
                SCAN_M.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 6.0 * sm(u, 0.15, 0.4) * (1 - sm(u, 2.35, 2.6)); SCANL.data.energy = 12 * sm(u, 0.15, 0.4) * (1 - sm(u, 2.35, 2.6))
            lens = (20 + 16 * rise) * (1 - crane) + 85 * crane
            if crane > 0: tgt = mix(tgt, MAL, crane); eye = mix(eye, MAL + Vector((0.0001, -0.0001, hojd)), crane)
            camera(eye, tgt, lens, (4.0 - 1.6 * rise) * (1 - crane) + 5.6 * crane)
            if crane > 0:    # nar kameran tittar rakt ner styrs upp-riktningen sjalv (mot +Y), sa att malet ligger rakt och still hela vagen ner
                f_ = (Vector(tgt) - Vector(eye)).normalized(); u_ = Vector((0, crane, 1 - crane)).normalized(); rt_ = f_.cross(u_).normalized(); up_ = rt_.cross(f_)
                CAM.rotation_euler = (Matrix((rt_, up_, -f_)).transposed() @ Matrix.Rotation(math.radians(2.5) * crane, 3, 'Z')).to_euler()
        elif VAR04 == 'A':   # en lang linje: lagt over raden, in genom stommen, ut och rakt ner i ramen
            Kin = K_X0 - 0.06; L0 = LAYOUT_X0 - 0.35; t1, t2 = 1.85, 2.45
            a1 = (Kin - 0.3 - L0) / t1; a2 = (K_X1 + 0.03 - Kin + 0.3) / (t2 - t1)
            def herm(s, p0, p1, v0, v1, dt): h00 = 2 * s ** 3 - 3 * s ** 2 + 1; h10 = s ** 3 - 2 * s ** 2 + s; h01 = -2 * s ** 3 + 3 * s ** 2; h11 = s ** 3 - s ** 2; return h00 * p0 + h10 * dt * v0 + h01 * p1 + h11 * dt * v1
            vmid = min(1.3 * a1, 2.4 * a2)
            if u < t1: x = herm(u / t1, L0, Kin - 0.3, 0.6 * a1, vmid, t1)
            elif u < t2: x = herm((u - t1) / (t2 - t1), Kin - 0.3, K_X1 + 0.03, vmid, 0.6, t2 - t1)
            else: x = K_X1 + 0.03 + 0.6 * (u - t2) * (1 - sm(u, t2, t2 + 0.4))
            ned = sm(u, t1 - 0.6, t1 + 0.1); crane = sm(u, t2 - 0.1, t2 + 0.5); dive = acc(t, T_E - 0.8, T_E - 0.02, 2.0)   # ut ur roret: upp och over ramen, sedan rakt ner i den
            eye = Vector((x, K_Y * ned, GROUND + 0.2 + (K_Z - GROUND - 0.2) * ned))
            fram = Vector((x + 0.8, K_Y * ned, GROUND + 0.02 + (K_Z - GROUND - 0.02) * ned + 0.35 * (1 - out(u, 0, 0.6, 2.0))))   # overgang in: tilten fran 0.3 fortsatter nerat
            eye = mix(eye, RAM_C + Vector((0.0001, 0.0, 0.2 - 0.155 * dive)), crane); tgt = mix(fram, RAM_C, crane)
            f_ = (tgt - eye).normalized(); upp = mix(Vector((0, 0, 1)), Vector((1, 0, 0)), crane).normalized(); rt_ = f_.cross(upp).normalized(); up_ = rt_.cross(f_)
            CAM.location = eye; CAM.rotation_euler = Matrix((rt_, up_, -f_)).transposed().to_euler(); cam_d.lens = (24 + 6 * ned) * (1 - crane) + 85 * crane; cam_d.dof.aperture_fstop = 4.0 + 1.6 * crane; cam_d.dof.focus_distance = max(0.03, (tgt - eye).length)
        elif VAR04 in 'CD':   # ovanifran: borjar tatt over golvet, lyfter och visar allt, sedan rakt ner (C: i ramen, D: i golvets pixlar)
            mid = Vector(((LAYOUT_X0 + LAYOUT_X1) / 2, (LAYOUT_Y0 + LAYOUT_Y1) / 2, GROUND))
            if VAR04 == 'C': start = Vector(((K_X0 + K_X1) / 2, K_Y, GROUND)); H = 1.35; MAL = RAM_C; slut_h = 0.045; slut_l = 85
            elif OVERG: start = D_START; H = 2.9; MAL = Vector((LAYOUT_X1 + 0.3, LAYOUT_Y0 - 0.3, GROUND)); slut_l = 50; slut_h = 110 * PIX * slut_l / 36
            else: start = POS['kropp'] + Vector((KL / 2, KD / 2, GROUND)); H = 2.9; MAL = Vector((LAYOUT_X1 + 0.3, LAYOUT_Y0 - 0.3, GROUND)); slut_l = 50; slut_h = 110 * PIX * slut_l / 36
            if D_SKARM:   # malet ar LED-skarmen i mitten: kameran stiger, centrerar skarmen och dyker rakt ner i den, och slutar som B pa den morka delen under texten
                MAL = SKARM_B.matrix_world.translation.copy(); mid = Vector((MAL.x, MAL.y, GROUND)); slut_l = 85; slut_h = MAL.z - GROUND + 0.055
            upp_ = sm(u, 0.1, 2.0); dyk = acc(u, 2.25, 3.38, 2.0); yaw = math.radians(22) * sm(u, 0.2, 2.2) * (1 - sm(u, 2.3, 3.2))
            c_ = mix(start, mid, sm(u, 0.1, 1.9)); c_ = mix(c_, MAL, sm(u, 2.1, 3.0))
            if OVERG: h = HUP(t); c_ = mix(start, mid, sm(u, 0.35, 1.9)); c_ = mix(c_, MAL, sm(u, 2.1, 3.0))   # stiger med jamn upplevd fart, sidled forst nar kameran kommit upp
            else: h = 0.32 + (H - 0.32) * upp_
            if D_SKARM: dyk = 0.0   # nedfarden mot skarmen styrs langre ner
            h = h + (slut_h - h) * dyk
            if OVERG: yaw = YAW(t) * (1 - sm(u, 2.3, 3.2)) + (math.radians(2.5) * sm(u, 2.3, 3.2) if D_SKARM else 0)   # samma lutning som 0.5 borjar med
            eye = Vector((c_.x, c_.y, GROUND + h)); lut = 1.0 if OVERG else sm(u, 0.0, 0.45)
            f_ = mix(Vector((0, 0.75, -0.66)), Vector((0, 0, -1)), lut).normalized()        # overgang in: tilten fran 0.3 fortsatter ner till rakt ovanifran
            upp = Vector((-math.sin(yaw), math.cos(yaw), 0)) * lut + Vector((0, 0, 1)) * (1 - lut); rt_ = f_.cross(upp).normalized(); up_ = rt_.cross(f_)
            CAM.location = eye; CAM.rotation_euler = Matrix((rt_, up_, -f_)).transposed().to_euler()
            cam_d.lens = (LENS_G(t) if OVERG else 30) + (slut_l - 30) * dyk; cam_d.dof.aperture_fstop = 5.6; cam_d.dof.focus_distance = max(0.05, eye.z - GROUND)
            if D_SKARM and t > 11.4:   # ner mot LED-skarmen i jamn upplevd fart, svavar lutad over den medan den verifierar, och aker sedan rakt in tills pixlarna fyller bilden som i titeln
                C = SKARM_B.matrix_world.translation.copy()
                s_ = sm(t, 11.4, 13.0); hv = sm(t, 12.9, 14.6); p_ = acc(t, 14.45, END - 0.08, 2.2)
                d0 = GROUND + 2.9 - C.z; dh = 0.14 * (1 - 0.1 * hv); d = d0 * (dh / d0) ** s_ * (0.058 / dh) ** p_   # 0,058 m och 85 mm: ca 84 pixlar over bildbredden, som titelns rutnat
                a_ = math.radians(18 * s_ - 4 * hv) * (1 - p_); tg = C + Vector((0.004 * p_, 0, 0))
                dv = Vector((0, -math.sin(a_), math.cos(a_))); yw = math.radians(22) * (1 - s_)
                f_ = -dv; upp = Vector((-math.sin(yw), math.cos(yw), 0)); rt_ = f_.cross(upp).normalized(); up_ = rt_.cross(f_)
                CAM.location = tg + dv * d; CAM.rotation_euler = Matrix((rt_, up_, -f_)).transposed().to_euler()
                cam_d.lens = 30 + 20 * s_ + 35 * p_; cam_d.dof.aperture_fstop = 5.6 - 2.8 * s_ + 9 * p_; cam_d.dof.focus_distance = d
    else:            # 0.5 tatt pa skarmen: VERIFIERAR...
        lights('makro'); k = out(t, T_E, END, 1.8); SCREEN.data.materials[0] = SCR['av' if (t >= END - 0.06 or t < T_E + 0.3) else dots(t)]
        ent = out(t, T_E, T_E + 1.1, 2.6)       # overgang in fran 0.4: borjar tatt mot den slackta skarmen och backar ut ur den, skarmen tands
        push = acc(t, 14.5, END - 0.08, 2.2)    # overgang till titeln: kameran aker in tills skarmens pixlar fyller bilden (ca 80 pixlar over bildbredden, samma som titelns rutnat)
        for b in BUMPS: b.inputs['Strength'].default_value = 0.35
        camera(orbit(S, (16 - 16 * k) * (1 - push) * ent, 0.045 + ((0.3 - 0.075 * k) * (1 - push) + 0.058 * push - 0.045) * ent, 0.004 * (1 - push) * ent), S + Vector((0.004 * push, 0.0034 * max(push, 1 - ent), 0)), 85, 2.8 + 9 * push + 6 * (1 - ent), focus=S + Vector((0, 0.0034, 0)), roll=math.radians(2.5 * (1 - k)) * (1 - push) * ent)

# Omtajmning: par av (ny tid, ursprunglig tid) vid varje fras, linjart daremellan
WARP = [(0.0, 0.0), (15.2, 15.2)]   # ingen omtajmning: tiderna foljer den egna inspelningen av introt. Tajmas om nar den riktiga rosten ar inspelad.
def warp(t):
    for (n0, o0), (n1, o1) in zip(WARP, WARP[1:]):
        if t <= n1: return o0 + (o1 - o0) * (t - n0) / (n1 - n0)
    return WARP[-1][1]
def _blur_t(sc_):   # rorelseoskarpans delrutor stannar i samma scen som rutan, sa att inget blandas over klippen
    t, t0 = sc_.frame_current_final / FPS, sc_.frame_current / FPS
    for g in ((T_C, T_D) if D_SKARM else (T_C, T_D, T_E)):
        if t0 >= g > t: t = g
        if t0 < g <= t: t = g - 1e-4
    return t
bpy.app.handlers.frame_change_pre.append(lambda sc_, *_: state(_blur_t(sc_)) if sc_.render.use_motion_blur else None)
frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(WARP[-1][0] * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    # forsta rutan efter klippet till 0.3 renderas utan rorelseoskarpa (annars blandades 0.2 in)
    if VAR03 != 'K' and T_C + 0.03 <= f / FPS < ((13.4 if D_SKARM else T_E) if OVERG else T_D): sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5; sc.frame_set(f); state(_blur_t(sc))
    else: sc.render.use_motion_blur = False; state(min(warp(f / FPS), END - 0.001))
    bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
