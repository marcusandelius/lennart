# Storyboardrutor for Projekt Lennart, renderade fran den riktiga modellen (lennarts-matstation.glb).
# Kor:  blender -b -P render_frames.py -- <ut-mapp> <bredd> <samples> [rutnamn ...]
# Djur ar platshallare (dekalerna), elektronik och skrivare ar enkla block. Inget av det ar slutmaterial.
import bpy, bmesh, sys, os, math, json, random, traceback
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, SAMPLES, ONLY = a[0], int(a[1]), int(a[2]), a[3:]
OUT = os.path.abspath(OUT); os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = 'CYCLES'; pr = bpy.context.preferences.addons['cycles'].preferences; sc.cycles.device = 'CPU'
for kind in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
    try:
        pr.compute_device_type = kind; pr.get_devices(); ds = [d for d in pr.devices if d.type == kind]
        if ds:
            for d in pr.devices: d.use = d.type == kind
            sc.cycles.device = 'GPU'; break
    except Exception: pass
print('DEVICE', sc.cycles.device, flush=True)
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6
sc.render.resolution_x = WIDTH; sc.render.resolution_y = WIDTH * 9 // 16
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 90
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception as e: print('look', e)
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
BG = sc.world.node_tree.nodes['Background']

# ---------- modellen ----------
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, 'lennarts-matstation.glb'))
PARTS = {o.name: o for o in bpy.data.objects if o.type == 'MESH'}
GROUP = {d['name']: d['group'] for d in json.load(open(os.path.join(ROOT, 'delar.json'), encoding='utf-8'))}
ORIG_M = {n: o.matrix_world.copy() for n, o in PARTS.items()}
ORIG_MAT = {n: o.data.materials[0] for n, o in PARTS.items()}
ORIG_DATA = {n: o.data for n, o in PARTS.items()}
for o in PARTS.values():
    for p in o.data.polygons: p.use_smooth = False
def grp(*gs): return [n for n in PARTS if GROUP.get(n) in gs]
GROUND = -0.037

def mat(name, col, rough=0.6, emit=0.0, alpha=1.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    p.inputs['Alpha'].default_value = alpha
    if emit: p.inputs['Emission Color'].default_value = (*col, 1); p.inputs['Emission Strength'].default_value = emit
    return m
def img_mat(name, path, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(path); t.extension = 'CLIP'
    nt.links.new(t.outputs['Color'], p.inputs['Base Color']); nt.links.new(t.outputs['Alpha'], p.inputs['Alpha']); p.inputs['Roughness'].default_value = 0.9
    if emit: nt.links.new(t.outputs['Color'], p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value = emit
    return m

TEMP = []   # allt som skapas for en ruta och tas bort efterat
def add(o): sc.collection.objects.link(o); TEMP.append(o); return o
def quad(name, w, h, m, loc, rot=(0, 0, 0)):   # staende plan i XZ, framsida mot -Y, origo i nederkant
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, h), (-w / 2, 0, h)], [], [(0, 1, 2, 3)])
    me.uv_layers.new(); uv = me.uv_layers[0].data
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv[i].uv = c
    me.materials.append(m); o = bpy.data.objects.new(name, me); o.location = loc; o.rotation_euler = rot; return add(o)
def prim(kind, m, loc, scale=(1, 1, 1), rot=(0, 0, 0), **kw):
    {'cube': bpy.ops.mesh.primitive_cube_add, 'cyl': bpy.ops.mesh.primitive_cylinder_add, 'sphere': bpy.ops.mesh.primitive_uv_sphere_add,
     'cone': bpy.ops.mesh.primitive_cone_add, 'torus': bpy.ops.mesh.primitive_torus_add, 'plane': bpy.ops.mesh.primitive_plane_add}[kind](location=loc, rotation=rot, **kw)
    o = bpy.context.active_object; o.scale = scale; o.data.materials.append(m); TEMP.append(o)
    if kind in ('sphere', 'cyl', 'cone', 'torus'):
        for p in o.data.polygons: p.use_smooth = True
    return o
def light(loc, target, power, size=0.6, col=(1, 1, 1), kind='AREA'):
    d = bpy.data.lights.new('l', kind); d.energy = power; d.color = col
    if kind == 'AREA': d.size = size
    if kind == 'SUN': d.angle = size
    o = bpy.data.objects.new('l', d); o.location = loc; o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return add(o)
cam_d = bpy.data.cameras.new('cam'); CAM = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(CAM); sc.camera = CAM; cam_d.clip_start = 0.005
def camera(eye, target, lens=70, fstop=None, focus=None):
    CAM.location = eye; CAM.rotation_euler = (Vector(target) - Vector(eye)).to_track_quat('-Z', 'Y').to_euler(); cam_d.lens = lens
    cam_d.dof.use_dof = fstop is not None
    if fstop: cam_d.dof.aperture_fstop = fstop; cam_d.dof.focus_distance = (Vector(focus or target) - Vector(eye)).length
def world(col, s=1.0): BG.inputs[0].default_value = (*col, 1); BG.inputs[1].default_value = s
def show(names):
    for n, o in PARTS.items(): o.hide_render = n not in names
def move(names, d):
    for n in names: PARTS[n].matrix_world = Matrix.Translation(d) @ PARTS[n].matrix_world
def override(names, m):
    for n in names: PARTS[n].data.materials[0] = m
def cut(names, z):   # skar av delar vid hojden z (halvfardig utskrift)
    for n in names:
        o = PARTS[n]; o.data = o.data.copy(); bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=o.matrix_world.inverted() @ Vector((0, 0, z)), plane_no=(0, 0, 1), clear_outer=True)
        bm.to_mesh(o.data); bm.free()
def reset():
    for o in TEMP:
        try: bpy.data.objects.remove(o, do_unlink=True)
        except Exception: pass
    TEMP.clear()
    for n, o in PARTS.items(): o.matrix_world = ORIG_M[n]; o.data = ORIG_DATA[n]; o.data.materials[0] = ORIG_MAT[n]; o.hide_render = False
    sc.render.use_freestyle = False; world((0.004, 0.004, 0.005))

SCREENS = {k: img_mat('scr_' + k, os.path.join(ROOT, f'skarm-{f}.png'), emit=2.2) for k, f in
           [('vantar', 'vantar'), ('verifierar', 'verifierar'), ('granted', 'access-granted'), ('denied', 'access-denied')]}
DECAL = {'lennart': img_mat('d_lennart', os.path.join(ROOT, 'dekal-lennart.png')), 'skata': img_mat('d_skata', os.path.join(ROOT, 'dekal-skata.png'))}
def screen(state):   # skarmbilden pa ett plan precis bakom skarmramen (README)
    return quad('skarm', 0.049, 0.0362, SCREENS[state], (0, 0.0034, 0.0899))
def animal(kind, loc, h=0.2, face=(0, -1)):   # platshallare: dekalen som staende skylt, vriden mot kameran
    return quad(kind, h, h, DECAL[kind], loc, (0, 0, math.atan2(face[0], -face[1])))
def studio(key=(-0.7, -0.8, 0.9), power=16, floor=True, rim=None):
    world((0.004, 0.004, 0.005)); light(key, (0, 0.05, 0.1), power, 0.7)
    if rim: light(rim, (0, 0.05, 0.12), power * 0.6, 0.3)
    if floor: prim('plane', mat('floor', (0.012, 0.012, 0.014), 0.35), (0, 0, GROUND), size=8)
def outdoors(ground=(0.10, 0.22, 0.05), sun=(-1.5, 2.0, 0.9), warm=(1.0, 0.78, 0.5), strength=4.0, sky=(0.55, 0.68, 0.9)):
    world(sky, 0.5); light(sun, (0, 0, 0.1), strength, 0.03, warm, 'SUN')
    prim('plane', mat('ground', ground, 0.9), (0, 0, GROUND), size=12)
    random.seed(7)
    for i in range(46):   # oskarp bakgrund av lovverk
        g = random.choice([(0.10, 0.28, 0.06), (0.22, 0.38, 0.08), (0.05, 0.16, 0.04), (0.5, 0.5, 0.15), (0.16, 0.3, 0.1)])
        prim('sphere', mat('bok', g, 1, emit=random.uniform(0.5, 1.6)), (random.uniform(-3.5, 3.5), random.uniform(2.2, 4.5), random.uniform(-0.1, 2.2)), (random.uniform(0.2, 0.6),) * 3, segments=12, ring_count=6)
def plate(loc=(0, 0, GROUND), nuts=3):
    prim('cyl', mat('fat', (0.85, 0.83, 0.78), 0.4), (loc[0], loc[1], loc[2] + 0.004), (0.07, 0.07, 0.004), vertices=64, radius=1, depth=2)
    for i in range(nuts): nut((loc[0] + 0.022 * math.cos(i * 2.2), loc[1] + 0.022 * math.sin(i * 2.2), loc[2] + 0.016))
NUT = None
def nut(loc, r=0.0085): return prim('sphere', mat('not', (0.42, 0.24, 0.10), 0.45), loc, (r, r, r * 1.15), segments=24, ring_count=12, radius=1)
def blueprint():
    blue = (0.015, 0.06, 0.16); world(blue); m = mat('bp', blue, 1, emit=1.0); override(PARTS, m)
    sc.render.use_freestyle = True; vl = bpy.context.view_layer; vl.use_freestyle = True; fs = vl.freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new('ls'); ls.select_silhouette = ls.select_border = ls.select_crease = True
    fs.crease_angle = math.radians(150)
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('bp')
    ls.linestyle.color = (0.75, 0.88, 1.0); ls.linestyle.thickness = 1.4
    sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 1.3
def printer(z, tip):
    prim('cube', mat('badd', (0.03, 0.03, 0.035), 0.55), (0, 0.07, GROUND - 0.004), (0.16, 0.16, 0.004))
    brass = mat('massing', (0.85, 0.6, 0.25), 0.25, metal=1.0); steel = mat('stal', (0.12, 0.12, 0.13), 0.4, metal=1.0)
    prim('cone', brass, (tip[0], tip[1], tip[2] + 0.004), radius1=0.0006, radius2=0.004, depth=0.008, vertices=48, rot=(math.pi, 0, 0))
    prim('cube', brass, (tip[0], tip[1], tip[2] + 0.011), (0.005, 0.005, 0.003))
    prim('cube', steel, (tip[0], tip[1] + 0.004, tip[2] + 0.026), (0.011, 0.014, 0.012))
    prim('cube', mat('kapa', (0.05, 0.05, 0.055), 0.5), (tip[0], tip[1] + 0.01, tip[2] + 0.075), (0.03, 0.03, 0.037))

BODY, ROOF, BASE, BOWL, INNER = grp('Kropp'), grp('Tak'), grp('Bas'), grp('Skål'), grp('Inredning')
C3 = dict(eye=(0.52, -0.92, 0.36), target=(0, 0.02, 0.105), lens=80)   # en och samma kamera genom hela designsekvensen

def s_oppning_skarm():
    world((0, 0, 0)); screen('vantar'); light((0.5, -0.3, 0.5), (0, 0, 0.11), 1.2, 0.3, (1, 0.6, 0.4))
    camera((0.035, -0.26, 0.112), (0, 0, 0.108), 105, 2.0)
def s_oppning_avslojande():
    world((0, 0, 0)); screen('verifierar'); light((0.9, 0.9, 0.6), (0, 0.05, 0.15), 55, 0.4, (1, 0.75, 0.55)); light((-0.8, -0.6, 0.5), (0, 0, 0.1), 2.5, 0.8, (0.6, 0.7, 1))
    prim('plane', mat('floor', (0.012, 0.012, 0.014), 0.3), (0, 0, GROUND), size=8)
    animal('lennart', (0.17, -0.36, GROUND), 0.2, (-0.2, -1))
    camera((-0.16, -0.78, 0.07), (0.02, 0, 0.12), 70, 2.8, (0, 0, 0.11))
def s_lennart_intro():
    show([]); outdoors(ground=(0.30, 0.19, 0.10)); plate((-0.17, -0.02, GROUND)); animal('lennart', (0.03, 0, GROUND), 0.21, (0.25, -1))
    camera((0.28, -1.0, 0.03), (-0.04, 0, 0.065), 85, 2.8, (0.03, 0, 0.07))
def s_kuppen_spaning():
    show([]); outdoors(ground=(0.30, 0.19, 0.10), sun=(1.5, 1.0, 1.2), warm=(0.8, 0.85, 1.0), strength=2.5, sky=(0.35, 0.42, 0.55)); plate((-0.12, -0.05, GROUND))
    animal('skata', (0.08, 0.0, GROUND - 0.02), 0.3, (0, -1)); camera((-0.02, -0.55, -0.025), (0.03, 0, 0.09), 32, 4.0, (0.05, 0, 0.08))
def s_kuppen_bytet():
    show([]); outdoors(ground=(0.30, 0.19, 0.10), sun=(1.5, 1.0, 1.2), warm=(0.8, 0.85, 1.0), strength=2.5, sky=(0.35, 0.42, 0.55))
    animal('skata', (0, 0, GROUND - 0.02), 0.3, (0.2, -1)); nut((-0.122, -0.012, GROUND + 0.123), 0.008)
    camera((-0.05, -1.3, 0.1), (-0.07, 0, 0.1), 135, 2.8, (-0.1, 0, 0.1))
def s_tomt_fat():
    show([]); outdoors(ground=(0.30, 0.19, 0.10)); plate((0, 0, GROUND), 0)
    for i in range(7): prim('sphere', mat('smula', (0.5, 0.35, 0.2), 0.8), (0.03 * math.cos(i * 1.9) * (1 + i % 3 * 0.4), 0.03 * math.sin(i * 1.9), GROUND + 0.009), (0.0012,) * 3, radius=1)
    camera((0, -0.001, 0.6), (0, 0, GROUND), 85)
def s_skiss():
    show(BODY + BASE); blueprint(); camera(**C3)
def s_lera():
    clay = mat('lera', (0.55, 0.55, 0.56), 0.7); override(PARTS, clay); move(ROOF, (0, 0, 0.09)); move(BOWL, (0, -0.07, 0))
    world((0.004, 0.004, 0.005)); light((-0.7, -0.8, 0.9), (0, 0.05, 0.1), 16, 0.7); light((0.9, 0.7, 0.5), (0, 0.05, 0.12), 8, 0.3, (0.6, 0.75, 1))
    camera(**C3)
def s_farg():
    studio(rim=(0.9, 0.7, 0.5)); screen('vantar'); camera(**C3)
def s_inkop():
    show([]); world((0.004, 0.004, 0.005)); prim('plane', mat('duk', (0.02, 0.02, 0.023), 0.6), (0, 0, 0), size=6); light((-0.5, -0.5, 0.9), (0, 0, 0), 55, 0.6)
    pcb = mat('pcb', (0.04, 0.3, 0.12), 0.4); blk = mat('svart', (0.03, 0.03, 0.035), 0.4); blu = mat('servo', (0.05, 0.15, 0.55), 0.35); stl = mat('skruv', (0.6, 0.6, 0.62), 0.3, metal=1)
    prim('cube', pcb, (-0.2, 0.07, 0.003), (0.0425, 0.028, 0.002)); prim('cube', stl, (-0.225, 0.085, 0.009), (0.008, 0.007, 0.006)); prim('cube', blk, (-0.19, 0.07, 0.006), (0.007, 0.007, 0.001))
    prim('cube', pcb, (-0.09, 0.07, 0.003), (0.0125, 0.012, 0.001)); prim('cyl', blk, (-0.09, 0.07, 0.008), (0.004, 0.004, 0.004), radius=1, depth=2)
    prim('cube', blk, (0.0, 0.07, 0.003), (0.027, 0.02, 0.002)); quad('skarm', 0.049, 0.0362, SCREENS['vantar'], (0, 0.07 - 0.018, 0.0056), (math.pi / 2, 0, 0))
    for x in (0.09, 0.14): prim('cube', blu, (x, 0.07, 0.006), (0.0115, 0.006, 0.006)); prim('cyl', mat('horn', (0.9, 0.9, 0.9), 0.4), (x + 0.005, 0.07, 0.014), (0.003, 0.003, 0.002), radius=1, depth=2)
    for i, c in enumerate([(0.635, 0.227, 0.172), (0.93, 0.92, 0.89), (0.35, 0.37, 0.38)]): prim('torus', mat('spole%d' % i, c, 0.5), (-0.19 + i * 0.105, -0.06, 0.016), major_radius=0.034, minor_radius=0.016)
    for i in range(10): prim('cyl', stl, (0.11 + (i % 5) * 0.014, -0.045 - (i // 5) * 0.02, 0.002), (0.0022, 0.0022, 0.002), radius=1, depth=2)
    nut((0.23, 0.07, 0.009)); camera((0, -0.08, 1.0), (0.01, 0.005, 0), 48)
def s_slicer():
    show(['kropp', 'kropp_vit']); cut(['kropp', 'kropp_vit'], 0.105); override(['kropp', 'kropp_vit'], mat('sl', (0.6, 0.62, 0.66), 0.8))
    world((0.02, 0.024, 0.03)); light((-0.6, -0.7, 0.9), (0, 0.07, 0.05), 50, 0.9)
    prim('plane', mat('grid', (0.05, 0.055, 0.065), 0.8), (0, 0.075, 0), size=0.256)
    prim('plane', mat('lager', (1.0, 0.45, 0.05), 1, emit=3.0, alpha=0.5), (0, 0.075, 0.1052), size=0.2)
    camera((0.5, -0.75, 0.45), (0, 0.07, 0.07), 70)
def s_makro():
    show(['kropp', 'kropp_vit']); cut(['kropp', 'kropp_vit'], 0.105); tip = (0.0842, 0.062, 0.1054); printer(0.105, tip)
    world((0.003, 0.003, 0.004)); light((0.35, -0.25, 0.3), tip, 6, 0.12, (1, 0.9, 0.8)); light((-0.2, 0.3, 0.2), tip, 2, 0.2, (0.5, 0.7, 1))
    camera((0.2, -0.045, 0.125), (0.083, 0.055, 0.106), 105, 4.0, tip)
def s_timelapse():
    show(['kropp', 'kropp_vit']); cut(['kropp', 'kropp_vit'], 0.165); printer(0.165, (-0.03, 0.0005, 0.1654))
    world((0.003, 0.003, 0.004)); light((-0.6, -0.5, 0.6), (0, 0.07, 0.08), 9, 0.4, (1, 0.92, 0.85)); light((0.6, 0.6, 0.3), (0, 0.07, 0.1), 4, 0.2, (0.5, 0.7, 1))
    camera((0.42, -0.62, 0.2), (0, 0.06, 0.07), 60, 5.6)
def s_fardig_del():
    show(['kropp', 'kropp_vit']); prim('cube', mat('badd', (0.03, 0.03, 0.035), 0.55), (0, 0.07, -0.004), (0.16, 0.16, 0.004))
    world((0.003, 0.003, 0.004)); light((0.7, -0.2, 0.25), (0, 0.05, 0.1), 7, 0.25, (1, 0.9, 0.8)); light((-0.5, 0.5, 0.4), (0, 0.07, 0.1), 3, 0.3, (0.5, 0.7, 1))
    camera((0.42, -0.5, 0.05), (0, 0.05, 0.105), 50, 4.0, (0.085, 0, 0.1))
def explode():
    for n, d in {'fotter': -0.17, 'bottenplatta': -0.135, 'framgard_platta': -0.135, 'bas': -0.10, 'framgard': -0.10, 'grasmatta': -0.055, 'framgard_gras': -0.055, 'stenar': -0.03, 'framgard_stenar': -0.03}.items(): move([n], (0, 0, d))
    move(['framgard', 'framgard_gras', 'framgard_stenar', 'framgard_platta'], (0, -0.05, 0))
    move(ROOF, (0, 0, 0.36)); move(['tak_v', 'tak_v_vit'], (-0.05, 0, 0)); move(['tak_h', 'tak_h_vit'], (0.05, 0, 0)); move(['skorsten', 'skorsten_krage'], (0.05, 0, 0.07)); move(['nockkilar'], (0, 0, 0.05)); move(['takpackning'], (0, 0, -0.07))
    move(BOWL, (0, -0.13, 0.02)); move(['lucka', 'lucka_vit'], (0, -0.03, 0.06)); move(['servokapa', 'servopackning'], (0.03, 0, 0.05))
    move(['skarmram'], (0, -0.09, 0)); move(['solskydd', 'solskydd_vit'], (0, -0.06, 0)); move(['kropp_packning'], (0, 0, -0.02))
    move(['doserhus'], (0, 0, 0.22)); move(['doserhjul'], (-0.11, 0, 0.22)); move(['notmagasin'], (0, 0, 0.28)); move(['kamerafaste', 'skarmklamma'], (0, -0.09, 0.0))
    move(['elektroniklada', 'elpackning'], (0, 0.14, 0)); move(['monteringsplatta', 'genomforingar'], (0, 0.22, 0)); move(['ellock'], (0, 0.14, 0.05))
def s_sprangskiss():
    explode(); world((0.004, 0.004, 0.005)); light((-1.2, -1.2, 1.5), (0, 0.05, 0.3), 40, 1.2); light((1.2, 1.0, 0.7), (0, 0.05, 0.3), 14, 0.4, (0.6, 0.75, 1))
    camera((1.55, -1.7, 0.7), (0, 0.03, 0.235), 70)
def s_bas():
    show(BASE + BODY); move(BODY, (0, 0, 0.075)); move(['grasmatta', 'framgard_gras', 'stenar', 'framgard_stenar'], (0, 0, 0.025)); studio(rim=(0.9, 0.7, 0.4), floor=False)
    camera((0.55, -0.75, 0.0), (0, 0, 0.07), 60, 5.6)
def s_rontgen():
    ghost = mat('glas', (0.75, 0.3, 0.25), 0.3, alpha=0.13); override(BODY + ROOF, ghost); screen('vantar')
    world((0.004, 0.004, 0.005)); light((-0.7, -0.8, 0.9), (0, 0.05, 0.1), 18, 0.7); light((0.9, 0.7, 0.5), (0, 0.05, 0.12), 9, 0.3, (0.6, 0.75, 1))
    prim('plane', mat('floor', (0.012, 0.012, 0.014), 0.35), (0, 0, GROUND), size=8); nut((0, 0.06, 0.135)); nut((0.012, 0.07, 0.152)); nut((-0.01, 0.055, 0.168))
    camera((0.95, -0.62, 0.22), (0, 0.03, 0.105), 75)
def s_tak():
    move(['tak_v', 'tak_v_vit'], (-0.035, 0, 0.07)); move(['tak_h', 'tak_h_vit'], (0.035, 0, 0.07)); move(['takrannor', 'nockkilar'], (0, 0, 0.07)); move(['skorsten', 'skorsten_krage'], (0, 0, 0.15))
    studio(rim=(0.9, 0.7, 0.5)); screen('vantar'); camera((0.42, -0.85, 0.5), (0, 0.04, 0.2), 70)
def s_hjalte():
    studio(key=(-0.8, -0.6, 0.8), power=18, rim=(0.9, 0.8, 0.5)); screen('vantar'); camera((0.44, -0.9, 0.16), (0, 0, 0.105), 75, 5.6)
def s_skatan_kommer():
    outdoors(); screen('verifierar'); animal('skata', (0.19, -0.2, GROUND - 0.02), 0.3, (-0.3, -1)); camera((-0.38, -1.0, 0.07), (0.05, -0.05, 0.1), 70, 4.0, (0, 0, 0.11))
def s_denied():
    outdoors(); screen('denied'); animal('skata', (0.115, -0.24, GROUND - 0.03), 0.3, (-0.1, -1)); camera((-0.07, -0.6, 0.085), (0.02, 0, 0.1), 85, 4.0, (0, 0, 0.108))
def s_lennart_kommer():
    outdoors(); screen('verifierar'); animal('lennart', (0.2, -0.2, GROUND), 0.21, (-0.3, -1)); camera((-0.38, -1.0, 0.07), (0.05, -0.05, 0.1), 70, 4.0, (0, 0, 0.11))
def open_hatch():
    for n in ('lucka', 'lucka_vit'): PARTS[n].matrix_world = PARTS[n].matrix_world @ Matrix.Rotation(math.radians(-95), 4, 'X')
def s_granted():
    outdoors(); screen('granted'); open_hatch(); nut((0.0, -0.024, 0.016)); animal('lennart', (0.15, -0.07, GROUND), 0.21, (-0.3, -1))
    camera((-0.26, -0.72, 0.2), (0.045, -0.01, 0.075), 60, 4.0, (0, -0.02, 0.06))
def s_final():
    outdoors(sun=(-1.2, 2.2, 0.55), warm=(1.0, 0.62, 0.3), strength=5.5, sky=(0.75, 0.6, 0.5)); light((-0.5, -0.9, 0.4), (0, 0, 0.1), 3, 0.8, (1, 0.85, 0.7))
    screen('granted'); open_hatch(); animal('lennart', (0.16, -0.1, GROUND), 0.21, (-0.35, -1)); nut((0.085, -0.115, 0.068), 0.008)
    camera((-0.5, -0.95, 0.03), (0.04, -0.03, 0.105), 55, 2.8, (0, 0, 0.11))

def s_oppning_glugg():   # "artspecifik atkomstkontroll": den runda gluggen i gaveln
    world((0, 0, 0)); light((0.45, -0.25, 0.45), (0, 0, 0.17), 2.2, 0.25, (1, 0.7, 0.5)); light((-0.4, -0.3, 0.1), (0, 0, 0.19), 0.5, 0.4, (0.5, 0.65, 1))
    camera((0.05, -0.24, 0.172), (0, -0.005, 0.166), 105, 2.8)
def s_oppning_hjul():   # "motoriserad precisionsdosering": doseringshjulet genom genomskinliga vaggar
    show(INNER); override(['doserhus', 'notmagasin'], mat('glas2', (0.85, 0.77, 0.6), 0.3, alpha=0.16)); world((0, 0, 0))
    PARTS['doserhjul'].matrix_world = PARTS['doserhjul'].matrix_world @ Matrix.Rotation(math.radians(50), 4, 'X')
    light((0.5, -0.3, 0.4), (0, 0.057, 0.065), 5, 0.25, (1, 0.75, 0.55)); light((-0.4, 0.3, 0.2), (0, 0.057, 0.065), 1.5, 0.3, (0.5, 0.65, 1)); nut((0, 0.06, 0.103))
    camera((0.36, -0.2, 0.12), (0, 0.057, 0.075), 85, 4.0)
def s_oppning_delar():   # "fyrtioatta komponenter": en glimt av sprangskissen nerifran
    explode(); world((0, 0, 0)); light((0.9, 0.6, 0.9), (0, 0.05, 0.3), 45, 0.5, (1, 0.75, 0.55)); light((-0.8, -0.8, 0.2), (0, 0.05, 0.3), 6, 0.8, (0.5, 0.65, 1))
    camera((0.78, -0.9, -0.14), (0, 0.04, 0.25), 35, 4.0, (0, 0, 0.12))
# ---------- planen: skiss pa ritningsblatt med pappfigurer, moln och signal ----------
DECAL_E = {'lennart': img_mat('de_lennart', os.path.join(ROOT, 'dekal-lennart.png'), emit=1.0), 'skata': img_mat('de_skata', os.path.join(ROOT, 'dekal-skata.png'), emit=1.0)}
def plan_base(house=True):
    blueprint(); ls = bpy.context.view_layer.freestyle_settings.linesets[0]; col = bpy.data.collections.get('utan_linjer')
    if col is None:
        col = bpy.data.collections.new('utan_linjer'); sc.collection.children.link(col)
        for n in ('grasmatta', 'framgard_gras', 'blomlador_vaxter', 'blomlador_blommor_rod', 'blomlador_blommor_vit'): col.objects.link(PARTS[n])
    ls.select_by_collection = True; ls.collection = col; ls.collection_negation = 'EXCLUSIVE'
    if not house: show([])
    return col, PARTS['kropp'].data.materials[0]
def fig(kind, loc, h, col): o = quad(kind, h, h, DECAL_E[kind], loc); col.objects.link(o); return o
def txt(text, loc, size, col, color=(0.85, 0.93, 1.0)):
    c = bpy.data.curves.new('t', 'FONT'); c.body = text; c.size = size; c.align_x = 'CENTER'; o = add(bpy.data.objects.new('t', c)); o.location = loc; o.rotation_euler = (math.pi / 2, 0, 0); c.materials.append(mat('txt', color, 1, emit=1.4)); col.objects.link(o)
def cloud(loc, bp):
    for dx, dz, r in [(-0.07, 0, 0.045), (0, 0.02, 0.062), (0.075, 0.0, 0.048), (0.03, -0.012, 0.05), (-0.03, -0.012, 0.05)]: prim('sphere', bp, (loc[0] + dx, loc[1], loc[2] + dz), (r, r * 0.3, r), segments=48, ring_count=24, radius=1)
def signal(p, q, col, n=22, color=(0.85, 0.93, 1.0)):
    p, q = Vector(p), Vector(q); m = mat('sig', color, 1, emit=1.6)
    for i in range(n):
        k = (i + 0.5) / n; v = p.lerp(q, k); v.z += 0.05 * math.sin(math.pi * k); o = prim('cube', m, v, (0.0045, 0.002, 0.002), (0, -math.atan2(q.z - p.z, q.x - p.x), 0)); col.objects.link(o)
PLANCAM = dict(eye=(0.22, -1.8, 0.24), target=(0.22, 0, 0.24), lens=55)
def s_plan_problem():
    col, bp = plan_base(False); prim('cyl', bp, (0, 0, GROUND + 0.004), (0.07, 0.07, 0.004), vertices=64, radius=1, depth=2)
    for i in range(3): prim('sphere', bp, (0.022 * math.cos(i * 2.2), 0.022 * math.sin(i * 2.2), GROUND + 0.016), (0.0085,) * 3, radius=1)
    fig('skata', (0.15, 0.0, GROUND - 0.02), 0.3, col); fig('lennart', (0.5, 0.0, GROUND), 0.21, col); camera((0.22, -1.6, 0.1), (0.22, 0, 0.09), 70)
def s_plan_fraga():
    col, bp = plan_base(); screen('verifierar'); fig('skata', (0.36, -0.2, GROUND - 0.02), 0.3, col); cloud((0.5, 0.05, 0.41), bp); signal((0.0, -0.03, 0.168), (0.42, 0.0, 0.39), col); txt('EKORRE?', (0.5, -0.02, 0.475), 0.03, col); camera(**PLANCAM)
def s_plan_nej():
    col, bp = plan_base(); screen('denied'); fig('skata', (0.36, -0.2, GROUND - 0.02), 0.3, col); cloud((0.5, 0.05, 0.41), bp); signal((0.42, 0.0, 0.39), (0.0, -0.03, 0.168), col, color=(1.0, 0.42, 0.37)); txt('NEJ', (0.5, -0.02, 0.475), 0.034, col, (1.0, 0.42, 0.37)); camera(**PLANCAM)
def s_plan_ja():
    col, bp = plan_base(); screen('granted'); open_hatch(); prim('sphere', bp, (0.0, -0.024, 0.016), (0.0085,) * 3, radius=1); fig('lennart', (0.3, -0.16, GROUND), 0.21, col); cloud((0.5, 0.05, 0.41), bp)
    signal((0.42, 0.0, 0.39), (0.0, -0.03, 0.168), col, color=(0.37, 0.88, 0.56)); txt('JA', (0.5, -0.02, 0.475), 0.034, col, (0.37, 0.88, 0.56)); camera(**PLANCAM)
SHOTS = [('p1', s_plan_problem), ('p3', s_plan_fraga), ('p4', s_plan_nej), ('p5', s_plan_ja), ('26', s_oppning_glugg), ('27', s_oppning_hjul), ('28', s_oppning_delar), ('01', s_oppning_skarm), ('02', s_oppning_avslojande), ('04', s_lennart_intro), ('05', s_kuppen_spaning), ('06', s_kuppen_bytet), ('07', s_tomt_fat),
         ('08', s_skiss), ('09', s_lera), ('10', s_farg), ('11', s_inkop), ('12', s_slicer), ('13', s_makro), ('14', s_timelapse), ('15', s_fardig_del),
         ('16', s_sprangskiss), ('17', s_bas), ('18', s_rontgen), ('19', s_tak), ('20', s_hjalte), ('21', s_skatan_kommer), ('22', s_denied),
         ('23', s_lennart_kommer), ('24', s_granted), ('25', s_final)]
for name, fn in SHOTS:
    if ONLY and name not in ONLY: continue
    try:
        reset(); fn(); bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(OUT, name + '.jpg'); bpy.ops.render.render(write_still=True); print('RUTA', name, flush=True)
    except Exception: print('FEL', name); traceback.print_exc()
