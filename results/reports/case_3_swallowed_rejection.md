# Case 3 swallowed rejection

> Case 3 - the 'inherited' string :?R=W,:?E=W,... stops the retries but hides the rejection:
> the message ends Completed (action CW) although the receiver rejected it.

## AR under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AR` | `legacy-AR-194319` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194319||ADT^A28^ADT_A05|legacy-AR-194319|P|2.5
    EVN|A28|20261126194319
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|legacy-AR-194319|P|2.5
    MSA|CA|legacy-AR-194319
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:19.099 | received |  | `` |
| 18:43:19.104 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 44)
  44 18:43:19.097 in.legacy -> out.legacy  [Request/9] 
== event log
18:43:19.105 WARNING [out.legacy] Warning on HL7 Message body 8@EnsLib.HL7.Message / 138 because response 13@EnsLib.HL7.Message / 140 MSA code 'AR' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## AE under the legacy string completes with a warning

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `AE` | `legacy-AE-194321` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AE|20261126194321||ADT^A28^ADT_A05|legacy-AE-194321|P|2.5
    EVN|A28|20261126194321
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|legacy-AE-194321|P|2.5
    MSA|CA|legacy-AE-194321
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:21.269 | received |  | `` |
| 18:43:21.274 | ack_sent | AE | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 45)
  45 18:43:21.268 in.legacy -> out.legacy  [Request/9] 
== event log
18:43:21.274 WARNING [out.legacy] Warning on HL7 Message body 13@EnsLib.HL7.Message / 141 because response 11@EnsLib.HL7.Message / 143 MSA code 'AE' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C' and Reply message type ACK does not match expected type
```

**Result:** deliveries = **1**, final status = **Completed**, action codes = `CW`

**Verdict:** PASS

## Reply without MSA falls to :~=F

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `legacy` | 29203 | `NOMSA` | `legacy-NOMSA-194323` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOMSA|20261126194323||ADT^A28^ADT_A05|legacy-NOMSA-194323|P|2.5
    EVN|A28|20261126194323
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|legacy-NOMSA-194323|P|2.5
    MSA|CA|legacy-NOMSA-194323
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:23.446 | received |  | `` |
| 18:43:23.450 | ack_sent |  | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 46)
  46 18:43:23.445 in.legacy -> out.legacy  [Request/8] 
== event log
18:43:23.451 ERROR [out.legacy] ERROR <Ens>ErrGeneral: Quitting with error on HL7 Message body 11@EnsLib.HL7.Message / 144 because response 10@EnsLib.HL7.Message / 146 MSA code '~NoMSA' matched ReplyCodeActions 1-4 : ':?R=W,:?E=W,:~=F,:?A=C', resulting in Acti
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `F`

**Verdict:** PASS

**Script verdict:** ALL PASSED
