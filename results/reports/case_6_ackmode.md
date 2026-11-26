# Case 6 ackmode

> Case 6 - AckMode: what the SENDER receives.
> Cases 1-5 used AckMode=Immed, where the sender only ever sees IRIS' own 'MSA|CA'. With AckMode=App the service
> waits for the operation and answers with the downstream ACK - but only if the operation *completes*.
> When the operation fails or suspends, IRIS builds its own CE or sends nothing. The real downstream ACK (MSH-3 LAB)
> is what the sender sees only in the 'sender_has LAB' tests.

## App: the lab's real AA is forwarded to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AA` | `app.default-AA-162633` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126162633||ADT^A28^ADT_A05|app.default-AA-162633|P|2.5
    EVN|A28|20261126162633
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126152633||ACK|ACKapp.default-AA-162633|P|2.5
    MSA|AA|app.default-AA-162633
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:26:33.450 | received |  | `` |
| 15:26:33.453 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 46)
  46 15:26:33.449 in.app.default -> out.default  [Request/9] 
  47 15:26:33.454 out.default -> in.app.default  [Response/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

## App + default: the sender waits for the retries, then gets IRIS' own CE - never the lab's AR

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AR` | `app.default-AR-162635` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162635||ADT^A28^ADT_A05|app.default-AR-162635|P|2.5
    EVN|A28|20261126162635
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.1s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261626||ACK^A28|app.default-AR-162635|P|2.5
    MSA|CE|app.default-AR-162635
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:26:35.665 | received |  | `` |
| 15:26:35.668 | ack_sent | AR | `ACK` |
| 15:26:37.670 | received |  | `` |
| 15:26:37.673 | ack_sent | AR | `ACK` |
| 15:26:39.675 | received |  | `` |
| 15:26:39.679 | ack_sent | AR | `ACK` |
| 15:26:41.685 | received |  | `` |
| 15:26:41.690 | ack_sent | AR | `ACK` |
| 15:26:43.698 | received |  | `` |
| 15:26:43.702 | ack_sent | AR | `ACK` |
| 15:26:45.717 | received |  | `` |
| 15:26:45.719 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 48)
  48 15:26:35.664 in.app.default -> out.default  [Request/8] 
  49 15:26:45.72 out.default -> in.app.default  [Response/9] 
== event log
15:26:35.668 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 110 because response 13@EnsLib.HL7.Message / 111 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
15:26:37.674 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 110 because response 11@EnsLib.HL7.Message / 112 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
15:26:39.68 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 110 because response 13@EnsLib.HL7.Message / 113 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
15:26:41.691 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 110 because response 11@EnsLib.HL7.Message / 114 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
15:26:43.702 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 110 because response 13@EnsLib.HL7.Message / 115 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
15:26:45.706 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
15:26:45.706 INFO [out.default] Disconnecting from  lab:6600
15:26:45.711 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:26:45.72 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 110 because response 11@EnsLib.HL7.Message / 116 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
15:26:45.72 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message body
15:26:45.722 WARNING [in.app.default] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/110 returned with no response object and status: ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## App + :?R=F: no retry, the sender gets IRIS' own CE immediately

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AR` | `app.failrej-AR-162647` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162647||ADT^A28^ADT_A05|app.failrej-AR-162647|P|2.5
    EVN|A28|20261126162647
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261626||ACK^A28|app.failrej-AR-162647|P|2.5
    MSA|CE|app.failrej-AR-162647
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:26:47.940 | received |  | `` |
| 15:26:47.943 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 50)
  50 15:26:47.938 in.app.failrej -> out.failrej  [Request/8] 
  51 15:26:47.945 out.failrej -> in.app.failrej  [Response/9] 
== event log
15:26:47.945 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 118 because response 12@EnsLib.HL7.Message / 119 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting 
15:26:47.946 WARNING [in.app.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/118 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 118 bec
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## App + legacy string: the lab's real AR reaches the sender (operation 'Completed')

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.legacy` | 29213 | `AR` | `app.legacy-AR-162650` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162650||ADT^A28^ADT_A05|app.legacy-AR-162650|P|2.5
    EVN|A28|20261126162650
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126152650||ACK|ACKapp.legacy-AR-162650|P|2.5
    MSA|AR|app.legacy-AR-162650|Rejected
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:26:50.125 | received |  | `` |
| 15:26:50.127 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 52)
  52 15:26:50.123 in.app.legacy -> out.legacy  [Request/9] 
  53 15:26:50.128 out.legacy -> in.app.legacy  [Response/9] 
== event log
15:26:50.128 WARNING [out.legacy] Warning on HL7 Message body 10@EnsLib.HL7.Message / 121 because response 9@EnsLib.HL7.Message / 122 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## App + suspended message: the sender receives NO ACK (waits; here it gives up after 15 s)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AE` | `app.failrej-AE-162652` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126162652||ADT^A28^ADT_A05|app.failrej-AE-162652|P|2.5
    EVN|A28|20261126162652
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 15.0s) (no complete MLLP frame within 15s):
    <nothing>
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:26:52.313 | received |  | `` |
| 15:26:52.320 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 54)
  54 15:26:52.311 in.app.failrej -> out.failrej  [Request/5] 
== event log
15:26:52.321 ERROR [out.failrej] ERROR <Ens>ErrSuspending: Suspending message 54 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 8@EnsLib.HL7.Message / 123 because response 11@EnsLib.HL7.Message / 124 MSA code 'A
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## Msh, MSH-15=AL: commit ACK (CA) sent at once - the rejection is invisible to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-162709` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162709||ADT^A28^ADT_A05|msh.failrej-AR-162709|P|2.5|||AL|NE
    EVN|A28|20261126162709
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261627||ACK^A28|msh.failrej-AR-162709|P|2.5
    MSA|CA|msh.failrej-AR-162709
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:27:09.516 | received |  | `` |
| 15:27:09.520 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 55)
  55 15:27:09.515 in.msh.failrej -> out.failrej  [Request/8] 
== event log
15:27:09.522 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 125 because response 10@EnsLib.HL7.Message / 127 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Msh, MSH-16=AL: application ACK requested, IRIS builds a CE

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-162711` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162711||ADT^A28^ADT_A05|msh.failrej-AR-162711|P|2.5|||NE|AL
    EVN|A28|20261126162711
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261627||ACK^A28|msh.failrej-AR-162711|P|2.5
    MSA|CE|msh.failrej-AR-162711
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:27:11.700 | received |  | `` |
| 15:27:11.703 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 56)
  56 15:27:11.699 in.msh.failrej -> out.failrej  [Request/8] 
  57 15:27:11.704 out.failrej -> in.msh.failrej  [Response/9] 
== event log
15:27:11.704 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 128 because response 9@EnsLib.HL7.Message / 129 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting 
15:27:11.706 WARNING [in.msh.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/128 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 128 be
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## Msh, no ACK requested in the message: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-162713` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162713||ADT^A28^ADT_A05|msh.failrej-AR-162713|P|2.5
    EVN|A28|20261126162713
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.0s) (no complete MLLP frame within 10s):
    <nothing>
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:27:13.879 | received |  | `` |
| 15:27:13.882 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 58)
  58 15:27:13.878 in.msh.failrej -> out.failrej  [Request/8] 
== event log
15:27:13.883 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 12@EnsLib.HL7.Message / 131 because response 8@EnsLib.HL7.Message / 132 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Never: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `never.failrej` | 29215 | `AR` | `never.failrej-AR-162726` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162726||ADT^A28^ADT_A05|never.failrej-AR-162726|P|2.5
    EVN|A28|20261126162726
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.0s) (no complete MLLP frame within 10s):
    <nothing>
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:27:26.100 | received |  | `` |
| 15:27:26.103 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 59)
  59 15:27:26.098 in.never.failrej -> out.failrej  [Request/8] 
== event log
15:27:26.104 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 133 because response 11@EnsLib.HL7.Message / 134 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Byte: a single 0x06 ('OK') byte although the lab rejected the message

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `byte.failrej` | 29216 | `AR` | `byte.failrej-AR-162738` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162738||ADT^A28^ADT_A05|byte.failrej-AR-162738|P|2.5
    EVN|A28|20261126162738
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:27:38.309 | received |  | `` |
| 15:27:38.313 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 60)
  60 15:27:38.307 in.byte.failrej -> out.failrej  [Request/8] 
== event log
15:27:38.314 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 135 because response 13@EnsLib.HL7.Message / 136 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
