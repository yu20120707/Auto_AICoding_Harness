from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiContextHandoffIntegrationTest(unittest.TestCase):
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

    def prepare_diff_waiting_gate(self, tmpdir: Path, *, large: bool = False) -> None:
        self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        if large:
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
        self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)
        agents = tmpdir / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
        review = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")
        self.assertEqual(review.returncode, 0, review.stderr)

    def test_uninitialized_context_pack_handoff_fail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            context_pack = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack"))
            handoff = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff"))

            self.assertNotEqual(context_pack.returncode, 0)
            self.assertNotEqual(handoff.returncode, 0)
            self.assertIn(".ai/state.json", context_pack.stderr)
            self.assertIn(".ai/state.json", handoff.stderr)

    def test_small_init_generates_context_pack_and_handoff_without_state_change(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(init.returncode, 0, init.stderr)
            before = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))

            context_pack = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack"))
            handoff = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff"))
            self.assertEqual(context_pack.returncode, 0, context_pack.stderr)
            self.assertEqual(handoff.returncode, 0, handoff.stderr)

            context_text = (tmpdir / ".ai" / "context-pack.md").read_text(encoding="utf-8")
            handoff_text = (tmpdir / ".ai" / "handoff.md").read_text(encoding="utf-8")
            self.assertIn("- status: INIT", context_text)
            self.assertIn("- status: INIT", handoff_text)

            after = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(before, after)

    def test_large_and_diff_review_generate_context_pack_and_handoff(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_diff_waiting_gate(tmpdir, large=True)

            context_pack = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack"), "--force")
            handoff = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff"), "--force")
            self.assertEqual(context_pack.returncode, 0, context_pack.stderr)
            self.assertEqual(handoff.returncode, 0, handoff.stderr)

            context_text = (tmpdir / ".ai" / "context-pack.md").read_text(encoding="utf-8")
            handoff_text = (tmpdir / ".ai" / "handoff.md").read_text(encoding="utf-8")
            self.assertIn("WAITING_HUMAN_DIFF_APPROVAL", context_text)
            self.assertIn("current_gate: diff", handoff_text)
            self.assertIn(".ai/reviews/diff-review.md", context_text)

    def test_approve_then_handoff_mentions_approval(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_diff_waiting_gate(tmpdir)
            approve = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff")
            self.assertEqual(approve.returncode, 0, approve.stderr)

            handoff = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff"), "--force")
            self.assertEqual(handoff.returncode, 0, handoff.stderr)
            handoff_text = (tmpdir / ".ai" / "handoff.md").read_text(encoding="utf-8")
            self.assertIn("DIFF_APPROVED", handoff_text)
            self.assertIn(".ai/approvals/diff-approval.md", handoff_text)

    def test_reject_then_handoff_mentions_fix_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_diff_waiting_gate(tmpdir)
            reject = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "diff")
            self.assertEqual(reject.returncode, 0, reject.stderr)

            handoff = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff"), "--force")
            self.assertEqual(handoff.returncode, 0, handoff.stderr)
            handoff_text = (tmpdir / ".ai" / "handoff.md").read_text(encoding="utf-8")
            self.assertIn("NEEDS_FIX", handoff_text)
            self.assertIn("Fix issues and rerun `ai-review diff`.", handoff_text)

    def test_context_pack_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)

            path = tmpdir / ".ai" / "context-pack.md"
            path.write_text("user modified\n", encoding="utf-8")
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack"))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIPPED .ai/context-pack.md", result.stdout)
            self.assertEqual(path.read_text(encoding="utf-8"), "user modified\n")

    def test_handoff_force_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)

            path = tmpdir / ".ai" / "handoff.md"
            path.write_text("user modified\n", encoding="utf-8")
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff"), "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .ai/handoff.md", result.stdout)
            backups = list((tmpdir / ".ai" / "backups").rglob("handoff.md"))
            self.assertTrue(backups, "expected handoff backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_status_shows_context_pack_and_handoff(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("context_pack: yes", status.stdout)
            self.assertIn("handoff: yes", status.stdout)


if __name__ == "__main__":
    unittest.main()
