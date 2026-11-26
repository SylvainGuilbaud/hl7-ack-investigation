# Case 6 ackmode

> Case 6 - AckMode: what the SENDER receives.
> Cases 1-5 used AckMode=Immed, where the sender only ever sees IRIS' own 'MSA|CA'. With AckMode=App the service
> waits for the operation and answers with the downstream ACK - but only if the operation *completes*.
> When the operation fails or suspends, IRIS builds its own CE or sends nothing. The real downstream ACK (MSH-3 LAB)
> is what the sender sees only in the 'sender_has LAB' tests.

## App: the lab's real AA is forwarded to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AA` | `app.default-AA-191159` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126191159||ADT^A28^ADT_A05|app.default-AA-191159|P|2.5
    EVN|A28|20261126191159
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126181159||ACK|ACKapp.default-AA-191159|P|2.5
    MSA|AA|app.default-AA-191159
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:59.302 | received |  | `` |
| 18:11:59.304 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 143)
 143 18:11:59.301 in.app.default -> out.default  [Request/9] 
 144 18:11:59.305 out.default -> in.app.default  [Response/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

## App + default: the sender waits for the retries, then gets IRIS' own CE - never the lab's AR

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AR` | `app.default-AR-191201` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191201||ADT^A28^ADT_A05|app.default-AR-191201|P|2.5
    EVN|A28|20261126191201
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.1s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261912||ACK^A28|app.default-AR-191201|P|2.5
    MSA|CE|app.default-AR-191201
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:01.489 | received |  | `` |
| 18:12:01.494 | ack_sent | AR | `ACK` |
| 18:12:03.501 | received |  | `` |
| 18:12:03.506 | ack_sent | AR | `ACK` |
| 18:12:05.511 | received |  | `` |
| 18:12:05.519 | ack_sent | AR | `ACK` |
| 18:12:07.525 | received |  | `` |
| 18:12:07.529 | ack_sent | AR | `ACK` |
| 18:12:09.535 | received |  | `` |
| 18:12:09.539 | ack_sent | AR | `ACK` |
| 18:12:11.550 | received |  | `` |
| 18:12:11.552 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 145)
 145 18:12:01.488 in.app.default -> out.default  [Request/8] 
 146 18:12:11.554 out.default -> in.app.default  [Response/9] 
== event log
18:12:01.495 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 449 because response 10@EnsLib.HL7.Message / 450 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:12:03.507 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 449 because response 13@EnsLib.HL7.Message / 451 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:12:05.522 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 449 because response 10@EnsLib.HL7.Message / 452 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:12:07.53 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 449 because response 13@EnsLib.HL7.Message / 453 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:12:09.54 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 449 because response 10@EnsLib.HL7.Message / 454 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:12:11.542 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
18:12:11.543 INFO [out.default] Disconnecting from  lab:6600
18:12:11.546 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:12:11.553 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 449 because response 13@EnsLib.HL7.Message / 455 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:12:11.554 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
18:12:11.556 WARNING [in.app.default] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/449 returned with no response object and status: ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## App + :?R=F: no retry, the sender gets IRIS' own CE immediately

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AR` | `app.failrej-AR-191213` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191213||ADT^A28^ADT_A05|app.failrej-AR-191213|P|2.5
    EVN|A28|20261126191213
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261912||ACK^A28|app.failrej-AR-191213|P|2.5
    MSA|CE|app.failrej-AR-191213
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:13.792 | received |  | `` |
| 18:12:13.795 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 147)
 147 18:12:13.789 in.app.failrej -> out.failrej  [Request/8] 
 148 18:12:13.796 out.failrej -> in.app.failrej  [Response/9] 
== event log
18:12:13.796 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 457 because response 12@EnsLib.HL7.Message / 458 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting 
18:12:13.798 WARNING [in.app.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/457 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 457 bec
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## App + legacy string: the lab's real AR reaches the sender (operation 'Completed')

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.legacy` | 29213 | `AR` | `app.legacy-AR-191215` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191215||ADT^A28^ADT_A05|app.legacy-AR-191215|P|2.5
    EVN|A28|20261126191215
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126181215||ACK|ACKapp.legacy-AR-191215|P|2.5
    MSA|AR|app.legacy-AR-191215|Rejected
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:15.989 | received |  | `` |
| 18:12:15.992 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 149)
 149 18:12:15.987 in.app.legacy -> out.legacy  [Request/9] 
 150 18:12:15.993 out.legacy -> in.app.legacy  [Response/9] 
== event log
18:12:15.993 WARNING [out.legacy] Warning on HL7 Message body 12@EnsLib.HL7.Message / 460 because response 10@EnsLib.HL7.Message / 461 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## App + suspended message: the sender receives NO ACK (waits; here it gives up after 15 s)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AE` | `app.failrej-AE-191218` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126191218||ADT^A28^ADT_A05|app.failrej-AE-191218|P|2.5
    EVN|A28|20261126191218
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 15.0s) (no complete MLLP frame within 15s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:18.179 | received |  | `` |
| 18:12:18.182 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 151)
 151 18:12:18.178 in.app.failrej -> out.failrej  [Request/5] 
== event log
18:12:18.183 ERROR [out.failrej] ERROR <Ens>ErrSuspending: Suspending message 151 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 8@EnsLib.HL7.Message / 462 because response 11@EnsLib.HL7.Message / 463 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## Msh, MSH-15=AL: commit ACK (CA) sent at once - the rejection is invisible to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-191235` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191235||ADT^A28^ADT_A05|msh.failrej-AR-191235|P|2.5|||AL|NE
    EVN|A28|20261126191235
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261912||ACK^A28|msh.failrej-AR-191235|P|2.5
    MSA|CA|msh.failrej-AR-191235
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:35.380 | received |  | `` |
| 18:12:35.383 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 152)
 152 18:12:35.379 in.msh.failrej -> out.failrej  [Request/8] 
== event log
18:12:35.384 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 464 because response 10@EnsLib.HL7.Message / 466 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Msh, MSH-16=AL: application ACK requested, IRIS builds a CE

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-191237` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191237||ADT^A28^ADT_A05|msh.failrej-AR-191237|P|2.5|||NE|AL
    EVN|A28|20261126191237
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261912||ACK^A28|msh.failrej-AR-191237|P|2.5
    MSA|CE|msh.failrej-AR-191237
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:37.563 | received |  | `` |
| 18:12:37.566 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 153)
 153 18:12:37.562 in.msh.failrej -> out.failrej  [Request/8] 
 154 18:12:37.567 out.failrej -> in.msh.failrej  [Response/9] 
== event log
18:12:37.567 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 467 because response 9@EnsLib.HL7.Message / 468 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting 
18:12:37.568 WARNING [in.msh.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/467 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 467 be
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## Msh, no ACK requested in the message: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-191239` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191239||ADT^A28^ADT_A05|msh.failrej-AR-191239|P|2.5
    EVN|A28|20261126191239
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.0s) (no complete MLLP frame within 10s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:39.884 | received |  | `` |
| 18:12:39.888 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 155)
 155 18:12:39.883 in.msh.failrej -> out.failrej  [Request/8] 
== event log
18:12:39.889 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 12@EnsLib.HL7.Message / 470 because response 8@EnsLib.HL7.Message / 471 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Never: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `never.failrej` | 29215 | `AR` | `never.failrej-AR-191252` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191252||ADT^A28^ADT_A05|never.failrej-AR-191252|P|2.5
    EVN|A28|20261126191252
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.0s) (no complete MLLP frame within 10s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:12:52.112 | received |  | `` |
| 18:12:52.117 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 156)
 156 18:12:52.107 in.never.failrej -> out.failrej  [Request/8] 
== event log
18:12:52.118 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 472 because response 11@EnsLib.HL7.Message / 473 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Byte: a single 0x06 ('OK') byte although the lab rejected the message

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `byte.failrej` | 29216 | `AR` | `byte.failrej-AR-191304` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191304||ADT^A28^ADT_A05|byte.failrej-AR-191304|P|2.5
    EVN|A28|20261126191304
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:13:04.339 | received |  | `` |
| 18:13:04.347 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 157)
 157 18:13:04.337 in.byte.failrej -> out.failrej  [Request/8] 
== event log
18:13:04.349 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 474 because response 13@EnsLib.HL7.Message / 475 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
