from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiReviewDiffIntegrationTest(unittest.TestCase):
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

    def test_review_fails_when_uninitialized(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(".ai/state.json", result.stderr)

    def test_review_fails_when_not_git_repo(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(init.returncode, 0, init.stderr)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("git", result.stderr.lower())

    def test_review_fails_when_no_diff(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no git diff", result.stderr.lower())

    def test_review_generates_diff_material_and_updates_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)

            agents = tmpdir / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")
            self.assertEqual(result.returncode, 0, result.stderr)

            review_path = tmpdir / ".ai" / "reviews" / "diff-review.md"
            self.assertTrue(review_path.exists())
            review_text = review_path.read_text(encoding="utf-8")
            self.assertIn("## Git Status", review_text)
            self.assertIn("## Diff Stat", review_text)
            self.assertIn("## Changed Files", review_text)
            self.assertIn("## Human Decision", review_text)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "WAITING_HUMAN_DIFF_APPROVAL")
            self.assertEqual(state["current_gate"], "diff")

    def test_repeat_review_skips_without_force(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)

            agents = tmpdir / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff").returncode, 0)

            review_path = tmpdir / ".ai" / "reviews" / "diff-review.md"
            review_path.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIPPED .ai/reviews/diff-review.md", result.stdout)
            self.assertIn("state unchanged", result.stdout)
            self.assertEqual(review_path.read_text(encoding="utf-8"), "user modified\n")

    def test_force_review_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)

            agents = tmpdir / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff").returncode, 0)

            review_path = tmpdir / ".ai" / "reviews" / "diff-review.md"
            review_path.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .ai/reviews/diff-review.md", result.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("diff-review.md"))
            self.assertTrue(backups, "expected diff-review backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_status_shows_current_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)

            agents = tmpdir / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal change\n", encoding="utf-8")
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff").returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("status: WAITING_HUMAN_DIFF_APPROVAL", status.stdout)
            self.assertIn("current_gate: diff", status.stdout)


if __name__ == "__main__":
    unittest.main()
