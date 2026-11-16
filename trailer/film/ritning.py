# Projekt Lennart - ritningen: tre vyer av huset (framsida, ovanifran, sida) som svarta linjer pa vitt.
# Kor:  blender -b -P ritning.py -- <ut-mapp (absolut)>      Bilderna satts ihop till ett ritningsark med ffmpeg (se akt_design.py).
import bpy, sys, os, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[sys.argv.index('--') + 1]); os.makedirs(OUT, exist_ok=True); PX, SCALE = 1000, 0.40
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 1; sc.cycles.use_denoising = False
sc.render.resolution_x = sc.render.resolution_y = PX; sc.render.image_settings.file_format = 'PNG'; sc.view_settings.view_transform = 'Standard'
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; sc.world.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, 'lennarts-matstation.glb'))
PARTS = {o.name: o for o in bpy.data.objects if o.type == 'MESH'}
white = bpy.data.materials.new('vit'); white.use_nodes = True; nt = white.node_tree; e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (1, 1, 1, 1)
nt.links.new(e.outputs[0], [x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL'][0].inputs['Surface'])
pts = []
for o in PARTS.values():
    for i in range(len(o.data.materials)): o.data.materials[i] = white
    pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))); hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts))); c = (lo + hi) / 2
print('GRANSER', tuple(round(v, 4) for v in lo), tuple(round(v, 4) for v in hi), flush=True)
sc.render.use_freestyle = True; vl = bpy.context.view_layer; vl.use_freestyle = True; fs = vl.freestyle_settings; fs.crease_angle = math.radians(150)
ls = fs.linesets[0] if fs.linesets else fs.linesets.new('ls'); ls.select_silhouette = ls.select_border = ls.select_crease = True
if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('bp')
ls.linestyle.color = (0, 0, 0); sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 1.8
nol = bpy.data.collections.new('utan_linjer'); sc.collection.children.link(nol)
for n in ('grasmatta', 'framgard_gras', 'bas', 'framgard', 'blomlador_vaxter', 'blomlador_blommor_rod', 'blomlador_blommor_vit'):
    if n in PARTS: nol.objects.link(PARTS[n])
ls.select_by_collection = True; ls.collection = nol; ls.collection_negation = 'EXCLUSIVE'
cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cd.ortho_scale = SCALE; cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
for name, loc, rot in [('fram', (0, lo.y - 1, c.z), (math.pi / 2, 0, 0)), ('ovan', (0, c.y, hi.z + 1), (0, 0, 0)), ('sida', (hi.x + 1, c.y, c.z), (math.pi / 2, 0, math.pi / 2))]:
    cam.location = loc; cam.rotation_euler = rot; sc.render.filepath = os.path.join(OUT, name + '.png'); bpy.ops.render.render(write_still=True)
