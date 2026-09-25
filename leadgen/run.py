"""Collect → dedupe/filter → enrich → score → save, one clinic at a time.

    python leadgen/run.py                 # full run until TARGET_NEW leads
    python leadgen/run.py --target 20 --localities rohini   # test run
Safe to kill and re-run at any point: everything already done is skipped.
"""
import argparse
import random
import time

from playwright.sync_api import sync_playwright

import checkpoint
import export
from config import CHAIN_KEYWORDS, CHROMIUM, DELAY, LOCALITIES, NON_DELHI, PUSH_EVERY, START_NUMBER, TARGET_NEW
from dedupe import Deduper
from enrich import enrich
from practo import listing_page, profile
from score import build_row
from store import Store


def nap():
    time.sleep(random.uniform(*DELAY))


def out_of_scope(prof):
    name = (prof.get("name") or "").lower()
    addr = f"{prof.get('address', '')} {prof.get('locality', '')}".lower()
    if not prof.get("name"):
        return "no clinic name parsed"
    for k in CHAIN_KEYWORDS:
        if k in name:
            return f"chain/hospital ({k})"
    if (prof.get("branches") or 1) >= 5:
        return "chain (5+ locations)"
    for k in NON_DELHI:
        if k in addr:
            return f"outside Delhi ({k})"
    return ""


def process(store, dd, ctx, page, url):
    try:
        prof = profile(page, url)
    except Exception as e:
        print(f"  ! profile failed {url}: {str(e)[:80]}", flush=True)
        return False
    nap()
    reason = out_of_scope(prof)
    site = enrich(ctx, prof.get("website")) if not reason else {}
    if not reason:
        reason = dd.match(prof["name"], " ".join([prof.get("phone", "")] + site.get("phones", [])),
                          site.get("url") or prof.get("website"), prof.get("locality", ""))
    if not reason and not (prof.get("phone") or site.get("phones")):
        reason = "no phone found"
    if reason:
        store.mark_seen(url, "dropped", reason.split(" '")[0].split(" (")[0] if "duplicate" in reason else reason)
        print(f"  - drop {prof.get('name')!r}: {reason}", flush=True)
        return False
    num = store.next_num(START_NUMBER)
    row = build_row(num, prof, site, store.hits(url))
    store.add_lead(num, url, row)
    dd.add(row["Clinic"], row["Phone"] + " " + (prof.get("phone") or ""), row["Website"], row["Area"])
    export.build(store.leads(), store.drop_summary())
    print(f"  + #{num} {row['Clinic']} | {row['Phone']} | ads: {row['Practo Ads (Sponsored/Prime)']}", flush=True)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=TARGET_NEW)
    ap.add_argument("--localities", nargs="*", default=None)
    ap.add_argument("--max-pages", type=int, default=10)
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    store, dd = Store(), Deduper()
    for lead in store.leads():                      # resume: known accepted leads also dedupe
        dd.add(lead["Clinic"], lead["Phone"], lead["Website"], lead["Area"])
    queue = list(args.localities or LOCALITIES)
    since_push = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM, headless=True)
        ctx = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"), locale="en-IN")
        page = ctx.new_page()

        # finish profiles already discovered in an earlier run first
        for url in store.pending_urls():
            if store.count() >= args.target:
                break
            since_push += process(store, dd, ctx, page, url)

        i = 0
        while i < len(queue) and store.count() < args.target:
            loc = queue[i]
            i += 1
            for n in range(1, args.max_pages + 1):
                if store.count() >= args.target:
                    break
                if store.page_done(loc, n):
                    continue
                try:
                    res = listing_page(page, loc, n)
                except Exception as e:
                    print(f"! listing {loc} p{n} failed: {str(e)[:80]}", flush=True)
                    break
                nap()
                cards = res["cards"]
                if not args.localities:
                    queue += [l for l in res["localities"] if l not in queue]
                print(f"[{loc} p{n}] {len(cards)} clinics, total leads {store.count()}", flush=True)
                for url, c in cards.items():
                    store.add_hit(url, loc, n, c["sponsored"], c["prime"])
                for url in cards:
                    if store.count() >= args.target:
                        break
                    if store.is_seen(url):
                        continue
                    since_push += process(store, dd, ctx, page, url)
                    if since_push >= PUSH_EVERY and not args.no_push:
                        checkpoint.push(store.count())
                        since_push = 0
                store.mark_page(loc, n, len(cards))
                if len(cards) < 5:
                    break
        browser.close()

    export.build(store.leads(), store.drop_summary())
    if not args.no_push:
        checkpoint.push(store.count())
    print(f"Done: {store.count()} leads. Drops: {store.drop_summary()}")


if __name__ == "__main__":
    main()
