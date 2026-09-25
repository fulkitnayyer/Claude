"""Checkpoint marker. The repo is public, so lead data is never committed to git.

The runner prints a '[checkpoint]' line every PUSH_EVERY leads; whoever is driving
the run (Claude, in the session) sends the current xlsx to the user at that point.
SQLite + JSONL already hold every clinic the moment it is processed.
"""
import shutil

from config import DATA, OUT_XLSX


def push(count):
    if OUT_XLSX.exists():
        shutil.copy2(OUT_XLSX, DATA / f"snapshot-{count:04d}.xlsx")
    print(f"[checkpoint] {count} leads – {OUT_XLSX.name} ready to send", flush=True)
