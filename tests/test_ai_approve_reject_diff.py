from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiApproveRejectDiffIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_git(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def write_waiting_state_fixture(self, tmpdir: Path) -> None:
        state_path = tmpdir / ".ai" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "WAITING_HUMAN_DIFF_APPROVAL"
        state["current_gate"] = "diff"
        state["approved_gates"] = [gate for gate in state.get("approved_gates", []) if gate != "diff"]
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def prepare_waiting_diff_gate(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)
        agents = tmpdir / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
        review = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")
        self.assertEqual(review.returncode, 0, review.stderr)

    def test_uninitialized_approve_reject_fail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            approve = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff")
            reject = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "diff")

            self.assertNotEqual(approve.returncode, 0)
            self.assertNotEqual(reject.returncode, 0)
            self.assertIn(".ai/state.json", approve.stderr)
            self.assertIn(".ai/state.json", reject.stderr)

    def test_approve_reject_fail_when_not_waiting_diff_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(init.returncode, 0, init.stderr)

            approve = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff")
            reject = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "diff")

            self.assertNotEqual(approve.returncode, 0)
            self.assertNotEqual(reject.returncode, 0)
            self.assertFalse((tmpdir / ".ai" / "approvals" / "diff-approval.md").exists())
            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertNotEqual(state["status"], "DIFF_APPROVED")
            self.assertNotEqual(state["status"], "NEEDS_FIX")

    def test_approve_diff_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_diff_gate(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff")
            self.assertEqual(result.returncode, 0, result.stderr)

            approval_path = tmpdir / ".ai" / "approvals" / "diff-approval.md"
            self.assertTrue(approval_path.exists())
            self.assertIn("APPROVED", approval_path.read_text(encoding="utf-8"))

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "DIFF_APPROVED")
            self.assertIsNone(state["current_gate"])
            self.assertIn("diff", state.get("approved_gates", []))

    def test_reject_diff_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_diff_gate(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "diff")
            self.assertEqual(result.returncode, 0, result.stderr)

            approval_path = tmpdir / ".ai" / "approvals" / "diff-approval.md"
            self.assertTrue(approval_path.exists())
            self.assertIn("REJECTED", approval_path.read_text(encoding="utf-8"))

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "NEEDS_FIX")
            self.assertIsNone(state["current_gate"])
            self.assertNotIn("diff", state.get("approved_gates", []))

    def test_approval_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_diff_gate(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff").returncode, 0)

            approval_path = tmpdir / ".ai" / "approvals" / "diff-approval.md"
            approval_path.write_text("user modified\n", encoding="utf-8")
            self.write_waiting_state_fixture(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIPPED .ai/approvals/diff-approval.md", result.stdout)
            self.assertIn("state unchanged", result.stdout)
            self.assertEqual(approval_path.read_text(encoding="utf-8"), "user modified\n")

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "WAITING_HUMAN_DIFF_APPROVAL")
            self.assertEqual(state["current_gate"], "diff")

    def test_force_approval_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_diff_gate(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff").returncode, 0)

            approval_path = tmpdir / ".ai" / "approvals" / "diff-approval.md"
            approval_path.write_text("user modified\n", encoding="utf-8")
            self.write_waiting_state_fixture(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .ai/approvals/diff-approval.md", result.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("diff-approval.md"))
            self.assertTrue(backups, "expected diff-approval backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_status_shows_approve_reject_results(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_diff_gate(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff").returncode, 0)

            approve_status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(approve_status.returncode, 0, approve_status.stderr)
            self.assertIn("status: DIFF_APPROVED", approve_status.stdout)
            self.assertIn("current_gate: none", approve_status.stdout)

        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_waiting_diff_gate(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "diff").returncode, 0)

            reject_status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(reject_status.returncode, 0, reject_status.stderr)
            self.assertIn("status: NEEDS_FIX", reject_status.stdout)
            self.assertIn("current_gate: none", reject_status.stdout)


if __name__ == "__main__":
    unittest.main()
