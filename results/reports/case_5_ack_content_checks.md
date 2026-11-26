# Case 5 ack content checks

> Case 5 - what the default does with other ACK content.
> OTHERID: a well-formed AA whose MSA-2 is the control id of ANOTHER message (e.g. a stale ACK). It is not a retry case:
> it shows that the default accepts it silently, because :?A=C matches before :I?=W is reached.

## AE: suspended (:?E=S), not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AE` | `default-AE-20040104` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126200401||ADT^A28^ADT_A05|default-AE-20040104|P|2.5
    EVN|A28|20261126200401
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|default-AE-20040104|P|2.5
    MSA|CA|default-AE-20040104
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:01.096 | received |  | `` |
| 19:04:01.107 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 287)
 287 19:04:01.095 in.default -> out.default  [Request/5] 
== event log
19:04:01.108 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 287 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 11@EnsLib.HL7.Message / 739 because response 12@EnsLib.HL7.Message / 741 MSA code
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## No MSA: suspended (:~=S)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `NOMSA` | `default-NOMSA-20041371` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126200413||ADT^A28^ADT_A05|default-NOMSA-20041371|P|2.5
    EVN|A28|20261126200413
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|default-NOMSA-20041371|P|2.5
    MSA|CA|default-NOMSA-20041371
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:13.798 | received |  | `` |
| 19:04:13.808 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 300)
 300 19:04:13.793 in.default -> out.default  [Request/5] 
== event log
19:04:13.809 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 300 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 8@EnsLib.HL7.Message / 768 because response 12@EnsLib.HL7.Message / 770 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## AA that acknowledges ANOTHER message (MSA-2 mismatch): Completed, no warning (:?A=C matches before :I?=W)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `OTHERID` | `default-OTHERID-20044087` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|OTHERID|20261126200440||ADT^A28^ADT_A05|default-OTHERID-20044087|P|2.5
    EVN|A28|20261126200440
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|default-OTHERID-20044087|P|2.5
    MSA|CA|default-OTHERID-20044087
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:40.943 | received |  | `` |
| 19:04:40.949 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 312)
 312 19:04:40.94 in.default -> out.default  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
