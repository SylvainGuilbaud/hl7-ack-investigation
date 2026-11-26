# Case 2 corrected

> Case 2 - the correction: only RF -> F for :?R. Same ACK, one delivery, error stays visible.

## AR ACK with :?R=F is delivered once

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR` | `failrej-AR-194312` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194312||ADT^A28^ADT_A05|failrej-AR-194312|P|2.5
    EVN|A28|20261126194312
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|failrej-AR-194312|P|2.5
    MSA|CA|failrej-AR-194312
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:12.503 | received |  | `` |
| 18:43:12.507 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 41)
  41 18:43:12.501 in.failrej -> out.failrej  [Request/8] 
== event log
18:43:12.508 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 13@EnsLib.HL7.Message / 129 because response 10@EnsLib.HL7.Message / 131 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Same with ACK^A28^ACK

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AR3` | `failrej-AR3-194314` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126194314||ADT^A28^ADT_A05|failrej-AR3-194314|P|2.5
    EVN|A28|20261126194314
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|failrej-AR3-194314|P|2.5
    MSA|CA|failrej-AR3-194314
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:14.680 | received |  | `` |
| 18:43:14.684 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 42)
  42 18:43:14.679 in.failrej -> out.failrej  [Request/8] 
== event log
18:43:14.685 ERROR [out.failrej] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 10@EnsLib.HL7.Message / 132 because response 8@EnsLib.HL7.Message / 134 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

## Control: AA still completes normally

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `AA` | `failrej-AA-194316` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AA|20261126194316||ADT^A28^ADT_A05|failrej-AA-194316|P|2.5
    EVN|A28|20261126194316
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|failrej-AA-194316|P|2.5
    MSA|CA|failrej-AA-194316
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:16.867 | received |  | `` |
| 18:43:16.871 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 43)
  43 18:43:16.866 in.failrej -> out.failrej  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
