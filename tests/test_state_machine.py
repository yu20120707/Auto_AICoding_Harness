from __future__ import annotations

import unittest

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.state import default_state
from core.state_machine import (
    assert_review_allowed,
    assert_valid_state,
    assert_waiting_gate_for_decision,
)


class StateMachineTest(unittest.TestCase):
    def test_default_state_is_valid(self) -> None:
        state = default_state("cpp-linux-backend-system")
        assert_valid_state(state)

    def test_waiting_status_requires_matching_gate(self) -> None:
        state = default_state("cpp-linux-backend-system")
        state["status"] = "WAITING_HUMAN_PLAN_APPROVAL"
        state["current_gate"] = "spec"

        with self.assertRaisesRegex(RuntimeError, "requires current_gate=plan"):
            assert_valid_state(state)

    def test_large_plan_review_requires_spec_approval(self) -> None:
        state = default_state("cpp-linux-backend-system")
        state["mode"] = "large"

        with self.assertRaisesRegex(RuntimeError, "spec approval first"):
            assert_review_allowed(state, "plan")

    def test_large_diff_review_requires_plan_approval(self) -> None:
        state = default_state("cpp-linux-backend-system")
        state["mode"] = "large"
        state["status"] = "SPEC_APPROVED"
        state["approved_gates"] = ["spec"]

        with self.assertRaisesRegex(RuntimeError, "plan approval first"):
            assert_review_allowed(state, "diff")

    def test_large_final_review_requires_diff_approval(self) -> None:
        state = default_state("cpp-linux-backend-system")
        state["mode"] = "large"
        state["status"] = "PLAN_APPROVED"
        state["approved_gates"] = ["spec", "plan"]

        with self.assertRaisesRegex(RuntimeError, "diff approval first"):
            assert_review_allowed(state, "final")

    def test_waiting_gate_decision_requires_matching_state(self) -> None:
        state = default_state("cpp-linux-backend-system")
        state["status"] = "WAITING_HUMAN_DIFF_APPROVAL"
        state["current_gate"] = "diff"
        assert_waiting_gate_for_decision(state, "diff", action="approval")

        with self.assertRaisesRegex(RuntimeError, "current status does not allow plan approval"):
            assert_waiting_gate_for_decision(state, "plan", action="approval")

    def test_medium_review_path_is_not_forced_into_large_gate_chain(self) -> None:
        state = default_state("cpp-linux-backend-system", mode="medium")
        assert_review_allowed(state, "plan")
        assert_review_allowed(state, "diff")
        assert_review_allowed(state, "final")


if __name__ == "__main__":
    unittest.main()
