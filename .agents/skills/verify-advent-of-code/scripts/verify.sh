#!/usr/bin/env bash
# Run the Advent of Code solutions the way the owner does, and keep the evidence.
# Usage: verify.sh <doctor|test|days|real|cleanup|all>
set -uo pipefail

ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
RUN_ID="${VERIFY_RUN:-$(date +%Y%m%d-%H%M%S)}"
ART="${VERIFY_ARTIFACTS:-/tmp/advent-of-code-verify/$RUN_ID}"
mkdir -p "$ART"
cd "$ROOT" || exit 1

# run <name> <cmd...>: records command, stdout, stderr and exit code under $ART/<name>.*
run() {
  local name="$1"; shift
  printf '%q ' "$@" > "$ART/$name.cmd"; echo >> "$ART/$name.cmd"
  "$@" > "$ART/$name.stdout" 2> "$ART/$name.stderr"
  local rc=$?
  echo "$rc" > "$ART/$name.exit"
  echo "[$name] exit=$rc  ($ART/$name.*)"
  return "$rc"
}

expect() {
  local desc="$1" file="$2" pattern="$3"
  if grep -E -- "$pattern" "$file" >/dev/null; then echo "  PASS $desc"; else echo "  FAIL $desc (no /$pattern/ in $file)"; FAILED=1; fi
}

# gate <name> <cmd...>: one pre-PR gate step that must exit 0
gate() {
  local name="$1"; shift
  if run "$name" "$@"; then echo "  PASS $name"; else echo "  FAIL $name (see $ART/$name.stdout/.stderr)"; FAILED=1; fi
}

FAILED=0
SKIPPED=0

doctor_common() {
  echo "artifacts: $ART"
  echo "repo: $ROOT @ $(git rev-parse --short HEAD) ($(git rev-parse --abbrev-ref HEAD))"
  command -v uv >/dev/null || { echo "  FAIL uv not on PATH (https://docs.astral.sh/uv/)"; return 1; }
  echo "  PASS uv $(uv --version | cut -d' ' -f2)"
}

result() {
  if [ "$FAILED" != 0 ]; then echo "RESULT: FAIL ($1)"; elif [ "$SKIPPED" != 0 ]; then echo "RESULT: PASS with SKIP ($1): skipped features are unverified"; else echo "RESULT: PASS ($1)"; fi
  exit "$FAILED"
}

doctor() {
  doctor_common || return 1
  run sync uv sync --locked --all-groups || { echo "  FAIL uv sync --locked --all-groups (stale uv.lock?)"; return 1; }
  local pv; pv="$(uv run --no-sync python -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
  if uv run --no-sync python -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then echo "  PASS python $pv >= 3.11"; else echo "  FAIL python $pv < 3.11"; return 1; fi
  echo "days: $(ls -d [0-9][0-9][0-9][0-9]/[0-9][0-9]/main.py 2>/dev/null | wc -l) day scripts"
}

# CI's steps in order.
test_gate() {
  gate pytest uv run --no-sync pytest -q
  local line; line="$(grep -E '[0-9]+ passed' "$ART/pytest.stdout" | tail -1)"; echo "  pytest: ${line:-no summary line}"
  gate lint uv run --no-sync ruff check .
  gate format uv run --no-sync ruff format --check .
  gate ty uv run --no-sync ty check
}

# Each day in its own process on its committed sample, compared byte for byte
# with the pinned EXPECTED_SAMPLE_OUTPUT in tests/test_cli.py.
days() {
  local f y d name total=0 bad=0
  for f in [0-9][0-9][0-9][0-9]/[0-9][0-9]/main.py; do
    y="${f%%/*}"; d="${f#*/}"; d="${d%%/*}"; name="day-$y-$d"; total=$((total + 1))
    run "$name" uv run --no-sync python -c "import runpy; runpy.run_path('$f')['run']('sample')"
    uv run --no-sync python -c "from tests.test_cli import EXPECTED_SAMPLE_OUTPUT as E; print(E.get(($y, ${d#0}), '<unpinned>'), end='')" > "$ART/$name.expected"
    if [ "$(cat "$ART/$name.exit")" = 0 ] && cmp -s "$ART/$name.expected" "$ART/$name.stdout"; then
      echo "  PASS $y/$d prints its pinned sample answers"
    else
      echo "  FAIL $y/$d (exit $(cat "$ART/$name.exit"); diff $ART/$name.expected $ART/$name.stdout)"; bad=$((bad + 1)); FAILED=1
    fi
  done
  [ "$total" -gt 0 ] || { echo "  FAIL no day scripts found"; FAILED=1; }
  echo "  $((total - bad)) of $total days match"
}

# Real puzzle inputs are git-ignored and never in the repo or CI.
real() {
  local f y d inp n=0
  for f in [0-9][0-9][0-9][0-9]/[0-9][0-9]/main.py; do
    y="${f%%/*}"; d="${f#*/}"; d="${d%%/*}"; inp="inputs/$y/$d.txt"
    [ -f "$inp" ] || continue
    n=$((n + 1))
    run "real-$y-$d" uv run --no-sync python -c "import runpy; runpy.run_path('$f')['run']()"
    expect "$y/$d runs on the real input" "$ART/real-$y-$d.exit" '^0$'
  done
  if [ "$n" = 0 ]; then
    echo "  SKIP real: no real puzzle inputs (inputs/<year>/<DD>.txt) in this checkout; answers on real input are unverified"
    echo "skipped: no real inputs" > "$ART/real.skip"; SKIPPED=1
  fi
}

cleanup() {
  # Nothing long-lived is started; evidence stays.
  echo "cleanup done; evidence kept in $ART"
}

case "${1:-}" in
  doctor) doctor || FAILED=1 ;;
  test) test_gate ;;
  days) days ;;
  real) real ;;
  cleanup) cleanup ;;
  all) if doctor; then test_gate; days; real; else FAILED=1; echo "  doctor failed: not driving this checkout"; fi; cleanup ;;
  *) sed -n '2,3p' "$0"; exit 2 ;;
esac
result "$1"
