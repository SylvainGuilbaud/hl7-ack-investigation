# Case 3 swallowed rejection

> Case 3 - the 'inherited' string :?R=W,:?E=W,... stops the retries but hides the rejection:
> the message ends Completed (action CW) although the receiver rejected it.

## AR under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AR` | `legacy-AR-162532` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162532||ADT^A28^ADT_A05|legacy-AR-162532|P|2.5
    EVN|A28|20261126162532
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|legacy-AR-162532|P|2.5
    MSA|CA|legacy-AR-162532
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:32.681 | received |  | `` |
| 15:25:32.687 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 36)
  36 15:25:32.678 in.legacy -> out.legacy  [Request/9] 
== event log
15:25:32.688 WARNING [out.legacy] Warning on HL7 Message body 9@EnsLib.HL7.Message / 83 because response 13@EnsLib.HL7.Message / 85 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type AC
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## AE under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AE` | `legacy-AE-162534` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126162534||ADT^A28^ADT_A05|legacy-AE-162534|P|2.5
    EVN|A28|20261126162534
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|legacy-AE-162534|P|2.5
    MSA|CA|legacy-AE-162534
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:34.877 | received |  | `` |
| 15:25:34.880 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 37)
  37 15:25:34.876 in.legacy -> out.legacy  [Request/9] 
== event log
15:25:34.881 WARNING [out.legacy] Warning on HL7 Message body 13@EnsLib.HL7.Message / 86 because response 12@EnsLib.HL7.Message / 88 MSA code 'AE' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type A
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## Reply without MSA falls to :~=F

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `NOMSA` | `legacy-NOMSA-162537` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126162537||ADT^A28^ADT_A05|legacy-NOMSA-162537|P|2.5
    EVN|A28|20261126162537
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|legacy-NOMSA-162537|P|2.5
    MSA|CA|legacy-NOMSA-162537
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:37.050 | received |  | `` |
| 15:25:37.054 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 38)
  38 15:25:37.049 in.legacy -> out.legacy  [Request/8] 
== event log
15:25:37.055 ERROR [out.legacy] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 12@EnsLib.HL7.Message / 89 because response 10@EnsLib.HL7.Message / 91 MSA code '~NoMSA' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C', resulting in Action
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
