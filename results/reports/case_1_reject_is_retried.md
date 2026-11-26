# Case 1 reject is retried

> Case 1 - the symptom: the lab answers AR (a valid ACK) and the message is sent again and again.
> Default ReplyCodeActions contains :?R=RF  => Retry until FailureTimeout, then Fail.

## AR ACK under the documented default is retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR` | `default-AR-191030` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126191030||ADT^A28^ADT_A05|default-AR-191030|P|2.5
    EVN|A28|20261126191030
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261910||ACK^A28|default-AR-191030|P|2.5
    MSA|CA|default-AR-191030
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:10:30.352 | received |  | `` |
| 18:10:30.364 | ack_sent | AR | `ACK` |
| 18:10:32.371 | received |  | `` |
| 18:10:32.386 | ack_sent | AR | `ACK` |
| 18:10:34.390 | received |  | `` |
| 18:10:34.395 | ack_sent | AR | `ACK` |
| 18:10:36.407 | received |  | `` |
| 18:10:36.412 | ack_sent | AR | `ACK` |
| 18:10:38.419 | received |  | `` |
| 18:10:38.426 | ack_sent | AR | `ACK` |
| 18:10:40.442 | received |  | `` |
| 18:10:40.444 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 128)
 128 18:10:30.346 in.default -> out.default  [Request/8] 
== event log
18:10:30.365 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 397 because response 10@EnsLib.HL7.Message / 399 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:32.387 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 397 because response 13@EnsLib.HL7.Message / 400 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:34.396 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 397 because response 10@EnsLib.HL7.Message / 401 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:36.413 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 397 because response 13@EnsLib.HL7.Message / 402 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:38.427 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 397 because response 10@EnsLib.HL7.Message / 403 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:40.431 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
18:10:40.431 INFO [out.default] Disconnecting from  lab:6600
18:10:40.436 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:10:40.445 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 8@EnsLib.HL7.Message / 397 because response 13@EnsLib.HL7.Message / 404 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:40.445 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## Same with MSH-9 = ACK^A28^ACK (three components)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR3` | `default-AR3-191040` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126191040||ADT^A28^ADT_A05|default-AR3-191040|P|2.5
    EVN|A28|20261126191040
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261910||ACK^A28|default-AR3-191040|P|2.5
    MSA|CA|default-AR3-191040
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:10:40.854 | received |  | `` |
| 18:10:40.858 | ack_sent | AR | `ACK^A28^ACK` |
| 18:10:42.864 | received |  | `` |
| 18:10:42.868 | ack_sent | AR | `ACK^A28^ACK` |
| 18:10:44.871 | received |  | `` |
| 18:10:44.874 | ack_sent | AR | `ACK^A28^ACK` |
| 18:10:46.882 | received |  | `` |
| 18:10:46.886 | ack_sent | AR | `ACK^A28^ACK` |
| 18:10:48.889 | received |  | `` |
| 18:10:48.892 | ack_sent | AR | `ACK^A28^ACK` |
| 18:10:50.901 | received |  | `` |
| 18:10:50.903 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 129)
 129 18:10:40.853 in.default -> out.default  [Request/8] 
== event log
18:10:40.859 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 13@EnsLib.HL7.Message / 405 because response 10@EnsLib.HL7.Message / 407 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:10:42.869 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 13@EnsLib.HL7.Message / 405 because response 9@EnsLib.HL7.Message / 408 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:44.875 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 13@EnsLib.HL7.Message / 405 because response 10@EnsLib.HL7.Message / 409 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:10:46.888 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 13@EnsLib.HL7.Message / 405 because response 9@EnsLib.HL7.Message / 410 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:48.893 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 13@EnsLib.HL7.Message / 405 because response 10@EnsLib.HL7.Message / 411 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:10:50.894 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
18:10:50.894 INFO [out.default] Disconnecting from  lab:6600
18:10:50.896 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:10:50.904 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 13@EnsLib.HL7.Message / 405 because response 9@EnsLib.HL7.Message / 412 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:10:50.905 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

**Script verdict:** ALL PASSED
