# Case 3 swallowed rejection

> Case 3 - the 'inherited' string :?R=W,:?E=W,... stops the retries but hides the rejection:
> the message ends Completed (action CW) although the receiver rejected it.

## AR under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AR` | `legacy-AR-191058` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191058||ADT^A28^ADT_A05|legacy-AR-191058|P|2.5
    EVN|A28|20261126191058
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261910||ACK^A28|legacy-AR-191058|P|2.5
    MSA|CA|legacy-AR-191058
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:10:58.165 | received |  | `` |
| 18:10:58.168 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 133)
 133 18:10:58.162 in.legacy -> out.legacy  [Request/9] 
== event log
18:10:58.169 WARNING [out.legacy] Warning on HL7 Message body 10@EnsLib.HL7.Message / 422 because response 13@EnsLib.HL7.Message / 424 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## AE under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AE` | `legacy-AE-191100` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126191100||ADT^A28^ADT_A05|legacy-AE-191100|P|2.5
    EVN|A28|20261126191100
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|legacy-AE-191100|P|2.5
    MSA|CA|legacy-AE-191100
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:00.395 | received |  | `` |
| 18:11:00.399 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 134)
 134 18:11:00.394 in.legacy -> out.legacy  [Request/9] 
== event log
18:11:00.4 WARNING [out.legacy] Warning on HL7 Message body 13@EnsLib.HL7.Message / 425 because response 8@EnsLib.HL7.Message / 427 MSA code 'AE' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type AC
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## Reply without MSA falls to :~=F

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `NOMSA` | `legacy-NOMSA-191102` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126191102||ADT^A28^ADT_A05|legacy-NOMSA-191102|P|2.5
    EVN|A28|20261126191102
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|legacy-NOMSA-191102|P|2.5
    MSA|CA|legacy-NOMSA-191102
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:02.592 | received |  | `` |
| 18:11:02.596 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 135)
 135 18:11:02.59 in.legacy -> out.legacy  [Request/8] 
== event log
18:11:02.597 ERROR [out.legacy] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 8@EnsLib.HL7.Message / 428 because response 12@EnsLib.HL7.Message / 430 MSA code '~NoMSA' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C', resulting in Actio
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
