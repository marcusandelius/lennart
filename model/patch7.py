from lib import *
from manifold3d import FillRule
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
parts,P=load('parts_v6.json')
def text_cs(txt,size):
    tp=TextPath((0,0),txt,size=size,prop=FontProperties(family="DejaVu Sans",weight="bold"))
    polys=[p for p in tp.to_polygons() if len(p)>=3]; allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return CrossSection([[(float(x-c[0]),float(y-c[1])) for x,y in p] for p in polys], FillRule.EvenOdd), (allp.max(0)-allp.min(0))
cs,ext=text_cs("LENNART",11.5)
print("textens mått:", ext.round(1))
letters=cs.extrude(0.8).rotate([90,0,0]).translate([0,-46.0,12.0])       # 0,8 mm upphöjda vita bokstäver på skålens framsida
sv=M(P,'skal_vit')+letters
print("krock med röda skålen:", round((letters^M(P,'skal')).volume(),2), " med luckan:", round((letters^(M(P,'lucka')+M(P,'lucka_vit'))).volume(),2), "bbox", bb(letters).tolist())
put(parts,P,'skal_vit',sv)
json.dump(parts,open('parts_v7.json','w'))
