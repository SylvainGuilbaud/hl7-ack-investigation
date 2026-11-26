#!/usr/bin/env python3
"""Case 4 - the ACK reached IRIS' socket but never became a usable ACK.
Retry (if any) comes from the connection logic, NOT from ReplyCodeActions: no 'Action code' in the log."""
import sys; sys.dont_write_bytecode = True; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from harness import *
print("# Case 4 ack not recognised\n\n> Case 4 - the ACK reached IRIS' socket but never became a usable ACK.\n> Retry (if any) comes from the connection logic, NOT from ReplyCodeActions: no 'Action code' in the log.\n")
run("failrej", "NOFRAME", "ACK without MLLP end block: ErrEndBlock, not retried",            dict(deliveries=1, status="Error", no_actions=1))
run("failrej", "CLOSE",   "Socket closed without ACK: reconnect and resend until FailureTimeout", dict(deliveries=retried, status="Error", no_actions=1))
run("failrej", "LATE",    "ACK after 12 s > ResponseTimeout 5 s: read timeout, resent",       dict(deliveries=retried, status="Error", no_actions=1))
finish()
