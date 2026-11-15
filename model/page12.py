p='/mnt/user-data/outputs/lennarts-matstation-3d.html'
s=open(p).read()
def R(a,b):
    global s
    assert a in s, "MISSING "+a[:80]; s=s.replace(a,b,1)
i=s.index('function capsule(p0, p1, r, color){'); j=s.index('function faceCam(obj)')
s=s[:i]+r'''// en hand i naturlig storlek: handflata, fem fingrar med leder och naglar, handled, underarm och ärm
const SKIN = new THREE.MeshStandardMaterial({color:"#D8A584", roughness:.62}), NAIL = new THREE.MeshStandardMaterial({color:"#F1D3C2", roughness:.3}), CLOTH = new THREE.MeshStandardMaterial({color:"#2E4057", roughness:.95});
const V = (x,y,z) => new THREE.Vector3(x,y,z);
function limb(g, a, b, r0, r1, mat=SKIN){            // avsmalnande, rundad del mellan två punkter
  const L = a.distanceTo(b), cyl = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, L, 20), mat);
  cyl.position.copy(a).add(b).multiplyScalar(.5); cyl.quaternion.setFromUnitVectors(V(0,1,0), b.clone().sub(a).normalize());
  const s0 = new THREE.Mesh(new THREE.SphereGeometry(r0, 20, 14), mat), s1 = new THREE.Mesh(new THREE.SphereGeometry(r1, 20, 14), mat); s0.position.copy(a); s1.position.copy(b);
  [cyl,s0,s1].forEach(m => { m.castShadow = m.receiveShadow = true; g.add(m); });
}
function lump(g, c, r, sc, mat=SKIN){ const m = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), mat); m.position.copy(c); m.scale.set(...sc); m.castShadow = m.receiveShadow = true; g.add(m); return m; }
function nail(g, a, b, r, away){                     // nagel på yttersta leden, på fingrets ovansida
  const d = b.clone().sub(a).normalize(), n = away.clone().sub(d.clone().multiplyScalar(away.dot(d))).normalize();
  const m = lump(g, a.clone().lerp(b,.72).add(n.clone().multiplyScalar(r*.62)), r*.86, [1,1,1], NAIL);
  m.quaternion.setFromUnitVectors(V(0,0,1), n); m.scale.set(.82,1.05,.34); const q = new THREE.Quaternion().setFromUnitVectors(V(0,1,0), d.clone().applyQuaternion(m.quaternion.clone().invert()).setZ(0).normalize()); m.quaternion.multiply(q);
}
function buildHand(){
  // handens egna axlar: y mot fingrarna, x mot tummen, z ut från handflatan
  const g = new THREE.Group();
  lump(g, V(0,50,0), 1, [41,50,14]); lump(g, V(-8,18,3), 1, [33,22,15]); lump(g, V(27,34,9), 1, [19,31,15]); lump(g, V(-30,44,5), 1, [13,34,13]);
  const curl = (base, lens, radii, flex, splay) => { let pt = base.clone(), ang = 0; const pts = [pt.clone()];
    lens.forEach((L,k) => { ang += flex[k]*Math.PI/180; pt = pt.clone().add(V(splay, Math.cos(ang), Math.sin(ang)).normalize().multiplyScalar(L)); pts.push(pt.clone()); });
    lump(g, base, radii[0]+1.2, [1,1,1]);
    for(let k=0;k<3;k++) limb(g, pts[k], pts[k+1], radii[k], radii[k+1]);
    const dz = pts[3].clone().sub(pts[2]).normalize(); nail(g, pts[2], pts[3], radii[3], V(0, dz.z, -dz.y)); };
  curl(V(9,98,-2),  [46,30,23], [10,9,8,7],     [80,85,60], 0);          // långfinger, ringfinger och lillfinger är krökta in mot handflatan
  curl(V(-10,95,-2),[42,28,22], [9.5,8.6,7.6,6.8],[85,85,60], -.05);
  curl(V(-27,87,-1),[33,20,19], [8.4,7.4,6.6,6], [88,85,60], -.1);
  // pekfinger och tumme möts i ett nyp
  const K = V(27,97,-2), J1 = V(26,117,32), J2 = V(24,113,58), I = V(22,98,72);
  lump(g, K, 11, [1,1,1]); limb(g, K, J1, 10, 9); limb(g, J1, J2, 9, 8); limb(g, J2, I, 8, 7); nail(g, J2, I, 7, V(0,1,.6));
  const B = V(31,20,10), T1 = V(52,47,34), T2 = V(46,74,55), T = V(37,89,65);
  limb(g, B, T1, 14, 11.5); limb(g, T1, T2, 11.5, 10); limb(g, T2, T, 10, 8.6); nail(g, T2, T, 8.6, V(1,-.4,-.2));
  // handled, underarm och uppkavlad ärm
  const arm = new THREE.Group(); arm.scale.set(1,1,.8); g.add(arm);
  limb(arm, V(0,8,0), V(0,-60,0), 27, 25); limb(arm, V(0,-60,0), V(0,-170,-6), 25, 36);
  limb(arm, V(0,-150,-6), V(0,-420,-22), 41, 46, CLOTH); const cuff = new THREE.Mesh(new THREE.TorusGeometry(42, 7, 12, 28), CLOTH); cuff.rotation.x = Math.PI/2; cuff.position.set(0,-150,-6); cuff.castShadow = true; arm.add(cuff);
  // vrid handen så att tummen hamnar framför dekalen, pekfingret bakom och armen kommer in från betraktarens högra sida
  const pch = T.clone().sub(I).normalize(), a = V(0,-1,0), q = a.clone().sub(pch.clone().multiplyScalar(a.dot(pch))).normalize(), r = pch.clone().cross(q);
  const P2 = V(0,-1,0), Q2 = V(.95,0,.31).normalize(), R2 = P2.clone().cross(Q2);
  const M = new THREE.Matrix4().makeBasis(P2,Q2,R2).multiply(new THREE.Matrix4().makeBasis(pch,q,r).transpose());
  g.quaternion.setFromRotationMatrix(M);
  const mid = T.clone().add(I).multiplyScalar(.5).applyMatrix4(M);
  g.position.set(40-mid.x, -mid.y, 34-mid.z);                                  // nypet hamnar på svansens nederkant
  return g;
}
const lennart = new THREE.Group(), pose = new THREE.Group(), inner = new THREE.Group(), sticker = new THREE.Group(); {
  const [front, back] = stickerArt(); front.anisotropy = back.anisotropy = 4;
  const geo = new THREE.PlaneGeometry(118, 118, 16, 1); const pa = geo.attributes.position;
  for(let k=0;k<pa.count;k++){ const x = pa.getX(k); pa.setZ(k, -x*x*0.0016); }                 // dekalen böjer sig lite, som ett styvt papper
  geo.computeVertexNormals();
  const mf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:front, alphaTest:.5, roughness:.35, side:THREE.FrontSide}));
  const mb = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map:back, alphaTest:.5, roughness:.9, side:THREE.BackSide}));
  const depth = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:back, alphaTest:.5, side:THREE.DoubleSide});   // skuggan följer dekalens kontur
  mf.castShadow = true; mf.customDepthMaterial = depth; mf.receiveShadow = true;
  sticker.add(mf, mb); sticker.rotation.x = Math.PI/2; sticker.position.set(0,0,64);
  pose.position.set(0,0,12); inner.position.set(0,0,-12); inner.add(sticker, buildHand()); pose.add(inner); lennart.add(pose);   // pose vrids kring fötterna när han böjer sig ner
}
// mjuk skugga på marken under Lennart: gör att han ser ut att stå på gräset och lyfta när han hoppar
const shade = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d"); const g = x.createRadialGradient(64,64,4,64,64,62); g.addColorStop(0,"rgba(0,0,0,.55)"); g.addColorStop(1,"rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(0,0,128,128);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(150,150), new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c), transparent:true, depthWrite:false})); m.renderOrder = 2; m.visible = false; return m; })();
actors.add(shade);
function ground(){ const p = lennart.position; shade.visible = lennart.visible && p.z > -5 && p.y > -172 && Math.abs(p.x) < 112;      // bara över framgården
  const k = 1/(1+Math.max(0,p.z)/40); shade.position.set(p.x, p.y, 2.2); shade.rotation.z = lennart.rotation.z; shade.scale.set(.95*k, .34*k, 1); shade.material.opacity = .85*k; }
'''+s[j:]
R('function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); }); }',
  'function hop(obj, to, dur, h=26, hops=1){ const a = obj.position.toArray(); return tween(dur, t => { obj.position.set(lerp(a[0],to[0],t), lerp(a[1],to[1],t), lerp(a[2],to[2],t) + Math.abs(Math.sin(Math.PI*t*hops))*h); if(obj===lennart) ground(); }); }')
i=s.index('cap("Lennart tar sin nöt"'); j=s.index('lennart.visible = false; screen("idle")',i)
s=s[:i]+r'''cap("Lennart äter ur skålen", "Handen för fram honom och tippar ner huvudet till nöten.", .85);
    // hur mycket han måste luta för att nosen ska nå nöten, och var fötterna då ska stå
    const LIFT = 8, mx = MOUTH[0], mz = MOUTH[2]-12, yaw = lennart.rotation.z; let al = 0;
    while(al > -1.4 && LIFT+12 - mx*Math.sin(al) + mz*Math.cos(al) > SPOT[2]+12) al -= 0.01;
    const fx = mx*Math.cos(al) + mz*Math.sin(al), fy = MOUTH[1];
    const stand = [SPOT[0] - (fx*Math.cos(yaw) - fy*Math.sin(yaw)), SPOT[1] - (fx*Math.sin(yaw) + fy*Math.cos(yaw)), LIFT];
    h = hop(lennart, stand, 550, 18); run(); await h;
    const bow = tween(650, t => { pose.rotation.y = al*t; }); run(); await bow;
    nutsGroup.remove(n); inner.add(n); n.position.set(MOUTH[0]-3, MOUTH[1]-5, MOUTH[2]-7); served++; status();
    const nibble = tween(900, t => { pose.rotation.y = al + Math.sin(t*Math.PI*6)*0.05; }); run(); await nibble;
    cap("Lennart tar med sig nöten", "Luckan stängs långsamt, och bara när kameran inte ser någon rörelse.", .95);
    const rise = tween(600, t => { pose.rotation.y = al*(1-t); }); run(); await rise;
    const close = tween(1100, t => { lid.t = 1-t; }); h = hop(lennart, [LEN_X+10,-170,0], 900, 28, 2); run(); await Promise.all([h, close]);      // han hoppar baklänges hem, utan att vända sig
    h = hop(lennart, [LEN_X+70,-320,10], 800, 34, 2); run(); await h; inner.remove(n);
  }
  shade.visible = false; pose.rotation.y = 0; '''+s[j:]
R('lennart.visible = true; sticker.scale.x = 1; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart);','lennart.visible = true; pose.rotation.y = 0; lennart.position.set(LEN_X+60,-300,10); faceCam(lennart); ground();')
open(p,'w').write(s)
open('local.html','w').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///home/claude/fix/npm/node_modules/three/build/three.min.js'))
