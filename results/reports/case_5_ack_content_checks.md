# Case 5 ack content checks

> Case 5 - what the default does with other ACK content.
> OTHERID: a well-formed AA whose MSA-2 is the control id of ANOTHER message (e.g. a stale ACK). It is not a retry case:
> it shows that the default accepts it silently, because :?A=C matches before :I?=W is reached.

## AE: suspended (:?E=S), not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AE` | `default-AE-194413` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126194413||ADT^A28^ADT_A05|default-AE-194413|P|2.5
    EVN|A28|20261126194413
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|default-AE-194413|P|2.5
    MSA|CA|default-AE-194413
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:13.212 | received |  | `` |
| 18:44:13.217 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 52)
  52 18:44:13.21 in.default -> out.default  [Request/5] 
== event log
18:44:13.219 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 52 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 8@EnsLib.HL7.Message / 154 because response 13@EnsLib.HL7.Message / 156 MSA code 'A
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## No MSA: suspended (:~=S)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `NOMSA` | `default-NOMSA-194415` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126194415||ADT^A28^ADT_A05|default-NOMSA-194415|P|2.5
    EVN|A28|20261126194415
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|default-NOMSA-194415|P|2.5
    MSA|CA|default-NOMSA-194415
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:15.389 | received |  | `` |
| 18:44:15.394 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 53)
  53 18:44:15.388 in.default -> out.default  [Request/5] 
== event log
18:44:15.395 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 53 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 13@EnsLib.HL7.Message / 157 because response 10@EnsLib.HL7.Message / 159 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## AA that acknowledges ANOTHER message (MSA-2 mismatch): Completed, no warning (:?A=C matches before :I?=W)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `OTHERID` | `default-OTHERID-194417` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|OTHERID|20261126194417||ADT^A28^ADT_A05|default-OTHERID-194417|P|2.5
    EVN|A28|20261126194417
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261944||ACK^A28|default-OTHERID-194417|P|2.5
    MSA|CA|default-OTHERID-194417
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:44:17.559 | received |  | `` |
| 18:44:17.563 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 54)
  54 18:44:17.559 in.default -> out.default  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
