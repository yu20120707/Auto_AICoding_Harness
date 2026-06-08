#!/usr/bin/env sh
set -eu

cat <<'EOF'
Placeholder: replace scripts/ai_check.sh with this project's real verification sequence.

Recommended order:
1. build
2. test
3. optional lint or static analysis

Keep this script safe:
- Do not install dependencies.
- Do not modify business source code.
- Do not run destructive cleanup commands.

Example shape only, not a default:
  ./scripts/ai_build.sh
  ./scripts/ai_test.sh
  # optional: clang-tidy, cppcheck, formatting check
EOF
