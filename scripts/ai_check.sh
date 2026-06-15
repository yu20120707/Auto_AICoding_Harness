#!/usr/bin/env bash
set -euo pipefail

py -m compileall bin core
py tests/test_ai_state.py
py tests/test_ai_doctor.py
py tests/test_ai_upgrade_large.py
py tests/test_ai_review_spec_plan_final.py
py tests/test_ai_approve_reject_all_gates.py
py tests/test_ai_context_handoff.py
