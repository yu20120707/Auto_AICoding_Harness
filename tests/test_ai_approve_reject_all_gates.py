from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiApproveRejectAllGatesIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def prepare_large(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

    def load_state(self, tmpdir: Path) -> dict:
        return json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))

    def set_waiting_state(self, tmpdir: Path, *, gate: str, status: str) -> None:
        state_path = tmpdir / ".ai" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = status
        state["current_gate"] = gate
        state["approved_gates"] = [existing_gate for existing_gate in state.get("approved_gates", []) if existing_gate != gate]
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def prepare_waiting_gate(self, tmpdir: Path, gate: str) -> None:
        self.prepare_large(tmpdir)
        if gate in {"plan", "diff", "final"}:
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec").returncode, 0)
        if gate in {"diff", "final"}:
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan").returncode, 0)
        if gate == "final":
            self.assertEqual(subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True, text=True, check=False).returncode, 0)
            self.assertEqual(subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True, text=True, check=False).returncode, 0)
            agents = tmpdir / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal final flow\n", encoding="utf-8")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff").returncode, 0)
            (tmpdir / ".ai" / "verification.md").write_text(
                "# Verification\n\n## Ran\n\n- command: py tests/test_ai_init_small.py\n- result: passed\n- notes: smoke\n\n## Not Run\n\n- item:\n- reason:\n- required follow-up:\n",
                encoding="utf-8",
            )
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)
        review = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), gate)
        self.assertEqual(review.returncode, 0, review.stderr)

    def test_spec_approve_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "spec")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((tmpdir / ".ai" / "approvals" / "spec-approval.md").exists())

            state = self.load_state(tmpdir)
            self.assertEqual(state["status"], "SPEC_APPROVED")
            self.assertIsNone(state["current_gate"])
            self.assertIn("spec", state.get("approved_gates", []))

    def test_spec_reject_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "spec")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "spec")
            self.assertEqual(result.returncode, 0, result.stderr)
            approval_text = (tmpdir / ".ai" / "approvals" / "spec-approval.md").read_text(encoding="utf-8")
            self.assertIn("REJECTED", approval_text)

            state = self.load_state(tmpdir)
            self.assertEqual(state["status"], "NEEDS_REPLAN")
            self.assertIsNone(state["current_gate"])
            self.assertNotIn("spec", state.get("approved_gates", []))

    def test_plan_approve_and_reject_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "plan")
            approve = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan")
            self.assertEqual(approve.returncode, 0, approve.stderr)
            self.assertEqual(self.load_state(tmpdir)["status"], "PLAN_APPROVED")

        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "plan")
            reject = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "plan")
            self.assertEqual(reject.returncode, 0, reject.stderr)
            self.assertEqual(self.load_state(tmpdir)["status"], "NEEDS_REPLAN")

    def test_final_approve_and_reject_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "final")
            approve = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "final")
            self.assertEqual(approve.returncode, 0, approve.stderr)
            self.assertEqual(self.load_state(tmpdir)["status"], "DONE")

        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "final")
            reject = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "final")
            self.assertEqual(reject.returncode, 0, reject.stderr)
            self.assertEqual(self.load_state(tmpdir)["status"], "NEEDS_MORE_TESTS")

    def test_gate_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "spec")
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotEqual(self.load_state(tmpdir)["status"], "PLAN_APPROVED")

    def test_final_approval_requires_meaningful_verification(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "final")
            verification_path = tmpdir / ".ai" / "verification.md"
            verification_path.write_text(
                "# Verification\n\n## Ran\n\n- command:\n- result:\n- notes:\n\n## Not Run\n\n- item:\n- reason:\n- required follow-up:\n",
                encoding="utf-8",
            )

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "final")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(".ai/verification.md", result.stderr)
            self.assertEqual(self.load_state(tmpdir)["status"], "WAITING_HUMAN_FINAL_APPROVAL")

    def test_missing_review_file_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "spec")
            review_path = tmpdir / ".ai" / "reviews" / "spec-review.md"
            review_path.unlink()
            state_before = (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(state_before, (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))

    def test_approval_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "spec")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec").returncode, 0)

            approval_path = tmpdir / ".ai" / "approvals" / "spec-approval.md"
            approval_path.write_text("user modified\n", encoding="utf-8")
            self.set_waiting_state(tmpdir, gate="spec", status="WAITING_HUMAN_SPEC_APPROVAL")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIPPED .ai/approvals/spec-approval.md", result.stdout)
            self.assertEqual(approval_path.read_text(encoding="utf-8"), "user modified\n")
            state = self.load_state(tmpdir)
            self.assertEqual(state["status"], "WAITING_HUMAN_SPEC_APPROVAL")
            self.assertEqual(state["current_gate"], "spec")

    def test_force_approval_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "plan")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan").returncode, 0)

            approval_path = tmpdir / ".ai" / "approvals" / "plan-approval.md"
            approval_path.write_text("user modified\n", encoding="utf-8")
            self.set_waiting_state(tmpdir, gate="plan", status="WAITING_HUMAN_PLAN_APPROVAL")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .ai/approvals/plan-approval.md", result.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("plan-approval.md"))
            self.assertTrue(backups, "expected plan approval backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_status_shows_final_result(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_gate(tmpdir, "final")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "final").returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("status: DONE", status.stdout)
            self.assertIn("current_gate: none", status.stdout)


if __name__ == "__main__":
    unittest.main()
