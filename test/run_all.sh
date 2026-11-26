#!/usr/bin/env bash
# Runs the test scripts; each writes a Markdown report to results/reports/<script>.md,
# and results/reports/README.md indexes them. Full run ~8 minutes.
# The lab container logs to its OWN file, results/dashboard/lab<YYYY-MM-DD>.jsonl (new container => new log); at the end
# this script builds results/dashboard/dashboard<YYYY-MM-DD>.html from it (results/dashboard/ is git-ignored). The committed reference (results/lab.jsonl,
# dashboard.html, sessions.json - the ones the article quotes) is never touched.
# usage: test/run_all.sh [1 3 ...]     (script numbers; default: all)
set -u
cd "$(dirname "$0")/.."
OUT=results/reports; mkdir -p "$OUT"
docker exec hl7ack-iris true 2>/dev/null || { echo "stack not running: docker compose up -d --build"; exit 2; }
rc=0
IDX="$OUT/README.md"
# The lab container must be up. Its log file may not exist yet (fresh install, or results/dashboard/ emptied): the lab
# (re)creates it, and its .lab-current pointer, when it starts and on every message, so this is not an error.
[ "$(docker inspect -f '{{.State.Running}}' hl7ack-lab 2>/dev/null)" = "true" ] || { echo "the lab container (hl7ack-lab) is not running: docker compose up -d --build"; exit 2; }
LOG=$(python3 -B -I -c "import sys; sys.path.insert(0,'tools'); from labpath import current_log; print(current_log())")
echo "lab log of this run: $LOG$([ -f "$LOG" ] || echo ' (created by the lab on the first message)')"

# One run at a time: the operations are single-threaded and the lab answers on one connection, so two concurrent
# runs (or a run plus a hand-made test) delay and mix each other's messages and give false FAILs.
LOCK=results/dashboard/.run_all.lock
mkdir -p results/dashboard
if ! mkdir "$LOCK" 2>/dev/null; then
  other=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$other" ] && kill -0 "$other" 2>/dev/null; then
    echo "another run_all.sh is already running (pid $other): wait for it or cancel it (kill $other)"; exit 3
  fi
  echo "removing a stale lock (pid ${other:-?} is gone)"; rm -f "$LOCK/pid"; rmdir "$LOCK"; mkdir "$LOCK"
fi
echo $$ > "$LOCK/pid"

# Build results/dashboard/dashboard<date>.html + sessions<date>.json whenever the script ends: after the last test,
# after a failure, and also when it is cancelled (Ctrl-C / kill) - tests already run are in the lab log.
build_dashboard() {
  trap - EXIT
  rm -f "$LOCK/pid"; rmdir "$LOCK" 2>/dev/null
  echo
  python3 -B -I tools/dashboard.py || echo "dashboard generation failed"
  { echo; echo "- dashboard: \`$(python3 -B -I -c "import sys; sys.path.insert(0,'tools'); from labpath import current_log, sibling; print(sibling(current_log(),'dashboard','.html').name)")\` from \`$(python3 -B -I -c "import sys; sys.path.insert(0,'tools'); from labpath import current_log; print(current_log().name)")\`"; } >> "$IDX"
}
trap build_dashboard EXIT
trap 'echo; echo "interrupted"; exit 130' INT TERM
{ echo "# Test reports"; echo; echo "Run: $(date '+%Y-%m-%d %H:%M:%S'), image: $(docker exec hl7ack-iris iris qlist 2>/dev/null | cut -d^ -f3)"; echo
  echo "| script | tests | passed | report |"; echo "|---|---:|---:|---|"; } > "$IDX"
for f in test/case_*.py; do
  n=$(basename "$f" .py); num=${n#case_}; num=${num%%_*}
  if [ $# -gt 0 ] && ! printf '%s\n' "$@" | grep -qx "$num"; then continue; fi
  echo ">> $n"
  python3 -B -I "$f" > "$OUT/$n.md" 2>&1; r=$?
  tot=$(grep -c '^\*\*Verdict' "$OUT/$n.md"); ok=$(grep -c '^\*\*Verdict:\*\* PASS' "$OUT/$n.md")
  grep -E '^\*\*Verdict' "$OUT/$n.md" | sed 's/^/   /'
  echo "| $n | $tot | $ok | [$n.md]($n.md) |" >> "$IDX"
  [ $r -ne 0 ] && rc=1
done
echo
[ $rc -eq 0 ] && echo "ALL PASSED - reports in $OUT/ (index: $IDX)" || echo "FAILURES - see $OUT/"
exit $rc
