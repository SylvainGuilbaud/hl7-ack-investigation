# Case 4 ack not recognised

> Case 4 - the ACK reached IRIS' socket but never became a usable ACK.
> Retry (if any) comes from the connection logic, NOT from ReplyCodeActions: no 'Action code' in the log.

## ACK without MLLP end block: ErrEndBlock, not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `NOFRAME` | `failrej-NOFRAME-162539` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOFRAME|20261126162539||ADT^A28^ADT_A05|failrej-NOFRAME-162539|P|2.5
    EVN|A28|20261126162539
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|failrej-NOFRAME-162539|P|2.5
    MSA|CA|failrej-NOFRAME-162539
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:39.351 | received |  | `` |
| 15:25:39.356 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 39)
  39 15:25:39.348 in.failrej -> out.failrej  [Request/8] 
== event log
15:25:44.37 ERROR [out.failrej] ERROR <EnsEDIHL7>ErrEndBlock: Received unexpected EndBlock '' in input "", expected 'er, on |TCP|6600|682'
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## Socket closed without ACK: reconnect and resend until FailureTimeout

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `CLOSE` | `failrej-CLOSE-162545` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|CLOSE|20261126162545||ADT^A28^ADT_A05|failrej-CLOSE-162545|P|2.5
    EVN|A28|20261126162545
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|failrej-CLOSE-162545|P|2.5
    MSA|CA|failrej-CLOSE-162545
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:45.668 | received |  | `` |
| 15:25:45.672 | closing_without_ack |  | `` |
| 15:25:47.684 | received |  | `` |
| 15:25:47.686 | closing_without_ack |  | `` |
| 15:25:49.695 | received |  | `` |
| 15:25:49.697 | closing_without_ack |  | `` |
| 15:25:51.705 | received |  | `` |
| 15:25:51.709 | closing_without_ack |  | `` |
| 15:25:53.721 | received |  | `` |
| 15:25:53.724 | closing_without_ack |  | `` |
| 15:25:55.739 | received |  | `` |
| 15:25:55.742 | closing_without_ack |  | `` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 40)
  40 15:25:45.667 in.failrej -> out.failrej  [Request/8] 
== event log
15:25:45.675 INFO [out.failrej] Disconnecting from  lab:6600
15:25:45.676 ERROR [out.failrej] ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #5002: ObjectScript error: <READ>ReadLine+11^%IO.DeviceStream.1
15:25:47.68 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:47.689 INFO [out.failrej] Disconnecting from  lab:6600
15:25:49.691 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:49.7 INFO [out.failrej] Disconnecting from  lab:6600
15:25:51.701 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:51.711 INFO [out.failrej] Disconnecting from  lab:6600
15:25:53.716 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:53.728 INFO [out.failrej] Disconnecting from  lab:6600
15:25:55.733 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:25:55.744 INFO [out.failrej] Disconnecting from  lab:6600
15:25:55.745 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## ACK after 12 s > ResponseTimeout 5 s: read timeout, resent

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `LATE` | `failrej-LATE-162556` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|LATE|20261126162556||ADT^A28^ADT_A05|failrej-LATE-162556|P|2.5
    EVN|A28|20261126162556
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261625||ACK^A28|failrej-LATE-162556|P|2.5
    MSA|CA|failrej-LATE-162556
```

### What the downstream lab saw and answered (`results/lab.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 15:25:56.175 | received |  | `` |
| 15:26:08.180 | ack_sent | AA | `ACK` |
| 15:26:08.184 | received |  | `` |
| 15:26:20.189 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 41)
  41 15:25:56.17 in.failrej -> out.failrej  [Request/8] 
== event log
15:25:56.171 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
15:26:01.185 ERROR [out.failrej] ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for terminator SegTerminatorAscii=13, on |TCP|6600|682, data received =''
15:26:06.192 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for term
```

**Result:** deliveries = **2**, final status = **Error**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
