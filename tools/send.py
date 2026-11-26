#!/usr/bin/env python3
"""Send one synthetic ADT^A28 over MLLP and print the ACK that comes back.

usage: send.py HOST PORT MODE CONTROL_ID [MSH-15 [MSH-16]]   (accept / application ACK type, e.g. AL NE)
MODE goes into MSH-6; the downstream lab simulator reads it to decide how to answer.
"""
import socket, sys
from datetime import datetime

host, port, mode, ctrl = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
ack15, ack16 = (sys.argv[5:7] + ["", ""])[:2]
now = datetime.now().strftime("%Y%m%d%H%M%S")
msg = "\r".join([
    f"MSH|^~\\&|PAS|HOSP|IRIS|{mode}|{now}||ADT^A28^ADT_A05|{ctrl}|P|2.5" + (f"|||{ack15}|{ack16}" if ack15 or ack16 else ""),
    f"EVN|A28|{now}",
    "PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F",
    "PV1|1|N",
])
import os
WAIT = float(os.environ.get("SEND_WAIT", "40"))   # seconds to wait for an answer
s = socket.create_connection((host, port), timeout=WAIT)
s.sendall(b"\x0b" + msg.encode() + b"\x1c\x0d")
buf, note = b"", ""
t0 = datetime.now()
try:
    while b"\x1c" not in buf:
        c = s.recv(4096)
        if not c:
            note = "(connection closed by IRIS)"
            break
        buf += c
except socket.timeout:
    note = f"(no complete MLLP frame within {WAIT:.0f}s)"
took = (datetime.now() - t0).total_seconds()
show = lambda b: b.replace(b"\x0b", b"").replace(b"\x1c", b"").replace(b"\r", b"\n    ").decode(errors="replace").strip()
print("SENT:\n    " + show(msg.encode()))
print(f"ANSWER TO THE SENDER (after {took:.1f}s) {note}:")
print("    " + (show(buf) if buf and buf[:1] == b"\x0b" else (f"raw bytes {buf!r}" if buf else "<nothing>")))
