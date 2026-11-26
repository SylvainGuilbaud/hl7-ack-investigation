# Case 4 ack not recognised

> Case 4 - the ACK reached IRIS' socket but never became a usable ACK.
> Retry (if any) comes from the connection logic, NOT from ReplyCodeActions: no 'Action code' in the log.

## ACK without MLLP end block: ErrEndBlock, not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `NOFRAME` | `failrej-NOFRAME-20035897` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOFRAME|20261126200359||ADT^A28^ADT_A05|failrej-NOFRAME-20035897|P|2.5
    EVN|A28|20261126200359
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262003||ACK^A28|failrej-NOFRAME-20035897|P|2.5
    MSA|CA|failrej-NOFRAME-20035897
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:03:59.039 | received |  | `` |
| 19:03:59.044 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 286)
 286 19:03:59.037 in.failrej -> out.failrej  [Request/8] 
== event log
19:04:04.068 ERROR [out.failrej] ERROR <EnsEDIHL7>ErrEndBlock: Received unexpected EndBlock '' in input "", expected 'er, on |TCP|6600|9240'
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## Socket closed without ACK: reconnect and resend until FailureTimeout

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `CLOSE` | `failrej-CLOSE-20040587` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|CLOSE|20261126200405||ADT^A28^ADT_A05|failrej-CLOSE-20040587|P|2.5
    EVN|A28|20261126200405
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|failrej-CLOSE-20040587|P|2.5
    MSA|CA|failrej-CLOSE-20040587
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:05.920 | received |  | `` |
| 19:04:05.924 | closing_without_ack |  | `` |
| 19:04:07.935 | received |  | `` |
| 19:04:07.938 | closing_without_ack |  | `` |
| 19:04:09.950 | received |  | `` |
| 19:04:09.953 | closing_without_ack |  | `` |
| 19:04:11.964 | received |  | `` |
| 19:04:11.967 | closing_without_ack |  | `` |
| 19:04:13.979 | received |  | `` |
| 19:04:13.982 | closing_without_ack |  | `` |
| 19:04:15.994 | received |  | `` |
| 19:04:16.004 | closing_without_ack |  | `` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 299)
 299 19:04:05.919 in.failrej -> out.failrej  [Request/8] 
== event log
19:04:05.928 INFO [out.failrej] Disconnecting from  lab:6600
19:04:05.928 ERROR [out.failrej] ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #5002: ObjectScript error: <READ>ReadLine+11^%IO.DeviceStream.1
19:04:07.93 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:07.942 INFO [out.failrej] Disconnecting from  lab:6600
19:04:09.944 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:09.956 INFO [out.failrej] Disconnecting from  lab:6600
19:04:11.959 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:11.971 INFO [out.failrej] Disconnecting from  lab:6600
19:04:13.973 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:13.986 INFO [out.failrej] Disconnecting from  lab:6600
19:04:15.989 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
19:04:16.014 INFO [out.failrej] Disconnecting from  lab:6600
19:04:16.018 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## ACK after 12 s > ResponseTimeout 5 s: read timeout, resent

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `LATE` | `failrej-LATE-20041765` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|LATE|20261126200417||ADT^A28^ADT_A05|failrej-LATE-20041765|P|2.5
    EVN|A28|20261126200417
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611262004||ACK^A28|failrej-LATE-20041765|P|2.5
    MSA|CA|failrej-LATE-20041765
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 19:04:17.705 | received |  | `` |
| 19:04:29.714 | ack_sent | AA | `ACK` |
| 19:04:29.721 | received |  | `` |
| 19:04:41.725 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 306)
 306 19:04:17.704 in.failrej -> out.failrej  [Request/8] 
== event log
19:04:22.73 ERROR [out.failrej] ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for terminator SegTerminatorAscii=13, on |TCP|6600|9240, data received =''
19:04:27.761 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for term
```

**Result:** deliveries = **2**, final status = **Error**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
