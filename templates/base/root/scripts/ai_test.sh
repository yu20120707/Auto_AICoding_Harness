#!/usr/bin/env sh
set -eu

cat <<'EOF'
Placeholder: replace scripts/ai_test.sh with this project's real test commands.

Guidance:
- Run unit tests first, then integration or system tests as appropriate.
- Keep failure output visible.
- Do not delete failing tests to make the run pass.
- If tests cannot run, document the reason in the task artifacts.
- Do not install dependencies here.
- Do not modify business source code here.

Example shape only, not a default:
  ctest --test-dir build --output-on-failure
  ./build/tests/my_service_tests
EOF
