"""Commit + push the live data so it survives the container going away."""
import subprocess
import time

from config import GIT_BRANCH, REPO

TRAILER = ("\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
           "Claude-Session: https://claude.ai/code/session_01YLLFL3K4fAno2FBL5XzT26")


def push(count):
    paths = ["HealthGrow_Delhi_Dental_Prospects_Batch8.xlsx", "leadgen/data"]
    subprocess.run(["git", "add", *paths], cwd=REPO, check=False)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO).returncode == 0:
        return
    subprocess.run(["git", "commit", "-q", "-m", f"data: Batch 8 checkpoint – {count} leads" + TRAILER],
                   cwd=REPO, check=False)
    for wait in (0, 2, 4, 8, 16):
        time.sleep(wait)
        if subprocess.run(["git", "push", "-q", "-u", "origin", GIT_BRANCH], cwd=REPO).returncode == 0:
            print(f"[checkpoint] pushed at {count} leads", flush=True)
            return
    print("[checkpoint] push failed – data is still safe locally in leadgen/data", flush=True)
