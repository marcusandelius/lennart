# En hasselnot som faller, renderad med genomskinlig bakgrund, for att laggas pa slutet av 1.4 (verktyg/fall_14.py). Samma not som i 3D-scenerna.
# Ljuset ar mjukt dagsljus snett ovanifran vanster, som i mobilklippet.
# Kor:  blender -b -P verktyg/not_sprite.py -- <ut-mapp> <antal rutor>
import bpy, os, sys, math
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE)
a = sys.argv[sys.argv.index('--') + 1:]; OUT, N = os.path.abspath(a[0]), int(a[1]); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.use_denoising = True; sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = 160; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
try: sc.view_settings.view_transform = 'AgX'
except Exception: pass
def link(o): sc.collection.objects.link(o); return o
src = open(os.path.join(FILM, 'akt_inkop.py'), encoding='utf-8').read()
src = src[src.index('# hasselnotter: en liten hog'):src.index('NUTP = [')]           # notens form och material, ur inkopen
exec(compile(src, 'akt_inkop.py', 'exec'), globals())
n0.scale = (1, 1, 1)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.55, 0.62, 0.66, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.5
d = bpy.data.lights.new('sol', 'AREA'); d.energy = 900; d.size = 4; d.color = (1.0, 0.93, 0.84); l = link(bpy.data.objects.new('sol', d)); l.location = (-4, -3, 5); l.rotation_euler = (Vector((0, 0, 0)) - l.location).to_track_quat('-Z', 'Y').to_euler()
cd = bpy.data.cameras.new('cam'); cd.type = 'ORTHO'; cd.ortho_scale = 2.6; cam = link(bpy.data.objects.new('cam', cd)); sc.camera = cam; cam.location = (0, -8, 0); cam.rotation_euler = (math.pi / 2, 0, 0)
for f in range(N):   # noten tumlar: ett halvt varv over hela fallet
    s_ = f / max(1, N - 1); n0.rotation_euler = (-1.3 + 1.3 * s_, 0.0, 0.5 * (1 - s_))   # slutar upprattt med spetsen uppat, som noten borjar i 2.1
    sc.render.filepath = os.path.join(OUT, '%02d.png' % f); bpy.ops.render.render(write_still=True)
print('SPRITE', N, flush=True)
