#!/usr/bin/env python3
"""Mogify Studio — CINEMATIC business site (v2). Builds ./site.
DOMAIN SWAP: change BASE_URL below, run `python3 build.py`, republish.
PRICES: edit site/assets/js/config.js (ONE object, no rebuild needed).
WORDS: content.py (services, packages, add-ons, FAQ) — shared with v1."""
import os, json, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
# reuse v1 helpers (content, icons, JSON-LD builders, contact/legal/planner page bodies)
_src = open(os.path.join(HERE, "v1_parts.py"), encoding="utf-8").read()
exec(compile(_src, "v1_parts.py", "exec"))
BASE_URL = "https://mogify-cinematic.sites.tab.bot"   # <-- the ONE domain variable (no trailing slash)
ORG_ID = BASE_URL + "/#org"
SITE = os.path.join(HERE, "site")
LASTMOD = "2026-10-31"
PAGES.clear()
e = html.escape

NAV = [("Services", "/services"), ("Packages", "/packages"), ("Work", "/work"), ("Planner", "/planner"), ("About", "/about"), ("Contact", "/contact")]
SVC_IMG = {"web": "/assets/img/web/kora-skincare.webp", "logo": "/assets/img/work/logo-veinus-25.webp", "brand": "/assets/img/work/brand-sho-es-game-on-5.webp",
           "uiux": "/assets/img/product/fluxa-home.webp", "motion": "/assets/video/motion-promo.webp", "anim3d": "/assets/video/cloth-reveal.webp",
           "social": "/assets/img/work/social-fermentation-found-fire-12.webp", "book": "/assets/img/work/book-z-steals-the-spotlight-45.webp", "video": "/assets/video/idea-to-life.webp"}

def header(active=None):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == active else ""}>{n}</a>' for n, h in NAV)
    mnav = "".join(f'<a href="{h}"><small>0{i+1}</small><span>{n}</span></a>' for i, (n, h) in enumerate([("Home", "/")] + NAV))
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="hd"><a class="hd-logo" href="/" aria-label="Mogify Studio home"><img src="/assets/brand/mogify-logo-white.png" alt="Mogify Studio" width="592" height="187"></a>
<nav class="hd-nav" aria-label="Main">{nav}</nav>
<a class="btn btn-glow btn-sm hd-cta mag" href="/planner">Start a project {ARR}</a>
<button class="hd-menu" type="button" aria-expanded="false" aria-controls="menu"><span>Menu</span><i aria-hidden="true"></i></button>
</header>
<div class="menu" id="menu"><nav aria-label="Menu">{mnav}</nav>
<div class="menu-foot"><a class="btn btn-glow" href="/planner">Start your project {ARR}</a><a class="btn btn-wa" href="{wa('Hi Mogify Studio! I want to start a project.')}" target="_blank" rel="noopener">{bi('wa')} WhatsApp</a></div></div>"""

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}">{e(s["short"])}</a></li>' for s in SERVICES)
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{bi(k)}</a>' for k, n, u, h_ in SOCIALS)
    return f"""<footer class="ft"><div class="wrap">
<div class="ft-grid">
 <div class="ft-brand"><img src="/assets/brand/mogify-logo-white.png" alt="Mogify Studio" width="592" height="187" loading="lazy"><p>Creative and digital studio in Karachi, Pakistan. Websites, brand identity, UI/UX, motion and 3D for businesses in Pakistan and worldwide.</p><div class="socials">{soc}</div></div>
 <div><h4>Services</h4><ul>{svc}</ul></div>
 <div><h4>Studio</h4><ul><li><a href="/packages">Packages</a></li><li><a href="/planner">Project Planner</a></li><li><a href="/work">Work</a></li><li><a href="/about">About</a></li><li><a href="/faq">FAQ</a></li><li><a href="/contact">Contact</a></li></ul></div>
 <div><h4>Talk to us</h4><ul><li><a href="{wa('Hi Mogify Studio! I want to start a project.')}" target="_blank" rel="noopener">WhatsApp +92 323 2194013</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="/contact#call">Book a quick call</a></li></ul></div>
</div>
<div class="ft-big" aria-hidden="true">Mogify Studio</div>
<div class="ft-bot"><span>© <span data-year>2026</span> Mogify Studio · Karachi, Pakistan</span><span><a href="/privacy">Privacy</a> · <a href="/terms">Terms</a></span></div>
</div></footer>"""

def page(path, title, desc, body, ld=None, active=None, body_class="", scripts=(), priority=0.7, og_image="/og.png", noindex=False, gl=False):
    graph = [org_ld(), {"@type": "WebPage", "@id": url(path) + "#page", "url": url(path), "name": title, "description": desc, "isPartOf": {"@type": "WebSite", "@id": BASE_URL + "/#site", "url": BASE_URL + "/", "name": "Mogify Studio", "publisher": {"@id": ORG_ID}}, "inLanguage": "en"}] + (ld or [])
    ldj = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    sc = "".join(f'<script src="{s}" defer></script>' for s in scripts)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    glc = '<canvas id="gl" aria-hidden="true"></canvas>' if gl else ""
    doc = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="Mogify Studio">
<meta name="theme-color" content="#06090F">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{url(path)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Mogify Studio"><meta property="og:locale" content="en_US">
<meta property="og:url" content="{url(path)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{url(og_image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Mogify Studio, web design, branding and motion studio in Karachi">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@mogifystudio"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{url(og_image)}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/cine.css?v=__V__">
<script src="/assets/js/boot.js?v=__V__"></script>
<script type="application/ld+json">{ldj}</script>
</head>
<body class="{body_class}">
<div class="ambient" aria-hidden="true"></div>{glc}
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<div class="grain" aria-hidden="true"></div>
<div class="pt" aria-hidden="true"><i></i><b></b><img src="/assets/brand/mogify-mark-w.png" alt="" width="148" height="172"></div>
<script src="/assets/js/config.js?v=__V__"></script>
<script src="/assets/vendor/vendor.js?v=__V__" defer></script>
{'<script src="/assets/js/gl.js?v=__V__" defer></script>' if gl else ''}
<script src="/assets/js/cine.js?v=__V__" defer></script>{sc}
</body>
</html>
"""
    out = os.path.join(SITE, "index.html" if path == "/" else path.strip("/") + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    if not noindex: PAGES.append((path, priority))

def crumbs(items):
    out = []
    for i, (n, p) in enumerate(items):
        out.append(f'<a href="{p}">{e(n)}</a>' if i < len(items) - 1 else f'<span aria-current="page">{e(n)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(out) + '</nav>'

def phero(eyebrow, h1, lead, items, ctas="", extra="", h1_ur=None, lead_ur=None, side="", num=""):
    return f"""<section class="ph"><div class="wrap">{crumbs(items)}<span class="eyebrow">{eyebrow}</span>
<h1 class="h-xl split-h">{h1}</h1><p class="lead rv">{lead}</p>{f'<div class="hero-ctas rv" style="margin-top:30px">{ctas}</div>' if ctas else ''}{extra}</div>{f'<div class="ph-num" aria-hidden="true">{num}</div>' if num else ''}</section>"""

def sec_head(eyebrow, h, p="", center=False, tag="h2", hid=None):
    plead = ('<p class="lead rv">' + p + '</p>') if p else ""
    return f'<div class="sec-h"><span class="eyebrow">{eyebrow}</span><{tag} class="h-m split-h"{(" id=%s" % chr(34)+hid+chr(34)) if hid else ""}>{h}</{tag}>{plead}</div>'

def cta_band(h="Your project could be <em class='s teal'>next.</em>", p="Tell us what you need in about two minutes with the Project Planner, or just say hi on WhatsApp. Moiz, the founder, replies personally.", wa_text="Hi Mogify Studio! I want to start a project."):
    h = h.replace("class='s'", "class='s teal'").replace('class="s"', 'class="s teal"')
    return f"""<section class="cta2"><div class="wrap"><span class="eyebrow">Let's work together</span><h2 class="h-l split-h">{h}</h2><p class="rv">{p}</p>
<div class="hero-ctas rv"><a class="btn btn-glow btn-lg mag" href="/planner">Start your project {ARR}</a><a class="btn btn-line btn-lg" href="{wa(wa_text)}" target="_blank" rel="noopener">{bi('wa')} Chat on WhatsApp</a></div></div></section>"""

def faq_block(faqs, open_first=False):
    return '<div class="faq">' + "".join(f'<details class="rv"{" open" if (open_first and i == 0) else ""}><summary>{e(q)}<i aria-hidden="true"></i></summary><div class="a">{a}</div></details>' for i, (q, a) in enumerate(faqs)) + '</div>'

def EM(t): return '<em class="s teal">' + t + '</em>'
TN = {"starter": "Starter", "growth": "Growth", "premium": "Premium"}
def pk_cards(s):
    out = []
    for idx, (tid, tname, tfor) in enumerate(s["tiers"]):
        feats = []
        for row in s["compare"]:
            v = row[1 + idx]
            if v is False: continue
            feats.append(f'<li>{ic("check")}<span>{e(row[0])}{": <b>" + e(str(v)) + "</b>" if v is not True else ""}</span></li>')
        rec = tid == RECOMMENDED
        msg = f"Hi Mogify Studio! I'm interested in the {s['name']} {tname} package. Can you share a quote?"
        steps = "".join(f"<li>{e(x)}</li>" for x in TIER_STEPS[tid])
        out.append(f"""<article class="pkc{' rec' if rec else ''} rv d{idx}">
<div><div class="top"><span class="tn">{tname}</span>{'<span class="rt">Recommended</span>' if rec else ''}</div><h3>{e(s['short'])} {tname}</h3><p class="for">{e(tfor)}</p></div>
<div class="pr"><span class="pv" data-price="{s['id']}.{tid}">Price on request</span><span class="pn" data-price-note>Fixed quote after a quick brief</span></div>
<ul>{''.join(feats)}</ul>
<div class="acts"><a class="btn {'btn-glow' if rec else 'btn-line'} btn-block" href="{wa(msg)}" target="_blank" rel="noopener" data-pkg="{e(s['name'])} {tname}">{bi('wa')} Get a quote</a><a class="btn btn-line btn-block btn-sm" href="/planner?service={s['id']}&amp;tier={tid}">Plan this in detail {ARR}</a></div>
<details><summary>How it's delivered</summary><ol>{steps}</ol></details>
</article>""")
    return '<div class="pk">' + "".join(out) + '</div>'

def cmp_block(s):
    return f'<details class="cmp-wrap rv"><summary>Compare {e(s["short"])} packages side by side</summary>{compare_table(s)}</details>'

def gal_items(items):
    out = []
    for w in items:
        cap = f'<span class="cap"><b>{e(w["title"])}</b>{e(w["sub"])}</span>'
        tag = '<span class="tag c">Concept</span>' if w.get("concept") else ""
        img = f'<img src="{w["img"]}" alt="{e(w["alt"])}" loading="lazy" decoding="async" width="{w["w"]}" height="{w["h"]}">'
        cat = w["cat"]
        if w.get("href"):
            ext = w["href"].startswith("http")
            out.append(f'<a href="{w["href"]}" data-cat="{cat}" data-cursor="Open"{" target=_blank rel=noopener" if ext else ""} aria-label="{e(w["title"])}">{tag}{img}{cap}</a>')
        else:
            out.append(f'<button type="button" data-cat="{cat}" data-lb data-cursor="View" data-full="{w["full"]}" data-title="{e(w["title"])}" data-sub="{e(w["sub"])}"{" data-video" if w.get("video") else ""} aria-label="Open {e(w["title"])}">{tag}{img}{cap}{"<span class=play></span>" if w.get("video") else ""}</button>')
    return "".join(out)

LB = f'<div class="lb" role="dialog" aria-modal="true" aria-label="Work viewer" hidden><button class="lb-x" type="button" aria-label="Close">{ic("x")}</button><button class="lb-p" type="button" aria-label="Previous">{ic("left")}</button><button class="lb-n" type="button" aria-label="Next">{ic("right")}</button><figure><div class="lb-media"></div><figcaption></figcaption></figure></div>'

def WK(title): return next(w for w in WORK if w["title"] == title)

# ============================== HOME ==============================
def build_home():
    reel_items = [WK("Kora"), WK("Idea to Life"), WK("The Notceb Financial Group"), WK("Aurelle Coffee Roasters"), WK("Logo Reveal"), WK("Sho'es — Game On"), WK("Halo Audio"), WK("Details Make the Difference"), WK("Pizza Cat"), WK("Nimbus AI"), WK("Fermentation Found Fire"), WK("Z Steals the Spotlight")]
    cards = []
    for w in reel_items:
        wide = w["cat"] == "web"
        tag = '<span class="tag c">Concept</span>' if w.get("concept") else f'<span class="tag">{ {"web":"Website","brand":"Brand identity","logo":"Logo","motion":"Motion","social":"Social ad","book":"Book cover"}.get(w["cat"], "Work") }</span>'
        if w.get("video"):
            media = f'<video data-auto muted loop playsinline preload="none" poster="{w["img"]}" data-src="{w["full"]}" aria-label="{e(w["alt"])}"></video>'
            inner = f'{tag}{media}<figcaption><b>{e(w["title"])}</b><span>{e(w["sub"])}</span></figcaption>'
            cards.append(f'<figure class="rc"><button type="button" data-lb data-video data-cursor="Play" data-full="{w["full"]}" data-title="{e(w["title"])}" data-sub="{e(w["sub"])}" aria-label="Play {e(w["title"])}" style="position:absolute;inset:0;z-index:3"></button>{inner}</figure>')
        else:
            media = f'<img src="{w["img"]}" alt="{e(w["alt"])}" loading="lazy" decoding="async" width="{w["w"]}" height="{w["h"]}">'
            inner = f'{tag}{media}<figcaption><b>{e(w["title"])}</b><span>{e(w["sub"])}</span></figcaption>'
            if w.get("href"):
                cards.append(f'<a class="rc{" wide" if wide else ""}" href="{w["href"]}" data-cursor="Open"{" target=_blank rel=noopener" if w["href"].startswith("http") else ""}>{inner}</a>')
            else:
                cards.append(f'<figure class="rc"><button type="button" data-lb data-cursor="View" data-full="{w["full"]}" data-title="{e(w["title"])}" data-sub="{e(w["sub"])}" aria-label="Open {e(w["title"])}" style="position:absolute;inset:0;z-index:3"></button>{inner}</figure>')
    svrows = "".join(f'<a class="svr" href="/services/{s["slug"]}" data-k="{s["id"]}"><span class="n">{i+1:02d}</span><span class="nm">{e(s["short"])}</span><span class="go">{ARR}</span><span class="ds">{e(s["card"])}</span><span class="pv"><img src="{SVC_IMG[s["id"]]}" alt="" loading="lazy" decoding="async"></span></a>' for i, s in enumerate(SERVICES))
    flo = "".join(f'<img src="{SVC_IMG[s["id"]]}" alt="" data-k="{s["id"]}" loading="lazy" decoding="async">' for s in SERVICES)
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="hp-{s["id"]}" tabindex="{0 if i == 0 else -1}">{ic(s["id"])}{e(s["short"])}</button>' for i, s in enumerate(SERVICES))
    panels = "".join(f'<div class="pk-panel" id="hp-{s["id"]}" role="tabpanel"{"" if i == 0 else " hidden"}>{pk_cards(s)}</div>' for i, s in enumerate(SERVICES))
    words = ["Websites", "Brand identity", "Logos", "UI/UX", "Motion", "3D", "Social & ads", "Book covers", "Video"]
    row = "".join(f'<span class="{["f", "", "t"][i % 3]}">{w}</span>' for i, w in enumerate(words))
    body = f"""
<section class="hero k-in" data-gl="logo" aria-labelledby="hero-t">
 <img class="hero-fallback" src="/assets/brand/mogify-mark-w.png" alt="" width="148" height="172">
 <div class="hero-top wrap" aria-hidden="true"><span>Creative &amp; digital studio</span><span>Karachi · Worldwide</span></div>
 <div class="wrap hero-inner">
  <div class="hero-hint fade-up" style="--d:.6" aria-hidden="true">Touch the logo</div>
  <h1 class="hero-h" id="hero-t"><span class="ln"><span style="--i:0">Make your</span></span><span class="ln"><span style="--i:1">brand</span></span><span class="ln"><span style="--i:2">impossible</span></span><span class="ln"><span style="--i:3"><em class="s">to scroll past.</em></span></span></h1>
  <div class="hero-row">
   <p class="hero-sub fade-up" style="--d:.1"><b>Mogify Studio</b> designs websites, brand identities, motion and 3D for businesses in Pakistan and worldwide. Hand-made in Karachi.</p>
   <div class="hero-ctas fade-up" style="--d:.25"><a class="btn btn-glow btn-lg mag" href="/planner">Start your project {ARR}</a><a class="btn btn-line btn-lg" href="#work">See the work</a></div>
  </div>
  <div class="scroll-cue fade-up" style="--d:.4" aria-hidden="true"><i></i>Scroll to begin</div>
 </div>
</section>

<section class="chap" data-gl="wave" aria-labelledby="mani-t">
 <div class="wrap">
  <div class="chap-label"><span><b>01</b> — The idea</span><span>Why Mogify</span></div>
  <h2 class="sr-only" id="mani-t">Why Mogify</h2>
  <p class="mani-txt">Most brands blend in. Same templates, same stock photos, same forgettable feed. We do the opposite: every logo, website and frame is made from scratch around <span class="s">one idea, yours.</span></p>
  <div class="mani-foot">
   <div class="pillar rv"><b>A</b><h3>You talk to the founder</h3><p>Muhammad Moiz Ali works with you directly, from the first message to the final files. No account managers in between.</p></div>
   <div class="pillar rv d1"><b>B</b><h3>Hand-made, never templated</h3><p>Websites are hand-coded, fast and mobile-first. Logos, identities, motion and 3D are designed in-house for your brand only.</p></div>
   <div class="pillar rv d2"><b>C</b><h3>A fixed quote, before anything starts</h3><p>Clear packages, a written quote and agreed checkpoints, so you always know what happens next.</p></div>
  </div>
 </div>
</section>

<div class="marq" aria-hidden="true"><div class="marq-row">{row}{row}</div><div class="marq-row">{row}{row}</div></div>

<section class="chap" id="services" data-gl="sphere" aria-labelledby="sv-t">
 <div class="wrap">
  <div class="chap-label"><span><b>02</b> — Services</span><span>Nine crafts, one studio</span></div>
  <h2 class="h-l split-h" id="sv-t" style="margin-bottom:clamp(30px,5vw,70px);max-width:12ch">Everything your brand needs to <em class="s teal">stand out.</em></h2>
  <div class="svl">{svrows}</div>
 </div>
 <div class="sv-float" aria-hidden="true">{flo}</div>
</section>

<section class="reel" id="work" data-gl="galaxy" aria-labelledby="wk-t">
 <div class="reel-track">
  <div class="reel-intro"><div class="chap-label" style="margin-bottom:0;border:0"><span><b>03</b> — Selected work</span></div><h2 class="h-l split-h" id="wk-t">Work that <em class="s teal">moves.</em></h2><p class="lead rv">Websites, identities, logos, motion and 3D from the Mogify studio. Keep scrolling; the reel moves sideways.</p></div>
  {''.join(cards)}
  <div class="reel-end"><h3 class="h-m">See every project.</h3><p class="muted">Logos, brand systems, social ads, book covers, apps and films.</p><a class="btn btn-glow mag" href="/work">Open the full gallery {ARR}</a></div>
 </div>
 <div class="reel-bar" aria-hidden="true"><i></i></div>
</section>

<section class="chap" data-gl="wave" aria-labelledby="pr-t">
 <div class="wrap">
  <div class="chap-label"><span><b>04</b> — Process</span><span>From first message to final files</span></div>
  <h2 class="h-l split-h" id="pr-t" style="margin-bottom:clamp(30px,5vw,70px);max-width:13ch">Simple process. <em class="s teal">No surprises.</em></h2>
  <ol class="proc">
   <li class="pstep"><span class="num">01</span><h3>Brief</h3><p>Tell us what you need in the two-minute Project Planner or on WhatsApp: goals, style, timeline and budget range.</p></li>
   <li class="pstep"><span class="num">02</span><h3>Fixed quote</h3><p>Moiz replies with a clear scope, a fixed price and a timeline in writing, before any work starts.</p></li>
   <li class="pstep"><span class="num">03</span><h3>Design &amp; build</h3><p>You review the work at agreed checkpoints. Revision rounds are included in every package.</p></li>
   <li class="pstep"><span class="num">04</span><h3>Launch &amp; handover</h3><p>Final files, a live website or ready-to-post videos, handed over with everything you need to use them.</p></li>
  </ol>
 </div>
</section>

<section class="chap" id="packages" data-gl="galaxy" aria-labelledby="pk-t">
 <div class="wrap">
  <div class="chap-label"><span><b>05</b> — Packages</span><span>Starter · Growth · Premium</span></div>
  <h2 class="h-l split-h" id="pk-t" style="max-width:13ch">Pick a package. <em class="s teal">Or build your own.</em></h2>
  <p class="lead rv" style="margin:22px 0 34px">Three clear packages for every service. Each one lists exactly what you get, and every quote is fixed before work starts.</p>
  <div class="svtabs" role="tablist" aria-label="Choose a service" data-tabs>{tabs}</div>
  {panels}
  <p class="rv" style="margin-top:26px"><a class="btn btn-line" href="/packages">All packages, comparisons and add-ons {ARR}</a></p>
 </div>
</section>

<section class="chap" data-gl="wave" aria-labelledby="pl-t">
 <div class="wrap"><div class="pl-cta">
  <span class="eyebrow">06 — Project Planner</span>
  <h2 class="h-l split-h" id="pl-t">Plan your project in <em class="s teal">two minutes.</em></h2>
  <p class="lead rv">Tap through seven quick steps. Your brief and project scope build live as you go, then one tap sends everything to Moiz on WhatsApp or email.</p>
  <div class="rail" aria-hidden="true"><span>Services</span><span>Details</span><span>Goals</span><span>Style</span><span>Timeline</span><span>Budget</span><span>Send</span></div>
  <div class="hero-ctas rv"><a class="btn btn-glow btn-lg mag" href="/planner">Open the Project Planner {ARR}</a><a class="btn btn-line btn-lg" href="{wa('Hi Mogify Studio! I want to start a project.')}" target="_blank" rel="noopener">{bi('wa')} Or just say hi</a></div>
 </div></div>
</section>

<section class="chap" data-gl="galaxy" aria-labelledby="fq-t" style="padding-top:0">
 <div class="wrap-n">
  <div class="chap-label"><span><b>07</b> — Questions</span><span>Straight answers</span></div>
  <h2 class="h-m split-h" id="fq-t" style="margin-bottom:30px">Good to know.</h2>
  {faq_block(HOME_FAQS, open_first=True)}
 </div>
</section>

<section class="final" data-gl="logoC" aria-labelledby="fin-t">
 <div class="wrap">
  <span class="eyebrow">Your turn</span>
  <h2 class="h-xl split-h" id="fin-t">Your brand could be <em class="s teal">next.</em></h2>
  <p class="rv">Tell us about your business. Moiz, the founder, replies personally with a clear plan and a fixed quote.</p>
  <div class="hero-ctas rv"><a class="btn btn-glow btn-lg mag" href="/planner">Start your project {ARR}</a><a class="btn btn-wa btn-lg" href="{wa('Hi Moiz! I saw the Mogify Studio website and want to talk about a project.')}" target="_blank" rel="noopener">{bi('wa')} WhatsApp Moiz</a></div>
 </div>
</section>
{LB}"""
    ld = [faq_ld(HOME_FAQS), {"@type": "WebSite", "@id": BASE_URL + "/#site", "url": BASE_URL + "/", "name": "Mogify Studio", "publisher": {"@id": ORG_ID}}]
    page("/", "Mogify Studio | Web Design, Branding, Motion & 3D Studio in Karachi", "Mogify Studio is a creative and digital studio in Karachi, Pakistan. Websites, brand identity, logos, UI/UX, motion graphics and 3D animation for businesses in Pakistan and worldwide.", body, ld=ld, active="/", body_class="home", priority=1.0, gl=True)

# ============================== SERVICES ==============================
def build_services():
    items = [("Home", "/"), ("Services", "/services")]
    cards = "".join(f'<a class="svc-card rv d{i % 3}" href="/services/{s["slug"]}" data-cursor="Explore"><span class="im"><img src="{SVC_IMG[s["id"]]}" alt="" loading="lazy" decoding="async"></span><span class="n">{i+1:02d}</span><span class="bd"><h3>{e(s["name"])}</h3><p>{e(s["card"])}</p><span class="more">Explore {ARR}</span></span></a>' for i, s in enumerate(SERVICES))
    body = phero("Services", "Nine crafts. <em class='s teal'>One studio.</em>", "Websites, brand identity, logos, UI/UX, motion, 3D, social creatives, book covers and video. Pick one, or combine them into one package.", items, ctas=f'<a class="btn btn-glow btn-lg mag" href="/planner">Plan your project {ARR}</a><a class="btn btn-line btn-lg" href="/packages">See packages</a>', num="09")
    body += f'<section class="sec" style="padding-top:0"><div class="wrap"><div class="svc-grid">{cards}</div></div></section>' + cta_band()
    ld = [crumbs_ld(items), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i+1, "url": url("/services/" + s["slug"]), "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    page("/services", "Services | Web Design, Branding, Logo, Motion & 3D | Mogify Studio Karachi", "Explore Mogify Studio services: web design and development, logo design, brand identity, UI/UX, motion graphics, 3D animation, social media creatives, book covers and video editing.", body, ld=ld, active="/services", priority=0.9)

def build_service(s):
    i = SERVICES.index(s)
    items = [("Home", "/"), ("Services", "/services"), (s["name"], "/services/" + s["slug"])]
    ctas = f'<a class="btn btn-glow btn-lg mag" href="/planner?service={s["id"]}">Plan your {e(s["noun"])} {ARR}</a><a class="btn btn-line btn-lg" href="#packages">See packages</a>'
    body = phero(f"Service {i+1:02d} / 09", e(s["title"]), e(s["intro"]), items, ctas=ctas, num=f"{i+1:02d}")
    dl = "".join(f'<div class="dcard rv d{j % 3}"><b>{j+1:02d}</b><h3>{e(a)}</h3><p>{e(b_)}</p></div>' for j, (a, b_) in enumerate(s["deliverables"]))
    body += f'<section class="sec" style="padding-top:0"><div class="wrap">{sec_head("What you get", e(s["tagline"]))}<div class="grid-d">{dl}</div></div></section>'
    body += f'<section class="sec" style="padding-top:0"><div class="wrap">{sec_head("Ideal for", "Made for businesses " + EM("like yours.") + "")}<div class="ideal rv">{"".join(f"<span>{e(x)}</span>" for x in s["ideal"])}</div></div></section>'
    pr = "".join(f'<li class="pstep"><span class="num">{j+1:02d}</span><h3>{e(a)}</h3><p>{e(b_)}</p></li>' for j, (a, b_) in enumerate(s["process"]))
    body += f'<section class="sec" style="padding-top:0"><div class="wrap">{sec_head("How it works", "From brief to " + EM("final files.") + "")}<ol class="proc">{pr}</ol></div></section>'
    body += f'<section class="sec" id="packages" style="padding-top:0"><div class="wrap">{sec_head("Packages", e(s["short"]) + " packages", "Every package has a fixed quote before work starts. Prices are confirmed after a quick brief.")}{pk_cards(s)}{cmp_block(s)}</div></section>'
    wk = work_for(s)
    if wk:
        body += f'<section class="sec" style="padding-top:0"><div class="wrap">{sec_head("Related work", "From the " + EM("studio.") + "")}<div class="gal">{gal_items(wk)}</div></div></section>' + LB
    body += f'<section class="sec" style="padding-top:0"><div class="wrap-n">{sec_head("Questions", "Good to know.")}{faq_block(s["faqs"])}</div></section>'
    body += cta_band(h=f"Ready for your <em class='s teal'>{e(s['noun'])}?</em>", wa_text=f"Hi Mogify Studio! I'm interested in {s['name']}.")
    ld = [crumbs_ld(items), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["intro"], "provider": {"@id": ORG_ID}, "areaServed": ["Karachi", "Pakistan", "Worldwide"], "url": url("/services/" + s["slug"]),
          "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["name"] + " packages", "itemListElement": [{"@type": "Offer", "name": f"{s['name']} {tn}", "description": tf} for _, tn, tf in s["tiers"]]}}, faq_ld(s["faqs"])]
    page("/services/" + s["slug"], f"{s['title']} | Mogify Studio Karachi", (s["intro"][:150].rsplit(" ", 1)[0] + "…") if len(s["intro"]) > 155 else s["intro"], body, ld=ld, active="/services", priority=0.8)

# ============================== PACKAGES ==============================
def build_packages():
    items = [("Home", "/"), ("Packages", "/packages")]
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="pk-{s["id"]}" tabindex="{0 if i == 0 else -1}">{ic(s["id"])}{e(s["short"])}</button>' for i, s in enumerate(SERVICES))
    panels = "".join(f'<div class="pk-panel" id="pk-{s["id"]}" role="tabpanel"{"" if i == 0 else " hidden"}><h2 class="h-m" style="margin-top:30px">{e(s["name"])}</h2><p class="muted" style="margin-top:8px;max-width:640px">{e(s["card"])} <a href="/services/{s["slug"]}" style="color:var(--teal-hi)">About this service →</a></p>{pk_cards(s)}{cmp_block(s)}</div>' for i, s in enumerate(SERVICES))
    ad = "".join(f'<div class="addon rv"><b>{e(n)}</b><p>{e(dsc)}</p><div class="ap"><span data-addon="{aid}">On request</span><a href="{wa("Hi Mogify Studio! Can you share a quote for the add-on: " + n + "?")}" target="_blank" rel="noopener">Ask on WhatsApp</a></div></div>' for aid, n, dsc in ADDONS)
    body = phero("Packages", "Clear packages. <em class='s teal'>Fixed quotes.</em>", "Three packages for every service, Starter, Growth and Premium, each listing exactly what you get. Tap Get a quote and WhatsApp opens with the package already named.", items, num="03")
    body += f'<section class="sec" style="padding-top:0"><div class="wrap"><div class="svtabs" role="tablist" aria-label="Choose a service" data-tabs data-hash>{tabs}</div>{panels}</div></section>'
    body += f'<section class="sec" style="padding-top:0"><div class="wrap">{sec_head("Add-ons", "Add exactly " + EM("what you need.") + "", "Extras you can add to any package. Ask for a quote on WhatsApp.")}<div class="addons">{ad}</div></div></section>'
    body += cta_band(h="Need a mix? Build a <em class='s teal'>custom package.</em>", p="Pick every service you need in the Project Planner, for example a logo, a website and a launch reel, and we will put together one package with one fixed quote.")
    offers = []
    for s in SERVICES:
        for _, tn, tf in s["tiers"]: offers.append({"@type": "Offer", "name": f"{s['name']} {tn}", "description": tf, "url": url("/packages") + "#" + s["id"], "seller": {"@id": ORG_ID}})
    page("/packages", "Packages & Pricing | Website, Logo & Branding Packages | Mogify Studio", "Compare Starter, Growth and Premium packages for websites, logos, branding, UI/UX, motion, 3D, social creatives, book covers and video. Get a fixed quote on WhatsApp.", body, ld=[crumbs_ld(items), {"@type": "OfferCatalog", "name": "Mogify Studio packages", "itemListElement": offers}], active="/packages", priority=0.9)

# ============================== WORK ==============================
def build_work():
    items = [("Home", "/"), ("Work", "/work")]
    cats = [("all", "All"), ("web", "Websites"), ("brand", "Brand identity"), ("logo", "Logos"), ("social", "Social & ads"), ("book", "Book covers"), ("product", "UI/UX"), ("motion", "Motion & 3D")]
    chips = "".join(f'<button type="button" data-f="{k}" aria-selected="{"true" if k == "all" else "false"}">{n}</button>' for k, n in cats)
    order = ["web", "motion", "brand", "logo", "product", "social", "book"]
    ws = sorted(WORK, key=lambda w: order.index(w["cat"]) if w["cat"] in order else 9)
    body = phero("Work", "The <em class='s teal'>reel.</em>", "Websites, brand identities, logos, apps, social ads, book covers, motion and 3D from Mogify Studio. Projects marked Concept are self-initiated designs that show our skills.", items, num=str(len(WORK)))
    body += f'<section class="sec" style="padding-top:0"><div class="wrap"><div class="svtabs" data-filter-for="gal" role="toolbar" aria-label="Filter work">{chips}</div><div class="gal" id="gal" style="margin-top:18px">{gal_items(ws)}</div></div></section>' + LB + cta_band()
    page("/work", "Work | Websites, Logos, Branding & Motion Portfolio | Mogify Studio", "See Mogify Studio work: websites, brand identities, logos, UI/UX, social media creatives, book covers, motion graphics and 3D animation.", body, ld=[crumbs_ld(items)], active="/work", priority=0.8)

def chip_fix(t):
    return t.replace('class="svtabs"', 'class="svtabs"')

# ============================== ABOUT ==============================
def build_about():
    items = [("Home", "/"), ("About", "/about")]
    body = phero("About Mogify", "We help good businesses <em class='s teal'>look as good as they are.</em>", "Mogify Studio is a creative and digital studio in Karachi, Pakistan, founded by Muhammad Moiz Ali. We design websites, brand identities, logos, UI/UX, motion and 3D for startups and growing businesses in Pakistan and worldwide.", items)
    body += f"""<section class="sec" style="padding-top:0"><div class="wrap founder">
<figure class="rv"><img src="/assets/img/founder.webp" alt="Muhammad Moiz Ali, founder of Mogify Studio" width="800" height="800" loading="lazy"><figcaption>Muhammad Moiz Ali<small>Founder &amp; Creative Director</small></figcaption></figure>
<div class="txt"><span class="eyebrow">The founder</span><h2 class="h-m split-h" style="margin:18px 0 24px">Hi, I'm Moiz. <em class="s teal">I run Mogify.</em></h2>
<p class="rv">I started Mogify Studio in Karachi with a simple belief: brand identities and websites are not decoration. They are how customers decide whether to trust a business.</p>
<p class="rv">At Mogify you work with me directly, from the first message to the final files. Websites are hand-coded and built mobile-first. Logos, identities, motion and 3D are made in-house, from scratch, for your brand only.</p>
<p class="rv">The name says what we do: we <em class="s teal">modify</em> brands until they stand out. Modify your brand with Mogify.</p>
<div class="hero-ctas rv"><a class="btn btn-glow btn-lg mag" href="/planner">Start your project {ARR}</a><a class="btn btn-wa btn-lg" href="{wa('Hi Moiz! I found Mogify Studio on your website and want to talk about a project.')}" target="_blank" rel="noopener">{bi('wa')} Message Moiz</a></div></div>
</div></section>"""
    vals = [("01", "Craft over templates", "Every logo, layout and frame is designed for your brand. Nothing is pulled from a template library."), ("02", "Clarity over surprises", "Clear packages, a fixed quote and agreed checkpoints, so you always know what is happening next."), ("03", "Business over decoration", "Design exists to win trust, enquiries and sales. That is how we judge our own work.")]
    vc = "".join(f'<li class="pstep"><span class="num">{a}</span><h3>{b_}</h3><p>{c}</p></li>' for a, b_, c in vals)
    body += f'<section class="sec" style="padding-top:0"><div class="wrap">{sec_head("What we stand for", "Three things we " + EM("never compromise on.") + "")}<ol class="proc">{vc}</ol></div></section>'
    body += cta_band()
    person = {"@type": "Person", "name": "Muhammad Moiz Ali", "jobTitle": "Founder & Creative Director", "worksFor": {"@id": ORG_ID}, "image": url("/assets/img/founder.webp"), "address": {"@type": "PostalAddress", "addressLocality": "Karachi", "addressCountry": "PK"}, "sameAs": ["https://www.linkedin.com/in/muhammad-moiz-ali-167102412/"]}
    page("/about", "About Mogify Studio | Founded by Muhammad Moiz Ali, Karachi", "Mogify Studio is a creative and digital studio in Karachi, Pakistan, founded by Muhammad Moiz Ali. Websites, branding, UI/UX, motion and 3D made in-house.", body, ld=[crumbs_ld(items), person], active="/about", priority=0.7)

def build_404():
    nf = f'<section class="nf" data-gl="logoC"><div class="wrap"><span class="eyebrow">404</span><h1 class="h-xl split-h" style="margin:20px auto">This page got <em class="s teal">mogified.</em></h1><p class="lead rv" style="margin:0 auto 30px">We could not find that page. Try one of these instead.</p><div class="hero-ctas rv" style="justify-content:center"><a class="btn btn-glow btn-lg" href="/">Home</a><a class="btn btn-line btn-lg" href="/packages">Packages</a><a class="btn btn-line btn-lg" href="/planner">Project Planner</a></div></div></section>'
    page("/404", "Page not found | Mogify Studio", "This page could not be found. Explore Mogify Studio services, packages and the Project Planner instead.", nf, noindex=True, gl=True)

if __name__ == "__main__":
    build_home(); build_services()
    for s in SERVICES: build_service(s)
    build_packages(); build_planner(); build_work(); build_about(); build_contact(); build_faq(); build_legal(); build_404(); build_work_pages(); build_meta()
    print("built", len(PAGES), "pages, assets v", stamp_version())
