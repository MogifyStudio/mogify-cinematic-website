/* Mogify Studio — Cinematic site script (smooth scroll, cursor, transitions, kinetic reveals, packages, lightbox). */
(function(){
  var d = document, h = d.documentElement, $ = function(s,c){return (c||d).querySelector(s)}, $$ = function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && matchMedia('(hover:hover) and (pointer:fine)').matches;
  var C = window.MOGIFY || {prices:{}, addons:{}};
  var hasG = !!(window.gsap && window.ScrollTrigger) && !reduce;
  if (hasG) gsap.registerPlugin(ScrollTrigger);

  // ---------- smooth scroll ----------
  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    if (hasG) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(function(t){ lenis.raf(t * 1000); }); gsap.ticker.lagSmoothing(0); }
    else { (function raf(t){ lenis.raf(t); requestAnimationFrame(raf); })(0); }
    $$('a[href^="#"]').forEach(function(a){ a.addEventListener('click', function(e){ var id = a.getAttribute('href'); if (id.length > 1 && $(id)) { e.preventDefault(); lenis.scrollTo(id, {offset: -80}); } }); });
  }

  // ---------- header ----------
  var hd = $('.hd'), lastY = 0;
  function onScroll(){
    var y = window.scrollY || 0;
    if (hd) { hd.classList.toggle('scrolled', y > 10); hd.classList.toggle('hide', y > lastY && y > 400 && !d.body.classList.contains('menu-open')); }
    lastY = y;
  }
  addEventListener('scroll', onScroll, {passive:true}); onScroll();
  var mb = $('.hd-menu');
  function setMenu(open){ d.body.classList.toggle('menu-open', open); if (mb) { mb.setAttribute('aria-expanded', open); mb.querySelector('span').textContent = open ? 'Close' : 'Menu'; } if (lenis) open ? lenis.stop() : lenis.start(); }
  if (mb) mb.addEventListener('click', function(){ setMenu(!d.body.classList.contains('menu-open')); });
  addEventListener('keydown', function(e){ if (e.key === 'Escape') { setMenu(false); closeLb(); } });

  // ---------- page transitions ----------
  var pt = $('.pt');
  if (pt && h.classList.contains('pt-enter')) pt.classList.add('leave');
  function internal(a){
    if (!a || a.target === '_blank' || a.hasAttribute('download')) return false;
    var href = a.getAttribute('href') || '';
    if (!href || href[0] === '#' || /^(mailto|tel|https?:\/\/wa\.me|whatsapp)/i.test(href)) return false;
    var u; try { u = new URL(a.href, location.href); } catch(e) { return false; }
    if (u.origin !== location.origin) return false;
    if (u.pathname === location.pathname && u.hash) return false;
    return u;
  }
  if (!reduce) d.addEventListener('click', function(e){
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a'); var u = internal(a); if (!u) return;
    e.preventDefault();
    try { sessionStorage.setItem('mgf-pt', '1'); } catch(_) {}
    if (pt) pt.classList.remove('leave');
    h.classList.add('pt-in');
    setTimeout(function(){ location.href = u.href; }, 620);
  });
  addEventListener('pageshow', function(e){ if (e.persisted) { h.classList.remove('pt-in'); if (pt) pt.classList.remove('leave'); setMenu(false); } });

  // ---------- custom cursor + magnetic ----------
  if (fine && !reduce) {
    h.classList.add('has-cursor');
    var cur = d.createElement('div'); cur.className = 'cur'; cur.setAttribute('aria-hidden', 'true');
    var dot = d.createElement('div'); dot.className = 'cur-dot'; dot.setAttribute('aria-hidden', 'true');
    d.body.appendChild(cur); d.body.appendChild(dot);
    var mx = -100, my = -100, cx = -100, cy = -100;
    addEventListener('pointermove', function(e){ mx = e.clientX; my = e.clientY; dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)'; }, {passive:true});
    (function loop(){ cx += (mx - cx) * 0.18; cy += (my - cy) * 0.18; cur.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)'; requestAnimationFrame(loop); })();
    d.addEventListener('pointerover', function(e){
      var v = e.target.closest('[data-cursor]'), l = e.target.closest('a,button,summary,label,input,textarea');
      cur.classList.toggle('view', !!v); cur.textContent = v ? v.getAttribute('data-cursor') : '';
      cur.classList.toggle('link', !v && !!l);
    });
    $$('.mag').forEach(function(el){
      el.addEventListener('pointermove', function(e){ var r = el.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top; el.style.transform = 'translate(' + ((x - r.width/2) * 0.28) + 'px,' + ((y - r.height/2) * 0.35) + 'px)'; el.style.setProperty('--mx', x + 'px'); el.style.setProperty('--my', y + 'px'); });
      el.addEventListener('pointerleave', function(){ el.style.transform = ''; });
    });
  }
  $$('.pkc').forEach(function(el){ el.addEventListener('pointermove', function(e){ var r = el.getBoundingClientRect(); el.style.setProperty('--gx', (e.clientX - r.left) + 'px'); el.style.setProperty('--gy', (e.clientY - r.top) + 'px'); }); });

  // ---------- split headings into words ----------
  var wi = 0;
  function splitNode(node){
    $$('*', node); 
    Array.prototype.slice.call(node.childNodes).forEach(function(n){
      if (n.nodeType === 3) {
        var parts = n.textContent.split(/(\s+)/), frag = d.createDocumentFragment();
        parts.forEach(function(p){
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(' ')); return; }
          var w = d.createElement('span'); w.className = 'w'; var s = d.createElement('span'); s.style.setProperty('--i', wi++); s.textContent = p; w.appendChild(s); frag.appendChild(w);
        });
        n.parentNode.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') splitNode(n);
    });
  }
  $$('.split-h').forEach(function(el){ wi = 0; splitNode(el); });

  // ---------- reveal on scroll ----------
  var rv = $$('.rv, .split-h, .rail, .pstep');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, {rootMargin: '0px 0px -10% 0px', threshold: 0.05});
    rv.forEach(function(el){ io.observe(el); });
  } else rv.forEach(function(el){ el.classList.add('in'); });

  // ---------- prices (ONE config object in config.js) ----------
  function priceFor(key, isAddon){
    var v = null;
    if (isAddon) v = (C.addons || {})[key];
    else { var p = key.split('.'); v = ((C.prices || {})[p[0]] || {})[p[1]]; }
    return (v === undefined || v === null || v === '') ? null : String(v);
  }
  $$('[data-price]').forEach(function(el){ var v = priceFor(el.getAttribute('data-price')); if (v) { el.textContent = v; el.classList.add('has-price'); } else el.textContent = el.hasAttribute('data-short') ? 'On request' : (C.noPriceText || 'Price on request'); });
  $$('[data-price-note]').forEach(function(el){ if (C.priceNote) el.textContent = C.priceNote; });
  $$('[data-addon]').forEach(function(el){ var v = priceFor(el.getAttribute('data-addon'), true); el.textContent = v || 'On request'; });
  window.MOGIFY_PRICE = priceFor;
  $$('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });

  // ---------- package switcher ----------
  $$('[data-tabs]').forEach(function(tabs){
    var btns = $$('[role=tab]', tabs);
    function show(id, push){
      btns.forEach(function(b){ var on = b.getAttribute('aria-controls') === id; b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1; var p = d.getElementById(b.getAttribute('aria-controls')); if (p) p.hidden = !on; if (on && b.scrollIntoView && push) { var box = b.parentNode; box.scrollTo({left: b.offsetLeft - box.clientWidth/2 + b.clientWidth/2, behavior: 'smooth'}); } });
      if (push && tabs.hasAttribute('data-hash')) history.replaceState(null, '', '#' + id.replace(/^pk-/, ''));
      if (hasG) ScrollTrigger.refresh();
    }
    btns.forEach(function(b){ b.addEventListener('click', function(){ show(b.getAttribute('aria-controls'), true); }); });
    if (tabs.hasAttribute('data-hash') && location.hash && d.getElementById('pk-' + location.hash.slice(1))) show('pk-' + location.hash.slice(1), false);
  });

  // ---------- work filter + lightbox ----------
  $$('[data-filter-for]').forEach(function(box){
    var gal = d.getElementById(box.getAttribute('data-filter-for'));
    $$('button', box).forEach(function(b){ b.addEventListener('click', function(){
      $$('button', box).forEach(function(x){ x.setAttribute('aria-selected', x === b); });
      var f = b.getAttribute('data-f');
      $$(':scope > *', gal).forEach(function(it){ it.hidden = !(f === 'all' || it.getAttribute('data-cat') === f); });
      if (hasG) ScrollTrigger.refresh();
    }); });
  });
  var lb = $('.lb'), lbItems = [], lbI = 0;
  function openLb(list, i){ if (!lb) return; lbItems = list; lbI = i; renderLb(); lb.hidden = false; if (lenis) lenis.stop(); d.body.style.overflow = 'hidden'; $('.lb-x', lb).focus(); }
  function closeLb(){ if (!lb || lb.hidden) return; lb.hidden = true; $('.lb-media', lb).innerHTML = ''; if (lenis) lenis.start(); d.body.style.overflow = ''; }
  function renderLb(){
    var b = lbItems[lbI], m = $('.lb-media', lb), full = b.getAttribute('data-full');
    m.innerHTML = '';
    if (b.hasAttribute('data-video')) { var v = d.createElement('video'); v.src = full; v.controls = true; v.autoplay = true; v.muted = true; v.loop = true; v.playsInline = true; v.setAttribute('playsinline', ''); m.appendChild(v); }
    else { var im = d.createElement('img'); im.src = full; im.alt = b.querySelector('img') ? b.querySelector('img').alt : ''; m.appendChild(im); }
    $('figcaption', lb).innerHTML = '';
    var t = d.createElement('b'); t.textContent = b.getAttribute('data-title') || ''; var s = d.createElement('small'); s.textContent = b.getAttribute('data-sub') || '';
    $('figcaption', lb).appendChild(t); $('figcaption', lb).appendChild(s);
  }
  if (lb) {
    d.addEventListener('click', function(e){ var b = e.target.closest('[data-lb]'); if (!b) return; var list = $$('[data-lb]').filter(function(x){ return !x.hidden; }); openLb(list, list.indexOf(b)); });
    $('.lb-x', lb).addEventListener('click', closeLb);
    $('.lb-p', lb).addEventListener('click', function(){ lbI = (lbI - 1 + lbItems.length) % lbItems.length; renderLb(); });
    $('.lb-n', lb).addEventListener('click', function(){ lbI = (lbI + 1) % lbItems.length; renderLb(); });
    lb.addEventListener('click', function(e){ if (e.target === lb) closeLb(); });
  }

  // ---------- autoplay muted videos only while visible ----------
  var vids = $$('video[data-auto]');
  if ('IntersectionObserver' in window && vids.length) {
    var vio = new IntersectionObserver(function(es){ es.forEach(function(en){ var v = en.target; if (en.isIntersecting && !reduce) { if (!v.src && v.dataset.src) v.src = v.dataset.src; var p = v.play(); if (p && p.catch) p.catch(function(){}); } else if (!v.paused) v.pause(); }); }, {threshold: 0.2});
    vids.forEach(function(v){ vio.observe(v); });
  }

  // ---------- services: hover preview (desktop) / centre-activate (phone) ----------
  var flo = $('.sv-float'), rows = $$('.svr');
  if (flo && rows.length && fine) {
    var fx = 0, fy = 0, tx = 0, ty = 0, on = false;
    rows.forEach(function(r){
      r.addEventListener('pointerenter', function(){ on = true; flo.classList.add('on'); $$('img', flo).forEach(function(im){ im.classList.toggle('on', im.getAttribute('data-k') === r.getAttribute('data-k')); }); });
      r.addEventListener('pointerleave', function(){ on = false; flo.classList.remove('on'); });
    });
    addEventListener('pointermove', function(e){ tx = e.clientX; ty = e.clientY; }, {passive:true});
    (function fl(){ fx += (tx - fx) * 0.12; fy += (ty - fy) * 0.12; flo.style.transform = 'translate3d(' + fx + 'px,' + fy + 'px,0) scale(' + (on ? 1 : .6) + ') rotate(' + ((tx - fx) * 0.03) + 'deg)'; requestAnimationFrame(fl); })();
  } else if (rows.length && 'IntersectionObserver' in window) {
    var rio = new IntersectionObserver(function(es){ es.forEach(function(en){ en.target.classList.toggle('on', en.isIntersecting); }); }, {rootMargin: '-42% 0px -42% 0px'});
    rows.forEach(function(r){ rio.observe(r); });
  }

  // ---------- WebGL scene states per chapter ----------
  var glSecs = $$('[data-gl]');
  if (glSecs.length && 'IntersectionObserver' in window) {
    var gio = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting && window.MGL) window.MGL.set(en.target.getAttribute('data-gl')); }); }, {rootMargin: '-50% 0px -50% 0px'});
    glSecs.forEach(function(s){ gio.observe(s); });
  }

  // ---------- manifesto: words light up with scroll ----------
  $$('.mani-txt').forEach(function(el){
    var words = [];
    (function walk(node, serif){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if (n.nodeType === 3) { var frag = d.createDocumentFragment(); n.textContent.split(/(\s+)/).forEach(function(p){ if (!p) return; if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(' ')); return; } var s = d.createElement('span'); s.className = 'mw' + (serif ? ' s' : ''); s.textContent = p; words.push(s); frag.appendChild(s); }); n.parentNode.replaceChild(frag, n); }
        else if (n.nodeType === 1) walk(n, serif || n.classList.contains('s'));
      });
    })(el, false);
    if (!hasG) { words.forEach(function(w){ w.style.opacity = 1; }); return; }
    ScrollTrigger.create({ trigger: el, start: 'top 82%', end: 'bottom 45%', scrub: true, onUpdate: function(st){ var n = st.progress * words.length * 1.05; words.forEach(function(w, i){ w.style.opacity = Math.max(0.14, Math.min(1, n - i + 0.6)); }); } });
  });

  // ---------- marquee driven by scroll velocity ----------
  var mrows = $$('.marq-row');
  if (mrows.length && !reduce) {
    var xs = mrows.map(function(){ return 0; }), vel = 0, py = scrollY;
    (function mq(){
      var y = scrollY; vel += ((y - py) - vel) * 0.1; py = y;
      mrows.forEach(function(r, i){
        var half = r.scrollWidth / 2, dir = i % 2 ? 1 : -1;
        xs[i] += dir * (0.6 + Math.abs(vel) * 0.35);
        if (xs[i] <= -half) xs[i] += half; if (xs[i] > 0) xs[i] -= half;
        r.style.transform = 'translate3d(' + xs[i] + 'px,0,0)';
      });
      requestAnimationFrame(mq);
    })();
  }

  // ---------- horizontal work reel ----------
  var reel = $('.reel'), track = reel && $('.reel-track', reel), bar = reel && $('.reel-bar i', reel);
  if (reel && track) {
    if (hasG) {
      var dist = function(){ return Math.max(0, track.scrollWidth - innerWidth); };
      gsap.to(track, { x: function(){ return -dist(); }, ease: 'none', scrollTrigger: { trigger: reel, pin: true, start: 'top top', end: function(){ return '+=' + dist(); }, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1, onUpdate: function(st){ if (bar) bar.style.transform = 'scaleX(' + st.progress + ')'; } } });
      $$('.rc img, .rc video', track).forEach(function(m){ gsap.fromTo(m, {scale: 1.18}, {scale: 1, ease: 'none', scrollTrigger: { trigger: reel, start: 'top top', end: function(){ return '+=' + dist(); }, scrub: true }}); });
    } else h.classList.add('no-pin');
  }

  // ---------- hero exit parallax ----------
  var hero = $('.hero');
  if (hero && hasG) {
    gsap.to('.hero-inner', { yPercent: -18, opacity: 0, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
  }
  if (hasG) $$('[data-par]').forEach(function(el){ gsap.fromTo(el, {yPercent: parseFloat(el.dataset.par)}, {yPercent: -parseFloat(el.dataset.par), ease: 'none', scrollTrigger: {trigger: el, start: 'top bottom', end: 'bottom top', scrub: true}}); });

  // ---------- go ----------
  h.classList.add('ready');
  addEventListener('load', function(){ if (hasG) ScrollTrigger.refresh(); });
})();
