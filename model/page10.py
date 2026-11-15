import re, json
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:90]; s=s.replace(a,b,1)
def region(start,end,new):
    global s
    i=s.index(start); j=s.index(end,i); s=s[:i]+new+s[j:]
# ---- bort med dörrvarianterna ----
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v8.json').read()+s[j:]
R('const PIVOT = {v1_dorr:[0,-1.2,1.8], v1_dorr_vit:[0,-1.2,1.8], v2_dorr:[-14.5,-2.4,0], v2_dorr_vit:[-14.5,-2.4,0], v3_dorr:[0,-0.8,35], v3_dorr_vit:[0,-0.8,35], doserhjul:[0,57,64.3],','const PIVOT = {doserhjul:[0,57,64.3],')
R(' Under Entré kan du växla mellan tre förslag på dörr.','')
# ---- panelen ----
region('    <aside>\n      <fieldset id="entre">','  </div>\n  <h2>Delar att skriva ut</h2>','''    <aside>
      <section class="card">
        <h3>Demo</h3>
        <button class="act big" id="visit" type="button"><span class="ic" style="background:#2B7546">&#9654;</span><span><b>Lennart kommer på besök</b><small>Kameran känner igen honom och en nöt rullar ut</small></span></button>
        <button class="act big" id="mech" type="button"><span class="ic" style="background:#8A5A2E">&#9881;</span><span><b>Se mekanismen inifrån</b><small>Samma besök, men med genomskinligt hus</small></span></button>
        <button class="act big" id="deny" type="button"><span class="ic" style="background:#B02A22">&#10005;</span><span><b>Objuden gäst</b><small>En skata försöker och får ACCESS DENIED</small></span></button>
        <div class="pair">
          <button class="act" id="fill" type="button"><span class="ic" style="background:#8A5A2E">&#8681;</span>Fyll på nötter</button>
          <button class="act" id="roofbtn" type="button"><span class="ic" style="background:#5A5E62">&#8679;</span>Lyft av taket</button>
        </div>
        <p class="status" id="status" aria-live="polite"></p>
      </section>
      <section class="card">
        <h3>Montering</h3>
        <button class="act big" id="asmStart" type="button"><span class="ic" style="background:#3B6A2B">&#9654;</span><span><b>Spela upp monteringen</b><small>Tio steg, från bas till blomlådor</small></span></button>
      </section>
      <section class="card">
        <h3>Visa</h3>
        <fieldset id="groups" class="chips"><legend class="sr">Delgrupper</legend></fieldset>
        <label class="row"><input type="checkbox" id="patio"> Uteplatsen</label>
        <label class="row"><input type="checkbox" id="ghost"> Genomskinliga väggar och tak</label>
        <label class="row"><input type="checkbox" id="xray"> Röntgen: allt genomskinligt</label>
        <label for="explode" style="display:block;margin-top:.5rem">Plocka isär</label>
        <input type="range" id="explode" min="0" max="100" value="0">
      </section>
      <div class="facts" id="facts"></div>
    </aside>
''')
R('''      <span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span>
    </div>
    <aside>''','''      <span class="hint">Dra för att rotera · högerklick eller scrollknapp och dra för att flytta · scrolla för att zooma</span>
      <div class="cap" id="cap" hidden>
        <div class="capbody"><b id="capT"></b><span id="capX" aria-live="polite"></span></div>
        <div class="capctl" id="capCtl" hidden>
          <button type="button" id="asmPrev" aria-label="Föregående steg">&#9664;</button>
          <button type="button" id="asmPlay" aria-label="Pausa">&#10074;&#10074;</button>
          <button type="button" id="asmNext" aria-label="Nästa steg">&#9654;</button>
          <button type="button" id="asmEnd" class="txt">Stäng</button>
        </div>
        <div class="capbar"><i id="capBar"></i></div>
      </div>
    </div>
    <aside>''')
R('.stage{position:relative;background:var(--stage);border-radius:14px;overflow:hidden;aspect-ratio:4/3;min-height:20rem;touch-action:none}',
  '.stage{position:relative;background:var(--stage);border-radius:18px;overflow:hidden;height:clamp(26rem,82vh,60rem);touch-action:none;border:1px solid var(--line)}\n#pstage{height:clamp(22rem,64vh,46rem)}')
R('.views{position:absolute;left:.7rem;top:.7rem;display:flex;gap:.4rem}','.views{position:absolute;left:.7rem;top:.7rem;right:.7rem;display:flex;gap:.4rem;flex-wrap:wrap}')
R('@media (min-width:60rem){.layout{grid-template-columns:1fr 19rem}}','@media (min-width:60rem){.layout{grid-template-columns:1fr 21rem;align-items:start}}')
R('aside{display:flex;flex-direction:column;gap:1.1rem}','aside{display:flex;flex-direction:column;gap:.9rem}')
R('</style>','''.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:1rem}
.card h3{margin:0 0 .7rem;font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.card button.act{background:var(--paper)}
button.act.big{padding:.7rem .8rem;border-radius:12px;gap:.7rem}
button.act.big .ic{width:2.1rem;height:2.1rem;font-size:.95rem}
button.act.big b{display:block;line-height:1.25}
button.act.big small{display:block;color:var(--ink-2);font-size:.85rem;line-height:1.3}
button.act{transition:transform .12s,border-color .12s}
button.act:not(:disabled):active{transform:scale(.985)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:.45rem}
.pair button.act{margin-bottom:0;font-size:.9rem;padding:.5rem .6rem}
.card .status{margin:.7rem 0 0}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.5rem}
.chips label.row{border:1px solid var(--line);border-radius:999px;padding:.2rem .65rem .2rem .5rem;font-size:.9rem;gap:.4rem;background:var(--paper)}
.chips input{width:.95rem;height:.95rem}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.cap{position:absolute;left:50%;bottom:1rem;transform:translateX(-50%);width:min(34rem,calc(100% - 1.6rem));background:color-mix(in srgb,var(--surface) 94%,transparent);border:1px solid var(--line);border-radius:14px;padding:.75rem 1rem .9rem;box-shadow:0 8px 28px rgba(0,0,0,.16);display:grid;grid-template-columns:1fr auto;gap:.3rem .8rem;align-items:center;overflow:hidden;animation:capin .25s ease-out}
.cap[hidden]{display:none}
@keyframes capin{from{opacity:0;transform:translate(-50%,8px)}to{opacity:1;transform:translate(-50%,0)}}
.capbody b{display:block;font-size:1.05rem;line-height:1.25}
.capbody span{display:block;color:var(--ink-2);font-size:.95rem;line-height:1.35}
.capctl{display:flex;gap:.3rem}
.capctl[hidden]{display:none}
.capctl button{font:inherit;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;min-width:2.2rem;height:2.2rem;cursor:pointer;font-size:.8rem}
.capctl button.txt{padding:0 .8rem;font-size:.9rem}
.capctl button:disabled{opacity:.4;cursor:default}
.capbar{position:absolute;left:0;right:0;bottom:0;height:4px;background:var(--line)}
.capbar i{display:block;height:100%;width:0;background:var(--accent);transition:width .35s}
.stage:has(.cap:not([hidden])) .hint{display:none}
@media (prefers-reduced-motion:reduce){.cap{animation:none}.capbar i{transition:none}}
</style>''')
# ---- apply(): utan varianter, med aktörer ----
i=s.index('let roofLift = 0, asmStep = 0, asmAnim = 1, variant = 1;'); j=s.index('const ASM = [',i)
s=s[:i]+'let roofLift = 0, asmStep = 0, asmAnim = 1, peek = 0;\nconst SOLID_IN_XRAY = new Set(["doserhjul","lucka","lucka_vit"]);\n// monteringen i tio steg, i den ordning delarna sätts ihop\n'+s[j:]
R(' PARTS.filter(p=>p.concept).forEach(p => STEP_OF[p.name] = 8);','')
R('    let vis = solo ? p.name===solo : state[p.group] && (!p.var || p.var.includes(variant));','    let vis = solo ? p.name===solo : state[p.group];')
R('''      else if((ghost.checked || (asmStep>=4 && asmStep<=7)) && (p.group==="Kropp" || p.group==="Tak")) op = p.group==="Tak" ? 0.12 : 0.2;   // under monteringen av insidan syns den genom väggarna''',
  '''      else if(p.group==="Kropp" || p.group==="Tak"){
        const g = (ghost.checked || (asmStep>=4 && asmStep<=7)) ? 1 : peek;          // insidan syns genom väggarna när den monteras eller visas
        op = 1 - g*(p.group==="Tak" ? 0.88 : 0.8);
      }''')
R('''  nutsGroup.visible = inner && (!asmStep || asmStep>=7);''','''  nutsGroup.visible = inner && (!asmStep || asmStep>=7);
  if(pocket) pocket.visible = nutsGroup.visible;                                   // nöten i hjulets ficka följer de andra nötterna
  actors.visible = !solo && ex.value==0 && !asmStep;''')
R('  if(p.concept) return;                       // dörrvarianterna är koncept och har inga utskriftsfiler än\n','')
R('<p>${PARTS.filter(p=>!p.concept).length} delar,','<p>${PARTS.length} delar,')
# ---- demo ----
region('const nutGeo = new THREE.SphereGeometry','new ResizeObserver(resize).observe(stage);', r'''const nutGeo = new THREE.SphereGeometry(8.5, 18, 12); nutGeo.scale(1,1,1.15);
const nutMat = new THREE.MeshStandardMaterial({color:"#8A5A2E", roughness:.7});
const wheel = meshes.find(m=>m.userData.name==="doserhjul").userData.holder;        // vrids kring sin axel
const DUMP = 130*Math.PI/180, AX = [0,57,64.3], PKT = 19.3;                           // tömvinkel, axelns läge, nötens avstånd från axeln i fickan
const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set t(v){ lids.forEach(h=>h.rotation.x=-1.66*v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};
// platser i magasinet: en nöt i halsen över hjulet, resten i tratten och lådan ovanför
const SLOTS = [[0,57,105.5],[-10,56,116],[10,56,116],[0,73,117]];
for(const y of [52,70,88]) for(const x of [-20,0,20]) SLOTS.push([x,y,132]);
for(const z of [150,166]) for(const y of [49,65.5,82,97]) for(const x of [-34,-17,0,17,34]) SLOTS.push([x+(z===166?2:0), y+(z===166?1:0), z]);
const nearAxis = p => Math.hypot(p[0], p[1]-57);
SLOTS.sort((a,b)=> (a[2]-b[2]) || (nearAxis(a)-nearAxis(b)));
const hopper = []; let pocket = null, served = 0, busy = false;
const tweens = [];
function tween(dur, fn, delay=0){ return new Promise(res => tweens.push({t0:performance.now()+delay, dur, fn, res})); }
let raf = 0;
function tick(now){
  for(let i=tweens.length-1;i>=0;i--){ const tw=tweens[i]; const k=(now-tw.t0)/tw.dur; if(k<0) continue; const e=Math.min(1,k); tw.fn(e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2); if(e>=1){ tweens.splice(i,1); tw.res(); } }
  draw(); raf = tweens.length ? requestAnimationFrame(tick) : 0;
}
function run(){ if(!raf) raf = requestAnimationFrame(tick); }
const lerp=(a,b,t)=>a+(b-a)*t;
const wait = ms => { const w = tween(ms, ()=>{}); run(); return w; };
function path(obj, pts, dur, delay=0){
  const seg=[]; let L=0; for(let i=1;i<pts.length;i++){ const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1],pts[i][2]-pts[i-1][2]); seg.push(d); L+=d; }
  return tween(dur, t => { let s=t*L, i=0; while(i<seg.length-1 && s>seg[i]){ s-=seg[i]; i++; } const u=Math.min(1,s/seg[i]); const a=pts[i], b=pts[i+1]; obj.position.set(lerp(a[0],b[0],u),lerp(a[1],b[1],u),lerp(a[2],b[2],u)); obj.rotation.x+=0.15; }, delay);
}
// kameran glider mellan vyer
function flyTo(o, dur=1000){
  const off = patio.checked ? PED_H+FOOT : 0;
  const a = {x:TARGET.x, y:TARGET.y, z:TARGET.z, th:view.th, ph:view.ph, r:view.r, fov:cam.fov};
  let dth = o.th-a.th; dth = Math.atan2(Math.sin(dth), Math.cos(dth));
  const tw = tween(dur, t => { TARGET.set(lerp(a.x,o.T[0],t), lerp(a.y,o.T[1]+off,t), lerp(a.z,o.T[2],t)); view.th = a.th+dth*t; view.ph = lerp(a.ph,o.ph,t); view.r = lerp(a.r,o.r,t); cam.fov = lerp(a.fov,32,t); cam.updateProjectionMatrix(); });
  run(); return tw;
}
const VIEW_VISIT = {T:[0,62,58], th:-0.62, ph:1.2, r:700}, VIEW_MECH = {T:[0,80,-40], th:-1.32, ph:1.38, r:600}, VIEW_HOME = {T:[0,105,-20], th:-0.55, ph:1.15, r:860};
// textremsan i bilden
const capEl = document.getElementById("cap"), capBar = document.getElementById("capBar");
function cap(title, text, progress){ capEl.hidden = false; document.getElementById("capT").textContent = title; document.getElementById("capX").textContent = text; if(progress!==undefined) capBar.style.width = (progress*100)+"%"; }
function capHide(){ capEl.hidden = true; capBar.style.width = "0"; }
const acts = [...document.querySelectorAll("aside button.act")];
function setBusy(b){ busy = b; acts.forEach(x => x.disabled = b); }
function status(){ document.getElementById("status").textContent = `I magasinet: ${hopper.length + (pocket?1:0)} nötter. Lennart har fått ${served}.`; }
function demoReset(){ if(asmStep) asmStop(); if(ex.value!=0) ex.value = 0; solo = null; markRow(); apply(); }
function seat(n){ nutsGroup.remove(n); wheel.add(n); n.position.set(0,0,PKT); }                 // nöten ligger i hjulets ficka
function unseat(n){ const w=new THREE.Vector3(); n.getWorldPosition(w); nutsGroup.worldToLocal(w); wheel.remove(n); nutsGroup.add(n); n.position.copy(w); n.visible = true; }
function loadPocket(){
  if(pocket || !hopper.length) return Promise.resolve();
  const n = hopper.shift(); pocket = n; const from = n.position.toArray();
  return path(n, [from, [0,57,Math.max(from[2],106)], [0,57,AX[2]+PKT]], 450).then(()=>seat(n));
}
const fillBtn = document.getElementById("fill"), roofBtn = document.getElementById("roofbtn");
const isFull = () => hopper.length === SLOTS.length && !!pocket;
function fillLabel(){ fillBtn.lastChild.textContent = isFull() ? "Töm magasinet" : "Fyll på nötter"; }
function freeSlots(){ const used = new Set(hopper.map(n=>n.userData.slot)); return SLOTS.map((s,i)=>i).filter(i=>!used.has(i)); }
function sortHopper(){ hopper.sort((a,b)=> (a.position.z-b.position.z) || (nearAxis(a.position.toArray())-nearAxis(b.position.toArray()))); }
function addNut(i){ const n = new THREE.Mesh(nutGeo, nutMat); n.userData.slot = i; n.rotation.set(Math.random()*3,Math.random()*3,0); nutsGroup.add(n); hopper.push(n); return n; }

// ---- aktörerna: Lennart och skatan ----
const actors = new THREE.Group(); nutsGroup.parent.add(actors);
function blob(r, color, pos, sc=[1,1,1]){ const m = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), new THREE.MeshStandardMaterial({color, roughness:.85})); m.position.set(...pos); m.scale.set(...sc); m.castShadow = true; return m; }
function cone(r, h, color, pos, rot){ const m = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14), new THREE.MeshStandardMaterial({color, roughness:.8})); m.position.set(...pos); m.rotation.set(...rot); m.castShadow = true; return m; }
const FUR = "#B4552B", CREAM = "#F0E2CC", DARK = "#1B1B1D";
const lennart = new THREE.Group(); {
  const g = new THREE.Group(); g.scale.setScalar(2.2); lennart.add(g);
  g.add(blob(14,FUR,[0,0,20],[1,1,1.3]), blob(10,CREAM,[0,7,19],[.9,.8,1.2]), blob(9.5,FUR,[0,7,44]), blob(4.6,CREAM,[0,15,42]), blob(1.4,DARK,[0,19.2,43.2]),
    blob(1.5,DARK,[5,13.4,47]), blob(1.5,DARK,[-5,13.4,47]), cone(2.8,8,FUR,[5,4,55],[Math.PI/2,0,0]), cone(2.8,8,FUR,[-5,4,55],[Math.PI/2,0,0]),
    blob(3.6,FUR,[7,12,27]), blob(3.6,FUR,[-7,12,27]), blob(5,FUR,[8,8,3.2],[1,1.6,.6]), blob(5,FUR,[-8,8,3.2],[1,1.6,.6]),
    blob(9,FUR,[0,-13,16]), blob(9.6,FUR,[0,-20,28]), blob(9.2,FUR,[0,-22,41]), blob(8,FUR,[0,-17,52]), blob(6.5,FUR,[0,-10,58]));
}
const skata = new THREE.Group(); {
  const g = new THREE.Group(); g.scale.setScalar(1.25); skata.add(g);
  g.add(blob(26,DARK,[0,0,46],[.8,1.45,.85]), blob(20,"#F4F4F0",[0,8,40],[.8,1.15,.8]), blob(14,DARK,[0,36,64]), cone(4.5,20,"#2A2A2E",[0,57,63],[0,0,0]),
    blob(1.6,"#EDEDED",[6.5,44,68]), blob(1.6,"#EDEDED",[-6.5,44,68]), blob(7,"#1F2B44",[0,-58,52],[.9,6,.45]), blob(14,"#F4F4F0",[17,2,50],[.3,1.2,.5]), blob(14,"#F4F4F0",[-17,2,50],[.3,1.2,.5]),
    blob(2,"#2A2A2E",[6,6,12],[1,1,6]), blob(2,"#2A2A2E",[-6,6,12],[1,1,6]));
}
lennart.visible = skata.visible = false; actors.add(lennart, skata);
function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); }); }
const SPOT = [0,-24,13.2], MOUTH = [0,33,92];

async function moveRoof(upNow){
  if(roofUp===upNow) return; const a = roofLift, b = upNow ? 1 : 0;
  const tw = tween(900, t => { roofLift = a+(b-a)*t; apply(); }); run(); await tw;
  roofUp = upNow; roofBtn.lastChild.textContent = roofUp ? "Lägg på taket" : "Lyft av taket";
}
let roofUp = false;
function setPeek(v, dur=600){ const a = peek; const tw = tween(dur, t => { peek = lerp(a,v,t); apply(); }); run(); return tw; }

// ---- Lennart kommer på besök ----
async function visit(inside){
  if(busy) return; setBusy(true); demoReset(); await moveRoof(false);
  const back = {T:[TARGET.x, TARGET.y-(patio.checked?PED_H+FOOT:0), TARGET.z], th:view.th, ph:view.ph, r:view.r}, hadX = xray.checked;
  if(inside){ xray.checked = true; apply(); await flyTo(VIEW_MECH); } else await flyTo(VIEW_VISIT);
  lennart.visible = true; lennart.rotation.z = 0; lennart.position.set(0,-235,-90);
  cap("Lennart klättrar upp", "Han tar repstegen upp till framgården.", .1);
  let h = hop(lennart, [0,-150,0], 700, 60); run(); await h; h = hop(lennart, [0,-104,0], 800, 22, 2); run(); await h;
  cap("Kameran tittar", "Den tar tre bilder och AI:n avgör vem som står där.", .3); screen("scan"); await wait(1500);
  if(!pocket){
    screen("empty"); cap("Magasinet är tomt", "Lennart får vänta. Fyll på nötter och prova igen.", 1); await wait(2400);
  } else {
    screen("ok"); cap("ACCESS GRANTED", "Det är Lennart. Luckan öppnas och hjulet vrider fram en nöt.", .5);
    const open = tween(900, t => { lid.t = t; }), turn = tween(1300, t => { wheel.rotation.x = DUMP*t; }, 350);
    run(); await Promise.all([open, turn]);
    cap("En nöt rullar ut", "Fickan släpper nöten i rännan, och den rullar ner i skålen.", .7);
    const n = pocket; pocket = null; unseat(n);
    const fall = path(n, [n.position.toArray(),[0,33.7,41.2],[0,18.7,28.6],[0,3.7,16.0],[0,-5,13.2],SPOT], 1500);
    const ret = tween(1200, t => { wheel.rotation.x = DUMP*(1-t); }, 900);
    run(); await Promise.all([fall, ret]); const lp = loadPocket(); run(); await lp;
    cap("Lennart tar sin nöt", "Sedan stängs luckan långsamt, och bara när kameran inte ser någon rörelse.", .9);
    h = hop(lennart, [0,-92,0], 450, 14); run(); await h;
    const lp0 = lennart.position; const grab = path(n, [SPOT, [0,-40,40], [lp0.x+MOUTH[0], lp0.y+MOUTH[1], MOUTH[2]]], 600); run(); await grab;
    nutsGroup.remove(n); lennart.add(n); n.position.set(...MOUTH); served++; status();
    await wait(500);
    const turnAway = tween(450, t => { lennart.rotation.z = Math.PI*t; }); run(); await turnAway;
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [0,-160,0], 800, 24, 2); run(); await Promise.all([h, close]);
    h = hop(lennart, [0,-240,-100], 600, 50); run(); await h; lennart.remove(n);
  }
  lennart.visible = false; screen("idle"); fillLabel(); status(); capHide();
  if(inside){ xray.checked = hadX; apply(); }
  await flyTo(back, 900); setBusy(false);
}
document.getElementById("visit").addEventListener("click", () => visit(false));
document.getElementById("mech").addEventListener("click", () => visit(true));
// ---- Objuden gäst ----
document.getElementById("deny").addEventListener("click", async () => {
  if(busy) return; setBusy(true); demoReset(); await moveRoof(false);
  const back = {T:[TARGET.x, TARGET.y-(patio.checked?PED_H+FOOT:0), TARGET.z], th:view.th, ph:view.ph, r:view.r};
  await flyTo(VIEW_VISIT);
  skata.visible = true; skata.position.set(260,-300,220); skata.rotation.z = 0.5;
  cap("En skata landar", "Hon har sett var nötterna kommer ut.", .15);
  let h = hop(skata, [34,-112,0], 1100, 30); run(); await h;
  cap("Kameran tittar", "Tre bilder, och AI:n avgör vem som står där.", .4); screen("scan"); await wait(1500);
  screen("no"); cap("ACCESS DENIED", "Inte en ekorre. Luckan förblir stängd och besöket sparas som en incidentrapport.", .7);
  const shake = tween(700, t => { lid.px = Math.sin(t*Math.PI*8)*1.2*(1-t); }); h = hop(skata, [34,-112,0], 900, 12, 3); run(); await Promise.all([shake, h]); lid.px = 0;
  await wait(1500);
  cap("Skatan ger upp", "Nötterna ligger kvar i magasinet.", 1);
  h = hop(skata, [-280,-320,260], 1200, 40); run(); await h;
  skata.visible = false; screen("idle"); capHide(); await flyTo(back, 900); setBusy(false);
});
// ---- taket och påfyllningen ----
roofBtn.addEventListener("click", async () => { if(busy) return; setBusy(true); demoReset(); await moveRoof(!roofUp); setBusy(false); });
fillBtn.addEventListener("click", async () => {
  if(busy) return; setBusy(true); demoReset();
  const wasUp = roofUp, emptying = isFull();
  cap(emptying ? "Magasinet töms" : "Påfyllning", "Taket hålls av magneter. Lyft av det, så ligger magasinet öppet.", .3);
  await moveRoof(true);
  if(emptying){
    const all = hopper.splice(0); if(pocket){ unseat(pocket); all.push(pocket); pocket=null; }
    const jobs = all.map((n,i) => path(n, [n.position.toArray(), [n.position.x, n.position.y, 330]], 600, i*12).then(()=>nutsGroup.remove(n)));
    run(); await Promise.all(jobs);
  } else {
    cap("Påfyllning", "Häll i hasselnötter i skal, 18–22 mm. Magasinet rymmer ungefär 50.", .7);
    const jobs = []; freeSlots().forEach((i,k) => { const s=SLOTS[i]; const n=addNut(i); n.position.set(s[0], s[1], 330); jobs.push(path(n, [[s[0],s[1],330],[s[0],s[1],s[2]]], 650, k*30)); });
    run(); await Promise.all(jobs); sortHopper();
    if(!pocket){ const p = loadPocket(); run(); await p; const i=freeSlots()[0]; if(i!==undefined){ const s=SLOTS[i]; const n=addNut(i); n.position.set(...s); sortHopper(); } }
  }
  if(!wasUp) await moveRoof(false);
  status(); fillLabel(); capHide(); setBusy(false);
});
// ---- monteringen spelas upp av sig själv ----
const asmCtl = document.getElementById("capCtl"), asmPlayBtn = document.getElementById("asmPlay");
let asmPlaying = false, asmTimer = 0;
function asmShow(n){
  clearTimeout(asmTimer); asmStep = n; const st = ASM[n-1];
  cap(`${n}. ${st.title}`, st.text, n/ASM.length);
  document.getElementById("asmPrev").disabled = n===1; document.getElementById("asmNext").disabled = n===ASM.length;
  asmAnim = 0; apply(); tween(900, t => { asmAnim = t; apply(); }); run();
  if(asmPlaying){ if(n<ASM.length) asmTimer = setTimeout(() => asmShow(n+1), 3600); else asmSetPlaying(false); }
}
function asmSetPlaying(b){ asmPlaying = b; asmPlayBtn.innerHTML = b ? "&#10074;&#10074;" : "&#9654;"; asmPlayBtn.setAttribute("aria-label", b ? "Pausa" : "Spela"); if(!b) clearTimeout(asmTimer); }
function asmStop(){ clearTimeout(asmTimer); asmPlaying = false; asmStep = 0; asmAnim = 1; asmCtl.hidden = true; capHide(); acts.forEach(x => x.disabled = false); apply(); }
document.getElementById("asmStart").addEventListener("click", async () => {
  if(busy) return; demoReset(); ex.value = 0; roofLift = 0; roofUp = false; roofBtn.lastChild.textContent = "Lyft av taket";
  acts.forEach(x => x.disabled = true); asmCtl.hidden = false; asmStep = 1; asmAnim = 0; apply();
  await flyTo(VIEW_HOME, 800); asmSetPlaying(true); asmShow(1);
});
document.getElementById("asmPrev").addEventListener("click", () => { if(asmStep>1){ asmSetPlaying(false); asmShow(asmStep-1); } });
document.getElementById("asmNext").addEventListener("click", () => { if(asmStep<ASM.length){ asmSetPlaying(false); asmShow(asmStep+1); } });
asmPlayBtn.addEventListener("click", () => { if(asmPlaying) asmSetPlaying(false); else { asmSetPlaying(true); asmShow(asmStep<ASM.length ? asmStep+1 : 1); } });
document.getElementById("asmEnd").addEventListener("click", asmStop);
// start med fullt magasin och en nöt i hjulets ficka
SLOTS.forEach((s,i) => { const n = addNut(i); n.position.set(...s); }); sortHopper();
{ const n = hopper.shift(); pocket = n; seat(n); const m = addNut(n.userData.slot); m.position.set(...SLOTS[n.userData.slot]); sortHopper(); }
screen("idle"); status(); fillLabel();

''')
R('''  else if(mode==="empty"){''','''  else if(mode==="scan"){ c.fillStyle="#F2C14E"; c.font="bold 30px Courier New, monospace"; c.fillText("VERIFIERAR…",168,124); }
  else if(mode==="empty"){''')
R("Prova demon: fyll på nötter, öppna luckan, lyft av taket eller följ monteringen steg för steg.","Prova demon: låt Lennart komma på besök, titta på mekanismen inifrån eller spela upp monteringen.")
# rester av dörrvarianterna
s=re.sub(r'\n// byt entré\nfunction setVariant.*?\n// montering steg för steg','',s,flags=re.S)
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
for k in ('variant','setVariant','v1_dorr','asmGo','asmBox','lidbtn','lidIsOpen','trayNuts'):
    print(k, s.count(k))
