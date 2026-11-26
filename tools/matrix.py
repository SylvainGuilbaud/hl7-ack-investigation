#!/usr/bin/env python3
"""Run the test matrix: every (case, simulator mode) pair, then print a Markdown table.

For each cell it sends one message, waits until IRIS has finished with it, then reads
  - how many times the lab simulator RECEIVED it   (the lab's current log results/dashboard/lab<date>.jsonl, independent of IRIS)
  - the final status and the ReplyCodeActions action codes IRIS logged (Repro.Trace.Summary)

Rows = every inbound service of the production (ReplyCodeActions x AckMode), columns = what the lab does.
usage: matrix.py [--cases a,b] [--modes AA,AR] [--out results/matrix.md]
"""
import argparse, json, subprocess, sys, time, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True      # no __pycache__ in the repo
sys.path.insert(0, str(ROOT / "tools"))
from labpath import current_log, sibling
# case label -> (port, AckMode of the service, operation, extra sender args = MSH-15 MSH-16)
CASES = {
    "default":        (29201, "Immed", "out.default", ()),
    "failrej":        (29202, "Immed", "out.failrej", ()),
    "legacy":         (29203, "Immed", "out.legacy",  ()),
    "app.default":    (29211, "App",   "out.default", ()),
    "app.failrej":    (29212, "App",   "out.failrej", ()),
    "app.legacy":     (29213, "App",   "out.legacy",  ()),
    "msh.failrej+AL": (29214, "Msh",   "out.failrej", ("AL", "NE")),   # MSH-15=AL: accept ACK requested
    "msh.failrej+App": (29214, "Msh",  "out.failrej", ("NE", "AL")),   # MSH-16=AL: application ACK requested
    "msh.failrej":    (29214, "Msh",   "out.failrej", ()),             # no ACK requested
    "never.failrej":  (29215, "Never", "out.failrej", ()),
    "byte.failrej":   (29216, "Byte",  "out.failrej", ()),
}
SEND_WAIT = 15      # seconds the sender waits for an answer

MODES = ["AA", "AE", "AR", "AR3", "OTHERID", "NOMSA", "NOFRAME", "CLOSE", "LATE"]
LATE_DELAY = 12
TERMINAL = {"Completed", "Error", "Suspended", "Discarded", "Aborted"}


def iris(code: str) -> str:
    r = subprocess.run(["docker", "exec", "-i", "hl7ack-iris", "iris", "session", "IRIS", "-U", "REPRO"],
                       input=code + "\nhalt\n", capture_output=True, text=True)
    return r.stdout


def summary(ctrl):
    out = iris(f'do ##class(Repro.Trace).Summary("{ctrl}")')
    line = next((l for l in out.splitlines() if l.startswith("SUMMARY|")), "SUMMARY|?||")
    _, status, actions, errs = (line.split("|") + ["", "", ""])[:4]
    return status, actions, errs


def sender_view(out: str) -> str:
    """What the sender received, from send.py's output: MSA-1 and who built the ACK (IRIS or the lab)."""
    ans = out.split("ANSWER TO THE SENDER", 1)[-1]
    if "MSA|" in ans:
        code = ans.split("MSA|", 1)[1].split("|", 1)[0].strip()
        who = "lab" if "|LAB|SIM|" in ans else "IRIS"
        return f"{code} ({who})"
    if "<nothing>" in ans:
        return "nothing"
    return "byte 0x06" if "\x06" in ans else "?"


def lab_events(ctrl):
    p = current_log()
    ev = [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
    return [e for e in ev if e.get("control_id") == ctrl]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=",".join(CASES))
    ap.add_argument("--modes", default=",".join(MODES))
    ap.add_argument("--out", default=str(ROOT / "results" / "matrix.md"), help="default: results/matrix.md (the committed reference!)")
    ap.add_argument("--no-dashboard", action="store_true")
    a = ap.parse_args()
    cases = [c for c in a.cases.split(",") if c in CASES]
    rows = []
    run = time.strftime("%H%M%S")
    for case in cases:
        for mode in a.modes.split(","):
            port, ackmode, op, ackargs = CASES[case]
            ctrl = f"{case.replace('+', '_')}-{mode}-{run}"
            t0 = time.time()
            sent = subprocess.run([sys.executable, "-B", "-I", str(ROOT / "tools/send.py"), "localhost", str(port), mode, ctrl, *ackargs],
                                  capture_output=True, text=True, check=True,
                                  env={"SEND_WAIT": str(SEND_WAIT), "PATH": "/usr/bin:/bin"}).stdout
            received = sender_view(sent)
            # wait for IRIS to finish with the message (terminal status), max 60 s
            status = actions = errs = ""
            while time.time() - t0 < 60:
                time.sleep(2)
                status, actions, errs = summary(ctrl)
                if status in TERMINAL:
                    break
            took = time.time() - t0
            if mode == "LATE":
                time.sleep(LATE_DELAY + 8)   # let the lab finish both late replies (one per attempt) ...
                iris(f'do ##class(Repro.Trace).ResetOperation("{op}")')   # ... and drop the stale bytes from IRIS' socket
            deliveries = sum(1 for e in lab_events(ctrl) if e["event"] == "received")
            acks = sum(1 for e in lab_events(ctrl) if e["event"] == "ack_sent")
            rows.append((case, ackmode, mode, deliveries, acks, status, actions, received, f"{took:.0f}s"))
            print(f"{case:16} {mode:8} deliveries={deliveries} acks={acks} final={status} actions={actions} sender={received}", flush=True)
    md = ["| case | AckMode | lab mode | deliveries | ACKs sent by lab | final status | action codes logged | sender receives | wall time |",
          "|---|---|---|---:|---:|---|---|---|---:|"]
    for r in rows:
        md.append("| " + " | ".join(str(x) for x in r) + " |")
    Path(a.out).write_text("\n".join(md) + "\n")
    print("\n" + "\n".join(md))
    if not a.no_dashboard:       # dashboard<date>.html next to the log the run just wrote
        subprocess.run([sys.executable, "-B", "-I", str(ROOT / "tools" / "dashboard.py")], check=False)


if __name__ == "__main__":
    main()
