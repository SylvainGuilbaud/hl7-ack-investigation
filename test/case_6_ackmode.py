#!/usr/bin/env python3
"""Case 6 - AckMode: what the SENDER receives.
Cases 1-5 used AckMode=Immed, where the sender only ever sees IRIS' own 'MSA|CA'. With AckMode=App the service
waits for the operation and answers with the downstream ACK - but only if the operation *completes*.
When the operation fails or suspends, IRIS builds its own CE or sends nothing. The real downstream ACK (MSH-3 LAB)
is what the sender sees only in the 'sender_has LAB' tests."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from harness import *
print("# Case 6 ackmode\n\n> Case 6 - AckMode: what the SENDER receives.\n> Cases 1-5 used AckMode=Immed, where the sender only ever sees IRIS' own 'MSA|CA'. With AckMode=App the service\n> waits for the operation and answers with the downstream ACK - but only if the operation *completes*.\n> When the operation fails or suspends, IRIS builds its own CE or sends nothing. The real downstream ACK (MSH-3 LAB)\n> is what the sender sees only in the 'sender_has LAB' tests.\n")
# --- AckMode=App ------------------------------------------------------------------------------
run("app.default", "AA", "App: the lab's real AA is forwarded to the sender",
    dict(deliveries=1, status="Completed", sender_has=["MSH|^~\\&|LAB|SIM", "MSA|AA"]))
run("app.default", "AR", "App + default: the sender waits for the retries, then gets IRIS' own CE - never the lab's AR",
    dict(deliveries=retried, status="Error", actions="RF", sender_has="MSA|CE", sender_lacks=["MSA|AR", "|LAB|SIM"]))
run("app.failrej", "AR", "App + :?R=F: no retry, the sender gets IRIS' own CE immediately",
    dict(deliveries=1, status="Error", actions="F", sender_has="MSA|CE", sender_lacks="MSA|AR"))
run("app.legacy", "AR", "App + legacy string: the lab's real AR reaches the sender (operation 'Completed')",
    dict(deliveries=1, status="Completed", actions="CW", sender_has=["|LAB|SIM", "MSA|AR"]))
run("app.failrej", "AE", "App + suspended message: the sender receives NO ACK (waits; here it gives up after 15 s)",
    dict(deliveries=1, status="Suspended", actions="S", sender_has="<nothing>"), wait=15)
# --- other AckModes ---------------------------------------------------------------------------
run("msh.failrej", "AR", "Msh, MSH-15=AL: commit ACK (CA) sent at once - the rejection is invisible to the sender",
    dict(deliveries=1, status="Error", actions="F", sender_has="MSA|CA"), ack=("AL", "NE"))
run("msh.failrej", "AR", "Msh, MSH-16=AL: application ACK requested, IRIS builds a CE",
    dict(deliveries=1, status="Error", actions="F", sender_has="MSA|CE"), ack=("NE", "AL"))
run("msh.failrej", "AR", "Msh, no ACK requested in the message: nothing comes back",
    dict(deliveries=1, status="Error", actions="F", sender_has="<nothing>"), wait=10)
run("never.failrej", "AR", "Never: nothing comes back",
    dict(deliveries=1, status="Error", actions="F", sender_has="<nothing>"), wait=10)
run("byte.failrej", "AR", "Byte: a single 0x06 ('OK') byte although the lab rejected the message",
    dict(deliveries=1, status="Error", actions="F", sender_has="\x06"), wait=10)
finish()
