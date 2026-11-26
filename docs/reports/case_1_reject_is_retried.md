# Case 1 reject is retried

> Case 1 - the symptom: the lab answers AR (a valid ACK) and the message is sent again and again.
> Default ReplyCodeActions contains :?R=RF  => Retry until FailureTimeout, then Fail.

## AR ACK under the documented default is retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR` | `default-AR-162504` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126162504||ADT^A28^ADT_A05|default-AR-162504|P|2.5
    EVN|A28|20261126162504
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|default-AR-162504|P|2.5
    MSA|CA|default-AR-162504
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:04.319 | received |  | `` |
| 15:25:04.325 | ack_sent | AR | `ACK` |
| 15:25:06.330 | received |  | `` |
| 15:25:06.334 | ack_sent | AR | `ACK` |
| 15:25:08.342 | received |  | `` |
| 15:25:08.348 | ack_sent | AR | `ACK` |
| 15:25:10.350 | received |  | `` |
| 15:25:10.354 | ack_sent | AR | `ACK` |
| 15:25:12.360 | received |  | `` |
| 15:25:12.363 | ack_sent | AR | `ACK` |
| 15:25:14.380 | received |  | `` |
| 15:25:14.382 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 31)
  31 15:25:04.313 in.default -> out.default  [Request/8] 
== event log
15:25:04.327 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 58 because response 12@EnsLib.HL7.Message / 60 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:06.335 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 58 because response 11@EnsLib.HL7.Message / 61 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:08.349 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 58 because response 12@EnsLib.HL7.Message / 62 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:10.355 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 58 because response 11@EnsLib.HL7.Message / 63 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:12.364 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 58 because response 12@EnsLib.HL7.Message / 64 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:14.371 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
15:25:14.371 INFO [out.default] Disconnecting from  lab:6600
15:25:14.376 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:14.382 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 58 because response 11@EnsLib.HL7.Message / 65 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:14.383 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## Same with MSH-9 = ACK^A28^ACK (three components)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR3` | `default-AR3-162514` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126162514||ADT^A28^ADT_A05|default-AR3-162514|P|2.5
    EVN|A28|20261126162514
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|default-AR3-162514|P|2.5
    MSA|CA|default-AR3-162514
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:14.768 | received |  | `` |
| 15:25:14.771 | ack_sent | AR | `ACK^A28^ACK` |
| 15:25:16.775 | received |  | `` |
| 15:25:16.779 | ack_sent | AR | `ACK^A28^ACK` |
| 15:25:18.785 | received |  | `` |
| 15:25:18.789 | ack_sent | AR | `ACK^A28^ACK` |
| 15:25:20.802 | received |  | `` |
| 15:25:20.808 | ack_sent | AR | `ACK^A28^ACK` |
| 15:25:22.811 | received |  | `` |
| 15:25:22.814 | ack_sent | AR | `ACK^A28^ACK` |
| 15:25:24.829 | received |  | `` |
| 15:25:24.831 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 32)
  32 15:25:14.767 in.default -> out.default  [Request/8] 
== event log
15:25:14.772 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 66 because response 12@EnsLib.HL7.Message / 68 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
15:25:16.78 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 66 because response 10@EnsLib.HL7.Message / 69 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:18.79 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 66 because response 12@EnsLib.HL7.Message / 70 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:20.81 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 66 because response 10@EnsLib.HL7.Message / 71 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code 
15:25:22.815 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 66 because response 12@EnsLib.HL7.Message / 72 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
15:25:24.817 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
15:25:24.817 INFO [out.default] Disconnecting from  lab:6600
15:25:24.822 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:24.832 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 66 because response 10@EnsLib.HL7.Message / 73 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
15:25:24.832 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

**Script verdict:** ALL PASSED
