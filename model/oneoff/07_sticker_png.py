# Körd 2026-11-14 i /home/claude/fix: spara dekalerna och skärmens lägen som PNG ur förhandsgranskningen (local.html = sidan med lokal three.js).
from playwright.sync_api import sync_playwright
import base64
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); pg.route("**/fonts.googleapis.com/**", lambda r: r.abort()); pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.abort())
    pg.goto("file:///home/claude/fix/local.html"); pg.wait_for_timeout(3500)
    for fn,name in (("squirrelArt","dekal-lennart.png"),("magpieArt","dekal-skata.png")):
        d=pg.evaluate(f"{fn}()[0].image.toDataURL('image/png')")
        open('/home/claude/fix/'+name,'wb').write(base64.b64decode(d.split(',')[1]))
    for mode,name in (("idle","skarm-vantar.png"),("ok","skarm-access-granted.png"),("no","skarm-access-denied.png"),("scan","skarm-verifierar.png")):
        d=pg.evaluate(f"(()=>{{ screen('{mode}'); const m=screenMesh.material.map; return (m.image||m.source.data).toDataURL('image/png'); }})()")
        open('/home/claude/fix/'+name,'wb').write(base64.b64decode(d.split(',')[1]))
    b.close()
print("ok")
