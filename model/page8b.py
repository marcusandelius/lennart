import re, json, base64, zipfile, io, os, markdown
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
# ---------- Utskrift-fliken: ny vy ----------
i=s.index('// ================= UTSKRIFT: BYGGPLATTOR ================='); j=s.rindex('</script>')
s=s[:i]+r'''// ================= UTSKRIFT: BYGGPLATTOR =================
let plateView = null;
function initPlates(){
  if(plateView){ plateView.resize(); return; }
  const PLATES = JSON.parse(document.getElementById("platedata").textContent);
  const st = document.getElementById("pstage");
  const r2 = new THREE.WebGLRenderer({antialias:true, alpha:true}); r2.setPixelRatio(Math.min(window.devicePixelRatio,2));
  r2.shadowMap.enabled = true; r2.shadowMap.type = THREE.PCFSoftShadowMap; st.prepend(r2.domElement);
  const sc = new THREE.Scene(); const cam2 = new THREE.PerspectiveCamera(30,1,1,6000);
  sc.add(new THREE.HemisphereLight(0xF2F5FF, 0x77736A, 0.62));
  const l1 = new THREE.DirectionalLight(0xFFF3E0, 0.85); l1.position.set(-220,420,300); l1.castShadow = true; l1.shadow.mapSize.set(2048,2048);
  Object.assign(l1.shadow.camera,{left:-230,right:230,top:330,bottom:-230,near:1,far:1500}); sc.add(l1);
  const l2 = new THREE.DirectionalLight(0xDDE6FF, 0.3); l2.position.set(300,200,-300); sc.add(l2);
  const g = new THREE.Group(); g.rotation.x = -Math.PI/2; sc.add(g);
  // byggplattan: ljus yta med rutnät var 16:e mm
  const grid = (()=>{ const c=document.createElement("canvas"); c.width=c.height=1024; const x=c.getContext("2d");
    x.fillStyle="#C9C6BB"; x.fillRect(0,0,1024,1024); x.strokeStyle="rgba(60,55,45,.16)"; x.lineWidth=1;
    for(let i=0;i<=256;i+=16){ const q=i*4; x.beginPath(); x.moveTo(q,0); x.lineTo(q,1024); x.stroke(); x.beginPath(); x.moveTo(0,q); x.lineTo(1024,q); x.stroke(); }
    x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018); return new THREE.CanvasTexture(c); })();
  const edge = new THREE.MeshStandardMaterial({color:"#8F8C82"});
  const bed = new THREE.Mesh(new THREE.BoxGeometry(256,256,3), [edge,edge,edge,edge,new THREE.MeshStandardMaterial({map:grid, roughness:.9}),edge]);
  bed.position.set(0,0,-1.5); bed.receiveShadow = true; g.add(bed);
  const holder = new THREE.Group(); holder.position.set(-128,-128,0); g.add(holder);
  const T = new THREE.Vector3(0,30,0); const v = {th:-0.5, ph:0.85, r:640};
  const labels = document.createElement("div"); labels.style.cssText = "position:absolute;inset:0;overflow:hidden;pointer-events:none"; st.appendChild(labels);
  let current = null, picked = null;
  function place(){ cam2.position.set(T.x+v.r*Math.sin(v.ph)*Math.sin(v.th), T.y+v.r*Math.cos(v.ph), T.z+v.r*Math.sin(v.ph)*Math.cos(v.th)); cam2.lookAt(T); }
  function draw2(){
    place(); r2.render(sc, cam2);
    if(!current) return;
    const w = st.clientWidth, h = st.clientHeight; holder.updateMatrixWorld();
    current.groups.forEach((gr,k) => { const pt = new THREE.Vector3(gr.cx, gr.cy, gr.top+3).applyMatrix4(holder.matrixWorld).project(cam2);
      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });
  }
  function resize2(){ const w=st.clientWidth, h=st.clientHeight; if(!w||!h) return; r2.setSize(w,h,false); cam2.aspect=w/h; cam2.updateProjectionMatrix(); draw2(); }
  // rotera, flytta (högerklick, scrollknapp eller skift) och zooma
  const ptr = new Map(); let pan2=false, pinch=0, mid=null;
  function pan(dx,dy){ const rgt=new THREE.Vector3(), up=new THREE.Vector3(); cam2.updateMatrixWorld(); rgt.setFromMatrixColumn(cam2.matrixWorld,0); up.setFromMatrixColumn(cam2.matrixWorld,1); const k=v.r*0.0011; T.addScaledVector(rgt,-dx*k).addScaledVector(up,dy*k); }
  const cv = r2.domElement;
  cv.addEventListener("contextmenu", e=>e.preventDefault());
  cv.addEventListener("mousedown", e=>{ if(e.button===1) e.preventDefault(); });
  cv.addEventListener("pointerdown", e=>{ cv.setPointerCapture(e.pointerId); ptr.set(e.pointerId,{x:e.clientX,y:e.clientY}); pan2 = e.button===2||e.button===1||e.shiftKey;
    if(ptr.size===2){ const [a,b]=[...ptr.values()]; pinch=Math.hypot(a.x-b.x,a.y-b.y); mid={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; } });
  cv.addEventListener("pointermove", e=>{ if(!ptr.has(e.pointerId)) return; const q=ptr.get(e.pointerId); const dx=e.clientX-q.x, dy=e.clientY-q.y; ptr.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if(ptr.size===1){ if(pan2) pan(dx,dy); else { v.th-=dx*0.008; v.ph=Math.min(Math.PI/2-0.02, Math.max(0.05, v.ph-dy*0.008)); } }
    else if(ptr.size===2){ const [a,b]=[...ptr.values()]; const d=Math.hypot(a.x-b.x,a.y-b.y), m={x:(a.x+b.x)/2,y:(a.y+b.y)/2}; if(pinch) v.r=Math.min(1800,Math.max(80,v.r*pinch/d)); if(mid) pan(m.x-mid.x,m.y-mid.y); pinch=d; mid=m; }
    draw2(); });
  const up2 = e=>{ ptr.delete(e.pointerId); pinch=0; mid=null; }; cv.addEventListener("pointerup",up2); cv.addEventListener("pointercancel",up2);
  cv.addEventListener("wheel", e=>{ e.preventDefault(); v.r=Math.min(1800,Math.max(80,v.r*(1+e.deltaY*0.001))); draw2(); }, {passive:false});
  const Q = 0.005, cache = {};
  function b64(sv,Ty){ const bin=atob(sv); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return new Ty(u.buffer); }
  function meshesOf(i){
    if(cache[i]) return cache[i];
    cache[i] = PLATES[i].items.map(it => {
      const q=b64(it.pos, Uint16Array), pos=new Float32Array(q.length); for(let k=0;k<q.length;k++) pos[k]=q[k]*Q;
      let geo=new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos,3));
      geo.setIndex(new THREE.BufferAttribute(it.i32 ? b64(it.idx,Uint32Array) : b64(it.idx,Uint16Array),1));
      geo=geo.toNonIndexed(); geo.computeVertexNormals();
      const m=new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color:it.color, roughness:.75, transparent:true})); m.castShadow=true; m.receiveShadow=true; m.userData.group=it.group; return m; });
    return cache[i];
  }
  const fmtH = h => h < 0.95 ? `ca ${Math.max(10,Math.round(h*6)*10)} min` : `ca ${String(Math.round(h*2)/2).replace(".",",")} h`;
  const box = document.getElementById("plates"), info = document.getElementById("pinfo");
  let lastPhase = null;
  PLATES.forEach((p,i) => {
    if(p.phase!==lastPhase){ const h=document.createElement("div"); h.className="ph"; h.textContent=p.phase; box.appendChild(h); lastPhase=p.phase; }
    const b=document.createElement("button"); b.type="button"; b.textContent=`Platta ${i+1}${p.material==="TPU"?" · TPU":""}`; b.dataset.i=i; b.setAttribute("aria-pressed","false");
    b.addEventListener("click",()=>show(i)); box.appendChild(b);
  });
  const total = PLATES.reduce((a,p)=>a+p.hours,0);
  function highlight(){ holder.children.forEach(m => { const dim = picked && m.userData.group!==picked; m.material.opacity = dim ? 0.15 : 1; m.material.depthWrite = !dim; m.castShadow = !dim; });
    info.querySelectorAll("li").forEach(li => li.setAttribute("aria-pressed", String(li.dataset.g===picked))); draw2(); }
  function show(i){
    current = PLATES[i]; picked = null;
    holder.clear(); meshesOf(i).forEach(m=>holder.add(m));
    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("");
    box.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed", String(+b.dataset.i===i)));
    const rows = current.groups.map(gr => `<li data-g="${gr.g}" tabindex="0" role="button" aria-pressed="false"><span>${gr.colors.map(c=>`<span class="sw" style="background:${c}"></span>`).join("")}</span><span><b>${gr.name}</b>${gr.how}<small>${fmtH(gr.hours)} · ${gr.files.join(", ")}</small></span></li>`).join("");
    info.innerHTML = `<h3>Platta ${i+1} av ${PLATES.length}</h3><p style="margin:0;color:var(--ink-2)">${current.phase} · ${current.material}</p>
      <p class="ptime">${fmtH(current.hours)}<small>uppskattad tid för plattan · alla ${PLATES.length} plattor ca ${Math.round(total)} h</small></p>
      <p style="margin:0 0 .4rem;color:var(--ink-2);font-size:.9rem">Klicka på en del för att lyfta fram den.</p><ul>${rows}</ul>`;
    info.querySelectorAll("li").forEach(li => { const pick = () => { picked = picked===li.dataset.g ? null : li.dataset.g; highlight(); };
      li.addEventListener("click", pick); li.addEventListener("keydown", e => { if(e.key==="Enter"||e.key===" "){ e.preventDefault(); pick(); } }); });
    T.set(0, Math.min(110, current.height*0.42), 10); v.r = Math.max(600, 470 + current.height*2.0); v.th = -0.5; v.ph = current.height > 120 ? 1.05 : 0.85;
    highlight();
  }
  plateView = {resize: resize2};
  new ResizeObserver(resize2).observe(st);
  resize2(); show(0);
}
'''+s[j:]
R("Så här kan delarna ligga på X2D:ns byggplatta, 256 × 256 mm. Plattorna är sorterade i den ordning de bör skrivas ut, och delarna håller sig inom 235,5 mm bredd, som är vad skrivaren når när båda munstyckena används. TPU skrivs ut på egna plattor eftersom det kräver andra inställningar. Bambu Studio kan placera om delarna automatiskt, så se det här som ett förslag.",
  "Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm, och varje del har en etikett. Flera delar skrivs ut upp och ner eller liggande för att slippa stöd, så de ser inte ut som i huset. Det står vid varje del hur den ligger. Plattorna är sorterade i den ordning de bör skrivas ut, och TPU ligger på egna plattor. Bambu Studio kan placera om delarna automatiskt, så se placeringen som ett förslag.")
# ---------- data: plattor, zip, fillista ----------
a=s.index('<script id="platedata" type="application/json">')+len('<script id="platedata" type="application/json">'); b=s.index('</script>',a)
s=s[:a]+open('plates.json').read()+s[b:]
with zipfile.ZipFile('/mnt/user-data/outputs/lennarts-matstation-3d.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir('stl')): z.write('stl/'+f, f)
zb=open('/mnt/user-data/outputs/lennarts-matstation-3d.zip','rb').read()
files=[(x.filename,x.file_size) for x in zipfile.ZipFile(io.BytesIO(zb)).infolist()]
a=s.index('<script id="zipdata" type="application/octet-stream">')+len('<script id="zipdata" type="application/octet-stream">'); b=s.index('</script>',a)
s=s[:a]+base64.b64encode(zb).decode()+s[b:]
s=re.sub(r'const FILES = \[.*?\];', lambda m: 'const FILES = '+json.dumps(files)+';', s, count=1, flags=re.S)
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
print(len(files),"filer,",round(len(s)/1e6,1),"MB")
