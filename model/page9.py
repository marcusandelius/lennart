import re, json
p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)>=1, "MISSING "+a[:90]; s=s.replace(a,b) if cnt==0 else s.replace(a,b,cnt)
i=s.index('const PARTS = ')+len('const PARTS = '); j=s.index(';\n', i)
s=s[:i]+open('parts_v9.json').read()+s[j:]
a=s.index('<script id="platedata" type="application/json">')+len('<script id="platedata" type="application/json">'); b=s.index('</script>',a)
s=s[:a]+open('plates.json').read()+s[b:]
R('const PIVOT = {doserhjul:[0,57,64.3],','const PIVOT = {v1_dorr:[0,-1.2,1.8], v1_dorr_vit:[0,-1.2,1.8], v2_dorr:[-14.5,-2.4,0], v2_dorr_vit:[-14.5,-2.4,0], v3_dorr:[0,-0.8,35], v3_dorr_vit:[0,-0.8,35], doserhjul:[0,57,64.3],')
R('PARTS.forEach(p => {\n  const tr = document.createElement("tr");','PARTS.forEach(p => {\n  if(p.concept) return;                       // dörrvarianterna är koncept och har inga utskriftsfiler än\n  const tr = document.createElement("tr");')
R('<p>${PARTS.length} delar,','<p>${PARTS.filter(p=>!p.concept).length} delar,')
R('''      <fieldset><legend>Demo</legend>''','''      <fieldset id="entre"><legend>Entré</legend>
        <label class="row"><input type="radio" name="var" value="1" checked> Vindbryggan</label>
        <label class="row"><input type="radio" name="var" value="2"> Stugdörren</label>
        <label class="row"><input type="radio" name="var" value="3"> Svängdörren</label>
        <label class="row"><input type="radio" name="var" value="0"> Skålen med lucka (nuvarande)</label>
        <p class="status" id="vtxt" aria-live="polite"></p>
      </fieldset>
      <fieldset><legend>Demo</legend>''')
R('let roofLift = 0, asmStep = 0, asmAnim = 1;','let roofLift = 0, asmStep = 0, asmAnim = 1, variant = 1;')
R('const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1));','const STEP_OF = {}; ASM.forEach((st,i) => st.parts.forEach(n => STEP_OF[n] = i+1)); PARTS.filter(p=>p.concept).forEach(p => STEP_OF[p.name] = 8);')
R('    let vis = solo ? p.name===solo : state[p.group];','    let vis = solo ? p.name===solo : state[p.group] && (!p.var || p.var.includes(variant));')
R('''const lids = meshes.filter(m=>m.userData.name.startsWith("lucka")).map(m=>m.userData.holder);
const lid = {set rx(v){ lids.forEach(h=>h.rotation.x=v); }, set px(v){ lids.forEach(h=>h.position.x=h.userData.base[0]+v); }};''',
'''// entréns fyra varianter: vilka delar som rör sig, kring vilken axel och hur långt
const DOORS = {0:{names:["lucka","lucka_vit"], axis:"x", open:-1.66}, 1:{names:["v1_dorr","v1_dorr_vit"], axis:"x", open:1.6}, 2:{names:["v2_dorr","v2_dorr_vit"], axis:"z", open:-1.4}, 3:{names:["v3_dorr","v3_dorr_vit"], axis:"x", open:-1.15}};
Object.values(DOORS).forEach(d => d.h = meshes.filter(m=>d.names.includes(m.userData.name)).map(m=>m.userData.holder));
const lid = {set t(v){ const d = DOORS[variant]; d.h.forEach(h=>h.rotation[d.axis]=d.open*v); }, set px(v){ DOORS[variant].h.forEach(h=>h.position.x=h.userData.base[0]+v); }};
const ring5 = (cy, z) => k => { const q = [[0,cy],[-13,cy-4],[13,cy-4],[-7,cy+8],[7,cy+8]][k%5]; return [q[0], q[1], z+Math.floor(k/5)*10]; };
const SPOTS = {0: k => [-24+(k%4)*16, -28+Math.floor(k/4)%2*14, 13.2+Math.floor(k/8)*12], 1: ring5(-56, 9.2), 2: ring5(-45, 10.3), 3: ring5(-45, 10.3)};
const EXITS = {0:[[0,-5,13.2]], 1:[[0,-6,12.9],[0,-34,12.5]], 2:[[0,-6,12.6],[0,-26,12.3]], 3:[[0,-6,12.6],[0,-26,12.3]]};
const VTXT = {1:"Dörren fälls ner som en vindbrygga och blir rampen som nöten rullar ut på. Samma servo som i dag, gömt i stolpen.",
  2:"En sidohängd dörr med hjärta slås upp och nöten rullar ut på trappstenen. Servots axel är gångjärnet.",
  3:"Luckan hänger i överkanten och nöten knuffar upp den själv på vägen ut. Inget servo utomhus.",
  0:"Dagens lösning: nöten rullar ner i en skål under en lucka. Det är den här som utskriftsfilerna gäller."};
const LIDTXT = {0:"Öppna / Stäng lucka", 1:"Öppna / Stäng dörren", 2:"Öppna / Stäng dörren", 3:"Släpp ut en nöt"};''')
R('const open = tween(900, t => { lid.rx = -1.66*t; });','const flap = variant===3;\n    const open = flap ? Promise.resolve() : tween(900, t => { lid.t = t; });')
R('const k = trayNuts.length; const spot = [ -24 + (k%4)*16, -28 + Math.floor(k/4)%2*14, 13.2 + Math.floor(k/8)*12 ];','const spot = SPOTS[variant](trayNuts.length);')
R('[0,3.7,16.0],[0,-5,13.2],[spot[0]*0.5,-14,13.2],spot], 1500);','[0,3.7,16.0],...EXITS[variant],spot], 1500);\n      if(flap) tween(1500, t => { lid.t = Math.sin(Math.PI*Math.min(1,Math.max(0,(t-0.45)/0.5))); });   // nöten knuffar upp luckan')
R('fillLabel(); lidIsOpen = true;','fillLabel(); lidIsOpen = !flap; if(flap) setTimeout(()=>screen("idle"), 1600);')
R('const close = tween(900, t => { lid.rx = -1.66*(1-t); }); run(); await close;','const close = tween(900, t => { lid.t = 1-t; }); run(); await close;')
R('if(lidIsOpen){ const c = tween(700, t => { lid.rx = -1.66*(1-t); }); run(); await c; lidIsOpen=false; }','if(lidIsOpen){ const c = tween(700, t => { lid.t = 1-t; }); run(); await c; lidIsOpen=false; }')
R('// montering steg för steg','''// byt entré
function setVariant(v){
  lid.t = 0; lidIsOpen = false; trayNuts.splice(0).forEach(n => nutsGroup.remove(n));
  variant = v; lid.t = 0;
  document.getElementById("lidbtn").lastChild.textContent = LIDTXT[v]; document.getElementById("vtxt").textContent = VTXT[v];
  screen("idle"); status(); apply();
}
document.getElementById("entre").addEventListener("change", e => { if(e.target.name!=="var") return; if(busy){ document.querySelector(`#entre input[value="${variant}"]`).checked = true; return; } setVariant(+e.target.value); });
// montering steg för steg''')
R('screen("idle"); status(); fillLabel();\n','setVariant(1); fillLabel();\n')
# byggplattan: rätt zon för två munstycken och mått
R('''x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018);''','''x.fillStyle="rgba(176,42,34,.20)"; x.fillRect(0,0,82,1024); x.strokeStyle="rgba(176,42,34,.55)"; x.lineWidth=3; x.beginPath(); x.moveTo(82,0); x.lineTo(82,1024); x.stroke();
    x.strokeStyle="rgba(60,55,45,.55)"; x.lineWidth=6; x.strokeRect(3,3,1018,1018);''')
R('''    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("");''','''    labels.innerHTML = current.groups.map(gr=>`<span class="plabel">${gr.name}</span>`).join("") + `<span class="plabel dim">256 mm</span><span class="plabel dim">256 mm</span><span class="plabel dim">20,5 mm: bara vänster munstycke</span>`;''')
R('''      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });''','''      const el = labels.children[k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; el.style.display = pt.z<1 ? "" : "none"; });
    [[128,-9,0],[265,128,0],[10,265,0]].forEach((q,k) => { const pt = new THREE.Vector3(...q).applyMatrix4(holder.matrixWorld).project(cam2);
      const el = labels.children[current.groups.length+k]; el.style.left = ((pt.x+1)/2*w)+"px"; el.style.top = ((1-pt.y)/2*h)+"px"; });''')
R('.pinfo li{cursor:pointer','.plabel.dim{background:none;border:0;color:var(--ink-2);transform:translate(-50%,-50%)}\n.pinfo li{cursor:pointer')
R("Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm, och varje del har en etikett.","Varje platta är en utskrift. Den ljusa ytan är X2D:ns byggplatta, 256 × 256 mm. Den röda remsan till vänster, 20,5 mm, når bara det vänstra munstycket, så delarna ligger utanför den. Varje del har en etikett.")
R("lyft av taket eller följ monteringen steg för steg.","lyft av taket eller följ monteringen steg för steg. Under Entré kan du växla mellan tre förslag på dörr.")
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
print("ok")
