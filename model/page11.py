p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
i=s.index('const lennart = new THREE.Group(); {'); j=s.index('const skata = new THREE.Group(); {')
s=s[:i]+r'''// Lennart spelas av en klisterdekal som en hand håller i och låter hoppa
function stickerArt(){
  const S = 512, a = document.createElement("canvas"); a.width = a.height = S; const c = a.getContext("2d");
  let seed = 7; const rnd = () => (seed = (seed*16807) % 2147483647) / 2147483647;
  const FURC = "#B4572B", DARKC = "#8A3F1E", LIGHT = "#DB8F55", CREAMC = "#F5E8D4";
  const ell = (x,y,rx,ry,rot,fill) => { c.beginPath(); c.ellipse(x,y,rx,ry,rot,0,Math.PI*2); c.fillStyle = fill; c.fill(); };
  const grad = (x,y,r,c0,c1) => { const g = c.createRadialGradient(x-r*.3,y-r*.35,r*.1,x,y,r); g.addColorStop(0,c0); g.addColorStop(1,c1); return g; };
  // svansen: en bred, yvig båge bakom kroppen
  c.lineCap = "round"; c.lineJoin = "round";
  const tail = () => { c.beginPath(); c.moveTo(318,418); c.bezierCurveTo(430,400,470,250,415,150); c.bezierCurveTo(395,112,360,98,335,112); };
  tail(); c.strokeStyle = DARKC; c.lineWidth = 104; c.stroke();
  tail(); c.strokeStyle = FURC; c.lineWidth = 88; c.stroke();
  tail(); c.strokeStyle = LIGHT; c.lineWidth = 34; c.globalAlpha = .55; c.stroke(); c.globalAlpha = 1;
  // kropp, lår, mage
  ell(262,332,90,112,-0.18,grad(262,332,115,LIGHT,FURC));
  ell(296,388,72,64,0,grad(296,388,74,FURC,DARKC));
  ell(214,338,46,84,-0.1,grad(214,338,86,"#FFFAF0",CREAMC));
  // bakre örat, huvud, nos
  c.beginPath(); c.moveTo(232,140); c.lineTo(262,62); c.lineTo(274,150); c.closePath(); c.fillStyle = DARKC; c.fill();
  ell(192,186,64,55,-0.1,grad(192,186,66,LIGHT,FURC));
  ell(142,202,32,25,0.1,grad(142,202,34,"#E9A56A",FURC));
  ell(160,216,30,19,0.15,CREAMC);
  ell(113,197,7,6,0,"#2B1A12");
  // främre örat med tofs
  c.beginPath(); c.moveTo(196,142); c.lineTo(222,58); c.lineTo(246,146); c.closePath(); c.fillStyle = FURC; c.fill();
  c.beginPath(); c.moveTo(208,138); c.lineTo(222,84); c.lineTo(236,140); c.closePath(); c.fillStyle = "#E7B08A"; c.fill();
  // öga
  ell(178,174,13,12,0,CREAMC); ell(178,174,9.5,9.5,0,"#17100C"); ell(174.5,170,3.2,3.2,0,"#FFFFFF");
  // arm, tass, fot
  ell(186,292,17,38,0.55,grad(186,292,38,FURC,DARKC)); ell(163,318,12,10,0,DARKC);
  ell(218,440,52,17,0,grad(218,440,52,FURC,DARKC));
  // päls: korta streck i pälsens riktning, bara ovanpå det som redan är ritat
  c.globalCompositeOperation = "source-atop"; c.lineWidth = 1.6;
  for(let k=0;k<2600;k++){ const x = 100+rnd()*380, y = 60+rnd()*400; const tailSide = x > 330; const ang = tailSide ? -1.2+rnd()*.7 : 1.1+rnd()*.8; const L = 5+rnd()*9;
    c.strokeStyle = rnd()<.5 ? "rgba(255,214,170,.20)" : "rgba(90,36,14,.20)"; c.beginPath(); c.moveTo(x,y); c.lineTo(x+Math.cos(ang)*L, y+Math.sin(ang)*L); c.stroke(); }
  c.globalCompositeOperation = "source-over";
  // morrhår
  c.strokeStyle = "rgba(40,25,15,.7)"; c.lineWidth = 1.3; [[-34,-8],[-38,2],[-32,12]].forEach(d => { c.beginPath(); c.moveTo(126,206); c.lineTo(126+d[0],206+d[1]); c.stroke(); });
  // dekalen: vit stansad kant runt motivet, sedan en svag blank yta
  const b = document.createElement("canvas"); b.width = b.height = S; const d = b.getContext("2d");
  for(let k=0;k<28;k++){ const t = k/28*Math.PI*2; d.drawImage(a, Math.cos(t)*15, Math.sin(t)*15); }
  d.globalCompositeOperation = "source-in"; d.fillStyle = "#FBFBF8"; d.fillRect(0,0,S,S);
  const back = document.createElement("canvas"); back.width = back.height = S; back.getContext("2d").drawImage(b,0,0);    // baksidan: bara vitt papper
  d.globalCompositeOperation = "source-over"; d.drawImage(a,0,0);
  d.globalCompositeOperation = "source-atop"; const gl = d.createLinearGradient(80,40,430,470); gl.addColorStop(0,"rgba(255,255,255,.28)"); gl.addColorStop(.35,"rgba(255,255,255,0)"); gl.addColorStop(.7,"rgba(255,255,255,0)"); gl.addColorStop(1,"rgba(0,0,0,.10)"); d.fillStyle = gl; d.fillRect(0,0,S,S);
  return [new THREE.CanvasTexture(b), new THREE.CanvasTexture(back)];
}
function capsule(p0, p1, r, color){            // rundad stav mellan två punkter: fingrar och arm
  const g = new THREE.Group(), a = new THREE.Vector3(...p0), b = new THREE.Vector3(...p1), L = a.distanceTo(b), mat = new THREE.MeshStandardMaterial({color, roughness:.75});
  const cyl = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 18), mat); cyl.position.copy(a).add(b).multiplyScalar(.5); cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), b.clone().sub(a).normalize());
  const s0 = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 12), mat), s1 = s0.clone(); s0.position.copy(a); s1.position.copy(b);
  [cyl,s0,s1].forEach(m => { m.castShadow = true; g.add(m); }); return g;
}
const lennart = new THREE.Group(), sticker = new THREE.Group(); {
  const [front, back] = stickerArt(); front.anisotropy = back.anisotropy = 4;
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1); const pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, metalness:0, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  mf.castShadow = mb.castShadow = true; mf.customDepthMaterial = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:front, alphaTest:.5});
  sticker.add(mf, mb); sticker.rotation.x = Math.PI/2; sticker.position.set(0,0,64); lennart.add(sticker);
  // handen: tumme framför dekalen, pekfinger bakom, armen ut mot betraktaren
  const SKIN = "#E3B595", hand = new THREE.Group();
  hand.add(capsule([66,-17,26],[42,-5,44],8.5,SKIN), capsule([66,13,28],[42,5,46],7.5,SKIN),
    blob(8.5,SKIN,[70,12,18]), blob(8.5,SKIN,[75,9,8]), blob(8,SKIN,[79,5,-1]),
    blob(25,SKIN,[82,-6,14],[1,.62,.82]), capsule([92,-16,12],[148,-98,22],17,SKIN), capsule([140,-86,20],[250,-246,40],21,"#2E4057"));
  lennart.add(hand);
}
function faceCam(obj){ const c = actors.worldToLocal(cam.position.clone()); obj.rotation.z = Math.atan2(c.x-obj.position.x, -(c.y-obj.position.y)); }
'''+s[j:]
R('MOUTH = [0,25.5,71], LEN_X = 36, LTURN = 0.45;     // Lennart sitter snett till höger så att skålen syns','MOUTH = [-36,-4,70], LEN_X = 30;     // nosen på dekalen; Lennart står lite till höger så att skålen syns')
R('lennart.visible = true; lennart.rotation.z = LTURN; lennart.position.set(LEN_X,-235,-90);','lennart.visible = true; sticker.scale.x = 1; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart);')
R('cap("Lennart klättrar upp", "Han tar repstegen upp till framgården.", .1);','cap("Lennart kommer hoppande", "I demon spelas han av en klisterdekal.", .1);')
R('let h = hop(lennart, [LEN_X,-150,0], 700, 60); run(); await h; h = hop(lennart, [LEN_X,-100,0], 800, 22, 2); run(); await h;','let h = hop(lennart, [LEN_X+10,-165,0], 900, 34, 2); run(); await h; h = hop(lennart, [LEN_X,-104,0], 900, 26, 2); run(); await h;')
R('h = hop(lennart, [LEN_X-6,-88,0], 450, 14); run(); await h;','h = hop(lennart, [LEN_X-4,-86,0], 450, 16); run(); await h;')
R('const turnAway = tween(450, t => { lennart.rotation.z = LTURN+(Math.PI-LTURN)*t; }); run(); await turnAway;','const turnAway = tween(500, t => { sticker.scale.x = 1-2*t; n.position.x = MOUTH[0]*(1-2*t); }); run(); await turnAway;      // dekalen vänds och Lennart hoppar hem')
R('h = hop(lennart, [LEN_X-10,-160,0], 800, 24, 2); run(); await Promise.all([h, close]);\n    h = hop(lennart, [0,-240,-100], 600, 50); run(); await h; lennart.remove(n);','h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);\n    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h; lennart.remove(n);')
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
