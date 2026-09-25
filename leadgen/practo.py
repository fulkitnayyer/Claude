"""Practo listing + clinic-profile collection (Playwright). Raw HTML is cached for re-parsing."""
import hashlib
import json
import re

from config import CACHE, LISTING_URL, PRACTO

CARD_JS = r"""
() => {
  const out = {};
  for (const a of document.querySelectorAll('a[href*="/delhi/clinic/"]')) {
    const href = a.href.split('?')[0].split('#')[0];
    if (/\/clinics\//.test(href)) continue;
    // climb to the listing card (the smallest ancestor holding a single clinic link)
    let el = a, card = a;
    for (let i = 0; i < 8 && el.parentElement; i++) {
      el = el.parentElement;
      const n = new Set([...el.querySelectorAll('a[href*="/delhi/clinic/"]')]
                  .map(x => x.href.split('?')[0])).size;
      if (n > 1) break;
      card = el;
    }
    const t = (card.innerText || '').replace(a.innerText || '', ' ');
    const prev = out[href] || {sponsored: false, prime: false, text: ''};
    out[href] = {
      sponsored: prev.sponsored || /\bsponsored\b/i.test(t) || !!card.querySelector('[data-qa-id*="sponsor" i],[class*="sponsor" i]'),
      prime: prev.prime || /\bprime\b/i.test(t) || !!card.querySelector('[data-qa-id*="prime" i],[class*="prime" i],img[alt*="prime" i]'),
      text: prev.text || t.slice(0, 400),
    };
  }
  const locs = [...document.querySelectorAll('a[href*="/delhi/clinics/dental-clinics/"]')]
      .map(a => a.href.split('?')[0].split('/').pop()).filter(Boolean);
  return {cards: out, localities: [...new Set(locs)]};
}
"""


def _cache(kind, url, html):
    CACHE.mkdir(parents=True, exist_ok=True)
    name = hashlib.sha1(url.encode()).hexdigest()[:16]
    (CACHE / f"{kind}-{name}.html").write_text(html, encoding="utf-8")


def cached(kind, url):
    p = CACHE / f"{kind}-{hashlib.sha1(url.encode()).hexdigest()[:16]}.html"
    return p.read_text(encoding="utf-8") if p.exists() else None


def listing_page(page, locality, n):
    url = LISTING_URL.format(locality=locality) + (f"?page={n}" if n > 1 else "")
    page.goto(url, timeout=45000, wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    for _ in range(4):                      # lazy-loaded cards
        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(600)
    _cache("list", url, page.content())
    return page.evaluate(CARD_JS)


# ---------------------------------------------------------------------------
# Profile parsing
# ---------------------------------------------------------------------------
def _jsonld(html):
    items = []
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S):
        try:
            data = json.loads(block)
        except Exception:
            continue
        for d in data if isinstance(data, list) else [data]:
            items += d.get("@graph", [d]) if isinstance(d, dict) else []
    return items


PROFILE_JS = r"""
() => {
  const q = s => document.querySelector(s);
  const txt = s => (q(s)?.innerText || '').trim();
  const body = document.body.innerText;
  const doctors = [];
  const seen = new Set();
  for (const a of document.querySelectorAll('a[href*="/delhi/doctor/"]')) {
    const href = a.href.split('?')[0];
    const name = (a.innerText || '').trim();
    if (!name || !/^dr/i.test(name) || seen.has(href)) continue;
    seen.add(href);
    let box = a;
    for (let i = 0; i < 4 && box.parentElement && (box.innerText || '').length < 60; i++) box = box.parentElement;
    const t = (box.parentElement || box).innerText || '';
    const quals = (t.match(/\b(BDS|MDS|DDS|MSc|M\.Sc|FICOI|FAGE|MFDS|PhD|Diploma)[^\n]*/) || [''])[0];
    const exp = (t.match(/(\d+)\+?\s*years? experience/i) || [''])[0];
    doctors.push({name: name.split('\n')[0], quals: quals.slice(0, 120), exp, url: href});
  }
  const services = [...document.querySelectorAll('[data-qa-id*="service" i], [class*="service" i] li, [class*="services" i] span')]
      .map(e => e.innerText.trim()).filter(t => t && t.length < 60);
  const website = [...document.querySelectorAll('a[href^="http"]')]
      .map(a => a.href).find(h => !/practo|google|facebook|instagram|twitter|youtube|linkedin|apple|play\.google/i.test(h)) || '';
  const other = body.match(/(\d+)\s+(?:other\s+)?(?:locations|branches|clinics)\b/i);
  return {
    name: txt('h1') || document.title.split(',')[0],
    locality: txt('[data-qa-id="clinic-locality"], [data-qa-id="practice_locality"]'),
    address: txt('[data-qa-id="clinic-address"], [data-qa-id="clinic_address"], [itemprop="streetAddress"]'),
    doctors, services: [...new Set(services)].slice(0, 40), website,
    prime: /\bprime\b/i.test(txt('header') + txt('[class*="badge" i]') + txt('[data-qa-id*="prime" i]')),
    reviews: parseInt((body.match(/(\d[\d,]*)\s+(?:patient\s+)?(?:stories|feedback|reviews)/i) || ['', '0'])[1].replace(/,/g, '')),
    fees: (body.match(/₹\s?\d[\d,]*/) || [''])[0],
    established: (body.match(/(?:established|since|founded)\s+(?:in\s+)?((?:19|20)\d\d)/i) || ['', ''])[1],
    other_locations: other ? parseInt(other[1]) : 0,
  };
}
"""

PHONE_RE = re.compile(r"(?<![\d.])(?:(?:\+91[\s-]?|0)?[6-9]\d{4}[\s-]?\d{5}|0\d{2,4}[\s-]?\d{6,8})(?!\d)")


def visible_text(html):
    """Page text without <script>/<style> bodies, so CSS values like .6666666667s never parse as phones."""
    html = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def profile(page, url):
    page.goto(url, timeout=45000, wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    info = page.evaluate(PROFILE_JS)
    # Reveal the contact number (Practo hides it behind a button)
    for label in ("Call Now", "Contact Clinic", "Call", "View Phone", "Show Number"):
        try:
            btn = page.get_by_text(label, exact=False).first
            if btn.count() and btn.is_visible():
                btn.click(timeout=3000)
                page.wait_for_timeout(1500)
                break
        except Exception:
            continue
    html = page.content()
    _cache("profile", url, html)
    if info.get("prime") and "prime" in (info.get("name") or "").lower():
        info["prime"] = False   # "Prime" is part of the clinic's name, not the badge
    tel = re.findall(r'href=["\']tel:([^"\']+)', html)
    text = visible_text(html)
    labelled = re.findall(r"Phone number\s*([+\d][\d\s-]{8,16}\d)", text)
    m = tel or labelled or PHONE_RE.findall(text)
    phone = m[0].strip() if m else ""

    for item in _jsonld(html):
        t = item.get("@type")
        t = " ".join(t) if isinstance(t, list) else str(t)
        if any(k in t for k in ("Dentist", "MedicalClinic", "LocalBusiness", "MedicalBusiness")):
            info["name"] = info["name"] or item.get("name")
            addr = item.get("address") or {}
            if isinstance(addr, dict) and not info["address"]:
                info["address"] = ", ".join(x for x in (addr.get("streetAddress"), addr.get("addressLocality"),
                                                        addr.get("postalCode")) if x)
                info["locality"] = info["locality"] or addr.get("addressLocality", "")
            phone = phone or item.get("telephone") or ""
            rating = item.get("aggregateRating") or {}
            if isinstance(rating, dict) and not info["reviews"]:
                try:
                    info["reviews"] = int(rating.get("reviewCount") or rating.get("ratingCount") or 0)
                except ValueError:
                    pass
    # Practo's h1 is "<Clinic name>, <Locality>"; split it so Clinic and Area are clean
    name = (info.get("name") or "").strip()
    if "," in name:
        head, tail = name.rsplit(",", 1)
        if tail.strip() and len(tail.strip()) <= 40:
            info["name"] = head.strip()
            if not info.get("locality") or info["locality"].strip().lower() == "delhi":
                info["locality"] = tail.strip()
    info["phone"] = phone
    info["url"] = url
    info["branches"] = 1 + (info.pop("other_locations") or 0)
    return info
