from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiUpgradeMediumIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_small_to_medium_upgrade_succeeds(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)

            upgrade = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "medium")
            self.assertEqual(upgrade.returncode, 0, upgrade.stderr)
            self.assertIn("[OK] Current mode is now medium", upgrade.stdout)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "medium")
            for path in [
                ".ai/implementation-plan.md",
                ".ai/run-trace.md",
                ".ai/verification.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_medium_to_large_upgrade_succeeds(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium").returncode, 0)

            upgrade = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")
            self.assertEqual(upgrade.returncode, 0, upgrade.stderr)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "large")
            self.assertTrue((tmpdir / ".ai" / "epic.md").exists())

    def test_second_upgrade_reports_already_medium(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "medium").returncode, 0)

            second = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "medium")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("ALREADY_MEDIUM", second.stdout)


if __name__ == "__main__":
    unittest.main()
