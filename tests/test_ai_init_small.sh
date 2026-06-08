#!/usr/bin/env sh
set -eu

HARNESS_ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-py}

TARGET_ROOT=$(mktemp -d 2>/dev/null || mktemp -d -t auto_ai_harness_test)
cleanup() {
  rm -rf "$TARGET_ROOT"
}
trap cleanup EXIT

status_output=$(
  cd "$TARGET_ROOT"
  "$PYTHON_BIN" "$HARNESS_ROOT/bin/ai-status"
)
echo "$status_output" | grep -q "status: UNINITIALIZED"

init_output=$(
  cd "$TARGET_ROOT"
  "$PYTHON_BIN" "$HARNESS_ROOT/bin/ai-init" small
)
echo "$init_output" | grep -q "CREATED AGENTS.md"
test -f "$TARGET_ROOT/AGENTS.md"
test -f "$TARGET_ROOT/.ai/.gitkeep"
test -f "$TARGET_ROOT/.ai/state.json"
test -f "$TARGET_ROOT/scripts/ai_build.sh"
test -f "$TARGET_ROOT/scripts/ai_test.sh"
test -f "$TARGET_ROOT/scripts/ai_check.sh"

second_output=$(
  cd "$TARGET_ROOT"
  "$PYTHON_BIN" "$HARNESS_ROOT/bin/ai-init" small
)
echo "$second_output" | grep -q "SKIPPED AGENTS.md"

printf '%s\n' "user modified" > "$TARGET_ROOT/AGENTS.md"
force_output=$(
  cd "$TARGET_ROOT"
  "$PYTHON_BIN" "$HARNESS_ROOT/bin/ai-init" small --force
)
echo "$force_output" | grep -q "OVERWRITTEN AGENTS.md"

backup_file=$(find "$TARGET_ROOT/.ai/backups" -type f -path '*/AGENTS.md' | head -n 1)
test -n "$backup_file"
grep -q "user modified" "$backup_file"

status_output=$(
  cd "$TARGET_ROOT"
  "$PYTHON_BIN" "$HARNESS_ROOT/bin/ai-status"
)
echo "$status_output" | grep -q "initialized: yes"
echo "$status_output" | grep -q "status: INIT"
echo "$status_output" | grep -q "scripts/ai_check.sh: yes"
