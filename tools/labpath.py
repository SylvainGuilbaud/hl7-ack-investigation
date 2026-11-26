"""Where is the lab's delivery log, and what are its sibling files called?

The lab container writes results/dashboard/lab<YYYY-MM-DD>.jsonl (date of the container start) and records the file
name in results/dashboard/.lab-current. The dashboard and its session cache are written next to the log.
results/dashboard/ is git-ignored. Every tool (tests, matrix, dashboard) asks this module, so a fresh install / new container
gets its own log, dashboard and session cache, and the committed reference files
(results/lab.jsonl, dashboard.html, sessions.json - the ones the article quotes) are never touched.
"""
import contextlib, fcntl, json, os, time
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


def lab_events(ctrl: str) -> list:
    """Every event the lab logged for one control id (independent of IRIS)."""
    p = current_log()
    if not p.exists():
        return []
    ev = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    return [e for e in ev if e.get("control_id") == ctrl]


@contextlib.contextmanager
def operation_lock(op: str):
    """One test at a time per OPERATION, whatever the service, the script or the tool.

    The services in front differ, but they all feed a few operations (out.default, out.failrej, out.legacy), each with
    PoolSize 1 and ONE TCP connection to the lab: two tests on the same operation queue behind each other and the
    second one reads the lab's log too early (false FAIL). With this lock the test scripts and the matrix can run in
    parallel, and next to each other: work on different operations overlaps, work on the same one waits its turn.
    flock is released by the OS if the process dies."""
    LIVE.mkdir(parents=True, exist_ok=True)
    with open(LIVE / f".op-{op}.lock", "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def wait_late_replies(ctrl: str, late_delay: float = 12, poll: float = 0.5) -> None:
    """After a LATE message: wait until the lab has sent the ack of every delivery.

    The lab answers each delivery late_delay seconds late and one at a time, so both replies (one per IRIS attempt)
    arrive after IRIS gave up. 'All acked' must hold twice in a row: the lab logs the next 'received' a few ms after the
    previous 'ack_sent'."""
    stable, deadline = 0, time.time() + 2 * late_delay + 10
    while stable < 2 and time.time() < deadline:
        e = lab_events(ctrl)
        got, acked = sum(x["event"] == "received" for x in e), sum(x["event"] == "ack_sent" for x in e)
        stable = stable + 1 if got and acked >= got else 0
        time.sleep(poll)
