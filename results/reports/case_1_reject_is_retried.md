# Case 1 reject is retried

> Case 1 - the symptom: the lab answers AR (a valid ACK) and the message is sent again and again.
> Default ReplyCodeActions contains :?R=RF  => Retry until FailureTimeout, then Fail.

## AR ACK under the documented default is retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR` | `default-AR-194251` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR|20261126194251||ADT^A28^ADT_A05|default-AR-194251|P|2.5
    EVN|A28|20261126194251
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261942||ACK^A28|default-AR-194251|P|2.5
    MSA|CA|default-AR-194251
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:42:51.469 | received |  | `` |
| 18:42:51.480 | ack_sent | AR | `ACK` |
| 18:42:53.484 | received |  | `` |
| 18:42:53.491 | ack_sent | AR | `ACK` |
| 18:42:55.494 | received |  | `` |
| 18:42:55.498 | ack_sent | AR | `ACK` |
| 18:42:57.504 | received |  | `` |
| 18:42:57.509 | ack_sent | AR | `ACK` |
| 18:42:59.514 | received |  | `` |
| 18:42:59.521 | ack_sent | AR | `ACK` |
| 18:43:01.538 | received |  | `` |
| 18:43:01.541 | ack_sent | AR | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 39)
  39 18:42:51.466 in.default -> out.default  [Request/8] 
== event log
18:42:51.481 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 10@EnsLib.HL7.Message / 113 because response 13@EnsLib.HL7.Message / 115 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:42:53.493 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 10@EnsLib.HL7.Message / 113 because response 11@EnsLib.HL7.Message / 116 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:42:55.499 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 10@EnsLib.HL7.Message / 113 because response 13@EnsLib.HL7.Message / 117 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:42:57.51 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 10@EnsLib.HL7.Message / 113 because response 11@EnsLib.HL7.Message / 118 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:42:59.522 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 10@EnsLib.HL7.Message / 113 because response 13@EnsLib.HL7.Message / 119 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:43:01.525 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
18:43:01.525 INFO [out.default] Disconnecting from  lab:6600
18:43:01.53 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:01.542 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 10@EnsLib.HL7.Message / 113 because response 11@EnsLib.HL7.Message / 120 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:43:01.542 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

## Same with MSH-9 = ACK^A28^ACK (three components)

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `default` | 29201 | `AR3` | `default-AR3-194301` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|AR3|20261126194301||ADT^A28^ADT_A05|default-AR3-194301|P|2.5
    EVN|A28|20261126194301
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|default-AR3-194301|P|2.5
    MSA|CA|default-AR3-194301
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:01.921 | received |  | `` |
| 18:43:01.925 | ack_sent | AR | `ACK^A28^ACK` |
| 18:43:03.927 | received |  | `` |
| 18:43:03.931 | ack_sent | AR | `ACK^A28^ACK` |
| 18:43:05.934 | received |  | `` |
| 18:43:05.938 | ack_sent | AR | `ACK^A28^ACK` |
| 18:43:07.941 | received |  | `` |
| 18:43:07.948 | ack_sent | AR | `ACK^A28^ACK` |
| 18:43:09.950 | received |  | `` |
| 18:43:09.954 | ack_sent | AR | `ACK^A28^ACK` |
| 18:43:11.968 | received |  | `` |
| 18:43:11.973 | ack_sent | AR | `ACK^A28^ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 40)
  40 18:43:01.92 in.default -> out.default  [Request/8] 
== event log
18:43:01.926 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 121 because response 13@EnsLib.HL7.Message / 123 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:43:03.932 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 121 because response 8@EnsLib.HL7.Message / 124 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:43:05.939 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 121 because response 13@EnsLib.HL7.Message / 125 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:43:07.949 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 121 because response 8@EnsLib.HL7.Message / 126 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:43:09.955 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 121 because response 13@EnsLib.HL7.Message / 127 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action co
18:43:11.956 INFO [out.default] Attempting to re-connect on try #6 (ReconnectRetry value is 5
18:43:11.956 INFO [out.default] Disconnecting from  lab:6600
18:43:11.958 INFO [out.default] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:11.974 ERROR [out.default] ERROR <Ens>ErrGeneral: Retrying HL7 Message body 11@EnsLib.HL7.Message / 121 because response 8@EnsLib.HL7.Message / 128 MSA code 'AR' matched ReplyCodeActions 1-6 : ':?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W', resulting in Action cod
18:43:11.975 ERROR [out.default] ERROR <Ens>ErrGeneral: Discarding message on ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrGeneral: Retrying HL7 Message bod
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `RF,RF,RF,RF,RF,RF,RF`

**Verdict:** PASS

**Script verdict:** ALL PASSED
