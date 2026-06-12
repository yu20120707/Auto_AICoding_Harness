from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.profile import load_profile


class ProfileLoadingTest(unittest.TestCase):
    def test_cpp_profile_manifest_loads(self) -> None:
        manifest = load_profile(REPO_ROOT, "cpp-linux-backend-system")
        self.assertEqual(manifest.name, "cpp-linux-backend-system")
        self.assertEqual(manifest.display_name, "C++ Linux Backend System")
        self.assertIn("cpp", manifest.languages)
        self.assertIn("network_io_change", manifest.risk_triggers)
        self.assertEqual(manifest.verification["build"], "project_defined")

    def test_missing_profile_manifest_fails(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "missing profile manifest"):
            load_profile(REPO_ROOT, "does-not-exist")


class ProfileValidationIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_ai_init_rejects_unknown_profile(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(
                tmpdir,
                str(REPO_ROOT / "bin" / "ai-init"),
                "small",
                "--profile",
                "does-not-exist",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing profile manifest", result.stderr)


if __name__ == "__main__":
    unittest.main()
