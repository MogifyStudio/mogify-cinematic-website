/* Mogify Studio — hero particle engine (hand-written WebGL, no library).
   Particles are sampled from the ORIGINAL Mogify mark image (assets/brand/mogify-mark-w.png, the dark-background version),
   so the logo you see is the real logo, rebuilt from light. States: logo, sphere, wave, galaxy. */
(function(){
  var cv = document.getElementById('gl'); if (!cv) return;
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var gl = null;
  try { gl = cv.getContext('webgl', {antialias:false, alpha:true, premultipliedAlpha:true, depth:false, stencil:false, powerPreference:'high-performance'}); } catch(e) {}
  if (!gl) { root.classList.add('no-gl'); return; }

  var W = innerWidth, isMob = W < 900;
  var cores = navigator.hardwareConcurrency || 4, mem = navigator.deviceMemory || 4;
  var N = isMob ? 7500 : 15000;
  if (cores <= 4 || mem <= 3) N = Math.round(N * 0.7);
  var DPR = Math.min(window.devicePixelRatio || 1, isMob ? 1.5 : 1.75);

  var VS = [
  'precision highp float;',
  'attribute vec3 aLogo; attribute vec3 aSphere; attribute vec3 aWave; attribute vec3 aGal; attribute vec4 aRnd; attribute float aCol;',
  'uniform float uTime, uIntro, uChaos, uAspect, uPR, uSize, uAlpha, uCam;',
  'uniform vec4 uW; uniform vec3 uLogo; uniform vec3 uShape; uniform vec2 uMouse; uniform float uMouseStr; uniform vec2 uTilt;',
  'varying vec3 vCol; varying float vA;',
  'mat2 rot(float a){ float c=cos(a), s=sin(a); return mat2(c,-s,s,c); }',
  'void main(){',
  '  vec3 lg = aLogo * uLogo.z + vec3(uLogo.xy, 0.0);',
  '  lg.z += sin(uTime*1.3 + aLogo.y*3.0 + aLogo.x*2.0) * 0.025;',
  '  vec3 sp = aSphere; sp.xz = rot(uTime*0.18) * sp.xz; sp.yz = rot(0.35) * sp.yz;',
  '  sp *= 1.0 + 0.06*sin(uTime*1.7 + aRnd.x*12.0);',
  '  sp = sp * uShape.z + vec3(uShape.xy, 0.0);',
  '  vec3 wv = aWave; wv.y += sin(wv.x*1.25 + uTime*0.9)*0.22 + cos(wv.z*1.6 + uTime*0.7)*0.2 + sin((wv.x+wv.z)*2.3 + uTime*1.4)*0.05;',
  '  vec3 gx = aGal; gx.xz = rot(uTime*0.05 + 0.25/(0.4+length(aGal.xz))) * gx.xz;',
  '  vec3 p = lg*uW.x + sp*uW.y + wv*uW.z + gx*uW.w;',
  '  float amp = 0.012 + uChaos*0.9*aRnd.w;',
  '  p += vec3(sin(uTime*0.8 + aRnd.x*6.283), cos(uTime*0.7 + aRnd.y*6.283), sin(uTime*0.6 + aRnd.z*6.283)) * amp;',
  '  float t = clamp(uIntro*1.7 - aRnd.w*0.7, 0.0, 1.0); t = t*t*(3.0-2.0*t);',
  '  vec3 st = aGal * 1.6; st.xz = rot(uTime*0.25) * st.xz;',
  '  p = mix(st, p, t);',
  '  p.xz = rot(uTilt.x) * p.xz; p.yz = rot(uTilt.y) * p.yz;',
  '  float z = uCam - p.z; float f = 2.4142;',
  '  vec4 c = vec4(p.x*f/uAspect, p.y*f, 0.0, z);',
  '  vec2 ndc = c.xy / c.w; vec2 d = ndc - uMouse; d.x *= uAspect; float dl = length(d);',
  '  float push = smoothstep(0.42, 0.0, dl) * uMouseStr;',
  '  if (dl > 0.0001) { ndc += (d/dl) * vec2(1.0/uAspect, 1.0) * push * 0.16; }',
  '  c.xy = ndc * c.w;',
  '  gl_Position = c;',
  '  float sz = uSize * (0.55 + aRnd.z*0.9) * uPR * (f / z);',
  '  gl_PointSize = max(sz * (1.0 + push*1.2), 1.0);',
  '  vec3 teal = vec3(0.0, 0.72, 0.66); vec3 hi = vec3(0.22, 0.92, 0.85); vec3 wh = vec3(0.93, 0.97, 1.0);',
  '  vec3 base = aCol > 0.5 ? wh : mix(teal, hi, aRnd.y*0.6);',
  '  float lw = uW.x;',
  '  vCol = mix(mix(teal, hi, aRnd.x), base, clamp(lw*1.2 + (1.0-t), 0.0, 1.0));',
  '  vCol = mix(vCol, vec3(1.0), push*0.6);',
  '  vA = uAlpha * (0.8 + aRnd.y*0.4) * (0.35 + 0.65*t) * (1.0 + uW.x*0.5);',
  '}'].join('\n');
  var FS = [
  'precision mediump float; varying vec3 vCol; varying float vA;',
  'void main(){ vec2 c = gl_PointCoord - 0.5; float d = length(c); float a = smoothstep(0.5, 0.1, d); a = a*a; gl_FragColor = vec4(vCol*a*vA, a*vA); }'].join('\n');

  function sh(type, src){ var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); } return s; }
  var prog;
  try { prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog); if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error('link'); }
  catch(e) { root.classList.add('no-gl'); return; }
  gl.useProgram(prog);
  var U = {}; ['uTime','uIntro','uChaos','uAspect','uPR','uSize','uAlpha','uCam','uW','uLogo','uShape','uMouse','uMouseStr','uTilt'].forEach(function(n){ U[n] = gl.getUniformLocation(prog, n); });

  function rnd(){ return Math.random(); }
  function buffers(pts){
    var aLogo = new Float32Array(N*3), aSph = new Float32Array(N*3), aWave = new Float32Array(N*3), aGal = new Float32Array(N*3), aRnd = new Float32Array(N*4), aCol = new Float32Array(N);
    var gold = Math.PI * (3 - Math.sqrt(5));
    var cols = Math.ceil(Math.sqrt(N * 1.75)), rows = Math.ceil(N / cols);
    for (var i = 0; i < N; i++) {
      var p = pts[(Math.random() * pts.length) | 0];
      aLogo[i*3] = p[0]; aLogo[i*3+1] = p[1]; aLogo[i*3+2] = (rnd()-0.5)*0.07; aCol[i] = p[2];
      var y = 1 - (i / (N-1)) * 2, r = Math.sqrt(1 - y*y), th = gold * i;
      aSph[i*3] = Math.cos(th)*r; aSph[i*3+1] = y; aSph[i*3+2] = Math.sin(th)*r;
      var cx = i % cols, cy = (i / cols) | 0;
      aWave[i*3] = (cx / (cols-1) - 0.5) * 9.0; aWave[i*3+1] = -1.15; aWave[i*3+2] = (cy / (rows-1)) * -7.0 + 1.6;
      var arm = (i % 3) * 2.094, rr = Math.pow(rnd(), 0.55) * 3.4, ang = rr * 1.9 + arm + (rnd()-0.5)*0.6;
      aGal[i*3] = Math.cos(ang)*rr; aGal[i*3+1] = (rnd()-0.5) * 0.5 * (1.1 - rr/3.4) + (rnd()-0.5)*0.15; aGal[i*3+2] = Math.sin(ang)*rr - 0.5;
      aRnd[i*4] = rnd(); aRnd[i*4+1] = rnd(); aRnd[i*4+2] = rnd(); aRnd[i*4+3] = rnd();
    }
    [['aLogo',aLogo,3],['aSphere',aSph,3],['aWave',aWave,3],['aGal',aGal,3],['aRnd',aRnd,4],['aCol',aCol,1]].forEach(function(a){
      var loc = gl.getAttribLocation(prog, a[0]); if (loc < 0) return;
      var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, a[1], gl.STATIC_DRAW);
      gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, a[2], gl.FLOAT, false, 0, 0);
    });
  }

  // ---- state machine (targets lerped every frame)
  var cur = {w:[0,0,0,1], logo:[0,0,1], shape:[0,0,1], alpha:1, size:1};
  var tgt = {w:[1,0,0,0], logo:[0,0,1], shape:[0,0,1], alpha:1, size:1};
  var chaos = 0, intro = reduce ? 1 : 0, introStart = 0, state = 'logo';
  var aspect = 1, halfH = 1.657, halfW = 1.657, cam = 4;
  function layout(name){
    var mob = innerWidth < 900;
    var L, S = [0,0,1.25], a = 1, size = 1;
    if (name === 'logo') { L = mob ? [0, halfH*0.39, Math.min(0.5, halfW*0.6)] : [halfW*0.56, 0.18, Math.min(0.88, halfW*0.3)]; }
    else if (name === 'logoC') { L = [0, mob ? 0.1 : 0.05, mob ? Math.min(0.6, halfW*0.7) : 1.05]; a = 0.42; }
    else L = [0,0,1];
    if (name === 'sphere') { S = mob ? [0, halfH*0.45, Math.min(0.85, halfW*0.9)] : [halfW*0.55, 0, 1.35]; a = 0.8; }
    if (name === 'wave') a = 0.75;
    if (name === 'galaxy') a = 0.6;
    return {L:L, S:S, a:a};
  }
  var W4 = {logo:[1,0,0,0], logoC:[1,0,0,0], sphere:[0,1,0,0], wave:[0,0,1,0], galaxy:[0,0,0,1]};
  function set(name){
    if (!W4[name]) return;
    if (name !== state) chaos = Math.min(1, chaos + 0.85);
    state = name; var l = layout(name);
    tgt.w = W4[name].slice(); tgt.logo = l.L; tgt.shape = l.S; tgt.alpha = l.a;
  }

  var mouse = [9,9], mStr = 0, mTgt = 0, tilt = [0,0], tiltT = [0,0], lastMove = 0;
  function onMove(x, y){
    mouse[0] = (x / innerWidth) * 2 - 1; mouse[1] = -((y / innerHeight) * 2 - 1);
    mTgt = 1; lastMove = performance.now();
    if (!isMob) { tiltT[0] = mouse[0] * 0.18; tiltT[1] = -mouse[1] * 0.1; }
  }
  addEventListener('pointermove', function(e){ onMove(e.clientX, e.clientY); }, {passive:true});
  addEventListener('touchmove', function(e){ var t = e.touches[0]; if (t) onMove(t.clientX, t.clientY); }, {passive:true});
  addEventListener('touchstart', function(e){ var t = e.touches[0]; if (t) onMove(t.clientX, t.clientY); }, {passive:true});
  addEventListener('deviceorientation', function(e){ if (e.gamma == null) return; tiltT[0] = Math.max(-1, Math.min(1, e.gamma / 35)) * 0.22; tiltT[1] = Math.max(-1, Math.min(1, (e.beta - 45) / 40)) * 0.12; }, {passive:true});

  var cw = 0, ch = 0;
  function resize(force){
    var w = cv.clientWidth, h = cv.clientHeight;
    if (!force && w === cw && Math.abs(h - ch) < 140) return;
    cw = w; ch = h; cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR);
    gl.viewport(0, 0, cv.width, cv.height);
    aspect = w / h; halfW = halfH * aspect;
    var l = layout(state); tgt.logo = l.L; tgt.shape = l.S;
    if (!started) { cur.logo = l.L.slice(); cur.shape = l.S.slice(); }
  }
  addEventListener('resize', function(){ resize(false); });

  var started = false, last = 0, t0 = performance.now(), running = true, visible = true;
  function lerp(a, b, k){ return a + (b - a) * k; }
  function frame(now){
    if (!running) return;
    requestAnimationFrame(frame);
    if (!visible) return;
    var dt = Math.min(0.05, (now - last) / 1000 || 0.016); last = now;
    var t = (now - t0) / 1000;
    if (!reduce) intro = Math.min(1, (now - introStart) / 2600);
    var k = 1 - Math.exp(-dt * 2.6);
    for (var i = 0; i < 4; i++) cur.w[i] = lerp(cur.w[i], tgt.w[i], k);
    for (i = 0; i < 3; i++) { cur.logo[i] = lerp(cur.logo[i], tgt.logo[i], k); cur.shape[i] = lerp(cur.shape[i], tgt.shape[i], k); }
    cur.alpha = lerp(cur.alpha, tgt.alpha, k);
    chaos *= Math.exp(-dt * 1.6);
    if (now - lastMove > 900) mTgt = 0;
    mStr = lerp(mStr, mTgt, 1 - Math.exp(-dt * 6));
    tilt[0] = lerp(tilt[0], tiltT[0], 1 - Math.exp(-dt * 3)); tilt[1] = lerp(tilt[1], tiltT[1], 1 - Math.exp(-dt * 3));
    draw(t);
  }
  function draw(t){
    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform1f(U.uTime, t); gl.uniform1f(U.uIntro, intro); gl.uniform1f(U.uChaos, chaos);
    gl.uniform1f(U.uAspect, aspect); gl.uniform1f(U.uPR, DPR); gl.uniform1f(U.uSize, isMob ? 3.8 : 4.2); gl.uniform1f(U.uAlpha, cur.alpha); gl.uniform1f(U.uCam, cam);
    gl.uniform4fv(U.uW, cur.w); gl.uniform3fv(U.uLogo, cur.logo); gl.uniform3fv(U.uShape, cur.shape);
    gl.uniform2fv(U.uMouse, mouse); gl.uniform1f(U.uMouseStr, mStr); gl.uniform2fv(U.uTilt, tilt);
    gl.drawArrays(gl.POINTS, 0, N);
  }
  document.addEventListener('visibilitychange', function(){ visible = !document.hidden; });

  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE);

  var img = new Image();
  img.onload = function(){
    var c = document.createElement('canvas'), w = img.naturalWidth, h = img.naturalHeight;
    c.width = w; c.height = h; var x = c.getContext('2d'); x.drawImage(img, 0, 0);
    var d; try { d = x.getImageData(0, 0, w, h).data; } catch(e) { root.classList.add('no-gl'); return; }
    var pts = [], s = 2 / h;
    for (var yy = 0; yy < h; yy++) for (var xx = 0; xx < w; xx++) {
      var o = (yy*w + xx) * 4; if (d[o+3] < 140) continue;
      var tealPx = d[o+1] > 100 && d[o] < 110 && d[o+2] < 200;
      pts.push([(xx - w/2 + Math.random() - 0.5) * s, -(yy - h/2 + Math.random() - 0.5) * s, tealPx ? 0 : 1]);
    }
    buffers(pts);
    resize(true); set('logo'); cur.logo = tgt.logo.slice(); chaos = 0;
    started = true; introStart = performance.now(); last = introStart;
    root.classList.add('gl-on');
    if (reduce) { cur.w = [1,0,0,0]; draw(0); running = false; return; }
    requestAnimationFrame(frame);
  };
  img.onerror = function(){ root.classList.add('no-gl'); };
  img.src = '/assets/brand/mogify-mark-w.png';

  window.MGL = { set: function(n){ set(n); if (reduce && started) { cur.w = tgt.w.slice(); cur.logo = tgt.logo.slice(); cur.shape = tgt.shape.slice(); cur.alpha = tgt.alpha; draw(0); } } };
})();
