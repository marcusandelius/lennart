p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
def region(a,b,new,inclusive_end=False):
    global s
    i=s.index(a); j=s.index(b,i); s=s[:i]+new+(s[j+len(b):] if inclusive_end else s[j:])
# --- dekalerna: gemensam efterbehandling, ekorre och skata ---
R('function stickerArt(){\n  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");',
  'function squirrelArt(){\n  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");')
region('  // dekalen: vit stansad kant runt motivet, sedan en svag blank yta\n','  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];\n}\n', r'''  return stickerFinish(a);
}
function stickerFinish(a){                       // vit stansad kant runt motivet, sedan en svag blank yta; baksidan är bara vitt papper
  const S = a.width, b = document.createElement("canvas"); b.width = b.height = S; const d = b.getContext("2d");
  for(let k=0;k<28;k++){ const t = k/28*Math.PI*2; d.drawImage(a, Math.cos(t)*15, Math.sin(t)*15); }
  d.globalCompositeOperation = "source-in"; d.fillStyle = "#FBFBF8"; d.fillRect(0,0,S,S);
  const back = document.createElement("canvas"); back.width = back.height = S; back.getContext("2d").drawImage(b,0,0);
  d.globalCompositeOperation = "source-over"; d.drawImage(a,0,0);
  d.globalCompositeOperation = "source-atop"; const gl = d.createLinearGradient(80,40,430,470); gl.addColorStop(0,"rgba(255,255,255,.28)"); gl.addColorStop(.35,"rgba(255,255,255,0)"); gl.addColorStop(.7,"rgba(255,255,255,0)"); gl.addColorStop(1,"rgba(0,0,0,.10)"); d.fillStyle = gl; d.fillRect(0,0,S,S);
  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];
}
function magpieArt(){
  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d"); c.translate(0,42);
  let seed = 11; const rnd = () => (seed = (seed*16807) % 2147483647) / 2147483647;
  const BLK = "#17181C", WHT = "#F6F5F0", BLU = "#1F3F6E";
  const ell = (x,y,rx,ry,rot,fill) => { c.beginPath(); c.ellipse(x,y,rx,ry,rot,0,Math.PI*2); c.fillStyle = fill; c.fill(); };
  // den långa stjärten med blågrön glans
  const tg = c.createLinearGradient(300,290,490,380); tg.addColorStop(0,"#16303F"); tg.addColorStop(.5,"#1F5A5E"); tg.addColorStop(1,"#1B2A55");
  c.beginPath(); c.moveTo(300,262); c.lineTo(494,362); c.lineTo(486,384); c.lineTo(292,318); c.closePath(); c.fillStyle = tg; c.fill();
  // ben och fötter
  c.strokeStyle = "#2A2A2E"; c.lineWidth = 7; c.lineCap = "round";
  [[226,330,220,398],[262,332,266,398]].forEach(l => { c.beginPath(); c.moveTo(l[0],l[1]); c.lineTo(l[2],l[3]); c.stroke(); c.beginPath(); c.moveTo(l[2]-20,l[3]+3); c.lineTo(l[2],l[3]); c.lineTo(l[2]+16,l[3]+4); c.stroke(); });
  // kropp, vit buk, vinge, vit skulderfläck
  ell(248,268,98,62,-0.25,BLK);
  ell(232,300,72,40,-0.2,WHT);
  const wg = c.createLinearGradient(240,240,370,310); wg.addColorStop(0,"#1B2C52"); wg.addColorStop(1,BLU); ell(302,272,74,27,0.32,wg);
  ell(268,240,46,16,0.38,WHT);
  // hals, huvud, näbb, öga
  ell(196,236,52,46,-0.3,BLK); ell(160,204,45,43,0,BLK);
  c.beginPath(); c.moveTo(124,190); c.lineTo(66,210); c.lineTo(126,224); c.closePath(); c.fillStyle = "#2B2C31"; c.fill();
  ell(150,194,8,8,0,"#6B6F78"); ell(150,194,6,6,0,"#0B0B0D"); ell(148,192,2,2,0,"#FFFFFF");
  // fjädrar: korta streck ovanpå det som redan är ritat
  c.globalCompositeOperation = "source-atop"; c.lineWidth = 1.5;
  for(let k=0;k<1800;k++){ const x = 80+rnd()*420, y = 150+rnd()*260, L = 6+rnd()*10, ang = 0.35+rnd()*.5;
    c.strokeStyle = rnd()<.5 ? "rgba(120,160,220,.16)" : "rgba(0,0,0,.14)"; c.beginPath(); c.moveTo(x,y); c.lineTo(x+Math.cos(ang)*L, y+Math.sin(ang)*L); c.stroke(); }
  c.globalCompositeOperation = "source-over";
  return stickerFinish(a);
}
''', inclusive_end=True)
# --- hand och docka ---
R('function buildHand(){','function buildHand(grip){')
region('  // vrid handen så att bara tummen hamnar framför dekalen','const lennart = new THREE.Group(), pose = new THREE.Group()', r'''  // vrid handen så att bara tummen hamnar framför dekalen, med handflatan snett upp till höger om nypet
  const pch = T.clone().sub(I).normalize(), mid0 = T.clone().add(I).multiplyScalar(.5), toPalm = V(0,50,5).sub(mid0);
  const q = toPalm.sub(pch.clone().multiplyScalar(toPalm.dot(pch))).normalize(), r = pch.clone().cross(q);
  const P2 = V(0,-1,0), Q2 = V(Math.cos(.5),0,Math.sin(.5)), R2 = P2.clone().cross(Q2);
  const M = new THREE.Matrix4().makeBasis(P2,Q2,R2).multiply(new THREE.Matrix4().makeBasis(pch,q,r).transpose());
  g.quaternion.setFromRotationMatrix(M); g.scale.setScalar(.86); arm.scale.setScalar(.86);
  const mid = mid0.applyMatrix4(M); g.position.set(grip[0]-mid.x*.86, -mid.y*.86, grip[1]-mid.z*.86);
  arm.quaternion.setFromUnitVectors(V(0,-1,0), V(.86,-.44,.24).normalize());         // armen kommer in från betraktarens högra sida, handleden är böjd
  g.userData.arm = arm;
  return g;
}
// en docka: dekal + hand. pose vrids kring fötterna när handen vinklar ner dekalen
function makePuppet(tex, grip){
  const [front, back] = tex; front.anisotropy = back.anisotropy = 4;
  const P = {root:new THREE.Group(), pose:new THREE.Group(), inner:new THREE.Group(), sticker:new THREE.Group()};
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1), pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  const depth = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:back, alphaTest:.5, side:THREE.DoubleSide});   // skuggan följer dekalens kontur
  mf.customDepthMaterial = mb.customDepthMaterial = depth;
  P.sticker.add(mf, mb); P.sticker.rotation.x = Math.PI/2; P.sticker.position.set(0,0,64);
  P.hand = buildHand(grip); P.arm = P.hand.userData.arm;
  P.pose.position.set(0,0,12); P.inner.position.set(0,0,-12); P.inner.add(P.sticker, P.hand); P.pose.add(P.inner); P.root.add(P.pose, P.arm);
  P.root.userData.puppet = P; P.root.visible = false; return P;
}
const LP = makePuppet(squirrelArt(), [46,58]), SP = makePuppet(magpieArt(), [34,52]);
const lennart = LP.root, pose = LP.pose, skata = SP.root;
''')
region('const lennart = new THREE.Group(), pose = new THREE.Group()','// mjuk skugga på marken under Lennart','')
region('function syncArm(){','function faceCam(obj)', r'''function syncArm(P){ P.root.updateMatrixWorld(true); P.arm.position.copy(P.root.worldToLocal(P.hand.getWorldPosition(new THREE.Vector3()))); }   // armen följer handleden när handen vinklas
function ground(P){ syncArm(P); const p = P.root.position; shade.visible = P.root.visible && p.z > -5 && p.y > -172 && Math.abs(p.x) < 112;      // bara över framgården
  const k = 1/(1+Math.max(0,p.z)/40); shade.position.set(p.x, p.y, 2.2); shade.rotation.z = P.root.rotation.z; shade.scale.set(.95*k, .34*k, 1); shade.material.opacity = .5*k; }
// hur mycket dockan måste luta för att nosen eller näbben ska nå en punkt, och var fötterna då ska stå
function bowTo(P, tip, target, lift){
  const mx = tip[0], mz = tip[2]-12, yaw = P.root.rotation.z; let al = 0;
  while(al > -1.4 && lift+12 - mx*Math.sin(al) + mz*Math.cos(al) > target[2]) al -= 0.01;
  const fx = mx*Math.cos(al) + mz*Math.sin(al), fy = tip[1];
  return {al, stand:[target[0] - (fx*Math.cos(yaw) - fy*Math.sin(yaw)), target[1] - (fx*Math.sin(yaw) + fy*Math.cos(yaw)), lift]};
}
function tilt(P, from, to, dur){ const tw = tween(dur, t => { P.pose.rotation.y = lerp(from,to,t); syncArm(P); }); run(); return tw; }
''')
region('const skata = new THREE.Group(); {','lennart.visible = skata.visible = false; actors.add(lennart, skata);','actors.add(lennart, skata);', inclusive_end=True)
R('if(obj===lennart) ground(); }); }','if(obj.userData.puppet) ground(obj.userData.puppet); }); }')
R('MOUTH = [-36,-4,70], LEN_X = 30;','MOUTH = [-36,-4,70], BEAK = [-44,-4,56], LEN_X = 30;')
R('faceCam(lennart); ground();','faceCam(lennart); ground(LP);')
# --- besöket: huvudet i skålen, ingen nöt i munnen ---
region('cap("Lennart äter ur skålen"','lennart.visible = false; screen("idle")', r'''cap("Lennart äter ur skålen", "Handen för fram honom och tippar ner huvudet i skålen.", .85);
    const bw = bowTo(LP, MOUTH, [SPOT[0], SPOT[1], SPOT[2]+10], 8);
    h = hop(lennart, bw.stand, 550, 18); run(); await h;
    await tilt(LP, 0, bw.al, 650);
    const eat = tween(1500, t => { pose.rotation.y = bw.al + Math.sin(t*Math.PI*8)*0.05; syncArm(LP); n.scale.setScalar(Math.max(0.001, 1-t*1.1)); }); run(); await eat;       // nöten äts upp i skålen
    nutsGroup.remove(n); n.scale.setScalar(1); served++; status();
    cap("Lennart är nöjd", "Luckan stängs långsamt, och bara när kameran inte ser någon rörelse.", .95);
    await tilt(LP, bw.al, 0, 600);
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);      // han hoppar baklänges hem, utan att vända sig
    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h;
  }
  shade.visible = false; pose.rotation.y = 0; ''')
# --- skatan ---
region('skata.visible = true; skata.position.set(260,-300,220);','skata.visible = false; screen("idle"); capHide();', r'''skata.visible = true; SP.pose.rotation.y = 0; skata.position.set(60,-300,10); faceCam(skata); ground(SP);
  cap("En skata kommer hoppande", "Även hon spelas av en klisterdekal.", .15);
  let h = hop(skata, [14,-165,0], 900, 34, 2); run(); await h; h = hop(skata, [8,-112,0], 800, 24, 2); run(); await h;
  cap("Kameran tittar", "Tre bilder, och AI:n avgör vem som står där.", .4); screen("scan"); await wait(1500);
  screen("no"); cap("ACCESS DENIED", "Inte en ekorre. Luckan förblir stängd och besöket sparas som en incidentrapport.", .65);
  await wait(900);
  cap("Skatan pickar på luckan", "Hon försöker ändå, men luckan är stängd och nötterna ligger kvar.", .85);
  const pk = bowTo(SP, BEAK, [4,-28,39], 4);
  h = hop(skata, pk.stand, 500, 16); run(); await h;
  for(let k=0;k<3;k++){ await tilt(SP, k ? pk.al*.55 : 0, pk.al, 220); const shake = tween(260, t => { lid.px = Math.sin(t*Math.PI*4)*1.0*(1-t); }); run(); await Promise.all([shake, tilt(SP, pk.al, pk.al*.55, 260)]); lid.px = 0; }
  await tilt(SP, pk.al*.55, 0, 350); await wait(500);
  cap("Skatan ger upp", "Hon hoppar därifrån utan nöt.", 1);
  h = hop(skata, [20,-170,0], 900, 28, 2); run(); await h; h = hop(skata, [80,-320,10], 800, 34, 2); run(); await h;
  shade.visible = false; ''')
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
for k in ('ground()','syncArm()','sticker.','inner.','stickerArt','LTURN'): print(k, s.count(k))
