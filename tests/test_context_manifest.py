from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.context_manifest import (  # noqa: E402
    ContextManifestEntry,
    render_context_manifest,
    validate_context_manifest_payload,
)


class ContextManifestUnitTest(unittest.TestCase):
    def test_render_manifest_is_jsonl_without_source_text(self) -> None:
        rendered = render_context_manifest(
            [ContextManifestEntry(".ai/spec.md", "Large-mode requirement source", "implement")]
        )

        lines = rendered.splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["path"], ".ai/spec.md")
        self.assertNotIn("# Spec", rendered)

    def test_disallows_raw_source_references_by_default(self) -> None:
        errors = validate_context_manifest_payload(
            {"path": "src/main.cpp", "reason": "raw source", "phase": "implement"}
        )

        self.assertIn("path is disallowed by default: src/main.cpp", errors)
        self.assertIn("path is outside allowed context manifest scope: src/main.cpp", errors)


class ContextManifestIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_large_context_pack_generates_and_consumes_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack"), "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(".ai/tasks/init-large/context.jsonl", result.stdout)
            manifest_path = tmpdir / ".ai" / "tasks" / "init-large" / "context.jsonl"
            self.assertTrue(manifest_path.exists())
            manifest_text = manifest_path.read_text(encoding="utf-8")
            self.assertIn('"path": ".ai/spec.md"', manifest_text)
            self.assertNotIn("# Spec", manifest_text)

            context_text = (tmpdir / ".ai" / "context-pack.md").read_text(encoding="utf-8")
            self.assertIn("## Context Manifest", context_text)
            self.assertIn("context manifest valid: yes", context_text)
            self.assertIn(".ai/spec.md [implement]", context_text)

    def test_small_context_pack_does_not_generate_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack"), "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("context.jsonl", result.stdout)
            self.assertFalse((tmpdir / ".ai" / "tasks").exists())
            context_text = (tmpdir / ".ai" / "context-pack.md").read_text(encoding="utf-8")
            self.assertNotIn("## Context Manifest", context_text)


if __name__ == "__main__":
    unittest.main()
