# Case 1 reject is retried

> Case 1 - the symptom: the lab answers AR (a valid ACK) and the message is sent again and again.
> Default ReplyCodeActions contains :?R=RF  => Retry until FailureTimeout, then Fail.

## AR ACK under the documented default is retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR` | `default-AR-20035040` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126200350||ADT^A28^ADT_A05|default-AR-20035040|P|2.5
    EVN|A28|20261126200350
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262003||ACK^A28|default-AR-20035040|P|2.5
    MSA|CA|default-AR-20035040
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:03:50.454 | received |  | `` |
| 19:03:50.458 | ack_sent | AR | `ACK` |
| 19:03:52.461 | received |  | `` |
| 19:03:52.464 | ack_sent | AR | `ACK` |
| 19:03:54.465 | received |  | `` |
| 19:03:54.469 | ack_sent | AR | `ACK` |
| 19:03:56.473 | received |  | `` |
| 19:03:56.480 | ack_sent | AR | `ACK` |
| 19:03:58.483 | received |  | `` |
| 19:03:58.487 | ack_sent | AR | `ACK` |
| 19:04:00.502 | received |  | `` |
| 19:04:00.504 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 282)
 282 19:03:50.453 in.default -> out.default  [Request/8] 
== event log
19:03:50.459 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 723 because response 12@EnsLib.HL7.Message / 725 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:03:52.464 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 723 because response 11@EnsLib.HL7.Message / 731 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:03:54.47 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 723 because response 12@EnsLib.HL7.Message / 733 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action code
19:03:56.481 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 723 because response 11@EnsLib.HL7.Message / 734 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:03:58.488 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 723 because response 12@EnsLib.HL7.Message / 735 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:00.492 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
19:04:00.493 INFO [out.default] Disconnecting from  lab:6600
19:04:00.494 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:00.506 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 9@EnsLib.HL7.Message / 723 because response 11@EnsLib.HL7.Message / 738 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:00.506 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## Same with MSH-9 = ACK^A28^ACK (three components)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR3` | `default-AR3-20040315` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126200403||ADT^A28^ADT_A05|default-AR3-20040315|P|2.5
    EVN|A28|20261126200403
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|default-AR3-20040315|P|2.5
    MSA|CA|default-AR3-20040315
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:03.200 | received |  | `` |
| 19:04:03.211 | ack_sent | AR | `ACK^A28^ACK` |
| 19:04:05.213 | received |  | `` |
| 19:04:05.217 | ack_sent | AR | `ACK^A28^ACK` |
| 19:04:07.220 | received |  | `` |
| 19:04:07.226 | ack_sent | AR | `ACK^A28^ACK` |
| 19:04:09.230 | received |  | `` |
| 19:04:09.235 | ack_sent | AR | `ACK^A28^ACK` |
| 19:04:11.239 | received |  | `` |
| 19:04:11.243 | ack_sent | AR | `ACK^A28^ACK` |
| 19:04:13.256 | received |  | `` |
| 19:04:13.260 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 292)
 292 19:04:03.199 in.default -> out.default  [Request/8] 
== event log
19:04:03.212 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 746 because response 12@EnsLib.HL7.Message / 748 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
19:04:05.218 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 746 because response 8@EnsLib.HL7.Message / 758 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:07.228 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 746 because response 12@EnsLib.HL7.Message / 764 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
19:04:09.236 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 746 because response 8@EnsLib.HL7.Message / 765 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:11.244 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 746 because response 12@EnsLib.HL7.Message / 766 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
19:04:13.245 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
19:04:13.245 INFO [out.default] Disconnecting from  lab:6600
19:04:13.247 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:13.261 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 746 because response 8@EnsLib.HL7.Message / 767 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
19:04:13.261 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

**Script verdict:** ALL PASSED
