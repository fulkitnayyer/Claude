"""Duplicate detection against the master tracker and against leads already accepted."""
import re
from urllib.parse import urlparse

import openpyxl

from config import MASTER_XLSX

STOP = {"dr", "dr.", "dental", "clinic", "clinics", "care", "centre", "center", "the", "and", "&",
        "multispeciality", "multispecialty", "implant", "implants", "studio", "dentistry", "hospital",
        "orthodontic", "smile", "s", "of", "delhi", "new"}


def norm_name(name):
    words = re.findall(r"[a-z0-9]+", (name or "").lower())
    return " ".join(w for w in words if w not in STOP)


def phones(text):
    """Last-10-digit keys for every Indian phone-looking number in text."""
    out = set()
    for m in re.findall(r"(?:\+?91[\s-]?)?(?:0)?[\d][\d\s-]{8,13}\d", text or ""):
        d = re.sub(r"\D", "", m)
        if len(d) >= 10:
            out.add(d[-10:])
    return out


def domain(url):
    if not url or not str(url).startswith("http"):
        return ""
    host = urlparse(str(url)).netloc.lower()
    return host[4:] if host.startswith("www.") else host


class Deduper:
    def __init__(self):
        self.names, self.phones, self.domains = set(), set(), set()
        wb = openpyxl.load_workbook(MASTER_XLSX, read_only=True)
        for row in wb["Delhi Prospects"].iter_rows(min_row=2, values_only=True):
            if row[1]:
                self.add(row[1], row[4], row[8], row[2])

    def add(self, name, phone, website, area=""):
        n = norm_name(name)
        if n:
            self.names.add((n, norm_name(area).split(" ")[0] if area else ""))
            self.names.add((n, ""))
        self.phones |= phones(str(phone or ""))
        d = domain(website)
        if d:
            self.domains.add(d)

    def match(self, name, phone, website, area=""):
        """Return a reason string if this clinic duplicates a known one, else ''."""
        for p in phones(str(phone or "")):
            if p in self.phones:
                return f"duplicate phone {p}"
        d = domain(website)
        if d and d in self.domains:
            return f"duplicate website {d}"
        n = norm_name(name)
        # generic names like "Dental Clinic" normalise to '' and are only matched by phone/site
        # a one-word name like "rohini" only counts as a duplicate within the same area
        a = norm_name(area).split(" ")[0] if area else ""
        if n and len(n) > 3 and ((n, a) in self.names or (len(n.split()) >= 2 and (n, "") in self.names)):
            return f"duplicate name '{n}'"
        return ""
