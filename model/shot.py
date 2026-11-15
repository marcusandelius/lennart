from playwright.sync_api import sync_playwright
from PIL import Image
import sys, time
btn=sys.argv[1] if len(sys.argv)>1 else "#visit"
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(viewport={"width":1440,"height":950}); pg.on("pageerror", lambda e: print("ERR", e))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort()); pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.abort())
    pg.goto("file:///home/claude/fix/local.html"); pg.wait_for_timeout(4000)
    bb=pg.query_selector("#stage").bounding_box(); clip={"x":bb["x"],"y":bb["y"],"width":bb["width"],"height":bb["height"]}
    pg.click(btn); seen=[]; ims=[]; t0=time.time()
    want=["Kameran tittar","Lennart äter ur skålen","Lennart tar med sig nöten"]
    while time.time()-t0<60 and len(ims)<len(want):
        t=pg.inner_text("#capT")
        if t==want[len(ims)]:
            pg.wait_for_timeout(1500 if len(ims)==1 else 700); pg.screenshot(path=f"s{len(ims)}.png",clip=clip); ims.append(Image.open(f"s{len(ims)}.png"))
        pg.wait_for_timeout(100)
    for _ in range(80):
        if not pg.evaluate("busy"): break
        pg.wait_for_timeout(500)
    print(pg.inner_text("#status"), len(ims))
    b.close()
w,h=ims[0].size; W=Image.new("RGB",(w*len(ims),h))
for i,im in enumerate(ims): W.paste(im,(i*w,0))
W.resize((1560,int(1560*h/(w*len(ims))))).save("stk.png")
