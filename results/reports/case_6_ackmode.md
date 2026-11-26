# Case 6 ackmode

> Case 6 - AckMode: what the SENDER receives.
> Cases 1-5 used AckMode=Immed, where the sender only ever sees IRIS' own 'MSA|CA'. With AckMode=App the service
> waits for the operation and answers with the downstream ACK - but only if the operation *completes*.
> When the operation fails or suspends, IRIS builds its own CE or sends nothing. The real downstream ACK (MSH-3 LAB)
> is what the sender sees only in the 'sender_has LAB' tests.

## App: the lab's real AA is forwarded to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AA` | `app.default-AA-20040178` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126200401||ADT^A28^ADT_A05|app.default-AA-20040178|P|2.5
    EVN|A28|20261126200401
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126190401||ACK|ACKapp.default-AA-20040178|P|2.5
    MSA|AA|app.default-AA-20040178
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:01.825 | received |  | `` |
| 19:04:01.830 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 288)
 288 19:04:01.824 in.app.default -> out.default  [Request/9] 
 289 19:04:01.831 out.default -> in.app.default  [Response/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

## App + default: the sender waits for the retries, then gets IRIS' own CE - never the lab's AR

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AR` | `app.default-AR-20041444` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200414||ADT^A28^ADT_A05|app.default-AR-20041444|P|2.5
    EVN|A28|20261126200414
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.1s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|app.default-AR-20041444|P|2.5
    MSA|CE|app.default-AR-20041444
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:14.501 | received |  | `` |
| 19:04:14.509 | ack_sent | AR | `ACK` |
| 19:04:16.515 | received |  | `` |
| 19:04:16.520 | ack_sent | AR | `ACK` |
| 19:04:18.522 | received |  | `` |
| 19:04:18.525 | ack_sent | AR | `ACK` |
| 19:04:20.531 | received |  | `` |
| 19:04:20.536 | ack_sent | AR | `ACK` |
| 19:04:22.544 | received |  | `` |
| 19:04:22.552 | ack_sent | AR | `ACK` |
| 19:04:24.568 | received |  | `` |
| 19:04:24.574 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 301)
 301 19:04:14.5 in.app.default -> out.default  [Request/8] 
 307 19:04:24.577 out.default -> in.app.default  [Response/9] 
== event log
19:04:14.51 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 771 because response 9@EnsLib.HL7.Message / 772 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
19:04:16.52 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 771 because response 11@EnsLib.HL7.Message / 777 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:18.526 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 771 because response 9@EnsLib.HL7.Message / 783 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:20.537 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 771 because response 11@EnsLib.HL7.Message / 784 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
19:04:22.553 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 771 because response 9@EnsLib.HL7.Message / 785 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:24.555 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
19:04:24.555 INFO [out.default] Disconnecting from  lab:6600
19:04:24.557 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:24.575 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 771 because response 11@EnsLib.HL7.Message / 786 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
19:04:24.576 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
19:04:24.579 WARNING [in.app.default] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/771 returned with no response object and status: ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## App + :?R=F: no retry, the sender gets IRIS' own CE immediately

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AR` | `app.failrej-AR-20044475` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200444||ADT^A28^ADT_A05|app.failrej-AR-20044475|P|2.5
    EVN|A28|20261126200444
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|app.failrej-AR-20044475|P|2.5
    MSA|CE|app.failrej-AR-20044475
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:44.802 | received |  | `` |
| 19:04:44.805 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 319)
 319 19:04:44.801 in.app.failrej -> out.failrej  [Request/8] 
 320 19:04:44.807 out.failrej -> in.app.failrej  [Response/9] 
== event log
19:04:44.806 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 804 because response 10@EnsLib.HL7.Message / 805 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting 
19:04:44.809 WARNING [in.app.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/804 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 804 bec
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## App + legacy string: the lab's real AR reaches the sender (operation 'Completed')

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.legacy` | 29213 | `AR` | `app.legacy-AR-20044545` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200445||ADT^A28^ADT_A05|app.legacy-AR-20044545|P|2.5
    EVN|A28|20261126200445
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126190445||ACK|ACKapp.legacy-AR-20044545|P|2.5
    MSA|AR|app.legacy-AR-20044545|Rejected
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:45.505 | received |  | `` |
| 19:04:45.511 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 322)
 322 19:04:45.503 in.app.legacy -> out.legacy  [Request/9] 
 323 19:04:45.511 out.legacy -> in.app.legacy  [Response/9] 
== event log
19:04:45.511 WARNING [out.legacy] Warning on HL7 Message body 12@EnsLib.HL7.Message / 808 because response 11@EnsLib.HL7.Message / 810 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## App + suspended message: the sender receives NO ACK (it waits; here the test gives up after 5 s)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AE` | `app.failrej-AE-20050108` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126200501||ADT^A28^ADT_A05|app.failrej-AE-20050108|P|2.5
    EVN|A28|20261126200501
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 5.0s) (no complete MLLP frame within 5s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:05:01.134 | received |  | `` |
| 19:05:01.140 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 326)
 326 19:05:01.133 in.app.failrej -> out.failrej  [Request/5] 
== event log
19:05:01.14 ERROR [out.failrej] ERROR <Ens>ErrSuspending: Suspending message 326 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 12@EnsLib.HL7.Message / 822 because response 11@EnsLib.HL7.Message / 823 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## Msh, MSH-15=AL: commit ACK (CA) sent at once - the rejection is invisible to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-20051242` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200512||ADT^A28^ADT_A05|msh.failrej-AR-20051242|P|2.5|||AL|NE
    EVN|A28|20261126200512
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262005||ACK^A28|msh.failrej-AR-20051242|P|2.5
    MSA|CA|msh.failrej-AR-20051242
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:05:12.483 | received |  | `` |
| 19:05:12.489 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 333)
 333 19:05:12.48 in.msh.failrej -> out.failrej  [Request/8] 
== event log
19:05:12.49 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 833 because response 9@EnsLib.HL7.Message / 835 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting i
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Msh, MSH-16=AL: application ACK requested, IRIS builds a CE

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-20052393` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200523||ADT^A28^ADT_A05|msh.failrej-AR-20052393|P|2.5|||NE|AL
    EVN|A28|20261126200523
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262005||ACK^A28|msh.failrej-AR-20052393|P|2.5
    MSA|CE|msh.failrej-AR-20052393
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:05:23.994 | received |  | `` |
| 19:05:24.001 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 337)
 337 19:05:23.987 in.msh.failrej -> out.failrej  [Request/8] 
 338 19:05:24.002 out.failrej -> in.msh.failrej  [Response/9] 
== event log
19:05:23.989 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:05:24.002 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 839 because response 12@EnsLib.HL7.Message / 840 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
19:05:24.003 WARNING [in.msh.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/839 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 839 be
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## Msh, no ACK requested in the message: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-20055010` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200550||ADT^A28^ADT_A05|msh.failrej-AR-20055010|P|2.5
    EVN|A28|20261126200550
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 5.0s) (no complete MLLP frame within 5s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:05:50.162 | received |  | `` |
| 19:05:50.169 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 348)
 348 19:05:50.16 in.msh.failrej -> out.failrej  [Request/8] 
== event log
19:05:50.17 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 850 because response 12@EnsLib.HL7.Message / 851 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting i
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Never: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `never.failrej` | 29215 | `AR` | `never.failrej-AR-20055644` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200556||ADT^A28^ADT_A05|never.failrej-AR-20055644|P|2.5
    EVN|A28|20261126200556
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 5.0s) (no complete MLLP frame within 5s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:05:56.523 | received |  | `` |
| 19:05:56.545 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 350)
 350 19:05:56.522 in.never.failrej -> out.failrej  [Request/8] 
== event log
19:05:56.547 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 855 because response 10@EnsLib.HL7.Message / 856 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Byte: a single 0x06 ('OK') byte although the lab rejected the message

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `byte.failrej` | 29216 | `AR` | `byte.failrej-AR-20060312` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200603||ADT^A28^ADT_A05|byte.failrej-AR-20060312|P|2.5
    EVN|A28|20261126200603
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:06:03.183 | received |  | `` |
| 19:06:03.191 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 354)
 354 19:06:03.182 in.byte.failrej -> out.failrej  [Request/8] 
== event log
19:06:03.192 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 860 because response 12@EnsLib.HL7.Message / 861 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
