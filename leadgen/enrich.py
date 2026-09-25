"""Fetch a clinic's own website (home + contact page) for phone, email and WhatsApp."""
import re
from urllib.parse import urljoin

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<![\d.])(?:(?:\+91[\s-]?|0)?[6-9]\d{4}[\s-]?\d{5}|(?:\+91[\s-]?|0)11[\s-]?\d{4}[\s-]?\d{4})(?!\d)")
WA_RE = re.compile(r"(?:wa\.me/|whatsapp\.com/send/?\?phone=)\+?(\d{10,13})")
BAD_EMAIL = ("example.", "sentry", "wixpress", ".png", ".jpg", "domain.com", "yourmail", "email@")
AGGREGATORS = ("practo.com", "justdial", "lybrate", "facebook.com", "instagram.com", "google.", "sulekha",
               "credihealth", "clinicspots", "youtube", "twitter", "linkedin", "wa.me", "whatsapp")


def is_own_site(url):
    return bool(url) and url.startswith("http") and not any(a in url for a in AGGREGATORS)


def scan(html):
    """Returns (phones, emails, whatsapp). Phones keep a leading 0 (e.g. '08037353763') so
    STD landlines and call-forwarding lines are not mistaken for mobiles; +91 is dropped."""
    text = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    tel = re.findall(r'href=["\']tel:([^"\']+)', html)
    phones = []
    for p in tel + PHONE_RE.findall(text):
        d = re.sub(r"\D", "", p)
        d = d[2:] if len(d) == 12 and d.startswith("91") else d
        if len(d) in (10, 11) and d not in phones:
            phones.append(d)
    emails = [e for e in dict.fromkeys(EMAIL_RE.findall(html)) if not any(b in e.lower() for b in BAD_EMAIL)]
    wa = [n[-10:] for n in dict.fromkeys(WA_RE.findall(html)) if n[-10:][0] in "6789"]
    return phones, emails, (wa[0] if wa else "")


def enrich(context, url):
    """context: a Playwright BrowserContext. Returns dict(url, ok, phones, emails, whatsapp)."""
    out = {"url": url, "ok": False, "phones": [], "emails": [], "whatsapp": ""}
    if not is_own_site(url):
        out["url"] = ""
        return out
    page = context.new_page()
    try:
        html_all = ""
        resp = page.goto(url, timeout=25000, wait_until="domcontentloaded")
        if resp and resp.ok:
            out["ok"] = True
            page.wait_for_timeout(1500)
            html_all = page.content()
            contact = page.eval_on_selector_all(
                "a[href]", "els => els.map(e => e.href).filter(h => /contact|reach|appointment|about/i.test(h))")
            for c in list(dict.fromkeys(contact))[:2]:
                try:
                    page.goto(urljoin(url, c), timeout=20000, wait_until="domcontentloaded")
                    page.wait_for_timeout(1000)
                    html_all += page.content()
                except Exception:
                    pass
        out["phones"], out["emails"], out["whatsapp"] = scan(html_all)
    except Exception as e:
        out["error"] = str(e)[:120]
    finally:
        page.close()
    return out
