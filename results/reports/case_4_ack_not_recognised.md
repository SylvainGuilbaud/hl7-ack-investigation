# Case 4 ack not recognised

> Case 4 - the ACK reached IRIS' socket but never became a usable ACK.
> Retry (if any) comes from the connection logic, NOT from ReplyCodeActions: no 'Action code' in the log.

## ACK without MLLP end block: ErrEndBlock, not retried

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `NOFRAME` | `failrej-NOFRAME-191104` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|NOFRAME|20261126191104||ADT^A28^ADT_A05|failrej-NOFRAME-191104|P|2.5
    EVN|A28|20261126191104
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|failrej-NOFRAME-191104|P|2.5
    MSA|CA|failrej-NOFRAME-191104
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:04.835 | received |  | `` |
| 18:11:04.839 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 136)
 136 18:11:04.834 in.failrej -> out.failrej  [Request/8] 
== event log
18:11:09.844 ERROR [out.failrej] ERROR <EnsEDIHL7>ErrEndBlock: Received unexpected EndBlock '' in input "", expected 'er, on |TCP|6600|3724'
```

**Result:** deliveries = **1**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## Socket closed without ACK: reconnect and resend until FailureTimeout

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `CLOSE` | `failrej-CLOSE-191111` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|CLOSE|20261126191111||ADT^A28^ADT_A05|failrej-CLOSE-191111|P|2.5
    EVN|A28|20261126191111
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|failrej-CLOSE-191111|P|2.5
    MSA|CA|failrej-CLOSE-191111
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:11.261 | received |  | `` |
| 18:11:11.264 | closing_without_ack |  | `` |
| 18:11:13.275 | received |  | `` |
| 18:11:13.277 | closing_without_ack |  | `` |
| 18:11:15.287 | received |  | `` |
| 18:11:15.289 | closing_without_ack |  | `` |
| 18:11:17.306 | received |  | `` |
| 18:11:17.309 | closing_without_ack |  | `` |
| 18:11:19.320 | received |  | `` |
| 18:11:19.323 | closing_without_ack |  | `` |
| 18:11:21.335 | received |  | `` |
| 18:11:21.337 | closing_without_ack |  | `` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 137)
 137 18:11:11.26 in.failrej -> out.failrej  [Request/8] 
== event log
18:11:11.27 INFO [out.failrej] Disconnecting from  lab:6600
18:11:11.271 ERROR [out.failrej] ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #5002: ObjectScript error: <READ>ReadLine+11^%IO.DeviceStream.1
18:11:13.272 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:11:13.279 INFO [out.failrej] Disconnecting from  lab:6600
18:11:15.283 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:11:15.291 INFO [out.failrej] Disconnecting from  lab:6600
18:11:17.301 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:11:17.312 INFO [out.failrej] Disconnecting from  lab:6600
18:11:19.314 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:11:19.327 INFO [out.failrej] Disconnecting from  lab:6600
18:11:21.331 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:11:21.339 INFO [out.failrej] Disconnecting from  lab:6600
18:11:21.34 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrOutConnectionLost: Lost HL7 Read connection to lab:6600 - detected via ERROR #5
```

**Result:** deliveries = **6**, final status = **Error**, action codes = `-`

**Verdict:** PASS

## ACK after 12 s > ResponseTimeout 5 s: read timeout, resent

| case | port | lab mode (MSH-6) | control id |
|---|---|---|---|
| `failrej` | 29202 | `LATE` | `failrej-LATE-191121` |

### Sent, and what the sender gets back from IRIS

```text
SENT:
    MSH|^~\&|PAS|HOSP|IRIS|LATE|20261126191121||ADT^A28^ADT_A05|failrej-LATE-191121|P|2.5
    EVN|A28|20261126191121
    PID|1||123456^^^PAS^MR||DOE^JANE||19800101|F
    PV1|1|N
ANSWER TO THE SENDER (after 0.0s) :
    MSH|^~\&|EnsembleHL7|ISC|PAS|HOSP|202611261911||ACK^A28|failrej-LATE-191121|P|2.5
    MSA|CA|failrej-LATE-191121
```

### What the downstream lab saw and answered (`results/dashboard/lab2026-11-26.jsonl`)

| time | event | MSA-1 | MSH-9 |
|---|---|---|---|
| 18:11:21.746 | received |  | `` |
| 18:11:33.750 | ack_sent | AA | `ACK` |
| 18:11:33.763 | received |  | `` |
| 18:11:45.771 | ack_sent | AA | `ACK` |

### What IRIS recorded (`Repro.Trace.Report`)

```text
== message headers (session 138)
 138 18:11:21.741 in.failrej -> out.failrej  [Request/8] 
== event log
18:11:21.742 INFO [out.failrej] Opened TCP connection from local address 192.168.204.83 to remote address lab:6600
18:11:26.75 ERROR [out.failrej] ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for terminator SegTerminatorAscii=13, on |TCP|6600|3724, data received =''
18:11:31.755 ERROR [out.failrej] ERROR <Ens>ErrFailureTimeout: FailureTimeout of 10 seconds exceeded in EnsLib.HL7.Operation.TCPOperation; status from last attempt was ERROR <Ens>ErrTCPTerminatedReadTimeoutExpired: TCP Read timeout (5) expired waiting for term
```

**Result:** deliveries = **2**, final status = **Error**, action codes = `-`

**Verdict:** PASS

**Script verdict:** ALL PASSED
