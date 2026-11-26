#!/usr/bin/env python3
"""Case 1 - the symptom: the lab answers AR (a valid ACK) and the message is sent again and again.
Default ReplyCodeActions contains :?R=RF  => Retry until FailureTimeout, then Fail."""
import sys; sys.dont_write_bytecode = True; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from harness import *
print('# Case 1 reject is retried\n\n> Case 1 - the symptom: the lab answers AR (a valid ACK) and the message is sent again and again.\n> Default ReplyCodeActions contains :?R=RF  => Retry until FailureTimeout, then Fail.\n')
run("default", "AR",  "AR ACK under the documented default is retried",           dict(deliveries=retried, status="Error", actions="RF"))
run("default", "AR3", "Same with MSH-9 = ACK^A28^ACK (three components)",         dict(deliveries=retried, status="Error", actions="RF"))
finish()
