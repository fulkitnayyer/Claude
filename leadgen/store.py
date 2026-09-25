"""SQLite source of truth. Every clinic is committed the moment it is processed."""
import json
import sqlite3
import time

from config import DATA, DB_PATH, JSONL_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS seen (          -- every Practo profile URL touched, accepted or not
    url TEXT PRIMARY KEY, status TEXT, reason TEXT, ts REAL
);
CREATE TABLE IF NOT EXISTS leads (         -- accepted leads, one row per clinic
    num INTEGER PRIMARY KEY, url TEXT UNIQUE, data TEXT, ts REAL
);
CREATE TABLE IF NOT EXISTS listing_hits (  -- sponsored/prime evidence seen on listing pages
    url TEXT, locality TEXT, page INTEGER, sponsored INTEGER, prime INTEGER,
    PRIMARY KEY (url, locality, page)
);
CREATE TABLE IF NOT EXISTS done_pages (locality TEXT, page INTEGER, n INTEGER, PRIMARY KEY (locality, page));
"""


class Store:
    def __init__(self):
        DATA.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(DB_PATH)
        self.db.executescript(SCHEMA)
        self.db.commit()

    # --- listing pages -------------------------------------------------
    def page_done(self, locality, page):
        return self.db.execute("SELECT 1 FROM done_pages WHERE locality=? AND page=?",
                               (locality, page)).fetchone() is not None

    def mark_page(self, locality, page, n):
        self.db.execute("INSERT OR REPLACE INTO done_pages VALUES (?,?,?)", (locality, page, n))
        self.db.commit()

    def add_hit(self, url, locality, page, sponsored, prime):
        self.db.execute("INSERT OR REPLACE INTO listing_hits VALUES (?,?,?,?,?)",
                        (url, locality, page, int(sponsored), int(prime)))
        self.db.commit()

    def hits(self, url):
        return self.db.execute("SELECT locality, page, sponsored, prime FROM listing_hits WHERE url=?",
                               (url,)).fetchall()

    def pending_urls(self):
        return [r[0] for r in self.db.execute(
            "SELECT DISTINCT h.url FROM listing_hits h LEFT JOIN seen s ON s.url=h.url "
            "WHERE s.url IS NULL ORDER BY h.rowid")]

    # --- profiles ------------------------------------------------------
    def is_seen(self, url):
        return self.db.execute("SELECT 1 FROM seen WHERE url=?", (url,)).fetchone() is not None

    def mark_seen(self, url, status, reason=""):
        self.db.execute("INSERT OR REPLACE INTO seen VALUES (?,?,?,?)", (url, status, reason, time.time()))
        self.db.commit()

    def next_num(self, start):
        r = self.db.execute("SELECT MAX(num) FROM leads").fetchone()[0]
        return start if r is None else r + 1

    def add_lead(self, num, url, row):
        payload = json.dumps(row, ensure_ascii=False)
        with self.db:
            self.db.execute("INSERT INTO leads VALUES (?,?,?,?)", (num, url, payload, time.time()))
            self.db.execute("INSERT OR REPLACE INTO seen VALUES (?,?,?,?)", (url, "accepted", "", time.time()))
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(payload + "\n")
            f.flush()

    def leads(self):
        return [json.loads(r[0]) for r in self.db.execute("SELECT data FROM leads ORDER BY num")]

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM leads").fetchone()[0]

    def drop_summary(self):
        return self.db.execute("SELECT reason, COUNT(*) FROM seen WHERE status='dropped' "
                               "GROUP BY reason ORDER BY 2 DESC").fetchall()
