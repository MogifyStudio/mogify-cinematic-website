const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const SITE = path.join(__dirname, '..', 'site');
const read = (p) => fs.readFileSync(path.join(SITE, p), 'utf8');
const pages = ['index.html','services.html','packages.html','planner.html','work.html','about.html','contact.html','faq.html','privacy.html','terms.html','404.html',
  ...fs.readdirSync(path.join(SITE,'services')).map(f => 'services/' + f)];

test('every page has title, viewport, description, canonical and no placeholders', () => {
  for (const p of pages) {
    const h = read(p);
    assert.match(h, /<title>[^<]{10,}<\/title>/, p + ' title');
    assert.match(h, /<meta name="viewport" content="width=device-width, initial-scale=1/, p + ' viewport');
    assert.match(h, /<meta name="description" content="[^"]{30,}"/, p + ' description');
    assert.match(h, /rel="canonical" href="https:\/\/mogify-cinematic\.sites\.tab\.bot/, p + ' canonical');
    assert.doesNotMatch(h, /lorem ipsum|\bTODO\b|\bPLACEHOLDER\b|__V__|>undefined</, p + ' placeholder');
  }
});

test('local asset references resolve', () => {
  for (const p of pages) {
    const h = read(p);
    const refs = [...h.matchAll(/(?:src|href)="(\/[^"#?]+)/g)].map(m => m[1]);
    for (const r of refs) {
      const f = path.join(SITE, r);
      const ok = fs.existsSync(f) || fs.existsSync(f + '.html') || fs.existsSync(path.join(f, 'index.html'));
      assert.ok(ok, p + ' -> missing ' + r);
    }
  }
});

test('home carries the cinematic hero, chapters and honest content', () => {
  const h = read('index.html');
  assert.match(h, /<canvas id="gl"/);
  assert.match(h, /gl\.js/);
  assert.match(h, /impossible/);
  for (const id of ['services','work','packages']) assert.match(h, new RegExp('id="' + id + '"'));
  assert.match(h, /class="reel"/);
  assert.doesNotMatch(h, /testimonial|trusted by|5-star|★★★/i);
  const ld = JSON.parse(h.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const types = JSON.stringify(ld);
  assert.match(types, /ProfessionalService/); assert.match(types, /FAQPage/);
});

test('one price config, every package price reads from it, quotes open WhatsApp naming the package', () => {
  const cfg = read('assets/js/config.js');
  assert.match(cfg, /window\.MOGIFY\s*=/);
  const pk = read('packages.html');
  const prices = [...pk.matchAll(/data-price="(\w+)\.(starter|growth|premium)"/g)];
  assert.ok(prices.length >= 27, 'package price spots: ' + prices.length);
  const quotes = [...pk.matchAll(/href="https:\/\/wa\.me\/923232194013\?text=([^"]+)"[^>]*data-pkg/g)].map(m => decodeURIComponent(m[1]));
  assert.ok(quotes.length >= 27);
  assert.ok(quotes.every(q => /(Starter|Growth|Premium) package/.test(q)));
  assert.doesNotMatch(pk, /(PKR|Rs\.?|\$)\s?\d/, 'no invented prices in HTML');
});

test('service pages carry Service JSON-LD; sitemap and robots use BASE_URL', () => {
  const s = read('services/web-design.html');
  assert.match(s, /"@type": "Service"/);
  const sm = read('sitemap.xml');
  assert.match(sm, /https:\/\/mogify-cinematic\.sites\.tab\.bot\/packages/);
  assert.match(read('robots.txt'), /Sitemap: https:\/\/mogify-cinematic\.sites\.tab\.bot\/sitemap\.xml/);
});

test('planner page wires the brief to WhatsApp and email', () => {
  const p = read('planner.html');
  assert.match(p, /id="planner"/); assert.match(p, /data-wa="923232194013"/); assert.match(p, /mogifystudio@gmail\.com/);
  assert.match(p, /planner\.js/);
});
