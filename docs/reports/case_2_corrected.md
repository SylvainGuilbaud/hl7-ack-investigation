# Case 2 corrected

> Case 2 - the correction: only RF -> F for :?R. Same ACK, one delivery, error stays visible.

## AR ACK with :?R=F is delivered once

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR` | `failrej-AR-162525` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162525||ADT^A28^ADT_A05|failrej-AR-162525|P|2.5
    EVN|A28|20261126162525
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|failrej-AR-162525|P|2.5
    MSA|CA|failrej-AR-162525
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:25.330 | received |  | `` |
| 15:25:25.334 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 33)
  33 15:25:25.329 in.failrej -> out.failrej  [Request/8] 
== event log
15:25:25.335 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 74 because response 12@EnsLib.HL7.Message / 76 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Same with ACK^A28^ACK

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR3` | `failrej-AR3-162527` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126162527||ADT^A28^ADT_A05|failrej-AR3-162527|P|2.5
    EVN|A28|20261126162527
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|failrej-AR3-162527|P|2.5
    MSA|CA|failrej-AR3-162527
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:27.751 | received |  | `` |
| 15:25:27.754 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 34)
  34 15:25:27.75 in.failrej -> out.failrej  [Request/8] 
== event log
15:25:27.755 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 12@EnsLib.HL7.Message / 77 because response 13@EnsLib.HL7.Message / 79 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting i
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Control: AA still completes normally

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AA` | `failrej-AA-162530` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126162530||ADT^A28^ADT_A05|failrej-AA-162530|P|2.5
    EVN|A28|20261126162530
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.1s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|failrej-AA-162530|P|2.5
    MSA|CA|failrej-AA-162530
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:30.272 | received |  | `` |
| 15:25:30.334 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 35)
  35 15:25:30.261 in.failrej -> out.failrej  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
