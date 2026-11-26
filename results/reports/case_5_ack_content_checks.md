# Case 5 ack content checks

> Case 5 - what the default does with other ACK content.
> OTHERID: a well-formed AA whose MSA-2 is the control id of ANOTHER message (e.g. a stale ACK). It is not a retry case:
> it shows that the default accepts it silently, because :?A=C matches before :I?=W is reached.

## AE: suspended (:?E=S), not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AE` | `default-AE-191152` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126191152||ADT^A28^ADT_A05|default-AE-191152|P|2.5
    EVN|A28|20261126191152
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|default-AE-191152|P|2.5
    MSA|CA|default-AE-191152
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:52.659 | received |  | `` |
| 18:11:52.664 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 140)
 140 18:11:52.657 in.default -> out.default  [Request/5] 
== event log
18:11:52.665 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 140 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 9@EnsLib.HL7.Message / 438 because response 10@EnsLib.HL7.Message / 440 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## No MSA: suspended (:~=S)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `NOMSA` | `default-NOMSA-191154` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126191154||ADT^A28^ADT_A05|default-NOMSA-191154|P|2.5
    EVN|A28|20261126191154
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|default-NOMSA-191154|P|2.5
    MSA|CA|default-NOMSA-191154
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:54.849 | received |  | `` |
| 18:11:54.853 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 141)
 141 18:11:54.847 in.default -> out.default  [Request/5] 
== event log
18:11:54.854 ERROR [out.default] ERROR <Ens>ErrSuspending: Suspending message 141 as requested by message handler with status: ERROR <Ens>ErrGeneral: Suspending HL7 Message body 10@EnsLib.HL7.Message / 441 because response 8@EnsLib.HL7.Message / 443 MSA code '
```

**Result:** deliveries = **1**, final status = **Suspended**, action codes = `S`

**Verdict:** PASS

## AA that acknowledges ANOTHER message (MSA-2 mismatch): Completed, no warning (:?A=C matches before :I?=W)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `OTHERID` | `default-OTHERID-191156` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|OTHERID|20261126191157||ADT^A28^ADT_A05|default-OTHERID-191156|P|2.5
    EVN|A28|20261126191157
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|default-OTHERID-191156|P|2.5
    MSA|CA|default-OTHERID-191156
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:57.050 | received |  | `` |
| 18:11:57.054 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 142)
 142 18:11:57.05 in.default -> out.default  [Request/9] 
== event log
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
