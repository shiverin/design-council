#!/usr/bin/env bash
# Tests for council_lint.py. Exit 0 when all pass.
set -u
D="$(cd "$(dirname "$0")" && pwd)"; L="$D/../scripts/council_lint.py"; F="$D/fixtures"
pass=0; fail=0
t() { local name="$1" want="$2"; shift 2; "$@" >/dev/null 2>&1; local got=$?
  if [ "$got" -eq "$want" ]; then pass=$((pass+1)); echo "PASS $name"; else fail=$((fail+1)); echo "FAIL $name (want $want got $got)"; fi; }
has() { python3 -I "$L" "$1" | grep -q "\[[a-z]*:$2\]"; }
t "bad.tsx flags" 1 python3 -I "$L" "$F/bad.tsx"
t "clean.tsx clean" 0 python3 -I "$L" "$F/clean.tsx"
t "bad.css flags" 1 python3 -I "$L" "$F/bad.css"
t "clean.css clean" 0 python3 -I "$L" "$F/clean.css"
t "no args usage" 2 python3 -I "$L"
for r in transition-all pulse-non-loader hover-scale gradient-text purple-blue-gradient welcome-back emoji hype-word arbitrary-spacing; do
  t "bad.tsx has $r" 0 has "$F/bad.tsx" "$r"; done
for r in transition-all purple-blue-gradient gradient-text default-font tracked-caps-label off-grid-px outline-none animate-layout-prop no-reduced-motion; do
  t "bad.css has $r" 0 has "$F/bad.css" "$r"; done
echo "$pass passed, $fail failed"; [ "$fail" -eq 0 ]
