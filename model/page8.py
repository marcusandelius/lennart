import re, json, base64, zipfile, io, os, markdown
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
def region(start, end, new, keep_end=True):
    global s
    i=s.index(start); j=s.index(end, i)
    s=s[:i]+new+(s[j:] if keep_end else s[j+len(end):])
# ---------- data ----------
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v8.json').read()+s[j:]
R('const LABEL = {','const LABEL = {doserhus:"Doserhus med ränna",doserhjul:"Doserhjul",kropp_sockel:"Stengrund",')
R('const PIVOT = {doseringsskiva:[0,64,0], lucka:[0,-8,32.2], lucka_vit:[0,-8,32.2]};','const PIVOT = {doserhjul:[0,57,64.3], lucka:[0,-8,32.2], lucka_vit:[0,-8,32.2]};')
times=json.load(open('times.json'))
m=re.search(r'const TIMES = (\{[^}]*\});', s); s=s[:m.start(1)]+json.dumps(times)+s[m.end(1):]
# ---------- kontroller ----------
R('<div class="views"><button type="button" id="reset">Återställ vy</button><button type="button" data-v="close">Närbild</button></div>',
  '<div class="views"><button type="button" id="reset">Återställ vy</button><button type="button" data-v="close">Närbild</button><button type="button" data-v="front">Framifrån</button><button type="button" data-v="side">Från sidan</button><button type="button" data-v="inside">Inuti</button></div>')
R('''        <button class="act" id="lidbtn" type="button"><span class="ic" style="background:#2B7546">&#8645;</span>Öppna / Stäng lucka</button>''',
  '''        <button class="act" id="lidbtn" type="button"><span class="ic" style="background:#2B7546">&#8645;</span>Öppna / Stäng lucka</button>
        <button class="act" id="roofbtn" type="button"><span class="ic" style="background:#5A5E62">&#8679;</span>Lyft av taket</button>''')
R('''        <label class="row"><input type="checkbox" id="ghost"> Genomskinlig kropp</label>''',
  '''        <label class="row"><input type="checkbox" id="ghost"> Genomskinliga väggar och tak</label>
        <label class="row"><input type="checkbox" id="xray"> Röntgen: allt genomskinligt</label>''')
R('''      <div class="facts" id="facts"></div>''','''      <fieldset><legend>Montering</legend>
        <button class="act" id="asmStart" type="button"><span class="ic" style="background:#3B6A2B">&#9776;</span>Visa monteringen steg för steg</button>
        <div id="asmBox" hidden>
          <p class="asmt" id="asmTitle"></p><p class="asmx" id="asmText" aria-live="polite"></p>
          <div class="asmnav"><button type="button" id="asmPrev">Föregående</button><button type="button" id="asmNext">Nästa</button><button type="button" id="asmEnd">Visa allt</button></div>
        </div>
      </fieldset>
      <div class="facts" id="facts"></div>''')
R('</style>','''.asmt{font-weight:700;margin:.2rem 0 .2rem}
.asmx{margin:0 0 .6rem;color:var(--ink-2);font-size:.95rem}
.asmnav{display:flex;gap:.4rem;flex-wrap:wrap}
.asmnav button{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
.asmnav button:disabled{opacity:.45;cursor:default}
.plabel{position:absolute;transform:translate(-50%,-110%);font-size:.78rem;line-height:1.2;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:.1rem .45rem;pointer-events:none;white-space:nowrap}
.pinfo li{cursor:pointer;border-radius:6px;padding:.4rem .3rem}
.pinfo li[aria-pressed="true"]{background:var(--surface);outline:1px solid var(--line)}
.pinfo li b{display:block}
.pinfo li small{color:var(--ink-2);display:block}
</style>''')
# ---------- apply(): röntgen, taklyft, montering ----------
region('let solo = null;\nfunction apply(){', '// faktaruta och tabell', r'''let solo = null;
const xray = document.getElementById("xray"); xray.addEventListener("change", apply);
let roofLift = 0, asmStep = 0, asmAnim = 1;
const SOLID_IN_XRAY = new Set(["doserhjul","lucka","lucka_vit"]);
// monteringen i tio steg, i den ordning delarna sätts ihop
const ASM = [
  {title:"Basen", text:"Lägg ballasten i basen och skruva på bottenplattorna. Skruva ihop basen och framgården med tre skruvar och tryck i fötterna.", from:[0,0,-120], parts:["bas","framgard","bottenplatta","framgard_platta","fotter"]},
  {title:"Gräsmattorna", text:"Lägg gräsmattorna och stenplattorna på basen och framgården.", parts:["grasmatta","stenar","framgard_gras","framgard_stenar"]},
  {title:"Kroppen", text:"Lägg packningen på plats och ställ kroppen på de två styrtapparna. Dra sex skruvar inifrån.", parts:["kropp_packning","kropp","kropp_sockel","kropp_vit"]},
  {title:"Insidan av kroppen", text:"Gör klart insidan medan den är tom: fönsterinsatserna, skärmen med ram och klämma, och kameran med sitt fäste.", from:[0,90,60], parts:["fonsterrutor","skarmram","skarmklamma","kamerafaste"]},
  {title:"Elektroniken", text:"Skruva fast elektroniklådan utifrån genom bakväggen. Skjut ner monteringsplattan med all elektronik uppifrån och lägg på locket.", parts:["elpackning","elektroniklada","monteringsplatta","ellock","genomforingar"]},
  {title:"Doseringen", text:"Ställ doserhuset på sina styrtappar och dra två skruvar. Lägg hjulet i sätet och skruva fast servot från höger.", parts:["doserhus","doserhjul"]},
  {title:"Magasinet", text:"Sätt magasinet över hjulet och dra dess två skruvar framtill. Fyll på med nötter.", parts:["notmagasin"]},
  {title:"Farstukvisten", text:"Skruva fast skålen i basen, montera luckan med sitt servo och sätt på stolphatten.", from:[0,-110,30], parts:["skal","skal_vit","lucka","lucka_vit","servopackning","servokapa"]},
  {title:"Taket", text:"Pressa ihop takhalvorna med nockkilarna, tryck fast skorstenen och takrännorna och lägg taket på plats. Magneterna håller det.", parts:["tak_v","tak_v_vit","tak_h","tak_h_vit","nockkilar","skorsten","skorsten_krage","takrannor","takpackning"]},
  {title:"Detaljerna", text:"Tryck fast kamerans solskydd, häng blomlådorna på fönsterkarmarna och snäpp fast stuprören.", from:[0,-60,90], parts:["solskydd","solskydd_vit","blomlador","blomlador_vaxter","blomlador_blommor_rod","blomlador_blommor_vit","stupror","stupror_vit"]}
];
const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1));
function apply(){
  const f = ex.value/100;
  meshes.forEach(m => {
    const p = m.userData, o = EXPLODE[p.group], b = m.userData.holder.userData.base;
    let dx = o[0]*f, dy = o[1]*f, dz = o[2]*f;
    if(p.group==="Tak") dz += roofLift*150;
    let vis = solo ? p.name===solo : state[p.group];
    if(asmStep && !solo){
      const st = STEP_OF[p.name] || 1; vis = st <= asmStep;
      if(st===asmStep){ const k = 1-asmAnim, d = ASM[st-1].from || [0,0,170]; dx += d[0]*k; dy += d[1]*k; dz += d[2]*k; }
    }
    m.userData.holder.position.set(b[0]+dx, b[1]+dy, b[2]+dz);
    m.visible = vis;
    let op = 1;
    if(!solo){
      if(xray.checked && !SOLID_IN_XRAY.has(p.name)) op = 0.14;
      else if(ghost.checked && (p.group==="Kropp" || p.group==="Tak")) op = p.group==="Tak" ? 0.12 : 0.18;
    }
    m.material.opacity = op; m.material.depthWrite = op===1; m.castShadow = op===1;
  });
  const inner = !solo && ex.value==0 && state.Inredning;
  nutsGroup.visible = inner && (!asmStep || asmStep>=7);
  screenMesh.visible = !solo && state.Kropp && (!asmStep || asmStep>=4);
  camG.visible = inner && (!asmStep || asmStep>=4);
  camGlass.visible = !solo && state.Kropp && ex.value==0 && (!asmStep || asmStep>=4);
  draw();
}
''')
R('<p>Magasinet rymmer ca 0,35 liter hasselnötter</p>','<p>Magasinet rymmer ca 0,35 liter, ungefär 50 hasselnötter</p><p>Nötter: i skal, 18–22 mm</p>')
# vyknappar
R('''  else if(v==="door"){ TARGET.set(420,520,300); Object.assign(view,{th:0.22, ph:1.0, r:3000}); cam.fov=50; }''',
  '''  else if(v==="door"){ TARGET.set(420,520,300); Object.assign(view,{th:0.22, ph:1.0, r:3000}); cam.fov=50; }
  else if(v==="front"){ const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,120+z,-10); Object.assign(view,{th:0, ph:1.45, r:820}); cam.fov=32; }
  else if(v==="side" || v==="inside"){ const z = patio.checked ? PED_H+FOOT : 0; TARGET.set(0,95+z,-55); Object.assign(view,{th:-1.45, ph:1.42, r:620}); cam.fov=32; if(v==="inside" && !xray.checked){ xray.checked = true; apply(); } }''')
# ---------- demo: hjul i stället för skiva, tak som lyfts ----------
region('const nutGeo = new THREE.SphereGeometry', 'new ResizeObserver(resize).observe(stage);', r'''const nutGeo = new THREE.SphereGeometry(8.5, 18, 12); nutGeo.scale(1,1,1.15);
const nutMat = new THREE.MeshStandardMaterial({color:"#8A5A2E", roughness:.7});
const wheel = meshes.find(m=>m.userData.name==="doserhjul").userData.holder;        // vrids kring sin axel
const DUMP = 130*Math.PI/180, AX = [0,57,64.3], PKT = 19.3;                           // tömvinkel, axelns läge, nötens avstånd från axeln i fickan
const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set rx(v){ lids.forEach(h=>h.rotation.x=v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};
// platser i magasinet: en nöt i halsen över hjulet, resten i tratten och lådan ovanför
const SLOTS = [[0,57,105.5],[-10,56,116],[10,56,116],[0,73,117]];
for(const y of [52,70,88]) for(const x of [-20,0,20]) SLOTS.push([x,y,132]);
for(const z of [150,166]) for(const y of [49,65.5,82,97]) for(const x of [-34,-17,0,17,34]) SLOTS.push([x+(z===166?2:0), y+(z===166?1:0), z]);
const nearAxis = p => Math.hypot(p[0], p[1]-57);
SLOTS.sort((a,b)=> (a[2]-b[2]) || (nearAxis(a)-nearAxis(b)));
const hopper = []; let pocket = null; const trayNuts = []; let busy = false;
const tweens = [];
function tween(dur, fn, delay=0){ return new Promise(res => tweens.push({t0:performance.now()+delay, dur, fn, res})); }
let raf = 0;
function tick(now){
  for(let i=tweens.length-1;i>=0;i--){ const tw=tweens[i]; const k=(now-tw.t0)/tw.dur; if(k<0) continue; const e=Math.min(1,k); tw.fn(e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2); if(e>=1){ tweens.splice(i,1); tw.res(); } }
  draw(); raf = tweens.length ? requestAnimationFrame(tick) : 0;
}
function run(){ if(!raf) raf = requestAnimationFrame(tick); }
const lerp=(a,b,t)=>a+(b-a)*t;
function path(obj, pts, dur, delay=0){
  const seg=[]; let L=0; for(let i=1;i<pts.length;i++){ const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1],pts[i][2]-pts[i-1][2]); seg.push(d); L+=d; }
  return tween(dur, t => { let s=t*L, i=0; while(i<seg.length-1 && s>seg[i]){ s-=seg[i]; i++; } const u=Math.min(1,s/seg[i]); const a=pts[i], b=pts[i+1]; obj.position.set(lerp(a[0],b[0],u),lerp(a[1],b[1],u),lerp(a[2],b[2],u)); obj.rotation.x+=0.15; }, delay);
}
function status(){ document.getElementById("status").textContent = `I magasinet: ${hopper.length + (pocket?1:0)} nötter. I skålen: ${trayNuts.length}.`; }
function demoView(){ if(view.r>1500) preset("close"); if(ex.value!=0){ ex.value=0; } if(asmStep) asmGo(0); solo=null; markRow(); apply(); }
function seat(n){ nutsGroup.remove(n); wheel.add(n); n.position.set(0,0,PKT); }                 // nöten ligger i hjulets ficka
function unseat(n){ const w=new THREE.Vector3(); n.getWorldPosition(w); nutsGroup.worldToLocal(w); wheel.remove(n); nutsGroup.add(n); n.position.copy(w); }
function loadPocket(){
  if(pocket || !hopper.length) return Promise.resolve();
  const n = hopper.shift(); pocket = n; const from = n.position.toArray();
  return path(n, [from, [0,57,Math.max(from[2],106)], [0,57,AX[2]+PKT]], 450).then(()=>seat(n));
}
const fillBtn = document.getElementById("fill"), roofBtn = document.getElementById("roofbtn");
const isFull = () => hopper.length === SLOTS.length-1 && !!pocket;
function fillLabel(){ fillBtn.lastChild.textContent = isFull() ? "Töm behållaren" : "Fyll på nötter"; }
function freeSlots(){ const used = new Set(hopper.map(n=>n.userData.slot)); return SLOTS.map((s,i)=>i).filter(i=>!used.has(i)); }
function sortHopper(){ hopper.sort((a,b)=> (a.position.z-b.position.z) || (nearAxis(a.position.toArray())-nearAxis(b.position.toArray()))); }
function addNut(i){ const n = new THREE.Mesh(nutGeo, nutMat); n.userData.slot = i; n.rotation.set(Math.random()*3,Math.random()*3,0); nutsGroup.add(n); hopper.push(n); return n; }
let roofUp = false;
async function moveRoof(upNow){
  if(roofUp===upNow) return; const a = roofLift, b = upNow ? 1 : 0;
  const tw = tween(900, t => { roofLift = a+(b-a)*t; apply(); }); run(); await tw;
  roofUp = upNow; roofBtn.lastChild.textContent = roofUp ? "Lägg på taket" : "Lyft av taket";
}
roofBtn.addEventListener("click", async () => { if(busy) return; busy=true; demoView(); await moveRoof(!roofUp); busy=false; });
fillBtn.addEventListener("click", async () => {
  if(busy) return; busy=true; demoView();
  const wasUp = roofUp; await moveRoof(true);                    // taket lyfts av, precis som när man fyller på på riktigt
  if(isFull()){
    const all = hopper.splice(0).concat(trayNuts.splice(0)); if(pocket){ unseat(pocket); all.push(pocket); pocket=null; }
    const jobs = all.map((n,i) => path(n, [n.position.toArray(), [n.position.x, n.position.y, 330]], 600, i*12).then(()=>nutsGroup.remove(n)));
    run(); await Promise.all(jobs);
  } else {
    const jobs=[]; const free = freeSlots(); if(pocket) free.shift();           // halsens plats står tom när en nöt redan ligger i fickan? nej: den fylls
    freeSlots().forEach((i,k) => { const s=SLOTS[i]; const n=addNut(i); n.position.set(s[0], s[1], 330); jobs.push(path(n, [[s[0],s[1],330],[s[0],s[1],s[2]]], 650, k*30)); });
    run(); await Promise.all(jobs); sortHopper();
    if(!pocket){ const p = loadPocket(); run(); await p; const i=freeSlots()[0]; if(i!==undefined){ const s=SLOTS[i]; const n=addNut(i); n.position.set(...s); sortHopper(); } }
  }
  if(!wasUp) await moveRoof(false);
  status(); fillLabel(); busy=false;
});
let lidIsOpen = false;
document.getElementById("lidbtn").addEventListener("click", async () => {
  if(busy) return; busy=true; demoView();
  if(!lidIsOpen){
    screen(pocket ? "ok" : "empty");
    const open = tween(900, t => { lid.rx = -1.66*t; });
    if(pocket){
      const turn = tween(1200, t => { wheel.rotation.x = DUMP*t; }, 300);          // hjulet vrider fickan framåt och nedåt
      run(); await Promise.all([open, turn]);
      const n = pocket; pocket = null; unseat(n);
      const k = trayNuts.length; const spot = [ -24 + (k%4)*16, -28 + Math.floor(k/4)%2*14, 13.2 + Math.floor(k/8)*12 ];
      trayNuts.push(n);
      const fall = path(n, [n.position.toArray(),[0,33.7,41.2],[0,18.7,28.6],[0,3.7,16.0],[0,-5,13.2],[spot[0]*0.5,-14,13.2],spot], 1500);
      const back = tween(1200, t => { wheel.rotation.x = DUMP*(1-t); }, 800);
      run(); await Promise.all([fall, back]);
      const lp = loadPocket(); run(); await lp;
    } else { run(); await open; }
    fillLabel(); lidIsOpen = true;
  } else {
    const close = tween(900, t => { lid.rx = -1.66*(1-t); }); run(); await close;
    screen("idle"); lidIsOpen = false;
  }
  status(); busy=false;
});
document.getElementById("deny").addEventListener("click", async () => {
  if(busy) return; busy=true; demoView(); screen("no");
  if(lidIsOpen){ const c = tween(700, t => { lid.rx = -1.66*(1-t); }); run(); await c; lidIsOpen=false; }
  const shake = tween(600, t => { lid.px = Math.sin(t*Math.PI*8)*1.2*(1-t); }); run(); await shake; lid.px = 0;
  setTimeout(()=>{ screen("idle"); busy=false; }, 2400);
});
// montering steg för steg
const asmBox = document.getElementById("asmBox"), asmStart = document.getElementById("asmStart");
function asmGo(n){
  asmStep = n; asmBox.hidden = !n; asmStart.hidden = !!n;
  if(!n){ asmAnim = 1; apply(); return; }
  const st = ASM[n-1];
  document.getElementById("asmTitle").textContent = `Steg ${n} av ${ASM.length}: ${st.title}`;
  document.getElementById("asmText").textContent = st.text;
  document.getElementById("asmPrev").disabled = n===1; document.getElementById("asmNext").disabled = n===ASM.length;
  asmAnim = 0; apply(); tween(900, t => { asmAnim = t; apply(); }); run();
}
asmStart.addEventListener("click", () => { if(busy) return; if(view.r>1500) preset("close"); ex.value = 0; roofLift = 0; roofUp = false; roofBtn.lastChild.textContent = "Lyft av taket"; solo = null; markRow(); asmGo(1); });
document.getElementById("asmPrev").addEventListener("click", () => { if(asmStep>1) asmGo(asmStep-1); });
document.getElementById("asmNext").addEventListener("click", () => { if(asmStep<ASM.length) asmGo(asmStep+1); });
document.getElementById("asmEnd").addEventListener("click", () => asmGo(0));
// start med fullt magasin och en nöt i hjulets ficka
SLOTS.forEach((s,i) => { const n = addNut(i); n.position.set(...s); }); sortHopper();
{ const n = hopper.shift(); pocket = n; seat(n); const m = addNut(n.userData.slot); m.position.set(...SLOTS[n.userData.slot]); sortHopper(); }
screen("idle"); status(); fillLabel();

''')
R('const isFull = () => hopper.length === SLOTS.length-1 && !!pocket;','const isFull = () => hopper.length === SLOTS.length && !!pocket;')
R('''    const jobs=[]; const free = freeSlots(); if(pocket) free.shift();           // halsens plats står tom när en nöt redan ligger i fickan? nej: den fylls
''','''    const jobs=[];
''')
R("Version 6 av 3D-modellen","Version 7 av 3D-modellen")
R("Prova demon: fyll på nötter och öppna luckan.","Prova demon: fyll på nötter, öppna luckan, lyft av taket eller följ monteringen steg för steg.")
open(p,'w').write(s); print("steg 1 klart")
