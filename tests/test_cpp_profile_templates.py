from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class CppProfileTemplatesIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_ai_init_small_generates_cpp_profile_docs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(result.returncode, 0, result.stderr)

            for path in [
                "docs/ai/cpp-system.md",
                "docs/ai/linux-debug.md",
                "docs/ai/network.md",
                "docs/ai/concurrency.md",
                "docs/ai/api-abi.md",
                "docs/ai/performance.md",
                "docs/ai/observability.md",
                "docs/ai/cmake.md",
                "docs/ai/build.md",
                "docs/ai/testing.md",
                "docs/ai/verification-matrix.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_generated_profile_docs_contain_key_terms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)

            self.assertIn("RAII", (tmpdir / "docs/ai/cpp-system.md").read_text(encoding="utf-8"))
            self.assertIn("EAGAIN", (tmpdir / "docs/ai/network.md").read_text(encoding="utf-8"))
            self.assertIn("atomic", (tmpdir / "docs/ai/concurrency.md").read_text(encoding="utf-8"))
            self.assertIn("ABI", (tmpdir / "docs/ai/api-abi.md").read_text(encoding="utf-8"))
            self.assertIn("baseline", (tmpdir / "docs/ai/performance.md").read_text(encoding="utf-8"))
            self.assertIn("metrics", (tmpdir / "docs/ai/observability.md").read_text(encoding="utf-8"))
            self.assertIn("target_link_libraries", (tmpdir / "docs/ai/cmake.md").read_text(encoding="utf-8"))
            self.assertIn("compile_commands", (tmpdir / "docs/ai/build.md").read_text(encoding="utf-8"))

            testing_text = (tmpdir / "docs/ai/testing.md").read_text(encoding="utf-8")
            self.assertTrue("GTest" in testing_text or "CTest" in testing_text)
            matrix_text = (tmpdir / "docs/ai/verification-matrix.md").read_text(encoding="utf-8")
            self.assertIn("Risk Trigger", matrix_text)
            self.assertIn("scripts/ai_check.sh", matrix_text)

    def test_scripts_are_safe_placeholders(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)

            for path in [
                "scripts/ai_build.sh",
                "scripts/ai_test.sh",
                "scripts/ai_check.sh",
            ]:
                content = (tmpdir / path).read_text(encoding="utf-8")
                lowered = content.lower()
                self.assertTrue(
                    "placeholder" in lowered or "todo" in lowered or "replace" in lowered,
                    path,
                )
                self.assertNotIn("rm -rf /", content)
                self.assertNotIn("curl | sh", content)
                self.assertNotIn("sudo apt install", content)

    def test_readme_and_current_capabilities_are_updated(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        capabilities = (REPO_ROOT / "docs/design/current-capabilities.md").read_text(encoding="utf-8")
        combined = readme + "\n" + capabilities

        self.assertIn("v1.7-optimization-hardening", combined)
        self.assertIn("cpp-linux-backend-system", combined)
        self.assertIn("ai-install-skills", combined)
        self.assertIn("verification matrix", combined.lower())


if __name__ == "__main__":
    unittest.main()
