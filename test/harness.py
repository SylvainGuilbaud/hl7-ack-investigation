"""Shared helpers for the test scripts. stdlib only; needs `docker compose up -d` first."""
import json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORTS = {"default": 29201, "failrej": 29202, "legacy": 29203,
         # same operations, other AckMode on the service (what the sender gets back)
         "app.default": 29211, "app.failrej": 29212, "app.legacy": 29213,
         "msh.failrej": 29214, "never.failrej": 29215, "byte.failrej": 29216}
TERMINAL = {"Completed", "Error", "Suspended", "Discarded", "Aborted"}
LATE_DELAY = 12
_failed = []


def iris(code):
    r = subprocess.run(["docker", "exec", "-i", "hl7ack-iris", "iris", "session", "IRIS", "-U", "REPRO"],
                       input=code + "\nhalt\n", capture_output=True, text=True)
    return r.stdout


def lab_events(ctrl):
    p = ROOT / "results" / "lab.jsonl"
    if not p.exists():
        return []
    ev = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    return [e for e in ev if e.get("control_id") == ctrl]


def summary(ctrl):
    out = iris(f'do ##class(Repro.Trace).Summary("{ctrl}")')
    line = next((l for l in out.splitlines() if l.startswith("SUMMARY|")), "SUMMARY|?||")
    return (line.split("|") + ["", "", ""])[1:4]


def fence(text, lang="text"):
    return f"```{lang}\n{text.rstrip()}\n```\n"


def run(case, mode, title, expect, ack=(), wait=40):
    """Send one message through `case` with the lab answering `mode`; print a Markdown report; check `expect`.

    expect: dict with optional keys  deliveries (int | callable), status (str), actions (substring), no_actions,
            sender_has / sender_lacks (substring(s) of what the SENDER received)
    ack:    (MSH-15, MSH-16) set by the sender;  wait: seconds the sender waits for an answer
    """
    ctrl = f"{case}-{mode}-{time.strftime('%H%M%S')}"
    ctrl = ctrl.replace("..", ".")
    print(f"## {title}\n")
    print(f"| case | port | lab mode (MSH-6) | control id |\n|---|---|---|---|\n| `{case}` | {PORTS[case]} | `{mode}` | `{ctrl}` |\n")
    sent = subprocess.run([sys.executable, "-I", str(ROOT / "tools/send.py"), "localhost", str(PORTS[case]), mode, ctrl, *ack],
                          capture_output=True, text=True, check=True, env={"SEND_WAIT": str(wait), "PATH": "/usr/bin:/bin"}).stdout
    answer = sent.split("ANSWER TO THE SENDER", 1)[-1]
    print("### Sent, and what the sender gets back from IRIS\n")
    print(fence(sent))
    t0 = time.time()
    status = actions = errs = ""
    while time.time() - t0 < 60:
        time.sleep(2)
        status, actions, errs = summary(ctrl)
        if status in TERMINAL:
            break
    if mode == "LATE":
        time.sleep(LATE_DELAY + 8)          # let the lab finish both late replies (one per attempt) ...
        iris(f'do ##class(Repro.Trace).ResetOperation("out.{case.split(".")[-1]}")')   # ... then drop the stale bytes
    ev = lab_events(ctrl)
    print("### What the downstream lab saw and answered (`results/lab.jsonl`)\n")
    rows = ["| time | event | MSA-1 | MSH-9 |", "|---|---|---|---|"]
    for e in ev:
        rows.append(f"| {e['ts'][11:23]} | {e['event']} | {e.get('msa1', '')} | `{e.get('msh9', '')}` |")
    print("\n".join(rows) + "\n")
    print("### What IRIS recorded (`Repro.Trace.Report`)\n")
    rep = iris(f'do ##class(Repro.Trace).Report("{ctrl}")')
    print(fence("\n".join(l[:260] for l in rep.splitlines() if l.strip() and not l.startswith(("Node:", "REPRO>")))))
    deliveries = sum(1 for e in ev if e["event"] == "received")
    problems = []
    d = expect.get("deliveries")
    if d is not None and not (d(deliveries) if callable(d) else deliveries == d):
        problems.append(f"deliveries={deliveries}, expected {getattr(d, '__doc__', d)}")
    if "status" in expect and status != expect["status"]:
        problems.append(f"status={status}, expected {expect['status']}")
    if "actions" in expect and expect["actions"] not in actions:
        problems.append(f"action codes '{actions}' do not contain '{expect['actions']}'")
    if "no_actions" in expect and actions:
        problems.append(f"expected no ReplyCodeActions action code, got '{actions}'")
    for key, want in (("sender_has", True), ("sender_lacks", False)):
        for needle in ([expect[key]] if isinstance(expect.get(key), str) else expect.get(key, [])):
            if (needle in answer) != want:
                problems.append(f"sender answer {'lacks' if want else 'contains'} '{needle}'")
    print(f"**Result:** deliveries = **{deliveries}**, final status = **{status}**, action codes = `{actions or '-'}`\n")
    print(f"**Verdict:** {'PASS' if not problems else 'FAIL - ' + '; '.join(problems)}\n")
    if problems:
        _failed.append(title)
    return not problems


def finish():
    print(f"**Script verdict:** {'ALL PASSED' if not _failed else 'FAILED - ' + ', '.join(_failed)}")
    sys.exit(1 if _failed else 0)


def retried(n):
    return n > 1
retried.__doc__ = "more than 1 (retried)"
