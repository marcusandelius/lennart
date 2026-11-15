from playwright.sync_api import sync_playwright
from PIL import Image
CLIP="""(P=>{ const cv=P.sticker.children[1].material.map.image, d=cv.getContext('2d').getImageData(0,0,512,512).data, mf=P.sticker.children[0]; P.root.updateMatrixWorld(true);
  let tray=0, lid=0, wall=0, n=0; for(let v=0;v<512;v+=6) for(let u=0;u<512;u+=6){ if(d[(v*512+u)*4+3]<128) continue; n++;
    const x=(u/512-.5)*118, y=(.5-v/512)*118; const w=actors.worldToLocal(mf.localToWorld(new THREE.Vector3(x,y,-x*x*0.0016)));
    const inOuter=Math.abs(w.x)<=40&&w.y>=-46&&w.y<=0&&w.z>=0&&w.z<=28, inCav=Math.abs(w.x)<37.2&&w.y>-43.2&&w.y<-2.8&&w.z>3.2;
    if(inOuter&&!inCav) tray++; if(Math.abs(w.x)<=41.5&&w.y>=-15&&w.y<=-3&&w.z>=29&&w.z<=74) lid++; if(w.y>0) wall++; }
  return {n,tray,lid,wall}; })"""
HANDCLIP="""(P=>{ const cv=P.sticker.children[1].material.map.image, d=cv.getContext('2d').getImageData(0,0,512,512).data, mf=P.sticker.children[0]; P.root.updateMatrixWorld(true);
  const inside=(x,y)=>{ const u=Math.round((x/118+.5)*512), v=Math.round((.5-y/118)*512); return u>=0&&u<512&&v>=0&&v<512&&d[(v*512+u)*4+3]>128; };
  const out={}; let idx=0; const A=new THREE.Vector3(), B=new THREE.Vector3(), C=new THREE.Vector3();
  const sd=q=>q.z+q.x*q.x*0.0016;
  [P.hand,P.arm].forEach(grp=>grp.traverse(o=>{ if(!o.isMesh) return; idx++; const g=o.geometry, pos=g.attributes.position, ix=g.index; let n=0;
    const L=k=>mf.worldToLocal(o.localToWorld(new THREE.Vector3().fromBufferAttribute(pos,k)));
    const loc=[]; for(let k=0;k<pos.count;k++) loc.push(L(k));
    for(let t=0;t<ix.count;t+=3){ const tri=[loc[ix.getX(t)],loc[ix.getX(t+1)],loc[ix.getX(t+2)]];
      for(let e=0;e<3;e++){ const a=tri[e], b=tri[(e+1)%3], sa=sd(a), sb=sd(b); if(sa*sb<0){ const f=sa/(sa-sb); if(inside(a.x+(b.x-a.x)*f, a.y+(b.y-a.y)*f)) n++; } } }
    if(n) out[idx+':'+g.type.replace('Geometry','')]=n; }));
  return out; })"""
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(viewport={"width":1440,"height":950}); pg.on("pageerror", lambda e: print("ERR", e))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort()); pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.abort())
    pg.goto("file:///home/claude/fix/local.html"); pg.wait_for_timeout(4000)
    bb=pg.query_selector("#stage").bounding_box(); clip={"x":bb["x"],"y":bb["y"],"width":bb["width"],"height":bb["height"]}
    V1="TARGET.set(0,62,58); Object.assign(view,{th:-0.62,ph:1.2,r:700}); draw();"
    BOW="(()=>{lids.forEach(h=>h.rotation.x=-1.66); LP.pose.rotation.y=0; const bw=bowTo(LP,MOUTH,[SPOT[0]+4,SPOT[1]-4,SPOT[2]+15],10); lennart.position.set(...bw.stand); LP.pose.rotation.y=bw.al; ground(LP); draw(); return bw.al;})()"
    pg.evaluate(V1+"lennart.visible=true; lennart.position.set(30,-104,0); faceCam(lennart); ground(LP); draw()"); print("handen genom ekorren, stående:", pg.evaluate(HANDCLIP+"(LP)")); pg.wait_for_timeout(400); pg.screenshot(path="a0.png",clip=clip)
    pg.evaluate("TARGET.set(40,75,95); Object.assign(view,{th:-0.45,ph:1.2,r:300}); draw(); faceCam(lennart); ground(LP); draw()"); pg.wait_for_timeout(400); pg.screenshot(path="a1.png",clip=clip)
    pg.evaluate("TARGET.set(40,75,95); Object.assign(view,{th:2.4,ph:1.1,r:300}); draw();"); pg.wait_for_timeout(400); pg.screenshot(path="a2.png",clip=clip)
    print("vinkel", pg.evaluate(V1+"faceCam(lennart);"+BOW), "klipp vy 1:", pg.evaluate(CLIP+"(LP)")); print("handen genom ekorren, böjd:", pg.evaluate(HANDCLIP+"(LP)")); pg.wait_for_timeout(400); pg.screenshot(path="a3.png",clip=clip)
    print("klipp vy inifrån:", pg.evaluate("TARGET.set(0,80,-40); Object.assign(view,{th:-1.32,ph:1.38,r:600}); draw(); faceCam(lennart);"+BOW+";"+CLIP+"(LP)")); pg.wait_for_timeout(400); pg.screenshot(path="a4.png",clip=clip)
    pg.evaluate(V1+"lennart.visible=false; lids.forEach(h=>h.rotation.x=0); skata.visible=true; skata.position.set(8,-112,0); faceCam(skata); (()=>{const pk=bowTo(SP,BEAK,[4,-28,39],4); skata.position.set(...pk.stand); SP.pose.rotation.y=pk.al; ground(SP); draw();})()"); print("handen genom skatan:", pg.evaluate(HANDCLIP+"(SP)")); pg.wait_for_timeout(400); pg.screenshot(path="a5.png",clip=clip)
    b.close()
ims=[Image.open(f"a{i}.png") for i in range(6)]
w,h=ims[0].size; W=Image.new("RGB",(w*3,h*2))
for i,im in enumerate(ims): W.paste(im,((i%3)*w,(i//3)*h))
W.resize((1560,int(1560*h*2/(w*3)))).save("stk.png")
