# Case 2 corrected

> Case 2 - the correction: only RF -> F for :?R. Same ACK, one delivery, error stays visible.

## AR ACK with :?R=F is delivered once

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR` | `failrej-AR-191051` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191051||ADT^A28^ADT_A05|failrej-AR-191051|P|2.5
    EVN|A28|20261126191051
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261910||ACK^A28|failrej-AR-191051|P|2.5
    MSA|CA|failrej-AR-191051
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:10:51.486 | received |  | `` |
| 18:10:51.492 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 130)
 130 18:10:51.485 in.failrej -> out.failrej  [Request/8] 
== event log
18:10:51.493 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 413 because response 8@EnsLib.HL7.Message / 414 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Same with ACK^A28^ACK

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR3` | `failrej-AR3-191053` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126191053||ADT^A28^ADT_A05|failrej-AR3-191053|P|2.5
    EVN|A28|20261126191053
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261910||ACK^A28|failrej-AR3-191053|P|2.5
    MSA|CA|failrej-AR3-191053
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:10:53.703 | received |  | `` |
| 18:10:53.708 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 131)
 131 18:10:53.702 in.failrej -> out.failrej  [Request/8] 
== event log
18:10:53.709 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 416 because response 11@EnsLib.HL7.Message / 418 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Control: AA still completes normally

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AA` | `failrej-AA-191055` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126191055||ADT^A28^ADT_A05|failrej-AA-191055|P|2.5
    EVN|A28|20261126191055
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261910||ACK^A28|failrej-AA-191055|P|2.5
    MSA|CA|failrej-AA-191055
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:10:55.895 | received |  | `` |
| 18:10:55.900 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 132)
 132 18:10:55.893 in.failrej -> out.failrej  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
