# Case 6 ackmode

> Case 6 - AckMode: what the SENDER receives.
> Cases 1-5 used AckMode=Immed, where the sender only ever sees IRIS' own 'MSA|CA'. With AckMode=App the service
> waits for the operation and answers with the downstream ACK - but only if the operation *completes*.
> When the operation fails or suspends, IRIS builds its own CE or sends nothing. The real downstream ACK (MSH-3 LAB)
> is what the sender sees only in the 'sender_has LAB' tests.

## App: the lab's real AA is forwarded to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AA` | `app.default-AA-194419` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126194419||ADT^A28^ADT_A05|app.default-AA-194419|P|2.5
    EVN|A28|20261126194419
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126184419||ACK|ACKapp.default-AA-194419|P|2.5
    MSA|AA|app.default-AA-194419
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:19.793 | received |  | `` |
| 18:44:19.799 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 55)
  55 18:44:19.792 in.app.default -> out.default  [Request/9] 
  56 18:44:19.8 out.default -> in.app.default  [Response/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

## App + default: the sender waits for the retries, then gets IRIS' own CE - never the lab's AR

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.default` | 29211 | `AR` | `app.default-AR-194421` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194421||ADT^A28^ADT_A05|app.default-AR-194421|P|2.5
    EVN|A28|20261126194421
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.1s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|app.default-AR-194421|P|2.5
    MSA|CE|app.default-AR-194421
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:21.984 | received |  | `` |
| 18:44:21.986 | ack_sent | AR | `ACK` |
| 18:44:23.991 | received |  | `` |
| 18:44:23.994 | ack_sent | AR | `ACK` |
| 18:44:25.996 | received |  | `` |
| 18:44:26.000 | ack_sent | AR | `ACK` |
| 18:44:28.003 | received |  | `` |
| 18:44:28.011 | ack_sent | AR | `ACK` |
| 18:44:30.014 | received |  | `` |
| 18:44:30.018 | ack_sent | AR | `ACK` |
| 18:44:32.028 | received |  | `` |
| 18:44:32.030 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 57)
  57 18:44:21.983 in.app.default -> out.default  [Request/8] 
  58 18:44:32.032 out.default -> in.app.default  [Response/9] 
== event log
18:44:21.987 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 165 because response 13@EnsLib.HL7.Message / 166 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:44:23.995 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 165 because response 11@EnsLib.HL7.Message / 167 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:44:26.001 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 165 because response 13@EnsLib.HL7.Message / 168 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:44:28.013 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 165 because response 11@EnsLib.HL7.Message / 169 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:44:30.019 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 165 because response 13@EnsLib.HL7.Message / 170 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:44:32.02 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
18:44:32.02 INFO [out.default] Disconnecting from  lab:6600
18:44:32.021 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:44:32.031 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 12@EnsLib.HL7.Message / 165 because response 11@EnsLib.HL7.Message / 171 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:44:32.032 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
18:44:32.034 WARNING [in.app.default] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/165 returned with no response object and status: ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## App + :?R=F: no retry, the sender gets IRIS' own CE immediately

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AR` | `app.failrej-AR-194434` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194434||ADT^A28^ADT_A05|app.failrej-AR-194434|P|2.5
    EVN|A28|20261126194434
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|app.failrej-AR-194434|P|2.5
    MSA|CE|app.failrej-AR-194434
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:34.245 | received |  | `` |
| 18:44:34.249 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 59)
  59 18:44:34.244 in.app.failrej -> out.failrej  [Request/8] 
  60 18:44:34.25 out.failrej -> in.app.failrej  [Response/9] 
== event log
18:44:34.25 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 173 because response 12@EnsLib.HL7.Message / 174 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting i
18:44:34.252 WARNING [in.app.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/173 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 173 bec
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## App + legacy string: the lab's real AR reaches the sender (operation 'Completed')

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.legacy` | 29213 | `AR` | `app.legacy-AR-194436` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194436||ADT^A28^ADT_A05|app.legacy-AR-194436|P|2.5
    EVN|A28|20261126194436
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|LAB|SIM|IRIS|HOSP|20261126184436||ACK|ACKapp.legacy-AR-194436|P|2.5
    MSA|AR|app.legacy-AR-194436|Rejected
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:36.473 | received |  | `` |
| 18:44:36.478 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 61)
  61 18:44:36.471 in.app.legacy -> out.legacy  [Request/9] 
  62 18:44:36.479 out.legacy -> in.app.legacy  [Response/9] 
== event log
18:44:36.479 WARNING [out.legacy] Warning on HL7 Message body 10@EnsLib.HL7.Message / 176 because response 8@EnsLib.HL7.Message / 177 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## App + suspended message: the sender receives NO ACK (waits; here it gives up after 15 s)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `app.failrej` | 29212 | `AE` | `app.failrej-AE-194438` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126194438||ADT^A28^ADT_A05|app.failrej-AE-194438|P|2.5
    EVN|A28|20261126194438
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 15.0s) (no complete MLLP frame within 15s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:38.671 | received |  | `` |
| 18:44:38.676 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 63)
  63 18:44:38.67 in.app.failrej -> out.failrej  [Request/5] 
== event log
18:44:38.676 ERROR [out.failrej] ERROR <Ens>ErrSuspending: Suspending message 63 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 8@EnsLib.HL7.Message / 178 because response 11@EnsLib.HL7.Message / 179 MSA code 'A
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## Msh, MSH-15=AL: commit ACK (CA) sent at once - the rejection is invisible to the sender

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-194455` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194455||ADT^A28^ADT_A05|msh.failrej-AR-194455|P|2.5|||AL|NE
    EVN|A28|20261126194455
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|msh.failrej-AR-194455|P|2.5
    MSA|CA|msh.failrej-AR-194455
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:55.902 | received |  | `` |
| 18:44:55.908 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 64)
  64 18:44:55.9 in.msh.failrej -> out.failrej  [Request/8] 
== event log
18:44:55.909 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 180 because response 10@EnsLib.HL7.Message / 182 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Msh, MSH-16=AL: application ACK requested, IRIS builds a CE

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-194458` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194458||ADT^A28^ADT_A05|msh.failrej-AR-194458|P|2.5|||NE|AL
    EVN|A28|20261126194458
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|msh.failrej-AR-194458|P|2.5
    MSA|CE|msh.failrej-AR-194458
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:58.083 | received |  | `` |
| 18:44:58.087 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 65)
  65 18:44:58.081 in.msh.failrej -> out.failrej  [Request/8] 
  66 18:44:58.088 out.failrej -> in.msh.failrej  [Response/9] 
== event log
18:44:58.088 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 183 because response 9@EnsLib.HL7.Message / 184 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting 
18:44:58.09 WARNING [in.msh.failrej] Constructing ACK with code CE because SendRequestSync() of 8@EnsLib.HL7.Message/183 returned with no response object and status: ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 183 bec
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F,F`

**Verdict:** PASS

## Msh, no ACK requested in the message: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `msh.failrej` | 29214 | `AR` | `msh.failrej-AR-194500` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194500||ADT^A28^ADT_A05|msh.failrej-AR-194500|P|2.5
    EVN|A28|20261126194500
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.0s) (no complete MLLP frame within 10s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:45:00.338 | received |  | `` |
| 18:45:00.342 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 67)
  67 18:45:00.338 in.msh.failrej -> out.failrej  [Request/8] 
== event log
18:45:00.343 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 12@EnsLib.HL7.Message / 186 because response 8@EnsLib.HL7.Message / 187 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Never: nothing comes back

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `never.failrej` | 29215 | `AR` | `never.failrej-AR-194512` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194512||ADT^A28^ADT_A05|never.failrej-AR-194512|P|2.5
    EVN|A28|20261126194512
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 10.0s) (no complete MLLP frame within 10s):
    <nothing>
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:45:12.525 | received |  | `` |
| 18:45:12.529 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 68)
  68 18:45:12.524 in.never.failrej -> out.failrej  [Request/8] 
== event log
18:45:12.53 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 188 because response 11@EnsLib.HL7.Message / 189 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting i
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Byte: a single 0x06 ('OK') byte although the lab rejected the message

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `byte.failrej` | 29216 | `AR` | `byte.failrej-AR-194524` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194524||ADT^A28^ADT_A05|byte.failrej-AR-194524|P|2.5
    EVN|A28|20261126194524
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:45:24.703 | received |  | `` |
| 18:45:24.706 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 69)
  69 18:45:24.701 in.byte.failrej -> out.failrej  [Request/8] 
== event log
18:45:24.707 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 190 because response 13@EnsLib.HL7.Message / 191 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
