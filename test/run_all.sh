#!/usr/bin/env bash
# Runs the test scripts; each writes a Markdown report to results/reports/<script>.md,
# and results/reports/README.md indexes them. Full run ~6 minutes.
# usage: test/run_all.sh [1 3 ...]     (script numbers; default: all)
set -u
cd "$(dirname "$0")/.."
OUT=results/reports; mkdir -p "$OUT"
docker exec hl7ack-iris true 2>/dev/null || { echo "stack not running: docker compose up -d --build"; exit 2; }
rc=0
IDX="$OUT/README.md"
{ echo "# Test reports"; echo; echo "Run: $(date '+%Y-%m-%d %H:%M:%S'), image: $(docker exec hl7ack-iris iris qlist 2>/dev/null | cut -d^ -f3)"; echo
  echo "| script | tests | passed | report |"; echo "|---|---:|---:|---|"; } > "$IDX"
for f in test/case_*.py; do
  n=$(basename "$f" .py); num=${n#case_}; num=${num%%_*}
  if [ $# -gt 0 ] && ! printf '%s\n' "$@" | grep -qx "$num"; then continue; fi
  echo ">> $n"
  python3 -I "$f" > "$OUT/$n.md" 2>&1; r=$?
  tot=$(grep -c '^\*\*Verdict' "$OUT/$n.md"); ok=$(grep -c '^\*\*Verdict:\*\* PASS' "$OUT/$n.md")
  grep -E '^\*\*Verdict' "$OUT/$n.md" | sed 's/^/   /'
  echo "| $n | $tot | $ok | [$n.md]($n.md) |" >> "$IDX"
  [ $r -ne 0 ] && rc=1
done
echo; [ $rc -eq 0 ] && echo "ALL PASSED - reports in $OUT/ (index: $IDX)" || echo "FAILURES - see $OUT/"
exit $rc
