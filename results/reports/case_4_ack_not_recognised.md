# Case 4 ack not recognised

> Case 4 - the ACK reached IRIS' socket but never became a usable ACK.
> Retry (if any) comes from the connection logic, NOT from ReplyCodeActions: no 'Action code' in the log.

## ACK without MLLP end block: ErrEndBlock, not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `NOFRAME` | `failrej-NOFRAME-194325` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOFRAME|20261126194325||ADT^A28^ADT_A05|failrej-NOFRAME-194325|P|2.5
    EVN|A28|20261126194325
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|failrej-NOFRAME-194325|P|2.5
    MSA|CA|failrej-NOFRAME-194325
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:25.699 | received |  | `` |
| 18:43:25.708 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 47)
  47 18:43:25.697 in.failrej -> out.failrej  [Request/8] 
== event log
18:43:30.735 ERROR [out.failrej] ERROR <EnsEDIHL7>ErrEndBlock: Received unexpected EndBlock '' in input "", expected 'er, on |TCP|6600|1444'
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## Socket closed without ACK: reconnect and resend until FailureTimeout

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `CLOSE` | `failrej-CLOSE-194331` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|CLOSE|20261126194332||ADT^A28^ADT_A05|failrej-CLOSE-194331|P|2.5
    EVN|A28|20261126194332
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|failrej-CLOSE-194331|P|2.5
    MSA|CA|failrej-CLOSE-194331
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:32.023 | received |  | `` |
| 18:43:32.028 | closing_without_ack |  | `` |
| 18:43:34.044 | received |  | `` |
| 18:43:34.048 | closing_without_ack |  | `` |
| 18:43:36.061 | received |  | `` |
| 18:43:36.064 | closing_without_ack |  | `` |
| 18:43:38.078 | received |  | `` |
| 18:43:38.081 | closing_without_ack |  | `` |
| 18:43:40.090 | received |  | `` |
| 18:43:40.098 | closing_without_ack |  | `` |
| 18:43:42.116 | received |  | `` |
| 18:43:42.119 | closing_without_ack |  | `` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 48)
  48 18:43:32.022 in.failrej -> out.failrej  [Request/8] 
== event log
18:43:32.032 INFO [out.failrej] Disconnecting from  lab:6600
18:43:32.032 ERROR [out.failrej] ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #5002: ObjectScript error: <READ>ReadLine+11^%IO.DeviceStream.1
18:43:34.037 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:34.052 INFO [out.failrej] Disconnecting from  lab:6600
18:43:36.057 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:36.067 INFO [out.failrej] Disconnecting from  lab:6600
18:43:38.071 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:38.084 INFO [out.failrej] Disconnecting from  lab:6600
18:43:40.087 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:40.103 INFO [out.failrej] Disconnecting from  lab:6600
18:43:42.11 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:42.121 INFO [out.failrej] Disconnecting from  lab:6600
18:43:42.122 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## ACK after 12 s > ResponseTimeout 5 s: read timeout, resent

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `LATE` | `failrej-LATE-194342` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|LATE|20261126194342||ADT^A28^ADT_A05|failrej-LATE-194342|P|2.5
    EVN|A28|20261126194342
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261943||ACK^A28|failrej-LATE-194342|P|2.5
    MSA|CA|failrej-LATE-194342
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:43:42.476 | received |  | `` |
| 18:43:54.481 | ack_sent | AA | `ACK` |
| 18:43:54.488 | received |  | `` |
| 18:44:06.496 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 49)
  49 18:43:42.471 in.failrej -> out.failrej  [Request/8] 
== event log
18:43:42.472 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:43:47.49 ERROR [out.failrej] ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for terminator SegTerminatorAscii=13, on |TCP|6600|1444, data received =''
18:43:52.508 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for term
```

**Result:** deliveries = **2**, final status = **Error**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
