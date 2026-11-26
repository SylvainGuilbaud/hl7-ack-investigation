# Case 2 corrected

> Case 2 - the correction: only RF -> F for :?R. Same ACK, one delivery, error stays visible.

## AR ACK with :?R=F is delivered once

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR` | `failrej-AR-20040450` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200404||ADT^A28^ADT_A05|failrej-AR-20040450|P|2.5
    EVN|A28|20261126200404
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|failrej-AR-20040450|P|2.5
    MSA|CA|failrej-AR-20040450
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:04.568 | received |  | `` |
| 19:04:04.574 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 295)
 295 19:04:04.567 in.failrej -> out.failrej  [Request/8] 
== event log
19:04:04.575 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 754 because response 12@EnsLib.HL7.Message / 756 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Same with ACK^A28^ACK

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR3` | `failrej-AR3-20041632` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126200416||ADT^A28^ADT_A05|failrej-AR3-20041632|P|2.5
    EVN|A28|20261126200416
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|failrej-AR3-20041632|P|2.5
    MSA|CA|failrej-AR3-20041632
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:16.378 | received |  | `` |
| 19:04:16.381 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 303)
 303 19:04:16.372 in.failrej -> out.failrej  [Request/8] 
== event log
19:04:16.373 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:16.382 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 774 because response 9@EnsLib.HL7.Message / 776 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Control: AA still completes normally

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AA` | `failrej-AA-20044333` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126200443||ADT^A28^ADT_A05|failrej-AA-20044333|P|2.5
    EVN|A28|20261126200443
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|failrej-AA-20044333|P|2.5
    MSA|CA|failrej-AA-20044333
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:43.399 | received |  | `` |
| 19:04:43.405 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 316)
 316 19:04:43.398 in.failrej -> out.failrej  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
