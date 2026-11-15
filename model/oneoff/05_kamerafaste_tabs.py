# Körd 2026-11-15 i /home/claude/fix: förläng kamerafästets två klackar ner till byggplattan (de började 0,47 mm upp).
import trimesh, numpy as np
from manifold3d import Manifold, Mesh
m=trimesh.load('stl/15_kamerafaste.stl'); lo,hi=m.bounds; print("bounds", np.round(lo,2), np.round(hi,2))
M_=Manifold(Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32)))
add=Manifold()
for sx in (1,-1):
    tab=M_^Manifold.cube([30,60,60]).translate([17 if sx>0 else -47,-30,lo[2]-1])
    tb=tab.bounding_box(); print("flik", sx, "nederkant z=%.2f"%tb[2], "x %.1f..%.1f y %.1f..%.1f"%(tb[0],tb[3],tb[1],tb[4]))
    sl=tab^Manifold.cube([200,200,0.3]).translate([-100,-100,tb[2]])
    sb=sl.bounding_box()
    add=add+Manifold.cube([sb[3]-sb[0], sb[4]-sb[1], tb[2]-lo[2]+0.3]).translate([sb[0],sb[1],lo[2]])
new=M_+add
me=new.to_mesh(); t=trimesh.Trimesh(np.array(me.vert_properties)[:,:3], np.array(me.tri_verts), process=False)
t.export('stl/15_kamerafaste.stl'); c=trimesh.load('stl/15_kamerafaste.stl'); print("tät:", c.is_watertight, np.round(c.extents,1))
