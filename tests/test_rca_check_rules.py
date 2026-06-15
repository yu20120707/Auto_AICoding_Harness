from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class RcaCheckRulesIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([PYTHON, *args], cwd=tmpdir, capture_output=True, text=True, check=False)

    def test_reject_generates_rca_and_unenforced_rule_draft(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "spec")

            self.assertEqual(result.returncode, 0, result.stderr)
            rca_path = tmpdir / ".ai" / "tasks" / "init-large" / "rca.md"
            draft_path = tmpdir / "docs" / "ai" / "check-rules" / "drafts" / "init-large-spec.md"
            index_path = tmpdir / "docs" / "ai" / "check-rules" / "index.md"
            self.assertTrue(rca_path.exists())
            self.assertTrue(draft_path.exists())
            self.assertTrue(index_path.exists())
            self.assertIn("RCA Draft", rca_path.read_text(encoding="utf-8"))
            draft_text = draft_path.read_text(encoding="utf-8")
            self.assertIn("DRAFT_NOT_ENFORCED", draft_text)
            self.assertIn("must not be added", draft_text)
            index_text = index_path.read_text(encoding="utf-8")
            self.assertIn("not enforced automatically", index_text)
            self.assertNotIn("init-large-spec.md", index_text)


if __name__ == "__main__":
    unittest.main()
