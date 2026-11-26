# Case 3 swallowed rejection

> Case 3 - the 'inherited' string :?R=W,:?E=W,... stops the retries but hides the rejection:
> the message ends Completed (action CW) although the receiver rejected it.

## AR under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AR` | `legacy-AR-20035240` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200352||ADT^A28^ADT_A05|legacy-AR-20035240|P|2.5
    EVN|A28|20261126200352
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262003||ACK^A28|legacy-AR-20035240|P|2.5
    MSA|CA|legacy-AR-20035240
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:03:52.443 | received |  | `` |
| 19:03:52.448 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 284)
 284 19:03:52.442 in.legacy -> out.legacy  [Request/9] 
== event log
19:03:52.449 WARNING [out.legacy] Warning on HL7 Message body 12@EnsLib.HL7.Message / 728 because response 10@EnsLib.HL7.Message / 730 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## AE under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AE` | `legacy-AE-20040384` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126200403||ADT^A28^ADT_A05|legacy-AE-20040384|P|2.5
    EVN|A28|20261126200403
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|legacy-AE-20040384|P|2.5
    MSA|CA|legacy-AE-20040384
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:03.935 | received |  | `` |
| 19:04:03.942 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 294)
 294 19:04:03.923 in.legacy -> out.legacy  [Request/9] 
== event log
19:04:03.925 INFO [out.legacy] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:03.943 WARNING [out.legacy] Warning on HL7 Message body 8@EnsLib.HL7.Message / 750 because response 9@EnsLib.HL7.Message / 752 MSA code 'AE' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type A
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## Reply without MSA falls to :~=F

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `NOMSA` | `legacy-NOMSA-20043002` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126200430||ADT^A28^ADT_A05|legacy-NOMSA-20043002|P|2.5
    EVN|A28|20261126200430
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|legacy-NOMSA-20043002|P|2.5
    MSA|CA|legacy-NOMSA-20043002
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:30.064 | received |  | `` |
| 19:04:30.069 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 311)
 311 19:04:30.063 in.legacy -> out.legacy  [Request/8] 
== event log
19:04:30.07 ERROR [out.legacy] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 9@EnsLib.HL7.Message / 790 because response 12@EnsLib.HL7.Message / 792 MSA code '~NoMSA' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C', resulting in Action
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
