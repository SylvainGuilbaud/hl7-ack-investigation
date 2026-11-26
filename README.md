# The ACK arrived — why is my HL7 message still being retried?

Standalone lab for the InterSystems Developer Community article. Everything is synthetic.

```
sender ──MLLP──▶ in.<case> ──▶ out.<case> ──MLLP──▶ lab (Python simulator, :6600)
 (tools/send.py)  HL7 TCP service  HL7 TCP operation     answers AA/AE/AR/… on demand
                  AckMode varies   ReplyCodeActions varies
```

* **IRIS**: `irishealth-community:latest-cd` (set `IRIS_IMAGE` in `.env`; pin a tag for reproducibility).
  Built at image time: namespace `REPRO`, production `Repro.Production` auto-started. `_SYSTEM`/`SuperUser` password `SYS`.
* **lab** (`simulator/lab.py`): stdlib-only MLLP receiver. It reads **MSH-6** of what it receives and misbehaves accordingly,
  and logs every delivery to `results/lab.jsonl` — so "how many times was it sent" is counted *outside* IRIS.
* One service/operation pair per `ReplyCodeActions` variant; all other settings are identical
  (`ResponseTimeout=5`, `RetryInterval=2`, `FailureTimeout=10`, `ArchiveIO=1` on every item).

| case | `ReplyCodeActions` |
|---|---|
| `default` | empty → documented default `:?R=RF,:?E=S,:~=S,:?A=C,:*=S,:I?=W,:T?=C` |
| `failrej` | `:?R=F,:?E=S,:~=S,:?A=C,:*=S,:I?=W,:T?=C` (only change: `RF` → `F`) |
| `legacy`  | `:?R=W,:?E=W,:~=F,:?A=C,:T?=C,:*=F` (an "inherited" string) |

Two things vary independently. **ReplyCodeActions** (operation, how IRIS reacts to the lab's ACK) and
**AckMode** (service, what the *sender* gets back):

| service | port | AckMode | operation |
|---|---|---|---|
| `in.default` / `in.failrej` / `in.legacy` | 29201-29203 | `Immed` | `out.default` / `out.failrej` / `out.legacy` |
| `in.app.default` / `in.app.failrej` / `in.app.legacy` | 29211-29213 | `App` | same three operations |
| `in.msh.failrej` | 29214 | `Msh` (MSH-15/16 of the message decide) | `out.failrej` |
| `in.never.failrej` | 29215 | `Never` | `out.failrej` |
| `in.byte.failrej` | 29216 | `Byte` | `out.failrej` |

## Run it

```bash
docker compose up -d --build          # ~2 min first time
python3 tools/send.py localhost 29201 AR demo-1       # ports: see the table above
SEND_WAIT=15 python3 tools/send.py localhost 29211 AR demo-2   # AckMode=App; optional args: MSH-15 MSH-16
docker exec -i hl7ack-iris iris session IRIS -U REPRO <<< 'do ##class(Repro.Trace).Report("demo-1")'
python3 tools/matrix.py               # all 11 services x 9 lab modes = 99 rows, ~20 min, writes results/matrix.md
```
Management Portal: http://localhost:9772/csp/sys/UtilHome.csp (namespace `REPRO`). `tools/gen_production.py` regenerates `Production.cls` from its CASES table.

Lab modes (MSH-6): `AA AE AR AR3`(AR with MSH-9 `ACK^A28^ACK`) `OTHERID`(AA whose MSA-2 is the control id of *another* message) `NOMSA` `NOFRAME`(no MLLP end block) `CLOSE`(socket closed, no ACK) `LATE`(AA after 12 s).

## Tests (`test/`)

Six scripts, 24 tests, each one sends a synthetic message, then writes a **Markdown report**: what was sent, the ACK the sender got,
what the lab received/answered, the IRIS trace, and a PASS/FAIL verdict against the expected behaviour.

| script | shows |
|---|---|
| `case_1_reject_is_retried` | the symptom: `AR` / `ACK^A28^ACK` retried under the default |
| `case_2_corrected` | `:?R=F`: same ACK, one delivery |
| `case_3_swallowed_rejection` | the legacy string hides the rejection (`CW`) |
| `case_4_ack_not_recognised` | unframed, dropped and late ACKs: retry without any `Action code` |
| `case_5_ack_content_checks` | `AE`, no MSA, an ACK for another message (MSA-2 mismatch) under the default |
| `case_6_ackmode` | `AckMode` `App` / `Msh` / `Never` / `Byte`: what the **sender** receives (the lab's real ACK or not) |

```bash
test/run_all.sh          # all, ~8 min -> results/reports/*.md + results/reports/README.md (index)
test/run_all.sh 1 4      # selected scripts
python3 -I test/case_2_corrected.py   # one script, report on stdout
```
A reference run is committed in `docs/reports/`.

## The investigation, in the order that worked

1. **Count deliveries at the receiver**, not in IRIS (`results/lab.jsonl`). Is it really being resent, and at what interval?
2. **Look at what the receiver actually answered** (`MSA-1`, `MSA-2`, `MSH-9`) — the ACK the *sender* sees from IRIS (`MSA|CA`, `AckMode=Immed`) is a different ACK.
3. **Read the Event Log of the session** (`Repro.Trace.Report`). The text `matched ReplyCodeActions … resulting in Action code XX` names the entry that fired and the action taken.
4. **Check the effective `ReplyCodeActions`** (blank ≠ nothing: blank means the default string above) and remember: entries are evaluated left to right, **the first non-warning match wins**.
5. Only then change a setting, and re-run the matrix.

## Results (2026.3.0.212, see `docs/matrix.md`, traces in `docs/traces/`)

| lab answers | `default` | `failrej` | `legacy` |
|---|---|---|---|
| AA | 1 delivery, Completed | same | same |
| AE | 1, Suspended (`S`) | same | 1, Completed (`CW`) |
| **AR** | **6 deliveries**, Error (`RF`, retried until FailureTimeout) | **1**, Error (`F`) | 1, Completed (`CW`) — rejection silently accepted |
| **AR3** (`ACK^A28^ACK`) | **6**, Error | **1**, Error | 1, Completed (`CW`) |
| AA for another message (MSA-2 mismatch) | 1, Completed, **no warning** (`:?A=C` matches before `:I?=W`) | same | same |
| no MSA | 1, Suspended | same | 1, Error (`F`) |
| ACK without MLLP end block | 1, Error `ErrEndBlock`, no retry | same | same |
| socket closed, no ACK | **6**, Error (connection-loss retry) | **6** | **6** |
| ACK after 12 s (> ResponseTimeout 5) | **2**, Error (timeout, retried once before FailureTimeout) | **2** | **2** |

### What the sender gets (`AckMode`), 2026.3 — `case_6`

| AckMode | lab answers | operation result | sender receives |
|---|---|---|---|
| `Immed` | anything | anything | IRIS' own `MSA|CA`, immediately — the lab's ACK is never seen |
| `App` | AA | Completed | **the lab's real ACK** (MSH-3 `LAB`) |
| `App` | AR, default | Error after 6 deliveries | IRIS-built `MSA|CE` after ~10 s (log: *Constructing ACK with code CE because SendRequestSync() … returned with no response object*) |
| `App` | AR, `:?R=F` | Error, 1 delivery | IRIS-built `MSA|CE` at once |
| `App` | AR, legacy string | Completed (`CW`) | **the lab's real `AR`** |
| `App` | AE, suspended (`S`) | Suspended | **nothing** (observed ≥ 100 s) — a sender with its own timeout will resend |
| `Msh` | AR | Error | `CA` if MSH-15=AL, IRIS-built `CE` if MSH-16=AL, nothing if neither |
| `Never` | AR | Error | nothing |
| `Byte` | AR | Error | one `0x06` byte ("OK") |

So the real downstream ACK only reaches the sender when the operation *completes*; a failure replaces it with a synthetic `CE`,
and a suspension replaces it with silence — which is another way a message ends up resent, this time by the sender.

Takeaways: three different causes of "ACK arrived, still retried" — (a) an `AR` under the default `:?R=RF`;
(b) an ACK IRIS never recognised as one (late, unframed, connection dropped) which is retried by the adapter's
connection logic, **not** by ReplyCodeActions (no `Action code` in the log); (c) copying `R` into a custom string.
`failrej` fixes only (a); (b) needs the receiver or `ResponseTimeout` fixed.

## Caveats
* Tested on `latest-cd` = **2026.3**, not 2026.2 — set `IRIS_IMAGE` to a 2026.2 image if the article must say 2026.2.
* `F` on AR leaves the message in Error and the sender is not told (`AckMode=Immed`); alerting/resubmit is a business decision, not shown here.
* The 7th `RF` in the Summary column for AR is the final "Discarding message" log line quoting the last attempt, not a 7th delivery.
