from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiUpgradeLargeIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_upgrade_fails_when_uninitialized(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not initialized", result.stderr)
            self.assertFalse((tmpdir / ".ai" / "epic.md").exists())

    def test_small_to_large_upgrade_succeeds(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(init.returncode, 0, init.stderr)

            upgrade = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")
            self.assertEqual(upgrade.returncode, 0, upgrade.stderr)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "large")
            for path in [
                ".ai/epic.md",
                ".ai/implementation-plan.md",
                ".ai/run-trace.md",
                ".ai/reviews",
                ".ai/approvals",
                ".ai/subagent-packets/README.md",
                ".ai/subagent-packets/planner.md",
                ".ai/subagent-packets/reviewer.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_second_upgrade_reports_already_large(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            state_before = (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8")
            second = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("ALREADY_LARGE", second.stdout)
            state_after = (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8")
            self.assertEqual(state_before, state_after)

    def test_force_upgrade_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            epic_path = tmpdir / ".ai" / "epic.md"
            epic_path.write_text("user modified\n", encoding="utf-8")

            forced = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large", "--force")
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertIn("OVERWRITTEN .ai/epic.md", forced.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("epic.md"))
            self.assertTrue(backups, "expected epic backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))
            self.assertIn("# Epic", epic_path.read_text(encoding="utf-8"))

    def test_ai_status_shows_large_mode(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("initialized: yes", status.stdout)
            self.assertIn("mode: large", status.stdout)
            self.assertIn("status: INIT", status.stdout)
            self.assertIn("large files: present", status.stdout)
            self.assertIn("reviews dir: present", status.stdout)
            self.assertIn("approvals dir: present", status.stdout)


if __name__ == "__main__":
    unittest.main()
