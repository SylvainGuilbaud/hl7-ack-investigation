#!/usr/bin/env python3
"""Run the test matrix: every (case, simulator mode) pair, then print a Markdown table.

For each cell it sends one message, waits until IRIS has finished with it, then reads
  - how many times the lab simulator RECEIVED it   (the lab's current log results/dashboard/lab<date>.jsonl, independent of IRIS)
  - the final status and the ReplyCodeActions action codes IRIS logged (Repro.Trace.Summary)

Rows = every inbound service of the production (ReplyCodeActions x AckMode), columns = what the lab does.
Cells run IN PARALLEL, one worker per operation (out.default, out.failrej, out.legacy): the cells of one operation run
one after the other, and every cell holds that operation's lock (tools/labpath.py, operation_lock), so it also
cannot collide with test/run_all.sh or a hand-made test. Use --serial for one cell at a time.

usage: matrix.py [--cases a,b] [--modes AA,AR] [--out results/dashboard/matrix.md] [--serial]
       The default --out, results/matrix.md, is the COMMITTED reference the article quotes: pass --out for your own runs.
"""
import argparse, subprocess, sys, time, os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True      # no __pycache__ in the repo
sys.path.insert(0, str(ROOT / "tools"))
from labpath import lab_events, operation_lock, wait_late_replies
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
POLL = 0.5          # seconds between two looks at IRIS while a message is being processed


def send_wait(case):
    """How long the SENDER waits for an answer. Services that answer at once (Immed, Msh with MSH-15, Byte) or never
    (Msh without a request, Never) need only a few seconds. The ones that wait for the operation (App, and Msh with
    MSH-16) can answer only after its retries, about 10 s (FailureTimeout), so they get a longer wait."""
    return 15 if CASES[case][1] == "App" or case == "msh.failrej+App" else 5

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


def run_cell(case, mode, run):
    """One message through one service; returns the table row. The caller holds the operation's lock."""
    port, ackmode, op, ackargs = CASES[case]
    ctrl = f"{case.replace('+', '_')}-{mode}-{run}"
    t0 = time.time()
    sent = subprocess.run([sys.executable, "-B", "-I", str(ROOT / "tools/send.py"), "localhost", str(port), mode, ctrl, *ackargs],
                          capture_output=True, text=True, check=True,
                          env={"SEND_WAIT": str(send_wait(case)), "PATH": "/usr/bin:/bin"}).stdout
    received = sender_view(sent)
    # wait for IRIS to finish with the message (terminal status), max 60 s
    status = actions = errs = ""
    while time.time() - t0 < 60:
        time.sleep(POLL)
        status, actions, errs = summary(ctrl)
        if status in TERMINAL:
            break
    took = time.time() - t0
    if mode == "LATE":
        wait_late_replies(ctrl, LATE_DELAY, POLL)                     # the lab has sent both late replies ...
        iris(f'do ##class(Repro.Trace).ResetOperation("{op}")')       # ... drop the stale bytes from IRIS' socket
    ev = lab_events(ctrl)
    deliveries = sum(1 for e in ev if e["event"] == "received")
    acks = sum(1 for e in ev if e["event"] == "ack_sent")
    print(f"{case:16} {mode:8} deliveries={deliveries} acks={acks} final={status} actions={actions} sender={received}", flush=True)
    return (case, ackmode, mode, deliveries, acks, status, actions, received, f"{took:.0f}s")


def lane(cells, run):
    """The cells of ONE operation, in order. Returns {(case, mode): row}."""
    out = {}
    for case, mode in cells:
        with operation_lock(CASES[case][2]):
            out[(case, mode)] = run_cell(case, mode, run)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=",".join(CASES))
    ap.add_argument("--modes", default=",".join(MODES))
    ap.add_argument("--out", default=str(ROOT / "results" / "matrix.md"), help="default: results/matrix.md (the committed reference!)")
    ap.add_argument("--serial", action="store_true", help="one cell at a time (default: one worker per operation)")
    ap.add_argument("--no-dashboard", action="store_true")
    a = ap.parse_args()
    cases = [c for c in a.cases.split(",") if c in CASES]
    modes = a.modes.split(",")
    order = [(c, m) for c in cases for m in modes]
    run = time.strftime("%H%M%S")
    t0 = time.time()

    lanes = {}                                    # operation -> its cells, in table order
    for c, m in order:
        lanes.setdefault(CASES[c][2], []).append((c, m))
    if a.serial:
        lanes = {"all": order}
    print(f"{len(order)} cells, {len(lanes)} worker(s): " + ", ".join(f"{op} ({len(v)})" for op, v in lanes.items()), flush=True)
    results = {}
    with ThreadPoolExecutor(max_workers=max(1, len(lanes))) as pool:
        for part in pool.map(lambda cells: lane(cells, run), lanes.values()):
            results.update(part)

    rows = [results[k] for k in order]
    md = ["| case | AckMode | lab mode | deliveries | ACKs sent by lab | final status | action codes logged | sender receives | wall time |",
          "|---|---|---|---:|---:|---|---|---|---:|"]
    for r in rows:
        md.append("| " + " | ".join(str(x) for x in r) + " |")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(md) + "\n")
    print("\n" + "\n".join(md))
    print(f"\n{len(rows)} cells in {time.time() - t0:.0f} s ({'serial' if a.serial else 'parallel, one worker per operation'}) -> {a.out}")
    if not a.no_dashboard:       # dashboard<date>.html next to the log the run just wrote
        subprocess.run([sys.executable, "-B", "-I", str(ROOT / "tools" / "dashboard.py")], check=False)


if __name__ == "__main__":
    main()
