from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiReviewSpecPlanFinalIntegrationTest(unittest.TestCase):
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

    def approve_spec(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec").returncode, 0)

    def approve_plan(self, tmpdir: Path) -> None:
        self.approve_spec(tmpdir)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan").returncode, 0)

    def approve_diff(self, tmpdir: Path) -> None:
        self.approve_plan(tmpdir)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)
        git_init = subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True, text=True, check=False)
        self.assertEqual(git_init.returncode, 0, git_init.stderr)
        git_add = subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True, text=True, check=False)
        self.assertEqual(git_add.returncode, 0, git_add.stderr)
        agents = tmpdir / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff").returncode, 0)

    def rewrite_state(self, tmpdir: Path, *, status: str, current_gate: str | None, approved_gates: list[str]) -> None:
        state_path = tmpdir / ".ai" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = status
        state["current_gate"] = current_gate
        state["approved_gates"] = approved_gates
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def test_review_spec_plan_final_fail_when_uninitialized(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            for gate in ["spec", "plan", "final"]:
                result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), gate)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(".ai/state.json", result.stderr)

    def test_spec_review_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec")
            self.assertEqual(result.returncode, 0, result.stderr)

            review_path = tmpdir / ".ai" / "reviews" / "spec-review.md"
            self.assertTrue(review_path.exists())
            self.assertIn("Spec Review", review_path.read_text(encoding="utf-8"))

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "WAITING_HUMAN_SPEC_APPROVAL")
            self.assertEqual(state["current_gate"], "spec")

    def test_plan_review_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            self.approve_spec(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan")
            self.assertEqual(result.returncode, 0, result.stderr)

            review_path = tmpdir / ".ai" / "reviews" / "plan-review.md"
            self.assertTrue(review_path.exists())
            self.assertIn("Plan Review", review_path.read_text(encoding="utf-8"))

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "WAITING_HUMAN_PLAN_APPROVAL")
            self.assertEqual(state["current_gate"], "plan")

    def test_final_review_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            self.approve_diff(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "final")
            self.assertEqual(result.returncode, 0, result.stderr)

            review_path = tmpdir / ".ai" / "reviews" / "final-review.md"
            self.assertTrue(review_path.exists())
            review_text = review_path.read_text(encoding="utf-8")
            self.assertIn("Final Review", review_text)
            self.assertIn(".ai/verification.md", review_text)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "WAITING_HUMAN_FINAL_APPROVAL")
            self.assertEqual(state["current_gate"], "final")

    def test_spec_review_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)

            review_path = tmpdir / ".ai" / "reviews" / "spec-review.md"
            review_path.write_text("user modified\n", encoding="utf-8")
            self.rewrite_state(tmpdir, status="INIT", current_gate=None, approved_gates=[])
            state_before = (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIPPED .ai/reviews/spec-review.md", result.stdout)
            self.assertEqual(review_path.read_text(encoding="utf-8"), "user modified\n")
            self.assertEqual(state_before, (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))

    def test_plan_review_force_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            self.approve_spec(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan").returncode, 0)

            review_path = tmpdir / ".ai" / "reviews" / "plan-review.md"
            review_path.write_text("user modified\n", encoding="utf-8")
            self.rewrite_state(tmpdir, status="SPEC_APPROVED", current_gate=None, approved_gates=["spec"])

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .ai/reviews/plan-review.md", result.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("plan-review.md"))
            self.assertTrue(backups, "expected plan review backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_status_shows_final_current_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            self.approve_diff(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "final").returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("status: WAITING_HUMAN_FINAL_APPROVAL", status.stdout)
            self.assertIn("current_gate: final", status.stdout)


if __name__ == "__main__":
    unittest.main()
