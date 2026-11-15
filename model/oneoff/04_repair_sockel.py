# Körd 2026-11-15 i /home/claude/fix: laga den grå stengrundens STL efter export (gör den tät igen).
import trimesh
m=trimesh.load('stl/05_kropp_sockel_gra.stl', process=True)
m.merge_vertices(digits_vertex=3); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices(); trimesh.repair.fill_holes(m); trimesh.repair.fix_normals(m)
m=trimesh.util.concatenate([c for c in m.split(only_watertight=False) if abs(c.volume)>1]); m.export('stl/05_kropp_sockel_gra.stl')
print("sockel tät:", trimesh.load('stl/05_kropp_sockel_gra.stl').is_watertight, round(m.volume))
