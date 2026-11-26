#!/usr/bin/env python3
"""Case 3 - the 'inherited' string :?R=W,:?E=W,... stops the retries but hides the rejection:
the message ends Completed (action CW) although the receiver rejected it."""
import sys; sys.dont_write_bytecode = True; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from harness import *
print("# Case 3 swallowed rejection\n\n> Case 3 - the 'inherited' string :?R=W,:?E=W,... stops the retries but hides the rejection:\n> the message ends Completed (action CW) although the receiver rejected it.\n")
run("legacy", "AR", "AR under the legacy string completes with a warning", dict(deliveries=1, status="Completed", actions="CW"))
run("legacy", "AE", "AE under the legacy string completes with a warning", dict(deliveries=1, status="Completed", actions="CW"))
run("legacy", "NOMSA", "Reply without MSA falls to :~=F",                   dict(deliveries=1, status="Error", actions="F"))
finish()
