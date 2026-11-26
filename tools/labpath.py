"""Where is the lab's delivery log, and what are its sibling files called?

The lab container writes results/dashboard/lab<YYYY-MM-DD>.jsonl (date of the container start) and records the file
name in results/dashboard/.lab-current. The dashboard and its session cache are written next to the log.
results/dashboard/ is git-ignored. Every tool (tests, matrix, dashboard) asks this module, so a fresh install / new container
gets its own log, dashboard and session cache, and the committed reference files
(results/lab.jsonl, dashboard.html, sessions.json - the ones the article quotes) are never touched.
"""
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
LIVE = RESULTS / "dashboard"          # this checkout's own runs (git-ignored); RESULTS itself holds the committed reference
POINTER = LIVE / ".lab-current"


def current_log() -> Path:
    """LAB_LOG_FILE env > pointer written by the lab > newest results/dashboard/lab<date>.jsonl > today's (not yet existing) name.

    It never falls back to the committed reference results/lab.jsonl: a missing live log must stay visible
    (the file does not exist) instead of silently aiming tools at the published files."""
    if os.environ.get("LAB_LOG_FILE"):
        return Path(os.environ["LAB_LOG_FILE"]).resolve()
    if POINTER.exists():
        p = LIVE / POINTER.read_text().strip()
        if p.name:
            return p
    dated = sorted(LIVE.glob("lab*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return dated[0] if dated else LIVE / f"lab{datetime.now():%Y-%m-%d}.jsonl"


def sibling(log: Path, prefix: str, ext: str) -> Path:
    """lab2026-11-26.jsonl -> dashboard2026-11-26.html / sessions2026-11-26.json ; lab.jsonl -> dashboard.html / sessions.json"""
    stem = Path(log).stem
    suffix = stem[3:] if stem.startswith("lab") else ""
    return Path(log).with_name(f"{prefix}{suffix}{ext}")
