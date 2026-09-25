"""Turn collected facts into a tracker row: scores, notes, phone confidence. No invention."""
import re

CORE = ["implant", "aligner", "invisalign", "root canal", "rct", "crown", "veneer", "cosmetic",
        "smile design", "whitening", "orthodont", "braces", "full mouth"]


def _is_mobile(p):
    d = re.sub(r"\D", "", p or "")[-10:]
    return len(d) == 10 and d[0] in "6789"


def _fmt(p):
    d = re.sub(r"\D", "", p)[-10:]
    return f"+91 {d[:5]} {d[5:]}" if _is_mobile(d) else p.strip()


def build_row(num, prof, site, hits):
    doctors = prof.get("doctors") or []
    services = " ".join(prof.get("services") or []).lower()
    quals = " ".join(d.get("quals", "") for d in doctors).upper()
    core_hits = sorted({c for c in CORE if c in services})
    n_docs = len(doctors)
    reviews = prof.get("reviews") or 0
    branches = prof.get("branches") or 1

    sponsored = [h for h in hits if h[2]]
    prime = bool(prof.get("prime")) or any(h[3] for h in hits)
    if sponsored and prime:
        ads = "Yes – Sponsored + Prime"
    elif sponsored:
        ads = "Yes – Sponsored"
    elif prime:
        ads = "Yes – Prime"
    else:
        ads = "No (not seen)"
    evidence = []
    if sponsored:
        evidence.append("Sponsored slot on: " + ", ".join(f"{h[0]} p{h[1]}" for h in sponsored[:4]))
    if prime:
        evidence.append("Prime badge on Practo profile")
    evidence = "; ".join(evidence) or "No Sponsored slot or Prime badge seen during collection"

    # --- phone / reachability --------------------------------------------------
    site_phones = [p for p in (site.get("phones") or []) if p]
    site_mobiles = [p for p in site_phones if _is_mobile(p)]
    practo_phone = prof.get("phone") or ""
    if site_mobiles or site_phones:
        phone = " / ".join(_fmt(p) for p in (site_mobiles or site_phones)[:2])
        conf = "Verified: clinic's own website"
    elif practo_phone:
        phone = _fmt(practo_phone)
        conf = "Directory (Practo listing – likely call-forwarding)"
    else:
        phone, conf = "Not found", "—"

    if site.get("whatsapp"):
        wa = f"Yes – confirmed ({site['whatsapp']} link on site)"
    elif site_mobiles:
        wa = "Yes (assumed – mobile)"
    elif practo_phone:
        wa = "Uncertain – Practo number may be a call-forwarding line; confirm direct mobile"
    else:
        wa = "Not found"
    email = (site.get("emails") or ["Not found"])[0]

    # --- scores -----------------------------------------------------------------
    fit = 3
    fit += 1 if len(core_hits) >= 3 else 0
    fit += 1 if "MDS" in quals else 0
    fit -= 1 if branches >= 3 else 0
    fit -= 1 if not core_hits and not services else 0

    signal = 3
    signal += 2 if (sponsored and prime) else 1 if (sponsored or prime) else 0
    signal += 1 if reviews >= 100 else 0
    signal -= 1 if reviews < 5 and not (sponsored or prime) else 0
    signal += 1 if n_docs >= 3 and not (sponsored and prime) else 0

    reach = 2
    reach += 2 if conf.startswith("Verified") and site_mobiles else 1 if conf.startswith("Verified") else 0
    reach += 1 if site.get("whatsapp") else 0
    reach += 1 if email != "Not found" else 0
    reach -= 1 if phone == "Not found" else 0
    clamp = lambda x: max(1, min(5, x))

    # --- notes (facts only) -----------------------------------------------------
    why = []
    if n_docs:
        why.append(f"{n_docs}-dentist bench" if n_docs > 1 else "Solo dentist practice")
    if "MDS" in quals:
        why.append("MDS specialist(s)")
    if core_hits:
        why.append("offers " + ", ".join(core_hits[:4]))
    if reviews:
        why.append(f"{reviews} Practo reviews")
    if prof.get("established"):
        why.append(f"est. {prof['established']}")
    if sponsored or prime:
        why.append("already paying for Practo visibility – warm 'is your spend working?' opener")
    check = []
    if not conf.startswith("Verified"):
        check.append("Confirm a direct mobile – only the Practo number was found.")
    if not site.get("url"):
        check.append("No own website found.")
    elif not site.get("ok"):
        check.append("Own website did not load – check it is still live.")
    if not doctors:
        check.append("No dentist name on Practo profile.")
    check.append("Google Ads status not yet checked.")

    lead_dentist = "; ".join(
        ", ".join(x for x in (d.get("name"), d.get("quals"), d.get("exp")) if x) for d in doctors[:3]
    ) or "Not found"

    return {
        "#": num,
        "Clinic": prof.get("name"),
        "Area": prof.get("area") or prof.get("locality"),
        "Lead Dentist & Qualifications": lead_dentist,
        "Phone": phone,
        "Phone Confidence": conf,
        "WhatsApp": wa,
        "Email": email,
        "Website": site.get("url") or "Not found",
        "Address": prof.get("address") or "Not found",
        "Branches": f"{branches} (per Practo)" if branches > 1 else "1 (independent)",
        "Why Call / Notes": (lambda t: t[0].upper() + t[1:])("; ".join(why) + ".") if why else "Practo-listed Delhi clinic.",
        "Check First": " ".join(check),
        "Fit (1-5)": clamp(fit),
        "Signal (1-5)": clamp(signal),
        "Reachability (1-5)": clamp(reach),
        "Status": "Not started",
        "Google Ads Status": "Not checked yet",
        "Ads Evidence / Last Shown": None,
        "Message Angle": "Warm — is your Practo spend working?" if (sponsored or prime)
                         else "Cold — missed-patients snapshot",
        "Practo Ads (Sponsored/Prime)": ads,
        "Practo Ads Evidence": evidence,
        "Practo URL": prof.get("url"),
    }
