# Projekt Lennart - del 5: utskriftsvaggen. Atta riktiga timelapse-klipp fran 3D-skrivaren i en bento-layout med olika storlekar.
# Bilden borjar pa en utskrift i helbild, kameran backar och vrids sa att vaggen syns snett med djup, rutorna dyker fram
# utat fran den forsta. Vaggen planas sedan ut till en exakt layout. Under varje ruta fylls en tunn forloppslinje, och alla
# blir klara i samma ogonblick (rakt klipp till sprangskissen, 6.1).
# Kor:  blender -b -P akt_utskrift.py -- <ut-mapp (absolut)> <bredd> [tider i sekunder ...]
# Klippen ligger i film/timelapse/rutor/<1-8>/%04d.jpg (uppdelade med ffmpeg, 1280 px). Varje ruta spelar sitt klipp fran borjan
# nar den dyker fram och sista bilden landar nar alla blir klara (DONE), sa korta klipp gar langsammare och langa fortare.
import bpy, sys, os, math, random
from mathutils import Vector, Euler, Matrix
HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[sys.argv.index('--') + 1:]; OUT, WIDTH, TIMES = os.path.abspath(a[0]), int(a[1]), [float(x) for x in a[2:]]
os.makedirs(OUT, exist_ok=True); FPS, END, DONE = 25, 10.0, 9.1   # 5.2 = 0-4 s, 5.3 = 4-10 s. Alla blir klara pa slutet av repliken i 5.3
RUTOR = os.path.join(HERE, 'timelapse', 'rutor')
NF = {k: len([f for f in os.listdir(os.path.join(RUTOR, str(k))) if f.endswith('.jpg')]) for k in range(1, 9)}

bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
    try: sc.render.engine = eng; break
    except Exception: pass
sc.render.resolution_x = WIDTH; sc.render.resolution_y = WIDTH * 9 // 16; sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 95
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception as e: print('look', e)
try: sc.eevee.taa_render_samples = 32
except Exception: pass

# bakgrund: morkt petroleumbla, samma som resten av filmen
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; bg = sc.world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.004, 0.014, 0.018, 1)
def link(o): sc.collection.objects.link(o); return o

# ---------- layouten: 6 x 4 celler pa en yta som ar 16 x 9, tolv rutor i olika storlekar ----------
CW, CH, G = 16 / 6, 9 / 4, 0.07
LAYOUT = [  # (kolumn, rad, bredd, hojd)
    (0, 0, 3, 2),   # A huvudrutan, 16:9 - bilden borjar har
    (3, 0, 2, 1), (5, 0, 1, 2), (3, 1, 2, 1),
    (0, 2, 2, 2), (2, 2, 2, 1), (2, 3, 2, 1), (4, 2, 2, 2)]
# klipp och beskarning: (klipp 1-8, zoom, mitt u, mitt v) - zoom < 1 skar bort fisheye-kanterna. Klippen ar numrerade i datumordning (se film/timelapse)
CROP = [(3, 0.86, 0.55, 0.50),   # A stugans roda kropp
        (6, 0.85, 0.52, 0.50), (7, 1.0, 0.55, 0.5), (4, 0.75, 0.55, 0.66),
        (1, 0.80, 0.58, 0.58), (5, 0.85, 0.52, 0.50), (2, 0.58, 0.47, 0.68), (8, 0.78, 0.52, 0.47)]

def rrect(w, h, r, name):
    pts = []
    for cx, cy, a0 in [(w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180)]:
        pts += [(cx + r * math.cos(math.radians(a0 + 90 * i / 8)), cy + r * math.sin(math.radians(a0 + 90 * i / 8))) for i in range(9)]
    me = bpy.data.meshes.new(name); me.from_pydata([(x, y, 0) for x, y in pts], [], [list(range(len(pts)))]); uv = me.uv_layers.new()
    for l in me.loops: x, y = pts[l.vertex_index]; uv.data[l.index].uv = (x / w + 0.5, y / h + 0.5)
    return me

def frame_img(k, n): return bpy.data.images.load(os.path.join(RUTOR, str(k), '%04d.jpg' % min(max(n, 0), NF[k] - 1)), check_existing=True)
TILES = []; rng = random.Random(4)
for i, ((c, r, w, h), (k, z, cu, cv)) in enumerate(zip(LAYOUT, CROP)):
    tw, th = w * CW - 2 * G, h * CH - 2 * G; cx, cy = -8 + (c + w / 2) * CW, 4.5 - (r + h / 2) * CH
    m = bpy.data.materials.new('ruta%d' % i); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = frame_img(k, 0); tx.extension = 'EXTEND'
    uvn = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    ai, at = 16 / 9, tw / th; fw, fh = (1.0, ai / at) if at >= ai else (at / ai, 1.0)
    sw, sh = fw * z, fh * z; ou = min(max(cu - sw / 2, 0), 1 - sw); ov = min(max(cv - sh / 2, 0), 1 - sh)
    mp.inputs['Location'].default_value = (ou, ov, 0); mp.inputs['Scale'].default_value = (sw, sh, 1)
    nt.links.new(uvn.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs[0], tx.inputs['Vector']); nt.links.new(tx.outputs['Color'], em.inputs['Color']); nt.links.new(em.outputs[0], o_.inputs['Surface'])
    ob = link(bpy.data.objects.new('ruta%d' % i, rrect(tw, th, 0.09, 'ruta%d' % i))); ob.data.materials.append(m)
    # forloppslinjen langst ner i rutan
    pm = bpy.data.materials.new('linje%d' % i); pm.use_nodes = True; pe = pm.node_tree.nodes.new('ShaderNodeEmission'); pe.inputs['Color'].default_value = (1.0, 0.42, 0.2, 1)
    pm.node_tree.nodes.remove(pm.node_tree.nodes['Principled BSDF']); pm.node_tree.links.new(pe.outputs[0], pm.node_tree.nodes['Material Output'].inputs['Surface'])
    pme = bpy.data.meshes.new('l'); pme.from_pydata([(0, 0, 0), (1, 0, 0), (1, 0.045, 0), (0, 0.045, 0)], [], [(0, 1, 2, 3)]); pme.materials.append(pm)
    bar = link(bpy.data.objects.new('linje%d' % i, pme)); bar.parent = ob; bar.location = (-tw / 2 + 0.16, -th / 2 + 0.14, 0.002)
    d = (Vector((cx, cy)) - Vector((-4, 2.25))).length
    TILES.append(dict(ob=ob, bar=bar, w=tw - 0.32, home=Vector((cx, cy, 0)), em=em, pe=pe, mp=mp, tx=tx, k=k, s0=(sw, sh), o0=(ou, ov), dist=d, dz=rng.uniform(-0.9, 0.9) if i else 0.0, push=rng.uniform(0.02, 0.06)))
order = sorted(range(len(TILES)), key=lambda j: TILES[j]['dist'])
for n, j in enumerate(order): TILES[j]['t0'] = 0.0 if j == 0 else 1.9 + 0.11 * n     # rutorna dyker fram utat fran huvudrutan

cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 50; CAM = link(bpy.data.objects.new('cam', cam_d)); sc.camera = CAM; cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 2.2
def sm(t, a, b): x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)
def ease_out(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
TF = math.tan(math.atan(18 / 50))       # halva bildvinkeln

def state(t):
    flat = sm(t, 5.2, 8.4); door = sm(t, 9.3, 10.25) ** 1.6   # door: rutorna glider isar som dorrar och kameran aker in genom oppningen (overgang till sprangskissen)
    for T in TILES:
        u = 1.0 if T['t0'] == 0 else ease_out((t - T['t0']) / 0.75); vis = t >= T['t0']   # huvudrutan syns fullt fran start
        T['ob'].hide_render = not vis; T['bar'].hide_render = not vis
        sx_ = 1 if T['home'].x > 0 else -1; T['ob'].location = T['home'] + Vector((sx_ * door * (9 + 0.5 * abs(T['home'].x)), 0, -7 * (1 - u) + T['dz'] * (1 - flat) + 4 * door)); T['ob'].rotation_euler = (0, -sx_ * 0.9 * door, 0)
        s = 0.86 + 0.14 * u; T['ob'].scale = (s, s, 1); T['em'].inputs['Strength'].default_value = 1.0 * u
        p = min(1, max(0, (t - T['t0']) / (DONE - T['t0']))) if vis else 0; T['bar'].scale = (max(p * T['w'], 0.001), 1, 1)
        T['tx'].image = frame_img(T['k'], round(p * (NF[T['k']] - 1)))   # klippet gar fran forsta till sista bilden medan linjen fylls
        T['pe'].inputs['Strength'].default_value = 3.0 + 14.0 * (sm(t, DONE, DONE + 0.08) * (1 - sm(t, DONE + 0.15, DONE + 0.6)))   # alla linjer blixtrar till nar de blir klara samtidigt
        k = T['push'] * min(t, DONE) / DONE; sw, sh = T['s0']; T['mp'].inputs['Scale'].default_value = (sw * (1 - k), sh * (1 - k), 1)       # langsam inzoomning i varje ruta
        T['mp'].inputs['Location'].default_value = (T['o0'][0] + sw * k / 2, T['o0'][1] + sh * k / 2, 0)
    # kameran: helbild pa huvudrutan -> backar och vrids till en sned vy av vaggen -> glider tillbaka rakt fram nar vaggen planas ut
    back = sm(t, 1.7, 5.0); home = sm(t, 5.0, 8.6)
    tgt = Vector((-4, 2.25, 0)).lerp(Vector((0, 0, 0)), back)
    dist = (4.0 / TF) * (1 - back) + 25.5 * back - 1.2 * home + 0.35 * (1 - back) * (1 - t / 1.7 if t < 1.7 else 0) - 19 * door
    yaw = math.radians(-22 * back + 22 * home); pitch = math.radians(9 * back - 9 * home)
    off = Vector((math.sin(yaw) * math.cos(pitch), -math.sin(pitch), math.cos(yaw) * math.cos(pitch))) * dist
    CAM.location = tgt + off; fw_ = (tgt - CAM.location).normalized(); rt = fw_.cross(Vector((0, 1, 0))).normalized(); up = rt.cross(fw_)   # vaggen ar uppratt i XY-planet: Y ar upp
    CAM.matrix_world = Matrix((rt, up, -fw_)).transposed().to_4x4(); CAM.matrix_world.translation = tgt + off; cam_d.dof.focus_distance = dist
    cam_d.dof.aperture_fstop = 2.2 + 30 * home

frames = sorted({round(t * FPS) for t in TIMES}) if TIMES else range(int(END * FPS))
for f in frames:
    p = os.path.join(OUT, f'{f:04d}.jpg')
    if os.path.exists(p) and os.path.getsize(p) > 0: continue
    state(f / FPS); bpy.context.view_layer.update(); sc.render.filepath = p; bpy.ops.render.render(write_still=True); print('RUTA', f, flush=True)
    for im in list(bpy.data.images):
        if im.users == 0: bpy.data.images.remove(im)
