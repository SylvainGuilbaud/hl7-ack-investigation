#!/usr/bin/env python3
"""Case 5 - what the default does with other ACK content.
OTHERID: a well-formed AA whose MSA-2 is the control id of ANOTHER message (e.g. a stale ACK). It is not a retry case:
it shows that the default accepts it silently, because :?A=C matches before :I?=W is reached."""
import sys; sys.dont_write_bytecode = True; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from harness import *
print('# Case 5 ack content checks\n\n> Case 5 - what the default does with other ACK content.\n> OTHERID: a well-formed AA whose MSA-2 is the control id of ANOTHER message (e.g. a stale ACK). It is not a retry case:\n> it shows that the default accepts it silently, because :?A=C matches before :I?=W is reached.\n')
run("default", "AE",    "AE: suspended (:?E=S), not retried",                       dict(deliveries=1, status="Suspended", actions="S"))
run("default", "NOMSA", "No MSA: suspended (:~=S)",                                 dict(deliveries=1, status="Suspended", actions="S"))
run("default", "OTHERID", "AA that acknowledges ANOTHER message (MSA-2 mismatch): Completed, no warning (:?A=C matches before :I?=W)",
    dict(deliveries=1, status="Completed", no_actions=1))
finish()
