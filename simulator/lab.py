#!/usr/bin/env python3
"""Synthetic downstream HL7 receiver ("the LAB").

It listens on one MLLP port and decides how to answer each message from the
*receiving facility* field (MSH-6) of the message it receives, e.g. MSH-6 = AR.
Every message received is appended to a JSON-lines file, so the number of
deliveries per control id can be counted independently of IRIS.

stdlib only.
"""
import json, os, socket, sys, threading, time
from datetime import datetime

VT, FS, CR = b"\x0b", b"\x1c", b"\x0d"
PORT = int(os.environ.get("LAB_PORT", "6600"))
LATE_DELAY = float(os.environ.get("LATE_DELAY", "12"))   # seconds, for mode LATE
# One log per lab container start: results/dashboard/lab<YYYY-MM-DD>.jsonl (appended to if it already exists).
# results/dashboard/ is git-ignored; results/lab.jsonl is the committed reference the article quotes: never written here.
LOG = os.environ.get("LAB_LOG") or f"/results/dashboard/lab{datetime.now():%Y-%m-%d}.jsonl"
lock = threading.Lock()
conn_seq = 0

MODES = {
    "AA":     "plain ACK, MSA|AA",
    "AE":     "application error, MSA|AE",
    "AR":     "application reject, MSA|AR",
    "AR3":    "MSA|AR, MSH-9 = ACK^A28^ACK (three components)",
    "OTHERID": "MSA|AA, but MSA-2 is the control id of ANOTHER message (an ACK that is not for this message)",
    "NOMSA":  "reply has no MSA segment at all",
    "LATE":   "MSA|AA, but only after LATE_DELAY seconds",
    "NOFRAME":"MSA|AA bytes sent without the MLLP end block (0x1C 0x0D)",
    "CLOSE":  "read the message, close the socket, send nothing",
}


def now(fmt="%Y%m%d%H%M%S"):
    return datetime.now().strftime(fmt)


def ack(ctrl_id, code, msh9="ACK", msa2=None, text=""):
    msa2 = ctrl_id if msa2 is None else msa2
    return "\r".join([
        f"MSH|^~\\&|LAB|SIM|IRIS|HOSP|{now()}||{msh9}|ACK{ctrl_id}|P|2.5",
        f"MSA|{code}|{msa2}" + (f"|{text}" if text else ""),
    ])


def frame(msg: str) -> bytes:
    return VT + msg.encode() + FS + CR


def record(**kw):
    kw["ts"] = datetime.now().isoformat(timespec="milliseconds")
    with lock, open(LOG, "a") as f:
        f.write(json.dumps(kw) + "\n")


def field(msg: str, seg: str, idx: int) -> str:
    for line in msg.split("\r"):
        if line.startswith(seg + "|"):
            p = line.split("|")
            # MSH-1 is the separator itself, so MSH-n sits at index n-1
            i = idx - 1 if seg == "MSH" else idx
            return p[i] if i < len(p) else ""
    return ""


def handle(sock, peer, cid):
    buf = b""
    try:
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                record(event="peer_closed", conn=cid)
                return
            buf += chunk
            while FS in buf:
                raw, buf = buf.split(FS, 1)
                buf = buf.lstrip(CR)
                msg = raw.lstrip(VT).decode(errors="replace")
                ctrl = field(msg, "MSH", 10)
                mode = field(msg, "MSH", 6).strip().upper() or "AA"
                record(event="received", conn=cid, control_id=ctrl, mode=mode)
                reply_to(sock, cid, ctrl, mode)
    except OSError as e:
        record(event="socket_error", conn=cid, error=str(e))
    finally:
        sock.close()


def reply_to(sock, cid, ctrl, mode):
    if mode == "CLOSE":
        record(event="closing_without_ack", conn=cid, control_id=ctrl)
        sock.shutdown(socket.SHUT_RDWR)
        return
    if mode == "LATE":
        time.sleep(LATE_DELAY)
    msg = {
        "AE":    lambda: ack(ctrl, "AE", text="Application error"),
        "AR":    lambda: ack(ctrl, "AR", text="Rejected"),
        "AR3":   lambda: ack(ctrl, "AR", msh9="ACK^A28^ACK", text="Rejected"),
        "OTHERID": lambda: ack(ctrl, "AA", msa2="OTHER-" + ctrl),
        "NOMSA": lambda: "\r".join([f"MSH|^~\\&|LAB|SIM|IRIS|HOSP|{now()}||ACK|ACK{ctrl}|P|2.5", "ERR|^^^207"]),
    }.get(mode, lambda: ack(ctrl, "AA"))()
    data = frame(msg)
    if mode == "NOFRAME":
        data = VT + msg.encode()
    try:
        sock.sendall(data)
        record(event="ack_sent", conn=cid, control_id=ctrl, mode=mode,
               msa1=field(msg, "MSA", 1), msh9=field(msg, "MSH", 9))
    except OSError as e:
        record(event="ack_send_failed", conn=cid, control_id=ctrl, mode=mode, error=str(e))


def main():
    global conn_seq
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(os.path.join(os.path.dirname(LOG), ".lab-current"), "w") as f:   # tells the tools which log is live
        f.write(os.path.basename(LOG))
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(16)
    print(f"lab simulator listening on {PORT}, log={LOG}", flush=True)
    while True:
        s, peer = srv.accept()
        conn_seq += 1
        record(event="connected", conn=conn_seq, peer=peer[0])
        threading.Thread(target=handle, args=(s, peer, conn_seq), daemon=True).start()


if __name__ == "__main__":
    main()
