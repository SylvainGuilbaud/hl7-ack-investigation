#!/usr/bin/env python3
"""Case 2 - the correction: only RF -> F for :?R. Same ACK, one delivery, error stays visible."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from harness import *
print('# Case 2 corrected\n\n> Case 2 - the correction: only RF -> F for :?R. Same ACK, one delivery, error stays visible.\n')
run("failrej", "AR",  "AR ACK with :?R=F is delivered once",  dict(deliveries=1, status="Error", actions="F"))
run("failrej", "AR3", "Same with ACK^A28^ACK",                dict(deliveries=1, status="Error", actions="F"))
run("failrej", "AA",  "Control: AA still completes normally", dict(deliveries=1, status="Completed"))
finish()
