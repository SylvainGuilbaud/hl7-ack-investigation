# Open Exchange description

## HL7 ACK Investigation Lab

### Docker lab that reproduces "the ACK arrived, so why is my HL7 message still retried?" in IRIS for Health, with traces, a test matrix and a dashboard.

## Full description

When an HL7 TCP operation gets a valid ACK and still resends the message, the cause isn't always `ReplyCodeActions`. This lab reproduces the symptom with synthetic messages and gives you a repeatable investigation method.

- **Stack:** one `docker compose up` starts IRIS for Health community (`latest-cd`, tested on 2026.3) with a ready production, plus a small Python HL7 receiver that answers `AA`, `AE`, `AR`, `ACK^A28^ACK`, an ACK for another message, no `MSA`, no MLLP end block, a closed socket, or a late ACK.
- **Production:** 11 inbound services cross three `ReplyCodeActions` variants with five `AckMode` values (`Immed`, `App`, `Msh`, `Never`, `Byte`). Because the receiver logs every delivery outside IRIS, you can count how many times a message was really sent.
- **Tests:** 24 scripted tests, each writing a Markdown report (message sent, ACK received, IRIS trace, PASS/FAIL), plus a 99-row matrix.
- **Dashboard:** `tools/dashboard.py` turns the receiver's log into one page, with a link to each message's Visual Trace.
- **What it shows:**
  - The default `:?R=RF` retries `AR` for the whole `FailureTimeout`.
  - Closed, late and unframed ACKs are retried by the connection layer, with no action code in the log.
  - With `AckMode=App`, a failed operation gives the sender an IRIS-built `CE`, and a suspended one gives it nothing.
- **Article:** the companion article walks through the six-step investigation method and a decision flow.

Quick start:

```bash
docker compose up -d --build
test/run_all.sh
python3 tools/dashboard.py --open
```

## Suggested tags / categories

HL7, Interoperability, ACK, ReplyCodeActions, Health Connect, Docker, Troubleshooting, Testing

## Fields to fill in on the form

- **Product version:** 2026.3 (the version actually tested)
- **Repository URL:** https://github.com/SylvainGuilbaud/hl7-ack-investigation
- **License:** MIT
- **Article link:** add the Developer Community post URL once it's published
