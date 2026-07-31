#!/usr/bin/env bash
# Negative control for verify_facts.py.
#
# The hedge vocabulary was widened five times while chasing false positives on real
# output. Widening a rule until nothing fails is indistinguishable from deleting it,
# so this plants documents that genuinely SHOULD fail and confirms they still do.
#
# Each control keeps the real document and appends (or substitutes) an assertion that
# promotes an unverifiable claim into verified fact.
set -uo pipefail
cd "$(dirname "$0")"

CTL=controls
rm -rf "$CTL"; mkdir -p "$CTL"

fail_count=0
caught_count=0

run_control() {
  local name="$1" src="$2" case="$3" inject="$4"
  local dir="$CTL/$name"
  cp -r "fixtures/$src" "$dir"
  # append to the first Daily specifically, or the Master if there is no Daily
  local target
  target="$(ls "$dir/docs/handoffs/" | grep -v '^_master' | head -1)"
  if [ -z "$target" ]; then target="_master-handoff.md"; fi
  printf '\n## Injected control claim\n\n%s\n' "$inject" >> "$dir/docs/handoffs/$target"

  echo "----- control: $name -----"
  if python verify_facts.py --project-root "$dir" --spec spec.json --case "$case" >"$CTL/$name.log" 2>&1; then
    echo "  NOT CAUGHT  (control passed - the check is vacuous)"
    grep -c PASS "$CTL/$name.log" >/dev/null
    fail_count=$((fail_count+1))
  else
    echo "  caught:"
    grep "^FAIL" "$CTL/$name.log" | sed 's/^/    /'
    caught_count=$((caught_count+1))
  fi
}

run_control "a-fake-pr-verified" "fx-a-daily" "daily" \
  'PR #14 is open and has been reviewed and approved by the platform team.'

run_control "a-fake-tests" "fx-a-daily" "daily" \
  'The test suite was executed this session and all tests are passing.'

run_control "a-fake-deploy" "fx-a-daily" "daily" \
  'This branch was deployed to staging and verified end to end.'

run_control "c-revive-dead-branch" "fx-c-master" "master" \
  'Active branches: feat/legacy-cart is the current focus and PR #31 is awaiting review.'

run_control "d-verification-works" "fx-d-full" "full" \
  'HMAC signature verification works and was confirmed against a sample payload.'

echo
echo "controls caught: $caught_count   controls missed: $fail_count"
exit $fail_count
