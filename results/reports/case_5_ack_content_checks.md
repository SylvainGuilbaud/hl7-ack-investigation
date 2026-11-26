# Case 5 ack content checks

> Case 5 - what the default does with other ACK content.
> OTHERID: a well-formed AA whose MSA-2 is the control id of ANOTHER message (e.g. a stale ACK). It is not a retry case:
> it shows that the default accepts it silently, because :?A=C matches before :I?=W is reached.

## AE: suspended (:?E=S), not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AE` | `default-AE-165500` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126165501||ADT^A28^ADT_A05|default-AE-165500|P|2.5
    EVN|A28|20261126165501
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261655||ACK^A28|default-AE-165500|P|2.5
    MSA|CA|default-AE-165500
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:55:01.033 | received |  | `` |
| 15:55:01.040 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 227)
 227 15:55:01.03 in.default -> out.default  [Request/5] 
== event log
15:55:01.041 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 227 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 8@EnsLib.HL7.Message / 414 because response 11@EnsLib.HL7.Message / 416 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## No MSA: suspended (:~=S)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `NOMSA` | `default-NOMSA-165503` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126165503||ADT^A28^ADT_A05|default-NOMSA-165503|P|2.5
    EVN|A28|20261126165503
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261655||ACK^A28|default-NOMSA-165503|P|2.5
    MSA|CA|default-NOMSA-165503
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:55:03.227 | received |  | `` |
| 15:55:03.231 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 228)
 228 15:55:03.225 in.default -> out.default  [Request/5] 
== event log
15:55:03.232 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 228 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 11@EnsLib.HL7.Message / 417 because response 13@EnsLib.HL7.Message / 419 MSA code
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## AA that acknowledges ANOTHER message (MSA-2 mismatch): Completed, no warning (:?A=C matches before :I?=W)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `OTHERID` | `default-OTHERID-165505` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|OTHERID|20261126165505||ADT^A28^ADT_A05|default-OTHERID-165505|P|2.5
    EVN|A28|20261126165505
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261655||ACK^A28|default-OTHERID-165505|P|2.5
    MSA|CA|default-OTHERID-165505
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:55:05.464 | received |  | `` |
| 15:55:05.471 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 229)
 229 15:55:05.463 in.default -> out.default  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
